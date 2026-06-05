import uuid
from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.models.base import Base

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True, unique=True)
    original_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # 'FASTA', 'FASTQ', 'FASTQ_GZ', 'CSV', 'TSV'
    file_size = Column(BigInteger, nullable=False)
    storage_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    job = relationship("Job", back_populates="uploaded_file")
