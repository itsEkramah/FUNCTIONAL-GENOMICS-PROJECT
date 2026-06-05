import os
import subprocess
import zipfile
import re
import gzip
from typing import Dict, Any
from Bio.SeqIO.QualityIO import FastqGeneralIterator

def run_fastqc(fastq_path: str, output_dir: str, log_logger) -> Dict[str, Any]:
    """
    Executes FastQC quality control on a FASTQ file (raw or trimmed).
    Parses outputs if successful, otherwise triggers Python-based fallback metrics calculation.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Resolve output files names based on fastq filename
    # e.g., "test_reads.fastq" -> "test_reads_fastqc.zip"
    basename = os.path.basename(fastq_path)
    # Strip common FASTQ extensions
    for ext in (".fastq.gz", ".fastq", ".fq.gz", ".fq"):
        if basename.endswith(ext):
            base_id = basename[:-len(ext)]
            break
    else:
        base_id = os.path.splitext(basename)[0]
        
    zip_output = os.path.join(output_dir, f"{base_id}_fastqc.zip")
    html_output = os.path.join(output_dir, f"{base_id}_fastqc.html")
    
    cmd = ["fastqc", "-o", output_dir, fastq_path]
    log_logger.info(f"Executing FastQC: {' '.join(cmd)}")
    
    try:
        # Run FastQC command
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        log_logger.info("FastQC completed successfully. Parsing reports.")
        
        # Parse metrics from zip file
        return _parse_fastqc_zip(zip_output, base_id, log_logger)
        
    except (subprocess.CalledProcessError, FileNotFoundError, RuntimeError) as e:
        log_logger.warning(f"FastQC failed or binary missing ({str(e)}). Running offline Python QC analyzer.")
        # Trigger Python fallback QC calculation
        metrics = _run_python_qc(fastq_path, log_logger)
        
        # Write mock HTML file
        with open(html_output, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head><title>FastQC Mock Report</title></head>
<body style="font-family: sans-serif; padding: 20px; background-color: #f8fafc;">
    <h2>FastQC Mock Report (Offline Fallback)</h2>
    <p>File: <b>{basename}</b></p>
    <ul>
        <li>Total Sequences: <b>{metrics['total_reads']:,}</b></li>
        <li>GC Content: <b>{metrics['gc_content']:.2f}%</b></li>
        <li>Average Quality Score: <b>{metrics['average_quality']:.2f}</b></li>
    </ul>
</body>
</html>
""")
            
        # Write mock ZIP file with data file
        _write_mock_fastqc_zip(zip_output, base_id, metrics)
        return metrics

def _parse_fastqc_zip(zip_path: str, base_id: str, log_logger) -> Dict[str, Any]:
    """
    Extracts and parses fastqc_data.txt from FastQC output zip.
    """
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"FastQC ZIP report not found: {zip_path}")
        
    total_reads = 0
    gc_content = 0.0
    average_quality = 0.0
    
    with zipfile.ZipFile(zip_path, 'r') as archive:
        data_filename = f"{base_id}_fastqc/fastqc_data.txt"
        try:
            with archive.open(data_filename) as f:
                content = f.read().decode('utf-8')
        except KeyError:
            # Try to list files and find fastqc_data.txt
            for name in archive.namelist():
                if name.endswith("fastqc_data.txt"):
                    with archive.open(name) as f:
                        content = f.read().decode('utf-8')
                    break
            else:
                raise FileNotFoundError(f"Could not locate fastqc_data.txt in ZIP: {zip_path}")
                
    # Parse total sequences and %GC
    for line in content.split("\n"):
        if line.startswith("Total Sequences"):
            total_reads = int(line.split("\t")[1].strip())
        elif line.startswith("%GC"):
            gc_content = float(line.split("\t")[1].strip())
            
    # Parse Per sequence quality scores block to calculate average quality
    # Locate quality scores module
    qual_match = re.search(r">>Per sequence quality scores.*?>>END_MODULE", content, re.DOTALL)
    if qual_match:
        qual_lines = qual_match.group(0).split("\n")[2:-1] # skip module header and table headers
        sum_scores = 0.0
        total_count = 0.0
        for line in qual_lines:
            parts = line.split("\t")
            if len(parts) >= 2:
                # Can be a range (e.g. 25-29) or single score
                score_str = parts[0].strip()
                count = float(parts[1].strip())
                if "-" in score_str:
                    s1, s2 = score_str.split("-")
                    score = (float(s1) + float(s2)) / 2.0
                else:
                    score = float(score_str)
                sum_scores += score * count
                total_count += count
        if total_count > 0:
            average_quality = sum_scores / total_count
            
    log_logger.info(f"Parsed QC: reads={total_reads}, GC%={gc_content:.2f}, AvgQuality={average_quality:.2f}")
    return {
        "total_reads": total_reads,
        "gc_content": gc_content,
        "average_quality": round(average_quality, 4)
    }

def _run_python_qc(fastq_path: str, log_logger) -> Dict[str, Any]:
    """
    Python-only memory-safe streaming quality analyzer for FASTQ files.
    """
    total_reads = 0
    total_bases = 0
    total_gc = 0
    total_quality = 0.0
    
    # Handle gzip files automatically
    if fastq_path.endswith(".gz"):
        handle = gzip.open(fastq_path, "rt", encoding="utf-8")
    else:
        handle = open(fastq_path, "r", encoding="utf-8", errors="ignore")
        
    try:
        iterator = FastqGeneralIterator(handle)
        for _, seq, qual in iterator:
            total_reads += 1
            length = len(seq)
            total_bases += length
            total_gc += seq.count("G") + seq.count("C")
            
            # Sum up Phred scores
            total_quality += sum(ord(c) - 33 for c in qual)
            
            # Log progress on large datasets
            if total_reads % 100000 == 0:
                log_logger.info(f"Analyzed {total_reads} reads...")
    finally:
        handle.close()
        
    gc_content = (total_gc / total_bases * 100.0) if total_bases > 0 else 0.0
    avg_quality = (total_quality / total_bases) if total_bases > 0 else 0.0
    
    return {
        "total_reads": total_reads,
        "gc_content": round(gc_content, 4),
        "average_quality": round(avg_quality, 4)
    }

def _write_mock_fastqc_zip(zip_path: str, base_id: str, metrics: Dict[str, Any]):
    """
    Compiles a mock zip archive containing the parsed fastqc_data.txt file.
    """
    mock_content = f"""##FastQC Mock data
Total Sequences	{metrics['total_reads']}
%GC	{metrics['gc_content']}
>>Per sequence quality scores	pass
#Quality	Count
{int(metrics['average_quality'])}	{metrics['total_reads']}
>>END_MODULE
"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(f"{base_id}_fastqc/fastqc_data.txt", mock_content)
