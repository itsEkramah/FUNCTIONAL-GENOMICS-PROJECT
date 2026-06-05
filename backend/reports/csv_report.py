import os
import csv
from typing import List, Dict, Any
from backend.reports.base_report import BaseReport

class CsvReport(BaseReport):
    """
    Exposes compilation methods to export analysis results to standard CSV tabular sheets.
    """
    def generate(self, seqid: str, orfs: List[Dict[str, Any]], annotations: List[Dict[str, Any]], domains: List[Dict[str, Any]], pathways: List[Dict[str, Any]]) -> str:
        """
        Generates unified CSV file of annotations and returns path.
        """
        output_path = self.get_output_path(f"{seqid}_summary.csv")
        
        # Build lookups
        annot_map = {h["query_protein"]: h for h in annotations}
        
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            # Headers
            writer.writerow([
                "SequenceID", "ORF_ID", "Strand", "Start", "End", "Length_bp", 
                "Subject_Protein", "Identity_Percent", "E-value", "Annotation"
            ])
            
            for idx, orf in enumerate(orfs):
                orf_name = f"seq_{idx + 1}"
                hit = annot_map.get(orf_name)
                
                subj = hit["subject_protein"] if hit else "No Match"
                ident = hit["identity_percent"] if hit else "."
                eval_val = hit["evalue"] if hit else "."
                annot = hit["annotation"] if hit else "Uncharacterized protein"
                
                writer.writerow([
                    seqid, f"ORF_{idx + 1}", orf["strand"], orf["start"], orf["end"], orf["length"],
                    subj, ident, eval_val, annot
                ])
                
        return output_path
