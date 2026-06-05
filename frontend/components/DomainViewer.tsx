import React, { useState } from 'react';
import { PfamDomain } from '../types';

interface DomainViewerProps {
  domains: PfamDomain[];
}

export const DomainViewer: React.FC<DomainViewerProps> = ({ domains }) => {
  // Filter unique query protein IDs
  const proteinIds = Array.from(new Set(domains.map((d) => d.protein_id)));
  
  // Set default selected protein safely
  const [selectedProtein, setSelectedProtein] = useState<string>(proteinIds[0] || 'seq_1');

  const currentDomains = domains.filter((d) => d.protein_id === selectedProtein);

  // Simulated backbone length
  const proteinLength = 650;

  const colors = ['bg-[#3B82F6]', 'bg-[#22C55E]', 'bg-[#06B6D4]', 'bg-purple-600', 'bg-pink-600'];

  return (
    <div className="bg-[#0B1220] p-6 rounded-lg border border-[#1F2937] text-white flex flex-col gap-6">
      <div className="flex items-center justify-between border-b border-[#1F2937] pb-3">
        <h4 className="text-sm font-bold text-[#60A5FA] font-mono">Pfam Domain Architecture Viewer</h4>
        <select
          value={selectedProtein}
          onChange={(e) => setSelectedProtein(e.target.value)}
          className="bg-[#111827] border border-[#1F2937] rounded px-3 py-1 text-xs font-mono text-[#F9FAFB] outline-none"
        >
          {proteinIds.map((pid) => (
            <option key={pid} value={pid}>
              {pid}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-6 mt-2 relative">
        <p className="text-xs text-[#9CA3AF] font-mono">Protein Length backbone: {proteinLength} aa</p>
        
        {/* Visual Line */}
        <div className="relative h-4 bg-gray-700 rounded-full w-full flex items-center shadow-inner">
          {currentDomains.map((dom, index) => {
            const leftOffset = (dom.domain_start / proteinLength) * 100;
            const widthOffset = ((dom.domain_end - dom.domain_start) / proteinLength) * 100;
            const color = colors[index % colors.length];

            return (
              <div
                key={dom.pfam_accession}
                className={`absolute h-6 rounded border border-[#0B1220] flex items-center justify-center text-[8px] font-bold font-mono text-white cursor-pointer ${color} group`}
                style={{ left: `${leftOffset}%`, width: `${widthOffset}%` }}
                title={`${dom.pfam_name} (${dom.domain_start}-${dom.domain_end})`}
              >
                <span className="truncate px-1">{dom.pfam_name}</span>
                
                {/* Domain Hover Detail box */}
                <div className="absolute top-8 left-0 scale-0 group-hover:scale-100 bg-[#1F2937] border border-[#3B82F6] p-3 rounded shadow-lg text-[10px] w-48 flex flex-col gap-1 z-50 transition-all font-mono pointer-events-none">
                  <p className="text-[#60A5FA] font-bold">{dom.pfam_name}</p>
                  <p>Accession: {dom.pfam_accession}</p>
                  <p>Coords: {dom.domain_start} - {dom.domain_end} aa</p>
                  <p>E-value: {dom.evalue.toExponential(2)}</p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Labels under backbone */}
        <div className="flex justify-between text-[10px] text-gray-500 font-mono select-none px-1">
          <span>0 aa</span>
          <span>{proteinLength} aa</span>
        </div>
      </div>
    </div>
  );
};
