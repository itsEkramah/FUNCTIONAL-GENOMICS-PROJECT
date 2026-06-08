import os
import shutil
import gzip
import requests

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA_DIR = os.path.join(BASE_DIR, "test_data")

FASTA_SRC_DIR = os.path.join(TEST_DATA_DIR, "fasta")
FASTQ_SRC_DIR = os.path.join(TEST_DATA_DIR, "fastq_demo")

FASTA_DEMO_DIR = os.path.join(TEST_DATA_DIR, "fasta_demo")
FASTQ_DEMO_DIR = os.path.join(TEST_DATA_DIR, "fastq_demo") # keep in place
TSV_DEMO_DIR = os.path.join(TEST_DATA_DIR, "tsv_demo")
CSV_DEMO_DIR = os.path.join(TEST_DATA_DIR, "csv_demo")

# Ensure directories exist
for d in [FASTA_DEMO_DIR, FASTQ_DEMO_DIR, TSV_DEMO_DIR, CSV_DEMO_DIR]:
    os.makedirs(d, exist_ok=True)

# Datasets definition
FASTA_DEFS = [
    {"acc": "NC_045512.2", "name": "NC_045512.2.fasta"},
    {"acc": "NC_002549.1", "name": "NC_002549.1.fasta"},
    {"acc": "NC_007373.1", "name": "NC_007373.1.fasta"},
    {"acc": "NC_001416.1", "name": "NC_001416.1.fasta"},
    {"acc": "NC_001731.1", "name": "NC_001731.1.fasta"},
    {"acc": "NC_000883.2", "name": "NC_000883.2.fasta"},
    {"acc": "NC_011503.2", "name": "NC_011503.2.fasta"},
    {"acc": "NC_002137.1", "name": "NC_002137.1.fasta"},
    {"acc": "NC_004102.1", "name": "NC_004102.1.fasta"},
    {"acc": "NC_012532.1", "name": "NC_012532.1.fasta"},
]

TSV_DEFS = [
    {"name": "GSE147507_RawReadCounts_Human.tsv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE147nnn/GSE147507/suppl/GSE147507_RawReadCounts_Human.tsv.gz"},
    {"name": "GSE60424_normalized_counts.txt.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE60nnn/GSE60424/suppl/GSE60424_GEOSubmit_FC1to11_normalized_counts.txt.gz"},
    {"name": "GSE112002_raw_counts.txt.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE112nnn/GSE112002/suppl/GSE112002_rnaseq_raw_counts.txt.gz"},
    {"name": "GSE112002_rlog_DEGenes.txt.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE112nnn/GSE112002/suppl/GSE112002_rnaseq_rlog_DEGenes.txt.gz"},
    {"name": "GSE157103_genes_ec.tsv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE157nnn/GSE157103/suppl/GSE157103_genes.ec.tsv.gz"},
    {"name": "GSE157103_genes_tpm.tsv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE157nnn/GSE157103/suppl/GSE157103_genes.tpm.tsv.gz"},
    {"name": "GSE171110_raw_counts.txt.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE171nnn/GSE171110/suppl/GSE171110_Data_RNAseq_raw_counts_geo.txt.gz"},
    {"name": "GSE171110_norm_counts.txt.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE171nnn/GSE171110/suppl/GSE171110_Data_RNAseq_norm_counts_geo.txt.gz"},
    {"name": "GSE152418_RawCounts.txt.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE152nnn/GSE152418/suppl/GSE152418_p20047_Study1_RawCounts.txt.gz"},
    {"name": "GSE166190_Raw_counts.txt.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE166nnn/GSE166190/suppl/GSE166190_Raw_counts.txt.gz"}
]

