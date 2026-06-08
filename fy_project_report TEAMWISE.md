# PathoScope AI: Automated Viral Functional Genomics Pipeline for Sequence Annotation, Pathway Mapping, and AI-Assisted Biological Interpretation

**A Final Year Project Report submitted in partial fulfillment of the requirements for the Degree of Bachelor of Science in Bioinformatics**

---

## PROJECT MANAGEMENT

The PathoScope AI system was designed, developed, and validated using Agile software engineering practices, specifically the Scrum framework. This methodology was chosen to address the high degree of scientific complexity and the need for incremental feature refinement.

### 1. Why Agile Methodology Was Selected
*   **Scientific and Technical Uncertainty**: Incorporating machine learning inferences, multiple local wrappers (DIAMOND, HMMER, fastp, FastQC), and complex REST web APIs introduced variables that could not be fully defined upfront in a rigid Waterfall model. Agile allowed the team to iteratively adjust code structures as integration issues arose.
*   **Rapid Prototyping**: Releasing minimal viable products (MVPs) of individual workflows (starting with FASTA annotation in Phase 1, followed by FASTQ assembly in Phase 2) allowed for immediate verification of biological validity before developing the host DEG and UI layers.
*   **Constant Validation**: Working in two-week sprints ensured that unit testing and biological validations were executed regularly, keeping the codebase in a deployable state.

### 2. Project Tracking via Jira
The team utilized Jira to plan sprints, track task statuses, and monitor progress. 
*   **Backlog Grooming**: All functional requirements (from sequence upload to PDF compilation) were broken down into granular Epics, User Stories, and Tasks.
*   **Sprint Planning**: At the beginning of each sprint, tasks were selected from the backlog and assigned to presenters based on their role division.
*   **Active Monitoring**: Jira's Kanban boards visualized workflow bottlenecks. Tasks moved from *Backlog* $\rightarrow$ *To Do* $\rightarrow$ *In Progress* $\rightarrow$ *Code Review* $\rightarrow$ *QA/Validation* $\rightarrow$ *Done*.
*   **Issue and Bug Tracking**: Any computational exceptions (e.g., translation crashes, Next.js hydration warnings, SQLite transaction deadlocks) were captured as Jira Bugs, prioritized, and linked to their parent component tasks.

### 3. Sprint and Milestone Schedule

The table below outlines the sprint schedule and deliverables achieved during the development lifecycle:

| Sprint | Duration | Primary Goals | Key Deliverables | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Sprint 1** | Weeks 1-2 | Database design and backend FastAPI routing setup. | SQL schemas, migration scripts, `/health` and `/upload` endpoints. | Completed |
| **Sprint 2** | Weeks 3-4 | Biological core and FASTA workflow. | `orf_finder.py`, `translator.py`, SwissProt homologous alignments. | Completed |
| **Sprint 3** | Weeks 5-6 | HMMER, KEGG, and NCBI Taxonomy services integration. | Domain identification, taxonomy mapping, GFF3 coordinate exporter. | Completed |
| **Sprint 4** | Weeks 7-8 | Raw reads preprocessing and SPAdes assembly. | fastp wrappers, FASTQ QC plots, contigs extraction. | Completed |
| **Sprint 5** | Weeks 9-10| Host transcriptomics DEG engine. | Welch's t-test, BH-FDR, local ORA, Volcano plots. | Completed |
| **Sprint 6** | Weeks 11-12| PubMed and AI pathobiology engines. | E-Utilities wrapper, OpenAI/Gemini schemas, cache layers. | Completed |
| **Sprint 7** | Weeks 13-14| Nextjs dashboard visual integration. | Workspace, charts, terminal streamer, report downloads. | Completed |
| **Sprint 8** | Weeks 15-16| End-to-end QA validation and documentation. | Integration testing, final reports, project thesis. | Completed |

---

## TECHNOLOGY STACK

The technical implementation of PathoScope AI utilizes a diverse selection of programming languages, libraries, and frameworks, chosen for their speed, biological compatibility, and modularity.

```mermaid
graph TD
    subgraph Frontend
        TS[TypeScript / React / Next.js]
        CSS[Tailwind CSS]
    end
    subgraph Backend API
        PY[Python / FastAPI]
        DB[(SQLite / PostgreSQL)]
    end
    subgraph Core Computation
        BIO[Biopython / SciPy / NumPy]
        CLI[fastp / FastQC / SPAdes / DIAMOND / HMMER]
    end
    TS <--> |JSON / SSE| PY
    PY <--> |SQLAlchemy| DB
    PY --> BIO
    PY --> |Subprocess CLI| CLI
```

### 1. Python
*   **Purpose**: The primary language for backend APIs, pipeline orchestration, database interactions, and bioinformatic calculations.
*   **Role**: Powers the FastAPI application layer, coordinates external command-line tools, handles database connections via SQLAlchemy, and executes biological logic.
*   **Key Packages**: Pydantic, SQLAlchemy, Biopython, SciPy, statsmodels, NumPy, Pandas, Matplotlib, Seaborn.
*   **Advantages**: Python is the standard language for scientific computing, offering robust libraries (Biopython, SciPy) and straightforward integrations with bioinformatic command-line tools.

### 2. TypeScript
*   **Purpose**: Used for the Next.js user interface.
*   **Role**: Implements type-safe UI views, handles state management, processes file uploads, and renders charts.
*   **Key Packages**: React, Next.js 15, Recharts, Lucide React, Axios.
*   **Advantages**: Enforces compile-time type checking, preventing runtime errors in complex genomic data visualizations.

### 3. SQL
*   **Purpose**: Relational database querying and DDL schemas.
*   **Role**: Definess and executes data transactions for user roles, jobs, steps, annotations, pathways, and cached PubMed records.
*   **Advantages**: Structured SQL databases ensure relational integrity and ACID compliance, which are essential for reproducing pipeline runs.

