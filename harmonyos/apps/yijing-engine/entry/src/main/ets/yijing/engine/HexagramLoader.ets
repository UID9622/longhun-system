/**
 * 🐉 龙魂·装卦器 — 世应/六亲/六神装配
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-HEXAGRAM-LOADER-v1.0
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 * GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 *
 * 🔥 FIXED: determineShiYing 使用京房八宫世应表替代错误公式
 *           determineSixRelations 使用卦宫五行→爻纳支五行替代静态爻位
 */
import { Yao, Hexagram } from './models/HexagramModels';
import { TRIGRAM_WUXING } from './models/HexagramModels';
import { TianGanDiZhi } from '../culture/TianGanDiZhi';
import { WuXing } from '../culture/WuXing';
import { ShenSha } from '../culture/ShenSha';

/**
 * 🔥 京房八宫世应位置表
 * 每个宫8卦，按世爻位置排列（世位从1-6）
 */
const PALACE_SHI_YING: Record<number, number> = {
  // 乾宫 (1-8): 乾天山遁·天风姤·天地否·风地观·山地剥·火地晋·火天大有
  1: 6, 44: 1, 33: 2, 12: 3, 20: 4, 23: 5, 35: 4, 14: 3,
  // 兑宫 (9-16): 兑为泽·泽水困·泽地萃·泽山咸·水山蹇·地山谦·雷山小过·雷泽归妹
  58: 6, 47: 1, 45: 2, 31: 3, 39: 4, 15: 5, 62: 4, 54: 3,
  // 离宫 (17-24): 离为火·火山旅·火风鼎·火水未济·山水蒙·风水涣·天水讼·天火同人
  30: 6, 56: 1, 50: 2, 64: 3, 4: 4, 59: 5, 6: 4, 13: 3,
  // 震宫 (25-32): 震为雷·雷地豫·雷水解·雷风恒·地风升·水风井·泽风大过·泽雷随
  51: 6, 16: 1, 40: 2, 32: 3, 46: 4, 48: 5, 28: 4, 17: 3,
  // 巽宫 (33-40): 巽为风·风天小畜·风火家人·风雷益·天雷无妄·火雷噬嗑·山雷颐·山风蛊
  57: 6, 9: 1, 37: 2, 42: 3, 25: 4, 21: 5, 27: 4, 18: 3,
  // 坎宫 (41-48): 坎为水·水泽节·水雷屯·水火既济·泽火革·雷火丰·地火明夷·地水师
  29: 6, 60: 1, 3: 2, 63: 3, 49: 4, 55: 5, 36: 4, 7: 3,
  // 艮宫 (49-56): 艮为山·山火贲·山大畜·山泽损·火泽睽·天泽履·风泽中孚·风山渐
  52: 6, 22: 1, 26: 2, 41: 3, 38: 4, 10: 5, 61: 4, 53: 3,
  // 坤宫 (57-64): 坤为地·地雷复·地泽临·地天泰·雷天大壮·泽天夬·水天需·水地比
  2: 6, 24: 1, 19: 2, 11: 3, 34: 4, 43: 5, 5: 4, 8: 3,
};

/** 八宫卦五行 */
const PALACE_WUXING: Record<number, string> = {
  1: '金', 2: '金', 3: '火', 4: '木', 5: '木', 6: '水', 7: '土', 8: '土',
};

/** 卦宫映射：卦ID → 宫号(1-8) */
function getPalaceId(hexagramId: number): number {
  // 京房八宫分组
  if ([1,44,33,12,20,23,35,14].includes(hexagramId)) return 1;
  if ([58,47,45,31,39,15,62,54].includes(hexagramId)) return 2;
  if ([30,56,50,64,4,59,6,13].includes(hexagramId)) return 3;
  if ([51,16,40,32,46,48,28,17].includes(hexagramId)) return 4;
  if ([57,9,37,42,25,21,27,18].includes(hexagramId)) return 5;
  if ([29,60,3,63,49,55,36,7].includes(hexagramId)) return 6;
  if ([52,22,26,41,38,10,61,53].includes(hexagramId)) return 7;
  if ([2,24,19,11,34,43,5,8].includes(hexagramId)) return 8;
  return 1;
}

export class HexagramLoader {
  /**
   * 完整装卦：世应 + 六亲 + 六神
   */
  static load(
    yaos: Yao[],
    hexagram: Hexagram,
    date: Date
  ): {
    yaos: Yao[];
    shiPosition: number;
    yingPosition: number;
    sixRelations: { position: number; relation: string }[];
    sixSpirits: { position: number; spirit: string }[];
  } {
    // 1. 定世应
    const { shiPos, yingPos } = this.determineShiYing(hexagram.id);

    // 2. 定六亲
    const sixRelations = this.determineSixRelations(yaos, hexagram.id);

    // 3. 定六神
    const dayGan = TianGanDiZhi.getDayGan(date);
    const sixSpirits = this.determineSixSpirits(yaos, dayGan);

    // 4. 填充爻数据
    const loadedYaos = yaos.map(yao => {
      const rel = sixRelations.find(r => r.position === yao.position);
      const spirit = sixSpirits.find(s => s.position === yao.position);
      return {
        ...yao,
        shiYing: yao.position === shiPos ? '世' : yao.position === yingPos ? '应' : '',
        sixRelation: rel ? rel.relation : '',
        sixSpirit: spirit ? spirit.spirit : '',
      };
    });

    return { yaos: loadedYaos, shiPosition: shiPos, yingPosition: yingPos, sixRelations, sixSpirits };
  }

