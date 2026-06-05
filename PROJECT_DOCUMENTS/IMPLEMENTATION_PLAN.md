IMPLEMENTATION_PLAN.md

This is the most important Antigravity execution document because Ralph Loop, GSD, and Antigravity will build directly from it.

IMPLEMENTATION_PLAN.md
PathoScope AI Implementation Plan

Version: 1.0

Purpose:

This document defines the exact build order for the entire project.

Critical Rule:

Never build the entire application at once.

Every phase must be completed, tested, verified, and committed before the next phase starts.

DEVELOPMENT METHODOLOGY

The project must follow:

GSD

↓

Phase Planning

↓

Antigravity Execution

↓

Ralph Loop

↓

CodeRabbit Review

↓

Verification

↓

Next Phase

No phase may start until the previous phase passes verification.

PHASE 0 — PROJECT INITIALIZATION

Goal:

Create production-grade repository structure.

Duration:

1 day

Deliverable:

Clean architecture.

Tasks

Create folders:

backend/

frontend/

project-docs/

storage/

docker/

tests/

Backend structure:

backend/

api/

pipeline/

core/

services/

utils/

config/

reports/

tests/

Frontend structure:

frontend/

app/

components/

hooks/

lib/

services/

types/

Create:

.env.example

.gitignore

README.md

docker-compose.yml

Success Criteria:

✓ Structure created

✓ Git initialized

✓ No application code yet

PHASE 1 — DATABASE FOUNDATION

Goal:

Build PostgreSQL schema.

Duration:

1–2 days

Tasks

Setup:

PostgreSQL

SQLAlchemy

Alembic

Implement tables:

users

sessions

jobs

job_steps

uploaded_files

reports

From BACKEND_SCHEMA.md

Verification

Must be able to:

Create User

↓

Create Job

↓

Create Job Step

↓

Update Job Status

Success Criteria

✓ Database operational

✓ Migrations operational

✓ Tables created

✓ Relationships working

PHASE 2 — FASTAPI FOUNDATION

Goal:

Build backend API skeleton.

Duration:

1 day

Create:

app.py

routes.py

config.py

database.py

Endpoints:

GET /health

POST /upload

POST /job/start

GET /job/status

GET /job/results

Verification

Swagger available.

All routes respond.

Success Criteria

✓ FastAPI operational

✓ OpenAPI docs generated

✓ Validation operational

PHASE 3 — JOB MANAGER

Goal:

Create workflow execution system.

MOST IMPORTANT PHASE

Create:

pipeline_runner.py

run_manager.py

Implement:

Job Creation

↓

Step Execution

↓

Step Validation

↓

Progress Tracking

↓

Failure Detection

Required Logic

Run Step

↓

Validate Output

↓

Success

OR

Fail

Never continue on failure.

Verification

Create dummy workflow.

Force failure.

Pipeline stops immediately.

Success Criteria

✓ No fake completion

✓ Accurate status tracking

✓ Failure recovery working

PHASE 4 — FILE VALIDATION SYSTEM

Goal:

Detect workflows automatically.

Create:

validators.py

file_detector.py

Detection Rules

.fasta

.fa

.fna

↓

FASTA Workflow
.fastq

.fastq.gz

↓

FASTQ Workflow
.csv

.tsv

↓

DEG Workflow

Verification

Upload all file types.

Workflow detected correctly.

Success Criteria

✓ Automatic detection works

✓ Invalid files rejected

PHASE 5 — FASTA PIPELINE

Goal:

Build viral genome workflow.

Create:

workflow_fasta.py

Pipeline:

Validation

↓

QC

↓

ORF Detection

↓

Translation

↓

DIAMOND

↓

Pfam

↓

KEGG

↓

Taxonomy

↓

PubMed

↓

AI Interpretation

↓

Reports

Subphase 5.1

QC Module

Implement:

Genome Length

GC %

Ambiguous Bases

Subphase 5.2

ORF Detection

Create:

orf_finder.py

Requirements:

6-frame scanning

Forward strand

Reverse complement strand

Minimum ORF:

100 bp

Subphase 5.3

Translation

Use:

Biopython

Seq.translate()

Must safely handle:

Partial codons

Ambiguous nucleotides

Stop codons

Fix:

KeyError: stop

permanently.

Subphase 5.4

