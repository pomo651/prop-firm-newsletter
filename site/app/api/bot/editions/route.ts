import { botWrite } from "@/lib/bot";

// {edition_date, subject, preview?, intro?, outro?, sections:[{headline, body, why?, sources?}]}
// Always saved as draft; a published edition is locked. Only the owner publishes (/api/owner).
export const POST = (req: Request) => botWrite(req, "ft_upsert_edition", "e", "object");
