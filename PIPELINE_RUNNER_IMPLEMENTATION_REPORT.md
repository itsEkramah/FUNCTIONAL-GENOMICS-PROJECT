# PIPELINE_RUNNER_IMPLEMENTATION_REPORT.md — Pipeline Runner Implementation Report

> **Document Status**: `FINAL`  
> **Target Module**: `backend/pipeline/pipeline_runner.py`  
> **Development Constraint**: PIPELINE RUNNER ORCHESTRATION IMPLEMENTED — NO WORKFLOW LOGIC  

This document explains the technical implementation of the `pipeline_runner.py` orchestration engine.

---

## 1. EXECUTION LIFECYCLE

The `PipelineRunner` manages pipeline runs in a background thread or asynchronous task context. The lifecycle is mapped through three distinct phases:

1. **Job Initialization**:
   * Renders `create_job(...)` to write a new `Job` row in PostgreSQL with status `QUEUED` and progress `0`.
   * Invokes `register_steps(...)` to prepopulate the list of sequential steps (`JobStep` table) with state `PENDING`.
   * Caches status keys in Redis (`job_status:{job_id} = 'QUEUED'`, `job_progress:{job_id} = '0'`).
2. **Sequential Loop Processing**:
   * Launches `run_job(...)` in the background.
   * Updates Job status to `RUNNING` in PostgreSQL and Redis.
   * Loops through steps sorted by `step_order`.
   * For each step:
     * Sets `JobStep.status = 'RUNNING'` in database.
     * Executes the step function (`step.run_func`).
     * Shuts down database sessions before calling any long-running external executables to prevent connection pool exhaustion.
     * Re-opens the database session to run the validation gate (`step.validate_func`).
     * If validation passes, marks step `COMPLETED` and recalculates progress.
     * If validation fails or tool execution throws an exception, halts the loop and triggers the fail-safe path.
3. **Termination**:
   * On Complete Success: Sets job status to `COMPLETED` and progress to `100` in both database layers.
   * On Failure: Sets job status to `FAILED`, saves the step traceback into `failed_reason` column, sets progress to `0`, and stops.

---

## 2. STATE MACHINE

The pipeline manages a two-tiered state machine:

### Job State Transitions
* `QUEUED` ──► `RUNNING`: Worker begins processing the job.
* `RUNNING` ──► `COMPLETED`: All steps execute and pass validation checks.
* `RUNNING` ──► `FAILED`: Any step fails validation or throws an exception.
* `RUNNING` ──► `CANCELLED`: User requests job termination.

### Step State Transitions
* `PENDING` ──► `RUNNING`: Step execution begins.
* `RUNNING` ──► `COMPLETED`: Step executes successfully and passes validation gates.
* `RUNNING` ──► `FAILED`: Step throws an error or fails validation checks.

---

## 3. ERROR HANDLING & FAIL-SAFE ISOLATION

* **Subprocess Exceptions**: Step execution blocks (`step.run_func`) are wrapped in `try-except` blocks. Any thrown exception (such as `FileNotFoundError`, `TimeoutExpired`, or bad exit codes) is caught by the runner.
* **Checkpoint Fail-Safe**: If validation fails, the runner calls `self._fail_step(...)`. This marks the active step `FAILED`, records the error message, sets the parent Job status to `FAILED`, logs the trace, and updates Redis keys to ensure the frontend reflects the failure. No subsequent steps are run.
* **DB Connection Pool Protection**: Long-running subprocesses (such as SPAdes assembly) can block threads for hours. Holding database connections open during this time will starve the pool. The runner commits and closes its database session before executing `step.run_func`, and opens a new session once completed to evaluate validation results.

---

## 4. VALIDATION CHAIN

Checkpoint validation is mandatory (Execute ──► Validate ──► Continue/Fail). The `PipelineStep` class defines `validate_func`, which:
1. **Verifies File Presence**: Confirms required output files (e.g. `orfs.fasta`, `diamond.tsv`, `scaffolds.fasta`) exist in the job directory.
2. **Verifies File Size**: Rejects files with size = 0.
3. **Verifies Format Integrity**: Checks file headers (e.g., checks GFF3 format syntax, parses JSON schemas).
4. **Verifies Biological Thresholds**: Ensures values (E-value, sequence length, percent identity) fall within the limits defined in `thresholds.py`.

---

## 5. RECOVERY STRATEGY

* **Active Cancellation Checks**: The runner checks the job status in Redis and PostgreSQL (`self._is_cancelled`) before executing each step. If a cancellation is detected, it terminates the pipeline, sets status to `CANCELLED`, and releases resources.
* **Crash Recovery**: If the host system crashes or restarts:
  * Upon restart, the system scans the database for jobs stuck in the `RUNNING` state.
  * It verifies which outputs exist in `storage/jobs/{job_id}/outputs/`.
  * If a job was interrupted mid-step, it is marked `FAILED` with an explanation log, allowing the user to restart it from the last completed step.
