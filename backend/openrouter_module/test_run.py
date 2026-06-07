import os
import json
import logging
from backend.openrouter_module.biological_interpreter import BiologicalInterpreter
from backend.openrouter_module.report_generator import ReportGenerator

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TestRun")

def run_e2e_test():
    logger.info("Initializing PathoScope OpenRouter Module End-to-End Test...")
    
    # Mock Functional Genomics Input Data
    mock_genes = [
        {"gene_id": "STAT1", "log2FoldChange": 2.8, "padj": 0.0001, "regulation": "UP"},
        {"gene_id": "MX1", "log2FoldChange": 3.2, "padj": 0.0002, "regulation": "UP"},
        {"gene_id": "OAS1", "log2FoldChange": 1.9, "padj": 0.0051, "regulation": "UP"},
        {"gene_id": "ISG15", "log2FoldChange": 4.1, "padj": 0.00001, "regulation": "UP"}
    ]
    
    mock_pathways = [
        {"Term": "JAK-STAT signaling pathway", "Overlap": "8/42", "pvalue": 0.0005},
        {"Term": "Viral carcinogenesis", "Overlap": "12/80", "pvalue": 0.0012}
    ]
    
    mock_go_terms = [
        {"Term": "type I interferon signaling pathway", "ID": "GO:0060337"},
        {"Term": "defense response to virus", "ID": "GO:0051607"}
    ]
    
    mock_diseases = ["Influenza A", "Severe Viral Infection", "Pneumonia"]
    
    mock_metadata = {
        "organism": "Orthomyxoviridae virus subtype H1N1",
        "tissue": "Lung epithelial cells",
        "timepoint": "24h post-infection"
    }

    # Instantiate interpreter
    interpreter = BiologicalInterpreter()
    
    logger.info("Running interpretation...")
    result = interpreter.interpret_findings(
        genes=mock_genes,
        pathways=mock_pathways,
        go_terms=mock_go_terms,
        disease_associations=mock_diseases,
        metadata=mock_metadata
    )
    
    # Output result to screen
    logger.info("\n--- PIPELINE COMPLETED SUCCESSFULLY ---")
    logger.info(f"Model used for final report: {result['model_used']}")
    logger.info(f"Summary length: {len(result['summary'])} chars")
    logger.info(f"Literature evidence: {result['literature_evidence']}")
    
    # Generate reports
    logger.info("Generating final reports...")
    report_gen = ReportGenerator(output_dir="storage/reports")
    paths = report_gen.generate_all_reports(job_id="test_job_123", interpretation_data=result)
    
    logger.info(f"HTML Report generated at: {os.path.abspath(paths['html'])}")
    logger.info(f"Markdown Report generated at: {os.path.abspath(paths['markdown'])}")
    logger.info(f"JSON Output generated at: {os.path.abspath(paths['json'])}")

if __name__ == "__main__":
    run_e2e_test()
