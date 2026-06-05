# PUBMED_SERVICE_REPORT.md — PubMed Evidence Engine Report

This report outlines the system architecture, API retrieval flow, XML parsing structure, and two-tiered caching logic for the PubMed Evidence Engine in PathoScope AI v3.0.

---

## 1. System Architecture

The PubMed Evidence Engine fetches, filters, ranks, and caches biomedical publications from NCBI's E-Utilities (Entrez) to ground pathobiology interpretations.

```
       [Query Target: Organism & Protein Keywords]
                           │
                           ▼
              [Check Redis Cache (1st Tier)]
                 Key: pubmed:{query_hash}
                           │
             ┌─────────────┴─────────────┐
        Cache Hit                   Cache Miss
             │                           │
             ▼                           ▼
      [Return Articles]     [Check PostgreSQL Cache (2nd Tier)]
                             Table: pubmed_queries / pubmed_articles
                                         │
                           ┌─────────────┴─────────────┐
                      Cache Hit                   Cache Miss
                           │                           │
                           ▼                           ▼
                    [Return Articles]       [Query NCBI E-Utilities API]
                                            1. esearch (Search PMIDs)
                                            2. efetch (Fetch XML metadata)
                                                       │
                                                       ▼
                                            [Parse XML & Score Relevance]
                                                       │
                                                       ▼
                                            [Write to PostgreSQL Cache]
                                                       │
                                                       ▼
                                            [Write to Redis Cache]
```

---

## 2. API Retrieval Flow

1. **NCBI E-Utilities esearch**:
   * Resolves search keywords into a list of PMIDs.
   * Endpoint: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
   * Parameters: `db=pubmed`, `term={query}`, `retmode=json`, `retmax=10`.
2. **NCBI E-Utilities efetch**:
   * Retrieves full XML metadata for identified PMIDs.
   * Endpoint: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`
   * Parameters: `db=pubmed`, `id={pmid1,pmid2,...}`, `retmode=xml`.

---

## 3. XML Parsing Logic

The XML parser uses Python's standard `xml.etree.ElementTree` to extract the following elements from the `<PubmedArticle>` node:

* **PMID**: Retrieved from `MedlineCitation/PMID`.
* **Title**: Retrieved from `MedlineCitation/Article/ArticleTitle`.
* **Authors**: List of author names compiled from `MedlineCitation/Article/AuthorList/Author`. We extract `<ForeName>` and `<LastName>` and format them as a JSON list.
* **Journal**: Retrieved from `MedlineCitation/Article/Journal/Title` or `ISOAbbreviation`.
* **Year**: Retrieved from `MedlineCitation/Article/Journal/JournalIssue/PubDate/Year`. If unavailable (e.g. for some review or online-only articles), parses the `<MedlineDate>` field.
* **Abstract**: Concatenates all `<AbstractText>` elements.
* **DOI**: Parsed from the `<ArticleIdList/ArticleId>` tag where `IdType="doi"`.

---

## 4. Two-Tiered Caching Scheme

To avoid exceeding the NCBI rate limit (3 anonymous requests per second) and ensure rapid pipeline runs:

1. **In-Memory Cache (Redis)**:
   * Key: `pubmed:{query_hash}` where query hash is the MD5 of the lower-cased query text.
   * Data Type: String (serialized JSON list of article dictionaries).
   * Expiration (TTL): 30 days.
2. **Relational Cache (PostgreSQL/SQLite)**:
   * Table `pubmed_queries` stores the search term query hash, text, and type.
   * Table `pubmed_articles` stores the parsed details (PMID, title, abstract, authors, DOI, year, journal, relevance score) foreign-keyed to `pubmed_queries.id`.
   * On cache miss at both tiers, the API queries NCBI, writes the results to the database and Redis simultaneously, and returns them.

---

## 5. Relevance Scoring Algorithm

To ensure abstracts are biologically relevant, we compute a relevance score for each article:
$$\text{Relevance Score} = w_1 \times N_{\text{organism}} + w_2 \times N_{\text{protein}}$$
Where:
* $N_{\text{organism}}$ is the count of occurrences of the organism name in the title and abstract.
* $N_{\text{protein}}$ is the count of occurrences of protein names or pathway keywords.
* $w_1 = 2.0$ (higher weight for matching target pathogen/organism).
* $w_2 = 1.0$ (weight for matching protein terms).
Articles with a score of `0` are filtered out or ranked lower to prevent unrelated literature from contaminating the context.

---

## 6. Error & Offline Fallback Modes

* **Network Timeout / API Down**: The request catches `requests.exceptions.RequestException`, logs the incident as a warning trace, and returns an empty list or searches a local dictionary of offline pre-defined articles.
* **Rate Limiting (HTTP 429)**: The engine pauses and retries the request using an exponential backoff wrapper (retrying up to 3 times with pauses: 1s, 2s, 4s).
