from typing import List, Dict, Any
from Bio.Seq import Seq

def scan_strand(sequence: str, strand_code: str, seq_len: int, min_len: int) -> List[Dict[str, Any]]:
    """
    Scans a single strand sequence codon-by-codon in 3 frames for ORFs.
    
    Parameters:
    -----------
    sequence : str
        The DNA sequence to scan.
    strand_code : str
        '+' for forward strand, '-' for reverse complement strand.
    seq_len : int
        The total length of the original forward sequence.
    min_len : int
        Minimum ORF length in base pairs.
        
    Returns:
    --------
    orfs : list
        List of identified ORFs on this strand.
    """
    orfs = []
    # Loop over the 3 frames (0, 1, 2)
    for frame in [0, 1, 2]:
        orf_start = -1
        for i in range(frame, len(sequence) - 2, 3):
            codon = sequence[i:i+3]
            if codon == "ATG":
                if orf_start == -1:
                    orf_start = i
            elif codon in ("TAA", "TAG", "TGA"):
                if orf_start != -1:
                    orf_len = (i + 3) - orf_start
                    if orf_len >= min_len:
                        # Calculate start and end coordinates in 1-based forward genome indexing
                        if strand_code == "+":
                            start_pos = orf_start + 1
                            end_pos = i + 3
                        else:
                            # Map RC coordinate back to forward strand
                            # i + 3 is the end of the stop codon on RC sequence (0-indexed)
                            # orf_start is the index of ATG on RC sequence
                            start_pos = seq_len - (i + 3) + 1
                            end_pos = seq_len - orf_start
                        
                        orfs.append({
                            "sequence": sequence[orf_start:i+3],
                            "start": start_pos,
                            "end": end_pos,
                            "length": orf_len,
                            "strand": strand_code,
                            "frame": frame + 1
                        })
                    orf_start = -1
    return orfs

def remove_overlapping_orfs(orfs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Compares all identified ORFs and removes shorter ORFs where sequences 
    overlap on the same strand.
    """
    # Sort ORFs by length descending (longest first)
    sorted_orfs = sorted(orfs, key=lambda x: x["length"], reverse=True)
    non_overlapping = []
    
    for candidate in sorted_orfs:
        overlap = False
        for accepted in non_overlapping:
            if candidate["strand"] == accepted["strand"]:
                # Check overlap on forward strand coordinates
                if (candidate["start"] <= accepted["end"]) and (candidate["end"] >= accepted["start"]):
                    overlap = True
                    break
        if not overlap:
            non_overlapping.append(candidate)
            
    # Return sorted by forward strand start coordinate
    return sorted(non_overlapping, key=lambda x: x["start"])

def find_orfs(sequence: str, min_len: int = 100) -> List[Dict[str, Any]]:
    """
    Orchestrates 6-frame ORF scanning on both forward and reverse complement strands.
    """
    seq_upper = sequence.upper()
    seq_len = len(seq_upper)
    
    # 1. Scan forward strand
    forward_orfs = scan_strand(seq_upper, "+", seq_len, min_len)
    
    # 2. Compute reverse complement using BioPython
    seq_obj = Seq(seq_upper)
    rc_sequence = str(seq_obj.reverse_complement())
    reverse_orfs = scan_strand(rc_sequence, "-", seq_len, min_len)
    
    # 3. Combine and eliminate overlaps
    combined_orfs = forward_orfs + reverse_orfs
    filtered_orfs = remove_overlapping_orfs(combined_orfs)
    
    return filtered_orfs
