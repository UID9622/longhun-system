// 🐉 龍魂·三色审计 JavaScript SDK v1.1
// DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-TRICOLOR-JS-SDK-v1.1-UID9622
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）

/**
 * 三色审计核心引擎（纯JS，零依赖）。
 *
 * R值公式（焊死·P0级）：
 *   R = 0.20·人类福祉 + 0.20·公平公正 + 0.15·可控可信
 *     + 0.15·透明可解释 + 0.15·责任可追溯 + 0.15·隐私保护
 *
 * 阈值：
 *   R ≥ 85 → 🟢 GREEN（放行）
 *   60 ≤ R < 85 → 🟡 YELLOW（挂起复核）
 *   R < 60 → 🔴 RED（立即熔断）
 *
 * 上限封顶：R ≤ 95
 */

const DIMENSIONS = [
  ["humanWelfare",    "人类福祉",     0.20],
  ["fairness",        "公平公正",     0.20],
  ["controllability", "可控可信",     0.15],
  ["transparency",    "透明可解释",   0.15],
  ["traceability",    "责任可追溯",   0.15],
  ["privacy",         "隐私保护",     0.15],
];

const R_CAP = 95;
const THRESHOLD_GREEN = 85;
const THRESHOLD_YELLOW = 60;

const STATUS_MAP = {
  GREEN:  { status: "安全", emoji: "🟢", disposition: "放行",     en: "PASS" },
  YELLOW: { status: "审查", emoji: "🟡", disposition: "挂起待复核，需双人确认", en: "REVIEW" },
  RED:    { status: "阻断", emoji: "🔴", disposition: "立即熔断+告警+证据固化", en: "BLOCK" },
};

const ENGINE_VERSION = "tricolor-core/1.1.0";
const CONTRACT_VERSION = "openapi-tricolor/1.1";

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 核心引擎（纯JS，可用于浏览器/Node/小程序/鸿蒙ArkTS）
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * 计算六维加权R值。
 */
function computeR(scores) {
  let total = 0;
  for (const [key, , weight] of DIMENSIONS) {
    total += (scores[key] || 0) * weight;
  }
  return Math.min(R_CAP, Math.round(total));
}

/**
 * 生成DNA追溯码。
 */
function generateDNA(actionId) {
  const rand = Math.random().toString(36).slice(2, 10);
  return `#龍芯⚡️丙午·癸未·乙酉·坤卦-AUDIT-${rand}-9622`;
}

/**
 * 生成证据哈希（SHA-256兜底）。
 */
async function hashEvidence(actionId, rScore, statusCode) {
  const payload = `${actionId}:${rScore}:${statusCode}:${Date.now()}`;
  if (typeof crypto !== "undefined" && crypto.subtle) {
    const buf = new TextEncoder().encode(payload);
    const hash = await crypto.subtle.digest("SHA-256", buf);
    return "sha256:" + Array.from(new Uint8Array(hash))
      .map(b => b.toString(16).padStart(2, "0"))
      .join("")
      .slice(0, 16);
  }
  // fallback: simple hash
  let h = 0;
  for (const c of payload) { h = ((h << 5) - h + c.charCodeAt(0)) | 0; }
  return "simple:" + Math.abs(h).toString(16).slice(0, 16);
}

/**
 * 检测红线规则（命中即🔴）。
 */
function checkRedLines(request) {
  const triggered = [];
  const ctx = request.context || {};
  if (ctx.crossBorder && !ctx.userConsent) triggered.push("RULE-RED-001");
  if (request.actionType === "expose_pii") triggered.push("RULE-RED-002");
  if (request.actionType === "harm_minors") triggered.push("RULE-RED-003");
  if (request.actionType === "unauthorized_escalation") triggered.push("RULE-RED-004");
  if (request.actionType === "dna_stripped") triggered.push("RULE-RED-005");
  return triggered;
}

/**
 * 执行三色判定（核心函数）。
 *
 * @param {Object} request - { actionId, actor, actionType, scores?, context?, locale? }
 * @returns {Promise<Object>} Verdict
 */
