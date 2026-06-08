import React, { useState, useEffect } from 'react';
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
  const [searchFilter, setSearchFilter] = useState('');
  const [sortField, setSortField] = useState<'identity' | 'evalue' | 'bitscore'>('identity');
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('desc');

  const workflow = results.workflow_type;

  const [degThresholds, setDegThresholds] = useState({
    fdr_threshold: 0.05,
    lfc_threshold: 1.0,
    min_cpm: 0.5,
    min_sample_frac: 0.20
  });
  const [thresholdsLoaded, setThresholdsLoaded] = useState(false);
  const [thresholdSaved, setThresholdSaved] = useState(false);
  const [savingThresholds, setSavingThresholds] = useState(false);

  useEffect(() => {
    if (workflow === 'DEG' && results.job_id) {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
      fetch(`${apiBase}/jobs/${results.job_id}/thresholds`)
        .then((res) => {
          if (!res.ok) throw new Error('Failed to load thresholds');
          return res.json();
        })
        .then((data) => {
          setDegThresholds({
            fdr_threshold: data.fdr_threshold ?? 0.05,
            lfc_threshold: data.lfc_threshold ?? 1.0,
            min_cpm: data.min_cpm ?? 0.5,
            min_sample_frac: data.min_sample_frac ?? 0.20
          });
          setThresholdsLoaded(true);
        })
        .catch((err) => {
          console.error('Error fetching thresholds:', err);
          setThresholdsLoaded(true);
        });
    }
  }, [workflow, results.job_id]);

  const handleApplyThresholds = async () => {
    const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
    setSavingThresholds(true);
    setThresholdSaved(false);
    try {
      const res = await fetch(`${apiBase}/jobs/${results.job_id}/thresholds`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(degThresholds),
      });
      if (!res.ok) {
        throw new Error('Failed to save thresholds');
      }
      setThresholdSaved(true);

      const startRes = await fetch(`${apiBase}/jobs/${results.job_id}/restart`, {
        method: 'POST',
      });
      if (!startRes.ok) {
        const errBody = await startRes.json().catch(() => ({}));
        throw new Error(errBody?.detail || 'Failed to restart job');
      }

      window.location.href = `/workspace?jobId=${results.job_id}`;
    } catch (err) {
      console.error(err);
      alert('Error applying thresholds: ' + (err instanceof Error ? err.message : String(err)));
    } finally {
      setSavingThresholds(false);
    }
  };

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

            {workflow === 'DEG' && thresholdsLoaded && (
              <div className="col-span-1 md:col-span-3 bg-[#111827]/80 border border-[#30363d] rounded-xl p-6 shadow-2xl flex flex-col gap-6 transition-all duration-300 hover:border-[#3b82f6]/40">
                <div className="flex items-center justify-between border-b border-[#30363d] pb-4">
                  <div className="flex items-center gap-3">
                    <span className="material-symbols-outlined text-[#3b82f6] text-2xl">tune</span>
                    <div>
                      <h4 className="font-bold text-base text-white">Differential Gene Expression (DEG) Parameter Settings</h4>
                      <p className="text-xs text-[#8b949e] mt-0.5">Customize statistics and pre-filtering thresholds for this analysis job.</p>
                    </div>
                  </div>
                  {thresholdSaved && (
                    <span className="text-xs text-[#22c55e] font-semibold bg-[#22c55e]/10 border border-[#22c55e]/30 px-3 py-1 rounded-full flex items-center gap-1.5">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#22c55e]" />
                      Parameters Saved
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
                  {/* FDR (padj) Slider */}
                  <div className="flex flex-col gap-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-gray-300">FDR Threshold (adj. p-value)</span>
                      <span className="text-sm font-bold text-[#3b82f6] bg-[#3b82f6]/10 px-2 py-0.5 rounded font-mono">
                        {degThresholds.fdr_threshold.toFixed(3)}
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0.001"
                      max="0.100"
                      step="0.001"
                      value={degThresholds.fdr_threshold}
                      onChange={(e) =>
                        setDegThresholds({
                          ...degThresholds,
                          fdr_threshold: parseFloat(e.target.value),
                        })
                      }
                      className="w-full accent-[#3b82f6] bg-gray-700 h-1.5 rounded-lg appearance-none cursor-pointer"
                    />
                    <span className="text-[10px] text-[#8b949e]">
                      False Discovery Rate significance cutoff for multi-hypothesis test correction (Benjamini-Hochberg). Recommended: 0.05.
                    </span>
                  </div>

                  {/* Log2 Fold-Change (log2FC) Slider */}
                  <div className="flex flex-col gap-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-gray-300">Log2 Fold-Change (|log2FC|)</span>
                      <span className="text-sm font-bold text-[#3b82f6] bg-[#3b82f6]/10 px-2 py-0.5 rounded font-mono">
                        {degThresholds.lfc_threshold.toFixed(1)}
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0.0"
                      max="3.0"
                      step="0.1"
                      value={degThresholds.lfc_threshold}
                      onChange={(e) =>
                        setDegThresholds({
                          ...degThresholds,
                          lfc_threshold: parseFloat(e.target.value),
                        })
                      }
                      className="w-full accent-[#3b82f6] bg-gray-700 h-1.5 rounded-lg appearance-none cursor-pointer"
                    />
                    <span className="text-[10px] text-[#8b949e]">
                      Minimum absolute fold change required between Control vs Treatment groups. Recommended: 1.0.
                    </span>
                  </div>

                  {/* min_cpm Slider */}
                  <div className="flex flex-col gap-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-gray-300">Minimum Expression (CPM)</span>
                      <span className="text-sm font-bold text-[#3b82f6] bg-[#3b82f6]/10 px-2 py-0.5 rounded font-mono">
                        {degThresholds.min_cpm.toFixed(1)}
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0.0"
                      max="2.0"
                      step="0.1"
                      value={degThresholds.min_cpm}
                      onChange={(e) =>
                        setDegThresholds({
                          ...degThresholds,
                          min_cpm: parseFloat(e.target.value),
                        })
                      }
                      className="w-full accent-[#3b82f6] bg-gray-700 h-1.5 rounded-lg appearance-none cursor-pointer"
                    />
                    <span className="text-[10px] text-[#8b949e]">
                      Pre-filtering expression cutoff in Counts Per Million. Removes low-expression genes to restore statistical power. Recommended: 0.5.
                    </span>
                  </div>

                  {/* min_sample_frac Slider */}
                  <div className="flex flex-col gap-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-semibold text-gray-300">Min Sample Fraction</span>
                      <span className="text-sm font-bold text-[#3b82f6] bg-[#3b82f6]/10 px-2 py-0.5 rounded font-mono">
                        {degThresholds.min_sample_frac.toFixed(2)}
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0.00"
                      max="1.00"
                      step="0.05"
                      value={degThresholds.min_sample_frac}
                      onChange={(e) =>
                        setDegThresholds({
                          ...degThresholds,
                          min_sample_frac: parseFloat(e.target.value),
                        })
                      }
                      className="w-full accent-[#3b82f6] bg-gray-700 h-1.5 rounded-lg appearance-none cursor-pointer"
                    />
                    <span className="text-[10px] text-[#8b949e]">
                      Minimum fraction of samples that must express the gene above CPM threshold. Recommended: 0.20.
                    </span>
                  </div>
                </div>

                <div className="flex items-center justify-between border-t border-[#30363d] pt-4 mt-2">
                  <div className="flex items-center gap-2 text-[11px] text-[#8b949e]">
                    <span className="material-symbols-outlined text-sm text-[#eab308]">warning</span>
                    <span>Modifying settings will reset current results and execute the full analysis pipeline again.</span>
                  </div>
                  <button
                    onClick={handleApplyThresholds}
                    disabled={savingThresholds}
                    className="bg-[#3b82f6] hover:bg-[#2563eb] disabled:bg-[#1d4ed8]/50 text-white font-semibold px-6 py-2.5 rounded-lg transition-all flex items-center gap-2 shadow-lg shadow-[#3b82f6]/20 hover:shadow-[#3b82f6]/40 cursor-pointer text-xs"
                  >
                    {savingThresholds ? (
                      <>
                        <span className="material-symbols-outlined text-base animate-spin">sync</span>
                        Applying...
                      </>
                    ) : (
                      <>
                        <span className="material-symbols-outlined text-base">play_arrow</span>
                        Apply Thresholds & Re-run
                      </>
                    )}
                  </button>
                </div>
              </div>
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

        {activeTab === 'annotations' && results.annotations && (() => {
          const anns = results.annotations;

          // --- Computed stats ---
          const totalHits = anns.length;
          const uniqueTargets = [...new Set(anns.map(a => a.subject_protein))];
          const avgIdentity = anns.length > 0 ? anns.reduce((s, a) => s + a.identity_percent, 0) / anns.length : 0;
          const bestHit = anns.length > 0 ? anns.reduce((best, a) => a.identity_percent > best.identity_percent ? a : best, anns[0]) : null;
          const highConfCount = anns.filter(a => a.identity_percent >= 60).length;
          const medConfCount = anns.filter(a => a.identity_percent >= 30 && a.identity_percent < 60).length;
          const lowConfCount = anns.filter(a => a.identity_percent < 30).length;

          // --- Protein distribution (top 6 targets by frequency) ---
          const targetFreq: Record<string, number> = {};
          anns.forEach(a => { targetFreq[a.subject_protein] = (targetFreq[a.subject_protein] || 0) + 1; });
          const topTargets = Object.entries(targetFreq).sort((a, b) => b[1] - a[1]).slice(0, 6);
          const maxFreq = topTargets.length > 0 ? topTargets[0][1] : 1;

          // --- Filtered & sorted annotations ---
          const filtered = anns.filter(a =>
            !searchFilter ||
            a.query_protein.toLowerCase().includes(searchFilter.toLowerCase()) ||
            a.subject_protein.toLowerCase().includes(searchFilter.toLowerCase()) ||
            a.annotation.toLowerCase().includes(searchFilter.toLowerCase())
          );
          const sorted = [...filtered].sort((a, b) => {
            let va: number, vb: number;
            if (sortField === 'identity') { va = a.identity_percent; vb = b.identity_percent; }
            else if (sortField === 'evalue') { va = a.evalue; vb = b.evalue; }
            else { va = a.bitscore; vb = b.bitscore; }
            return sortDir === 'desc' ? vb - va : va - vb;
          });

          // --- Helpers ---
          const identityColor = (pct: number) => pct >= 60 ? '#22C55E' : pct >= 30 ? '#EAB308' : '#EF4444';
          const identityLabel = (pct: number) => pct >= 60 ? 'High' : pct >= 30 ? 'Moderate' : 'Low';
          const evalBadge = (ev: number) => {
            if (ev <= 1e-30) return { text: 'Excellent', color: 'text-[#22C55E]', bg: 'bg-[#22C55E]/10 border-[#22C55E]/30' };
            if (ev <= 1e-10) return { text: 'Strong', color: 'text-[#3B82F6]', bg: 'bg-[#3B82F6]/10 border-[#3B82F6]/30' };
            if (ev <= 1e-5)  return { text: 'Moderate', color: 'text-[#EAB308]', bg: 'bg-[#EAB308]/10 border-[#EAB308]/30' };
            return { text: 'Weak', color: 'text-[#EF4444]', bg: 'bg-[#EF4444]/10 border-[#EF4444]/30' };
          };

          const toggleSort = (field: 'identity' | 'evalue' | 'bitscore') => {
            if (sortField === field) setSortDir(d => d === 'desc' ? 'asc' : 'desc');
            else { setSortField(field); setSortDir(field === 'evalue' ? 'asc' : 'desc'); }
          };

          // Extract clean protein name from annotation string
          const cleanProteinName = (ann: string) => {
            const match = ann.match(/\(([^)]+)\)/);
            return match ? match[1] : ann.split('Match:')[1]?.trim() || ann;
          };

          return (
            <div className="flex flex-col gap-6">
              {/* Header */}
              <div className="border-b border-[#1F2937] pb-3">
                <h4 className="text-sm font-bold text-[#60A5FA] font-mono flex items-center gap-2">
                  <span className="inline-block w-2 h-2 rounded-full bg-[#3B82F6]" />
                  DIAMOND BLASTp Homology Analysis
                </h4>
                <p className="text-xs text-gray-400 mt-1">
                  Sequence similarity search against curated SwissProt protein database using DIAMOND ultra-fast aligner.
                </p>
              </div>

              {/* ── Summary Dashboard ── */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937] flex flex-col gap-1">
                  <p className="text-[10px] text-gray-500 font-mono uppercase tracking-wide">Total Hits</p>
                  <p className="text-2xl font-bold font-mono text-white">{totalHits}</p>
                  <p className="text-[10px] text-gray-500">aligned sequences</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937] flex flex-col gap-1">
                  <p className="text-[10px] text-gray-500 font-mono uppercase tracking-wide">Unique Targets</p>
                  <p className="text-2xl font-bold font-mono text-[#06B6D4]">{uniqueTargets.length}</p>
                  <p className="text-[10px] text-gray-500">SwissProt proteins</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937] flex flex-col gap-1">
                  <p className="text-[10px] text-gray-500 font-mono uppercase tracking-wide">Avg Identity</p>
                  <p className="text-2xl font-bold font-mono" style={{ color: identityColor(avgIdentity) }}>
                    {avgIdentity.toFixed(1)}%
                  </p>
                  <p className="text-[10px] text-gray-500">{identityLabel(avgIdentity)} confidence</p>
                </div>
                <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937] flex flex-col gap-1">
                  <p className="text-[10px] text-gray-500 font-mono uppercase tracking-wide">Best Hit</p>
                  <p className="text-lg font-bold font-mono text-[#22C55E] truncate">{bestHit?.identity_percent.toFixed(1)}%</p>
                  <p className="text-[10px] text-gray-400 truncate">{bestHit?.subject_protein}</p>
                </div>
              </div>

              {/* ── Confidence Distribution ── */}
              <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                <p className="text-[10px] text-gray-500 font-mono uppercase tracking-wide mb-3">Hit Confidence Distribution</p>
                <div className="flex gap-2 items-end h-6 w-full">
                  <div 
                    className="rounded-sm transition-all duration-500" 
                    style={{ 
                      width: `${totalHits > 0 ? (highConfCount / totalHits) * 100 : 0}%`, 
                      height: '100%', 
                      backgroundColor: '#22C55E',
                      minWidth: highConfCount > 0 ? '20px' : '0px'
                    }} 
                  />
                  <div 
                    className="rounded-sm transition-all duration-500" 
                    style={{ 
                      width: `${totalHits > 0 ? (medConfCount / totalHits) * 100 : 0}%`, 
                      height: '100%', 
                      backgroundColor: '#EAB308',
                      minWidth: medConfCount > 0 ? '20px' : '0px'
                    }} 
                  />
                  <div 
                    className="rounded-sm transition-all duration-500" 
                    style={{ 
                      width: `${totalHits > 0 ? (lowConfCount / totalHits) * 100 : 0}%`, 
                      height: '100%', 
                      backgroundColor: '#EF4444',
                      minWidth: lowConfCount > 0 ? '20px' : '0px'
                    }} 
                  />
                </div>
                <div className="flex gap-4 mt-2">
                  <span className="text-[10px] font-mono text-gray-400 flex items-center gap-1.5">
                    <span className="inline-block w-2 h-2 rounded-full bg-[#22C55E]" /> High (≥60%): {highConfCount}
                  </span>
                  <span className="text-[10px] font-mono text-gray-400 flex items-center gap-1.5">
                    <span className="inline-block w-2 h-2 rounded-full bg-[#EAB308]" /> Moderate (30-60%): {medConfCount}
                  </span>
                  <span className="text-[10px] font-mono text-gray-400 flex items-center gap-1.5">
                    <span className="inline-block w-2 h-2 rounded-full bg-[#EF4444]" /> Low (&lt;30%): {lowConfCount}
                  </span>
                </div>
              </div>

              {/* ── Top Target Proteins Distribution ── */}
              <div className="bg-[#0B1220] p-4 rounded-lg border border-[#1F2937]">
                <p className="text-[10px] text-gray-500 font-mono uppercase tracking-wide mb-3">Top SwissProt Target Proteins</p>
                <div className="flex flex-col gap-2">
                  {topTargets.map(([protein, count]) => (
                    <div key={protein} className="flex items-center gap-3">
                      <span className="text-[10px] font-mono text-[#60A5FA] w-36 truncate">{protein}</span>
                      <div className="flex-1 h-5 bg-[#111827] rounded-sm overflow-hidden relative">
                        <div
                          className="h-full rounded-sm transition-all duration-700"
                          style={{
                            width: `${(count / maxFreq) * 100}%`,
                            background: 'linear-gradient(90deg, #3B82F6, #06B6D4)'
                          }}
                        />
                        <span className="absolute right-2 top-0.5 text-[9px] font-mono text-gray-300">{count} hits</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* ── Search + Sort Controls ── */}
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="relative flex-1 min-w-[200px] max-w-sm">
                  <input
                    type="text"
                    placeholder="Search by query, target, or annotation..."
                    value={searchFilter}
                    onChange={e => setSearchFilter(e.target.value)}
                    className="w-full bg-[#0B1220] border border-[#1F2937] rounded px-3 py-2 text-xs font-mono text-white placeholder-gray-500 focus:border-[#3B82F6] focus:outline-none transition-colors"
                  />
                  {searchFilter && (
                    <button
                      onClick={() => setSearchFilter('')}
                      className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-white text-xs"
                    >
                      ✕
                    </button>
                  )}
                </div>
                <div className="flex gap-2">
                  {(['identity', 'evalue', 'bitscore'] as const).map(f => (
                    <button
                      key={f}
                      onClick={() => toggleSort(f)}
                      className={`text-[10px] font-mono uppercase px-3 py-1.5 rounded border transition-colors ${
                        sortField === f
                          ? 'bg-[#3B82F6]/20 border-[#3B82F6]/50 text-[#60A5FA]'
                          : 'bg-[#0B1220] border-[#1F2937] text-gray-400 hover:border-gray-500'
                      }`}
                    >
                      {f === 'identity' ? 'Identity %' : f === 'evalue' ? 'E-Value' : 'Bit Score'}
                      {sortField === f && <span className="ml-1">{sortDir === 'desc' ? '↓' : '↑'}</span>}
                    </button>
                  ))}
                </div>
                <span className="text-[10px] text-gray-500 font-mono">
                  Showing {sorted.length} of {totalHits}
                </span>
              </div>

              {/* ── Results Table ── */}
              <div className="overflow-x-auto rounded-lg border border-[#1F2937]">
                <table className="min-w-full divide-y divide-[#1F2937] text-sm">
                  <thead className="bg-[#0B1220]">
                    <tr>
                      <th className="px-4 py-3 text-left text-[10px] font-mono text-gray-500 uppercase tracking-wider">#</th>
                      <th className="px-4 py-3 text-left text-[10px] font-mono text-gray-500 uppercase tracking-wider">Query Seq</th>
                      <th className="px-4 py-3 text-left text-[10px] font-mono text-gray-500 uppercase tracking-wider">SwissProt Target</th>
                      <th className="px-4 py-3 text-left text-[10px] font-mono text-gray-500 uppercase tracking-wider">Protein Function</th>
                      <th className="px-4 py-3 text-left text-[10px] font-mono text-gray-500 uppercase tracking-wider">Identity</th>
                      <th className="px-4 py-3 text-left text-[10px] font-mono text-gray-500 uppercase tracking-wider">E-Value</th>
                      <th className="px-4 py-3 text-left text-[10px] font-mono text-gray-500 uppercase tracking-wider">Bit Score</th>
                      <th className="px-4 py-3 text-right text-[10px] font-mono text-gray-500 uppercase tracking-wider">Links</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#111827]">
                    {sorted.map((ann, idx) => {
                      const badge = evalBadge(ann.evalue);
                      const protName = cleanProteinName(ann.annotation);
                      const rawRow = `Query: ${ann.query_protein} | Subject: ${ann.subject_protein} | Identity: ${ann.identity_percent}% | E-value: ${ann.evalue} | Bitscore: ${ann.bitscore} | Annotation: ${ann.annotation}`;
                      const uniprotId = ann.subject_protein.split('_')[0];

                      return (
                        <tr key={idx} className="hover:bg-[#172033] transition-colors group">
                          <td className="px-4 py-3 text-[10px] font-mono text-gray-600">{idx + 1}</td>
                          <td className="px-4 py-3 font-mono font-bold text-[#60A5FA] text-xs">{ann.query_protein}</td>
                          <td className="px-4 py-3">
                            <span className="font-mono text-xs text-white font-semibold">{ann.subject_protein}</span>
                          </td>
                          <td className="px-4 py-3 text-xs text-gray-300 max-w-[180px] truncate" title={protName}>
                            {protName}
                          </td>
                          <td className="px-4 py-3">
                            <div className="flex items-center gap-2">
                              <div className="w-16 h-2 bg-[#111827] rounded-full overflow-hidden">
                                <div
                                  className="h-full rounded-full transition-all duration-500"
                                  style={{
                                    width: `${Math.min(ann.identity_percent, 100)}%`,
                                    backgroundColor: identityColor(ann.identity_percent)
                                  }}
                                />
                              </div>
                              <span className="text-xs font-mono font-semibold" style={{ color: identityColor(ann.identity_percent) }}>
                                {ann.identity_percent.toFixed(1)}%
                              </span>
                            </div>
                          </td>
                          <td className="px-4 py-3">
                            <span className={`text-[9px] font-mono px-2 py-0.5 rounded border ${badge.bg} ${badge.color}`}>
                              {ann.evalue.toExponential(2)} · {badge.text}
                            </span>
                          </td>
                          <td className="px-4 py-3 font-mono text-xs text-gray-300">{ann.bitscore?.toFixed(1) || '—'}</td>
                          <td className="px-4 py-3 text-right">
                            <div className="flex gap-1.5 justify-end opacity-60 group-hover:opacity-100 transition-opacity">
                              <a
                                href={`https://www.uniprot.org/uniprot/${uniprotId}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-[9px] font-mono px-2 py-1 rounded bg-[#111827] border border-[#1F2937] text-[#60A5FA] hover:border-[#3B82F6] hover:text-white transition-colors"
                                title="View on UniProt"
                              >
                                UniProt ↗
                              </a>
                              <button
                                onClick={() => copyAnnotationRow(rawRow, idx)}
                                className="text-[9px] font-mono px-2 py-1 rounded bg-[#111827] border border-[#1F2937] text-gray-400 hover:border-gray-500 hover:text-white transition-colors"
                              >
                                {copiedIndex === idx ? '✓' : 'Copy'}
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          );
        })()}

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
                      const url = (kegg as any).url || (isKeggMap 
                        ? `https://www.genome.jp/dbget-bin/www_bget?pathway+${cleanId}`
                        : `https://www.google.com/search?q=KEGG+pathway+${encodeURIComponent(kegg.pathway_name)}`);

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
