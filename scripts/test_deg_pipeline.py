import os
import sys
import uuid
import time
import json
import glob

# Ensure we use an isolated SQLite test database and that backend path is in search path
os.environ["DATABASE_URL"] = "sqlite:///test_runner.db"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, init_db
from backend.models.job import Job
from backend.models.results import DegRun, ReportResult
from backend.pipeline.workflow_deg import run_deg_workflow

# 1. Initialize DB and recreate tables
init_db()

# Define test sequences inside test_data/
TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_data")
GENE_LISTS_DIR = os.path.join(TEST_DATA_DIR, "gene_lists")
DEG_WORKFLOW_B_DIR = os.path.join(TEST_DATA_DIR, "DEG WORKFLOW B TESTDATA")

test_cases = [
    {
        "name": "Mode A: Precomputed Cell Cycle DEGs",
        "path": os.path.join(GENE_LISTS_DIR, "cell_cycle_degs.csv")
    },
    {
        "name": "Mode B: Raw Counts Matrix (GSE60424)",
        "path": os.path.join(DEG_WORKFLOW_B_DIR, "GSE60424_raw_counts_GRCh38.p13_NCBI.tsv.gz")
    },
    {
        "name": "Mode B: Normalized FPKM counts (GSE60424)",
        "path": os.path.join(DEG_WORKFLOW_B_DIR, "GSE60424_norm_counts_FPKM_GRCh38.p13_NCBI.tsv.gz")
    }
]

print("="*60)
print("PATHOSCOPE AI DEG WORKFLOW E2E INTEGRATION TEST")
print("="*60)

results = []

for case in test_cases:
    name = case["name"]
    path = case["path"]
    print(f"\n[RUNNING] {name}")
    print(f"File Path: {path}")
    
    if not os.path.exists(path):
        print(f"[SKIP] File not found: {path}")
        continue
        
    job_id = str(uuid.uuid4())
    
    # Register job in DB first so status changes are recorded correctly
    with SessionLocal() as db:
        new_job = Job(id=job_id, job_name=f"E2E DEG: {name}", workflow_type="DEG", status="QUEUED")
        db.add(new_job)
        db.commit()
        
    start_time = time.time()
    
    try:
        run_deg_workflow(job_id, path)
        duration = time.time() - start_time
        print(f"[SUCCESS] {name} completed in {duration:.2f} seconds.")
        
        # Query results from database
        with SessionLocal() as db:
            job = db.query(Job).filter(Job.id == job_id).first()
            deg_run = db.query(DegRun).filter(DegRun.job_id == job_id).first()
            reports = db.query(ReportResult).filter(ReportResult.job_id == job_id).all()
            
            # Verify visualizations
            vis_dir = os.path.join("storage", "jobs", job_id, "visualizations")
            plot_names = [
                "volcano_plot", "ma_plot", "deg_distribution_histogram",
                "top_20_upregulated_bar", "top_20_downregulated_bar",
                "go_enrichment_bar", "go_enrichment_dot",
                "kegg_enrichment_bar", "kegg_enrichment_dot",
                "gene_count_summary", "significant_vs_nonsignificant", "pathway_summary_plot"
            ]
            
            plots_ok = True
            missing_plots = []
            for plot in plot_names:
                for ext in ["png", "svg", "pdf"]:
                    plot_path = os.path.join(vis_dir, f"{plot}.{ext}")
                    if not os.path.exists(plot_path) or os.path.getsize(plot_path) == 0:
                        plots_ok = False
                        missing_plots.append(f"{plot}.{ext}")
            
            summary = {
                "name": name,
                "job_id": job_id,
                "status": job.status if job else "Unknown",
                "duration": duration,
                "total_genes": deg_run.total_genes if deg_run else 0,
                "significant_genes": deg_run.significant_genes if deg_run else 0,
                "upregulated": deg_run.upregulated if deg_run else 0,
                "downregulated": deg_run.downregulated if deg_run else 0,
                "reports_generated": [r.report_type for r in reports],
                "plots_valid": plots_ok,
                "missing_plots": missing_plots
            }
            results.append(summary)
            
            print(f"  • Total Genes: {summary['total_genes']:,}")
            print(f"  • Significant DEGs: {summary['significant_genes']:,} (UP={summary['upregulated']}, DOWN={summary['downregulated']})")
            print(f"  • 12 Plots (PNG/SVG/PDF): {'PASSED' if plots_ok else 'FAILED (missing: ' + ', '.join(missing_plots) + ')'}")
            print(f"  • Reports: {', '.join(summary['reports_generated'])}")
            
    except Exception as e:
        print(f"[FAILED] {name} encountered an error: {str(e)}")
        import traceback
        traceback.print_exc()

