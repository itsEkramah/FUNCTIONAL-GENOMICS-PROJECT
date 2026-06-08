import os
import json
import asyncio
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from backend.database import get_db
from backend.models.job import Job, JobStep
from backend.pipeline.workflow_fasta import run_fasta_workflow
from backend.pipeline.workflow_fastq import run_fastq_workflow
from backend.pipeline.workflow_deg import run_deg_workflow
from backend.core.deg_engine import (
    DEFAULT_FDR_THRESHOLD,
    DEFAULT_LFC_THRESHOLD,
    DEFAULT_MIN_CPM,
    DEFAULT_MIN_SAMPLE_FRAC
)
from backend.config.constants import PROJECT_ROOT

router = APIRouter()

# Global set to track currently running job IDs and prevent concurrent duplication
RUNNING_JOBS = set()

class DegThresholds(BaseModel):
    fdr_threshold: float = DEFAULT_FDR_THRESHOLD
    lfc_threshold: float = DEFAULT_LFC_THRESHOLD
    min_cpm: float = DEFAULT_MIN_CPM
    min_sample_frac: float = DEFAULT_MIN_SAMPLE_FRAC

def execute_pipeline(job_id: str, workflow_type: str, file_path: str):
    try:
        if workflow_type == "FASTA":
            run_fasta_workflow(job_id, file_path)
        elif workflow_type == "FASTQ":
            run_fastq_workflow(job_id, file_path)
        elif workflow_type == "DEG":
            run_deg_workflow(job_id, file_path)
    except Exception as e:
        print(f"Exception running workflow {workflow_type} for job {job_id}: {str(e)}")
    finally:
        RUNNING_JOBS.discard(job_id)

