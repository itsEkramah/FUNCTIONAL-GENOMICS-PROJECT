'use client';

import React, { useState, useEffect, Suspense, useCallback } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { ResultsViewer } from '../../../components/ResultsViewer';
import { useJobs } from '../../../hooks/useJobs';

function ResultsContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const jobId = searchParams.get('jobId');
  const { job, results, loading, error } = useJobs(jobId);

  if (!jobId) {
    return (
      <div className="min-h-screen bg-[#0c1321] flex items-center justify-center">
        <div className="text-center flex flex-col items-center gap-4">
          <span className="material-symbols-outlined text-5xl text-gray-600">search_off</span>
          <h2 className="text-xl font-bold text-white">No Job Selected</h2>
          <p className="text-sm text-gray-400 max-w-md">
            No analysis job ID was specified. Return to the workspace to upload a dataset and run a pipeline.
          </p>
          <button
            onClick={() => router.push('/workspace')}
            className="mt-4 bg-[#3B82F6] hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-lg transition-colors flex items-center gap-2"
          >
            <span className="material-symbols-outlined text-lg">arrow_back</span>
            Back to Workspace
          </button>
        </div>
      </div>
    );
  }

  if (loading && !results) {
    return (
      <div className="min-h-screen bg-[#0c1321] flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <span className="material-symbols-outlined text-4xl text-[#3B82F6] animate-spin">sync</span>
          <span className="text-sm font-semibold text-white">Loading Analysis Results...</span>
          <span className="text-xs text-gray-500 font-mono">{jobId}</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#0c1321] flex items-center justify-center">
        <div className="text-center flex flex-col items-center gap-4">
          <span className="material-symbols-outlined text-5xl text-[#EF4444]">error</span>
          <h2 className="text-xl font-bold text-white">Failed to Load Results</h2>
          <p className="text-sm text-gray-400">{error}</p>
          <button
            onClick={() => router.push('/workspace')}
            className="mt-4 bg-[#1F2937] hover:bg-[#374151] text-white font-semibold px-6 py-3 rounded-lg transition-colors border border-[#374151]"
          >
            Return to Workspace
          </button>
        </div>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="min-h-screen bg-[#0c1321] flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <span className="material-symbols-outlined text-4xl text-[#3B82F6] animate-spin">sync</span>
          <span className="text-sm font-semibold text-white">Waiting for results...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0c1321] text-[#dce2f6]">
      {/* Top Navigation Bar */}
      <div className="sticky top-0 z-50 bg-[#151b2a]/95 backdrop-blur-md border-b border-[#1F2937]">
        <div className="max-w-[1800px] mx-auto px-6 py-3 flex items-center justify-between">
          {/* Left: Back + Title */}
          <div className="flex items-center gap-4">
            <button
              onClick={() => router.push(`/workspace?jobId=${jobId}`)}
              className="flex items-center gap-1.5 text-gray-400 hover:text-white transition-colors text-xs font-mono"
            >
              <span className="material-symbols-outlined text-base">arrow_back</span>
              Pipeline
            </button>
            <div className="w-px h-5 bg-[#1F2937]" />
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[#3B82F6] text-lg">biotech</span>
              <h1 className="text-sm font-bold text-white">Scientific Analysis Workspace</h1>
            </div>
          </div>

          {/* Right: Status + Job ID */}
          <div className="flex items-center gap-4">
            <span className="text-[10px] font-mono text-gray-500 hidden md:block">
              JOB: {jobId?.substring(0, 8)}...
            </span>
            {job?.status === 'COMPLETED' && (
              <span className="text-[10px] uppercase font-bold text-[#22C55E] tracking-wider bg-[#22C55E]/10 px-2.5 py-1 rounded border border-[#22C55E]/20 flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#22C55E]" />
                Analysis Complete
              </span>
            )}
            <span className="text-[10px] uppercase font-mono px-2.5 py-1 rounded bg-[#0B1220] border border-[#1F2937] text-[#60A5FA]">
              {results.workflow_type}
            </span>
          </div>
        </div>
      </div>

      {/* Full-Width Results Content */}
      <div className="max-w-[1800px] mx-auto px-6 py-6">
        <ResultsViewer results={results} />
      </div>
    </div>
  );
}

export default function ResultsPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-[#0c1321] flex items-center justify-center text-[#dce2f6]">
        <div className="flex flex-col items-center gap-2">
          <span className="material-symbols-outlined text-4xl text-[#3B82F6] animate-spin">sync</span>
          <span className="text-sm font-semibold">Loading Results...</span>
        </div>
      </div>
    }>
      <ResultsContent />
    </Suspense>
  );
}
