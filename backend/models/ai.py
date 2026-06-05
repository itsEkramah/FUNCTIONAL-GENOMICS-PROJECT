import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.models.base import Base

class AIInterpretation(Base):
    __tablename__ = "ai_interpretations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, unique=True)
    ai_provider = Column(String(20), nullable=False)  # 'gemini', 'openai', 'offline'
    model_name = Column(String(50), nullable=False)
    findings = Column(String, nullable=False)
    literature_summary = Column(String, nullable=False)
    biological_interpretation = Column(String, nullable=False)
    confidence_assessment = Column(String(20), nullable=False)  # 'HIGH', 'MEDIUM', 'LOW'
    limitations = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    job = relationship("Job", back_populates="ai_interpretation")
