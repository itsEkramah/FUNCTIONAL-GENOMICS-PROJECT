# PLAN.md — Technical Specification and Implementation Plan

This plan outlines the architecture, tasks, and verification gates for building **PathoScope AI v3.0**.

Structure:

Phase 1
Foundation

Phase 2
Database

Phase 3
Pipeline Runner

Phase 4
FASTA Workflow

Phase 5
FASTQ Workflow

Phase 6
DEG Workflow

Phase 7
PubMed

Phase 8
AI

Phase 9
API

Phase 10
Frontend

Phase 11
Testing

Phase 12
Deployment
---

## Technical Architecture

```
PathoScope AI v3.0
├── config.py                  # Hardcoded biological thresholds and constants
├── core/
│   └── input_detector.py      # File type routing via structural header checks
├── workflow_a/
│   └── orf_predictor.py       # FASTA genome ORF prediction (BioPython)
├── workflow_b/
│   └── ora_engine.py          # GEO2R transcriptomics Over-Representation Analysis
├── workflow_c/
│   └── fastp_runner.py        # Real-time NGS FASTQ preprocessing via fastp JSON parser
├── pipeline/
│   └── pipeline_runner.py     # Pipeline orchestrator with checkpoint output validation
└── api/
    └── routes.py              # FastAPI endpoints, chunk-streaming, & SSE updates
```

---

## Tasks

### Wave 1: Foundation and Routing

<task type="auto">
  <name>Create config.py</name>
  <files>
    config.py
  </files>
  <action>
    Create a configuration file to house all hardcoded biological thresholds and global constants.
    
    Required Constants:
    - MIN_ORF_LENGTH = 100
    - EVALUE = 1e-5
  </action>
  <verify>
    python -c "import config; assert config.MIN_ORF_LENGTH == 100; assert config.EVALUE == 1e-5"
  </verify>
  <done>
    config.py exists and contains the correct, assertable threshold values.
  </done>
</task>

<task type="auto">
  <name>Build core/input_detector.py</name>
  <files>
    core/input_detector.py
  </files>
  <action>
    Create a file detector that inspects structural headers of uploaded files to route them to the appropriate workflow.
    
    Detection Rules:
    - Starts with `>`: FASTA (Workflow A)
    - Starts with `@`: FASTQ (Workflow C)
    - Starts with custom text headers (e.g. `Gene`, `ID`, `Expression`): TSV/CSV Expression table (Workflow B)
  </action>
  <verify>
    python -c "from core.input_detector import detect_file_type; assert detect_file_type('>seq\nATGC') == 'FASTA'; assert detect_file_type('@seq\nATGC\n+\n####') == 'FASTQ'"
  </verify>
  <done>
    `detect_file_type` successfully distinguishes and returns 'FASTA', 'FASTQ', or 'EXPRESSION' based on head inspection.
  </done>
</task>

---

### Wave 2: Analysis Workflows

<task type="auto">
  <name>Build workflow_a/orf_predictor.py</name>
  <files>
    workflow_a/orf_predictor.py
  </files>
  <action>
    Implement Open Reading Frame (ORF) prediction from FASTA sequence.
    Use BioPython's Seq object translation.
    
    Requirements:
    - Translate codon sequences using `to_stop=True`.
    - Filter translation results with a length threshold of `MIN_ORF_LENGTH` (imported from `config.py`).
  </action>
  <verify>
    python -c "from workflow_a.orf_predictor import predict_orfs; print('ORF predictor module imported successfully')"
  </verify>
  <done>
    `predict_orfs` returns identified protein sequences larger than the minimum threshold.
  </done>
</task>

<task type="auto">
  <name>Build workflow_c/fastp_runner.py</name>
  <files>
    workflow_c/fastp_runner.py
  </files>
  <action>
    Create a subprocess wrapper to run fastp on FASTQ files.
    
    Requirements:
    - Invoke fastp via subprocess and capture the output JSON file.
    - Parse fastp JSON output to extract quality metrics (e.g. total_reads, q30_rate).
  </action>
  <verify>
    python -c "from workflow_c.fastp_runner import run_fastp; print('fastp runner module imported successfully')"
  </verify>
  <done>
    `run_fastp` successfully wraps fastp execution and parses the results.
  </done>
</task>

<task type="auto">
  <name>Build workflow_b/ora_engine.py</name>
  <files>
    workflow_b/ora_engine.py
  </files>
  <action>
    Implement GEO2R-style transcriptomics enrichment engine.
    
    Requirements:
    - Implement the one-sided Fisher's Exact Test using scipy.stats.fisher_exact.
    - Compute p-values for overlapping target genes and background sets.
  </action>
  <verify>
    python -c "from workflow_b.ora_engine import run_ora; print('ORA engine module imported successfully')"
  </verify>
  <done>
    `run_ora` calculates statistical enrichment of gene sets.
  </done>
</task>

---

### Wave 3: Integration and API

<task type="auto">
  <name>Build pipeline/pipeline_runner.py</name>
  <files>
    pipeline/pipeline_runner.py
  </files>
  <action>
    Orchestrate the individual workflows.
    
    Requirements:
    - Detect incoming file type via `input_detector.py`.
    - Run the corresponding workflow module.
    - Verify output files at each step against strict checkpoints (e.g. file size > 0, formats are correct).
  </action>
  <verify>
    python -c "from pipeline.pipeline_runner import PipelineRunner; print('Pipeline runner module imported successfully')"
  </verify>
  <done>
    Pipeline orchestrator processes files and verifies output stages sequentially.
  </done>
</task>

<task type="auto">
  <name>Build api/routes.py</name>
  <files>
    api/routes.py
  </files>
  <action>
    Expose endpoints using FastAPI.
    
    Endpoints Required:
    - `/upload`: Asynchronous chunk-streaming file upload endpoint.
    - `/progress`: Server-Sent Events (SSE) progress update channel routing pipeline status.
  </action>
  <verify>
    python -c "from api.routes import app; print('FastAPI app imported successfully')"
  </verify>
  <done>
    FastAPI routing is functional and SSE streams correctly.
  </done>
</task>
