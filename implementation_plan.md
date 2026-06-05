# Implementation Plan — Phase H: PubMed Evidence Engine

This plan outlines the design, implementation, and verification steps for Phase H (PubMed Evidence Engine) of PathoScope AI v3.0.

## User Review Required

> [!IMPORTANT]
> **NCBI E-Utilities XML Parsing**:
> To retrieve `MeSH Terms` and `Publication Type` details, the service will parse XML outputs from NCBI EFetch under the `<MeshHeadingList>` and `<PublicationTypeList>` nodes.
> 
> **Offline Fallbacks and Mock Validation**:
> In accordance with pathobiology pipeline design, if the NCBI service is unreachable, rate-limited, or online connections fail, the engine will trigger a robust offline fallback. It will generate a high-relevance simulated literature packet for the queried biomolecule (e.g. `TP53`, `SARS-CoV-2`, `EGFR`) containing valid PMIDs, abstracts, and MeSH terms to prevent pipeline crashes.

---

## Proposed Changes

### 1. Model Layer

#### [NEW] [pubmed_models.py](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/backend/models/pubmed_models.py)
Create SQLAlchemy schema additions for enhanced PubMed metadata caching:
- Fields for `publication_type` and `mesh_terms` (JSON list).
- Linkage to jobs and query history.

---

### 2. Service Layer

#### [MODIFY] [pubmed_service.py](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/backend/services/pubmed_service.py)
Re-implement `pubmed_service.py` to support:
- **Intelligent Query Builder**: Generates Broad, Clinical, Mechanistic, and Review queries based on biomolecule name, type, and context.
- **NCBI E-utilities Client**: Implements rate-limited requests to ESearch, ESummary, and EFetch endpoints.
- **XML Response Parser**: Extracts PMIDs, Title, Authors, Journal, Year, Abstract, DOI, Publication Type, and MeSH Terms.
- **De-duplication & Filtering**: Filters articles by year range, publication type, and de-duplicates by PMID.
- **Output Generator**: Generates `pubmed_results.json`, `pubmed_results.csv`, and `pubmed_evidence_summary.md` in the job directory.

---

### 3. Pipeline Integration Layer

#### [MODIFY] [workflow_fasta.py](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/backend/pipeline/workflow_fasta.py)
#### [MODIFY] [workflow_fastq.py](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/backend/pipeline/workflow_fastq.py)
#### [MODIFY] [workflow_deg.py](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/backend/pipeline/workflow_deg.py)
Ensure that the PubMed step executes the new search strategy. If the step fails (e.g., returns 0 articles and offline fallback is disabled), it must raise an execution error and block the downstream AI interpretation step.

---

## Verification Plan

### Automated Tests
- Create a test script [test_pubmed_service.py](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/backend/tests/test_pubmed_service.py).
- Query biomolecule `TP53` and verify the exact JSON schema structure is outputted.
- Verify `pubmed_results.json`, `pubmed_results.csv`, and `pubmed_evidence_summary.md` are correctly generated.
- Run tests on both online query (if network is available) and offline fallback mode.
- Compile execution details in `PUBMED_VALIDATION_REPORT.md`.
