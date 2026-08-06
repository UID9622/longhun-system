/**
 * 🐉 龙魂·起卦器
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-HEXAGRAM-CASTER-v1.0
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 * GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 *
 * 起卦方式：六爻金钱卦 · 时间起卦(梅花易数) · 数字起卦
 * 🔥 BUG FIX: buildHexagram 上下卦索引修正
 *    yaos[0]=上爻(六)·yaos[5]=初爻(一)
 *    下卦=初爻+二爻+三爻 → yaos[5].isYang, yaos[4].isYang, yaos[3].isYang
 *    上卦=四爻+五爻+上爻 → yaos[2].isYang, yaos[1].isYang, yaos[0].isYang
 */
import hilog from '@ohos.hilog';
import { Yao, Hexagram, Trigram } from './models/HexagramModels';
import { getHexagramByTrigrams } from './models/YijingData';
import { TRIGRAM_NAMES } from './models/HexagramModels';

const TAG = 'HexagramCaster';
const DOMAIN = 0xFF40;

export class HexagramCaster {
  /**
   * 🔥 六爻金钱卦（三枚铜钱掷六次）
   * 正面(阳)=3, 反面(阴)=2
   * 三枚之和: 6=老阴×变, 7=少阳—, 8=少阴- -, 9=老阳—○变
   */
  static castByCoins(seed?: number): { yaos: Yao[]; movingIndices: number[] } {
    const yaos: Yao[] = [];
    const movingIndices: number[] = [];

    const rng = seed !== undefined ? this.seededRandom(seed) : Math.random;

    // 从初爻(位1)往上到上爻(位6)依次起卦
    for (let pos = 1; pos <= 6; pos++) {
      let sum = 0;
      for (let j = 0; j < 3; j++) {
        sum += rng() < 0.5 ? 3 : 2;
      }

      const isYang = sum === 7 || sum === 9;
      const isMoving = sum === 6 || sum === 9;

      yaos.push({
        position: pos,
        name: getYaoName(pos, isYang),
        isYang: isYang,
        isMoving: isMoving,
        changed: false,
        sixRelation: '',
        sixSpirit: '',
        shiYing: '',
        text: '',
      });

      if (isMoving) {
        movingIndices.push(pos - 1);
      }
    }

    return { yaos, movingIndices };
  }

  /**
   * 🔥 时间起卦（梅花易数）
   * 上卦=(年+月+日)%8, 下卦=(年+月+日+时)%8, 动爻=(年+月+日+时)%6
   */
  static castByTime(date: Date): { yaos: Yao[]; movingIndices: number[] } {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hour = date.getHours();

    // 上卦数(0-7) → 乾1兑2离3震4巽5坎6艮7坤8(0→8)
    const upperNum = ((year + month + day) % 8);
    const lowerNum = ((year + month + day + hour) % 8);
    const movingIndex = ((year + month + day + hour) % 6); // 0→初爻,5→上爻

    const upperTrigram = (upperNum === 0 ? 7 : upperNum - 1) as Trigram;
    const lowerTrigram = (lowerNum === 0 ? 7 : lowerNum - 1) as Trigram;

    const upperBits = trigramToBits(upperTrigram);
    const lowerBits = trigramToBits(lowerTrigram);

    const yaos: Yao[] = [];
    const movingIndices: number[] = [];

    // 从初爻(1)到上爻(6): 先下卦3爻，再上卦3爻
    for (let pos = 1; pos <= 6; pos++) {
      const isYang = pos <= 3 ? lowerBits[pos - 1] : upperBits[pos - 4];
      const isMoving = (pos - 1) === movingIndex;

      yaos.push({
        position: pos,
        name: getYaoName(pos, isYang),
        isYang: isYang,
        isMoving: isMoving,
        changed: false,
        sixRelation: '',
        sixSpirit: '',
        shiYing: '',
        text: '',
      });

      if (isMoving) {
        movingIndices.push(pos - 1);
      }
    }

    return { yaos, movingIndices };
  }

