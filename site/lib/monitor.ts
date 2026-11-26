import "server-only";
import { rpc } from "./db";

// One grading for the /admin/monitor page and the alert job: public.ft_monitor.
export type MonState = "ok" | "late" | "needs" | "fail" | "wait" | "off";
export type MonStep = { key: string; title: string; who: string; due: string; state: MonState; detail: string };
export type MonDay = { date: string; state: "ok" | "late" | "fail" | "wait" | "off"; steps: MonStep[] };
export type MonAlert = { edition_date: string; step: string; state: string; detail: string | null; sent_at: string };
export type Monitor = { at: string; days: MonDay[]; alerts: MonAlert[] };

export const getMonitor = (days = 14) => rpc<Monitor>("ft_monitor", { days });

// One row per FT-grok bot for today: last DB write + today's output. We only see what reaches the DB.
export type BotStatus = { bot: string; job: string; due: string; state: MonState; today: string; last: string | null };
export const getBots = () => rpc<BotStatus[]>("ft_monitor_bots");

export const STEP_KEYS = ["collect", "picks", "draft", "publish", "short", "approve"] as const;
