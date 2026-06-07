import os
from typing import List, Dict, Any
from datetime import datetime

from backend.database import SessionLocal
from backend.models.ai import AIInterpretation
from backend.config.settings import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

def generate_interpretation(
    job_id: str,
    organism_name: str,
    annotations: List[Dict[str, Any]],
    domains: List[Dict[str, Any]],
    pathways: List[Dict[str, Any]],
    articles: List[Dict[str, Any]],
    log_logger
) -> Dict[str, Any]:
    """
    Orchestrates the AI pathobiology interpretation using Gemini or OpenAI APIs.
    Falls back to a structured rule-based offline summary if no API keys are configured.
    
    Parameters:
    -----------
    job_id : str
        The unique UUID identifier of the active pipeline job.
    organism_name : str
        Target scientific taxon name.
    annotations : list of dict
        SwissProt homologous alignment results.
    domains : list of dict
        Pfam domain signature hits.
    pathways : list of dict
        KEGG biochemical pathway maps.
    articles : list of dict
        PubMed abstracts literature evidence.
    log_logger : Logger
        Active job logger.
        
    Returns:
    --------
    interpretation : dict
        Parsed components of the pathobiology summary.
    """
    log_logger.info("Starting AI pathobiology interpretation module.")
    
    # Check for empty findings
    if not annotations and not domains and not pathways:
        log_logger.warning("No genomic annotations found. Emitting insufficient evidence response.")
        return _save_offline_fallback(
            job_id,
            organism_name,
            "Insufficient evidence for interpretation (no genomic annotations found).",
            "LOW",
            "Analysis aborted due to lack of homology or domain hits."
        )

    # 1. Format input details for prompt context
    annot_str = "\n".join([f"- Query {h['query_protein']} matched {h['subject_protein']} (Identity: {h['identity_percent']}%, E-value: {h['evalue']})" for h in annotations[:5]])
    dom_str = "\n".join([f"- Domain {d['pfam_name']} ({d['pfam_accession']}) in protein {d['protein_id']} (E-value: {d['evalue']})" for d in domains[:5]])
    path_str = "\n".join([f"- Mapped to KEGG pathway: {p['pathway_name']} (FDR: {p['fdr']})" for p in pathways[:5]])
    lit_str = "\n".join([f"- PMID: {a['pmid']} Title: {a['title']} Abstract: {a['abstract'][:200]}..." for a in articles[:3]])

    prompt = f"""
Pathogen Target Organism: {organism_name}

Identified Homologous Alignments:
{annot_str}

Identified Protein Domains:
{dom_str}

Mapped Biological Pathways:
{path_str}

Retrieved Scientific Publications:
{lit_str}
"""

    system_instruction = """
You are an expert pathogen pathobiology AI interpreter.
Generate a structured, evidence-cited pathobiology interpretation based strictly on the query context.
You must follow these rules:
1. Every claim must cite the specific subject protein or PMID number supporting it.
2. If there are no active annotations, output: "Insufficient evidence for interpretation". Do not hallucinate clinical symptoms or replication mechanisms.
3. Your response must consist exactly of these 5 sections, formatted as markdown headers:
   - ### Findings: [Summary of proteins, pathways, and taxons identified. Explicitly highlight "Why this gene is significant" for the top annotated genes.]
   - ### Evidence: [Citations of alignment scores and PMIDs]
   - ### Interpretation: [Detailed pathology explanation. Explicitly analyze "Why this pathway is activated" based on the matched genomic markers, and detail any "Therapeutic implications" or target options.]
   - ### Confidence: [HIGH / MEDIUM / LOW with reason]
   - ### Limitations: [Analysis bottlenecks and lack of wet-lab validation]
"""

    # 2. Select API route — try OpenAI first (primary), then Gemini as secondary
    # Reason: OpenAI key is valid; Gemini key may not be available
    if settings.is_openai_available:
        log_logger.info("Invoking OpenAI GPT API...")
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.openai_api_key)
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=2000
                )
            except Exception as quota_err:
                if "quota" in str(quota_err).lower() or "rate" in str(quota_err).lower():
                    log_logger.warning(f"GPT-4o quota/rate error: {quota_err}. Trying gpt-3.5-turbo fallback.")
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.2,
                        max_tokens=2000
                    )
                else:
                    raise
            text = response.choices[0].message.content
            parsed = _parse_markdown_response(text, "openai", response.model)
            _commit_ai_result(job_id, parsed)
            return parsed
        except Exception as openai_err:
            log_logger.error(f"OpenAI API request failed: {str(openai_err)}. Attempting Gemini failover.")

    if settings.is_gemini_available:
        log_logger.info("Invoking Google Gemini API...")
        import time
        # Try multiple Gemini models in order of preference
        gemini_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        last_gemini_err = None
        
        for model_name in gemini_models:
            for attempt in range(2):  # 2 attempts per model
                try:
                    from google import genai
                    client = genai.Client(api_key=settings.gemini_api_key)
                    log_logger.info(f"Trying Gemini model: {model_name} (attempt {attempt + 1})")
                    response = client.models.generate_content(
                        model=model_name,
                        contents=[system_instruction + "\n\n" + prompt]
                    )
                    parsed = _parse_markdown_response(response.text, "gemini", model_name)
                    _commit_ai_result(job_id, parsed)
                    log_logger.info(f"Gemini {model_name} succeeded.")
                    return parsed
                except Exception as gemini_err:
                    last_gemini_err = gemini_err
                    err_str = str(gemini_err)
                    log_logger.warning(f"Gemini {model_name} attempt {attempt + 1} failed: {err_str[:200]}")
                    # If it's a 503/overloaded error, wait and retry
                    if "503" in err_str or "UNAVAILABLE" in err_str or "overloaded" in err_str.lower():
                        time.sleep(3)
                        continue
                    # If it's a different error (e.g. model not found), skip to next model
                    break
        
        if last_gemini_err:
            log_logger.error(f"All Gemini models failed. Last error: {str(last_gemini_err)[:300]}")

    # 3. OpenRouter fallback (uses raw HTTP to avoid OpenAI SDK version issues)
    if settings.is_openrouter_available:
        log_logger.info("Invoking OpenRouter API as final LLM fallback...")
        import time
        import requests as _requests
        
        openrouter_models = [
            "deepseek/deepseek-r1-0528",
            "deepseek/deepseek-v3.2",
            "nvidia/nemotron-3-super-120b-a12b:free",
            "openrouter/free",
        ]
        last_or_err = None
        
        for or_model in openrouter_models:
            try:
                log_logger.info(f"Trying OpenRouter model: {or_model}")
                # Build JSON request payload
                payload = {
                    "model": or_model,
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 2000
                }
                # Enable reasoning for models that support it
                if "deepseek-r1" in or_model or "deepseek-v3" in or_model or "nemotron" in or_model or "free" in or_model:
                    payload["reasoning"] = {"enabled": True}
                
                or_resp = _requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.openrouter_api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://pathoscope-genomics.ai",
                        "X-Title": "PathoScope AI Pipeline"
                    },
                    json=payload,
                    timeout=60
                )
                or_resp.raise_for_status()
                or_data = or_resp.json()
                message = or_data.get("choices", [{}])[0].get("message", {})
                text = message.get("content", "")
                
                # Extract thinking/reasoning details if available
                reasoning = message.get("reasoning") or ""
                reasoning_details = message.get("reasoning_details")
                if reasoning_details and isinstance(reasoning_details, list):
                    reasoning_list = []
                    for rd in reasoning_details:
                        if isinstance(rd, dict) and rd.get("text"):
                            reasoning_list.append(rd["text"])
                    if reasoning_list:
                        reasoning = "\n".join(reasoning_list)
                
                if text and len(text.strip()) > 50:
                    parsed = _parse_markdown_response(text, "openrouter", or_model)
                    if reasoning:
                        parsed["limitations"] = parsed["limitations"] + f"\n\n### AI Thinking Process:\n{reasoning.strip()}"
                    _commit_ai_result(job_id, parsed)
                    log_logger.info(f"OpenRouter {or_model} succeeded.")
                    return parsed
                else:
                    log_logger.warning(f"OpenRouter {or_model} returned empty/short response, trying next model.")
                    continue
            except Exception as or_err:
                last_or_err = or_err
                err_str = str(or_err)
                log_logger.warning(f"OpenRouter {or_model} failed: {err_str[:200]}")
                time.sleep(1)
                continue
        
        if last_or_err:
            log_logger.error(f"All OpenRouter models failed. Last error: {str(last_or_err)[:300]}")

    # 4. Final Fallback: Offline Rule-Based Summary
    log_logger.warning("All LLM providers failed (OpenAI/Gemini/OpenRouter). Running offline rule-based interpretation.")
    findings = f"Identified {len(annotations)} SwissProt annotations, {len(domains)} Pfam domain signatures, and {len(pathways)} biochemical pathways for organism '{organism_name}'."
    evidence = f"Aligned queries to SwissProt targets (e.g. {annotations[0]['subject_protein'] if annotations else 'None'}) and Pfam entries ({domains[0]['pfam_name'] if domains else 'None'}). Literature supported by PMIDs: {', '.join([a['pmid'] for a in articles])}."
    
    interpretation = f"PathoScope offline diagnostic completed. Mapped species is {organism_name}. Detailed pathobiology review requires active Gemini or OpenAI API keys in .env."
    confidence = "MEDIUM" if articles else "LOW"
    limitations = "All LLM API providers failed (OpenAI quota exceeded, Gemini unavailable, OpenRouter unreachable). Running under offline fallback mode. Results lack synthesis."

    parsed = {
        "ai_provider": "offline",
        "model_name": "offline-fallback",
        "findings": findings,
        "literature_summary": evidence,
        "biological_interpretation": interpretation,
        "confidence_assessment": confidence,
        "limitations": limitations
    }
    _commit_ai_result(job_id, parsed)
    return parsed

