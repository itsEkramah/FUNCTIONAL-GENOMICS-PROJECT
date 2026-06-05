import os

def detect_file_type(file_path: str) -> str:
    """
    Inspects the header of a file to determine if it is FASTA, FASTQ, or a DEG expression table.
    
    Parameters:
    -----------
    file_path : str
        Path to the file to inspect.
        
    Returns:
    --------
    file_type : str
        'FASTA', 'FASTQ', or 'DEG'.
        
    Raises:
    -------
    ValueError
        If the file format is not recognized.
    FileNotFoundError
        If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    # Read the first few lines of the file, stripping empty rows
    header_lines = []
    
    # Handle gzip files if necessary (although detector usually runs on local unzipped or decompressed chunk previews)
    if file_path.endswith(".gz"):
        import gzip
        try:
            with gzip.open(file_path, "rt", encoding="utf-8") as f:
                for _ in range(10):
                    line = f.readline()
                    if not line:
                        break
                    line_stripped = line.strip()
                    if line_stripped:
                        header_lines.append(line_stripped)
        except Exception as e:
            raise ValueError(f"Failed to read compressed gzip file: {str(e)}")
    else:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for _ in range(10):
                    line = f.readline()
                    if not line:
                        break
                    line_stripped = line.strip()
                    if line_stripped:
                        header_lines.append(line_stripped)
        except Exception as e:
            raise ValueError(f"Failed to read file: {str(e)}")
            
    if not header_lines:
        raise ValueError("File is empty.")
        
    first_line = header_lines[0]
    
    # 1. FASTA check: First line starts with '>'
    if first_line.startswith(">"):
        return "FASTA"
        
    # 2. FASTQ check: First line starts with '@' and third line starts with '+'
    if first_line.startswith("@"):
        # Look for the '+' marker in subsequent lines (typically line 2 is sequence, line 3 is '+', line 4 is quality)
        for i in range(1, min(len(header_lines), 4)):
            if header_lines[i].startswith("+"):
                return "FASTQ"
        # Fallback if file is short but starts with @
        return "FASTQ"
        
    # 3. DEG check: Header contains 'gene_id', 'log2foldchange', or 'pvalue'
    first_line_lower = first_line.lower()
    if "gene_id" in first_line_lower or "pvalue" in first_line_lower or "log2foldchange" in first_line_lower:
        return "DEG"
        
    # If it is a CSV/TSV table without headers, check column values
    if "," in first_line or "\t" in first_line:
        return "DEG"
        
    raise ValueError(f"Unable to auto-detect file format for: {file_path}")
