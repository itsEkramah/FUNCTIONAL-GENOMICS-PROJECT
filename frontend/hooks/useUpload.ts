import { useState, useCallback } from 'react';
import { Job } from '../types';
import { api } from '../services/api';

export const useUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [uploadedJob, setUploadedJob] = useState<Job | null>(null);

  const reset = useCallback(() => {
    setFile(null);
    setUploading(false);
    setUploadProgress(0);
    setError(null);
    setUploadedJob(null);
  }, []);

  const handleFileChange = useCallback((selectedFile: File) => {
    setFile(selectedFile);
    setError(null);
  }, []);

  const upload = useCallback(async () => {
    if (!file) return;
    setUploading(true);
    setUploadProgress(10);
    setError(null);

    try {
      // Simulate simple progressive upload steps for user feedback
      const interval = setInterval(() => {
        setUploadProgress((prev) => (prev < 90 ? prev + 15 : prev));
      }, 200);

      const jobData = await api.uploadFile(file);
      clearInterval(interval);
      setUploadProgress(100);
      setUploadedJob(jobData);
    } catch (err: any) {
      setError(err?.response?.data?.detail || err?.message || 'Failed to upload file.');
    } finally {
      setUploading(false);
    }
  }, [file]);

  return {
    file,
    uploading,
    uploadProgress,
    error,
    uploadedJob,
    handleFileChange,
    upload,
    reset,
  };
};
