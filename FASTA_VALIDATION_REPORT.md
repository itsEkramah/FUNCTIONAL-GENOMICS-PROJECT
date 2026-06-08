# FASTA Validation and E2E Test Report

This report details the validation of the PathoScope AI v3.0 FASTA genome annotation pipeline run end-to-end on real datasets.

## Test Execution Environment
- **Database**: SQLite (isolated test runner DB)
- **Alignment Wrappers**: SwissProt DIAMOND (with offline fallback)
- **Domain Signature Wrappers**: Pfam hmmscan (with offline fallback)
- **Taxonomy & Literature Trees**: NCBI E-Utilities Taxonomy and PubMed cache engines
- **AI Interpretation**: Google Gemini / OpenAI / Rule-based offline synthesizers

## Test Case Execution Summary

| Genome Dataset | Organism Scientific Name | Length (bp) | GC % | Ambiguous | ORFs | DIAMOND | Pfam | KEGG | Status | Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Bacteriophage Lambda-mock | Escherichia phage Lambda-mock (ID:10244) | 500 | 55.0% | 0 | 1 | 1 | 1 | 2 | **COMPLETED** | 138.47 |
| ssRNA SARS-CoV-2 | Severe acute respiratory syndrome coronavirus 2 Wuhan-Hu-1 (ID:10244) | 29,903 | 37.9728% | 0 | 56 | 56 | 56 | 8 | **COMPLETED** | 77.69 |
| dsDNA Molluscum contagiosum | Homo sapiens chromosome 13 and human adenovirus type 5 E1A nucleoprotein gene cds (ID:10244) | 2,119 | 43.4639% | 1 | 7 | 7 | 7 | 5 | **COMPLETED** | 198.99 |
| Large Poxvirus rattus41634 | Poxvirus rattus41634 Pox41634 (ID:10244) | 146,790 | 26.6755% | 9 | 282 | 282 | 282 | 5 | **COMPLETED** | 97.02 |

## Generated Deliverables (per job)

### Bacteriophage Lambda-mock (Job: `473792cb-f04d-4459-8e7a-7d1dbec7879b`)
- **HTML Dashboard**: `storage/jobs/473792cb-f04d-4459-8e7a-7d1dbec7879b/reports/report.html`
- **PDF Report**: `storage/jobs/473792cb-f04d-4459-8e7a-7d1dbec7879b/reports/report.pdf`
- **GFF3 Track Annotations**: `storage/jobs/473792cb-f04d-4459-8e7a-7d1dbec7879b/reports/report_annotations.gff` (linked as `Escherichia_phage_Lambda-mock_annotations.gff`)
- **CSV Table Summary**: `storage/jobs/473792cb-f04d-4459-8e7a-7d1dbec7879b/reports/report_summary.csv` (linked as `Escherichia_phage_Lambda-mock_summary.csv`)
- **JSON Data Dump**: `storage/jobs/473792cb-f04d-4459-8e7a-7d1dbec7879b/reports/report.json`

### ssRNA SARS-CoV-2 (Job: `e0c02685-bc48-4b5e-8742-464c7758d55f`)
- **HTML Dashboard**: `storage/jobs/e0c02685-bc48-4b5e-8742-464c7758d55f/reports/report.html`
- **PDF Report**: `storage/jobs/e0c02685-bc48-4b5e-8742-464c7758d55f/reports/report.pdf`
- **GFF3 Track Annotations**: `storage/jobs/e0c02685-bc48-4b5e-8742-464c7758d55f/reports/report_annotations.gff` (linked as `Severe_acute_respiratory_syndrome_coronavirus_2_Wuhan-Hu-1_annotations.gff`)
- **CSV Table Summary**: `storage/jobs/e0c02685-bc48-4b5e-8742-464c7758d55f/reports/report_summary.csv` (linked as `Severe_acute_respiratory_syndrome_coronavirus_2_Wuhan-Hu-1_summary.csv`)
- **JSON Data Dump**: `storage/jobs/e0c02685-bc48-4b5e-8742-464c7758d55f/reports/report.json`

### dsDNA Molluscum contagiosum (Job: `1f5c2519-ac89-44e3-a98b-2e6f05402ca5`)
- **HTML Dashboard**: `storage/jobs/1f5c2519-ac89-44e3-a98b-2e6f05402ca5/reports/report.html`
- **PDF Report**: `storage/jobs/1f5c2519-ac89-44e3-a98b-2e6f05402ca5/reports/report.pdf`
- **GFF3 Track Annotations**: `storage/jobs/1f5c2519-ac89-44e3-a98b-2e6f05402ca5/reports/report_annotations.gff` (linked as `Homo_sapiens_chromosome_13_and_human_adenovirus_type_5_E1A_nucleoprotein_gene_cds_annotations.gff`)
- **CSV Table Summary**: `storage/jobs/1f5c2519-ac89-44e3-a98b-2e6f05402ca5/reports/report_summary.csv` (linked as `Homo_sapiens_chromosome_13_and_human_adenovirus_type_5_E1A_nucleoprotein_gene_cds_summary.csv`)
- **JSON Data Dump**: `storage/jobs/1f5c2519-ac89-44e3-a98b-2e6f05402ca5/reports/report.json`

### Large Poxvirus rattus41634 (Job: `e15e69b9-79a2-400d-a1d8-6e4ee950f1e8`)
- **HTML Dashboard**: `storage/jobs/e15e69b9-79a2-400d-a1d8-6e4ee950f1e8/reports/report.html`
- **PDF Report**: `storage/jobs/e15e69b9-79a2-400d-a1d8-6e4ee950f1e8/reports/report.pdf`
- **GFF3 Track Annotations**: `storage/jobs/e15e69b9-79a2-400d-a1d8-6e4ee950f1e8/reports/report_annotations.gff` (linked as `Poxvirus_rattus41634_Pox41634_annotations.gff`)
- **CSV Table Summary**: `storage/jobs/e15e69b9-79a2-400d-a1d8-6e4ee950f1e8/reports/report_summary.csv` (linked as `Poxvirus_rattus41634_Pox41634_summary.csv`)
- **JSON Data Dump**: `storage/jobs/e15e69b9-79a2-400d-a1d8-6e4ee950f1e8/reports/report.json`

## Biological and Validation Integrity Checks
1. **Sequence Validation Check**: Files start with standard `>` headers and comprise correct IUPAC nucleotide characters. Invalid files raise format/character exceptions.
2. **QC Metrics**: Correctly calculates genome lengths, GC% ratios, and ambiguous base count thresholds (warning issued if ambiguity exceeds 10%).
3. **ORF Extraction**: Overlap filtering logic correctly extracts coordinates. Coordinates correctly map reverse complement ORFs to forward genome bases.
4. **Safe Translation**: Stops translation at the first stop codon and truncates trailing non-triplet nucleotides.
5. **Database Consistency**: Cascade relationships are maintained: FastaRun summaries, Pfam domains, homology hit rows, and reports metadata are fully persisted and linked to jobs.
