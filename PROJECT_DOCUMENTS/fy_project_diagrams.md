# PathoScope AI: Technical Architecture and System Diagrams

This document contains 20 publication-quality system diagrams, data flows, and state machines representing the actual software design and implementation of the PathoScope AI platform.

---

## DIAGRAM 1: COMPLETE SYSTEM ARCHITECTURE

```mermaid
graph TD
    User([User Browser]) <--> |"HTTP / JSON / SSE"| API[FastAPI Backend Server]
    API <--> |"SQLAlchemy ORM"| DB[(SQLite / PostgreSQL)]
    
    subgraph "API Routing Layer"
        UploadRoute["/api/upload"]
        JobsRoute["/api/jobs"]
        ReportsRoute["/api/reports"]
        SettingsRoute["/api/settings"]
    end
    
    subgraph "Core Orchestration"
        Detector[Workflow Auto-Detection Engine]
        Runner[Pipeline Runner Core]
    end
    
    subgraph "Active Execution Engines"
        FASTA[FASTA Engine]
        FASTQ[FASTQ Engine]
        DEG[DEG Engine]
    end
    
    subgraph "External Integration Services"
        DIAMOND[DIAMOND Service]
        HMMER[HMMER Service]
        NCBI[NCBI Taxonomy & Entrez Service]
        PubMed[PubMed Literature Service]
        AI[AI Interpretation Service]
    end
    
    subgraph "Local Filesystem Storage"
        JobsStorage["storage/jobs/{job_id}/"]
        Outputs["Raw Outputs & Logs"]
        Exporters["HTML / PDF / GFF3 Reports"]
    end
    
    User <--> UploadRoute & JobsRoute & ReportsRoute & SettingsRoute
    UploadRoute --> Detector
    Detector --> |"Routes Job"| Runner
    Runner --> |"Spawns Thread"| FASTA & FASTQ & DEG
    
    FASTA --> DIAMOND & HMMER & NCBI & PubMed & AI
    FASTQ --> NCBI & PubMed & AI
    DEG --> PubMed & AI
    
    Runner <--> |"Reads/Writes Logs & Data"| JobsStorage
    JobsStorage --- Outputs & Exporters
```

*   **Diagram Title**: System Integration Architecture
*   **Purpose**: To illustrate the overall interaction between the frontend client, the FastAPI routing controllers, core execution modules, and external web APIs.
*   **Explanation**: When a user uploads a file, it enters `/api/upload` where the auto-detection module reads its headers to classify the file. The pipeline runner is triggered to spawn an execution thread. The thread coordinates sequence translations, local alignments (via DIAMOND/HMMER subprocess wrappers), taxonomic queries, literature extraction, and AI analysis. The intermediate artifacts and final reports are stored locally in the filesystem (`storage/jobs/{job_id}/`) and registered in the SQL database.

---

## DIAGRAM 2: FRONTEND COMPONENT ARCHITECTURE

```mermaid
graph TD
    App["Next.js App Router (app/layout.tsx)"] --> Sidebar["Sidebar Navigation"]
    App --> MainWorkspace["Workspace Page (workspace/page.tsx)"]
    App --> Settings["Settings Page (settings/page.tsx)"]
    App --> Reports["Reports Page (reports/page.tsx)"]
    App --> Manual["Documentation Page (documentation/page.tsx)"]
    
    MainWorkspace --> Dropzone["Dropzone Uploader"]
    MainWorkspace --> Terminal["Terminal Log Viewer (SSE)"]
    MainWorkspace --> PipelineSteps["Pipeline Steps Tracker"]
    MainWorkspace --> ResultsViewer["Results Viewer Tab Container"]
    
    ResultsViewer --> Overview["Overview Stats Summary"]
    ResultsViewer --> QCViewer["QC Quality Charts"]
    ResultsViewer --> ORFMap["ORF Visual Map"]
    ResultsViewer --> Aligns["DIAMOND & Pfam Domain Tables"]
    ResultsViewer --> TaxTree["Taxonomy Tree Viewer"]
    ResultsViewer --> PubMedTab["Literature & PubMed Articles"]
    ResultsViewer --> AISynth["AI Interpretation Viewer"]
    ResultsViewer --> DEGPlots["DEG Volcano & MA Plots (Recharts)"]
```

*   **Diagram Title**: Next.js Component Hierarchy
*   **Purpose**: Illustrates the parent-child relationships and page-level organization of the React frontend.
*   **Explanation**: The frontend follows the Next.js App Router structure. The core page is the `Workspace` which manages the user uploads and hosts components for streaming backend logs (`Terminal`), rendering progress bars (`PipelineSteps`), and visualizing output tabs. It uses interactive components like Recharts for plotting DEG expression values and custom DOM structures to render tree taxonomic lineages.

---

## DIAGRAM 3: BACKEND ARCHITECTURE LAYERS

