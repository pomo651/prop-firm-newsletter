import { botWrite } from "@/lib/bot";

// {edition_date, video_url?, title?} — always saved as draft. Only the owner approves a Short.
export const POST = (req: Request) => botWrite(req, "ft_upsert_video", "v", "object");
