/**
 * 🐉 龙魂·六十四卦完整数据库 — 纯中文
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-YIJING-DATA-v1.0
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 * GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 * 数据来源: 《周易》原文 + engines/longhun/personas/yijing_hexagrams.json
 * — 64卦全量·卦辞·彖辞·象辞·六爻爻辞 —
 */
import { Hexagram, Trigram } from './HexagramModels';

/** 64卦Unicode符号映射 (U+4DC0 - U+4DFF) */
const GUA_SYMBOLS: string[] = [
  '', '䷀', '䷁', '䷂', '䷃', '䷄', '䷅', '䷆', '䷇',  //  1-8
  '䷈', '䷉', '䷊', '䷋', '䷌', '䷍', '䷎', '䷏',        //  9-16
  '䷐', '䷑', '䷒', '䷓', '䷔', '䷕', '䷖', '䷗',        // 17-24
  '䷘', '䷙', '䷚', '䷛', '䷜', '䷝', '䷞', '䷟',        // 25-32
  '䷠', '䷡', '䷢', '䷣', '䷤', '䷥', '䷦', '䷧',        // 33-40
  '䷨', '䷩', '䷪', '䷫', '䷬', '䷭', '䷮', '䷯',        // 41-48
  '䷰', '䷱', '䷲', '䷳', '䷴', '䷵', '䷶', '䷷',        // 49-56
  '䷸', '䷹', '䷺', '䷻', '䷼', '䷽', '䷾', '䷿',        // 57-64
];

/**
 * 六十四卦完整数据库
 * 卦序: 乾坤屯蒙需讼师 比小畜兮履泰否 ...
 */
