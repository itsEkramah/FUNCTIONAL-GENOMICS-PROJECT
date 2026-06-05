BACKEND_SCHEMA.md
PathoScope AI Database & Data Architecture Specification

Version: 1.0

Authority:

MASTER_BLUEPRINT.md
BLUEPRINT.md
PROJECT_RULES.md
TRD.md
1. PURPOSE

This document defines:

Database architecture
Table definitions
Relationships
Indexing strategy
Storage architecture
Job tracking
Workflow state tracking
PubMed storage
AI interpretation storage
Report storage
Security model

This document is the authoritative source for all backend data structures.

2. DATABASE SELECTION

Primary Database:

PostgreSQL

Reason:

ACID compliant
Reliable
Production ready
Supports JSON
Strong indexing
Excellent FastAPI support
3. DATABASE OVERVIEW

Database Name:

pathoscope_ai

Contains:

users

sessions

jobs

job_steps

uploaded_files

fasta_runs

fastq_runs

deg_runs

annotations

pfam_domains

taxonomy_results

kegg_results

pubmed_queries

pubmed_articles

ai_interpretations

reports

audit_logs
4. USERS TABLE

Purpose:

Store user accounts.

Table:

users

Columns:

Column	Type
id	UUID PK
username	VARCHAR(100)
email	VARCHAR(255)
password_hash	TEXT
role	VARCHAR(20)
created_at	TIMESTAMP
updated_at	TIMESTAMP

Role Values:

admin

user

Indexes:

email UNIQUE

username UNIQUE
5. SESSIONS TABLE

Purpose:

Authentication tracking.

Table:

sessions

Columns:

Column	Type
id	UUID PK
user_id	UUID FK
token	TEXT
created_at	TIMESTAMP
expires_at	TIMESTAMP

Relationship:

users → sessions

1:N
6. JOBS TABLE

Most Important Table

Tracks every workflow.

Table:

jobs

Columns:

Column	Type
id	UUID PK
job_name	TEXT
workflow_type	TEXT
status	TEXT
progress_percent	INTEGER
user_id	UUID FK
created_at	TIMESTAMP
started_at	TIMESTAMP
completed_at	TIMESTAMP
failed_reason	TEXT

Workflow Types:

FASTA

FASTQ

DEG

Status Values:

QUEUED

RUNNING

FAILED

COMPLETED

CANCELLED

Indexes:

status

workflow_type

created_at
7. JOB_STEPS TABLE

Purpose:

Track every pipeline step.

Table:

job_steps

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
step_name	TEXT
step_order	INTEGER
status	TEXT
start_time	TIMESTAMP
end_time	TIMESTAMP
log_path	TEXT
output_path	TEXT
error_message	TEXT

Relationship:

jobs → job_steps

1:N
8. UPLOADED_FILES TABLE

Purpose:

Track user uploads.

Table:

uploaded_files

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
original_name	TEXT
file_type	TEXT
file_size	BIGINT
storage_path	TEXT
uploaded_at	TIMESTAMP

Supported Types:

FASTA

FASTQ

FASTQ_GZ

CSV

TSV
9. FASTA_RUNS TABLE

Purpose:

Store FASTA workflow summary.

Table:

fasta_runs

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
genome_length	INTEGER
gc_content	FLOAT
ambiguity_count	INTEGER
total_orfs	INTEGER
translated_proteins	INTEGER
created_at	TIMESTAMP
10. FASTQ_RUNS TABLE

Purpose:

Store FASTQ workflow summary.

Table:

fastq_runs

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
raw_reads	BIGINT
filtered_reads	BIGINT
average_quality	FLOAT
assembly_contigs	INTEGER
created_at	TIMESTAMP
11. DEG_RUNS TABLE

Purpose:

Store DEG workflow summary.

Table:

deg_runs

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
total_genes	INTEGER
significant_genes	INTEGER
upregulated	INTEGER
downregulated	INTEGER
created_at	TIMESTAMP
12. ANNOTATIONS TABLE

Purpose:

Store DIAMOND annotations.

Table:

annotations

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
query_protein	TEXT
subject_protein	TEXT
identity_percent	FLOAT
coverage_percent	FLOAT
evalue	FLOAT
bitscore	FLOAT
annotation	TEXT

Indexes:

query_protein

annotation
13. PFAM_DOMAINS TABLE

Purpose:

Store HMMER results.

Table:

