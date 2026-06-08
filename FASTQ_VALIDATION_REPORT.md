# FASTQ Validation and E2E Test Report

This report details the validation of the PathoScope AI v3.0 FASTQ raw sequencing reads processing, quality control, assembly, and downstream annotation pipeline run end-to-end on real datasets.

## Test Execution Environment
- **Database**: SQLite (isolated test runner DB)
- **QC Service**: FastQC Raw and Trimmed QC (with offline python fallback)
- **Trimming Service**: fastp adapter & quality-trimming (with offline python fallback)
- **Assembly Service**: SPAdes de novo assembler in `--rnaviral` mode (with offline python fallback)
- **Downstream FASTA Pipeline**: Reuses Phase E FASTA workflow steps (ORF detection, Translation, SwissProt DIAMOND, Pfam hmmscan, KEGG mapping, NCBI Taxonomy, PubMed, AI, Reports)

## Test Case Execution Summary

| Dataset | Raw Reads | Filtered Reads | Survivability % | Avg Quality | Contigs | Status | Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TESTX_H7YRLADXX_S1_L001_R1_001.fastq.gz | 25,000 | 24,998 | 99.99% | 37.29 | 1 | **COMPLETED** | 157.05 |
| TESTX_H7YRLADXX_S1_L001_R1_001.fastq/TESTX_H7YRLADXX_S1_L001_R1_001.fastq | 25,000 | 24,998 | 99.99% | 37.29 | 1 | **COMPLETED** | 114.07 |
| TESTX_H7YRLADXX_S1_L001_R2_001.fastq.gz | 25,000 | 24,926 | 99.70% | 36.34 | 1 | **COMPLETED** | 109.85 |
| TESTX_H7YRLADXX_S1_L001_R2_001.fastq/TESTX_H7YRLADXX_S1_L001_R2_001.fastq | 25,000 | 24,926 | 99.70% | 36.34 | 1 | **COMPLETED** | 116.53 |
| TESTX_H7YRLADXX_S1_L002_R1_001.fastq.gz | 25,000 | 25,000 | 100.00% | 37.31 | 1 | **COMPLETED** | 106.65 |
| TESTX_H7YRLADXX_S1_L002_R1_001.fastq/TESTX_H7YRLADXX_S1_L002_R1_001.fastq | 25,000 | 25,000 | 100.00% | 37.31 | 1 | **COMPLETED** | 106.91 |
| TESTX_H7YRLADXX_S1_L002_R2_001.fastq.gz | 25,000 | 24,902 | 99.61% | 36.49 | 1 | **COMPLETED** | 105.72 |
| TESTX_H7YRLADXX_S1_L002_R2_001.fastq/TESTX_H7YRLADXX_S1_L002_R2_001.fastq | 25,000 | 24,902 | 99.61% | 36.49 | 1 | **COMPLETED** | 112.03 |
| TESTY_H7YRLADXX_S1_L001_R1_001.fastq.gz | 25,000 | 24,999 | 100.00% | 37.45 | 1 | **COMPLETED** | 110.25 |
| TESTY_H7YRLADXX_S1_L001_R2_001.fastq.gz | 25,000 | 24,935 | 99.74% | 36.47 | 1 | **COMPLETED** | 107.38 |
| TESTY_H7YRLADXX_S1_L002_R1_001.fastq.gz | 25,000 | 25,000 | 100.00% | 37.53 | 1 | **COMPLETED** | 112.93 |
| TESTY_H7YRLADXX_S1_L002_R2_001.fastq.gz | 25,000 | 24,902 | 99.61% | 36.65 | 1 | **COMPLETED** | 104.44 |
| test_reads.fastq | 387 | 345 | 89.15% | 34.55 | 1 | **COMPLETED** | 94.03 |

## Generated Deliverables (per job)

### TESTX_H7YRLADXX_S1_L001_R1_001.fastq.gz (Job: `8ca4c169-a00d-4c19-ac09-0470e39b9db7`)
- **FastQC Raw Reports**: `storage/jobs/8ca4c169-a00d-4c19-ac09-0470e39b9db7/fastqc_raw/`
- **fastp Reports**: `storage/jobs/8ca4c169-a00d-4c19-ac09-0470e39b9db7/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/8ca4c169-a00d-4c19-ac09-0470e39b9db7/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/8ca4c169-a00d-4c19-ac09-0470e39b9db7/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/8ca4c169-a00d-4c19-ac09-0470e39b9db7/input.fasta`
- **HTML Dashboard**: `storage/jobs/8ca4c169-a00d-4c19-ac09-0470e39b9db7/reports/report.html`
- **PDF Report**: `storage/jobs/8ca4c169-a00d-4c19-ac09-0470e39b9db7/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/8ca4c169-a00d-4c19-ac09-0470e39b9db7/reports/report.json`