@router.get("/jobs/{job_id}/thresholds")
async def get_deg_thresholds(job_id: str):
    """Returns the current DEG analysis thresholds for a job (defaults if not set)."""
    job_dir = os.path.join(PROJECT_ROOT, "storage", "jobs", job_id)
    thresholds_path = os.path.join(job_dir, "thresholds.json")
    if os.path.exists(thresholds_path):
        try:
            with open(thresholds_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    # Return defaults
    return {
        "fdr_threshold": DEFAULT_FDR_THRESHOLD,
        "lfc_threshold": DEFAULT_LFC_THRESHOLD,
        "min_cpm": DEFAULT_MIN_CPM,
        "min_sample_frac": DEFAULT_MIN_SAMPLE_FRAC
    }

@router.post("/jobs/{job_id}/thresholds")
async def set_deg_thresholds(job_id: str, thresholds: DegThresholds, db: Session = Depends(get_db)):
    """
    Sets DEG analysis thresholds for a specific job.
    These are saved to thresholds.json and used by the pipeline at Step 3 (Statistical Analysis).
    Only applicable for DEG workflow jobs that have not yet completed Step 3.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.workflow_type != "DEG":
        raise HTTPException(status_code=400, detail="Thresholds only apply to DEG workflow jobs.")

    # Validate ranges
    if not (0 < thresholds.fdr_threshold <= 1.0):
        raise HTTPException(status_code=422, detail="fdr_threshold must be in range (0, 1]")
    if thresholds.lfc_threshold < 0:
        raise HTTPException(status_code=422, detail="lfc_threshold must be >= 0")
    if thresholds.min_cpm < 0:
        raise HTTPException(status_code=422, detail="min_cpm must be >= 0")
    if not (0 <= thresholds.min_sample_frac <= 1.0):
        raise HTTPException(status_code=422, detail="min_sample_frac must be in range [0, 1]")

    job_dir = os.path.join(PROJECT_ROOT, "storage", "jobs", job_id)
    os.makedirs(job_dir, exist_ok=True)
    thresholds_path = os.path.join(job_dir, "thresholds.json")

    data = {
        "fdr_threshold": thresholds.fdr_threshold,
        "lfc_threshold": thresholds.lfc_threshold,
        "min_cpm": thresholds.min_cpm,
        "min_sample_frac": thresholds.min_sample_frac
    }
    with open(thresholds_path, "w") as f:
        json.dump(data, f, indent=4)

    return {"status": "saved", "thresholds": data}

@router.post("/jobs/{job_id}/start")
async def start_job(job_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Guard against starting an already active/finished job or concurrently running duplicate
    if job.status in ("RUNNING", "COMPLETED", "FAILED") or job_id in RUNNING_JOBS:
        return {"status": job.status}
        
    if not job.uploaded_file:
        raise HTTPException(status_code=400, detail="No uploaded file associated with this job")
        
    file_path = job.uploaded_file.storage_path
    
    # Lock the job ID in the running set
    RUNNING_JOBS.add(job_id)
    
    # Set status to RUNNING
    job.status = "RUNNING"
    job.started_at = datetime.utcnow()
    db.commit()
    
    background_tasks.add_task(execute_pipeline, job.id, job.workflow_type, file_path)
    return {"status": "RUNNING"}


@router.post("/jobs/{job_id}/restart")
async def restart_job(job_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Resets a DEG job's status to QUEUED and clears all prior pipeline results
    (DegRun, reports, steps, enrichments, PubMed, AI interpretation) so that the
    pipeline can be re-run cleanly with new threshold parameters.
    This powers the 'Apply Thresholds & Re-run' button in the frontend.
    """
    from backend.models.results import DegRun, ReportResult
    from backend.models.pubmed import PubMedQuery
    from backend.models.ai import AIInterpretation
    from backend.models.annotation import KeggPathwayResult, TaxonomyResult, AnnotationResult, PfamDomain

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.workflow_type != "DEG":
        raise HTTPException(status_code=400, detail="Restart only supported for DEG workflow jobs.")
    if job_id in RUNNING_JOBS or job.status == "RUNNING":
        raise HTTPException(status_code=409, detail="Job is already running. Cancel it first.")

    if not job.uploaded_file:
        raise HTTPException(status_code=400, detail="No uploaded file associated with this job.")

    # ── Cascade-delete all prior pipeline outputs ──────────────────────────────
    db.query(DegRun).filter(DegRun.job_id == job_id).delete(synchronize_session=False)
    db.query(ReportResult).filter(ReportResult.job_id == job_id).delete(synchronize_session=False)
    db.query(JobStep).filter(JobStep.job_id == job_id).delete(synchronize_session=False)
    db.query(KeggPathwayResult).filter(KeggPathwayResult.job_id == job_id).delete(synchronize_session=False)
    db.query(TaxonomyResult).filter(TaxonomyResult.job_id == job_id).delete(synchronize_session=False)
    db.query(AnnotationResult).filter(AnnotationResult.job_id == job_id).delete(synchronize_session=False)
    db.query(PfamDomain).filter(PfamDomain.job_id == job_id).delete(synchronize_session=False)
    db.query(PubMedQuery).filter(PubMedQuery.job_id == job_id).delete(synchronize_session=False)
    db.query(AIInterpretation).filter(AIInterpretation.job_id == job_id).delete(synchronize_session=False)
    # ───────────────────────────────────────────────────────────────────────────

    # Reset the job to a fresh QUEUED state
    job.status = "QUEUED"
    job.progress_percent = 0
    job.started_at = None
    job.completed_at = None
    job.failed_reason = None
    db.commit()

    # Trigger fresh pipeline run
    file_path = job.uploaded_file.storage_path
    RUNNING_JOBS.add(job_id)
    background_tasks.add_task(execute_pipeline, job_id, job.workflow_type, file_path)
    return {"status": "RUNNING", "message": "Job reset and restarted with new thresholds."}

@router.post("/jobs/{job_id}/cancel")
async def cancel_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.status = "CANCELLED"
    job.completed_at = datetime.utcnow()
    db.commit()
    return {"status": "CANCELLED"}

@router.get("/jobs/{job_id}/status")
async def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "id": job.id,
        "job_name": job.job_name,
        "workflow_type": job.workflow_type,
        "status": job.status,
        "progress_percent": job.progress_percent,
        "failed_reason": job.failed_reason,
        "created_at": job.created_at.isoformat() + "Z" if job.created_at else None,
        "steps": [
            {
                "step_name": s.step_name,
                "step_order": s.step_order,
                "status": s.status,
                "error_message": s.error_message
            }
            for s in sorted(job.steps, key=lambda s: s.step_order)
        ]
    }

