BLUEPRINT.md
=
System Engineering Manual



# BLUEPRINT.md

# PathoScope AI System Engineering Blueprint

Version: 1.0

Status: Production Architecture Specification

Authoritative Reference:
MASTER_BLUEPRINT.md

---

# 1. PURPOSE

This document defines the complete engineering architecture of PathoScope AI.

It serves as the primary technical blueprint for:

* Antigravity
* GSD
* Ralph Loop
* CodeRabbit
* Human developers

The document describes:

* Folder structure
* Execution flow
* Pipeline orchestration
* Biological workflows
* Service integrations
* Data flow
* Validation rules
* Failure handling
* Deployment strategy

No implementation details should violate this document.

---

# 2. SYSTEM OVERVIEW

PathoScope AI is composed of five major subsystems.

Subsystem A

Frontend Layer

Purpose:

User interaction.

Responsibilities:

* File upload
* Workflow configuration
* Progress display
* Results visualization
* Report download

The frontend performs no biological analysis.

---

Subsystem B

API Layer

Purpose:

Request handling.

Responsibilities:

* Authentication
* Upload management
* Workflow initiation
* Status retrieval
* Report delivery

The API never performs biological calculations.

---

Subsystem C

Pipeline Layer

Purpose:

Workflow orchestration.

Responsibilities:

* Run workflows
* Track execution
* Validate outputs
* Stop on failure

This layer controls execution order.

---

Subsystem D

Biological Engine Layer

Purpose:

Scientific computation.

Responsibilities:

* QC
* ORF prediction
* Translation
* Annotation
* DEG analysis
* Pathway mapping

This layer contains the biological logic.

---

Subsystem E

Evidence Layer

Purpose:

Scientific grounding.

Responsibilities:

* PubMed retrieval
* Evidence ranking
* Citation storage
* Literature support

This layer supplies evidence to AI interpretation.

---

# 3. HIGH LEVEL DATA FLOW

User Upload

↓

API Validation

↓

Pipeline Runner

↓

Workflow Selection

↓

Biological Processing

↓

Result Validation

↓

PubMed Retrieval

↓

AI Interpretation

↓

Report Generation

↓

Frontend Visualization

---

# 4. PROJECT DIRECTORY STRUCTURE

backend/

api/

pipeline/

core/

services/

reports/

storage/

utils/

config/

tests/

frontend/

src/

public/

components/

hooks/

pages/

styles/

project-docs/

clones/

---

# 5. CONFIGURATION ARCHITECTURE

All thresholds originate from a single source.

backend/config/

config.yaml

thresholds.yaml

tool_paths.yaml

env_loader.py

No module may hardcode thresholds.

Every workflow imports thresholds from config.

---

# 6. PIPELINE RUNNER DESIGN

pipeline_runner.py

Purpose:

Central orchestration engine.

The runner is the only component allowed to execute workflows.

No workflow may self-execute.

No API endpoint may directly execute tools.

All execution passes through pipeline_runner.

---

# 7. PIPELINE EXECUTION STATES

State 1

QUEUED

Job accepted.

Waiting for execution.

---

State 2

RUNNING

Workflow executing.

---

State 3

COMPLETED

All validations passed.

---

State 4

FAILED

Execution stopped.

---

State 5

CANCELLED

User terminated workflow.

---

# 8. PIPELINE VALIDATION MODEL

Every step follows:

Execute

↓

Validate Output

↓

Continue

OR

Fail

Validation is mandatory.

No exceptions.

---

Example:

FastQC

↓

Verify Report Exists

↓

Verify Report Non-Empty

↓

Continue

Otherwise

↓

Fail Workflow

---

# 9. FASTA WORKFLOW ENGINE

workflow_fasta.py

Purpose:

Analyze viral genome FASTA files.

Input:

FASTA

FNA

FA

Output:

Annotated viral genome report

---

Step 1

Input Validation

Checks:

Valid FASTA

Non-empty sequence

Valid nucleotide characters

---

Step 2

Sequence QC

Calculate:

Length

GC%

N%

Ambiguous bases

---

Step 3

ORF Detection

Six frame scanning

Frames:

+1
+2
+3
-1
-2
-3

---

Step 4

ORF Filtering

Threshold:

≥100 bp

