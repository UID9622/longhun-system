# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 🐉 龍魂·三色审计 JS SDK - 客户端
 * DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-JS-SDK-CLIENT-V1.0-UID9622
 * License: MulanPSL v2
 */

import axios, { AxiosInstance } from "axios";
import { Scores, Verdict, EvidenceChain } from "./models";
import {
  TricolorError,
  RedLineException,
  ReviewRequiredException,
} from "./exceptions";

export class TricolorClient {
  private client: AxiosInstance;
  private baseUrl: string;

  constructor(
    config: { baseUrl?: string; token?: string; timeout?: number } = {}
  ) {
    this.baseUrl = (
      config.baseUrl || "https://uid9622.cn/api/tricolor"
    ).replace(/\/$/, "");
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: config.timeout || 30000,
      headers: {
        "Content-Type": "application/json",
        ...(config.token
          ? { Authorization: `Bearer ${config.token}` }
          : {}),
      },
    });
  }

  async evaluate(params: {
    actionId: string;
    actor: string;
    actionType: string;
    scores?: Scores;
    description?: string;
    context?: Record<string, any>;
    locale?: string;
  }): Promise<Verdict> {
    const payload: any = {
      action_id: params.actionId,
      actor: params.actor,
      action_type: params.actionType,
      locale: params.locale || "zh-CN",
    };
    if (params.scores) payload.scores = params.scores.toJSON();
    if (params.description) payload.description = params.description;
    if (params.context) payload.context = params.context;

    try {
      const resp = await this.client.post("/v1/tricolor/evaluate", payload);
      const verdict = Verdict.fromJSON(resp.data);
      if (verdict.statusCode === "RED") throw new RedLineException(verdict);
      if (verdict.statusCode === "YELLOW")
        throw new ReviewRequiredException(verdict);
      return verdict;
    } catch (err) {
      if (
        err instanceof RedLineException ||
        err instanceof ReviewRequiredException
      )
        throw err;
      if (axios.isAxiosError(err) && err.response) {
        const data = err.response.data;
        throw new TricolorError(
          data.code || "TC-UNKNOWN",
          data.message || "未知错误",
          data.dna || ""
        );
      }
      throw err;
    }
  }

  async getEvidence(dna: string): Promise<EvidenceChain> {
    const resp = await this.client.get(
      `/v1/tricolor/evidence/${encodeURIComponent(dna)}`
    );
    return EvidenceChain.fromJSON(resp.data);
  }

  async getRules(): Promise<any> {
    const resp = await this.client.get("/v1/tricolor/rules");
    return resp.data;
  }

  async getVersion(): Promise<any> {
    const resp = await this.client.get("/v1/tricolor/version");
    return resp.data;
  }
}
