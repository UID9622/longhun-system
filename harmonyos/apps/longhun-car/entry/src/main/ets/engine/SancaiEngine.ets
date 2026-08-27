/**
 * 🐉 龍魂 · 三才算法引擎
 * 天时(0.34) + 地利(0.33) + 人和(0.33) = 决策
 * 不是算路，是算"该不该走"
 * License: MulanPSL v2
 * DNA: #龍芯⚡️2026-08-11-CAR-SANCAI-ENGINE-v2.0-UID9622
 */

export interface SancaiInput {
  // 天时
  weather: 'sunny' | 'rainy' | 'snowy' | 'foggy' | 'windy';
  temperature: number;
  timeOfDay: 'dawn' | 'morning' | 'noon' | 'afternoon' | 'dusk' | 'night';
  // 地利
  trafficLevel: 0 | 1 | 2 | 3 | 4 | 5;
  roadCondition: 'excellent' | 'good' | 'fair' | 'poor' | 'hazardous';
  terrain: 'flat' | 'hilly' | 'mountainous' | 'urban' | 'rural';
  // 人和
  driverFatigue: 0 | 1 | 2 | 3 | 4 | 5;
  passengerComfort: 0 | 1 | 2 | 3 | 4 | 5;
  urgencyLevel: 0 | 1 | 2 | 3 | 4 | 5;
}

export interface SancaiOutput {
  score: number;
  decision: 'proceed' | 'caution' | 'reroute' | 'stop' | 'manual_override';
  hexagram: string;
  description: string;
  details: {
    heaven: number;
    earth: number;
    human: number;
  };
}

export class SancaiEngine {
  private static WEATHER_WEIGHTS: Record<string, number> = {
    sunny: 0.9, rainy: 0.6, snowy: 0.3, foggy: 0.2, windy: 0.5
  };

  private static TRAFFIC_WEIGHTS: Record<number, number> = {
    0: 1.0, 1: 0.9, 2: 0.7, 3: 0.5, 4: 0.3, 5: 0.1
  };

  private static FATIGUE_WEIGHTS: Record<number, number> = {
    0: 1.0, 1: 0.9, 2: 0.8, 3: 0.6, 4: 0.4, 5: 0.2
  };

  /**
   * 三才决策引擎
   */
  static evaluate(input: SancaiInput): SancaiOutput {
    const heaven = this.calculateHeaven(input);
    const earth = this.calculateEarth(input);
    const human = this.calculateHuman(input);
    const score = heaven * 0.34 + earth * 0.33 + human * 0.33;
    const digitalRoot = this.digitalRoot(Math.round(score * 100));

    let decision: SancaiOutput['decision'];
    let hexagram: string;
    let description: string;

    if (digitalRoot === 3 || digitalRoot === 9) {
      decision = 'manual_override';
      hexagram = digitalRoot === 3 ? '震卦' : '艮卦';
      description = digitalRoot === 3
        ? '天时异常，建议人工确认'
        : '高危场景，强制人工接管';
    } else if (score >= 0.8) {
      decision = 'proceed';
      hexagram = '乾卦';
      description = '天时地利人和，畅通无阻';
    } else if (score >= 0.6) {
      decision = 'caution';
      hexagram = '坤卦';
      description = '条件一般，谨慎驾驶';
    } else if (score >= 0.4) {
      decision = 'reroute';
      hexagram = '坎卦';
      description = '路况不佳，建议绕行';
    } else {
      decision = 'stop';
      hexagram = '离卦';
      description = '危险！立即停车';
    }

    return {
      score,
      decision,
      hexagram,
      description,
      details: {
        heaven: Math.round(heaven * 100) / 100,
        earth: Math.round(earth * 100) / 100,
        human: Math.round(human * 100) / 100
      }
    };
  }

  private static calculateHeaven(input: SancaiInput): number {
    const weatherWeight = this.WEATHER_WEIGHTS[input.weather] || 0.5;
    const timeWeight = input.timeOfDay === 'night' ? 0.5 : 1.0;
    return Math.min(1, weatherWeight * timeWeight);
  }

  private static calculateEarth(input: SancaiInput): number {
    const trafficWeight = this.TRAFFIC_WEIGHTS[input.trafficLevel] || 0.5;
    const roadWeightMap: Record<string, number> = {
      excellent: 1.0, good: 0.9, fair: 0.7, poor: 0.4, hazardous: 0.2
    };
    const roadWeight = roadWeightMap[input.roadCondition] || 0.5;
    return Math.min(1, trafficWeight * roadWeight);
  }

  private static calculateHuman(input: SancaiInput): number {
    const fatigueWeight = this.FATIGUE_WEIGHTS[input.driverFatigue] || 0.5;
    const comfortWeight = 1 - (input.passengerComfort / 5) * 0.3;
    const urgencyWeight = 0.5 + (input.urgencyLevel / 5) * 0.5;
    return Math.min(1, fatigueWeight * 0.4 + comfortWeight * 0.3 + urgencyWeight * 0.3);
  }

  /**
   * 数字根计算
   */
  private static digitalRoot(n: number): number {
    while (n >= 10) {
      let sum = 0;
      while (n > 0) {
        sum += n % 10;
        n = Math.floor(n / 10);
      }
      n = sum;
    }
    return n;
  }
}

/**
 * 道德经注释
 * 第8章: "上善若水" → 三才如水，适应万物
 * 第25章: "道法自然" → 决策遵循自然规律
 * 第63章: "图难于其易，为大于其细" → 从易处着手，由细处积累
 */
