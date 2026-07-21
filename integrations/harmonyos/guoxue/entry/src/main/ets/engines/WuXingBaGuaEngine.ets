// entry/src/main/ets/engines/WuXingBaGuaEngine.ets
// 龍魂 · 五行八卦引擎
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { WuXingData, BaGuaData } from '../models/GuoxueModel';

export class WuXingBaGuaEngine {
  private wuXingData: Map<string, WuXingData> = new Map([
    ['金', new WuXingData({ element: '金', generation: '生水', restriction: '克木', color: '白', direction: '西', season: '秋', organ: '肺', emotion: '悲' })],
    ['木', new WuXingData({ element: '木', generation: '生火', restriction: '克土', color: '青', direction: '东', season: '春', organ: '肝', emotion: '怒' })],
    ['水', new WuXingData({ element: '水', generation: '生木', restriction: '克火', color: '黑', direction: '北', season: '冬', organ: '肾', emotion: '恐' })],
    ['火', new WuXingData({ element: '火', generation: '生土', restriction: '克金', color: '赤', direction: '南', season: '夏', organ: '心', emotion: '喜' })],
    ['土', new WuXingData({ element: '土', generation: '生金', restriction: '克水', color: '黄', direction: '中', season: '长夏', organ: '脾', emotion: '思' })]
  ]);

  private baGuaData: Map<string, BaGuaData> = new Map([
    ['乾', new BaGuaData({ name: '乾', symbol: '☰', nature: '天', attribute: '健', family: '父', direction: '西北', number: 1 })],
    ['坤', new BaGuaData({ name: '坤', symbol: '☷', nature: '地', attribute: '顺', family: '母', direction: '西南', number: 2 })],
    ['震', new BaGuaData({ name: '震', symbol: '☳', nature: '雷', attribute: '动', family: '长男', direction: '东', number: 3 })],
    ['巽', new BaGuaData({ name: '巽', symbol: '☴', nature: '风', attribute: '入', family: '长女', direction: '东南', number: 4 })],
    ['坎', new BaGuaData({ name: '坎', symbol: '☵', nature: '水', attribute: '陷', family: '中男', direction: '北', number: 5 })],
    ['离', new BaGuaData({ name: '离', symbol: '☲', nature: '火', attribute: '丽', family: '中女', direction: '南', number: 6 })],
    ['艮', new BaGuaData({ name: '艮', symbol: '☶', nature: '山', attribute: '止', family: '少男', direction: '东北', number: 7 })],
    ['兑', new BaGuaData({ name: '兑', symbol: '☱', nature: '泽', attribute: '悦', family: '少女', direction: '西', number: 8 })]
  ]);

  getWuXing(element: string): WuXingData | undefined {
    return this.wuXingData.get(element);
  }

  getBaGua(name: string): BaGuaData | undefined {
    return this.baGuaData.get(name);
  }

  getRelation(from: string, to: string): string {
    const wuXing = ['金', '木', '水', '火', '土'];
    const fromIndex = wuXing.indexOf(from);
    const toIndex = wuXing.indexOf(to);
    if (fromIndex === -1 || toIndex === -1) return '未知';
    if ((fromIndex + 1) % 5 === toIndex) return `${from}生${to}`;
    if ((fromIndex + 2) % 5 === toIndex) return `${from}克${to}`;
    if ((toIndex + 1) % 5 === fromIndex) return `${to}生${from}`;
    if ((toIndex + 2) % 5 === fromIndex) return `${to}克${from}`;
    return '同';
  }

  getBaGuaWuXing(gua: string): string {
    const map: Map<string, string> = new Map([
      ['乾', '金'], ['兑', '金'],
      ['震', '木'], ['巽', '木'],
      ['坎', '水'],
      ['离', '火'],
      ['坤', '土'], ['艮', '土']
    ]);
    return map.get(gua) || '未知';
  }

  getAllWuXing(): WuXingData[] {
    return Array.from(this.wuXingData.values());
  }

  getAllBaGua(): BaGuaData[] {
    return Array.from(this.baGuaData.values());
  }

  /** 生成八卦六十四卦简要说明 */
  getGuaDescription(name: string): string {
    const desc: Map<string, string> = new Map([
      ['乾', '乾为天 ☰☰ — 元亨利贞。象征天，代表创造、刚健、主动。彖曰：大哉乾元，万物资始。'],
      ['坤', '坤为地 ☷☷ — 元亨利牝马之贞。象征地，代表柔顺、包容、承载。彖曰：至哉坤元，万物资生。'],
      ['震', '震为雷 ☳☳ — 亨。象征雷，代表震动、惊醒、变革。彖曰：震，亨。震来虩虩，恐致福也。'],
      ['巽', '巽为风 ☴☴ — 小亨，利有攸往。象征风，代表顺从、渗透、无孔不入。'],
      ['坎', '坎为水 ☵☵ — 习坎，有孚。象征水，代表艰险、深沉、智慧。'],
      ['离', '离为火 ☲☲ — 利贞，亨。象征火，代表光明、依附、文明。'],
      ['艮', '艮为山 ☶☶ — 艮其背。象征山，代表停止、静止、稳重。'],
      ['兑', '兑为泽 ☱☱ — 亨利贞。象征泽，代表喜悦、言说、交流。']
    ]);
    return desc.get(name) || '未知卦象';
  }
}

export const wuXingBaGuaEngine = new WuXingBaGuaEngine();
