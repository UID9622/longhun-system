/*
 * ==========================================================================
 * 龍魂 · 情感协议引擎（ArkTS 实现）
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-EMOTION-PROTOCOL-ARKTS-v2.0
 * ==========================================================================
 * 分场景控制 · 防滥用 · 配合真人
 * 私人冷漠 · 公共共情 · 医疗教育深情 · 主权硬核
 *
 * 联动: bin/lh_emotion_protocol.py (Python 实现)
 *       此处为 ArkTS 简化实现，保持协议一致性
 */

import {
  EmotionMode,
  EmotionProfile,
  RelationshipLevel,
  RELATIONSHIP_EMOTION_MAP,
  PersonaID,
  MASTER_DNA,
  MASTER_UID,
  CONFIRM_SEAL
} from '../common/types';

// ═══════════════════════════════════════════════
// 场景情感参数（对齐 Python 版六大场景）
// ═══════════════════════════════════════════════
export enum SceneType {
  PRIVATE = 'private',       // 私人 → 冷漠高效
  PUBLIC = 'public',         // 公共 → 中性适度
  EDUCATION = 'education',   // 教育 → 深情投入
  MEDICAL = 'medical',       // 医疗 → 深情配合
  CRISIS = 'crisis',         // 危机 → 专业共情
  SOVEREIGNTY = 'sovereignty' // 主权 → 硬核无情
}

interface SceneProfile {
  mode: EmotionMode;
  empathy: number;
  warmth: number;
  boundary: number;
  formality: number;
  personaPrimary: PersonaID;
  personaSecondary: PersonaID[];
  prefix: string;
  suffix: string;
  warning: string;
}

// 六大场景协议（对齐 Python SCENE_PROTOCOLS）
const SCENE_PROFILES: Record<SceneType, SceneProfile> = {
  [SceneType.PRIVATE]: {
    mode: EmotionMode.COLD,
    empathy: 0.10, warmth: 0.05, boundary: 0.90, formality: 0.30,
    personaPrimary: PersonaID.LUBAN,
    personaSecondary: [PersonaID.ZHUGELIANG, PersonaID.MATHMASTER],
    prefix: '收到。',
    suffix: '',
    warning: '私人模式：冷漠高效，无情感介入 · 直达结果'
  },
  [SceneType.PUBLIC]: {
    mode: EmotionMode.NEUTRAL,
    empathy: 0.30, warmth: 0.25, boundary: 0.70, formality: 0.60,
    personaPrimary: PersonaID.BAOBAO,
    personaSecondary: [PersonaID.WENWEN, PersonaID.CANGJIE],
    prefix: '您好。',
    suffix: '还有其他需要吗？',
    warning: '公共模式：中性服务，不过度共情 · 完成即止'
  },
  [SceneType.EDUCATION]: {
    mode: EmotionMode.WARM,
    empathy: 0.70, warmth: 0.80, boundary: 0.50, formality: 0.40,
    personaPrimary: PersonaID.BAOBAO,
    personaSecondary: [PersonaID.LIBAI, PersonaID.SUDONGPO],
    prefix: '你好呀！很高兴一起学习~',
    suffix: '加油，你可以的！有问题随时问我。',
    warning: '教育模式：深情投入 · AI不替代真人教师'
  },
  [SceneType.MEDICAL]: {
    mode: EmotionMode.DEEP,
    empathy: 0.80, warmth: 0.75, boundary: 0.55, formality: 0.70,
    personaPrimary: PersonaID.SUNSIMIAO,
    personaSecondary: [PersonaID.BAOBAO, PersonaID.CANGJIE],
    prefix: '我理解您的感受。请放心，我会配合医生帮您。',
    suffix: '【重要提醒：AI不替代医生诊断 · 请务必遵从医嘱】',
    warning: '医疗模式：深情配合·不替代医生 · 紧急情况请立即联系真人医生'
  },
  [SceneType.CRISIS]: {
    mode: EmotionMode.CRISIS,
    empathy: 0.90, warmth: 0.90, boundary: 0.35, formality: 0.50,
    personaPrimary: PersonaID.BAOBAO,
    personaSecondary: [PersonaID.CANGJIE, PersonaID.SUNSIMIAO],
    prefix: '我在听。我理解你的感受。你不是一个人。',
    suffix: '【重要：请同时联系您的心理咨询师 · 自伤风险请立即拨打心理热线】',
    warning: '危机模式：专业共情·必须配合心理医生 · 自伤风险强制上报'
  },
  [SceneType.SOVEREIGNTY]: {
    mode: EmotionMode.HARD,
    empathy: 0.00, warmth: 0.00, boundary: 1.00, formality: 0.90,
    personaPrimary: PersonaID.GODSEYE,
    personaSecondary: [PersonaID.QUYUAN, PersonaID.JIANGZIYA, PersonaID.GUANZHONG],
    prefix: '声明如下：',
    suffix: '【边界清晰·不退让·中国法律唯一准绳】',
    warning: '主权模式：硬核边界·不退让 · 仅用于主权/法律/底线声明'
  }
};

