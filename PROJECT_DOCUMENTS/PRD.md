# Product Requirement Document (PRD) — Task List

This log tracks the requirements and success criteria for each coding module in the PathoScope AI v3.0 pipeline.

---

## Tasks

### Task 1: Global Configurations
- **File**: `config.py`
- **Goal**: Create a configuration file containing all hardcoded biological constants.
- **Success Criteria**: Define constants `MIN_ORF_LENGTH=100` and `EVALUE=1e-5`.

### Task 2: File Routing and Input Detection
- **File**: `core/input_detector.py`
- **Goal**: Route files based on structural header inspection.
- **Success Criteria**: Inspect headers and identify files starting with `>` as FASTA, `@` as FASTQ, and table headers (e.g. `Gene`, `ID`) as Expression data.

### Task 3: ORF Prediction
- **File**: `workflow_a/orf_predictor.py`
- **Goal**: Predict ORFs using BioPython translation.
- **Success Criteria**: Perform native translation with `to_stop=True` and filter by `MIN_ORF_LENGTH`.

### Task 4: NGS Quality Control Runner
- **File**: `workflow_c/fastp_runner.py`
- **Goal**: Execute and parse fastp.
- **Success Criteria**: Use subprocess wrappers to run fastp and parse the resulting JSON metrics (e.g. Q30 rate).

### Task 5: Over-Representation Analysis
- **File**: `workflow_b/ora_engine.py`
- **Goal**: Implement GEO2R-style ORA engine.
- **Success Criteria**: Perform a one-sided Fisher's Exact Test using scipy.stats to calculate enrichment p-values.

### Task 6: Pipeline Runner Orchestrator
- **File**: `pipeline/pipeline_runner.py`
- **Goal**: Orchestrate workflows with output validation.
- **Success Criteria**: Chain routing, execution, and validation of outputs at each step, failing if empty or malformed.

### Task 7: API and Streaming Endpoints
- **File**: `api/routes.py`
- **Goal**: Build FastAPI web endpoints.
- **Success Criteria**: Support async chunk-streaming file uploads and Server-Sent Events (SSE) progress update channels.
