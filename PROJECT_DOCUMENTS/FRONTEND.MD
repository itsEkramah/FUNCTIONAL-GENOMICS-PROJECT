##ONE MORE THIING IT IS GIVING OPTION TO COPY CODE TO CLIPBOARD

## LANDIG PAGE 1 AND LANDING PAGE 2 SCROLLABLE      


<!DOCTYPE html><html class="dark" lang="en" style=""><head>
<meta charset="utf-8">
<meta content="width=device-width, initial-scale=1.0" name="viewport">
<title>PathoScope AI | Genomic Research Platform</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;family=JetBrains+Mono:wght@400&amp;display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet">
<script id="tailwind-config">
      tailwind.config = {
        darkMode: "class",
        theme: {
          extend: {
            "colors": {
                    "on-surface-variant": "#c2c6d6",
                    "on-secondary": "#003640",
                    "error-container": "#93000a",
                    "on-tertiary-fixed": "#002113",
                    "surface-container": "#19202e",
                    "on-tertiary-fixed-variant": "#005236",
                    "secondary-fixed": "#acedff",
                    "on-primary": "#002e6a",
                    "bg-panel": "#172033",
                    "tertiary": "#4edea3",
                    "success": "#10B981",
                    "on-primary-fixed": "#001a42",
                    "inverse-on-surface": "#2a3040",
                    "on-error": "#690005",
                    "surface": "#0c1321",
                    "text-primary": "#F9FAFB",
                    "primary-fixed-dim": "#adc6ff",
                    "text-muted": "#9CA3AF",
                    "inverse-surface": "#dce2f6",
                    "on-secondary-fixed-variant": "#004e5c",
                    "secondary": "#4cd7f6",
                    "outline": "#8c909f",
                    "bg-card": "#1F2937",
                    "surface-bright": "#323949",
                    "primary-container": "#4d8eff",
                    "on-tertiary": "#003824",
                    "bg-secondary": "#111827",
                    "surface-container-low": "#151b2a",
                    "on-primary-container": "#00285d",
                    "surface-variant": "#2e3544",
                    "surface-container-high": "#232a39",
                    "secondary-fixed-dim": "#4cd7f6",
                    "tertiary-container": "#00a572",
                    "on-tertiary-container": "#00311f",
                    "on-surface": "#dce2f6",
                    "background": "#0c1321",
                    "on-secondary-fixed": "#001f26",
                    "surface-dim": "#0c1321",
                    "warning": "#F59E0B",
                    "text-secondary": "#D1D5DB",
                    "outline-variant": "#424754",
                    "tertiary-fixed-dim": "#4edea3",
                    "on-secondary-container": "#00424e",
                    "on-primary-fixed-variant": "#004395",
                    "primary": "#adc6ff",
                    "error": "#EF4444",
                    "tertiary-fixed": "#6ffbbe",
                    "surface-container-highest": "#2e3544",
                    "surface-container-lowest": "#070e1c",
                    "on-background": "#dce2f6",
                    "on-error-container": "#ffdad6",
                    "inverse-primary": "#005ac2",
                    "primary-fixed": "#d8e2ff",
                    "surface-tint": "#adc6ff",
                    "secondary-container": "#03b5d3"
            },
            "borderRadius": {
                    "DEFAULT": "0.125rem",
                    "lg": "0.25rem",
                    "xl": "0.5rem",
                    "full": "0.75rem"
            },
            "spacing": {
                    "inner-padding": "1rem",
                    "gutter": "1.5rem",
                    "container-max": "1280px",
                    "panel-gap": "1rem",
                    "card-padding": "1.5rem"
            },
            "fontFamily": {
                    "body-sm": ["Inter"],
                    "badge": ["Inter"],
                    "body-base": ["Inter"],
                    "subheading": ["Inter"],
                    "code-xs": ["JetBrains Mono"],
                    "headline-md": ["Inter"],
                    "headline-lg": ["Inter"],
                    "code-sm": ["JetBrains Mono"]
            },
            "fontSize": {
                    "body-sm": ["12px", {"lineHeight": "16px", "fontWeight": "400"}],
                    "badge": ["10px", {"lineHeight": "12px", "letterSpacing": "0.05em", "fontWeight": "700"}],
                    "body-base": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                    "subheading": ["14px", {"lineHeight": "20px", "fontWeight": "600"}],
                    "code-xs": ["10px", {"lineHeight": "14px", "fontWeight": "400"}],
                    "headline-md": ["18px", {"lineHeight": "24px", "fontWeight": "600"}],
                    "headline-lg": ["24px", {"lineHeight": "32px", "fontWeight": "700"}],
                    "code-sm": ["12px", {"lineHeight": "18px", "fontWeight": "400"}]
            }
          },
        },
      }
    </script>
<style>
        body {
            background-color: #0c1321;
            color: #dce2f6;
            font-family: 'Inter', sans-serif;
        }
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        .bento-grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 1.5rem;
        }
        .workflow-card {
            background-color: #1F2937;
            border: 1px solid #424754;
            transition: all 0.2s ease-in-out;
        }
        .workflow-card:hover {
            border-color: #adc6ff;
            background-color: #172033;
        }
        .hero-gradient {
            background: radial-gradient(circle at 50% 50%, rgba(173, 198, 255, 0.08) 0%, rgba(12, 19, 33, 0) 70%);
        }
    </style>
</head>
<body class="selection:bg-primary-container selection:text-on-primary-container">
<!-- TopNavBar -->
<nav class="bg-surface dark:bg-surface border-b border-outline-variant fixed top-0 w-full h-16 z-50 flex justify-between items-center px-gutter">
<div class="flex items-center gap-8">
<span class="font-headline-md text-headline-md font-bold text-primary">PathoScope AI</span>
<div class="hidden md:flex items-center gap-6">
<a class="font-body-base text-body-base text-primary border-b-2 border-primary pb-1 hover:text-primary transition-colors" href="#">Dashboard</a>
<a class="font-body-base text-body-base text-on-surface-variant hover:text-primary transition-colors" href="#">Workspace</a>
<a class="font-body-base text-body-base text-on-surface-variant hover:text-primary transition-colors" href="#">Reports</a>
<a class="font-body-base text-body-base text-on-surface-variant hover:text-primary transition-colors" href="#">Literature Explorer</a>
<a class="font-body-base text-body-base text-on-surface-variant hover:text-primary transition-colors" href="#">Settings</a>
</div>
</div>
<div class="flex items-center gap-4">
<button class="text-on-surface-variant hover:text-primary transition-colors"><span class="material-symbols-outlined" data-icon="notifications">notifications</span></button>
<button class="text-on-surface-variant hover:text-primary transition-colors"><span class="material-symbols-outlined" data-icon="help">help</span></button>
<button class="text-on-surface-variant hover:text-primary transition-colors"><span class="material-symbols-outlined" data-icon="account_circle">account_circle</span></button>
</div>
</nav>
<main class="pt-16 min-h-screen">
<!-- Hero Section -->
<section class="relative overflow-hidden pt-24 pb-32 px-gutter hero-gradient">
<div class="max-w-container-max mx-auto text-center">

<h1 class="font-headline-lg text-6xl md:text-7xl font-bold text-text-primary tracking-tight mb-6">PathoScope AI</h1>
<p class="font-subheading text-xl text-text-muted max-w-2xl mx-auto mb-12">Automated Functional Genomics Platform. Accelerated discovery through machine learning assisted pathogen analysis.</p>
<div class="max-w-md mx-auto">
  <!-- Upload Zone -->
  <div class="border-2 border-dashed border-outline-variant bg-surface-container-low rounded-xl p-8 mb-4 hover:border-primary/50 hover:bg-surface-container transition-all cursor-pointer group">
    <div class="flex flex-col items-center">
      <span class="material-symbols-outlined text-4xl text-primary mb-3 group-hover:scale-110 transition-transform">upload_file</span>
      <span class="font-subheading text-lg text-text-primary mb-1">Upload Data File</span>
      <span class="font-body-sm text-text-muted">Drag and drop or click to browse</span>
    </div>
  </div>
  
  <!-- File Type Guidance -->
  <div class="text-center mb-8">
    <p class="font-body-sm text-on-surface-variant/70 italic">Acceptable formats: FASTA, FASTQ ,FASTQ.GZ, CSV,CSV.GZ, TSV ,TSV.GZ</p>
  </div>

  <!-- Primary Action -->
  <div class="flex justify-center">
    <button class="w-full max-w-xs bg-primary text-on-primary font-subheading text-subheading px-8 py-4 rounded-lg hover:opacity-90 transition-all flex items-center justify-center gap-3 shadow-lg shadow-primary/10">
      <span class="material-symbols-outlined text-[20px]">analytics</span>
      Start Analysis
    </button>
  </div>
</div>
</div>
<!-- Dashboard Preview / Decorative Element -->
<div class="mt-20 max-w-5xl mx-auto rounded-xl border border-outline-variant bg-surface-container-low shadow-2xl overflow-hidden">
<div class="bg-surface-container-high px-4 py-2 border-b border-outline-variant flex items-center gap-2">
<div class="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></div>
<div class="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
<div class="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50"></div>
<div class="ml-4 font-code-sm text-code-sm text-on-surface-variant">terminal — analysis_engine_v2.sh</div>
</div>
<div class="p-6 font-code-sm text-code-sm text-primary leading-relaxed">
<div class="flex gap-4 mb-2" style="opacity: 1; transform: translateY(0px); transition: 0.4s ease-out;"><span class="text-text-muted">[09:42:01]</span> <span class="text-tertiary">INFO</span> Initializing PathoScope Core...</div>
<div class="flex gap-4 mb-2" style="opacity: 1; transform: translateY(0px); transition: 0.4s ease-out;"><span class="text-text-muted">[09:42:04]</span> <span class="text-tertiary">INFO</span> Loading Genomic Reference Model (SARS-CoV-2)...</div>
<div class="flex gap-4 mb-2" style="opacity: 1; transform: translateY(0px); transition: 0.4s ease-out;"><span class="text-text-muted">[09:42:08]</span> <span class="text-primary-container">EXEC</span> Aligning FASTA sequences to hg38 reference...</div>
<div class="flex gap-4 mb-2" style="opacity: 1; transform: translateY(0px); transition: 0.4s ease-out;"><span class="text-text-muted">[09:42:15]</span> <span class="text-warning">WARN</span> Low coverage detected at locus 1420-1455. Re-indexing...</div>
<div class="flex gap-4" style="opacity: 1; transform: translateY(0px); transition: 0.4s ease-out;"><span class="text-text-muted">[09:42:22]</span> <span class="text-success">DONE</span> Analysis Complete. Found 12 high-confidence variants.</div>
<div class="animate-pulse inline-block w-2 h-4 bg-primary ml-1 align-middle" style="opacity: 1; transform: translateY(0px); transition: 0.4s ease-out;"></div>
</div>
</div>
</section>
<!-- Stats Section -->

