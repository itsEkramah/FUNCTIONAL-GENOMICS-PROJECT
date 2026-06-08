# REPOSITORY_EXTRACTION_REPORT.md — Repository Extraction Report

This document details the exact directories, files, and modules within the `clones/` reference repositories that contain the algorithmic and architectural logic required to build **PathoScope AI v3.0**. 

---

## 1. ORF-Finder (clones/ORF-Finder)

* **Repository Name**: `ORF-Finder`
* **Folder**: Root folder (`/`)
* **File**: `orf_finder.py` (lines 79–246)
* **Purpose**: Coordinates 6-frame ORF codon scanning, start/stop codon coordinate calculations, sequence translation, and overlap elimination.
* **Why Needed**:
  * Implements the logic for checking all six reading frames (+1, +2, +3 on the forward strand, and -1, -2, -3 on the reverse complement).
  * Provides the `remove_overlap` logic, which compares all identified ORFs on the same strand and filters out shorter, overlapping candidate coordinates.
* **Whether to Copy Algorithm or Architecture**: Copy the **algorithm** for scanning (identifying `ATG` start codons and searching codon-by-codon for `TAA`, `TAG`, `TGA` stop codons) and overlap-filtering (filtering coordinate overlaps on the same strand).
* **Whether to Rewrite from Scratch**: **Rewrite from scratch**. The reference script is written as a flat, monolithic CLI utility with custom dictionaries. We must rewrite it into a modular, object-oriented class library (`backend/core/orf_finder.py`) that imports biological parameters (`MIN_ORF_LENGTH`) dynamically from our configurations and utilizes BioPython for core sequences.

---

## 2. biopython (clones/biopython)

* **Repository Name**: `biopython`
* **Folder**: `Bio/SeqIO` and `Bio`
* **Files**: 
  * `Bio/SeqIO/QualityIO.py` (line 839: `FastqGeneralIterator`)
  * `Bio/Seq.py` (line 2110: `translate()`, `reverse_complement()`)
* **Purpose**: Low-level sequence extraction, safe DNA-to-peptide translation, coordinate complements, and stream-based FASTQ parsing.
* **Why Needed**:
  * `FastqGeneralIterator` provides a high-performance, memory-safe parser that reads FASTQ records sequentially. This is crucial for handling large files (up to several GB) on a standard workstation without running out of RAM (enforcing Rule 6.5).
  * BioPython translation handles stop codon mapping and avoids terminating on partial codons or unknown nucleotides, which prevents raw `KeyError: stop` failures during annotation.
* **Whether to Copy Algorithm or Architecture**: Study the **architecture** and use BioPython directly as a core system dependency.
* **Whether to Rewrite from Scratch**: **Do not rewrite**. BioPython will be loaded as an external package dependency in `requirements.txt`. We will import its standard modules into `backend/core/orf_finder.py` and `backend/core/translator.py`.

---

## 3. OpenGene/fastp (clones/fastp)

* **Repository Name**: `fastp`
* **Folder**: `src/`
* **Files**:
  * `src/filter.cpp` (filtering quality and length bounds)
  * `src/jsonreporter.cpp` (metrics reporting format)
* **Purpose**: Preprocessing engine for NGS raw reads (trimming adapters, low-quality bases, and short reads).
* **Why Needed**:
  * Outlines the standard filters (Q20 quality scores, read length >= 50bp) that must be applied to FASTQ data.
  * Details the JSON report structure, which we must parse to extract filtered read counts, adapter insertions, and Q30 percentages.
* **Whether to Copy Algorithm or Architecture**: Copy the **architecture** (wrap fastp as a subprocess service) and the output parsing structure.
* **Whether to Rewrite from Scratch**: **Do not rewrite the tool**. We run the compiled `fastp` binary as an external executable wrapped by `backend/services/fastp_service.py`. We will rewrite the JSON parser from scratch in Python to map metrics directly to database schema columns.

---

## 4. DIAMOND (clones/diamond)

* **Repository Name**: `DIAMOND`
* **Folder**: Root folder (`/`)
* **File**: `README.md` and wiki documentation
* **Purpose**: High-throughput protein database search (blastp mode).
* **Why Needed**:
  * Documents the alignment CLI flags (e.g. `--very-sensitive -f 6`) and defines query identity, query coverage, and E-value outputs.
* **Whether to Copy Algorithm or Architecture**: Copy the **architecture** (subprocess wrapper and tabular output parsing).
* **Whether to Rewrite from Scratch**: **Do not rewrite the tool**. DIAMOND is a compiled binary. We will run it as a subprocess wrapped by `backend/services/diamond_service.py` and parse its TSV tabular outputs (`-f 6`) using Python's `csv` or `pandas` reader.