  /**
   * 🔥 数字起卦（用户输入三个数字）
   * 上卦=num1%8, 下卦=num2%8, 动爻=num3%6
   */
  static castByNumbers(num1: number, num2: number, num3: number): { yaos: Yao[]; movingIndices: number[] } {
    const upperNum = num1 % 8;
    const lowerNum = num2 % 8;
    const movingIndex = num3 % 6;

    const upperTrigram = (upperNum === 0 ? 7 : upperNum - 1) as Trigram;
    const lowerTrigram = (lowerNum === 0 ? 7 : lowerNum - 1) as Trigram;

    const upperBits = trigramToBits(upperTrigram);
    const lowerBits = trigramToBits(lowerTrigram);

    const yaos: Yao[] = [];
    const movingIndices: number[] = [];

    for (let pos = 1; pos <= 6; pos++) {
      const isYang = pos <= 3 ? lowerBits[pos - 1] : upperBits[pos - 4];
      const isMoving = (pos - 1) === movingIndex;

      yaos.push({
        position: pos,
        name: getYaoName(pos, isYang),
        isYang: isYang,
        isMoving: isMoving,
        changed: false,
        sixRelation: '',
        sixSpirit: '',
        shiYing: '',
        text: '',
      });

      if (isMoving) {
        movingIndices.push(pos - 1);
      }
    }

    return { yaos, movingIndices };
  }

  /**
   * 🔥 从六爻构建卦象 — BUG FIXED
   * yaos 按 position 1(初爻)→6(上爻) 顺序排列
   * 下卦=初爻(位1)+二爻(位2)+三爻(位3) = yaos[0-2]
   * 上卦=四爻(位4)+五爻(位5)+上爻(位6) = yaos[3-5]
   */
  static buildHexagram(yaos: Yao[]): Hexagram | undefined {
    const lowerBits = [yaos[0].isYang, yaos[1].isYang, yaos[2].isYang];
    const upperBits = [yaos[3].isYang, yaos[4].isYang, yaos[5].isYang];
    const lowerTrigram = bitsToTrigram(lowerBits);
    const upperTrigram = bitsToTrigram(upperBits);
    return getHexagramByTrigrams(upperTrigram, lowerTrigram);
  }

  /**
   * 从本卦构建变卦（动爻取反后重组）
   */
  static buildChangedHexagram(yaos: Yao[]): { hexagram?: Hexagram; yaos: Yao[] } {
    const changedYaos = yaos.map(y => {
      if (!y.isMoving) return { ...y };
      return { ...y, isYang: !y.isYang, changed: true };
    });

    const hex = this.buildHexagram(changedYaos);
    return { hexagram: hex, yaos: changedYaos };
  }

  /**
   * 🔥 构建互卦（本卦二三四爻为下卦，三四五爻为上卦）
   */
  static buildMutualHexagram(yaos: Yao[]): Hexagram | undefined {
    const lowerBits = [yaos[1].isYang, yaos[2].isYang, yaos[3].isYang]; // 位2+3+4
    const upperBits = [yaos[2].isYang, yaos[3].isYang, yaos[4].isYang]; // 位3+4+5
    const lowerTrigram = bitsToTrigram(lowerBits);
    const upperTrigram = bitsToTrigram(upperBits);
    return getHexagramByTrigrams(upperTrigram, lowerTrigram);
  }

  /** 种子随机数 */
  private static seededRandom(seed: number): () => number {
    let s = seed;
    return () => {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
  }
}

// ════════════════════════════════════════
// 公用工具函数
// ════════════════════════════════════════

/** 获取爻名: 初九/初六, 九二/六二, ..., 上九/上六 */
export function getYaoName(position: number, isYang: boolean): string {
  const posNames: Record<number, string> = {
    1: '初', 2: '二', 3: '三', 4: '四', 5: '五', 6: '上',
  };
  return posNames[position] + (isYang ? '九' : '六');
}

/**
 * 八卦 → 三爻位数组 [下,中,上]
 * 先天序：乾[1,1,1] 兑[1,1,0] 离[1,0,1] 震[1,0,0]
 *         巽[0,1,1] 坎[0,1,0] 艮[0,0,1] 坤[0,0,0]
 */
export function trigramToBits(trigram: Trigram): boolean[] {
  const map: Record<number, boolean[]> = {
    0: [true, true, true],   // 乾
    1: [true, true, false],  // 兑
    2: [true, false, true],  // 离
    3: [true, false, false], // 震
    4: [false, true, true],  // 巽
    5: [false, true, false], // 坎
    6: [false, false, true], // 艮
    7: [false, false, false],// 坤
  };
  return map[trigram] || [false, false, false];
}

/** 三爻位 → 八卦 */
export function bitsToTrigram(bits: boolean[]): Trigram {
  const key = bits.map(b => b ? '1' : '0').join('');
  const map: Record<string, Trigram> = {
    '111': 0, '110': 1, '101': 2, '100': 3,
    '011': 4, '010': 5, '001': 6, '000': 7,
  };
  return map[key] ?? Trigram.KUN;
}

/** 八卦符号 */
export function getTrigramSymbol(trigram: Trigram): string {
  const syms = ['☰', '☱', '☲', '☳', '☴', '☵', '☶', '☷'];
  return syms[trigram] || '?';
}
