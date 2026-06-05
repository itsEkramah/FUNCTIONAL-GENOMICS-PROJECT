from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from backend.models.user import User, Session as UserSession
from backend.models.job import Job, JobStep
from backend.models.file import UploadedFile
from backend.models.results import FastaRun, FastqRun, DegRun, ReportResult
from backend.models.annotation import AnnotationResult, PfamDomain, TaxonomyResult, KeggPathwayResult
from backend.models.pubmed import PubMedQuery, PubMedArticle
from backend.models.ai import AIInterpretation

# =============================================================================
# USER & SESSION REPOSITORY
# =============================================================================

def create_user(db: Session, username: str, email: str, password_hash: str, role: str = "user") -> User:
    db_user = User(username=username, email=email, password_hash=password_hash, role=role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_session(db: Session, user_id: str, token: str, expires_at: datetime) -> UserSession:
    db_session = UserSession(user_id=user_id, token=token, expires_at=expires_at)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_session_by_token(db: Session, token: str) -> Optional[UserSession]:
    return db.query(UserSession).filter(UserSession.token == token).first()

# =============================================================================
# JOB & STEP TRACKING REPOSITORY
# =============================================================================

def get_job_by_id(db: Session, job_id: str) -> Optional[Job]:
    return db.query(Job).filter(Job.id == job_id).first()

def update_job_status(db: Session, job_id: str, status: str, failed_reason: Optional[str] = None) -> Optional[Job]:
    db_job = get_job_by_id(db, job_id)
    if db_job:
        db_job.status = status
        if status == "RUNNING" and not db_job.started_at:
            db_job.started_at = datetime.utcnow()
        elif status in ("COMPLETED", "FAILED", "CANCELLED"):
            db_job.completed_at = datetime.utcnow()
            if failed_reason:
                db_job.failed_reason = failed_reason
        db.commit()
        db.refresh(db_job)
    return db_job

def update_job_progress(db: Session, job_id: str, progress: int) -> Optional[Job]:
    db_job = get_job_by_id(db, job_id)
    if db_job:
        db_job.progress_percent = progress
        db.commit()
        db.refresh(db_job)
    return db_job

def get_job_steps(db: Session, job_id: str) -> List[JobStep]:
    return db.query(JobStep).filter(JobStep.job_id == job_id).order_by(JobStep.step_order).all()

def update_step_status(db: Session, job_id: str, step_name: str, status: str, error_message: Optional[str] = None, log_path: Optional[str] = None, output_path: Optional[str] = None) -> Optional[JobStep]:
    db_step = db.query(JobStep).filter(JobStep.job_id == job_id, JobStep.step_name == step_name).first()
    if db_step:
        db_step.status = status
        if status == "RUNNING":
            db_step.start_time = datetime.utcnow()
        elif status in ("COMPLETED", "FAILED"):
            db_step.end_time = datetime.utcnow()
            if error_message:
                db_step.error_message = error_message
            if log_path:
                db_step.log_path = log_path
            if output_path:
                db_step.output_path = output_path
        db.commit()
        db.refresh(db_step)
    return db_step

# =============================================================================
# FILE UPLOAD REPOSITORY
# =============================================================================

def register_uploaded_file(db: Session, original_name: str, file_type: str, file_size: int, storage_path: str, job_id: Optional[str] = None) -> UploadedFile:
    db_file = UploadedFile(
        job_id=job_id,
        original_name=original_name,
        file_type=file_type,
        file_size=file_size,
        storage_path=storage_path
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

# =============================================================================
# WORKFLOW RUN SUMMARIES REPOSITORY
# =============================================================================

def save_fasta_run(db: Session, job_id: str, genome_length: int, gc_content: float, ambiguity_count: int, total_orfs: int, translated_proteins: int) -> FastaRun:
    db_run = FastaRun(
        job_id=job_id,
        genome_length=genome_length,
        gc_content=gc_content,
        ambiguity_count=ambiguity_count,
        total_orfs=total_orfs,
        translated_proteins=translated_proteins
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

def save_fastq_run(db: Session, job_id: str, raw_reads: int, filtered_reads: int, average_quality: float, assembly_contigs: Optional[int] = None) -> FastqRun:
    db_run = FastqRun(
        job_id=job_id,
        raw_reads=raw_reads,
        filtered_reads=filtered_reads,
        average_quality=average_quality,
        assembly_contigs=assembly_contigs
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

def save_deg_run(db: Session, job_id: str, total_genes: int, significant_genes: int, upregulated: int, downregulated: int) -> DegRun:
    db_run = DegRun(
        job_id=job_id,
        total_genes=total_genes,
        significant_genes=significant_genes,
        upregulated=upregulated,
        downregulated=downregulated
    )
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    return db_run

# =============================================================================
# BIOLOGICAL ANNOTATION HITS REPOSITORY
# =============================================================================

def save_annotations(db: Session, job_id: str, hits: List[Dict[str, Any]]) -> List[AnnotationResult]:
    db_hits = []
    for hit in hits:
        db_hit = AnnotationResult(
            job_id=job_id,
            query_protein=hit["query_protein"],
            subject_protein=hit["subject_protein"],
            identity_percent=hit["identity_percent"],
            coverage_percent=hit["coverage_percent"],
            evalue=hit["evalue"],
            bitscore=hit["bitscore"],
            annotation=hit["annotation"]
        )
        db.add(db_hit)
        db_hits.append(db_hit)
    db.commit()
    return db_hits

def save_pfam_domains(db: Session, job_id: str, domains: List[Dict[str, Any]]) -> List[PfamDomain]:
    db_domains = []
    for dom in domains:
        db_dom = PfamDomain(
            job_id=job_id,
            protein_id=dom["protein_id"],
            pfam_accession=dom["pfam_accession"],
            pfam_name=dom["pfam_name"],
            domain_start=dom["domain_start"],
            domain_end=dom["domain_end"],
            evalue=dom["evalue"]
        )
        db.add(db_dom)
        db_domains.append(db_dom)
    db.commit()
    return db_domains

def save_taxonomy_result(db: Session, job_id: str, tax_id: int, organism_name: str, lineage: List[str], rank: str) -> TaxonomyResult:
    db_tax = TaxonomyResult(
        job_id=job_id,
        tax_id=tax_id,
        organism_name=organism_name,
        lineage=lineage,
        rank=rank
    )
    db.add(db_tax)
    db.commit()
    db.refresh(db_tax)
    return db_tax

def save_kegg_results(db: Session, job_id: str, pathways: List[Dict[str, Any]]) -> List[KeggPathwayResult]:
    db_pathways = []
    for path in pathways:
        db_path = KeggPathwayResult(
            job_id=job_id,
            pathway_id=path["pathway_id"],
            pathway_name=path["pathway_name"],
            gene_count=path["gene_count"],
            pvalue=path["pvalue"],
            fdr=path["fdr"]
        )
        db.add(db_path)
        db_pathways.append(db_path)
    db.commit()
    return db_pathways

# =============================================================================
# PUBMED EVIDENCE REPOSITORY
# =============================================================================

def get_cached_pubmed_query(db: Session, query_text: str) -> Optional[PubMedQuery]:
    return db.query(PubMedQuery).filter(PubMedQuery.query_text == query_text).first()

def cache_pubmed_query(db: Session, job_id: str, query_text: str, query_type: str, articles: List[Dict[str, Any]]) -> PubMedQuery:
    # 1. Create search query node
    db_query = PubMedQuery(job_id=job_id, query_text=query_text, query_type=query_type)
    db.add(db_query)
    db.commit()
    db.refresh(db_query)

    # 2. Add individual article leaves
    for art in articles:
        # Check if PMID already exists in DB to prevent unique constraint failures
        existing = db.query(PubMedArticle).filter(PubMedArticle.pmid == art["pmid"]).first()
        if existing:
            # Re-link existing or continue
            continue
        
        db_art = PubMedArticle(
            query_id=db_query.id,
            pmid=art["pmid"],
            title=art["title"],
            journal=art["journal"],
            publication_year=art["publication_year"],
            authors=art["authors"],
            doi=art.get("doi"),
            abstract=art["abstract"],
            relevance_score=art["relevance_score"]
        )
        db.add(db_art)
    db.commit()
    return db_query

# =============================================================================
# AI INTERPRETATION REPOSITORY
# =============================================================================

def save_ai_interpretation(db: Session, job_id: str, ai_provider: str, model_name: str, findings: str, literature_summary: str, biological_interpretation: str, confidence_assessment: str, limitations: str) -> AIInterpretation:
    db_ai = AIInterpretation(
        job_id=job_id,
        ai_provider=ai_provider,
        model_name=model_name,
        findings=findings,
        literature_summary=literature_summary,
        biological_interpretation=biological_interpretation,
        confidence_assessment=confidence_assessment,
        limitations=limitations
    )
    db.add(db_ai)
    db.commit()
    db.refresh(db_ai)
    return db_ai

# =============================================================================
# REPORTS REPOSITORY
# =============================================================================

def save_report(db: Session, job_id: str, report_type: str, report_path: str) -> ReportResult:
    db_rep = ReportResult(job_id=job_id, report_type=report_type, report_path=report_path)
    db.add(db_rep)
    db.commit()
    db.refresh(db_rep)
    return db_rep
