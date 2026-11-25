import { botWrite } from "@/lib/bot";

// [{name, kind, url, active?}] — kind: official | x | press | community | youtube | review | other
export const POST = (req: Request) => botWrite(req, "ft_upsert_sources", "rows", "array");
