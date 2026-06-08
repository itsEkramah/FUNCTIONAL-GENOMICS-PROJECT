# PathoScope AI — Scientific Correctness Audit Report

**Date**: June 5, 2026  
**Auditor**: Antigravity  
**Status**: Completed  

---

## 1. Executive Summary

This audit report evaluates the biological correctness, computational validity, and pipeline integration of the PathoScope AI platform. We have inspected the entire codebase, reference clones, and execution flow. While the platform contains robust core scientific logic (e.g. 6-frame ORF scanning, Benjamini-Hochberg FDR correction, t-test calculations, and streaming FASTQ quality parsing), several components rely on hardcoded fallback results, mock components, or incomplete integrations.

---

## 2. Module Audit Classifications

### A. Real Modules (Computational & Biologically Correct)
- **FASTA Input Validator**: Reads sequence data, detects format, and validates IUPAC nucleotide characters.
- **Genome QC**: Computes real genome length, GC content, and base ambiguity counts.
- **6-Frame ORF Detector**: Scans forward and reverse complement strands in three reading frames, filtering by length (>= 100 bp) and resolving overlaps.
- **Translation Engine**: Translates DNA to peptide sequences using BioPython.
- **FASTQ Streaming QC & Trimming Fallbacks**: Streams raw reads, calculates exact quality stats, and filters low-quality bases (Q20, length >= 50 bp) in Python if external binaries are missing.
- **DEG Statistical Classifier**: Performs Welch's t-test on count matrices and multiple testing correction using Benjamini-Hochberg FDR.
- **PubMed NCBI E-Utilities Client**: Generates queries, fetches XML records, and parses abstracts, title, year, journal, MeSH terms, and author details.

### B. Mocked / Placeholder Modules (Requires Repair)
- **DIAMOND Aligner Fallback (`diamond_service.py`)**: If the command line aligner is missing or fails, the offline fallback writes hardcoded homologous hits (`REF_seq_1_POL` with 92.5% identity and 1e-42 E-value) for all query sequences, disregarding dataset content.
- **HMMER hmmscan Fallback (`hmmer_service.py`)**: If hmmscan is missing, the fallback writes the identical `PF00948` (Flavi_NS5) domain mapping with fixed coordinates `[50, 280]` for all sequences.
- **KEGG Pathway Mapper (`kegg_service.py`)**: Performs mapping by checking if accessions contain substrings like "POL", "RDRP", "ENV", "GLYCO", which relies entirely on mock homology hit descriptions.
- **SPAdes Assembler Fallback (`spades_service.py`)**: Copies a static reference SARS-CoV-2 genome (`NC_045512.2.fasta`) if assembly fails, which behaves as a static mock sequence.
- **Frontend Volcano Plot (`VolcanoPlot.tsx`)**: Renders a hardcoded SVG with static coordinates and fixed genes (e.g. TP53, TNF).
- **Frontend Gene Drill-Down**: Displays a hardcoded list of human genes (MAPK1, IL6, TNF, TP53, EGFR, STAT3) on the DEG dashboard.

### C. Incomplete Modules (Requires Repair)
- **FASTA & FASTQ Plot Generation**: No plotting or visualization is implemented in the backend for genome statistics or read quality.
- **GFF3/CSV Windows Reports**: Fails on Windows systems with `[Errno 22] Invalid argument` if sequence headers contain pipe characters (`|`), as the raw ID is used to construct GFF3/CSV filenames.
- **HTML/PDF Reports**: Both reports lack major required sections (e.g. execution stats, visualizations gallery, threshold details, and software versions) and are not of publication-quality.
- **AI Keys configuration**: The parser doesn't strip enclosing quotes (`"`) from environment variables, which can break the Google Gemini/OpenAI API configurations.
- **PubMed Redesign**: There is no independent page or dashboard for lit search. PubMed data is tightly bound to the AI pathobiology module.

---

## 3. Recommended Action Plan

1. **Filename Sanitization**: Implement Windows-compatible filename cleaning globally.
2. **Dynamic Homology fallbacks**: Implement a Python-based alignment matching query sequences against reference sets to generate dynamic identity%, coverage%, bitscore, and e-values.
3. **DEG Performance Tuning**: Vectorise the pandas row-median imputation to resolve hangs.
4. **Matplotlib Visualizations**: Build backend plotting modules for FASTA, FASTQ, and DEG.
5. **Report Upgrades**: Enhance HTML and PDF report generation.
6. **PubMed dashboard**: Decouple PubMed search into its own view and dashboard API.
