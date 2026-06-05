import pytest
import os
import time
import tracemalloc
from backend.core.qc_engine import run_sequence_qc
from backend.core.orf_finder import find_orfs

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "test_data")
LARGE_BATCH_DIR = os.path.join(TEST_DATA_DIR, "fasta", "20_large_batch_dataset")

def test_large_batch_performance():
    """
    Performance test: runs biological QC and ORF scanning on 20 Dengue genome FASTA files.
    Measures processing runtime and peak memory usage.
    """
    if not os.path.exists(LARGE_BATCH_DIR):
        pytest.skip("Large batch dataset directory not found.")

    files = [f for f in os.listdir(LARGE_BATCH_DIR) if f.endswith(".fasta")]
    if not files:
        pytest.skip("No FASTA files found in large batch dataset.")

    # Start memory tracing
    tracemalloc.start()
    start_time = time.time()

    total_length = 0
    total_orfs = 0

    for file_name in files:
        file_path = os.path.join(LARGE_BATCH_DIR, file_name)
        
        # Read sequence
        sequence_lines = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.startswith(">"):
                    sequence_lines.append(line.strip())
        sequence = "".join(sequence_lines)
        
        # 1. Run QC
        qc = run_sequence_qc(sequence)
        total_length += qc["genome_length"]
        
        # 2. Run ORF Finder (min_len set to 100 bp)
        orfs = find_orfs(sequence, min_len=100)
        total_orfs += len(orfs)

    end_time = time.time()
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    duration = end_time - start_time
    peak_mem_mb = peak_mem / (1024 * 1024)

    print(f"\n⚡ Performance Report:")
    print(f"   • Total Genomes Processed: {len(files)}")
    print(f"   • Cumulative Sequence Length: {total_length} bp")
    print(f"   • Total ORFs Identified: {total_orfs}")
    print(f"   • Processing Duration: {duration:.4f} seconds")
    print(f"   • Peak Memory Usage: {peak_mem_mb:.4f} MB")

    # Assert correctness
    assert total_length > 0
    # Enforce performance targets (e.g. processing 20 files must complete in under 30 seconds and use < 15MB peak memory)
    assert duration < 30.0
    assert peak_mem_mb < 15.0
