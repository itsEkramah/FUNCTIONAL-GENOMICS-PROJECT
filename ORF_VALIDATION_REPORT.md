# PathoScope AI — ORF Validation Report

**Date**: June 5, 2026  
**Auditor**: Antigravity  
**Status**: Completed  

---

## 1. Coordinate Mapping & Frame Handling Audit

We performed a deep inspection of `backend/core/orf_finder.py`, checking six-frame scanning and start/stop codon coordination.

### A. Scanning & Codon Detection
- Codons are scanned frame-by-frame starting at offset `frame` (0, 1, 2).
- Start codon is identified by `ATG` (0-indexed `orf_start`).
- Stop codons are identified by `TAA`, `TAG`, `TGA`.
- Minimum ORF length filter (default 100 bp) is applied: `orf_len >= min_len`.

### B. Strand Coordinate Translation
For the forward strand (`+`):
- `start_pos = orf_start + 1` (1-based index of first base of `ATG`).
- `end_pos = i + 3` (1-based index of last base of the stop codon).

For the reverse complement strand (`-`):
- `start_pos = seq_len - (i + 3) + 1`
- `end_pos = seq_len - orf_start`

### Mathematical Proof of RC Mapping:
Consider a genome of length `seq_len`. A 0-indexed position $k$ on the RC sequence corresponds to the 0-indexed position $seq\_len - 1 - k$ on the forward strand.
An RC ORF spans RC indices $[orf\_start, i + 2]$ (where $i+3$ is the exclusive end).
- The first base on RC (index $orf\_start$) corresponds to forward index $seq\_len - 1 - orf\_start$.
- The last base of the stop codon on RC (index $i + 2$) corresponds to forward index $seq\_len - 1 - (i + 2) = seq\_len - i - 3$.
Since transcription on the negative strand runs from high to low coordinates, the forward coordinates range from $seq\_len - i - 3$ to $seq\_len - 1 - orf\_start$.
In 1-based indexing:
- Start position = $(seq\_len - i - 3) + 1 = seq\_len - i - 2$.
- End position = $(seq\_len - 1 - orf\_start) + 1 = seq\_len - orf\_start$.

Our formulas:
- `start_pos = seq_len - (i + 3) + 1` = $seq\_len - i - 2$.
- `end_pos = seq_len - orf_start`.
Both match the mathematical derivation exactly. Coordinates are biologically correct.

---

## 2. Windows Filename Sanitization Fix

- **Issue**: Fasta headers with pipe characters (`|`) led to illegal filenames on Windows (e.g. `ENA|AF389121|AF389121.1_annotations.gff`).
- **Fix**: Added regex/character replacement in `BaseReport.get_output_path` to substitute all Windows illegal characters (`\ / : * ? " < > |`) with underscores (`_`).
