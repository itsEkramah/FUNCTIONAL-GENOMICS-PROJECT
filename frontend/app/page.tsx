'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';

export default function LandingPage() {
  const [terminalLines, setTerminalLines] = useState<Array<{ time: string; level: string; msg: string; color: string }>>([]);

  const logDatabase = [
    { time: '09:42:01', level: 'INFO', msg: 'Initializing PathoScope Core...', color: 'text-tertiary' },
    { time: '09:42:04', level: 'INFO', msg: 'Loading Genomic Reference Model (SARS-CoV-2)...', color: 'text-tertiary' },
    { time: '09:42:08', level: 'EXEC', msg: 'Aligning FASTA sequences to hg38 reference...', color: 'text-primary-container' },
    { time: '09:42:15', level: 'WARN', msg: 'Low coverage detected at locus 1420-1455. Re-indexing...', color: 'text-warning' },
    { time: '09:42:22', level: 'DONE', msg: 'Analysis Complete. Found 12 high-confidence variants.', color: 'text-success' }
  ];

  useEffect(() => {
    // Typing simulation on landing page
    logDatabase.forEach((line, index) => {
      setTimeout(() => {
        setTerminalLines((prev) => [...prev, line]);
      }, 600 + index * 1000);
    });
  }, []);

  return (
    <main className="flex-1 min-h-screen relative overflow-y-auto">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-20 pb-24 px-gutter hero-gradient">
        <div className="max-w-container-max mx-auto text-center">
          <h1 className="text-5xl md:text-7xl font-bold text-text-primary tracking-tight mb-6">
            PathoScope AI
          </h1>
          <p className="text-lg md:text-xl text-text-muted max-w-2xl mx-auto mb-12 font-medium">
            Automated Functional Genomics Platform. Accelerated discovery through machine learning assisted pathogen analysis.
          </p>
          
          <div className="max-w-md mx-auto">
            {/* Upload Zone Link */}
            <Link href="/workspace">
              <div className="border-2 border-dashed border-outline-variant bg-surface-container-low rounded-xl p-8 mb-6 hover:border-primary/50 hover:bg-surface-container transition-all cursor-pointer group">
                <div className="flex flex-col items-center">
                  <span className="material-symbols-outlined text-4xl text-primary mb-3 group-hover:scale-110 transition-transform">
                    upload_file
                  </span>
                  <span className="text-lg text-text-primary font-semibold mb-1">Upload Data File</span>
                  <span className="text-xs text-text-muted">Drag and drop or click to browse workspace</span>
                </div>
              </div>
            </Link>

            {/* File Type Guidance */}
            <div className="text-center mb-8">
              <p className="text-xs text-on-surface-variant/70 italic">
                Acceptable formats: FASTA, FASTQ, FASTQ.GZ, CSV, CSV.GZ, TSV, TSV.GZ
              </p>
            </div>

            {/* Primary Action */}
            <div className="flex justify-center">
              <Link href="/workspace" className="w-full max-w-xs">
                <button className="w-full bg-primary text-on-primary font-semibold px-8 py-4 rounded-lg hover:opacity-90 transition-all flex items-center justify-center gap-3 shadow-lg shadow-primary/10">
                  <span className="material-symbols-outlined text-[20px]">analytics</span>
                  Start Analysis
                </button>
              </Link>
            </div>
          </div>
        </div>

        {/* Dashboard Preview / Terminal Visual */}
        <div className="mt-20 max-w-4xl mx-auto rounded-xl border border-outline-variant bg-surface-container-low shadow-2xl overflow-hidden">
          <div className="bg-surface-container-high px-4 py-2 border-b border-outline-variant flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></div>
            <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
            <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50"></div>
            <div className="ml-4 font-mono text-xs text-on-surface-variant">terminal — analysis_engine_v2.sh</div>
          </div>
          <div className="p-6 font-mono text-xs leading-relaxed text-primary h-48 overflow-y-auto">
            {terminalLines.map((line, idx) => (
              <div key={idx} className="flex gap-4 mb-2 transition-all duration-300">
                <span className="text-text-muted">[{line.time}]</span>
                <span className={line.color}>{line.level}</span>
                <span>{line.msg}</span>
              </div>
            ))}
            <div className="animate-pulse inline-block w-2 h-4 bg-primary ml-1 align-middle"></div>
          </div>
        </div>
      </section>

      {/* Workflows Section */}
      <section className="py-20 px-gutter border-t border-outline-variant bg-surface-container-lowest">
        <div className="max-w-container-max mx-auto">
          <div className="mb-16 text-center md:text-left">
            <h2 className="text-3xl font-bold text-text-primary mb-4">Supported Workflows & Pipelines</h2>
            <p className="text-sm text-text-muted max-w-xl">
              Standardized pipelines for rapid genomic processing. Engineered for high-throughput laboratory environments.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* FASTA */}
            <div className="bg-bg-card border border-outline-variant p-6 rounded-xl flex flex-col h-full hover:border-[#adc6ff] transition-all">
              <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary mb-6">
                <span className="material-symbols-outlined">dns</span>
              </div>
              <h3 className="text-lg font-bold text-text-primary mb-3">FASTA Analysis</h3>
              <p className="text-sm text-text-muted mb-8 flex-grow">
                Primary sequence alignment and homology modeling. Identify conserved domains and functional motifs with sub-millisecond latency.
              </p>
              <Link href="/workspace" className="flex items-center gap-2 text-primary hover:underline text-sm font-semibold mt-auto">
                Launch Pipeline
                <span className="material-symbols-outlined text-sm">arrow_outward</span>
              </Link>
            </div>
            
            {/* FASTQ */}
            <div className="bg-bg-card border border-outline-variant p-6 rounded-xl flex flex-col h-full hover:border-[#adc6ff] transition-all">
              <div className="w-12 h-12 rounded-lg bg-tertiary/10 flex items-center justify-center text-tertiary mb-6">
                <span className="material-symbols-outlined">analytics</span>
              </div>
              <h3 className="text-lg font-bold text-text-primary mb-3">FASTQ Processing</h3>
              <p className="text-sm text-text-muted mb-8 flex-grow">
                Raw read quality control, trimming, and de novo assembly. Built-in error correction for Illumina and Oxford Nanopore platforms.
              </p>
              <Link href="/workspace" className="flex items-center gap-2 text-tertiary hover:underline text-sm font-semibold mt-auto">
                Launch Pipeline
                <span className="material-symbols-outlined text-sm">arrow_outward</span>
              </Link>
            </div>
            
            {/* DEG */}
            <div className="bg-bg-card border border-outline-variant p-6 rounded-xl flex flex-col h-full hover:border-[#adc6ff] transition-all">
              <div className="w-12 h-12 rounded-lg bg-secondary/10 flex items-center justify-center text-secondary mb-6">
                <span className="material-symbols-outlined">stacked_line_chart</span>
              </div>
              <h3 className="text-lg font-bold text-text-primary mb-3">DEG Profiling</h3>
              <p className="text-sm text-text-muted mb-8 flex-grow">
                Differential Gene Expression analysis with integrated volcano plots and GO enrichment. Identify critical pathways automatically.
              </p>
              <Link href="/workspace" className="flex items-center gap-2 text-secondary hover:underline text-sm font-semibold mt-auto">
                Launch Pipeline
                <span className="material-symbols-outlined text-sm">arrow_outward</span>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer / CTA */}
      <section className="py-20 px-gutter bg-surface-container-low border-t border-outline-variant relative overflow-hidden">
        <div className="absolute inset-0 opacity-10 pointer-events-none grid-bg-pattern"></div>
        <div className="max-w-container-max mx-auto text-center relative z-10">
          <h2 className="text-3xl md:text-4xl font-bold text-text-primary mb-6">Ready to accelerate your research?</h2>
          
          <div className="flex justify-center gap-4">
            <Link href="/workspace">
              <button className="bg-primary text-on-primary font-semibold px-10 py-4 rounded-lg hover:shadow-[0_0_20px_rgba(173,198,255,0.3)] transition-all">
                Create Workspace
              </button>
            </Link>
          </div>

          <div className="mt-20 pt-12 border-t border-outline-variant flex flex-col md:flex-row justify-between items-center gap-8 text-xs text-on-surface-variant">
            <div className="text-primary font-bold text-lg">PathoScope AI</div>
            <div className="flex gap-8">
              <Link href="/documentation" className="hover:text-primary transition-colors">Documentation</Link>
              <a href="#" className="hover:text-primary transition-colors">API Reference</a>
              <a href="#" className="hover:text-primary transition-colors">Compliance</a>
              <a href="#" className="hover:text-primary transition-colors">Contact Support</a>
            </div>
            <div>
              © 2026 PathoScope Genomic Solutions. All rights reserved.
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
