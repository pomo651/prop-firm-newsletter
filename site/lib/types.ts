// Shapes returned by the public.ft_* RPCs. Safe to import from client components.

export type Category = "rule_change" | "launch" | "payout" | "pricing" | "promo" | "allegation";

export const CATEGORY_LABEL: Record<Category, string> = {
  rule_change: "Rule change", launch: "Launch", payout: "Payout",
  pricing: "Pricing", promo: "Promo", allegation: "Allegation",
};

export type Pick = {
  id: number; title: string; source: string; url: string;
  firm: string | null; category: Category | null; picked_at: string;
};

export type Stats = {
  sources: number;
  sourceKinds: Record<string, number>;
  items: number;
  items24h: number;
  picks: number;
  picks24h: number;
  editions: number;
  latestEdition: string | null;
  latest: Pick[];
  at: string;
};

export type Section = { headline: string; body: string; why?: string; sources?: string[] };

export type EditionSummary = {
  edition_date: string;
  subject: string;
  preview: string | null;
  status: "draft" | "published";
  published_at: string | null;
  section_count: number;
  headlines: string[];
};

export type Video = {
  video_url: string | null;
  title: string | null;
  status: "draft" | "approved" | "uploaded";
  approved_at: string | null;
};

export type Edition = {
  edition_date: string;
  subject: string;
  preview: string | null;
  intro: string | null;
  outro: string | null;
  sections: Section[];
  status: "draft" | "published";
  published_at: string | null;
  video: Video | null;
};

export type OwnerAction = "publish" | "unpublish" | "approve_video" | "unapprove_video" | "mark_uploaded";
