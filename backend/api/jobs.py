import os
import asyncio
from datetime import datetime
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.job import Job, JobStep
from backend.pipeline.workflow_fasta import run_fasta_workflow
from backend.pipeline.workflow_fastq import run_fastq_workflow
from backend.pipeline.workflow_deg import run_deg_workflow

router = APIRouter()

# Global set to track currently running job IDs and prevent concurrent duplication
RUNNING_JOBS = set()

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
        res["kegg_results"] = [
            {
                "pathway_id": k.pathway_id,
                "pathway_name": k.pathway_name,
                "gene_count": k.gene_count,
                "pvalue": k.pvalue,
                "fdr": k.fdr
            }
            for k in job.kegg_results
        ]
        
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