<!-- Workflows Section -->
<section class="py-24 px-gutter">
<div class="max-w-container-max mx-auto">
<div class="mb-16">
<h2 class="font-headline-lg text-headline-lg text-text-primary mb-4">Supported Workflows / PIPELINES</h2>
<p class="font-body-base text-body-base text-text-muted max-w-xl">Standardized pipelines for rapid genomic processing. Engineered for high-throughput laboratory environments.</p>
</div>
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<!-- FASTA -->
<div class="workflow-card p-card-padding rounded-xl flex flex-col h-full">
<div class="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center text-primary mb-6">
<span class="material-symbols-outlined" data-icon="dna">dns</span>
</div>
<h3 class="font-headline-md text-headline-md text-text-primary mb-3">FASTA Analysis</h3>
<p class="font-body-base text-body-base text-text-muted mb-8 flex-grow">Primary sequence alignment and homology modeling. Identify conserved domains and functional motifs with sub-millisecond latency.</p>
<div class="flex items-center gap-2 text-primary font-subheading text-subheading">
<span class="">Launch Pipeline</span>
<span class="material-symbols-outlined" data-icon="arrow_outward">arrow_outward</span>
</div>
</div>
<!-- FASTQ -->
<div class="workflow-card p-card-padding rounded-xl flex flex-col h-full">
<div class="w-12 h-12 rounded-lg bg-tertiary/10 flex items-center justify-center text-tertiary mb-6">
<span class="material-symbols-outlined" data-icon="analytics">analytics</span>
</div>
<h3 class="font-headline-md text-headline-md text-text-primary mb-3">FASTQ Processing</h3>
<p class="font-body-base text-body-base text-text-muted mb-8 flex-grow">Raw read quality control, trimming, and de novo assembly. Built-in error correction for Illumina and Oxford Nanopore platforms.</p>
<div class="flex items-center gap-2 text-tertiary font-subheading text-subheading">
<span class="">Launch Pipeline</span>
<span class="material-symbols-outlined" data-icon="arrow_outward">arrow_outward</span>
</div>
</div>
<!-- DEG -->
<div class="workflow-card p-card-padding rounded-xl flex flex-col h-full">
<div class="w-12 h-12 rounded-lg bg-secondary/10 flex items-center justify-center text-secondary mb-6">
<span class="material-symbols-outlined" data-icon="stacked_line_chart">stacked_line_chart</span>
</div>
<h3 class="font-headline-md text-headline-md text-text-primary mb-3">DEG Profiling&nbsp;</h3>
<p class="font-body-base text-body-base text-text-muted mb-8 flex-grow">Differential Gene Expression analysis with integrated volcano plots and GO enrichment. Identify critical pathways automatically.</p>
<div class="flex items-center gap-2 text-secondary font-subheading text-subheading">
<span class="">Launch Pipeline</span>
<span class="material-symbols-outlined" data-icon="arrow_outward">arrow_outward</span>
</div>
</div>
</div>
</div>
</section>
<!-- CTA / Footer -->
<section class="py-24 px-gutter bg-surface-container-low border-t border-outline-variant relative overflow-hidden">
<div class="absolute inset-0 opacity-10 pointer-events-none" style="background-image: radial-gradient(#adc6ff 1px, transparent 1px); background-size: 24px 24px;"></div>
<div class="max-w-container-max mx-auto text-center relative z-10">
<h2 class="font-headline-lg text-4xl font-bold text-text-primary mb-6">Ready to accelerate your research?</h2>

<div class="flex justify-center gap-4">
<button class="bg-primary text-on-primary font-subheading text-subheading px-10 py-4 rounded-lg hover:shadow-[0_0_20px_rgba(173,198,255,0.3)] transition-all">
                        Create Workspace
                    </button>
</div>
<div class="mt-20 pt-12 border-t border-outline-variant flex flex-col md:flex-row justify-between items-center gap-8">
<div class="font-headline-md text-primary font-bold">PathoScope AI</div>
<div class="flex gap-12 font-body-sm text-body-sm text-on-surface-variant">
<a class="hover:text-primary transition-colors" href="#">Documentation</a>
<a class="hover:text-primary transition-colors" href="#">API Reference</a>
<a class="hover:text-primary transition-colors" href="#">Compliance</a>
<a class="hover:text-primary transition-colors" href="#">Contact Support</a>
</div>
<div class="font-body-sm text-body-sm text-on-surface-variant">
                        © 2024 PathoScope Genomic Solutions. All rights reserved.
                    </div>
</div>
</div>
</section>
</main>
<script>
        // Micro-interaction for the terminal typing effect (simplified)
        document.addEventListener('DOMContentLoaded', () => {
            const lines = document.querySelectorAll('.font-code-sm div');
            lines.forEach((line, index) => {
                line.style.opacity = '0';
                line.style.transform = 'translateY(10px)';
                setTimeout(() => {
                    line.style.transition = 'all 0.4s ease-out';
                    line.style.opacity = '1';
                    line.style.transform = 'translateY(0)';
                }, 500 + (index * 400));
            });
        });
    </script>


