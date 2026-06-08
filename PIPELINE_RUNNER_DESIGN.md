# PIPELINE_RUNNER_DESIGN.md — Pipeline Runner Design Specification

> **Document Status**: `FINAL`  
> **Target Module**: `backend/pipeline/pipeline_runner.py`  
> **Development Constraint**: NO CODE IMPLEMENTED YET — STRICT ARCHITECTURAL ALIGNMENT PHASE  

---

## 1. OBJECTIVE & BOUNDARIES

The `pipeline_runner.py` is the single authoritative orchestrator of PathoScope AI v3.0. It coordinates the execution of tool wrappers, calculates progress metrics, validates file assets at each checkpoint, and manages database transactions.

### Architectural Rules (From PROJECT_RULES.md)
* **Execution Monopolization**: No API endpoint, service class, or CLI route may execute tools directly. All runs must pass through `pipeline_runner.py` (Rule 2.5).
* **Validation Gate Model**: Every step executes, validates outputs, and either continues or fails. Step warnings immediately fail the entire job. Simulated success or fake progress is strictly prohibited.
* **Connection Protection**: Database connections must be released immediately before invoking long subprocess commands (SPAdes, FastQC) to prevent pool starvation.

---

## 2. EXECUTION LIFECYCLE

The runner manages a job from upload detection through report compilation.

```
       [API Layer]
            │  1. POST /api/v1/job/start
            ▼
┌───────────────────────┐
│  1. INITIALIZATION    │ ──► Parse JOB_ID; Load job metadata from database
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  2. SESSION DECOUPLING│ ──► Commit and close active DB connection pool
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  3. WORKFLOW MAPPING  │ ──► Load step list based on workflow type (FASTA/FASTQ/DEG)
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  4. SEQUENTIAL LOOP   │ ◄─── Repeat for each step in mapping
│   (Execute & Validate)│ ───► Verify output files exist and match thresholds
└───────────┬───────────┘
            │
            ├─── Validation Passed ──► Proceed to next step
            │
            └─── Validation Failed ──► [TRIGGER FAIL-SAFE] ──► Abort loop
            │
            ▼
┌───────────────────────┐
│  5. REPORT GENERATOR  │ ──► Compile HTML, PDF, GFF3, JSON, CSV files
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  6. TERMINATION       │ ──► Re-open DB session, write COMPLETED/FAILED, update Redis
└───────────────────────┘
```

---

## 3. STATE MACHINE & STATUS TRANSITIONS

The runner manages a two-tiered state machine: one at the **Job** level and one at the **Step** level.

### Job Status Transitions
```
              ┌───────────────┐
              │    QUEUED     │  (Created on upload)
              └───────┬───────┘
                      │
                      │  Job begins processing
                      ▼
              ┌───────────────┐
              │    RUNNING    │
              └─────┬───┬─────┘
                    │   │
   Validation fails │   │ All steps succeed
   or error caught  │   │ & validations pass
                    │   └───────────────────────┐
                    ▼                           ▼
            ┌───────────────┐           ┌───────────────┐
            │    FAILED     │           │   COMPLETED   │
            └───────────────┘           └───────────────┘
                    ▲
                    │ User terminates
                    │ mid-execution
            ┌───────┴───────┐
            │   CANCELLED   │
            └───────────────┘
```

#### Transition Table
| Origin State | Event | Target State | DB Updates | Redis Updates |
|--------------|-------|--------------|------------|---------------|
| `None` | File upload detected | `QUEUED` | Insert job row; Set default timestamps | Set `job_status:id = 'QUEUED'` |
| `QUEUED` | Worker thread picks up job | `RUNNING` | Set `started_at = NOW()`; Set `status = 'RUNNING'` | Set `job_status:id = 'RUNNING'`; Set `job_progress:id = 0` |
| `RUNNING` | Validation check fails | `FAILED` | Set `failed_reason = error`; Set `status = 'FAILED'` | Set `job_status:id = 'FAILED'` |
| `RUNNING` | Exception is thrown | `FAILED` | Set `failed_reason = traceback`; Set `status = 'FAILED'` | Set `job_status:id = 'FAILED'` |
| `RUNNING` | All steps complete | `COMPLETED` | Set `completed_at = NOW()`; Set `status = 'COMPLETED'` | Set `job_status:id = 'COMPLETED'`; Set `job_progress:id = 100` |
| `RUNNING` | User terminates job | `CANCELLED` | Set `failed_reason = 'Cancelled by user'`; Set `status = 'CANCELLED'` | Set `job_status:id = 'CANCELLED'` |

---

## 4. VALIDATION GATE & CHECKPOINT SYSTEM

Every tool wrapper must perform post-execution verification. The runner blocks execution unless all checkpoints are verified.