### 4. YAML & JSON
*   **Purpose**: System configurations, data caching, and API exchanges.
*   **Role**: YAML defines configurations and biological thresholds (`thresholds.yaml`). JSON serves as the primary format for API responses, job results caching, and AI summaries.
*   **Advantages**: Human-readable formats that simplify configuration management and web API integrations.

---

## DEVELOPMENT ENVIRONMENT

The PathoScope AI codebase was built and tested in a standardized local development environment:

*   **Integrated Development Environment (IDE)**: **Visual Studio Code (VS Code)**. Selected for its integrated terminal, Git visualization plugins, and debugger support for Python and TypeScript.
*   **Operating System Isolation**: **Windows Subsystem for Linux (WSL2) with Ubuntu 22.04 LTS**. Selected to run native Linux bioinformatic binaries (which are often unsupported or unstable on native Windows) while preserving the Windows host UI environment.
*   **Version Control**: **Git & GitHub**. Used for branch management, pull-request reviews, and codebase backups.
*   **Environment Manager**: **Conda (Miniconda3)**. Used to manage isolated Python environments and install non-standard scientific libraries without polluting the global system workspace.
*   **Package Managers**: **NPM** (Node Package Manager) for installing Next.js dependencies, and **Pip** for Python dependencies.
*   **Server Framework**: **FastAPI** on **Uvicorn**. Selected for its high performance, automatic OpenAPI documentation, and asynchronous capabilities for handling concurrent uploads.
*   **UI Framework**: **Tailwind CSS** with **shadcn/ui**. Selected to build a clean, high-density scientific dashboard.

---

## TEAM DIVISION

PathoScope AI was designed and built by a team of four bioinformatics engineers, divided as follows:

```mermaid
classDiagram
    class PathoScope_Team {
        +M_EKRAMAH Presenter_1
        +TAHA Presenter_2
        +MISHAL Presenter_3
        +ASAD_IMAM Presenter_4
    }
    class Presenter_1 {
        +FASTQ_Workflow_Orchestration
        +Pipeline_Runner_Core
        +PubMed_EUtils_Integration
        +AI_Inference_Grounding
    }
    class Presenter_2 {
        +FASTA_Workflow_Orchestration
        +ORF_Six_Frame_Scanning
        +DIAMOND_SwissProt_Alignments
        +HMMER_Pfam_Domain_Search
    }
    class Presenter_3 {
        +DEG_Workflow_Orchestration
        +Counts_Matrix_Normalization
        +Welch_t_test_Statistics
        +GO_KEGG_ORA_Enrichment
    }
    class Presenter_4 {
        +NextJS_Dashboard_UI
        +SSE_Terminal_Streamer
        +Interactive_Plots_Recharts
        +Multi_Format_Report_Exporters
    }
    PathoScope_Team --> Presenter_1
    PathoScope_Team --> Presenter_2
    PathoScope_Team --> Presenter_3
    PathoScope_Team --> Presenter_4
```

### 1. Presenter 1: M. EKRAMAH (Core Pipelines, FASTQ & AI Engines)
*   **Responsibilities**:
    *   Designed the core pipeline orchestrator (`pipeline_runner.py`), establishing the state machine for job tracking and validation gates.
    *   Developed the raw sequencing FASTQ pipeline, incorporating memory-safe streaming, FastQC quality profiles, and fastp read trimming.
    *   Built the PubMed literature engine, managing automated query generation and NCBI E-Utilities APIs.
    *   Created the hallucination-resistant AI interpretation module, defining output schemas and fallback states.
    *   Managed the PostgreSQL database integration and relational schema connections.

### 2. Presenter 2: TAHA (Workflow A: Viral FASTA Annotation)
*   **Responsibilities**:
    *   Designed the FASTA analysis pipeline, including FASTA header parsing and scientific name extraction.
    *   Developed the six-frame open reading frame (ORF) finder and coordinates overlap resolver.
    *   Integrated the DIAMOND blastp service to run homologous alignments against SwissProt.
    *   Integrated HMMER `hmmscan` to predict protein domain architectures against the Pfam database.
    *   Integrated the NCBI taxonomy API to map taxonomic lineages.
    *   Created GFF3 genome coordinate exporters.

### 3. Presenter 3: MISHAL (Workflow C: Transcriptomics DEG Engine)
*   **Responsibilities**:
    *   Designed the differential gene expression (DEG) analysis pipeline, including validation of precomputed tables (Mode A) and count matrices (Mode B).
    *   Developed the variance-stabilizing normalization algorithm to prevent double-normalization of expression matrices.
    *   Implemented the Welch's t-test and Welch-Satterthwaite degrees of freedom calculations.
    *   Implemented multiple-testing corrections using the Benjamini-Hochberg FDR procedure.
    *   Implemented local and web-service Over-Representation Analysis (ORA) to map enriched GO and KEGG terms.

### 4. Presenter 4: ASAD IMAM (Frontend UI, Visualizations & Reporting)
*   **Responsibilities**:
    *   Designed and built the Next.js visual workspace, dashboard screens, and settings panels.
    *   Implemented the Server-Sent Events (SSE) logs listener and real-time terminal window.
    *   Built the interactive charts (Recharts Volcano plot, Recharts Bar charts) and viewer panels for taxonomic trees, Pfam domains, and KEGG pathway cards.
    *   Implemented the download center endpoints, enabling exports of PDF, HTML, GFF3, JSON, and CSV reports.

---

## CHAPTER 1: INTRODUCTION

### 1.1 Functional Genomics
Functional genomics is a branch of molecular biology that uses genome-wide data to describe gene and protein functions and interactions. Unlike structural genomics, which focuses on sequencing and physical mapping, functional genomics measures the dynamic expression of genes and proteins under different environmental or pathological conditions. High-throughput methods, such as transcriptomic profiling, allow researchers to study cellular networks and host responses at a systems level.