</body></html>                          



 ## WORKPLACE  


 
  <!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>PathoScope AI - Unified Analysis Workspace</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;family=JetBrains+Mono:wght@400&amp;family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&amp;display=swap" rel="stylesheet"/>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        ::-webkit-scrollbar {
            width: 4px;
            height: 4px;
        }
        ::-webkit-scrollbar-track {
            background: #0c1321;
        }
        ::-webkit-scrollbar-thumb {
            background: #1f2937;
            border-radius: 10px;
        }
        @keyframes pulse-ring {
            0% { transform: scale(.8); opacity: 0.5; }
            100% { transform: scale(1.5); opacity: 0; }
        }
        .pulse-active {
            position: relative;
        }
        .pulse-active::after {
            content: "";
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            background: inherit;
            border-radius: inherit;
            animation: pulse-ring 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
    </style>
<script id="tailwind-config">
        tailwind.config = {
          darkMode: "class",
          theme: {
            extend: {
              "colors": {
                      "on-surface-variant": "#c2c6d6",
                      "on-secondary": "#003640",
                      "error-container": "#93000a",
                      "on-tertiary-fixed": "#002113",
                      "surface-container": "#19202e",
                      "on-tertiary-fixed-variant": "#005236",
                      "secondary-fixed": "#acedff",
                      "on-primary": "#002e6a",
                      "bg-panel": "#172033",
                      "tertiary": "#4edea3",
                      "success": "#10B981",
                      "on-primary-fixed": "#001a42",
                      "inverse-on-surface": "#2a3040",
                      "on-error": "#690005",
                      "surface": "#0c1321",
                      "text-primary": "#F9FAFB",
                      "primary-fixed-dim": "#adc6ff",
                      "text-muted": "#9CA3AF",
                      "inverse-surface": "#dce2f6",
                      "on-secondary-fixed-variant": "#004e5c",
                      "secondary": "#4cd7f6",
                      "outline": "#8c909f",
                      "bg-card": "#1F2937",
                      "surface-bright": "#323949",
                      "primary-container": "#4d8eff",
                      "on-tertiary": "#003824",
                      "bg-secondary": "#111827",
                      "surface-container-low": "#151b2a",
                      "on-primary-container": "#00285d",
                      "surface-variant": "#2e3544",
                      "surface-container-high": "#232a39",
                      "secondary-fixed-dim": "#4cd7f6",
                      "tertiary-container": "#00a572",
                      "on-tertiary-container": "#00311f",
                      "on-surface": "#dce2f6",
                      "background": "#0c1321",
                      "on-secondary-fixed": "#001f26",
                      "surface-dim": "#0c1321",
                      "warning": "#F59E0B",
                      "text-secondary": "#D1D5DB",
                      "outline-variant": "#424754",
                      "tertiary-fixed-dim": "#4edea3",
                      "on-secondary-container": "#00424e",
                      "on-primary-fixed-variant": "#004395",
                      "primary": "#adc6ff",
                      "error": "#EF4444",
                      "tertiary-fixed": "#6ffbbe",
                      "surface-container-highest": "#2e3544",
                      "surface-container-lowest": "#070e1c",
                      "on-background": "#dce2f6",
                      "on-error-container": "#ffdad6",
                      "inverse-primary": "#005ac2",
                      "primary-fixed": "#d8e2ff",
                      "surface-tint": "#adc6ff",
                      "secondary-container": "#03b5d3"
              },
              "borderRadius": {
                      "DEFAULT": "0.125rem",
                      "lg": "0.25rem",
                      "xl": "0.5rem",
                      "full": "0.75rem"
              },
              "spacing": {
                      "inner-padding": "1rem",
                      "gutter": "1.5rem",
                      "container-max": "1280px",
                      "panel-gap": "1rem",
                      "card-padding": "1.5rem"
              },
              "fontFamily": {
                      "body-sm": ["Inter"],
                      "badge": ["Inter"],
                      "body-base": ["Inter"],
                      "subheading": ["Inter"],
                      "code-xs": ["JetBrains Mono"],
                      "headline-md": ["Inter"],
                      "headline-lg": ["Inter"],
                      "code-sm": ["JetBrains Mono"]
              },
              "fontSize": {
                      "body-sm": ["12px", {"lineHeight": "16px", "fontWeight": "400"}],
                      "badge": ["10px", {"lineHeight": "12px", "letterSpacing": "0.05em", "fontWeight": "700"}],
                      "body-base": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                      "subheading": ["14px", {"lineHeight": "20px", "fontWeight": "600"}],
                      "code-xs": ["10px", {"lineHeight": "14px", "fontWeight": "400"}],
                      "headline-md": ["18px", {"lineHeight": "24px", "fontWeight": "600"}],
                      "headline-lg": ["24px", {"lineHeight": "32px", "fontWeight": "700"}],
                      "code-sm": ["12px", {"lineHeight": "18px", "fontWeight": "400"}]
              }
            },
          },
        }
    </script>
</head>
<body class="bg-background text-on-background font-body-base overflow-hidden selection:bg-primary/30">
<!-- TopNavBar -->
<header class="bg-surface text-primary font-body-base flex justify-between items-center px-gutter w-full h-16 border-b border-outline-variant fixed top-0 z-50">
<div class="flex items-center gap-8">
<span class="font-headline-md text-headline-md font-bold text-primary">PathoScope AI</span>
<nav class="hidden md:flex items-center gap-6">
<a class="text-primary border-b-2 border-primary pb-1 font-body-base" href="#">Dashboard</a>
<a class="text-on-surface-variant hover:text-primary transition-colors font-body-base" href="#">Workspace</a>
<a class="text-on-surface-variant hover:text-primary transition-colors font-body-base" href="#">Reports</a>
<a class="text-on-surface-variant hover:text-primary transition-colors font-body-base" href="#">Literature Explorer</a>
<a class="text-on-surface-variant hover:text-primary transition-colors font-body-base" href="#">Settings</a>
</nav>
</div>
<div class="flex items-center gap-4">
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary">notifications</button>
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary">help</button>
<button class="material-symbols-outlined text-primary">account_circle</button>
</div>
</header>
<!-- SideNavBar -->
<aside class="fixed left-0 top-16 bottom-0 w-64 bg-surface-container flex flex-col p-inner-padding border-r border-outline-variant z-40">
<div class="mb-8">
<div class="flex items-center gap-3 mb-2">
<div class="w-8 h-8 rounded bg-primary-container flex items-center justify-center">
<span class="material-symbols-outlined text-on-primary-container" style="font-size: 20px;">biotech</span>
</div>
<div>
<h3 class="font-subheading text-subheading font-semibold text-on-surface">Genomic Workspace</h3>
<p class="text-[10px] text-on-surface-variant tracking-wider uppercase">v2.4.0-stable</p>
</div>
</div>
<button class="w-full mt-4 bg-primary text-on-primary py-2 px-4 rounded-lg font-subheading text-subheading hover:opacity-90 transition-all flex items-center justify-center gap-2">
<span class="material-symbols-outlined" style="font-size: 18px;">add</span>
                New Pipeline
            </button>
</div>
<nav class="flex-1 flex flex-col gap-1">
<a class="flex items-center gap-3 px-3 py-2 bg-primary-container text-on-primary-container rounded-lg font-body-sm text-body-sm" href="#">
<span class="material-symbols-outlined">cloud_upload</span> Uploads
            </a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg font-body-sm text-body-sm transition-all" href="#">
<span class="material-symbols-outlined">settings_input_component</span> Active Jobs
            </a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg font-body-sm text-body-sm transition-all" href="#">
<span class="material-symbols-outlined">inventory_2</span> Archive
            </a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg font-body-sm text-body-sm transition-all" href="#">
<span class="material-symbols-outlined">key</span> API Keys
            </a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg font-body-sm text-body-sm transition-all" href="#">
<span class="material-symbols-outlined">menu_book</span> Documentation
            </a>
</nav>
<div class="mt-auto pt-4 border-t border-outline-variant flex flex-col gap-1">
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg font-body-sm text-body-sm" href="#">
<span class="material-symbols-outlined">dns</span> System Status
            </a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg font-body-sm text-body-sm" href="#">
<span class="material-symbols-outlined">logout</span> Logout
            </a>
</div>
</aside>
<!-- Main Workspace -->
<main class="ml-64 mt-16 h-[calc(100vh-64px)] grid grid-cols-12 overflow-hidden">
<!-- Left Panel: Upload Center -->
<section class="col-span-3 bg-surface-container-low p-inner-padding flex flex-col gap-panel border-r border-outline-variant overflow-y-auto">
<div class="flex justify-between items-center">
<h2 class="font-subheading text-subheading text-on-surface">Upload Center</h2>
<span class="bg-success/10 text-success font-badge text-badge px-2 py-0.5 rounded border border-success/20">FILE DETECTED</span>
</div>
<div class="flex-1 flex flex-col items-center justify-center border-2 border-dashed border-outline-variant rounded-xl p-8 text-center bg-surface-container-lowest/50 hover:border-primary transition-colors cursor-pointer group">
<div class="w-16 h-16 rounded-full bg-surface-variant flex items-center justify-center mb-4 group-hover:bg-primary-container transition-colors">
<span class="material-symbols-outlined text-primary group-hover:text-on-primary-container" style="font-size: 32px;">upload_file</span>
</div>
<p class="font-subheading text-on-surface mb-1">metagenome_sample_049.fasta</p>
<p class="font-body-sm text-on-surface-variant">142.5 MB • Ready for analysis</p>
</div>
<div class="bg-bg-card rounded-lg p-card-padding border border-outline-variant">
<h4 class="font-subheading text-on-surface mb-3 flex items-center gap-2">
<span class="material-symbols-outlined text-primary" style="font-size: 16px;">tune</span>
                    Parameters
                </h4>
<div class="space-y-4">
<div>
<label class="block font-badge text-badge text-on-surface-variant uppercase mb-1">Sequencing Tech</label>
<select class="w-full bg-surface-container-high border-none text-on-surface text-body-sm rounded p-2 focus:ring-1 focus:ring-primary">
<option>Illumina HiSeq</option>
<option>Oxford Nanopore</option>
<option>PacBio HiFi</option>
</select>
</div>
<div class="flex items-center justify-between">
<span class="font-body-sm text-on-surface-variant">E-value Cutoff</span>
<span class="font-code-sm text-on-surface">1e-5</span>
</div>
<div class="h-1 bg-surface-variant rounded-full overflow-hidden">
<div class="h-full bg-primary w-2/3"></div>
</div>
</div>
</div>
</section>
<!-- Center Panel: Pipeline Runner -->
<section class="col-span-4 bg-background flex flex-col overflow-hidden border-r border-outline-variant">
<div class="p-inner-padding border-b border-outline-variant flex justify-between items-center bg-surface-container-low">
<h2 class="font-subheading text-subheading text-on-surface">Live Pipeline Runner</h2>
<div class="flex items-center gap-2">
<span class="w-2 h-2 rounded-full bg-primary pulse-active"></span>
<span class="font-badge text-badge text-primary uppercase">Processing</span>
</div>
</div>
<!-- Pipeline Stepper -->
<div class="flex-1 overflow-y-auto p-inner-padding">
<div class="space-y-0 relative">
<!-- Vertical Line Connector -->
<div class="absolute left-4 top-4 bottom-4 w-px bg-outline-variant"></div>
<!-- Steps -->
<div class="relative flex items-start gap-4 mb-6">
<div class="z-10 w-8 h-8 rounded-full bg-success text-on-primary flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[18px]">check</span>
</div>
<div class="pt-1 flex-1">
<h4 class="font-subheading text-on-surface">Input Validation</h4>
<p class="font-body-sm text-on-surface-variant">FASTA headers verified. No malformed characters.</p>
</div>
</div>
<div class="relative flex items-start gap-4 mb-6">
<div class="z-10 w-8 h-8 rounded-full bg-success text-on-primary flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[18px]">check</span>
</div>
<div class="pt-1 flex-1">
<h4 class="font-subheading text-on-surface">Sequence QC</h4>
<p class="font-body-sm text-on-surface-variant">Filtering low complexity regions. Q30 &gt; 98.4%.</p>
</div>
</div>
<div class="relative flex items-start gap-4 mb-6">
<div class="z-10 w-8 h-8 rounded-full bg-success text-on-primary flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[18px]">check</span>
</div>
<div class="pt-1 flex-1">
<h4 class="font-subheading text-on-surface">ORF Prediction</h4>
<p class="font-body-sm text-on-surface-variant">Prodigal identified 4,281 candidate ORFs.</p>
</div>
</div>
<div class="relative flex items-start gap-4 mb-6">
<div class="z-10 w-8 h-8 rounded-full bg-success text-on-primary flex items-center justify-center shrink-0">
<span class="material-symbols-outlined text-[18px]">check</span>
</div>
<div class="pt-1 flex-1">
<h4 class="font-subheading text-on-surface">Translation</h4>
<p class="font-body-sm text-on-surface-variant">Standard genetic code applied to ORF sequences.</p>
</div>
</div>
<div class="relative flex items-start gap-4 mb-6">
<div class="z-10 w-8 h-8 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center shrink-0 pulse-active">
<span class="material-symbols-outlined text-[18px] animate-spin">refresh</span>
</div>
<div class="pt-1 flex-1">
<h4 class="font-subheading text-primary">DIAMOND Annotation</h4>
<p class="font-body-sm text-primary">Matching against NR database... (68% complete)</p>
</div>
</div>
<!-- Pending Steps -->
<div class="relative flex items-start gap-4 mb-6 opacity-40">
<div class="z-10 w-8 h-8 rounded-full bg-surface-variant text-on-surface-variant flex items-center justify-center shrink-0">
<div class="w-1.5 h-1.5 rounded-full bg-on-surface-variant"></div>
</div>
<div class="pt-1 flex-1">
<h4 class="font-subheading">Pfam Domains</h4>
</div>
</div>
<div class="relative flex items-start gap-4 mb-6 opacity-40">
<div class="z-10 w-8 h-8 rounded-full bg-surface-variant text-on-surface-variant flex items-center justify-center shrink-0">
<div class="w-1.5 h-1.5 rounded-full bg-on-surface-variant"></div>
</div>
<div class="pt-1 flex-1">
<h4 class="font-subheading">KEGG Pathways</h4>
</div>
</div>
<div class="relative flex items-start gap-4 mb-6 opacity-40">
<div class="z-10 w-8 h-8 rounded-full bg-surface-variant text-on-surface-variant flex items-center justify-center shrink-0">
<div class="w-1.5 h-1.5 rounded-full bg-on-surface-variant"></div>
</div>
<div class="pt-1 flex-1">
<h4 class="font-subheading">Taxonomy Profile</h4>
</div>
</div>
</div>
</div>
<!-- Live Console Terminal -->
<div class="h-1/3 bg-surface-container-lowest border-t border-outline-variant flex flex-col">
<div class="px-4 py-2 border-b border-outline-variant flex items-center gap-2">
<span class="material-symbols-outlined text-on-surface-variant" style="font-size: 14px;">terminal</span>
<span class="font-code-xs text-code-xs text-on-surface-variant uppercase">Scientific Logs</span>
</div>
<div class="flex-1 p-4 font-code-sm text-code-sm overflow-y-auto space-y-1">
<p class="text-text-muted">[2023-10-27 14:02:11] <span class="text-success">INFO</span>: Prodigal v2.6.3 started.</p>
<p class="text-text-muted">[2023-10-27 14:02:45] <span class="text-success">INFO</span>: Prediction complete. Found 4281 ORFs.</p>
<p class="text-text-muted">[2023-10-27 14:02:46] <span class="text-success">INFO</span>: Starting DIAMOND v2.0.15 annotation.</p>
<p class="text-text-muted">[2023-10-27 14:03:02] <span class="text-text-primary">RUN</span>: Querying 1024/4281 sequences against NR_v2023...</p>
<p class="text-text-muted">[2023-10-27 14:03:15] <span class="text-text-primary">RUN</span>: Block 2/4 processing. Current E-value mean: 1.4e-12.</p>
<div class="flex items-center gap-2">
<span class="text-primary animate-pulse">&gt;</span>
<span class="text-primary">_</span>
</div>
</div>
</div>
</section>
<!-- Right Panel: Results Viewer -->
<section class="col-span-5 bg-surface-container-low flex flex-col overflow-hidden">
<!-- Result Tabs -->
<div class="flex items-center border-b border-outline-variant overflow-x-auto bg-surface-container-low scrollbar-hide">
<button class="px-6 py-4 border-b-2 border-primary text-primary font-subheading text-subheading shrink-0">Overview</button>
<button class="px-6 py-4 text-on-surface-variant hover:text-on-surface font-subheading text-subheading shrink-0">QC</button>
<button class="px-6 py-4 text-on-surface-variant hover:text-on-surface font-subheading text-subheading shrink-0">ORFs</button>
<button class="px-6 py-4 text-on-surface-variant hover:text-on-surface font-subheading text-subheading shrink-0">Homology</button>
<button class="px-6 py-4 text-on-surface-variant hover:text-on-surface font-subheading text-subheading shrink-0">Taxonomy</button>
<button class="px-6 py-4 border-b-2 border-transparent text-primary font-subheading text-subheading shrink-0 flex items-center gap-2">
                    PubMed
                    <span class="bg-primary/20 text-primary text-[10px] px-1.5 rounded-full">12</span>
</button>
<button class="px-6 py-4 text-on-surface-variant hover:text-on-surface font-subheading text-subheading shrink-0">AI Interpretation</button>
</div>
<!-- Scrollable Content Area -->
<div class="flex-1 overflow-y-auto p-inner-padding space-y-6">
<!-- Grounded AI Analysis -->
<div class="bg-bg-panel border border-primary/20 rounded-xl overflow-hidden shadow-xl shadow-black/20">
<div class="p-card-padding bg-primary/5 border-b border-primary/10 flex justify-between items-center">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-primary" style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
<h3 class="font-headline-md text-headline-md text-primary">Grounded AI Analysis</h3>
</div>
<div class="flex items-center gap-2 bg-success/20 text-success px-3 py-1 rounded-full border border-success/30">
<span class="material-symbols-outlined text-[14px]">verified</span>
<span class="font-badge text-badge">CONFIDENCE: HIGH</span>
</div>
</div>
<div class="p-card-padding space-y-4">
<p class="text-on-surface leading-relaxed">
                            Preliminary analysis suggests the presence of <strong class="text-primary">Bacillus anthracis</strong> signature markers in the metagenomic sample. Specifically, ORF_3921 shows 99.8% homology with the <em class="italic">pagA</em> gene (Protective Antigen) located on the pXO1 plasmid.
                        </p>
<div class="grid grid-cols-3 gap-4">
<div class="bg-surface-variant p-3 rounded border border-outline-variant">
<span class="block font-badge text-badge text-on-surface-variant uppercase mb-1">Key Virulence Factor</span>
<span class="font-subheading text-on-surface">pagA, lef, cya</span>
</div>
<div class="bg-surface-variant p-3 rounded border border-outline-variant">
<span class="block font-badge text-badge text-on-surface-variant uppercase mb-1">Pathogen Index</span>
<span class="font-subheading text-error">Critical (9.2)</span>
</div>
<div class="bg-surface-variant p-3 rounded border border-outline-variant">
<span class="block font-badge text-badge text-on-surface-variant uppercase mb-1">Antibiotic Resistance</span>
<span class="font-subheading text-warning">blaZ (detected)</span>
</div>
</div>
</div>
</div>
<!-- PubMed Cards -->
<div class="space-y-4">
<h3 class="font-subheading text-on-surface flex items-center gap-2">
<span class="material-symbols-outlined text-primary">library_books</span>
                        Relevant Literature (Top Matches)
                    </h3>
<div class="bg-bg-card border border-outline-variant rounded-lg p-card-padding hover:border-primary transition-colors cursor-pointer group">
<div class="flex justify-between items-start mb-2">
<span class="font-code-sm text-code-sm text-primary group-hover:underline">PMID: 34829105</span>
<span class="text-on-surface-variant text-[11px]">2021 • Nature Microbiology</span>
</div>
<h4 class="font-subheading text-on-surface group-hover:text-primary transition-colors mb-2 leading-tight">
                            Genomic Characterization of Highly Virulent Bacillus anthracis Strains in Arid Climates.
                        </h4>
<p class="font-body-sm text-on-surface-variant line-clamp-2">
                            This study investigates the molecular evolution of pXO1 and pXO2 plasmids across diverse environmental isolates...
                        </p>
</div>
<div class="bg-bg-card border border-outline-variant rounded-lg p-card-padding hover:border-primary transition-colors cursor-pointer group">
<div class="flex justify-between items-start mb-2">
<span class="font-code-sm text-code-sm text-primary group-hover:underline">PMID: 29118320</span>
<span class="text-on-surface-variant text-[11px]">2018 • Science Immunology</span>
</div>
<h4 class="font-subheading text-on-surface group-hover:text-primary transition-colors mb-2 leading-tight">
                            Molecular Mechanism of pagA-mediated Cell Entry and Toxin Translocation.
                        </h4>
<p class="font-body-sm text-on-surface-variant line-clamp-2">
                            Using cryo-EM, researchers mapped the heptameric prepore structure of the protective antigen...
                        </p>
</div>
</div>
<!-- Data Visualization Placeholder -->
<div class="bg-bg-panel rounded-xl border border-outline-variant p-card-padding">
<div class="flex justify-between items-center mb-4">
<h4 class="font-subheading text-on-surface">Taxonomy Distribution</h4>
<button class="material-symbols-outlined text-on-surface-variant">fullscreen</button>
</div>
<div class="relative h-48 w-full bg-surface-container-lowest rounded overflow-hidden flex items-center justify-center border border-outline-variant">
<!-- Simulated Chart -->
<div class="flex items-end gap-2 h-32">
<div class="w-8 bg-primary rounded-t" style="height: 90%;"></div>
<div class="w-8 bg-secondary rounded-t" style="height: 60%;"></div>
<div class="w-8 bg-tertiary rounded-t" style="height: 40%;"></div>
<div class="w-8 bg-primary/40 rounded-t" style="height: 25%;"></div>
<div class="w-8 bg-primary/20 rounded-t" style="height: 15%;"></div>
</div>
</div>
</div>
</div>
<!-- Footer Actions -->
<div class="p-inner-padding border-t border-outline-variant bg-surface-container flex justify-between items-center">
<div class="flex items-center gap-4">
<button class="flex items-center gap-2 px-3 py-1.5 bg-surface-variant rounded border border-outline-variant text-on-surface hover:bg-surface-bright transition-all">
<span class="material-symbols-outlined" style="font-size: 18px;">download</span>
<span class="font-body-sm">Export JSON</span>
</button>
<button class="flex items-center gap-2 px-3 py-1.5 bg-surface-variant rounded border border-outline-variant text-on-surface hover:bg-surface-bright transition-all">
<span class="material-symbols-outlined" style="font-size: 18px;">description</span>
<span class="font-body-sm">PDF Summary</span>
</button>
</div>
<div class="text-on-surface-variant font-code-xs text-code-xs">
                    SERVER: node-us-east-412 • LATENCY: 24ms
                </div>
</div>
</section>
</main>
<!-- Contextual FAB (Hidden as per requirement for Workspace Detail) -->
<!-- Determined suppression based on "Task-Focused" UI -->
<script>
        // Micro-interaction for the Terminal logs
        const logContainer = document.querySelector('.overflow-y-auto.font-code-sm');
        const logs = [
            "INFO: DIAMOND query block 3 started.",
            "WARN: ORF_1204 has low complexity region at [14..45].",
            "INFO: Alignment hit found in B. anthracis AMES str.",
            "INFO: Confidence score updated for sequence group 09.",
            "RUN: KEGG pathway mapper initializing..."
        ];
        
        let logIndex = 0;
        setInterval(() => {
            if (logIndex < logs.length) {
                const p = document.createElement('p');
                p.className = 'text-text-muted';
                const time = new Date().toLocaleTimeString('en-GB', { hour12: false });
                p.innerHTML = `<span class="text-text-muted">[2023-10-27 ${time}]</span> <span class="text-success">INFO</span>: ${logs[logIndex]}`;
                logContainer.insertBefore(p, logContainer.lastElementChild);
                logIndex++;
                logContainer.scrollTop = logContainer.scrollHeight;
            }
        }, 4000);
    </script>
</body></html>              




##      PAGE 2



 <!DOCTYPE html>

<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>PathoScope AI - Genomic Dashboard</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;family=JetBrains+Mono:wght@400&amp;family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&amp;display=swap" rel="stylesheet"/>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0c1321;
        }
        ::-webkit-scrollbar-thumb {
            background: #1F2937;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #2e3544;
        }
        .bento-grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 1.5rem;
        }
    </style>
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "on-surface-variant": "#c2c6d6",
                        "on-secondary": "#003640",
                        "error-container": "#93000a",
                        "on-tertiary-fixed": "#002113",
                        "surface-container": "#19202e",
                        "on-tertiary-fixed-variant": "#005236",
                        "secondary-fixed": "#acedff",
                        "on-primary": "#002e6a",
                        "bg-panel": "#172033",
                        "tertiary": "#4edea3",
                        "success": "#10B981",
                        "on-primary-fixed": "#001a42",
                        "inverse-on-surface": "#2a3040",
                        "on-error": "#690005",
                        "surface": "#0c1321",
                        "text-primary": "#F9FAFB",
                        "primary-fixed-dim": "#adc6ff",
                        "text-muted": "#9CA3AF",
                        "inverse-surface": "#dce2f6",
                        "on-secondary-fixed-variant": "#004e5c",
                        "secondary": "#4cd7f6",
                        "outline": "#8c909f",
                        "bg-card": "#1F2937",
                        "surface-bright": "#323949",
                        "primary-container": "#4d8eff",
                        "on-tertiary": "#003824",
                        "bg-secondary": "#111827",
                        "surface-container-low": "#151b2a",
                        "on-primary-container": "#00285d",
                        "surface-variant": "#2e3544",
                        "surface-container-high": "#232a39",
                        "secondary-fixed-dim": "#4cd7f6",
                        "tertiary-container": "#00a572",
                        "on-tertiary-container": "#00311f",
                        "on-surface": "#dce2f6",
                        "background": "#0c1321",
                        "on-secondary-fixed": "#001f26",
                        "surface-dim": "#0c1321",
                        "warning": "#F59E0B",
                        "text-secondary": "#D1D5DB",
                        "outline-variant": "#424754",
                        "tertiary-fixed-dim": "#4edea3",
                        "on-secondary-container": "#00424e",
                        "on-primary-fixed-variant": "#004395",
                        "primary": "#adc6ff",
                        "error": "#EF4444",
                        "tertiary-fixed": "#6ffbbe",
                        "surface-container-highest": "#2e3544",
                        "surface-container-lowest": "#070e1c",
                        "on-background": "#dce2f6",
                        "on-error-container": "#ffdad6",
                        "inverse-primary": "#005ac2",
                        "primary-fixed": "#d8e2ff",
                        "surface-tint": "#adc6ff",
                        "secondary-container": "#03b5d3"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    "spacing": {
                        "inner-padding": "1rem",
                        "gutter": "1.5rem",
                        "container-max": "1280px",
                        "panel-gap": "1rem",
                        "card-padding": "1.5rem"
                    },
                    "fontFamily": {
                        "body-sm": ["Inter"],
                        "badge": ["Inter"],
                        "body-base": ["Inter"],
                        "subheading": ["Inter"],
                        "code-xs": ["JetBrains Mono"],
                        "headline-md": ["Inter"],
                        "headline-lg": ["Inter"],
                        "code-sm": ["JetBrains Mono"]
                    },
                    "fontSize": {
                        "body-sm": ["12px", {"lineHeight": "16px", "fontWeight": "400"}],
                        "badge": ["10px", {"lineHeight": "12px", "letterSpacing": "0.05em", "fontWeight": "700"}],
                        "body-base": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                        "subheading": ["14px", {"lineHeight": "20px", "fontWeight": "600"}],
                        "code-xs": ["10px", {"lineHeight": "14px", "fontWeight": "400"}],
                        "headline-md": ["18px", {"lineHeight": "24px", "fontWeight": "600"}],
                        "headline-lg": ["24px", {"lineHeight": "32px", "fontWeight": "700"}],
                        "code-sm": ["12px", {"lineHeight": "18px", "fontWeight": "400"}]
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-background text-on-background font-body-base antialiased">
<!-- TopNavBar -->
<header class="bg-surface text-primary font-body-base docked full-width top-0 border-b border-outline-variant flex justify-between items-center px-gutter w-full h-16 fixed z-50">
<div class="flex items-center gap-8">
<span class="font-headline-md text-headline-md font-bold text-primary">PathoScope AI</span>
<nav class="hidden md:flex gap-6">
<a class="font-body-base text-body-base text-primary border-b-2 border-primary pb-1 transition-colors" href="#">Dashboard</a>
<a class="font-body-base text-body-base text-on-surface-variant hover:text-primary transition-colors" href="#">Workspace</a>
<a class="font-body-base text-body-base text-on-surface-variant hover:text-primary transition-colors" href="#">Reports</a>
<a class="font-body-base text-body-base text-on-surface-variant hover:text-primary transition-colors" href="#">Literature Explorer</a>
<a class="font-body-base text-body-base text-on-surface-variant hover:text-primary transition-colors" href="#">Settings</a>
</nav>
</div>
<div class="flex items-center gap-4">
<button class="p-2 hover:text-primary transition-colors opacity-80 active:opacity-100">
<span class="material-symbols-outlined">notifications</span>
</button>
<button class="p-2 hover:text-primary transition-colors opacity-80 active:opacity-100">
<span class="material-symbols-outlined">help</span>
</button>
<button class="p-2 hover:text-primary transition-colors opacity-80 active:opacity-100">
<span class="material-symbols-outlined">account_circle</span>
</button>
</div>
</header>
<!-- SideNavBar -->
<aside class="fixed left-0 top-16 bottom-0 flex flex-col p-inner-padding bg-surface-container text-primary font-body-sm docked left-0 h-full w-64 border-r border-outline-variant z-40">
<div class="flex items-center gap-3 mb-8 px-2">
<div class="w-8 h-8 rounded bg-primary flex items-center justify-center">
<span class="material-symbols-outlined text-on-primary">science</span>
</div>
<div>
<p class="font-subheading text-subheading font-semibold text-on-surface">Genomic Workspace</p>
<p class="text-[10px] opacity-60">v2.4.0-stable</p>
</div>
</div>
<button class="mb-6 w-full bg-primary text-on-primary font-subheading py-2 px-4 rounded transition-all duration-200 ease-in-out hover:opacity-90 flex items-center justify-center gap-2">
<span class="material-symbols-outlined">add</span>
            New Pipeline
        </button>
<nav class="flex-1 space-y-1">
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all duration-200" href="#">
<span class="material-symbols-outlined">cloud_upload</span>
                Uploads
            </a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all duration-200" href="#">
<span class="material-symbols-outlined">settings_input_component</span>
                Active Jobs
            </a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all duration-200" href="#">
<span class="material-symbols-outlined">inventory_2</span>
                Archive
            </a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all duration-200" href="#">
<span class="material-symbols-outlined">key</span>
                API Keys
            </a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all duration-200" href="#">
<span class="material-symbols-outlined">menu_book</span>
                Documentation
            </a>
</nav>
<div class="pt-4 border-t border-outline-variant space-y-1">
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all duration-200" href="#">
<span class="material-symbols-outlined">dns</span>
                System Status
            </a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all duration-200" href="#">
<span class="material-symbols-outlined">logout</span>
                Logout
            </a>
</div>
</aside>
<!-- Main Content -->
<main class="ml-64 mt-16 p-gutter min-h-screen">
<div class="max-w-container-max mx-auto space-y-gutter">
<!-- Page Header -->
<div class="flex justify-between items-end">
<div>
<h1 class="font-headline-lg text-headline-lg text-text-primary">Researcher Dashboard</h1>
<p class="text-text-muted mt-1">Real-time surveillance of genomic pipeline execution and infrastructure health.</p>
</div>
<div class="text-right">
<p class="text-code-xs font-code-xs text-text-muted">LAST SYNC</p>
<p class="font-code-sm text-code-sm text-tertiary">2023-11-24 14:32:01 UTC</p>
</div>
</div>
<!-- KPI Cards -->
<div class="grid grid-cols-1 md:grid-cols-4 gap-panel-gap">
<div class="bg-bg-card border border-outline-variant p-card-padding rounded-lg">
<div class="flex justify-between items-start">
<span class="text-text-muted font-subheading text-subheading">Total Analyses</span>
<span class="material-symbols-outlined text-primary">analytics</span>
</div>
<p class="text-[32px] font-bold text-text-primary mt-2">14,208</p>
<div class="flex items-center gap-1 mt-2">
<span class="material-symbols-outlined text-success text-sm">trending_up</span>
<span class="text-success text-badge font-badge">+12.5% this month</span>
</div>
</div>
<div class="bg-bg-card border border-outline-variant p-card-padding rounded-lg relative overflow-hidden">
<div class="absolute top-0 left-0 w-1 h-full bg-secondary"></div>
<div class="flex justify-between items-start">
<span class="text-text-muted font-subheading text-subheading">Running Jobs</span>
<span class="material-symbols-outlined text-secondary animate-pulse">sync</span>
</div>
<p class="text-[32px] font-bold text-text-primary mt-2">24</p>
<p class="text-text-muted text-badge font-badge mt-2">12 Queued in Buffer</p>
</div>
<div class="bg-bg-card border border-outline-variant p-card-padding rounded-lg">
<div class="flex justify-between items-start">
<span class="text-text-muted font-subheading text-subheading">Completed Jobs</span>
<span class="material-symbols-outlined text-success">check_circle</span>
</div>
<p class="text-[32px] font-bold text-text-primary mt-2">13,942</p>
<p class="text-text-muted text-badge font-badge mt-2">98.2% Success Rate</p>
</div>
<div class="bg-bg-card border border-outline-variant p-card-padding rounded-lg">
<div class="flex justify-between items-start">
<span class="text-text-muted font-subheading text-subheading">Failed Jobs</span>
<span class="material-symbols-outlined text-error">error</span>
</div>
<p class="text-[32px] font-bold text-text-primary mt-2">242</p>
<div class="flex items-center gap-1 mt-2">
<span class="material-symbols-outlined text-error text-sm">warning</span>
<span class="text-error text-badge font-badge">Check logs for errors</span>
</div>
</div>
</div>
<div class="bento-grid">
<!-- Main Activity Table -->
<div class="col-span-12 lg:col-span-8 bg-bg-card border border-outline-variant rounded-lg overflow-hidden flex flex-col">
<div class="p-card-padding border-b border-outline-variant flex justify-between items-center">
<h2 class="font-subheading text-subheading text-text-primary">Recent Analysis Execution Logs</h2>
<button class="text-primary text-body-sm hover:underline">View All Logs</button>
</div>
<div class="overflow-x-auto">
<table class="w-full text-left border-collapse">
<thead class="bg-surface-container-low text-text-muted font-body-sm">
<tr>
<th class="px-6 py-3 font-semibold border-b border-outline-variant">Job Name</th>
<th class="px-6 py-3 font-semibold border-b border-outline-variant">Workflow Type</th>
<th class="px-6 py-3 font-semibold border-b border-outline-variant">Status</th>
<th class="px-6 py-3 font-semibold border-b border-outline-variant">Progress</th>
<th class="px-6 py-3 font-semibold border-b border-outline-variant">Action</th>
</tr>
</thead>
<tbody class="text-body-base divide-y divide-outline-variant">
<tr class="hover:bg-surface-variant transition-colors group">
<td class="px-6 py-4 font-code-sm text-code-sm text-text-primary">WGS_RUN_A920_PRO</td>
<td class="px-6 py-4">FASTQ Variant Call</td>
<td class="px-6 py-4">
<span class="px-2 py-1 bg-secondary-container/20 text-secondary border border-secondary/30 rounded-full text-badge font-badge">RUNNING</span>
</td>
<td class="px-6 py-4">
<div class="w-full bg-surface-container h-1.5 rounded-full">
<div class="bg-secondary h-1.5 rounded-full" style="width: 65%"></div>
</div>
<span class="text-code-xs font-code-xs text-text-muted mt-1 block">65%</span>
</td>
<td class="px-6 py-4">
<button class="flex items-center gap-1 text-primary hover:text-primary-container transition-colors">
<span class="material-symbols-outlined text-[18px]">search</span>
                                            Inspect
                                        </button>
</td>
</tr>
<tr class="hover:bg-surface-variant transition-colors">
<td class="px-6 py-4 font-code-sm text-code-sm text-text-primary">SARS_SURV_LONDON_2</td>
<td class="px-6 py-4">FASTA Assembly</td>
<td class="px-6 py-4">
<span class="px-2 py-1 bg-success/20 text-success border border-success/30 rounded-full text-badge font-badge">COMPLETED</span>
</td>
<td class="px-6 py-4">
<div class="w-full bg-surface-container h-1.5 rounded-full">
<div class="bg-success h-1.5 rounded-full" style="width: 100%"></div>
</div>
<span class="text-code-xs font-code-xs text-text-muted mt-1 block">100%</span>
</td>
<td class="px-6 py-4">
<button class="flex items-center gap-1 text-primary hover:text-primary-container transition-colors">
<span class="material-symbols-outlined text-[18px]">search</span>
                                            Inspect
                                        </button>
</td>
</tr>
<tr class="hover:bg-surface-variant transition-colors">
<td class="px-6 py-4 font-code-sm text-code-sm text-text-primary">RNA_SEQ_MT_441</td>
<td class="px-6 py-4">DEG Analysis</td>
<td class="px-6 py-4">
<span class="px-2 py-1 bg-error/20 text-error border border-error/30 rounded-full text-badge font-badge">FAILED</span>
</td>
<td class="px-6 py-4">
<div class="w-full bg-surface-container h-1.5 rounded-full">
<div class="bg-error h-1.5 rounded-full" style="width: 12%"></div>
</div>
<span class="text-code-xs font-code-xs text-text-muted mt-1 block">12%</span>
</td>
<td class="px-6 py-4">
<button class="flex items-center gap-1 text-error hover:text-error-container transition-colors">
<span class="material-symbols-outlined text-[18px]">warning</span>
                                            Logs
                                        </button>
</td>
</tr>
<tr class="hover:bg-surface-variant transition-colors">
<td class="px-6 py-4 font-code-sm text-code-sm text-text-primary">ONT_NANO_P3_RUN</td>
<td class="px-6 py-4">Long Read FASTQ</td>
<td class="px-6 py-4">
<span class="px-2 py-1 bg-tertiary/20 text-tertiary border border-tertiary/30 rounded-full text-badge font-badge">QUEUED</span>
</td>
<td class="px-6 py-4">
<div class="w-full bg-surface-container h-1.5 rounded-full">
<div class="bg-outline-variant h-1.5 rounded-full" style="width: 0%"></div>
</div>
<span class="text-code-xs font-code-xs text-text-muted mt-1 block">0%</span>
</td>
<td class="px-6 py-4">
<button class="flex items-center gap-1 text-primary hover:text-primary-container transition-colors">
<span class="material-symbols-outlined text-[18px]">search</span>
                                            Inspect
                                        </button>
</td>
</tr>
</tbody>
</table>
</div>
</div>
<!-- Trends Chart Area -->
<div class="col-span-12 lg:col-span-4 space-y-gutter">
<div class="bg-bg-card border border-outline-variant p-card-padding rounded-lg h-full flex flex-col">
<div class="flex justify-between items-center mb-6">
<h2 class="font-subheading text-subheading text-text-primary">Workflow Usage Trends</h2>
<select class="bg-surface border-none text-badge font-badge text-text-muted rounded py-1 pr-8 focus:ring-1 focus:ring-primary">
<option>Last 7 Days</option>
<option>Last 30 Days</option>
</select>
</div>
<div class="flex-1 flex flex-col justify-end gap-4 min-h-[300px]">
<!-- Mock Chart Bars -->
<div class="flex items-end justify-between h-48 px-2 gap-4">
<div class="flex flex-col items-center flex-1 group">
<div class="w-full bg-primary-container/40 rounded-t-sm relative transition-all group-hover:bg-primary-container/60" style="height: 80%">
<div class="absolute -top-6 left-1/2 -translate-x-1/2 text-code-xs font-code-xs text-primary hidden group-hover:block">1.2k</div>
</div>
<span class="text-code-xs font-code-xs text-text-muted mt-2">FASTA</span>
</div>
<div class="flex flex-col items-center flex-1 group">
<div class="w-full bg-secondary-container/40 rounded-t-sm relative transition-all group-hover:bg-secondary-container/60" style="height: 95%">
<div class="absolute -top-6 left-1/2 -translate-x-1/2 text-code-xs font-code-xs text-secondary hidden group-hover:block">1.8k</div>
</div>
<span class="text-code-xs font-code-xs text-text-muted mt-2">FASTQ</span>
</div>
<div class="flex flex-col items-center flex-1 group">
<div class="w-full bg-tertiary-container/40 rounded-t-sm relative transition-all group-hover:bg-tertiary-container/60" style="height: 45%">
<div class="absolute -top-6 left-1/2 -translate-x-1/2 text-code-xs font-code-xs text-tertiary hidden group-hover:block">640</div>
</div>
<span class="text-code-xs font-code-xs text-text-muted mt-2">DEG</span>
</div>
</div>
<div class="grid grid-cols-1 gap-3 pt-6 border-t border-outline-variant">
<div class="flex items-center justify-between">
<div class="flex items-center gap-2">
<div class="w-2 h-2 rounded-full bg-primary"></div>
<span class="text-body-sm text-text-secondary">Primary Alignment</span>
</div>
<span class="font-code-sm text-code-sm text-text-primary">42%</span>
</div>
<div class="flex items-center justify-between">
<div class="flex items-center gap-2">
<div class="w-2 h-2 rounded-full bg-secondary"></div>
<span class="text-body-sm text-text-secondary">Variant Discovery</span>
</div>
<span class="font-code-sm text-code-sm text-text-primary">38%</span>
</div>
<div class="flex items-center justify-between">
<div class="flex items-center gap-2">
<div class="w-2 h-2 rounded-full bg-tertiary"></div>
<span class="text-body-sm text-text-secondary">Expression Profile</span>
</div>
<span class="font-code-sm text-code-sm text-text-primary">20%</span>
</div>
</div>
</div>
</div>
</div>
</div>
<!-- System Infrastructure Panel -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-panel-gap">
<div class="bg-bg-panel border border-outline-variant p-4 rounded-lg flex items-center gap-4">
<div class="w-10 h-10 bg-surface-container rounded flex items-center justify-center text-secondary">
<span class="material-symbols-outlined">memory</span>
</div>
<div class="flex-1">
<div class="flex justify-between items-center mb-1">
<span class="text-body-sm font-semibold text-text-primary uppercase tracking-wider">Compute Load</span>
<span class="text-code-xs font-code-xs text-secondary">78%</span>
</div>
<div class="w-full bg-surface-container h-1 rounded-full overflow-hidden">
<div class="bg-secondary h-full" style="width: 78%"></div>
</div>
</div>
</div>
<div class="bg-bg-panel border border-outline-variant p-4 rounded-lg flex items-center gap-4">
<div class="w-10 h-10 bg-surface-container rounded flex items-center justify-center text-primary">
<span class="material-symbols-outlined">storage</span>
</div>
<div class="flex-1">
<div class="flex justify-between items-center mb-1">
<span class="text-body-sm font-semibold text-text-primary uppercase tracking-wider">Storage (PETA)</span>
<span class="text-code-xs font-code-xs text-primary">62%</span>
</div>
<div class="w-full bg-surface-container h-1 rounded-full overflow-hidden">
<div class="bg-primary h-full" style="width: 62%"></div>
</div>
</div>
</div>
<div class="bg-bg-panel border border-outline-variant p-4 rounded-lg flex items-center gap-4">
<div class="w-10 h-10 bg-surface-container rounded flex items-center justify-center text-tertiary">
<span class="material-symbols-outlined">public</span>
</div>
<div class="flex-1">
<div class="flex justify-between items-center mb-1">
<span class="text-body-sm font-semibold text-text-primary uppercase tracking-wider">Network IO</span>
<span class="text-code-xs font-code-xs text-tertiary">1.2 GB/s</span>
</div>
<div class="w-full bg-surface-container h-1 rounded-full overflow-hidden">
<div class="bg-tertiary h-full" style="width: 45%"></div>
</div>
</div>
</div>
</div>
</div>
</main>
<!-- Floating Action for Quick Access -->
<div class="fixed bottom-8 right-8 z-50">
<button class="w-14 h-14 bg-primary text-on-primary rounded-full shadow-lg flex items-center justify-center transition-transform hover:scale-110 active:scale-95 group relative">
<span class="material-symbols-outlined text-[28px]">terminal</span>
<div class="absolute right-full mr-4 bg-bg-card border border-outline-variant px-3 py-1.5 rounded whitespace-nowrap text-body-sm text-text-primary opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity">
                Open Lab Console
            </div>
</button>
</div>
<script>
        // Simple micro-interaction for the console button
        const consoleBtn = document.querySelector('button .material-symbols-outlined[textContent="terminal"]')?.parentElement;
        if (consoleBtn) {
            consoleBtn.addEventListener('click', () => {
                console.log('PathoScope CLI initialized...');
                // Trigger a ripple or similar minor effect if needed
            });
        }

        // Simulating live data updates
        setInterval(() => {
            const cpuLoadText = document.querySelector('.text-code-xs.text-secondary');
            const cpuBar = cpuLoadText?.parentElement?.nextElementSibling?.firstElementChild;
            if (cpuLoadText && cpuBar) {
                const newVal = Math.floor(Math.random() * (85 - 70) + 70);
                cpuLoadText.innerText = `${newVal}%`;
                cpuBar.style.width = `${newVal}%`;
            }
        }, 3000);
    </script>
</body></html>   

 ###  PAGE 3
 
 
  <!DOCTYPE html><html class="dark" lang="en" style=""><head>
<meta charset="utf-8">
<meta content="width=device-width, initial-scale=1.0" name="viewport">
<title>PathoScope AI - Reports Center</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&amp;family=JetBrains+Mono:wght@400&amp;display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet">
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "on-surface-variant": "#c2c6d6",
                        "on-secondary": "#003640",
                        "error-container": "#93000a",
                        "on-tertiary-fixed": "#002113",
                        "surface-container": "#19202e",
                        "on-tertiary-fixed-variant": "#005236",
                        "secondary-fixed": "#acedff",
                        "on-primary": "#002e6a",
                        "bg-panel": "#172033",
                        "tertiary": "#4edea3",
                        "success": "#10B981",
                        "on-primary-fixed": "#001a42",
                        "inverse-on-surface": "#2a3040",
                        "on-error": "#690005",
                        "surface": "#0c1321",
                        "text-primary": "#F9FAFB",
                        "primary-fixed-dim": "#adc6ff",
                        "text-muted": "#9CA3AF",
                        "inverse-surface": "#dce2f6",
                        "on-secondary-fixed-variant": "#004e5c",
                        "secondary": "#4cd7f6",
                        "outline": "#8c909f",
                        "bg-card": "#1F2937",
                        "surface-bright": "#323949",
                        "primary-container": "#4d8eff",
                        "on-tertiary": "#003824",
                        "bg-secondary": "#111827",
                        "surface-container-low": "#151b2a",
                        "on-tertiary-container": "#00311f",
                        "on-surface": "#dce2f6",
                        "background": "#0c1321",
                        "on-secondary-fixed": "#001f26",
                        "surface-dim": "#0c1321",
                        "warning": "#F59E0B",
                        "text-secondary": "#D1D5DB",
                        "outline-variant": "#424754",
                        "tertiary-fixed-dim": "#4edea3",
                        "on-secondary-container": "#00424e",
                        "on-primary-fixed-variant": "#004395",
                        "primary": "#adc6ff",
                        "error": "#EF4444",
                        "tertiary-fixed": "#6ffbbe",
                        "surface-container-highest": "#2e3544",
                        "surface-container-lowest": "#070e1c",
                        "on-background": "#dce2f6",
                        "on-error-container": "#ffdad6",
                        "inverse-primary": "#005ac2",
                        "primary-fixed": "#d8e2ff",
                        "surface-tint": "#adc6ff",
                        "secondary-container": "#03b5d3"
                    },
                    "borderRadius": {
                        "DEFAULT": "0.125rem",
                        "lg": "0.25rem",
                        "xl": "0.5rem",
                        "full": "0.75rem"
                    },
                    "spacing": {
                        "inner-padding": "1rem",
                        "gutter": "1.5rem",
                        "container-max": "1280px",
                        "panel-gap": "1rem",
                        "card-padding": "1.5rem"
                    },
                    "fontFamily": {
                        "body-sm": ["Inter"],
                        "badge": ["Inter"],
                        "body-base": ["Inter"],
                        "subheading": ["Inter"],
                        "code-xs": ["JetBrains Mono"],
                        "headline-md": ["Inter"],
                        "headline-lg": ["Inter"],
                        "code-sm": ["JetBrains Mono"]
                    },
                    "fontSize": {
                        "body-sm": ["12px", {"lineHeight": "16px", "fontWeight": "400"}],
                        "badge": ["10px", {"lineHeight": "12px", "letterSpacing": "0.05em", "fontWeight": "700"}],
                        "body-base": ["14px", {"lineHeight": "20px", "fontWeight": "400"}],
                        "subheading": ["14px", {"lineHeight": "20px", "fontWeight": "600"}],
                        "code-xs": ["10px", {"lineHeight": "14px", "fontWeight": "400"}],
                        "headline-md": ["18px", {"lineHeight": "24px", "fontWeight": "600"}],
                        "headline-lg": ["24px", {"lineHeight": "32px", "fontWeight": "700"}],
                        "code-sm": ["12px", {"lineHeight": "18px", "fontWeight": "400"}]
                    }
                },
            },
        }
    </script>
