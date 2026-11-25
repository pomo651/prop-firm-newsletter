import { botWrite } from "@/lib/bot";

// {edition_date, subject, preview?, intro?, outro?, sections:[{headline, body, why?, sources?}], status?}
// status defaults to draft. Only the owner flips it to published.
export const POST = (req: Request) => botWrite(req, "ft_upsert_edition", "e", "object");
