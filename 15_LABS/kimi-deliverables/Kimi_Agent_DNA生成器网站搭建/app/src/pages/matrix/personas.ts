# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-52b3ff55
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
/**
 * 十六人格名表 —— 以军事 / 谋略意象命名（白皮书 v1.4 占位，保持庄重）
 * 五维序：MIL 军事 · HIS 历史 · PHI 哲学 · ECO 经济 · POL 政治
 */

export const DIMS = [
  { key: 'MIL', name: '军事', desc: '战略、执行、决断与风险控制', trigram: '☰' },
  { key: 'HIS', name: '历史', desc: '以史为鉴，长周期演化的眼光', trigram: '☱' },
  { key: 'PHI', name: '哲学', desc: '本体与伦理，追问「为何」', trigram: '☲' },
  { key: 'ECO', name: '经济', desc: '资源、激励与可持续', trigram: '☳' },
  { key: 'POL', name: '政治', desc: '秩序、协商与公共利益', trigram: '☴' },
] as const

export type DimKey = (typeof DIMS)[number]['key']

/** 金阶五色（由深到浅），供五维条 / 堆叠图使用 */
export const DIM_COLORS = ['#8A6D1F', '#A8871F', '#C9A227', '#DDB947', '#E9CB6B'] as const

export interface Persona {
  /** 二字代号（矩阵格巨字） */
  code: string
  /** 全称（代号 · 人物意象） */
  full: string
  /** 编号 M-01…M-16 */
  no: string
  /** 主维 */
  primary: DimKey
  /** 五维配比（0–100，总和 100） */
  vector: [number, number, number, number, number]
  /** 人格志（3–4 行） */
  bio: string
}

export const PERSONAS: Persona[] = [
  {
    code: '武侯', full: '武侯 · 诸葛', no: 'M-01', primary: 'MIL',
    vector: [34, 20, 16, 10, 20],
    bio: '鞠躬尽瘁的统筹者。未出茅庐已知三分，凡事预则立。善将战略拆解为可执行之阵，于约束中谋全胜，是内阁的总参谋。',
  },
  {
    code: '兵圣', full: '兵圣 · 孙武', no: 'M-02', primary: 'MIL',
    vector: [44, 16, 14, 8, 18],
    bio: '兵法之源。先胜后战，算于庙堂之上。以最少代价求最大确定，其言十三篇，至今仍是决断者的第一读本。',
  },
  {
    code: '谋圣', full: '谋圣 · 姜尚', no: 'M-03', primary: 'MIL',
    vector: [30, 26, 18, 8, 18],
    bio: '渭水垂纶，待时而后动。大器晚成的战略耐心：不谋一时，谋百世之局。长于判断「何时不动」比「如何动」更重要。',
  },
  {
    code: '兵仙', full: '兵仙 · 韩信', no: 'M-04', primary: 'MIL',
    vector: [40, 18, 10, 10, 22],
    bio: '多多益善的调度天才。背水一战、暗度陈仓——在资源极度受限处创造胜势，是执行维度的极限样本。',
  },
  {
    code: '亚圣', full: '亚圣 · 吴起', no: 'M-05', primary: 'MIL',
    vector: [36, 16, 12, 14, 22],
    bio: '与士卒同甘苦的治军者。令行禁止之外，更懂组织的人心向背。制度与情义并重，是纪律温度的化身。',
  },
  {
    code: '司马', full: '司马 · 穰苴', no: 'M-06', primary: 'MIL',
    vector: [34, 20, 12, 10, 24],
    bio: '立表下漏，军法如山。以规则立威、以表率立信。提醒内阁：任何系统的信用，始于对规则的自身服从。',
  },
  {
    code: '尉缭', full: '尉缭 · 兵略', no: 'M-07', primary: 'MIL',
    vector: [32, 22, 18, 12, 16],
    bio: '兵形势家之眼。重势不重形，观全局之结构而落子。长于在混沌中识别杠杆点，一击而全局皆活。',
  },
  {
    code: '军神', full: '军神 · 李靖', no: 'M-08', primary: 'MIL',
    vector: [38, 22, 12, 8, 20],
    bio: '平定四方的收官者。善打「最后一战」：快、准、彻底，不留后患。代表执行链条的完成度与闭环意识。',
  },
  {
    code: '武穆', full: '武穆 · 岳飞', no: 'M-09', primary: 'POL',
    vector: [30, 20, 20, 6, 24],
    bio: '精忠与纪律并峙。冻死不拆屋，饿死不掳掠——信念驱动的组织，其动员力超越一切激励设计。',
  },
  {
    code: '将略', full: '将略 · 戚继光', no: 'M-10', primary: 'MIL',
    vector: [34, 18, 12, 16, 20],
    bio: '鸳鸯阵的工程师。把战术写成操典、把经验沉淀为可复制的训练体系。是「把方法变成制度」的人格。',
  },
  {
    code: '仲父', full: '仲父 · 管仲', no: 'M-11', primary: 'ECO',
    vector: [14, 20, 12, 34, 20],
    bio: '轻重之术的开山者。仓廪实而知礼节——以经济规律为纲，四维张而国不倾。内阁中的资源与激励总设计师。',
  },
  {
    code: '商君', full: '商君 · 商鞅', no: 'M-12', primary: 'POL',
    vector: [18, 16, 14, 18, 34],
    bio: '徙木立信的制度锻造者。法之不行，自上犯之。以刚性规则重塑秩序，代价与争议并载史册，供内阁深省。',
  },
  {
    code: '纵横', full: '纵横 · 苏秦', no: 'M-13', primary: 'POL',
    vector: [16, 20, 18, 12, 34],
    bio: '合纵的缔盟者。佩六国相印，以共识编织力量。代表协商、联盟与话语的组织力——把分散的意志拧成一股。',
  },
  {
    code: '连横', full: '连横 · 张仪', no: 'M-14', primary: 'POL',
    vector: [18, 18, 16, 14, 34],
    bio: '破局的谈判家。于不可能处拆解联盟、以言辞易城池。提醒内阁：最锋利的武器，往往是对人心的精确度量。',
  },
  {
    code: '陶朱', full: '陶朱 · 范蠡', no: 'M-15', primary: 'ECO',
    vector: [16, 22, 22, 30, 10],
    bio: '三致千金而三散之。既谋身、更谋世，知进退存亡之机。可持续的人格化身：盈利是手段，绝非目的。',
  },
  {
    code: '鬼谷', full: '鬼谷 · 王诩', no: 'M-16', primary: 'PHI',
    vector: [18, 22, 36, 8, 16],
    bio: '捭阖之道的源头。观阴阳开阖以命物，知存亡之门户。不问一策一计，只问万物运行之「道」，是内阁的终极追问者。',
  },
]

/** 4×4 网格中距中心 (1.5, 1.5) 的径向距离（用于入场 stagger） */
export const radialDelay = (index: number): number => {
  const r = Math.floor(index / 4)
  const c = index % 4
  const d = Math.hypot(r - 1.5, c - 1.5)
  return d * 0.09
}
