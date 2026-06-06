import React, { useState } from 'react';
import { PipelineResults } from '../types';
import { VolcanoPlot } from './VolcanoPlot';
import { DomainViewer } from './DomainViewer';
import { TaxonomyTree } from './TaxonomyTree';
import { AIReport } from './AIReport';

interface ResultsViewerProps {
  results: PipelineResults;
}

export const ResultsViewer: React.FC<ResultsViewerProps> = ({ results }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedGene, setSelectedGene] = useState<any>(null);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const workflow = results.workflow_type;

  const downloadFile = (reportType: string, path: string) => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
    const backendBase = apiBase.replace(/\/api$/, '');
    if (reportType) {
      window.open(`${apiBase}/reports/${results.job_id}/${reportType.toLowerCase()}`, '_blank');
    } else {
      window.open(`${backendBase}${path}`, '_blank');
    }
  };

  const copyAnnotationRow = (rowText: string, index: number) => {
    navigator.clipboard.writeText(rowText).then(() => {
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    });
  };

  return (
    <div className="bg-[#1F2937] p-6 rounded-lg border border-[#1F2937] text-[#F9FAFB] flex flex-col gap-6">
      <div className="flex items-center justify-between border-b border-[#111827] pb-3">
        <h3 className="text-lg font-bold text-[#60A5FA]">Scientific Analysis Workspace</h3>
        <span className="text-xs uppercase font-mono px-2 py-1 rounded bg-[#0B1220] border border-[#1F2937] text-[#22C55E]">
          {workflow} Output
        </span>
      </div>

      {/* Tabs headers */}
      <div className="flex flex-wrap gap-2 border-b border-[#111827] pb-2">
        <button
          onClick={() => setActiveTab('overview')}
          className={`px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
            activeTab === 'overview' ? 'bg-[#3B82F6]' : 'hover:bg-[#172033]'
          }`}
        >
          Overview
        </button>

        {workflow !== 'DEG' && (
          <>
            <button
              onClick={() => setActiveTab('orfs')}
              className={`px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
                activeTab === 'orfs' ? 'bg-[#3B82F6]' : 'hover:bg-[#172033]'
              }`}
            >
              ORF & Domains
            </button>
            <button
              onClick={() => setActiveTab('annotations')}
              className={`px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
                activeTab === 'annotations' ? 'bg-[#3B82F6]' : 'hover:bg-[#172033]'
              }`}
            >
              Homology (DIAMOND)
            </button>
            <button
              onClick={() => setActiveTab('taxonomy')}
              className={`px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
                activeTab === 'taxonomy' ? 'bg-[#3B82F6]' : 'hover:bg-[#172033]'
              }`}
            >
              Taxonomy
            </button>
          </>
        )}

        {workflow === 'DEG' && (
          <>
            <button
              onClick={() => setActiveTab('volcano')}
              className={`px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
                activeTab === 'volcano' ? 'bg-[#3B82F6]' : 'hover:bg-[#172033]'
              }`}
            >
              Volcano Plot
            </button>
            <button
              onClick={() => setActiveTab('drilldown')}
              className={`px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
                activeTab === 'drilldown' ? 'bg-[#3B82F6]' : 'hover:bg-[#172033]'
              }`}
            >
              Gene Drill-Down
            </button>
          </>
        )}

        <button
          onClick={() => setActiveTab('pathways')}
          className={`px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
            activeTab === 'pathways' ? 'bg-[#3B82F6]' : 'hover:bg-[#172033]'
          }`}
        >
          Pathways (KEGG)
        </button>

        <button
          onClick={() => setActiveTab('ai')}
          className={`px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
            activeTab === 'ai' ? 'bg-[#3B82F6]' : 'hover:bg-[#172033]'
          }`}
        >
          AI Pathobiology
        </button>

        <button
          onClick={() => setActiveTab('pubmed_lit')}
          className={`px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
            activeTab === 'pubmed_lit' ? 'bg-[#3B82F6]' : 'hover:bg-[#172033]'
          }`}
        >
          PubMed Literature
        </button>

        <button
          onClick={() => setActiveTab('downloads')}
          className={`px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
            activeTab === 'downloads' ? 'bg-[#3B82F6]' : 'hover:bg-[#172033]'
          }`}
        >
          Download Center
        </button>

        {results.visualizations && results.visualizations.length > 0 && (
          <button
            onClick={() => setActiveTab('visualizations')}
            className={`px-4 py-2 rounded text-xs font-semibold uppercase tracking-wider transition-colors ${
              activeTab === 'visualizations' ? 'bg-[#3B82F6]' : 'hover:bg-[#172033]'
            }`}
          >
            Visualizations
          </button>
        )}
      </div>

      {/* Tabs content */}
      <div className="flex flex-col gap-4">
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {results.fasta_run && (
              <>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Genome Length</p>
                  <p className="text-2xl font-bold font-mono">{results.fasta_run.genome_length.toLocaleString()} bp</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">GC Content</p>
                  <p className="text-2xl font-bold font-mono">{results.fasta_run.gc_content.toFixed(2)} %</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Ambiguity (N count)</p>
                  <p className="text-2xl font-bold font-mono">{results.fasta_run.ambiguity_count.toLocaleString()}</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Predicted ORFs</p>
                  <p className="text-2xl font-bold font-mono">{results.fasta_run.total_orfs}</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Translated Proteins</p>
                  <p className="text-2xl font-bold font-mono">{results.fasta_run.translated_proteins}</p>
                </div>
              </>
            )}

            {results.fastq_run && (
              <>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Raw Reads</p>
                  <p className="text-2xl font-bold font-mono">{results.fastq_run.raw_reads.toLocaleString()}</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Filtered Reads</p>
                  <p className="text-2xl font-bold font-mono">{results.fastq_run.filtered_reads.toLocaleString()}</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Average Read Quality</p>
                  <p className="text-2xl font-bold font-mono">Q{results.fastq_run.average_quality.toFixed(1)}</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Assembly Contigs</p>
                  <p className="text-2xl font-bold font-mono">{results.fastq_run.assembly_contigs}</p>
                </div>
              </>
            )}

            {results.deg_run && (
              <>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Total Genes Mapped</p>
                  <p className="text-2xl font-bold font-mono">{results.deg_run.total_genes.toLocaleString()}</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Significant DEGs</p>
                  <p className="text-2xl font-bold font-mono text-[#EAB308]">{results.deg_run.significant_genes}</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Upregulated (log2FC ≥ 1.0)</p>
                  <p className="text-2xl font-bold font-mono text-[#22C55E]">{results.deg_run.upregulated}</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                  <p className="text-xs text-[#9CA3AF] font-mono">Downregulated (log2FC ≤ -1.0)</p>
                  <p className="text-2xl font-bold font-mono text-[#EF4444]">{results.deg_run.downregulated}</p>
                </div>
              </>
            )}
          </div>
        )}

        {activeTab === 'orfs' && results.pfam_domains && (
          <DomainViewer 
            domains={results.pfam_domains} 
            annotations={results.annotations || []}
            orfs={results.orfs || []}
          />
        )}

        {activeTab === 'annotations' && results.annotations && (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-[#1F2937] text-sm">
              <thead className="bg-[#0B1220]">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-mono text-[#9CA3AF]">Query</th>
                  <th className="px-4 py-2 text-left text-xs font-mono text-[#9CA3AF]">SwissProt Hit</th>
                  <th className="px-4 py-2 text-left text-xs font-mono text-[#9CA3AF]">Identity %</th>
                  <th className="px-4 py-2 text-left text-xs font-mono text-[#9CA3AF]">E-Value</th>
                  <th className="px-4 py-2 text-left text-xs font-mono text-[#9CA3AF]">Annotation</th>
                  <th className="px-4 py-2 text-right text-xs font-mono text-[#9CA3AF]">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1F2937]">
                {results.annotations.map((ann, idx) => {
                  const rawRow = `Query: ${ann.query_protein} | Subject: ${ann.subject_protein} | Identity: ${ann.identity_percent}% | E-value: ${ann.evalue} | Annotation: ${ann.annotation}`;
                  return (
                    <tr key={idx} className="hover:bg-[#172033]">
                      <td className="px-4 py-2 font-mono font-bold text-[#60A5FA]">{ann.query_protein}</td>
                      <td className="px-4 py-2 font-mono">{ann.subject_protein}</td>
                      <td className="px-4 py-2 font-mono">{ann.identity_percent}%</td>
                      <td className="px-4 py-2 font-mono">{ann.evalue.toExponential(2)}</td>
                      <td className="px-4 py-2 text-gray-300">{ann.annotation}</td>
                      <td className="px-4 py-2 text-right">
                        <button
                          onClick={() => copyAnnotationRow(rawRow, idx)}
                          className="text-[#60A5FA] hover:text-[#3B82F6] text-xs font-mono select-none"
                        >
                          {copiedIndex === idx ? '✓ Copied' : 'Copy'}
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {activeTab === 'taxonomy' && results.taxonomy_results && (
          <TaxonomyTree taxonomy={results.taxonomy_results} />
        )}

        {activeTab === 'volcano' && (
          <div className="bg-[#0B1220] p-6 rounded-lg">
            <VolcanoPlot onSelectGene={setSelectedGene} />
          </div>
        )}

        {activeTab === 'drilldown' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
              <h4 className="text-sm font-bold text-[#60A5FA] border-b border-[#1F2937] pb-2 mb-3">Significant Gene Listings</h4>
              <div className="flex flex-col gap-2 overflow-y-auto max-h-[300px] pr-2">
                {['MAPK1', 'IL6', 'TNF', 'TP53', 'EGFR', 'STAT3'].map((gene) => (
                  <div
                    key={gene}
                    onClick={() => setSelectedGene({ symbol: gene, fc: gene === 'TP53' || gene === 'EGFR' || gene === 'STAT3' ? 2.4 : -1.8, fdr: 0.002 })}
                    className="p-2 rounded bg-[#172033] hover:bg-[#1F2937] cursor-pointer flex justify-between text-xs font-mono"
                  >
                    <span>{gene}</span>
                    <span className={gene === 'TP53' || gene === 'EGFR' || gene === 'STAT3' ? 'text-[#22C55E]' : 'text-[#EF4444]'}>
                      {gene === 'TP53' || gene === 'EGFR' || gene === 'STAT3' ? 'UP' : 'DOWN'}
                    </span>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937] flex flex-col gap-4">
              <h4 className="text-sm font-bold text-[#60A5FA] border-b border-[#1F2937] pb-2">Gene Inspector</h4>
              {selectedGene ? (
                <div className="flex flex-col gap-2 font-mono text-xs">
                  <p><strong>Gene Symbol</strong>: {selectedGene.symbol}</p>
                  <p><strong>log2 Fold Change</strong>: {selectedGene.fc}</p>
                  <p><strong>FDR p-adj</strong>: {selectedGene.fdr}</p>
                  <button
                    onClick={() => navigator.clipboard.writeText(`Gene: ${selectedGene.symbol} | Log2FC: ${selectedGene.fc} | FDR: ${selectedGene.fdr}`)}
                    className="mt-4 bg-[#3B82F6] hover:bg-blue-600 text-white font-semibold py-1 px-3 rounded w-24 select-none"
                  >
                    Copy Gene
                  </button>
                </div>
              ) : (
                <p className="text-gray-500 italic text-xs">Select a gene from the volcano plot or list to inspect details.</p>
              )}
            </div>
          </div>
        )}

        {activeTab === 'ai' && results.ai_interpretation && (
          <AIReport ai={results.ai_interpretation} />
        )}

        {activeTab === 'pubmed_lit' && (
          <div className="flex flex-col gap-4">
            <div className="border-b border-[#1F2937] pb-2">
              <h4 className="text-sm font-bold text-[#60A5FA] font-mono">Retrieved PubMed Literature Evidence</h4>
              <p className="text-xs text-gray-400 mt-1">
                Scientific articles retrieved from the NCBI PubMed database matching identified target genes, pathways, or pathogens.
              </p>
            </div>
            
            {results.pubmed && results.pubmed.length > 0 ? (
              <div className="grid grid-cols-1 gap-4">
                {results.pubmed.map((art) => (
                  <div key={art.pmid} className="bg-[#0B1220] border border-[#1F2937] p-5 rounded-lg flex flex-col gap-3">
                    <div className="flex justify-between items-start gap-2">
                      <span className="text-[10px] font-mono text-[#06B6D4] bg-[#111827] px-2.5 py-0.5 rounded border border-[#1F2937]">
                        PMID: {art.pmid}
                      </span>
                      {art.publication_type && (
                        <span className="text-[9px] uppercase font-mono px-2 py-0.5 bg-[#3B82F6]/10 text-[#60A5FA] border border-[#3B82F6]/30 rounded">
                          {art.publication_type}
                        </span>
                      )}
                    </div>
                    
                    <h4 className="text-sm font-bold leading-snug">{art.title}</h4>
                    
                    <p className="text-[10px] text-gray-400 font-mono">
                      {art.journal} ({art.publication_year}) | {art.authors.map(a => `${a.forename || ''} ${a.lastname || ''}`).join(', ')}
                    </p>
                    
                    <div className="text-xs leading-relaxed text-gray-300 bg-[#111827] p-3 rounded border border-[#1F2937] whitespace-pre-wrap">
                      {art.abstract}
                    </div>

                    {art.mesh_terms && art.mesh_terms.length > 0 && (
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {art.mesh_terms.map(tag => (
                          <span key={tag} className="text-[9px] font-mono px-2 py-0.5 rounded bg-[#111827] border border-gray-700 text-gray-300">
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}

                    <div className="flex gap-3 mt-2 pt-2 border-t border-[#111827]">
                      <a
                        href={`https://pubmed.ncbi.nlm.nih.gov/${art.pmid}/`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-[#3B82F6] hover:bg-blue-600 text-white text-xs font-semibold py-1.5 px-4 rounded transition-colors flex items-center justify-center select-none"
                      >
                        View PubMed Article ↗
                      </a>
                      {art.doi && (
                        <a
                          href={`https://doi.org/${art.doi}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="bg-[#172033] hover:bg-[#1F2937] border border-[#1F2937] text-white text-xs font-semibold py-1.5 px-4 rounded transition-colors flex items-center justify-center select-none"
                        >
                          Publisher DOI ↗
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 italic text-xs">No PubMed literature evidence retrieved or cached for this analysis.</p>
            )}
          </div>
        )}

        {activeTab === 'pathways' && results.kegg_results && (
          <div className="flex flex-col gap-4">
            <div className="border-b border-[#1F2937] pb-2">
              <h4 className="text-sm font-bold text-[#60A5FA] font-mono">KEGG Pathway Mapping & Significance Analysis</h4>
              <p className="text-xs text-gray-400 mt-1">
                Genes mapped to functional KEGG database categories, with significance scores and hyperlinked pathway entry cards.
              </p>
            </div>
            {results.kegg_results.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-[#1F2937] text-sm">
                  <thead className="bg-[#0B1220]">
                    <tr>
                      <th className="px-4 py-2 text-left text-xs font-mono text-[#9CA3AF]">Pathway ID</th>
                      <th className="px-4 py-2 text-left text-xs font-mono text-[#9CA3AF]">Pathway Term / Name</th>
                      <th className="px-4 py-2 text-left text-xs font-mono text-[#9CA3AF]">Gene Count</th>
                      <th className="px-4 py-2 text-left text-xs font-mono text-[#9CA3AF]">P-value</th>
                      <th className="px-4 py-2 text-left text-xs font-mono text-[#9CA3AF]">FDR (adj.p)</th>
                      <th className="px-4 py-2 text-right text-xs font-mono text-[#9CA3AF]">External Reference</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#1F2937]">
                    {results.kegg_results.map((kegg, idx) => {
                      const cleanId = kegg.pathway_id.trim();
                      const isKeggMap = /^[a-zA-Z]{3,4}\d+$/.test(cleanId) || cleanId.startsWith("map") || cleanId.startsWith("hsa");
                      const url = isKeggMap 
                        ? `https://www.genome.jp/dbget-bin/www_bget?pathway+${cleanId}`
                        : `https://www.google.com/search?q=KEGG+pathway+${encodeURIComponent(kegg.pathway_name)}`;

                      return (
                        <tr key={idx} className="hover:bg-[#172033]">
                          <td className="px-4 py-2 font-mono font-bold text-[#60A5FA]">
                            {isKeggMap ? (
                              <a href={url} target="_blank" rel="noopener noreferrer" className="hover:underline">
                                {cleanId}
                              </a>
                            ) : (
                              cleanId
                            )}
                          </td>
                          <td className="px-4 py-2 text-gray-300 font-medium">{kegg.pathway_name}</td>
                          <td className="px-4 py-2 font-mono">{kegg.gene_count}</td>
                          <td className="px-4 py-2 font-mono">
                            {kegg.pvalue !== undefined && kegg.pvalue !== null && !isNaN(Number(kegg.pvalue)) 
                              ? Number(kegg.pvalue).toExponential(2) 
                              : 'N/A'}
                          </td>
                          <td className="px-4 py-2 font-mono">
                            {kegg.fdr !== undefined && kegg.fdr !== null && !isNaN(Number(kegg.fdr)) 
                              ? Number(kegg.fdr).toExponential(2) 
                              : 'N/A'}
                          </td>
                          <td className="px-4 py-2 text-right">
                            <a 
                              href={url} 
                              target="_blank" 
                              rel="noopener noreferrer" 
                              className="text-xs text-[#60A5FA] hover:text-[#3B82F6] hover:underline font-mono"
                            >
                              KEGG Card ↗
                            </a>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-gray-500 italic text-xs">No KEGG pathway mappings or enriched terms detected for this run.</p>
            )}
          </div>
        )}

        {activeTab === 'downloads' && results.reports && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {results.reports.map((report) => (
              <div key={report.report_type} className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937] flex flex-col gap-2 justify-between">
                <div>
                  <h4 className="text-sm font-bold text-[#60A5FA] font-mono">{report.report_type} Format</h4>
                  <p className="text-xs text-gray-500 mt-1">Grounded pipeline audit dump.</p>
                </div>
                <button
                  onClick={() => downloadFile(report.report_type, report.report_path)}
                  className="bg-[#3B82F6] hover:bg-blue-600 text-white text-xs font-semibold py-1.5 px-3 rounded w-full mt-3 transition-colors"
                >
                  Download Report
                </button>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'visualizations' && results.visualizations && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {results.visualizations.map((url, idx) => {
              const filename = url.split('/').pop() || '';
              const title = filename
                .replace(/\.[^/.]+$/, "")
                .replace(/_/g, " ")
                .replace(/\b\w/g, c => c.toUpperCase());

              return (
                <div key={idx} className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937] flex flex-col gap-3">
                  <h4 className="text-sm font-bold text-[#60A5FA] font-mono">{title}</h4>
                  <div className="bg-[#172033] rounded p-2 flex items-center justify-center border border-[#1F2937]">
                    <img 
                      src={`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${url}`} 
                      alt={title}
                      className="max-h-[350px] object-contain rounded hover:scale-105 transition-transform duration-200" 
                    />
                  </div>
                  <div className="flex gap-2 justify-end">
                    <button
                      onClick={() => window.open(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}${url}`, '_blank')}
                      className="text-xs text-[#60A5FA] hover:text-[#3B82F6] font-semibold"
                    >
                      View Full Size
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