```
       [Execute Service Subprocess]
                    │
                    ▼
       [Check 1: File Presence]
         ├── Missing ──► [Fail Step]
         └── Exists
              │
              ▼
       [Check 2: File Size]
         ├── Size = 0 ──► [Fail Step]
         └── Size > 0
              │
              ▼
       [Check 3: Format Integrity]
         ├── Corrupted ──► [Fail Step]
         └── Valid
              │
              ▼
       [Check 4: Biological Thresholds]
         ├── Out of bounds ──► [Fail Step]
         └── Within bounds
              │
              ▼
       [Check 5: Database Commit]
         ├── DB Transaction Error ──► [Fail Step]
         └── Committed ──► [Proceed to Next Step]
```

### Detailed Validation Requirements

| Step Name | Output Files to Validate | Format / Content Check | Biological Threshold Check |
|-----------|--------------------------|------------------------|----------------------------|
| **Input Validation** | Uploaded file path | FASTA/FASTQ/DEG schema | Length > 0, characters valid |
| **QC (Raw)** | `fastqc_raw.html`, `raw.zip` | Valid ZIP, HTML not empty | Base quality trends > 0 |
| **fastp Trimming** | `trimmed.fastq.gz`, `fastp.json` | Valid GZIP, valid JSON | reads_after_filtering > 0, Q20 minimum |
| **QC (Trimmed)** | `fastqc_trimmed.html`, `trimmed.zip`| Valid HTML, valid ZIP | Base quality post-trimming verified |
| **SPAdes Assembly**| `scaffolds.fasta` | Valid FASTA headers | Total contigs >= 1, N50 > 0 |
| **Contig Filter** | `filtered_contigs.fasta` | Filter out < 500bp contigs | Contig length >= 500bp |
| **ORF Detection** | `orfs.fasta` | Coordinates map to genome | ORF length >= `MIN_ORF_LENGTH_BP` (100) |
| **Translation** | `proteins.fasta` | Valid peptide characters | Protein length = (ORF length / 3) - 1 |
| **DIAMOND** | `diamond.tsv` | Tabular values (qseqid...) | EVALUE <= 1e-5, Identity >= 30%, Coverage >= 50% |
| **HMMER Pfam** | `hmmer.tsv` | Domain alignments parsed | Alignment evalue <= 1e-5 |
| **KEGG Mapping** | `kegg.json` | Valid JSON array | Pathway size: `15 <= pathway <= 500` genes |
| **NCBI Taxonomy** | `taxonomy.json` | Lineage hierarchy JSONB | Taxonomic rank assigned |
| **PubMed Fetch** | `articles.json` | PMIDs match cache | Abstract contains content |
| **AI Interpretation**| `ai_report.json` | 5-section schema (Findings...) | No fake PMIDs, citations must match cache |

---

## 5. ERROR HANDLING & RECOVERY LOGIC

### Error Isolation Model
* **Subprocess timeouts**: Executables (like SPAdes) are run with timeouts (e.g. 2 hours). If a subprocess times out, the runner kills the child process, catches `subprocess.TimeoutExpired`, logs the state, updates the step database to `FAILED`, and sets the job status to `FAILED`.
* **Database Connection Protection**:
  * Before running a tool subprocess, the runner commits and closes the SQLAlchemy session:
    ```python
    db.commit()
    db.close()
    ```
  * After the subprocess terminates, the runner opens a new session to record step status. This prevents database connection leaks during long subprocess runs.

### Recovery Logic (Post-Crash Reconstruction)
* If the FastAPI server restarts due to a crash or power failure:
  * On reboot, a background system recovery script searches for jobs in the database with status `RUNNING` or `QUEUED`.
  * For each interrupted job:
    * It checks the last completed step in `job_steps`.
    * It scans `storage/jobs/{job_id}/outputs/` to verify the presence and integrity of cached files for the completed step.
    * If cached files exist and pass validation checks: the job is marked `FAILED` with a traceback log explaining the system restart, allowing users to restart the job from the last verified checkpoint rather than starting from the beginning.

---

## 6. LOGGING & PROGRESS REPORTING

### Logging Design
* Logs are stored permanently in `storage/jobs/{job_id}/logs/pipeline.log`.
* Log messages use a strict, structured template:
  `[TIMESTAMP] [JOB_ID] [STEP_NAME] [LEVEL] MESSAGE`
* System errors must log: parameters, commands executed, and stack traces.

### Progress Reporting Logic
* The runner calculates job progress using completed step milestones:
  $$\text{Progress \%} = \left( \frac{\text{Completed Steps}}{\text{Total Steps}} \right) \times 100$$
* After a step completes, the runner:
  1. Writes the new progress percentage to PostgreSQL (`jobs` table).
  2. Updates the Redis progress string (`job_progress:{job_id}`).
  3. Publishes a progress update event to Redis Pub/Sub.
* The API layer catches the published Redis Pub/Sub events and streams updates to the client via Server-Sent Events (SSE).
* **Strict Constraint**: Renders progress incrementally. The frontend only displays values sent by the backend. No fake progress increments or simulated completion times are allowed.
