// entry/src/main/ets/engines/XingXiuEngine.ets
// 龍魂 · 二十八星宿引擎
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { XingXiuData } from '../models/GuoxueModel';

export class XingXiuEngine {
  private xingXiuList: XingXiuData[] = [
    // 东方青龙七宿
    new XingXiuData({ name: '角', direction: '东方青龙', animal: '苍龙', constellation: '室女座', auspicious: true, meaning: '天门，主造化万物，布君威信' }),
    new XingXiuData({ name: '亢', direction: '东方青龙', animal: '苍龙', constellation: '室女座', auspicious: true, meaning: '天府，主天下万物' }),
    new XingXiuData({ name: '氐', direction: '东方青龙', animal: '苍龙', constellation: '天秤座', auspicious: false, meaning: '天根，主疫疾' }),
    new XingXiuData({ name: '房', direction: '东方青龙', animal: '苍龙', constellation: '天蝎座', auspicious: true, meaning: '天府，主左骖' }),
    new XingXiuData({ name: '心', direction: '东方青龙', animal: '苍龙', constellation: '天蝎座', auspicious: false, meaning: '天王，主明堂' }),
    new XingXiuData({ name: '尾', direction: '东方青龙', animal: '苍龙', constellation: '天蝎座', auspicious: true, meaning: '天江，主后宫' }),
    new XingXiuData({ name: '箕', direction: '东方青龙', animal: '苍龙', constellation: '人马座', auspicious: true, meaning: '天津，主八风' }),

    // 北方玄武七宿
    new XingXiuData({ name: '斗', direction: '北方玄武', animal: '玄武', constellation: '人马座', auspicious: true, meaning: '天庙，主宰相禄位' }),
    new XingXiuData({ name: '牛', direction: '北方玄武', animal: '玄武', constellation: '摩羯座', auspicious: true, meaning: '天关，主牺牲' }),
    new XingXiuData({ name: '女', direction: '北方玄武', animal: '玄武', constellation: '宝瓶座', auspicious: true, meaning: '天少府，主布帛' }),
    new XingXiuData({ name: '虚', direction: '北方玄武', animal: '玄武', constellation: '宝瓶座', auspicious: false, meaning: '天节，主哭泣' }),
    new XingXiuData({ name: '危', direction: '北方玄武', animal: '玄武', constellation: '宝瓶座', auspicious: false, meaning: '天市，主架屋' }),
    new XingXiuData({ name: '室', direction: '北方玄武', animal: '玄武', constellation: '飞马座', auspicious: true, meaning: '天营，主军粮' }),
    new XingXiuData({ name: '壁', direction: '北方玄武', animal: '玄武', constellation: '飞马座', auspicious: true, meaning: '天厩，主图书' }),

    // 西方白虎七宿
    new XingXiuData({ name: '奎', direction: '西方白虎', animal: '白虎', constellation: '仙女座/双鱼座', auspicious: true, meaning: '天豕，主武库' }),
    new XingXiuData({ name: '娄', direction: '西方白虎', animal: '白虎', constellation: '白羊座', auspicious: true, meaning: '天狱，主苑牧' }),
    new XingXiuData({ name: '胃', direction: '西方白虎', animal: '白虎', constellation: '白羊座', auspicious: true, meaning: '天仓，主五谷' }),
    new XingXiuData({ name: '昴', direction: '西方白虎', animal: '白虎', constellation: '金牛座', auspicious: false, meaning: '天耳，主狱事' }),
    new XingXiuData({ name: '毕', direction: '西方白虎', animal: '白虎', constellation: '金牛座', auspicious: true, meaning: '天耳，主边兵' }),
    new XingXiuData({ name: '觜', direction: '西方白虎', animal: '白虎', constellation: '猎户座', auspicious: false, meaning: '天苑，主守御' }),
    new XingXiuData({ name: '参', direction: '西方白虎', animal: '白虎', constellation: '猎户座', auspicious: true, meaning: '天市，主诛斩' }),

    // 南方朱雀七宿
    new XingXiuData({ name: '井', direction: '南方朱雀', animal: '朱雀', constellation: '双子座', auspicious: false, meaning: '天阙，主水衡' }),
    new XingXiuData({ name: '鬼', direction: '南方朱雀', animal: '朱雀', constellation: '巨蟹座', auspicious: false, meaning: '天目，主视明' }),
    new XingXiuData({ name: '柳', direction: '南方朱雀', animal: '朱雀', constellation: '长蛇座', auspicious: true, meaning: '天库，主厨食' }),
    new XingXiuData({ name: '星', direction: '南方朱雀', animal: '朱雀', constellation: '长蛇座', auspicious: true, meaning: '天都，主衣裳' }),
    new XingXiuData({ name: '张', direction: '南方朱雀', animal: '朱雀', constellation: '长蛇座', auspicious: true, meaning: '天庙，主珍宝' }),
    new XingXiuData({ name: '翼', direction: '南方朱雀', animal: '朱雀', constellation: '巨爵座', auspicious: true, meaning: '天乐，主俳倡' }),
    new XingXiuData({ name: '轸', direction: '南方朱雀', animal: '朱雀', constellation: '乌鸦座', auspicious: true, meaning: '天车，主风' })
  ];

  getByDirection(direction: string): XingXiuData[] {
    return this.xingXiuList.filter(x => x.direction === direction);
  }

  getByName(name: string): XingXiuData | undefined {
    return this.xingXiuList.find(x => x.name === name);
  }

  getAll(): XingXiuData[] {
    return this.xingXiuList;
  }

  getFourAnimals(): string[] {
    return ['东方青龙', '北方玄武', '西方白虎', '南方朱雀'];
  }

  isAuspicious(name: string): boolean {
    const xing = this.getByName(name);
    return xing ? xing.auspicious : false;
  }

  getAnimalEmoji(animal: string): string {
    const map: Map<string, string> = new Map([
      ['苍龙', '🐉'], ['玄武', '🐢'], ['白虎', '🐯'], ['朱雀', '🕊️']
    ]);
    return map.get(animal) || '⭐';
  }

  getAuspiciousCount(): { auspicious: number, inauspicious: number } {
    let auspicious = 0;
    let inauspicious = 0;
    this.xingXiuList.forEach(x => x.auspicious ? auspicious++ : inauspicious++);
    return { auspicious, inauspicious };
  }
}

export const xingXiuEngine = new XingXiuEngine();