export const HEXAGRAM_DATA: Hexagram[] = [
  // ═══ 1. 乾为天 ䷀ ═══
  {
    id: 1, name: '乾', symbol: GUA_SYMBOLS[1],
    upperTrigram: Trigram.QIAN, lowerTrigram: Trigram.QIAN,
    description: '元亨利贞。',
    interpretation: '乾：天行健，君子以自强不息。大哉乾元，万物资始，乃统天。云行雨施，品物流形。大明终始，六位时成，时乘六龙以御天。乾道变化，各正性命，保合太和，乃利贞。首出庶物，万国咸宁。',
    yaoText: [
      '初九：潜龙勿用。',
      '九二：见龙在田，利见大人。',
      '九三：君子终日乾乾，夕惕若厉，无咎。',
      '九四：或跃在渊，无咎。',
      '九五：飞龙在天，利见大人。',
      '上九：亢龙有悔。',
    ],
    image: '天行健，君子以自强不息。',
    attribute: '纯阳·刚健',
  },
  // ═══ 2. 坤为地 ䷁ ═══
  {
    id: 2, name: '坤', symbol: GUA_SYMBOLS[2],
    upperTrigram: Trigram.KUN, lowerTrigram: Trigram.KUN,
    description: '元亨，利牝马之贞。君子有攸往，先迷后得主，利西南得朋，东北丧朋。安贞吉。',
    interpretation: '坤：地势坤，君子以厚德载物。至哉坤元，万物资生，乃顺承天。坤厚载物，德合无疆。含弘光大，品物咸亨。牝马地类，行地无疆，柔顺利贞。',
    yaoText: [
      '初六：履霜，坚冰至。',
      '六二：直方大，不习无不利。',
      '六三：含章可贞。或从王事，无成有终。',
      '六四：括囊，无咎无誉。',
      '六五：黄裳，元吉。',
      '上六：龙战于野，其血玄黄。',
    ],
    image: '地势坤，君子以厚德载物。',
    attribute: '纯阴·柔顺',
  },
  // ═══ 3. 水雷屯 ䷂ ═══
  {
    id: 3, name: '屯', symbol: GUA_SYMBOLS[3],
    upperTrigram: Trigram.KAN, lowerTrigram: Trigram.ZHEN,
    description: '元亨利贞。勿用有攸往。利建侯。',
    interpretation: '屯：云雷屯，君子以经纶。刚柔始交而难生，动乎险中，大亨贞。雷雨之动满盈，天造草昧，宜建侯而不宁。',
    yaoText: [
      '初九：磐桓，利居贞，利建侯。',
      '六二：屯如邅如，乘马班如。匪寇婚媾，女子贞不字，十年乃字。',
      '六三：即鹿无虞，惟入于林中，君子几不如舍，往吝。',
      '六四：乘马班如，求婚媾，往吉，无不利。',
      '九五：屯其膏，小贞吉，大贞凶。',
      '上六：乘马班如，泣血涟如。',
    ],
    image: '云雷屯，君子以经纶。',
    attribute: '起始艰难',
  },
  // ═══ 4. 山水蒙 ䷃ ═══
  {
    id: 4, name: '蒙', symbol: GUA_SYMBOLS[4],
    upperTrigram: Trigram.GEN, lowerTrigram: Trigram.KAN,
    description: '亨。匪我求童蒙，童蒙求我。初筮告，再三渎，渎则不告。利贞。',
    interpretation: '蒙：山下出泉蒙，君子以果行育德。蒙，山下有险，险而止蒙。蒙亨，以亨行时中也。匪我求童蒙，童蒙求我，志应也。',
    yaoText: [
      '初六：发蒙，利用刑人，用说桎梏，以往吝。',
      '九二：包蒙吉，纳妇吉，子克家。',
      '六三：勿用取女，见金夫，不有躬，无攸利。',
      '六四：困蒙，吝。',
      '六五：童蒙，吉。',
      '上九：击蒙，不利为寇，利御寇。',
    ],
    image: '山下出泉蒙，君子以果行育德。',
    attribute: '启蒙',
  },
  // ═══ 5. 水天需 ䷄ ═══
  {
    id: 5, name: '需', symbol: GUA_SYMBOLS[5],
    upperTrigram: Trigram.KAN, lowerTrigram: Trigram.QIAN,
    description: '有孚，光亨，贞吉。利涉大川。',
    interpretation: '需：云上于天需，君子以饮食宴乐。需，须也，险在前也。刚健而不陷，其义不困穷矣。需有孚光亨贞吉，位乎天位，以正中也。',
    yaoText: [
      '初九：需于郊，利用恒，无咎。',
      '九二：需于沙，小有言，终吉。',
      '九三：需于泥，致寇至。',
      '六四：需于血，出自穴。',
      '九五：需于酒食，贞吉。',
      '上六：入于穴，有不速之客三人来，敬之终吉。',
    ],
    image: '云上于天需，君子以饮食宴乐。',
    attribute: '等待时机',
  },
  // ═══ 6. 天水讼 ䷅ ═══
  {
    id: 6, name: '讼', symbol: GUA_SYMBOLS[6],
    upperTrigram: Trigram.QIAN, lowerTrigram: Trigram.KAN,
    description: '有孚窒惕，中吉，终凶。利见大人，不利涉大川。',
    interpretation: '讼：天与水违行讼，君子以作事谋始。讼，上刚下险，险而健讼。讼有孚窒惕中吉，刚来而得中也。终凶，讼不可成也。',
    yaoText: [
      '初六：不永所事，小有言，终吉。',
      '九二：不克讼，归而逋，其邑人三百户，无眚。',
      '六三：食旧德，贞厉，终吉。或从王事，无成。',
      '九四：不克讼，复即命，渝安贞，吉。',
      '九五：讼，元吉。',
      '上九：或锡之鞶带，终朝三褫之。',
    ],
    image: '天与水违行讼，君子以作事谋始。',
    attribute: '争讼',
  },
  // ═══ 7. 地水师 ䷆ ═══
  {
    id: 7, name: '师', symbol: GUA_SYMBOLS[7],
    upperTrigram: Trigram.KUN, lowerTrigram: Trigram.KAN,
    description: '贞，丈人吉，无咎。',
    interpretation: '师：地中有水师，君子以容民畜众。师，众也。贞，正也。能以众正，可以王矣。刚中而应，行险而顺，以此毒天下，而民从之，吉又何咎矣。',
    yaoText: [
      '初六：师出以律，否臧凶。',
      '九二：在师中，吉，无咎。王三锡命。',
      '六三：师或舆尸，凶。',
      '六四：师左次，无咎。',
      '六五：田有禽，利执言，无咎。长子帅师，弟子舆尸，贞凶。',
      '上六：大君有命，开国承家，小人勿用。',
    ],
    image: '地中有水师，君子以容民畜众。',
    attribute: '行师用兵',
  },
  // ═══ 8. 水地比 ䷇ ═══
  {
    id: 8, name: '比', symbol: GUA_SYMBOLS[8],
    upperTrigram: Trigram.KAN, lowerTrigram: Trigram.KUN,
    description: '吉。原筮，元永贞，无咎。不宁方来，后夫凶。',
    interpretation: '比：地上有水比，先王以建万国亲诸侯。比，吉也。比，辅也，下顺从也。原筮元永贞无咎，以刚中也。不宁方来，上下应也。',
    yaoText: [
      '初六：有孚比之，无咎。有孚盈缶，终来有它，吉。',
      '六二：比之自内，贞吉。',
      '六三：比之匪人。',
      '六四：外比之，贞吉。',
      '九五：显比，王用三驱，失前禽。邑人不诫，吉。',
      '上六：比之无首，凶。',
    ],
    image: '地上有水比，先王以建万国亲诸侯。',
    attribute: '亲比',
  },
  // ═══ 9-64 略用紧凑格式继续 ═══
  // 9. 风天小畜 ䷈
  { id: 9, name: '小畜', symbol: GUA_SYMBOLS[9], upperTrigram: Trigram.XUN, lowerTrigram: Trigram.QIAN,
    description: '亨。密云不雨，自我西郊。',
    interpretation: '风行天上小畜，君子以懿文德。',
    yaoText: ['初九：复自道，何其咎，吉。', '九二：牵复，吉。', '九三：舆说辐，夫妻反目。',
      '六四：有孚，血去惕出，无咎。', '九五：有孚挛如，富以其邻。', '上九：既雨既处，尚德载，妇贞厉。月几望，君子征凶。'],
    image: '风行天上小畜，君子以懿文德。', attribute: '小有积蓄' },
  // 10. 天泽履 ䷉
  { id: 10, name: '履', symbol: GUA_SYMBOLS[10], upperTrigram: Trigram.QIAN, lowerTrigram: Trigram.DUI,
    description: '履虎尾，不咥人，亨。',
    interpretation: '上天下泽履，君子以辨上下定民志。',
    yaoText: ['初九：素履，往无咎。', '九二：履道坦坦，幽人贞吉。', '六三：眇能视，跛能履，履虎尾咥人凶。武人为于大君。',
      '九四：履虎尾，愬愬终吉。', '九五：夬履，贞厉。', '上九：视履考祥，其旋元吉。'],
    image: '上天下泽履，君子以辨上下定民志。', attribute: '谨慎践履' },
  // 11. 地天泰 ䷊
  { id: 11, name: '泰', symbol: GUA_SYMBOLS[11], upperTrigram: Trigram.KUN, lowerTrigram: Trigram.QIAN,
    description: '小往大来，吉亨。',
    interpretation: '天地交泰，后以财成天地之道，辅相天地之宜，以左右民。',
    yaoText: ['初九：拔茅茹，以其汇，征吉。', '九二：包荒，用冯河，不遐遗，朋亡，得尚于中行。',
      '九三：无平不陂，无往不复，艰贞无咎。勿恤其孚，于食有福。',
      '六四：翩翩不富，以其邻，不戒以孚。', '六五：帝乙归妹，以祉元吉。', '上六：城复于隍，勿用师。自邑告命，贞吝。'],
    image: '天地交泰，后以财成天地之道。', attribute: '通泰吉祥' },
  // 12. 天地否 ䷋
  { id: 12, name: '否', symbol: GUA_SYMBOLS[12], upperTrigram: Trigram.QIAN, lowerTrigram: Trigram.KUN,
    description: '否之匪人，不利君子贞。大往小来。',
    interpretation: '天地不交否，君子以俭德辟难，不可荣以禄。',
    yaoText: ['初六：拔茅茹，以其汇，贞吉亨。', '六二：包承，小人吉，大人否亨。',
      '六三：包羞。', '九四：有命无咎，畴离祉。', '九五：休否，大人吉。其亡其亡，系于苞桑。', '上九：倾否，先否后喜。'],
    image: '天地不交否，君子以俭德辟难。', attribute: '闭塞不通' },
  // 13. 天火同人 ䷌
  { id: 13, name: '同人', symbol: GUA_SYMBOLS[13], upperTrigram: Trigram.QIAN, lowerTrigram: Trigram.LI,
    description: '同人于野，亨。利涉大川，利君子贞。',
    interpretation: '天与火同人，君子以类族辨物。',
    yaoText: ['初九：同人于门，无咎。', '六二：同人于宗，吝。', '九三：伏戎于莽，升其高陵，三岁不兴。',
      '九四：乘其墉，弗克攻，吉。', '九五：同人先号咷而后笑，大师克相遇。', '上九：同人于郊，无悔。'],
    image: '天与火同人，君子以类族辨物。', attribute: '同人于野' },
  // 14. 火天大有 ䷍
  { id: 14, name: '大有', symbol: GUA_SYMBOLS[14], upperTrigram: Trigram.LI, lowerTrigram: Trigram.QIAN,
    description: '元亨。',
    interpretation: '火在天上大有，君子以遏恶扬善，顺天休命。',
    yaoText: ['初九：无交害，匪咎，艰则无咎。', '九二：大车以载，有攸往，无咎。',
      '九三：公用亨于天子，小人弗克。', '九四：匪其彭，无咎。', '六五：厥孚交如，威如，吉。', '上九：自天祐之，吉无不利。'],
    image: '火在天上大有，君子以遏恶扬善。', attribute: '大有收获' },
  // 15. 地山谦 ䷎
  { id: 15, name: '谦', symbol: GUA_SYMBOLS[15], upperTrigram: Trigram.KUN, lowerTrigram: Trigram.GEN,
    description: '亨，君子有终。',
    interpretation: '地中有山谦，君子以裒多益寡，称物平施。',
    yaoText: ['初六：谦谦君子，用涉大川，吉。', '六二：鸣谦，贞吉。', '九三：劳谦君子，有终吉。',
      '六四：无不利，撝谦。', '六五：不富以其邻，利用侵伐，无不利。', '上六：鸣谦，利用行师，征邑国。'],
    image: '地中有山谦，君子以裒多益寡。', attribute: '谦逊受益' },
  // 16. 雷地豫 ䷏
  { id: 16, name: '豫', symbol: GUA_SYMBOLS[16], upperTrigram: Trigram.ZHEN, lowerTrigram: Trigram.KUN,
    description: '利建侯行师。',
    interpretation: '雷出地奋豫，先王以作乐崇德，殷荐之上帝，以配祖考。',
    yaoText: ['初六：鸣豫，凶。', '六二：介于石，不终日，贞吉。', '六三：盱豫，悔。迟有悔。',
      '九四：由豫，大有得。勿疑，朋盍簪。', '六五：贞疾，恒不死。', '上六：冥豫，成有渝，无咎。'],
    image: '雷出地奋豫，先王以作乐崇德。', attribute: '喜悦豫乐' },
  // 17. 泽雷随 ䷐
  { id: 17, name: '随', symbol: GUA_SYMBOLS[17], upperTrigram: Trigram.DUI, lowerTrigram: Trigram.ZHEN,
    description: '元亨利贞，无咎。',
    interpretation: '泽中有雷随，君子以向晦入宴息。',
    yaoText: ['初九：官有渝，贞吉。出门交有功。', '六二：系小子，失丈夫。', '六三：系丈夫，失小子。随有求得，利居贞。',
      '九四：随有获，贞凶。有孚在道，以明，何咎。', '九五：孚于嘉，吉。', '上六：拘系之，乃从维之，王用亨于西山。'],
    image: '泽中有雷随，君子以向晦入宴息。', attribute: '随顺时势' },
  // 18. 山风蛊 ䷑
  { id: 18, name: '蛊', symbol: GUA_SYMBOLS[18], upperTrigram: Trigram.GEN, lowerTrigram: Trigram.XUN,
    description: '元亨，利涉大川。先甲三日，后甲三日。',
    interpretation: '山下有风蛊，君子以振民育德。',
    yaoText: ['初六：干父之蛊，有子，考无咎，厉终吉。', '九二：干母之蛊，不可贞。',
      '九三：干父之蛊，小有悔，无大咎。', '六四：裕父之蛊，往见吝。', '六五：干父之蛊，用誉。', '上九：不事王侯，高尚其事。'],
    image: '山下有风蛊，君子以振民育德。', attribute: '蛊惑整治' },
  // 19. 地泽临 ䷒
  { id: 19, name: '临', symbol: GUA_SYMBOLS[19], upperTrigram: Trigram.KUN, lowerTrigram: Trigram.DUI,
    description: '元亨利贞。至于八月有凶。',
    interpretation: '泽上有地临，君子以教思无穷，容保民无疆。',
    yaoText: ['初九：咸临，贞吉。', '九二：咸临，吉无不利。', '六三：甘临，无攸利。既忧之，无咎。',
      '六四：至临，无咎。', '六五：知临，大君之宜，吉。', '上六：敦临，吉无咎。'],
    image: '泽上有地临，君子以教思无穷。', attribute: '监临督导' },
  // 20. 风地观 ䷓
  { id: 20, name: '观', symbol: GUA_SYMBOLS[20], upperTrigram: Trigram.XUN, lowerTrigram: Trigram.KUN,
    description: '盥而不荐，有孚颙若。',
    interpretation: '风行地上观，先王以省方观民设教。',
    yaoText: ['初六：童观，小人无咎，君子吝。', '六二：窥观，利女贞。', '六三：观我生，进退。',
      '六四：观国之光，利用宾于王。', '九五：观我生，君子无咎。', '上九：观其生，君子无咎。'],
    image: '风行地上观，先王以省方观民设教。', attribute: '观察审视' },
  // 21. 火雷噬嗑 ䷔
  { id: 21, name: '噬嗑', symbol: GUA_SYMBOLS[21], upperTrigram: Trigram.LI, lowerTrigram: Trigram.ZHEN,
    description: '亨，利用狱。',
    interpretation: '雷电噬嗑，先王以明罚敕法。',
    yaoText: ['初九：屦校灭趾，无咎。', '六二：噬肤灭鼻，无咎。', '六三：噬腊肉，遇毒。小吝，无咎。',
      '九四：噬干胏，得金矢，利艰贞，吉。', '六五：噬干肉，得黄金，贞厉，无咎。', '上九：何校灭耳，凶。'],
    image: '雷电噬嗑，先王以明罚敕法。', attribute: '明断刑狱' },
  // 22. 山火贲 ䷕
  { id: 22, name: '贲', symbol: GUA_SYMBOLS[22], upperTrigram: Trigram.GEN, lowerTrigram: Trigram.LI,
    description: '亨。小利有攸往。',
    interpretation: '山下有火贲，君子以明庶政，无敢折狱。',
    yaoText: ['初九：贲其趾，舍车而徒。', '六二：贲其须。', '九三：贲如濡如，永贞吉。',
      '六四：贲如皤如，白马翰如，匪寇婚媾。', '六五：贲于丘园，束帛戋戋，吝，终吉。', '上九：白贲，无咎。'],
    image: '山下有火贲，君子以明庶政。', attribute: '文饰美化' },
  // 23. 山地剥 ䷖
  { id: 23, name: '剥', symbol: GUA_SYMBOLS[23], upperTrigram: Trigram.GEN, lowerTrigram: Trigram.KUN,
    description: '不利有攸往。',
    interpretation: '山附于地剥，上以厚下安宅。',
    yaoText: ['初六：剥床以足，蔑贞凶。', '六二：剥床以辨，蔑贞凶。', '六三：剥之，无咎。',
      '六四：剥床以肤，凶。', '六五：贯鱼，以宫人宠，无不利。', '上九：硕果不食，君子得舆，小人剥庐。'],
    image: '山附于地剥，上以厚下安宅。', attribute: '剥落衰败' },
  // 24. 地雷复 ䷗
  { id: 24, name: '复', symbol: GUA_SYMBOLS[24], upperTrigram: Trigram.KUN, lowerTrigram: Trigram.ZHEN,
    description: '亨。出入无疾，朋来无咎。反复其道，七日来复，利有攸往。',
    interpretation: '雷在地中复，先王以至日闭关，商旅不行，后不省方。',
    yaoText: ['初九：不远复，无祗悔，元吉。', '六二：休复，吉。', '六三：频复，厉，无咎。',
      '六四：中行独复。', '六五：敦复，无悔。', '上六：迷复，凶，有灾眚。用行师，终有大败，以其国君凶，至于十年不克征。'],
    image: '雷在地中复，先王以至日闭关。', attribute: '恢复复兴' },
  // 25. 天雷无妄 ䷘
  { id: 25, name: '无妄', symbol: GUA_SYMBOLS[25], upperTrigram: Trigram.QIAN, lowerTrigram: Trigram.ZHEN,
    description: '元亨利贞。其匪正有眚，不利有攸往。',
    interpretation: '天下雷行无妄，先王以茂对时育万物。',
    yaoText: ['初九：无妄，往吉。', '六二：不耕获，不菑畲，则利有攸往。', '六三：无妄之灾，或系之牛，行人之得，邑人之灾。',
      '九四：可贞，无咎。', '九五：无妄之疾，勿药有喜。', '上九：无妄，行有眚，无攸利。'],
    image: '天下雷行无妄，先王以茂对时育万物。', attribute: '无妄之福' },
  // 26. 山天大畜 ䷙
  { id: 26, name: '大畜', symbol: GUA_SYMBOLS[26], upperTrigram: Trigram.GEN, lowerTrigram: Trigram.QIAN,
    description: '利贞，不家食吉，利涉大川。',
    interpretation: '天在山中大畜，君子以多识前言往行，以畜其德。',
    yaoText: ['初九：有厉利已。', '九二：舆说辐。', '九三：良马逐，利艰贞。曰闲舆卫，利有攸往。',
      '六四：童牛之牿，元吉。', '六五：豮豕之牙，吉。', '上九：何天之衢，亨。'],
    image: '天在山中大畜，君子以多识前言往行。', attribute: '大积蓄' },
  // 27. 山雷颐 ䷚
  { id: 27, name: '颐', symbol: GUA_SYMBOLS[27], upperTrigram: Trigram.GEN, lowerTrigram: Trigram.ZHEN,
    description: '贞吉。观颐，自求口实。',
    interpretation: '山下有雷颐，君子以慎言语，节饮食。',
    yaoText: ['初九：舍尔灵龟，观我朵颐，凶。', '六二：颠颐，拂经，于丘颐，征凶。',
      '六三：拂颐，贞凶。十年勿用，无攸利。', '六四：颠颐，吉。虎视眈眈，其欲逐逐，无咎。', '六五：拂经，居贞吉，不可涉大川。',
      '上九：由颐，厉吉，利涉大川。'],
    image: '山下有雷颐，君子以慎言语节饮食。', attribute: '养生自养' },
  // 28. 泽风大过 ䷛
  { id: 28, name: '大过', symbol: GUA_SYMBOLS[28], upperTrigram: Trigram.DUI, lowerTrigram: Trigram.XUN,
    description: '栋桡，利有攸往，亨。',
    interpretation: '泽灭木大过，君子以独立不惧，遁世无闷。',
    yaoText: ['初六：藉用白茅，无咎。', '九二：枯杨生稊，老夫得其女妻，无不利。',
      '九三：栋桡，凶。', '九四：栋隆，吉。有它吝。', '九五：枯杨生华，老妇得其士夫，无咎无誉。', '上六：过涉灭顶，凶，无咎。'],
    image: '泽灭木大过，君子以独立不惧。', attribute: '大过度' },
  // 29. 坎为水 ䷜
  { id: 29, name: '坎', symbol: GUA_SYMBOLS[29], upperTrigram: Trigram.KAN, lowerTrigram: Trigram.KAN,
    description: '习坎，有孚，维心亨，行有尚。',
    interpretation: '水洊至习坎，君子以常德行，习教事。',
    yaoText: ['初六：习坎，入于坎窞，凶。', '九二：坎有险，求小得。', '六三：来之坎坎，险且枕，入于坎窞，勿用。',
      '六四：樽酒簋贰，用缶，纳约自牖，终无咎。', '九五：坎不盈，祗既平，无咎。', '上六：系用徽纆，寘于丛棘，三岁不得，凶。'],
    image: '水洊至习坎，君子以常德行。', attribute: '重险' },
  // 30. 离为火 ䷝
  { id: 30, name: '离', symbol: GUA_SYMBOLS[30], upperTrigram: Trigram.LI, lowerTrigram: Trigram.LI,
    description: '利贞，亨。畜牝牛，吉。',
    interpretation: '明两作离，大人以继明照于四方。',
    yaoText: ['初九：履错然，敬之无咎。', '六二：黄离，元吉。', '九三：日昃之离，不鼓缶而歌，则大耋之嗟，凶。',
      '九四：突如其来如，焚如，死如，弃如。', '六五：出涕沱若，戚嗟若，吉。', '上九：王用出征，有嘉折首，获匪其丑，无咎。'],
    image: '明两作离，大人以继明照于四方。', attribute: '光明' },
  // 31. 泽山咸 ䷞
  { id: 31, name: '咸', symbol: GUA_SYMBOLS[31], upperTrigram: Trigram.DUI, lowerTrigram: Trigram.GEN,
    description: '亨，利贞。取女吉。',
    interpretation: '山上有泽咸，君子以虚受人。',
    yaoText: ['初六：咸其拇。', '六二：咸其腓，凶，居吉。', '九三：咸其股，执其随，往吝。',
      '九四：贞吉悔亡，憧憧往来，朋从尔思。', '九五：咸其脢，无悔。', '上六：咸其辅颊舌。'],
    image: '山上有泽咸，君子以虚受人。', attribute: '感应相通' },
  // 32. 雷风恒 ䷟
  { id: 32, name: '恒', symbol: GUA_SYMBOLS[32], upperTrigram: Trigram.ZHEN, lowerTrigram: Trigram.XUN,
    description: '亨，无咎，利贞。利有攸往。',
    interpretation: '雷风恒，君子以立不易方。',
    yaoText: ['初六：浚恒，贞凶，无攸利。', '九二：悔亡。', '九三：不恒其德，或承之羞，贞吝。',
      '九四：田无禽。', '六五：恒其德，贞。妇人吉，夫子凶。', '上六：振恒，凶。'],
    image: '雷风恒，君子以立不易方。', attribute: '恒久不变' },
  // 33. 天山遁 ䷠
  { id: 33, name: '遁', symbol: GUA_SYMBOLS[33], upperTrigram: Trigram.QIAN, lowerTrigram: Trigram.GEN,
    description: '亨，小利贞。',
    interpretation: '天下有山遁，君子以远小人，不恶而严。',
    yaoText: ['初六：遁尾，厉，勿用有攸往。', '六二：执之用黄牛之革，莫之胜说。',
      '九三：系遁，有疾厉，畜臣妾吉。', '九四：好遁，君子吉，小人否。', '九五：嘉遁，贞吉。', '上九：肥遁，无不利。'],
    image: '天下有山遁，君子以远小人。', attribute: '退避隐遁' },
  // 34. 雷天大壮 ䷡
  { id: 34, name: '大壮', symbol: GUA_SYMBOLS[34], upperTrigram: Trigram.ZHEN, lowerTrigram: Trigram.QIAN,
    description: '利贞。',
    interpretation: '雷在天上大壮，君子以非礼弗履。',
    yaoText: ['初九：壮于趾，征凶，有孚。', '九二：贞吉。', '九三：小人用壮，君子用罔，贞厉。羝羊触藩，羸其角。',
      '九四：贞吉悔亡，藩决不羸，壮于大舆之輹。', '六五：丧羊于易，无悔。', '上六：羝羊触藩，不能退，不能遂，无攸利，艰则吉。'],
    image: '雷在天上大壮，君子以非礼弗履。', attribute: '大壮盛极' },
  // 35. 火地晋 ䷢
  { id: 35, name: '晋', symbol: GUA_SYMBOLS[35], upperTrigram: Trigram.LI, lowerTrigram: Trigram.KUN,
    description: '康侯用锡马蕃庶，昼日三接。',
    interpretation: '明出地上晋，君子以自昭明德。',
    yaoText: ['初六：晋如，摧如，贞吉。罔孚，裕无咎。', '六二：晋如，愁如，贞吉。受兹介福，于其王母。',
      '六三：众允，悔亡。', '九四：晋如鼫鼠，贞厉。', '六五：悔亡，失得勿恤，往吉无不利。', '上九：晋其角，维用伐邑，厉吉无咎，贞吝。'],
    image: '明出地上晋，君子以自昭明德。', attribute: '晋升进步' },
  // 36. 地火明夷 ䷣
  { id: 36, name: '明夷', symbol: GUA_SYMBOLS[36], upperTrigram: Trigram.KUN, lowerTrigram: Trigram.LI,
    description: '利艰贞。',
    interpretation: '明入地中明夷，君子以莅众，用晦而明。',
    yaoText: ['初九：明夷于飞，垂其翼。君子于行，三日不食，有攸往，主人有言。',
      '六二：明夷，夷于左股，用拯马壮，吉。', '九三：明夷于南狩，得其大首，不可疾贞。',
      '六四：入于左腹，获明夷之心，于出门庭。', '六五：箕子之明夷，利贞。', '上六：不明晦，初登于天，后入于地。'],
    image: '明入地中明夷，君子以莅众用晦。', attribute: '光明受伤' },
  // 37. 风火家人 ䷤
  { id: 37, name: '家人', symbol: GUA_SYMBOLS[37], upperTrigram: Trigram.XUN, lowerTrigram: Trigram.LI,
    description: '利女贞。',
    interpretation: '风自火出家人，君子以言有物而行有恒。',
    yaoText: ['初九：闲有家，悔亡。', '六二：无攸遂，在中馈，贞吉。', '九三：家人嗃嗃，悔厉吉。妇子嘻嘻，终吝。',
      '六四：富家，大吉。', '九五：王假有家，勿恤，吉。', '上九：有孚威如，终吉。'],
    image: '风自火出家人，君子以言有物。', attribute: '家庭和睦' },
  // 38. 火泽睽 ䷥
  { id: 38, name: '睽', symbol: GUA_SYMBOLS[38], upperTrigram: Trigram.LI, lowerTrigram: Trigram.DUI,
    description: '小事吉。',
    interpretation: '上火下泽睽，君子以同而异。',
    yaoText: ['初九：悔亡，丧马勿逐，自复。见恶人无咎。', '九二：遇主于巷，无咎。',
      '六三：见舆曳，其牛掣，其人天且劓，无初有终。', '九四：睽孤，遇元夫，交孚，厉无咎。',
      '六五：悔亡，厥宗噬肤，往何咎。', '上九：睽孤，见豕负涂，载鬼一车，先张之弧，后说之弧，匪寇婚媾，往遇雨则吉。'],
    image: '上火下泽睽，君子以同而异。', attribute: '乖背睽违' },
  // 39. 水山蹇 ䷦
  { id: 39, name: '蹇', symbol: GUA_SYMBOLS[39], upperTrigram: Trigram.KAN, lowerTrigram: Trigram.GEN,
    description: '利西南，不利东北。利见大人，贞吉。',
    interpretation: '山上有水蹇，君子以反身修德。',
    yaoText: ['初六：往蹇，来誉。', '六二：王臣蹇蹇，匪躬之故。', '九三：往蹇来反。',
      '六四：往蹇来连。', '九五：大蹇朋来。', '上六：往蹇来硕，吉。利见大人。'],
    image: '山上有水蹇，君子以反身修德。', attribute: '蹇难险阻' },
  // 40. 雷水解 ䷧
  { id: 40, name: '解', symbol: GUA_SYMBOLS[40], upperTrigram: Trigram.ZHEN, lowerTrigram: Trigram.KAN,
    description: '利西南，无所往，其来复吉。有攸往，夙吉。',
    interpretation: '雷雨作解，君子以赦过宥罪。',
    yaoText: ['初六：无咎。', '九二：田获三狐，得黄矢，贞吉。', '六三：负且乘，致寇至，贞吝。',
      '九四：解而拇，朋至斯孚。', '六五：君子维有解，吉。有孚于小人。', '上六：公用射隼于高墉之上，获之，无不利。'],
    image: '雷雨作解，君子以赦过宥罪。', attribute: '险难消解' },
  // 41. 山泽损 ䷨
  { id: 41, name: '损', symbol: GUA_SYMBOLS[41], upperTrigram: Trigram.GEN, lowerTrigram: Trigram.DUI,
    description: '有孚，元吉，无咎，可贞。利有攸往。曷之用？二簋可用享。',
    interpretation: '山下有泽损，君子以惩忿窒欲。',
    yaoText: ['初九：已事遄往，无咎，酌损之。', '九二：利贞，征凶，弗损益之。',
      '六三：三人行则损一人，一人行则得其友。', '六四：损其疾，使遄有喜，无咎。',
      '六五：或益之十朋之龟，弗克违，元吉。', '上九：弗损益之，无咎，贞吉，利有攸往，得臣无家。'],
    image: '山下有泽损，君子以惩忿窒欲。', attribute: '损下益上' },
  // 42. 风雷益 ䷩
  { id: 42, name: '益', symbol: GUA_SYMBOLS[42], upperTrigram: Trigram.XUN, lowerTrigram: Trigram.ZHEN,
    description: '利有攸往，利涉大川。',
    interpretation: '风雷益，君子以见善则迁，有过则改。',
    yaoText: ['初九：利用为大作，元吉，无咎。', '六二：或益之十朋之龟，弗克违，永贞吉。王用享于帝，吉。',
      '六三：益之用凶事，无咎。有孚中行，告公用圭。', '六四：中行，告公从，利用为依迁国。',
      '九五：有孚惠心，勿问元吉。有孚惠我德。', '上九：莫益之，或击之，立心勿恒，凶。'],
    image: '风雷益，君子以见善则迁有过则改。', attribute: '损上益下' },
  // 43. 泽天夬 ䷪
  { id: 43, name: '夬', symbol: GUA_SYMBOLS[43], upperTrigram: Trigram.DUI, lowerTrigram: Trigram.QIAN,
    description: '扬于王庭，孚号有厉。告自邑，不利即戎。利有攸往。',
    interpretation: '泽上于天夬，君子以施禄及下，居德则忌。',
    yaoText: ['初九：壮于前趾，往不胜为咎。', '九二：惕号，莫夜有戎，勿恤。',
      '九三：壮于頄，有凶。君子夬夬，独行遇雨，若濡有愠，无咎。', '九四：臀无肤，其行次且。牵羊悔亡，闻言不信。',
      '九五：苋陆夬夬，中行无咎。', '上六：无号，终有凶。'],
    image: '泽上于天夬，君子以施禄及下。', attribute: '刚决果断' },
  // 44. 天风姤 ䷫
  { id: 44, name: '姤', symbol: GUA_SYMBOLS[44], upperTrigram: Trigram.QIAN, lowerTrigram: Trigram.XUN,
    description: '女壮，勿用取女。',
    interpretation: '天下有风姤，后以施命诰四方。',
    yaoText: ['初六：系于金柅，贞吉。有攸往，见凶。羸豕孚蹢躅。', '九二：包有鱼，无咎，不利宾。',
      '九三：臀无肤，其行次且，厉，无大咎。', '九四：包无鱼，起凶。', '九五：以杞包瓜，含章，有陨自天。', '上九：姤其角，吝，无咎。'],
    image: '天下有风姤，后以施命诰四方。', attribute: '遇合邂逅' },
  // 45. 泽地萃 ䷬
  { id: 45, name: '萃', symbol: GUA_SYMBOLS[45], upperTrigram: Trigram.DUI, lowerTrigram: Trigram.KUN,
    description: '亨。王假有庙。利见大人，亨，利贞。用大牲吉。利有攸往。',
    interpretation: '泽上于地萃，君子以除戎器，戒不虞。',
    yaoText: ['初六：有孚不终，乃乱乃萃，若号一握为笑，勿恤，往无咎。',
      '六二：引吉，无咎。孚乃利用禴。', '六三：萃如，嗟如，无攸利。往无咎，小吝。',
      '九四：大吉，无咎。', '九五：萃有位，无咎。匪孚，元永贞，悔亡。', '上六：赍咨涕洟，无咎。'],
    image: '泽上于地萃，君子以除戎器戒不虞。', attribute: '聚集会聚' },
  // 46. 地风升 ䷭
  { id: 46, name: '升', symbol: GUA_SYMBOLS[46], upperTrigram: Trigram.KUN, lowerTrigram: Trigram.XUN,
    description: '元亨，用见大人，勿恤。南征吉。',
    interpretation: '地中生木升，君子以顺德，积小以高大。',
    yaoText: ['初六：允升，大吉。', '九二：孚乃利用禴，无咎。', '九三：升虚邑。',
      '六四：王用亨于岐山，吉无咎。', '六五：贞吉，升阶。', '上六：冥升，利于不息之贞。'],
    image: '地中生木升，君子以顺德积小。', attribute: '上升进展' },
  // 47. 泽水困 ䷮
  { id: 47, name: '困', symbol: GUA_SYMBOLS[47], upperTrigram: Trigram.DUI, lowerTrigram: Trigram.KAN,
    description: '亨，贞，大人吉，无咎。有言不信。',
    interpretation: '泽无水困，君子以致命遂志。',
    yaoText: ['初六：臀困于株木，入于幽谷，三岁不觌。', '九二：困于酒食，朱绂方来，利用享祀，征凶，无咎。',
      '六三：困于石，据于蒺藜，入于其宫，不见其妻，凶。', '九四：来徐徐，困于金车，吝，有终。',
      '九五：劓刖，困于赤绂。乃徐有说，利用祭祀。', '上六：困于葛藟，于臲卼，曰动悔，有悔，征吉。'],
    image: '泽无水困，君子以致命遂志。', attribute: '穷困艰难' },
  // 48. 水风井 ䷯
  { id: 48, name: '井', symbol: GUA_SYMBOLS[48], upperTrigram: Trigram.KAN, lowerTrigram: Trigram.XUN,
    description: '改邑不改井，无丧无得，往来井井。汔至亦未繘井，羸其瓶，凶。',
    interpretation: '木上有水井，君子以劳民劝相。',
    yaoText: ['初六：井泥不食，旧井无禽。', '九二：井谷射鲋，瓮敝漏。', '九三：井渫不食，为我心恻。可用汲，王明，并受其福。',
      '六四：井甃，无咎。', '九五：井洌，寒泉食。', '上六：井收勿幕，有孚元吉。'],
    image: '木上有水井，君子以劳民劝相。', attribute: '井养不息' },
  // 49. 泽火革 ䷰
  { id: 49, name: '革', symbol: GUA_SYMBOLS[49], upperTrigram: Trigram.DUI, lowerTrigram: Trigram.LI,
    description: '己日乃孚，元亨利贞，悔亡。',
    interpretation: '泽中有火革，君子以治历明时。',
    yaoText: ['初九：巩用黄牛之革。', '六二：己日乃革之，征吉，无咎。', '九三：征凶，贞厉。革言三就，有孚。',
      '九四：悔亡，有孚改命，吉。', '九五：大人虎变，未占有孚。', '上六：君子豹变，小人革面，征凶，居贞吉。'],
    image: '泽中有火革，君子以治历明时。', attribute: '变革更新' },
  // 50. 火风鼎 ䷱
  { id: 50, name: '鼎', symbol: GUA_SYMBOLS[50], upperTrigram: Trigram.LI, lowerTrigram: Trigram.XUN,
    description: '元吉，亨。',
    interpretation: '木上有火鼎，君子以正位凝命。',
    yaoText: ['初六：鼎颠趾，利出否，得妾以其子，无咎。', '九二：鼎有实，我仇有疾，不我能即，吉。',
      '九三：鼎耳革，其行塞，雉膏不食，方雨亏悔，终吉。', '九四：鼎折足，覆公餗，其形渥，凶。',
      '六五：鼎黄耳金铉，利贞。', '上九：鼎玉铉，大吉，无不利。'],
    image: '木上有火鼎，君子以正位凝命。', attribute: '鼎新革故' },
  // 51. 震为雷 ䷲
  { id: 51, name: '震', symbol: GUA_SYMBOLS[51], upperTrigram: Trigram.ZHEN, lowerTrigram: Trigram.ZHEN,
    description: '亨。震来虩虩，笑言哑哑。震惊百里，不丧匕鬯。',
    interpretation: '洊雷震，君子以恐惧修省。',
    yaoText: ['初九：震来虩虩，后笑言哑哑，吉。', '六二：震来厉，亿丧贝。跻于九陵，勿逐，七日得。',
      '六三：震苏苏，震行无眚。', '九四：震遂泥。', '六五：震往来厉，亿无丧有事。', '上六：震索索，视矍矍，征凶。震不于其躬，于其邻，无咎。婚媾有言。'],
    image: '洊雷震，君子以恐惧修省。', attribute: '震动惊醒' },
  // 52. 艮为山 ䷳
  { id: 52, name: '艮', symbol: GUA_SYMBOLS[52], upperTrigram: Trigram.GEN, lowerTrigram: Trigram.GEN,
    description: '艮其背，不获其身，行其庭，不见其人，无咎。',
    interpretation: '兼山艮，君子以思不出其位。',
    yaoText: ['初六：艮其趾，无咎，利永贞。', '六二：艮其腓，不拯其随，其心不快。',
      '九三：艮其限，列其夤，厉薰心。', '六四：艮其身，无咎。', '六五：艮其辅，言有序，悔亡。', '上九：敦艮，吉。'],
    image: '兼山艮，君子以思不出其位。', attribute: '静止节制' },
  // 53. 风山渐 ䷴
  { id: 53, name: '渐', symbol: GUA_SYMBOLS[53], upperTrigram: Trigram.XUN, lowerTrigram: Trigram.GEN,
    description: '女归吉，利贞。',
    interpretation: '山上有木渐，君子以居贤德善俗。',
    yaoText: ['初六：鸿渐于干，小子厉，有言，无咎。', '六二：鸿渐于磐，饮食衎衎，吉。',
      '九三：鸿渐于陆，夫征不复，妇孕不育，凶。利御寇。', '六四：鸿渐于木，或得其桷，无咎。',
      '九五：鸿渐于陵，妇三岁不孕，终莫之胜，吉。', '上九：鸿渐于逵，其羽可用为仪，吉。'],
    image: '山上有木渐，君子以居贤德善俗。', attribute: '循序渐进' },
  // 54. 雷泽归妹 ䷵
  { id: 54, name: '归妹', symbol: GUA_SYMBOLS[54], upperTrigram: Trigram.ZHEN, lowerTrigram: Trigram.DUI,
    description: '征凶，无攸利。',
    interpretation: '泽上有雷归妹，君子以永终知敝。',
    yaoText: ['初九：归妹以娣，跛能履，征吉。', '九二：眇能视，利幽人之贞。',
      '六三：归妹以须，反归以娣。', '九四：归妹愆期，迟归有时。', '六五：帝乙归妹，其君之袂，不如其娣之袂良。月几望，吉。',
      '上六：女承筐无实，士刲羊无血，无攸利。'],
    image: '泽上有雷归妹，君子以永终知敝。', attribute: '婚嫁归依' },
  // 55. 雷火丰 ䷶
  { id: 55, name: '丰', symbol: GUA_SYMBOLS[55], upperTrigram: Trigram.ZHEN, lowerTrigram: Trigram.LI,
    description: '亨，王假之。勿忧，宜日中。',
    interpretation: '雷电皆至丰，君子以折狱致刑。',
    yaoText: ['初九：遇其配主，虽旬无咎，往有尚。', '六二：丰其蔀，日中见斗，往得疑疾。有孚发若，吉。',
      '九三：丰其沛，日中见沫，折其右肱，无咎。', '九四：丰其蔀，日中见斗，遇其夷主，吉。',
      '六五：来章，有庆誉，吉。', '上六：丰其屋，蔀其家，窥其户，阒其无人，三岁不觌，凶。'],
    image: '雷电皆至丰，君子以折狱致刑。', attribute: '丰大盛大' },
  // 56. 火山旅 ䷷
  { id: 56, name: '旅', symbol: GUA_SYMBOLS[56], upperTrigram: Trigram.LI, lowerTrigram: Trigram.GEN,
    description: '小亨，旅贞吉。',
    interpretation: '山上有火旅，君子以明慎用刑而不留狱。',
    yaoText: ['初六：旅琐琐，斯其所取灾。', '六二：旅即次，怀其资，得童仆贞。',
      '九三：旅焚其次，丧其童仆，贞厉。', '九四：旅于处，得其资斧，我心不快。',
      '六五：射雉一矢亡，终以誉命。', '上九：鸟焚其巢，旅人先笑后号咷。丧牛于易，凶。'],
    image: '山上有火旅，君子以明慎用刑。', attribute: '旅行漂泊' },
  // 57. 巽为风 ䷸
  { id: 57, name: '巽', symbol: GUA_SYMBOLS[57], upperTrigram: Trigram.XUN, lowerTrigram: Trigram.XUN,
    description: '小亨，利有攸往，利见大人。',
    interpretation: '随风巽，君子以申命行事。',
    yaoText: ['初六：进退，利武人之贞。', '九二：巽在床下，用史巫纷若，吉无咎。',
      '九三：频巽，吝。', '六四：悔亡，田获三品。', '九五：贞吉悔亡，无不利。无初有终，先庚三日，后庚三日，吉。',
      '上九：巽在床下，丧其资斧，贞凶。'],
    image: '随风巽，君子以申命行事。', attribute: '顺从深入' },
  // 58. 兑为泽 ䷹
  { id: 58, name: '兑', symbol: GUA_SYMBOLS[58], upperTrigram: Trigram.DUI, lowerTrigram: Trigram.DUI,
    description: '亨，利贞。',
    interpretation: '丽泽兑，君子以朋友讲习。',
    yaoText: ['初九：和兑，吉。', '九二：孚兑，吉，悔亡。', '六三：来兑，凶。',
      '九四：商兑，未宁，介疾有喜。', '九五：孚于剥，有厉。', '上六：引兑。'],
    image: '丽泽兑，君子以朋友讲习。', attribute: '喜悦和悦' },
  // 59. 风水涣 ䷺
  { id: 59, name: '涣', symbol: GUA_SYMBOLS[59], upperTrigram: Trigram.XUN, lowerTrigram: Trigram.KAN,
    description: '亨。王假有庙，利涉大川，利贞。',
    interpretation: '风行水上涣，先王以享于帝立庙。',
    yaoText: ['初六：用拯马壮，吉。', '九二：涣奔其机，悔亡。', '六三：涣其躬，无悔。',
      '六四：涣其群，元吉。涣有丘，匪夷所思。', '九五：涣汗其大号，涣王居，无咎。', '上九：涣其血，去逖出，无咎。'],
    image: '风行水上涣，先王以享于帝立庙。', attribute: '涣散聚合' },
  // 60. 水泽节 ䷻
  { id: 60, name: '节', symbol: GUA_SYMBOLS[60], upperTrigram: Trigram.KAN, lowerTrigram: Trigram.DUI,
    description: '亨。苦节不可贞。',
    interpretation: '泽上有水节，君子以制数度，议德行。',
    yaoText: ['初九：不出户庭，无咎。', '九二：不出门庭，凶。', '六三：不节若，则嗟若，无咎。',
      '六四：安节，亨。', '九五：甘节，吉。往有尚。', '上六：苦节，贞凶，悔亡。'],
    image: '泽上有水节，君子以制数度议德行。', attribute: '节制节约' },
  // 61. 风泽中孚 ䷼
  { id: 61, name: '中孚', symbol: GUA_SYMBOLS[61], upperTrigram: Trigram.XUN, lowerTrigram: Trigram.DUI,
    description: '豚鱼吉，利涉大川，利贞。',
    interpretation: '泽上有风中孚，君子以议狱缓死。',
    yaoText: ['初九：虞吉，有它不燕。', '九二：鸣鹤在阴，其子和之。我有好爵，吾与尔靡之。',
      '六三：得敌，或鼓或罢，或泣或歌。', '六四：月几望，马匹亡，无咎。', '九五：有孚挛如，无咎。', '上九：翰音登于天，贞凶。'],
    image: '泽上有风中孚，君子以议狱缓死。', attribute: '诚信感应' },
  // 62. 雷山小过 ䷽
  { id: 62, name: '小过', symbol: GUA_SYMBOLS[62], upperTrigram: Trigram.ZHEN, lowerTrigram: Trigram.GEN,
    description: '亨，利贞。可小事，不可大事。飞鸟遗之音，不宜上，宜下，大吉。',
    interpretation: '山上有雷小过，君子以行过乎恭，丧过乎哀，用过乎俭。',
    yaoText: ['初六：飞鸟以凶。', '六二：过其祖，遇其妣。不及其君，遇其臣，无咎。',
      '九三：弗过防之，从或戕之，凶。', '九四：无咎，弗过遇之。往厉必戒，勿用永贞。',
      '六五：密云不雨，自我西郊，公弋取彼在穴。', '上六：弗遇过之，飞鸟离之，凶，是谓灾眚。'],
    image: '山上有雷小过，君子以行过乎恭。', attribute: '小过度' },
  // 63. 水火既济 ䷾
  { id: 63, name: '既济', symbol: GUA_SYMBOLS[63], upperTrigram: Trigram.KAN, lowerTrigram: Trigram.LI,
    description: '亨小，利贞。初吉终乱。',
    interpretation: '水在火上既济，君子以思患而豫防之。',
    yaoText: ['初九：曳其轮，濡其尾，无咎。', '六二：妇丧其茀，勿逐，七日得。',
      '九三：高宗伐鬼方，三年克之。小人勿用。', '六四：繻有衣袽，终日戒。', '九五：东邻杀牛，不如西邻之禴祭，实受其福。',
      '上六：濡其首，厉。'],
    image: '水在火上既济，君子以思患而豫防之。', attribute: '既成未成' },
  // 64. 火水未济 ䷿
  { id: 64, name: '未济', symbol: GUA_SYMBOLS[64], upperTrigram: Trigram.LI, lowerTrigram: Trigram.KAN,
    description: '亨。小狐汔济，濡其尾，无攸利。',
    interpretation: '火在水上未济，君子以慎辨物居方。',
    yaoText: ['初六：濡其尾，吝。', '九二：曳其轮，贞吉。', '六三：未济，征凶，利涉大川。',
      '九四：贞吉，悔亡。震用伐鬼方，三年有赏于大国。', '六五：贞吉，无悔。君子之光，有孚，吉。',
      '上九：有孚于饮酒，无咎。濡其首，有孚失是。'],
    image: '火在水上未济，君子以慎辨物居方。', attribute: '事业未成' },
];

