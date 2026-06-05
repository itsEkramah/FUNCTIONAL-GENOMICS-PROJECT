UI_UX_BRIEF.md
PathoScope AI UI/UX Design System Specification

Version: 1.0

Authority:

PRD.md
TRD.md
APP_FLOW.md
MASTER_BLUEPRINT.md
1. DESIGN PHILOSOPHY

PathoScope AI is NOT:

a generic dashboard
a student project UI
a colorful SaaS landing page
a toy bioinformatics website

PathoScope AI MUST feel like:

Illumina BaseSpace
Galaxy Project
Benchling
CLC Genomics Workbench
UCSC Genome Browser
Nextflow Tower
nf-core monitoring dashboard

combined into one modern web application.

The user should immediately feel:

Professional

Scientific

Research-grade

Trustworthy

Computationally intensive

The UI must communicate:

Real analysis is happening.

Real bioinformatics tools are executing.

Real biological results are being generated.

Never create a UI that looks like:

cryptocurrency dashboard
social media app
startup landing page
AI chatbot website
2. DESIGN STYLE

Style:

Scientific Enterprise Platform

Keywords:

Minimal

Professional

High-information density

Research-focused

Dark mode first

Modern bioinformatics

Design Inspiration:

Benchling
Galaxy
Nextflow Tower
Databricks
Grafana
VS Code Dark+
UCSC Genome Browser
3. COLOR SYSTEM

Primary Theme:

Dark Scientific Theme
Background

Primary Background

#0B1120

Deep scientific navy

Secondary Background

#111827

Card Background

#1F2937

Panel Background

#172033
Primary Accent

Scientific Blue

#3B82F6

Used for:

buttons
active tabs
progress indicators
workflow highlights
Secondary Accent

Cyan

#06B6D4

Used for:

pathway visualization
taxonomy
metadata
Success
#10B981

Used for:

completed pipeline steps
passed QC
successful annotation
Warning
#F59E0B

Used for:

incomplete annotation
low confidence findings
Error
#EF4444

Used for:

failed pipeline steps
invalid files
Text

Primary Text

#F9FAFB

Secondary Text

#D1D5DB

Muted Text

#9CA3AF
4. TYPOGRAPHY

Font:

Inter

Fallback:

Roboto

Headings:

Bold

Clear

Scientific

Avoid:

Fancy fonts

Rounded fonts

Decorative fonts
5. MOST IMPORTANT UX DECISION
SINGLE ANALYSIS PAGE

DO NOT create:

Upload Page

↓

Progress Page

↓

Results Page

↓

Report Page

This is bad UX.

Instead:

Create:

Unified Analysis Workspace

Everything happens on ONE PAGE.

User Flow:

Upload File

↓

Detect Workflow

↓

Start Analysis

↓

Live Pipeline Execution

↓

Results Appear

↓

AI Interpretation Appears

↓

Reports Available

ALL ON SAME PAGE

This is EXACTLY how:

Benchling
Nextflow Tower
Databricks

work.

6. AUTOMATIC WORKFLOW DETECTION

Critical Requirement

User uploads file.

Frontend sends metadata to backend.

Backend detects:

.fasta

.fa

.fna

↓

Workflow = FASTA

.fastq

.fastq.gz

↓

Workflow = FASTQ

.csv

.tsv

↓

Workflow = DEG


---

Frontend immediately updates:

