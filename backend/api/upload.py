import os
import shutil
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.utils.file_detector import detect_file_type
from backend.models.job import Job, JobStep
from backend.models.file import UploadedFile

router = APIRouter()

UPLOAD_DIR = os.path.join("storage", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=dict)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Save uploaded file to local storage
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    file_size = os.path.getsize(file_path)
    
    # 2. Auto-detect workflow type
    try:
        detected_type = detect_file_type(file_path)
    except Exception as e:
        # Clean up file on failure
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=str(e))
        
    # 3. Create Job record
    job = Job(
        job_name=f"Run - {file.filename}",
        workflow_type=detected_type,
        status="QUEUED",
        progress_percent=0,
        created_at=datetime.utcnow()
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # 4. Register Uploaded File metadata
    uploaded_file = UploadedFile(
        job_id=job.id,
        original_name=file.filename,
        file_type=detected_type,
        file_size=file_size,
        storage_path=file_path,
        uploaded_at=datetime.utcnow()
    )
    db.add(uploaded_file)
    
    # 5. Register pipeline steps based on workflow type
    if detected_type == "FASTA":
        step_names = [
            "Input Validation", "Sequence QC", "ORF Detection", "Translation",
            "DIAMOND Annotation", "Pfam Annotation", "KEGG Mapping",
            "NCBI Taxonomy", "PubMed Retrieval", "AI Interpretation", "Report Generation"
        ]
    elif detected_type == "FASTQ":
        step_names = [
            "FASTQ Input Validation", "FastQC Raw Read QC", "fastp Quality Trimming", "FastQC Trimmed Read QC",
            "SPAdes De Novo Assembly", "Contig Length Filtering", "FASTA Input Validation", "Sequence QC",
            "ORF Detection", "Translation", "DIAMOND Annotation", "Pfam Annotation", "KEGG Mapping",
            "NCBI Taxonomy", "PubMed Retrieval", "AI Interpretation", "Report Generation"
        ]
    else: # DEG
        step_names = [
            "Input Validation", "Normalization & ID Standardization", "Statistical Classification",
            "GO Enrichment", "KEGG Enrichment", "PubMed Integration",
            "AI Interpretation", "Visualizations Generation", "Report Generation"
        ]
        
    for idx, name in enumerate(step_names, start=1):
        step = JobStep(
            job_id=job.id,
            step_name=name,
            step_order=idx,
            status="PENDING"
        )
        db.add(step)
        
    db.commit()
    db.refresh(job)
    
    return {
        "id": job.id,
        "job_name": job.job_name,
        "workflow_type": job.workflow_type,
        "status": job.status,
        "progress_percent": job.progress_percent,
        "created_at": job.created_at.isoformat() + "Z",
        "steps": [{"step_name": s.step_name, "status": s.status, "step_order": s.step_order} for s in job.steps]
    }