```mermaid
graph TD
    Req[Client Request] --> API["FastAPI Routing Layer (backend/api/)"]
    API --> |"Job Start / Stop"| Controller["Pipeline Controller & SSE Streamer"]
    
    subgraph "Core Processing Layer"
        Controller --> Runner["Pipeline Runner Engine (pipeline_runner.py)"]
        Runner --> FASTAWorkflow["Workflow FASTA (workflow_fasta.py)"]
        Runner --> FASTQWorkflow["Workflow FASTQ (workflow_fastq.py)"]
        Runner --> DEGWorkflow["Workflow DEG (workflow_deg.py)"]
    end
    
    subgraph "Service Wrapper Layer"
        FASTAWorkflow & FASTQWorkflow & DEGWorkflow --> Exec["Subprocess CLI Wrappers (fastp, FastQC, SPAdes, DIAMOND, HMMER)"]
        FASTAWorkflow & FASTQWorkflow & DEGWorkflow --> WebAPI["Web API Integration (NCBI, KEGG, OpenAI, Gemini)"]
    end
    
    subgraph "Data & Storage Access Layer"
        Runner & WebAPI --> Repo["Database Repository (repository.py)"]
        Repo --> DB[("SQL Database (SQLite / Postgres)")]
        Runner --> FileSystem["Local File I/O (storage/jobs/)"]
    end
    
    FileSystem --> Res[Client Response]
```

*   **Diagram Title**: Backend Layered Architecture and Request Lifecycle
*   **Purpose**: Maps the flow of requests from the HTTP endpoint through the calculation engines down to data persistence.
*   **Explanation**: The backend uses a decoupled, three-tier architecture. The **API Layer** acts as the controller, validating HTTP parameters and parsing uploaded streams. The **Core Processing Layer** runs long-lived pipelines inside background worker threads, ensuring the API remains responsive. The **Service Layer** abstracts interactions with local binary command-line executables and external web clients, caching duplicate requests to database tables.

---

## DIAGRAM 4: WORKFLOW AUTO-DETECTION ENGINE

```mermaid
graph TD
    Upload[Uploaded File Stream] --> Ext{"Check File Extension"}
    
    Ext --> |".gz"| Decompress["Read Gzip Header Chunk"]
    Ext --> |".fasta / .fa / .fna"| ReadFasta["Read First 10 Lines"]
    Ext --> |".fastq / .fq"| ReadFastq["Read First 10 Lines"]
    Ext --> |".csv / .tsv / .txt"| ReadTable["Read First 10 Lines"]
    
    Decompress --> ReadFasta & ReadFastq
    
    ReadFasta --> TestFasta{"Starts with '>'?"}
    TestFasta --> |"Yes"| RouteFASTA["Assign FASTA Workflow (Workflow A)"]
    TestFasta --> |"No"| Err["Raise ValueError (Format Unrecognized)"]
    
    ReadFastq --> TestFastq{"Starts with '@' & Line 3 starts with '+'?"}
    TestFastq --> |"Yes"| RouteFASTQ["Assign FASTQ Workflow (Workflow B)"]
    TestFastq --> |"No"| Err
    
    ReadTable --> TestHeader{"Contains gene_id, log2FoldChange, or pvalue?"}
    TestHeader --> |"Yes"| RouteDEG["Assign DEG Workflow (Workflow C)"]
    TestHeader --> |"No"| CheckDelim{"Contains comma or tab?"}
    CheckDelim --> |"Yes"| RouteDEG
    CheckDelim --> |"No"| Err
```

*   **Diagram Title**: File Auto-Detection Decision Matrix
*   **Purpose**: Detailed flow of how the system parses and routes uploaded datasets.
*   **Explanation**: Implemented in `file_detector.py`. The system reads only the first 10 lines of the file (or decompresses the first chunk if `.gz` is detected) to prevent high-memory allocations. It searches for classic biological indicators: `>` for FASTA headers, `@` and `+` pairing for FASTQ quality records, and expressions like `log2foldchange` or structural delimiters (commas and tabs) to route the data to the appropriate processing pipeline.

---

## DIAGRAM 5: FASTA PIPELINE WORKFLOW (11 STEPS)

```mermaid
graph TB
    Start([Upload FASTA]) --> S1["1. File Input Validation (IUPAC check)"]
    S1 --> S2["2. Sequence QC Metrics (GC% / Length)"]
    S2 --> S3["3. Six-Frame ORF Detection (min_length >= 100 bp)"]
    S3 --> S4["4. Amino Acid Translation (Safe Stop Truncation)"]
    S4 --> S5["5. DIAMOND Homology Search (vs. SwissProt)"]
    S5 --> S6["6. Pfam Domain Search (HMMER hmmscan)"]
    S6 --> S7["7. KEGG Pathway Mapping"]
    S7 --> S8["8. NCBI Taxonomy Lineage Lookup"]
    S8 --> S9["9. PubMed Literature Retrieval"]
    S9 --> S10["10. AI Pathobiology Summary Synthesis"]
    S10 --> S11["11. HTML/PDF/GFF3 Report Compilation"]
    S11 --> End([Results Loaded & Exportable])

    style S1 fill:#f9f,stroke:#333,stroke-width:1px
    style S5 fill:#bbf,stroke:#333,stroke-width:1px
    style S6 fill:#bbf,stroke:#333,stroke-width:1px
    style S10 fill:#bfb,stroke:#333,stroke-width:1px
```

