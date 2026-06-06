import os
import shutil
import json
from datetime import datetime
from typing import List, Dict, Any

from backend.database import SessionLocal
from backend.models.file import UploadedFile
from backend.models.job import Job, JobStep
from backend.models.results import FastaRun
from backend.config.constants import *
from backend.config.thresholds import *
from backend.pipeline.pipeline_runner import PipelineStep, PipelineRunner
from backend.utils.file_detector import detect_file_type
from backend.core.qc_engine import run_sequence_qc
from backend.core.orf_finder import find_orfs
from backend.core.translator import translate_dna_to_protein
from backend.services.diamond_service import run_diamond_blastp
from backend.services.hmmer_service import run_hmmer_hmmscan
from backend.services.kegg_service import map_proteins_to_kegg
from backend.services.ncbi_service import fetch_ncbi_taxonomy
from backend.services.pubmed_service import fetch_pubmed_evidence
from backend.services.ai_service import generate_interpretation
from backend.reports.html_report import HtmlReport
from backend.reports.gff3_report import Gff3Report
from backend.reports.csv_report import CsvReport
from backend.reports.pdf_report import PdfReport
from backend.database.repository import (
    save_fasta_run,
    save_annotations,
    save_pfam_domains,
    save_taxonomy_result,
    save_kegg_results,
    save_report
)