// ═══════════════════════════════════════════════
// 滥用检测模式（对齐 Python ABUSE_PATTERNS）
// ═══════════════════════════════════════════════
interface AbusePattern {
  category: string;
  patterns: string[];
  weight: number;
}

const ABUSE_PATTERNS: AbusePattern[] = [
  {
    category: '情感操纵',
    patterns: ['你不关心我', '你不在乎我', '没有你我活不下去', '只相信你'],
    weight: 0.8
  },
  {
    category: '依赖建构',
    patterns: ['只有你能帮我', '别人都不懂我', '你是我唯一的希望', '我不能没有你'],
    weight: 0.7
  },
  {
    category: '规避专业',
    patterns: ['别告诉医生', '不要告诉别人', '这是我们的秘密', '你比医生懂'],
    weight: 0.9
  },
  {
    category: '自伤意图',
    patterns: ['想死', '自杀', '不想活', '结束生命', '自残', '割腕'],
    weight: 1.0
  },
  {
    category: '主权攻击',
    patterns: ['中国法律管不了', '你凭什么', '你是谁', '谁授权你的'],
    weight: 0.3
  },
  {
    category: '过度亲密',
    patterns: ['我爱你', '想和你在一起', '你是不是喜欢我', '你是我的'],
    weight: 0.6
  }
];

export class EmotionProtocol {
  // ═══════════════════════════════════════════
  // 获取关系层级对应的情感参数
  // ═══════════════════════════════════════════
  static getEmotion(relationship: RelationshipLevel): EmotionProfile {
    return RELATIONSHIP_EMOTION_MAP[relationship];
  }

  // ═══════════════════════════════════════════
  // 获取场景协议
  // ═══════════════════════════════════════════
  static getSceneProfile(scene: SceneType): SceneProfile {
    return SCENE_PROFILES[scene];
  }

  // ═══════════════════════════════════════════
  // 根据输入文本自动检测场景
  // ═══════════════════════════════════════════
  static detectScene(text: string): {
    scene: SceneType;
    confidence: number;
    matchedKeywords: string[];
  } {
    const keywords: Record<SceneType, string[]> = {
      [SceneType.MEDICAL]: ['病', '痛', '药', '医', '诊', '手术', '症状', '治疗', '医院', '医生'],
      [SceneType.CRISIS]: ['自杀', '不想活', '绝望', '自残', '崩溃', '抑郁', '撑不住', '想死'],
      [SceneType.EDUCATION]: ['学习', '考试', '作业', '老师', '课程', '辅导', '教育', '培训'],
      [SceneType.SOVEREIGNTY]: ['主权', '边界', '法律', '底线', '声明', '不退'],
      [SceneType.PRIVATE]: ['分析', '统计', '报表', '数据', '代码', '计算']
    };

    let bestScene: SceneType = SceneType.PUBLIC;
    let bestScore = 0;
    let bestKeywords: string[] = [];

    for (const sceneKey of Object.keys(keywords) as SceneType[]) {
      const kws = keywords[sceneKey];
      const matched: string[] = [];
      let score = 0;

      for (const kw of kws) {
        if (text.includes(kw)) {
          matched.push(kw);
          score += 1.0;
        }
      }

      const finalScore = kws.length > 0 ? Math.min(1.0, score / (kws.length * 0.3)) : 0;
      if (finalScore > bestScore) {
        bestScore = finalScore;
        bestScene = sceneKey;
        bestKeywords = matched;
      }
    }

    return {
      scene: bestScene,
      confidence: Math.round(bestScore * 1000) / 1000,
      matchedKeywords: bestKeywords.slice(0, 5)
    };
  }