CSV_DEFS = [
    {"name": "cell_cycle_degs.csv", "url": "https://raw.githubusercontent.com/itsEkramah/FUNCTIONAL-GENOMICS-PROJECT/main/test_data/gene_lists/cell_cycle_degs.csv"},
    {"name": "GSE161731_counts.csv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE161nnn/GSE161731/suppl/GSE161731_counts.csv.gz"},
    {"name": "GSE161731_xpr_nlcpm.csv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE161nnn/GSE161731/suppl/GSE161731_xpr_nlcpm.csv.gz"},
    {"name": "GSE183947_fpkm.csv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE183nnn/GSE183947/suppl/GSE183947_fpkm.csv.gz"},
    {"name": "GSE156063_swab_gene_counts.csv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE156nnn/GSE156063/suppl/GSE156063_swab_gene_counts.csv.gz"},
    {"name": "GSE185263_raw_counts.csv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE185nnn/GSE185263/suppl/GSE185263_raw_counts.csv.gz"},
    {"name": "GSE150910_gene_counts.csv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE150nnn/GSE150910/suppl/GSE150910_gene-level_count_file.csv.gz"},
    {"name": "GSE161731_counts_key.csv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE161nnn/GSE161731/suppl/GSE161731_counts_key.csv.gz"},
    {"name": "GSE161731_key.csv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE161nnn/GSE161731/suppl/GSE161731_key.csv.gz"},
    {"name": "GSE164471_ENSG_counts.csv.gz", "url": "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE164nnn/GSE164471/suppl/GSE164471_GESTALT_Muscle_ENSG_counts_annotated.csv.gz"}
]

FASTQ_FILES = [
    "ERR10000183_1.fastq.gz",
    "ERR10000249_1.fastq.gz",
    "ERR10000864_1.fastq.gz",
    "ERR10001732_1.fastq.gz",
    "ERR10004191_1.fastq.gz",
    "ERR10004815_1.fastq.gz",
    "ERR10004981_1.fastq.gz",
    "ERR10014444_1.fastq.gz",
    "ERR10021986_1.fastq.gz",
    "ERR10022353_1.fastq.gz"
]