*   **Diagram Title**: FASTA Workflow Steps
*   **Purpose**: Illustrates the chronological execution steps inside `workflow_fasta.py`.
*   **Explanation**: This pipeline starts by screening characters to filter out non-nucleotide strings. It uses a sliding window to predict ORFs in all 6 frames. The predicted sequences are translated into proteins and queried against SwissProt using DIAMOND and Pfam using HMMER. Taxonomy IDs are retrieved to build search terms for literature and AI interpretation before compiling GFF3 coordinates and PDF documents.

---

## DIAGRAM 6: FASTQ PIPELINE WORKFLOW (QC, ASSEMBLY, ANNOTATION)

```mermaid
graph TD
    Start[Raw FASTQ File] --> S1["1. Input Validation (Record Iterator)"]
    S1 --> S2["2. Raw FastQC Profile"]
    S2 --> S3["3. fastp Quality Trimming (Q20 / Len >= 50)"]
    S3 --> S4["4. Trimmed FastQC Profile"]
    S4 --> S5["5. SPAdes De Novo Assembly (--rnaviral mode)"]
    S5 --> S6["6. Contig Length Filter (>= 500 bp)"]
    S6 --> S7["7. Save Assembled Contigs (input.fasta)"]
    S7 --> S8["8. Chain into Workflow A (Steps 1-11)"]
    
    subgraph "Chained Annotation"
        S8 --> FASTAWorkflow["FASTA Pipeline Execution"]
    end
```

*   **Diagram Title**: Raw Reads Quality Control and Assembly Pipeline
*   **Purpose**: Visualizes the preprocessing, assembly, and downstream annotation flow for Next-Generation Sequencing reads.
*   **Explanation**: Implemented in `workflow_fastq.py`. The raw reads are validated, run through an initial FastQC analysis, and trimmed using `fastp` to eliminate low-quality sequences (under Q20) and adapters. The trimmed reads are verified with a secondary FastQC pass and assembled into contigs using SPAdes. Contigs longer than 500 bp are saved and piped directly into the FASTA annotation engine to identify viral components.

---

## DIAGRAM 7: DEG PIPELINE WORKFLOW (HOST TRANSCRIPTOMICS)

```mermaid
graph TD
    Start[Counts Table or Precomputed DEGs] --> S1["1. File Format & Normalization Validation"]
    
    S1 --> CheckType{"Mode Selection"}
    CheckType --> |"Raw Count Matrix"| CPM["2. CPM Normalization & Log2 Transform"]
    CheckType --> |"Precomputed Table"| Skip["Verify Columns (log2FC, pvalue)"]
    
    CPM --> S2["3. Welch's t-test Calculation"]
    Skip --> FDR["4. Benjamini-Hochberg FDR Adjusted P-values"]
    S2 --> FDR
    
    FDR --> S3["5. DEG Classification (UP / DOWN / NS)"]
    S3 --> S4["6. Local Over-Representation Analysis (Fisher's exact test)"]
    S3 --> S5["7. Web Enrichment API Queries (GO & KEGG via GSEApy)"]
    
    S4 & S5 --> S6["8. PubMed literature linking for target pathways"]
    S6 --> S7["9. AI Transcriptomic Summary"]
    S7 --> S8["10. Plot Generation (Volcano / MA / Pathways)"]
    S8 --> S9["11. HTML / PDF Exporter"]
```

*   **Diagram Title**: DEG Analysis and Pathway Enrichment Pipeline
*   **Purpose**: Illustrates the statistical calculations, corrections, and functional annotations performed inside `workflow_deg.py`.
*   **Explanation**: The DEG workflow handles raw counts by converting them to Counts Per Million (CPM) and applying a $\log_2$ transformation. It runs a Welch's t-test to compare control vs. treatment conditions, adjusts for multiple testing using the Benjamini-Hochberg FDR algorithm, and performs Over-Representation Analysis (ORA). These results are linked to biological databases to generate interactive plots and exportable reports.

---

## DIAGRAM 8: FASTA DATA FLOW (INPUT / OUTPUT STATE)

```mermaid
graph LR
    FASTA["Raw FASTA String (Nucleotides)"] --> |"qc_engine.py"| QC["GC Content & Base Counts"]
    FASTA --> |"orf_finder.py"| ORFs["ORF Coordinates & Strands"]
    ORFs --> |"translator.py"| AA["Amino Acid Strings (Proteins)"]
    AA --> |"diamond_service.py"| Annot["Homology Hits (SwissProt)"]
    AA --> |"hmmer_service.py"| Domains["Domain Accessions (Pfam)"]
    Annot & Domains --> |"gff3_report.py"| GFF["GFF3 Coordinate Exporter"]
    Annot & Domains --> |"pubmed_service.py"| PubMed["PMID literature matches"]
    PubMed --> |"ai_service.py"| Reports["Structured Summary Reports"]
```

