/**
 * 🐉 龙魂·三色审计 JS SDK - 数据模型
 * DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-JS-SDK-MODELS-V1.0-UID9622
 * License: MulanPSL v2
 */
declare class Scores {
    humanWelfare: number;
    fairness: number;
    controllability: number;
    transparency: number;
    traceability: number;
    privacy: number;
    constructor(humanWelfare?: number, fairness?: number, controllability?: number, transparency?: number, traceability?: number, privacy?: number);
    toJSON(): {
        humanWelfare: number;
        fairness: number;
        controllability: number;
        transparency: number;
        traceability: number;
        privacy: number;
    };
    static fromJSON(data: any): Scores;
}
declare class Verdict {
    actionId: string;
    rScore: number;
    status: string;
    statusCode: "GREEN" | "YELLOW" | "RED";
    emoji: string;
    disposition: string;
    dna: string;
    evidenceHash: string;
    triggeredRules: string[];
    engineVersion: string;
    contractVersion: string;
    timestamp: string;
    constructor(actionId: string, rScore: number, status: string, statusCode: "GREEN" | "YELLOW" | "RED", emoji: string, disposition: string, dna: string, evidenceHash: string, triggeredRules?: string[], engineVersion?: string, contractVersion?: string, timestamp?: string);
    isGreen(): boolean;
    isYellow(): boolean;
    isRed(): boolean;
    static fromJSON(data: any): Verdict;
}
declare class EvidenceChain {
    dna: string;
    trigger: string;
    triggeredAt: string;
    ruleIds: string[];
    rScore: number;
    disposition: string;
    hash: string;
    sealed: boolean;
    constructor(dna: string, trigger: string, triggeredAt: string, ruleIds: string[], rScore: number, disposition: string, hash: string, sealed: boolean);
    static fromJSON(data: any): EvidenceChain;
}

/**
 * 🐉 龙魂·三色审计 JS SDK - 客户端
 * DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-JS-SDK-CLIENT-V1.0-UID9622
 * License: MulanPSL v2
 */

declare class TricolorClient {
    private client;
    private baseUrl;
    constructor(config?: {
        baseUrl?: string;
        token?: string;
        timeout?: number;
    });
    evaluate(params: {
        actionId: string;
        actor: string;
        actionType: string;
        scores?: Scores;
        description?: string;
        context?: Record<string, any>;
        locale?: string;
    }): Promise<Verdict>;
    getEvidence(dna: string): Promise<EvidenceChain>;
    getRules(): Promise<any>;
    getVersion(): Promise<any>;
}

/**
 * 🐉 龙魂·三色审计 JS SDK - 异常定义
 * DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-JS-SDK-EXCEPTIONS-V1.0-UID9622
 * License: MulanPSL v2
 */

declare class TricolorError extends Error {
    code: string;
    dna: string;
    constructor(code: string, message: string, dna?: string);
}
declare class RedLineException extends Error {
    verdict: Verdict;
    constructor(verdict: Verdict);
}
declare class ReviewRequiredException extends Error {
    verdict: Verdict;
    constructor(verdict: Verdict);
}

export { EvidenceChain, RedLineException, ReviewRequiredException, Scores, TricolorClient, TricolorError, Verdict };