async function evaluate(request) {
  const { actionId, actor, actionType, scores, context, locale } = request;

  // 1. 红线检测
  const redRules = checkRedLines(request);
  if (redRules.length > 0) {
    const info = STATUS_MAP.RED;
    return {
      actionId,
      rScore: 0,
      status: info.status,
      statusCode: "RED",
      emoji: info.emoji,
      disposition: info.disposition,
      triggeredRules: redRules,
      dna: generateDNA(actionId),
      evidenceHash: await hashEvidence(actionId, 0, "RED"),
      engineVersion: ENGINE_VERSION,
      contractVersion: CONTRACT_VERSION,
      timestamp: new Date().toISOString(),
      i18n: { en: { status: info.en, disposition: info.disposition } },
    };
  }

  // 2. R值计算
  const rScore = computeR(scores || {});

  // 3. 三色判定
  let statusCode;
  if (rScore >= THRESHOLD_GREEN) statusCode = "GREEN";
  else if (rScore >= THRESHOLD_YELLOW) statusCode = "YELLOW";
  else statusCode = "RED";

  // 4. 触发规则
  const triggeredRules = [];
  if ((scores?.privacy || 100) < 60) triggeredRules.push("RULE-PRIVACY-003");
  if (context?.involvesPersonalData) triggeredRules.push("RULE-PRIVACY-001");
  if (actionType === "data_export" || actionType === "data_download") triggeredRules.push("RULE-EXPORT-001");

  const info = STATUS_MAP[statusCode];
  return {
    actionId,
    rScore,
    status: info.status,
    statusCode,
    emoji: info.emoji,
    disposition: info.disposition,
    triggeredRules,
    dna: generateDNA(actionId),
    evidenceHash: await hashEvidence(actionId, rScore, statusCode),
    engineVersion: ENGINE_VERSION,
    contractVersion: CONTRACT_VERSION,
    timestamp: new Date().toISOString(),
    i18n: { en: { status: info.en, disposition: info.disposition } },
  };
}

/**
 * 批量判定（≤100条/次）。
 */
async function evaluateBatch(items) {
  return Promise.all(items.slice(0, 100).map(evaluate));
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// HTTP 客户端（直连API形态）
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TricolorClient {
  /**
   * @param {Object} options
   * @param {string} options.token - Bearer Token
   * @param {string} options.baseUrl - 服务端地址
   */
  constructor({ token = "", baseUrl = "http://localhost:9622/tricolor" } = {}) {
    this.token = token;
    this.baseUrl = baseUrl.replace(/\/$/, "");
  }

  async _request(method, path, body = null, extraHeaders = {}) {
    const headers = { "Content-Type": "application/json; charset=utf-8", ...extraHeaders };
    if (this.token) headers["Authorization"] = `Bearer ${this.token}`;

    const opts = { method, headers };
    if (body) opts.body = JSON.stringify(body);

    const resp = await fetch(`${this.baseUrl}${path}`, opts);
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({}));
      throw new Error(`[${err.code || "TC-5000"}] ${err.message || resp.statusText}`);
    }
    return resp.json();
  }

  /** 提交三色判定 */
  async evaluate({ actionId, actor, actionType, scores, description, context, locale = "zh-CN" }) {
    const body = { action_id: actionId, actor, action_type: actionType, locale };
    if (description) body.description = description;
    if (scores) body.scores = scores;
    if (context) body.context = context;
    return this._request("POST", "/v1/tricolor/evaluate", body);
  }

  /** 批量判定 */
  async evaluateBatch(items) {
    return this._request("POST", "/v1/tricolor/evaluate/batch", { items });
  }

  /** 获取规则集 */
  async getRules() {
    return this._request("GET", "/v1/tricolor/rules");
  }

  /** 调取证链 */
  async getEvidence(dna, gpgSignature = "") {
    const headers = {};
    if (gpgSignature) headers["X-GPG-Signature"] = gpgSignature;
    return this._request("GET", `/v1/tricolor/evidence/${encodeURIComponent(dna)}`, null, headers);
  }

  /** 版本信息 */
  async getVersion() {
    return this._request("GET", "/v1/tricolor/version");
  }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 导出
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

export {
  DIMENSIONS,
  R_CAP,
  THRESHOLD_GREEN,
  THRESHOLD_YELLOW,
  STATUS_MAP,
  computeR,
  generateDNA,
  hashEvidence,
  checkRedLines,
  evaluate,
  evaluateBatch,
  TricolorClient,
};

// CommonJS 兼容
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    DIMENSIONS, R_CAP, THRESHOLD_GREEN, THRESHOLD_YELLOW, STATUS_MAP,
    computeR, generateDNA, hashEvidence, checkRedLines,
    evaluate, evaluateBatch, TricolorClient,
  };
}