```text
Workflow Detected

Viral Genome Analysis

or

Workflow Detected

FASTQ Pipeline

or

Workflow Detected

Transcriptomics DEG Analysis

User NEVER manually chooses workflow.

Backend decides.

Frontend only displays.

7. MAIN ANALYSIS WORKSPACE

Route:

/workspace

This is the MOST IMPORTANT page.

Layout

┌────────────────────────────────────┐

 Header

└────────────────────────────────────┘

┌────────────┬───────────────────────┐

 Upload      Analysis Workspace

 Panel       Results Panel

             Pipeline Panel

             AI Panel

└────────────┴───────────────────────┘
8. LEFT SIDEBAR

Contains:

Upload Area

Drag and drop

Displays:

Filename

File Size

Workflow Type

Upload Time

Buttons:

Start Analysis

Cancel Job
9. CENTER PANEL

Live Pipeline Runner

MOST IMPORTANT VISUALIZATION

Example:

✓ Input Validation

✓ FASTQ Validation

✓ FastQC

✓ fastp

⟳ SPAdes Running

○ ORF Detection

○ Translation

○ DIAMOND

○ Pfam

○ KEGG

○ Taxonomy

○ PubMed

○ AI Interpretation

○ Reports

Colors:

Completed

Green

Running

Blue Pulsing

Queued

Gray

Failed

Red
10. REAL-TIME PIPELINE LOGS

Below workflow.

Live log terminal.

Example:

[INFO]

Running FastQC

[INFO]

FastQC completed

[INFO]

Running fastp

[INFO]

Reads before filtering: 210,000

[INFO]

Reads after filtering: 180,000

Source:

Backend API only.

Never simulated.

11. RESULTS PANEL

Results appear IMMEDIATELY when step finishes.

Not at end.

Example:

After ORF detection:

ORFs Found

128

appears instantly.

After DIAMOND:

Annotated Proteins

103

appears instantly.

After KEGG:

Pathways Found

17

appears instantly.

After PubMed:

Literature Articles

52

appears instantly.

This creates perception of:

Real science

Real progress

Real computation
12. FASTA RESULT LAYOUT

Tabs:

Overview

QC

ORFs

Annotation

Pfam

KEGG

Taxonomy

PubMed

AI Interpretation
13. FASTQ RESULT LAYOUT

Additional Tabs:

Raw QC

Trimmed QC

Assembly

Visual Cards:

Reads

Contigs

GC %

N50

Longest Contig
14. DEG RESULT LAYOUT

Visualizations:

Volcano Plot

Interactive

KEGG Bubble Plot

Interactive

GO Enrichment Plot

Interactive

Significant Gene Table

Searchable

15. TAXONOMY VIEWER

Must look like:

NCBI Taxonomy Browser

Tree Structure:

Realm

└── Kingdom

     └── Phylum

          └── Class

               └── Order

                    └── Family

                         └── Genus

                              └── Species

Collapsible.

Interactive.

16. PFAM VIEWER

Must show:

Protein Domain Architecture

Example:

Protein_1

|----Helicase----|

          |----RNA Polymerase----|

Interactive hover.

17. PUBMED VIEWER

Critical Requirement

Each article card shows:

Title

Authors

Journal

Year

PMID

Buttons:

View Abstract

Open PubMed
18. AI INTERPRETATION PANEL

MOST IMPORTANT SCIENTIFIC FEATURE

Must NEVER look like ChatGPT.

Layout:

Computational Findings

Supporting Literature

Biological Interpretation

Confidence Assessment

Limitations

Each section expandable.

Confidence Badge:

High

Medium

Low
19. REPORT GENERATOR PANEL

Appears automatically.

Buttons:

Download HTML

Download PDF

Download JSON

Download CSV

Download GFF3
20. BACKEND CONNECTION REQUIREMENTS

Google Stitch MUST generate UI assuming:

Backend API is authoritative.

Frontend NEVER:

estimates progress
simulates pipeline
fabricates results
generates fake completion

Every 3 seconds:

Frontend polls:

GET /jobs/{job_id}/status

And:

GET /jobs/{job_id}/results

Backend controls everything.

Frontend only renders.


# 21. GOOGLE STITCH MASTER PROMPT

Paste the entire prompt below into Google Stitch.

---

You are a Senior Bioinformatics Product Designer, Enterprise UX Architect, Scientific Visualization Expert, and Next.js Dashboard Designer.

Design a COMPLETE production-grade web application UI called:

# PathoScope AI

Automated Viral Functional Genomics Pipeline for Sequence Annotation, Pathway Mapping, PubMed Evidence Retrieval, and AI-Assisted Biological Interpretation.

The application must NOT look like a student project.

The application must look comparable to:

* Benchling
* Illumina BaseSpace
* Galaxy Project
* UCSC Genome Browser
* Databricks
* Nextflow Tower
* Grafana Enterprise

The design must feel:

* Scientific
* Professional
* Research-grade
* Enterprise-level
* Modern
* Trustworthy

---

# CRITICAL DESIGN RULE

DO NOT create separate pages for:

* Upload
* Progress
* Results

Instead create ONE unified scientific workspace.

Everything happens on the same page.

Workflow:

Upload File

↓

Auto Detect Workflow

↓

Run Pipeline

↓

Show Live Execution

↓

Show Results As They Arrive

↓

Show PubMed Evidence

↓

Show AI Interpretation

↓

Generate Reports

All inside one workspace.

---

# DARK SCIENTIFIC THEME

Primary Background:

#0B1120

Secondary Background:

#111827

Card Background:

#1F2937

Panel Background:

#172033

Primary Accent:

#3B82F6

Secondary Accent:

#06B6D4

Success:

#10B981

Warning:

#F59E0B

Error:

#EF4444

Primary Text:

#F9FAFB

Secondary Text:

#D1D5DB

Muted Text:

#9CA3AF

---

# TYPOGRAPHY

Font:

Inter

Style:

* clean
* scientific
* modern
* enterprise

Avoid decorative fonts.

---

# APPLICATION LAYOUT

Create a full-screen scientific workspace.

Layout:

Header

↓

Left Sidebar

↓

Main Analysis Workspace

↓

Right Results Panel

Structure:

```text
┌───────────────────────────────────────────────┐
│ Header                                        │
└───────────────────────────────────────────────┘