### TESTX_H7YRLADXX_S1_L001_R1_001.fastq/TESTX_H7YRLADXX_S1_L001_R1_001.fastq (Job: `bbbdf714-afe5-400a-9041-d4be451c7382`)
- **FastQC Raw Reports**: `storage/jobs/bbbdf714-afe5-400a-9041-d4be451c7382/fastqc_raw/`
- **fastp Reports**: `storage/jobs/bbbdf714-afe5-400a-9041-d4be451c7382/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/bbbdf714-afe5-400a-9041-d4be451c7382/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/bbbdf714-afe5-400a-9041-d4be451c7382/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/bbbdf714-afe5-400a-9041-d4be451c7382/input.fasta`
- **HTML Dashboard**: `storage/jobs/bbbdf714-afe5-400a-9041-d4be451c7382/reports/report.html`
- **PDF Report**: `storage/jobs/bbbdf714-afe5-400a-9041-d4be451c7382/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/bbbdf714-afe5-400a-9041-d4be451c7382/reports/report.json`

### TESTX_H7YRLADXX_S1_L001_R2_001.fastq.gz (Job: `3406dea0-a173-4195-b079-0c57261df448`)
- **FastQC Raw Reports**: `storage/jobs/3406dea0-a173-4195-b079-0c57261df448/fastqc_raw/`
- **fastp Reports**: `storage/jobs/3406dea0-a173-4195-b079-0c57261df448/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/3406dea0-a173-4195-b079-0c57261df448/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/3406dea0-a173-4195-b079-0c57261df448/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/3406dea0-a173-4195-b079-0c57261df448/input.fasta`
- **HTML Dashboard**: `storage/jobs/3406dea0-a173-4195-b079-0c57261df448/reports/report.html`
- **PDF Report**: `storage/jobs/3406dea0-a173-4195-b079-0c57261df448/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/3406dea0-a173-4195-b079-0c57261df448/reports/report.json`

### TESTX_H7YRLADXX_S1_L001_R2_001.fastq/TESTX_H7YRLADXX_S1_L001_R2_001.fastq (Job: `ca0ced64-dc04-43b2-8f30-94a8cf72da72`)
- **FastQC Raw Reports**: `storage/jobs/ca0ced64-dc04-43b2-8f30-94a8cf72da72/fastqc_raw/`
- **fastp Reports**: `storage/jobs/ca0ced64-dc04-43b2-8f30-94a8cf72da72/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/ca0ced64-dc04-43b2-8f30-94a8cf72da72/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/ca0ced64-dc04-43b2-8f30-94a8cf72da72/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/ca0ced64-dc04-43b2-8f30-94a8cf72da72/input.fasta`
- **HTML Dashboard**: `storage/jobs/ca0ced64-dc04-43b2-8f30-94a8cf72da72/reports/report.html`
- **PDF Report**: `storage/jobs/ca0ced64-dc04-43b2-8f30-94a8cf72da72/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/ca0ced64-dc04-43b2-8f30-94a8cf72da72/reports/report.json`

### TESTX_H7YRLADXX_S1_L002_R1_001.fastq.gz (Job: `d6b938f6-2d06-4d5a-b85c-d864b533f20d`)
- **FastQC Raw Reports**: `storage/jobs/d6b938f6-2d06-4d5a-b85c-d864b533f20d/fastqc_raw/`
- **fastp Reports**: `storage/jobs/d6b938f6-2d06-4d5a-b85c-d864b533f20d/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/d6b938f6-2d06-4d5a-b85c-d864b533f20d/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/d6b938f6-2d06-4d5a-b85c-d864b533f20d/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/d6b938f6-2d06-4d5a-b85c-d864b533f20d/input.fasta`
- **HTML Dashboard**: `storage/jobs/d6b938f6-2d06-4d5a-b85c-d864b533f20d/reports/report.html`
- **PDF Report**: `storage/jobs/d6b938f6-2d06-4d5a-b85c-d864b533f20d/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/d6b938f6-2d06-4d5a-b85c-d864b533f20d/reports/report.json`

