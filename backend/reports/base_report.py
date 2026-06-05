import os

class BaseReport:
    """
    Abstract base class for all report exporters.
    """
    def __init__(self, job_dir: str):
        self.job_dir = job_dir
        self.reports_dir = os.path.join(job_dir, "reports")
        os.makedirs(self.reports_dir, exist_ok=True)
        
    def get_output_path(self, filename: str) -> str:
        # Sanitize filename for Windows OS compatibility
        for char in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']:
            filename = filename.replace(char, '_')
        return os.path.join(self.reports_dir, filename)
