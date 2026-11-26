"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

// 18px line icons, stroke = currentColor (bustem: .bz-ni svg)
const I = {
  today: <path d="M3 12h4l3-8 4 16 3-8h4" />,
  monitor: <><rect x="3" y="4" width="18" height="16" rx="2" /><path d="M7 15l3-3 3 2 4-5" /></>,
  items: <><path d="M4 6h16M4 12h16M4 18h10" /></>,
  editions: <><rect x="4" y="3" width="16" height="18" rx="2" /><path d="M8 8h8M8 12h8M8 16h5" /></>,
  sources: <><circle cx="12" cy="12" r="8" /><path d="M4 12h16M12 4a12 12 0 0 1 0 16M12 4a12 12 0 0 0 0 16" /></>,
  flow: <><circle cx="6" cy="6" r="2.5" /><circle cx="18" cy="18" r="2.5" /><path d="M8.5 6H15a3 3 0 0 1 0 6H9a3 3 0 0 0 0 6h6.5" /></>,
  site: <><path d="M14 4h6v6M20 4l-9 9" /><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" /></>,
};
const ico = (k: keyof typeof I) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" aria-hidden>{I[k]}</svg>
);

const GROUPS: { label: string; links: { href: string; label: string; icon: keyof typeof I }[] }[] = [
  { label: "Today", links: [{ href: "/admin", label: "Today", icon: "today" }, { href: "/admin/monitor", label: "Monitor", icon: "monitor" }] },
  { label: "Content", links: [
    { href: "/admin/items", label: "Items & picks", icon: "items" },
    { href: "/admin/editions", label: "Editions & Shorts", icon: "editions" },
    { href: "/admin/sources", label: "Sources", icon: "sources" },
  ] },
  { label: "Team", links: [{ href: "/admin/workflows", label: "Workflows", icon: "flow" }] },
];

export function AdminNav() {
  const path = usePathname();
  const [open, setOpen] = useState(false);
  const on = (href: string) => (href === "/admin" ? path === "/admin" : path.startsWith(href));
  return (
    <>
      <button className="ft-menu bz-btn ghost sm" onClick={() => setOpen(true)} aria-label="Open menu">☰ Menu</button>
      <aside className={`bz-side${open ? " open" : ""}`} onClick={() => setOpen(false)}>
        <Link href="/admin" className="ft-brand"><span className="ft-mark" aria-hidden /> Funded Tape</Link>
        {GROUPS.map((g) => (
          <div key={g.label}>
            <div className="bz-gl">{g.label}</div>
            {g.links.map((l) => (
              <Link key={l.href} href={l.href} className={`bz-ni${on(l.href) ? " on" : ""}`} aria-current={on(l.href) ? "page" : undefined}>
                {ico(l.icon)}{l.label}
              </Link>
            ))}
          </div>
        ))}
        <div className="bz-foot">
          <Link href="/" className="bz-ni">{ico("site")}View site</Link>
          <form method="post" action="/api/admin/logout"><button className="bz-ni ft-out">Sign out</button></form>
        </div>
      </aside>
    </>
  );
}
