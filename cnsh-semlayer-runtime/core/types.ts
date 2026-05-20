/** CNSH-SEMLAYER · 类型契约 v1.4 · 实现分 Phase */

export type Lang = "zh-CN" | "zh-TW" | "en-US" | "ja-JP" | "km-KH";

export type RouteMode = "public" | "sovereign";

export type AIProtocol = "claude" | "gpt" | "deepseek" | "mcp" | "local";

export interface DNASignature {
  gpg: string;
  confirm: string;
  seal: string;
  trace?: string;
}

export interface CNSHPacket {
  cnsh: string;
  sourceLang?: Lang;
  mode: RouteMode;
  dna?: string;
}

export interface LocalizedOutput {
  text: string;
  annotations?: string;
  lang: Lang;
}

export type EmitTarget = "clipboard" | "notion" | "jsonl";

export interface EmitReceipt {
  chainHash: string;
  dna: string;
  tsUtc8: string;
}