def _parse_markdown_response(text: str, provider: str, model: str) -> Dict[str, Any]:
    """
    Helper to extract markdown headers into separate fields.
    """
    sections = {
        "findings": "",
        "literature_summary": "",
        "biological_interpretation": "",
        "confidence_assessment": "MEDIUM",
        "limitations": ""
    }
    
    current_key = None
    lines = text.split("\n")
    accumulated = []
    
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith("### Findings"):
            if current_key: sections[current_key] = "\n".join(accumulated).strip()
            current_key = "findings"
            accumulated = [line_strip.replace("### Findings:", "").replace("### Findings", "").strip()]
        elif line_strip.startswith("### Evidence"):
            if current_key: sections[current_key] = "\n".join(accumulated).strip()
            current_key = "literature_summary"
            accumulated = [line_strip.replace("### Evidence:", "").replace("### Evidence", "").strip()]
        elif line_strip.startswith("### Interpretation"):
            if current_key: sections[current_key] = "\n".join(accumulated).strip()
            current_key = "biological_interpretation"
            accumulated = [line_strip.replace("### Interpretation:", "").replace("### Interpretation", "").strip()]
        elif line_strip.startswith("### Confidence"):
            if current_key: sections[current_key] = "\n".join(accumulated).strip()
            current_key = "confidence_assessment"
            accumulated = [line_strip.replace("### Confidence:", "").replace("### Confidence", "").strip()]
        elif line_strip.startswith("### Limitations"):
            if current_key: sections[current_key] = "\n".join(accumulated).strip()
            current_key = "limitations"
            accumulated = [line_strip.replace("### Limitations:", "").replace("### Limitations", "").strip()]
        else:
            if current_key:
                accumulated.append(line)
                
    if current_key:
        sections[current_key] = "\n".join(accumulated).strip()
        
    # Map confidence to standard categories
    conf = sections["confidence_assessment"].upper()
    if "HIGH" in conf:
        sections["confidence_assessment"] = "HIGH"
    elif "LOW" in conf:
        sections["confidence_assessment"] = "LOW"
    else:
        sections["confidence_assessment"] = "MEDIUM"
        
    return {
        "ai_provider": provider,
        "model_name": model,
        "findings": sections["findings"] or "No findings structured.",
        "literature_summary": sections["literature_summary"] or "No evidence cited.",
        "biological_interpretation": sections["biological_interpretation"] or "No interpretation parsed.",
        "confidence_assessment": sections["confidence_assessment"],
        "limitations": sections["limitations"] or "No limitations parsed."
    }

