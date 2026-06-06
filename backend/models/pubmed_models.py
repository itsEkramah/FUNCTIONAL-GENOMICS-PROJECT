import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Double, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.models.base import Base

class PubMedQuery(Base):
    __tablename__ = "pubmed_queries"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    query_text = Column(String, nullable=False)
    query_type = Column(String(50), nullable=False)  # 'protein', 'pfam', 'taxonomy', 'pathway', 'gene', 'broad', 'clinical', 'mechanistic', 'review'
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    job = relationship("Job", back_populates="pubmed_queries")
    articles = relationship("PubMedArticle", back_populates="query", cascade="all, delete-orphan")

class PubMedArticle(Base):
    __tablename__ = "pubmed_articles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    query_id = Column(String, ForeignKey("pubmed_queries.id", ondelete="CASCADE"), nullable=False)
    pmid = Column(String(50), nullable=False)
    title = Column(String, nullable=False)
    journal = Column(String, nullable=False)
    publication_year = Column(Integer, nullable=False)
    authors = Column(JSON, nullable=False)  # list of dicts: [{"forename": "...", "lastname": "..."}]
    doi = Column(String(100), nullable=True)
    abstract = Column(String, nullable=False)
    relevance_score = Column(Double, nullable=False)
    publication_type = Column(String(150), nullable=True)  # Review, Journal Article, Clinical Trial, etc.
    mesh_terms = Column(JSON, nullable=True)  # list of strings: ["Apoptosis", "Tumor Suppressor Protein p53", etc.]

    query = relationship("PubMedQuery", back_populates="articles")