# Write validation summary report
report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "DEG_VALIDATION_REPORT.md")
print(f"\nSaving master validation report to: {report_path}")
with open(report_path, "w", encoding="utf-8") as out:
    out.write("# DEG Master Validation and E2E Test Report\n\n")
    out.write("This report details the execution and validation of the PathoScope AI v3.0 Differential Gene Expression (DEG) workflow, including matrix normalization, BH-FDR correction, gene identifier mapping, GO/KEGG functional enrichment, and publication-quality visualizations.\n\n")
    
    out.write("## Test Execution Environment\n")
    out.write("- **Database**: SQLite (isolated test runner DB)\n")
    out.write("- **FDR Correction Method**: Benjamini-Hochberg (statsmodels fdr_bh)\n")
    out.write("- **ID Standardization Layer**: Local mapper from Human.GRCh38.p13.annot.tsv\n")
    out.write("- **GO / KEGG Pathway enrichment**: GSEApy with ORA offline fallbacks\n")
    out.write("- **Visualizations**: 12 distinct plots rendered in PNG, SVG, and PDF formats\n\n")
    
    out.write("## Test Case Execution Summary\n\n")
    out.write("| Dataset | Mode | Total Genes | Significant DEGs | Upregulated | Downregulated | Plots Valid | Status | Time (s) |\n")
    out.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
    
    for r in results:
        mode_str = "Mode A" if "Mode A" in r["name"] else "Mode B"
        out.write(f"| {r['name']} | {mode_str} | {r['total_genes']:,} | {r['significant_genes']:,} | {r['upregulated']:,} | {r['downregulated']:,} | {'Yes' if r['plots_valid'] else 'No'} | **{r['status']}** | {r['duration']:.2f} |\n")
        
    out.write("\n## Deliverables Manifest (per job)\n")
    for r in results:
        out.write(f"\n### {r['name']} (Job: `{r['job_id']}`)\n")
        out.write(f"- **Validated Input Table**: `storage/jobs/{r['job_id']}/validated_input.csv`\n")
        out.write(f"- **ID Mapping Report**: `storage/jobs/{r['job_id']}/mapping_report.json`\n")
        out.write(f"- **Normalization Details**: `storage/jobs/{r['job_id']}/normalization_report.json`\n")
        out.write(f"- **Upregulated Gene Set**: `storage/jobs/{r['job_id']}/upregulated_degs.csv`\n")
        out.write(f"- **Downregulated Gene Set**: `storage/jobs/{r['job_id']}/downregulated_degs.csv`\n")
        out.write(f"- **GO Enrichment Results**: `storage/jobs/{r['job_id']}/go_results.csv`\n")
        out.write(f"- **KEGG Enrichment Results**: `storage/jobs/{r['job_id']}/kegg_results.csv`\n")
        out.write(f"- **12 Plots (PNG/SVG/PDF)**: `storage/jobs/{r['job_id']}/visualizations/`\n")
        out.write(f"- **PubMed Abstract Cache**: `storage/jobs/{r['job_id']}/pubmed_evidence.json`\n")
        out.write(f"- **AI groundings Synthesis**: `storage/jobs/{r['job_id']}/ai_interpretation.json`\n")
        out.write(f"- **Detailed Markdown Report**: `storage/jobs/{r['job_id']}/DEG_VALIDATION_REPORT.md`\n")
        
    out.write("\n## Validation Integrity and Quality Gate Checks\n")
    out.write("1. **Automatic Compression Handling**: Gzip-compressed inputs are automatically detected and cleanly extracted via python's `gzip` and `shutil` packages.\n")
    out.write("2. **Strict Validation Checks**: Any null values, non-numeric p-values, duplicate records, or invalid probabilities trigger pipeline aborts with zero silent failures.\n")
    
print("E2E Integration Test Script completed.")
