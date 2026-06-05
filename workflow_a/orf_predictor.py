from Bio.Seq import Seq
import config

def scan_strand(sequence: str, min_len: int) -> list:
    orfs = []
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
                        orfs.append(sequence[orf_start:i+3])
                    orf_start = -1
    return orfs

def predict_orfs(dna_sequence: str) -> list:
    seq_upper = dna_sequence.upper()
    min_len = config.MIN_ORF_LENGTH
    
    # 1. Forward strand ORFs
    forward_orfs = scan_strand(seq_upper, min_len)
    
    # 2. Reverse complement strand ORFs
    rc_sequence = str(Seq(seq_upper).reverse_complement())
    reverse_orfs = scan_strand(rc_sequence, min_len)
    
    combined_orfs = forward_orfs + reverse_orfs
    
    # Translate all ORFs using native BioPython translation with to_stop=True
    proteins = []
    for orf in combined_orfs:
        # Translate the codon sequence to protein
        prot = str(Seq(orf).translate(to_stop=True))
        proteins.append(prot)
        
    return proteins
