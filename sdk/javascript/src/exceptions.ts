/**
 * 🐉 龍魂·三色审计 JS SDK - 异常定义
 * DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-JS-SDK-EXCEPTIONS-V1.0-UID9622
 * License: MulanPSL v2
 */

import { Verdict } from "./models";

export class TricolorError extends Error {
  code: string;
  dna: string;

  constructor(code: string, message: string, dna: string = "") {
    super(`[${code}] ${message}`);
    this.code = code;
    this.dna = dna;
    this.name = "TricolorError";
  }
}

export class RedLineException extends Error {
  verdict: Verdict;

  constructor(verdict: Verdict) {
    super(
      `🔴 红线触发: ${verdict.status} (R=${verdict.rScore}) DNA=${verdict.dna}`
    );
    this.verdict = verdict;
    this.name = "RedLineException";
  }
}

export class ReviewRequiredException extends Error {
  verdict: Verdict;

  constructor(verdict: Verdict) {
    super(
      `🟡 需要审查: ${verdict.status} (R=${verdict.rScore}) DNA=${verdict.dna}`
    );
    this.verdict = verdict;
    this.name = "ReviewRequiredException";
  }
}