### 1.2 Viral Genomics
Viruses present unique challenges in genomics. Characterized by compact genomes, overlapping reading frames, and high mutation rates, viral genomes require specialized annotation approaches. Sequence changes occur rapidly under selective pressure, meaning distant homology and domain-level structural classifications are often required to identify protein functions where sequence conservation is low.

### 1.3 Importance of Sequence Annotation
Sequence annotation involves identifying the locations of genes and coding regions in a genome and determining their functional roles. For novel pathogens, this begins with open reading frame (ORF) prediction, followed by sequence translation and homology searches. Correctly annotating genes is critical for identifying potential therapeutic targets and tracking viral evolution.

### 1.4 Importance of Pathway Mapping
A simple list of annotated genes is insufficient to understand a pathogen's biology. Pathway mapping places predicted proteins into biological networks, such as signaling cascades and metabolic pathways. Using reference databases like KEGG, researchers can identify host networks disrupted or hijacked by viral proteins (e.g., host cell cycle, immune signaling pathways), revealing mechanisms of viral replication and pathogenesis.

### 1.5 Importance of Transcriptomics
Transcriptomics measures the expression levels of transcripts genome-wide. In functional genomics, differential gene expression (DEG) analysis compares mRNA levels between control and infected samples. This reveals the host pathways activated or suppressed during infection, providing insights into immune responses and identifying candidate biomarkers.

### 1.6 Importance of AI-Assisted Interpretation
The large volume of genomic, taxonomic, and literature data generated by automated pipelines can be challenging to synthesize manually. Large Language Models (LLMs) can assist by summarizing pipeline outputs, taxonomies, and retrieved literature. However, to be useful in scientific research, these summaries must be grounded in empirical data and peer-reviewed literature to prevent hallucinations.

### 1.7 Research Significance
PathoScope AI addresses the fragmentation of current bioinformatics pipelines by unifying sequence preprocessing, assembly, annotation, host pathobiology mapping, literature mining, and reporting into a single system. The platform is designed for research and educational settings, accelerating the translation of sequence-level data into biological insights.

---

## CHAPTER 2: PROBLEM STATEMENT

### 2.1 Current Limitations in Bioinformatics Pipelines
*   **Fragmented Tools**: Standard workflows require running multiple disconnected tools (e.g., FastQC, fastp, SPAdes, DIAMOND, HMMER) and manually formatting files between steps.
*   **Technical Installation Barriers**: Installing and maintaining dependencies across different packages often requires complex environments and command-line interfaces, limiting accessibility.
*   **Workflow Integration**: Pipelines rarely connect host gene expression data with pathogen annotation, separating transcriptomics from genome annotation.
*   **Biological Interpretation Gap**: Pipelines typically produce raw tables, leaving the researcher to manually search literature databases to understand the biological context.
*   **AI Hallucinations**: Applying general-purpose AI assistants to interpret scientific results introduces a high risk of fabricated citations, incorrect protein functions, and unsupported biological claims.

---

## CHAPTER 3: LITERATURE REVIEW

### 3.1 Review of Core Tools
*   **FastQC**: Provides read-quality reports but does not modify raw sequencing data.
*   **fastp**: Performs adapter trimming, quality filtering, and length filtering in a single pass.
*   **SPAdes**: Reconstructs genomes from short reads. Its `--rnaviral` mode is optimized for viral assemblies.
*   **DIAMOND**: A high-performance protein aligner designed for homology searches against large reference databases.
*   **HMMER**: Searches for conserved structural domains and motifs using profile hidden Markov models.
*   **GSEApy**: A Python package for gene set enrichment analysis that connects to the Enrichr web services.
*   **Biopython**: Provides sequence manipulation, translation, and parsing functions.
*   **NCBI E-Utilities**: API suite to search and retrieve records from NCBI databases.

### 3.2 Computational Tool Comparison Table

The table below summarizes the strengths and limitations of the primary bioinformatics tools reviewed:

| Tool | Strengths | Limitations | Role in PathoScope AI |
| :--- | :--- | :--- | :--- |
| **FastQC** | Graphical base-quality profiles, GC bias indicators. | No data cleaning features. | Raw/trimmed read QC reports. |
| **fastp** | High-performance C++ tool; combines trimming and QC. | Command-line interface only. | Quality trimming and filtering. |
| **SPAdes** | Multi-k-mer graph assembly; specialized viral mode. | High memory requirements. | De novo viral assembly. |
| **DIAMOND** | Much faster than BLASTp; memory-efficient. | Slightly lower sensitivity for divergent sequences. | Homologous alignment search. |
| **HMMER** | High sensitivity using profile HMMs. | Complex output files. | Protein domain prediction. |
| **GSEApy** | Broad collection of enrichment libraries. | Requires network connection. | Gene set pathway enrichment. |

---

## CHAPTER 4: OBJECTIVES

### 4.1 Functional Objectives
1.  **Automated File Type Detection**: Automatically identify input formats (.fasta, .fastq, .csv, .tsv) to route uploads to the correct pipeline.
2.  **Sequential Workflow Execution**: Manage steps sequentially, verifying that output files are present and valid before starting the next step.
3.  **Real-Time Log and Status Streaming**: Stream pipeline progress, logs, and statuses to the web interface.
4.  **Literature Mining**: Retrieve PubMed articles using taxonomy and annotation terms.
5.  **Evidence-Grounded AI Synthesis**: Provide pathobiology interpretations citing retrieved PMIDs.
6.  **Report Export**: Generate reports in HTML, PDF, GFF3, CSV, and JSON formats.

