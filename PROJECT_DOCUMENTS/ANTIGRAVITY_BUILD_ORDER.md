ANTIGRAVITY_BUILD_ORDER.md

This is critical.

Antigravity performs much better when exact build order is specified.

Contents:

PHASE 1

Project Skeleton

backend/
frontend/

No functionality.

Only structure.

--------------------------------

PHASE 2

Configuration Layer

settings.py

constants.py

.env support

logging

--------------------------------

PHASE 3

Database Layer

SQLite schema

models

repositories

--------------------------------

PHASE 4

Pipeline Runner

pipeline_runner.py

job tracking

status tracking

failure tracking

--------------------------------

PHASE 5

FASTA Workflow

Input validation

QC

ORF detection

Translation

DIAMOND

Pfam

Taxonomy

--------------------------------

PHASE 6

FASTQ Workflow

FastQC

fastp

SPAdes

Contig filtering

Reuse FASTA workflow

--------------------------------

PHASE 7

DEG Workflow

Validation

FDR

Classification

KEGG

GO

--------------------------------

PHASE 8

PubMed Service

E-Utilities

Caching

Citation generation

--------------------------------

PHASE 9

AI Interpretation

Gemini

OpenAI

Evidence-grounded prompting

--------------------------------

PHASE 10

FastAPI Routes

Upload

Run

Status

Results

--------------------------------

PHASE 11

Frontend

Dashboard

Workspace

Reports

Settings

--------------------------------

PHASE 12

Testing

Unit

Integration

E2E

--------------------------------

PHASE 13

Deployment