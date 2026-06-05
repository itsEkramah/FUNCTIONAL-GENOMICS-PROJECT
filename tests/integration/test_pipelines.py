import pytest
import os
from backend.utils.file_detector import detect_file_type

# Paths to test data directories
TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "test_data")
FASTA_TEST_DIR = os.path.join(TEST_DATA_DIR, "fasta")
FASTQ_TEST_DIR = os.path.join(TEST_DATA_DIR, "fastq")
DEG_TEST_DIR = os.path.join(TEST_DATA_DIR, "gene_lists")

def test_file_type_detection_success():
    # 1. Test real FASTA file
    fasta_path = os.path.join(FASTA_TEST_DIR, "BK066888.1 .fasta.fasta")
    assert detect_file_type(fasta_path) == "FASTA"

    # 2. Test real FASTQ file
    fastq_path = os.path.join(FASTQ_TEST_DIR, "test_reads.fastq")
    assert detect_file_type(fastq_path) == "FASTQ"

    # 3. Test real DEG file
    deg_path = os.path.join(DEG_TEST_DIR, "cell_cycle_degs.csv")
    assert detect_file_type(deg_path) == "DEG"

def test_file_type_detection_failures():
    # 1. Missing file raises FileNotFoundError
    with pytest.raises(FileNotFoundError):
        detect_file_type("nonexistent_file.fasta")

    # 2. Invalid inputs from negative dataset
    invalid_fasta_path = os.path.join(FASTA_TEST_DIR, "07_invalid_input", "invalid_characters.fasta")
    # This should be recognized as FASTA by format header, but contains bad characters
    assert detect_file_type(invalid_fasta_path) == "FASTA"

def test_empty_file_fails(tmp_path):
    # Create empty file
    empty_file = tmp_path / "empty.fasta"
    empty_file.write_text("")
    
    with pytest.raises(ValueError, match="File is empty"):
        detect_file_type(str(empty_file))