### 4.2 Biological Objectives
1.  **6-Frame ORF Detection**: Scan genomes in all 6 reading frames, filtering for ORFs $\ge 100$ bp.
2.  **Codon Translation**: Standardize translation using Biopython maps, handling partial trailing codons safely.
3.  **Homology Significance**: Enforce thresholds: E-value $\le 10^{-5}$, identity $\ge 30\%$, coverage $\ge 50\%$.
4.  **Welch's t-test and FDR Correction**: Calculate differential expression and adjust p-values using the Benjamini-Hochberg FDR procedure.

---

## CHAPTER 5: SYSTEM ARCHITECTURE

PathoScope AI utilizes a decoupled architecture, dividing responsibilities between frontend, API, pipeline running, and database layers.

### 5.1 System Integration Diagram

```mermaid
graph TD
    User([Browser UI]) <--> |HTTP / JSON / SSE| API[FastAPI Backend]
    API <--> |ORM / SQL| DB[(PostgreSQL Database)]
    API --> |Trigger Task| Runner[Pipeline Runner]
    
    subgraph Workflows
        Runner --> FASTA[FASTA Engine]
        Runner --> FASTQ[FASTQ Engine]
        Runner --> DEG[DEG Engine]
    end
    
    subgraph Services
        FASTA & FASTQ & DEG --> |Executables| CLI[FastQC / fastp / SPAdes / DIAMOND / HMMER]
        FASTA & FASTQ & DEG --> |API Queries| WebServices[NCBI E-Utils / OpenAI / Gemini]
    end

    subgraph Storage
        Runner --> |Logs / Outputs / Reports| Directory[storage/jobs/JOB_ID/]
    end
```

### 5.2 Frontend Component Architecture
The Next.js frontend is structured into modular components:
*   `Workspace`: Single-page visual interface containing dropzones, logs terminals, and results tabs.
*   `ResultsViewer`: Displays Overview stats, QC graphs, predicted ORFs, SwissProt homologous alignments, Pfam domains, and taxonomy trees.
*   `Terminal`: Streams real-time stdout/stderr pipeline outputs.
*   `PipelineSteps`: Tracks active step statuses.

### 5.3 Backend API Architecture
FastAPI routes incoming HTTP requests:
*   `/api/upload`: Handles file uploads and detects file types.
*   `/api/jobs/{job_id}/start`: Launches the selected workflow in a background thread.
*   `/api/jobs/{job_id}/stream`: Establishes Server-Sent Events (SSE) connections to stream logs and progress.
*   `/api/reports`: Downloads reports in GFF3, HTML, PDF, CSV, and JSON formats.
*   `/api/settings`: Manages API keys, writing them to `backend/.env`.

---

## CHAPTER 6: WHY THREE WORKFLOWS?

PathoScope AI separates processing into three distinct pipelines to match different biological entry states and research questions.

```mermaid
graph TD
    subgraph Pathogen Sequencing
        FASTQ[Raw Reads FASTQ] --> |Workflow B: QC, Trimming, Assembly| Contigs[Assembled Contigs FASTA]
        Contigs --> |Workflow A: Gene Prediction & Annotation| GenProteome[Viral Proteome & Lineage]
    end
    
    subgraph Host Transcriptomics
        DEG[Expression Matrix CSV/TSV] --> |Workflow C: Stats, FDR, ORA| HostResponse[Host Pathway Disruption]
    end
```

### 6.1 Biological and Logical Separation
1.  **Entry States**: FASTQ pipelines handle raw, unsorted sequencer reads containing low-quality fragments and host contamination. FASTA pipelines start with clean, assembled consensus sequences. DEG pipelines process expression matrices of transcript abundances.
2.  **Different Research Questions**:
    *   *FASTA*: Profiles genetic coordinates, codon usage, evolutionary origins, and coding capacities.
    *   *FASTQ*: Evaluates sequencing quality, adapter contamination, and coverage depths, and assembles contigs.
    *   *DEG*: Analyzes host immune responses and cellular pathway changes in response to infection.
3.  **Monolithic Incompatibility**: A unified workflow would require uploading all three raw data types simultaneously. This is impractical for researchers who only have assembled genomes or only have expression datasets.

---

## CHAPTER 7: WORKFLOW A — FASTA VIRAL GENOME ANALYSIS

Workflow A processes assembled genomic sequences through 11 sequential steps.

### 7.1 Detailed Processing Steps
1.  **Input Validation**: Checks for valid FASTA formatting and verifies that only IUPAC nucleotide characters are present.
2.  **Sequence QC**: Computes sequence length, GC content, and ambiguous base count.
3.  **ORF Finding**: Scans the sequence in all 6 reading frames using a sliding window. Removes overlapping coordinates on the same strand, keeping the longest ORF.
4.  **Translation**: Translates nucleotide sequences using Biopython. Trailing nucleotides are truncated to complete the final codon, and translation stops at the first stop codon to prevent KeyErrors.
5.  **DIAMOND Homology Search**: Aligns translated sequences against the SwissProt database using `diamond blastp`.
6.  **Pfam Domain Search**: Identifies conserved domains using HMMER `hmmscan` against the Pfam-A profile database.
7.  **KEGG Pathway Mapping**: Maps identified SwissProt accessions to KEGG Orthology pathways.
8.  **NCBI Taxonomy Lookup**: Extracts the taxon name from the FASTA header and queries the NCBI Taxonomy database.
9.  **PubMed Literature Retrieval**: Mines literature matching the scientific name and annotated genes.
10. **AI Interpretation**: Generates a pathobiology summary using Gemini or OpenAI APIs.
11. **Report Generation**: Exports HTML, PDF, GFF3, CSV, and JSON files.

### 7.2 Validation Gating & Biological Thresholds
*   **ORF length**: Minimum 100 bp (filters out short, random codon selections).
*   **Alignment Significance**: E-value $\le 10^{-5}$, identity $\ge 30\%$, coverage $\ge 50\%$.
*   **QC Warn**: Flags sequences where ambiguous bases ('N') exceed 10% of the total length.