*   **Diagram Title**: Sequence Translation and Database Mapping Data Flow
*   **Purpose**: Follows the transformation of nucleotide sequences into proteins, annotations, and structured reports.
*   **Explanation**: This diagram shows the data transformations in the FASTA pipeline. Raw nucleotide inputs are parsed into coordinate intervals (ORFs), translated to amino acid representations (AA), mapped to protein accessions (SwissProt/Pfam), and exported as GFF3 genomic features, PubMed citations, and AI summaries.

---

## DIAGRAM 9: FASTQ DATA FLOW

```mermaid
graph LR
    FASTQ["Raw FASTQ (Sequencing Reads)"] --> |"fastp_service.py"| Trimmed["Trimmed Reads (Q20 Filtered)"]
    Trimmed --> |"spades_service.py"| Assembly["Assembled Graph (GFA)"]
    Assembly --> |"Contig Parser"| Contigs["Contigs (FASTA file)"]
    Contigs --> |"Chained Pipeline"| ORFs["Predicted ORFs"]
    ORFs --> |"Annotation Engine"| Proteins["Functional Annotations & Pathways"]
```

*   **Diagram Title**: Raw Reads to Functional Annotation Data Flow
*   **Purpose**: Documents the progression of raw Next-Generation Sequencing reads through assembly and functional annotation.
*   **Explanation**: Raw reads containing sequencing adapters and low-quality bases are trimmed by `fastp` to produce high-quality reads. SPAdes compiles these reads into assembly graphs to reconstruct consensus sequences (Contigs). These contigs are then processed by the gene prediction modules to identify coding regions and annotated pathways.

---

## DIAGRAM 10: DEG DATA FLOW

```mermaid
graph LR
    Counts["Raw Counts (Integer Matrix)"] --> |"CPM / Log2"| Normalized["Normalized Matrix (Float values)"]
    Normalized --> |"Welch's t-test"| Statistics["Mean, Variance, t-stats, p-values"]
    Statistics --> |"BH correction"| Adjust["FDR adjusted p-values (padj)"]
    Adjust --> |"Thresholds: p < 0.05, |FC| >= 1"| DEGs["Significant Genes (UP / DOWN)"]
    DEGs --> |"Fisher's Exact / Web APIs"| Enrichment["Enriched Pathways (GO / KEGG)"]
    Enrichment --> |"visualization_engine.py"| Volcano["Volcano & MA Plots (Matplotlib / Recharts)"]
```

*   **Diagram Title**: Transcriptomic Abundance Data Transformations
*   **Purpose**: Maps the data transformations from raw transcript counts to annotated pathways and volcano plot coordinates.
*   **Explanation**: Raw counts are normalized to log2-CPM values. The system computes statistical variables (means, standard deviations, t-statistics, and p-values) using Welch's t-test. The p-values are adjusted using the Benjamini-Hochberg procedure to classify genes as UP, DOWN, or Not Significant. These classified genes are then mapped to pathway databases.

---

## DIAGRAM 11: DATABASE SCHEMA (ER DIAGRAM)

```mermaid
erDiagram
    users ||--o{ jobs : "creates"
    jobs ||--o{ job_steps : "executes"
    jobs ||--|| fasta_results : "saves"
    jobs ||--|| fastq_results : "saves"
    jobs ||--|| deg_results : "saves"
    jobs ||--o{ files : "contains"
    jobs ||--o{ pubmed_queries : "queries"
    pubmed_queries ||--o{ pubmed_articles : "caches"
    jobs ||--|| ai_interpretations : "generates"

    users {
        string id PK
        string username
        string email
        string password_hash
        string role
        timestamp created_at
    }

    jobs {
        string id PK
        string job_name
        string workflow_type
        string status
        int progress_percent
        string user_id FK
        timestamp created_at
        timestamp started_at
        timestamp completed_at
        string failed_reason
    }

    job_steps {
        string id PK
        string job_id FK
        string step_name
        int step_order
        string status
        timestamp start_time
        timestamp end_time
        string error_message
    }

    fasta_results {
        string id PK
        string job_id FK
        json sequence_summary
        json orfs
        json alignments
        json domains
        json taxonomy
    }

    fastq_results {
        string id PK
        string job_id FK
        json raw_qc_summary
        json trimmed_qc_summary
        json assembly_summary
    }

    deg_results {
        string id PK
        string job_id FK
        json raw_matrix_summary
        json statistics
        json enriched_pathways
    }

    files {
        string id PK
        string job_id FK
        string filename
        string file_path
        string file_type
        int file_size
        timestamp uploaded_at
    }

    pubmed_queries {
        string id PK
        string job_id FK
        string query_text
        timestamp searched_at
    }

    pubmed_articles {
        string id PK
        string query_id FK
        string pmid
        string title
        string abstract
        string authors
        string doi
        string journal
        string pub_date
    }

    ai_interpretations {
        string id PK
        string job_id FK
        string provider
        string model
        string prompt_text
        text response_json
        timestamp generated_at
    }
```