/**
 * 根据上下卦获取卦象
 * 64卦 = 上卦(3位二进制) × 下卦(3位二进制) = 6位二进制 → 查表
 */
export function getHexagramByTrigrams(upper: Trigram, lower: Trigram): Hexagram | undefined {
  return HEXAGRAM_DATA.find(h => h.upperTrigram === upper && h.lowerTrigram === lower);
}

/**
 * 根据ID获取卦象
 */
export function getHexagramById(id: number): Hexagram | undefined {
  if (id < 1 || id > 64) return undefined;
  return HEXAGRAM_DATA[id - 1];
}

/**
 * 周易卦序歌（速查）
 */
export const HEXAGRAM_SONG: string[] = [
  '', '乾', '坤', '屯', '蒙', '需', '讼', '师', '比',
  '小畜', '履', '泰', '否', '同人', '大有', '谦', '豫',
  '随', '蛊', '临', '观', '噬嗑', '贲', '剥', '复',
  '无妄', '大畜', '颐', '大过', '坎', '离', '咸', '恒',
  '遁', '大壮', '晋', '明夷', '家人', '睽', '蹇', '解',
  '损', '益', '夬', '姤', '萃', '升', '困', '井',
  '革', '鼎', '震', '艮', '渐', '归妹', '丰', '旅',
  '巽', '兑', '涣', '节', '中孚', '小过', '既济', '未济',
];
