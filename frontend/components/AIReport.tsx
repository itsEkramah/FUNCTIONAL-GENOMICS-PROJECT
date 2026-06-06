import React, { useState } from 'react';
import { AIInterpretation } from '../types';

interface AIReportProps {
  ai: AIInterpretation;
}

export const AIReport: React.FC<AIReportProps> = ({ ai }) => {
  const [copied, setCopied] = useState(false);

  const getConfidenceColor = (conf: string) => {
    if (conf === 'HIGH') return 'bg-[#22C55E] text-[#0B1220]';
    if (conf === 'MEDIUM') return 'bg-[#EAB308] text-black';
    return 'bg-[#EF4444] text-white';
  };

  const copyFullReport = () => {
    const markdownReport = `
# PathoScope AI Pathobiology Report
AI Provider: ${ai.ai_provider} (${ai.model_name})
Confidence Assessment: ${ai.confidence_assessment}

## Computational Findings
${ai.findings}

## Supporting Literature
${ai.literature_summary}

## Biological Interpretation & Pathology
${ai.biological_interpretation}

## Analysis Limitations
${ai.limitations}
    `.trim();

    navigator.clipboard.writeText(markdownReport).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="flex flex-col gap-4 text-white w-full">
      <div className="flex items-center justify-between border-b border-[#1F2937] pb-3 mb-1">
        <div className="flex items-center gap-3">
          <h4 className="text-sm font-bold text-[#60A5FA] font-mono">Grounded AI Analysis</h4>
          <span className="text-[10px] font-mono bg-[#111827] px-2 py-0.5 rounded text-[#9CA3AF] border border-[#1F2937]">
            {ai.ai_provider} ({ai.model_name})
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={copyFullReport}
            className="text-[#60A5FA] hover:text-[#3B82F6] text-xs font-semibold px-2 py-1 bg-[#111827] border border-[#1F2937] rounded select-none transition-colors"
          >
            {copied ? '✓ Copied' : 'Copy Report'}
          </button>
          <span className={`text-[10px] uppercase font-bold font-mono px-2 py-1 rounded ${getConfidenceColor(ai.confidence_assessment)}`}>
            Confidence: {ai.confidence_assessment}
          </span>
        </div>
      </div>

      <div className="flex flex-col gap-4 w-full">
        <details open className="bg-[#0B1220] border border-[#1F2937] rounded-lg p-5 group">
          <summary className="font-bold text-sm cursor-pointer list-none flex justify-between items-center select-none text-[#60A5FA]">
            <span>Computational Findings</span>
            <span className="transition-transform group-open:rotate-180">▼</span>
          </summary>
          <p className="mt-3 text-xs leading-relaxed text-gray-300 whitespace-pre-wrap font-sans">{ai.findings}</p>
        </details>

        <details open className="bg-[#0B1220] border border-[#1F2937] rounded-lg p-5 group">
          <summary className="font-bold text-sm cursor-pointer list-none flex justify-between items-center select-none text-[#60A5FA]">
            <span>Supporting Literature Reference</span>
            <span className="transition-transform group-open:rotate-180">▼</span>
          </summary>
          <p className="mt-3 text-xs leading-relaxed text-gray-300 whitespace-pre-wrap font-sans">{ai.literature_summary}</p>
        </details>

        <details open className="bg-[#0B1220] border border-[#1F2937] rounded-lg p-5 group">
          <summary className="font-bold text-sm cursor-pointer list-none flex justify-between items-center select-none text-[#60A5FA]">
            <span>Biological Interpretation & Pathology</span>
            <span className="transition-transform group-open:rotate-180">▼</span>
          </summary>
          <p className="mt-3 text-xs leading-relaxed text-gray-300 whitespace-pre-wrap font-sans">{ai.biological_interpretation}</p>
        </details>

        <details className="bg-[#0B1220] border border-[#1F2937] rounded-lg p-5 group">
          <summary className="font-bold text-sm cursor-pointer list-none flex justify-between items-center select-none text-[#60A5FA]">
            <span>Analysis Limitations</span>
            <span className="transition-transform group-open:rotate-180">▼</span>
          </summary>
          <p className="mt-3 text-xs leading-relaxed text-gray-300 whitespace-pre-wrap font-sans">{ai.limitations}</p>
        </details>
      </div>
    </div>
  );
};
