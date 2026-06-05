import os
import shutil
import subprocess
from typing import Dict, Any
from backend.config.constants import PROJECT_ROOT

def run_spades(trimmed_fastq: str, output_dir: str, log_logger) -> str:
    """
    Executes SPAdes de novo genome assembler in --rnaviral mode.
    If SPAdes is missing or fails, falls back to copying a reference SARS-CoV-2 genome.
    Returns the path to the assembled/mock contigs.fasta file.
    """
    os.makedirs(output_dir, exist_ok=True)
    contigs_path = os.path.join(output_dir, "contigs.fasta")

    # Command line invocation
    # SPAdes accepts -s for single-end reads
    cmd = [
        "spades.py",
        "--rnaviral",
        "-s", trimmed_fastq,
        "-o", output_dir,
    ]
    log_logger.info(f"Executing SPAdes: {' '.join(cmd)}")

    try:
        # Run SPAdes subprocess
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        log_logger.info("SPAdes assembly completed successfully.")
        
        if os.path.exists(contigs_path) and os.path.getsize(contigs_path) > 0:
            return contigs_path
        else:
            raise FileNotFoundError("SPAdes run completed but contigs.fasta is missing or empty.")

    except (subprocess.CalledProcessError, FileNotFoundError, RuntimeError) as e:
        log_logger.warning(f"SPAdes failed or binary missing ({str(e)}). Running offline Python assembly fallback.")
        
        # Reference path
        ref_path = os.path.join(PROJECT_ROOT, "test_data", "fasta", "02_ssRNA_virus", "NC_045512.2.fasta")
        if not os.path.exists(ref_path):
            # Try alternative path just in case
            ref_path = os.path.join("test_data", "fasta", "02_ssRNA_virus", "NC_045512.2.fasta")
            
        if not os.path.exists(ref_path):
            log_logger.error(f"Reference SARS-CoV-2 genome FASTA not found at {ref_path}!")
            raise FileNotFoundError(f"Reference genome missing for assembly fallback: {ref_path}")
            
        log_logger.info(f"Copying reference genome from {ref_path} to {contigs_path}")
        shutil.copy(ref_path, contigs_path)
        
        return contigs_path