*   **Diagram Title**: System Database Entity-Relationship Diagram
*   **Purpose**: Illustrates the tables, columns, data types, and primary/foreign key relationships in the SQL database.
*   **Explanation**: The database uses a centralized `jobs` table to manage workflows. Users can own multiple jobs, and each job registers its execution history in `job_steps`. To ensure flexibility for varying bioinformatics outputs, the final calculations are stored as structured JSON documents in `fasta_results`, `fastq_results`, and `deg_results` tables.

---

## DIAGRAM 12: JOB LIFECYCLE STATE MACHINE

```mermaid
stateDiagram-v2
    [*] --> QUEUED : User clicks 'Start Analysis'
    
    QUEUED --> RUNNING : Worker thread pulls job
    
    state RUNNING {
        [*] --> Validation
        Validation --> Processing : Passes input validation
        Validation --> FAILED : Invalid characters / format
        Processing --> GeneratingReports : Steps completed and validated
        Processing --> FAILED : Tool crash / Out of memory
        GeneratingReports --> COMPLETED : Exporters successfully compile
        GeneratingReports --> FAILED : Writer permission error
    }
    
    RUNNING --> CANCELLED : User clicks 'Cancel Job'
    
    FAILED --> [*] : Log error & write failure reason
    COMPLETED --> ARCHIVED : User deletes job database entry
    CANCELLED --> [*] : Clean temp storage files
    ARCHIVED --> [*] : Cascade delete database records
```

*   **Diagram Title**: Job Execution State Transition Diagram
*   **Purpose**: Details the states and transitions of analysis runs from initialization through completion or failure.
*   **Explanation**: When a user submits an analysis, the job state begins at `QUEUED`. A background worker thread picks up the job and moves it to `RUNNING`. If any validation gates fail or a tool subprocess crashes, the state transitions to `FAILED`. A user can manually transition the job to `CANCELLED`, which triggers cleanup routines to delete temporary run directories.

---

## DIAGRAM 13: PIPELINE STATUS TRACKER (SSE STREAMING)

```mermaid
sequenceDiagram
    autonumber
    actor Client as User Browser (React)
    participant Server as FastAPI Backend
    participant Worker as Background Thread
    participant SSE as Server-Sent Events (Stream)
    
    Client->>Server: POST /api/jobs/{job_id}/start
    Server->>Worker: Dispatch workflow execution
    Server-->>Client: 200 OK (Job status: RUNNING)
    
    Client->>Server: GET /api/jobs/{job_id}/stream
    Server-->>Client: Establish Persistent SSE Channel
    
    loop Sequential Execution
        Worker->>Worker: Run PipelineStep (e.g., fastp)
        Worker->>Server: Update step status in DB
        Server->>SSE: Emit 'message' event (e.g., "fastp:running")
        SSE-->>Client: Stream state update (Update UI progress bar)
        Worker->>Worker: Execute validation checks
        Note over Worker, Server: Step succeeded
        Worker->>Server: Update step completed
        Server->>SSE: Emit 'message' event (e.g., "fastp:completed")
        SSE-->>Client: Stream state update (Progress bar moves forward)
    end
    
    Worker->>Server: Finalize job status to COMPLETED
    Server->>SSE: Emit 'message' event (e.g., "pipeline:completed")
    SSE-->>Client: Stream final status
    Client->>Server: Close SSE Connection
```

*   **Diagram Title**: Real-time Status and Log Streaming sequence
*   **Purpose**: Illustrates the communication flow that powers the real-time terminal and pipeline steps tracker on the UI.
*   **Explanation**: The frontend communicates asynchronously with the backend. After starting a job, the client opens a Server-Sent Events (SSE) connection (`/api/jobs/{job_id}/stream`). As the background thread completes execution steps and updates the database, the server emits events over the SSE channel, updating the client's progress bars and terminal logs in real-time.

---

## DIAGRAM 14: AI INTERPRETATION ARCHITECTURE

```mermaid
graph TD
    Data[Pipeline Results JSON] --> Aggregator["Data Aggregator (ai_service.py)"]
    
    subgraph "Context Extraction"
        Aggregator --> Hits["Select top homologous hits (DIAMOND)"]
        Aggregator --> Domains["Extract identified Pfam domains"]
        Aggregator --> Tax["Extract taxonomic lineage info"]
        Aggregator --> PMIDs["Assemble retrieved PubMed abstracts"]
    end
    
    Hits & Domains & Tax & PMIDs --> PromptBuilder["Structured Prompt Compiler"]
    
    subgraph "Inference Orchestration"
        PromptBuilder --> ApiCheck{"Are API Keys Configured?"}
        
        ApiCheck --> |"Yes"| LLM["Gemini-1.5-Flash / GPT-4o Client"]
        ApiCheck --> |"No"| Fallback["Offline Rule-Based Summary Engine"]
        
        LLM --> Parser["JSON Schema Parser"]
        Parser --> Success{"Valid JSON Response?"}
        Success --> |"Yes"| Final["Grounded Pathobiology Interpretation"]
        Success --> |"No"| Fallback
    end
    
    Fallback --> Final
    Final --> DB["Save to database & Embed in Reports"]
```

