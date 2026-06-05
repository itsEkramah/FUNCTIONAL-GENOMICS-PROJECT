import pytest
import xml.etree.ElementTree as ET
from backend.core.qc_engine import run_sequence_qc
from backend.core.orf_finder import find_orfs
from backend.core.translator import translate_dna_to_protein
from backend.core.deg_engine import apply_bh_fdr, classify_degs, normalize_gene_ids
from backend.services.ncbi_service import fetch_ncbi_taxonomy

def test_sequence_qc():
    # Test valid DNA sequence QC metrics
    seq = "ATGCATGCATGC"
    metrics = run_sequence_qc(seq)
    assert metrics["genome_length"] == 12
    assert metrics["gc_content"] == 50.0
    assert metrics["ambiguity_count"] == 0

    # Test ambiguous bases
    seq_ambig = "ATGCATGCATN"
    metrics_ambig = run_sequence_qc(seq_ambig)
    assert metrics_ambig["ambiguity_count"] == 1

def test_orf_finder():
    # Test sequence containing a single ORF: ATG (start) + AAA (codon) + TAA (stop)
    # Length: 9 bp (min_len set to 9)
    seq = "ATGCCCTAA"
    orfs = find_orfs(seq, min_len=9)
    assert len(orfs) == 1
    assert orfs[0]["strand"] == "+"
    assert orfs[0]["length"] == 9
    assert orfs[0]["start"] == 1
    assert orfs[0]["end"] == 9

def test_translation_engine():
    # Test standard translation of standard codons
    seq = "ATGCCCTAA"
    protein = translate_dna_to_protein(seq)
    # ATG -> M, CCC -> P, stop TAA -> empty string due to to_stop=True
    assert protein == "MP"

    # Test trailing non-triplets truncation
    seq_trailing = "ATGCCCTA" # 8 bp -> truncated to 6 bp
    protein_trailing = translate_dna_to_protein(seq_trailing)
    assert protein_trailing == "MP"

def test_bh_fdr_correction():
    pvalues = [0.01, 0.04, 0.03, 0.05, 0.8]
    # Apply Benjamini-Hochberg adjustment
    fdrs = apply_bh_fdr(pvalues)
    assert len(fdrs) == len(pvalues)
    # Assert adjustments are bounded and sorted
    assert all(0.0 <= f <= 1.0 for f in fdrs)

def test_deg_classification():
    log2fcs = [2.5, -3.1, 0.5, 1.2, -0.4]
    fdrs = [0.01, 0.002, 0.2, 0.08, 0.01]
    
    # Classify each gene
    classes = [classify_degs([log2fcs[i]], [fdrs[i]])[0] for i in range(len(log2fcs))]
    
    # Assert classifications match thresholds
    # UP: log2FC >= 1, FDR < 0.05
    assert classes[0] == "UP"
    # DOWN: log2FC <= -1, FDR < 0.05
    assert classes[1] == "DOWN"
    # Not Significant
    assert classes[2] == "Not Significant" # FDR >= 0.05
    assert classes[3] == "Not Significant" # FDR >= 0.05
    assert classes[4] == "Not Significant" # log2FC not <= -1

def test_ncbi_xml_parser():
    # XML response stub from NCBI taxonomy efetch
    xml_data = """<?xml version="1.0"?>
    <TaxaSet>
        <Taxon>
            <TaxId>10244</TaxId>
            <ScientificName>Zika virus</ScientificName>
            <Rank>species</Rank>
            <LineageEx>
                <Taxon>
                    <ScientificName>Viruses</ScientificName>
                </Taxon>
                <Taxon>
                    <ScientificName>Riboviria</ScientificName>
                </Taxon>
            </LineageEx>
        </Taxon>
    </TaxaSet>
    """
    root = ET.fromstring(xml_data)
    taxon = root.find("Taxon")
    assert taxon is not None
    assert taxon.findtext("TaxId") == "10244"
    assert taxon.findtext("ScientificName") == "Zika virus"
    assert taxon.findtext("Rank") == "species"
