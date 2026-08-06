/**
 * 🐉 龙魂·六神分配
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SHENSHA-v1.0
 * License: MulanPSL v2
 * 创建者: 诸葛鑫（UID9622）
 *
 * 六神按日天干排列：
 * 甲乙起青龙→朱雀→勾陈→腾蛇→白虎→玄武
 * 丙丁起朱雀→勾陈→腾蛇→白虎→玄武→青龙
 * 戊己起勾陈→腾蛇→白虎→玄武→青龙→朱雀
 * 庚辛起白虎→玄武→青龙→朱雀→勾陈→腾蛇
 * 壬癸起玄武→青龙→朱雀→勾陈→腾蛇→白虎
 */
export class ShenSha {
  /** 六神全序 */
  static readonly SIX_SPIRITS = ['青龙', '朱雀', '勾陈', '腾蛇', '白虎', '玄武'];

  /** 按日天干返回初爻起神索引 */
  static getSixSpiritStartIndex(dayGan: string): number {
    const map: Record<string, number> = {
      '甲': 0, '乙': 0,   // 青龙起
      '丙': 1, '丁': 1,   // 朱雀起
      '戊': 2, '己': 2,   // 勾陈起
      '庚': 4, '辛': 4,   // 白虎起
      '壬': 5, '癸': 5,   // 玄武起
    };
    return map[dayGan] ?? 0;
  }

  /** 获取六神含义 */
  static getSpiritMeaning(spirit: string): string {
    const m: Record<string, string> = {
      '青龙': '主吉，喜庆之事，贵人相助',
      '朱雀': '主口舌，文书之事，宜谨慎言辞',
      '勾陈': '主田土，牢狱，迟滞之事',
      '腾蛇': '主虚惊，怪异，诡诈之事',
      '白虎': '主凶伤，孝服，血光之灾',
      '玄武': '主盗贼，暗昧，隐私之事',
    };
    return m[spirit] || '';
  }

  /** 取六亲含义 */
  static getRelationMeaning(relation: string): string {
    const m: Record<string, string> = {
      '父母': '主文书、学业、长辈庇佑',
      '兄弟': '主竞争、破财、合伙之事',
      '子孙': '主福德、医药、解忧消灾',
      '妻财': '主财运、妻室、资财之物',
      '官鬼': '主功名、官非、疾病之忧',
    };
    return m[relation] || '';
  }
}
