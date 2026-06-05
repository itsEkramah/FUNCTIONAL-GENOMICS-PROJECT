# DATABASE_DESIGN_REPORT.md — Database Design Report

> **Document Status**: `FINAL`  
> **Database Engine**: PostgreSQL 16+ / Redis 7.2+  
> **ORM Engine**: SQLAlchemy 2.0+ (Declarative Mapping) / Alembic Migrations  
> **Development Constraint**: NO CODE IMPLEMENTED YET — STRICT ARCHITECTURAL ALIGNMENT PHASE  

---

## 1. DATABASE OVERVIEW

PathoScope AI v3.0 uses **PostgreSQL** as its primary persistent database engine (`pathoscope_ai`) to enforce transaction integrity, structural normalization, and high query speed. **Redis** is used as a high-performance in-memory cache layer to store transient pipeline statuses, progress indicators, and API query results.

---

## 2. RELATIONAL SCHEMA MAP (17 TABLES)

Below are the detailed schema definitions for all 17 tables. Every field includes its SQL type, nullability constraint, default value, and key definitions.

```
  ┌────────────────────────────────────────────────────────────────────────┐
  │                            POSTGRESQL SCHEMA                           │
  ├────────────────────────────────────────────────────────────────────────┤
  │  1. users: UUID, username, email, password_hash, role, created_at      │
  │  2. sessions: UUID, user_id (FK), token, created_at, expires_at        │
  │  3. jobs: UUID, job_name, workflow_type, status, progress, user_id     │
  │  4. job_steps: UUID, job_id (FK), step_name, order, status, logs_path  │
  │  5. uploaded_files: UUID, job_id (FK), original_name, size, path       │
  │  6. fasta_runs: UUID, job_id (FK), length, GC%, total_orfs, proteins   │
  │  7. fastq_runs: UUID, job_id (FK), raw_reads, filtered_reads, contigs  │
  │  8. deg_runs: UUID, job_id (FK), total_genes, sig_genes, up, down      │
  │  9. annotations: UUID, job_id (FK), query, subject, identity, evalue   │
  │ 10. pfam_domains: UUID, job_id (FK), protein_id, accession, start, end │
  │ 11. taxonomy_results: UUID, job_id (FK), tax_id, name, lineage, rank   │
  │ 12. kegg_results: UUID, job_id (FK), pathway_id, name, gene_count, fdr │
  │ 13. pubmed_queries: UUID, job_id (FK), query_text, query_type          │
  │ 14. pubmed_articles: UUID, query_id (FK), pmid, title, abstract, DOI   │
  │ 15. ai_interpretations: UUID, job_id (FK), provider, findings, limits  │
  │ 16. reports: UUID, job_id (FK), report_type (GFF3/PDF), report_path    │
  │ 17. audit_logs: UUID, user_id (FK), action, details (JSONB)            │
  └────────────────────────────────────────────────────────────────────────┘
```

### 1. `users`
Stores user authentication details and administrative roles.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `username`: `VARCHAR(100)` (Not Null, Unique)
* `email`: `VARCHAR(255)` (Not Null, Unique)
* `password_hash`: `TEXT` (Not Null)
* `role`: `VARCHAR(20)` (Not Null, Default: `'user'`, constraints: `'admin'`, `'user'`)
* `created_at`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)
* `updated_at`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)

### 2. `sessions`
Tracks active user session tokens.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `user_id`: `UUID` (Foreign Key -> `users.id`, On Delete Cascade, Not Null)
* `token`: `TEXT` (Not Null, Unique)
* `created_at`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)
* `expires_at`: `TIMESTAMP` (Not Null)

