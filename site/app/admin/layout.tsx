import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { isAdmin } from "@/lib/admin";
import { AdminNav } from "@/components/admin/AdminNav";
import "./bustem.css";
import "./admin.css";

// Admin shell: FDE "bustem" theme (VHealth / Kids Map admin look). Rules: app/admin/THEME.md.
const geist = Geist({ subsets: ["latin"], variable: "--font-geist" });
const geistMono = Geist_Mono({ subsets: ["latin"], variable: "--font-geist-mono" });

export const metadata: Metadata = { title: { default: "Admin", template: "%s · Admin · Funded Tape" }, robots: { index: false } };

export default async function AdminLayout({ children }: { children: React.ReactNode }) {
  const ok = await isAdmin();
  return (
    <div className={`bz ft-adm ${geist.variable} ${geistMono.variable}`}>
      {ok ? (
        <div className="bz-shell">
          <AdminNav />
          <main className="bz-main">{children}</main>
        </div>
      ) : (
        <Login />
      )}
    </div>
  );
}

function Login() {
  return (
    <main className="ft-login">
      <form className="bz-card" method="post" action="/api/admin/login">
        <div className="ft-brand"><span className="ft-mark" aria-hidden /> Funded Tape</div>
        <h1>Admin</h1>
        <div className="bz-sub">Use the preview key.</div>
        <label className="bz-field">
          <span className="bz-label">Key</span>
          <input name="key" type="password" autoComplete="current-password" required autoFocus />
        </label>
        <div className="bz-btns"><button className="bz-btn" type="submit">Sign in</button></div>
      </form>
    </main>
  );
}
