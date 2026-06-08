# FASTA_WORKFLOW_REPORT.md — FASTA Genome Annotation Workflow Report

This report outlines the biological workflow, execution steps, input/output validation, and reference logic sources for the FASTA genome annotation pipeline in PathoScope AI v3.0.

---

## Workflow Steps Overview

```
[Input FASTA File]
       │
       ▼
1. Input Validation (Verify headers and nucleotide alphabet)
       │
       ▼
2. Sequence QC (Length, GC%, ambiguous base count)
       │
       ▼
3. ORF Detection (6-frame scanning with 100 bp threshold)
       │
       ▼
4. Translation (Safe BioPython translation, codon truncation, to_stop=True)
       │
       ▼
5. DIAMOND Annotation (Homologous matching against SwissProt)
       │
       ▼
6. Pfam Annotation (hmmscan domain signatures)
       │
       ▼
7. KEGG Mapping (Viral entry & replication pathways)
       │
       ▼
8. NCBI Taxonomy (E-Utilities species lineage tree lookup)
       │
       ▼
9. PubMed Retrieval (Caching literature evidence fetch)
       │
       ▼
10. AI Interpretation (Evidence-grounded pathogen pathobiology report)
       │
       ▼
11. Report Generation (HTML, PDF, GFF3, CSV, and JSON outputs)
```

---

## Detailed Step Specifications

### 1. Input Validation
* **Input**: Uploaded FASTA raw sequence file (`.fasta`, `.fa`, `.fna`).
* **Output**: Verified sequence path or memory-staged sequence string.
* **Validation Checkpoint**: File must start with a `>` header line. Nucleotides must consist of standard IUPAC characters (`A`, `T`, `C`, `G`, `N`, `R`, `Y`, etc.). Characters must not be binary or empty.
* **Biological Rationale**: Prevents downstream syntax and parse errors by filtering out corrupt or invalid files (e.g. accidentally uploading FASTQ or DEG tables to the FASTA pipeline).
* **Repository Logic Source**: `clones/ORF-Finder/orf_finder.py` (header matching using regular expressions).

### 2. Sequence QC
* **Input**: Checked DNA sequence string.
* **Output**: QC metrics dictionary: `{ genome_length, gc_content, ambiguity_count }`.
* **Validation Checkpoint**: Length > 0 bp. Ambiguity count should be low (logged if `N` characters exceed 10% of total length).
* **Biological Rationale**: High GC content is characteristic of specific viral genomes. Ambiguous base counts measure sequence quality and assembly coverage.
* **Repository Logic Source**: Inspired by `clones/viralrecon` subworkflow base calculations.

### 3. ORF Detection
* **Input**: QC-checked DNA sequence.
* **Output**: List of identified open reading frames (coordinate start, end, strand, length, frame).
* **Validation Checkpoint**: ORF length must be >= `100 bp` (threshold imported from `thresholds.py`). Coordinates must reside within sequence boundaries.
* **Biological Rationale**: An ORF starting with `ATG` and ending with a stop codon (`TAA`, `TAG`, `TGA`) represents a candidate gene encoding a protein. Restricting to >= 100 bp reduces noise and false-positive calls.
* **Repository Logic Source**: `clones/ORF-Finder/orf_finder.py` (modified to support reverse-complement mapping and overlap-filtering).

### 4. Translation
* **Input**: Identified nucleotide ORF sequences.
* **Output**: Corresponding amino acid (peptide) sequences.
* **Validation Checkpoint**: Length > 0. Residues must map to standard standard genetic code characters. Safe translation truncates trailing non-triplets. Passes `to_stop=True` to prevent `KeyError('stop')` failures.
* **Biological Rationale**: Homology search programs (like blastp) align protein sequences, which are more conserved than nucleotide sequences.
* **Repository Logic Source**: `clones/biopython` (`Seq.translate`).

### 5. DIAMOND Annotation
* **Input**: Translated peptide sequence FASTA.
* **Output**: Homology mapping hits TSV.
* **Validation Checkpoint**: Hits filtered by: E-value <= `1e-5`, identity >= `30%`, alignment coverage >= `50%`.
* **Biological Rationale**: Aligns proteins against SwissProt to infer protein function based on homologous sequences with known activity.
* **Repository Logic Source**: `clones/diamond` (subprocess call and output format parsing).

### 6. Pfam Annotation
* **Input**: Translated peptide sequence FASTA.
* **Output**: Domain alignments file (`.domtbl`).
* **Validation Checkpoint**: Hits filtered by HMM E-value <= `1e-5`.
* **Biological Rationale**: Identifies structural domains and protein family motifs to suggest functional classifications when alignment matches fail.
* **Repository Logic Source**: `clones/viralrecon` (integrates Pfam domain annotation via HMMER/hmmscan).

### 7. KEGG Mapping
* **Input**: Annotated SwissProt protein names.
* **Output**: List of mapped pathway identifiers and pathway names.
* **Validation Checkpoint**: Pathway size matches limits: `15 <= pathway_size <= 500`.
* **Biological Rationale**: Maps annotated pathogen proteins to biological pathways to reveal replication, structural assembly, or host immune evasion mechanisms.
* **Repository Logic Source**: `clones/GSEApy` / custom mapping databases.

### 8. NCBI Taxonomy
* **Input**: Specified organism name or annotation hits species keywords.
* **Output**: Taxonomy metadata: taxonomic ID, rank, and complete lineage list.
* **Validation Checkpoint**: TaxID resolved. Correctly matches biological domains (e.g. Viruses, Bacteria).
* **Biological Rationale**: Determines exact evolutionary lineage of the target genome.
* **Repository Logic Source**: NCBI E-Utilities API documentation.

### 9. PubMed Retrieval
* **Input**: Organism name and annotated protein keywords.
* **Output**: Cached articles list (PMID, title, authors, journal, year, abstract, DOI).
* **Validation Checkpoint**: Avoid duplicate requests using local SQL cache search. Relevance scoring filters out unrelated abstracts.
* **Biological Rationale**: Automates literature search to collect scientific abstracts describing the pathobiology of the organism.
* **Repository Logic Source**: E-Utilities literature search protocols.

### 10. AI Interpretation
* **Input**: Full list of findings (QC, annotations, pathways, taxonomy) and PubMed abstracts.
* **Output**: Structuredpathology interpretation text.
* **Validation Checkpoint**: Output must follow exact headers (Findings, Evidence, Interpretation, Confidence, Limitations). Never invent claims. Returns "Insufficient evidence" if findings are empty.
* **Biological Rationale**: Translates raw bioinformatics tables into readable pathobiology summaries, grounded strictly in published research.
* **Repository Logic Source**: OpenAI and Gemini developer guides.

### 11. Report Generation
* **Input**: Pipeline run metadata, database entries, and logs.
* **Output**: GFF3, HTML, PDF, CSV, and JSON files written to job directory.
* **Validation Checkpoint**: File sizes > 0. Valid HTML and GFF3 formats.
* **Biological Rationale**: Provides shareable, publication-grade reports for clinical or lab environments.
* **Repository Logic Source**: Standard GFF3 v3 specifications and HTML5/CSS standards.
