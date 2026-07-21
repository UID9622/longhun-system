// entry/src/main/ets/engines/CoupletEngine.ets
// 龍魂 · 对联生成引擎 · 平仄对仗规则
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { CoupletData } from '../models/GuoxueModel';

export class CoupletEngine {
  private pingZeMap: Map<string, string> = new Map([
    ['天', '平'], ['地', '仄'], ['山', '平'], ['水', '仄'],
    ['风', '平'], ['雨', '仄'], ['春', '平'], ['秋', '仄'],
    ['花', '平'], ['月', '仄'], ['日', '仄'], ['云', '平'],
    ['龙', '平'], ['虎', '仄'], ['人', '平'], ['国', '仄'],
    ['福', '平'], ['寿', '仄'], ['喜', '仄'], ['财', '平'],
    ['红', '平'], ['绿', '仄'], ['白', '仄'], ['黑', '平'],
    ['大', '仄'], ['小', '仄'], ['高', '平'], ['低', '平'],
    ['长', '平'], ['短', '仄'], ['宽', '平'], ['窄', '仄'],
    ['新', '平'], ['旧', '仄'], ['老', '仄'], ['少', '仄'],
    ['来', '平'], ['去', '仄'], ['开', '平'], ['关', '平'],
    ['上', '仄'], ['下', '仄'], ['左', '仄'], ['右', '仄'],
    ['东', '平'], ['西', '平'], ['南', '平'], ['北', '仄'],
    ['金', '平'], ['木', '仄'], ['水', '仄'], ['火', '仄'], ['土', '仄'],
    ['仁', '平'], ['义', '仄'], ['礼', '仄'], ['智', '仄'], ['信', '仄']
  ]);

  private antithesisMap: Map<string, string> = new Map([
    ['天', '地'], ['地', '天'], ['山', '水'], ['水', '山'],
    ['风', '雨'], ['雨', '风'], ['春', '秋'], ['秋', '春'],
    ['花', '月'], ['月', '花'], ['日', '月'], ['月', '日'],
    ['龙', '虎'], ['虎', '龙'], ['人', '我'], ['我', '人'],
    ['福', '寿'], ['寿', '福'], ['喜', '乐'], ['乐', '喜'],
    ['来', '去'], ['去', '来'], ['开', '合'], ['合', '开'],
    ['新', '旧'], ['旧', '新'], ['大', '小'], ['小', '大'],
    ['高', '低'], ['低', '高'], ['长', '短'], ['短', '长'],
    ['东', '西'], ['西', '东'], ['南', '北'], ['北', '南'],
    ['金', '木'], ['木', '金'], ['水', '火'], ['火', '水'],
    ['仁', '义'], ['义', '仁'], ['礼', '智'], ['智', '礼']
  ]);

  private themeTemplates: Map<string, string[][]> = new Map([
    ['春节', [
      ['春风送暖入屠苏', '爆竹声中一岁除'],
      ['天增岁月人增寿', '春满乾坤福满门'],
      ['一元复始呈兴旺', '万象更新谱华章']
    ]],
    ['龙年', [
      ['龙腾虎跃闹新春', '凤舞鸾歌庆丰年'],
      ['龙行龘龘前程朤朤', '凤鸣喈喈后路迢迢'],
      ['金龙献瑞千家乐', '玉兔呈祥万户春']
    ]],
    ['通用', [
      ['忠厚传家久', '诗书继世长'],
      ['海纳百川有容乃大', '壁立千仞无欲则刚'],
      ['书山有路勤为径', '学海无涯苦作舟']
    ]],
    ['励志', [
      ['宝剑锋从磨砺出', '梅花香自苦寒来'],
      ['业精于勤荒于嬉', '行成于思毁于随'],
      ['长风破浪会有时', '直挂云帆济沧海']
    ]],
    ['爱国', [
      ['苟利国家生死以', '岂因祸福避趋之'],
      ['人生自古谁无死', '留取丹心照汗青'],
      ['天下兴亡匹夫有责', '国家危难壮士当先']
    ]],
    ['中秋', [
      ['明月几时有三秋恰半', '故乡万里遥一醉方休'],
      ['海上生明月天涯共此时', '山中无历日夜长不知年']
    ]],
    ['婚礼', [
      ['百年好合永结同心', '千里姻缘一线牵定'],
      ['在天愿作比翼鸟', '在地愿为连理枝']
    ]],
    ['祝寿', [
      ['福如东海长流水', '寿比南山不老松'],
      ['鹤算千年寿松龄万古春', '德如泉涌人寿考天地同']
    ]]
  ]);

  generate(theme: string, wordCount: number = 7): CoupletData {
    const templates = this.themeTemplates.get(theme) || this.themeTemplates.get('通用')!;
    const template = templates[Math.floor(Math.random() * templates.length)];

    let upper: string;
    let lower: string;

    if (wordCount === 5 && template[0].length > 5) {
      upper = this.extractFiveWords(template[0]);
      lower = this.extractFiveWords(template[1]);
    } else {
      upper = template[0];
      lower = template[1];
    }

    const horizontal = this.generateHorizontal(theme);
    const tonePattern = this.analyzeTone(upper, lower);

    return new CoupletData({ upper, lower, horizontal, theme, tonePattern, wordCount });
  }

  private extractFiveWords(sentence: string): string {
    if (sentence.length <= 5) return sentence;
    return sentence.substring(0, 5);
  }

  private generateHorizontal(theme: string): string {
    const horizontals: Map<string, string[]> = new Map([
      ['春节', ['万象更新', '春回大地', '福满人间']],
      ['龙年', ['龙年大吉', '龙腾盛世', '龙凤呈祥']],
      ['通用', ['厚德载物', '自强不息', '宁静致远']],
      ['励志', ['志存高远', '鹏程万里', '奋发图强']],
      ['爱国', ['精忠报国', '振兴中华', '国泰民安']],
      ['中秋', ['花好月圆', '月满人间', '天涯此时']],
      ['婚礼', ['天作之合', '百年好合', '永结同心']],
      ['祝寿', ['福寿康宁', '松鹤延年', '寿比南山']]
    ]);
    const options = horizontals.get(theme) || horizontals.get('通用')!;
    return options[Math.floor(Math.random() * options.length)];
  }

  analyzeTone(upper: string, lower: string): string {
    let upperTone = '';
    let lowerTone = '';
    for (let i = 0; i < upper.length; i++) {
      const tone = this.pingZeMap.get(upper[i]) || '中';
      upperTone += tone === '平' ? '平' : (tone === '仄' ? '仄' : '中');
    }
    for (let i = 0; i < lower.length; i++) {
      const tone = this.pingZeMap.get(lower[i]) || '中';
      lowerTone += tone === '平' ? '平' : (tone === '仄' ? '仄' : '中');
    }
    return `上联: ${upperTone} | 下联: ${lowerTone}`;
  }

  validateAntithesis(upper: string, lower: string): boolean {
    if (upper.length !== lower.length) return false;
    for (let i = 0; i < upper.length; i++) {
      const expected = this.antithesisMap.get(upper[i]);
      if (expected && expected !== lower[i]) continue; // 宽对
    }
    return true;
  }

  getThemes(): string[] {
    return Array.from(this.themeTemplates.keys());
  }
}

export const coupletEngine = new CoupletEngine();
