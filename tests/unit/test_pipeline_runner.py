import os
# Configure DATABASE_URL for SQLite before importing backend database modules
os.environ["DATABASE_URL"] = "sqlite:///test_runner.db"

import pytest
from backend.database import SessionLocal, init_db
from backend.models.job import Job, JobStep
from backend.pipeline.pipeline_runner import PipelineRunner, PipelineStep

@pytest.fixture(autouse=True)
def setup_database():
    # Setup test database and initialize tables
    init_db()
    yield
    # Cleanup database file after tests
    if os.path.exists("test_runner.db"):
        try:
            os.remove("test_runner.db")
        except Exception:
            pass

def test_pipeline_runner_success():
    runner = PipelineRunner()
    
    # 1. Create a dummy job
    job_id = runner.create_job(job_name="Success Run", workflow_type="FASTA")
    assert job_id is not None
    
    # Define dummy functions
    outputs = []
    
    def step1_run(job_dir, logger):
        outputs.append("step1_run")
        return "data1"
        
    def step1_val(job_dir, output, logger):
        assert output == "data1"
        return True
        
    def step2_run(job_dir, logger):
        outputs.append("step2_run")
        return "data2"
        
    def step2_val(job_dir, output, logger):
        assert output == "data2"
        return True

    # 2. Register steps
    step1 = PipelineStep(name="Step One", order=1, run_func=step1_run, validate_func=step1_val)
    step2 = PipelineStep(name="Step Two", order=2, run_func=step2_run, validate_func=step2_val)
    steps = [step1, step2]
    
    runner.register_steps(job_id, steps)
    
    # 3. Run pipeline
    runner.run_job(job_id, steps)
    
    # 4. Verify results
    with SessionLocal() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        assert job.status == "COMPLETED"
        assert job.progress_percent == 100
        
        db_steps = db.query(JobStep).filter(JobStep.job_id == job_id).order_by(JobStep.step_order).all()
        assert len(db_steps) == 2
        assert db_steps[0].status == "COMPLETED"
        assert db_steps[1].status == "COMPLETED"
        
    assert outputs == ["step1_run", "step2_run"]

def test_pipeline_runner_validation_failure():
    runner = PipelineRunner()
    job_id = runner.create_job(job_name="Failure Run", workflow_type="FASTA")
    
    outputs = []
    
    def step1_run(job_dir, logger):
        outputs.append("step1_run")
        return "data_ok"
        
    def step1_val(job_dir, output, logger):
        return True
        
    def step2_run(job_dir, logger):
        outputs.append("step2_run")
        return "data_bad"
        
    def step2_val(job_dir, output, logger):
        # Validation fails
        return False
        
    def step3_run(job_dir, logger):
        outputs.append("step3_run")
        return "data3"
        
    def step3_val(job_dir, output, logger):
        return True

    step1 = PipelineStep(name="Step One", order=1, run_func=step1_run, validate_func=step1_val)
    step2 = PipelineStep(name="Step Two", order=2, run_func=step2_run, validate_func=step2_val)
    step3 = PipelineStep(name="Step Three", order=3, run_func=step3_run, validate_func=step3_val)
    steps = [step1, step2, step3]
    
    runner.register_steps(job_id, steps)
    runner.run_job(job_id, steps)
    
    with SessionLocal() as db:
        job = db.query(Job).filter(Job.id == job_id).first()
        assert job.status == "FAILED"
        assert "Step Two failed" in job.failed_reason
        
        db_steps = db.query(JobStep).filter(JobStep.job_id == job_id).order_by(JobStep.step_order).all()
        assert db_steps[0].status == "COMPLETED"
        assert db_steps[1].status == "FAILED"
        assert db_steps[2].status == "PENDING"  # Aborted before execution
        
    # Assert that step 3 was never executed
    assert outputs == ["step1_run", "step2_run"]
