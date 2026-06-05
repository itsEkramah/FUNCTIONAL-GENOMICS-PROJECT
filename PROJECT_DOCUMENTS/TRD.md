TRD.md
Technical Requirements Document
Project Name

PathoScope AI

Automated Viral Functional Genomics Pipeline for Sequence Annotation, Pathway Mapping, and AI-Assisted Biological Interpretation

1. Purpose

This document defines the complete technical architecture of PathoScope AI.

This document serves as the engineering contract for:

Antigravity
GSD
Ralph Loop
CodeRabbit
Human Developers

All implementation decisions must follow this document.

If implementation conflicts with this document:

TRD wins.

2. High-Level Architecture

The system follows a strict decoupled architecture.

Browser

↓

Next.js Frontend

↓

FastAPI Backend

↓

Pipeline Runner

↓

Bioinformatics Services

↓

Databases / Reports

↓

PubMed Engine

↓

AI Interpretation Engine

No component may bypass this flow.

3. Technology Stack
Frontend

Framework:

Next.js 15

Language:

TypeScript

UI Components:

shadcn/ui

Styling:

Tailwind CSS

Charts:

Recharts

Icons:

Lucide React

File Upload:

React Dropzone

State Management:

TanStack Query
Backend

Framework:

FastAPI

Language:

Python 3.12+

Validation:

Pydantic

Server:

Uvicorn
Database

Primary Database:

PostgreSQL

Reason:

Reliable
Structured
Production ready
Cache Layer
Redis

Purpose:

Job status caching
Progress updates
PubMed cache
ORM
SQLAlchemy
Migration Tool
Alembic
4. Bioinformatics Tool Stack
FASTQ QC

Tool:

FastQC

Purpose:

Raw quality control

Read Trimming

Tool:

fastp

Purpose:

Adapter trimming
Quality filtering
Length filtering
Assembly

Tool:

SPAdes

Mode:

--rnaviral
Protein Annotation

Tool:

DIAMOND

Mode:

blastp
Domain Prediction

Tool:

HMMER

Database:

Pfam-A
Pathway Mapping

Tool:

KEGG Mapping Service
Taxonomy

Source:

NCBI Taxonomy
Literature Retrieval

Source:

PubMed

API:

NCBI E-Utilities
5. AI Architecture

Supported Models:

Gemini

Provider:

Google Gemini API
OpenAI

Provider:

OpenAI API
6. API Key Management

Keys must NEVER be hardcoded.

Keys must NEVER be committed.

Keys must NEVER appear in frontend.

.env Structure
OPENAI_API_KEY=

GEMINI_API_KEY=

POSTGRES_USER=

POSTGRES_PASSWORD=

POSTGRES_DB=

POSTGRES_HOST=

POSTGRES_PORT=

REDIS_HOST=

REDIS_PORT=
AI Service Behavior

If Gemini key exists:

Gemini available

If OpenAI key exists:

OpenAI available

If both exist:

User may select provider

If neither exists:

AI interpretation disabled

Pipeline still functions

7. Backend Folder Architecture
backend/

api/

pipeline/

core/

services/

utils/

config/

reports/

storage/

tests/
8. API Layer Design

Folder:

backend/api

Responsibilities:

Routing
Validation
Authentication
File uploads
Job status

Forbidden:

ORF detection
QC analysis
Annotation logic
9. Pipeline Layer Design

Folder:

backend/pipeline

Responsibilities:

Workflow orchestration
Status tracking
Validation
Error handling

Files:

workflow_fasta.py

workflow_fastq.py

workflow_deg.py

pipeline_runner.py
10. Core Layer Design

Folder:

backend/core

Contains:

orf_finder.py

translator.py

qc_engine.py

deg_engine.py

taxonomy_parser.py

Purpose:

Pure biological computation

11. Service Layer Design

Folder:

backend/services

Purpose:

External tool wrappers

Files:

fastqc_service.py

fastp_service.py

spades_service.py

diamond_service.py

hmmer_service.py

