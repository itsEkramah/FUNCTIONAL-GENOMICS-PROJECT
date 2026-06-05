Read:

project-docs/PRD.md
project-docs/TRD.md
project-docs/APP_FLOW.md
project-docs/UI_UX_BRIEF.md
project-docs/BACKEND_SCHEMA.md
project-docs/IMPLEMENTATION_PLAN.md
project-docs/GITHUB_REFERENCE.md
project-docs/BLUEPRINT.md
project-docs/MASTER_BLUEPRINT.md

Create PROJECT_RULES.md.

# PROJECT_RULES.md

Version: 1.0

Authority Level: Highest

Applies To:

* Antigravity
* GSD
* Ralph Loop
* CodeRabbit
* Human Developers
* Future Contributors

---

# PURPOSE

This document defines mandatory repository rules.

These rules override:

* Agent assumptions
* AI-generated suggestions
* Convenience shortcuts
* Temporary fixes

Any implementation violating these rules must be rejected.

---

# SECTION 1 — PROJECT IDENTITY

## Rule 1.1

PathoScope AI is a Bioinformatics Pipeline Platform.

It is NOT:

* an AI chatbot
* a dashboard project
* a visualization project
* an LLM wrapper

---

## Rule 1.2

Biological correctness is the highest priority.

Priority order:

1 Biological correctness

2 Reproducibility

3 Pipeline reliability

4 Software quality

5 User experience

---

## Rule 1.3

A failed pipeline is preferable to a fake successful pipeline.

---

# SECTION 2 — ARCHITECTURE RULES

## Rule 2.1

Frontend must never perform biological analysis.

Forbidden:

* ORF prediction
* Translation
* Annotation
* DEG calculations
* Taxonomy assignment
* AI interpretation

---

## Rule 2.2

Frontend responsibilities only:

* Upload files
* Trigger workflows
* Display status
* Display results
* Download reports

---

## Rule 2.3

API layer must never contain scientific logic.

API responsibilities:

* validation
* routing
* authentication
* request handling

---

## Rule 2.4

All scientific computation belongs inside:

```text
backend/core
backend/services
backend/pipeline
```

Only.

---

## Rule 2.5

All workflow execution must pass through:

```text
pipeline_runner.py
```

No exceptions.

---

## Rule 2.6

No route may directly execute:

* FastQC
* fastp
* DIAMOND
* HMMER
* SPAdes

---

# SECTION 3 — PIPELINE RULES

## Rule 3.1

Every pipeline step must follow:

Execute

↓

Validate

↓

Continue

or

Fail

---

## Rule 3.2

Every step must produce a tangible output.

Examples:

FastQC

Produces:

```text
report.html
report.zip
```

---

DIAMOND

Produces:

```text
diamond.tsv
```

---

No output

↓

Pipeline fails

---

## Rule 3.3

No workflow may continue after failed validation.

---

## Rule 3.4

Pipeline status values are restricted to:

```text
QUEUED
RUNNING
COMPLETED
FAILED
CANCELLED
```

---

## Rule 3.5

COMPLETED status may only be assigned when:

All steps succeed

AND

All validations pass

---

# SECTION 4 — BIOLOGICAL RULES

## Rule 4.1

All biological thresholds must originate from:

```text
backend/config/thresholds.yaml
```

Never hardcode values elsewhere.

---

## Rule 4.2

Mandatory ORF threshold

```text
MIN_ORF_LENGTH_BP = 100
```

---

## Rule 4.3

Mandatory DIAMOND threshold

```text
EVALUE <= 1e-5
```

---

## Rule 4.4

Mandatory identity threshold

```text
IDENTITY >= 30%
```

---

## Rule 4.5

Mandatory coverage threshold

```text
COVERAGE >= 50%
```

---

## Rule 4.6

FASTQ filtering thresholds

```text
Q20 minimum
READ LENGTH >= 50 bp
```

---

## Rule 4.7

DEG thresholds

```text
LOG2FC >= 1

LOG2FC <= -1

FDR <= 0.05
```

---

## Rule 4.8

Pathway size limits

```text
15 <= pathway <= 500 genes
```

---

# SECTION 5 — FASTA WORKFLOW RULES

## Rule 5.1

Supported formats

```text
.fasta
.fa
.fna
```

Only.

---

## Rule 5.2

All genomes must undergo:

1 Validation

2 QC

3 ORF detection

4 Translation

5 Annotation

6 Taxonomy

7 Reporting

---

## Rule 5.3

ORF prediction must scan:

```text
+1
+2
+3
-1
-2
-3
```

All six reading frames.

---

## Rule 5.4

Translation must use Biopython.

No custom codon dictionaries.

---

## Rule 5.5

KeyError('stop') must never terminate execution.

Partial codons must be handled safely.

---

# SECTION 6 — FASTQ WORKFLOW RULES

## Rule 6.1

Supported formats

```text
.fastq
.fastq.gz
.fq
.fq.gz
```

---

## Rule 6.2

Raw reads must always pass through:

