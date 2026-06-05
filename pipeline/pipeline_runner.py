import os
import uuid

class PipelineStep:
    def __init__(self, name: str, order: int, run_func, validate_func):
        self.name = name
        self.order = order
        self.run_func = run_func
        self.validate_func = validate_func

class PipelineRunner:
    def __init__(self):
        pass

    def create_job(self, job_name: str, workflow_type: str, user_id=None) -> str:
        return str(uuid.uuid4())

    def register_steps(self, job_id: str, steps: list):
        pass

    def run_job(self, job_id: str, steps: list):
        job_dir = os.path.join("storage", "jobs", job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        for step in sorted(steps, key=lambda s: s.order):
            output = step.run_func(job_dir, None)
            is_valid = step.validate_func(job_dir, output, None)
            if not is_valid:
                raise ValueError(f"Step {step.name} failed validation.")
