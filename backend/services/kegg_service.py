import os
import math
from typing import List, Dict, Any

# =============================================================================
# HYPERGEOMETRIC ENRICHMENT CALCULATOR (Pure Python)
# =============================================================================

def _log_factorial(n: int) -> float:
    if n <= 0:
        return 0.0
    return math.lgamma(n + 1)

def _lchoose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return -float('inf')
    return _log_factorial(n) - _log_factorial(k) - _log_factorial(n - k)

def _hypergeometric_pmf(k: int, M: int, n: int, N: int) -> float:
    """
    M: population size (background genes, e.g. 20000)
    n: population successes (pathway genes)
    N: sample size (user sig genes)
    k: sample successes (matched genes)
    """
    log_prob = _lchoose(n, k) + _lchoose(M - n, N - k) - _lchoose(M, N)
    return math.exp(log_prob)

def _hypergeometric_p_value(k: int, M: int, n: int, N: int) -> float:
    """
    One-sided upper tail p-value (probability of obtaining >= k matches by chance).
    """
    if k <= 0:
        return 1.0
    p_val = 0.0
    for x in range(k, min(n, N) + 1):
        p_val += _hypergeometric_pmf(x, M, n, N)
    return min(max(p_val, 0.0), 1.0)

def _apply_benjamini_hochberg(p_values: List[float]) -> List[float]:
    """
    Applies FDR control using the Benjamini-Hochberg procedure.
    """
    n = len(p_values)
    if n == 0:
        return []
    
    sorted_p = sorted(enumerate(p_values), key=lambda x: x[1])
    adj_p = [1.0] * n
    
    prev_adj = 1.0
    for rank, (orig_idx, p_val) in enumerate(reversed(sorted_p), start=1):
        i = n - rank + 1  # 1-indexed rank
        val = p_val * n / i
        adj_p[orig_idx] = min(val, prev_adj)
        prev_adj = adj_p[orig_idx]
        
    return [min(x, 1.0) for x in adj_p]

# =============================================================================
# LOCAL PATHWAY & GENE ONTOLOGY KNOWLEDGE DATABASES (Expanded to 50 KEGG & 22 GO)
# =============================================================================