@router.get("/jobs/{job_id}/results")
async def get_job_results(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    res = {
        "job_id": job.id,
        "workflow_type": job.workflow_type,
    }
    
    # Load ORFs from disk if present
    from backend.config.constants import PROJECT_ROOT
    import json
    orfs_path = os.path.join(PROJECT_ROOT, "storage", "jobs", job_id, "orfs.json")
    if os.path.exists(orfs_path):
        try:
            with open(orfs_path, "r", encoding="utf-8") as f:
                res["orfs"] = json.load(f)
        except Exception:
            res["orfs"] = []
    else:
        res["orfs"] = []
    
    if job.fasta_run:
        res["fasta_run"] = {
            "genome_length": job.fasta_run.genome_length,
            "gc_content": job.fasta_run.gc_content,
            "ambiguity_count": job.fasta_run.ambiguity_count,
            "total_orfs": job.fasta_run.total_orfs,
            "translated_proteins": job.fasta_run.translated_proteins
        }
    if job.fastq_run:
        res["fastq_run"] = {
            "raw_reads": job.fastq_run.raw_reads,
            "filtered_reads": job.fastq_run.filtered_reads,
            "average_quality": job.fastq_run.average_quality,
            "assembly_contigs": job.fastq_run.assembly_contigs
        }
    if job.deg_run:
        res["deg_run"] = {
            "total_genes": job.deg_run.total_genes,
            "significant_genes": job.deg_run.significant_genes,
            "upregulated": job.deg_run.upregulated,
            "downregulated": job.deg_run.downregulated
        }
        
    if job.annotations:
        res["annotations"] = [
            {
                "query_protein": a.query_protein,
                "subject_protein": a.subject_protein,
                "identity_percent": a.identity_percent,
                "coverage_percent": a.coverage_percent,
                "evalue": a.evalue,
                "bitscore": a.bitscore,
                "annotation": a.annotation
            }
            for a in job.annotations
        ]
        
    if job.pfam_domains:
        res["pfam_domains"] = [
            {
                "protein_id": d.protein_id,
                "pfam_accession": d.pfam_accession,
                "pfam_name": d.pfam_name,
                "domain_start": d.domain_start,
                "domain_end": d.domain_end,
                "evalue": d.evalue
            }
            for d in job.pfam_domains
        ]
        
    if job.kegg_results:
        from backend.services.kegg_service import LOCAL_PATHWAY_DB
        kegg_list = []
        for k in job.kegg_results:
            p_id = k.pathway_id.strip()
            url = ""
            if p_id in LOCAL_PATHWAY_DB:
                url = LOCAL_PATHWAY_DB[p_id]["url"]
            elif "hsa" in p_id or "map" in p_id:
                url = f"https://www.genome.jp/dbget-bin/www_bget?pathway+{p_id}"
            elif p_id.startswith("R-HSA-") or "REACTOME" in p_id.upper():
                url = f"https://reactome.org/content/detail/{p_id}"
            else:
                url = f"https://www.genome.jp/dbget-bin/www_bget?pathway+{p_id}"
                
            kegg_list.append({
                "pathway_id": k.pathway_id,
                "pathway_name": k.pathway_name,
                "gene_count": k.gene_count,
                "pvalue": k.pvalue,
                "fdr": k.fdr,
                "url": url
            })
        res["kegg_results"] = kegg_list
        
    if job.taxonomy_results:
        t = job.taxonomy_results[0]
        res["taxonomy_results"] = {
            "tax_id": t.tax_id,
            "organism_name": t.organism_name,
            "rank": t.rank,
            "lineage": t.lineage
        }
        
    if job.pubmed_queries:
        articles = []
        seen_pmids = set()
        for q in job.pubmed_queries:
            for a in q.articles:
                if a.pmid not in seen_pmids:
                    seen_pmids.add(a.pmid)
                    articles.append({
                        "pmid": a.pmid,
                        "title": a.title,
                        "journal": a.journal,
                        "publication_year": a.publication_year,
                        "authors": a.authors if a.authors else [],
                        "doi": a.doi,
                        "abstract": a.abstract,
                        "publication_type": a.publication_type if a.publication_type else "Journal Article",
                        "mesh_terms": a.mesh_terms if a.mesh_terms else []
                    })
        res["pubmed"] = articles
    
    # Fallback: load PubMed from JSON file if DB has no results
    if "pubmed" not in res or not res.get("pubmed"):
        import json as _json
        from backend.config.constants import PROJECT_ROOT
        job_dir = os.path.join(PROJECT_ROOT, "storage", "jobs", job_id)
        for fname in ["pubmed_articles.json", "pubmed_evidence.json"]:
            pubmed_json = os.path.join(job_dir, fname)
            if os.path.exists(pubmed_json):
                try:
                    with open(pubmed_json, "r", encoding="utf-8") as f:
                        file_articles = _json.load(f)
                    if file_articles and isinstance(file_articles, list):
                        res["pubmed"] = file_articles
                        break
                except Exception:
                    pass
        
    if job.ai_interpretation:
        res["ai_interpretation"] = {
            "ai_provider": job.ai_interpretation.ai_provider,
            "model_name": job.ai_interpretation.model_name,
            "findings": job.ai_interpretation.findings,
            "literature_summary": job.ai_interpretation.literature_summary,
            "biological_interpretation": job.ai_interpretation.biological_interpretation,
            "confidence_assessment": job.ai_interpretation.confidence_assessment,
            "limitations": job.ai_interpretation.limitations
        }
        
    from backend.config.constants import PROJECT_ROOT
    import json
    
    def make_web_path(absolute_path: str) -> str:
        if not absolute_path:
            return ""
        abs_norm = os.path.normpath(absolute_path).replace("\\", "/")
        root_norm = os.path.normpath(PROJECT_ROOT).replace("\\", "/")
        if abs_norm.startswith(root_norm):
            rel = abs_norm[len(root_norm):]
            if not rel.startswith("/"):
                rel = "/" + rel
            return rel
        return absolute_path

    if job.reports:
        res["reports"] = [
            {
                "report_type": r.report_type,
                "report_path": make_web_path(r.report_path)
            }
            for r in job.reports
        ]
        
    manifest_path = os.path.join(PROJECT_ROOT, "storage", "jobs", job_id, "visualization_manifest.json")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                rel_paths = json.load(f)
                res["visualizations"] = [f"/storage/jobs/{job_id}/{p}" for p in rel_paths]
        except Exception:
            res["visualizations"] = []
    else:
        vis_dir = os.path.join(PROJECT_ROOT, "storage", "jobs", job_id, "visualizations")
        if os.path.exists(vis_dir):
            try:
                res["visualizations"] = [f"/storage/jobs/{job_id}/visualizations/{f}" for f in os.listdir(vis_dir) if f.endswith(".png")]
            except Exception:
                res["visualizations"] = []
        else:
            res["visualizations"] = []
            
    return res

@router.get("/jobs/{job_id}/stream")
async def stream_job_updates(job_id: str, db: Session = Depends(get_db)):
    async def event_generator():
        log_path = os.path.join("storage", "jobs", job_id, "logs", "pipeline.log")
        
        last_progress = -1
        last_status = None
        last_step_states = {}
        file_position = 0
        
        while True:
            db.expire_all()
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                break
                
            if os.path.exists(log_path):
                try:
                    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                        f.seek(file_position)
                        new_lines = f.readlines()
                        file_position = f.tell()
                        
                        for line in new_lines:
                            line = line.strip()
                            if line:
                                yield f"data: {line}\n\n"
                except Exception:
                    pass
                    
            if job.progress_percent != last_progress:
                last_progress = job.progress_percent
                yield f"event: progress\ndata: {{\"percent\": {job.progress_percent}}}\n\n"
                
            for step in job.steps:
                if last_step_states.get(step.step_name) != step.status:
                    last_step_states[step.step_name] = step.status
                    yield f"event: step_change\ndata: {{\"step_name\": \"{step.step_name}\", \"status\": \"{step.status}\"}}\n\n"
                    
            if job.status != last_status:
                last_status = job.status
                yield f"event: job_status\ndata: {{\"status\": \"{job.status}\"}}\n\n"
                
            if job.status in ("COMPLETED", "FAILED", "CANCELLED"):
                if os.path.exists(log_path):
                    try:
                        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                            f.seek(file_position)
                            new_lines = f.readlines()
                            for line in new_lines:
                                line = line.strip()
                                if line:
                                    yield f"data: {line}\n\n"
                    except Exception:
                        pass
                break
                
            await asyncio.sleep(0.5)
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/jobs")
async def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    return [
        {
            "id": j.id,
            "job_name": j.job_name,
            "workflow_type": j.workflow_type,
            "status": j.status,
            "progress_percent": j.progress_percent,
            "created_at": j.created_at.isoformat() + "Z" if j.created_at else None
        }
        for j in jobs
    ]
