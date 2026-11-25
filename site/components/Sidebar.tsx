"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV = [
  { href: "/", label: "Home" },
  { href: "/daily", label: "Daily newsletter" },
];

export function Sidebar() {
  const path = usePathname();
  const active = (href: string) => (href === "/" ? path === "/" : path.startsWith(href));
  return (
    <aside className="sidebar">
      <Link href="/" className="brand">
        <span className="brand-mark" aria-hidden>
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="#fff" strokeWidth="1.6">
            <path d="M1 4h14M1 8h10M1 12h6" strokeLinecap="round" />
          </svg>
        </span>
        Funded Tape
      </Link>
      <nav className="nav" aria-label="Main">
        <div className="nav-label">Read</div>
        {NAV.map((n) => (
          <Link key={n.href} href={n.href} aria-current={active(n.href) ? "page" : undefined}>
            {n.label}
          </Link>
        ))}
      </nav>
      <div className="sidebar-foot">Independent prop firm news. Not financial advice.</div>
    </aside>
  );
}
