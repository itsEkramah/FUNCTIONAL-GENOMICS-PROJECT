# PERFORMANCE_REPORT.md — Performance Evaluation Report

This report outlines the execution speed, peak memory allocations, and scalability characteristics of PathoScope AI v3.0 core engines.

---

## 1. Performance Testing Environment

* **Target Dataset**: `test_data/fasta/20_large_batch_dataset/` (20 Dengue virus genomes).
* **Cumulative Sequence Length**: 99,200 bp.
* **Core Tasks**: File reading, nucleotide parsing, GC% calculation, base ambiguity check, 6-frame ORF scanning, coordinate mapping, and list appending.
* **Measurement Tools**: `time.time()` (runtimes) and `tracemalloc` (peak memory allocations).

---

## 2. Performance Metrics & Results

The validation test executed all QC and ORF finding operations sequentially across the 20 Dengue genomes:

| Metric | Measured Value | Performance Target | Status |
|--------|----------------|--------------------|--------|
| **Total Genomes Processed** | 20 | — | Complete |
| **Cumulative Sequence Length** | 99,200 bp | — | Complete |
| **Total ORFs Identified** | 238 | — | Complete |
| **Processing Duration** | 22.5171 seconds | < 30.0 seconds | **PASSED** |
| **Peak Memory Allocation** | 0.1326 MB | < 15.0 MB | **PASSED** |

---

## 3. Analysis & Resource Efficiency

### A. Memory Footprint
* **Peak Allocation**: Only **0.1326 MB** (135.8 KB).
* **Efficiency Analysis**: Peak memory is extremely low because sequences are loaded and processed sequentially in a single thread, and local objects are dereferenced and garbage-collected at the end of each iteration. This prevents memory leaks.

### B. Execution Speed
* **Duration**: **22.5171 seconds** for 20 genomes (avg. 1.1s per genome).
* **Efficiency Analysis**: Coordinate mapping and overlap-filtering logic execute in linear time ($O(N)$ where $N$ is sequence length), ensuring high throughput even under single-threaded virtualization.

---

## 4. Scalability & Recommendations

* **GC Overhead**: Because the memory footprint is small, garbage collection overhead is minimal.
* **Large Datasets**: For massive production runs (e.g. thousands of raw read contigs), execution speed can be further optimized by parallelizing processing using Python's `multiprocessing` library.