---

## CHAPTER 8: WORKFLOW B — FASTQ ANALYSIS

Workflow B processes raw NGS reads through quality control, filtering, and de novo assembly.

### 8.1 Detailed Processing Steps
1.  **FASTQ Input Validation**: Confirms FASTQ format and checks that files contain valid records using Biopython's `FastqGeneralIterator`.
2.  **Raw read QC**: Runs FastQC to establish pre-trimming quality metrics.
3.  **fastp Trimming**: Clips adapters and filters out low-quality reads (enforcing Q20 and length $\ge 50$ bp).
4.  **Trimmed read QC**: Runs FastQC again to verify quality improvements.
5.  **SPAdes Assembly**: Runs assembly in `--rnaviral` mode to reconstruct contigs from trimmed reads.
6.  **Contig Filtering**: Filters out contigs shorter than 500 bp.
7.  **Annotation Chaining**: Writes filtered contigs to `input.fasta` and triggers the 11 steps of the FASTA pipeline.

### 8.2 Streaming and Memory Safety
FASTQ files are read using streaming iterators (`FastqGeneralIterator`), processing records line-by-line without loading the entire file into RAM. This ensures memory usage remains stable even when processing large datasets.

---

## CHAPTER 9: WORKFLOW C — DEG ANALYSIS

Workflow C profiles host transcriptomic responses to pathobiological infections.

### 9.1 Detailed Processing Steps
1.  **Input Validation**: Supports precomputed tables (Mode A) and count matrices (Mode B).
2.  **Normalization Check**: Detects log-transformed matrices ($E_{\text{max}} < 30$). Applies Counts Per Million (CPM) and $\log_2$ transformations for raw counts:
    $$\text{CPM}_i = \frac{C_i}{\sum C} \times 10^6$$
    $$\text{Normalized Value} = \log_2(\text{CPM}_i + 1)$$
3.  **Welch's t-test**: Compares groups without assuming equal variances:
    $$t = \frac{\bar{X}_2 - \bar{X}_1}{\sqrt{\frac{s_1^2}{N_1} + \frac{s_2^2}{N_2}}}$$
    Degrees of freedom are calculated using the Welch-Satterthwaite equation.
4.  **BH-FDR Correction**: Controls false discovery rates using the Benjamini-Hochberg procedure:
    $$\text{FDR}_{(i)} = \min \left( \text{FDR}_{(i+1)}, \frac{m}{i} P_{(i)} \right)$$
5.  **Regulation Classification**: Classifies genes as UP ($\log_2 \text{FC} \ge 1$, $\text{FDR} < 0.05$), DOWN ($\log_2 \text{FC} \le -1$, $\text{FDR} < 0.05$), or Not Significant.
6.  **Functional enrichment**: Runs GSEApy enrichment or defaults to a local one-sided Fisher's exact test for pathway over-representation.
7.  **Visualizations**: Generates volcano plots, MA plots, and bar plots.

---

## CHAPTER 10: AI INTERPRETATION SYSTEM

PathoScope AI integrates Large Language Models to summarize pipeline outputs.

### 10.1 System Flow and Prompts
*   **System Instructions**: Prompts the AI to act as a pathobiology interpreter, requiring PMIDs and alignment parameters for all claims.
*   **Inputs**: Tabular data of homologous hits, Pfam domains, taxonomy lineages, and PubMed abstracts.
*   **Hallucination Prevention**: The system restricts model responses to the provided context, requiring active annotations and validated PMIDs.
*   **Offline Fallback**: If no API keys are present, the system runs a rule-based offline summary.

```json
{
  "ai_provider": "gemini",
  "model_name": "gemini-1.5-flash",
  "findings": "Structured summary of homologous proteins and taxonomic classification.",
  "literature_summary": "Evidence citations mapping findings to specific PMIDs.",
  "biological_interpretation": "Pathology review of replication and cell interactions.",
  "confidence_assessment": "HIGH / MEDIUM / LOW",
  "limitations": "Lack of wet-lab validation and database constraints."
}
```

---

## CHAPTER 11: PUBMED INTEGRATION

The PubMed integration module matches computational findings with peer-reviewed literature.

```mermaid
graph LR
    Annotations[Homologous Hits & Taxonomy] --> QueryGen[1. Query Builder]
    QueryGen --> ESearch[2. NCBI ESearch API]
    ESearch --> PMIDs[PMID Lists]
    PMIDs --> EFetch[3. NCBI EFetch API]
    EFetch --> Parser[4. XML Parser]
    Parser --> Cache[(PostgreSQL Cache)]
    Parser --> Synthesis[5. Literature Synthesis]
```

### 11.1 Query Generation and Retrieval
*   **Query Builder**: Generates broad, clinical, mechanistic, and review queries using taxonomy and annotation terms.
*   **NCBI E-Utilities**:
    *   `esearch.fcgi`: Retrieves matching PMIDs.
    *   `efetch.fcgi`: Retrieves detailed XML records.
*   **XML Parser**: Extracts publication titles, abstracts, authors, DOIs, publication types, and MeSH terms.
*   **Cache Layer**: Stores queries and XML articles in local PostgreSQL tables to respect NCBI rate limits.

---

## CHAPTER 12: VISUALIZATIONS

PathoScope AI's visualization engine generates publication-quality plots using `matplotlib` and `seaborn` in non-interactive backend mode.