*   **Diagram Title**: Hallucination-Resistant AI Interpretation Pipeline
*   **Purpose**: Details the construction, execution, and validation of AI-generated summaries.
*   **Explanation**: Implemented in `ai_service.py`. The AI engine extracts structured outputs from the pipeline runs (such as SwissProt homolog IDs and Pfam domains) and retrieved PubMed abstracts. It compiles these into a formatted prompt. If API credentials are configured, the system queries the model using structured JSON schemas to ensure reliable outputs. If no key is set or the model returns an invalid format, the system falls back to a rule-based offline summary.

---

## DIAGRAM 15: PUBMED LITERATURE MINING ARCHITECTURE

```mermaid
graph TD
    Start[Organism Name & Target Genes] --> QueryGen["Search Query Compiler"]
    
    subgraph "E-Utilities Pipeline"
        QueryGen --> ESearch["NCBI ESearch API (/esearch.fcgi)"]
        ESearch --> CacheCheck{"Are PMIDs cached in Local DB?"}
        
        CacheCheck --> |"Yes"| ReadCache["Load cached article abstracts"]
        CacheCheck --> |"No"| FetchAPI["NCBI EFetch API (/efetch.fcgi)"]
        
        FetchAPI --> Parse["XML Abstract and Metadata Parser"]
        Parse --> WriteCache["Cache articles in DB (pubmed_articles)"]
    end
    
    ReadCache & WriteCache --> LiteratureDashboard["Structured Literature Object"]
    LiteratureDashboard --> Output["UI Panel & AI Prompt Context"]
```

*   **Diagram Title**: Automated Literature Mining Pipeline
*   **Purpose**: Illustrates the search, retrieval, XML parsing, and database caching of PubMed records.
*   **Explanation**: Implemented in `pubmed_service.py`. The system builds search queries using the organism's scientific name and gene symbols. It queries the NCBI Entrez `/esearch.fcgi` API to retrieve a list of matching PMIDs. It then checks the local database to see if these abstracts are already cached. If they are not, it fetches the XML records using `/efetch.fcgi`, parses the metadata (authors, title, journal, publication date, abstract text), and caches the records in the database.

---

## DIAGRAM 16: REPORT GENERATION PIPELINE

```mermaid
graph TD
    Results[Job Results JSON] --> Aggregator["Data Aggregator"]
    Aggregator --> AI["Load AI Summary"]
    Aggregator --> PM["Load PubMed Abstracts"]
    Aggregator --> Plots["Load Matplotlib/Seaborn Plots"]
    
    AI & PM & Plots --> BaseReport["BaseReport Interface"]
    
    BaseReport --> HTMLWriter["HTML Exporter (html_report.py)"]
    BaseReport --> PDFWriter["PDF Exporter (pdf_report.py)"]
    BaseReport --> GFF3Writer["GFF3 Coordinate Exporter (gff3_report.py)"]
    BaseReport --> DataWriter["JSON / CSV Exporter"]
    
    subgraph "HTML Formatting"
        HTMLWriter --> StaticHTML["Self-contained responsive dashboard HTML"]
    end
    
    subgraph "PDF Rendering"
        PDFWriter --> Flowable["ReportLab flowable layout engine"]
        Flowable --> PrintablePDF["Print-ready PDF document"]
    end
    
    subgraph "Genomic Feature Mapping"
        GFF3Writer --> ReverseCheck{"Is ORF on reverse strand?"}
        ReverseCheck --> |"Yes"| Recalc["Recalculate coordinates based on gene boundaries"]
        ReverseCheck --> |"No"| WriteDirect["Write standard GFF3 features"]
        Recalc & WriteDirect --> OutputGFF["Assembled GFF3 File"]
    end
```

*   **Diagram Title**: Multi-Format Export Pipeline
*   **Purpose**: Documents the compilation of PDF, HTML, GFF3, and JSON/CSV reports.
*   **Explanation**: The reporting system takes results from the databases, appends AI summaries, PubMed articles, and static plots, and runs them through subclassed exporters. The GFF3 exporter maps predicted ORFs and Pfam domain structures back to genomic coordinates, recalculating alignments for reverse strand features using gene boundaries.

---

## DIAGRAM 17: VISUALIZATION ARCHITECTURE