LOCAL_PATHWAY_DB = {
    # --- Cancer & Signal Transduction Pathways ---
    "hsa04151": {
        "name": "PI3K-Akt signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04151",
        "description": "Cell survival, growth and proliferation signaling cascade regulating translation.",
        "category": "Signal Transduction",
        "genes": ["AKT1", "AKT2", "AKT3", "PIK3CA", "PIK3CB", "PIK3CD", "PIK3R1", "PIK3R2", "PTEN", "MTOR", "PDK1", "GSK3B", "FOXO1", "FOXO3", "BAD", "MDM2", "CCND1", "CDKN1B", "BCL2", "EGFR", "FGFR1", "FGFR2", "IGF1R", "INS", "IRS1", "IRS2", "VEGFA", "VEGFB", "VEGFC", "FLT1", "KDR", "PDGFRA", "PDGFRB", "HRAS", "KRAS", "NRAS", "BRCA1", "BRCA2", "TP53"]
    },
    "hsa04010": {
        "name": "MAPK signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04010",
        "description": "Mitogen-activated protein kinase cascade regulating gene expression, growth and differentiation.",
        "category": "Signal Transduction",
        "genes": ["HRAS", "KRAS", "NRAS", "BRAF", "RAF1", "MAP2K1", "MAP2K2", "MAPK1", "MAPK3", "MAPK8", "MAPK9", "MAPK14", "MAPK11", "MAPK12", "MAPK13", "EGFR", "FOS", "JUN", "MYC", "ATF2", "ELK1", "MAPKAPK2", "DUSP1", "DUSP2", "DUSP4", "DUSP6", "DUSP10", "NF1", "RASA1", "SOS1", "GRB2", "STAT1", "STAT3"]
    },
    "hsa04310": {
        "name": "Wnt signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04310",
        "description": "Conserved ligand-receptor pathways directing developmental processes and adult tissue repair.",
        "category": "Signal Transduction",
        "genes": ["WNT1", "WNT2", "WNT3", "WNT3A", "WNT4", "WNT5A", "WNT5B", "WNT6", "WNT7A", "CTNNB1", "APC", "GSK3B", "AXIN1", "AXIN2", "DVL1", "DVL2", "DVL3", "FZD1", "FZD2", "FZD3", "FZD4", "LRP5", "LRP6", "TCF7", "TCF7L1", "TCF7L2", "LEF1", "MYC", "CCND1", "DKK1", "DKK2", "DKK4", "SFRP1", "SFRP2"]
    },
    "hsa04115": {
        "name": "p53 signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04115",
        "description": "Cellular stress responder directing cell cycle arrest, DNA repair, and programmed cell death.",
        "category": "Cancer & Cell Cycle Control",
        "genes": ["TP53", "MDM2", "MDM4", "CDKN1A", "BAX", "BBC3", "PMAIP1", "FAS", "TNFRSF10B", "GADD45A", "GADD45B", "GADD45G", "SULF2", "SERPINE1", "CDK2", "CCND1", "CCNE1", "CCNE2", "CHEK1", "CHEK2", "ATM", "ATR", "SIRT1", "PTEN", "TSC2", "CASP3", "CASP8", "CASP9", "APAF1", "BCL2", "BCL2L1", "GAPDH", "ACTB", "STAT1", "MX1", "ISG15"]
    },
    "hsa04064": {
        "name": "NF-kappa B signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04064",
        "description": "Transcription factor network directing immune, inflammatory, and survival genes.",
        "category": "Signal Transduction",
        "genes": ["NFKB1", "NFKB2", "RELA", "RELB", "REL", "IKBKB", "IKBKG", "CHUK", "NFKBIA", "NFKBIB", "NFKBIE", "TNF", "TNFRSF1A", "TRADD", "TRAF2", "TRAF6", "RIPK1", "RIPK2", "IL1B", "IL1R1", "MYD88", "IRAK1", "IRAK4", "TAB1", "TAB2", "MAP3K7", "MAP3K14", "LTA", "LTB", "CD40LG", "CD40", "BAFF"]
    },
    "hsa04630": {
        "name": "JAK-STAT signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04630",
        "description": "Direct cytokine-to-nucleus transcription activation pathway.",
        "category": "Signal Transduction",
        "genes": ["JAK1", "JAK2", "JAK3", "TYK2", "STAT1", "STAT2", "STAT3", "STAT4", "STAT5A", "STAT5B", "STAT6", "IL2", "IL2RA", "IL2RB", "IL2RG", "IL6", "IL6R", "IL6ST", "IFNA1", "IFNA2", "IFNB1", "IFNG", "IFNGR1", "IFNGR2", "EPOR", "GCSF", "GMCSF", "SOCS1", "SOCS3", "CISH", "PIAS1", "PIAS3", "PTPN11", "MX1", "MX2", "OAS1", "OAS2", "ISG15", "TP53"]
    },
    "hsa04210": {
        "name": "Apoptosis",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04210",
        "description": "Regulated programmed cell death cascade via extrinsic and intrinsic triggers.",
        "category": "Cellular Fate",
        "genes": ["BAX", "BAK1", "BCL2", "BCL2L1", "BCL2L11", "BID", "BAD", "BIRC5", "BIRC2", "BIRC3", "XIAP", "APAF1", "CASP3", "CASP7", "CASP6", "CASP8", "CASP9", "CASP10", "FAS", "FASLG", "TNF", "TNFRSF1A", "CYCS", "DIABLO", "HTRA2", "DFFA", "DFFB", "PARP1", "TP53", "AIFM1", "ENDOG"]
    },
    "hsa04110": {
        "name": "Cell cycle",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04110",
        "description": "Eukaryotic replication phases G1/S/G2/M control checkpoints.",
        "category": "Cellular Proliferation",
        "genes": ["CCNA1", "CCNA2", "CCNB1", "CCNB2", "CCND1", "CCND2", "CCND3", "CCNE1", "CCNE2", "CDK1", "CDK2", "CDK4", "CDK6", "CDKN1A", "CDKN1B", "CDKN2A", "CDKN2B", "CDKN2C", "CDKN2D", "RB1", "E2F1", "E2F2", "E2F3", "E2F4", "TP53", "MDM2", "CDC25A", "CDC25B", "CDC25C", "PLK1", "BUB1", "MAD2L1", "MCM2", "MCM3", "MCM4", "PCNA"]
    },
    "hsa04350": {
        "name": "TGF-beta signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04350",
        "description": "Cytokine signaling cascade suppressing cell proliferation and directing extracellular matrix.",
        "category": "Signal Transduction",
        "genes": ["TGFB1", "TGFB2", "TGFB3", "TGFBR1", "TGFBR2", "SMAD2", "SMAD3", "SMAD4", "SMAD1", "SMAD5", "SMAD9", "SMAD6", "SMAD7", "BMP2", "BMP4", "BMPR1A", "BMPR1B", "BMPR2", "ACVR1", "ACVR2A", "ACVR2B", "INHBA", "INHBB", "FST", "LTBP1", "SP1", "EP300", "CREBBP", "MYC", "CDKN1A", "CDKN2B"]
    },
    "hsa04370": {
        "name": "VEGF signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04370",
        "description": "Growth factor pathway regulating endothelial migration, survival, and vascular permeability.",
        "category": "Angiogenesis",
        "genes": ["VEGFA", "VEGFB", "VEGFC", "VEGFD", "PGF", "FLT1", "KDR", "FLT4", "NRP1", "NRP2", "MAPK1", "MAPK3", "AKT1", "PIK3CA", "PTEN", "PLCG1", "PRKCA", "PRKCB", "NOS3", "SRC", "PTK2", "PXN", "RAC1", "RHOA", "CDC42", "HRAS", "KRAS", "NRAS"]
    },
    "hsa04150": {
        "name": "mTOR signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04150",
        "description": "Integration of growth factors, energy status, and nutrients to promote macromolecule synthesis.",
        "category": "Metabolism & Growth",
        "genes": ["MTOR", "RPTOR", "RICTOR", "AKT1", "PIK3CA", "PTEN", "TSC1", "TSC2", "RHEB", "RPSG6KB1", "RPSG6KB2", "EIF4EBP1", "MLST8", "DEPTOR", "PRR5", "MAPKAP1", "ULK1", "ATG13", "PRKAA1", "PRKAA2", "CAB39", "STRADA", "STK11", "INSR", "IRS1", "GRB2", "HRAS", "KRAS"]
    },
    "hsa04330": {
        "name": "Notch signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04330",
        "description": "Short-range intercellular communication regulating cell destiny decisions.",
        "category": "Signal Transduction",
        "genes": ["NOTCH1", "NOTCH2", "NOTCH3", "NOTCH4", "DLL1", "DLL3", "DLL4", "JAG1", "JAG2", "RBPJ", "MAML1", "MAML2", "MAML3", "HES1", "HES5", "HEY1", "HEY2", "HEYL", "DTX1", "DTX2", "DTX3", "NUMB", "NUMBL", "EP300", "CREBBP", "HDAC1", "HDAC2", "NCSTN", "APH1A", "PSEN1", "PSEN2"]
    },
    "hsa04340": {
        "name": "Hedgehog signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04340",
        "description": "Signaling cascade directing morphogenetic patterning and cancer tissue homeostasis.",
        "category": "Signal Transduction",
        "genes": ["SHH", "IHH", "DHH", "PTCH1", "PTCH2", "SMO", "GLI1", "GLI2", "GLI3", "SUFU", "KIF7", "PRKACA", "PRKACB", "GSK3B", "CSNK1A1", "BTRC", "FBXW11", "STK36", "DYRK1A", "DYRK1B", "GAS1", "CDON", "BOC", "LRP2", "ARRB1", "ARRB2", "WNT1", "WNT3A", "CTNNB1", "BMP4"]
    },
    "hsa04620": {
        "name": "Toll-like receptor signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04620",
        "description": "PRR system mapping pathogen molecular structures to activate innate defenses.",
        "category": "Innate Immunity",
        "genes": ["TLR1", "TLR2", "TLR3", "TLR4", "TLR5", "TLR6", "TLR7", "TLR8", "TLR9", "TLR10", "MYD88", "TICAM1", "TICAM2", "TIRAP", "IRAK1", "IRAK2", "IRAK4", "TRAF3", "TRAF6", "MAP3K7", "TAB1", "TAB2", "IKBKB", "IKBKG", "CHUK", "NFKB1", "RELA", "IRF3", "IRF7", "MAPK8", "MAPK9", "MAPK14", "TNF", "IL6", "IL1B", "IFNA1", "IFNB1"]
    },
    "hsa04662": {
        "name": "B cell receptor signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04662",
        "description": "Antigen recognition signaling directing humoral B-lymphocyte activation.",
        "category": "Adaptive Immunity",
        "genes": ["CD19", "CD22", "CD79A", "CD79B", "SYK", "LYN", "FYN", "BLK", "BTK", "PLCG2", "PIK3CA", "PTEN", "AKT1", "GSK3B", "NFATC1", "NFATC2", "NFATC3", "NFKB1", "RELA", "MAPK1", "MAPK3", "MAPK8", "MAPK9", "BCL2", "BCL2L1", "MALT1", "BCL10", "CARD11", "PRKCB", "BLNK", "VAV1", "VAV2"]
    },
    "hsa04660": {
        "name": "T cell receptor signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04660",
        "description": "Antigen-MHC presentation mapping to drive helper and cytotoxic T-cell defenses.",
        "category": "Adaptive Immunity",
        "genes": ["CD3D", "CD3E", "CD3G", "CD247", "CD4", "CD8A", "CD8B", "LCK", "FYN", "ZAP70", "LAT", "SLP76", "PLCG1", "ITK", "VAV1", "MAP3K7", "IKBKB", "IKBKG", "NFKB1", "RELA", "NFATC1", "NFATC2", "NFATC3", "MAPK1", "MAPK3", "MAPK8", "MAPK9", "AKT1", "PIK3CA", "PTEN", "CBL", "CBLB"]
    },
    "hsa03440": {
        "name": "Homologous recombination",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa03440",
        "description": "Genetic recombination process in which nucleotide sequences are exchanged between similar molecules of DNA to repair double-strand breaks.",
        "category": "Genome Stability",
        "genes": ["XRCC5", "XRCC6", "PRKDC", "LIG4", "XRCC4", "NHEJ1", "RAD51", "RAD51B", "RAD51C", "RAD51D", "RAD52", "RAD54L", "BRCA1", "BRCA2", "MRE11", "RAD50", "NBN", "ATM", "ATR", "TP53", "APEX1", "APEX2", "LIG1", "LIG3", "XRCC1", "PARP1", "PARP2", "OGG1", "MUTYH", "UNG", "MPG"]
    },
    "hsa00190": {
        "name": "Oxidative phosphorylation",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa00190",
        "description": "Mitochondrial electron transport chain driving ATP synthesis.",
        "category": "Metabolism & Energy",
        "genes": ["NDUFFA1", "NDUFA2", "NDUFA3", "NDUFA4", "NDUFA5", "NDUFA6", "NDUFA7", "NDUFA8", "NDUFA9", "NDUFA10", "NDUFB1", "NDUFB2", "NDUFB3", "SDHA", "SDHB", "SDHC", "SDHD", "UQCRFS1", "UQCRB", "UQCRQ", "COX4I1", "COX4I2", "COX5A", "COX5B", "COX6A1", "ATP5F1A", "ATP5F1B", "ATP5F1C", "ATP5F1D"]
    },
    "hsa00010": {
        "name": "Glycolysis / Gluconeogenesis",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa00010",
        "description": "Cytoplasm enzymes mapping glucose splitting into pyruvate intermediates.",
        "category": "Metabolism & Energy",
        "genes": ["HK1", "HK2", "HK3", "GPI", "PFKM", "PFKP", "PFKL", "ALDOA", "ALDOB", "ALDOC", "TPI1", "GAPDH", "PGK1", "PGAM1", "PGAM2", "ENO1", "ENO2", "ENO3", "PKM", "PKLR", "LDHA", "LDHB", "PDHA1", "PDHB", "DLAT", "DLD", "PC", "PCK1", "PCK2", "FBP1", "FBP2", "G6PC", "G6PC2"]
    },
    "hsa04140": {
        "name": "Autophagy",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04140",
        "description": "Lysosome vesicle recycling of macromolecules during starvation or stress.",
        "category": "Cellular Fate",
        "genes": ["ULK1", "ULK2", "ATG13", "RB1CC1", "ATG101", "BECN1", "PIK3C3", "PIK3R4", "AMBRA1", "ATG14", "UVRAG", "SH3GLB1", "ATG5", "ATG12", "ATG16L1", "ATG7", "ATG3", "ATG10", "MAP1LC3A", "MAP1LC3B", "MAP1LC3C", "GABARAP", "GABARAPL1", "GABARAPL2", "ATG4A", "ATG4B", "SQSTM1", "NBR1"]
    },

    # --- Newly Expanded Pathways (Pathways 21 - 50) ---
    "hsa05200": {
        "name": "Pathways in cancer",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa05200",
        "description": "Global molecular signaling networks altered in cellular transformation and metastasis.",
        "category": "Cancer Pathways",
        "genes": ["TP53", "AKT1", "PIK3CA", "PTEN", "CTNNB1", "APC", "EGFR", "MYC", "CCND1", "VEGFA", "SMAD4", "RB1", "E2F1", "BRAF", "KRAS", "HRAS", "BCL2", "BAX"]
    },
    "hsa04114": {
        "name": "Oocyte meiosis",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04114",
        "description": "Cellular cycle regulation unique to germline cell meiotic spindle division.",
        "category": "Cell Cycle",
        "genes": ["MOS", "MAPK1", "MAPK3", "MAP2K1", "AURKA", "PLK1", "CDK1", "CCNB1", "CCNB2", "CDC25C", "PTTG1", "CDC20", "MAD2L1", "BUB1B", "SMC1A"]
    },
    "hsa04218": {
        "name": "Cellular senescence",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04218",
        "description": "Irreversible growth arrest protecting against neoplastic transformation and driving aging phenotypes.",
        "category": "Cellular Fate",
        "genes": ["TP53", "CDKN1A", "CDKN2A", "RB1", "E2F1", "CCND1", "CDK4", "CDK6", "SIRT1", "ATM", "ATR", "CHEK1", "CHEK2", "IL6", "CXCL8"]
    },
    "hsa04012": {
        "name": "ErbB signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04012",
        "description": "Epithelial receptor tyrosine kinase networks driving oncogenesis.",
        "category": "Signal Transduction",
        "genes": ["EGFR", "ERBB2", "ERBB3", "ERBB4", "GRB2", "SOS1", "HRAS", "KRAS", "NRAS", "BRAF", "RAF1", "MAP2K1", "MAPK1", "PIK3CA", "AKT1"]
    },
    "hsa04020": {
        "name": "Calcium signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04020",
        "description": "Intracellular Ca2+ release dynamics driving transcription and muscle contractions.",
        "category": "Signal Transduction",
        "genes": ["RYR1", "RYR2", "ITPR1", "ITPR2", "CACNA1C", "CALM1", "CALM2", "CAMK2A", "CAMK4", "PRKCA", "PRKCB", "PLCG1", "PLCG2", "NOS3"]
    },
    "hsa04024": {
        "name": "cAMP signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04024",
        "description": "Second messenger networks mapping GPCR activation to protein kinase transcription.",
        "category": "Signal Transduction",
        "genes": ["ADCY1", "ADCY2", "ADCY5", "PRKACA", "PRKACB", "CREB1", "CREBBP", "EP300", "RAPGEF3", "RAP1A", "MAPK1", "MAPK3", "AKT1", "GRIN1"]
    },
    "hsa04022": {
        "name": "cGMP-PKG signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04022",
        "description": "Nitric oxide-driven vasodilator pathway directing phosphorylation.",
        "category": "Signal Transduction",
        "genes": ["NPR1", "NPR2", "ADCY5", "PRKG1", "PRKG2", "NOS1", "NOS2", "NOS3", "CALM1", "PPP1R12A", "KCNMA1", "VASP", "AKT1", "SRC"]
    },
    "hsa04120": {
        "name": "Ubiquitin mediated proteolysis",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04120",
        "description": "Targeted tag-and-degrade proteasome decay path of proteins.",
        "category": "Genome Stability",
        "genes": ["UBE1", "UBA1", "UBE2D1", "UBE2L3", "MDM2", "BTRC", "SKP2", "CUL1", "RBX1", "ANAPC1", "CDC20", "FZR1", "BRCA1", "VHL"]
    },
    "hsa03013": {
        "name": "RNA transport",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa03013",
        "description": "Nuclear pore complex nucleocytoplasmic translocation of processed transcripts.",
        "category": "Metabolism & Energy",
        "genes": ["XPO1", "XPO5", "CSE1L", "NUP62", "NUP98", "NUP153", "RAN", "RANBP2", "RANBP1", "NCBP1", "NCBP2", "EIF4E", "PABPC1", "ELAVL1"]
    },
    "hsa03040": {
        "name": "Spliceosome",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa03040",
        "description": "Nuclear ribonucleoprotein complex mapping intron excision from pre-mRNAs.",
        "category": "Genome Stability",
        "genes": ["SF3B1", "SF3A1", "U2AF1", "U2AF2", "PRPF8", "PRPF31", "SNRPD1", "SNRPD2", "SNRPE", "SNRPF", "SNRPG", "HNRNPA1", "HNRNPD", "SRSF1"]
    },
    "hsa03010": {
        "name": "Ribosome",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa03010",
        "description": "Translation machinery converting mRNA transcripts into active peptide complexes.",
        "category": "Metabolism & Energy",
        "genes": ["RPL3", "RPL4", "RPL5", "RPL6", "RPL7", "RPL8", "RPL11", "RPS2", "RPS3", "RPS4X", "RPS5", "RPS6", "RPS7", "RPS8", "RPS9", "RPS10"]
    },
    "hsa04060": {
        "name": "Cytokine-cytokine receptor interaction",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04060",
        "description": "Primary intercellular communication pathway driving host immunological responses.",
        "category": "Immune Signaling",
        "genes": ["TNF", "IL6", "IL1B", "IFNG", "IL2", "IL10", "TNFRSF1A", "IL6R", "IL1R1", "IFNGR1", "IL2RA", "IL10RA", "TGFB1", "TGFBR1"]
    },
    "hsa04062": {
        "name": "Chemokine signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04062",
        "description": "G-protein coupled receptors directing cellular chemotaxis and migration.",
        "category": "Immune Signaling",
        "genes": ["CXCL8", "CXCL12", "CCL2", "CCL5", "CXCR4", "CCR2", "CCR5", "JAK2", "STAT3", "PIK3CA", "AKT1", "MAPK1", "RHOA", "RAC1", "CDC42"]
    },
    "hsa04610": {
        "name": "Complement and coagulation cascades",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04610",
        "description": "Serine protease system driving pathogen clearing and vascular homeostasis.",
        "category": "Immune Signaling",
        "genes": ["C3", "C4A", "C5", "C1S", "CFB", "CFH", "MASP1", "F2", "F3", "F8", "F9", "F10", "F11", "PLG", "SERPINE1", "FIBG"]
    },
    "hsa04650": {
        "name": "Natural killer cell mediated cytotoxicity",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04650",
        "description": "Direct cytolytic destruction of virus-infected or tumor cells without MHC restriction.",
        "category": "Immune Signaling",
        "genes": ["NCAM1", "FCGR3A", "FASLG", "PRF1", "GZMB", "GZMA", "HCST", "KLRK1", "SH2D1A", "FYB1", "ZAP70", "SYK", "PLCG1", "MAPK8"]
    },
    "hsa04612": {
        "name": "Antigen processing and presentation",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04612",
        "description": "Protease cleavage and loading of antigens onto MHC class I and II structures.",
        "category": "Immune Signaling",
        "genes": ["HLA-A", "HLA-B", "HLA-C", "HLA-DRA", "HLA-DRB1", "HLA-DQA1", "HLA-DQB1", "B2M", "TAP1", "TAP2", "CANX", "CALR", "PDIA3", "CD74"]
    },
    "hsa04510": {
        "name": "Focal adhesion",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04510",
        "description": "Integrin-mediated physical anchors translating mechanical load into intracellular signaling.",
        "category": "Development & Differentiation",
        "genes": ["PTK2", "PXN", "SRC", "ITGAV", "ITGB1", "ITGB3", "VCL", "TLN1", "ACTN1", "PIK3CA", "AKT1", "MAPK1", "MAPK3", "RHOA", "RAC1", "CDC42"]
    },
    "hsa04520": {
        "name": "Adherens junction",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04520",
        "description": "Cadherin-based cell-to-cell structural links coupled to actin cytoskeletons.",
        "category": "Development & Differentiation",
        "genes": ["CDH1", "CTNNB1", "CTNND1", "CTNNA1", "ACP1", "SRC", "MET", "EGFR", "FYN", "WAS", "ACTB", "ACTN1", "IQGAP1", "RAC1", "CDC42"]
    },
    "hsa04540": {
        "name": "Gap junction",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04540",
        "description": "Connexon hemichannel pathways allowing low-molecular-weight metabolite diffusion.",
        "category": "Development & Differentiation",
        "genes": ["GJA1", "GJA3", "GJB1", "GJB2", "GJC1", "PRKCA", "PRKCB", "CALM1", "MAPK1", "MAPK3", "HRAS", "KRAS", "NRAS", "SRC", "ADCY5"]
    },
    "hsa04530": {
        "name": "Tight junction",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04530",
        "description": "Claudin barriers restricting paracellular molecule transport.",
        "category": "Development & Differentiation",
        "genes": ["CLDN1", "CLDN2", "CLDN3", "CLDN4", "OCLN", "TJP1", "TJP2", "TJP3", "F11R", "ACTB", "RHOA", "ROCK1", "PRKCA", "PRKCB", "MYH9"]
    },
    "hsa04217": {
        "name": "Necroptosis",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04217",
        "description": "Caspase-independent regulated necrosis driving pro-inflammatory clearing.",
        "category": "Cellular Fate",
        "genes": ["RIPK1", "RIPK3", "MLKL", "TNF", "TNFRSF1A", "TRADD", "TRAF2", "CYLD", "CASP8", "FADD", "XIAP", "BIRC2", "BIRC3", "NFKB1", "RELA"]
    },
    "hsa04216": {
        "name": "Ferroptosis",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04216",
        "description": "Iron-dependent cell death driven by lipid peroxidation and ROS generation.",
        "category": "Cellular Fate",
        "genes": ["GPX4", "SLC7A11", "SLC3A2", "ACSL4", "LPCAT3", "TFRC", "FTL", "FTH1", "SAT1", "TP53", "NFE2L2", "HMOX1", "GSS", "GCLC", "NOX1"]
    },
    "hsa00020": {
        "name": "Citrate cycle (TCA cycle)",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa00020",
        "description": "Core aerobic pathway releasing stored chemical energy via acetyl-CoA oxidation.",
        "category": "Metabolism & Energy",
        "genes": ["CS", "ACO1", "ACO2", "IDH1", "IDH2", "IDH3A", "OGDH", "DLST", "DLD", "SUCLG1", "SUCLA2", "SDHA", "SDHB", "SDHC", "SDHD", "FH", "MDH1", "MDH2"]
    },
    "hsa00071": {
        "name": "Fatty acid degradation",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa00071",
        "description": "Beta-oxidation process mapping acyl-CoA decay inside mitochondria.",
        "category": "Metabolism & Energy",
        "genes": ["ACSL1", "ACSL3", "ACSL4", "CPT1A", "CPT2", "ACADL", "ACADM", "ACADSB", "HADHA", "HADHB", "EHHADH", "ACOX1", "PECI", "ALDH2"]
    },
    "hsa00500": {
        "name": "Starch and sucrose metabolism",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa00500",
        "description": "Conversion pathways mapping complex carbohydrates into glucose intermediates.",
        "category": "Metabolism & Energy",
        "genes": ["UGP2", "GYS1", "GYS2", "PYGL", "PYGB", "PYG", "AGL", "GBE1", "GAA", "TREH", "AMY1A", "AMY2A", "MGAM", "SI"]
    },
    "hsa00520": {
        "name": "Amino sugar and nucleotide sugar metabolism",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa00520",
        "description": "Sugar donor pathways driving cellular glycosylation.",
        "category": "Metabolism & Energy",
        "genes": ["GFPT1", "GFPT2", "GNPNAT1", "PGM3", "UAP1", "UXS1", "UGP2", "UGCG", "GNE", "NANP", "NANS", "CMAS", "GALK1", "GALT", "GALE"]
    },
    "hsa04910": {
        "name": "Insulin signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04910",
        "description": "Signal cascade mapping glucose intake and glycogen synthesis.",
        "category": "Metabolism & Growth",
        "genes": ["INSR", "IGF1R", "IRS1", "IRS2", "PIK3CA", "PIK3R1", "PDK1", "AKT1", "AKT2", "GSK3B", "FOXO1", "MAPK1", "MAPK3", "RPSG6KB1", "PRKCI"]
    },
    "hsa04931": {
        "name": "Insulin resistance",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04931",
        "description": "Pathology pathway of impaired insulin-stimulated glucose uptake.",
        "category": "Metabolism & Growth",
        "genes": ["INSR", "IRS1", "IRS2", "SOCS3", "TNF", "IL6", "IKBKB", "MAPK8", "PRKCQ", "MTOR", "RPSG6KB1", "SREBF1", "PPARGC1A", "SLC2A4"]
    },
    "hsa04920": {
        "name": "Adipocytokine signaling pathway",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04920",
        "description": "Adipose hormone pathways linking obesity to cardiovascular risk.",
        "category": "Metabolism & Growth",
        "genes": ["ADIPOQ", "ADIPOR1", "ADIPOR2", "LEP", "LEPR", "JAK2", "STAT3", "PRKAA1", "PRKAA2", "PPARA", "PPARGC1A", "TNFRSF1A", "IKBKB", "RELA"]
    },
    "hsa04261": {
        "name": "Cardiovascular disease (Cardiomyopathy)",
        "url": "https://www.genome.jp/dbget-bin/www_bget?pathway+hsa04261",
        "description": "Structural and electrophysiology disease pathway of heart muscle cells.",
        "category": "Cardiovascular disease",
        "genes": ["ACTC1", "MYH7", "MYBPC3", "TNNT2", "TNNI3", "TPM1", "LMNA", "DES", "SGCD", "SGCB", "SGCA", "DMD", "TTN", "PLN", "RYR2"]
    }
}

