'use client';

import React, { useEffect, useState } from 'react';
import { api } from '../../services/api';

export default function SettingsPage() {
  const [keys, setKeys] = useState({ gemini_key: '', openai_key: '' });
  const [status, setStatus] = useState({ gemini_connected: false, openai_connected: false });
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const res = await api.getSettings();
        setStatus(res);
      } catch (err) {
        console.error(err);
      }
    };
    fetchSettings();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMessage(null);
    try {
      await api.updateSettings(keys);
      setMessage('API Keys saved successfully on the server (.env).');
      // Reload status
      const res = await api.getSettings();
      setStatus(res);
      setKeys({ gemini_key: '', openai_key: '' });
    } catch (err) {
      setMessage('Failed to update API keys.');
    } finally {
      setSaving(false);
    }
  };

  const getStatusBadge = (connected: boolean) => {
    return connected
      ? 'bg-[#22C55E]/10 border border-[#22C55E] text-[#22C55E]'
      : 'bg-[#EF4444]/10 border border-[#EF4444] text-[#EF4444]';
  };

  return (
    <div className="p-inner-padding max-w-container-max mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 text-white bg-[#0c1321]">
      {/* API settings */}
      <div className="md:col-span-2 bg-[#1F2937] p-6 rounded-lg border border-[#1F2937] flex flex-col gap-6">
        <div>
          <h2 className="text-xl font-bold text-[#60A5FA]">AI Provider Configurations</h2>
          <p className="text-xs text-gray-400 mt-1">Keys are stored securely in backend server environmental variables.</p>
        </div>

        <form onSubmit={handleSave} className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-[#9CA3AF] font-mono">Google Gemini API Key</label>
            <input
              type="password"
              placeholder="••••••••••••••••••••••••••••••••••••••••"
              value={keys.gemini_key}
              onChange={(e) => setKeys({ ...keys, gemini_key: e.target.value })}
              className="bg-[#111827] border border-[#1F2937] rounded px-3 py-2 text-sm text-[#F9FAFB] w-full outline-none focus:border-[#3B82F6] font-mono"
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-semibold text-[#9CA3AF] font-mono">OpenAI API Key</label>
            <input
              type="password"
              placeholder="••••••••••••••••••••••••••••••••••••••••"
              value={keys.openai_key}
              onChange={(e) => setKeys({ ...keys, openai_key: e.target.value })}
              className="bg-[#111827] border border-[#1F2937] rounded px-3 py-2 text-sm text-[#F9FAFB] w-full outline-none focus:border-[#3B82F6] font-mono"
            />
          </div>

          {message && (
            <p className={`text-xs p-2 rounded ${message.includes('successfully') ? 'bg-[#22C55E]/10 text-[#22C55E]' : 'bg-[#EF4444]/10 text-[#EF4444]'}`}>
              {message}
            </p>
          )}

          <button
            type="submit"
            disabled={saving}
            className="bg-[#3B82F6] hover:bg-blue-600 disabled:bg-gray-700 text-white font-bold py-2 px-4 rounded w-32 mt-2 transition-colors"
          >
            {saving ? 'Saving...' : 'Save Keys'}
          </button>
        </form>
      </div>

      {/* Provider connection Status info card */}
      <div className="md:col-span-1 bg-[#1F2937] p-6 rounded-lg border border-[#1F2937] flex flex-col gap-6">
        <h3 className="text-lg font-bold text-[#60A5FA] border-b border-[#111827] pb-2">Provider Status</h3>
        
        <div className="flex flex-col gap-4 font-mono text-xs">
          <div className="flex items-center justify-between">
            <span>Gemini API Status:</span>
            <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${getStatusBadge(status.gemini_connected)}`}>
              {status.gemini_connected ? 'CONNECTED' : 'DISCONNECTED'}
            </span>
          </div>

          <div className="flex items-center justify-between">
            <span>OpenAI API Status:</span>
            <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${getStatusBadge(status.openai_connected)}`}>
              {status.openai_connected ? 'CONNECTED' : 'DISCONNECTED'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
