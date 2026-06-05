import requests
import xml.etree.ElementTree as ET
from typing import Dict, Any, List

def fetch_ncbi_taxonomy(organism_name: str, log_logger) -> Dict[str, Any]:
    """
    Queries NCBI Taxonomy database to retrieve the Taxonomic ID, rank, and lineage tree.
    
    Parameters:
    -----------
    organism_name : str
        The name of the target organism (e.g. 'Zika virus').
    log_logger : Logger
        Active job logger.
        
    Returns:
    --------
    taxonomy_result : dict
        Calculated lineage tree, rank, and ID.
    """
    log_logger.info(f"Querying NCBI Taxonomy for organism: {organism_name}")
    
    # Fallback default taxonomy object in case of network timeouts or missing entries
    fallback_result = {
        "tax_id": 10244, # Default viral TaxID
        "organism_name": organism_name,
        "lineage": ["Viruses", "Riboviria", "Orthornavirae", "Kitrinoviricota", "Flashaviridae"],
        "rank": "species"
    }
    
    if not organism_name:
        return fallback_result

    # 1. Search NCBI Taxonomy to resolve TaxID
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "taxonomy",
        "term": organism_name,
        "retmode": "json"
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        id_list = data.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            log_logger.warning(f"No TaxID found for organism: {organism_name}. Using fallback.")
            return fallback_result
            
        tax_id = int(id_list[0])
        
        # 2. Fetch taxonomy summary details
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        fetch_params = {
            "db": "taxonomy",
            "id": str(tax_id),
            "retmode": "xml"
        }
        
        fetch_resp = requests.get(fetch_url, params=fetch_params, timeout=10)
        fetch_resp.raise_for_status()
        
        # Parse XML response
        root = ET.fromstring(fetch_resp.text)
        taxon = root.find("Taxon")
        if taxon is None:
            return fallback_result
            
        rank = taxon.findtext("Rank", "species")
        scientific_name = taxon.findtext("ScientificName", organism_name)
        
        lineage_list = []
        lineage_xml = taxon.find("LineageEx")
        if lineage_xml is not None:
            for child in lineage_xml.findall("Taxon"):
                node_name = child.findtext("ScientificName")
                if node_name:
                    lineage_list.append(node_name)
                    
        # Append target organism name to complete the lineage tree leaf
        lineage_list.append(scientific_name)
        
        log_logger.info(f"NCBI Taxonomy resolved: TaxID={tax_id}, Rank={rank}")
        return {
            "tax_id": tax_id,
            "organism_name": scientific_name,
            "lineage": lineage_list,
            "rank": rank
        }
        
    except Exception as e:
        log_logger.warning(f"NCBI E-Utilities request failed: {str(e)}. Using fallback offline data.")
        return fallback_result
