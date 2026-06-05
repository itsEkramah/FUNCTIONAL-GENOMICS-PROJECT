import os
import subprocess
import json
import gzip
from typing import Dict, Any
from Bio.SeqIO.QualityIO import FastqGeneralIterator

def run_fastp(fastq_path: str, output_fastq: str, output_dir: str, log_logger) -> Dict[str, Any]:
    """
    Executes fastp quality trimming and adapter removal on a FASTQ file.
    If fastp is not installed or fails, falls back to a custom Python-based streaming QC trimmer.
    """
    os.makedirs(output_dir, exist_ok=True)
    json_report = os.path.join(output_dir, "fastp.json")
    html_report = os.path.join(output_dir, "fastp.html")

    # Command line invocation
    cmd = [
        "fastp",
        "-i", fastq_path,
        "-o", output_fastq,
        "-j", json_report,
        "-h", html_report,
        "-q", "20",  # Q20 quality score threshold
        "-l", "50",  # length filtering threshold
    ]
    log_logger.info(f"Executing fastp command: {' '.join(cmd)}")

    try:
        # Run fastp subprocess
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        log_logger.info("fastp completed successfully. Parsing reports.")
        
        # Parse metrics from JSON
        with open(json_report, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        raw_reads = data["summary"]["before_filtering"]["total_reads"]
        filtered_reads = data["summary"]["after_filtering"]["total_reads"]
        
        # Calculate exact average quality of filtered reads
        metrics = _calculate_fastq_metrics(output_fastq, log_logger)
        
        return {
            "raw_reads": raw_reads,
            "filtered_reads": filtered_reads,
            "average_quality": metrics["average_quality"],
            "gc_content": metrics["gc_content"]
        }

    except (subprocess.CalledProcessError, FileNotFoundError, RuntimeError) as e:
        log_logger.warning(f"fastp failed or binary missing ({str(e)}). Running offline Python trimming fallback.")
        
        # Run Python fallback quality filtering
        metrics = _run_python_trimmer(fastq_path, output_fastq, log_logger)
        
        # Write mock fastp JSON
        mock_json_data = {
            "summary": {
                "before_filtering": {
                    "total_reads": metrics["raw_reads"],
                    "total_bases": metrics["raw_bases"],
                },
                "after_filtering": {
                    "total_reads": metrics["filtered_reads"],
                    "total_bases": metrics["filtered_bases"],
                }
            }
        }
        with open(json_report, "w", encoding="utf-8") as f:
            json.dump(mock_json_data, f, indent=4)
            
        # Write mock HTML page
        with open(html_report, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head><title>fastp Mock Report</title></head>
<body style="font-family: sans-serif; padding: 20px; background-color: #f8fafc;">
    <h2>fastp Mock Report (Offline Fallback)</h2>
    <p>Input file: <b>{os.path.basename(fastq_path)}</b></p>
    <ul>
        <li>Raw Reads: <b>{metrics['raw_reads']:,}</b></li>
        <li>Filtered Reads: <b>{metrics['filtered_reads']:,}</b> ({(metrics['filtered_reads']/metrics['raw_reads']*100.0) if metrics['raw_reads'] > 0 else 0.0:.2f}%)</li>
        <li>Average Quality: <b>{metrics['average_quality']:.2f}</b></li>
        <li>GC Content: <b>{metrics['gc_content']:.2f}%</b></li>
    </ul>
</body>
</html>
""")
            
        return {
            "raw_reads": metrics["raw_reads"],
            "filtered_reads": metrics["filtered_reads"],
            "average_quality": metrics["average_quality"],
            "gc_content": metrics["gc_content"]
        }

def _calculate_fastq_metrics(fastq_path: str, log_logger) -> Dict[str, Any]:
    """
    Helper to calculate average quality and GC content for a FASTQ file.
    """
    total_bases = 0
    total_gc = 0
    total_quality = 0.0
    
    if fastq_path.endswith(".gz"):
        handle = gzip.open(fastq_path, "rt", encoding="utf-8")
    else:
        handle = open(fastq_path, "r", encoding="utf-8", errors="ignore")
        
    try:
        iterator = FastqGeneralIterator(handle)
        for _, seq, qual in iterator:
            total_bases += len(seq)
            total_gc += seq.count("G") + seq.count("C")
            total_quality += sum(ord(c) - 33 for c in qual)
    finally:
        handle.close()
        
    gc_content = (total_gc / total_bases * 100.0) if total_bases > 0 else 0.0
    avg_quality = (total_quality / total_bases) if total_bases > 0 else 0.0
    
    return {
        "average_quality": round(avg_quality, 4),
        "gc_content": round(gc_content, 4)
    }

def _run_python_trimmer(fastq_path: str, output_fastq: str, log_logger) -> Dict[str, Any]:
    """
    Python fallback trimmer. Trims bases with Phred score < 20 from ends.
    Discards reads shorter than 50bp. Aborts if 0 reads survive.
    """
    raw_reads = 0
    raw_bases = 0
    filtered_reads = 0
    filtered_bases = 0
    filtered_gc = 0
    filtered_quality_sum = 0.0

    # Open input stream
    if fastq_path.endswith(".gz"):
        in_handle = gzip.open(fastq_path, "rt", encoding="utf-8")
    else:
        in_handle = open(fastq_path, "r", encoding="utf-8", errors="ignore")
        
    # Open output stream
    if output_fastq.endswith(".gz"):
        out_handle = gzip.open(output_fastq, "wt", encoding="utf-8")
    else:
        out_handle = open(output_fastq, "w", encoding="utf-8")

    try:
        iterator = FastqGeneralIterator(in_handle)
        for title, seq, qual in iterator:
            raw_reads += 1
            raw_bases += len(seq)
            
            # Convert quality string to Phred scores
            scores = [ord(c) - 33 for c in qual]
            
            # Trim from left end (Phred < 20)
            start = 0
            while start < len(scores) and scores[start] < 20:
                start += 1
                
            # Trim from right end (Phred < 20)
            end = len(scores)
            while end > start and scores[end - 1] < 20:
                end -= 1
                
            trimmed_len = end - start
            if trimmed_len >= 50:
                filtered_reads += 1
                trimmed_seq = seq[start:end]
                trimmed_qual = qual[start:end]
                
                # Write trimmed read
                out_handle.write(f"@{title}\n{trimmed_seq}\n+\n{trimmed_qual}\n")
                
                # Update metrics
                filtered_bases += trimmed_len
                filtered_gc += trimmed_seq.count("G") + trimmed_seq.count("C")
                filtered_quality_sum += sum(scores[start:end])
                
            if raw_reads % 100000 == 0:
                log_logger.info(f"Processed {raw_reads} raw reads. {filtered_reads} reads survived.")
                
    finally:
        in_handle.close()
        out_handle.close()

    if filtered_reads == 0:
        log_logger.error("0 reads survived quality filtering!")
        raise ValueError("Quality filtering failed: 0 reads survived quality filtering.")

    gc_content = (filtered_gc / filtered_bases * 100.0) if filtered_bases > 0 else 0.0
    avg_quality = (filtered_quality_sum / filtered_bases) if filtered_bases > 0 else 0.0

    log_logger.info(f"Trimming complete. Raw reads: {raw_reads}, Filtered reads: {filtered_reads} ({(filtered_reads/raw_reads*100.0) if raw_reads > 0 else 0.0:.2f}%)")
    
    return {
        "raw_reads": raw_reads,
        "raw_bases": raw_bases,
        "filtered_reads": filtered_reads,
        "filtered_bases": filtered_bases,
        "average_quality": round(avg_quality, 4),
        "gc_content": round(gc_content, 4)
    }