```mermaid
graph TD
    subgraph "Backend Static Plot Generation (visualization_engine.py)"
        DataIn[Result Matrices] --> Matplotlib["Non-Interactive Matplotlib Backend (Agg)"]
        Matplotlib --> VolcanoMat["Volcano Plot (.png)"]
        Matplotlib --> MAMat["MA Plot (.png)"]
        Matplotlib --> GCWindow["GC Content Sliding Window (.png)"]
        Matplotlib --> PfamFreq["Pfam Domain Frequencies (.png)"]
    end
    
    subgraph "Frontend Interactive Visualization (Next.js UI)"
        DataJSON[JSON Results] --> Recharts["Recharts Component Library"]
        Recharts --> VolcInt["Interactive Volcano Plot"]
        Recharts --> DomainChart["Visual Domain Coordinate Map"]
        Recharts --> TaxTree["Dynamic Taxonomy Lineage Tree"]
    end

    VolcanoMat & MAMat & GCWindow & PfamFreq --> Storage["storage/jobs/JOB_ID/"]
    VolcInt & DomainChart & TaxTree --> UI["Interactive Client Workspace"]
```

*   **Diagram Title**: Hybrid Visualization Pipeline
*   **Purpose**: Showcases the separation between backend static image rendering and frontend interactive graphing.
*   **Explanation**: The system uses a hybrid model. The Python backend uses a non-interactive Matplotlib backend (`Agg`) to output static `.png` files directly into job storage for inclusion in PDF/HTML reports. The React frontend uses Recharts to render interactive plots with tooltips, dynamic coordinate maps, and expandable taxonomy trees using JSON data.

---

## DIAGRAM 18: DEPLOYMENT ARCHITECTURE

```mermaid
graph TD
    subgraph "Local WSL2 Development Setup (Ubuntu 22.04 LTS)"
        LocalUI[NextJS UI - port 3000] <--> |"SSE / JSON"| LocalAPI[FastAPI Server - port 8000]
        LocalAPI <--> |"SQLAlchemy"| LocalDB[(Local SQLite Database)]
        LocalAPI --> |"Subprocess run"| Binaries["Local Binaries (fastp, FastQC, SPAdes, HMMER, DIAMOND)"]
        LocalAPI --> |"Local Write"| LocalStore["Local storage/ Directory"]
    end
    
    subgraph "Production Deployment Setup"
        Vercel["Frontend - Vercel Serverless"] <--> |"JSON (CORS enabled)"| Render["Backend - Render Web Service"]
        Render <--> |"SQL"| Supabase[(PostgreSQL Instance)]
        Render --> |"Docker Container"| ProdBinaries["Preinstalled Docker Binaries"]
        Render --> |"Persistent Volume"| CloudStore["Mounted Block Storage"]
    end
    
    subgraph "External Cloud Services"
        LocalAPI & Render --> NCBI[NCBI Taxonomy & Entrez Web Services]
        LocalAPI & Render --> LLM[OpenAI / Gemini API Services]
    end
```

*   **Diagram Title**: Local vs. Production Cloud Deployments
*   **Purpose**: Details the architecture of the local WSL2 setup compared to a distributed cloud deployment.
*   **Explanation**: Locally, the project runs under WSL2 with Next.js on port 3000 communicating with FastAPI on port 8000 using SQLite. In production, the Next.js frontend is deployed to Vercel, and the FastAPI backend is packaged inside a Docker container (pre-loading bioinformatic tools) on Render. The backend connects to a PostgreSQL instance on Supabase and uses mounted block storage to write run directories.

---

## DIAGRAM 19: DETAILED DIRECTORY STRUCTURE

```mermaid
graph TD
    Root["FUNCTIONAL GENOMICS PROJECT / (Root Workspace)"]
    
    Root --> Backend["backend/ (FastAPI Application)"]
    Backend --> API["api/ (HTTP Routers: upload, jobs, reports, settings)"]
    Backend --> Config["config/ (settings.py, thresholds.yaml, tool_paths.yaml)"]
    Backend --> Core["core/ (deg_engine, orf_finder, qc_engine, translator, visualization_engine)"]
    Backend --> DBDir["database/ (SQLAlchemy connection pool and repositories)"]
    Backend --> Models["models/ (SQL schemas: users, jobs, results, pubmed, ai)"]
    Backend --> Pipelines["pipeline/ (pipeline_runner.py, workflow_fasta, workflow_fastq, workflow_deg)"]
    Backend --> Reports["reports/ (base_report, html_report, pdf_report, gff3_report)"]
    Backend --> Services["services/ (ai, diamond, fastp, fastqc, hmmer, kegg, ncbi, pubmed)"]
    
    Root --> Frontend["frontend/ (Next.js Application)"]
    Frontend --> App["app/ (Routing pages: workspace, dashboard, settings, reports)"]
    Frontend --> Components["components/ (AIReport, DomainViewer, Terminal, VolcanoPlot, Sidebar)"]
    Frontend --> Service["services/ (Axios client: api.ts)"]
    
    Root --> Store["storage/ (Local Run Outputs, logs, and report pdfs)"]
    Root --> TestData["test_data/ (Validation FASTQ, FASTA, and DEG expression lists)"]
    Root --> Tests["tests/ (Unit and Integration testing scripts)"]
    
    style Backend fill:#fcf,stroke:#333,stroke-width:1px
    style Frontend fill:#cff,stroke:#333,stroke-width:1px
```