### 3. `jobs`
Main pipeline execution monitor.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_name`: `TEXT` (Not Null)
* `workflow_type`: `VARCHAR(20)` (Not Null, constraints: `'FASTA'`, `'FASTQ'`, `'DEG'`)
* `status`: `VARCHAR(20)` (Not Null, Default: `'QUEUED'`, constraints: `'QUEUED'`, `'RUNNING'`, `'FAILED'`, `'COMPLETED'`, `'CANCELLED'`)
* `progress_percent`: `INTEGER` (Not Null, Default: `0`, Check: `progress_percent >= 0 AND progress_percent <= 100`)
* `user_id`: `UUID` (Foreign Key -> `users.id`, On Delete Set Null, Nullable)
* `created_at`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)
* `started_at`: `TIMESTAMP` (Nullable)
* `completed_at`: `TIMESTAMP` (Nullable)
* `failed_reason`: `TEXT` (Nullable)

### 4. `job_steps`
Tracks execution logs and outputs for individual pipeline steps.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Cascade, Not Null)
* `step_name`: `TEXT` (Not Null)
* `step_order`: `INTEGER` (Not Null)
* `status`: `VARCHAR(20)` (Not Null, Default: `'PENDING'`, constraints: `'PENDING'`, `'RUNNING'`, `'FAILED'`, `'COMPLETED'`)
* `start_time`: `TIMESTAMP` (Nullable)
* `end_time`: `TIMESTAMP` (Nullable)
* `log_path`: `TEXT` (Nullable)
* `output_path`: `TEXT` (Nullable)
* `error_message`: `TEXT` (Nullable)

### 5. `uploaded_files`
Tracks user uploads and storage locations.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Set Null, Nullable, Unique)
* `original_name`: `TEXT` (Not Null)
* `file_type`: `VARCHAR(20)` (Not Null, constraints: `'FASTA'`, `'FASTQ'`, `'FASTQ_GZ'`, `'CSV'`, `'TSV'`)
* `file_size`: `BIGINT` (Not Null)
* `storage_path`: `TEXT` (Not Null)
* `uploaded_at`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)

### 6. `fasta_runs`
Biological run summary for FASTA files.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Cascade, Not Null, Unique)
* `genome_length`: `INTEGER` (Not Null)
* `gc_content`: `DOUBLE PRECISION` (Not Null)
* `ambiguity_count`: `INTEGER` (Not Null, Default: `0`)
* `total_orfs`: `INTEGER` (Not Null)
* `translated_proteins`: `INTEGER` (Not Null)
* `created_at`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)

### 7. `fastq_runs`
Biological run summary for FASTQ files.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Cascade, Not Null, Unique)
* `raw_reads`: `BIGINT` (Not Null)
* `filtered_reads`: `BIGINT` (Not Null)
* `average_quality`: `DOUBLE PRECISION` (Not Null)
* `assembly_contigs`: `INTEGER` (Nullable)
* `created_at`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)

### 8. `deg_runs`
Transcriptomics run summary for expression tables.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Cascade, Not Null, Unique)
* `total_genes`: `INTEGER` (Not Null)
* `significant_genes`: `INTEGER` (Not Null)
* `upregulated`: `INTEGER` (Not Null)
* `downregulated`: `INTEGER` (Not Null)
* `created_at`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)

### 9. `annotations`
Stores DIAMOND homology mapping hits.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Cascade, Not Null)
* `query_protein`: `TEXT` (Not Null)
* `subject_protein`: `TEXT` (Not Null)
* `identity_percent`: `DOUBLE PRECISION` (Not Null)
* `coverage_percent`: `DOUBLE PRECISION` (Not Null)
* `evalue`: `DOUBLE PRECISION` (Not Null)
* `bitscore`: `DOUBLE PRECISION` (Not Null)
* `annotation`: `TEXT` (Not Null)

### 10. `pfam_domains`
Stores HMMER protein domain prediction hits.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Cascade, Not Null)
* `protein_id`: `TEXT` (Not Null)
* `pfam_accession`: `VARCHAR(50)` (Not Null)
* `pfam_name`: `TEXT` (Not Null)
* `domain_start`: `INTEGER` (Not Null)
* `domain_end`: `INTEGER` (Not Null)
* `evalue`: `DOUBLE PRECISION` (Not Null)

### 11. `taxonomy_results`
Stores NCBI Taxonomy assignments.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Cascade, Not Null)
* `tax_id`: `INTEGER` (Not Null)
* `organism_name`: `TEXT` (Not Null)
* `lineage`: `JSONB` (Not Null)
* `rank`: `VARCHAR(50)` (Not Null)

### 12. `kegg_results`
Stores biological pathway map hits.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Cascade, Not Null)
* `pathway_id`: `VARCHAR(50)` (Not Null)
* `pathway_name`: `TEXT` (Not Null)
* `gene_count`: `INTEGER` (Not Null)
* `pvalue`: `DOUBLE PRECISION` (Not Null)
* `fdr`: `DOUBLE PRECISION` (Not Null)

### 13. `pubmed_queries`
Caches NCBI E-Utilities literature search keywords.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Cascade, Not Null)
* `query_text`: `TEXT` (Not Null)
* `query_type`: `VARCHAR(20)` (Not Null, constraints: `'protein'`, `'pfam'`, `'taxonomy'`, `'pathway'`, `'gene'`)
* `created_at`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)

### 14. `pubmed_articles`
Caches downloaded PubMed abstracts to avoid API rate limits.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `query_id`: `UUID` (Foreign Key -> `pubmed_queries.id`, On Delete Cascade, Not Null)
* `pmid`: `VARCHAR(50)` (Not Null, Unique)
* `title`: `TEXT` (Not Null)
* `journal`: `TEXT` (Not Null)
* `publication_year`: `INTEGER` (Not Null)
* `authors`: `JSONB` (Not Null)
* `doi`: `VARCHAR(100)` (Nullable)
* `abstract`: `TEXT` (Not Null)
* `relevance_score`: `DOUBLE PRECISION` (Not Null)

### 15. `ai_interpretations`
Stores grounded LLM biological interpretations.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Cascade, Not Null, Unique)
* `ai_provider`: `VARCHAR(20)` (Not Null, constraints: `'gemini'`, `'openai'`)
* `model_name`: `VARCHAR(50)` (Not Null)
* `findings`: `TEXT` (Not Null)
* `literature_summary`: `TEXT` (Not Null)
* `biological_interpretation`: `TEXT` (Not Null)
* `confidence_assessment`: `VARCHAR(20)` (Not Null, constraints: `'HIGH'`, `'MEDIUM'`, `'LOW'`)
* `limitations`: `TEXT` (Not Null)
* `created_at`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)

### 16. `reports`
Tracks compiled HTML, PDF, GFF3, JSON, and CSV reports.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `job_id`: `UUID` (Foreign Key -> `jobs.id`, On Delete Cascade, Not Null)
* `report_type`: `VARCHAR(10)` (Not Null, constraints: `'HTML'`, `'PDF'`, `'CSV'`, `'JSON'`, `'GFF3'`)
* `report_path`: `TEXT` (Not Null)
* `generated_at`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)

### 17. `audit_logs`
Permanent, read-only system audit log.
* `id`: `UUID` (Primary Key, Default: `uuid_generate_v4()`)
* `user_id`: `UUID` (Foreign Key -> `users.id`, On Delete Set Null, Nullable)
* `action`: `TEXT` (Not Null)
* `resource_type`: `VARCHAR(50)` (Not Null)
* `resource_id`: `TEXT` (Not Null)
* `timestamp`: `TIMESTAMP` (Not Null, Default: `CURRENT_TIMESTAMP`)
* `details`: `JSONB` (Nullable)

---

## 3. DATABASE INDEXES

To optimize query latency during dashboard updates and result rendering, the following indexes are required:

| Index Name | Table | Columns | Target Operations / Justification |
|------------|-------|---------|------------------------------------|
| `idx_users_email` | `users` | `email` (Unique) | User login lookup |
| `idx_sessions_token` | `sessions` | `token` (Unique) | Session validation |
| `idx_jobs_status` | `jobs` | `status` | Dashboard status filters / queues |
| `idx_jobs_user_id` | `jobs` | `user_id` | Renders user history list |
| `idx_job_steps_job_id` | `job_steps` | `job_id`, `step_order` | Live status tree matching |
| `idx_annotations_query` | `annotations` | `job_id`, `query_protein` | Mapping annotation details by ID |
| `idx_pfam_protein_id` | `pfam_domains` | `job_id`, `protein_id` | Renders domain map |
| `idx_pubmed_articles_pmid`| `pubmed_articles` | `pmid` (Unique) | PMID caching |
| `idx_kegg_results_job_id` | `kegg_results` | `job_id` | Renders KEGG charts |
| `idx_reports_job_id` | `reports` | `job_id` | Downloads list retrieval |

---

## 4. RELATIONAL SHADOW RULES (FOREIGN KEY ACTIONS)

* **Cascade Deletes**: Deleting a record from `jobs` automatically cascades and deletes related entries in child tables: `job_steps`, `fasta_runs`, `fastq_runs`, `deg_runs`, `annotations`, `pfam_domains`, `taxonomy_results`, `kegg_results`, `pubmed_queries`, `ai_interpretations`, and `reports`.
* **Safe Audits**: Deleting a user from the `users` table sets `user_id` to `NULL` in the `jobs` and `audit_logs` tables. This protects historical logs from database corruption.
* **Audit Rule**: Records in the `audit_logs` table are read-only and cannot be updated or deleted by user operations.

---

## 5. JOB TRACKING SCHEMA

```
[PostgreSQL Database]                                              [Redis Cache]
Table: jobs                                                  Key: job_status:{job_id}
 - id (UUID PK)                                              Type: String (RUNNING, FAILED)
 - status (QUEUED, RUNNING)                                  TTL: 24 Hours
 - progress_percent (0-100)                                  
      │                                                           │
      ▼ (Sync State updates)                                      ▼ (Sync State updates)
