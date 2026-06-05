import os
from datetime import datetime
from typing import List, Dict, Any

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from backend.reports.base_report import BaseReport

class PdfReport(BaseReport):
    """
    Exposes compilation methods to compile self-contained static PDF reports.
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
        ai_result: Dict[str, Any]
    ) -> str:
        output_path = self.get_output_path("report.pdf")
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )
        
        styles = getSampleStyleSheet()
        
        # Define clean, modern color scheme (Dark slate, deep blue, orange accents)
        primary_color = colors.HexColor("#1e293b")
        secondary_color = colors.HexColor("#3b82f6")
        accent_color = colors.HexColor("#f97316")
        bg_dark = colors.HexColor("#0f172a")
        text_light = colors.HexColor("#f8fafc")
        border_color = colors.HexColor("#cbd5e1")
        
        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Heading1'],
            fontSize=22,
            leading=26,
            textColor=primary_color,
            spaceAfter=15
        )
        
        h2_style = ParagraphStyle(
            'DocH2',
            parent=styles['Heading2'],
            fontSize=14,
            leading=18,
            textColor=secondary_color,
            spaceBefore=15,
            spaceAfter=8,
            keepWithNext=True
        )
        
        body_style = ParagraphStyle(
            'DocBody',
            parent=styles['BodyText'],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#334155"),
            spaceAfter=6
        )
        
        body_bold = ParagraphStyle(
            'DocBodyBold',
            parent=body_style,
            fontName='Helvetica-Bold'
        )
        
        meta_style = ParagraphStyle(
            'DocMeta',
            parent=body_style,
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#64748b")
        )
        
        ai_title_style = ParagraphStyle(
            'DocAITitle',
            parent=body_style,
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            textColor=accent_color,
            spaceBefore=8,
            spaceAfter=2
        )
        
        story = []
        
        # Header / Title
        story.append(Paragraph("PathoScope AI v3.0 — Genome Annotation Report", title_style))
        story.append(Paragraph(f"Job ID: {job_id} | Sequence ID: {seqid} | Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}", meta_style))
        story.append(Spacer(1, 15))
        
        # Summary Grid (QC, Classification, Annotation)
        summary_data = [
            [
                Paragraph("<b>Sequence Quality Control</b>", body_bold),
                Paragraph("<b>Pathogen Classification</b>", body_bold),
                Paragraph("<b>Annotation Summary</b>", body_bold)
            ],
            [
                Paragraph(f"Genome Length: <b>{qc.get('genome_length', 0):,} bp</b><br/>"
                          f"GC Content: <b>{qc.get('gc_content', 0.0)}%</b><br/>"
                          f"Ambiguity Count: <b>{qc.get('ambiguity_count', 0)}</b>", body_style),
                Paragraph(f"Taxon ID: <b>{taxonomy.get('tax_id', '10244')}</b><br/>"
                          f"Scientific Name: <b>{taxonomy.get('organism_name', 'Unknown pathogen')}</b><br/>"
                          f"Rank: <b>{taxonomy.get('rank', 'species')}</b>", body_style),
                Paragraph(f"Total ORFs: <b>{len(orfs)}</b><br/>"
                          f"DIAMOND hits: <b>{len(annotations)}</b><br/>"
                          f"Pfam Domains: <b>{len(domains)}</b>", body_style)
            ]
        ]
        
        summary_table = Table(summary_data, colWidths=[170, 170, 170])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
            ('TEXTCOLOR', (0,0), (-1,0), primary_color),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, border_color),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 15))
        
        # AI Pathobiology Summary
        story.append(Paragraph("🤖 Evidence-Grounded AI Pathobiology Summary", h2_style))
        
        ai_data = [
            [Paragraph(f"Provider: <b>{ai_result.get('ai_provider', 'offline')}</b> | Model: <b>{ai_result.get('model_name', 'fallback')}</b> | Confidence: <b>{ai_result.get('confidence_assessment', 'LOW')}</b>", meta_style)],
            [Paragraph("Findings Summary", ai_title_style)],
            [Paragraph(ai_result.get('findings', 'None'), body_style)],
            [Paragraph("Literature Evidence", ai_title_style)],
            [Paragraph(ai_result.get('literature_summary', 'None'), body_style)],
            [Paragraph("Biological Pathogenesis Analysis", ai_title_style)],
            [Paragraph(ai_result.get('biological_interpretation', 'None'), body_style)],
            [Paragraph("Technical Limitations", ai_title_style)],
            [Paragraph(ai_result.get('limitations', 'None'), body_style)]
        ]
        
        ai_table = Table(ai_data, colWidths=[510])
        ai_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('PADDING', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(ai_table)
        
        # Page Break before tables for cleaner layout
        story.append(PageBreak())
        
        # DIAMOND Table
        story.append(Paragraph("DIAMOND Homologous Annotations (Top 10)", h2_style))
        diamond_headers = ["Query", "Subject Accession", "Identity", "Coverage", "E-value", "Bitscore"]
        diamond_rows = [diamond_headers]
        for h in annotations[:10]:
            diamond_rows.append([
                h['query_protein'],
                h['subject_protein'],
                f"{h['identity_percent']}%",
                f"{h['coverage_percent']}%",
                f"{h['evalue']:.2e}",
                f"{h['bitscore']:.1f}"
            ])
            
        if len(diamond_rows) == 1:
            diamond_rows.append(["No homologous annotations identified.", "", "", "", "", ""])
            
        diamond_table = Table(diamond_rows, colWidths=[80, 110, 80, 80, 80, 80])
        diamond_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), primary_color),
            ('TEXTCOLOR', (0,0), (-1,0), text_light),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, border_color),
            ('PADDING', (0,0), (-1,-1), 6),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('FONTSIZE', (0,1), (-1,-1), 8),
        ]))
        story.append(diamond_table)
        story.append(Spacer(1, 15))
        
        # Pfam predicted domains
        story.append(Paragraph("Pfam Predicted Domains (Top 10)", h2_style))
        pfam_headers = ["Protein ID", "Accession", "Domain Name", "Coordinates", "E-value"]
        pfam_rows = [pfam_headers]
        for d in domains[:10]:
            pfam_rows.append([
                d['protein_id'],
                d['pfam_accession'],
                d['pfam_name'],
                f"{d['domain_start']} - {d['domain_end']}",
                f"{d['evalue']:.2e}"
            ])
            
        if len(pfam_rows) == 1:
            pfam_rows.append(["No domains identified.", "", "", "", ""])
            
        pfam_table = Table(pfam_rows, colWidths=[100, 100, 110, 100, 100])
        pfam_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), primary_color),
            ('TEXTCOLOR', (0,0), (-1,0), text_light),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, border_color),
            ('PADDING', (0,0), (-1,-1), 6),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('FONTSIZE', (0,1), (-1,-1), 8),
        ]))
        story.append(pfam_table)
        story.append(Spacer(1, 15))
        
        # KEGG pathways mapping
        story.append(Paragraph("Mapped KEGG Biochemical Pathways (Top 10)", h2_style))
        kegg_headers = ["Pathway ID", "Pathway Name", "Gene Matches", "FDR"]
        kegg_rows = [kegg_headers]
        for p in pathways[:10]:
            kegg_rows.append([
                p['pathway_id'],
                p['pathway_name'],
                str(p['gene_count']),
                f"{p['fdr']:.4f}"
            ])
            
        if len(kegg_rows) == 1:
            kegg_rows.append(["No pathways mapped.", "", "", ""])
            
        kegg_table = Table(kegg_rows, colWidths=[100, 230, 90, 90])
        kegg_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), primary_color),
            ('TEXTCOLOR', (0,0), (-1,0), text_light),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, border_color),
            ('PADDING', (0,0), (-1,-1), 6),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 9),
            ('FONTSIZE', (0,1), (-1,-1), 8),
        ]))
        story.append(kegg_table)
        
        doc.build(story)
        return output_path
