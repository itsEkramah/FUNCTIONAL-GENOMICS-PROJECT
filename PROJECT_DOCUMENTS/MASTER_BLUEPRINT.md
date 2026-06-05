MASTER_BLUEPRINT.md = Project Constitution
Every biological interpretation produced by the platform must be supported by:

1. Validated computational outputs

AND

2. Peer-reviewed literature evidence retrieved from PubMed

No interpretation may be generated using AI alone.

# MASTER_BLUEPRINT.md

# PathoScope AI v1.0

## Master System Blueprint

### Project Title

An Automated Viral Functional Genomics Pipeline for Sequence Annotation, Pathway Mapping, and AI-Assisted Biological Interpretation

---

# 1. Executive Summary

PathoScope AI is a production-grade bioinformatics platform designed to perform automated viral genomics and transcriptomics analysis through reproducible, evidence-based computational workflows.

The platform combines:

* Viral genome annotation
* NGS FASTQ processing
* Differential gene expression analysis
* Functional annotation
* Taxonomic classification
* Domain prediction
* Pathway mapping
* AI-assisted biological interpretation

into a single unified web platform.

The system is designed to emulate the workflow reliability of:

* GEO2R
* Galaxy
* nf-core
* Nextflow
* Modern genomic analysis platforms

while remaining deployable on commodity hardware.

The project is NOT a visualization project.

The project is NOT an AI chatbot project.

The project is fundamentally a bioinformatics pipeline platform.

All biological computations originate from validated backend workflows.

Frontend components are visualization layers only.

---

# 2. Core Mission

Provide a reproducible, transparent, biologically defensible platform capable of transforming raw biological data into scientifically meaningful interpretations.

The system must support:

1. Viral FASTA genome analysis
2. FASTQ sequencing analysis
3. Differential expression analysis
4. Functional annotation
5. Taxonomy mapping
6. Pathway analysis
7. AI-assisted interpretation

without generating fabricated biological findings.

---

# 3. Project Philosophy

## Rule 1

Biological correctness is more important than visual appearance.

## Rule 2

Reproducibility is more important than speed.

## Rule 3

Pipeline truth is more important than user experience convenience.

## Rule 4

A failed analysis is better than a fake successful analysis.

## Rule 5

AI interpretation never overrides biological evidence.

---

# 4. Architectural Principles

The entire system follows the following principles.

## Separation of Concerns

Frontend responsibilities:

* Upload files
* Display progress
* Show results
* Export reports

Backend responsibilities:

* Execute workflows
* Manage tools
* Store outputs
* Validate results
* Generate reports

AI responsibilities:

* Explain evidence
* Summarize findings
* Interpret outputs

AI must never:

* Generate annotations
* Invent pathways
* Invent taxonomy
* Create fake significance

---
Literature-supported interpretation is mandatory.

If PubMed evidence cannot be retrieved, the system must report insufficient evidence rather than generating speculative biological conclusions.

# 5. Supported Workflows

The platform contains three independent workflow engines.

## Workflow A

FASTA Viral Genome Analysis

Input:

* FASTA
* FNA
* FA

Output:

* ORFs
* Proteins
* Functional annotation
* Taxonomy
* Pfam domains
* KEGG categories
* Reports

---

## Workflow B

FASTQ Processing Workflow

Input:

* FASTQ
* FASTQ.GZ

Output:

* QC metrics
* Trimmed reads
* Assembly
* Contigs
* ORFs
* Functional annotation

---

## Workflow C

Differential Gene Expression Workflow

Input:

CSV

TSV

Required columns:

* gene_id
* log2FoldChange
* pvalue

Output:

* Significant genes
* Volcano plots
* Enrichment analysis
* Biological interpretation

---

# 6. Production Architecture

The platform follows an nf-core inspired architecture.

backend/

api/

pipeline/

core/

services/

utils/

reports/

storage/

tests/

frontend/

public/

src/

components/

pages/

hooks/

styles/

---

