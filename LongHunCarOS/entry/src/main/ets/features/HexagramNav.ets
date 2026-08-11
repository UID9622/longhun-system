/**
 * 🐉 龍魂 · 五泉十景卦象导航
 * 路况用卦象表达：坎=水=堵车，离=火=事故，乾=天=畅通
 * 五泉十景：金泉(乾)、木泉(震)、水泉(坎)、火泉(离)、土泉(坤)
 * License: MulanPSL v2
 * DNA: #龍芯⚡️2026-08-11-CAR-HEXAGRAM-NAV-v2.0-UID9622
 */
import { GanzhiUtil } from '../common/utils/GanzhiUtil';

export interface HexagramNavData {
  hexagram: string;
  meaning: string;
  color: string;
  suggestion: string;
  confidence: number;
  dna: string;
  wuquanShijing?: string;
  scenicScore?: number;
}

export class HexagramNav {
  private static HEXAGRAM_MAP: Record<string, { meaning: string; color: string; suggestion: string; wuquan?: string }> = {
    '坎卦': { meaning: '水 · 堵车', color: '#4a90d9', suggestion: '建议绕行，耐心等待', wuquan: '水泉' },
    '离卦': { meaning: '火 · 事故', color: '#d94a4a', suggestion: '立即减速，注意避让', wuquan: '火泉' },
    '坤卦': { meaning: '地 · 施工', color: '#d9b44a', suggestion: '注意警示，提前变道', wuquan: '土泉' },
    '乾卦': { meaning: '天 · 畅通', color: '#4ad94a', suggestion: '正常通行，保持车速', wuquan: '金泉' },
    '震卦': { meaning: '雷 · 急刹', color: '#d97a4a', suggestion: '保持警惕，控制车距', wuquan: '木泉' },
    '巽卦': { meaning: '风 · 变道', color: '#8a8ad9', suggestion: '注意后方，安全变道', wuquan: '风泉' },
    '兑卦': { meaning: '泽 · 积水', color: '#4ad9d9', suggestion: '减速通过，防止水滑', wuquan: '泽泉' },
    '艮卦': { meaning: '山 · 慢行', color: '#8a8a8a', suggestion: '减速慢行，注意观察', wuquan: '山泉' }
  };

  private static SHIJING_SCENES = [
    '金泉观日', '木泉听风', '水泉映月', '火泉观霞', '土泉望岳',
    '风泉抚松', '泽泉观荷', '山泉望云', '雷泉听雨', '天泉观星'
  ];

  /**
   * 根据路况生成卦象
   */
  static evaluate(roadCondition: {
    trafficLevel: 0 | 1 | 2 | 3 | 4 | 5;
    hasAccident: boolean;
    hasConstruction: boolean;
    weather: string;
    isNight: boolean;
    scenicType?: string;
  }): HexagramNavData {
    let hexagram = '乾卦';
    let confidence = 0.8;
    let wuquan = '金泉';
    let scenicScore = 85;

    if (roadCondition.hasAccident) {
      hexagram = '离卦'; confidence = 0.95; wuquan = '火泉'; scenicScore = 30;
    } else if (roadCondition.hasConstruction) {
      hexagram = '坤卦'; confidence = 0.85; wuquan = '土泉'; scenicScore = 50;
    } else if (roadCondition.trafficLevel >= 4) {
      hexagram = '坎卦'; confidence = 0.9; wuquan = '水泉'; scenicScore = 40;
    } else if (roadCondition.trafficLevel >= 2) {
      hexagram = '艮卦'; confidence = 0.7; wuquan = '山泉'; scenicScore = 60;
    } else if (roadCondition.weather === 'rainy' || roadCondition.weather === 'snowy') {
      hexagram = '兑卦'; confidence = 0.75; wuquan = '泽泉'; scenicScore = 55;
    }

    if (roadCondition.scenicType) {
      scenicScore = this.calculateScenicScore(roadCondition.scenicType, hexagram);
    }

    const info = this.HEXAGRAM_MAP[hexagram] || this.HEXAGRAM_MAP['乾卦'];

    return {
      hexagram,
      meaning: info.meaning,
      color: info.color,
      suggestion: info.suggestion,
      confidence,
      dna: `#龍芯⚡️${GanzhiUtil.getCurrentGanzhi()}·${hexagram}-NAV-${Date.now().toString(36)}-UID9622`,
      wuquanShijing: `${wuquan} · ${this.getRandomScene()}`,
      scenicScore
    };
  }

  private static calculateScenicScore(scenicType: string, hexagram: string): number {
    const baseScores: Record<string, number> = {
      'mountain': 90, 'lake': 85, 'forest': 80, 'urban': 70, 'rural': 75
    };
    const hexagramModifiers: Record<string, number> = {
      '乾卦': 10, '坤卦': 5, '坎卦': -20, '离卦': -30,
      '震卦': -10, '巽卦': 0, '艮卦': 8, '兑卦': -15
    };
    const baseScore = baseScores[scenicType] || 70;
    const modifier = hexagramModifiers[hexagram] || 0;
    return Math.max(0, Math.min(100, baseScore + modifier));
  }

  private static getRandomScene(): string {
    const idx = Math.floor(Math.random() * this.SHIJING_SCENES.length);
    return this.SHIJING_SCENES[idx];
  }

  static getColorStyle(hexagram: string): string {
    const info = this.HEXAGRAM_MAP[hexagram];
    return info ? info.color : '#ffffff';
  }

  static getWuquan(hexagram: string): string {
    const info = this.HEXAGRAM_MAP[hexagram];
    return info?.wuquan || '金泉';
  }

  static getAllHexagrams(): string[] {
    return Object.keys(this.HEXAGRAM_MAP);
  }

  static getDeploymentConfig(): {
    minHarmonyVersion: string;
    requiredPermissions: string[];
    recommendedSettings: Record<string, object>;
  } {
    return {
      minHarmonyVersion: '4.0.0',
      requiredPermissions: [
        'ohos.permission.LOCATION',
        'ohos.permission.CAMERA',
        'ohos.permission.MICROPHONE',
        'ohos.permission.READ_MEDIA',
        'ohos.permission.DISTRIBUTED_DATASYNC'
      ],
      recommendedSettings: {
        updateInterval: 5000,
        cacheSize: 100,
        maxRetries: 3,
        timeout: 10000,
        scenicMode: true,
        autoAdjust: true
      }
    };
  }

  static validateConfig(config: {
    updateInterval?: number; cacheSize?: number;
    scenicMode?: boolean; autoAdjust?: boolean;
  }): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!config.updateInterval || config.updateInterval < 1000) {
      errors.push('更新间隔不能小于1000ms');
    }
    if (!config.cacheSize || config.cacheSize < 10) {
      errors.push('缓存大小不能小于10');
    }
    if (config.scenicMode && !config.autoAdjust) {
      errors.push('启用景观点模式时建议开启自动调整');
    }

    return { valid: errors.length === 0, errors };
  }
}

/**
 * 道德经注释
 * 第8章: "上善若水" → 坎卦如水，顺势而为
 * 第27章: "善行无辙迹" → 好导航不留痕迹
 * 第25章: "人法地，地法天，天法道，道法自然" → 五泉十景顺应自然
 */
