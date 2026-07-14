// entry/src/main/ets/engines/HistoricalFigureEngine.ets
// 龍魂 · 历史人物引擎
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { HistoricalFigure } from '../models/GuoxueModel';

export class HistoricalFigureEngine {
  private figures: Map<string, HistoricalFigure> = new Map([
    ['诸葛亮', new HistoricalFigure({
      name: '诸葛亮', dynasty: '三国·蜀汉', era: '181-234年',
      achievements: ['隆中对定三分天下', '赤壁之战联吴抗曹', '六出祁山北伐中原', '发明木牛流马', '治蜀有方'],
      personality: '鞠躬尽瘁，死而后已。智慧超群，忠诚不渝。',
      famousQuotes: ['非淡泊无以明志，非宁静无以致远', '鞠躬尽瘁，死而后已', '亲贤臣，远小人'],
      relatedEvents: ['三顾茅庐', '草船借箭', '空城计', '白帝城托孤', '五丈原']
    })],
    ['曹操', new HistoricalFigure({
      name: '曹操', dynasty: '三国·魏', era: '155-220年',
      achievements: ['挟天子以令诸侯', '统一北方', '屯田制恢复生产', '唯才是举'],
      personality: '奸雄本色，雄才大略。文韬武略，不拘小节。',
      famousQuotes: ['宁教我负天下人，休教天下人负我', '老骥伏枥，志在千里', '对酒当歌，人生几何'],
      relatedEvents: ['官渡之战', '赤壁之战', '煮酒论英雄', '华容道']
    })],
    ['岳飞', new HistoricalFigure({
      name: '岳飞', dynasty: '南宋', era: '1103-1142年',
      achievements: ['精忠报国抗金兵', '郾城大捷', '收复失地', '治军严明'],
      personality: '精忠报国，刚正不阿。文武双全，气节凛然。',
      famousQuotes: ['精忠报国', '莫等闲，白了少年头，空悲切', '壮志饥餐胡虏肉，笑谈渴饮匈奴血'],
      relatedEvents: ['岳母刺字', '郾城之战', '十二道金牌', '风波亭']
    })],
    ['文天祥', new HistoricalFigure({
      name: '文天祥', dynasty: '南宋', era: '1236-1283年',
      achievements: ['起兵抗元', '被俘不屈', '留下正气歌', '舍生取义'],
      personality: '浩然正气，宁死不屈。忠贞不渝，气节高尚。',
      famousQuotes: ['人生自古谁无死，留取丹心照汗青', '天地有正气，杂然赋流形', '孔曰成仁，孟曰取义'],
      relatedEvents: ['崖山海战', '过零丁洋', '正气歌', '柴市就义']
    })],
    ['孔子', new HistoricalFigure({
      name: '孔子', dynasty: '春秋·鲁', era: '前551-前479年',
      achievements: ['创立儒家学说', '周游列国传播思想', '删述六经', '有教无类'],
      personality: '温良恭俭让，博学而笃志。仁德为本，教化天下。',
      famousQuotes: ['己所不欲，勿施于人', '学而时习之，不亦说乎', '三人行，必有我师焉'],
      relatedEvents: ['周游列国', '杏坛讲学', '韦编三绝', '陈蔡之厄']
    })],
    ['老子', new HistoricalFigure({
      name: '老子', dynasty: '春秋·楚', era: '约前571-前471年',
      achievements: ['著《道德经》', '创立道家学说', '提出无为而治', '道法自然'],
      personality: '清静无为，道法自然。大智若愚，超然物外。',
      famousQuotes: ['道可道，非常道', '上善若水', '无为而无不为'],
      relatedEvents: ['紫气东来', '骑牛出关', '著书五千言']
    })],
    ['秦始皇', new HistoricalFigure({
      name: '秦始皇', dynasty: '秦', era: '前259-前210年',
      achievements: ['统一六国', '建立中央集权', '统一文字货币度量衡', '修长城', '建兵马俑'],
      personality: '雄才大略，残暴专横。功过参半，千古一帝。',
      famousQuotes: ['朕为始皇帝，后世以计数', '天下共苦战斗不休，以有侯王'],
      relatedEvents: ['统一六国', '焚书坑儒', '修筑长城', '巡游天下', '沙丘之变']
    })],
    ['汉武帝', new HistoricalFigure({
      name: '汉武帝', dynasty: '西汉', era: '前156-前87年',
      achievements: ['独尊儒术', '开拓疆域', '派张骞通西域', '抗击匈奴', '盐铁官营'],
      personality: '雄才大略，好大喜功。开疆拓土，文治武功。',
      famousQuotes: ['犯强汉者，虽远必诛', '盖有非常之功，必待非常之人'],
      relatedEvents: ['罢黜百家', '卫青霍去病北伐', '张骞通西域', '巫蛊之祸']
    })],
    ['唐太宗', new HistoricalFigure({
      name: '李世民', dynasty: '唐', era: '598-649年',
      achievements: ['玄武门之变夺位', '贞观之治', '完善科举', '虚心纳谏', '天可汗'],
      personality: '英明果断，从谏如流。文武兼备，胸怀天下。',
      famousQuotes: ['以铜为镜，可以正衣冠', '水能载舟，亦能覆舟', '疾风知劲草，板荡识诚臣'],
      relatedEvents: ['玄武门之变', '贞观之治', '魏征进谏', '凌烟阁二十四功臣']
    })],
    ['武则天', new HistoricalFigure({
      name: '武则天', dynasty: '唐', era: '624-705年',
      achievements: ['中国历史上唯一女皇帝', '开创殿试', '发展科举', '重视农业'],
      personality: '心狠手辣，雄才大略。知人善任，政治手腕高超。',
      famousQuotes: ['欲安其家，先安其国', '君子虽殒，善名不灭'],
      relatedEvents: ['入宫为才人', '废唐建周', '神龙政变', '无字碑']
    })],
    ['朱元璋', new HistoricalFigure({
      name: '朱元璋', dynasty: '明', era: '1328-1398年',
      achievements: ['建立明朝', '推翻元朝', '恢复汉人政权', '严惩贪官', '休养生息'],
      personality: '出身贫寒，雄才大略。猜忌多疑，手段狠辣。',
      famousQuotes: ['驱逐胡虏，恢复中华', '高筑墙，广积粮，缓称王'],
      relatedEvents: ['红巾军起义', '鄱阳湖之战', '建立明朝', '胡惟庸案', '蓝玉案']
    })],
    ['郑和', new HistoricalFigure({
      name: '郑和', dynasty: '明', era: '1371-1433年',
      achievements: ['七下西洋', '开拓海上丝绸之路', '促进中外交流', '展示国威'],
      personality: '勇敢坚毅，胸怀天下。和平使者，航海先驱。',
      famousQuotes: ['宣德化而柔远人', '及临外邦，番王之不恭者，生擒之'],
      relatedEvents: ['七下西洋', '到达非洲', '建立航海图', '马六甲访问']
    })],
    ['林则徐', new HistoricalFigure({
      name: '林则徐', dynasty: '清', era: '1785-1850年',
      achievements: ['虎门销烟', '禁烟运动', '编译《四洲志》', '开眼看世界'],
      personality: '刚正不阿，忧国忧民。民族英雄，开眼看世界第一人。',
      famousQuotes: ['苟利国家生死以，岂因祸福避趋之', '海纳百川，有容乃大', '壁立千仞，无欲则刚'],
      relatedEvents: ['虎门销烟', '鸦片战争', '贬谪伊犁', '治理黄河']
    })],
    ['孙中山', new HistoricalFigure({
      name: '孙中山', dynasty: '民国', era: '1866-1925年',
      achievements: ['创立兴中会', '领导辛亥革命', '建立中华民国', '提出三民主义'],
      personality: '革命先驱，百折不挠。天下为公，博爱无私。',
      famousQuotes: ['革命尚未成功，同志仍须努力', '天下为公', '吾志所向，一往无前'],
      relatedEvents: ['辛亥革命', '建立民国', '护法运动', '国共合作']
    })]
  ]);

  query(name: string): HistoricalFigure | undefined {
    return this.figures.get(name);
  }

  search(keyword: string): HistoricalFigure[] {
    const results: HistoricalFigure[] = [];
    for (const [name, figure] of this.figures) {
      if (name.includes(keyword) ||
          figure.dynasty.includes(keyword) ||
          figure.achievements.some(a => a.includes(keyword))) {
        results.push(figure);
      }
    }
    return results;
  }

  getAll(): HistoricalFigure[] {
    return Array.from(this.figures.values());
  }

  getAllNames(): string[] {
    return Array.from(this.figures.keys());
  }

  filterByDynasty(dynasty: string): HistoricalFigure[] {
    return Array.from(this.figures.values()).filter(f => f.dynasty.includes(dynasty));
  }

  getDynasties(): string[] {
    const set = new Set<string>();
    for (const f of this.figures.values()) {
      set.add(f.dynasty);
    }
    return Array.from(set);
  }
}

export const figureEngine = new HistoricalFigureEngine();
