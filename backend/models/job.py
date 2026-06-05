import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.models.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_name = Column(String, nullable=False)
    workflow_type = Column(String, nullable=False)  # 'FASTA', 'FASTQ', 'DEG'
    status = Column(String, nullable=False, default="QUEUED")  # 'QUEUED', 'RUNNING', 'FAILED', 'COMPLETED', 'CANCELLED'
    progress_percent = Column(Integer, nullable=False, default=0)
    user_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    failed_reason = Column(String, nullable=True)

    user = relationship("User", back_populates="jobs")
    steps = relationship("JobStep", back_populates="job", cascade="all, delete-orphan")
    uploaded_file = relationship("UploadedFile", uselist=False, back_populates="job")
    fasta_run = relationship("FastaRun", uselist=False, back_populates="job", cascade="all, delete-orphan")
    fastq_run = relationship("FastqRun", uselist=False, back_populates="job", cascade="all, delete-orphan")
    deg_run = relationship("DegRun", uselist=False, back_populates="job", cascade="all, delete-orphan")
    annotations = relationship("AnnotationResult", back_populates="job", cascade="all, delete-orphan")
    pfam_domains = relationship("PfamDomain", back_populates="job", cascade="all, delete-orphan")
    taxonomy_results = relationship("TaxonomyResult", back_populates="job", cascade="all, delete-orphan")
    kegg_results = relationship("KeggPathwayResult", back_populates="job", cascade="all, delete-orphan")
    pubmed_queries = relationship("PubMedQuery", back_populates="job", cascade="all, delete-orphan")
    ai_interpretation = relationship("AIInterpretation", uselist=False, back_populates="job", cascade="all, delete-orphan")
    reports = relationship("ReportResult", back_populates="job", cascade="all, delete-orphan")

class JobStep(Base):
    __tablename__ = "job_steps"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    step_name = Column(String, nullable=False)
    step_order = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="PENDING")  # 'PENDING', 'RUNNING', 'FAILED', 'COMPLETED'
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    log_path = Column(String, nullable=True)
    output_path = Column(String, nullable=True)
    error_message = Column(String, nullable=True)

    job = relationship("Job", back_populates="steps")