<style>
        .material-symbols-outlined {
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }
        body {
            background-color: #0c1321;
            color: #dce2f6;
            -webkit-font-smoothing: antialiased;
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 4px;
            height: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: #151b2a;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #424754;
            border-radius: 2px;
        }
    </style>
</head>
<body class="font-body-base text-body-base overflow-hidden flex flex-col h-screen">
<!-- TopNavBar -->
<header class="flex justify-between items-center px-gutter w-full h-16 bg-surface dark:bg-surface border-b border-outline-variant fixed top-0 z-50">
<div class="flex items-center gap-8">
<span class="font-headline-md text-headline-md font-bold text-primary">PathoScope AI</span>
<nav class="hidden md:flex gap-6">
<a class="text-on-surface-variant hover:text-primary transition-colors font-body-base text-body-base" href="#">Dashboard</a>
<a class="text-on-surface-variant hover:text-primary transition-colors font-body-base text-body-base" href="#">Workspace</a>
<a class="text-primary border-b-2 border-primary pb-1 font-body-base text-body-base" href="#">Reports</a>
<a class="text-on-surface-variant hover:text-primary transition-colors font-body-base text-body-base" href="#">Literature Explorer</a>
<a class="text-on-surface-variant hover:text-primary transition-colors font-body-base text-body-base" href="#">Settings</a>
</nav>
</div>
<div class="flex items-center gap-4">
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors">notifications</button>
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors">help</button>
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors">account_circle</button>
</div>
</header>
<div class="flex flex-1 pt-16">
<!-- SideNavBar -->
<aside class="fixed left-0 top-16 bottom-0 flex flex-col p-inner-padding bg-surface-container dark:bg-surface-container border-r border-outline-variant w-64 hidden lg:flex">
<div class="mb-8 px-2">
<div class="flex items-center gap-3 mb-1">
<div class="w-8 h-8 bg-primary rounded flex items-center justify-center">
<span class="material-symbols-outlined text-on-primary">science</span>
</div>
<div>
<h2 class="font-subheading text-subheading font-semibold text-on-surface">Genomic Workspace</h2>
<p class="text-[10px] uppercase tracking-wider text-text-muted">v2.4.0-stable</p>
</div>
</div>
</div>

