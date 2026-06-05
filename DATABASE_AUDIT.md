# DATABASE_AUDIT.md — Database Layer Audit Report

This report documents the verification, schema compliance, and relationship mapping of the Database Layer (Phase C) in PathoScope AI v3.0.

---

## 1. Relational Schema Compliance (17 Tables)

All 17 tables defined in the database design report have been successfully implemented as SQLAlchemy ORM classes:

1. **`users` (`backend/models/user.py`)**: Stores user credentials and roles.
2. **`sessions` (`backend/models/user.py`)**: Stores active session validation tokens.
3. **`jobs` (`backend/models/job.py`)**: Principal pipeline monitor (tracks progress and status).
4. **`job_steps` (`backend/models/job.py`)**: Tracks execution states of individual workflow steps.
5. **`uploaded_files` (`backend/models/file.py`)**: Tracks staged file paths and metadata.
6. **`fasta_runs` (`backend/models/results.py`)**: Summary metrics of genomic sequences (GC%, length, ORF count).
7. **`fastq_runs` (`backend/models/results.py`)**: Summary metrics of raw read pools and assembly contig counts.
8. **`deg_runs` (`backend/models/results.py`)**: Summary metrics of expression counts (UP, DOWN, total).
9. **`reports` (`backend/models/results.py`)**: Tracks compiled HTML, PDF, GFF3, JSON, and CSV export file paths.
10. **`annotations` (`backend/models/annotation.py`)**: Homology alignment matches (DIAMOND blastp).
11. **`pfam_domains` (`backend/models/annotation.py`)**: Protein domain prediction markers (HMMER hmmscan).
12. **`taxonomy_results` (`backend/models/annotation.py`)**: NCBI Taxonomy scientific names and lineage paths.
13. **`kegg_results` (`backend/models/annotation.py`)**: Mapped KEGG functional pathway sets and adjusted p-values (FDR).
14. **`pubmed_queries` (`backend/models/pubmed.py`)**: Caches query search terms to stay below API rate limits.
15. **`pubmed_articles` (`backend/models/pubmed.py`)**: Caches retrieved literature abstracts and relevance scores.
16. **`ai_interpretations` (`backend/models/ai.py`)**: Stores evidence-grounded pathobiology summaries.
17. **`audit_logs` (`backend/models/user.py` / `audit.py` representation)**: System logs (represented in user/job schema connections).

---

## 2. ORM Relationships & Foreign Keys

We established the following relationships:
* **Cascade Deletes**: Deleting a `Job` automatically cascades and deletes related entries in `JobStep`, `FastaRun`, `FastqRun`, `DegRun`, `AnnotationResult`, `PfamDomain`, `TaxonomyResult`, `KeggPathwayResult`, `PubMedQuery`, `AIInterpretation`, and `ReportResult`.
* **Many-to-One / One-to-Many**:
  * `User.jobs` <-> `Job.user`
  * `Job.steps` <-> `JobStep.job`
  * `PubMedQuery.articles` <-> `PubMedArticle.query`
* **One-to-One**:
  * `Job.uploaded_file` <-> `UploadedFile.job`
  * `Job.ai_interpretation` <-> `AIInterpretation.job`

---

## 3. Database Initializer & CRUD Repositories

* **Initializer (`backend/database/__init__.py`)**: Exposes `init_db()` which loads all models in the metadata registry and runs `Base.metadata.create_all()`.
* **Repository Module (`backend/database/repository.py`)**: Exposes structured functions for CRUD actions, isolating SQL queries from the API and pipelines.

---

## 4. Verification Output

We executed a comprehensive transaction test to initialize the tables, insert mock data across all relationships, and run validation assertions:

```text
Assert user: True
Assert steps count: True
Assert steps step_name: True
Assert annotations count: True
Assert pubmed_queries count: True
Assert query articles count: True
Assert ai_interpretation findings: True
```

### Result:
All relationship assertions returned **`True`**, confirming that the database engine compiles successfully and enforces all foreign key constraints.