---

Step 5

Translation

Convert DNA → protein

Using Biopython

---

Step 6

DIAMOND Annotation

Database:

SwissProt

Output:

Top hits

Identity

Coverage

E-value

---

Step 7

Pfam Domain Search

Database:

Pfam-A

Output:

Protein domains

---

Step 8

KEGG Mapping

Output:

Functional categories

---

Step 9

NCBI Taxonomy

Output:

Lineage

Species

Taxonomic tree

---

Step 10

Result Validation

Verify:

ORFs generated

Annotation completed

Reports generated

---

# 10. FASTQ WORKFLOW ENGINE

workflow_fastq.py

Purpose:

Process raw sequencing reads.

Input:

FASTQ

FASTQ.GZ

---

Step 1

Upload Validation

---

Step 2

FastQC

Raw reads

---

Step 3

fastp

Filtering

Adapter removal

Q20 enforcement

Length filtering

---

Step 4

FastQC

Post-trimming

---

Step 5

SPAdes Assembly

Optional

---

Step 6

Contig Validation

---

Step 7

Pass Contigs To FASTA Workflow

---

# 11. DEG WORKFLOW ENGINE

workflow_deg.py

Purpose:

GEO2R-style transcriptomics analysis.

Input:

CSV

TSV

Required Columns:

gene_id

log2FoldChange

pvalue

---

Step 1

Validate Columns

---

Step 2

Gene ID Normalization

HGNC

Ensembl

Entrez

---

Step 3

FDR Correction

Benjamini-Hochberg

---

Step 4

Classification

UP

DOWN

NON-SIGNIFICANT

---

Step 5

KEGG Enrichment

---

Step 6

GO Enrichment

---

Step 7

Volcano Plot

---

Step 8

Result Validation

---

# 12. PUBMED EVIDENCE ENGINE

Purpose:

Ground AI interpretation.

No interpretation may occur without evidence.

---

Workflow

Annotation Results

↓

Query Generator

↓

PubMed Search

↓

Evidence Ranking

↓

Evidence Bundle

↓

AI Interpretation

---

# 13. PUBMED QUERY GENERATOR

Query Sources

Protein Name

Pfam Domain

KEGG Pathway

Taxonomic Organism

Gene Symbol

The generator creates ranked search terms.

---

# 14. PUBMED EVIDENCE CACHE

storage/pubmed/

run_id/

Stores:

PMIDs

Abstracts

Queries

Evidence scores

This prevents repeated API calls.

---

# 15. AI INTERPRETATION ENGINE

Supported Models

Gemini

OpenAI

Keys loaded from:

.env

Variables:

GEMINI_API_KEY

OPENAI_API_KEY

Never exposed to frontend.

---

# 16. AI INTERPRETATION FORMAT

Section 1

Computational Findings

Section 2

Literature Evidence

Section 3

Biological Meaning

Section 4

Confidence

Section 5

Limitations

---

# 17. REPORT GENERATION SYSTEM

Formats

HTML

PDF

CSV

JSON

GFF3

Reports must be reproducible.

---

# 18. ERROR HANDLING STRATEGY

Failure Types

Validation Failure

Tool Failure

Parsing Failure

Network Failure

Database Failure

AI Failure

PubMed Failure

Every failure must:

Log

Store diagnostics

Return error

Stop pipeline

---

# 19. LOGGING STRATEGY

Every step logs:

Start Time

End Time

Status

Output

Errors

Resource Usage

Logs stored permanently.

---

# 20. TESTING STRATEGY

Unit Tests

Integration Tests

Workflow Tests

End-to-End Tests

Biological Validation Tests

Every workflow must have test datasets.

---

# 21. DEPLOYMENT TARGET

Primary:

Local Deployment

Student Workstation

16GB RAM

GTX 1660 Super

Ryzen 5 5600

Secondary:

Linux Server

Cloud VM

University Server

---

# 22. SUCCESS CRITERIA

The project is considered complete when:

FASTA workflow processes real genomes.

FASTQ workflow processes real reads.

DEG workflow produces valid enrichment results.

PubMed evidence retrieval functions correctly.

AI interpretation is evidence-based.

Reports are reproducible.

Frontend displays real backend progress.

No simulated execution exists anywhere in the system.