<div class="mb-6 px-2">
    <h3 class="font-badge text-badge text-text-muted uppercase mb-3">Upload Center</h3>
    <p class="text-[10px] text-text-muted mb-2">Acceptable: FASTA, FASTQ, CSV, TSV</p>
    <button class="w-full py-2 bg-primary text-on-primary font-subheading rounded-lg flex items-center justify-center gap-2 hover:opacity-90 transition-all shadow-lg shadow-primary/10">
        <span class="material-symbols-outlined text-[20px]">upload</span>
        New Pipeline
    </button>
</div><nav class="flex-1 space-y-1">
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all" href="#">
<span class="material-symbols-outlined">cloud_upload</span>
<span class="font-body-sm text-body-sm">Uploads</span>
</a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all" href="#">
<span class="material-symbols-outlined">settings_input_component</span>
<span class="font-body-sm text-body-sm">Active Jobs</span>
</a>
<a class="flex items-center gap-3 px-3 py-2 bg-primary-container text-on-primary-container rounded-lg transition-all" href="#">
<span class="material-symbols-outlined" style="font-variation-settings: &quot;FILL&quot; 1;">inventory_2</span>
<span class="font-body-sm text-body-sm">Archive</span>
</a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all" href="#">
<span class="material-symbols-outlined">key</span>
<span class="font-body-sm text-body-sm">API Keys</span>
</a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all" href="#">
<span class="material-symbols-outlined">menu_book</span>
<span class="font-body-sm text-body-sm">Documentation</span>
</a>
</nav>
<div class="mt-auto pt-4 border-t border-outline-variant space-y-1">
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all" href="#">
<span class="material-symbols-outlined">dns</span>
<span class="font-body-sm text-body-sm">System Status</span>
</a>
<a class="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-surface-variant rounded-lg transition-all" href="#">
<span class="material-symbols-outlined">logout</span>
<span class="font-body-sm text-body-sm">Logout</span>
</a>
</div>
</aside>
<!-- Main Content Area -->
<main class="flex-1 ml-0 lg:ml-64 bg-surface-dim p-gutter overflow-y-auto custom-scrollbar">
<!-- Header & Filter Section -->
<div class="max-w-container-max mx-auto space-y-6">
<div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
<div>
<h1 class="font-headline-lg text-headline-lg text-text-primary">Reports Center</h1>
<p class="text-text-muted font-body-base">Review and export detailed genomic analysis outputs.</p>
</div>
<div class="flex items-center gap-2">
<button class="flex items-center gap-2 px-4 py-2 bg-surface-container-high border border-outline-variant rounded-lg text-on-surface-variant hover:bg-surface-variant transition-colors">
<span class="material-symbols-outlined text-[20px]">filter_list</span>
<span class="font-subheading">Filters</span>
</button>
<div class="h-8 w-px bg-outline-variant mx-2"></div>
<div class="flex bg-surface-container-low border border-outline-variant rounded-lg p-1">
<button class="px-3 py-1 bg-primary text-on-primary rounded font-subheading">List</button>
<button class="px-3 py-1 text-on-surface-variant hover:text-on-surface">Grid</button>
</div>
</div>
</div>
<!-- Filters Strip -->
<div class="bg-surface-container p-4 rounded-xl border border-outline-variant flex flex-wrap gap-4 items-end">
<div class="space-y-1.5">
<label class="font-badge text-badge text-text-muted uppercase">Workflow Type</label>
<select class="bg-bg-panel border border-outline-variant text-on-surface rounded-lg px-3 py-2 font-body-sm focus:ring-primary focus:border-primary w-48">
<option>All Workflows</option>
<option>WGS Assembly</option>
<option>Metagenomic Profiling</option>
<option>Variant Calling (GATK)</option>
<option>Phylogenetic Tree</option>
</select>
</div>
<div class="space-y-1.5">
<label class="font-badge text-badge text-text-muted uppercase">Date Range</label>
<div class="flex items-center gap-2">
<input class="bg-bg-panel border border-outline-variant text-on-surface rounded-lg px-3 py-2 font-body-sm focus:ring-primary focus:border-primary" type="date">
<span class="text-text-muted">to</span>
<input class="bg-bg-panel border border-outline-variant text-on-surface rounded-lg px-3 py-2 font-body-sm focus:ring-primary focus:border-primary" type="date">
</div>
</div>
<div class="space-y-1.5">
<label class="font-badge text-badge text-text-muted uppercase">Confidence Level</label>
<div class="flex gap-2">
<button class="px-3 py-2 border border-outline-variant rounded-lg font-body-sm bg-bg-panel text-on-surface-variant hover:border-primary">High</button>
<button class="px-3 py-2 border border-outline-variant rounded-lg font-body-sm bg-bg-panel text-on-surface-variant hover:border-primary">Med</button>
</div>
</div>
<button class="ml-auto px-4 py-2 text-primary font-subheading hover:underline">Clear all filters</button>
</div>
<!-- Reports Table/List -->
<div class="bg-surface-container rounded-xl border border-outline-variant overflow-hidden">
<div class="overflow-x-auto custom-scrollbar">
<table class="w-full text-left border-collapse">
<thead>
<tr class="bg-surface-container-high border-b border-outline-variant">
<th class="px-6 py-4 font-badge text-badge text-text-muted uppercase tracking-wider">Analysis Name / ID</th>
<th class="px-6 py-4 font-badge text-badge text-text-muted uppercase tracking-wider">Workflow</th>
<th class="px-6 py-4 font-badge text-badge text-text-muted uppercase tracking-wider">Completed</th>
<th class="px-6 py-4 font-badge text-badge text-text-muted uppercase tracking-wider">Quality</th>
<th class="px-6 py-4 font-badge text-badge text-text-muted uppercase tracking-wider">Exports</th>
<th class="px-6 py-4"></th>
</tr>
</thead>
<tbody class="divide-y divide-outline-variant">
<!-- Row 1 -->
<tr class="hover:bg-bg-panel transition-colors group">
<td class="px-6 py-5">
<div class="flex flex-col">
<span class="font-subheading text-on-surface">SARS-CoV-2_VUI-202112</span>
<span class="font-code-xs text-text-muted uppercase">JOB-8821-XQ</span>
</div>
</td>
<td class="px-6 py-5">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-secondary text-[18px]">hub</span>
<span class="text-on-surface-variant font-body-base">Viral Genome Analysis</span>
</div>
</td>
<td class="px-6 py-5 text-on-surface-variant font-body-sm">
                                        Oct 24, 2023 · 14:32
                                    </td>
