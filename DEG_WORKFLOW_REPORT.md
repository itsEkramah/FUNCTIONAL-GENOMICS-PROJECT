# DEG_WORKFLOW_REPORT.md — Differential Gene Expression (DEG) Workflow Report

This report outlines the biological workflow, execution steps, statistical calculations, and reference logic sources for the Differential Gene Expression (DEG) pipeline in PathoScope AI v3.0.

---

## Workflow Steps Overview

```
[Expression Table CSV / TSV]
              │
              ▼
1. Input Validation (Verify columns: gene_id, log2FoldChange, pvalue)
              │
              ▼
2. Normalization (Strip version suffixes, Ensembl-to-HGNC mapping)
              │
              ▼
3. BH-FDR Correction (Benjamini-Hochberg multiple testing correction)
              │
              ▼
4. Classification (UP / DOWN / NS labeling based on thresholds)
              │
              ▼
5. KEGG Pathway Enrichment (GSEAPy functional pathway mapping)
              │
              ▼
6. GO Enrichment (Gene Ontology functional processes)
              │
              ▼
7. PubMed Retrieval (Fetch literature abstracts for key genes/pathways)
              │
              ▼
8. AI Interpretation (Evidence-grounded transcription report)
              │
              ▼
9. Report Generation (Volcano plots, Bubble plots, HTML/PDF/CSV)
```

---

## Detailed Step Specifications

### 1. Input Validation
* **Input**: Expression metrics table (`.csv`, `.tsv`, `.txt`).
* **Output**: Cleaned pandas DataFrame.
* **Validation Checkpoint**: Verifies that columns `gene_id`, `log2FoldChange`, and `pvalue` exist. Checks that values are numeric and drops rows with missing, infinite, or invalid data.
* **Biological Rationale**: Ensures that the input is a valid gene expression summary matrix before applying statistical testing.
* **Repository Logic Source**: `clones/deg-analysis-pipeline/DEG.py` (Cell 2 raw data load).

### 2. Normalization
* **Input**: Validated gene list with Ensembl IDs, HGNC symbols, or other formats.
* **Output**: Standardized HGNC gene symbols list, filtered to protein-coding genes.
* **Validation Checkpoint**: Strips version suffixes (e.g. `ENSG00000139618.15` -> `ENSG00000139618`). Queries MyGene.info API (with offline fallback if unavailable).
* **Biological Rationale**: Mapped IDs are standardized to biological symbols so that downstream Gene Set Enrichment databases (KEGG/GO) can match the genes accurately.
* **Repository Logic Source**: `clones/deg-analysis-pipeline/DEG.py` (Cell 8 mygene querymany).

### 3. BH-FDR Correction
* **Input**: Unadjusted p-values from statistical comparisons.
* **Output**: Adjusted p-values (False Discovery Rate - FDR).
* **Validation Checkpoint**: Executed using `statsmodels.stats.multitest.multipletests(method='fdr_bh')`. Falls back to a pure-Python cumulative BH calculation if statsmodels is unavailable.
* **Statistical Rationale**: In high-throughput biology, testing thousands of genes simultaneously results in a high probability of false discoveries (Type I errors). The Benjamini-Hochberg procedure controls the False Discovery Rate (FDR).
* **Repository Logic Source**: `clones/deg-analysis-pipeline/DEG.py` (Line 445 multipletests).

### 4. Classification
* **Input**: Mapped genes, log2FCs, and adjusted p-values (FDR).
* **Output**: Categorized gene categories.
* **Validation Checkpoint**:
  * **Upregulated (UP)**: `log2FoldChange >= 1.0` and `FDR < 0.05`.
  * **Downregulated (DOWN)**: `log2FoldChange <= -1.0` and `FDR < 0.05`.
  * **Not Significant (NS)**: All other genes.
* **Biological Rationale**: Standard threshold filters select biologically significant genes showing significant fold change and statistical confidence.
* **Repository Logic Source**: `clones/deg-analysis-pipeline/DEG.py` (Lines 455-469 significance checks).

### 5. KEGG Pathway Enrichment
* **Input**: UP and DOWN regulated gene lists.
* **Output**: Enriched KEGG biological pathway terms (P-value, FDR, enrichment score).
* **Validation Checkpoint**: Filters pathways to retain those with gene counts within `15 <= pathway_size <= 500`. Uses GSEAPy Enrichr.
* **Biological Rationale**: Identifies which metabolic and signalling pathways are altered in the experiment.
* **Repository Logic Source**: `clones/GSEApy` and `clones/deg-analysis-pipeline/DEG.py` (enrichr queries).

### 6. GO Enrichment
* **Input**: UP and DOWN regulated gene lists.
* **Output**: Enriched Gene Ontology terms (Biological Process, Molecular Function, Cellular Component).
* **Validation Checkpoint**: Pathway size matches the configured thresholds.
* **Biological Rationale**: Grouping genes by shared cellular process, location, or binding activity provides high-level functional insights.
* **Repository Logic Source**: `clones/GSEApy` (enrichr interface).

### 7. PubMed Retrieval
* **Input**: Top enriched pathways and key classified genes.
* **Output**: Cached publication citations and abstracts.
* **Validation Checkpoint**: Queries local database cache first. Compiles relevance scores.
* **Biological Rationale**: Fetches references explaining the role of the significant genes or pathways in disease states.
* **Repository Logic Source**: E-Utilities literature search.

### 8. AI Interpretation
* **Input**: Mapped results (significant genes, enriched pathways) and PubMed abstracts.
* **Output**: Grounded, evidence-cited transcription report.
* **Validation Checkpoint**: Outputs exact sections: Findings, Evidence, Interpretation, Confidence, Limitations. Hallucinations are forbidden.
* **Biological Rationale**: Explains downstream metabolic or pathology outcomes based on transcription profiles.
* **Repository Logic Source**: Master Blueprint.

### 9. Report Generation
* **Input**: Classification data and enrichment statistics.
* **Output**: Volcano plot PNG, Bubble plot PNG, HTML, PDF, and CSV files in job folder.
* **Validation Checkpoint**: Validates plot generation, check file outputs.
* **Biological Rationale**: Volcano plots show the relationship between statistical significance (FDR) and magnitude of change (log2FC) for all genes. Bubble plots show pathway enrichment p-values and overlapping gene ratios.
* **Repository Logic Source**: `clones/deg-analysis-pipeline/DEG.py` (Cells 6 and 9 plotting).
