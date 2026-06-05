# PIPELINE_RUNNER_AUDIT.md — Pipeline Runner Audit Report

This report documents the verification, state machine correctness, and validation checkpoints of the Pipeline Runner (Phase D) in PathoScope AI v3.0.

---

## 1. System Implementation & Design

The Pipeline Runner (`backend/pipeline/pipeline_runner.py`) orchestrates all bioinformatics workflows using a strict, decoupled gate model.

```
       [Start Job Execution]
                 │
                 ▼
     [Set Job status to RUNNING]
                 │
                 ▼
       [Loop through Steps] ◄──────────────────────┐
                 │                                 │
        (Pre-step cancellation check)              │
                 │                                 │
                 ▼                                 │
       [Set Step status to RUNNING]                │
                 │                                 │
                 ▼                                 │
       [Execute Step run_func()]                   │
                 │                                 │
                 ▼                                 │
      [Execute Step validate_func()]               │
        - Check output file exists                 │
        - Verify content / formats                 │
                 │                                 │
        ┌────────┴────────┐                        │
     Passed             Failed                     │
        │                 │                        │
        ▼                 ▼                        │
 [Set Step status    [Set Step & Job status        │
   to COMPLETED]       to FAILED, log trace,       │
        │              terminate loop]             │
        ▼                 │                        │
  [Update overall         ▼                        │
   Job Progress %]   [Aborted Loop]                │
        │                                          │
        └──────────────────────────────────────────┘
```

---

## 2. Code Compliance & Key Features

* **Step Registration**: Dynamically tracks individual `PipelineStep` instances containing `name`, `order`, `run_func`, and `validate_func` properties.
* **Orchestrated Execution**: Sorts step execution lists by sequence `order` and runs them inside an isolated try/except block.
* **Checkpoint Validation**: Enforces gate validation checks immediately after each step runs. If any checkpoint returns `False` or raises an exception, subsequent steps are marked `PENDING` and are not executed.
* **Redis and Database Sync**: Simultaneously synchronizes progress percentages and status keywords to Redis (publishing to SSE listeners) and the PostgreSQL/SQLite databases.
* **Clean Logging**: Directs standard out and errors into dedicated job folders: `storage/jobs/{job_id}/logs/pipeline.log`.

---

## 3. Verification Log

We executed unit tests designed to evaluate the runner under success and validation failure conditions:

```powershell
python -m pytest tests/unit/test_pipeline_runner.py -v
```

### Execution Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.11.8, pytest-9.0.3, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: G:\LAST FINAL FUNCTIONAL GENOICS PROJECT\FUNCTIONAL GENOMICS PROJECT
plugins: anyio-4.13.0
collected 2 items

tests/unit/test_pipeline_runner.py::test_pipeline_runner_success PASSED  [ 50%]
tests/unit/test_pipeline_runner.py::test_pipeline_runner_validation_failure PASSED [100%]

======================== 2 passed in 67.23s (0:01:07) =========================
```

### Analysis of Test Results:
1. **`test_pipeline_runner_success`**: Confirmed that when all steps complete and validate successfully, the runner advances step-by-step, updates progress percent incrementally, and marks the job `COMPLETED` at `100%`.
2. **`test_pipeline_runner_validation_failure`**: Confirmed that if Step Two fails its `validate_func` checkpoint, the runner stops immediately. Step Three is left in its initial `PENDING` state (never executed), and the job is set to `FAILED`. This matches our professor-required validation gate architecture.