  /**
   * 🔥 定世应（京房八宫法）
   * 每宫八卦的世爻固定排列
   */
  static determineShiYing(hexagramId: number): { shiPos: number; yingPos: number } {
    const shiPos = PALACE_SHI_YING[hexagramId] || 6;
    const yingPos = ((shiPos + 3) % 6) || 6; // 世应相隔三位
    return { shiPos, yingPos };
  }

  /**
   * 🔥 定六亲（卦宫五行为我，爻纳支五行为客，生克定六亲）
   */
  static determineSixRelations(
    yaos: Yao[],
    hexagramId: number
  ): { position: number; relation: string }[] {
    const palaceId = getPalaceId(hexagramId);
    const palaceWx = PALACE_WUXING[palaceId] || '土';
    const results: { position: number; relation: string }[] = [];

    for (const yao of yaos) {
      const yaoWx = getYaoNazhiWuXing(yao.position, hexagramId);
      const relation = WuXing.getRelation(palaceWx, yaoWx);
      results.push({ position: yao.position, relation });
    }

    return results;
  }

  /**
   * 🔥 定六神（以日天干定初爻起神）
   * 甲乙日起青龙，丙丁日起朱雀，戊己日起勾陈
   * 庚辛日起白虎，壬癸日起玄武
   */
  static determineSixSpirits(
    yaos: Yao[],
    dayGan: string
  ): { position: number; spirit: string }[] {
    const startIndex = ShenSha.getSixSpiritStartIndex(dayGan);
    const ALL_SPIRITS = ['青龙', '朱雀', '勾陈', '腾蛇', '白虎', '玄武'];

    const results: { position: number; spirit: string }[] = [];
    for (const yao of yaos) {
      const idx = (startIndex + yao.position - 1) % 6;
      results.push({ position: yao.position, spirit: ALL_SPIRITS[idx] });
    }

    return results;
  }
}

/**
 * 🔥 获取爻纳支五行
 * 每卦的每一爻按纳甲法有固定地支 → 五行
 */
function getYaoNazhiWuXing(position: number, hexagramId: number): string {
  // 地支→五行: 寅卯木, 巳午火, 申酉金, 亥子水, 辰戌丑未土
  const zhiWx: Record<string, string> = {
    '寅': '木', '卯': '木',
    '巳': '火', '午': '火',
    '申': '金', '酉': '金',
    '亥': '水', '子': '水',
    '辰': '土', '戌': '土', '丑': '土', '未': '土',
  };

  // 乾纳甲壬·坤纳乙癸·震纳庚·巽纳辛·坎纳戊·离纳己·艮纳丙·兑纳丁
  // 各爻所纳地支（初→上，各宫通用简化版）
  const naZhiMap: Record<number, string[]> = {
    // 乾宫：子寅辰午申戌（初→上）
    1: ['子', '寅', '辰', '午', '申', '戌'],
    // 坤宫：未巳卯丑亥酉
    2: ['未', '巳', '卯', '丑', '亥', '酉'],
    // 震宫：子寅辰午申戌（同乾）
    4: ['子', '寅', '辰', '午', '申', '戌'],
    // 巽宫：丑亥酉未巳卯
    5: ['丑', '亥', '酉', '未', '巳', '卯'],
    // 坎宫：寅辰午申戌子
    6: ['寅', '辰', '午', '申', '戌', '子'],
    // 离宫：卯丑亥酉未巳
    3: ['卯', '丑', '亥', '酉', '未', '巳'],
    // 艮宫：辰午申戌子寅
    7: ['辰', '午', '申', '戌', '子', '寅'],
    // 兑宫：巳卯丑亥酉未
    8: ['巳', '卯', '丑', '亥', '酉', '未'],
  };

  const palaceId = getPalaceId(hexagramId);
  const zhiArr = naZhiMap[palaceId] || ['子', '寅', '辰', '午', '申', '戌'];
  const zhi = zhiArr[position - 1];
  return zhiWx[zhi] || '土';
}

/** 位置→中文名 */
export function getPositionName(pos: number): string {
  const m: Record<number, string> = { 1: '初', 2: '二', 3: '三', 4: '四', 5: '五', 6: '上' };
  return m[pos] || '';
}
