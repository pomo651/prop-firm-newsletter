import { Sidebar } from "@/components/Sidebar";

// Public site shell (Home, Daily). The admin has its own shell in app/admin/layout.tsx.
export default function SiteLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="shell">
      <Sidebar />
      <main className="main">{children}</main>
    </div>
  );
}