def _save_offline_fallback(job_id: str, organism: str, reason: str, confidence: str, limits: str) -> Dict[str, Any]:
    parsed = {
        "ai_provider": "offline",
        "model_name": "offline-fallback",
        "findings": f"Pathogen: {organism}",
        "literature_summary": "Insufficient literature evidence.",
        "biological_interpretation": reason,
        "confidence_assessment": confidence,
        "limitations": limits
    }
    _commit_ai_result(job_id, parsed)
    return parsed

def _commit_ai_result(job_id: str, parsed: Dict[str, Any]):
    """
    Saves the parsed AI report fields to the SQL database.
    """
    try:
        with SessionLocal() as db:
            # Clear existing entry if exists
            existing = db.query(AIInterpretation).filter(AIInterpretation.job_id == job_id).first()
            if existing:
                db.delete(existing)
                db.commit()
                
            db_ai = AIInterpretation(
                job_id=job_id,
                ai_provider=parsed["ai_provider"],
                model_name=parsed["model_name"],
                findings=parsed["findings"],
                literature_summary=parsed["literature_summary"],
                biological_interpretation=parsed["biological_interpretation"],
                confidence_assessment=parsed["confidence_assessment"],
                limitations=parsed["limitations"]
            )
            db.add(db_ai)
            db.commit()
    except Exception as e:
        logger.warning(f"Failed to commit AI Interpretation to database: {str(e)}")

