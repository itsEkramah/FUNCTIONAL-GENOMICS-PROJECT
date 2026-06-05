import React, { useEffect, useRef, useState } from 'react';

interface TerminalProps {
  logs: string[];
}

export const Terminal: React.FC<TerminalProps> = ({ logs }) => {
  const bottomRef = useRef<HTMLDivElement>(null);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const getLineColor = (line: string) => {
    if (line.includes('[ERROR]')) return 'text-[#EF4444]';
    if (line.includes('[WARN]')) return 'text-[#EAB308]';
    if (line.includes('[INFO]')) return 'text-[#06B6D4]';
    return 'text-[#D1D5DB]';
  };

  const copyLogs = () => {
    if (logs.length === 0) return;
    const rawText = logs.join('\n');
    navigator.clipboard.writeText(rawText).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="bg-[#0B1220] rounded-lg border border-[#1F2937] text-white p-4 flex flex-col gap-2 font-mono text-xs shadow-inner">
      <div className="flex items-center justify-between border-b border-[#1F2937] pb-2 mb-2">
        <div className="flex items-center gap-2">
          <span className="h-3 w-3 rounded-full bg-[#EF4444]" />
          <span className="h-3 w-3 rounded-full bg-[#EAB308]" />
          <span className="h-3 w-3 rounded-full bg-[#22C55E]" />
          <span className="text-xs text-[#9CA3AF] pl-2">System Execution Log</span>
        </div>
        <div className="flex items-center gap-3">
          {logs.length > 0 && (
            <button
              onClick={copyLogs}
              className="text-[#60A5FA] hover:text-[#3B82F6] transition-colors flex items-center gap-1 bg-[#172033] px-2 py-0.5 rounded border border-[#1F2937] select-none"
            >
              <span>{copied ? '✓ Copied' : 'Copy'}</span>
            </button>
          )}
          <div className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-[#3B82F6] animate-ping" />
            <span className="text-[10px] text-[#3B82F6] font-semibold uppercase">Real-Time</span>
          </div>
        </div>
      </div>

      <div className="h-[200px] overflow-y-auto flex flex-col gap-1 pr-2 select-text selection:bg-[#3B82F6]/30">
        {logs.length === 0 ? (
          <p className="text-gray-500 italic select-none">Console idle. Logs will stream here during pipeline execution.</p>
        ) : (
          logs.map((log, index) => (
            <div key={index} className={`whitespace-pre-wrap leading-relaxed ${getLineColor(log)}`}>
              {log}
            </div>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};
