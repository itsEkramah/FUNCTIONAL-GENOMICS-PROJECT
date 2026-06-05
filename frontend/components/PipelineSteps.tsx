import React from 'react';
import { JobStep } from '../types';

interface PipelineStepsProps {
  steps: JobStep[];
  progress: number;
}

export const PipelineSteps: React.FC<PipelineStepsProps> = ({ steps, progress }) => {
  const getStepIcon = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return (
          <div className="h-6 w-6 rounded-full bg-[#22C55E] flex items-center justify-center text-[#0B1220] font-bold text-xs">
            ✓
          </div>
        );
      case 'RUNNING':
        return (
          <div className="h-6 w-6 rounded-full bg-[#3B82F6] flex items-center justify-center animate-spin">
            <svg className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
          </div>
        );
      case 'FAILED':
        return (
          <div className="h-6 w-6 rounded-full bg-[#EF4444] flex items-center justify-center text-white font-bold text-xs">
            ✕
          </div>
        );
      default:
        return (
          <div className="h-6 w-6 rounded-full bg-gray-700 flex items-center justify-center text-gray-500 font-bold text-xs">
            ○
          </div>
        );
    }
  };

  const sortedSteps = [...steps].sort((a, b) => a.step_order - b.step_order);

  return (
    <div className="bg-[#1F2937] p-6 rounded-lg border border-[#1F2937] text-[#F9FAFB] flex flex-col gap-4">
      <div className="flex items-center justify-between border-b border-[#111827] pb-2">
        <h3 className="text-lg font-bold text-[#60A5FA]">Live Pipeline Track</h3>
        <span className="text-sm font-mono bg-[#0B1220] px-2 py-1 rounded text-[#22C55E]">
          Progress: {progress}%
        </span>
      </div>

      <div className="w-full bg-[#111827] rounded-full h-2">
        <div
          className="bg-[#3B82F6] h-2 rounded-full transition-all duration-500"
          style={{ width: `${progress}%` }}
        />
      </div>

      <div className="flex flex-col gap-3 mt-2 overflow-y-auto max-h-[300px]">
        {sortedSteps.map((step, idx) => {
          const isRunning = step.status === 'RUNNING';
          const isCompleted = step.status === 'COMPLETED';
          const isFailed = step.status === 'FAILED';
          
          return (
            <div key={step.id} className="flex items-center justify-between relative pl-2">
              {idx < sortedSteps.length - 1 && (
                <div className={`absolute left-5 top-6 bottom-0 w-0.5 ${isCompleted ? 'bg-[#22C55E]' : 'bg-gray-700'}`} style={{ height: '24px' }} />
              )}
              <div className="flex items-center gap-3">
                {getStepIcon(step.status)}
                <span className={`text-sm ${isRunning ? 'text-[#3B82F6] font-bold' : isFailed ? 'text-[#EF4444]' : 'text-[#D1D5DB]'}`}>
                  {step.step_name}
                </span>
              </div>
              <div className="text-xs text-[#9CA3AF] font-mono">
                {step.end_time && step.start_time ? (
                  `${((new Date(step.end_time).getTime() - new Date(step.start_time).getTime()) / 1000).toFixed(1)}s`
                ) : isRunning ? (
                  <span className="text-[#3B82F6] animate-pulse">Running</span>
                ) : (
                  'Pending'
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
