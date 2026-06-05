import os

def detect_file_type(input_data: str) -> str:
    content = input_data
    if os.path.exists(input_data):
        try:
            with open(input_data, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1024)
        except Exception:
            pass
            
    content = content.strip()
    if not content:
        raise ValueError("File is empty")
        
    if content.startswith('>'):
        return 'FASTA'
    elif content.startswith('@'):
        return 'FASTQ'
    else:
        return 'EXPRESSION'
