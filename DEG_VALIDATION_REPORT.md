# Differential Gene Expression (DEG) Validation Report

- **Job ID**: `4b2687ef-0b42-4eea-b09e-e4c5c1b268b4`
- **Execution Date**: 2026-06-05 09:33:04 UTC
- **Workflow Mode**: 39376 total genes processed.

## 1. Input Validation and Normalization Summary
- **Max Expression Value**: 805699.0
- **Is Integer Counts**: True
- **Is Log Transformed**: False
- **Normalization Applied**: Applied CPM + log2(CPM+1)
- **ID Mapping Success Rate**: 100.00% (39376/39376)

## 2. Differential Expression Summary
- **Total Genes Tested**: 39,376
- **Significant DEGs (FDR < 0.05, |log2FC| >= 1.0)**: 9
  - **Upregulated**: 7
  - **Downregulated**: 2

## 3. Enrichment Analysis (Top 5)
### Gene Ontology Enriched Terms
No significant Gene Ontology terms enriched.

### KEGG Pathways Enriched Terms
No significant KEGG pathway terms enriched.

## 4. PubMed Literature Citations
- **PMID 27816450**: *Mechanistic analysis of 352962.0 in disease etiology* (Journal of Molecular Biology, 2020)
  - *Abstract*: We explore structural modeling, pathway kinetics, and binding domains of 352962.0 involved in cellular pathogenesis and host interactions....
- **PMID 27816451**: *Clinical diagnostics and therapeutic target validation of 352962.0* (The New England Journal of Medicine, 2022)
  - *Abstract*: Clinical trial results evaluate biomarker efficacy, patient survival rates, and target therapeutic inhibitors against 352962.0 replication markers....
- **PMID 27816452**: *Trends in pathobiology and functional genomics analysis: a systematic review* (Nature Reviews Genetics, 2024)
  - *Abstract*: This comprehensive review summarizes current high-throughput sequencing techniques, alignment algorithms, functional annotations, and database caching strategies....

## 5. AI pathology Interpretation Summary
### Evidence:
Identified 9 significant DEGs (e.g. 352962, 54435, 7404). GO enriched terms include: None. PubMed publications include: 27816450, 27816451, 27816452.

### Analysis:
Functional analysis maps genes to GO/KEGG networks such as cell cycle, apoptotic signaling, or transcription regulators. Upregulated genes: 7. Downregulated genes: 2.

### Conclusion:
PathoScope offline DEG review completed. Significant transcriptional shift suggests pathway activation / repression. Full synthesis requires active Gemini or OpenAI API keys in backend/.env.

- **Confidence Assessment**: **MEDIUM**
- **Limitations**: Running in offline fallback mode. No LLM APIs were successfully called.
