# API_LAYER_REPORT.md — FastAPI API Layer Report

This report outlines the API design, endpoints, request/response models, and asynchronous background worker integration for the FastAPI API layer in PathoScope AI v3.0.

---

## 1. Decoupled Architecture Design

In compliance with design principles, the API layer acts as a thin routing and validation interface. It contains no scientific or pipeline execution logic. It delegates execution to the `PipelineRunner` and background workers.

```
 [Client API Call] ──► [FastAPI Route Validation]
                              │
                    (If validation passes)
                              │
                              ▼
                 [runner.create_job() (DB)]
                              │
                              ▼
                 [runner.register_steps() (DB)]
                              │
                              ▼
             [Add to BackgroundTasks Queue]
                              │
          ┌───────────────────┴───────────────────┐
          ▼                                       ▼
  [Return JSON to Client]               [Asynchronous Execution]
  e.g. { "job_id": "...",                - runner.run_job()
         "status": "QUEUED" }            - Status updates via Redis/DB
```

---

## 2. API Endpoint Specifications

### 1. `/upload` (POST)
* **Description**: Upload sequences (FASTA/FASTQ) or gene expression tables.
* **Payload**: Multipart file stream.
* **Response**:
  ```json
  {
    "file_id": "550e8400-e29b-41d4-a716-446655440000",
    "original_name": "virus.fasta",
    "detected_type": "FASTA",
    "storage_path": "storage/uploads/550e8400-e29b-41d4-a716-446655440000.fasta",
    "file_size": 24050
  }
  ```
* **Validation**: Checks file size limits (e.g. 500MB). Performs basic header scanning (first few lines) to confirm the file matches the extension.

### 2. `/run` (POST)
* **Description**: Queues a new analysis job and launches execution.
* **Request Body**:
  ```json
  {
    "file_path": "storage/uploads/550e8400-e29b-41d4-a716-446655440000.fasta",
    "job_name": "Zika Pathogen Run",
    "workflow_type": "FASTA"
  }
  ```
* **Response**:
  ```json
  {
    "job_id": "8f3b1102-1209-411a-8bb0-ff0f81d11100",
    "status": "QUEUED",
    "progress_percent": 0
  }
  ```
* **Orchestration**: Instantiates pipeline steps, calls `PipelineRunner.create_job()`, registers steps, and triggers background execution via FastAPI `BackgroundTasks`.

### 3. `/status/{job_id}` (GET)
* **Description**: Polling endpoint to retrieve the execution status of a job.
* **Response**:
  ```json
  {
    "job_id": "8f3b1102-1209-411a-8bb0-ff0f81d11100",
    "status": "RUNNING",
    "progress_percent": 36,
    "started_at": "2026-06-04T01:30:00Z",
    "completed_at": null,
    "failed_reason": null,
    "steps": [
      { "step_name": "Input Validation", "status": "COMPLETED", "order": 1 },
      { "step_name": "Sequence QC", "status": "COMPLETED", "order": 2 },
      { "step_name": "ORF Detection", "status": "RUNNING", "order": 3 }
    ]
  }
  ```
* **Caching**: Attempts to query status and progress from Redis keys (`job_status:{job_id}`, `job_progress:{job_id}`) first. If empty, falls back to querying the database.

### 4. `/results/{job_id}` (GET)
* **Description**: Retrieves structured biological output details once the job is completed.
* **Response**:
  ```json
  {
    "job_id": "8f3b1102-1209-411a-8bb0-ff0f81d11100",
    "workflow_type": "FASTA",
    "qc_metrics": { "genome_length": 10800, "gc_content": 48.2, "ambiguity_count": 0 },
    "orfs_count": 8,
    "annotations": [
      { "query_protein": "ORF_1", "subject_protein": "NP_040608.1", "identity": 98.4, "evalue": 1e-45 }
    ],
    "pfam_domains": [
      { "protein_id": "ORF_1", "pfam_accession": "PF00948", "pfam_name": "Flavi_NS5" }
    ],
    "kegg_pathways": [
      { "pathway_id": "map05168", "pathway_name": "Viral Entry / Replication" }
    ],
    "taxonomy": { "tax_id": 10244, "organism_name": "Zika virus", "lineage": ["Viruses", "Riboviria"] },
    "ai_interpretation": {
      "findings": "Zika virus genome...",
      "evidence": "Homology matches with NP_040608.1 (e-value: 1e-45). PMID:26886450",
      "interpretation": "Pathogen identified as Zika virus...",
      "confidence": "HIGH",
      "limitations": "Analysis based on in silico translation."
    }
  }
  ```

### 5. `/reports/{job_id}` (GET)
* **Description**: Downloads the compiled files in GFF3, HTML, PDF, CSV, or JSON format.
* **Parameters**: `format=HTML` (defaults to HTML).
* **Response**: Static file response (`FileResponse`). Returns content with matching MIME type (`text/html`, `application/pdf`, `text/plain`, etc.).

### 6. `/settings` (GET)
* **Description**: Returns environment keys status and configuration thresholds.
* **Response**:
  ```json
  {
    "api_availability": {
      "openai": true,
      "gemini": false
    },
    "thresholds": {
      "MIN_ORF_LENGTH_BP": 100,
      "DIAMOND_EVALUE_MAX": 1e-5,
      "DIAMOND_IDENTITY_MIN": 30.0,
      "DIAMOND_COVERAGE_MIN": 50.0,
      "FASTQ_QUALITY_PHRED": 20,
      "FASTQ_READ_LENGTH_MIN": 50,
      "FASTQ_CONTIG_LENGTH_MIN": 500,
      "DEG_FDR_MAX": 0.05,
      "DEG_LOG2FC_UP": 1.0,
      "DEG_LOG2FC_DOWN": -1.0,
      "PATHWAY_SIZE_MIN": 15,
      "PATHWAY_SIZE_MAX": 500
    }
  }
  ```

---

## 3. Asynchronous Execution Lifecycle

1. Client sends request to `/run`.
2. Router verifies database connection, checks file exists in upload registry.
3. Router initializes `Job` model (`status="QUEUED"`) and inserts steps in `JobStep` model.
4. Router schedules `BackgroundTasks.add_task(runner.run_job, job_id, steps)` and returns immediately.
5. In the background task thread, `PipelineRunner.run_job` updates status to `RUNNING` in PostgreSQL and updates status/progress keys in Redis.
6. The thread executes steps sequentially, checking for cancellation events between steps.
7. Upon successful step verification, database progress is updated, and status update is published to Redis channel `job_updates:{job_id}`.
8. If a step fails, the thread logs the traceback, sets the step and job statuses to `FAILED` with the reason, and terminates immediately.
