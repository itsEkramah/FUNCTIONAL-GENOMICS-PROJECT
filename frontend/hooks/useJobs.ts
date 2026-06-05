import { useState, useEffect, useRef, useCallback } from 'react';
import { Job, PipelineResults } from '../types';
import { api } from '../services/api';

export const useJobs = (jobId: string | null) => {
  const [job, setJob] = useState<Job | null>(null);
  const [results, setResults] = useState<PipelineResults | null>(null);
  const [logs, setLogs] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const eventSourceRef = useRef<EventSource | null>(null);
  const pollingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  const clearLogs = useCallback(() => setLogs([]), []);

  const fetchResults = useCallback(async (id: string) => {
    setLoading(true);
    try {
      const res = await api.getJobResults(id);
      setResults(res);
    } catch (err: any) {
      setError('Failed to fetch job analysis results.');
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchStatusOnce = useCallback(async (id: string) => {
    try {
      const currentJob = await api.getJobStatus(id);
      setJob(currentJob);
      if (currentJob.status === 'COMPLETED') {
        fetchResults(id);
      }
    } catch (err) {
      console.error(err);
    }
  }, [fetchResults]);

  useEffect(() => {
    if (!jobId) {
      setJob(null);
      setResults(null);
      setLogs([]);
      return;
    }

    setLoading(true);
    fetchStatusOnce(jobId);

    // Set up EventSource SSE for log and step status streams
    const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
    const sseUrl = `${API_BASE}/jobs/${jobId}/stream`;
    const es = new EventSource(sseUrl);
    eventSourceRef.current = es;

    es.onmessage = (event) => {
      const dataStr = event.data;
      if (dataStr.startsWith('[INFO]') || dataStr.startsWith('[WARN]') || dataStr.startsWith('[ERROR]')) {
        setLogs((prev) => [...prev, dataStr]);
      }
    };

    es.addEventListener('progress', (e: any) => {
      const data = JSON.parse(e.data);
      setJob((prev) => prev ? { ...prev, progress_percent: data.percent } : null);
    });

    es.addEventListener('step_change', (e: any) => {
      fetchStatusOnce(jobId);
    });

    es.addEventListener('job_status', (e: any) => {
      const data = JSON.parse(e.data);
      setJob((prev) => prev ? { ...prev, status: data.status } : null);
      if (data.status === 'COMPLETED') {
        es.close();
        fetchResults(jobId);
      } else if (data.status === 'FAILED' || data.status === 'CANCELLED') {
        es.close();
      }
    });

    es.onerror = () => {
      // If SSE errors out, close EventSource and start Polling Fallback
      es.close();
      console.warn('EventSource SSE connection closed or failed. Switching to polling fallback.');
      
      if (!pollingIntervalRef.current) {
        pollingIntervalRef.current = setInterval(() => {
          fetchStatusOnce(jobId);
        }, 3000);
      }
    };

    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
      if (pollingIntervalRef.current) {
        clearInterval(pollingIntervalRef.current);
        pollingIntervalRef.current = null;
      }
    };
  }, [jobId, fetchResults, fetchStatusOnce]);

  return { job, results, logs, loading, error, clearLogs };
};
