'use client';

import React from 'react';

export default function DocumentationPage() {
  return (
    <div className="p-inner-padding max-w-4xl mx-auto space-y-8 bg-[#0c1321] text-[#dce2f6] select-text">
      {/* Title */}
      <div>
        <h1 className="text-3xl font-bold text-text-primary">PathoScope AI Documentation</h1>
        <p className="text-sm text-text-muted mt-2">
          Technical specifications, biological pipeline validations, and operational manual for PathoScope AI v3.0.
        </p>
      </div>

      {/* Quick Start Manual */}
      <section className="bg-[#1F2937] p-6 rounded-lg border border-[#424754] space-y-4">
        <h2 className="text-lg font-bold text-[#60A5FA] border-b border-[#111827] pb-2">Quick Start Manual</h2>
        <div className="text-xs leading-relaxed space-y-3">
          <p>
            PathoScope AI simplifies bioinformatics pipeline runs by automatically detecting sequence file types and routing them to the correct workflow calculation engine:
          </p>
          <ol className="list-decimal pl-5 space-y-2">
            <li>
              <strong>Sequence Upload</strong>: Navigate to the **Workspace** page and drop your sequence file (FASTA, FASTQ, or expression table DEG) into the upload dropzone.
            </li>
            <li>
              <strong>Automatic Detection</strong>: The platform scans file headers (&apos;&gt;&apos; for FASTA, &apos;@&apos; for FASTQ, tabular headers for DEG) and labels the detected workflow with a colored badge.
            </li>
            <li>
              <strong>Pipeline Execution</strong>: Click **Run Pipeline**. The center panel streams live pipeline steps and raw stdout logs from bioinformatics binaries.
            </li>
            <li>
              <strong>Progressive Results</strong>: View metrics and charts (e.g. Pfam domains, taxonomy lineages, volcano plots, and Pubmed publications) instantly as steps finish.
            </li>
            <li>
              <strong>Export Outputs</strong>: Use the Download Center to download audit-ready HTML, PDF, GFF3, CSV, and JSON results bundles.
            </li>
          </ol>
        </div>
      </section>

      {/* Biological Specifications */}
      <section className="space-y-4">
        <h2 className="text-lg font-bold text-[#60A5FA] border-b border-[#424754] pb-2 font-mono">Biological Workflows Specification</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs">
          <div className="bg-[#1F2937] border border-[#424754] p-4 rounded-lg">
            <h3 className="font-bold text-white mb-2">FASTA Genome Analysis</h3>
            <ul className="list-disc pl-4 space-y-1.5 text-text-muted">
              <li>Ambiguity base count & GC%</li>
              <li>6-frame translation (BioPython)</li>
              <li>SwissProt Blast alignment (DIAMOND)</li>
              <li>Pfam domain architecture</li>
              <li>NCBI taxonomy assignment</li>
            </ul>
          </div>
          <div className="bg-[#1F2937] border border-[#424754] p-4 rounded-lg">
            <h3 className="font-bold text-white mb-2">FASTQ NGS Quality Control</h3>
            <ul className="list-disc pl-4 space-y-1.5 text-text-muted">
              <li>Raw sequence check (FastQC)</li>
              <li>Adapter trimming & Q20 trim (fastp)</li>
              <li>Viral contigs assembly (SPAdes)</li>
              <li>Length filtering (&ge;500bp)</li>
              <li>Automatic handoff to FASTA</li>
            </ul>
          </div>
          <div className="bg-[#1F2937] border border-[#424754] p-4 rounded-lg">
            <h3 className="font-bold text-white mb-2">DEG Transcriptomics</h3>
            <ul className="list-disc pl-4 space-y-1.5 text-text-muted">
              <li>Normalizations (HGNC/Ensembl)</li>
              <li>Benjamini-Hochberg FDR correction</li>
              <li>UP/DOWN/NS classification</li>
              <li>GO & KEGG enrichment maps</li>
              <li>Pubmed & AI pathbiology interpretation</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Authoritative Thresholds Table */}
      <section className="space-y-4">
        <h2 className="text-lg font-bold text-[#60A5FA] border-b border-[#424754] pb-2 font-mono">System Threshold Constants</h2>
        <div className="overflow-x-auto bg-[#1F2937] rounded-lg border border-[#424754]">
          <table className="w-full text-left border-collapse text-xs font-mono">
            <thead className="bg-[#151b2a] text-[#9CA3AF]">
              <tr>
                <th className="px-4 py-3 border-b border-[#424754]">Constant</th>
                <th className="px-4 py-3 border-b border-[#424754]">Value</th>
                <th className="px-4 py-3 border-b border-[#424754]">Subsystem</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#424754] text-white">
              <tr>
                <td className="px-4 py-2">MIN_ORF_LENGTH_BP</td>
                <td className="px-4 py-2">100 bp</td>
                <td className="px-4 py-2">ORF Predictor</td>
              </tr>
              <tr>
                <td className="px-4 py-2">EVALUE_THRESHOLD</td>
                <td className="px-4 py-2">1e-5</td>
                <td className="px-4 py-2">DIAMOND / blastp</td>
              </tr>
              <tr>
                <td className="px-4 py-2">IDENTITY_THRESHOLD</td>
                <td className="px-4 py-2">30 %</td>
                <td className="px-4 py-2">DIAMOND Alignment</td>
              </tr>
              <tr>
                <td className="px-4 py-2">COVERAGE_THRESHOLD</td>
                <td className="px-4 py-2">50 %</td>
                <td className="px-4 py-2">DIAMOND Alignment</td>
              </tr>
              <tr>
                <td className="px-4 py-2">FASTQ_MIN_PHRED</td>
                <td className="px-4 py-2">Q20</td>
                <td className="px-4 py-2">fastp Trimming</td>
              </tr>
              <tr>
                <td className="px-4 py-2">FASTQ_MIN_LEN</td>
                <td className="px-4 py-2">50 bp</td>
                <td className="px-4 py-2">fastp Trimming</td>
              </tr>
              <tr>
                <td className="px-4 py-2">DEG_FDR_THRESHOLD</td>
                <td className="px-4 py-2">0.05</td>
                <td className="px-4 py-2">DEG classification</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