def generate_deg_interpretation(
    job_id: str,
    significant_genes: List[Dict[str, Any]],
    go_results: List[Dict[str, Any]],
    kegg_results: List[Dict[str, Any]],
    pubmed_evidence: List[Dict[str, Any]],
    log_logger
) -> Dict[str, Any]:
    """
    Orchestrates the AI pathology interpretation for Differential Gene Expression (DEG) results.
    """
    log_logger.info("Starting AI interpretation for DEG results.")
    
    # 1. Format inputs for prompt context
    gene_str = "\n".join([f"- Gene {g['gene_id']}: log2FC={g['log2FoldChange']:.2f}, adj.p={g['padj']:.4f} ({g['regulation']})" for g in significant_genes[:10]])
    go_str = "\n".join([f"- GO Term {p['Term']} (P-value: {p['P-value']:.4f}, Overlap: {p['Overlap']})" for p in go_results[:5]])
    kegg_str = "\n".join([f"- KEGG Pathway {p['Term']} (P-value: {p['P-value']:.4f}, Overlap: {p['Overlap']})" for p in kegg_results[:5]])
    lit_str = "\n".join([f"- PMID: {a['pmid']} Title: {a['title']} Abstract: {a['abstract'][:200]}..." for a in pubmed_evidence[:3]])

    prompt = f"""
Significant Differentially Expressed Genes:
{gene_str}

Top Enriched Gene Ontology (GO) Terms:
{go_str}

Top Enriched KEGG Pathways:
{kegg_str}

Retrieved Scientific Publications:
{lit_str}
"""

    system_instruction = """
You are an expert transcriptomics and pathology AI interpreter.
Generate a structured, evidence-cited pathobiology interpretation based strictly on the query context.
You must follow these rules:
1. Every claim must cite the specific gene, pathway term, or PMID number supporting it.
2. Do not hallucinate clinical symptoms or replication mechanisms not backed by the input data.
3. Your response must consist exactly of these 5 sections, formatted as markdown headers:
   - ### Evidence: [Citations of statistical scores, fold changes, and PMIDs. Explicitly explain "Why this gene is significant" for your key differentially expressed genes.]
   - ### Analysis: [Pathology explanation of the cellular processes altered based on DEGs and enrichment. Explicitly analyze "Why this pathway is activated" based on the matched KEGG terms.]
   - ### Conclusion: [Synthesis and biological summary of transcriptomics outcomes. Explicitly detail "Therapeutic implications" and downstream target potentials.]
   - ### Confidence: [HIGH / MEDIUM / LOW with reason]
   - ### Limitations: [Analysis bottlenecks, such as a lack of wet-lab validation]
"""

    # 2. Select API route — try OpenAI first (primary), then Gemini as secondary
    if settings.is_openai_available:
        log_logger.info("Invoking OpenAI GPT API for DEG...")
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.openai_api_key)
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=2000
                )
            except Exception as quota_err:
                if "quota" in str(quota_err).lower() or "rate" in str(quota_err).lower():
                    log_logger.warning(f"GPT-4o quota/rate error: {quota_err}. Trying gpt-3.5-turbo fallback.")
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.2,
                        max_tokens=2000
                    )
                else:
                    raise
            text = response.choices[0].message.content
            parsed = _parse_deg_markdown_response(text, "openai", response.model)
            _commit_ai_result(job_id, parsed)
            return parsed
        except Exception as openai_err:
            log_logger.error(f"OpenAI API request failed: {str(openai_err)}. Attempting Gemini failover.")

    if settings.is_gemini_available:
        log_logger.info("Invoking Google Gemini API for DEG...")
        try:
            from google import genai
            client = genai.Client(api_key=settings.gemini_api_key)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[system_instruction + "\n\n" + prompt]
            )
            parsed = _parse_deg_markdown_response(response.text, "gemini", "gemini-2.5-flash")
            _commit_ai_result(job_id, parsed)
            return parsed
        except Exception as gemini_err:
            log_logger.error(f"Gemini API request failed: {str(gemini_err)}")

    # 2b. OpenRouter fallback for DEG
    if settings.is_openrouter_available:
        log_logger.info("Invoking OpenRouter API as LLM fallback for DEG...")
        import time
        import requests as _requests
        
        openrouter_models = [
            "deepseek/deepseek-r1-0528",
            "deepseek/deepseek-v3.2",
            "nvidia/nemotron-3-super-120b-a12b:free",
            "openrouter/free",
        ]
        last_or_err = None
        
        for or_model in openrouter_models:
            try:
                log_logger.info(f"Trying OpenRouter model: {or_model} for DEG")
                # Build JSON request payload
                payload = {
                    "model": or_model,
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 2000
                }
                # Enable reasoning for models that support it
                if "deepseek-r1" in or_model or "deepseek-v3" in or_model or "nemotron" in or_model or "free" in or_model:
                    payload["reasoning"] = {"enabled": True}
                
                or_resp = _requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.openrouter_api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://pathoscope-genomics.ai",
                        "X-Title": "PathoScope AI Pipeline"
                    },
                    json=payload,
                    timeout=60
                )
                or_resp.raise_for_status()
                or_data = or_resp.json()
                message = or_data.get("choices", [{}])[0].get("message", {})
                text = message.get("content", "")
                
                # Extract thinking/reasoning details if available
                reasoning = message.get("reasoning") or ""
                reasoning_details = message.get("reasoning_details")
                if reasoning_details and isinstance(reasoning_details, list):
                    reasoning_list = []
                    for rd in reasoning_details:
                        if isinstance(rd, dict) and rd.get("text"):
                            reasoning_list.append(rd["text"])
                    if reasoning_list:
                        reasoning = "\n".join(reasoning_list)
                
                if text and len(text.strip()) > 50:
                    parsed = _parse_deg_markdown_response(text, "openrouter", or_model)
                    if reasoning:
                        parsed["limitations"] = parsed["limitations"] + f"\n\n### AI Thinking Process:\n{reasoning.strip()}"
                    _commit_ai_result(job_id, parsed)
                    log_logger.info(f"OpenRouter {or_model} succeeded for DEG.")
                    return parsed
                else:
                    log_logger.warning(f"OpenRouter {or_model} returned empty/short response, trying next model.")
                    continue
            except Exception as or_err:
                last_or_err = or_err
                err_str = str(or_err)
                log_logger.warning(f"OpenRouter {or_model} failed for DEG: {err_str[:200]}")
                time.sleep(1)
                continue
        
        if last_or_err:
            log_logger.error(f"All OpenRouter models failed for DEG. Last error: {str(last_or_err)[:300]}")

    # 3. Fallback: Offline Rule-Based Summary
    log_logger.warning("Active API keys missing or requests failed. Running offline rule-based interpretation.")
    
    evidence = f"Identified {len(significant_genes)} significant DEGs (e.g. {', '.join([g['gene_id'] for g in significant_genes[:3]])}). GO enriched terms include: {go_results[0]['Term'] if go_results else 'None'}. PubMed publications include: {', '.join([a['pmid'] for a in pubmed_evidence])}."
    findings = f"Functional analysis maps genes to GO/KEGG networks such as cell cycle, apoptotic signaling, or transcription regulators. Upregulated genes: {len([g for g in significant_genes if g['regulation'] == 'UP'])}. Downregulated genes: {len([g for g in significant_genes if g['regulation'] == 'DOWN'])}."
    interpretation = "PathoScope offline DEG review completed. Significant transcriptional shift suggests pathway activation / repression. Full synthesis requires active Gemini or OpenAI API keys in backend/.env."
    confidence = "MEDIUM" if pubmed_evidence else "LOW"
    limitations = "Running in offline fallback mode. No LLM APIs were successfully called."

    parsed = {
        "ai_provider": "offline",
        "model_name": "offline-fallback",
        "findings": findings,
        "literature_summary": evidence,
        "biological_interpretation": interpretation,
        "confidence_assessment": confidence,
        "limitations": limitations
    }
    _commit_ai_result(job_id, parsed)
    return parsed

