/**
 * 🐉 龍魂 · 风险因子熔断引擎 v2.1
 * =================================
 * DNA: #龍芯⚡️丙午·丙申·丁巳·恒卦-RISK-FUSE-v2.1-UID9622
 * License: MulanPSL v2
 *
 * v2.0→v2.1 修正:
 *   v2.0 用"得分数字根为3或9"触发强制人工接管
 *   → 约 2/9 决策被伪随机拦截，与真实风险无关 —— "安全剧场"
 *   v2.1 熔断只看真实风险因子：
 *     🔴 强制人工接管：疲劳≥4 / 危险路况 / 恶劣天气夜间
 *     🟡 建议人工确认：疲劳3 / 雨夜 / 较差路况
 *     数字根降级为审计标签，写进史官记录供回溯，不参与安全决策
 *
 * 参考来源: Kimi三色审计安全复盘
 * 关联: SancaiEngine.ets（三才评估）→ RiskFuseEngine（熔断判定）
 */

import { SancaiInput } from './SancaiEngine';

export interface FuseResult {
  approved: boolean;
  level: 'normal' | 'caution' | 'fuse';
  triggers: string[];       // 命中的真实风险因子（可解释！）
  digitalRootTag: number;   // 审计标签，仅记录不拦截
}

export class RiskFuseEngine {
  /** 熔断判定：只看真实风险因子 */
  static process(input: SancaiInput, score: number): FuseResult {
    const triggers: string[] = [];
    let level: FuseResult['level'] = 'normal';

    // 🔴 强制人工接管（任一命中）
    if (input.driverFatigue >= 4) {
      triggers.push('驾驶员疲劳等级≥4（真实生理风险）');
      level = 'fuse';
    }
    if (input.roadCondition === 'hazardous') {
      triggers.push('危险路况（hazardous）');
      level = 'fuse';
    }
    if ((input.weather === 'snowy' || input.weather === 'foggy')
        && input.timeOfDay === 'night') {
      triggers.push('恶劣天气+夜间复合风险');
      level = 'fuse';
    }

    // 🟡 建议人工确认（任一命中，且不高于已有级别）
    if (level === 'normal') {
      if (input.driverFatigue === 3) {
        triggers.push('疲劳等级3');
        level = 'caution';
      }
      if (input.weather === 'rainy' && input.timeOfDay === 'night') {
        triggers.push('雨夜');
        level = 'caution';
      }
      if (input.roadCondition === 'poor') {
        triggers.push('较差路况');
        level = 'caution';
      }
    }

    return {
      approved: level === 'normal',
      level,
      triggers,
      // 数字根降级为审计标签，不参与安全决策
      digitalRootTag: RiskFuseEngine.digitalRoot(Math.round(score * 100))
    };
  }

  /** 数字根：降级为审计标签，写进史官记录供回溯分析 */
  static digitalRoot(n: number): number {
    while (n >= 10) {
      let s = 0;
      while (n > 0) {
        s += n % 10;
        n = Math.floor(n / 10);
      }
      n = s;
    }
    return n;
  }
}