*   **Diagram Title**: System Codebase Directory Structure
*   **Purpose**: Visualizes the organization of folders and code files within the workspace.
*   **Explanation**: The workspace is structured into a clean monorepo. The `backend/` directory isolates biological calculations and services, the `frontend/` directory isolates Next.js components and user interfaces, `storage/` manages runtime artifacts, and `test_data/` holds reference datasets for validation.

---

## DIAGRAM 20: COMPLETE END-TO-END USER JOURNEY

```mermaid
sequenceDiagram
    autonumber
    actor User as Researcher (Browser)
    participant UI as NextJS UI (React)
    participant Server as FastAPI Server
    participant Runner as Pipeline Runner
    participant Core as Biological Core
    participant CLI as Bio Tools (fastp, HMMER)
    participant Cloud as Web APIs (NCBI, Gemini)
    participant DB as SQLite / PostgreSQL
    
    User->>UI: Logs in & Opens Workspace Page
    UI->>Server: GET /api/settings (Check API Connection Status)
    Server-->>UI: Return Key Availability
    
    User->>UI: Drag-and-drops raw FASTQ file
    UI->>Server: POST /api/upload (Stream uploaded file)
    Server->>Server: Detect File Format (Validates raw FASTQ reads)
    Server-->>UI: Returns Upload ID & Auto-detected Type (FASTQ)
    
    User->>UI: Clicks 'Start Analysis'
    UI->>Server: POST /api/jobs/{job_id}/start
    Server->>DB: Write Job (status: QUEUED) & Step records (PENDING)
    Server->>Runner: Dispatch Worker Thread
    Server-->>UI: Return job started confirmation
    
    UI->>Server: GET /api/jobs/{job_id}/stream (Establish SSE connection)
    Server-->>UI: SSE Channel Connected
    
    Note over Runner, CLI: Execute Quality Control & Assembly
    Runner->>DB: Update Step 1 (FastQC: RUNNING)
    Server->>UI: Stream Event: 'FastQC running'
    Runner->>CLI: run_fastqc subprocess
    CLI-->>Runner: Return raw quality reports
    
    Runner->>DB: Update Step 2 (fastp: RUNNING)
    Server->>UI: Stream Event: 'fastp running'
    Runner->>CLI: run_fastp subprocess
    CLI-->>Runner: Return adapter-trimmed FASTQ reads
    
    Runner->>DB: Update Step 3 (SPAdes: RUNNING)
    Server->>UI: Stream Event: 'SPAdes assembly running'
    Runner->>CLI: run_spades --rnaviral
    CLI-->>Runner: Return assembled contigs (FASTA)
    
    Note over Runner, Cloud: Chained Gene Annotation & Annotation
    Runner->>Core: Scan contigs in 6 reading frames (orf_finder.py)
    Core-->>Runner: Return predicted ORFs and translation sequences
    
    Runner->>CLI: run_diamond blastp against SwissProt & run_hmmscan Pfam
    CLI-->>Runner: Return homologous proteins and functional domains
    
    Runner->>Cloud: Query NCBI Taxonomy & KEGG pathways
    Cloud-->>Runner: Return viral lineage and pathway descriptions
    
    Runner->>Cloud: Build literature search & query PubMed abstracts
    Cloud-->>Runner: Return PubMed articles (Cache in DB)
    
    Runner->>Cloud: Build pathobiology prompt & trigger Gemini AI
    Cloud-->>Runner: Return structured pathology interpretation
    
    Note over Runner, Server: Compile Outputs & Complete Job
    Runner->>Core: Generate static charts (Volcano/QC plots)
    Runner->>Core: Compile GFF3 coordinates & PDF files
    Runner->>DB: Update Job status to COMPLETED
    Server->>UI: Stream Event: 'Job Completed'
    
    UI->>Server: GET /api/jobs/{job_id}/results
    Server-->>UI: Return completed result package (JSON)
    UI->>UI: Populate dashboard charts, tables, and AI summary tabs
    
    User->>UI: Clicks 'Download PDF Report'
    UI->>Server: GET /api/reports/{job_id}/download/pdf
    Server-->>User: Stream generated PDF document
```

*   **Diagram Title**: System End-to-End User Journey Sequence
*   **Purpose**: A comprehensive visualization mapping the entire lifecycle of a user-initiated FASTQ run.
*   **Explanation**: This sequence diagram walks through the complete workflow of a FASTQ run. It shows how the user interface, backend routers, thread orchestrators, subprocess command-line tools, external APIs, and local databases work together to process raw sequencing reads and produce clean, annotated reports.
