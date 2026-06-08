# BACKEND_ARCHITECTURE_REPORT.md — Backend Architecture Report

> **Document Status**: `FINAL`  
> **Target Environment**: FastAPI + Uvicorn / PostgreSQL + Redis / Python 3.12+  
> **Development Constraint**: NO CODE IMPLEMENTED YET — STRICT ARCHITECTURAL ALIGNMENT PHASE  

---

## 1. BACKEND FOLDER & FILE TREE

```
backend/
├── app.py                      # Main FastAPI server entrypoint & router mounts
├── database.py                 # SQLAlchemy engine, sessionmaker, and session contexts
├── config.py                   # Pydantic-settings config loader (.env & config files)
├── config/
│   ├── thresholds.yaml         # Global biological constants (EVALUE, MIN_ORF_LENGTH)
│   └── tool_paths.yaml         # Path mappings to tool binaries (fastp, FastQC, SPAdes, etc.)
├── api/
│   ├── __init__.py
│   ├── auth.py                 # User login, session validation, token creation
│   ├── upload.py               # Asynchronous chunk-streaming upload endpoints
│   ├── jobs.py                 # Job initialization, status polling, and results retrieval
│   ├── reports.py              # Download endpoints for GFF3, PDF, and HTML reports
│   └── settings.py             # Environment configuration (API key setups)
├── pipeline/
│   ├── __init__.py
│   ├── pipeline_runner.py      # Background orchestrator managing job step validations
│   ├── workflow_fasta.py       # FASTA viral genome annotation sequence runner
│   ├── workflow_fastq.py       # FASTQ raw reads quality, trimming, and assembly runner
│   └── workflow_deg.py         # DEG transcriptomics analysis sequence runner
├── core/
│   ├── __init__.py
│   ├── orf_finder.py           # 6-frame scanning and overlap removal calculations
│   ├── translator.py           # Resilient DNA-to-peptide sequence translator
│   ├── qc_engine.py            # Genome length, GC%, and ambiguous base calculator
│   └── deg_engine.py           # Benjamini-Hochberg FDR calculations & fold change classification
├── services/
│   ├── __init__.py
│   ├── fastqc_service.py       # FastQC execution subprocess wrapper
│   ├── fastp_service.py        # fastp execution subprocess wrapper & JSON output parser
│   ├── spades_service.py       # SPAdes --rnaviral execution subprocess wrapper
│   ├── diamond_service.py      # DIAMOND blastp execution subprocess wrapper & TSV parser
│   ├── hmmer_service.py        # HMMER hmmscan execution subprocess wrapper & alignment parser
│   ├── kegg_service.py         # KEGG pathway annotation & GSEApy enrichment wrapper
│   ├── ncbi_service.py         # NCBI Taxonomy lineage fetcher
│   ├── pubmed_service.py       # NCBI E-Utilities literature search, fetcher, & query caching
│   └── ai_service.py           # OpenAI/Gemini API wrapper for evidence-grounded summaries
├── models/
│   ├── __init__.py
│   ├── base.py                 # SQLAlchemy declarative base class
│   ├── user.py                 # User accounts and login Sessions tables mapping
│   ├── job.py                  # Jobs and JobSteps state tracking tables mapping
│   ├── file.py                 # UploadedFiles metadata tables mapping
│   ├── results.py              # FastaRuns, FastqRuns, and DegRuns metadata tables mapping
│   ├── annotation.py           # DIAMOND, Pfam, NCBI Taxonomy, and KEGG results mapping
│   ├── pubmed.py               # PubMedQueries and PubMedArticles mapping
│   └── ai.py                   # AIInterpretations report sections mapping
├── reports/
│   ├── __init__.py
│   ├── base_report.py          # Abstract report builder class definition
│   ├── html_report.py          # HTML report compiler
│   ├── pdf_report.py           # PDF report builder using ReportLab
│   ├── csv_report.py           # CSV / JSON results compiler
│   └── gff3_report.py          # GFF3 genomics annotation builder
├── utils/
│   ├── __init__.py
│   ├── file_detector.py        # Header checking utility for automatic workflow selection
│   └── logger.py               # Unified logging handler (writes to file and stdout)
└── tests/
    ├── __init__.py
    ├── unit/                   # Tests for config, core engines, and utilities
    ├── integration/            # Tests for DB transactions, subprocess wrappers, and APIs
    └── bio_validation/         # Verification tests on authentic viral genomes and reads
```

---

## 2. FILE RESPONSIBILITY MATRIX