### TESTX_H7YRLADXX_S1_L002_R1_001.fastq/TESTX_H7YRLADXX_S1_L002_R1_001.fastq (Job: `16030b34-8549-4d2b-a86e-d5dff1c7314b`)
- **FastQC Raw Reports**: `storage/jobs/16030b34-8549-4d2b-a86e-d5dff1c7314b/fastqc_raw/`
- **fastp Reports**: `storage/jobs/16030b34-8549-4d2b-a86e-d5dff1c7314b/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/16030b34-8549-4d2b-a86e-d5dff1c7314b/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/16030b34-8549-4d2b-a86e-d5dff1c7314b/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/16030b34-8549-4d2b-a86e-d5dff1c7314b/input.fasta`
- **HTML Dashboard**: `storage/jobs/16030b34-8549-4d2b-a86e-d5dff1c7314b/reports/report.html`
- **PDF Report**: `storage/jobs/16030b34-8549-4d2b-a86e-d5dff1c7314b/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/16030b34-8549-4d2b-a86e-d5dff1c7314b/reports/report.json`

### TESTX_H7YRLADXX_S1_L002_R2_001.fastq.gz (Job: `aa26f56d-d15a-428f-8c6f-d9d26e53b56f`)
- **FastQC Raw Reports**: `storage/jobs/aa26f56d-d15a-428f-8c6f-d9d26e53b56f/fastqc_raw/`
- **fastp Reports**: `storage/jobs/aa26f56d-d15a-428f-8c6f-d9d26e53b56f/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/aa26f56d-d15a-428f-8c6f-d9d26e53b56f/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/aa26f56d-d15a-428f-8c6f-d9d26e53b56f/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/aa26f56d-d15a-428f-8c6f-d9d26e53b56f/input.fasta`
- **HTML Dashboard**: `storage/jobs/aa26f56d-d15a-428f-8c6f-d9d26e53b56f/reports/report.html`
- **PDF Report**: `storage/jobs/aa26f56d-d15a-428f-8c6f-d9d26e53b56f/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/aa26f56d-d15a-428f-8c6f-d9d26e53b56f/reports/report.json`

### TESTX_H7YRLADXX_S1_L002_R2_001.fastq/TESTX_H7YRLADXX_S1_L002_R2_001.fastq (Job: `44a4ce37-5ff5-427c-8d65-1c94f6ec4a40`)
- **FastQC Raw Reports**: `storage/jobs/44a4ce37-5ff5-427c-8d65-1c94f6ec4a40/fastqc_raw/`
- **fastp Reports**: `storage/jobs/44a4ce37-5ff5-427c-8d65-1c94f6ec4a40/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/44a4ce37-5ff5-427c-8d65-1c94f6ec4a40/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/44a4ce37-5ff5-427c-8d65-1c94f6ec4a40/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/44a4ce37-5ff5-427c-8d65-1c94f6ec4a40/input.fasta`
- **HTML Dashboard**: `storage/jobs/44a4ce37-5ff5-427c-8d65-1c94f6ec4a40/reports/report.html`
- **PDF Report**: `storage/jobs/44a4ce37-5ff5-427c-8d65-1c94f6ec4a40/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/44a4ce37-5ff5-427c-8d65-1c94f6ec4a40/reports/report.json`

### TESTY_H7YRLADXX_S1_L001_R1_001.fastq.gz (Job: `04359d67-1383-473e-b928-e7608c0b9488`)
- **FastQC Raw Reports**: `storage/jobs/04359d67-1383-473e-b928-e7608c0b9488/fastqc_raw/`
- **fastp Reports**: `storage/jobs/04359d67-1383-473e-b928-e7608c0b9488/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/04359d67-1383-473e-b928-e7608c0b9488/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/04359d67-1383-473e-b928-e7608c0b9488/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/04359d67-1383-473e-b928-e7608c0b9488/input.fasta`
- **HTML Dashboard**: `storage/jobs/04359d67-1383-473e-b928-e7608c0b9488/reports/report.html`
- **PDF Report**: `storage/jobs/04359d67-1383-473e-b928-e7608c0b9488/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/04359d67-1383-473e-b928-e7608c0b9488/reports/report.json`

### TESTY_H7YRLADXX_S1_L001_R2_001.fastq.gz (Job: `abf29cfc-d6d6-44cb-af95-ccda8835a56a`)
- **FastQC Raw Reports**: `storage/jobs/abf29cfc-d6d6-44cb-af95-ccda8835a56a/fastqc_raw/`
- **fastp Reports**: `storage/jobs/abf29cfc-d6d6-44cb-af95-ccda8835a56a/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/abf29cfc-d6d6-44cb-af95-ccda8835a56a/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/abf29cfc-d6d6-44cb-af95-ccda8835a56a/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/abf29cfc-d6d6-44cb-af95-ccda8835a56a/input.fasta`
- **HTML Dashboard**: `storage/jobs/abf29cfc-d6d6-44cb-af95-ccda8835a56a/reports/report.html`
- **PDF Report**: `storage/jobs/abf29cfc-d6d6-44cb-af95-ccda8835a56a/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/abf29cfc-d6d6-44cb-af95-ccda8835a56a/reports/report.json`

