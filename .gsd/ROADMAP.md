---
milestone: PathoScope AI v3.0
version: 3.0.0
updated: 2026-06-03T23:53:00Z
---

# Roadmap

> **Current Phase:** Done
> **Status:** completed

## Must-Haves (from SPEC)

- [x] Configuration of biological constants (`config.py`)
- [x] Input detector routing files (`core/input_detector.py`)
- [x] FASTA ORF predictor using BioPython (`workflow_a/orf_predictor.py`)
- [x] ORA enrichment engine using Fisher's Exact Test (`workflow_b/ora_engine.py`)
- [x] NGS fastp runner (`workflow_c/fastp_runner.py`)
- [x] Pipeline runner with verification checkpoints (`pipeline/pipeline_runner.py`)
- [x] FastAPI endpoints with chunk-streaming and SSE (`api/routes.py`)

---

## Phases

### Phase 1: Foundation and Input Routing
**Status:** ✅ Complete
**Objective:** Define global biological constants and build structural file routing detector.
**Requirements:** Task 1, Task 2

**Plans:**
- [x] Plan 1.1: Core configurations and biological constants (`config.py`)
- [x] Plan 1.2: Header-based input detector (`core/input_detector.py`)

---

### Phase 2: Core Analysis Workflows
**Status:** ✅ Complete
**Objective:** Implement the three primary biological analysis workflows: FASTA annotations, Over-Representation Analysis, and NGS fastp preprocessing.
**Depends on:** Phase 1
**Requirements:** Task 3, Task 4, Task 5

**Plans:**
- [x] Plan 2.1: ORF Predictor (`workflow_a/orf_predictor.py`)
- [x] Plan 2.2: ORA Enrichment Engine (`workflow_b/ora_engine.py`)
- [x] Plan 2.3: fastp Runner and Parser (`workflow_c/fastp_runner.py`)

---

### Phase 3: Pipeline Integration
**Status:** ✅ Complete
**Objective:** Orchestrate the workflows into a unified pipeline runner with checkpointing and verification.
**Depends on:** Phase 2
**Requirements:** Task 6

**Plans:**
- [x] Plan 3.1: Pipeline Runner Orchestrator (`pipeline/pipeline_runner.py`)

---

### Phase 4: API & Streaming Endpoints
**Status:** ✅ Complete
**Objective:** Expose the pipeline orchestration via a decoupled FastAPI backend with chunk-streaming and SSE progress reporting.
**Depends on:** Phase 3
**Requirements:** Task 7

**Plans:**
- [x] Plan 4.1: FastAPI Server and Streaming Endpoints (`api/routes.py`)

---

## Progress Summary

| Phase | Status | Plans | Complete |
|-------|--------|-------|----------|
| 1     | ✅      | 2/2   | 100%     |
| 2     | ✅      | 3/3   | 100%     |
| 3     | ✅      | 1/1   | 100%     |
| 4     | ✅      | 1/1   | 100%     |

---

## Timeline

| Phase | Started | Completed | Duration |
|-------|---------|-----------|----------|
| 1     | 2026-06-03 | 2026-06-04 | 1 day    |
| 2     | 2026-06-04 | 2026-06-05 | 1 day    |
| 3     | 2026-06-05 | 2026-06-05 | <1 day   |
| 4     | 2026-06-05 | 2026-06-06 | 1 day    |
