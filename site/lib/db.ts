import "server-only";
import { createClient } from "@supabase/supabase-js";

// All reads/writes go through the public.ft_* RPCs (schema funded_tape is not
// exposed). Service role key is server-only; see supabase/migrations.
function client() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw new Error("SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not set");
  return createClient(url, key, { auth: { persistSession: false } });
}

export async function rpc<T>(fn: string, args?: Record<string, unknown>): Promise<T> {
  const { data, error } = await client().rpc(fn, args);
  if (error) throw new Error(`${fn}: ${error.message}`);
  return data as T;
}

export type Pick = { id: number; title: string; source: string; url: string; firm: string | null; picked_at: string };

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

export type Edition = {
  edition_date: string;
  subject: string;
  preview: string | null;
  intro: string | null;
  outro: string | null;
  sections: Section[];
  status: "draft" | "published";
  published_at: string | null;
};

export const getStats = () => rpc<Stats>("ft_stats");
export const getEditions = (includeDrafts: boolean) =>
  rpc<EditionSummary[]>("ft_editions", { include_drafts: includeDrafts });
export const getEdition = (date: string, includeDrafts: boolean) =>
  rpc<Edition | null>("ft_edition", { d: date, include_drafts: includeDrafts });

export const isPreview = (key: string | string[] | undefined) =>
  !!process.env.PREVIEW_KEY && key === process.env.PREVIEW_KEY;
