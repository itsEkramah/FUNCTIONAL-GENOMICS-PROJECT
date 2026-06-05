'use client';

import React from 'react';
import '../app/globals.css';
import { Navbar } from '../components/Navbar';
import { Sidebar } from '../components/Sidebar';
import { usePathname } from 'next/navigation';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isLanding = pathname === '/';

  return (
    <html lang="en" className="dark">
      <head>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet" />
        <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
      </head>
      <body className="bg-[#0c1321] text-[#dce2f6] min-h-screen flex flex-col font-sans antialiased selection:bg-[#3B82F6]/30 overflow-x-hidden">
        <Navbar />
        <div className="flex flex-1 relative">
          {!isLanding && <Sidebar />}
          <main className={`flex-1 flex flex-col ${isLanding ? 'ml-0' : 'ml-64'}`}>
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
