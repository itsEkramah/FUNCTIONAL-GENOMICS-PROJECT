'use client';

import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';
import { Job } from '../../types';

export default function ReportsPage() {
  const [reports, setReports] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedWorkflow, setSelectedWorkflow] = useState('All Workflows');
  const [selectedQuality, setSelectedQuality] = useState<string | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const jobs = await api.getAllJobs();
        const completedJobs = jobs.filter((j) => j.status === 'COMPLETED');
        setReports(completedJobs);
      } catch (err) {
        console.error('Failed to query reports.');
      } finally {
        setLoading(false);
      }
    };
    fetchReports();
  }, []);

  const downloadReport = (jobId: string, format: string) => {
    // Show download toast
    setToastMessage(`Download started for ${format} format...`);
    setTimeout(() => setToastMessage(null), 3000);

    // Direct link to compiled assets folder mapped inside backend report services
    window.open(`${process.env.NEXT_PUBLIC_API_URL}/reports/${jobId}/${format.toLowerCase()}`, '_blank');
  };

  const clearFilters = () => {
    setSearch('');
    setSelectedWorkflow('All Workflows');
    setSelectedQuality(null);
  };

  const filtered = reports.filter((r) => {
    const matchesSearch = r.job_name.toLowerCase().includes(search.toLowerCase()) || r.workflow_type.toLowerCase().includes(search.toLowerCase());
    const matchesWorkflow = selectedWorkflow === 'All Workflows' || r.workflow_type === selectedWorkflow;
    
    // Quality classification match
    let matchesQuality = true;
    if (selectedQuality === 'High') {
      matchesQuality = r.progress_percent >= 90;
    } else if (selectedQuality === 'Med') {
      matchesQuality = r.progress_percent < 90;
    }

    return matchesSearch && matchesWorkflow && matchesQuality;
  });

  return (
    <div className="p-inner-padding max-w-container-max mx-auto space-y-6 bg-[#0c1321] text-[#dce2f6]">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 select-none">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Reports Center</h1>
          <p className="text-xs text-text-muted mt-1">Review and export detailed genomic analysis outputs.</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 px-4 py-2 bg-[#232a39] border border-[#424754] rounded-lg text-on-surface-variant hover:bg-[#2e3544] transition-colors text-xs font-semibold">
            <span className="material-symbols-outlined text-base">filter_list</span>
            Filters
          </button>
          <div className="h-8 w-px bg-[#424754] mx-2"></div>
          <div className="flex bg-[#151b2a] border border-[#424754] rounded-lg p-1 text-xs">
            <button className="px-3 py-1 bg-[#4d8eff] text-[#00285d] rounded font-semibold">List</button>
            <button className="px-3 py-1 text-on-surface-variant hover:text-white transition-colors">Grid</button>
          </div>
        </div>
      </div>

      {/* Filters Strip */}
      <div className="bg-[#19202e] p-4 rounded-xl border border-[#424754] flex flex-wrap gap-4 items-end select-none">
        <div className="space-y-1.5">
          <label className="block text-[10px] font-mono text-text-muted uppercase tracking-wider">Workflow Type</label>
          <select
            value={selectedWorkflow}
            onChange={(e) => setSelectedWorkflow(e.target.value)}
            className="bg-[#172033] border border-[#424754] text-on-surface rounded-lg px-3 py-2 text-xs font-mono w-48 outline-none"
          >
            <option>All Workflows</option>
            <option>FASTA</option>
            <option>FASTQ</option>
            <option>DEG</option>
          </select>
        </div>
        <div className="space-y-1.5">
          <label className="block text-[10px] font-mono text-text-muted uppercase tracking-wider">Search keyword</label>
          <input
            type="text"
            placeholder="Filter by name..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-[#172033] border border-[#424754] text-on-surface rounded-lg px-3 py-2 text-xs font-mono w-48 outline-none focus:border-primary"
          />
        </div>
        <div className="space-y-1.5">
          <label className="block text-[10px] font-mono text-text-muted uppercase tracking-wider">Confidence Level</label>
          <div className="flex gap-2">
            <button
              onClick={() => setSelectedQuality(selectedQuality === 'High' ? null : 'High')}
              className={`px-3 py-2 border rounded-lg text-xs font-mono transition-all ${
                selectedQuality === 'High' ? 'bg-primary border-primary text-[#00285d]' : 'bg-[#172033] border-[#424754] text-on-surface-variant'
              }`}
            >
              High
            </button>
            <button
              onClick={() => setSelectedQuality(selectedQuality === 'Med' ? null : 'Med')}
              className={`px-3 py-2 border rounded-lg text-xs font-mono transition-all ${
                selectedQuality === 'Med' ? 'bg-primary border-primary text-[#00285d]' : 'bg-[#172033] border-[#424754] text-on-surface-variant'
              }`}
            >
              Med
            </button>
          </div>
        </div>
        <button onClick={clearFilters} className="ml-auto text-xs text-primary font-semibold hover:underline">
          Clear all filters
        </button>
      </div>

      {/* Reports Table */}
      <div className="bg-[#19202e] rounded-xl border border-[#424754] overflow-hidden">
        <div className="overflow-x-auto custom-scrollbar">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#232a39] border-b border-[#424754] select-none text-[10px] text-text-muted uppercase tracking-wider font-mono">
                <th className="px-6 py-4 font-semibold">Analysis Name / ID</th>
                <th className="px-6 py-4 font-semibold">Workflow</th>
                <th className="px-6 py-4 font-semibold">Completed Date</th>
                <th className="px-6 py-4 font-semibold">Quality Rate</th>
                <th className="px-6 py-4 font-semibold">Exports</th>
                <th className="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#424754] text-xs font-mono">
              {loading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-text-muted italic">Querying reports center archive...</td>
                </tr>
              ) : filtered.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-12 text-center text-text-muted italic">No reports found matching selection.</td>
                </tr>
              ) : (
                filtered.map((rep) => {
                  const isHighQuality = rep.progress_percent >= 90;
                  return (
                    <tr key={rep.id} className="hover:bg-[#172033] transition-colors">
                      <td className="px-6 py-5">
                        <div className="flex flex-col">
                          <span className="font-semibold text-white">{rep.job_name}</span>
                          <span className="text-[10px] text-text-muted uppercase">JOB-{rep.id.slice(0, 8)}</span>
                        </div>
                      </td>
                      <td className="px-6 py-5">
                        <div className="flex items-center gap-2">
                          <span className="material-symbols-outlined text-secondary text-base">hub</span>
                          <span className="text-on-surface-variant">{rep.workflow_type} Pipeline</span>
                        </div>
                      </td>
                      <td className="px-6 py-5 text-on-surface-variant">
                        {new Date(rep.created_at).toLocaleString()}
                      </td>
                      <td className="px-6 py-5">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                          isHighQuality ? 'bg-success/10 border-success/20 text-success' : 'bg-warning/10 border-warning/20 text-warning'
                        }`}>
                          {isHighQuality ? 'High (98.2%)' : 'Med (84.1%)'}
                        </span>
                      </td>
                      <td className="px-6 py-5">
                        <div className="flex gap-1.5 select-none">
                          {['HTML', 'PDF', 'CSV', 'JSON'].map((format) => (
                            <button
                              key={format}
                              onClick={() => downloadReport(rep.id, format)}
                              className="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant text-[10px] font-bold"
                              title={format}
                            >
                              {format.slice(0, 3)}
                            </button>
                          ))}
                        </div>
                      </td>
                      <td className="px-6 py-5 text-right">
                        <button className="material-symbols-outlined text-on-surface-variant hover:text-primary text-base">open_in_new</button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Bento Insights Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 select-none">
        {/* Card 1 */}
        <div className="bg-[#19202e] rounded-xl border border-[#424754] p-card-padding flex flex-col justify-between">
          <div>
            <h3 className="font-semibold text-xs text-white uppercase tracking-wider">Storage Utilization</h3>
            <p className="text-text-muted text-xs mt-1">Archived results consume 84% of allocated storage tiers.</p>
          </div>
          <div className="mt-4">
            <div className="w-full bg-[#0c1321] h-2 rounded-full overflow-hidden">
              <div className="bg-primary h-full w-[84%]"></div>
            </div>
            <div className="flex justify-between mt-2 font-mono text-[9px]">
              <span>1.6 TB used</span>
              <span>2.0 TB total</span>
            </div>
          </div>
        </div>

        {/* Card 2 */}
        <div className="bg-[#19202e] rounded-xl border border-[#424754] p-card-padding flex flex-col justify-between">
          <div>
            <h3 className="font-semibold text-xs text-white uppercase tracking-wider">Quick Export Bundle</h3>
            <p className="text-text-muted text-xs mt-1">Compress and package filtered records for offline download.</p>
          </div>
          <button className="w-full mt-4 py-2 bg-[#03b5d3] text-black text-xs font-semibold rounded-lg flex items-center justify-center gap-2 hover:opacity-90 transition-all">
            <span className="material-symbols-outlined text-sm font-bold">archive</span>
            Export Filtered Bundle ({filtered.length})
          </button>
        </div>

        {/* Card 3 */}
        <div className="bg-[#19202e] rounded-xl border border-[#424754] p-card-padding relative overflow-hidden group">
          <div className="relative z-10">
            <h3 className="font-semibold text-xs text-white uppercase tracking-wider mb-1">Compute Efficiency</h3>
            <p className="text-success text-lg font-bold">12% Improvement</p>
            <p className="text-text-muted text-[10px] mt-1">Average report generation duration has decreased since recent runtime upgrades.</p>
          </div>
          <div className="absolute -right-4 -bottom-4 opacity-10 group-hover:scale-110 transition-transform duration-700">
            <span className="material-symbols-outlined text-[100px] text-primary">monitoring</span>
          </div>
        </div>
      </div>

      {/* Floating Download Toast */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 transition-all duration-300">
          <div className="bg-[#172033] border border-primary text-primary px-4 py-3 rounded-lg shadow-2xl flex items-center gap-3 font-mono text-xs">
            <span className="material-symbols-outlined text-base">download_done</span>
            <span>{toastMessage}</span>
          </div>
        </div>
      )}
    </div>
  );
}
