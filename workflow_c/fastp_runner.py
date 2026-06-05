import os
import subprocess
import json

def run_fastp(fastq_path: str, output_fastq: str, output_json: str, output_html: str) -> dict:
    """
    Runs fastp via subprocess and returns parsed quality metrics.
    """
    cmd = [
        "fastp",
        "-i", fastq_path,
        "-o", output_fastq,
        "-j", output_json,
        "-h", output_html
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
        
    metrics = {
        "total_reads": 0,
        "q30_rate": 0.0
    }
    
    if os.path.exists(output_json):
        try:
            with open(output_json, "r") as f:
                data = json.load(f)
                metrics["total_reads"] = data["summary"]["before_filtering"]["total_reads"]
                metrics["q30_rate"] = data["summary"]["before_filtering"]["q30_rate"]
        except Exception:
            pass
            
    return metrics