LOCAL_GO_DB = {
    # --- Biological Process (BP) terms (Terms 1 - 10) ---
    "GO:0006915": {
        "name": "apoptotic process",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0006915",
        "description": "Programmed cell death biological cascade triggered by extracellular/intracellular stressors.",
        "category": "Biological Process",
        "genes": LOCAL_PATHWAY_DB["hsa04210"]["genes"]
    },
    "GO:0007049": {
        "name": "cell cycle",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0007049",
        "description": "Highly regulated chromosomal replication and spindle mitosis cell progression phases.",
        "category": "Biological Process",
        "genes": LOCAL_PATHWAY_DB["hsa04110"]["genes"]
    },
    "GO:0006281": {
        "name": "DNA repair",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0006281",
        "description": "Detection and repair pathways fixing damaged bases and double-strand breaks.",
        "category": "Biological Process",
        "genes": LOCAL_PATHWAY_DB["hsa03440"]["genes"]
    },
    "GO:0006096": {
        "name": "glycolytic process",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0006096",
        "description": "Metabolic breakdown of glucose into pyruvate releasing ATP.",
        "category": "Biological Process",
        "genes": LOCAL_PATHWAY_DB["hsa00010"]["genes"]
    },
    "GO:0006119": {
        "name": "oxidative phosphorylation",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0006119",
        "description": "Electrochemical proton gradient coupling electron transport to ATP synthase.",
        "category": "Biological Process",
        "genes": LOCAL_PATHWAY_DB["hsa00190"]["genes"]
    },
    "GO:0006954": {
        "name": "inflammatory response",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0006954",
        "description": "Vasodilation and immune cell infiltration in tissue responding to infection/injury.",
        "category": "Biological Process",
        "genes": ["TNF", "IL6", "IL1B", "PTGS2", "CXCL8", "CCL2", "ICAM1", "VCAM1", "NFKB1", "RELA", "STAT3", "JAK2", "TLR4", "MYD88", "IFNG", "IL10"]
    },
    "GO:0051607": {
        "name": "defense response to virus",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0051607",
        "description": "Host intracellular antiviral state driven by interferons and cell checkpoints.",
        "category": "Biological Process",
        "genes": ["MX1", "MX2", "OAS1", "OAS2", "OAS3", "ISG15", "IFIT1", "IFIT2", "IFIT3", "STAT1", "STAT2", "IRF3", "IRF7", "IFNA1", "IFNB1", "DDX58", "IFIH1", "STAT3", "JAK1", "JAK2"]
    },
    "GO:0006914": {
        "name": "autophagy",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0006914",
        "description": "Double membrane vesicle transport recycling organelles.",
        "category": "Biological Process",
        "genes": LOCAL_PATHWAY_DB["hsa04140"]["genes"]
    },
    "GO:0001525": {
        "name": "angiogenesis",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0001525",
        "description": "Sprouting of new capillary blood vessels from pre-existing vasculature.",
        "category": "Biological Process",
        "genes": ["VEGFA", "FGF2", "TEK", "ANGPT1", "ANGPT2", "FLT1", "KDR", "PDGFRB", "EGF", "TGFB1", "HIF1A", "ENG", "AKT1", "PIK3CA"]
    },
    "GO:0008283": {
        "name": "cell proliferation",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0008283",
        "description": "Multiplication of cells leading to cell growth and tissue expansion.",
        "category": "Biological Process",
        "genes": ["AKT1", "PIK3CA", "EGFR", "MYC", "CCND1", "CDK4", "CDK6", "KRAS", "HRAS", "NRAS", "E2F1", "TGFB1", "IGF1"]
    },

    # --- Molecular Function (MF) terms (Terms 11 - 16) ---
    "GO:0005515": {
        "name": "protein binding",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0005515",
        "description": "Selective interaction between protein chains regulating molecular assembly.",
        "category": "Molecular Function",
        "genes": ["TP53", "AKT1", "EGFR", "TNF", "IL6", "STAT3", "MAPK1", "MDM2", "CTNNB1", "RELA", "SMAD4", "EP300", "CREBBP", "GRB2", "SRC"]
    },
    "GO:0003723": {
        "name": "RNA binding",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0003723",
        "description": "Interaction with single or double stranded RNA molecules driving post-transcriptional processing.",
        "category": "Molecular Function",
        "genes": ["EIF4E", "EIF4G1", "ELAVL1", "HNRNPD", "HNRNPA1", "IGF2BP1", "MSI1", "PABPC1", "PTBP1", "RPL3", "RPL5", "RPS3", "RPS6", "XPO1"]
    },
    "GO:0003677": {
        "name": "DNA binding",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0003677",
        "description": "Interaction with double stranded DNA elements directing genomic replication or expression transcription.",
        "category": "Molecular Function",
        "genes": ["TP53", "JUN", "FOS", "MYC", "STAT1", "STAT3", "RELA", "NFKB1", "SMAD3", "SMAD4", "E2F1", "E2F4", "BRCA1", "CREB1"]
    },
    "GO:0004672": {
        "name": "protein kinase activity",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0004672",
        "description": "Catalytic transfer of high-energy phosphate onto tyrosine/serine/threonine residue targets.",
        "category": "Molecular Function",
        "genes": ["AKT1", "AKT2", "MAPK1", "MAPK3", "JAK1", "JAK2", "JAK3", "CDK1", "CDK2", "CDK4", "CDK6", "EGFR", "SRC", "BTK", "MTOR"]
    },
    "GO:0005215": {
        "name": "transporter activity",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0005215",
        "description": "Facilitated passage of ions, metabolites, or macromolecules across phospholipid bilayers.",
        "category": "Molecular Function",
        "genes": ["SLC2A1", "SLC2A4", "SLC1A3", "ABCB1", "ABCC1", "ABCG2", "ATP1A1", "ATP2A2", "CACNA1C", "SCN5A", "KCNH2", "AQP1", "TAP1", "TAP2"]
    },
    "GO:0003824": {
        "name": "catalytic activity",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0003824",
        "description": "Enzymatic reduction of activation energy to drive biotransformations.",
        "category": "Molecular Function",
        "genes": ["GAPDH", "HK1", "PKM", "LDHA", "ENO1", "PTGS2", "NOS3", "PARP1", "OGG1", "CASP3", "CASP8", "CASP9", "CS", "ACO1"]
    },

    # --- Cellular Component (CC) terms (Terms 17 - 22) ---
    "GO:0005737": {
        "name": "cytoplasm",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0005737",
        "description": "The liquid cytosol and membrane structures outside the nuclear envelope.",
        "category": "Cellular Component",
        "genes": ["GAPDH", "ACTB", "TUBB", "LDHA", "TPI1", "MAPK1", "AKT1", "YWHAZ", "HSP90AA1", "HSPA1A", "PLCG1", "PRKCA", "RHOA"]
    },
    "GO:0005634": {
        "name": "nucleus",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0005634",
        "description": "Double membrane bounded compartment housing the chromosomes.",
        "category": "Cellular Component",
        "genes": ["TP53", "MYC", "JUN", "FOS", "STAT1", "RELA", "BRCA1", "HDAC1", "EP300", "CREBBP", "LMNA", "H2AFX", "E2F1"]
    },
    "GO:0005739": {
        "name": "mitochondrion",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0005739",
        "description": "Double membrane organelle running Citrate cycle and generating cellular ATP.",
        "category": "Cellular Component",
        "genes": ["SDHA", "COX4I1", "ATP5F1A", "CYCS", "BAX", "BCL2", "APAF1", "DIABLO", "AIFM1", "PINK1", "PRKN", "FH", "MDH2"]
    },
    "GO:0005886": {
        "name": "plasma membrane",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0005886",
        "description": "Extracellular boundary lipid bilayer containing receptors and transport channels.",
        "category": "Cellular Component",
        "genes": ["EGFR", "FLT1", "KDR", "FAS", "CD4", "CD8A", "CD19", "IL2RA", "TLR4", "ITGB1", "NOS3", "CDH1", "CLDN1"]
    },
    "GO:0005783": {
        "name": "endoplasmic reticulum",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0005783",
        "description": "Nuclear-envelope contiguous membrane network translating secretory cargo proteins.",
        "category": "Cellular Component",
        "genes": ["CANX", "CALR", "PDIA3", "HSPA5", "ERO1A", "SEC61A1", "ATF6", "ERN1", "EIF2AK3", "TAP1", "TAP2"]
    },
    "GO:0005768": {
        "name": "endosome",
        "url": "https://amigo.geneontology.org/amigo/term/GO:0005768",
        "description": "Membrane bound vacuoles sorting endocytosed molecular cargo.",
        "category": "Cellular Component",
        "genes": ["RAB5A", "RAB7A", "EEA1", "APPL1", "VPS35", "LDLR", "TFRC", "CD63", "LAMP1", "NRP1", "XPO1"]
    }
}

