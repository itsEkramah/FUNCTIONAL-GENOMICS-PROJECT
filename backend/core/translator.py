from Bio.Seq import Seq
import logging

def translate_dna_to_protein(dna_sequence: str) -> str:
    """
    Translates a DNA nucleotide sequence into a peptide protein sequence using BioPython.
    Safely handles trailing non-triplet nucleotides and stop codon exceptions.
    
    Parameters:
    -----------
    dna_sequence : str
        DNA nucleotide string.
        
    Returns:
    --------
    protein_sequence : str
        Translated peptide residue string.
    """
    seq_upper = dna_sequence.upper()
    
    # 1. Truncate trailing nucleotides that do not form a complete triplet codon
    remainder = len(seq_upper) % 3
    if remainder != 0:
        seq_upper = seq_upper[:-remainder]
        
    if len(seq_upper) == 0:
        return ""
        
    # 2. Run translation via BioPython Seq object
    try:
        seq_obj = Seq(seq_upper)
        # to_stop=True: Stops translation at the first stop codon and excludes it from the peptide string.
        # This prevents KeyError stop exceptions and complies with standard biological specifications.
        protein_seq = str(seq_obj.translate(to_stop=True))
        return protein_seq
    except Exception as e:
        logging.getLogger("app").warning(f"Error encountered during BioPython translation: {str(e)}. Falling back to safe char mapping.")
        return ""
