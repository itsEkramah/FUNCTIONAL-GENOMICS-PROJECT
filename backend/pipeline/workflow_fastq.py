import os
import shutil
import json
from typing import Dict, Any
from Bio import SeqIO
from Bio.SeqIO.QualityIO import FastqGeneralIterator

from backend.database import SessionLocal
from backend.config.constants import JOBS_DIR
from backend.pipeline.pipeline_runner import PipelineStep, PipelineRunner
from backend.utils.file_detector import detect_file_type
from backend.services.fastqc_service import run_fastqc
from backend.services.fastp_service import run_fastp
from backend.services.spades_service import run_spades
from backend.database.repository import save_fastq_run

# Import FASTA steps to chain them downstream
from backend.pipeline.workflow_fasta import (
    run_input_validation,
    validate_input_validation,
    run_sequence_qc_step,
    validate_sequence_qc_step,
    run_orf_detection_step,
    validate_orf_detection_step,
    run_translation_step,
    validate_translation_step,
    run_diamond_step,
    validate_diamond_step,
    run_pfam_step,
    validate_pfam_step,
    run_kegg_step,
    validate_kegg_step,
    run_taxonomy_step,
    validate_taxonomy_step,
    run_pubmed_step,
    validate_pubmed_step,
    run_ai_step,
    validate_ai_step,
    run_reports_step,
    validate_reports_step
)

# =============================================================================
# STEP 1: FASTQ INPUT VALIDATION
# =============================================================================

def run_fastq_input_validation(job_dir: str, logger) -> Dict[str, Any]:
    fastq_path = None
    for filename in ["input.fastq", "input.fastq.gz", "input.fq", "input.fq.gz"]:
        path = os.path.join(job_dir, filename)
        if os.path.exists(path):
            fastq_path = path
            break
            
    if not fastq_path:
        # Search for any fastq file
        for f in os.listdir(job_dir):
            if f.lower().endswith((".fastq", ".fastq.gz", ".fq", ".fq.gz")):
                fastq_path = os.path.join(job_dir, f)
                break
                
    if not fastq_path:
        logger.error(f"No input FASTQ file found in job directory: {job_dir}")
        raise FileNotFoundError(f"Missing input FASTQ file in {job_dir}")
        
    logger.info(f"Validating input FASTQ file: {fastq_path}")
    file_type = detect_file_type(fastq_path)
    if file_type != "FASTQ":
        logger.error(f"File detector identified file as {file_type}, not FASTQ.")
        raise ValueError(f"Uploaded file is not a valid FASTQ format (detected: {file_type})")
        
    # Check if file has at least one record (basic format check)
    try:
        if fastq_path.endswith(".gz"):
            import gzip
            with gzip.open(fastq_path, "rt", encoding="utf-8") as f:
                iterator = FastqGeneralIterator(f)
                next(iterator)
        else:
            with open(fastq_path, "r", encoding="utf-8", errors="ignore") as f:
                iterator = FastqGeneralIterator(f)
                next(iterator)
    except Exception as e:
        logger.error(f"Invalid FASTQ structure or empty file: {str(e)}")
        raise ValueError(f"Invalid FASTQ format: {str(e)}")
        
    logger.info("FASTQ input validation completed successfully.")
    return {"fastq_path": fastq_path}

def validate_fastq_input_validation(job_dir: str, output: Any, logger) -> bool:
    if not output or "fastq_path" not in output:
        return False
    return os.path.exists(output["fastq_path"])

# =============================================================================
# STEP 2: RAW READS QC (FASTQC)
# =============================================================================

