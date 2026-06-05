import os
from typing import List, Dict, Any
from backend.reports.base_report import BaseReport

class Gff3Report(BaseReport):
    """
    Exposes compilation methods to export genomic coordinate features to GFF3 v3 format.
    """
    def generate(self, seqid: str, orfs: List[Dict[str, Any]], domains: List[Dict[str, Any]]) -> str:
        """
        Writes identified open reading frames and domain architectures to a GFF3 file.
        
        Parameters:
        -----------
        seqid : str
            Parent sequence/genome ID.
        orfs : list of dict
            Identified ORFs.
        domains : list of dict
            Identified Pfam domains.
            
        Returns:
        --------
        output_path : str
            Absolute path to the compiled GFF3 file.
        """
        output_path = self.get_output_path(f"{seqid}_annotations.gff")
        
        # Build domains map keyed by query protein_id
        dom_map = {}
        for d in domains:
            p_id = d["protein_id"]
            if p_id not in dom_map:
                dom_map[p_id] = []
            dom_map[p_id].append(d)
            
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("##gff-version 3\n")
            f.write(f"##sequence-region {seqid} 1 500000\n")
            
            for idx, orf in enumerate(orfs):
                orf_id = f"orf_{idx + 1}"
                strand = orf["strand"]
                start = min(orf["start"], orf["end"])
                end = max(orf["start"], orf["end"])
                frame = orf["frame"]
                
                # 1. Write gene feature
                f.write(
                    f"{seqid}\tPathoScope_v3.0\tgene\t{start}\t{end}\t.\t{strand}\t.\t"
                    f"ID={orf_id};Name=ORF_{idx + 1};length={orf['length']}\n"
                )
                
                # 2. Write CDS feature
                f.write(
                    f"{seqid}\tPathoScope_v3.0\tCDS\t{start}\t{end}\t.\t{strand}\t0\t"
                    f"ID=cds_{orf_id};Parent={orf_id};Name=CDS_{idx + 1}\n"
                )
                
                # 3. Write domain match sub-features
                orf_key = f"seq_{idx + 1}" # ORFs are typically keyed seq_1, seq_2 etc.
                if orf_key in dom_map:
                    for d_idx, d in enumerate(dom_map[orf_key]):
                        # Map relative domain coordinates to genome absolute coordinates
                        # Note: relative domain coordinates are in amino acids, we convert to bp (multiply by 3)
                        rel_start_bp = (d["domain_start"] - 1) * 3
                        rel_end_bp = d["domain_end"] * 3
                        
                        if strand == "+":
                            d_start = start + rel_start_bp
                            d_end = start + rel_end_bp
                        else:
                            # Reverse strand coordinates map backwards from the end
                            d_start = end - rel_end_bp
                            d_end = end - rel_start_bp
                            
                        f.write(
                            f"{seqid}\tPathoScope_v3.0\tprotein_match\t{d_start}\t{d_end}\t.\t{strand}\t.\t"
                            f"ID=dom_{orf_id}_{d_idx+1};Parent={orf_id};Name={d['pfam_name']};Dbxref=Pfam:{d['pfam_accession']};E-value={d['evalue']}\n"
                        )
                        
        return output_path