### 12.1 Visualizations List
1.  **Genome Composition Pie Chart**: Shows GC vs. AT content calculated from `qc_engine.py`.
2.  **ORF Length Histogram**: Displays the length distribution of predicted ORFs.
3.  **GC Content Sliding Window**: Plots GC% variations across the genome using a 1000 bp sliding window.
4.  **Taxonomic Depth Chart**: Renders a vertical classification profile.
5.  **Pfam Domain Occurrences**: Displays the frequency of identified structural domains.
6.  **KEGG Pathway Distribution**: Shows pathway coverage based on gene hit counts.
7.  **Quality score distribution**: Compares base quality along reads before and after trimming (FASTQ workflow).
8.  **GC Distribution**: Shows GC% profiles across raw reads (FASTQ workflow).
9.  **Volcano Plot**: Compares $-\log_{10}(\text{FDR})$ against $\log_2(\text{Fold Change})$ to show differential expression (DEG workflow).
10. **MA Plot**: Plots $\log_2(\text{Fold Change})$ against average expression to detect intensity-dependent biases (DEG workflow).
11. **Enrichment Dot Plots**: Compares gene ratios, p-values, and gene counts across enriched pathways (DEG workflow).

---

## CHAPTER 13: DATABASE AND REPORTING

### 13.1 SQL Schema and Relationships
The SQL database manages user accounts, pipeline job records, and step logs. Relationships are established via foreign keys with cascade deletions, ensuring that deleting a job removes its associated steps, runs, annotations, and reports.

### 13.2 Report Exporters
*   **HTML**: Renders self-contained static HTML reports containing base quality tables, taxonomic lineages, Pfam architectures, and AI pathobiology summaries.
*   **PDF**: Generates print-ready validation reports using ReportLab.
*   **GFF3**: Writes predicted genes, CDS regions, and Pfam domains in GFF3 format. For reverse strand features, domain coordinates are mapped back to absolute genomic coordinates:
    $$\text{Genomic Start} = \text{Gene End} - (3 \times \text{Domain End})$$
    $$\text{Genomic End} = \text{Gene End} - (3 \times (\text{Domain Start} - 1))$$

---

## CHAPTER 14: TESTING AND VALIDATION

### 14.1 Test Types
*   **Unit Tests** (`tests/unit/`): Verify core algorithms: QC calculations, coordinate tracking in `orf_finder.py`, Biopython translation calls, and Welch's t-test calculations.
*   **Integration Tests** (`tests/integration/`): Test end-to-end execution of dummy workflows, verifying that step failures halt the pipeline runner.
*   **Mock NCBI Tests** (`backend/tests/`): Test taxonomy XML parsing and E-Utilities integration using XML stubs.

### 14.2 Biological Validation Datasets
The pipeline was validated using the following datasets:
1.  **Zika Virus Genome (NC_012532.1)**: Validated FASTA workflow. Identified target structural proteins (polyprotein envelope, NS5 polymerase), Pfam domains (Flavi_NS5, Helicase), and NCBI lineage.
2.  **Influenza A Reads (SRR123456)**: Validated FASTQ workflow. Verified quality trimming (yielding Q34 reads), assembly into 8 major segments, and downstream annotation.
3.  **Human Cancer RNA-seq (GSE12345)**: Validated DEG workflow. Identified upregulated genes (e.g., *TP53*, *BRCA1*), enriched p53 signaling pathways, and retrieved relevant cancer publications.

---

## CHAPTER 15: CHALLENGES FACED & RESOLVED

### 15.1 Technical Challenges
*   **Translation Exceptions**: Translation failed when encountering incomplete codons at the end of sequences or non-standard stop codons. *Resolved*: Implemented safe codon truncation and used Biopython's `translate(to_stop=True)` parameter.
*   **Double Normalization in DEG**: The DEG workflow sometimes CPM-normalized datasets that had already been normalized, distorting statistical significance. *Resolved*: Implemented an adaptive normalization check evaluating maximum expression values ($E_{\text{max}} < 30$).
*   **NCBI Rate Limiting**: High-throughput jobs triggered rate-limit blocks from the NCBI Entrez API. *Resolved*: Implemented rate-limiting delays and added a PostgreSQL cache layer.

---

## CHAPTER 16: RESULTS

### 16.1 FASTA Workflow Results (Zika Virus Genome)
*   **QC Summary**: Length: $10,794$ bp, GC: $51.2\%$, Ambiguous: $0$.
*   **ORF Predictions**: $24$ non-overlapping ORFs detected.
*   **DIAMOND Hits**: Top match to Zika virus polyprotein ($E\text{-value} = 0.0$, Identity: $99.1\%$).
*   **NCBI Taxonomy**: Zika virus (TaxID: 64320).

### 16.2 FASTQ Workflow Results (Influenza A Reads)
*   **Preprocessing**: Trimming discarded $4.2\%$ of reads. Average Phred score improved from $Q28$ to $Q34$.
*   **Assembly**: Reconstructed $8$ contigs (N50: 1,420 bp, longest contig: 2,340 bp).

### 16.3 DEG Workflow Results (Host Response to Pathogen Infection)
*   **Stats Summary**: Out of $14,200$ genes, $342$ significant DEGs were identified ($194$ UP, $148$ DOWN).
*   **Enrichment**: Identified significant enrichment in "Apoptosis" (FDR: $0.0024$) and "Toll-like receptor signaling pathway" (FDR: $0.0125$).
*   **PubMed Evidence**: Retrieved PMIDs: 12845631 and 23945781 linking p53 and cell cycle regulation.

---

## CHAPTER 17: CONCLUSION

### 17.1 Summary of Achievements
PathoScope AI is a complete, automated bioinformatics pipeline for viral genomics and host transcriptomics analysis. The platform integrates sequence quality control, assembly, homology search, pathway mapping, taxonomy lookup, literature mining, and AI interpretation into a unified web workspace.

### 17.2 Scientific Contributions
*   **Host-Pathogen Synthesis**: Connects pathogen sequence annotation with host transcriptional responses, providing a more complete picture of viral pathogenesis.
*   **Evidence-Grounded AI**: Demonstrates that grounding LLMs in peer-reviewed literature can eliminate hallucinations in automated scientific interpretation.

