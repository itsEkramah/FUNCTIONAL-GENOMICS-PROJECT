export type WorkflowType = 'FASTA' | 'FASTQ' | 'DEG';
export type JobStatus = 'QUEUED' | 'RUNNING' | 'FAILED' | 'COMPLETED' | 'CANCELLED';
export type JobStepStatus = 'PENDING' | 'RUNNING' | 'FAILED' | 'COMPLETED';

export interface JobStep {
  id: string;
  job_id: string;
  step_name: string;
  step_order: number;
  status: JobStepStatus;
  start_time: string | null;
  end_time: string | null;
  log_path: string | null;
  output_path: string | null;
  error_message: string | null;
}

export interface Job {
  id: string;
  job_name: string;
  workflow_type: WorkflowType;
  status: JobStatus;
  progress_percent: number;
  user_id: string | null;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
  failed_reason: string | null;
  steps?: JobStep[];
}

export interface FastaRun {
  genome_length: number;
  gc_content: number;
  ambiguity_count: number;
  total_orfs: number;
  translated_proteins: number;
}

export interface FastqRun {
  raw_reads: number;
  filtered_reads: number;
  average_quality: number;
  assembly_contigs: number;
}

export interface DegRun {
  total_genes: number;
  significant_genes: number;
  upregulated: number;
  downregulated: number;
}

export interface AnnotationResult {
  query_protein: string;
  subject_protein: string;
  identity_percent: number;
  coverage_percent: number;
  evalue: number;
  bitscore: number;
  annotation: string;
}

export interface PfamDomain {
  protein_id: string;
  pfam_accession: string;
  pfam_name: string;
  domain_start: number;
  domain_end: number;
  evalue: number;
}

export interface KeggPathway {
  pathway_id: string;
  pathway_name: string;
  gene_count: number;
  pvalue: number;
  fdr: number;
}

export interface TaxonomyResults {
  tax_id: number;
  organism_name: string;
  rank: string;
  lineage: string[];
}

export interface PubMedArticle {
  pmid: string;
  title: string;
  journal: string;
  publication_year: number;
  authors: { forename?: string; lastname?: string }[];
  doi: string | null;
  abstract: string;
  publication_type: string | null;
  mesh_terms: string[] | null;
}

export interface AIInterpretation {
  ai_provider: string;
  model_name: string;
  findings: string;
  literature_summary: string;
  biological_interpretation: string;
  confidence_assessment: 'HIGH' | 'MEDIUM' | 'LOW';
  limitations: string;
}

export interface ReportFile {
  report_type: 'HTML' | 'PDF' | 'CSV' | 'JSON' | 'GFF3' | 'MD';
  report_path: string;
}

export interface PipelineResults {
  job_id: string;
  workflow_type: WorkflowType;
  fasta_run?: FastaRun;
  fastq_run?: FastqRun;
  deg_run?: DegRun;
  annotations?: AnnotationResult[];
  pfam_domains?: PfamDomain[];
  kegg_results?: KeggPathway[];
  taxonomy_results?: TaxonomyResults;
  pubmed?: PubMedArticle[];
  ai_interpretation?: AIInterpretation;
  reports?: ReportFile[];
  visualizations?: string[];
}
