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

export * from "./types";
import type { EditionSummary, Edition, OwnerAction, Stats } from "./types";

export const getStats = () => rpc<Stats>("ft_stats");
export const getEditions = (includeDrafts: boolean) =>
  rpc<EditionSummary[]>("ft_editions", { include_drafts: includeDrafts });
export const getEdition = (date: string, includeDrafts: boolean) =>
  rpc<Edition | null>("ft_edition", { d: date, include_drafts: includeDrafts });

export const ownerAction = (date: string, action: OwnerAction, videoUrl?: string) =>
  rpc<Edition>("ft_owner_action", { d: date, action, video_url: videoUrl ?? null });

export const isPreview = (key: string | string[] | undefined) =>
  !!process.env.PREVIEW_KEY && key === process.env.PREVIEW_KEY;
