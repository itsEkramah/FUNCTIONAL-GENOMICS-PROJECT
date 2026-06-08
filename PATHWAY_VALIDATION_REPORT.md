# PathoScope AI Pathway System Validation Report

The PathoScope AI platform maps and statistically tests enriched biological processes and pathways for genomic and transcriptomic datasets. This report documents the design, verification, and frontend rendering of the pathway identification system.

## 1. Pathway Analysis Pipeline Flow
The pathway system supports two operational paradigms based on the pipeline type:
- **Homology Mapping (FASTA/FASTQ)**: Mapped using annotated homology hits from SwissProt via `map_proteins_to_kegg` in [kegg_service.py](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/backend/services/kegg_service.py).
- **Over-Representation Analysis (DEG)**: Evaluated using target gene lists from classified differential expression lists. Features automatic fallback between web services (GSEApy Enrichr) and local statistical engines (`run_local_ora` in [deg_engine.py](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/backend/core/deg_engine.py)).

---

## 2. Statistical ORA Verification
For the DEG pipeline, when the web service is offline or inaccessible, the local over-representation analysis (ORA) engine is invoked:
- **Test**: One-sided Fisher's Exact Test (`scipy.stats.fisher_exact(..., alternative="greater")`).
- **Multiple testing correction**: Benjamini-Hochberg False Discovery Rate (FDR-BH) adjusted p-value (`statsmodels.stats.multitest.multipletests`).
- **Databases Supported**: KEGG, GO Biological Process, GO Molecular Function, and GO Cellular Component.
- **Filtering**: Pathway databases are constrained to biological size parameters ($15 \le N \le 500$ genes) to screen out broad, uninformative terms and narrow, overly-specific single-gene categories.

### Bug Fix: DNA Replication Reference Database
A typo in the local reference database where `M MCM3` was entered instead of `MCM3` has been resolved in [deg_engine.py](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/backend/core/deg_engine.py). DNA Replication category mappings now evaluate all MCM complex elements correctly.

---

## 3. Frontend Results Workspace Integration
An interactive **Pathways (KEGG)** workspace tab has been added to [ResultsViewer.tsx](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/frontend/components/ResultsViewer.tsx):
- Exposes detailed information: Pathway ID, Pathway Term/Name, Overlap Gene Count, raw p-value, and FDR adjusted p-value.
- **Reference Hyperlinks**: Every pathway ID and row features external reference links to the official KEGG database (`https://www.genome.jp/dbget-bin/www_bget?pathway+<pathway_id>`). If the ID is not standard, the link defaults to search the KEGG directory.
- P-values and FDR values are rendered in professional exponential notation.