┌──────────────┬───────────────────┬────────────┐
│ Upload       │ Pipeline Runner   │ Results    │
│ Sidebar      │ + Logs            │ Viewer     │
└──────────────┴───────────────────┴────────────┘
```

Responsive desktop-first design.

---

# HEADER

Show:

PathoScope AI

Subtitle:

Automated Viral Functional Genomics Platform

Top navigation:

* Dashboard
* Workspace
* Reports
* Literature Explorer
* Settings

Right side:

User Profile

Notifications

System Status

---

# LEFT SIDEBAR

Create an Upload Center.

Drag and Drop Area.

Accept:

* FASTA
* FASTQ
* FASTQ.GZ
* CSV
* CSV.GZ
* TSV
* TSV.GZ

Display:

Filename

File Size

Upload Time

Detected Workflow

Buttons:

Validate File

Start Analysis

Cancel Analysis

Clear Workspace

---

# CRITICAL FEATURE

AUTO WORKFLOW DETECTION

When a file is uploaded:

Automatically detect:

FASTA

↓

Viral Genome Workflow

FASTQ

↓

FASTQ Analysis Workflow

CSV / TSV

↓

DEG Transcriptomics Workflow

Display:

Workflow Detected

with a large colored badge.

User should NEVER manually select workflow.

Backend determines workflow.

Frontend displays it.

---

# CENTER PANEL

Create a live pipeline runner.

This is the most important component.

Display workflow steps vertically.

Example:

```text
✓ Input Validation

✓ Quality Control

✓ ORF Detection

⟳ Translation Running

○ DIAMOND Annotation

○ Pfam Analysis

○ KEGG Mapping

○ Taxonomy Assignment

○ PubMed Retrieval

○ AI Interpretation

○ Report Generation
```

Use:

Green = Completed

Blue Pulsing = Running

Gray = Pending

Red = Failed

---

# LIVE TERMINAL PANEL

Below workflow.

Show live logs.

Style:

Scientific terminal.

Example:

```text
[INFO] Running FastQC