<td class="px-6 py-5">
<span class="px-2 py-0.5 bg-success/10 text-success border border-success/20 rounded font-badge uppercase">High (98.2%)</span>
</td>
<td class="px-6 py-5">
<div class="flex gap-1.5">
<button class="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant font-code-xs" title="HTML">HTML</button>
<button class="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant font-code-xs" title="PDF">PDF</button>
<button class="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant font-code-xs" title="JSON">JS</button>
<button class="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant font-code-xs" title="CSV">CSV</button>
</div>
</td>
<td class="px-6 py-5 text-right">
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary">open_in_new</button>
</td>
</tr>
<!-- Row 2 -->
<tr class="hover:bg-bg-panel transition-colors group">
<td class="px-6 py-5">
<div class="flex flex-col">
<span class="font-subheading text-on-surface">E.coli_K12_Reference_Run</span>
<span class="font-code-xs text-text-muted uppercase">JOB-8790-BK</span>
</div>
</td>
<td class="px-6 py-5">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-tertiary text-[18px]">biotech</span>
<span class="text-on-surface-variant font-body-base">FASTQ Analysis</span>
</div>
</td>
<td class="px-6 py-5 text-on-surface-variant font-body-sm">
                                        Oct 23, 2023 · 09:15
                                    </td>