def run_fastqc_raw(job_dir: str, logger) -> Dict[str, Any]:
    fastq_path = None
    for filename in ["input.fastq", "input.fastq.gz", "input.fq", "input.fq.gz"]:
        path = os.path.join(job_dir, filename)
        if os.path.exists(path):
            fastq_path = path
            break
    if not fastq_path:
        raise FileNotFoundError(f"Input FASTQ file not found in {job_dir}")
        
    output_dir = os.path.join(job_dir, "fastqc_raw")
    metrics = run_fastqc(fastq_path, output_dir, logger)
    
    # Save the raw metrics to a json file for validation
    metrics_path = os.path.join(job_dir, "raw_qc_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
        
    return metrics

def validate_fastqc_raw(job_dir: str, output: Any, logger) -> bool:
    metrics_path = os.path.join(job_dir, "raw_qc_metrics.json")
    if not os.path.exists(metrics_path):
        return False
    files = os.listdir(os.path.join(job_dir, "fastqc_raw"))
    has_zip = any(f.endswith(".zip") for f in files)
    has_html = any(f.endswith(".html") for f in files)
    return has_zip and has_html

# =============================================================================
# STEP 3: QUALITY TRIMMING (FASTP)
# =============================================================================

def run_fastp_trimming(job_dir: str, logger) -> Dict[str, Any]:
    fastq_path = None
    for filename in ["input.fastq", "input.fastq.gz", "input.fq", "input.fq.gz"]:
        path = os.path.join(job_dir, filename)
        if os.path.exists(path):
            fastq_path = path
            break
    if not fastq_path:
        raise FileNotFoundError(f"Input FASTQ file not found in {job_dir}")
        
    trimmed_fastq = os.path.join(job_dir, "trimmed.fastq")
    output_dir = os.path.join(job_dir, "fastp_reports")
    
    metrics = run_fastp(fastq_path, trimmed_fastq, output_dir, logger)
    
    # Save metrics to json file
    metrics_path = os.path.join(job_dir, "fastp_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
        
    return metrics

def validate_fastp_trimming(job_dir: str, output: Any, logger) -> bool:
    trimmed_fastq = os.path.join(job_dir, "trimmed.fastq")
    metrics_path = os.path.join(job_dir, "fastp_metrics.json")
    if not os.path.exists(trimmed_fastq) or not os.path.exists(metrics_path):
        return False
    if os.path.getsize(trimmed_fastq) == 0:
        return False
    return True

# =============================================================================
# STEP 4: TRIMMED READS QC (FASTQC)
# =============================================================================

def run_fastqc_trimmed(job_dir: str, logger) -> Dict[str, Any]:
    trimmed_fastq = os.path.join(job_dir, "trimmed.fastq")
    if not os.path.exists(trimmed_fastq):
        raise FileNotFoundError(f"Trimmed FASTQ file not found in {job_dir}")
        
    output_dir = os.path.join(job_dir, "fastqc_trimmed")
    metrics = run_fastqc(trimmed_fastq, output_dir, logger)
    
    metrics_path = os.path.join(job_dir, "trimmed_qc_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
        
    return metrics

def validate_fastqc_trimmed(job_dir: str, output: Any, logger) -> bool:
    metrics_path = os.path.join(job_dir, "trimmed_qc_metrics.json")
    if not os.path.exists(metrics_path):
        return False
    files = os.listdir(os.path.join(job_dir, "fastqc_trimmed"))
    has_zip = any(f.endswith(".zip") for f in files)
    has_html = any(f.endswith(".html") for f in files)
    return has_zip and has_html

# =============================================================================
# STEP 5: DE NOVO ASSEMBLY (SPADES)
# =============================================================================

def run_spades_assembly(job_dir: str, logger) -> Dict[str, Any]:
    trimmed_fastq = os.path.join(job_dir, "trimmed.fastq")
    if not os.path.exists(trimmed_fastq):
        raise FileNotFoundError(f"Trimmed FASTQ file not found in {job_dir}")
        
    assembly_dir = os.path.join(job_dir, "spades_assembly")
    contigs_path = run_spades(trimmed_fastq, assembly_dir, logger)
    
    return {"contigs_path": contigs_path}

def validate_spades_assembly(job_dir: str, output: Any, logger) -> bool:
    if not output or "contigs_path" not in output:
        return False
    contigs_path = output["contigs_path"]
    return os.path.exists(contigs_path) and os.path.getsize(contigs_path) > 0

# =============================================================================
# STEP 6: CONTIG LENGTH FILTERING & STATE PERSISTENCE
# =============================================================================

def run_contig_filtering(job_dir: str, logger) -> Dict[str, Any]:
    assembly_dir = os.path.join(job_dir, "spades_assembly")
    contigs_path = os.path.join(assembly_dir, "contigs.fasta")
    if not os.path.exists(contigs_path):
        raise FileNotFoundError(f"Assembly contigs.fasta not found at {contigs_path}")
        
    output_fasta = os.path.join(job_dir, "input.fasta")
    
    # Filter contigs >= 500bp
    filtered_contigs = []
    total_contigs = 0
    with open(contigs_path, "r") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            total_contigs += 1
            if len(record.seq) >= 500:
                filtered_contigs.append(record)
                
    # Write to input.fasta
    with open(output_fasta, "w") as out:
        SeqIO.write(filtered_contigs, out, "fasta")
        
    logger.info(f"Contig filtering complete. Total contigs: {total_contigs}, Filtered contigs (>=500bp): {len(filtered_contigs)}")
    
    # Retrieve metrics from previous runs to populate database model
    fastp_metrics_path = os.path.join(job_dir, "fastp_metrics.json")
    with open(fastp_metrics_path, "r", encoding="utf-8") as f:
        fastp_metrics = json.load(f)
        
    trimmed_qc_metrics_path = os.path.join(job_dir, "trimmed_qc_metrics.json")
    with open(trimmed_qc_metrics_path, "r", encoding="utf-8") as f:
        trimmed_metrics = json.load(f)
        
    raw_reads = fastp_metrics["raw_reads"]
    filtered_reads = fastp_metrics["filtered_reads"]
    average_quality = trimmed_metrics["average_quality"]
    
    # Load raw QC metrics
    raw_qc_metrics_path = os.path.join(job_dir, "raw_qc_metrics.json")
    raw_qc = {}
    if os.path.exists(raw_qc_metrics_path):
        with open(raw_qc_metrics_path, "r", encoding="utf-8") as f:
            raw_qc = json.load(f)
            
    # Generate FASTQ plots
    from backend.core.visualization_engine import generate_fastq_plots
    try:
        generate_fastq_plots(job_dir, raw_qc, trimmed_metrics, fastp_metrics, len(filtered_contigs), logger)
    except Exception as vis_err:
        logger.error(f"Failed to generate FASTQ visualizations: {str(vis_err)}")
        
    job_id = os.path.basename(job_dir)
    
    # Save FastqRun record in the database
    with SessionLocal() as db:
        save_fastq_run(
            db=db,
            job_id=job_id,
            raw_reads=raw_reads,
            filtered_reads=filtered_reads,
            average_quality=average_quality,
            assembly_contigs=len(filtered_contigs)
        )
        
    logger.info(f"Persisted FastqRun stats to DB. Job: {job_id}, raw_reads={raw_reads}, filtered={filtered_reads}, quality={average_quality}, contigs={len(filtered_contigs)}")
    
    return {
        "filtered_contigs": len(filtered_contigs),
        "total_contigs": total_contigs,
        "input_fasta": output_fasta
    }

def validate_contig_filtering(job_dir: str, output: Any, logger) -> bool:
    output_fasta = os.path.join(job_dir, "input.fasta")
    if not os.path.exists(output_fasta):
        return False
    try:
        with open(output_fasta, "r") as handle:
            records = list(SeqIO.parse(handle, "fasta"))
            return len(records) > 0
    except Exception:
        return False

# =============================================================================
# PIPELINE ORCHESTRATION (17 STEPS)
# =============================================================================

def run_fastq_workflow(job_id: str, fastq_path: str):
    """
    Orchestrates the sequential execution of the 17 FASTQ + FASTA workflow steps through PipelineRunner.
    """
    job_dir = os.path.join(JOBS_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)
    
    # Copy the input FASTQ file to the job directory
    basename = os.path.basename(fastq_path)
    if basename.endswith(".gz"):
        dest_name = "input.fastq.gz"
    else:
        dest_name = "input.fastq"
    shutil.copy(fastq_path, os.path.join(job_dir, dest_name))
    
    # Define FASTQ steps (1-6)
    step1 = PipelineStep("FASTQ Input Validation", 1, run_fastq_input_validation, validate_fastq_input_validation)
    step2 = PipelineStep("FastQC Raw Read QC", 2, run_fastqc_raw, validate_fastqc_raw)
    step3 = PipelineStep("fastp Quality Trimming", 3, run_fastp_trimming, validate_fastp_trimming)
    step4 = PipelineStep("FastQC Trimmed Read QC", 4, run_fastqc_trimmed, validate_fastqc_trimmed)
    step5 = PipelineStep("SPAdes De Novo Assembly", 5, run_spades_assembly, validate_spades_assembly)
    step6 = PipelineStep("Contig Length Filtering", 6, run_contig_filtering, validate_contig_filtering)
    
    # Define chained FASTA steps (7-17)
    step7 = PipelineStep("FASTA Input Validation", 7, run_input_validation, validate_input_validation)
    step8 = PipelineStep("Sequence QC", 8, run_sequence_qc_step, validate_sequence_qc_step)
    step9 = PipelineStep("ORF Detection", 9, run_orf_detection_step, validate_orf_detection_step)
    step10 = PipelineStep("Translation", 10, run_translation_step, validate_translation_step)
    step11 = PipelineStep("DIAMOND Annotation", 11, run_diamond_step, validate_diamond_step)
    step12 = PipelineStep("Pfam Annotation", 12, run_pfam_step, validate_pfam_step)
    step13 = PipelineStep("KEGG Mapping", 13, run_kegg_step, validate_kegg_step)
    step14 = PipelineStep("NCBI Taxonomy", 14, run_taxonomy_step, validate_taxonomy_step)
    step15 = PipelineStep("PubMed Retrieval", 15, run_pubmed_step, validate_pubmed_step)
    step16 = PipelineStep("AI Interpretation", 16, run_ai_step, validate_ai_step)
    step17 = PipelineStep("Report Generation", 17, run_reports_step, validate_reports_step)
    
    steps = [
        step1, step2, step3, step4, step5, step6,
        step7, step8, step9, step10, step11, step12, step13, step14, step15, step16, step17
    ]
    
    runner = PipelineRunner()
    runner.register_steps(job_id, steps)
    runner.run_job(job_id, steps)
