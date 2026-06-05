'use client';

import React, { useState, useEffect } from 'react';
import { Sidebar } from '../../components/Sidebar';
import { Navbar } from '../../components/Navbar';

interface Article {
  pmid: string;
  title: string;
  journal: string;
  publication_year: number;
  authors: { forename?: string; lastname?: string }[];
  doi?: string;
  abstract: string;
  publication_type: string;
  mesh_terms: string[];
  relevance_score: number;
}

interface CachedQuery {
  id: number;
  job_id: string;
  query_text: string;
  query_type: string;
  article_count: number;
}

export default function PubMedPage() {
  const [biomolecule, setBiomolecule] = useState('');
  const [biomoleculeType, setBiomoleculeType] = useState('Gene');
  const [context, setContext] = useState('');
  const [forceOffline, setForceOffline] = useState(false);
  const [loading, setLoading] = useState(false);
  const [articles, setArticles] = useState<Article[]>([]);
  const [searchStrategy, setSearchStrategy] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
  const [cachedQueries, setCachedQueries] = useState<CachedQuery[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchCache = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/pubmed/queries`);
      if (res.ok) {
        const data = await res.json();
        setCachedQueries(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchCache();
  }, []);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!biomolecule.trim()) return;

    setLoading(true);
    setError(null);
    setArticles([]);
    setSearchStrategy(null);
    setSummary(null);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/pubmed/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          biomolecule: biomolecule.trim(),
          biomolecule_type: biomoleculeType,
          context: context.trim(),
          force_offline: forceOffline
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'PubMed search failed.');
      }

      const data = await res.json();
      
      // Extract articles from categories
      const req = data.curated_literature_requirements;
      const combined: Article[] = [];
      ['mechanistic_articles', 'clinical_and_therapeutic_articles', 'latest_trends_and_reviews'].forEach(cat => {
        if (req && req[cat]) {
          Object.values(req[cat]).forEach((art: any) => {
            combined.push(art);
          });
        }
      });
      
      setArticles(combined);
      setSearchStrategy(data.pubmed_search_strategy);
      setSummary(data.evidence_synthesis_summary);
      fetchCache(); // Refresh queries history
    } catch (err: any) {
      setError(err.message || 'Network error.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B1220] text-white">
      <Navbar />
      <Sidebar />
      <main className="pl-64 pt-16 min-h-screen">
        <div className="p-8 max-w-7xl mx-auto flex flex-col gap-6">
          
          <div className="flex flex-col gap-2">
            <h2 className="text-2xl font-bold text-[#60A5FA] font-mono">PubMed Literature Explorer</h2>
            <p className="text-xs text-gray-400">Query the NCBI Entrez Utilities directly, analyze literature evidence, and view query history caches.</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            
            {/* Search Controls Panel */}
            <div className="lg:col-span-1 flex flex-col gap-4">
              <form onSubmit={handleSearch} className="bg-[#1F2937] p-5 rounded-lg border border-[#3b4252] flex flex-col gap-4">
                <h3 className="text-sm font-bold font-mono text-[#60A5FA]">Search Parameters</h3>
                
                <div className="flex flex-col gap-1.5">
                  <label className="text-[10px] uppercase font-mono text-gray-400">Target Biomolecule/Organism</label>
                  <input
                    type="text"
                    required
                    value={biomolecule}
                    onChange={(e) => setBiomolecule(e.target.value)}
                    placeholder="e.g. TP53, SARS-CoV-2"
                    className="bg-[#0B1220] border border-[#3b4252] rounded p-2 text-xs text-white focus:outline-none focus:border-[#3B82F6]"
                  />
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-[10px] uppercase font-mono text-gray-400">Biomolecule Type</label>
                  <select
                    value={biomoleculeType}
                    onChange={(e) => setBiomoleculeType(e.target.value)}
                    className="bg-[#0B1220] border border-[#3b4252] rounded p-2 text-xs text-white focus:outline-none focus:border-[#3B82F6]"
                  >
                    <option value="Gene">Gene / Locus</option>
                    <option value="Virus">Virus / Pathogen</option>
                    <option value="Protein">Protein / Enzyme</option>
                    <option value="Bacteria">Bacteria</option>
                  </select>
                </div>

                <div className="flex flex-col gap-1.5">
                  <label className="text-[10px] uppercase font-mono text-gray-400">Context/Keywords (Optional)</label>
                  <input
                    type="text"
                    value={context}
                    onChange={(e) => setContext(e.target.value)}
                    placeholder="e.g. cell cycle, replication"
                    className="bg-[#0B1220] border border-[#3b4252] rounded p-2 text-xs text-white focus:outline-none focus:border-[#3B82F6]"
                  />
                </div>

                <div className="flex items-center gap-2 mt-1">
                  <input
                    type="checkbox"
                    id="offline"
                    checked={forceOffline}
                    onChange={(e) => setForceOffline(e.target.checked)}
                    className="h-3.5 w-3.5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                  />
                  <label htmlFor="offline" className="text-[11px] font-mono text-gray-400 cursor-pointer select-none">
                    Force Offline Fallback
                  </label>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-[#3B82F6] hover:bg-blue-600 text-white text-xs font-semibold py-2 px-4 rounded transition-colors disabled:opacity-50 mt-2 select-none"
                >
                  {loading ? 'Searching...' : 'Retrieve Literature'}
                </button>
              </form>

              {/* Cache queries history */}
              <div className="bg-[#1F2937] p-5 rounded-lg border border-[#3b4252] flex flex-col gap-3">
                <h3 className="text-sm font-bold font-mono text-[#60A5FA] border-b border-[#3b4252] pb-2">History Caches</h3>
                <div className="flex flex-col gap-2 max-h-[250px] overflow-y-auto pr-1">
                  {cachedQueries.length === 0 ? (
                    <p className="text-[10px] text-gray-500 italic">No search history found.</p>
                  ) : (
                    cachedQueries.map((q) => (
                      <div
                        key={q.id}
                        onClick={() => {
                          setBiomolecule(q.query_text.split('"')[1] || q.query_text);
                          setContext('');
                        }}
                        className="p-2 rounded bg-[#0B1220] hover:bg-[#111827] cursor-pointer border border-[#3b4252] flex flex-col gap-1 text-[10px] font-mono"
                      >
                        <span className="text-[#60A5FA] truncate">{q.query_text}</span>
                        <div className="flex justify-between text-gray-500 text-[8px]">
                          <span>Type: {q.query_type}</span>
                          <span>Papers: {q.article_count}</span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>

            {/* Results Display Panel */}
            <div className="lg:col-span-3 flex flex-col gap-4">
              {error && (
                <div className="bg-red-500/10 border border-red-500/50 text-red-200 p-4 rounded text-xs">
                  Error: {error}
                </div>
              )}

              {loading && (
                <div className="bg-[#1F2937] p-8 rounded-lg border border-[#3b4252] flex flex-col items-center justify-center gap-3">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-[#3B82F6]" />
                  <p className="text-xs text-gray-400 font-mono">Retrieving matching literature records from NCBI E-Utilities...</p>
                </div>
              )}

              {!loading && articles.length === 0 && !error && (
                <div className="bg-[#1F2937] p-12 rounded-lg border border-[#3b4252] text-center">
                  <p className="text-sm text-gray-500 italic">Enter parameters and run search to view literature evidence.</p>
                </div>
              )}

              {articles.length > 0 && (
                <div className="flex flex-col gap-4">
                  {/* Strategy Summary */}
                  {searchStrategy && summary && (
                    <div className="bg-[#1F2937] p-4 rounded-lg border border-[#3b4252] grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-mono">
                      <div>
                        <p className="text-gray-400 text-[10px]">Broad Search Strategy</p>
                        <p className="text-white mt-1 truncate" title={searchStrategy.broad_search_query}>
                          {searchStrategy.broad_search_query}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-400 text-[10px]">Total Papers Retrieved</p>
                        <p className="text-white mt-1 font-bold">{summary.total_retrieved}</p>
                      </div>
                      <div>
                        <p className="text-gray-400 text-[10px]">Average Relevance Score</p>
                        <p className="text-white mt-1 font-bold text-[#EAB308]">{summary.average_relevance_score.toFixed(2)}</p>
                      </div>
                    </div>
                  )}

                  {/* Curated list */}
                  <div className="flex flex-col gap-3">
                    {articles.map((art) => (
                      <div key={art.pmid} className="bg-[#1F2937] border border-[#3b4252] p-5 rounded-lg flex flex-col gap-3">
                        <div className="flex justify-between items-start gap-2">
                          <span className="text-[10px] font-mono text-[#06B6D4] bg-[#0B1220] px-2 py-0.5 rounded border border-[#3b4252]">
                            PMID: {art.pmid}
                          </span>
                          <span className="text-[9px] uppercase font-mono px-2 py-0.5 bg-[#3B82F6]/10 text-[#60A5FA] border border-[#3B82F6]/30 rounded">
                            {art.publication_type}
                          </span>
                        </div>
                        <h4 className="text-sm font-bold leading-snug">{art.title}</h4>
                        <p className="text-[10px] text-gray-400 font-mono">
                          {art.journal} ({art.publication_year}) | {art.authors.map(a => `${a.forename || ''} ${a.lastname || ''}`).join(', ')}
                        </p>
                        
                        {/* MeSH terms */}
                        {art.mesh_terms && art.mesh_terms.length > 0 && (
                          <div className="flex flex-wrap gap-1">
                            {art.mesh_terms.slice(0, 5).map(tag => (
                              <span key={tag} className="text-[8px] font-mono px-1.5 py-0.5 rounded bg-[#0B1220] border border-[#3b4252] text-gray-300">
                                {tag}
                              </span>
                            ))}
                          </div>
                        )}

                        <div className="flex gap-2 mt-2">
                          <button
                            onClick={() => setSelectedArticle(art)}
                            className="bg-[#0B1220] hover:bg-[#111827] border border-[#3b4252] text-white text-[10px] font-semibold py-1.5 px-4 rounded transition-colors select-none"
                          >
                            View Abstract
                          </button>
                          {art.doi && (
                            <a
                              href={`https://doi.org/${art.doi}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="bg-[#3B82F6]/20 hover:bg-[#3B82F6]/30 text-[#60A5FA] border border-[#3B82F6]/50 text-[10px] font-semibold py-1.5 px-4 rounded transition-colors flex items-center justify-center select-none"
                            >
                              Publisher DOI
                            </a>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Abstract display Modal */}
      {selectedArticle && (
        <div className="fixed inset-0 bg-black/75 flex items-center justify-center z-50 p-4 font-sans">
          <div className="bg-[#1F2937] border border-[#3B82F6] rounded-lg max-w-2xl w-full p-6 relative flex flex-col gap-4 max-h-[85vh]">
            <button
              onClick={() => setSelectedArticle(null)}
              className="absolute top-4 right-4 text-white hover:text-[#EF4444] font-bold"
            >
              ✕
            </button>
            <span className="text-xs font-mono text-[#06B6D4]">NCBI PubMed PMID: {selectedArticle.pmid}</span>
            <h4 className="text-sm font-bold leading-normal pr-8">{selectedArticle.title}</h4>
            <div className="overflow-y-auto pr-2 mt-2 text-xs leading-relaxed text-gray-300 whitespace-pre-wrap">
              {selectedArticle.abstract}
            </div>
            {selectedArticle.mesh_terms && (
              <div className="mt-4 border-t border-[#111827] pt-3">
                <span className="text-[10px] uppercase font-mono text-gray-400 block mb-1.5">MeSH Keywords</span>
                <div className="flex flex-wrap gap-1.5">
                  {selectedArticle.mesh_terms.map((tag) => (
                    <span key={tag} className="text-[9px] font-mono px-2 py-0.5 rounded bg-[#0B1220] border border-gray-700">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
