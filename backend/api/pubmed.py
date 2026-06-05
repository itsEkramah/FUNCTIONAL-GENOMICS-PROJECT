from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any

from backend.database import get_db
from backend.services.pubmed_service import fetch_pubmed_evidence_package
from backend.models.pubmed_models import PubMedQuery, PubMedArticle

router = APIRouter()

class PubMedSearchRequest(BaseModel):
    biomolecule: str
    biomolecule_type: Optional[str] = "Gene"
    context: Optional[str] = ""
    force_offline: Optional[bool] = False

@router.post("/pubmed/search")
def search_pubmed(req: PubMedSearchRequest):
    """
    Independent search endpoint routing through the NCBI E-utilities service.
    """
    if not req.biomolecule:
        raise HTTPException(status_code=400, detail="Biomolecule parameter is required.")
        
    try:
        package = fetch_pubmed_evidence_package(
            biomolecule=req.biomolecule,
            biomolecule_type=req.biomolecule_type,
            context=req.context,
            force_offline=req.force_offline
        )
        return package
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NCBI query failed: {str(e)}")

@router.get("/pubmed/queries")
def get_cached_queries(db: Session = Depends(get_db)):
    """
    Returns lists of previously searched terms cached in the local database.
    """
    queries = db.query(PubMedQuery).order_by(PubMedQuery.id.desc()).all()
    return [
        {
            "id": q.id,
            "job_id": q.job_id,
            "query_text": q.query_text,
            "query_type": q.query_type,
            "article_count": len(q.articles)
        }
        for q in queries
    ]
