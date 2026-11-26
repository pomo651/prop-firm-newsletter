import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Funded Tape — prop firm news that matters", template: "%s · Funded Tape" },
  description:
    "Funded Tape watches prop firm help centers, rule pages, X accounts, trade press and trader communities, and keeps only the few changes that matter.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
