import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export const Sidebar = () => {
  const pathname = usePathname();

  const navLinks = [
    { name: 'Uploads / Workspace', href: '/workspace', icon: 'cloud_upload' },
    { name: 'Active Jobs / Stats', href: '/dashboard', icon: 'settings_input_component' },
    { name: 'Archive / Reports', href: '/reports', icon: 'inventory_2' },
    { name: 'PubMed Explorer', href: '/pubmed', icon: 'library_books' },
    { name: 'API Keys', href: '/settings', icon: 'key' },
    { name: 'Documentation', href: '/documentation', icon: 'menu_book' }
  ];

  return (
    <aside className="fixed left-0 top-16 bottom-0 w-64 bg-[#19202e] flex flex-col p-4 border-r border-[#424754] z-40 select-none">
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2 px-2">
          <div className="w-8 h-8 rounded bg-[#4d8eff] flex items-center justify-center">
            <span className="material-symbols-outlined text-[#002e6a] text-lg font-bold">biotech</span>
          </div>
          <div>
            <h3 className="text-xs font-bold text-white leading-tight">Genomic Workspace</h3>
            <p className="text-[10px] text-on-surface-variant tracking-wider uppercase">v2.4.0-stable</p>
          </div>
        </div>
        <Link href="/workspace">
          <button className="w-full mt-4 bg-[#adc6ff] text-[#002e6a] py-2 px-4 rounded-lg font-semibold hover:opacity-90 transition-all flex items-center justify-center gap-2 text-xs">
            <span className="material-symbols-outlined text-sm font-bold">add</span>
            New Pipeline
          </button>
        </Link>
      </div>

      <nav className="flex-1 flex flex-col gap-1">
        {navLinks.map((link) => {
          const isActive = pathname === link.href;
          return (
            <Link
              key={link.name}
              href={link.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                isActive
                  ? 'bg-[#4d8eff] text-[#00285d]'
                  : 'text-on-surface-variant hover:bg-[#2e3544] hover:text-white'
              }`}
            >
              <span className="material-symbols-outlined text-base">{link.icon}</span>
              {link.name}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto pt-4 border-t border-[#424754] flex flex-col gap-1">
        <a className="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-[#2e3544] rounded-lg text-xs" href="#">
          <span className="material-symbols-outlined text-base">dns</span> System Status
        </a>
        <a className="flex items-center gap-3 px-3 py-2 text-on-surface-variant hover:bg-[#2e3544] rounded-lg text-xs" href="#">
          <span className="material-symbols-outlined text-base">logout</span> Logout
        </a>
      </div>
    </aside>
  );
};