<td class="px-6 py-5">
<span class="px-2 py-0.5 bg-warning/10 text-warning border border-warning/20 rounded font-badge uppercase">Med (84.1%)</span>
</td>
<td class="px-6 py-5">
<div class="flex gap-1.5">
<button class="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant font-code-xs" title="HTML">HTML</button>
<button class="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant font-code-xs text-[9px]" title="GFF3">GFF3</button>
<button class="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant font-code-xs" title="JSON">JS</button>
</div>
</td>
<td class="px-6 py-5 text-right">
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary">open_in_new</button>
</td>
</tr>
<!-- Row 3 -->
<tr class="hover:bg-bg-panel transition-colors group">
<td class="px-6 py-5">
<div class="flex flex-col">
<span class="font-subheading text-on-surface">Mycobacterium_TBC_S14</span>
<span class="font-code-xs text-text-muted uppercase">JOB-8712-AA</span>
</div>
</td>
<td class="px-6 py-5">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-primary text-[18px]">account_tree</span>
<span class="text-on-surface-variant font-body-base">Viral Clade Analysis</span>
</div>
</td>
<td class="px-6 py-5 text-on-surface-variant font-body-sm">
                                        Oct 21, 2023 · 18:02
                                    </td>
<td class="px-6 py-5">
<span class="px-2 py-0.5 bg-success/10 text-success border border-success/20 rounded font-badge uppercase">High (99.9%)</span>
</td>
<td class="px-6 py-5">
<div class="flex gap-1.5">
<button class="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant font-code-xs" title="PDF">PDF</button>
<button class="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant font-code-xs" title="JSON">JS</button>
</div>
</td>
<td class="px-6 py-5 text-right">
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary">open_in_new</button>
</td>
</tr>
<!-- Row 4 -->
<tr class="hover:bg-bg-panel transition-colors group">
<td class="px-6 py-5">
<div class="flex flex-col">
<span class="font-subheading text-on-surface">P_Aeruginosa_Multi_Strain</span>
<span class="font-code-xs text-text-muted uppercase">JOB-8655-LV</span>
</div>
</td>
<td class="px-6 py-5">
<div class="flex items-center gap-2">
<span class="material-symbols-outlined text-secondary text-[18px]">dns</span>
<span class="text-on-surface-variant font-body-base">Viral Genome Annotation</span>
</div>
</td>
<td class="px-6 py-5 text-on-surface-variant font-body-sm">
                                        Oct 19, 2023 · 11:24
                                    </td>
