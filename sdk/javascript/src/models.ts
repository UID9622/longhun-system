# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 🐉 龍魂·三色审计 JS SDK - 数据模型
 * DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-JS-SDK-MODELS-V1.0-UID9622
 * License: MulanPSL v2
 */

export class Scores {
  constructor(
    public humanWelfare: number = 70,
    public fairness: number = 70,
    public controllability: number = 70,
    public transparency: number = 70,
    public traceability: number = 70,
    public privacy: number = 70
  ) {}

  toJSON() {
    return {
      humanWelfare: this.humanWelfare,
      fairness: this.fairness,
      controllability: this.controllability,
      transparency: this.transparency,
      traceability: this.traceability,
      privacy: this.privacy,
    };
  }

  static fromJSON(data: any): Scores {
    return new Scores(
      data.humanWelfare ?? 70,
      data.fairness ?? 70,
      data.controllability ?? 70,
      data.transparency ?? 70,
      data.traceability ?? 70,
      data.privacy ?? 70
    );
  }
}

export class Verdict {
  constructor(
    public actionId: string,
    public rScore: number,
    public status: string,
    public statusCode: "GREEN" | "YELLOW" | "RED",
    public emoji: string,
    public disposition: string,
    public dna: string,
    public evidenceHash: string,
    public triggeredRules: string[] = [],
    public engineVersion: string = "",
    public contractVersion: string = "",
    public timestamp: string = ""
  ) {}

  isGreen(): boolean {
    return this.statusCode === "GREEN";
  }
  isYellow(): boolean {
    return this.statusCode === "YELLOW";
  }
  isRed(): boolean {
    return this.statusCode === "RED";
  }

  static fromJSON(data: any): Verdict {
    return new Verdict(
      data.action_id ?? "",
      data.r_score ?? 0,
      data.status ?? "安全",
      data.status_code ?? "GREEN",
      data.emoji ?? "🟢",
      data.disposition ?? "",
      data.dna ?? "",
      data.evidence_hash ?? "",
      data.triggered_rules ?? [],
      data.engine_version ?? "",
      data.contract_version ?? "",
      data.timestamp ?? ""
    );
  }
}

export class EvidenceChain {
  constructor(
    public dna: string,
    public trigger: string,
    public triggeredAt: string,
    public ruleIds: string[],
    public rScore: number,
    public disposition: string,
    public hash: string,
    public sealed: boolean
  ) {}

  static fromJSON(data: any): EvidenceChain {
    const chain = data.chain || {};
    const integrity = data.integrity || {};
    return new EvidenceChain(
      data.dna ?? "",
      chain.trigger ?? "",
      chain.triggered_at ?? "",
      chain.rule_ids ?? [],
      chain.r_score ?? 0,
      chain.disposition ?? "",
      integrity.hash ?? "",
      integrity.sealed ?? false
    );
  }
}