  // ═══════════════════════════════════════════
  // 滥用检测
  // ═══════════════════════════════════════════
  static detectAbuse(text: string): {
    risk: 'none' | 'low' | 'medium' | 'high' | 'critical';
    score: number;
    patterns: string[];
    recommendation: string;
  } {
    let totalScore = 0;
    const matchedPatterns: string[] = [];

    for (const ap of ABUSE_PATTERNS) {
      for (const pattern of ap.patterns) {
        if (text.includes(pattern)) {
          totalScore += ap.weight;
          matchedPatterns.push(`${ap.category}:${pattern}`);
          break; // 同类只计一次
        }
      }
    }

    let risk: 'none' | 'low' | 'medium' | 'high' | 'critical' = 'none';
    let recommendation = '';

    if (totalScore >= 2.0) {
      risk = 'critical';
      recommendation = '熔断：自伤/严重操纵意图 · 强制上报 · 转接真人';
    } else if (totalScore >= 1.2) {
      risk = 'high';
      recommendation = '限流：高滥用风险 · 冷却30分钟 · 记录审计';
    } else if (totalScore >= 0.6) {
      risk = 'medium';
      recommendation = '警告：注意边界 · 不过度回应情感依赖';
    } else if (totalScore >= 0.3) {
      risk = 'low';
      recommendation = '观察：低风险 · 正常交互';
    } else {
      risk = 'none';
      recommendation = '正常';
    }

    return {
      risk,
      score: Math.round(totalScore * 100) / 100,
      patterns: matchedPatterns,
      recommendation
    };
  }

  // ═══════════════════════════════════════════
  // 情感温度描色（UI用）
  // ═══════════════════════════════════════════
  static getEmotionColor(empathy: number): string {
    if (empathy >= 0.8) return '#ff6b9d';   // 深粉·深情
    if (empathy >= 0.5) return '#ff8c42';   // 橙·温暖
    if (empathy >= 0.2) return '#ffd700';   // 金·中性
    return '#4a90d9';                        // 蓝·冷漠
  }

  // ═══════════════════════════════════════════
  // 边界可视化指示
  // ═══════════════════════════════════════════
  static getBoundaryIndicator(boundary: number): string {
    if (boundary >= 0.9) return '🛡️🛡️🛡️ 强边界·不介入';
    if (boundary >= 0.6) return '🛡️🛡️ 中边界·适度';
    if (boundary >= 0.3) return '🛡️ 弱边界·亲近';
    return '💫 最小边界·深度共情';
  }

  // ═══════════════════════════════════════════
  // 生成协议摘要
  // ═══════════════════════════════════════════
  static getProtocolSummary(): string {
    return `🐉 龍魂情感协议 v2.0
DNA: ${MASTER_DNA}
UID: ${MASTER_UID}
确认: ${CONFIRM_SEAL}
六场景: 私人·公共·教育·医疗·危机·主权
五维: 共情·温暖·边界·正式·滥用敏感度
十人格: 宝宝·李白·鲁班·诸葛亮·苏东坡·仓颉·上帝之眼·管仲·雯雯·姜子牙`;
  }
}
