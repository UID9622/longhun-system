/**
 * 🐉 龍魂 · 三才算法引擎（天时·地利·人和）
 * ========================================
 * DNA: #龍芯⚡️丙午·丙申·丁巳·恒卦-SANCAI-ENGINE-v2.1-UID9622
 * License: MulanPSL v2
 *
 * 权重结构（v2.0 设计保留不动）:
 *   天时(timing) 0.34 + 地利(terrain) 0.33 + 人和(human) 0.33 = 1.00
 *
 * 决策分档:
 *   >= 0.7   🟢 自主决策（建议采纳，驾驶员确认即可）
 *   0.4-0.7  🟡 辅助建议（提示给驾驶员，由驾驶员决断）
 *   < 0.4    🔴 建议谨慎（强制提示，但不强制接管——熔断由 RiskFuseEngine 独立判定）
 *
 * 关联: RiskFuseEngine.ets（风险熔断·真实风险因子触发）
 */

export interface SancaiInput {
  // 天时
  timeOfDay: 'dawn' | 'morning' | 'noon' | 'afternoon' | 'evening' | 'night';
  weather: 'clear' | 'cloudy' | 'rainy' | 'snowy' | 'foggy';
  visibility: number;        // 0-1
  temperature: number;       // ℃

  // 地利
  roadType: 'highway' | 'urban' | 'mountain' | 'tunnel' | 'bridge';
  roadCondition: 'good' | 'fair' | 'poor' | 'hazardous';
  trafficLevel: number;      // 0-1
  slope: number;             // 坡度 °

  // 人和
  driverFatigue: number;     // 0-5
  driverExperience: number;  // 0-1
  taskComplexity: number;    // 0-1
  passengerCount: number;
}

export interface SancaiResult {
  score: number;
  grade: 'autonomous' | 'assisted' | 'caution';
  breakdown: {
    timing: number;
    terrain: number;
    human: number;
  };
  suggestion: string;
}

/** 天时评分 */
function scoreTiming(input: SancaiInput): number {
  let s = 1.0;

  // 时段惩罚
  const nightPenalty: Record<string, number> = {
    'night': 0.3, 'dawn': 0.2, 'evening': 0.1
  };
  s -= nightPenalty[input.timeOfDay] ?? 0;

  // 天气惩罚
  const weatherPenalty: Record<string, number> = {
    'foggy': 0.3, 'snowy': 0.25, 'rainy': 0.15
  };
  s -= weatherPenalty[input.weather] ?? 0;

  s *= input.visibility;
  return Math.max(0, Math.min(1, s));
}

/** 地利评分 */
function scoreTerrain(input: SancaiInput): number {
  let s = 1.0;

  const roadPenalty: Record<string, number> = {
    'mountain': 0.25, 'tunnel': 0.15, 'bridge': 0.1
  };
  s -= roadPenalty[input.roadType] ?? 0;

  const conditionPenalty: Record<string, number> = {
    'hazardous': 0.4, 'poor': 0.2, 'fair': 0.1
  };
  s -= conditionPenalty[input.roadCondition] ?? 0;

  s *= (1 - input.trafficLevel * 0.3);
  s *= (1 - Math.abs(input.slope) / 45 * 0.2);
  return Math.max(0, Math.min(1, s));
}

/** 人和评分 */
function scoreHuman(input: SancaiInput): number {
  let s = 1.0;

  // 疲劳递减（非线性：疲劳4+时急剧下降）
  const f = input.driverFatigue;
  if (f <= 2) s -= f * 0.05;
  else if (f <= 3) s -= 0.1 + (f - 2) * 0.15;
  else s -= 0.25 + (f - 3) * 0.25;

  s *= input.driverExperience;
  s *= (1 - input.taskComplexity * 0.4);
  return Math.max(0, Math.min(1, s));
}

export class SancaiEngine {
  /** 三才综合评估 */
  static evaluate(input: SancaiInput): SancaiResult {
    const timing = scoreTiming(input);
    const terrain = scoreTerrain(input);
    const human = scoreHuman(input);

    // 权重固定：天0.34 地0.33 人0.33
    const score = timing * 0.34 + terrain * 0.33 + human * 0.33;

    let grade: SancaiResult['grade'];
    let suggestion: string;

    if (score >= 0.7) {
      grade = 'autonomous';
      suggestion = '🟢 建议采纳自主决策，驾驶员确认即可';
    } else if (score >= 0.4) {
      grade = 'assisted';
      suggestion = '🟡 辅助建议，请驾驶员最终决断';
    } else {
      grade = 'caution';
      suggestion = '🔴 建议谨慎驾驶，请高度注意路况';
    }

    return {
      score: Math.round(score * 100) / 100,
      grade,
      breakdown: {
        timing: Math.round(timing * 100) / 100,
        terrain: Math.round(terrain * 100) / 100,
        human: Math.round(human * 100) / 100
      },
      suggestion
    };
  }
}
