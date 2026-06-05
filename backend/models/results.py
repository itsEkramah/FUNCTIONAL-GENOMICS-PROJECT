import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Double, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from backend.models.base import Base

class FastaRun(Base):
    __tablename__ = "fasta_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, unique=True)
    genome_length = Column(Integer, nullable=False)
    gc_content = Column(Double, nullable=False)
    ambiguity_count = Column(Integer, nullable=False, default=0)
    total_orfs = Column(Integer, nullable=False)
    translated_proteins = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    job = relationship("Job", back_populates="fasta_run")

class FastqRun(Base):
    __tablename__ = "fastq_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, unique=True)
    raw_reads = Column(BigInteger, nullable=False)
    filtered_reads = Column(BigInteger, nullable=False)
    average_quality = Column(Double, nullable=False)
    assembly_contigs = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    job = relationship("Job", back_populates="fastq_run")

class DegRun(Base):
    __tablename__ = "deg_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, unique=True)
    total_genes = Column(Integer, nullable=False)
    significant_genes = Column(Integer, nullable=False)
    upregulated = Column(Integer, nullable=False)
    downregulated = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    job = relationship("Job", back_populates="deg_run")

class ReportResult(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    report_type = Column(String, nullable=False)  # 'HTML', 'PDF', 'CSV', 'JSON', 'GFF3'
    report_path = Column(String, nullable=False)
    generated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    job = relationship("Job", back_populates="reports")
