import logging
import os
import sys
from datetime import datetime
from backend.config.settings import settings
from backend.config.constants import STORAGE_DIR

# Establish global log format
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Ensure global logs directory exists
GLOBAL_LOGS_DIR = os.path.join(STORAGE_DIR, "logs")
os.makedirs(GLOBAL_LOGS_DIR, exist_ok=True)
GLOBAL_LOG_FILE = os.path.join(GLOBAL_LOGS_DIR, "app.log")

def setup_global_logging():
    """
    Configures root logging system to output to stdout and global file.
    """
    log_level_str = settings.log_level.upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Initialize handlers
    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(GLOBAL_LOG_FILE, encoding="utf-8")

    # Set formats
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    stdout_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(stdout_handler)
    root_logger.addHandler(file_handler)

    logging.info(f"Logger initialized. Level: {log_level_str}. Global log file: {GLOBAL_LOG_FILE}")

def get_logger(name: str) -> logging.Logger:
    """
    Gets a named logger instance.
    """
    return logging.getLogger(name)

def get_job_logger(job_id: str, job_dir: str) -> logging.Logger:
    """
    Creates and returns a specific logger instance routing to a dedicated job pipeline log file.
    
    Parameters:
    -----------
    job_id : str
        The unique identifier for the running job.
    job_dir : str
        The storage path where job inputs, outputs, and logs are kept.
        
    Returns:
    --------
    logger : Logger
        A Logger instance configured with a file handler pointing to the job log file.
    """
    logger = logging.getLogger(f"job_{job_id}")
    
    # Check if this logger already has handlers configured (prevent duplication)
    if logger.hasHandlers():
        return logger
        
    logger.setLevel(logging.DEBUG)
    
    # Configure job-specific log directory and file path
    job_logs_dir = os.path.join(job_dir, "logs")
    os.makedirs(job_logs_dir, exist_ok=True)
    job_log_file = os.path.join(job_logs_dir, "pipeline.log")
    
    # Create file handler
    file_handler = logging.FileHandler(job_log_file, encoding="utf-8")
    formatter = logging.Formatter(
        fmt=f"[%(asctime)s] [{job_id}] [%(levelname)s] %(message)s",
        datefmt=DATE_FORMAT
    )
    file_handler.setFormatter(formatter)
    
    # Add handler to job logger
    logger.addHandler(file_handler)
    
    # Prevent propagation to root logger to keep console output clean from verbose details
    logger.propagate = False
    
    logger.info(f"Dedicated pipeline logger initialized for job: {job_id}")
    return logger

# Run global setup upon import
setup_global_logging()
