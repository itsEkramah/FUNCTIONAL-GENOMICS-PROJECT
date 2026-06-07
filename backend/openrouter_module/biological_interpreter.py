import json
import re
import logging
from typing import Dict, Any, List, Optional
from backend.openrouter_module.model_fallback_manager import ModelFallbackManager
from backend.openrouter_module.pubmed_service import PubMedService

logger = logging.getLogger("BiologicalInterpreter")

class BiologicalInterpreter:
    """
    Bioinformatics interpreter that translates genomic alignment and expression statistics
    into clinical pathobiology models, retrieving support literature and synthesizing results.
    """
    def __init__(self, fallback_manager: ModelFallbackManager = None, pubmed_service: PubMedService = None):
        self.fallback_manager = fallback_manager or ModelFallbackManager()
        self.pubmed_service = pubmed_service or PubMedService()

    def interpret_findings(
        self,
        genes: List[Dict[str, Any]],
        pathways: List[Dict[str, Any]],
        go_terms: List[Dict[str, Any]],
        disease_associations: List[str],
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Runs the functional genomics analysis pipeline.
        Steps:
          1. Clean input structures
          2. Run PubMed literature evidence pipeline
          3. Generate system and user prompts
          4. Call OpenRouter fallback chain
          5. Parse results into structured JSON output
        """
        # 1. Clean genes and pathways list for PubMed queries
        gene_names = [g.get("gene_id", "") for g in genes if g.get("gene_id")][:5]
        pathway_names = [p.get("pathway_name", p.get("Term", "")) for p in pathways if p.get("pathway_name") or p.get("Term")][:3]
        
        # 2. Retrieve literature context
        logger.info("Retrieving PubMed literature evidence context...")
        lit_context, top_articles = self.pubmed_service.generate_context_block(gene_names, pathway_names)

        # 3. Formulate prompt templates
        system_prompt = """You are an expert bioinformatics AI interpretation agent.
Your task is to analyze functional genomics and transcriptomics datasets and generate a highly structured pathobiology report.
You must output a raw, parseable JSON object containing exactly the following keys. Do not add any conversational text or markdown code block markers around the JSON.

Expected JSON Structure:
{
  "model_used": "Leave empty - the application will fill this in",
  "genes": ["A list of genes analyzed with brief structural description of their expression shift"],
  "pathways": ["A list of biological pathways mapped and details of their upregulation/downregulation"],
  "biomarkers": ["Identified potential biological markers for diagnosis"],
  "therapeutic_targets": ["Identified high-affinity therapeutic drug targets"],
  "disease_associations": ["List of pathologically associated diseases"],
  "literature_evidence": ["Citations of PubMed records PMIDs supporting these findings"],
  "clinical_relevance": "Analysis of translation to clinical utility",
  "future_directions": "Recommended follow-up assays or dry-lab analyses",
  "summary": "Full executive synthesis and pathobiology summary"
}
"""

        # Format input dataset statistics
        gene_data_str = "\n".join([
            f"- Gene: {g.get('gene_id')} | Log2FC: {g.get('log2FoldChange', g.get('log2FC', 0.0)):.2f} | adj.p: {g.get('padj', g.get('pvalue', 0.0)):.4f}"
            for g in genes[:10]
        ])
        
        pathway_data_str = "\n".join([
            f"- Pathway: {p.get('pathway_name', p.get('Term', ''))} | Overlap: {p.get('Overlap', 'N/A')} | pvalue/FDR: {p.get('pvalue', p.get('fdr', 0.0)):.4f}"
            for p in pathways[:10]
        ])
        
        go_data_str = "\n".join([
            f"- GO Term: {gt.get('Term', gt.get('go_name', ''))} | ID: {gt.get('ID', '')}"
            for gt in go_terms[:5]
        ])

        user_prompt = f"""
Functional Genomics Dataset Input Profile:

Organism/Metadata: {json.dumps(metadata)}
Diseases Assumed: {", ".join(disease_associations)}

Significant Genes & Fold Changes:
{gene_data_str}

Enriched Metabolic/Signaling Pathways:
{pathway_data_str}

Gene Ontology (GO) Biological Process terms:
{go_data_str}

Supporting Literature Evidence from PubMed:
{lit_context}

Please generate the interpretation covering:
1. Executive Summary
2. Significant Gene Analysis
3. Biological Functions
4. Molecular Mechanisms
5. Disease Relevance
6. Biomarker Potential
7. Therapeutic Target Potential
8. Drug Associations
9. Pathway Interpretation
10. Literature Evidence
11. Clinical Relevance
12. Future Research Directions

Make sure to populate all the fields in the requested JSON structure.
"""

        # 4. Call Fallback chain
        content, reasoning, successful_model = self.fallback_manager.generate_completion_with_fallback(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=3000
        )

        if not content:
            logger.error("Failed to generate AI interpretation.")
            return self._get_offline_json_fallback(genes, pathways, top_articles, disease_associations)

        # 5. Parse output
        parsed_json = self._clean_and_parse_json(content)
        if parsed_json:
            parsed_json["model_used"] = successful_model
            if reasoning:
                parsed_json["summary"] = parsed_json["summary"] + f"\n\n### LLM Internal Reasoning Process:\n{reasoning}"
            return parsed_json
        
        # Parse fallback if JSON syntax was corrupted
        logger.warning("Failed to parse LLM response as JSON. Creating parsed fallback structure.")
        return self._get_offline_json_fallback(genes, pathways, top_articles, disease_associations, raw_response=content)

    def _clean_and_parse_json(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """
        Extracts and parses JSON content from a response, handling markdown fences.
        """
        cleaned = raw_text.strip()
        # Remove markdown code fences if present
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```[a-zA-Z0-9]*\n", "", cleaned)
            cleaned = re.sub(r"\n```$", "", cleaned)
            cleaned = cleaned.strip()
            
        try:
            return json.loads(cleaned)
        except Exception:
            # Try parsing using regex to extract JSON bracket block
            match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except Exception:
                    pass
            return None

    def _get_offline_json_fallback(
        self,
        genes: List[Dict[str, Any]],
        pathways: List[Dict[str, Any]],
        articles: List[Dict[str, Any]],
        diseases: List[str],
        raw_response: str = ""
    ) -> Dict[str, Any]:
        """
        Creates a structured offline summary if no LLM APIs were successful or output was corrupted.
        """
        gene_ids = [g.get("gene_id", "") for g in genes]
        path_ids = [p.get("pathway_name", p.get("Term", "")) for p in pathways]
        pmids = [a["pmid"] for a in articles]
        
        summary = "PathoScope offline diagnostic completed. High-throughput data parsed successfully."
        if raw_response:
            summary += f"\n\nRaw Model Text:\n{raw_response}"
            
        return {
            "model_used": "offline-fallback",
            "genes": gene_ids,
            "pathways": path_ids,
            "biomarkers": [f"{gene_ids[0]} Potential Diagnostic Marker" if gene_ids else "None"],
            "therapeutic_targets": [f"{gene_ids[1]} Candidate Target" if len(gene_ids) > 1 else "None"],
            "disease_associations": diseases,
            "literature_evidence": pmids,
            "clinical_relevance": "Transcriptional changes indicate functional pathway alterations.",
            "future_directions": "Verify targets using qRT-PCR and custom functional cell assays.",
            "summary": summary
        }
