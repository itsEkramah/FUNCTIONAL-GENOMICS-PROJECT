# PROJECT_STRUCTURE_REPORT.md — Project Structure Report

> **Document Status**: `FINAL`  
> **Authority**: `MASTER_BLUEPRINT.md`  
> **Development Constraint**: NO CODE IMPLEMENTED YET — SKELETON SETUP COMPLETE  

This document explains the organization and responsibilities of the directories and empty files generated for the **PathoScope AI v3.0** workspace.

---

## 1. PROJECT DIRECTORY OVERVIEW

```
PathoScope AI v3.0/
├── backend/                  # Python FastAPI backend codebase
├── frontend/                 # Next.js 15 frontend codebase
├── tests/                    # Testing suites (Unit, Integration, Bio Validation)
├── scripts/                  # Utility scripts for setup, db seeds, and helper tools
└── docs/                     # Operational documentation and user guides
```

---

## 2. BACKEND LAYER SPECIFICATION (`backend/`)

The backend codebase is divided into modular directories separating configuration, database handling, controllers (routers), orchestrators (pipelines), computational engines (core), wrappers (services), and exporters (reports).

### 2.1 root `backend/` files
* `app.py`: Main entry point of the FastAPI application. Sets up CORS, exception handlers, static directory mounts, and routes.
* `database.py`: Establishes SQLAlchemy connection pools, defines sessionmakers, and provides database session context managers.
* `config.py`: Exposes Pydantic-settings objects loading environment variables from `.env` and thresholds from YAML.

### 2.2 `backend/config/`
* `thresholds.yaml`: Authoritative source of biological constant thresholds (e.g. `MIN_ORF_LENGTH`, `EVALUE`, `IDENTITY`, `COVERAGE`).
* `tool_paths.yaml`: Configures path pointers to local external binaries (`fastp`, `FastQC`, `SPAdes`, `diamond`, `hmmscan`).

### 2.3 `backend/api/` (API Routers)
* `auth.py`: Manages user signup, logins, password encryption verification, and JWT session token creation.
* `upload.py`: Handles async chunk-streaming uploads, saves uploaded files to disk, and runs header checks to detect workflows.
* `jobs.py`: Initiates pipelines, exposes progress polling, and retrieves completed output tables.
* `reports.py`: Serves file downloads for compiled HTML, PDF, GFF3, JSON, and CSV reports.
* `settings.py`: Updates system parameters and manages external API keys (`OPENAI_API_KEY`, `GEMINI_API_KEY`).

### 2.4 `backend/pipeline/` (Orchestration Engine)
* `pipeline_runner.py`: Spawns background worker execution loops, manages job status, and forces checkpoints validation gates.
* `workflow_fasta.py`: Coordinates the sequence of the FASTA annotation workflow.
* `workflow_fastq.py`: Coordinates quality trimming, assembly, and hand-off of the FASTQ NGS raw reads workflow.
* `workflow_deg.py`: Coordinates Benjamini-Hochberg calculations, volcanoes, and enrichment mapping for DEG tables.

### 2.5 `backend/core/` (Pure Biological Computation)
* `orf_finder.py`: Handles 6-frame start/stop codon search coordinates and overlap removal on identical strands.
* `translator.py`: Translates DNA codons to amino acids using BioPython, protecting against partial codon anomalies.
* `qc_engine.py`: Computes baseline genome statistics (length, GC%, ambiguous base count).
* `deg_engine.py`: Runs statistical tests, performs Benjamini-Hochberg FDR adjustments, and groups expression classifications.

### 2.6 `backend/services/` (External Tool Wrappers)
* `fastqc_service.py`: Shell subprocess executor for FastQC.
* `fastp_service.py`: Subprocess wrapper for fastp trimming, Q20 checks, and JSON results parser.
* `spades_service.py`: Subprocess wrapper for SPAdes `--rnaviral` assembly.
* `diamond_service.py`: Subprocess wrapper for DIAMOND blastp against SwissProt. Parses TSV output tables.
* `hmmer_service.py`: Subprocess wrapper for HMMER `hmmscan` against Pfam-A.
* `kegg_service.py`: Maps annotated proteins to pathways. Wraps GSEApy enrichment mapping.
* `ncbi_service.py`: Retrieves Taxonomic ranks and lineages from NCBI.
* `pubmed_service.py`: NCBI E-Utilities literature search, metadata fetcher, and local cache manager.
* `ai_service.py`: Builds grounded system prompt instructions and wraps Gemini/OpenAI API requests.

