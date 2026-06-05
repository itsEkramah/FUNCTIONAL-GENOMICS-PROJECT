import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.job import Job

router = APIRouter()

@router.get("/reports/{job_id}/{report_type}")
async def get_report_file(job_id: str, report_type: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    report_type_upper = report_type.upper()
    for r in job.reports:
        if r.report_type == report_type_upper:
            if os.path.exists(r.report_path):
                media_type = "application/octet-stream"
                if report_type_upper == "HTML":
                    media_type = "text/html"
                elif report_type_upper == "PDF":
                    media_type = "application/pdf"
                elif report_type_upper == "JSON":
                    media_type = "application/json"
                elif report_type_upper == "CSV":
                    media_type = "text/csv"
                
                return FileResponse(r.report_path, media_type=media_type, filename=os.path.basename(r.report_path))
                
    raise HTTPException(status_code=404, detail=f"{report_type_upper} report file not found")
