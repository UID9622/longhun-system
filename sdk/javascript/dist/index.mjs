// src/client.ts
import axios from "axios";

// src/models.ts
var Scores = class _Scores {
  constructor(humanWelfare = 70, fairness = 70, controllability = 70, transparency = 70, traceability = 70, privacy = 70) {
    this.humanWelfare = humanWelfare;
    this.fairness = fairness;
    this.controllability = controllability;
    this.transparency = transparency;
    this.traceability = traceability;
    this.privacy = privacy;
  }
  toJSON() {
    return {
      humanWelfare: this.humanWelfare,
      fairness: this.fairness,
      controllability: this.controllability,
      transparency: this.transparency,
      traceability: this.traceability,
      privacy: this.privacy
    };
  }
  static fromJSON(data) {
    return new _Scores(
      data.humanWelfare ?? 70,
      data.fairness ?? 70,
      data.controllability ?? 70,
      data.transparency ?? 70,
      data.traceability ?? 70,
      data.privacy ?? 70
    );
  }
};
var Verdict = class _Verdict {
  constructor(actionId, rScore, status, statusCode, emoji, disposition, dna, evidenceHash, triggeredRules = [], engineVersion = "", contractVersion = "", timestamp = "") {
    this.actionId = actionId;
    this.rScore = rScore;
    this.status = status;
    this.statusCode = statusCode;
    this.emoji = emoji;
    this.disposition = disposition;
    this.dna = dna;
    this.evidenceHash = evidenceHash;
    this.triggeredRules = triggeredRules;
    this.engineVersion = engineVersion;
    this.contractVersion = contractVersion;
    this.timestamp = timestamp;
  }
  isGreen() {
    return this.statusCode === "GREEN";
  }
  isYellow() {
    return this.statusCode === "YELLOW";
  }
  isRed() {
    return this.statusCode === "RED";
  }
  static fromJSON(data) {
    return new _Verdict(
      data.action_id ?? "",
      data.r_score ?? 0,
      data.status ?? "\u5B89\u5168",
      data.status_code ?? "GREEN",
      data.emoji ?? "\u{1F7E2}",
      data.disposition ?? "",
      data.dna ?? "",
      data.evidence_hash ?? "",
      data.triggered_rules ?? [],
      data.engine_version ?? "",
      data.contract_version ?? "",
      data.timestamp ?? ""
    );
  }
};
var EvidenceChain = class _EvidenceChain {
  constructor(dna, trigger, triggeredAt, ruleIds, rScore, disposition, hash, sealed) {
    this.dna = dna;
    this.trigger = trigger;
    this.triggeredAt = triggeredAt;
    this.ruleIds = ruleIds;
    this.rScore = rScore;
    this.disposition = disposition;
    this.hash = hash;
    this.sealed = sealed;
  }
  static fromJSON(data) {
    const chain = data.chain || {};
    const integrity = data.integrity || {};
    return new _EvidenceChain(
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
};

// src/exceptions.ts
var TricolorError = class extends Error {
  constructor(code, message, dna = "") {
    super(`[${code}] ${message}`);
    this.code = code;
    this.dna = dna;
    this.name = "TricolorError";
  }
};
var RedLineException = class extends Error {
  constructor(verdict) {
    super(
      `\u{1F534} \u7EA2\u7EBF\u89E6\u53D1: ${verdict.status} (R=${verdict.rScore}) DNA=${verdict.dna}`
    );
    this.verdict = verdict;
    this.name = "RedLineException";
  }
};
var ReviewRequiredException = class extends Error {
  constructor(verdict) {
    super(
      `\u{1F7E1} \u9700\u8981\u5BA1\u67E5: ${verdict.status} (R=${verdict.rScore}) DNA=${verdict.dna}`
    );
    this.verdict = verdict;
    this.name = "ReviewRequiredException";
  }
};

// src/client.ts
var TricolorClient = class {
  constructor(config = {}) {
    this.baseUrl = (config.baseUrl || "https://uid9622.cn/api/tricolor").replace(/\/$/, "");
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: config.timeout || 3e4,
      headers: {
        "Content-Type": "application/json",
        ...config.token ? { Authorization: `Bearer ${config.token}` } : {}
      }
    });
  }
  async evaluate(params) {
    const payload = {
      action_id: params.actionId,
      actor: params.actor,
      action_type: params.actionType,
      locale: params.locale || "zh-CN"
    };
    if (params.scores)
      payload.scores = params.scores.toJSON();
    if (params.description)
      payload.description = params.description;
    if (params.context)
      payload.context = params.context;
    try {
      const resp = await this.client.post("/v1/tricolor/evaluate", payload);
      const verdict = Verdict.fromJSON(resp.data);
      if (verdict.statusCode === "RED")
        throw new RedLineException(verdict);
      if (verdict.statusCode === "YELLOW")
        throw new ReviewRequiredException(verdict);
      return verdict;
    } catch (err) {
      if (err instanceof RedLineException || err instanceof ReviewRequiredException)
        throw err;
      if (axios.isAxiosError(err) && err.response) {
        const data = err.response.data;
        throw new TricolorError(
          data.code || "TC-UNKNOWN",
          data.message || "\u672A\u77E5\u9519\u8BEF",
          data.dna || ""
        );
      }
      throw err;
    }
  }
  async getEvidence(dna) {
    const resp = await this.client.get(
      `/v1/tricolor/evidence/${encodeURIComponent(dna)}`
    );
    return EvidenceChain.fromJSON(resp.data);
  }
  async getRules() {
    const resp = await this.client.get("/v1/tricolor/rules");
    return resp.data;
  }
  async getVersion() {
    const resp = await this.client.get("/v1/tricolor/version");
    return resp.data;
  }
};
export {
  EvidenceChain,
  RedLineException,
  ReviewRequiredException,
  Scores,
  TricolorClient,
  TricolorError,
  Verdict
};