def download_file(url, target_path):
    print(f"Downloading {url} to {target_path}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url, headers=headers, timeout=60, stream=True)
        response.raise_for_status()
        with open(target_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("  Download complete.")
        return True
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return False

def verify_file(file_path):
    if not os.path.exists(file_path):
        return False, "Does not exist"
    
    size = os.path.getsize(file_path)
    if size == 0:
        return False, "Empty file"
    
    size_mb = size / (1024 * 1024)
    if size_mb > 150:
        return False, f"Too large ({size_mb:.2f} MB)"
    
    # If Gzip, test integrity
    if file_path.endswith(".gz"):
        try:
            with gzip.open(file_path, "rb") as f:
                f.read(100)
            return True, f"Valid Gzip ({size_mb:.2f} MB)"
        except Exception as e:
            return False, f"Corrupted Gzip: {e}"
            
    # If FASTA, check first char
    if file_path.endswith(".fasta"):
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                first_char = f.read(1)
            if first_char == ">":
                return True, f"Valid FASTA ({size_mb:.4f} MB)"
            else:
                return False, f"Invalid FASTA format (starts with '{first_char}')"
        except Exception as e:
            return False, f"Error reading FASTA: {e}"
            
    return True, f"Verified ({size_mb:.2f} MB)"

def process_fasta():
    print("\n--- Organizing FASTA Datasets ---")
    for f_def in FASTA_DEFS:
        acc = f_def["acc"]
        name = f_def["name"]
        dest_path = os.path.join(FASTA_DEMO_DIR, name)
        
        # Look for source file in FASTA_SRC_DIR
        found_src = None
        if os.path.exists(FASTA_SRC_DIR):
            for candidate in os.listdir(FASTA_SRC_DIR):
                if candidate.startswith(acc) and candidate.endswith(".fasta"):
                    found_src = os.path.join(FASTA_SRC_DIR, candidate)
                    break
        
        if found_src:
            print(f"Copying local source: {found_src} -> {dest_path}")
            shutil.copy2(found_src, dest_path)
        else:
            # Download if not found locally
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id={acc}&rettype=fasta"
            download_file(url, dest_path)

def process_tsv():
    print("\n--- Downloading/Verifying TSV Datasets ---")
    for t_def in TSV_DEFS:
        name = t_def["name"]
        url = t_def["url"]
        dest_path = os.path.join(TSV_DEMO_DIR, name)
        
        if os.path.exists(dest_path):
            ok, msg = verify_file(dest_path)
            if ok:
                print(f"Skipping {name} (Already exists & valid: {msg})")
                continue
            else:
                print(f"Re-downloading {name} (Previous file invalid: {msg})")
                
        download_file(url, dest_path)

def process_csv():
    print("\n--- Downloading/Verifying CSV Datasets ---")
    for c_def in CSV_DEFS:
        name = c_def["name"]
        url = c_def["url"]
        dest_path = os.path.join(CSV_DEMO_DIR, name)
        
        if os.path.exists(dest_path):
            ok, msg = verify_file(dest_path)
            if ok:
                print(f"Skipping {name} (Already exists & valid: {msg})")
                continue
            else:
                print(f"Re-downloading {name} (Previous file invalid: {msg})")
                
        download_file(url, dest_path)

def main():
    process_fasta()
    process_tsv()
    process_csv()
    
    # Verify everything
    print("\n============================================================")
    print("Verification Summary of All 40 Datasets")
    print("============================================================")
    
    report = []
    
    # 1. FASTA
    print("\n[FASTA DEMO FILES]")
    fasta_count = 0
    for f_def in FASTA_DEFS:
        path = os.path.join(FASTA_DEMO_DIR, f_def["name"])
        ok, msg = verify_file(path)
        print(f"  {f_def['name']}: {'[OK]' if ok else '[FAIL]'} {msg}")
        if ok: fasta_count += 1
        report.append(f"FASTA | {f_def['name']} | {'Valid' if ok else 'Invalid'} ({msg})")
        
    # 2. FASTQ
    print("\n[FASTQ DEMO FILES]")
    fastq_count = 0
    for name in FASTQ_FILES:
        path = os.path.join(FASTQ_DEMO_DIR, name)
        ok, msg = verify_file(path)
        print(f"  {name}: {'[OK]' if ok else '[FAIL]'} {msg}")
        if ok: fastq_count += 1
        report.append(f"FASTQ | {name} | {'Valid' if ok else 'Invalid'} ({msg})")
        
    # 3. TSV
    print("\n[TSV DEMO FILES]")
    tsv_count = 0
    for t_def in TSV_DEFS:
        path = os.path.join(TSV_DEMO_DIR, t_def["name"])
        ok, msg = verify_file(path)
        print(f"  {t_def['name']}: {'[OK]' if ok else '[FAIL]'} {msg}")
        if ok: tsv_count += 1
        report.append(f"TSV | {t_def['name']} | {'Valid' if ok else 'Invalid'} ({msg})")
        
    # 4. CSV
    print("\n[CSV DEMO FILES]")
    csv_count = 0
    for c_def in CSV_DEFS:
        path = os.path.join(CSV_DEMO_DIR, c_def["name"])
        ok, msg = verify_file(path)
        print(f"  {c_def['name']}: {'[OK]' if ok else '[FAIL]'} {msg}")
        if ok: csv_count += 1
        report.append(f"CSV | {c_def['name']} | {'Valid' if ok else 'Invalid'} ({msg})")
        
    total_valid = fasta_count + fastq_count + tsv_count + csv_count
    print("\n============================================================")
    print(f"Grand Total: {total_valid}/40 valid datasets.")
    print(f"FASTA: {fasta_count}/10, FASTQ: {fastq_count}/10, TSV: {tsv_count}/10, CSV: {csv_count}/10")
    print("============================================================")
    
    # Save verification report as an artifact list
    report_file = os.path.join(TEST_DATA_DIR, "datasets_verification_report.txt")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report))
    print(f"Verification log written to {report_file}")

if __name__ == "__main__":
    main()