### 2.7 `backend/models/` (SQLAlchemy ORM Mapping)
* `__init__.py`: Database registry file importing all models.
* `base.py`: Defines the SQLAlchemy `Base` declarative mapping class.
* `user.py`: Maps user credentials and active session token schemas.
* `job.py`: Maps jobs states (`status`, `progress_percent`) and sequential steps execution logs.
* `file.py`: Maps file metadata of user uploads.
* `results.py`: Maps summaries for FASTA, FASTQ, and DEG calculations.
* `annotation.py`: Maps alignment matching outputs, Pfam domains, NCBI Taxonomy lineage arrays, and KEGG pathway results.
* `pubmed.py`: Maps caches of literature search terms, PMIDs, and abstracts.
* `ai.py`: Maps generated AI interpretation reports.

### 2.8 `backend/reports/` (Exporters Compiler)
* `base_report.py`: Renders abstract file creation properties.
* `html_report.py`: Compiles self-contained static HTML result dashboards.
* `pdf_report.py`: Renders multi-page PDF documents using ReportLab flowables.
* `csv_report.py`: Exports tab/comma-separated results.
* `gff3_report.py`: Formats calculated ORF coordinates into GFF3 genomics annotation files.

### 2.9 `backend/utils/`
* `file_detector.py`: Inspects file headers to automatically route to FASTA (`>`), FASTQ (`@`), or DEG.
* `logger.py`: Creates a unified logger routing warnings and stack traces to files and standard outputs.

---

## 3. FRONTEND LAYER SPECIFICATION (`frontend/`)

The frontend represents a Next.js 15 single-page workspace application, styled using Tailwind CSS and shadcn/ui components.

### 3.1 `frontend/app/` (Next.js App Router Pages)
* `layout.tsx`: Renders the base HTML shell, imports Inter fonts, and sets up TanStack Query providers.
* `page.tsx`: Redirects user flows directly to the Dashboard or Workspace.
* `dashboard/page.tsx`: Displays analytical KPIs, workflow counts, and pipeline statistics.
* `workspace/page.tsx`: The primary workspace screen housing the dropzone, live terminal execution logs, progressive results panels, and report compilers.
* `reports/page.tsx`: A searchable grid displaying all compiled reports.
* `settings/page.tsx`: Configuration dashboard for OpenAI/Gemini credentials.
* `documentation/page.tsx`: Houses the user manual and validation genomes data.

### 3.2 `frontend/components/` (UI Components)
* `Navbar.tsx`: Persistent header navigation between workspace routes.
* `Dropzone.tsx`: Drag-and-drop file uploader area.
* `PipelineSteps.tsx`: Vertical progress checkmarks tracking execution states.
* `Terminal.tsx`: Console window streaming stdout logs from the pipeline.
* `ResultsViewer.tsx`: Progressive results viewer rendering overview metrics, annotations, and pathways.
* `TaxonomyTree.tsx`: Interactive expandable lineage tree mapping taxonomic ranks.
* `DomainViewer.tsx`: Renders domain architecture maps with hover details.
* `VolcanoPlot.tsx`: Interactive Volcano chart rendering upregulated and downregulated genes.
* `AIReport.tsx`: Renders structured, evidence-based AI interpretations citing PMID links.

### 3.3 `frontend/hooks/`
* `useJobs.ts`: Manages status polling and SSE channel subscriptions.
* `useUpload.ts`: Manages async chunk uploads.

### 3.4 `frontend/services/`
* `api.ts`: Configurations for HTTP requests (using Axios or native Fetch).

### 3.5 `frontend/types/`
* `index.ts`: TypeScript type definitions for Jobs, Steps, Annotations, and Users.

---

## 4. TESTS SPECIFICATION (`tests/`)

* `tests/unit/`: Verifies isolated algorithms (ORF scanner coordinate math, BH corrections, validator parsing).
* `tests/integration/`: Verifies database transaction cascades, API endpoints responding, and subprocess command builders.
* `tests/bio_validation/`: Verifies pipeline correctness on authentic genomics sequences (e.g. Zika virus genomes, raw reads datasets).
