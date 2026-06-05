import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export const Navbar = () => {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  const links = [
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Workspace', href: '/workspace' },
    { name: 'Reports Center', href: '/reports' },
    { name: 'Documentation', href: '/documentation' },
    { name: 'Settings', href: '/settings' },
  ];

  return (
    <nav className="bg-[#111827] border-b border-[#1F2937] text-[#F9FAFB] w-full z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <div className="flex-shrink-0 flex items-center gap-3">
              <span className="text-[#3B82F6] font-bold text-2xl tracking-wider">
                PathoScope AI
              </span>
              <span className="hidden md:inline text-xs text-[#9CA3AF] border-l border-[#1F2937] pl-3 py-1 font-mono">
                Viral Genomics v3.0
              </span>
            </div>
            <div className="hidden md:block pl-10">
              <div className="flex space-x-4">
                {links.map((link) => {
                  const isActive = pathname === link.href || (link.href === '/dashboard' && pathname === '/');
                  return (
                    <Link
                      key={link.name}
                      href={link.href}
                      className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                        isActive
                          ? 'bg-[#3B82F6] text-[#F9FAFB]'
                          : 'text-[#D1D5DB] hover:bg-[#1F2937] hover:text-[#F9FAFB]'
                      }`}
                    >
                      {link.name}
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>
          <div className="hidden md:flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-[#22C55E]" />
              <span className="text-xs text-[#9CA3AF] font-mono">DB Pipeline Engine Live</span>
            </div>
            <div className="h-8 w-8 rounded-full bg-[#1F2937] flex items-center justify-center border border-[#3B82F6]">
              <span className="text-xs font-bold text-[#3B82F6]">SCI</span>
            </div>
          </div>
          
          <div className="-mr-2 flex md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="inline-flex items-center justify-center p-2 rounded-md text-[#9CA3AF] hover:text-white hover:bg-[#1F2937]"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {isOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {isOpen && (
        <div className="md:hidden bg-[#111827] border-t border-[#1F2937] px-2 pt-2 pb-3 space-y-1">
          {links.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.name}
                href={link.href}
                onClick={() => setIsOpen(false)}
                className={`block px-3 py-2 rounded-md text-base font-medium ${
                  isActive ? 'bg-[#3B82F6] text-white' : 'text-[#D1D5DB] hover:bg-[#1F2937] hover:text-white'
                }`}
              >
                {link.name}
              </Link>
            );
          })}
        </div>
      )}
    </nav>
  );
};
