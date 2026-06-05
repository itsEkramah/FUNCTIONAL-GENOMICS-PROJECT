import os

# Project root path resolution
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CONFIG_DIR)
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)

# Data storage paths
STORAGE_DIR = os.path.join(PROJECT_ROOT, "storage")
JOBS_DIR = os.path.join(STORAGE_DIR, "jobs")
CACHE_DIR = os.path.join(STORAGE_DIR, "cache")
PUBMED_DIR = os.path.join(STORAGE_DIR, "pubmed")

# Workflow type definitions
WORKFLOW_FASTA = "FASTA"
WORKFLOW_FASTQ = "FASTQ"
WORKFLOW_DEG = "DEG"

# Job status state definitions
STATUS_QUEUED = "QUEUED"
STATUS_RUNNING = "RUNNING"
STATUS_COMPLETED = "COMPLETED"
STATUS_FAILED = "FAILED"
STATUS_CANCELLED = "CANCELLED"

# Job step status definitions
STEP_PENDING = "PENDING"
STEP_RUNNING = "RUNNING"
STEP_COMPLETED = "COMPLETED"
STEP_FAILED = "FAILED"

# API & Security
SESSION_ROLE_ADMIN = "admin"
SESSION_ROLE_USER = "user"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24
