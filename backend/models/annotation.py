import uuid
from sqlalchemy import Column, String, Integer, Double, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.models.base import Base

class AnnotationResult(Base):
    __tablename__ = "annotations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    query_protein = Column(String, nullable=False)
    subject_protein = Column(String, nullable=False)
    identity_percent = Column(Double, nullable=False)
    coverage_percent = Column(Double, nullable=False)
    evalue = Column(Double, nullable=False)
    bitscore = Column(Double, nullable=False)
    annotation = Column(String, nullable=False)

    job = relationship("Job", back_populates="annotations")

class PfamDomain(Base):
    __tablename__ = "pfam_domains"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    protein_id = Column(String, nullable=False)
    pfam_accession = Column(String(50), nullable=False)
    pfam_name = Column(String, nullable=False)
    domain_start = Column(Integer, nullable=False)
    domain_end = Column(Integer, nullable=False)
    evalue = Column(Double, nullable=False)

    job = relationship("Job", back_populates="pfam_domains")

class TaxonomyResult(Base):
    __tablename__ = "taxonomy_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    tax_id = Column(Integer, nullable=False)
    organism_name = Column(String, nullable=False)
    lineage = Column(JSON, nullable=False)  # JSON list
    rank = Column(String(50), nullable=False)

    job = relationship("Job", back_populates="taxonomy_results")

class KeggPathwayResult(Base):
    __tablename__ = "kegg_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    pathway_id = Column(String(50), nullable=False)
    pathway_name = Column(String, nullable=False)
    gene_count = Column(Integer, nullable=False)
    pvalue = Column(Double, nullable=False)
    fdr = Column(Double, nullable=False)

    job = relationship("Job", back_populates="kegg_results")
