import axios from 'axios';
import { Job, PipelineResults } from '../types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

export const api = {
  uploadFile: async (file: File): Promise<Job> => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post<Job>('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  startJob: async (jobId: string): Promise<{ status: string }> => {
    const res = await apiClient.post<{ status: string }>(`/jobs/${jobId}/start`);
    return res.data;
  },

  cancelJob: async (jobId: string): Promise<{ status: string }> => {
    const res = await apiClient.post<{ status: string }>(`/jobs/${jobId}/cancel`);
    return res.data;
  },

  getJobStatus: async (jobId: string): Promise<Job> => {
    const res = await apiClient.get<Job>(`/jobs/${jobId}/status`);
    return res.data;
  },

  getJobResults: async (jobId: string): Promise<PipelineResults> => {
    const res = await apiClient.get<PipelineResults>(`/jobs/${jobId}/results`);
    return res.data;
  },

  getSettings: async (): Promise<{ gemini_connected: boolean; openai_connected: boolean }> => {
    const res = await apiClient.get<{ gemini_connected: boolean; openai_connected: boolean }>('/settings');
    return res.data;
  },

  updateSettings: async (keys: { gemini_key?: string; openai_key?: string }): Promise<void> => {
    await apiClient.post('/settings', keys);
  },

  getAllJobs: async (): Promise<Job[]> => {
    const res = await apiClient.get<Job[]>('/jobs');
    return res.data;
  },

  getThresholds: async (jobId: string): Promise<{ fdr_threshold: number; lfc_threshold: number; min_cpm: number; min_sample_frac: number }> => {
    const res = await apiClient.get(`/jobs/${jobId}/thresholds`);
    return res.data;
  },

  setThresholds: async (jobId: string, thresholds: { fdr_threshold: number; lfc_threshold: number; min_cpm: number; min_sample_frac: number }): Promise<{ status: string; thresholds: object }> => {
    const res = await apiClient.post(`/jobs/${jobId}/thresholds`, thresholds);
    return res.data;
  },

  restartJob: async (jobId: string): Promise<{ status: string; message: string }> => {
    const res = await apiClient.post(`/jobs/${jobId}/restart`);
    return res.data;
  },
};