FastQC

↓

fastp

↓

FastQC

---

## Rule 6.3

No homemade trimming algorithms.

Use fastp.

---

## Rule 6.4

No homemade QC substitutes.

Use FastQC.

---

## Rule 6.5

Streaming support required.

Large files must not be loaded entirely into memory.

---

## Rule 6.6

Compressed FASTQ support required.

---

## Rule 6.7

SPAdes assembly is optional.

---

# SECTION 7 — DEG RULES

## Rule 7.1

Required columns:

```text
gene_id
log2FoldChange
pvalue
```

---

## Rule 7.2

FDR correction mandatory.

Method:

Benjamini-Hochberg

---

## Rule 7.3

No significance decisions using raw p-values.

---

## Rule 7.4

Volcano plot generation mandatory.

---

# SECTION 8 — PUBMED RULES

## Rule 8.1

PubMed evidence is mandatory.

---

## Rule 8.2

AI interpretation requires:

Computational evidence

AND

Literature evidence

---

## Rule 8.3

PubMed access method:

NCBI E-Utilities

---

## Rule 8.4

Store:

PMID

Title

Abstract

Journal

Year

---

## Rule 8.5

No fabricated citations.

---

## Rule 8.6

No fabricated PMIDs.

---

## Rule 8.7

No fabricated abstracts.

---

## Rule 8.8

If no literature evidence exists:

Return:

```text
Insufficient evidence for interpretation.
```

---

# SECTION 9 — AI INTERPRETATION RULES

## Rule 9.1

AI cannot generate biological conclusions without evidence.

---

## Rule 9.2

AI providers:

* Gemini
* OpenAI

Only.

---

## Rule 9.3

API keys stored only in:

```text
.env
```

Variables:

```text
OPENAI_API_KEY

GEMINI_API_KEY
```

---

## Rule 9.4

Frontend must never access API keys.

---

## Rule 9.5

AI interpretation format:

1 Findings

2 Literature

3 Analysis

4 Confidence

5 Limitations

---

## Rule 9.6

AI must cite supporting PMIDs.

---

# SECTION 10 — FRONTEND RULES

## Rule 10.1

No fake progress bars.

---

## Rule 10.2

No simulated completion.

---

## Rule 10.3

No hardcoded success messages.

---

## Rule 10.4

Progress must originate from backend state.

---

## Rule 10.5

Frontend polling required.

---

## Rule 10.6

Workflow state must be visible.

---

# SECTION 11 — REPORT RULES

Required outputs:

HTML

JSON

CSV

PDF

---

FASTA workflow additionally:

GFF3

---

Reports must contain:

Inputs

Methods

Parameters

Results

Limitations

---

# SECTION 12 — LOGGING RULES

Every step must log:

Start time

End time

Duration

Status

Output path

Errors

---

Logs must never be deleted automatically.

---

# SECTION 13 — TESTING RULES

Required test types:

Unit

Integration

Workflow

End-to-End

Biological Validation

---

Every bug fix requires a test.

---

No feature is complete without tests.

---

# SECTION 14 — GITHUB EXTRACTION RULES

## Rule 14.1

Reference repositories are learning resources.

Not source code to copy blindly.

---

## Rule 14.2

Allowed extraction:

Architecture patterns

Algorithms

CLI parameters

Workflow structures

Validation logic

---

## Rule 14.3

Forbidden:

Copying entire repositories

Copying UI

Copying workflows unchanged

Copying documentation verbatim

---

# SECTION 15 — ANTIGRAVITY RULES

## Rule 15.1

Never ask Antigravity to build the entire project in one prompt.

---

## Rule 15.2

All work must be phase-based.

---

## Rule 15.3

One workflow at a time.

---

## Rule 15.4

Pipeline architecture before UI.

---

## Rule 15.5

Backend before frontend.

---

## Rule 15.6

Biological validation before AI interpretation.

---

# SECTION 16 — GSD RULES

GSD is mandatory.

Every major feature requires:

Specification

Acceptance criteria

Verification criteria

Dependencies

---

No execution without specification.

---

# SECTION 17 — RALPH LOOP RULES

Tasks must be atomic.

Maximum scope:

One feature per task.

---

No task should require:

More than one subsystem.

---

# SECTION 18 — CODERABBIT RULES

All pull requests require review.

Critical findings must be fixed before merge.

---

# SECTION 19 — COMPLETION CRITERIA

PathoScope AI is complete only when:

✓ FASTA workflow runs on real genomes

✓ FASTQ workflow runs on real reads

✓ DEG workflow runs on real datasets

✓ DIAMOND annotation works

✓ Pfam integration works

✓ KEGG mapping works

✓ PubMed retrieval works

✓ AI interpretation is evidence-based

✓ Reports are reproducible

✓ Frontend reflects real backend status

✓ No simulated execution exists anywhere

---

# FINAL LAW

If biological evidence, software behavior, UI behavior, AI interpretation, or developer convenience conflict:

Biological evidence wins.

Always.
