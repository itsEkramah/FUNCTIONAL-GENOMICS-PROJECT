import React, { useState } from 'react';
import { AIInterpretation, PubMedArticle } from '../types';

interface AIReportProps {
  ai: AIInterpretation;
  pubmed: PubMedArticle[];
}

export const AIReport: React.FC<AIReportProps> = ({ ai, pubmed }) => {
  const [selectedArticle, setSelectedArticle] = useState<PubMedArticle | null>(null);
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
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 text-white">
      {/* Grounded report sections */}
      <div className="flex flex-col gap-4">
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

        <div className="flex flex-col gap-3">
          <details open className="bg-[#0B1220] border border-[#1F2937] rounded-lg p-4 group">
            <summary className="font-bold text-sm cursor-pointer list-none flex justify-between items-center select-none text-[#60A5FA]">
              <span>Computational Findings</span>
              <span className="transition-transform group-open:rotate-180">▼</span>
            </summary>
            <p className="mt-3 text-xs leading-relaxed text-gray-300 whitespace-pre-wrap">{ai.findings}</p>
          </details>

          <details open className="bg-[#0B1220] border border-[#1F2937] rounded-lg p-4 group">
            <summary className="font-bold text-sm cursor-pointer list-none flex justify-between items-center select-none text-[#60A5FA]">
              <span>Supporting Literature Reference</span>
              <span className="transition-transform group-open:rotate-180">▼</span>
            </summary>
            <p className="mt-3 text-xs leading-relaxed text-gray-300 whitespace-pre-wrap">{ai.literature_summary}</p>
          </details>

          <details open className="bg-[#0B1220] border border-[#1F2937] rounded-lg p-4 group">
            <summary className="font-bold text-sm cursor-pointer list-none flex justify-between items-center select-none text-[#60A5FA]">
              <span>Biological Interpretation & Pathology</span>
              <span className="transition-transform group-open:rotate-180">▼</span>
            </summary>
            <p className="mt-3 text-xs leading-relaxed text-gray-300 whitespace-pre-wrap">{ai.biological_interpretation}</p>
          </details>

          <details className="bg-[#0B1220] border border-[#1F2937] rounded-lg p-4 group">
            <summary className="font-bold text-sm cursor-pointer list-none flex justify-between items-center select-none text-[#60A5FA]">
              <span>Analysis Limitations</span>
              <span className="transition-transform group-open:rotate-180">▼</span>
            </summary>
            <p className="mt-3 text-xs leading-relaxed text-gray-300 whitespace-pre-wrap">{ai.limitations}</p>
          </details>
        </div>
      </div>

      {/* Publications grid */}
      <div className="flex flex-col gap-4">
        <h4 className="text-sm font-bold text-[#60A5FA] border-b border-[#1F2937] pb-3 mb-1 font-mono">Retrieved PubMed Evidence</h4>
        
        <div className="flex flex-col gap-3 overflow-y-auto max-h-[500px] pr-2">
          {pubmed.map((art) => (
            <div key={art.pmid} className="bg-[#0B1220] border border-[#1F2937] p-4 rounded-lg flex flex-col gap-2">
              <span className="text-[10px] font-mono text-[#06B6D4]">PMID: {art.pmid}</span>
              <h5 className="text-xs font-bold leading-snug">{art.title}</h5>
              <p className="text-[10px] text-gray-400">
                {art.journal} ({art.publication_year}) | {art.authors.map((a) => `${a.forename || ''} ${a.lastname || ''}`).join(', ')}
              </p>
              <div className="flex gap-2 mt-2">
                <button
                  onClick={() => setSelectedArticle(art)}
                  className="bg-[#172033] hover:bg-[#1F2937] border border-[#1F2937] text-white text-[10px] font-semibold py-1 px-3 rounded transition-colors"
                >
                  View Abstract
                </button>
                {art.doi && (
                  <a
                    href={`https://doi.org/${art.doi}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-[#3B82F6]/20 hover:bg-[#3B82F6]/30 text-[#60A5FA] border border-[#3B82F6]/50 text-[10px] font-semibold py-1 px-3 rounded transition-colors flex items-center justify-center"
                  >
                    View Publisher DOI
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Abstract display Modal */}
      {selectedArticle && (
        <div className="fixed inset-0 bg-black/75 flex items-center justify-center z-50 p-4 font-sans">
          <div className="bg-[#1F2937] border border-[#3B82F6] rounded-lg max-w-2xl w-full p-6 relative flex flex-col gap-4 max-h-[85vh]">
            <button
              onClick={() => setSelectedArticle(null)}
              className="absolute top-4 right-4 text-white hover:text-[#EF4444] font-bold"
            >
              ✕
            </button>
            <span className="text-xs font-mono text-[#06B6D4]">PubMed PMID: {selectedArticle.pmid}</span>
            <h4 className="text-sm font-bold leading-normal pr-8">{selectedArticle.title}</h4>
            <div className="overflow-y-auto pr-2 mt-2 text-xs leading-relaxed text-gray-300 whitespace-pre-wrap">
              {selectedArticle.abstract}
            </div>
            {selectedArticle.mesh_terms && (
              <div className="mt-4 border-t border-[#111827] pt-3">
                <span className="text-[10px] uppercase font-mono text-gray-400 block mb-1.5">MeSH Keywords</span>
                <div className="flex flex-wrap gap-1.5">
                  {selectedArticle.mesh_terms.map((tag) => (
                    <span key={tag} className="text-[9px] font-mono px-2 py-0.5 rounded bg-[#0B1220] border border-gray-700">
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
