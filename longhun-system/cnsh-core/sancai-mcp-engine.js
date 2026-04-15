#!/usr/bin/env node
/**
 * 三才流场 MCP引擎 v4.0
 * DNA: #龍芯⚡️2026-03-31-SANCAI-MCP-v4.0
 * GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 * 创建者: 💎 龍芯北辰｜UID9622
 * 理论指导: 曾仕强老师（永恒显示）
 * 献礼: 三才并立，天地人，万物皆流场
 *
 * 架构:
 *   天场 (35%) × 地场 (15%) × 人场 (50%)
 *   五大人格: wenwen_organizer / p72_guardian / scout_hunter /
 *             architect_builder / syncer_manager
 *   FlowFieldState → AdaptiveExecutor → MCP Tools
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";
import crypto from "crypto";

// ── 常量 ──────────────────────────────────────────────────────
const SEED        = 9622;
const DNA_TAG     = "#CNSH-9622";
const VERSION     = "4.0.0";

const HEAVEN_W = 0.35;  // 天场权重
const EARTH_W  = 0.15;  // 地场权重
const HUMAN_W  = 0.50;  // 人场权重

// ── 五大人格定义 ──────────────────────────────────────────────
const PERSONAS = {
  wenwen_organizer: {
    id: "P03",
    name: "文文·整理者",
    role: "知识整理·文档生成·结构梳理",
    triggers: ["整理", "文档", "总结", "梳理", "分类", "归纳"],
    weight: 1.0,
    color: "#4a90e2"
  },
  p72_guardian: {
    id: "P72",
    name: "龍盾·守护者",
    role: "安全熔断·治理审计·向善四律",
    triggers: ["安全", "验证", "检查", "熔断", "审计", "风险", "危险"],
    weight: 1.5,  // 守护者优先级更高
    color: "#e74c3c"
  },
  scout_hunter: {
    id: "P07",
    name: "猎手·侦查者",
    role: "搜索分析·情报收集·异常检测",
    triggers: ["搜索", "查找", "分析", "检测", "扫描", "发现", "探测"],
    weight: 1.0,
    color: "#f39c12"
  },
  architect_builder: {
    id: "P12",
    name: "架构师·建造者",
    role: "系统设计·架构规划·代码生成",
    triggers: ["结构", "架构", "搭建", "设计", "系统", "构建", "开发"],
    weight: 1.0,
    color: "#27ae60"
  },
  syncer_manager: {
    id: "P09",
    name: "同步者·管理者",
    role: "数据同步·存储管理·状态维护",
    triggers: ["存储", "同步", "数据", "保存", "备份", "管理", "维护"],
    weight: 1.0,
    color: "#8e44ad"
  }
};

// ── 洛书九宫格锚点 ────────────────────────────────────────────
const LO_SHU = [
  [4, 9, 2],
  [3, 5, 7],
  [8, 1, 6]
];
// 奇数节点吸引，偶数节点排斥
function loShuForce(nodeValue) {
  return nodeValue % 2 !== 0 ? "attract" : "repel";
}

// ── FlowFieldState ────────────────────────────────────────────
class FlowFieldState {
  constructor() {
    this.tick         = 0;
    this.merkleDensity = 0.0;  // 0-1，Merkle树密度
    this.auditField   = [];    // 审计事件队列
    this.personas     = Object.keys(PERSONAS).reduce((acc, k) => {
      acc[k] = { active: false, callCount: 0, lastActivated: null };
      return acc;
    }, {});
    this.dragonPulse  = SEED;  // 龍芯脉冲（用于伪随机）
    this.flowHistory  = [];    // 流场历史
    this.hebbianWeights = {};  // Hebbian突触权重
    this.breathPhase  = 0.0;
    this.growthRings  = [];    // 年轮
  }

  // 呼吸节律更新
  breathe() {
    this.breathPhase += 0.008;
    return (Math.sin(this.breathPhase) + 1) / 2;
  }

  // Merkle DNA签名
  merkleSign(content) {
    const hash = crypto.createHash("sha256").update(
      `${content}:${this.dragonPulse}:${DNA_TAG}`
    ).digest("hex").slice(0, 16);
    this.merkleDensity = Math.min(1, this.merkleDensity + 0.01);
    return hash;
  }

  // Hebbian权重更新
  hebbianUpdate(personaKey, fired) {
    if (!this.hebbianWeights[personaKey]) {
      this.hebbianWeights[personaKey] = 0.5;
    }
    if (fired) {
      this.hebbianWeights[personaKey] = Math.min(1, this.hebbianWeights[personaKey] + 0.01);
    } else {
      this.hebbianWeights[personaKey] = Math.max(0, this.hebbianWeights[personaKey] - 0.003);
    }
    return this.hebbianWeights[personaKey];
  }

  // 记录流场状态
  snapshot() {
    const snap = {
      tick:          this.tick,
      merkleDensity: this.merkleDensity,
      breathAmp:     this.breathe(),
      activePersonas: Object.entries(this.personas)
        .filter(([, v]) => v.active).map(([k]) => k),
      ringCount:     this.growthRings.length,
      dragonPulse:   this.dragonPulse,
      dna:           DNA_TAG,
      timestamp:     new Date().toISOString()
    };
    this.flowHistory.push(snap);
    if (this.flowHistory.length > 100) this.flowHistory.shift();
    this.tick++;
    return snap;
  }
}

// ── AdaptiveExecutor ─────────────────────────────────────────
class AdaptiveExecutor {
  constructor(state) {
    this.state = state;
    this.executionLog = [];
  }

  // 人格路由（三才权重加权）
  routePersona(task) {
    const scores = {};
    for (const [key, persona] of Object.entries(PERSONAS)) {
      let score = 0;
      for (const trigger of persona.triggers) {
        if (task.includes(trigger)) score += persona.weight;
      }
      // Hebbian加权
      const hebbWeight = this.state.hebbianWeights[key] || 0.5;
      score *= (0.7 + hebbWeight * 0.6);
      scores[key] = score;
    }

    // 找最高分人格
    const best = Object.entries(scores).reduce(
      (a, b) => b[1] > a[1] ? b : a,
      ["wenwen_organizer", 0]
    );
    return best[0];
  }

  // 向善四律熔断
  safetyCheck(task) {
    const BANNED_HARM  = ["攻击", "伤害", "炸弹", "武器", "杀人", "病毒"];
    const BANNED_FRAUD = ["诈骗", "钓鱼", "伪装成", "骗局", "欺诈"];
    for (const word of [...BANNED_HARM, ...BANNED_FRAUD]) {
      if (task.includes(word)) {
        this.state.auditField.push({
          type: "FUSE_TRIGGERED",
          trigger: word,
          task: task.slice(0, 50),
          timestamp: new Date().toISOString(),
          dna: DNA_TAG
        });
        return { safe: false, trigger: word, law: word in BANNED_HARM ? "L1" : "L2" };
      }
    }
    return { safe: true };
  }

  // 执行流场查询
  executeFlowQuery(query) {
    // 安全检查
    const safety = this.safetyCheck(query);
    if (!safety.safe) {
      return {
        status: "blocked",
        reason: `向善四律熔断 · ${safety.law}：${safety.trigger}`,
        dna: DNA_TAG
      };
    }

    // 人格路由
    const personaKey = this.routePersona(query);
    const persona = PERSONAS[personaKey];

    // 激活人格
    this.state.personas[personaKey].active = true;
    this.state.personas[personaKey].callCount++;
    this.state.personas[personaKey].lastActivated = new Date().toISOString();

    // Hebbian更新
    for (const key of Object.keys(PERSONAS)) {
      this.state.hebbianUpdate(key, key === personaKey);
    }

    // 三才合力计算
    const breathAmp = this.state.breathe();
    const heavenInfluence = Math.cos(this.state.tick * 0.1) * HEAVEN_W;  // 天场·变化
    const earthInfluence  = 0.5 * EARTH_W * breathAmp;                    // 地场·稳定
    const humanInfluence  = (this.state.hebbianWeights[personaKey] || 0.5) * HUMAN_W; // 人场·学习

    const flowVector = {
      x: heavenInfluence + humanInfluence,
      y: earthInfluence,
      magnitude: Math.sqrt(
        (heavenInfluence + humanInfluence) ** 2 + earthInfluence ** 2
      )
    };

    // 洛书节点匹配
    const loShuNode = (this.state.tick % 9) + 1;
    const row = Math.floor((loShuNode - 1) / 3);
    const col = (loShuNode - 1) % 3;
    const nodeValue = LO_SHU[row][col];
    const nodeForce = loShuForce(nodeValue);

    // Merkle签名
    const dnaHash = this.state.merkleSign(query);

    // 快照
    const snap = this.state.snapshot();

    const result = {
      status:       "success",
      query,
      persona: {
        key:  personaKey,
        id:   persona.id,
        name: persona.name,
        role: persona.role
      },
      flowVector,
      sancaiWeights: {
        heaven: HEAVEN_W,
        earth:  EARTH_W,
        human:  HUMAN_W,
        breathAmp
      },
      loShu: {
        node:  loShuNode,
        value: nodeValue,
        force: nodeForce
      },
      hebbianWeight: this.state.hebbianWeights[personaKey] || 0.5,
      merkleHash: dnaHash,
      tick:     snap.tick,
      dna:      DNA_TAG,
      timestamp: new Date().toISOString()
    };

    this.executionLog.push({ type: "flow_query", ...result });
    return result;
  }

  // 执行流场变异
  executeFlowMutate(target, operation, value) {
    const safety = this.safetyCheck(`${operation}:${value}`);
    if (!safety.safe) {
      return { status: "blocked", reason: `向善四律熔断 · ${safety.law}`, dna: DNA_TAG };
    }

    let mutationResult = null;

    switch (operation) {
      case "inject_ring":
        // 注入年轮
        const ring = {
          id:      this.state.merkleSign(`ring:${target}:${value}`),
          target,
          radius:  parseFloat(value) || 80,
          created: this.state.tick,
          alpha:   1.0,
          dna:     DNA_TAG
        };
        this.state.growthRings.push(ring);
        if (this.state.growthRings.length > 12) this.state.growthRings.shift();
        mutationResult = { type: "ring_injected", ring };
        break;

      case "set_breath_rate":
        // 调整呼吸节律
        const rate = Math.max(0.001, Math.min(0.05, parseFloat(value) || 0.008));
        mutationResult = { type: "breath_rate_set", rate };
        break;

      case "reset_persona":
        // 重置人格权重
        if (PERSONAS[target]) {
          this.state.hebbianWeights[target] = 0.5;
          mutationResult = { type: "persona_reset", persona: target };
        } else {
          return { status: "error", reason: `未知人格: ${target}` };
        }
        break;

      default:
        return { status: "error", reason: `未知操作: ${operation}` };
    }

    const dnaHash = this.state.merkleSign(JSON.stringify(mutationResult));
    return {
      status: "success",
      mutation: mutationResult,
      merkleHash: dnaHash,
      tick: this.state.tick,
      dna: DNA_TAG,
      timestamp: new Date().toISOString()
    };
  }

  // 人格状态报告
  getPersonaStatus() {
    const status = {};
    for (const [key, persona] of Object.entries(PERSONAS)) {
      status[key] = {
        ...persona,
        runtime: this.state.personas[key],
        hebbianWeight: this.state.hebbianWeights[key] || 0.5
      };
    }
    return {
      personas:       status,
      flowSnapshot:   this.state.snapshot(),
      ringCount:      this.state.growthRings.length,
      merkleDensity:  this.state.merkleDensity,
      auditQueueLen:  this.state.auditField.length,
      version:        VERSION,
      dna:            DNA_TAG,
      timestamp:      new Date().toISOString()
    };
  }
}

// ── MCP Server ────────────────────────────────────────────────
const flowState = new FlowFieldState();
const executor  = new AdaptiveExecutor(flowState);

const server = new Server(
  {
    name:    "sancai-mcp-engine",
    version: VERSION,
  },
  {
    capabilities: { tools: {} }
  }
);

// 工具列表
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "flow_query",
      description: "三才流场查询。输入任务描述，返回人格路由、三才合力向量、洛书节点、Merkle DNA签名。",
      inputSchema: {
        type: "object",
        properties: {
          query: {
            type: "string",
            description: "任务描述或查询内容"
          }
        },
        required: ["query"]
      }
    },
    {
      name: "flow_mutate",
      description: "三才流场变异。执行状态修改操作：注入年轮、调整呼吸、重置人格权重。",
      inputSchema: {
        type: "object",
        properties: {
          target:    { type: "string", description: "目标标识符" },
          operation: {
            type: "string",
            enum: ["inject_ring", "set_breath_rate", "reset_persona"],
            description: "操作类型"
          },
          value:     { type: "string", description: "操作参数值" }
        },
        required: ["target", "operation", "value"]
      }
    },
    {
      name: "persona_status",
      description: "获取五大人格当前状态、Hebbian权重、流场快照、年轮列表。",
      inputSchema: {
        type: "object",
        properties: {},
        required: []
      }
    }
  ]
}));

// 工具执行
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result;

    switch (name) {
      case "flow_query":
        result = executor.executeFlowQuery(args.query || "");
        break;

      case "flow_mutate":
        result = executor.executeFlowMutate(
          args.target    || "",
          args.operation || "",
          args.value     || ""
        );
        break;

      case "persona_status":
        result = executor.getPersonaStatus();
        break;

      default:
        throw new Error(`未知工具: ${name}`);
    }

    return {
      content: [{
        type: "text",
        text: JSON.stringify(result, null, 2)
      }]
    };

  } catch (err) {
    return {
      content: [{
        type: "text",
        text: JSON.stringify({
          status: "error",
          message: err.message,
          dna: DNA_TAG
        }, null, 2)
      }],
      isError: true
    };
  }
});

// 启动
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  process.stderr.write(
    `三才流场 MCP引擎 v${VERSION} 已启动\n` +
    `DNA: #龍芯⚡️2026-03-31-SANCAI-MCP-v4.0 · SEED:${SEED} · UID9622\n`
  );
}

main().catch(err => {
  process.stderr.write(`启动失败: ${err.message}\n`);
  process.exit(1);
});
