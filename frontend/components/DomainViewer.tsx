import React, { useState } from 'react';
import { PfamDomain, AnnotationResult } from '../types';

interface DomainViewerProps {
  domains: PfamDomain[];
  annotations?: AnnotationResult[];
  orfs?: any[];
}

export const DomainViewer: React.FC<DomainViewerProps> = ({ domains, annotations = [], orfs = [] }) => {
  // Extract unique query protein IDs
  const proteinIds = Array.from(new Set(domains.map((d) => d.protein_id)));
  
  // Set default selected protein
  const [selectedProtein, setSelectedProtein] = useState<string>(proteinIds[0] || 'seq_1');

  // Filter domains for selected protein
  const currentDomains = domains.filter((d) => d.protein_id === selectedProtein);

  // Map annotations: seq_id -> SwissProt description
  const annotationMap = new Map<string, string>();
  annotations.forEach((ann) => {
    const cleanAnnot = ann.annotation && ann.annotation !== 'Unknown' ? ann.annotation : '';
    const name = cleanAnnot 
      ? `${cleanAnnot} (${ann.subject_protein})` 
      : ann.subject_protein;
    annotationMap.set(ann.query_protein, name);
  });

  // Calculate dynamic protein backbone length
  const getProteinLength = (pid: string) => {
    const match = pid.match(/^seq_(\d+)$/);
    if (match && orfs && orfs.length > 0) {
      const idx = parseInt(match[1], 10) - 1;
      const orf = orfs[idx];
      if (orf && orf.length) {
        return Math.floor(orf.length / 3);
      }
    }
    // Fallback: estimate from the max domain end coordinate of the protein
    const pDomains = domains.filter((d) => d.protein_id === pid);
    const maxEnd = pDomains.reduce((max, d) => Math.max(max, d.domain_end), 0);
    return maxEnd > 0 ? Math.ceil(maxEnd * 1.15) : 600;
  };

  const proteinLength = getProteinLength(selectedProtein);

  // Estimate genome length from the max coordinates in ORFs
  const genomeLength = orfs && orfs.length > 0
    ? orfs.reduce((max, o) => Math.max(max, o.end), 1)
    : 10000; // fallback default

  // Categorize ORFs by frame/strand for the 6-Frame Genome Browser
  // Frames: +1, +2, +3 above genome axis; -1, -2, -3 below
  const forwardFrames: { [key: number]: any[] } = { 1: [], 2: [], 3: [] };
  const reverseFrames: { [key: number]: any[] } = { 1: [], 2: [], 3: [] };

  orfs.forEach((orf, index) => {
    const pid = `seq_${index + 1}`;
    const item = { ...orf, pid };
    if (orf.strand === '+') {
      const frameNum = orf.frame || 1;
      forwardFrames[frameNum].push(item);
    } else {
      const frameNum = orf.frame || 1;
      reverseFrames[frameNum].push(item);
    }
  });

  const trackColors = {
    forward: 'bg-gradient-to-r from-emerald-500 to-teal-400 border border-emerald-400 text-emerald-950',
    reverse: 'bg-gradient-to-r from-amber-500 to-rose-400 border border-amber-400 text-amber-950',
  };

  const colors = ['bg-[#3B82F6]', 'bg-[#22C55E]', 'bg-[#06B6D4]', 'bg-purple-600', 'bg-pink-600'];

  return (
    <div className="bg-[#0B1220] p-6 rounded-lg border border-[#1F2937] text-white flex flex-col gap-8">
      {/* Title & Selection */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-[#1F2937] pb-4 gap-4">
        <div>
          <h4 className="text-md font-bold text-[#60A5FA] font-mono">ORF Genomic Coordinates & Domain architectures</h4>
          <p className="text-xs text-gray-400 mt-1">
            Map open reading frames dynamically on the sequence genome and browse protein domain structures.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400 font-mono">Select Target:</span>
          <select
            value={selectedProtein}
            onChange={(e) => setSelectedProtein(e.target.value)}
            className="bg-[#111827] border border-[#1F2937] rounded px-3 py-1.5 text-xs font-mono text-[#F9FAFB] outline-none max-w-xs focus:border-[#3B82F6]"
          >
            {proteinIds.map((pid) => (
              <option key={pid} value={pid}>
                {pid} {annotationMap.has(pid) ? ` - ${annotationMap.get(pid)}` : ' - Unannotated ORF'}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* 1. 6-Frame Genome Browser Visualizer */}
      {orfs && orfs.length > 0 && (
        <div className="flex flex-col gap-3 bg-[#111827] p-5 rounded-lg border border-[#1F2937]">
          <div className="flex justify-between items-center mb-2">
            <h5 className="text-xs font-bold font-mono text-[#60A5FA] uppercase tracking-wider">Genome 6-Frame Browser Track</h5>
            <span className="text-[10px] font-mono text-gray-500">Genome Length: {genomeLength.toLocaleString()} bp</span>
          </div>

          <div className="relative flex flex-col gap-2 select-none">
            {/* Forward Frames (+3, +2, +1) */}
            {[3, 2, 1].map((f) => (
              <div key={`f+${f}`} className="relative h-6 bg-[#0B1220]/40 rounded border border-gray-900/50 flex items-center">
                <span className="absolute left-2 text-[9px] font-mono font-bold text-emerald-500 z-10">+{f}</span>
                {forwardFrames[f].map((orf) => {
                  const left = (orf.start / genomeLength) * 100;
                  const width = ((orf.end - orf.start) / genomeLength) * 100;
                  const isSelected = selectedProtein === orf.pid;
                  
                  return (
                    <div
                      key={orf.pid}
                      onClick={() => setSelectedProtein(orf.pid)}
                      className={`absolute h-4 rounded text-[9px] font-bold font-mono flex items-center justify-center cursor-pointer transition-all ${
                        isSelected 
                          ? 'bg-gradient-to-r from-cyan-400 to-emerald-400 border border-white shadow-[0_0_8px_rgba(52,211,153,0.5)] scale-y-110 z-20' 
                          : trackColors.forward
                      } group`}
                      style={{ left: `${left}%`, width: `${Math.max(width, 1.5)}%` }}
                    >
                      <span className="truncate px-1 text-[8px] pointer-events-none">
                        {orf.pid}
                      </span>
                      
                      {/* Tooltip */}
                      <div className="absolute bottom-6 scale-0 group-hover:scale-100 bg-[#1F2937] border border-[#3B82F6] p-3 rounded shadow-xl text-[10px] text-white w-52 flex flex-col gap-1 z-50 transition-all font-mono pointer-events-none left-1/2 -translate-x-1/2">
                        <p className="text-emerald-400 font-bold">{orf.pid} (Frame +{f})</p>
                        <p>Coords: {orf.start.toLocaleString()} - {orf.end.toLocaleString()} bp</p>
                        <p>Length: {orf.length.toLocaleString()} bp</p>
                        <p className="text-[#60A5FA] truncate">
                          {annotationMap.has(orf.pid) ? annotationMap.get(orf.pid) : 'No homology annotation'}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            ))}

            {/* Central Genome Axis */}
            <div className="relative h-2 my-2 bg-gradient-to-r from-emerald-600 via-sky-600 to-amber-600 rounded-full w-full flex items-center">
              {/* Coordinate Ticks */}
              {[0, 0.25, 0.5, 0.75, 1].map((p, idx) => {
                const tickVal = Math.floor(p * genomeLength);
                return (
                  <div 
                    key={idx} 
                    className="absolute flex flex-col items-center -translate-x-1/2" 
                    style={{ left: `${p * 100}%` }}
                  >
                    <div className="w-0.5 h-3 bg-gray-500"></div>
                    <span className="text-[8px] font-mono text-gray-500 mt-1 bg-[#111827] px-1 rounded">
                      {tickVal >= 1000 ? `${(tickVal / 1000).toFixed(1)}k bp` : `${tickVal} bp`}
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Reverse Frames (-1, -2, -3) */}
            {[1, 2, 3].map((f) => (
              <div key={`f-${f}`} className="relative h-6 bg-[#0B1220]/40 rounded border border-gray-900/50 flex items-center mt-2">
                <span className="absolute left-2 text-[9px] font-mono font-bold text-amber-500 z-10">-{f}</span>
                {reverseFrames[f].map((orf) => {
                  const left = (orf.start / genomeLength) * 100;
                  const width = ((orf.end - orf.start) / genomeLength) * 100;
                  const isSelected = selectedProtein === orf.pid;
                  
                  return (
                    <div
                      key={orf.pid}
                      onClick={() => setSelectedProtein(orf.pid)}
                      className={`absolute h-4 rounded text-[9px] font-bold font-mono flex items-center justify-center cursor-pointer transition-all ${
                        isSelected 
                          ? 'bg-gradient-to-r from-amber-400 to-rose-400 border border-white shadow-[0_0_8px_rgba(251,191,36,0.5)] scale-y-110 z-20' 
                          : trackColors.reverse
                      } group`}
                      style={{ left: `${left}%`, width: `${Math.max(width, 1.5)}%` }}
                    >
                      <span className="truncate px-1 text-[8px] pointer-events-none">
                        {orf.pid}
                      </span>
                      
                      {/* Tooltip */}
                      <div className="absolute bottom-6 scale-0 group-hover:scale-100 bg-[#1F2937] border border-[#3B82F6] p-3 rounded shadow-xl text-[10px] text-white w-52 flex flex-col gap-1 z-50 transition-all font-mono pointer-events-none left-1/2 -translate-x-1/2">
                        <p className="text-amber-400 font-bold">{orf.pid} (Frame -{f})</p>
                        <p>Coords: {orf.start.toLocaleString()} - {orf.end.toLocaleString()} bp</p>
                        <p>Length: {orf.length.toLocaleString()} bp</p>
                        <p className="text-[#60A5FA] truncate">
                          {annotationMap.has(orf.pid) ? annotationMap.get(orf.pid) : 'No homology annotation'}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 2. Sleek Pfam Domain Visualizer */}
      <div className="flex flex-col gap-6 bg-[#111827] p-5 rounded-lg border border-[#1F2937]">
        <div className="flex justify-between items-center">
          <h5 className="text-xs font-bold font-mono text-[#60A5FA] uppercase tracking-wider">
            Domain architecture Backbone: {selectedProtein}
          </h5>
          <span className="text-xs text-[#9CA3AF] font-mono">Protein Length: {proteinLength} aa</span>
        </div>

        <div className="relative mt-2 pt-4 pb-12 px-2">
          {/* Glowing Thin Backbone Wire */}
          <div className="relative h-1.5 bg-[#1F2937] shadow-[0_0_8px_rgba(59,130,246,0.2)] rounded-full w-full flex items-center">
            {currentDomains.map((dom, index) => {
              const leftOffset = (dom.domain_start / proteinLength) * 100;
              const widthOffset = ((dom.domain_end - dom.domain_start) / proteinLength) * 100;
              const color = colors[index % colors.length];

              return (
                <React.Fragment key={dom.pfam_accession}>
                  {/* Domain Capsule Pill */}
                  <div
                    className={`absolute h-7 rounded-full border border-gray-900/60 shadow-[0_2px_4px_rgba(0,0,0,0.3)] flex items-center justify-center text-[10px] font-bold font-mono text-white cursor-pointer transition-all hover:scale-105 hover:shadow-[0_0_10px_rgba(255,255,255,0.3)] ${color} group`}
                    style={{ left: `${leftOffset}%`, width: `${Math.max(widthOffset, 8)}%` }}
                  >
                    <span className="truncate px-2">{dom.pfam_name}</span>
                    
                    {/* Domain Hover Detail box */}
                    <div className="absolute top-9 bg-[#1F2937] border border-[#3B82F6] p-3 rounded shadow-2xl text-[10px] w-52 flex flex-col gap-1 z-50 transition-all font-mono pointer-events-none scale-0 group-hover:scale-100 left-1/2 -translate-x-1/2">
                      <p className="text-[#60A5FA] font-bold">{dom.pfam_name}</p>
                      <p className="text-[9px] text-gray-400">Accession: {dom.pfam_accession}</p>
                      <p>Residues: {dom.domain_start} - {dom.domain_end} aa</p>
                      <p>E-value: {dom.evalue.toExponential(2)}</p>
                    </div>
                  </div>

                  {/* Visual Coordinate Indicator Lines */}
                  <div 
                    className="absolute flex flex-col items-center -translate-x-1/2 top-4 select-none"
                    style={{ left: `${leftOffset}%` }}
                  >
                    <div className="w-px h-2 bg-gray-600"></div>
                    <span className="text-[8px] font-mono text-gray-500">{dom.domain_start}aa</span>
                  </div>
                  <div 
                    className="absolute flex flex-col items-center -translate-x-1/2 top-4 select-none"
                    style={{ left: `${leftOffset + widthOffset}%` }}
                  >
                    <div className="w-px h-2 bg-gray-600"></div>
                    <span className="text-[8px] font-mono text-gray-500">{dom.domain_end}aa</span>
                  </div>
                </React.Fragment>
              );
            })}
          </div>

          {/* Core Ruler Endpoints */}
          <div className="absolute left-2 right-2 bottom-3 flex justify-between text-[10px] text-gray-500 font-mono select-none">
            <span>0 aa</span>
            <span>{proteinLength} aa</span>
          </div>
        </div>

        {currentDomains.length === 0 && (
          <p className="text-center text-xs text-gray-500 italic py-2">
            No structural Pfam domains predicted for this translated sequence.
          </p>
        )}
      </div>

      {/* 3. Interactive Predicted ORFs Coordinates Table */}
      {orfs && orfs.length > 0 && (
        <div className="flex flex-col gap-4">
          <h4 className="text-xs font-bold font-mono text-[#60A5FA] uppercase tracking-wider">
            Predicted Open Reading Frames (ORFs) Coordinates List
          </h4>
          <div className="overflow-x-auto max-h-[300px] border border-[#1F2937] rounded-lg">
            <table className="min-w-full divide-y divide-[#1F2937] text-xs font-mono">
              <thead className="bg-[#111827] sticky top-0 z-10">
                <tr>
                  <th className="px-4 py-2.5 text-left text-[#9CA3AF]">Protein ID</th>
                  <th className="px-4 py-2.5 text-left text-[#9CA3AF]">Start Coordinate (bp)</th>
                  <th className="px-4 py-2.5 text-left text-[#9CA3AF]">End Coordinate (bp)</th>
                  <th className="px-4 py-2.5 text-left text-[#9CA3AF]">Length (bp)</th>
                  <th className="px-4 py-2.5 text-left text-[#9CA3AF]">Strand</th>
                  <th className="px-4 py-2.5 text-left text-[#9CA3AF]">Frame</th>
                  <th className="px-4 py-2.5 text-left text-[#9CA3AF]">Homologous SwissProt hit</th>
                  <th className="px-4 py-2.5 text-right text-[#9CA3AF]">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1F2937] bg-[#0B1220]/20">
                {orfs.map((orf, idx) => {
                  const pid = `seq_${idx + 1}`;
                  const hasAnnotation = annotationMap.has(pid);
                  const isSelected = selectedProtein === pid;
                  return (
                    <tr 
                      key={idx} 
                      onClick={() => setSelectedProtein(pid)}
                      className={`hover:bg-[#172033]/60 cursor-pointer transition-colors ${
                        isSelected ? 'bg-[#172033]/80 border-l-2 border-[#3B82F6]' : ''
                      }`}
                    >
                      <td className={`px-4 py-2.5 font-bold ${isSelected ? 'text-[#3B82F6]' : 'text-gray-300'}`}>
                        {pid} {isSelected && <span className="text-[9px] text-[#22C55E] ml-1">(Active)</span>}
                      </td>
                      <td className="px-4 py-2.5">{orf.start.toLocaleString()}</td>
                      <td className="px-4 py-2.5">{orf.end.toLocaleString()}</td>
                      <td className="px-4 py-2.5 font-bold text-gray-300">{orf.length.toLocaleString()} bp</td>
                      <td className="px-4 py-2.5">
                        <span className={`px-2 py-0.5 rounded text-[9px] font-bold ${
                          orf.strand === '+' ? 'bg-green-950/60 text-green-400 border border-green-900/60' : 'bg-red-950/60 text-red-400 border border-red-900/60'
                        }`}>
                          {orf.strand}
                        </span>
                      </td>
                      <td className="px-4 py-2.5">{orf.frame}</td>
                      <td className="px-4 py-2.5 text-gray-300 max-w-[200px] truncate">
                        {hasAnnotation ? (
                          <span className="text-[#60A5FA]" title={annotationMap.get(pid)}>
                            {annotationMap.get(pid)}
                          </span>
                        ) : (
                          <span className="text-gray-500 italic">No homolog hit</span>
                        )}
                      </td>
                      <td className="px-4 py-2.5 text-right">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedProtein(pid);
                          }}
                          className={`px-2 py-1 rounded text-[9px] font-semibold transition-colors ${
                            isSelected ? 'bg-[#3B82F6] text-white' : 'bg-[#172033] hover:bg-[#1F2937] text-gray-400'
                          }`}
                        >
                          Select
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
