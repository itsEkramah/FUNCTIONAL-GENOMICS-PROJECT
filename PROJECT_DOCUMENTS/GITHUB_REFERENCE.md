GITHUB_REFERENCE.md

Version: 1.0

Purpose:

This document defines exactly:

Which repositories are reference-only
Which files Antigravity must study
Which logic may be extracted
Which logic must NOT be copied
Which modules of PathoScope AI each repository supports

Critical Rule:

These repositories are NOT dependencies.

They are architecture references.

Antigravity must study them and rewrite logic into PathoScope AI architecture.

Never copy entire repositories.

Never embed external project structures.

Never import repository source trees directly.

CURRENT REFERENCE REPOSITORIES

Located at:

genomic-insight-navigator/

└── clones/

    ├── viralrecon/

    ├── biopython/

    ├── fastp/

    ├── diamond/

    ├── GSEApy/

    ├── deg-analysis-pipeline/

    └── ORF-Finder/
REPOSITORY 1
nf-core/viralrecon

Purpose:

Production-grade viral sequencing workflow.

Use as architectural reference.

DO NOT COPY PIPELINE.

Study workflow orchestration only.

Location

clones/viralrecon

Files To Study

FastQC + fastp Workflow
subworkflows/local/utils_nfcore_viralrecon_pipeline/main.nf

Study:

execution order
QC before trimming
QC after trimming
checkpoint logic

Extract:

FastQC

↓

fastp

↓

FastQC

PathoScope Module:

workflow_fastq.py
SPAdes Workflow

Study:

modules/local/assembly.nf

Extract:

SPAdes invocation pattern

input validation

output validation

PathoScope Module:

spades_service.py
Nextflow Pipeline Structure

Study:

workflows/

Extract:

workflow orchestration concepts

step chaining

dependency flow

PathoScope Module:

pipeline_runner.py

DO NOT COPY:

Nextflow DSL

Channel syntax

Container logic
REPOSITORY 2
biopython

Purpose:

Primary biological computation library.

This WILL be dependency.

Location

clones/biopython

Files To Study

FASTQ Streaming

Study:

Bio/SeqIO/QualityIO.py

Critical Function:

FastqGeneralIterator

Extract Logic:

stream FASTQ records

avoid loading entire file

memory-safe iteration

Used In:

fastq_parser.py
Translation Logic

Study:

Bio/Seq.py

Critical Function:

translate()

Extract:

codon validation

translation safety

stop codon handling

Used In:

orf_finder.py

translation_engine.py

Fixes:

KeyError: stop
Reverse Complement Logic

Study:

Bio/Seq.py

Extract:

reverse_complement()

Used In:

ORF scanning
FASTA Parsing

Study:

Bio/SeqIO

Extract:

FASTA validation

streaming sequence reading

Used In:

fasta_parser.py
REPOSITORY 3
OpenGene/fastp

Purpose:

Understand trimming logic.

Fastp itself will run as external executable.

Do NOT reimplement fastp.

Location

clones/fastp

Files To Study

Core Filtering Logic

Study:

src/filter.cpp

Understand:

quality filtering

length filtering

adapter trimming
JSON Output

Study:

src/jsonreporter.cpp

Extract:

output metrics structure

reads before filtering

reads after filtering

quality metrics

Used In:

fastp_service.py
CLI Parameters

Study:

README.md

Required Parameters

--qualified_quality_phred 20

--length_required 50

Hardcoded Professor Requirements

Q20

Length >=50 bp
REPOSITORY 4
DIAMOND

Purpose:

Protein annotation engine.

External executable.

Never reimplement.

Location

clones/diamond

Files To Study

Command Line Options

Study:

README.md

wiki/

Required Output Fields

qseqid

sseqid

pident

length

evalue

bitscore

qcovhsp

Required Command

diamond blastp

Parameters

--very-sensitive

-f 6

Thresholds

E-value <= 1e-5

Identity >= 30%

Coverage >= 50%

Used In

diamond_service.py
REPOSITORY 5
GSEApy

Purpose:

KEGG enrichment

GO enrichment

Gene set analysis

Location

clones/GSEApy

Files To Study

Study:

gseapy/enrichr.py

gseapy/parser.py

Extract:

input formats

enrichment workflow

result parsing

Used In

enrichment_service.py

workflow_deg.py

Required Enrichment

KEGG

GO BP

GO MF

GO CC

Pathway Limits

15 <= genes <= 500

Professor Requirement

REPOSITORY 6
deg-analysis-pipeline

Purpose:

Understand DEG workflow.

Reference only.

Location

clones/deg-analysis-pipeline

Study

Entire workflow.

Focus on:

input validation

DEG classification

result organization

Extract

Upregulated

Downregulated

Significant

Non-significant

PathoScope Rules

Up:

log2FC >= 1

FDR < 0.05

Down:

log2FC <= -1

FDR < 0.05

DO NOT COPY

plots

UI

folder structure
REPOSITORY 7
ORF-Finder

Purpose:

Reference implementation for ORF detection.

Location

clones/ORF-Finder

Files To Study

Study:

orf_finder.py

Extract

start codon detection

stop codon detection

coordinate calculation

frame tracking

DO NOT USE DIRECTLY

Rewrite into:

backend/core/orf_finder.py

Required Improvements

Must support:

6-frame scanning

forward strand

reverse strand

partial sequence protection

ambiguous nucleotide handling
ADDITIONAL REPOSITORIES REQUIRED

Your current 7 repositories are NOT enough.

You should also clone:

HMMER

Purpose

Pfam domain detection.

git clone https://github.com/EddyRivasLab/hmmer.git

Study:

hmmscan usage

output parsing

Used In:

hmmer_service.py
FastQC

Purpose

Quality control reports.

git clone https://github.com/s-andrews/FastQC.git

Study:

CLI execution

output structure

Used In:

fastqc_service.py
SPAdes

Purpose

Assembly wrapper understanding.

git clone https://github.com/ablab/spades.git

Study:

CLI parameters

assembly outputs

Used In:

spades_service.py
COMPLETE LOGIC EXTRACTION MAP
ORF Detection
    ← ORF-Finder
    ← Biopython

Translation
    ← Biopython

FASTA Parsing
    ← Biopython

FASTQ Streaming
    ← Biopython

Quality Control
    ← FastQC
    ← viralrecon

Trimming
    ← fastp
    ← viralrecon

Assembly
    ← SPAdes
    ← viralrecon

Protein Annotation
    ← DIAMOND

Pfam Annotation
    ← HMMER

KEGG Enrichment
    ← GSEApy

GO Enrichment
    ← GSEApy

DEG Analysis
    ← deg-analysis-pipeline

Workflow Orchestration
    ← viralrecon
    ← nf-core design principles
ABSOLUTE RULES FOR ANTIGRAVITY

Never copy:

Entire repositories

Notebook files

UI code

GitHub Actions

Dockerfiles

Tests from reference repos

Only extract:

Algorithms

CLI parameters

Validation logic

Workflow ordering

Output parsing logic

Everything must be rewritten into:

backend/

api/

pipeline/

core/

services/

utils/

following the architecture defined in MASTER_BLUEPRINT.md.