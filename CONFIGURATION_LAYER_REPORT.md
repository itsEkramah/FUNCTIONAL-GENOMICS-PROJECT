# CONFIGURATION_LAYER_REPORT.md — Configuration Layer Report

> **Document Status**: `FINAL`  
> **Backend Path**: `backend/config/` and `backend/utils/`  
> **Development Constraint**: ONLY CONFIGURATION INFRASTRUCTURE IMPLEMENTED — NO WORKFLOW LOGIC  

This document explains the settings, variables, system constants, biological thresholds, and centralized logging configurations implemented for **PathoScope AI v3.0**.

---

## 1. ENVIRONMENTAL SETTINGS (`backend/config/settings.py`)

All environment configurations are loaded dynamically from `backend/.env` using `python-dotenv` and validated via Pydantic. API keys are loaded dynamically into memory and are never hardcoded or committed to git.

| Setting Name | Environment Variable | Default Value | Purpose / Description |
|--------------|----------------------|---------------|-----------------------|
| `openai_api_key` | `OPENAI_API_KEY` | `""` (Empty String) | API key for OpenAI GPT models (e.g. gpt-4o) used for evidence-grounded summary generation. |
| `gemini_api_key` | `GEMINI_API_KEY` | `""` (Empty String) | API key for Google Gemini models (e.g. gemini-1.5-pro) used for summaries. |
| `database_url` | `DATABASE_URL` | `postgresql://user:password@localhost:5432/pathoscope_ai` | SQLAlchemy connection string for the PostgreSQL database. |
| `redis_url` | `REDIS_URL` | `redis://localhost:6379/0` | Connection string pointing to the Redis cache database. |
| `log_level` | `LOG_LEVEL` | `"INFO"` | Central logging severity cutoff level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |

### Status Methods
* `is_openai_available`: Returns `True` if `OPENAI_API_KEY` has a length > 0.
* `is_gemini_available`: Returns `True` if `GEMINI_API_KEY` has a length > 0.

---

## 2. SYSTEM CONSTANTS (`backend/config/constants.py`)

Exposes global system values, folder locations, and statuses.

### Directory Path Constants
* `STORAGE_DIR`: Points to `storage/` directory in project root.
* `JOBS_DIR`: Points to `storage/jobs/` where individual job folders are housed.
* `CACHE_DIR`: Points to `storage/cache/` for caching temporary files.
* `PUBMED_DIR`: Points to `storage/pubmed/` for caching PubMed articles.

### Workflow & Status Constants
* **Workflows**: `FASTA`, `FASTQ`, `DEG`.
* **Job States**:
  * `QUEUED`: Job created.
  * `RUNNING`: Running pipeline.
  * `COMPLETED`: All steps passed.
  * `FAILED`: Step error or validation fail.
  * `CANCELLED`: User terminated the run.
* **Job Steps States**: `PENDING`, `RUNNING`, `COMPLETED`, `FAILED`.

---

## 3. MANDATORY BIOLOGICAL THRESHOLDS (`backend/config/thresholds.py`)

All thresholds have been isolated and defined as global python variables. No other module is permitted to hardcode these limits.

### 3.1 FASTA Genome Analysis Thresholds
* `MIN_ORF_LENGTH_BP = 100`: Minimum length (in base pairs) for an Open Reading Frame (ORF) to be detected. Discards short sequence noise.
* `DIAMOND_EVALUE_MAX = 1e-5`: Maximum E-value allowed for blastp alignments against the SwissProt database. Forces high statistical confidence.
* `DIAMOND_IDENTITY_MIN = 30.0`: Minimum identity match percentage (30.0%) required for protein alignment hits.
* `DIAMOND_COVERAGE_MIN = 50.0`: Minimum alignment query coverage (50.0%) required to confirm a homology hit.

### 3.2 FASTQ Quality & Assembly Thresholds
* `FASTQ_QUALITY_PHRED = 20`: Enforces `fastp` Q20 base trimming (Phred quality score >= 20, equivalent to 99% base accuracy).
* `FASTQ_READ_LENGTH_MIN = 50`: Discards any trimmed reads shorter than 50bp to prevent assembly gaps.
* `FASTQ_CONTIG_LENGTH_MIN = 500`: Filters out short, low-confidence contigs < 500bp post-SPAdes assembly.

### 3.3 Transcriptomics DEG Thresholds
* `DEG_FDR_MAX = 0.05`: Maximum adjusted False Discovery Rate (FDR) allowed for differential expression significance.
* `DEG_LOG2FC_UP = 1.0`: Minimum log2 fold change required to label a gene as upregulated (equivalent to a 2-fold expression increase).
* `DEG_LOG2FC_DOWN = -1.0`: Maximum log2 fold change required to label a gene as downregulated (equivalent to a 50% expression drop).
* `PATHWAY_SIZE_MIN = 15`: Minimum gene set size allowed for KEGG/GO functional enrichment.
* `PATHWAY_SIZE_MAX = 500`: Maximum gene set size allowed for KEGG/GO enrichment.

---

## 4. CENTRALIZED LOGGING (`backend/utils/logger.py`)

Centralized logging formats message strings and routes logs to stdout and flat files.

### Design Features
1. **Console & App Logging**: Renders logs to console and `storage/logs/app.log` using format:
   `[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s`
2. **Job Isolation Logger**: Exposes `get_job_logger(job_id, job_dir)`, which returns a dedicated, isolated logger writing straight to `storage/jobs/{job_id}/logs/pipeline.log`.
3. **Traceback Capture**: Propagates warnings and traceback stack traces to files to ensure pipeline diagnostics are permanently preserved for audit.