┌────────────────────────────────────────────────────────────────────────┐
│                        pipeline_runner.py Execution                    │
└────────────────────────────────────────────────────────────────────────┘
      ▲ (Read order)                                              ▲ (Publish progress)
      │                                                           │
Table: job_steps                                             Key: job_progress:{job_id}
 - id (UUID PK)                                              Type: String (Integer: 0-100)
 - job_id (FK)                                               TTL: 24 Hours
 - step_name ("DIAMOND")
 - step_order (1, 2, 3...)
 - status (PENDING, RUNNING)
```

1. **Job Creation**:
   * The API layer inserts a new record into the `jobs` table (`status = 'QUEUED'`).
   * It creates sequential step templates in `job_steps` mapped by `step_order`.
2. **Execution Monitoring**:
   * The pipeline runner sets `jobs.status = 'RUNNING'` in PostgreSQL, updates `job_status:{job_id}` in Redis, and sets `progress_percent = 0`.
   * For each active step, it updates `job_steps.status = 'RUNNING'`.
   * Upon step success, it sets `job_steps.status = 'COMPLETED'` and calculates new progress:
     $$\text{Progress \%} = \left( \frac{\text{Completed Steps}}{\text{Total Steps}} \right) \times 100$$
   * The pipeline runner updates `jobs.progress_percent` in PostgreSQL and `job_progress:{job_id}` in Redis.
3. **Completion / Failure**:
   * On validation success: status is set to `COMPLETED` and progress to `100`.
   * On validation failure: status is set to `FAILED`, the step error details are recorded, and the runner stops.

---

## 6. PUBMED CACHING SCHEMA

To prevent query failures due to NCBI E-Utilities rate limits (3 requests/sec without API key), the system implements a two-tiered database and cache architecture.

```
                  [Query Target: Species & Protein]
                                  │
                                  ▼
                     [Redis: pubmed:{query_hash}]
                      (Check for cached PMIDs)
                                  │
        ┌─────────── Match Found ─┴─ No Match ──────────┐
        ▼                                               ▼
  [Return JSON list]                     [Postgres: pubmed_queries]
                                                │
                       ┌───────── Match Found ──┴─ No Match ───────┐
                       ▼                                           ▼
             [Read pubmed_articles]                      [NCBI E-Utilities Query]
                                                                   │
                                                                   ▼
                                                         [Save to pubmed_queries]
                                                                   │
                                                                   ▼
                                                        [Save to pubmed_articles]
