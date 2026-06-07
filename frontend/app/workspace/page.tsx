'use client';

import React, { useState, useEffect, Suspense, useCallback } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Dropzone } from '../../components/Dropzone';
import { PipelineSteps } from '../../components/PipelineSteps';
import { Terminal } from '../../components/Terminal';
import { useJobs } from '../../hooks/useJobs';
import { api } from '../../services/api';

function WorkspaceContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [jobId, setJobId] = useState<string | null>(null);

  useEffect(() => {
    const id = searchParams.get('jobId');
    if (id) {
      setJobId(id);
    }
  }, [searchParams]);

  const { job, results, logs, loading, error, clearLogs } = useJobs(jobId);

  const handleJobCreated = useCallback(async (id: string) => {
    clearLogs();
    setJobId(id);
    router.replace(`/workspace?jobId=${id}`);
    
    // Automatically trigger run after upload routing completes
    try {
      await api.startJob(id);
    } catch (err) {
      console.error(err);
    }
  }, [router, clearLogs]);

  const handleJobCancelled = useCallback(async () => {
    if (!jobId) return;
    try {
      await api.cancelJob(jobId);
    } catch (err) {
      console.error(err);
    }
  }, [jobId]);

  const isRunning = job ? job.status === 'RUNNING' : false;
  const hasNavigatedRef = React.useRef(false);

  // Auto-navigate to full-page results when pipeline completes
  useEffect(() => {
    if (job?.status === 'COMPLETED' && jobId && results && !hasNavigatedRef.current) {
      hasNavigatedRef.current = true;
      // Small delay to let the user see the "Completed" badge before navigating
      const timer = setTimeout(() => {
        router.push(`/workspace/results?jobId=${jobId}`);
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, [job?.status, jobId, results, router]);

  return (
    <div className="flex-1 w-full h-[calc(100vh-64px)] grid grid-cols-12 overflow-hidden bg-[#0c1321] text-[#dce2f6]">
      {/* Left Panel: Upload Center & Parameters (3/12 width) */}
      <section className="col-span-3 bg-[#151b2a] border-r border-[#1F2937] p-4 flex flex-col gap-4 overflow-y-auto custom-scrollbar select-none">
        <Dropzone
          onJobCreated={handleJobCreated}
          onJobCancelled={handleJobCancelled}
          isRunning={isRunning}
        />

        {/* Parameters widget */}
        <div className="bg-[#1F2937] rounded-lg p-5 border border-[#1F2937] flex flex-col gap-3">
          <h4 className="font-semibold text-sm text-[#F9FAFB] flex items-center gap-2 border-b border-[#111827] pb-2">
            <span className="material-symbols-outlined text-primary text-base">tune</span>
            Parameters
          </h4>
          <div className="flex flex-col gap-4 text-xs font-mono">
            <div>
              <label className="block text-[10px] text-text-muted uppercase tracking-wider mb-1">Sequencing Tech</label>
              <select className="w-full bg-[#111827] border border-[#1F2937] text-white rounded p-2 focus:ring-1 focus:ring-primary outline-none">
                <option>Illumina HiSeq</option>
                <option>Oxford Nanopore</option>
                <option>PacBio HiFi</option>
              </select>
            </div>
            <div className="flex items-center justify-between border-t border-[#111827] pt-3">
              <span className="text-[#9CA3AF]">E-value Cutoff</span>
              <span className="text-white font-bold">1e-5</span>
            </div>
            <div className="h-1 bg-gray-700 rounded-full overflow-hidden">
              <div className="h-full bg-primary w-2/3"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Center Panel: Pipeline Runner & Logs (4/12 width) */}
      <section className="col-span-4 bg-[#0c1321] border-r border-[#1F2937] flex flex-col overflow-hidden">
        {/* Pipeline Runner Header */}
        <div className="p-4 border-b border-[#1F2937] flex justify-between items-center bg-[#151b2a] select-none">
          <h2 className="font-semibold text-sm text-white">Live Pipeline Runner</h2>
          {isRunning ? (
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-primary pulse-active"></span>
              <span className="text-[10px] uppercase font-bold text-primary tracking-wider">Processing</span>
            </div>
          ) : job?.status === 'COMPLETED' ? (
            <span className="text-[10px] uppercase font-bold text-[#22C55E] tracking-wider bg-[#22C55E]/10 px-2 py-0.5 rounded border border-[#22C55E]/20">Completed</span>
          ) : job?.status === 'FAILED' ? (
            <span className="text-[10px] uppercase font-bold text-[#EF4444] tracking-wider bg-[#EF4444]/10 px-2 py-0.5 rounded border border-[#EF4444]/20">Failed</span>
          ) : (
            <span className="text-[10px] uppercase font-bold text-[#9CA3AF] tracking-wider">Idle</span>
          )}
        </div>

        {/* Vertical Stepper checklist */}
        <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
          {jobId && job ? (
            <PipelineSteps steps={job.steps || []} progress={job.progress_percent} />
          ) : (
            <p className="text-xs text-gray-500 italic select-none text-center mt-12">No active analysis. Drop a file to start.</p>
          )}
        </div>

        {/* Live logs terminal console */}
        <div className="h-1/3 border-t border-[#1F2937] flex flex-col overflow-hidden">
          <Terminal logs={logs} />
        </div>
      </section>

      {/* Right Panel: Results Preview (5/12 width) */}
      <section className="col-span-5 bg-[#151b2a] flex flex-col overflow-hidden">
        {job?.status === 'COMPLETED' && results ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center p-8 gap-6 select-none">
            {/* Success Animation */}
            <div className="relative">
              <div className="w-20 h-20 rounded-full bg-[#22C55E]/10 border-2 border-[#22C55E]/30 flex items-center justify-center">
                <span className="material-symbols-outlined text-4xl text-[#22C55E]">check_circle</span>
              </div>
              <div className="absolute inset-0 w-20 h-20 rounded-full border-2 border-[#22C55E]/20 animate-ping" />
            </div>

            <div>
              <p className="font-bold text-xl text-white mb-2">Analysis Complete</p>
              <p className="text-sm text-gray-400 max-w-sm">
                Your pipeline has finished processing. The full Scientific Analysis Workspace is ready.
              </p>
            </div>

            {/* Summary Quick Stats */}
            <div className="grid grid-cols-2 gap-3 w-full max-w-xs">
              <div className="bg-[#0B1220] rounded-lg p-3 border border-[#1F2937]">
                <p className="text-[10px] text-gray-500 font-mono uppercase">Workflow</p>
                <p className="text-sm font-bold text-[#60A5FA]">{results.workflow_type}</p>
              </div>
              <div className="bg-[#0B1220] rounded-lg p-3 border border-[#1F2937]">
                <p className="text-[10px] text-gray-500 font-mono uppercase">Status</p>
                <p className="text-sm font-bold text-[#22C55E]">Completed</p>
              </div>
              {results.annotations && (
                <div className="bg-[#0B1220] rounded-lg p-3 border border-[#1F2937]">
                  <p className="text-[10px] text-gray-500 font-mono uppercase">Annotations</p>
                  <p className="text-sm font-bold text-white">{results.annotations.length}</p>
                </div>
              )}
              {results.kegg_results && (
                <div className="bg-[#0B1220] rounded-lg p-3 border border-[#1F2937]">
                  <p className="text-[10px] text-gray-500 font-mono uppercase">Pathways</p>
                  <p className="text-sm font-bold text-white">{results.kegg_results.length}</p>
                </div>
              )}
            </div>

            {/* Primary CTA */}
            <button
              onClick={() => router.push(`/workspace/results?jobId=${jobId}`)}
              className="bg-[#3B82F6] hover:bg-blue-600 text-white font-semibold px-8 py-3.5 rounded-lg transition-all flex items-center gap-3 shadow-lg shadow-[#3B82F6]/20 hover:shadow-[#3B82F6]/40 mt-2"
            >
              <span className="material-symbols-outlined text-lg">open_in_new</span>
              Open Full Results Workspace
            </button>

            <p className="text-[10px] text-gray-600 font-mono mt-1">
              Redirecting automatically...
            </p>
          </div>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center text-center p-8 gap-3 select-none">
            <span className="material-symbols-outlined text-4xl text-gray-600">biotech</span>
            <div>
              <p className="font-semibold text-[#F9FAFB] text-sm">Results Viewer</p>
              <p className="text-xs text-gray-500 max-w-xs mt-1">
                When the pipeline completes, results will open in a full-page Scientific Analysis Workspace with all tabs.
              </p>
            </div>
            {isRunning && (
              <div className="flex items-center gap-2 mt-4">
                <span className="material-symbols-outlined text-lg text-[#3B82F6] animate-spin">sync</span>
                <span className="text-xs text-gray-400">Pipeline executing... {job?.progress_percent || 0}%</span>
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  );
}

export default function WorkspacePage() {
  return (
    <Suspense fallback={
      <div className="flex-grow flex items-center justify-center bg-[#0c1321] text-[#dce2f6]">
        <div className="flex flex-col items-center gap-2">
          <span className="material-symbols-outlined text-4xl text-primary animate-spin">sync</span>
          <span className="text-sm font-semibold">Loading Workspace...</span>
        </div>
      </div>
    }>
      <WorkspaceContent />
    </Suspense>
  );
}
