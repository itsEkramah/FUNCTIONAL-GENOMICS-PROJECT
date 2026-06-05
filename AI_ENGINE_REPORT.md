# AI_ENGINE_REPORT.md — AI Interpretation Engine Report

This report outlines the design, prompt structure, provider integration, environment configurations, and evidence-grounding constraints for the AI Interpretation Engine in PathoScope AI v3.0.

---

## 1. System Integration

The AI Interpretation Engine translates raw biological outputs (sequence statistics, alignment hits, domain predictions, pathways, taxonomy trees) and fetched literature evidence into a structured, publication-grade pathobiology interpretation.

```
                  [Orchestrator: Job Finishes Step 9]
                                  │
                                  ▼
                    [Load Inputs for Step 10]
        - QC Metrics, Annotations, Domains, Pathways, Taxonomy
        - PubMed Abstracts (PMIDs, Titles, Text)
                                  │
                                  ▼
                    [Determine Provider Route]
         Is GEMINI_API_KEY set? ────► Yes ──► Call Google Gemini API
                     │
                     No
                     │
         Is OPENAI_API_KEY set? ────► Yes ──► Call OpenAI GPT API
                     │
                     No
                     │
                     ▼
             [Run Offline Fallback]
       Return: "Insufficient evidence for interpretation 
       (active API keys not configured in the system environment)"
                                  │
                                  ▼
                   [Validate Response & Save]
         Verify 5 mandatory sections. Save to db table.
```

---

## 2. API Key Management

* **No Hardcoding**: All API keys are loaded dynamically from `.env` via the global `settings` object (`backend/config/settings.py`) which implements Pydantic BaseModel Field lookups.
* **Environment Keys**:
  * `GEMINI_API_KEY`: API key for Google Gemini (`google-generativeai`).
  * `OPENAI_API_KEY`: API key for OpenAI (`openai`).
* **Fallback Gate**: If neither key is present, the service logs a trace warning and falls back to a deterministic offline rule-based summary to prevent runtime execution failures.

---

## 3. Input Context Mapping

The payload fed to the LLM context is structured as a clear YAML/JSON dump containing:
1. **Metadata**: Job ID, workflow type (FASTA, FASTQ, DEG).
2. **Quality Control**: Length, GC%, assembly N50, read counts.
3. **Taxonomy**: Species name, rank, full lineage tree.
4. **Annotations & Domains**: Top SwissProt hit IDs, Pfam domain accessions.
5. **Pathways**: Mapped KEGG pathway IDs, pathway names, overlapping gene counts.
6. **Literature Evidence**: List of PMIDs, titles, and abstract snippets.

---

## 4. Prompt Engineering & Grounding Rules

### System Prompt Directive
```text
You are a board-certified clinical bioinformatician and pathogen pathobiology expert.
Your job is to write a highly detailed pathobiology interpretation based strictly on the provided experimental metrics and literature abstracts.

You must adhere to the following rules:
1. Grounding: Every claim in your interpretation must be cited using either database hits (e.g. subject proteins) or PubMed publication numbers (e.g., PMID:12345).
2. No Hallucinations: If no annotations or PubMed abstracts are provided, or if the evidence does not support a specific pathogen claim, you must state: "Insufficient evidence for interpretation". Do not invent biological claims, virulence pathways, or clinical symptoms.
3. Output Structure: You must format your response exactly under these 5 markdown headers:
   - ### Findings: [Summary of proteins, pathways, and taxons identified]
   - ### Evidence: [Citations of alignment scores and PMIDs]
   - ### Interpretation: [Biological explanation of pathogen or DEG profile]
   - ### Confidence: [HIGH / MEDIUM / LOW with justification]
   - ### Limitations: [Technical/experimental bottlenecks and suggestions]
```

---

## 5. Output Schema & Database Storage

The service parses the LLM markdown response into 5 separate fields and saves them into the `ai_interpretations` table:
* `job_id`: UUID mapping to the active job.
* `ai_provider`: `'gemini'`, `'openai'`, or `'offline'`.
* `model_name`: Model used (e.g., `'gemini-1.5-pro'`, `'gpt-4o'`, `'offline-fallback'`).
* `findings`: Text under the `Findings` section.
* `literature_summary`: Text under the `Evidence` section.
* `biological_interpretation`: Text under the `Interpretation` section.
* `confidence_assessment`: `'HIGH'`, `'MEDIUM'`, or `'LOW'`.
* `limitations`: Text under the `Limitations` section.

---

## 6. Offline Fallback Logic

When API keys are missing or requests fail due to network/rate-limiting errors:
* The system constructs a text summary based on rules:
  * Counts total ORFs, annotations, pathways.
  * Mapped organism name is reported as the primary finding.
  * Mapped PMIDs are listed as literature evidence.
  * Interpretation is set to: `"Insufficient evidence for interpretation (active API keys are not configured in the system environment)"`.
  * Confidence is set to: `"LOW"`.
  * Limitations is set to: `"No active API keys provided for Gemini or OpenAI. Offline execution mode was triggered."`
* This guarantees that the pipeline succeeds end-to-end and provides clean, honest metadata.