| Subsystem / File | Responsibility |
|------------------|----------------|
| `app.py` | Configures CORS, mounts endpoint routes (`/auth`, `/upload`, `/jobs`), handles global HTTP exceptions, and mounts static folders. |
| `database.py` | Initializes PostgreSQL connection pool. Provides dependency session generator `get_db` for APIs, and context manager `db_session` for background processes. |
| `config.py` | Reads `.env` and YAML files. Exposes application parameters (database credentials, API keys, biological constants, and binary paths). |
| `api/upload.py` | Receives files via async chunk-streaming, saves them to inputs storage, runs `file_detector.py`, and creates the initial Job record. |
| `api/jobs.py` | Resolves job triggers, returns job statuses, and exposes JSON outputs for finalized results. |
| `pipeline/pipeline_runner.py` | Spawns background worker tasks. Orchestrates individual pipeline steps, catches subprocess signals, updates step databases, and stops execution on failure. |
| `core/orf_finder.py` | Scans sequences for start and stop codons in all 6 reading frames. Removes overlaps on the same strand. |
| `core/translator.py` | Translates DNA to peptide codons, ignoring partial sequences at ends. Prevents KeyError crashes. |
| `core/deg_engine.py` | Runs statistics on log2 fold changes and calculates Benjamini-Hochberg FDR adjustments. |
| `services/*_service.py` | Execute biological tools via shell subprocesses, validates stderr output, and parses results files. |
| `services/pubmed_service.py` | Queries NCBI E-Utilities (`esearch`, `efetch`), filters query relevance scores, and stores results to local DB cache. |
| `services/ai_service.py` | Assembles grounded biological data and literature references into structured Gemini/OpenAI prompt structures. |
| `reports/*_report.py` | Compile results tables and text annotations into GFF3, HTML, and PDF file buffers. |
| `utils/file_detector.py` | Inspects file start lines to dynamically match FASTA (`>`), FASTQ (`@`), or DEG table column headers. |

---

## 3. COMPREHENSIVE MODULE IMPORTS MAP

```
[app.py]
  ├── imports ──► [database.py]
  └── imports ──► [api/routes (auth.py, upload.py, jobs.py, reports.py)]

[api/upload.py]
  ├── imports ──► [utils/file_detector.py]
  └── imports ──► [database.py] (SQLAlchemy Session)

[api/jobs.py]
  ├── imports ──► [pipeline/pipeline_runner.py]
  └── imports ──► [database.py] (SQLAlchemy Session)

[pipeline/pipeline_runner.py]
  ├── imports ──► [pipeline/workflow_fasta.py]
  ├── imports ──► [pipeline/workflow_fastq.py]
  ├── imports ──► [pipeline/workflow_deg.py]
  └── imports ──► [database.py] (SessionLocal Context)

[pipeline/workflow_fasta.py]
  ├── imports ──► [core/qc_engine.py]
  ├── imports ──► [core/orf_finder.py]
  ├── imports ──► [core/translator.py]
  ├── imports ──► [services/diamond_service.py]
  ├── imports ──► [services/hmmer_service.py]
  ├── imports ──► [services/kegg_service.py]
  ├── imports ──► [services/ncbi_service.py]
  ├── imports ──► [services/pubmed_service.py]
  ├── imports ──► [services/ai_service.py]
  └── imports ──► [reports/ (html_report, pdf_report, gff3_report)]

[pipeline/workflow_fastq.py]
  ├── imports ──► [services/fastqc_service.py]
  ├── imports ──► [services/fastp_service.py]
  ├── imports ──► [services/spades_service.py]
  └── imports ──► [pipeline/workflow_fasta.py] (Contig hand-off)

[pipeline/workflow_deg.py]
  ├── imports ──► [core/deg_engine.py]
  ├── imports ──► [services/kegg_service.py] (GSEApy Wrapper)
  ├── imports ──► [services/pubmed_service.py]
  ├── imports ──► [services/ai_service.py]
  └── imports ──► [reports/ (html_report, pdf_report)]
```

---

## 4. DETAILED PIPELINE EXECUTION FLOW

```text
[HTTP Request: POST /api/v1/job/start]
      │
      ▼
[API Layer creates BackgroundTask or Thread]
      │
      ▼
[pipeline_runner.py: run_job(job_id)]
  ├── 1. Fetch Job from database
  ├── 2. Set Job status to RUNNING in PostgreSQL & Redis
  ├── 3. Load Workflow Runner (workflow_fasta/fastq/deg)
  └── 4. Loop through Workflow Steps:
        │
        ├─► For each Step in StepList:
        │     ├── a. Update Step status in database to RUNNING
        │     ├── b. Invoke step function (or services wrapper subprocess)
        │     ├── c. Capture stdout/stderr logs into pipeline.log
        │     ├── d. Run validation check (e.g. check output file size/format)
        │     │        ├── Validation PASSED ──► Update Step to COMPLETED ──► Continue loop
        │     │        └── Validation FAILED ──► [FAIL PIPELINE GATE]
        │     │                                       │
        │     ▼                                       ▼
        │  [Continue to Next Step]            [Log step error details]
        │                                             │
        │                                             ▼
        │                                     [Update Step to FAILED]
        │                                             │
        │                                             ▼
        │                                     [Update Job status to FAILED]
        │                                             │
        │                                             ▼
        │                                     [Save failed_reason and STOP]
        │
        ▼
  [All Steps Completed Successfully]
        │
        ▼
  [Generate Reports (GFF3, PDF, HTML)]
        │
        ▼
  [Update Job status to COMPLETED & progress to 100%]
```

---

## 5. JOB TRACKING FLOW (CLIENT-SERVER STATE SYNC)

