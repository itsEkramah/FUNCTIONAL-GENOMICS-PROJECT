import React, { useState } from 'react';
import { TaxonomyResults } from '../types';

interface TaxonomyTreeProps {
  taxonomy: TaxonomyResults;
}

export const TaxonomyTree: React.FC<TaxonomyTreeProps> = ({ taxonomy }) => {
  const [collapsed, setCollapsed] = useState<Record<string, boolean>>({});

  const toggleNode = (node: string) => {
    setCollapsed((prev) => ({ ...prev, [node]: !prev[node] }));
  };

  return (
    <div className="bg-[#0B1220] p-6 rounded-lg border border-[#1F2937] text-white flex flex-col gap-4 font-mono text-sm">
      <div className="border-b border-[#1F2937] pb-2 mb-2">
        <h4 className="text-sm font-bold text-[#60A5FA]">NCBI Taxonomy Browser</h4>
      </div>

      <div className="flex flex-col gap-2 pl-2">
        {taxonomy.lineage.map((taxon, idx) => {
          const isCollapsed = collapsed[taxon];
          return (
            <div key={taxon} style={{ paddingLeft: `${idx * 16}px` }} className="flex flex-col gap-1">
              <div
                onClick={() => toggleNode(taxon)}
                className="cursor-pointer hover:text-[#60A5FA] flex items-center gap-1 select-none text-[#D1D5DB]"
              >
                <span>{isCollapsed ? '▶' : '▼'}</span>
                <span>{taxon}</span>
              </div>
            </div>
          );
        })}
        {/* Highlighted organism target */}
        <div style={{ paddingLeft: `${taxonomy.lineage.length * 16}px` }} className="mt-2">
          <div className="bg-[#06B6D4]/10 border border-[#06B6D4] text-[#06B6D4] font-bold p-3 rounded flex flex-col gap-1">
            <span className="text-[10px] uppercase tracking-wider font-mono">Organism Detected</span>
            <span className="text-sm font-bold italic">{taxonomy.organism_name}</span>
            <span className="text-[10px] text-gray-400 font-mono">NCBI TaxID: {taxonomy.tax_id} | Rank: {taxonomy.rank}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