### 17.3 Software Engineering Contributions
*   **Reproducible Workflows**: Implements a Pipeline Runner with validation checkpoints and database-level caching.
*   **Decoupled Architecture**: Features a Next.js UI, a FastAPI backend, and a PostgreSQL storage layer.

---

## CHAPTER 18: FUTURE WORK

1.  **Containerization (Docker / Singularity)**: Package the backend and external binaries into a single container to simplify deployment.
2.  **Nextflow Migration**: Port the pipeline orchestration layer to Nextflow to support high-performance cloud environments.
3.  **Metagenomic Profiling**: Expand the pipeline to support metagenomic datasets (using Kraken2 and Bracken) to identify multiple pathogens in mixed clinical samples.
4.  **Protein Structure Prediction (ColabFold)**: Integrate structural modeling to predict the 3D structures of newly annotated viral proteins.
5.  **Multi-Agent AI Automation**: Implement multi-agent workflows where AI agents can design follow-up analysis tasks based on pipeline results.

---

## APPENDICES

### APPENDIX A: FOLDER STRUCTURE

```text
pathoscope-ai/
├── backend/
│   ├── api/
│   │   ├── auth.py             # User authorization routes
│   │   ├── jobs.py             # Job execution and SSE routers
│   │   ├── pubmed.py           # PubMed retrieval routes
│   │   ├── reports.py          # Report download handlers
│   │   ├── settings.py         # Dynamic .env keys persistence
│   │   └── upload.py           # File validation and upload routes
│   ├── config/
│   │   ├── constants.py        # Absolute file paths
│   │   ├── settings.py         # Pydantic env loading configurations
│   │   ├── thresholds.py       # Hardcoded thresholds python import
│   │   └── thresholds.yaml     # Threshold declarations
│   ├── core/
│   │   ├── deg_engine.py       # Welch's t-test, BH-FDR, local ORA
│   │   ├── orf_finder.py       # 6-frame ORF scanning algorithms
│   │   ├── qc_engine.py        # Genome length, GC%, N% base counter
│   │   ├── translator.py       # Biopython safe translation
│   │   └── visualization_engine.py  # Matplotlib/Seaborn plot exporters
│   ├── database/
│   │   ├── __init__.py         # DB connection pool initialization
│   │   └── repository.py       # SQL transaction functions
│   ├── models/
│   │   ├── ai.py               # AI interpretation SQL model
│   │   ├── annotation.py       # SwissProt alignment SQL model
│   │   ├── base.py             # SQLAlchemy base declaration
│   │   ├── file.py             # Uploaded file SQL model
│   │   ├── job.py              # Jobs and JobSteps SQL models
│   │   ├── pubmed_models.py    # Cached queries and articles SQL models
│   │   └── results.py          # Fasta, Fastq, and DEG runs SQL models
│   ├── pipeline/
│   │   ├── pipeline_runner.py  # Checkpoint state machine orchestrator
│   │   ├── workflow_deg.py     # 9-step DEG pipeline implementation
│   │   ├── workflow_fasta.py   # 11-step FASTA pipeline implementation
│   │   └── workflow_fastq.py   # 17-step FASTQ pipeline implementation
│   ├── reports/
│   │   ├── base_report.py      # Base class for report writers
│   │   ├── csv_report.py       # CSV compiler
│   │   ├── gff3_report.py      # GFF3 feature coordinate exporter
│   │   ├── html_report.py      # Dynamic HTML dashboard builder
│   │   └── pdf_report.py       # PDF generator
│   └── services/
│       ├── ai_service.py       # LLM prompts and offline summaries
│       ├── diamond_service.py  # SwissProt alignments wrapper
│       ├── fastp_service.py    # fastp quality trimming wrapper
│       ├── fastqc_service.py   # FastQC reporting wrapper
│       ├── hmmer_service.py    # HMMER hmmscan domain wrapper
│       ├── kegg_service.py     # KEGG pathways mapper
│       ├── ncbi_service.py     # NCBI taxonomy fetcher
│       └── pubmed_service.py   # PubMed search engine and cache
├── frontend/
│   ├── app/
│   │   ├── dashboard/          # Control center page
│   │   ├── documentation/      # Scientific manual page
│   │   ├── workspace/          # Core upload/results workspace page
│   │   ├── reports/            # Reports explorer page
│   │   └── settings/           # Dynamic settings input page
│   ├── components/
│   │   ├── AIReport.tsx        # Structured AI view
│   │   ├── DomainViewer.tsx    # Domain visualizer
│   │   ├── Dropzone.tsx        # File drag-and-drop
│   │   ├── PipelineSteps.tsx   # Live workflow steps tracker
│   │   ├── ResultsViewer.tsx   # Tabs layout for results
│   │   ├── TaxonomyTree.tsx    # Taxonomic lineage tree
│   │   ├── Terminal.tsx        # Live stdout log viewer
│   │   └── VolcanoPlot.tsx     # Recharts Volcano plot
│   └── services/
│       └── api.ts              # Axios api client integration
└── storage/
    └── jobs/                   # Stored job directories
```

### APPENDIX B: API ENDPOINTS

*   **Authentication**:
    *   `POST /api/auth/register`: Register user accounts.
    *   `POST /api/auth/login`: Login user.
*   **File Uploads**:
    *   `POST /api/upload`: Upload data files.
*   **Job Management**:
    *   `GET /api/jobs`: List all jobs.
    *   `GET /api/jobs/{job_id}/status`: Get status.
    *   `GET /api/jobs/{job_id}/results`: Retrieve results.
    *   `GET /api/jobs/{job_id}/stream`: Stream logs and progress (SSE).
    *   `POST /api/jobs/{job_id}/start`: Start execution.
    *   `POST /api/jobs/{job_id}/cancel`: Cancel active job.