pfam_domains

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
protein_id	TEXT
pfam_accession	TEXT
pfam_name	TEXT
domain_start	INTEGER
domain_end	INTEGER
evalue	FLOAT
14. TAXONOMY_RESULTS TABLE

Purpose:

Store NCBI taxonomy results.

Table:

taxonomy_results

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
tax_id	INTEGER
organism_name	TEXT
lineage	JSONB
rank	TEXT
15. KEGG_RESULTS TABLE

Purpose:

Store pathway mappings.

Table:

kegg_results

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
pathway_id	TEXT
pathway_name	TEXT
gene_count	INTEGER
pvalue	FLOAT
fdr	FLOAT
16. PUBMED_QUERIES TABLE

Purpose:

Store search queries.

Table:

pubmed_queries

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
query_text	TEXT
query_type	TEXT
created_at	TIMESTAMP

Query Types:

protein

pfam

taxonomy

pathway

gene
17. PUBMED_ARTICLES TABLE

Purpose:

Store retrieved literature.

Table:

pubmed_articles

Columns:

Column	Type
id	UUID PK
query_id	UUID FK
pmid	TEXT
title	TEXT
journal	TEXT
publication_year	INTEGER
authors	JSONB
doi	TEXT
abstract	TEXT
relevance_score	FLOAT

Indexes:

pmid UNIQUE

publication_year
18. AI_INTERPRETATIONS TABLE

Purpose:

Store generated interpretations.

Table:

ai_interpretations

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
ai_provider	TEXT
model_name	TEXT
findings	TEXT
literature_summary	TEXT
biological_interpretation	TEXT
confidence_assessment	TEXT
limitations	TEXT
created_at	TIMESTAMP

AI Providers:

gemini

openai
19. REPORTS TABLE

Purpose:

Track generated reports.

Table:

reports

Columns:

Column	Type
id	UUID PK
job_id	UUID FK
report_type	TEXT
report_path	TEXT
generated_at	TIMESTAMP

Report Types:

HTML

PDF

CSV

JSON

GFF3
20. AUDIT_LOGS TABLE

Purpose:

Permanent audit trail.

Table:

audit_logs

Columns:

Column	Type
id	UUID PK
user_id	UUID FK
action	TEXT
resource_type	TEXT
resource_id	TEXT
timestamp	TIMESTAMP
details	JSONB

Never delete records.

21. STORAGE ARCHITECTURE

Filesystem Structure

storage/

jobs/

JOB_ID/

inputs/

outputs/

logs/

reports/

pubmed/

cache/
22. JOB DIRECTORY STRUCTURE

Example:

storage/jobs/

JOB_2026_000001/

inputs/

virus.fasta

outputs/

orfs.fasta

proteins.fasta

diamond.tsv

hmmer.tsv

reports/

report.html

report.pdf

logs/

pipeline.log

pubmed/

articles.json
23. REDIS CACHE DESIGN

Purpose:

Real-time performance.

Cache Keys:

job_status:{job_id}

job_progress:{job_id}

pubmed:{query_hash}

ai_prompt:{job_id}
24. DATA OWNERSHIP RULES

User owns:

uploads
jobs
reports
interpretations

Administrator owns:

system settings
tool configurations
user management
25. PERMISSIONS MATRIX
Action	User	Admin
Upload Files	Yes	Yes
Run Workflow	Yes	Yes
View Own Jobs	Yes	Yes
View Other Jobs	No	Yes
Delete Users	No	Yes
View Logs	Own	All
26. DATABASE INDEXING STRATEGY

Indexes Required:

jobs(status)

jobs(created_at)

job_steps(job_id)

annotations(query_protein)

pubmed_articles(pmid)

reports(job_id)

uploaded_files(job_id)
27. BACKUP STRATEGY

Daily:

Database Backup

Weekly:

Compressed Archive

Monthly:

Full Snapshot

28. SECURITY REQUIREMENTS

Passwords:

bcrypt

JWT Authentication:

RS256

API Keys:

Stored only in:

.env

Never database.

Never frontend.

29. ACCEPTANCE CRITERIA

Database architecture accepted only if:

✓ Every workflow tracked

✓ Every step tracked

✓ Every report tracked

✓ Every PubMed article tracked

✓ Every AI interpretation tracked

✓ User ownership enforced

✓ Job recovery supported

✓ Audit trail permanent

✓ Supports reproducibility