```
[Frontend Client]                    [FastAPI Server]                 [Redis Cache] / [Postgres]
        │                                   │                                     │
        │─── POST /api/v1/upload ──────────►│                                     │
        │    (Upload FASTA file)            │                                     │
        │                                   │─── Check File Header ──────────────►│
        │                                   │─── Create Job Record (QUEUED) ─────►│
        │◄── Return JOB_ID & Workflow ──────│                                     │
        │                                   │                                     │
        │─── POST /api/v1/job/start ───────►│                                     │
        │    (Starts background thread)     │─── Set Status = RUNNING ───────────►│ (Sync Redis & PG)
        │◄── Return 202 Accepted ───────────│                                     │
        │                                   │                                     │
        │─── GET /job/status (Poll 3s) ────►│                                     │
        │                                   │◄── Read Status & Progress ──────────│ (From Redis)
        │◄── Return status/progress % ──────│                                     │
        │                                   │                                     │
        │─── SSE /job/progress ────────────►│                                     │
        │    (Client listens to updates)    │◄── Push logs & completed steps ─────│ (From pipeline.log)
        │◄── Streamed step updates ─────────│                                     │
```

---

## 6. DATABASE TRANS-ACTION FLOW (ORM & CONNECTIONS)

1. **API Thread**:
   * Uses FastAPI dependency injection `db: Session = Depends(get_db)`.
   * Sessions are committed and automatically closed when HTTP responses return to the client.
2. **Background Thread (`pipeline_runner.py`)**:
   * API dependency injections are not available in background threads. 
   * The runner utilizes a custom database context manager:
     ```python
     with SessionLocal() as db:
         # Perform database updates (e.g. update job steps)
         db.commit()
     ```
   * Sessions are opened just-in-time and closed immediately before spawning any long-running tool subprocesses (FastQC, SPAdes). This ensures database connections are returned to the pool and are not held open during hour-long computations.

---

## 7. PUBMED RETRIEVAL & EVIDENCE FLOW

```
[Workflow Annotations Completed]
               │
               ▼
[Generate Search Term Queries]
  ├── Primary: "Organism Name" AND "Protein Name"
  ├── Secondary: "Organism Name" AND "Pfam Domain Name"
  └── Tertiary: "Organism Name" AND "KEGG Pathway"
               │
               ▼
[Check Local DB Cache (pubmed_queries)]
  ├── Match found ──► Retrieve PMIDs & abstracts from pubmed_articles
  └── No match ─────► [NCBI E-Utilities Query]
                        ├── a. esearch.fcgi ──► Retrieve PMIDs list
                        ├── b. efetch.fcgi  ──► Retrieve abstracts & DOIs
                        └── c. Store in pubmed_articles (Set unique PMID index)
               │
               ▼
[Relevance Scorer Engine]
  ├── Ranks articles by keyword overlap frequency
  └── Discards articles scoring below threshold
               │
               ▼
[Filter Top 10 Abstracts] ──► Output formatted evidence bundle to AI Service
```

---

## 8. EVIDENCE-GROUNDED AI INTERPRETATION FLOW

```
[Evidence Bundle (Metadata + Top Abstracts)] + [Biological Outputs (DIAMOND / Pfam)]
                                       │
                                       ▼
                       [Prompt Orchestrator Builder]
             (Builds strictly defined system prompt boundaries)
                                       │
                                       ▼
                         [Gemini / OpenAI API Wrapper]
                (Exchanges credentials via loaded .env keys)
                                       │
                                       ▼
                          [Check Literature Presence]
     ├── No abstracts present ──► Output "Insufficient evidence for interpretation."
     └── Abstracts present ─────► Generate Analysis & Cite PMIDs, e.g. [PMID: 1234567]
                                       │
                                       ▼
                   [Validate Output JSON Schema Alignment]
             (Ensures response parses into the 5 mandated keys)
                                       │
                                       ▼
                 [Save to database: ai_interpretations table]
```

---

## 9. REPORT GENERATION FLOW

When the pipeline completes all validation checkpoints, the Report Generator compiles raw table structures into final formats:

```
                  ┌────────────────────────────────────────┐
                  │          Database Run Metadata         │
                  │   (fasta_runs, annotations, pfam)      │
                  └───────────────────┬────────────────────┘
                                      │ Renders
             ┌────────────────────────┼────────────────────────┐
             ▼                        ▼                        ▼
  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
  │     GFF3 Report     │  │     PDF Report      │  │     HTML Report     │
  │  (gff3_report.py)   │  │   (pdf_report.py)   │  │  (html_report.py)   │
  ├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
  │ Maps ORF genomic    │  │ Builds styled pages │  │ Renders static, self│
  │ coordinates into    │  │ using ReportLab flow│  │ contained layout with│
  │ GFF3 standard fields│  │ tables and figures. │  │ integrated charts.  │
  └──────────┬──────────┘  └──────────┬──────────┘  └──────────┬──────────┘
             │                        │                        │
             └────────────────────────┼────────────────────────┘
                                      │ Saves to
                                      ▼
                        ┌────────────────────────────┐
                        │   storage/jobs/{job_id}/   │
                        │        reports/            │
                        └────────────────────────────┘
```
