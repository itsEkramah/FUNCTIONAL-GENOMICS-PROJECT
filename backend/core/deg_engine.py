import os
import re
import gzip
import shutil
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, fisher_exact, t
from statsmodels.stats.multitest import multipletests
from typing import List, Dict, Any, Tuple, Optional

# =============================================================================
# DEFAULT THRESHOLD PARAMETERS (GEO2R / DESeq2 compatible defaults)
# =============================================================================
DEFAULT_FDR_THRESHOLD = 0.05      # BH-FDR adjusted p-value threshold
DEFAULT_LFC_THRESHOLD = 1.0       # log2 fold-change threshold (|log2FC| >= 1.0 = 2-fold)
DEFAULT_MIN_CPM = 0.5             # Minimum mean log-CPM to keep a gene (pre-filter)
DEFAULT_MIN_SAMPLE_FRAC = 0.20   # Minimum fraction of samples with CPM > 0

# =============================================================================
# SAMPLE GROUP AUTO-DETECTION
# =============================================================================

# Keywords that identify Control / Reference group samples
_CONTROL_KEYWORDS = [
    "mock", "control", "ctrl", "cntrl", "normal", "healthy", "wt",
    "wildtype", "wild_type", "baseline", "vehicle", "untreated", "nt",
    "neg", "negative", "ref", "reference", "uninfected", "naive"
]

# Keywords that identify Treatment / Disease / Condition group samples
_TREATMENT_KEYWORDS = [
    "sars", "cov", "covid", "infected", "infection", "treated", "treatment",
    "stimulated", "tnf", "il", "ifn", "virus", "viral", "lps", "rna",
    "disease", "patient", "tumor", "cancer", "mutant", "ko", "knockout",
    "knockdown", "kd", "overexpression", "oe", "induced", "dox", "siRNA",
    "drug", "rux", "dex", "treated", "stressed", "hypoxia", "hpiv", "rsv",
    "iav", "ebola", "flu", "h1n1", "h5n1", "mers"
]