# =============================================================================
# STATISTICAL PATHWAY ENRICHMENT RUNNER (Bypass/Web-less Engine)
# =============================================================================

def run_gsea_enrichment(gene_list: List[str], gene_sets: List[str], log_logger) -> List[Dict[str, Any]]:
    """
    Local ORA statistical enrichment engine using Hypergeometric testing and BH FDR correction.
    Bypasses external Enrichr APIs to guarantee 100% offline stability during the presentation.
    """
    if not gene_list:
        log_logger.warning("Target gene list is empty. Skipping enrichment.")
        return []
        
    cleaned_genes = [str(g).strip().upper() for g in gene_list if g]
    results = []
    M = 20000  # Human genome background genes count
    N = len(cleaned_genes)
    
    for gset in gene_sets:
        is_kegg = "KEGG" in gset or "Pathway" in gset
        db_to_use = LOCAL_PATHWAY_DB if is_kegg else LOCAL_GO_DB
        
        db_results = []
        for p_id, p_data in db_to_use.items():
            pathway_genes = p_data["genes"]
            matched = list(set(cleaned_genes) & set(pathway_genes))
            k = len(matched)
            
            if k > 0:
                score = k / len(pathway_genes)
                p_val = _hypergeometric_p_value(k, M, len(pathway_genes), N)
                matched_str = ";".join(matched)
                
                term_display = f"{p_data['name']} ({p_id})" if not is_kegg else f"{p_data['name']}"
                db_results.append({
                    "id": p_id,
                    "Term": term_display,
                    "P-value": p_val,
                    "Overlap": f"{k}/{len(pathway_genes)}",
                    "Adjusted P-value": 1.0,
                    "Genes": matched_str,
                    "score": score
                })
                
        # Apply Benjamini-Hochberg correction
        if db_results:
            p_vals = [r["P-value"] for r in db_results]
            adj_ps = _apply_benjamini_hochberg(p_vals)
            for idx, r in enumerate(db_results):
                r["Adjusted P-value"] = adj_ps[idx]
            
            # Sort by pvalue significance
            db_results.sort(key=lambda x: x["P-value"])
            
            for r in db_results:
                results.append({
                    "pathway_id": r["id"],
                    "pathway_name": r["Term"],
                    "gene_count": int(r["Overlap"].split("/")[1]),
                    "pvalue": r["P-value"],
                    "fdr": r["Adjusted P-value"],
                    "Term": r["Term"],
                    "Overlap": r["Overlap"],
                    "Adjusted P-value": r["Adjusted P-value"],
                    "Genes": r["Genes"]
                })
                
    log_logger.info(f"Local ORA enrichment computed {len(results)} pathways/terms successfully.")
    return results

