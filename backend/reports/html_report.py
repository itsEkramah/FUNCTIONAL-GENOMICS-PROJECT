import os
from datetime import datetime
from typing import List, Dict, Any
from backend.reports.base_report import BaseReport

class HtmlReport(BaseReport):
    """
    Exposes compilation methods to compile self-contained static HTML result dashboards.
    """
    def generate(
        self,
        job_id: str,
        seqid: str,
        qc: Dict[str, Any],
        orfs: List[Dict[str, Any]],
        annotations: List[Dict[str, Any]],
        domains: List[Dict[str, Any]],
        pathways: List[Dict[str, Any]],
        taxonomy: Dict[str, Any],
        ai_result: Dict[str, Any],
        fastq_run: Dict[str, Any] = None
    ) -> str:
        """
        Compiles the full analysis dashboard to a standalone single HTML page.
        """
        output_path = self.get_output_path("report.html")
        
        fastq_card = ""
        if fastq_run:
            fastq_card = f"""
            <div class="card">
                <h2>FASTQ Quality & Preprocessing</h2>
                <div>Raw Read Count:</div>
                <div class="metric-value">{fastq_run.get('raw_reads', 0):,}</div>
                <div>Filtered Read Count:</div>
                <div class="metric-value">{fastq_run.get('filtered_reads', 0):,}</div>
                <div>Average Read Quality:</div>
                <div class="metric-value">Q{fastq_run.get('average_quality', 0.0):.1f}</div>
                <div>Assembly Contigs:</div>
                <div class="metric-value">{fastq_run.get('assembly_contigs', 0)}</div>
            </div>
            """
        
        # Format HTML rows for annotations
        annot_rows = ""
        for h in annotations:
            annot_rows += f"""
            <tr>
                <td>{h['query_protein']}</td>
                <td>{h['subject_protein']}</td>
                <td>{h['identity_percent']}%</td>
                <td>{h['coverage_percent']}%</td>
                <td>{h['evalue']}</td>
                <td>{h['bitscore']}</td>
                <td>{h['annotation']}</td>
            </tr>
            """
            
        # Format HTML rows for domains
        dom_rows = ""
        for d in domains:
            dom_rows += f"""
            <tr>
                <td>{d['protein_id']}</td>
                <td>{d['pfam_accession']}</td>
                <td>{d['pfam_name']}</td>
                <td>{d['domain_start']} - {d['domain_end']}</td>
                <td>{d['evalue']}</td>
            </tr>
            """
            
        # Format HTML rows for pathways
        path_rows = ""
        for p in pathways:
            path_rows += f"""
            <tr>
                <td>{p['pathway_id']}</td>
                <td>{p['pathway_name']}</td>
                <td>{p['gene_count']}</td>
                <td>{p['fdr']}</td>
            </tr>
            """

        # Check which visualizations exist
        vis_dir = os.path.join(self.job_dir, "visualizations")
        vis_section = ""
        if os.path.exists(vis_dir):
            files = sorted([f for f in os.listdir(vis_dir) if f.endswith(".png")])
            if files:
                vis_section = """
        <h2 class="section-header">Analytical Visualizations & QC Charts</h2>
        <div class="grid">
        """
                for f in files:
                    title = f.replace(".png", "").replace("_", " ").title()
                    vis_section += f"""
            <div class="card" style="text-align: center; background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px;">
                <h3 style="color: #58a6ff; font-size: 14px; margin-top: 0; font-family: 'Outfit', sans-serif; border-bottom: 1px solid #30363d; padding-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">{title}</h3>
                <img src="../visualizations/{f}" alt="{title}" style="max-width: 100%; max-height: 350px; height: auto; border-radius: 6px; border: 1px solid #30363d; margin-top: 10px;">
            </div>
            """
                vis_section += "\n        </div>"

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>PathoScope AI v3.0 — Pathogen Annotation Report</title>
    <style>
        body {{
            font-family: 'Outfit', 'Inter', sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        header {{
            background: linear-gradient(135deg, #1f2937, #111827);
            padding: 24px;
            border-radius: 12px;
            margin-bottom: 24px;
            border: 1px solid #30363d;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }}
        h1 {{
            margin: 0;
            color: #58a6ff;
            font-size: 28px;
        }}
        .job-id {{
            color: #8b949e;
            font-size: 14px;
            margin-top: 4px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }}
        .card {{
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }}
        .card h2 {{
            margin-top: 0;
            color: #58a6ff;
            font-size: 18px;
            border-bottom: 1px solid #30363d;
            padding-bottom: 10px;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #f0883e;
            margin: 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }}
        th, td {{
            text-align: left;
            padding: 10px;
            border-bottom: 1px solid #30363d;
        }}
        th {{
            background-color: #161b22;
            color: #8b949e;
            font-weight: 600;
        }}
        .section-header {{
            color: #58a6ff;
            margin-top: 40px;
            margin-bottom: 15px;
            border-bottom: 2px solid #58a6ff;
            padding-bottom: 8px;
        }}
        .ai-box {{
            background: linear-gradient(135deg, #1b263b, #0d1b2a);
            border: 1.5px dashed #415a77;
            padding: 24px;
            border-radius: 12px;
            margin-top: 30px;
        }}
        .ai-header {{
            color: #70a1ff;
            font-size: 20px;
            margin-top: 0;
            font-weight: bold;
        }}
        .ai-meta {{
            color: #8b949e;
            font-size: 12px;
            margin-bottom: 15px;
        }}
        .ai-section-title {{
            color: #ffaf40;
            font-weight: 600;
            margin-top: 15px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            font-size: 11px;
            border-radius: 4px;
            font-weight: bold;
            background-color: #238636;
            color: #ffffff;
        }}
        .badge.high {{ background-color: #238636; }}
        .badge.medium {{ background-color: #b07219; }}
        .badge.low {{ background-color: #da3633; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>PathoScope AI v3.0 Pathobiology Report</h1>
            <div class="job-id">Job ID: {job_id} | Sequence ID: {seqid} | Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</div>
        </header>

        <div class="grid">
            {fastq_card}
            <div class="card">
                <h2>Sequence Quality Control</h2>
                <div>Genome Length:</div>
                <div class="metric-value">{qc['genome_length']:,} bp</div>
                <div>GC Content:</div>
                <div class="metric-value">{qc['gc_content']}%</div>
                <div>Ambiguity Count:</div>
                <div class="metric-value">{qc['ambiguity_count']}</div>
            </div>

            <div class="card">
                <h2>Pathogen Classification</h2>
                <div>Taxon ID:</div>
                <div class="metric-value">{taxonomy.get('tax_id', '10244')}</div>
                <div>Scientific Name:</div>
                <div class="metric-value">{taxonomy.get('organism_name', 'Unknown pathogen')}</div>
                <div>Lineage:</div>
                <div style="margin-top: 8px; color: #8b949e; font-size:13px;">{", ".join(taxonomy.get('lineage', []))}</div>
            </div>

            <div class="card">
                <h2>Annotation Summary</h2>
                <div>Total ORFs Detected:</div>
                <div class="metric-value">{len(orfs)}</div>
                <div>DIAMOND Annotations:</div>
                <div class="metric-value">{len(annotations)}</div>
                <div>Pfam Domains:</div>
                <div class="metric-value">{len(domains)}</div>
            </div>
        </div>

        <div class="ai-box">
            <div class="ai-header">🤖 Evidence-Grounded AI Pathobiology Summary</div>
            <div class="ai-meta">Provider: {ai_result.get('ai_provider', 'offline')} | Model: {ai_result.get('model_name', 'fallback')} | Confidence: <span class="badge {ai_result.get('confidence_assessment', 'LOW').lower()}">{ai_result.get('confidence_assessment', 'LOW')}</span></div>
            
            <div class="ai-section-title">Findings Summary</div>
            <p>{ai_result.get('findings', 'None')}</p>
            
            <div class="ai-section-title">Literature Evidence</div>
            <p>{ai_result.get('literature_summary', 'None')}</p>
            
            <div class="ai-section-title">Biological Pathogenesis Analysis</div>
            <p>{ai_result.get('biological_interpretation', 'None')}</p>
            
            <div class="ai-section-title">Technical Limitations</div>
            <p>{ai_result.get('limitations', 'None')}</p>
        </div>

        {vis_section}

        <h2 class="section-header">DIAMOND Homologous Annotations</h2>
        <table>
            <thead>
                <tr>
                    <th>Query Protein</th>
                    <th>Subject Accession</th>
                    <th>Identity</th>
                    <th>Coverage</th>
                    <th>E-value</th>
                    <th>Bitscore</th>
                    <th>Functional Description</th>
                </tr>
            </thead>
            <tbody>
                {annot_rows or "<tr><td colspan='7'>No homologous annotations identified.</td></tr>"}
            </tbody>
        </table>

        <h2 class="section-header">Pfam Predicted Domains</h2>
        <table>
            <thead>
                <tr>
                    <th>Protein ID</th>
                    <th>Pfam Accession</th>
                    <th>Domain Name</th>
                    <th>Coordinates</th>
                    <th>Domain E-value</th>
                </tr>
            </thead>
            <tbody>
                {dom_rows or "<tr><td colspan='5'>No domains identified.</td></tr>"}
            </tbody>
        </table>

        <h2 class="section-header">Mapped KEGG Biochemical Pathways</h2>
        <table>
            <thead>
                <tr>
                    <th>Pathway ID</th>
                    <th>Pathway Name</th>
                    <th>Gene Matches</th>
                    <th>Calculated FDR</th>
                </tr>
            </thead>
            <tbody>
                {path_rows or "<tr><td colspan='4'>No pathways mapped.</td></tr>"}
            </tbody>
        </table>
    </div>
</body>
</html>
        """
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        return output_path