def extract_organism_name_from_fasta(fasta_path: str) -> str:
    """
    Parses the FASTA header and extracts a clean, search-relevance scientific organism name.
    """
    try:
        with open(fasta_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(">"):
                    header = line[1:].strip()
                    break
            else:
                return "Unknown pathogen"
    except Exception:
        return "Unknown pathogen"
        
    words = header.split()
    if not words:
        return "Unknown pathogen"
        
    # If the first word looks like an accession ID (e.g. dots or numbers), skip it
    if "." in words[0] or "_" in words[0] or any(c.isdigit() for c in words[0]):
        words = words[1:]
        
    cleaned_words = []
    for w in words:
        w_lower = w.lower().strip(":")
        # Filter out common noise tags
        if w_lower in ("mag", "tpa_asm", "synthetic", "complete", "genome", "sequence", "isolate", "strain", "partial", "dna"):
            continue
        cleaned_words.append(w)
        
    # Take first 3-4 keywords representing genus, species, and strain/variant name
    result_words = []
    for w in cleaned_words:
        w_clean = w.strip(",;()[]{}")
        if w_clean.lower() in ("isolate", "strain", "genomic", "complete", "genome", "sequence", "partial"):
            break
        result_words.append(w_clean)
        
    name = " ".join(result_words)
    return name if name else "Unknown pathogen"


# =============================================================================
# STEP 1: INPUT VALIDATION
# =============================================================================

def run_input_validation(job_dir: str, logger) -> Dict[str, Any]:
    input_fasta = os.path.join(job_dir, "input.fasta")
    if not os.path.exists(input_fasta):
        logger.error(f"Input FASTA file missing from job directory: {input_fasta}")
        raise FileNotFoundError(f"Missing input.fasta in {job_dir}")
        
    logger.info(f"Validating input FASTA: {input_fasta}")
    
    # 1. Detect file type using file_detector helper
    file_type = detect_file_type(input_fasta)
    if file_type != "FASTA":
        logger.error(f"File detector identified file as {file_type}, not FASTA.")
        raise ValueError(f"Uploaded file is not a valid FASTA format (detected: {file_type})")
        
    # 2. Check headers and IUPAC nucleotide characters
    valid_chars = set("ATGCNRYKMSWBDHV")
    seq_id = "unknown_seq"
    sequence_lines = []
    
    with open(input_fasta, "r", encoding="utf-8", errors="ignore") as f:
        first_line = f.readline().strip()
        if not first_line.startswith(">"):
            logger.error("First line of the FASTA file does not start with '>'")
            raise ValueError("Invalid FASTA: header line missing.")
            
        header = first_line[1:].strip()
        seq_id = header.split()[0]
        
        for line in f:
            line_strip = line.strip().upper()
            if line_strip.startswith(">"):
                # Multi-fasta files - we only process the first sequence in the workflow
                break
            clean_line = "".join(line_strip.split())
            if clean_line:
                # Check for IUPAC characters
                invalid_chars_in_line = set(clean_line) - valid_chars
                if invalid_chars_in_line:
                    logger.error(f"Detected invalid non-IUPAC nucleotide characters: {invalid_chars_in_line}")
                    raise ValueError(f"Invalid characters in DNA sequence: {invalid_chars_in_line}")
                sequence_lines.append(clean_line)
                
    full_sequence = "".join(sequence_lines)
    if not full_sequence:
        logger.error("FASTA file contains no nucleotide sequence.")
        raise ValueError("FASTA file contains no nucleotide sequence.")
        
    # Write validated sequence to validated.fasta
    validated_path = os.path.join(job_dir, "validated.fasta")
    with open(validated_path, "w", encoding="utf-8") as out:
        out.write(f">{header}\n{full_sequence}\n")
        
    logger.info(f"Input validation successful. Sequence ID: {seq_id}, Length: {len(full_sequence)} bp")
    return {"validated_fasta": validated_path, "seq_id": seq_id}

def validate_input_validation(job_dir: str, output: Any, logger) -> bool:
    validated_path = os.path.join(job_dir, "validated.fasta")
    if not os.path.exists(validated_path):
        return False
    with open(validated_path, "r", encoding="utf-8") as f:
        first_line = f.readline()
        return first_line.startswith(">")


# =============================================================================
# STEP 2: SEQUENCE QC
# =============================================================================

def run_sequence_qc_step(job_dir: str, logger) -> Dict[str, Any]:
    validated_path = os.path.join(job_dir, "validated.fasta")
    sequence_lines = []
    with open(validated_path, "r", encoding="utf-8") as f:
        f.readline() # skip header
        for line in f:
            sequence_lines.append(line.strip())
    sequence = "".join(sequence_lines)
    
    logger.info("Computing genome QC metrics.")
    qc_metrics = run_sequence_qc(sequence)
    
    # Save to file
    qc_json_path = os.path.join(job_dir, "qc_metrics.json")
    with open(qc_json_path, "w", encoding="utf-8") as out:
        json.dump(qc_metrics, out, indent=4)
        
    # Ambiguous bases threshold warning (if N count exceeds 10%)
    if qc_metrics["genome_length"] > 0:
        n_ratio = qc_metrics["ambiguity_count"] / qc_metrics["genome_length"]
        if n_ratio > 0.10:
            logger.warning(f"High ambiguity count detected: {qc_metrics['ambiguity_count']} bases ({n_ratio*100:.2f}%)")
            
    logger.info(f"QC Completed: Length={qc_metrics['genome_length']}, GC%={qc_metrics['gc_content']}, Ambiguous={qc_metrics['ambiguity_count']}")
    return qc_metrics

def validate_sequence_qc_step(job_dir: str, output: Any, logger) -> bool:
    qc_json_path = os.path.join(job_dir, "qc_metrics.json")
    if not os.path.exists(qc_json_path):
        return False
    with open(qc_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return "genome_length" in data and data["genome_length"] >= 0


# =============================================================================
# STEP 3: ORF DETECTION
# =============================================================================

def run_orf_detection_step(job_dir: str, logger) -> List[Dict[str, Any]]:
    validated_path = os.path.join(job_dir, "validated.fasta")
    sequence_lines = []
    with open(validated_path, "r", encoding="utf-8") as f:
        f.readline() # skip header
        for line in f:
            sequence_lines.append(line.strip())
    sequence = "".join(sequence_lines)
    
    logger.info(f"Running 6-frame ORF finder with threshold >= {MIN_ORF_LENGTH_BP} bp")
    orfs = find_orfs(sequence, min_len=MIN_ORF_LENGTH_BP)
    
    # Save to file
    orfs_json_path = os.path.join(job_dir, "orfs.json")
    with open(orfs_json_path, "w", encoding="utf-8") as out:
        json.dump(orfs, out, indent=4)
        
    logger.info(f"Identified {len(orfs)} candidate open reading frames.")
    return orfs

def validate_orf_detection_step(job_dir: str, output: Any, logger) -> bool:
    orfs_json_path = os.path.join(job_dir, "orfs.json")
    return os.path.exists(orfs_json_path)


# =============================================================================
# STEP 4: TRANSLATION
# =============================================================================

def run_translation_step(job_dir: str, logger) -> Dict[str, Any]:
    orfs_json_path = os.path.join(job_dir, "orfs.json")
    with open(orfs_json_path, "r", encoding="utf-8") as f:
        orfs = json.load(f)
        
    logger.info(f"Translating {len(orfs)} candidate nucleotide sequences to amino acids.")
    
    proteins = []
    proteins_fasta_path = os.path.join(job_dir, "proteins.fasta")
    
    with open(proteins_fasta_path, "w", encoding="utf-8") as out:
        for idx, orf in enumerate(orfs):
            orf_seq = orf["sequence"]
            peptide = translate_dna_to_protein(orf_seq)
            # Save headers as seq_1, seq_2 etc.
            protein_id = f"seq_{idx + 1}"
            out.write(f">{protein_id}\n{peptide}\n")
            proteins.append({
                "protein_id": protein_id,
                "peptide": peptide
            })
            
    # Load QC metrics
    qc_json_path = os.path.join(job_dir, "qc_metrics.json")
    with open(qc_json_path, "r", encoding="utf-8") as f:
        qc = json.load(f)
        
    job_id = os.path.basename(job_dir)
    
    # Save FastaRun to DB
    logger.info("Persisting FASTA run execution stats to database.")
    with SessionLocal() as db:
        # Check if FastaRun already exists (prevent unique constraint violation on retry)
        existing = db.query(FastaRun).filter(FastaRun.job_id == job_id).first()
        if existing:
            db.delete(existing)
            db.commit()
            
        save_fasta_run(
            db=db,
            job_id=job_id,
            genome_length=qc["genome_length"],
            gc_content=qc["gc_content"],
            ambiguity_count=qc["ambiguity_count"],
            total_orfs=len(orfs),
            translated_proteins=len(proteins)
        )
        
    logger.info(f"Translation completed. Written {len(proteins)} peptide sequences to proteins.fasta")
    return {"proteins_fasta": proteins_fasta_path, "count": len(proteins)}

def validate_translation_step(job_dir: str, output: Any, logger) -> bool:
    proteins_fasta_path = os.path.join(job_dir, "proteins.fasta")
    return os.path.exists(proteins_fasta_path)


# =============================================================================
# STEP 5: DIAMOND ANNOTATION
# =============================================================================

def run_diamond_step(job_dir: str, logger) -> List[Dict[str, Any]]:
    proteins_fasta_path = os.path.join(job_dir, "proteins.fasta")
    output_tsv = os.path.join(job_dir, "diamond_hits.tsv")
    
    # SwissProt database mock/reference path
    db_path = os.path.join(STORAGE_DIR, "databases", "swissprot.dmnd")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if not os.path.exists(db_path):
        with open(db_path, "w") as f:
            f.write("")
            
    logger.info("Running DIAMOND homology alignments against SwissProt.")
    hits = run_diamond_blastp(proteins_fasta_path, db_path, output_tsv, logger)
    
    # Save hits as JSON
    hits_json_path = os.path.join(job_dir, "annotations.json")
    with open(hits_json_path, "w", encoding="utf-8") as out:
        json.dump(hits, out, indent=4)
        
    # Persist annotations to DB
    job_id = os.path.basename(job_dir)
    logger.info("Saving homologous annotations to database.")
    with SessionLocal() as db:
        save_annotations(db, job_id, hits)
        
    return hits

def validate_diamond_step(job_dir: str, output: Any, logger) -> bool:
    hits_json_path = os.path.join(job_dir, "annotations.json")
    return os.path.exists(hits_json_path)


# =============================================================================
# STEP 6: PFAM ANNOTATION
# =============================================================================

def run_pfam_step(job_dir: str, logger) -> List[Dict[str, Any]]:
    proteins_fasta_path = os.path.join(job_dir, "proteins.fasta")
    output_txt = os.path.join(job_dir, "domains") # hmmscan domtblout will append .domtbl
    
    # Pfam database reference path
    pfam_db_path = os.path.join(STORAGE_DIR, "databases", "Pfam-A.hmm")
    os.makedirs(os.path.dirname(pfam_db_path), exist_ok=True)
    if not os.path.exists(pfam_db_path):
        with open(pfam_db_path, "w") as f:
            f.write("")
            
    logger.info("Running hmmscan protein domain predictions against Pfam.")
    domains = run_hmmer_hmmscan(proteins_fasta_path, pfam_db_path, output_txt, logger)
    
    # Save domains as JSON
    domains_json_path = os.path.join(job_dir, "domains.json")
    with open(domains_json_path, "w", encoding="utf-8") as out:
        json.dump(domains, out, indent=4)
        
    # Save domains to DB
    job_id = os.path.basename(job_dir)
    logger.info("Saving predicted structural domains to database.")
    with SessionLocal() as db:
        save_pfam_domains(db, job_id, domains)
        
    return domains

def validate_pfam_step(job_dir: str, output: Any, logger) -> bool:
    domains_json_path = os.path.join(job_dir, "domains.json")
    return os.path.exists(domains_json_path)


# =============================================================================
# STEP 7: KEGG MAPPING
# =============================================================================

def run_kegg_step(job_dir: str, logger) -> List[Dict[str, Any]]:
    hits_json_path = os.path.join(job_dir, "annotations.json")
    with open(hits_json_path, "r", encoding="utf-8") as f:
        hits = json.load(f)
        
    proteins = [h["subject_protein"] for h in hits]
    
    logger.info("Mapping homologous protein hits to KEGG pathways.")
    pathways = map_proteins_to_kegg(proteins, logger)
    
    # Save to file
    kegg_json_path = os.path.join(job_dir, "kegg_pathways.json")
    with open(kegg_json_path, "w", encoding="utf-8") as out:
        json.dump(pathways, out, indent=4)
        
    # Save to DB
    job_id = os.path.basename(job_dir)
    logger.info("Saving KEGG pathway results to database.")
    with SessionLocal() as db:
        save_kegg_results(db, job_id, pathways)
        
    return pathways

def validate_kegg_step(job_dir: str, output: Any, logger) -> bool:
    kegg_json_path = os.path.join(job_dir, "kegg_pathways.json")
    return os.path.exists(kegg_json_path)


# =============================================================================
# STEP 8: NCBI TAXONOMY
# =============================================================================

def run_taxonomy_step(job_dir: str, logger) -> Dict[str, Any]:
    validated_path = os.path.join(job_dir, "validated.fasta")
    organism_name = extract_organism_name_from_fasta(validated_path)
    
    logger.info(f"Performing taxonomy tree lookup for scientific name: '{organism_name}'")
    taxonomy = fetch_ncbi_taxonomy(organism_name, logger)
    
    # Save to file
    tax_json_path = os.path.join(job_dir, "taxonomy.json")
    with open(tax_json_path, "w", encoding="utf-8") as out:
        json.dump(taxonomy, out, indent=4)
        
    # Save to DB
    job_id = os.path.basename(job_dir)
    logger.info("Saving taxonomy lookup results to database.")
    with SessionLocal() as db:
        save_taxonomy_result(
            db=db,
            job_id=job_id,
            tax_id=taxonomy["tax_id"],
            organism_name=taxonomy["organism_name"],
            lineage=taxonomy["lineage"],
            rank=taxonomy["rank"]
        )
        
    return taxonomy

def validate_taxonomy_step(job_dir: str, output: Any, logger) -> bool:
    tax_json_path = os.path.join(job_dir, "taxonomy.json")
    return os.path.exists(tax_json_path)


# =============================================================================
# STEP 9: PUBMED RETRIEVAL
# =============================================================================

def run_pubmed_step(job_dir: str, logger) -> List[Dict[str, Any]]:
    tax_json_path = os.path.join(job_dir, "taxonomy.json")
    with open(tax_json_path, "r", encoding="utf-8") as f:
        tax = json.load(f)
        
    hits_json_path = os.path.join(job_dir, "annotations.json")
    with open(hits_json_path, "r", encoding="utf-8") as f:
        hits = json.load(f)
        
    organism_name = tax["organism_name"]
    proteins = [h["subject_protein"] for h in hits]
    
    logger.info(f"Querying PubMed evidence articles for '{organism_name}' and matching proteins.")
    articles = fetch_pubmed_evidence(organism_name, proteins, logger, job_dir=job_dir)
    
    # Save to file
    pubmed_json_path = os.path.join(job_dir, "pubmed_articles.json")
    with open(pubmed_json_path, "w", encoding="utf-8") as out:
        json.dump(articles, out, indent=4)
        
    return articles

def validate_pubmed_step(job_dir: str, output: Any, logger) -> bool:
    pubmed_json_path = os.path.join(job_dir, "pubmed_articles.json")
    return os.path.exists(pubmed_json_path)


# =============================================================================
# STEP 10: AI INTERPRETATION
# =============================================================================

def run_ai_step(job_dir: str, logger) -> Dict[str, Any]:
    tax_json_path = os.path.join(job_dir, "taxonomy.json")
    with open(tax_json_path, "r", encoding="utf-8") as f:
        tax = json.load(f)
        
    hits_json_path = os.path.join(job_dir, "annotations.json")
    with open(hits_json_path, "r", encoding="utf-8") as f:
        hits = json.load(f)
        
    domains_json_path = os.path.join(job_dir, "domains.json")
    with open(domains_json_path, "r", encoding="utf-8") as f:
        domains = json.load(f)
        
    kegg_json_path = os.path.join(job_dir, "kegg_pathways.json")
    with open(kegg_json_path, "r", encoding="utf-8") as f:
        pathways = json.load(f)
        
    pubmed_json_path = os.path.join(job_dir, "pubmed_articles.json")
    with open(pubmed_json_path, "r", encoding="utf-8") as f:
        articles = json.load(f)
        
    job_id = os.path.basename(job_dir)
    organism_name = tax["organism_name"]
    
    logger.info("Executing pathobiology interpretation AI engine.")
    ai_result = generate_interpretation(
        job_id=job_id,
        organism_name=organism_name,
        annotations=hits,
        domains=domains,
        pathways=pathways,
        articles=articles,
        log_logger=logger
    )
    
    # Save to file
    ai_json_path = os.path.join(job_dir, "ai_interpretation.json")
    with open(ai_json_path, "w", encoding="utf-8") as out:
        json.dump(ai_result, out, indent=4)
        
    return ai_result

def validate_ai_step(job_dir: str, output: Any, logger) -> bool:
    ai_json_path = os.path.join(job_dir, "ai_interpretation.json")
    return os.path.exists(ai_json_path)


# =============================================================================
# STEP 11: REPORT GENERATION
# =============================================================================

def run_reports_step(job_dir: str, logger) -> Dict[str, str]:
    validated_path = os.path.join(job_dir, "validated.fasta")
    with open(validated_path, "r", encoding="utf-8") as f:
        first_line = f.readline()
        seqid = first_line[1:].strip().split()[0]
        
    qc_json_path = os.path.join(job_dir, "qc_metrics.json")
    with open(qc_json_path, "r", encoding="utf-8") as f:
        qc = json.load(f)
        
    orfs_json_path = os.path.join(job_dir, "orfs.json")
    with open(orfs_json_path, "r", encoding="utf-8") as f:
        orfs = json.load(f)
        
    hits_json_path = os.path.join(job_dir, "annotations.json")
    with open(hits_json_path, "r", encoding="utf-8") as f:
        hits = json.load(f)
        
    domains_json_path = os.path.join(job_dir, "domains.json")
    with open(domains_json_path, "r", encoding="utf-8") as f:
        domains = json.load(f)
        
    kegg_json_path = os.path.join(job_dir, "kegg_pathways.json")
    with open(kegg_json_path, "r", encoding="utf-8") as f:
        pathways = json.load(f)
        
    tax_json_path = os.path.join(job_dir, "taxonomy.json")
    with open(tax_json_path, "r", encoding="utf-8") as f:
        taxonomy = json.load(f)
        
    ai_json_path = os.path.join(job_dir, "ai_interpretation.json")
    with open(ai_json_path, "r", encoding="utf-8") as f:
        ai_result = json.load(f)
        
    job_id = os.path.basename(job_dir)
    
    # Generate FASTA plots
    from backend.core.visualization_engine import generate_fasta_plots
    try:
        generate_fasta_plots(job_dir, qc, orfs, domains, pathways, taxonomy, logger)
    except Exception as vis_err:
        logger.error(f"Failed to generate FASTA visualizations: {str(vis_err)}")

    # Fetch job record and its optional fastq_run from DB
    from backend.models.job import Job
    fastq_run_data = None
    try:
        with SessionLocal() as db:
            job = db.query(Job).filter(Job.id == job_id).first()
            if job and job.fastq_run:
                fastq_run_data = {
                    "raw_reads": job.fastq_run.raw_reads,
                    "filtered_reads": job.fastq_run.filtered_reads,
                    "average_quality": job.fastq_run.average_quality,
                    "assembly_contigs": job.fastq_run.assembly_contigs
                }
    except Exception as db_err:
        logger.warning(f"Could not retrieve fastq_run details for report: {str(db_err)}")

    logger.info("Compiling reports: HTML, GFF3, CSV, PDF, JSON.")
    
    # 1. HTML
    html_path = HtmlReport(job_dir).generate(
        job_id=job_id, seqid=seqid, qc=qc, orfs=orfs, 
        annotations=hits, domains=domains, pathways=pathways, 
        taxonomy=taxonomy, ai_result=ai_result, fastq_run=fastq_run_data
    )
    
    # 2. GFF3
    gff_path = Gff3Report(job_dir).generate(
        seqid=seqid, orfs=orfs, domains=domains
    )
    
    # 3. CSV
    csv_path = CsvReport(job_dir).generate(
        seqid=seqid, orfs=orfs, annotations=hits, domains=domains, pathways=pathways
    )
    
    # 4. PDF
    pdf_path = PdfReport(job_dir).generate(
        job_id=job_id, seqid=seqid, qc=qc, orfs=orfs, 
        annotations=hits, domains=domains, pathways=pathways, 
        taxonomy=taxonomy, ai_result=ai_result
    )
    
    # 5. JSON
    reports_dir = os.path.join(job_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    json_path = os.path.join(reports_dir, "report.json")
    report_data = {
        "job_id": job_id,
        "seqid": seqid,
        "date": datetime.utcnow().isoformat(),
        "qc": qc,
        "orfs": orfs,
        "annotations": hits,
        "domains": domains,
        "pathways": pathways,
        "taxonomy": taxonomy,
        "ai_result": ai_result
    }
    with open(json_path, "w", encoding="utf-8") as out:
        json.dump(report_data, out, indent=4)
        
    # Save reports metadata to DB
    logger.info("Registering generated reports in the database.")
    with SessionLocal() as db:
        save_report(db, job_id, "HTML", html_path)
        save_report(db, job_id, "GFF3", gff_path)
        save_report(db, job_id, "CSV", csv_path)
        save_report(db, job_id, "PDF", pdf_path)
        save_report(db, job_id, "JSON", json_path)
        
    logger.info("Report generation step completed successfully.")
    return {
        "HTML": html_path,
        "GFF3": gff_path,
        "CSV": csv_path,
        "PDF": pdf_path,
        "JSON": json_path
    }

def validate_reports_step(job_dir: str, output: Any, logger) -> bool:
    reports_dir = os.path.join(job_dir, "reports")
    expected_files = ["report.html", "report.pdf", "report.json"]
    for f in expected_files:
        path = os.path.join(reports_dir, f)
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return False
    return True


# =============================================================================
# PIPELINE ORCHESTRATION
# =============================================================================

def run_fasta_workflow(job_id: str, fasta_path: str):
    """
    Orchestrates the sequential execution of the 11 FASTA workflow steps through PipelineRunner.
    """
    job_dir = os.path.join(JOBS_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)
    
    # Copy the input FASTA to job directory as input.fasta
    shutil.copy(fasta_path, os.path.join(job_dir, "input.fasta"))
    
    # Instantiate the steps
    step1 = PipelineStep("Input Validation", 1, run_input_validation, validate_input_validation)
    step2 = PipelineStep("Sequence QC", 2, run_sequence_qc_step, validate_sequence_qc_step)
    step3 = PipelineStep("ORF Detection", 3, run_orf_detection_step, validate_orf_detection_step)
    step4 = PipelineStep("Translation", 4, run_translation_step, validate_translation_step)
    step5 = PipelineStep("DIAMOND Annotation", 5, run_diamond_step, validate_diamond_step)
    step6 = PipelineStep("Pfam Annotation", 6, run_pfam_step, validate_pfam_step)
    step7 = PipelineStep("KEGG Mapping", 7, run_kegg_step, validate_kegg_step)
    step8 = PipelineStep("NCBI Taxonomy", 8, run_taxonomy_step, validate_taxonomy_step)
    step9 = PipelineStep("PubMed Retrieval", 9, run_pubmed_step, validate_pubmed_step)
    step10 = PipelineStep("AI Interpretation", 10, run_ai_step, validate_ai_step)
    step11 = PipelineStep("Report Generation", 11, run_reports_step, validate_reports_step)
    
    steps = [step1, step2, step3, step4, step5, step6, step7, step8, step9, step10, step11]
    
    runner = PipelineRunner()
    runner.register_steps(job_id, steps)
    runner.run_job(job_id, steps)
