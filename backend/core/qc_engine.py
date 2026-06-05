from typing import Dict, Any

def run_sequence_qc(sequence: str) -> Dict[str, Any]:
    """
    Calculates basic quality metrics for a genomic nucleotide sequence.
    
    Parameters:
    -----------
    sequence : str
        DNA sequence characters (upper case).
        
    Returns:
    --------
    qc_metrics : dict
        Calculated length, GC%, and ambiguous base count.
    """
    seq_upper = sequence.upper()
    length = len(seq_upper)
    if length == 0:
        return {
            "genome_length": 0,
            "gc_content": 0.0,
            "ambiguity_count": 0
        }
    
    # Count bases
    g_count = seq_upper.count("G")
    c_count = seq_upper.count("C")
    a_count = seq_upper.count("A")
    t_count = seq_upper.count("T")
    
    gc_content = ((g_count + c_count) / length) * 100.0
    
    # Ambiguous bases represent any character other than A, T, C, G
    ambiguity_count = length - (g_count + c_count + a_count + t_count)
    
    return {
        "genome_length": length,
        "gc_content": round(gc_content, 4),
        "ambiguity_count": ambiguity_count
    }