```

### Table Mapping
* **`pubmed_queries`**: Stores search terms (e.g. `query_text = 'Zika virus envelope protein'`) and queries types (`query_type = 'protein'`).
* **`pubmed_articles`**: Stores abstract metadata. PMIDs are unique (`pmid` column is indexed). If multiple queries retrieve the same PMID, the duplicate is ignored and linked via mapping tables.

---

## 7. PIPELINE RESULTS SCHEMA

Biological results are stored in structured database tables rather than flat text files to support real-time UI components (charts, trees, filters).

### FASTA Output Tables
* **`fasta_runs`**: Stores overall GC%, length, and ORF counts.
* **`annotations`**: Stores sequence homology matches, identity percentages, coverage scores, and E-values.
* **`pfam_domains`**: Stores protein domain start/end positions and accession IDs for drawing domain architecture diagrams.
* **`taxonomy_results`**: Stores the NCBI Taxonomy lineage array (realm, kingdom, class, genus, species) as a JSONB array.

### FASTQ Output Tables
* **`fastq_runs`**: Stores raw read counts, post-trimming read counts, average read quality scores, and the total count of assembled contigs.
* **`annotations`**: (Reuses the FASTA annotations tables once filtered contigs undergo homology matching).

### DEG Output Tables
* **`deg_runs`**: Stores total processed genes, significant gene count, and upregulated/downregulated totals.
* **`kegg_results`**: Stores pathway name, matching gene counts, and calculated FDR p-values.

---

## 8. REDIS CACHING STRATEGY

Redis handles volatile session data, live execution progress, and external API caching.

### Cache Key Definitions

| Key Format | Data Type | Purpose | TTL (Expiration) |
|------------|-----------|---------|------------------|
| `job_status:{job_id}` | `String` | Stores active job status | 24 Hours |
| `job_progress:{job_id}` | `String` | Stores active progress (0-100) | 24 Hours |
| `pubmed:{query_hash}` | `String` (JSON) | Caches list of matched PMIDs | 30 Days |
| `ai_prompt:{job_id}` | `String` | Caches active prompt structures | 1 Hour |
| `session:{token}` | `String` | Caches active session user details | 1 Hour |

### Eviction Policy
* Redis runs under the `volatile-lru` (Least Recently Used) eviction policy.
* If Redis runs out of memory, it will evict expired or least recently used transient cache keys first, keeping the database safe from data loss.
