import os
import json
from typing import Dict, Any

class ReportGenerator:
    """
    Bioinformatics report generator that formats structured genomics interpretation
    into production-grade Markdown, HTML dashboards, and JSON files.
    """
    def __init__(self, output_dir: str = "storage/reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_all_reports(self, job_id: str, interpretation_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generates and saves JSON, Markdown, and HTML reports.
        """
        job_dir = os.path.join(self.output_dir, job_id)
        os.makedirs(job_dir, exist_ok=True)
        
        json_path = self.save_json(job_dir, interpretation_data)
        md_path = self.save_markdown(job_dir, interpretation_data)
        html_path = self.save_html(job_dir, interpretation_data)
        
        return {
            "json": json_path,
            "markdown": md_path,
            "html": html_path
        }

    def save_json(self, target_dir: str, data: Dict[str, Any]) -> str:
        path = os.path.join(target_dir, "ai_biological_report.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return path

    def save_markdown(self, target_dir: str, data: Dict[str, Any]) -> str:
        path = os.path.join(target_dir, "ai_biological_report.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# PathoScope AI - Biological Interpretation Report\n\n")
            f.write(f"**Model Used**: `{data.get('model_used', 'offline')}`\n\n")
            
            f.write("## 📝 Executive Summary\n")
            f.write(f"{data.get('summary', 'No summary available.')}\n\n")
            
            f.write("## 🧬 Analyzed Genes & Regulation\n")
            for gene in data.get("genes", []):
                f.write(f"- {gene}\n")
            f.write("\n")
            
            f.write("## 🗺️ Enriched Biochemical Pathways\n")
            for path in data.get("pathways", []):
                f.write(f"- {path}\n")
            f.write("\n")
            
            f.write("## 🎯 Identified Biomarkers & Therapeutic Targets\n")
            f.write("### Biomarkers:\n")
            for bm in data.get("biomarkers", []):
                f.write(f"- {bm}\n")
            f.write("### Therapeutic Targets:\n")
            for tt in data.get("therapeutic_targets", []):
                f.write(f"- {tt}\n")
            f.write("\n")
            
            f.write("## 🏥 Disease Associations\n")
            for da in data.get("disease_associations", []):
                f.write(f"- {da}\n")
            f.write("\n")
            
            f.write("## 📚 Supporting PubMed Evidence\n")
            for lit in data.get("literature_evidence", []):
                f.write(f"- PMID: {lit}\n")
            f.write("\n")
            
            f.write("## 🔬 Clinical Relevance\n")
            f.write(f"{data.get('clinical_relevance', 'N/A')}\n\n")
            
            f.write("## 🚀 Future Research Directions\n")
            f.write(f"{data.get('future_directions', 'N/A')}\n")
            
        return path

    def save_html(self, target_dir: str, data: Dict[str, Any]) -> str:
        path = os.path.join(target_dir, "ai_biological_report.html")
        
        genes_list_html = "".join([f"<li class='item'>{g}</li>" for g in data.get("genes", [])])
        pathways_list_html = "".join([f"<li class='item'>{p}</li>" for p in data.get("pathways", [])])
        biomarkers_html = "".join([f"<li class='item bm'>{b}</li>" for b in data.get("biomarkers", [])])
        targets_html = "".join([f"<li class='item tt'>{t}</li>" for t in data.get("therapeutic_targets", [])])
        diseases_html = "".join([f"<li class='item'>{d}</li>" for d in data.get("disease_associations", [])])
        literature_html = "".join([f"<li class='item pmid'>PMID: {l}</li>" for l in data.get("literature_evidence", [])])

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>PathoScope AI - Biological Interpretation Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0b1220;
            color: #f3f4f6;
            margin: 0;
            padding: 40px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: #111827;
            border: 1px border #1f2937;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        }}
        h1 {{
            color: #60a5fa;
            font-size: 28px;
            border-bottom: 2px solid #1f2937;
            padding-bottom: 15px;
            margin-top: 0;
        }}
        h2 {{
            color: #93c5fd;
            font-size: 20px;
            margin-top: 30px;
            border-left: 4px solid #60a5fa;
            padding-left: 10px;
        }}
        .meta {{
            font-family: monospace;
            font-size: 12px;
            color: #9ca3af;
            background-color: #1f2937;
            padding: 8px 15px;
            border-radius: 6px;
            display: inline-block;
            margin-bottom: 20px;
        }}
        .grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .card {{
            background-color: #1f2937;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #374151;
        }}
        .card h3 {{
            margin-top: 0;
            color: #60a5fa;
        }}
        ul {{
            padding-left: 20px;
            margin: 0;
        }}
        li.item {{
            margin-bottom: 8px;
            font-size: 14px;
            color: #d1d5db;
        }}
        .summary-box {{
            line-height: 1.6;
            font-size: 15px;
            background-color: #0b1220;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #1f2937;
            white-space: pre-wrap;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            color: #6b7280;
            margin-top: 40px;
            border-top: 1px solid #1f2937;
            padding-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>PathoScope AI - Biological Interpretation Dashboard</h1>
        <div class="meta">MODEL RUN: {data.get('model_used', 'offline')}</div>
        
        <h2>📝 Executive Summary</h2>
        <div class="summary-box">{data.get('summary', 'N/A')}</div>
        
        <div class="grid" style="margin-top: 30px;">
            <div class="card">
                <h3>🧬 Significant Genes Analyzed</h3>
                <ul>{genes_list_html}</ul>
            </div>
            <div class="card">
                <h3>🗺️ Mapped Pathways</h3>
                <ul>{pathways_list_html}</ul>
            </div>
        </div>

        <div class="grid" style="margin-top: 20px;">
            <div class="card">
                <h3>🎯 Biomarkers & Targets</h3>
                <h4>Candidate Biomarkers:</h4>
                <ul>{biomarkers_html}</ul>
                <h4 style="margin-top:15px;">Therapeutic Targets:</h4>
                <ul>{targets_html}</ul>
            </div>
            <div class="card">
                <h3>📚 Supporting Evidence & Diseases</h3>
                <h4>Related Pathologies:</h4>
                <ul>{diseases_html}</ul>
                <h4 style="margin-top:15px;">NCBI Citations:</h4>
                <ul>{literature_html}</ul>
            </div>
        </div>

        <h2>🔬 Clinical Relevance</h2>
        <div class="summary-box">{data.get('clinical_relevance', 'N/A')}</div>

        <h2>🚀 Future Research Directions</h2>
        <div class="summary-box">{data.get('future_directions', 'N/A')}</div>
        
        <div class="footer">
            Generated automatically by PathoScope AI functional genomics reporting suite.
        </div>
    </div>
</body>
</html>
"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return path
