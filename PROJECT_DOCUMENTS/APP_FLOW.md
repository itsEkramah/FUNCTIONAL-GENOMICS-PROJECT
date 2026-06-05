APP_FLOW.md
PathoScope AI Application Flow Specification

Version: 1.0

Authority:

MASTER_BLUEPRINT.md
BLUEPRINT.md
TRD.md
BACKEND_SCHEMA.md
PROJECT_RULES.md
1. PURPOSE

This document defines:

Complete user journey
Navigation structure
Every page
Every button
Every workflow
Every success state
Every error state
Every loading state
Every backend interaction

This document is the source of truth for:

Google Stitch UI generation
Next.js frontend development
Antigravity frontend tasks
API integration planning

No frontend component should be created outside this flow.

2. APPLICATION FLOW OVERVIEW
Landing Page

↓

Dashboard

├── FASTA Analysis
├── FASTQ Analysis
├── DEG Analysis
├── Reports
├── Literature Explorer
├── Settings

↓

Pipeline Execution

↓

Results

↓

AI Interpretation

↓

Report Generation
3. LANDING PAGE

Route:

/

Purpose:

Introduce platform.

Sections:

Hero Section

Contains:

Project title
Short description
Start Analysis button
Features Section

Cards:

Viral Genome Annotation
FASTQ Processing
DEG Analysis
PubMed Integration
AI Interpretation
Report Generation
Architecture Section

Visual workflow:

FASTA

↓

ORF Detection

↓

DIAMOND

↓

Pfam

↓

KEGG

↓

PubMed

↓

AI Interpretation
Footer

Contains:

Documentation
GitHub
Contact

Buttons:

Start Analysis

Action:

Go To Dashboard
4. DASHBOARD

Route:

/dashboard

Purpose:

Main control center.

Dashboard Widgets

Total Jobs

Displays:

Completed Jobs

Running Jobs

Failed Jobs
Workflow Cards

Cards:

Viral Genome Analysis

Button:

Launch Workflow
FASTQ Analysis

Button:

Launch Workflow
DEG Analysis

Button:

Launch Workflow
Literature Explorer

Button:

Open Explorer
Reports

Button:

View Reports
5. FASTA ANALYSIS PAGE

Route:

/fasta-analysis

Purpose:

Run viral genome annotation workflow.

Page Sections

Upload Section

Accept:

.fasta

.fa

.fna

Validation:

File exists

↓

Valid FASTA

↓

Size acceptable

Buttons

Upload Genome

Action:

Upload file

Validate File

Action:

Backend validation

Start Analysis

Action:

Create Job

↓

Start Pipeline

6. FASTA PIPELINE VISUALIZATION

Pipeline Steps Display

1. Input Validation

2. Sequence QC

3. ORF Detection

4. Translation

5. DIAMOND Annotation

6. Pfam Analysis

7. KEGG Mapping

8. Taxonomy Assignment

9. PubMed Retrieval

10. AI Interpretation

11. Report Generation

Each Step Displays:

Pending

Running

Completed

Failed
7. FASTA SUCCESS FLOW
Pipeline Completed

↓

Results Page

↓

Visualization

↓

AI Interpretation

↓

Download Reports
8. FASTA ERROR FLOW

Examples:

Invalid FASTA

Display:

Uploaded file is not a valid FASTA file.
No ORFs Found

Display:

No ORFs above 100 bp detected.
DIAMOND Failure

Display:

Protein annotation step failed.
HMMER Failure

Display:

Pfam domain analysis failed.

Pipeline immediately stops.

No fake completion allowed.

9. FASTQ ANALYSIS PAGE

Route:

/fastq-analysis

Purpose:

Raw sequencing workflow.

Accepted Files

.fastq

.fastq.gz

Supports:

Single End

Paired End

Upload Section

Displays:

File Name

File Size

Detected Type

Buttons

Validate FASTQ

Action:

Run validation

Start Workflow

Action:

Create FASTQ Job

10. FASTQ PIPELINE FLOW

Displayed Workflow:

Input Validation

↓

FastQC (Raw)

↓

fastp Trimming

↓

FastQC (Cleaned)

↓

SPAdes Assembly

↓

Contig Validation

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
11. FASTQ VISUAL COMPONENTS
Raw QC Card

Shows:

Read Count
Mean Quality
GC %
fastp Summary

Shows:

Reads Removed
Reads Retained
Adapter Removal
Assembly Summary

Shows:

Contig Count
Longest Contig
N50
12. FASTQ ERROR STATES
Corrupted GZIP

Display:

Invalid FASTQ.GZ file.
FastQC Failure

Display:

FastQC execution failed.
fastp Failure

Display:

Quality trimming failed.
SPAdes Failure

Display:

Assembly failed.
13. DEG ANALYSIS PAGE

Route:

/deg-analysis

Purpose:

GEO2R-style transcriptomics workflow.

Accepted Files

CSV

TSV

Required Columns

gene_id

log2FoldChange

pvalue

Validation:

All columns present

↓

Data numeric

↓

Proceed

14. DEG PIPELINE FLOW
Input Validation

↓

Gene Mapping

↓

Normalization Check

↓

FDR Correction

↓

Classification

↓

KEGG Enrichment

↓

GO Enrichment

↓

PubMed Retrieval

↓

AI Interpretation

↓

Report Generation
15. DEG VISUALIZATIONS
Volcano Plot

Displays:

Upregulated

Downregulated

Non-significant
Significant Gene Table

Columns:

Gene

log2FC

pvalue

FDR
Enrichment Table

Columns:

Pathway

Gene Count

Pvalue

FDR
16. RESULTS PAGE

Route:

/results/{job_id}

Purpose:

Central results viewer.

Tabs

Overview
QC
ORFs
Annotation
Pfam
KEGG
Taxonomy
PubMed
AI Interpretation
Reports
17. ORF TAB

Displays:

ORF Table

Columns:

ORF ID

Start

End

Frame

Length

Protein Length
ORF Visualization

Genome viewer

Shows:

ORF locations
Strand direction
Coordinates
18. ANNOTATION TAB

Displays:

DIAMOND Hits

Columns:

Protein

Best Match

Identity %

Coverage %

E-value

Bitscore

Filters:

Identity

Coverage

E-value

19. PFAM TAB

Displays:

Protein domains.

Columns:

Protein

Pfam ID

Pfam Name

Start

End

E-value

Visualization:

Domain architecture viewer

20. KEGG TAB

Displays:

Pathway Cards

Each card:

Pathway Name

Gene Count

FDR

Visualization:

Interactive pathway charts

21. TAXONOMY TAB

Displays:

Taxonomy Tree

Hierarchy:

Realm

Kingdom

Phylum

Class

Order

Family

Genus

Species

Interactive expandable tree.

22. PUBMED TAB

Purpose:

Show supporting literature.

Columns:

PMID

Title

Journal

Year

Actions

View Abstract

Open modal

Open PubMed

External link

23. AI INTERPRETATION TAB

Purpose:

Evidence-based interpretation.

Sections

Computational Findings

Generated from:

Pipeline outputs

Supporting Literature

Generated from:

PubMed

Biological Interpretation

Generated from:

AI model

Confidence Assessment

High

Medium

Low

Limitations

Mandatory section.

24. REPORTS PAGE

Route:

/reports

Displays:

All generated reports.

Filters:

Workflow

Date

Status

Actions:

Download HTML
Download PDF
Download JSON
Download CSV
Download GFF3
25. SETTINGS PAGE

Route:

/settings

Purpose:

System configuration.

26. AI SETTINGS

Critical Section

Fields:

Gemini API Key

Stored in:

.env

Never database.

OpenAI API Key

Stored in:

.env

Never database.

UI Behavior:

Key Entered

↓

Backend Validation

↓

Stored In .env

↓

AI Service Activated

Status Indicators

Gemini Connected

Gemini Not Connected

OpenAI Connected

OpenAI Not Connected
27. JOB STATUS SYSTEM

Frontend NEVER simulates progress.

Progress source:

GET /jobs/{job_id}/status

Backend only.

Status Values

Queued

Running

Completed

Failed
28. EMPTY STATES
No Reports

Display:

No reports generated yet.
No Jobs

Display:

No analyses have been run.
No Literature

Display:

No supporting literature found.
29. LOADING STATES

Every page requires:

Skeleton loaders

Progress indicators

Status polling

Never:

Fake progress bars

Fake completion

Simulated waiting

30. APP FLOW ACCEPTANCE CRITERIA

Flow accepted only if:

✓ FASTA workflow fully navigable

✓ FASTQ workflow fully navigable

✓ DEG workflow fully navigable

✓ PubMed integration visible

✓ AI interpretation visible

✓ Reports downloadable

✓ Errors clearly displayed

✓ Backend controls progress

✓ No simulated pipeline behavior

✓ Compatible with Google Stitch UI generation