kegg_service.py

ncbi_service.py

pubmed_service.py

ai_service.py
12. Pipeline Runner Architecture

Most critical component.

File:

pipeline_runner.py

Responsibilities:

Create jobs
Execute workflow steps
Validate outputs
Update status
Stop on failure

Execution Model:

Run Step

↓

Validate Output

↓

Pass

or

Fail

No step may continue without validation.

13. Job Execution Strategy

Every analysis gets:

job_id

Example:

JOB_2026_00001

Job Folder:

storage/jobs/

JOB_ID/

Contains:

inputs/

outputs/

logs/

reports/
14. FASTA Workflow Technical Design

Input:

.fasta

.fa

.fna

Execution:

Input Validation

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

15. FASTQ Workflow Technical Design

Input:

.fastq

.fastq.gz

Execution:

Validation

↓

FastQC

↓

fastp

↓

FastQC

↓

SPAdes

↓

Contig Validation

↓

FASTA Workflow

Streaming support mandatory.

16. DEG Workflow Technical Design

Input:

CSV

TSV

Required Columns:

gene_id

log2FoldChange

pvalue

Execution:

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

AI Interpretation

↓

Reports

17. PubMed Architecture

Service:

pubmed_service.py

Uses:

NCBI E-Utilities

Endpoints:

esearch.fcgi

esummary.fcgi

efetch.fcgi

Stored Data:

PMID

Title

Authors

Journal

Abstract

Year

DOI

18. PubMed Caching

Storage:

Redis

Purpose:

Avoid repeated requests

Reduce API load

Improve speed

19. AI Interpretation Architecture

Input:

Validated biological outputs

PubMed evidence

Output:

Structured interpretation

Template:

Computational Findings

Supporting Literature

Biological Interpretation

Confidence Assessment

Limitations

Hallucination prevention mandatory.

20. Report Generation Architecture

Folder:

backend/reports

Formats:

HTML

PDF

CSV

JSON

GFF3

Every report contains:

Inputs

Methods

Thresholds

Results

Evidence

Limitations

21. Frontend Architecture

Framework:

Next.js

Responsibilities:

Upload files

View status

Display results

Download reports

Forbidden:

Biological computation

22. Frontend Pages
/

dashboard

fasta-analysis

fastq-analysis

deg-analysis

reports

settings

documentation
23. Frontend Components

Upload Components

Progress Components

Taxonomy Viewer

Pfam Viewer

KEGG Viewer

Volcano Plot Viewer

AI Interpretation Viewer

Report Viewer

24. Progress Tracking Design

Frontend never guesses progress.

Progress source:

GET /jobs/{job_id}/status

Backend authoritative.

25. Logging Architecture

Store:

Start Time

End Time

Status

Error

Resource Usage

Tool Output

Location:

storage/logs/
26. Testing Architecture

Required:

Unit Tests

Integration Tests

Workflow Tests

End-to-End Tests

Biological Validation Tests

27. Deployment Strategy

Development:

Local Machine

Production:

Linux Server

Ubuntu 24.04

Containerization:

Docker

Docker Compose

Future:

Kubernetes

Not MVP

28. Hardware Constraints

Target Development Machine:

Ryzen 5 5600

16 GB RAM

GTX 1660 Super

System must remain usable on this hardware.

Avoid:

loading huge files fully into memory
unnecessary duplication
expensive AI calls
29. Security Requirements

API keys encrypted

Passwords hashed

Input validation mandatory

Rate limiting enabled

File type validation mandatory

No arbitrary code execution

30. Technical Acceptance Criteria

System accepted only if:

✓ Real FASTA workflow works

✓ Real FASTQ workflow works

✓ Real DEG workflow works

✓ PubMed integration works

✓ Gemini integration works

✓ OpenAI integration works

✓ Reports reproducible

✓ Backend status accurate

✓ No simulated processing

✓ No fake outputs

✓ Architecture follows MASTER_BLUEPRINT.md and PROJECT_RULES.md