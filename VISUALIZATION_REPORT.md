# PathoScope AI Visualization System Report

The PathoScope AI platform features a robust, dedicated backend plotting engine in [visualization_engine.py](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/backend/core/visualization_engine.py) that generates publication-quality plots. These plots are seamlessly integrated into the Next.js results workspace and are automatically compiled into final HTML and PDF pipeline reports.

## 1. Backend Plotting Architecture
The plotting system is built on Matplotlib (`Agg` non-interactive backend) and Seaborn to guarantee high performance and styling flexibility. Plots are stored in `storage/jobs/<job_id>/visualizations/` in three vector and raster formats:
- **PNG** (300 DPI, optimized for fast web rendering)
- **SVG** (vector graphics, perfect for HTML report embedding and scaling)
- **PDF** (print quality, ideal for publication figures)

A JSON manifest file (`visualization_manifest.json`) is dynamically written upon completion, indexing all generated charts for fast API retrieval.

---

## 2. FASTA Pipeline Visualizations
For the genome/FASTA analysis workflow, the engine generates **6 distinct scientific charts**:

1. **Genome Base Composition (`genome_composition_pie`)**:
   - *Type*: Pie chart.
   - *Content*: Compares overall GC content vs. AT content, complete with total genome length labels.
2. **ORF Length Distribution (`orf_length_histogram`)**:
   - *Type*: Seaborn histogram with Kernel Density Estimate (KDE).
   - *Content*: Displays the frequency of detected open reading frames across length ranges.
3. **GC Content Sliding Window (`gc_sliding_window`)**:
   - *Type*: Line plot.
   - *Content*: Visualizes fluctuations in GC percentage across a 1000bp sliding window, highlighting localized GC skew relative to the genome average.
4. **Taxonomic Lineage Depth (`taxonomy_lineage_ranks`)**:
   - *Type*: Horizontal Seaborn bar chart.
   - *Content*: Maps taxonomic classification ranks (Genus, Family, Order, etc.) dynamically based on NCBI Taxonomy lookup.
5. **Pfam Domain Distribution (`pfam_domains_bar`)**:
   - *Type*: Horizontal bar chart.
   - *Content*: Displays frequencies of recognized structural Pfam domains in the predicted proteins.
6. **KEGG Pathway Map (`kegg_pathways_bar`)**:
   - *Type*: Horizontal bar chart.
   - *Content*: Shows gene hit counts across mapped KEGG metabolic and pathobiological pathways.

---

## 3. FASTQ Pipeline Visualizations
For the raw sequence/FASTQ assembly workflow, the engine compiles **5 quality control charts**:

1. **Phred Quality Score Distribution (`quality_score_distribution`)**:
   - *Type*: Double line plot.
   - *Content*: Compares mean quality scores per base position for raw reads vs. post-fastp trimmed reads, overlaying the standard Q20 threshold.
2. **GC Content Distribution (`gc_distribution`)**:
   - *Type*: Continuous distribution curve.
   - *Content*: Displays the percentage of reads matching a given average GC level.
3. **Read Length Distribution (`read_length_distribution`)**:
   - *Type*: Histogram.
   - *Content*: Shows base-pair length ranges of reads post-trimming.
4. **fastp Yield Summary (`fastqc_yield_comparison`)**:
   - *Type*: Bar chart.
   - *Content*: Summarizes the filtering performance (total raw reads vs. trimmed reads retained).
5. **SPAdes Assembly Contigs (`assembly_contigs_lengths`)**:
   - *Type*: Sorted bar chart.
   - *Content*: Renders the length distributions of the top 5 longest de-novo assembled contigs.

---

## 4. Frontend Workspace Integration
The Next.js workspace includes a fully functional **Visualizations Tab** within [ResultsViewer.tsx](file:///g:/LAST%20FINAL%20FUNCTIONAL%20GENOICS%20PROJECT/FUNCTIONAL%20GENOMICS%20PROJECT/frontend/components/ResultsViewer.tsx):
- Reads the relative web paths via the `/api/jobs/<job_id>/results` endpoint.
- Displays a clean, responsive CSS grid of cards for each generated chart.
- Includes smooth hover scale micro-animations for premium user experience.
- Provides a "View Full Size" button to open the high-res image directly in a new browser tab.