### TESTY_H7YRLADXX_S1_L002_R1_001.fastq.gz (Job: `47681dd6-8473-4115-940d-df6a912da0dd`)
- **FastQC Raw Reports**: `storage/jobs/47681dd6-8473-4115-940d-df6a912da0dd/fastqc_raw/`
- **fastp Reports**: `storage/jobs/47681dd6-8473-4115-940d-df6a912da0dd/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/47681dd6-8473-4115-940d-df6a912da0dd/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/47681dd6-8473-4115-940d-df6a912da0dd/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/47681dd6-8473-4115-940d-df6a912da0dd/input.fasta`
- **HTML Dashboard**: `storage/jobs/47681dd6-8473-4115-940d-df6a912da0dd/reports/report.html`
- **PDF Report**: `storage/jobs/47681dd6-8473-4115-940d-df6a912da0dd/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/47681dd6-8473-4115-940d-df6a912da0dd/reports/report.json`

### TESTY_H7YRLADXX_S1_L002_R2_001.fastq.gz (Job: `cd62a1a3-c9a1-403d-9a2f-aade790145ef`)
- **FastQC Raw Reports**: `storage/jobs/cd62a1a3-c9a1-403d-9a2f-aade790145ef/fastqc_raw/`
- **fastp Reports**: `storage/jobs/cd62a1a3-c9a1-403d-9a2f-aade790145ef/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/cd62a1a3-c9a1-403d-9a2f-aade790145ef/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/cd62a1a3-c9a1-403d-9a2f-aade790145ef/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/cd62a1a3-c9a1-403d-9a2f-aade790145ef/input.fasta`
- **HTML Dashboard**: `storage/jobs/cd62a1a3-c9a1-403d-9a2f-aade790145ef/reports/report.html`
- **PDF Report**: `storage/jobs/cd62a1a3-c9a1-403d-9a2f-aade790145ef/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/cd62a1a3-c9a1-403d-9a2f-aade790145ef/reports/report.json`

### test_reads.fastq (Job: `9784d702-8f66-4c43-8830-48b9bfb0d201`)
- **FastQC Raw Reports**: `storage/jobs/9784d702-8f66-4c43-8830-48b9bfb0d201/fastqc_raw/`
- **fastp Reports**: `storage/jobs/9784d702-8f66-4c43-8830-48b9bfb0d201/fastp_reports/`
- **FastQC Trimmed Reports**: `storage/jobs/9784d702-8f66-4c43-8830-48b9bfb0d201/fastqc_trimmed/`
- **SPAdes Assembly Contigs**: `storage/jobs/9784d702-8f66-4c43-8830-48b9bfb0d201/spades_assembly/contigs.fasta`
- **Filtered Downstream Input FASTA**: `storage/jobs/9784d702-8f66-4c43-8830-48b9bfb0d201/input.fasta`
- **HTML Dashboard**: `storage/jobs/9784d702-8f66-4c43-8830-48b9bfb0d201/reports/report.html`
- **PDF Report**: `storage/jobs/9784d702-8f66-4c43-8830-48b9bfb0d201/reports/report.pdf`
- **JSON Data Dump**: `storage/jobs/9784d702-8f66-4c43-8830-48b9bfb0d201/reports/report.json`

## Validation Integrity and Quality Gate Checks
1. **FASTQ Input Verification**: Confirms that file headers begin with '@' and contain correct sequencing coordinates/information, throwing format exceptions for malformed files.
2. **Raw/Trimmed QC**: Computes total sequences, GC%, and average Phred quality score before and after filtering.
3. **Memory-Safe Sliding Window Trimming**: Streams FASTQ files sequentially (RAM peak < 15MB) using Biopython's FastqGeneralIterator. Trims low quality ends (< Q20) and filters reads >= 50bp, aborting if 0 reads survive.
4. **Assembly and Length Filter**: Correctly executes de novo assembly and filters out short contigs (< 500bp), passing long contigs to the FASTA pipeline as `input.fasta`.
5. **Downstream Chaining**: Integrates all 11 FASTA steps perfectly, saving `FastqRun`, `FastaRun`, `AnnotationResult` (DIAMOND/Pfam), `TaxonomyResult`, and `ReportResult` database models.