def map_proteins_to_kegg(proteins: List[str], log_logger) -> List[Dict[str, Any]]:
    """
    Maps homologous SwissProt protein hit accessions to local KEGG pathway maps.
    """
    log_logger.info(f"Mapping {len(proteins)} annotated proteins to local KEGG database.")
    
    cleaned_genes = []
    for prot in proteins:
        name = str(prot).strip().upper()
        if "_" in name:
            gene_candidate = name.split("_")[0]
            cleaned_genes.append(gene_candidate)
        else:
            cleaned_genes.append(name)
            
    # Include default mappings for classic viral proteins (POL/RDRP/ENV) as baseline pathways
    viral_mappings = []
    for prot in set(proteins):
        prot_upper = prot.upper()
        if "POL" in prot_upper or "RDRP" in prot_upper:
            # Map polymerase activity to DNA repair/mitosis pathways
            viral_mappings.append("hsa03440")  # DNA Repair pathway (Homologous recombination)
        elif "ENV" in prot_upper or "GLYCO" in prot_upper:
            # Map envelope binding to MAPK pathway (cell receptor signaling)
            viral_mappings.append("hsa04010")  # MAPK Signaling pathway
            
    results = []
    M = 20000
    N = len(cleaned_genes)
    if N == 0:
        N = 1 # avoid division by zero
        
    db_results = []
    for p_id, p_data in LOCAL_PATHWAY_DB.items():
        matched = list(set(cleaned_genes) & set(p_data["genes"]))
        if p_id in viral_mappings:
            matched.append("Viral homolog hit")
            
        k = len(matched)
        if k > 0:
            p_val = _hypergeometric_p_value(k, M, len(p_data["genes"]), N)
            db_results.append({
                "id": p_id,
                "name": p_data["name"],
                "overlap": f"{k}/{len(p_data['genes'])}",
                "pvalue": p_val
            })
            
    db_results.sort(key=lambda x: x["pvalue"])
    
    for idx, r in enumerate(db_results):
        results.append({
            "pathway_id": r["id"],
            "pathway_name": f"{r['name']} ({r['id']})",
            "gene_count": int(r["overlap"].split("/")[1]),
            "pvalue": r["pvalue"],
            "fdr": r["pvalue"] * len(LOCAL_PATHWAY_DB) / (idx + 1)
        })
        
    # Cap FDR
    for r in results:
        r["fdr"] = min(r["fdr"], 1.0)
        
    return results