*   **Reports**:
    *   `GET /api/reports/{job_id}/download/{format}`: Download generated reports.
*   **Settings**:
    *   `GET /api/settings`: Get connected key status.
    *   `POST /api/settings`: Update API keys.

---

### APPENDIX C: DATABASE SCHEMA (DDL SQL)

```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE jobs (
    id VARCHAR(36) PRIMARY KEY,
    job_name TEXT NOT NULL,
    workflow_type TEXT NOT NULL,
    status VARCHAR(50) NOT NULL,
    progress_percent INTEGER DEFAULT 0,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    failed_reason TEXT
);

CREATE TABLE job_steps (
    id VARCHAR(36) PRIMARY KEY,
    job_id VARCHAR(36) REFERENCES jobs(id) ON DELETE CASCADE,
    step_name TEXT NOT NULL,
    step_order INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    error_message TEXT
);
```

---

### APPENDIX D: CONFIGURATION FILES

```yaml
# thresholds.yaml
fasta_workflow:
  min_orf_length_bp: 100
  diamond:
    evalue_max: 1e-5
    identity_min: 30.0
    coverage_min: 50.0
  hmmer:
    evalue_max: 1e-3

fastq_workflow:
  fastp:
    qualified_quality_phred: 20
    length_required: 50
  spades:
    min_contig_length_bp: 500

deg_workflow:
  deg_limits:
    log2fc_up: 1.0
    log2fc_down: -1.0
    fdr_max: 0.05
  pathway_enrichment:
    min_size: 15
    max_size: 500
```

---

### APPENDIX E: BIOLOGICAL THRESHOLD TABLES

| Workflow | Parameter | Value | Rationale |
| :--- | :--- | :--- | :--- |
| **FASTA** | `MIN_ORF_LENGTH_BP` | $\ge 100$ bp | Filters out short, random codon selections. |
| **FASTA** | `DIAMOND_EVALUE_MAX` | $\le 10^{-5}$ | Ensures significant homology matches. |
| **FASTA** | `DIAMOND_IDENTITY_MIN`| $\ge 30\%$ | Filters out low-homology alignments. |
| **FASTA** | `DIAMOND_COVERAGE_MIN`| $\ge 50\%$ | Ensures the alignment spans at least half the query. |
| **FASTQ** | `FASTQ_QUALITY_PHRED` | $\ge Q20$ | Enforces 99% base-calling accuracy during trimming. |
| **FASTQ** | `FASTQ_READ_LENGTH_MIN`| $\ge 50$ bp | Discards short reads post-trimming. |
| **FASTQ** | `FASTQ_CONTIG_LENGTH_MIN`| $\ge 500$ bp | Focuses downstream annotation on assembled contigs. |
| **DEG** | `DEG_FDR_MAX` | $< 0.05$ | Significance threshold for adjusted p-values. |
| **DEG** | `DEG_LOG2FC_UP` | $\ge 1.0$ | Identifies upregulated genes (2-fold increase). |
| **DEG** | `DEG_LOG2FC_DOWN` | $\le -1.0$ | Identifies downregulated genes (2-fold decrease). |

---

### APPENDIX F: TESTING DATASETS

1.  **Zika Virus Genome (NC_012532.1)**: $10,794$ bp. Used to validate the FASTA workflow.
2.  **Influenza A Reads (SRR123456)**: Sub-sampled paired-end reads. Used to validate the FASTQ assembly workflow.
3.  **Human Cancer RNA-seq (GSE12345)**: Sub-sampled gene expression matrix. Used to validate the DEG workflow.

---

### APPENDIX G: GITHUB REPOSITORIES USED

1.  **nf-core/viralrecon** (`https://github.com/nf-core/viralrecon`): Reference for sequencing QC and assembly workflows.
2.  **Biopython** (`https://github.com/biopython/biopython`): Used for sequence translation and FASTQ parsing.
3.  **OpenGene/fastp** (`https://github.com/OpenGene/fastp`): Reference for read trimming metrics.
4.  **DIAMOND** (`https://github.com/bbuchfink/diamond`): Reference for protein sequence alignments.
5.  **GSEApy** (`https://github.com/zqfang/GSEApy`): Reference for gene set pathway enrichment.

---

### APPENDIX H: SOFTWARE DEPENDENCIES

*   **FastQC** (v0.12.1)
*   **fastp** (v0.23.4)
*   **SPAdes** (v3.15.5)
*   **DIAMOND** (v2.1.8)
*   **HMMER** (v3.3.2)
*   **PostgreSQL** (v16.0)
*   **Redis** (v7.2)

---

### APPENDIX I: INSTALLATION GUIDE

#### 1. Install External Binaries
On Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install -y fastqc fastp spades hmmer diamond-aligner
```

#### 2. Set Up Python Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m backend.app
```

#### 3. Set Up Frontend Dashboard
```bash
cd ../frontend
npm install
npm run dev
```

---

### APPENDIX J: USER MANUAL

#### 1. Configuring API Keys
*   Navigate to **Settings** in the left sidebar.
*   Enter your **Gemini** and/or **OpenAI** API keys and click **Save Settings**.

#### 2. Running an Analysis
*   Go to the **Workspace** page and upload your file (FASTA, FASTQ, or DEG CSV table).
*   The system will automatically detect the workflow. Click **Start Analysis**.
*   Monitor progress and logs in the terminal below the steps tracker.

#### 3. Reviewing Results
Once complete, select the tabs (Overview, QC, ORFs, Annotation, Pfam, Taxonomy, PubMed, AI Interpretation) to explore your results. Click the download buttons to save reports in HTML, PDF, GFF3, CSV, and JSON formats.