# 7. Backend Folder Responsibilities

## api

Purpose:

Expose REST endpoints.

Contains:

* FastAPI app
* Routes
* Request validation
* Authentication

No biological logic allowed.

---

## pipeline

Purpose:

Workflow orchestration.

Contains:

* workflow_fasta.py
* workflow_fastq.py
* workflow_deg.py
* pipeline_runner.py

This folder controls execution order.

---

## core

Purpose:

Pure biological logic.

Contains:

* ORF detection
* Translation
* QC calculations
* DEG processing

No subprocess execution allowed.

---

## services

Purpose:

Tool integrations.

Contains wrappers for:

* FastQC
* fastp
* SPAdes
* DIAMOND
* HMMER
* NCBI

All external software calls originate here.

---

## utils

Purpose:

Shared utilities.

Contains:

* Logging
* Validators
* File IO
* Config loading

---

## reports

Purpose:

Generate:

* HTML
* JSON
* CSV
* PDF
* GFF3

---

## storage

Purpose:

Persistent data.

Stores:

* Uploaded files
* Temporary files
* Reports
* Databases

---

# 8. Pipeline Runner Philosophy

pipeline_runner.py is the most important file in the project.

Nothing executes without it.

Every workflow must pass through it.

Responsibilities:

* Start pipeline
* Track status
* Validate outputs
* Log execution
* Stop on failure

Status values:

QUEUED

RUNNING

COMPLETED

FAILED

CANCELLED

No workflow can bypass pipeline_runner.

---

# 9. Hardcoded Biological Thresholds

These values are mandatory.

ORF_MIN_LENGTH_BP = 100

DIAMOND_EVALUE_MAX = 1e-5

DIAMOND_IDENTITY_MIN = 30

DIAMOND_COVERAGE_MIN = 50

FASTQ_MIN_PHRED = 20

FASTQ_MIN_READ_LENGTH = 50

LOG2FC_UP = 1

LOG2FC_DOWN = -1

FDR_THRESHOLD = 0.05

MIN_PATHWAY_SIZE = 15

MAX_PATHWAY_SIZE = 500

These values are stored centrally and cannot be modified through the UI.

---

# 10. FASTA Workflow Blueprint

Step 1

Input validation

Checks:

* file exists
* FASTA format valid
* sequence length > 0

Output:

validated sequence

---

Step 2

Sequence QC

Calculate:

* GC content
* ambiguity count
* length statistics

Output:

QC report

---

Step 3

Six-frame ORF scanning

Frames:

+1
+2
+3

-1
-2
-3

Output:

candidate ORFs

---

Step 4

ORF filtering

Keep:

ORF >=100bp

Output:

validated ORFs

---

Step 5

Translation

Convert ORFs to proteins

Output:

protein sequences

---

Step 6

DIAMOND annotation

Output:

functional hits

---

Step 7

Pfam domain search

Output:

domain hits

---

Step 8

KEGG mapping

Output:

pathway categories

---

Step 9

NCBI taxonomy

Output:

taxonomy lineage

---

Step 10

Report generation

Output:

HTML

CSV

JSON

GFF3

---

# 11. FASTQ Workflow Blueprint

Step 1

FastQC

Raw read QC

Step 2

fastp

Trimming

Filtering

Step 3

FastQC

Post-trimming QC

Step 4

SPAdes assembly

Optional

Step 5

Contig filtering

Step 6

Reuse FASTA workflow

All contigs enter Workflow A

---

# 12. DEG Workflow Blueprint

Step 1

Validate table

Step 2

Normalize IDs

Step 3

Log2 transform if needed

Step 4

BH-FDR correction

Step 5

Classify genes

UP

DOWN

Step 6

KEGG enrichment

Step 7

GO enrichment

Step 8

Volcano plot

Step 9

Report generation

---

# 13. AI Interpretation Architecture

AI providers:

* Gemini
* OpenAI

Keys stored only in:

.env

Variables:

OPENAI_API_KEY

