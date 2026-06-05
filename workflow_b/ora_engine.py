import scipy.stats as stats

def run_ora(target_genes: set, pathway_genes: set, background_genes: set) -> float:
    """
    Computes enrichment p-value using one-sided Fisher's Exact Test.
    """
    # Restrict sets to background population
    target_genes = set(target_genes).intersection(background_genes)
    pathway_genes = set(pathway_genes).intersection(background_genes)
    
    a = len(target_genes.intersection(pathway_genes))
    b = len(pathway_genes) - a
    c = len(target_genes) - a
    d = len(background_genes) - len(target_genes) - b
    
    table = [[a, b], [c, d]]
    
    _, pvalue = stats.fisher_exact(table, alternative='greater')
    return pvalue
