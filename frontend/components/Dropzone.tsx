import React, { DragEvent, useRef, useState } from 'react';
import { useUpload } from '../hooks/useUpload';

interface DropzoneProps {
  onJobCreated: (jobId: string) => void;
  onJobCancelled: () => void;
  isRunning: boolean;
}

export const Dropzone: React.FC<DropzoneProps> = ({ onJobCreated, onJobCancelled, isRunning }) => {
  const { file, uploading, uploadProgress, error, uploadedJob, handleFileChange, upload, reset } = useUpload();
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const getWorkflowBadge = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    if (ext === 'fasta' || ext === 'fa' || ext === 'fna') {
      return { label: 'FASTA Genome Assembly', color: 'bg-[#06B6D4] text-black' };
    }
    if (ext === 'fastq' || ext === 'fq') {
      return { label: 'FASTQ Read Quality & Assembly', color: 'bg-purple-600 text-white' };
    }
    if (ext === 'csv' || ext === 'tsv' || ext === 'txt') {
      return { label: 'DEG Transcriptomics Table', color: 'bg-[#22C55E] text-black' };
    }
    return { label: 'Unknown Workflow Type', color: 'bg-yellow-600 text-white' };
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const selectFileClick = () => {
    fileInputRef.current?.click();
  };

  const triggerUploadAndStart = async () => {
    await upload();
  };

  const lastProcessedJobIdRef = useRef<string | null>(null);

  // Trigger callback when job metadata is populated from backend
  React.useEffect(() => {
    if (uploadedJob && uploadedJob.id !== lastProcessedJobIdRef.current) {
      lastProcessedJobIdRef.current = uploadedJob.id;
      onJobCreated(uploadedJob.id);
    }
  }, [uploadedJob, onJobCreated]);

  return (
    <div className="bg-[#1F2937] p-6 rounded-lg border border-[#1F2937] text-[#F9FAFB] flex flex-col gap-4">
      <h3 className="text-lg font-bold border-b border-[#111827] pb-2 text-[#60A5FA]">Upload Analysis Target</h3>
      
      {!file ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={selectFileClick}
          className={`h-48 border-2 border-dashed rounded-lg flex flex-col items-center justify-center cursor-pointer p-4 transition-colors ${
            isDragOver ? 'border-[#60A5FA] bg-[#172033]' : 'border-gray-600 hover:border-gray-500'
          }`}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={(e) => e.target.files && handleFileChange(e.target.files[0])}
            className="hidden"
            accept=".fasta,.fa,.fna,.fastq,.fq,.csv,.tsv,.gz"
          />
          <svg className="h-12 w-12 text-[#9CA3AF] mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <p className="text-sm font-semibold text-center">Drag & Drop file here</p>
          <p className="text-xs text-[#9CA3AF] mt-1 text-center">Accepts: FASTA, FASTQ, CSV/TSV (or .gz)</p>
        </div>
      ) : (
        <div className="bg-[#0B1220] p-4 rounded-lg flex flex-col gap-2 relative">
          <button
            onClick={reset}
            className="absolute top-2 right-2 text-[#9CA3AF] hover:text-[#EF4444]"
            title="Clear upload"
          >
            ✕
          </button>
          <p className="text-sm font-mono truncate pr-6">{file.name}</p>
          <p className="text-xs text-[#9CA3AF]">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
          
          <div className="mt-2">
            <span className={`text-[10px] uppercase font-bold px-2 py-1 rounded font-mono ${getWorkflowBadge(file.name).color}`}>
              {getWorkflowBadge(file.name).label}
            </span>
          </div>
        </div>
      )}

      {uploading && (
        <div className="w-full bg-[#111827] rounded-full h-2">
          <div className="bg-[#3B82F6] h-2 rounded-full transition-all duration-300" style={{ width: `${uploadProgress}%` }} />
        </div>
      )}

      {error && <p className="text-xs text-[#EF4444] bg-[#EF4444]/10 p-2 rounded">{error}</p>}

      <div className="flex gap-2 mt-2">
        <button
          onClick={triggerUploadAndStart}
          disabled={!file || uploading || isRunning}
          className="flex-1 bg-[#3B82F6] hover:bg-blue-600 disabled:bg-gray-700 disabled:text-gray-400 text-white font-semibold py-2 px-4 rounded transition-colors"
        >
          {uploading ? 'Uploading...' : 'Run Pipeline'}
        </button>
        {isRunning && (
          <button
            onClick={onJobCancelled}
            className="bg-[#EF4444] hover:bg-red-600 text-white font-semibold py-2 px-4 rounded transition-colors"
          >
            Cancel
          </button>
        )}
      </div>
    </div>
  );
};
