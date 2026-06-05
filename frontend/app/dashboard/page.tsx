'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { api } from '../../services/api';
import { Job } from '../../types';

export default function DashboardPage() {
  const [history, setHistory] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [computeLoad, setComputeLoad] = useState(78);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const jobs = await api.getAllJobs();
        const sorted = jobs.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        setHistory(sorted);
      } catch (err) {
        console.error('Failed to load job history.');
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();

    // Simulate compute load fluctuations
    const timer = setInterval(() => {
      setComputeLoad(Math.floor(Math.random() * (85 - 70) + 70));
    }, 4000);

    return () => clearInterval(timer);
  }, []);

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return 'bg-[#22C55E]/10 border border-[#22C55E]/20 text-[#22C55E]';
      case 'FAILED':
        return 'bg-[#EF4444]/10 border border-[#EF4444]/20 text-[#EF4444]';
      case 'RUNNING':
        return 'bg-[#3B82F6]/10 border border-[#3B82F6]/20 text-[#3B82F6]';
      default:
        return 'bg-gray-700/50 border border-gray-600 text-gray-400';
    }
  };

  return (
    <div className="p-inner-padding max-w-container-max mx-auto space-y-gutter bg-[#0c1321] text-[#dce2f6]">
      {/* Page Header */}
      <div className="flex justify-between items-end select-none">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Researcher Dashboard</h1>
          <p className="text-xs text-text-muted mt-1">Real-time surveillance of genomic pipeline execution and infrastructure health.</p>
        </div>
        <div className="text-right">
          <p className="text-[10px] font-mono text-text-muted uppercase">LAST SYNC</p>
          <p className="font-mono text-xs text-tertiary">
            {new Date().toISOString().replace('T', ' ').slice(0, 19)} UTC
          </p>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-panel-gap select-none">
        {/* Card 1 */}
        <div className="bg-[#1F2937] border border-[#424754] p-card-padding rounded-lg">
          <div className="flex justify-between items-start">
            <span className="text-[#9CA3AF] text-xs font-semibold">Total Analyses</span>
            <span className="material-symbols-outlined text-[#adc6ff] text-base">analytics</span>
          </div>
          <p className="text-3xl font-bold text-white mt-2 font-mono">{history.length}</p>
          <div className="flex items-center gap-1 mt-2">
            <span className="material-symbols-outlined text-[#10B981] text-xs">trending_up</span>
            <span className="text-[#10B981] text-[10px] font-bold">+12.5% this month</span>
          </div>
        </div>

        {/* Card 2 */}
        <div className="bg-[#1F2937] border border-[#424754] p-card-padding rounded-lg relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1 h-full bg-[#4cd7f6]"></div>
          <div className="flex justify-between items-start">
            <span className="text-[#9CA3AF] text-xs font-semibold">Running Jobs</span>
            <span className="material-symbols-outlined text-[#4cd7f6] animate-spin text-base">sync</span>
          </div>
          <p className="text-3xl font-bold text-white mt-2 font-mono">
            {history.filter((j) => j.status === 'RUNNING').length}
          </p>
          <p className="text-[#9CA3AF] text-[10px] font-semibold mt-2">Active processing buffer</p>
        </div>

        {/* Card 3 */}
        <div className="bg-[#1F2937] border border-[#424754] p-card-padding rounded-lg">
          <div className="flex justify-between items-start">
            <span className="text-[#9CA3AF] text-xs font-semibold">Completed Jobs</span>
            <span className="material-symbols-outlined text-[#10B981] text-base">check_circle</span>
          </div>
          <p className="text-3xl font-bold text-white mt-2 font-mono">
            {history.filter((j) => j.status === 'COMPLETED').length}
          </p>
          <p className="text-[#9CA3AF] text-[10px] font-semibold mt-2">98.2% success checkpoints</p>
        </div>

        {/* Card 4 */}
        <div className="bg-[#1F2937] border border-[#424754] p-card-padding rounded-lg">
          <div className="flex justify-between items-start">
            <span className="text-[#9CA3AF] text-xs font-semibold">Failed Jobs</span>
            <span className="material-symbols-outlined text-[#EF4444] text-base">error</span>
          </div>
          <p className="text-3xl font-bold text-white mt-2 font-mono">
            {history.filter((j) => j.status === 'FAILED').length}
          </p>
          <div className="flex items-center gap-1 mt-2">
            <span className="material-symbols-outlined text-[#EF4444] text-xs">warning</span>
            <span className="text-[#EF4444] text-[10px] font-semibold">Check logs for details</span>
          </div>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
        {/* Recent Analysis Table */}
        <div className="lg:col-span-8 bg-[#1F2937] border border-[#424754] rounded-lg overflow-hidden flex flex-col">
          <div className="p-card-padding border-b border-[#111827] flex justify-between items-center select-none">
            <h2 className="text-xs font-bold text-white uppercase tracking-wider">Recent Analysis Execution Logs</h2>
            <Link href="/reports" className="text-[#adc6ff] text-xs hover:underline">View All Reports</Link>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead className="bg-[#151b2a] text-[#9CA3AF] text-xs font-mono">
                <tr>
                  <th className="px-6 py-3 font-semibold border-b border-[#424754]">Job Name</th>
                  <th className="px-6 py-3 font-semibold border-b border-[#424754]">Workflow Type</th>
                  <th className="px-6 py-3 font-semibold border-b border-[#424754]">Status</th>
                  <th className="px-6 py-3 font-semibold border-b border-[#424754]">Progress</th>
                  <th className="px-6 py-3 font-semibold border-b border-[#424754]">Action</th>
                </tr>
              </thead>
              <tbody className="text-xs divide-y divide-[#424754] font-mono">
                {loading ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-8 text-center text-[#9CA3AF] italic">Querying execution logs index...</td>
                  </tr>
                ) : history.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-8 text-center text-[#9CA3AF] italic">No historical runs recorded. Process a file in the workspace to start.</td>
                  </tr>
                ) : (
                  history.slice(0, 5).map((job) => (
                    <tr key={job.id} className="hover:bg-[#2e3544] transition-colors">
                      <td className="px-6 py-4 text-white truncate max-w-[150px]">{job.job_name}</td>
                      <td className="px-6 py-4 text-[#adc6ff]">{job.workflow_type}</td>
                      <td className="px-6 py-4">
                        <span className={`text-[9px] uppercase font-bold px-2 py-0.5 rounded ${getStatusBadge(job.status)}`}>
                          {job.status}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="w-24 bg-[#111827] h-1.5 rounded-full overflow-hidden inline-block mr-2 align-middle">
                          <div className="bg-[#3B82F6] h-full" style={{ width: `${job.progress_percent}%` }}></div>
                        </div>
                        <span className="text-gray-400">{job.progress_percent}%</span>
                      </td>
                      <td className="px-6 py-4">
                        <Link href={`/workspace?jobId=${job.id}`} className="text-primary hover:text-white transition-colors flex items-center gap-1">
                          <span className="material-symbols-outlined text-sm">search</span> Inspect
                        </Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Workflow usage trends chart */}
        <div className="lg:col-span-4 bg-[#1F2937] border border-[#424754] p-card-padding rounded-lg flex flex-col select-none">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xs font-bold text-white uppercase tracking-wider">Workflow Usage Trends</h2>
            <span className="text-[10px] text-gray-500 font-mono bg-[#111827] px-2 py-0.5 rounded">Last 7 Days</span>
          </div>

          <div className="flex-1 flex flex-col justify-end gap-6 min-h-[180px]">
            {/* Bars charts */}
            <div className="flex items-end justify-between h-36 px-2 gap-4 border-b border-[#424754] pb-2">
              <div className="flex flex-col items-center flex-1 group">
                <div className="w-full bg-[#adc6ff]/40 rounded-t-sm relative transition-all group-hover:bg-[#adc6ff]/60" style={{ height: '70%' }}>
                  <div className="absolute -top-5 left-1/2 -translate-x-1/2 text-[9px] font-mono text-white">42%</div>
                </div>
                <span className="text-[9px] text-[#9CA3AF] mt-2 font-mono">FASTA</span>
              </div>
              <div className="flex flex-col items-center flex-1 group">
                <div className="w-full bg-[#4cd7f6]/40 rounded-t-sm relative transition-all group-hover:bg-[#4cd7f6]/60" style={{ height: '85%' }}>
                  <div className="absolute -top-5 left-1/2 -translate-x-1/2 text-[9px] font-mono text-white">38%</div>
                </div>
                <span className="text-[9px] text-[#9CA3AF] mt-2 font-mono">FASTQ</span>
              </div>
              <div className="flex flex-col items-center flex-1 group">
                <div className="w-full bg-[#4edea3]/40 rounded-t-sm relative transition-all group-hover:bg-[#4edea3]/60" style={{ height: '40%' }}>
                  <div className="absolute -top-5 left-1/2 -translate-x-1/2 text-[9px] font-mono text-white">20%</div>
                </div>
                <span className="text-[9px] text-[#9CA3AF] mt-2 font-mono">DEG</span>
              </div>
            </div>

            <div className="flex flex-col gap-2 font-mono text-[10px]">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Primary Alignment</span>
                <span className="text-white font-bold">42%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Variant Discovery</span>
                <span className="text-white font-bold">38%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Expression Profile</span>
                <span className="text-white font-bold">20%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* System Infrastructure progress bars */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-panel-gap select-none">
        <div className="bg-[#172033] border border-[#424754] p-4 rounded-lg flex items-center gap-4">
          <div className="w-10 h-10 bg-[#0c1321] rounded flex items-center justify-center text-[#4cd7f6] border border-[#424754]">
            <span className="material-symbols-outlined text-xl">memory</span>
          </div>
          <div className="flex-1">
            <div className="flex justify-between items-center mb-1">
              <span className="text-[10px] font-bold text-white uppercase tracking-wider">Compute Load</span>
              <span className="text-xs font-mono text-[#4cd7f6]">{computeLoad}%</span>
            </div>
            <div className="w-full bg-[#111827] h-1 rounded-full overflow-hidden">
              <div className="bg-[#4cd7f6] h-full transition-all duration-500" style={{ width: `${computeLoad}%` }}></div>
            </div>
          </div>
        </div>

        <div className="bg-[#172033] border border-[#424754] p-4 rounded-lg flex items-center gap-4">
          <div className="w-10 h-10 bg-[#0c1321] rounded flex items-center justify-center text-primary border border-[#424754]">
            <span className="material-symbols-outlined text-xl">storage</span>
          </div>
          <div className="flex-1">
            <div className="flex justify-between items-center mb-1">
              <span className="text-[10px] font-bold text-white uppercase tracking-wider">Storage (PETA)</span>
              <span className="text-xs font-mono text-primary">62%</span>
            </div>
            <div className="w-full bg-[#111827] h-1 rounded-full overflow-hidden">
              <div className="bg-primary h-full" style={{ width: '62%' }}></div>
            </div>
          </div>
        </div>

        <div className="bg-[#172033] border border-[#424754] p-4 rounded-lg flex items-center gap-4">
          <div className="w-10 h-10 bg-[#0c1321] rounded flex items-center justify-center text-tertiary border border-[#424754]">
            <span className="material-symbols-outlined text-xl">public</span>
          </div>
          <div className="flex-1">
            <div className="flex justify-between items-center mb-1">
              <span className="text-[10px] font-bold text-white uppercase tracking-wider">Network IO</span>
              <span className="text-xs font-mono text-tertiary">1.2 GB/s</span>
            </div>
            <div className="w-full bg-[#111827] h-1 rounded-full overflow-hidden">
              <div className="bg-tertiary h-full" style={{ width: '45%' }}></div>
            </div>
          </div>
        </div>
      </div>

      {/* Floating CLI Terminal Quick action */}
      <div className="fixed bottom-8 right-8 z-50">
        <Link href="/workspace">
          <button className="w-14 h-14 bg-primary text-on-primary rounded-full shadow-lg flex items-center justify-center transition-transform hover:scale-110 active:scale-95 group relative border border-primary/20">
            <span className="material-symbols-outlined text-[28px]">terminal</span>
            <div className="absolute right-full mr-4 bg-[#1F2937] border border-[#424754] px-3 py-1.5 rounded whitespace-nowrap text-xs text-white opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity font-mono">
              Open Workspace Console
            </div>
          </button>
        </Link>
      </div>
    </div>
  );
}
