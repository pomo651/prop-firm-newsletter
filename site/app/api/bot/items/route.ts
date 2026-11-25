import { botWrite } from "@/lib/bot";

// [{url, title, source_name, summary?, source_url?, firm?, collected_by?, collected_at?, status?}]
// status: new | picked | rejected. Re-sending a url updates it.
export const POST = (req: Request) => botWrite(req, "ft_upsert_items", "rows", "array");