[INFO] FastQC Completed

[INFO] Running fastp

[INFO] Reads Before Filtering: 1,200,000

[INFO] Reads After Filtering: 1,050,000
```

Must look like real pipeline execution.

---

# RESULTS PANEL

Results appear progressively.

Do NOT wait for pipeline completion.

Example:

After ORF step:

Card appears:

ORFs Found

128

---

After DIAMOND:

Annotated Proteins

103

---

After KEGG:

Pathways Identified

17

---

After PubMed:

Articles Retrieved

52

Results should dynamically appear as backend completes steps.

---

# FASTA WORKFLOW RESULTS

Create tabs:

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

---

# FASTQ WORKFLOW RESULTS

Additional tabs:

Raw QC

Trimmed QC

Assembly

Display:

Read Count

GC %

Quality Distribution

Contig Count

N50

Longest Contig

Assembly Statistics

---

# DEG WORKFLOW RESULTS

Display:

Volcano Plot

Interactive

KEGG Enrichment Bubble Plot

Interactive

GO Enrichment Plot

Interactive

Significant Gene Table

Searchable

Sortable

---

# TAXONOMY VIEWER

Create a collapsible NCBI-style taxonomy tree.

Example:

```text
Realm

└── Kingdom

    └── Phylum

        └── Class

            └── Order

                └── Family

                    └── Genus

                        └── Species
```

Interactive expand/collapse.

---

# PFAM DOMAIN VIEWER

Visualize domain architecture.

Example:

```text
Protein_1

|----Helicase----|

      |---Polymerase---|
```

Interactive hover tooltips.

---

# PUBMED LITERATURE EXPLORER

Display article cards.

Each card contains:

Title

Authors

Journal

Year

PMID

Buttons:

View Abstract

Open PubMed

Use a professional scientific article layout.

---

# AI INTERPRETATION PANEL

IMPORTANT

Do NOT create a chatbot.

This is NOT ChatGPT.

Create a scientific report viewer.

Sections:

Computational Findings

Supporting Literature

Biological Interpretation

Confidence Assessment

Limitations

Use expandable scientific cards.

Display confidence badge:

High

Medium

Low

---

# REPORT GENERATOR PANEL

Show report cards.

Buttons:

Download HTML

Download PDF

Download JSON

Download CSV

Download GFF3

Display generation status.

---

# SETTINGS PAGE

Create:

AI Provider Configuration

Fields:

Gemini API Key

OpenAI API Key

Status Indicators:

Gemini Connected

OpenAI Connected

Keys are stored in backend .env file.

Never exposed in frontend.

---

# DASHBOARD PAGE

Create scientific KPI cards.

Display:

Total Analyses

Running Jobs

Completed Jobs

Failed Jobs

Recent Reports

Recent Literature Searches

Recent AI Interpretations

Include charts showing:

Workflow Usage

Analysis Trends

Pipeline Performance

---

# DESIGN REQUIREMENTS

Use:

* shadcn/ui
* Tailwind CSS
* Next.js App Router style
* Enterprise dashboard patterns
* Modern scientific UI

Avoid:

* bright colors
* startup landing page style
* glassmorphism
* excessive gradients
* cartoon illustrations
* generic AI chatbot layouts

The final result should look like a professional bioinformatics platform used by researchers and genomics laboratories.



STITCH_UI_PROMPTS.md

Store every Google Stitch prompt.

Suggested sections:

Prompt 1:
Main Dashboard

Prompt 2:
Analysis Workspace

Prompt 3:
Reports Center

Prompt 4:
Settings Page

Prompt 5:
Taxonomy Viewer

Prompt 6:
KEGG Viewer

Prompt 7:
Pfam Viewer

Prompt 8:
PubMed Evidence Panel

Prompt 9:
AI Interpretation Panel

Prompt 10:
Mobile Layout

This becomes your UI design source of truth.