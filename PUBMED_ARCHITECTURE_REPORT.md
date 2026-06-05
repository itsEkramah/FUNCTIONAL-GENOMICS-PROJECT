# PathoScope AI — PubMed Architecture Report

**Date**: June 5, 2026  
**Auditor**: Antigravity  
**Status**: Completed  

---

## 1. Subsystem Architecture Redesign

We decoupled the PubMed literature retrieval system from the AI Interpretation module. Previously, search results were fetched dynamically during active pipeline runs and merged immediately into the AI context without an independent explorer.

### A. Core Architecture Flow

```text
PubMed Explorer Page (Frontend)
   │
   ├── [POST] /api/pubmed/search  ──> NCBI E-utilities / Fallback
   └── [GET]  /api/pubmed/queries ──> SQL Caches
```

1. **NCBI E-Utilities Engine**: Located in `backend/services/pubmed_service.py`, using ESearch (PMID listings), EFetch (XML details) with rate-limiting constraints (0.35s delay).
2. **Caching Layer**: Search records are persisted to SQLite (`PubMedQuery` and `PubMedArticle` models) to prevent duplicate API hits.
3. **API Routing Layer**: A dedicated route package `backend/api/pubmed.py` exposes:
   - `/api/pubmed/search` for search queries.
   - `/api/pubmed/queries` to fetch caching queries history.
4. **Independent Frontend Page**: Created `frontend/app/pubmed/page.tsx` displaying search controls, query strategies, relevance scores, and cached history.

---

## 2. Decoupled Evidence Extraction

- **Rule 8.3 & 8.4**: The system retrieves exact scientific articles including PMIDs, title, abstract, journal, year, and MeSH headings.
- **Rule 8.5 & 8.6**: No fabrication of abstracts or PMIDs. Fallback database contains real literature summaries.
- **Independent Usage**: Users can browse publications and search details for any biomolecule without running a full FASTA/FASTQ sequence pipeline.