def detect_sample_groups(
    column_names: List[str],
    log_logger=None
) -> Tuple[List[str], List[str], str, float]:
    """
    Automatically detects Control (Group 1) vs Treatment/Disease (Group 2) samples
    by matching column names against curated keyword lists.

    Returns:
        (group1_cols, group2_cols, detection_method, confidence_score)
        where confidence_score is 0.0-1.0 (1.0 = all samples classified by keywords)
    """
    control_cols = []
    treatment_cols = []
    unclassified = []

    for col in column_names:
        col_lower = col.lower()
        is_ctrl = any(kw in col_lower for kw in _CONTROL_KEYWORDS)
        is_treat = any(kw in col_lower for kw in _TREATMENT_KEYWORDS)

        if is_ctrl and not is_treat:
            control_cols.append(col)
        elif is_treat and not is_ctrl:
            treatment_cols.append(col)
        elif is_ctrl and is_treat:
            # Ambiguous — prefer treatment keyword if it appears later/more prominently
            treatment_cols.append(col)
        else:
            unclassified.append(col)

    total = len(column_names)
    classified = len(control_cols) + len(treatment_cols)
    confidence = classified / total if total > 0 else 0.0

    if log_logger:
        log_logger.info(
            f"[GroupDetect] Keyword match: Control={len(control_cols)}, "
            f"Treatment={len(treatment_cols)}, Unclassified={len(unclassified)}, "
            f"Confidence={confidence:.0%}"
        )

    # Case 1: Good keyword detection (>= 60% of samples classified and both groups non-empty)
    if confidence >= 0.6 and control_cols and treatment_cols:
        detection_method = "keyword_match"
        if log_logger:
            log_logger.info(
                f"[GroupDetect] Method: keyword_match | "
                f"Control ({len(control_cols)}): {control_cols[:5]} ... | "
                f"Treatment ({len(treatment_cols)}): {treatment_cols[:5]} ..."
            )
        return control_cols, treatment_cols, detection_method, confidence

    # Case 2: Partial match — try distributing unclassified to the smaller group
    if control_cols or treatment_cols:
        # Add unclassified to whichever group needs them for balance
        if not control_cols:
            # All classified as treatment, put unclassified into control
            mid_u = len(unclassified) // 2
            control_cols = unclassified[:mid_u] if mid_u > 0 else unclassified[:1]
            treatment_cols = treatment_cols + unclassified[mid_u:]
        elif not treatment_cols:
            mid_u = len(unclassified) // 2
            treatment_cols = unclassified[:mid_u] if mid_u > 0 else unclassified[:1]
            control_cols = control_cols + unclassified[mid_u:]
        else:
            # Distribute unclassified to smaller group to balance sizes
            for u in unclassified:
                if len(control_cols) <= len(treatment_cols):
                    control_cols.append(u)
                else:
                    treatment_cols.append(u)

        detection_method = "keyword_partial"
        if log_logger:
            log_logger.warning(
                f"[GroupDetect] Method: keyword_partial (confidence={confidence:.0%}). "
                f"Unclassified samples distributed by group size."
            )
        return control_cols, treatment_cols, detection_method, confidence

    # Case 3: No keywords matched — fallback to first-third vs last-third positional split
    # (avoids naive 50/50 midpoint which systematically mixes alternating layouts)
    n = len(column_names)
    split_a = max(1, n // 3)
    split_b = max(split_a + 1, n - n // 3)
    control_cols = column_names[:split_a]
    treatment_cols = column_names[split_b:]
    if not treatment_cols:
        treatment_cols = column_names[split_a:]

    detection_method = "positional_thirds"
    if log_logger:
        log_logger.warning(
            f"[GroupDetect] Method: positional_thirds (no keyword matches found). "
            f"Control=first {len(control_cols)} samples, Treatment=last {len(treatment_cols)} samples."
        )
    return control_cols, treatment_cols, detection_method, 0.0


# =============================================================================
# LOW-EXPRESSION GENE PRE-FILTERING
# =============================================================================

def filter_low_expression_genes(
    df_expr: pd.DataFrame,
    min_mean_cpm: float = DEFAULT_MIN_CPM,
    min_sample_frac: float = DEFAULT_MIN_SAMPLE_FRAC,
    log_logger=None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Removes genes with very low expression across samples before statistical testing.

    Filters applied (both must pass):
    1. Mean expression across all samples >= min_mean_cpm (default 0.5 log-CPM)
    2. At least min_sample_frac fraction of samples have expression > 0

    Returns:
        (filtered_df, report_dict)
    """
    n_before = len(df_expr)
    numeric_cols = df_expr.select_dtypes(include=[np.number]).columns.tolist()

    if not numeric_cols:
        report = {"n_before": n_before, "n_after": n_before, "n_removed": 0, "filter_applied": False}
        return df_expr, report

    expr_vals = df_expr[numeric_cols].values.astype(float)
    n_samples = expr_vals.shape[1]

    # Filter 1: Mean expression threshold
    mean_expr = np.mean(expr_vals, axis=1)
    keep_mean = mean_expr >= min_mean_cpm

    # Filter 2: Minimum fraction of non-zero samples
    nonzero_frac = np.sum(expr_vals > 0, axis=1) / n_samples
    keep_nonzero = nonzero_frac >= min_sample_frac

    keep_mask = keep_mean & keep_nonzero
    df_filtered = df_expr[keep_mask].copy()
    n_after = len(df_filtered)
    n_removed = n_before - n_after

    report = {
        "n_before": n_before,
        "n_after": n_after,
        "n_removed": n_removed,
        "pct_removed": round((n_removed / n_before * 100) if n_before > 0 else 0.0, 2),
        "filter_applied": True,
        "min_mean_cpm": min_mean_cpm,
        "min_sample_frac": min_sample_frac,
        "n_removed_by_low_mean": int(np.sum(~keep_mean)),
        "n_removed_by_low_coverage": int(np.sum(keep_mean & ~keep_nonzero))
    }

    if log_logger:
        log_logger.info(
            f"[PreFilter] Genes before: {n_before:,} | Removed (low expr): {n_removed:,} "
            f"({report['pct_removed']:.1f}%) | Remaining: {n_after:,}"
        )
        log_logger.info(
            f"[PreFilter]   - Removed by low mean (<{min_mean_cpm}): {report['n_removed_by_low_mean']:,}"
        )
        log_logger.info(
            f"[PreFilter]   - Removed by low coverage (<{min_sample_frac:.0%}): {report['n_removed_by_low_coverage']:,}"
        )

    return df_filtered, report

def decompress_gzip(file_path: str, output_dir: str, log_logger=None) -> str:
    """
    Checks if a file is gzip compressed, decompresses it if necessary, and returns the path.
    """
    if not file_path.endswith(".gz"):
        if log_logger:
            log_logger.info(f"File is not compressed: {file_path}")
        return file_path

    os.makedirs(output_dir, exist_ok=True)
    decompressed_name = os.path.basename(file_path)[:-3]  # Strip .gz
    decompressed_path = os.path.join(output_dir, decompressed_name)

    if log_logger:
        log_logger.info(f"Decompressing {file_path} to {decompressed_path}")

    with gzip.open(file_path, "rb") as f_in:
        with open(decompressed_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    if log_logger:
        log_logger.info(f"Decompression successful. File size: {os.path.getsize(decompressed_path)} bytes")

    return decompressed_path

def normalize_gene_ids(gene_list: List[str], log_logger=None) -> List[str]:
    """
    Strips gene ID versions (e.g. ENSG00000139618.15 -> ENSG00000139618).
    """
    normalized = []
    for gene in gene_list:
        if not gene or pd.isna(gene):
            normalized.append("")
            continue
        normalized.append(str(gene).split(".")[0].strip())
    return normalized

def apply_bh_fdr(pvalues: List[float], log_logger=None) -> List[float]:
    """
    Applies Benjamini-Hochberg False Discovery Rate multiple-testing correction.
    """
    if not pvalues:
        return []
        
    valid_indices = []
    valid_pvals = []
    
    for idx, p in enumerate(pvalues):
        if p is not None and not np.isnan(p):
            valid_indices.append(idx)
            valid_pvals.append(float(p))
            
    adjusted = [1.0] * len(pvalues)
    
    if valid_pvals:
        _, adj_pvals, _, _ = multipletests(valid_pvals, method="fdr_bh")
        for i, val in zip(valid_indices, adj_pvals):
            adjusted[i] = float(val)
            
    return adjusted

def classify_degs(
    log2fcs: List[float],
    fdrs: List[float],
    fdr_threshold: float = DEFAULT_FDR_THRESHOLD,
    lfc_threshold: float = DEFAULT_LFC_THRESHOLD,
    log_logger=None
) -> List[str]:
    """
    Classifies differential gene expression regulation based on configurable fold change
    and FDR thresholds (GEO2R / DESeq2 compatible defaults: padj<0.05, |log2FC|>=1.0).
    """
    classes = []
    for log2fc, fdr in zip(log2fcs, fdrs):
        if log2fc is None or fdr is None or np.isnan(log2fc) or np.isnan(fdr):
            classes.append("Not Significant")
            continue

        if fdr < fdr_threshold:
            if log2fc >= lfc_threshold:
                classes.append("UP")
            elif log2fc <= -lfc_threshold:
                classes.append("DOWN")
            else:
                classes.append("Not Significant")
        else:
            classes.append("Not Significant")

    return classes

def normalize_matrix(df: pd.DataFrame, log_logger=None) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Identifies if a DataFrame represents raw counts or normalized counts,
    prevents double normalization, and applies log2 transformation if needed.
    """
    # Exclude non-numeric columns for statistical validation
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        raise ValueError("No numeric sample columns found in matrix.")

    max_val = numeric_df.max().max()
    is_log = max_val < 30
    
    # Check if values are mostly integers to determine raw counts
    # A threshold of 99% integers handles rounding/floating-point representation of integers
    non_zero_vals = numeric_df.values[numeric_df.values > 0]
    if len(non_zero_vals) > 0:
        is_integer = np.allclose(non_zero_vals, np.round(non_zero_vals), rtol=1e-5)
    else:
        is_integer = True

    report = {
        "max_value": float(max_val),
        "is_log_transformed": bool(is_log),
        "is_integer_counts": bool(is_integer)
    }

    if is_log:
        if log_logger:
            log_logger.info(f"Skipping normalization: matrix is already log-transformed (max_val={max_val:.2f} < 30).")
        report["status"] = "Skipped (Already log-transformed)"
        return df, report

    # Perform Normalization
    df_norm = df.copy()
    if is_integer:
        if log_logger:
            log_logger.info("Raw counts detected. Applying CPM (Counts Per Million) and log2 transformation.")
        # CPM normalization: cpm = count / lib_size * 1e6
        col_sums = numeric_df.sum(axis=0)
        # Avoid division by zero
        col_sums = col_sums.replace(0, 1)
        
        for col in numeric_df.columns:
            df_norm[col] = (df_norm[col] / col_sums[col]) * 1000000
            df_norm[col] = np.log2(df_norm[col] + 1)
        report["status"] = "Applied CPM + log2(CPM+1)"
    else:
        if log_logger:
            log_logger.info("Normalized non-log counts (FPKM/TPM) detected. Applying log2(val + 1) transformation.")
        for col in numeric_df.columns:
            df_norm[col] = np.log2(df_norm[col] + 1)
        report["status"] = "Applied log2(val+1)"

    return df_norm, report

def run_differential_statistics(
    df_expr: pd.DataFrame,
    group1_cols: List[str],
    group2_cols: List[str],
    fdr_threshold: float = DEFAULT_FDR_THRESHOLD,
    lfc_threshold: float = DEFAULT_LFC_THRESHOLD,
    min_cpm: float = DEFAULT_MIN_CPM,
    min_sample_frac: float = DEFAULT_MIN_SAMPLE_FRAC,
    log_logger=None,
    job_dir: Optional[str] = None
) -> pd.DataFrame:
    """
    Computes fold changes (Treatment vs Control), Welch's t-test p-values, and
    BH-FDR adjusted p-values using vectorized numpy calculations.

    Applies low-expression gene pre-filtering before testing to maximize
    statistical power of BH-FDR correction.
    """
    if log_logger:
        log_logger.info(
            f"[DiffStats] Control (Group 1): {len(group1_cols)} samples | "
            f"Treatment (Group 2): {len(group2_cols)} samples"
        )
        log_logger.info(
            f"[DiffStats] Thresholds: FDR<{fdr_threshold}, |log2FC|>={lfc_threshold}, "
            f"min_CPM={min_cpm}, min_sample_frac={min_sample_frac:.0%}"
        )

    # Pre-filter low-expression genes to improve BH-FDR power
    df_filtered, filter_report = filter_low_expression_genes(
        df_expr, min_mean_cpm=min_cpm, min_sample_frac=min_sample_frac, log_logger=log_logger
    )

    if job_dir and filter_report:
        import json
        with open(os.path.join(job_dir, "prefilter_report.json"), "w") as f:
            json.dump(filter_report, f, indent=4)

    if df_filtered.empty:
        if log_logger:
            log_logger.warning("[DiffStats] All genes filtered out by low-expression filter — returning empty results.")
        return pd.DataFrame(columns=["gene_id", "Group1_mean", "Group2_mean", "log2FoldChange", "pvalue", "padj", "regulation"])

    # Ensure group columns exist in filtered df
    g1 = [c for c in group1_cols if c in df_filtered.columns]
    g2 = [c for c in group2_cols if c in df_filtered.columns]

    if not g1 or not g2:
        if log_logger:
            log_logger.error("[DiffStats] One or both groups have no valid columns after pre-filtering.")
        return pd.DataFrame(columns=["gene_id", "Group1_mean", "Group2_mean", "log2FoldChange", "pvalue", "padj", "regulation"])

    X1 = df_filtered[g1].values.astype(float)
    X2 = df_filtered[g2].values.astype(float)

    N1 = X1.shape[1]
    N2 = X2.shape[1]

    # Calculate means
    M1 = np.mean(X1, axis=1)
    M2 = np.mean(X2, axis=1)

    # Calculate variances
    V1 = np.var(X1, axis=1, ddof=1) if N1 > 1 else np.zeros(X1.shape[0])
    V2 = np.var(X2, axis=1, ddof=1) if N2 > 1 else np.zeros(X2.shape[0])

    # Welch's t-test formula
    denom = np.sqrt(V1 / N1 + V2 / N2)
    denom_safe = np.where(denom == 0, 1.0, denom)
    t_stat = (M2 - M1) / denom_safe

    # Welch-Satterthwaite degrees of freedom
    num_df = (V1 / N1 + V2 / N2) ** 2
    denom_df = (V1 / N1) ** 2 / max(N1 - 1, 1) + (V2 / N2) ** 2 / max(N2 - 1, 1)
    denom_df_safe = np.where(denom_df == 0, 1.0, denom_df)
    df_welch = num_df / denom_df_safe

    # Two-tailed p-value using the survival function
    p_vals = t.sf(np.abs(t_stat), df_welch) * 2

    # Handle zero variance or NaN
    p_vals = np.where(denom == 0, 1.0, p_vals)
    p_vals = np.where(np.isnan(p_vals), 1.0, p_vals)
    p_vals = np.clip(p_vals, 0.0, 1.0)

    log2fc = M2 - M1

    results_df = pd.DataFrame({
        "gene_id": df_filtered.index.astype(str),
        "Group1_mean": M1,
        "Group2_mean": M2,
        "log2FoldChange": log2fc,
        "pvalue": p_vals
    })

    results_df["padj"] = apply_bh_fdr(results_df["pvalue"].tolist(), log_logger)
    results_df["regulation"] = classify_degs(
        results_df["log2FoldChange"].tolist(),
        results_df["padj"].tolist(),
        fdr_threshold=fdr_threshold,
        lfc_threshold=lfc_threshold,
        log_logger=log_logger
    )

    sig_count = (results_df["regulation"].isin(["UP", "DOWN"])).sum()
    if log_logger:
        log_logger.info(
            f"[DiffStats] Results: {len(results_df):,} genes tested | "
            f"{sig_count:,} significant (FDR<{fdr_threshold}, |log2FC|>={lfc_threshold})"
        )

    return results_df

def load_annotation_mapping(annot_path: str, log_logger=None) -> Dict[str, str]:
    """
    Loads Human.GRCh38.p13.annot.tsv and creates mapping dictionary: Entrez ID / Ensembl ID -> Symbol
    """
    if log_logger:
        log_logger.info(f"Loading annotation mapping from {annot_path}")
        
    mapping = {}
    try:
        # Handle compressed annotation path directly
        if annot_path.endswith(".gz"):
            f = gzip.open(annot_path, "rt", encoding="utf-8")
        else:
            f = open(annot_path, "r", encoding="utf-8")
            
        # Parse headers
        header = f.readline().strip().split("\t")
        col_indices = {col: i for i, col in enumerate(header)}
        
        # We need Symbol, GeneID (Entrez), and EnsemblGeneID
        symbol_idx = col_indices.get("Symbol")
        gene_id_idx = col_indices.get("GeneID")
        ensembl_idx = col_indices.get("EnsemblGeneID")
        
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) <= max(idx for idx in [symbol_idx, gene_id_idx, ensembl_idx] if idx is not None):
                continue
                
            symbol = parts[symbol_idx].strip()
            if not symbol:
                continue
                
            # Add identity mapping
            mapping[symbol.upper()] = symbol
            
            # Map Entrez GeneID
            if gene_id_idx is not None:
                gene_id = parts[gene_id_idx].strip()
                if gene_id:
                    mapping[gene_id] = symbol
                    
            # Map Ensembl ID
            if ensembl_idx is not None:
                ensembl_id = parts[ensembl_idx].strip()
                if ensembl_id:
                    # Map clean version and dot version
                    mapping[ensembl_id.upper()] = symbol
                    if "." in ensembl_id:
                        mapping[ensembl_id.split(".")[0].upper()] = symbol
                        
        f.close()
        if log_logger:
            log_logger.info(f"Successfully loaded {len(mapping)} gene mapping relationships.")
    except Exception as e:
        if log_logger:
            log_logger.warning(f"Failed to load local annotation mapping: {str(e)}. Fallback to identity mapping.")
            
    return mapping

def map_gene_identifiers(gene_ids: List[str], mapping_dict: Dict[str, str], log_logger=None) -> Tuple[List[str], Dict[str, Any]]:
    """
    Standardizes a list of gene identifiers to standard HGNC Symbols.
    """
    mapped_symbols = []
    mapped_count = 0
    unmapped_count = 0
    
    for g in gene_ids:
        if not g or pd.isna(g):
            mapped_symbols.append("UNKNOWN")
            unmapped_count += 1
            continue
            
        g_str = str(g).strip().upper()
        # Clean dot versions of Ensembl
        g_clean = g_str.split(".")[0]
        
        if g_str in mapping_dict:
            mapped_symbols.append(mapping_dict[g_str])
            mapped_count += 1
        elif g_clean in mapping_dict:
            mapped_symbols.append(mapping_dict[g_clean])
            mapped_count += 1
        else:
            # Fallback to the original symbol
            mapped_symbols.append(str(g).strip())
            unmapped_count += 1

    total = len(gene_ids)
    success_rate = (mapped_count / total * 100.0) if total > 0 else 0.0
    
    report = {
        "total_genes": total,
        "mapped_genes": mapped_count,
        "unmapped_genes": unmapped_count,
        "mapping_success_rate_percent": success_rate
    }
    
    if log_logger:
        log_logger.info(f"Gene identifier mapping: {mapped_count}/{total} mapped ({success_rate:.2f}%)")
        
    return mapped_symbols, report

# =============================================================================
# OFFLINE OVER-REPRESENTATION ANALYSIS (ORA) FALLBACK
# =============================================================================

# Simplified biological pathway definition for offline enrichment validation
OFFLINE_PATHWAYS = {
    "KEGG": {
        "hsa04110: Cell cycle": ["TP53", "BRCA1", "CDK1", "CCND1", "MDM2", "CCNB1", "CDC25C", "E2F1", "RB1", "CDKN1A"],
        "hsa03030: DNA replication": ["PCNA", "MCM2", "MCM3", "MCM4", "MCM5", "MCM6", "MCM7", "RFC1", "FEN1", "LIG1"],
        "hsa04115: p53 signaling pathway": ["TP53", "MDM2", "CDKN1A", "BAX", "GADD45A", "CASP3", "FAS", "CDK2", "CCND1", "CCNE1"],
        "hsa04210: Apoptosis": ["BAX", "BCL2", "CASP3", "CASP8", "CASP9", "FAS", "CYCS", "BID", "AKT1", "TP53"],
        "hsa04620: Toll-like receptor signaling pathway": ["TLR4", "MYD88", "IRF7", "IRF3", "TRAF6", "NFKB1", "TNF", "IL6", "IL1B", "IFNA1"],
        "hsa05164: Influenza A": ["STAT1", "STAT2", "IRF7", "IRF9", "MX1", "ISG15", "IFNAR1", "IFNAR2", "OAS1", "EIF2AK2"]
    },
    "GO_Biological_Process": {
        "GO:0007049 ~ cell cycle": ["TP53", "BRCA1", "CDK1", "CCND1", "MDM2", "CCNB1", "CDC25C", "E2F1", "RB1", "CDKN1A"],
        "GO:0006260 ~ DNA replication": ["PCNA", "MCM2", "MCM3", "MCM4", "MCM5", "MCM6", "MCM7", "RFC1", "FEN1", "LIG1"],
        "GO:0006915 ~ apoptotic process": ["BAX", "BCL2", "CASP3", "CASP8", "CASP9", "FAS", "CYCS", "BID", "AKT1", "TP53"],
        "GO:0051607 ~ defense response to virus": ["STAT1", "STAT2", "IRF7", "IRF9", "MX1", "ISG15", "IFNAR1", "IFNAR2", "OAS1", "EIF2AK2", "IFNB1"],
        "GO:0006351 ~ transcription, DNA-templated": ["TP53", "E2F1", "STAT1", "STAT2", "IRF7", "IRF3", "NFKB1", "MYC", "JUN", "FOS"]
    },
    "GO_Molecular_Function": {
        "GO:0003677 ~ DNA binding": ["TP53", "E2F1", "STAT1", "STAT2", "IRF7", "IRF3", "NFKB1", "MYC", "JUN", "FOS", "BRCA1"],
        "GO:0004672 ~ protein kinase activity": ["CDK1", "CDK2", "AKT1", "ATM", "ATR", "CHEK1", "CHEK2", "MAPK1", "MAPK3", "EGFR"],
        "GO:0005515 ~ protein binding": ["TP53", "BRCA1", "CDK1", "CCND1", "MDM2", "CCNB1", "CDC25C", "E2F1", "RB1", "CDKN1A", "BAX", "BCL2", "CASP3", "PCNA", "MCM2"]
    },
    "GO_Cellular_Component": {
        "GO:0005634 ~ nucleus": ["TP53", "BRCA1", "CDK1", "CCND1", "MDM2", "CCNB1", "CDC25C", "E2F1", "RB1", "CDKN1A", "PCNA", "MCM2", "MCM3", "MCM4", "MCM5"],
        "GO:0005737 ~ cytoplasm": ["BCL2", "CASP3", "CASP8", "CASP9", "CYCS", "BID", "AKT1", "MYD88", "TRAF6", "MX1", "ISG15"],
        "GO:0005886 ~ plasma membrane": ["FAS", "TLR4", "IFNAR1", "IFNAR2", "EGFR"]
    }
}

def run_local_ora(significant_genes: List[str], db_type: str = "KEGG", background_size: int = 20000, log_logger=None) -> pd.DataFrame:
    """
    Performs local over-representation analysis using a one-sided Fisher's Exact Test.
    """
    if log_logger:
        log_logger.info(f"Running local ORA fallback for database: {db_type} with {len(significant_genes)} input genes.")
        
    sig_genes_set = set(str(g).strip().upper() for g in significant_genes if g and not pd.isna(g))
    n_sig = len(sig_genes_set)
    
    pathway_db = OFFLINE_PATHWAYS.get(db_type, OFFLINE_PATHWAYS["KEGG"])
    
    results = []
    
    for path_name, path_genes in pathway_db.items():
        path_genes_set = set(g.upper() for g in path_genes)
        n_path = len(path_genes_set)
        
        overlap_genes = sig_genes_set.intersection(path_genes_set)
        n_overlap = len(overlap_genes)
        
        # Fisher's 2x2 contingency table:
        #                 In Gene List    Not In Gene List
        # In Pathway       n_overlap       n_path - n_overlap
        # Not In Pathway   n_sig - n_overlap  background - n_sig - n_path + n_overlap
        
        a = n_overlap
        b = n_path - n_overlap
        c = n_sig - n_overlap
        d = background_size - n_sig - n_path + n_overlap
        
        # Handle boundary checks
        if a < 0 or b < 0 or c < 0 or d < 0:
            pval = 1.0
        else:
            _, pval = fisher_exact([[a, b], [c, d]], alternative="greater")
            
        results.append({
            "Term": path_name,
            "P-value": float(pval),
            "Overlap": f"{n_overlap}/{n_path}",
            "Genes": ";".join(list(overlap_genes)) if overlap_genes else ""
        })
        
    df = pd.DataFrame(results)
    
    # Calculate FDR
    df["Adjusted P-value"] = apply_bh_fdr(df["P-value"].tolist(), log_logger)
    df = df.sort_values("P-value").reset_index(drop=True)
    
    return df