GEMINI_API_KEY

Frontend never accesses keys.

AI receives only:

* validated outputs
* annotation results
* PubMed evidence

Interpretation format:

Evidence

Analysis

Conclusion

Unsupported claims prohibited.

---

# 13A. PubMed Evidence Engine

## Purpose

The PubMed Evidence Engine provides scientific literature support for all AI-generated biological interpretations.

The purpose of this module is to ensure that every biological conclusion presented by the system can be traced back to peer-reviewed scientific publications.

This module acts as the scientific grounding layer between computational outputs and AI interpretation.

Without PubMed evidence, the AI Interpretation Module must not generate biological conclusions.

---

## Scientific Principle

The system follows:

Computational Evidence
+
Scientific Literature Evidence
==============================

Biological Interpretation

AI is never allowed to interpret results without supporting evidence.

---

## Data Sources

Primary Source:

PubMed

Access Method:

NCBI E-Utilities API

Services:

esearch.fcgi

esummary.fcgi

efetch.fcgi

---

## PubMed Retrieval Workflow

Step 1

Receive validated biological outputs.

Examples:

Protein annotation

Pfam domains

KEGG pathways

Taxonomic classification

Differentially expressed genes

---

Step 2

Generate literature search queries.

Examples:

"RNA dependent RNA polymerase coronavirus"

"HIV capsid protein"

"Influenza NS1 protein"

"MAPK signaling pathway"

"Interferon response genes"

---

Step 3

Query PubMed.

Retrieve:

PMID

Title

Journal

Authors

Publication Date

Abstract

---

Step 4

Rank publications.

Priority:

Review articles

High citation studies

Recent publications

Experimental validation studies

---

Step 5

Store literature evidence.

Output:

pubmed_evidence.json

---

Step 6

Pass evidence to AI Interpretation Engine.

Only evidence-backed information is allowed.

---

## PubMed Search Strategy

Priority Order:

1. Exact protein match

2. Exact pathway match

3. Exact taxonomic organism match

4. Functional domain match

5. Related biological process

The system should attempt the highest confidence query first.

---

## PubMed Data Fields

For every retrieved publication:

PMID

Title

Journal

Publication Year

Authors

Abstract

Keywords

DOI

URL

---

## Evidence Ranking Score

Each paper receives:

Relevance Score

Publication Score

Recency Score

Combined Evidence Score

Top ranked publications are passed to AI.

---

## Storage Structure

backend/storage/pubmed/

run_id/

search_results.json

ranked_results.json

abstracts.json

evidence_bundle.json

---

## AI Interpretation Requirements

The AI receives:

Annotation outputs

Pathway outputs

Taxonomy outputs

DEG outputs

PubMed abstracts

The AI does NOT receive:

Raw FASTA

Raw FASTQ

Raw sequencing files

Unvalidated predictions

---

## Required Interpretation Format

Section 1

Computational Findings

Section 2

Supporting Literature

Section 3

Biological Interpretation

Section 4

Confidence Assessment

Section 5

Limitations

---

## Hallucination Prevention Rules

AI cannot:

Invent citations

Invent PMIDs

Invent pathways

Invent protein functions

Invent biological significance

Every statement must reference:

Computational result

or

PubMed evidence

or

Both

---

## Failure Conditions

Interpretation generation must fail if:

No PubMed evidence found

Annotation confidence below threshold

Taxonomy confidence below threshold

Pipeline validation failed

The system must report:

"Insufficient evidence for biological interpretation."

instead of generating speculative conclusions.

---

## Future Expansion

Planned Sources:

PMC Full Text

Europe PMC

KEGG Literature Links

UniProt Literature References

Gene Ontology References

These sources may supplement PubMed but never replace it.


# 14. Failure Philosophy

The system must fail safely.

If any step fails:

STOP PIPELINE

Do not continue.

Do not fabricate outputs.

Do not mark completed.

Log failure.

Store diagnostics.

Return meaningful error.
