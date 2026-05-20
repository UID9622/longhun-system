/**
 * Layer 2 · 双轨闸门 · CNSH-SEMLAYER v1.4
 * 公开 = 信任止于沟通层 · 主权 = DNA 三验后才出代码
 * DNA: #龍芯⚡2026-05-20-CNSH-SEMLAYER-RUNTIME-v1.4-SOVEREIGNTY-REWRITE
 */

import type { DNASignature, RouteMode } from "./types";

const GPG_EXPECTED = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F";
const CONFIRM_EXPECTED = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";
const SEAL_EXPECTED = "#ZHUGEXIN⚡2025-🇨🇳🐉⚖️-DEVICE-BIND-SOUL";

export function verifyGPG(gpg: string): boolean {
  return gpg.trim().toUpperCase() === GPG_EXPECTED;
}

export function matchConfirm(confirm: string): boolean {
  return confirm.trim() === CONFIRM_EXPECTED;
}

export function validateSeal(seal: string): boolean {
  return seal.trim() === SEAL_EXPECTED;
}

export function verifyThreeFactor(sig: DNASignature): boolean {
  return (
    verifyGPG(sig.gpg) && matchConfirm(sig.confirm) && validateSeal(sig.seal)
  );
}

/**
 * 分流：三验过 → 主权；否则 → 公开（不出代码类输出由上层 enforce）
 */
export function routeMode(_input: string, sig?: DNASignature): RouteMode {
  if (sig && verifyThreeFactor(sig)) {
    return "sovereign";
  }
  return "public";
}

/** 模式 A 禁止的输出类（上层调用） */
export const PUBLIC_FORBIDDEN = [
  "code",
  "deploy",
  "protocol_weld",
  "business_plan",
] as const;

export function assertPublicOutputAllowed(kind: string): void {
  if (PUBLIC_FORBIDDEN.includes(kind as (typeof PUBLIC_FORBIDDEN)[number])) {
    throw new Error(
      "模式 A：信任止于沟通层 · 代码/部署/协议焊接/商务方案需 DNA 三验（模式 B）"
    );
  }
}