---

## 5. GSEApy (clones/GSEApy)

* **Repository Name**: `GSEApy`
* **Folder**: `gseapy/`
* **Files**:
  * `gseapy/enrichr.py` (Enrichr wrapper)
  * `gseapy/parser.py` (gene list mapping)
* **Purpose**: Gene Set Enrichment Analysis (GSEA) mapping for Gene Ontology (GO) terms and KEGG pathways.
* **Why Needed**:
  * Implements pathway mapping and enrichment statistics for our transcriptomics DEG workflow.
  * Helps us enforce the pathway filter limits (`15 <= pathway size <= 500` genes).
* **Whether to Copy Algorithm or Architecture**: Study the **architecture** and use GSEApy directly as a package dependency.
* **Whether to Rewrite from Scratch**: **Do not rewrite**. GSEApy will be imported directly as a Python library dependency. We will write `backend/services/kegg_service.py` to wrap GSEApy calls and load pathways data into Pydantic models.

---

## 6. deg-analysis-pipeline (clones/deg-analysis-pipeline)

* **Repository Name**: `deg-analysis-pipeline`
* **Folder**: Root folder (`/`)
* **File**: `DEG.py` (lines 78–800)
* **Purpose**: Preprocessing gene expression matrices, matching metadata categories, calculating p-values via t-tests, applying Benjamini-Hochberg FDR adjustments, and sorting significant genes.
* **Why Needed**:
  * Provides the exact calculations needed for `workflow_deg.py` and `backend/core/deg_engine.py`.
  * Demonstrates the classification logic: Upregulated (`log2FC >= 1`, `FDR <= 0.05`), Downregulated (`log2FC <= -1`, `FDR <= 0.05`), and Non-Significant.
* **Whether to Copy Algorithm or Architecture**: Copy the **algorithm** for Benjamini-Hochberg adjustment (via `statsmodels.stats.multitest.multipletests`) and the preprocessing log-transformation steps.
* **Whether to Rewrite from Scratch**: **Rewrite from scratch**. The reference code is a monolithic script designed for Google Colab notebooks with static matplotlib figures. We must modularize it into clean, unit-testable Python classes (`backend/core/deg_engine.py`), separate calculations from plotting, and return raw coordinates to the client for interactive charts (Recharts).

---

## 7. nf-core/viralrecon (clones/viralrecon)

* **Repository Name**: `nf-core/viralrecon`
* **Folders**: 
  * `workflows/`
  * `subworkflows/local/`
* **Files**:
  * `workflows/viralrecon.nf`
  * `subworkflows/local/fastq_trim_fastp_fastqc.nf`
* **Purpose**: Production-grade Nextflow pipeline mapping for raw NGS quality control, assembly, and downstream annotation.
* **Why Needed**:
  * Provides the industry-standard execution order for FASTQ files (FastQC on raw reads ──► fastp trimming ──► FastQC on trimmed reads ──► SPAdes assembly ──► Contig extraction).
* **Whether to Copy Algorithm or Architecture**: Copy the **architecture** (the sequential orchestration, input parameter checks, and validation checkpoints).
* **Whether to Rewrite from Scratch**: **Rewrite from scratch**. Nextflow DSL is compiled for Nextflow runtimes. We will translate the workflow sequence into Python pipeline steps managed by `pipeline_runner.py` and `workflow_fastq.py`.

---

## 8. ADDITIONAL BIOINFORMATICS TOOL REFERENCES

As outlined in the `GITHUB_REFERENCE.md` manual, we require three additional external repositories to study tool parameter configurations:

### HMMER
* **Purpose**: Wrap Pfam domain detection and parse tabular outputs.
* **Extraction**: Study CLI flags for `hmmscan` and map coordinate outputs in `backend/services/hmmer_service.py`.
* **Strategy**: Subprocess wrapper (do not copy HMMER code).

### FastQC
* **Purpose**: Verify quality report structures and outputs.
* **Extraction**: Study FastQC CLI outputs (HTML reports and ZIP files).
* **Strategy**: Subprocess wrapper (do not copy FastQC code).

### SPAdes
* **Purpose**: Configure genome assembly for RNA viruses.
* **Extraction**: Study SPAdes assembly parameters, focusing on `--rnaviral` mode.
* **Strategy**: Subprocess wrapper (do not copy SPAdes code).
