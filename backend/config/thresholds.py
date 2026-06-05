"""
thresholds.py — Biological and Quality Threshold Configurations

This file contains all mandatory thresholds specified by the project rules and the professor.
No module may hardcode thresholds elsewhere; they must import from this module.
"""

# =============================================================================
# FASTA WORKFLOW THRESHOLDS
# =============================================================================

# Minimum length in base pairs for an Open Reading Frame (ORF) to be detected
MIN_ORF_LENGTH_BP = 100

# Maximum E-value allowed for DIAMOND homologous mapping alignments
DIAMOND_EVALUE_MAX = 1e-5

# Minimum percentage of identity required for DIAMOND alignments
DIAMOND_IDENTITY_MIN = 30.0  # 30%

# Minimum query alignment coverage required for DIAMOND hits
DIAMOND_COVERAGE_MIN = 50.0  # 50%


# =============================================================================
# FASTQ WORKFLOW THRESHOLDS
# =============================================================================

# Minimum Phred quality score for fastp read trimming
FASTQ_QUALITY_PHRED = 20  # Q20

# Minimum read length in base pairs to retain after fastp trimming
FASTQ_READ_LENGTH_MIN = 50  # 50 bp

# Minimum contig length in base pairs to keep post-SPAdes assembly
FASTQ_CONTIG_LENGTH_MIN = 500  # 500 bp


# =============================================================================
# DEG WORKFLOW THRESHOLDS
# =============================================================================

# Maximum False Discovery Rate (FDR) allowed for differential expression significance
DEG_FDR_MAX = 0.05

# Minimum Log2 Fold Change for upregulated gene classification
DEG_LOG2FC_UP = 1.0

# Maximum Log2 Fold Change for downregulated gene classification
DEG_LOG2FC_DOWN = -1.0

# Minimum gene count in a pathway to include in ORA/enrichment analysis
PATHWAY_SIZE_MIN = 15

# Maximum gene count in a pathway to include in ORA/enrichment analysis
PATHWAY_SIZE_MAX = 500
