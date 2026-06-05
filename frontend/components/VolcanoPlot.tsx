import React from 'react';

interface VolcanoPlotProps {
  onSelectGene: (gene: { symbol: string; fc: number; fdr: number }) => void;
}

export const VolcanoPlot: React.FC<VolcanoPlotProps> = ({ onSelectGene }) => {
  // SVG Mock Volcano Plot for maximum stability and fast load times
  const mockGenes = [
    { symbol: 'TP53', fc: 2.4, fdr: 0.001, cx: 380, cy: 80, color: '#22C55E' },
    { symbol: 'EGFR', fc: 1.8, fdr: 0.005, cx: 340, cy: 120, color: '#22C55E' },
    { symbol: 'STAT3', fc: 1.2, fdr: 0.012, cx: 310, cy: 160, color: '#22C55E' },
    { symbol: 'IL6', fc: -1.8, fdr: 0.002, cx: 120, cy: 100, color: '#3B82F6' },
    { symbol: 'TNF', fc: -2.1, fdr: 0.0008, cx: 80, cy: 70, color: '#3B82F6' },
    { symbol: 'MAPK1', fc: -1.1, fdr: 0.02, cx: 180, cy: 190, color: '#3B82F6' },
    { symbol: 'ACTB', fc: 0.1, fdr: 0.8, cx: 240, cy: 260, color: '#9CA3AF' },
    { symbol: 'GAPDH', fc: -0.2, fdr: 0.9, cx: 210, cy: 280, color: '#9CA3AF' },
  ];

  return (
    <div className="flex flex-col gap-4 text-white">
      <div className="flex justify-between items-center select-none">
        <h4 className="text-sm font-bold text-[#60A5FA] font-mono">Volcano Plot (log2FC vs -log10 FDR)</h4>
        <div className="flex gap-4 text-xs font-mono">
          <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-full bg-[#22C55E]" /> Upregulated</span>
          <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-full bg-[#3B82F6]" /> Downregulated</span>
          <span className="flex items-center gap-1"><span className="h-2 w-2 rounded-full bg-[#9CA3AF]" /> Muted</span>
        </div>
      </div>

      <div className="relative border border-[#1F2937] bg-[#111827] rounded p-2">
        <svg viewBox="0 0 500 350" className="w-full h-auto">
          {/* Threshold markers */}
          <line x1="0" y1="200" x2="500" y2="200" stroke="#EF4444" strokeDasharray="4 4" opacity="0.6" />
          <line x1="200" y1="0" x2="200" y2="350" stroke="#9CA3AF" strokeDasharray="4 4" opacity="0.4" />
          <line x1="300" y1="0" x2="300" y2="350" stroke="#9CA3AF" strokeDasharray="4 4" opacity="0.4" />

          {/* Grid labels */}
          <text x="240" y="340" fill="#9CA3AF" fontSize="10" fontFamily="monospace">0</text>
          <text x="40" y="340" fill="#9CA3AF" fontSize="10" fontFamily="monospace">-2</text>
          <text x="440" y="340" fill="#9CA3AF" fontSize="10" fontFamily="monospace">+2</text>
          <text x="10" y="20" fill="#9CA3AF" fontSize="8" fontFamily="monospace" transform="rotate(-90 10 20)">-log10(FDR)</text>
          <text x="220" y="345" fill="#9CA3AF" fontSize="8" fontFamily="monospace">log2FC</text>

          {/* Gene coordinates */}
          {mockGenes.map((gene) => (
            <g
              key={gene.symbol}
              onClick={() => onSelectGene({ symbol: gene.symbol, fc: gene.fc, fdr: gene.fdr })}
              className="cursor-pointer group"
            >
              <circle
                cx={gene.cx}
                cy={gene.cy}
                r="6"
                fill={gene.color}
                className="hover:r-8 transition-all duration-100"
              />
              <text
                x={gene.cx + 8}
                y={gene.cy + 4}
                fill="#F9FAFB"
                fontSize="8"
                fontFamily="monospace"
                className="opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"
              >
                {gene.symbol}
              </text>
            </g>
          ))}
        </svg>
      </div>
    </div>
  );
};
