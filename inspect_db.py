import sqlite3
import os

def inspect_file(db_name):
    print("=" * 60)
    print(f"DATABASE: {db_name}")
    print("=" * 60)
    if not os.path.exists(db_name):
        print("File does not exist.")
        return
        
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT j.id, j.job_name, j.workflow_type, k.pathway_id, k.pathway_name, k.gene_count, k.pvalue, k.fdr 
            FROM jobs j
            LEFT JOIN kegg_results k ON j.id = k.job_id
        """)
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print(f"Error querying database: {e}")
        return
    
    jobs = {}
    for row in rows:
        job_id = row[0]
        if job_id not in jobs:
            jobs[job_id] = {
                "name": row[1],
                "type": row[2],
                "results": []
            }
        if row[3] is not None:
            jobs[job_id]["results"].append(row[3:])
        
    for job_id, data in jobs.items():
        print(f"\nJob ID: {job_id} | Name: {data['name']} | Type: {data['type']}")
        if not data["results"]:
            print("  No KEGG results.")
            continue
        print(f"  Total KEGG results: {len(data['results'])}")
        for r in data["results"][:5]: # print top 5
            print(f"    - Pathway ID: {r[0]}, Name: {r[1]}, Count: {r[2]}, pvalue: {r[3]:.4e}, fdr: {r[4]:.4e}")
        if len(data["results"]) > 5:
            print(f"    ... and {len(data['results']) - 5} more")

def main():
    conn = sqlite3.connect("pathoscope.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, job_name, workflow_type FROM jobs")
    jobs = cursor.fetchall()
    
    for job_id, name, wf_type in jobs:
        print(f"\n============================================================")
        print(f"JOB ID: {job_id} | Name: {name} | Type: {wf_type}")
        print(f"============================================================")
        
        # Get annotations
        cursor.execute("SELECT query_protein, subject_protein, evalue, bitscore FROM annotations WHERE job_id = ?", (job_id,))
        annots = cursor.fetchall()
        print(f"  Annotations ({len(annots)}):")
        for q, s, e, b in annots[:5]:
            print(f"    - Query: {q}, Subject: {s}, evalue: {e:.2e}, bitscore: {b}")
        if len(annots) > 5:
            print(f"    ... and {len(annots) - 5} more")
            
        # Get KEGG results
        cursor.execute("SELECT pathway_id, pathway_name, gene_count, pvalue, fdr FROM kegg_results WHERE job_id = ?", (job_id,))
        keggs = cursor.fetchall()
        print(f"  KEGG Results ({len(keggs)}):")
        for p_id, p_name, cnt, pval, fdr in keggs:
            print(f"    - Pathway ID: {p_id}, Name: {p_name}, Count: {cnt}, pvalue: {pval:.4e}, fdr: {fdr:.4e}")

if __name__ == "__main__":
    main()