<td class="px-6 py-5">
<span class="px-2 py-0.5 bg-success/10 text-success border border-success/20 rounded font-badge uppercase">High (97.0%)</span>
</td>
<td class="px-6 py-5">
<div class="flex gap-1.5">
<button class="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant font-code-xs" title="HTML">HTML</button>
<button class="w-8 h-8 flex items-center justify-center bg-bg-card border border-outline-variant rounded hover:border-primary hover:text-primary transition-all text-on-surface-variant font-code-xs" title="CSV">CSV</button>
</div>
</td>
<td class="px-6 py-5 text-right">
<button class="material-symbols-outlined text-on-surface-variant hover:text-primary">open_in_new</button>
</td>
</tr>
</tbody>
</table>
</div>
<!-- Pagination -->
<div class="bg-surface-container-high px-6 py-3 flex items-center justify-between border-t border-outline-variant">
<span class="text-body-sm text-text-muted">Showing 1 to 4 of 128 reports</span>
<div class="flex gap-2">
<button class="p-1 border border-outline-variant rounded hover:bg-surface-variant disabled:opacity-50" disabled="">
<span class="material-symbols-outlined">chevron_left</span>
</button>
<button class="px-3 py-1 bg-primary text-on-primary rounded font-body-sm">1</button>
<button class="px-3 py-1 text-on-surface-variant hover:bg-surface-variant rounded font-body-sm">2</button>
<button class="px-3 py-1 text-on-surface-variant hover:bg-surface-variant rounded font-body-sm">3</button>
<button class="p-1 border border-outline-variant rounded hover:bg-surface-variant">
<span class="material-symbols-outlined">chevron_right</span>
</button>
</div>
</div>
</div>
<!-- Bento Style Insights Section -->
<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
<div class="bg-surface-container rounded-xl border border-outline-variant p-card-padding flex flex-col justify-between">
<div>
<h3 class="font-subheading text-on-surface mb-2">Storage Utilization</h3>
<p class="text-text-muted text-body-sm">Archived results are consuming 84% of your allocated genomic storage tier.</p>
</div>
<div class="mt-4">
<div class="w-full bg-surface-container-lowest h-2 rounded-full overflow-hidden">
<div class="bg-primary h-full w-[84%]"></div>
</div>
<div class="flex justify-between mt-2 font-code-xs">
<span class="">1.6 TB used</span>
<span class="">2.0 TB total</span>
</div>
</div>
</div>
<div class="bg-surface-container rounded-xl border border-outline-variant p-card-padding">
<h3 class="font-subheading text-on-surface mb-2">Quick Export Bundle</h3>
<p class="text-text-muted text-body-sm mb-4">Prepare all filtered results for bulk download.</p>
<button class="w-full py-2 bg-secondary-container text-on-secondary-container rounded-lg font-subheading flex items-center justify-center gap-2 hover:opacity-90 transition-all">
<span class="material-symbols-outlined">archive</span>
                            Export Selected (4)
                        </button>
</div>
<div class="bg-surface-container rounded-xl border border-outline-variant p-card-padding relative overflow-hidden group">
<div class="relative z-10">
<h3 class="font-subheading text-on-surface mb-1">Compute Efficiency</h3>
<p class="text-success text-headline-md font-bold">12% Improvement</p>
<p class="text-text-muted text-body-sm">Average report generation time has decreased since v2.4.0 update.</p>
</div>
<!-- Background Pattern Decor -->
<div class="absolute -right-4 -bottom-4 opacity-10 group-hover:scale-110 transition-transform duration-700">
<span class="material-symbols-outlined text-[120px] text-primary">monitoring</span>
</div>
</div>
</div>
</div>
</main>
</div>
<!-- Floating Toast for Micro-interaction -->
<div class="fixed bottom-6 right-6 translate-y-20 opacity-0 transition-all duration-300 pointer-events-none" id="toast">
<div class="bg-bg-panel border border-primary text-primary px-4 py-3 rounded-lg shadow-2xl flex items-center gap-3">
<span class="material-symbols-outlined">download_done</span>
<span class="font-subheading">Download started...</span>
</div>
</div>
<script>
        // Micro-interactions for download buttons
        document.querySelectorAll('button[title]').forEach(btn => {
            btn.addEventListener('click', () => {
                const toast = document.getElementById('toast');
                toast.classList.remove('translate-y-20', 'opacity-0');
                
                setTimeout(() => {
                    toast.classList.add('translate-y-20', 'opacity-0');
                }, 3000);
            });
        });

        // Hover animation logic for rows
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('mouseenter', () => {
                row.querySelector('button[title="HTML"]')?.classList.add('scale-105');
            });
            row.addEventListener('mouseleave', () => {
                row.querySelector('button[title="HTML"]')?.classList.remove('scale-105');
            });
        });
    </script>


</body></html>