DIAMOND Integration

Create:

diamond_service.py

Thresholds:

E-value <= 1e-5

Identity >= 30%

Coverage >= 50%

Subphase 5.5

Pfam

Create:

hmmer_service.py

Use:

hmmscan

against:

Pfam-A

Subphase 5.6

KEGG

Create:

kegg_service.py

Map proteins to pathways.

Subphase 5.7

Taxonomy

Create:

ncbi_service.py

Retrieve:

TaxID

Lineage

Species

Verification

Real viral FASTA.

Must produce:

ORFs

Proteins

Annotations

Pathways

Taxonomy

PHASE 6 — FASTQ PIPELINE

Goal:

Build production-grade NGS workflow.

Most difficult phase.

Create:

workflow_fastq.py

Step 1

FASTQ Validation

Check:

Format

Compression

Read Integrity

Step 2

FastQC

Create:

fastqc_service.py

Step 3

fastp

Create:

fastp_service.py

Parameters:

Q20

Length >= 50

Step 4

FastQC Recheck

Run again after trimming.

Step 5

SPAdes

Create:

spades_service.py

Use:

--rnaviral

Step 6

Contig Validation

Filter:

Length >= 500 bp

Step 7

Send contigs into FASTA workflow.

Reuse entire FASTA pipeline.

Verification

Real FASTQ file.

Not mock data.

Must survive:

30 MB+

50 MB+

100 MB+

datasets.

PHASE 7 — DEG WORKFLOW

Goal:

Build GEO2R-style analysis.

Create:

workflow_deg.py

deg_engine.py

Pipeline:

Validation

↓

Gene Mapping

↓

FDR Correction

↓

Classification

↓

KEGG

↓

GO

↓

PubMed

↓

AI

↓

Reports

Thresholds

log2FC >= 1

log2FC <= -1

FDR <= 0.05

Verification

Real DEG dataset.

Must generate:

Volcano plot

Enrichment results

Interpretation

PHASE 8 — PUBMED ENGINE

Goal:

Evidence retrieval.

Create:

pubmed_service.py

Use:

NCBI E-Utilities

Retrieve:

PMID

Title

Authors

Journal

Year

Abstract

DOI

Verification

Real PubMed retrieval.

PHASE 9 — AI INTERPRETATION ENGINE

Goal:

Evidence-grounded interpretation.

Create:

ai_service.py

Environment Variables:

OPENAI_API_KEY=

GEMINI_API_KEY=

User manually enters keys.

Stored only in:

.env

AI Inputs

Pipeline Results

PubMed Evidence

AI Output

Computational Findings

Supporting Literature

Biological Interpretation

Confidence Assessment

Limitations

Verification

No hallucinated biology.

Every statement traceable.

PHASE 10 — REPORT GENERATOR

Create:

html_report.py

pdf_report.py

json_report.py

gff3_report.py

Verification

All report formats downloadable.

PHASE 11 — FRONTEND FOUNDATION

Goal:

Generate UI using Google Stitch.

Deliverables:

Dashboard

Workspace

Reports

Settings

Verification

UI renders.

Responsive.

Professional.

PHASE 12 — API INTEGRATION

Connect:

Frontend

↓

FastAPI

Implement:

Real polling.

No fake progress.

Endpoints

/job/status

/job/results

/job/logs

Verification

UI reflects backend exactly.

PHASE 13 — VISUALIZATION LAYER

Build:

Taxonomy Viewer

Pfam Viewer

KEGG Viewer

Volcano Plot

QC Charts

Verification

Real data only.

PHASE 14 — TESTING

Required:

Unit Tests

Integration Tests

Workflow Tests

Biological Validation Tests

End-to-End Tests

Coverage target:

80%+
PHASE 15 — PRODUCTION HARDENING

Add:

Docker

Docker Compose

Redis

Caching

Logging

Error Recovery

Verification

System survives crashes.

Jobs recover.

Logs preserved.

PHASE 16 — FINAL VALIDATION

Project passes only if:

✓ FASTA workflow works

✓ FASTQ workflow works

✓ DEG workflow works

✓ PubMed works

✓ Gemini works

✓ OpenAI works

✓ Reports work

✓ No simulated results

✓ No fake completion

✓ Reproducible outputs

✓ Professor requirements satisfied
