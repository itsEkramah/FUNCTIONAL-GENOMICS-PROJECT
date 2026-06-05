import os
from datetime import datetime
from typing import List, Callable, Optional, Any

from backend.database import SessionLocal
from backend.models.job import Job, JobStep
from backend.config.constants import *
from backend.config.settings import settings
from backend.utils.logger import get_logger, get_job_logger

# Initialize root logger
root_logger = get_logger(__name__)

# Initialize Redis client with failover protection
redis_client = None
try:
    import redis
    redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
except Exception as e:
    root_logger.warning(f"Redis is not available: {str(e)}. Falling back to pure SQL database status tracking.")

class PipelineStep:
    """
    Represents an atomic step in a bioinformatics workflow.
    """
    def __init__(self, name: str, order: int, run_func: Callable[[str, Any], Any], validate_func: Callable[[str, Any, Any], bool]):
        self.name = name
        self.order = order
        self.run_func = run_func  # Takes (job_dir, job_logger)
        self.validate_func = validate_func  # Takes (job_dir, step_output, job_logger)

class PipelineRunner:
    """
    Orchestrates the sequential execution, validation, and status tracking of workflows.
    """
    def __init__(self):
        self.redis = redis_client

    def create_job(self, job_name: str, workflow_type: str, user_id: Optional[str] = None) -> str:
        """
        Creates a new Job record in the database, setting state to QUEUED.
        """
        with SessionLocal() as db:
            job = Job(
                job_name=job_name,
                workflow_type=workflow_type,
                status=STATUS_QUEUED,
                progress_percent=0,
                user_id=user_id,
                created_at=datetime.utcnow()
            )
            db.add(job)
            db.commit()
            db.refresh(job)
            job_id = job.id
        
        self._update_redis_status(job_id, STATUS_QUEUED, 0)
        root_logger.info(f"Initialized job {job_id} ('{job_name}') with state QUEUED.")
        return job_id

    def register_steps(self, job_id: str, steps: List[PipelineStep]):
        """
        Registers the sequence of pipeline steps in the database.
        Clears pre-existing placeholder steps first to prevent duplication.
        """
        with SessionLocal() as db:
            db.query(JobStep).filter(JobStep.job_id == job_id).delete()
            db.commit()
            
            for step in steps:
                db_step = JobStep(
                    job_id=job_id,
                    step_name=step.name,
                    step_order=step.order,
                    status=STEP_PENDING
                )
                db.add(db_step)
            db.commit()
        root_logger.info(f"Registered {len(steps)} pipeline steps for job {job_id}.")

    def run_job(self, job_id: str, steps: List[PipelineStep]):
        """
        Executes registered workflow steps in sequence.
        Enforces validation gates at each step. Aborts immediately on failure.
        """
        job_dir = os.path.join(JOBS_DIR, job_id)
        os.makedirs(job_dir, exist_ok=True)
        job_logger = get_job_logger(job_id, job_dir)

        job_logger.info(f"Starting pipeline execution for Job: {job_id}")

        # 1. Update Job Status to RUNNING
        with SessionLocal() as db:
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                job_logger.error(f"Job {job_id} not found in database. Aborting pipeline.")
                return
            job.status = STATUS_RUNNING
            job.started_at = datetime.utcnow()
            job.progress_percent = 0
            db.commit()

        self._update_redis_status(job_id, STATUS_RUNNING, 0)

        total_steps = len(steps)
        completed_count = 0

        # Sort steps by step_order to maintain correct sequence
        sorted_steps = sorted(steps, key=lambda s: s.order)

        # 2. Sequential Execution Loop
        for step in sorted_steps:
            job_logger.info(f"--- Executing Step {step.order}/{total_steps}: {step.name} ---")

            # Check for cancellation before executing step
            if self._is_cancelled(job_id):
                job_logger.warning("Pipeline run cancelled by user. Terminating execution.")
                self._terminate_job(job_id, STATUS_CANCELLED, "Cancelled by user", job_logger)
                return

            # Update step status to RUNNING in database
            step_id = None
            with SessionLocal() as db:
                db_step = db.query(JobStep).filter(
                    JobStep.job_id == job_id, 
                    JobStep.step_name == step.name
                ).first()
                if db_step:
                    db_step.status = STEP_RUNNING
                    db_step.start_time = datetime.utcnow()
                    db.commit()
                    step_id = db_step.id

            # Execute Step logic (Session remains closed during subprocess runs)
            step_output = None
            try:
                step_output = step.run_func(job_dir, job_logger)
            except Exception as run_error:
                job_logger.exception(f"Execution failed in step {step.name}: {str(run_error)}")
                self._fail_step(job_id, step.name, step_id, f"Execution error: {str(run_error)}", job_logger)
                return

            # Checkpoint Validation Gate
            job_logger.info(f"Validating output checkpoint for step: {step.name}")
            try:
                is_valid = step.validate_func(job_dir, step_output, job_logger)
                if not is_valid:
                    job_logger.error(f"Validation failed for step {step.name}. Checkpoint output missing or empty.")
                    self._fail_step(job_id, step.name, step_id, "Validation failed: output checkpoint missing or empty", job_logger)
                    return
            except Exception as val_error:
                job_logger.exception(f"Validation checkpoint threw an error in step {step.name}: {str(val_error)}")
                self._fail_step(job_id, step.name, step_id, f"Validation checkpoint error: {str(val_error)}", job_logger)
                return

            # Step Completed Successfully
            completed_count += 1
            progress = int((completed_count / total_steps) * 100)
            
            with SessionLocal() as db:
                db_step = db.query(JobStep).filter(JobStep.id == step_id).first()
                if db_step:
                    db_step.status = STEP_COMPLETED
                    db_step.end_time = datetime.utcnow()
                
                db_job = db.query(Job).filter(Job.id == job_id).first()
                if db_job:
                    db_job.progress_percent = progress
                db.commit()

            self._update_redis_status(job_id, STATUS_RUNNING, progress)
            job_logger.info(f"Step {step.name} completed successfully. Current progress: {progress}%")

        # 3. Finalize Job on Success
        job_logger.info("All pipeline steps executed and validated successfully. Finalizing job status.")
        with SessionLocal() as db:
            db_job = db.query(Job).filter(Job.id == job_id).first()
            if db_job:
                db_job.status = STATUS_COMPLETED
                db_job.completed_at = datetime.utcnow()
                db_job.progress_percent = 100
            db.commit()

        self._update_redis_status(job_id, STATUS_COMPLETED, 100)
        job_logger.info(f"Job {job_id} execution finished successfully.")

    def _is_cancelled(self, job_id: str) -> bool:
        """
        Queries status from Redis and PostgreSQL to detect cancellation events.
        """
        if self.redis:
            try:
                val = self.redis.get(f"job_status:{job_id}")
                if val == STATUS_CANCELLED:
                    return True
            except Exception:
                pass
        with SessionLocal() as db:
            job = db.query(Job).filter(Job.id == job_id).first()
            if job and job.status == STATUS_CANCELLED:
                return True
        return False

    def _update_redis_status(self, job_id: str, status: str, progress: int):
        """
        Sets status keys in Redis and publishes event to SSE listeners.
        """
        if self.redis:
            try:
                self.redis.set(f"job_status:{job_id}", status, ex=86400)
                self.redis.set(f"job_progress:{job_id}", str(progress), ex=86400)
                self.redis.publish(f"job_updates:{job_id}", f"{status}:{progress}")
            except Exception as e:
                root_logger.warning(f"Failed to sync state to Redis cache: {str(e)}. Disabling Redis client for this runner.")
                self.redis = None

    def _fail_step(self, job_id: str, step_name: str, step_id: Optional[str], error_msg: str, job_logger):
        """
        Updates step and job tables to FAILED, writes log trace, and aborts runner.
        """
        with SessionLocal() as db:
            if step_id:
                db_step = db.query(JobStep).filter(JobStep.id == step_id).first()
                if db_step:
                    db_step.status = STEP_FAILED
                    db_step.end_time = datetime.utcnow()
                    db_step.error_message = error_msg
            
            db_job = db.query(Job).filter(Job.id == job_id).first()
            if db_job:
                db_job.status = STATUS_FAILED
                db_job.failed_reason = f"Step {step_name} failed: {error_msg}"
                db_job.completed_at = datetime.utcnow()
            db.commit()

        self._update_redis_status(job_id, STATUS_FAILED, 0)
        job_logger.error(f"Job {job_id} terminated due to step failure: {step_name}.")

    def _terminate_job(self, job_id: str, status: str, reason: str, job_logger):
        """
        Handles job termination in case of user cancellation.
        """
        with SessionLocal() as db:
            db_job = db.query(Job).filter(Job.id == job_id).first()
            if db_job:
                db_job.status = status
                db_job.failed_reason = reason
                db_job.completed_at = datetime.utcnow()
            db.commit()
        self._update_redis_status(job_id, status, 0)
        job_logger.warning(f"Job {job_id} execution terminated with state {status}.")