def _parse_deg_markdown_response(text: str, provider: str, model: str) -> Dict[str, Any]:
    """
    Helper to extract markdown headers into separate fields for DEG.
    """
    sections = {
        "evidence": "",
        "analysis": "",
        "conclusion": "",
        "confidence": "MEDIUM",
        "limitations": ""
    }
    
    current_key = None
    lines = text.split("\n")
    accumulated = []
    
    for line in lines:
        line_strip = line.strip()
        if line_strip.startswith("### Evidence"):
            if current_key: sections[current_key] = "\n".join(accumulated).strip()
            current_key = "evidence"
            accumulated = [line_strip.replace("### Evidence:", "").replace("### Evidence", "").strip()]
        elif line_strip.startswith("### Analysis"):
            if current_key: sections[current_key] = "\n".join(accumulated).strip()
            current_key = "analysis"
            accumulated = [line_strip.replace("### Analysis:", "").replace("### Analysis", "").strip()]
        elif line_strip.startswith("### Conclusion"):
            if current_key: sections[current_key] = "\n".join(accumulated).strip()
            current_key = "conclusion"
            accumulated = [line_strip.replace("### Conclusion:", "").replace("### Conclusion", "").strip()]
        elif line_strip.startswith("### Confidence"):
            if current_key: sections[current_key] = "\n".join(accumulated).strip()
            current_key = "confidence"
            accumulated = [line_strip.replace("### Confidence:", "").replace("### Confidence", "").strip()]
        elif line_strip.startswith("### Limitations"):
            if current_key: sections[current_key] = "\n".join(accumulated).strip()
            current_key = "limitations"
            accumulated = [line_strip.replace("### Limitations:", "").replace("### Limitations", "").strip()]
        else:
            if current_key:
                accumulated.append(line)
                
    if current_key:
        sections[current_key] = "\n".join(accumulated).strip()
        
    # Map confidence to standard categories
    conf = sections["confidence"].upper()
    if "HIGH" in conf:
        sections["confidence"] = "HIGH"
    elif "LOW" in conf:
        sections["confidence"] = "LOW"
    else:
        sections["confidence"] = "MEDIUM"
        
    return {
        "ai_provider": provider,
        "model_name": model,
        "findings": sections["analysis"] or "No analysis structured.",
        "literature_summary": sections["evidence"] or "No evidence cited.",
        "biological_interpretation": sections["conclusion"] or "No conclusion parsed.",
        "confidence_assessment": sections["confidence"],
        "limitations": sections["limitations"] or "No limitations parsed."
    }
