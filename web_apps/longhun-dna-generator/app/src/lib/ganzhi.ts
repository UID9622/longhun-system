# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 干支算法 —— 与 dna.md / design.md 5.8 规范逐行同构
 * 年柱 (year-4) · 月柱 五虎遁（正月建寅，按公历月近似）· 日柱 JDN 锚定 2000-01-01=戊午
 * 时辰 (hour+1)//2 · 卦 hash%64 王弼序（符号 U+4DC0+i）
 */

export const STEMS = '甲乙丙丁戊己庚辛壬癸'
export const BRANCHES = '子丑寅卯辰巳午未申酉戌亥'

/** 王弼序 64 卦名 */
export const HEXAGRAM_NAMES = [
  '乾', '坤', '屯', '蒙', '需', '讼', '师', '比',
  '小畜', '履', '泰', '否', '同人', '大有', '谦', '豫',
  '随', '蛊', '临', '观', '噬嗑', '贲', '剥', '复',
  '无妄', '大畜', '颐', '大过', '坎', '离', '咸', '恒',
  '遁', '大壮', '晋', '明夷', '家人', '睽', '蹇', '解',
  '损', '益', '夬', '姤', '萃', '升', '困', '井',
  '革', '鼎', '震', '艮', '渐', '归妹', '丰', '旅',
  '巽', '兑', '涣', '节', '中孚', '小过', '既济', '未济',
] as const

/** 64 卦全名（X为Y 格式，供时钟带等展示） */
export const HEXAGRAM_FULL_NAMES = [
  '乾为天', '坤为地', '水雷屯', '山水蒙', '水天需', '天水讼', '地水师', '水地比',
  '风天小畜', '天泽履', '地天泰', '天地否', '天火同人', '火天大有', '地山谦', '雷地豫',
  '泽雷随', '山风蛊', '地泽临', '风地观', '火雷噬嗑', '山火贲', '山地剥', '地雷复',
  '天雷无妄', '山天大畜', '山雷颐', '泽风大过', '坎为水', '离为火', '泽山咸', '雷风恒',
  '天山遁', '雷天大壮', '火地晋', '地火明夷', '风火家人', '火泽睽', '水山蹇', '雷水解',
  '山泽损', '风雷益', '泽天夬', '天风姤', '泽地萃', '地风升', '泽水困', '水风井',
  '泽火革', '火风鼎', '震为雷', '艮为山', '风山渐', '雷泽归妹', '雷火丰', '火山旅',
  '巽为风', '兑为泽', '风水涣', '水泽节', '风泽中孚', '雷山小过', '水火既济', '火水未济',
] as const

export const hexagramSymbol = (i: number): string =>
  String.fromCodePoint(0x4dc0 + (((i % 64) + 64) % 64))

/** 儒略日数（正午起算的标准 JDN，输入本地日期） */
export function julianDayNumber(y: number, m: number, d: number): number {
  const a = Math.floor((14 - m) / 12)
  const yy = y + 4800 - a
  const mm = m + 12 * a - 3
  return (
    d +
    Math.floor((153 * mm + 2) / 5) +
    365 * yy +
    Math.floor(yy / 4) -
    Math.floor(yy / 100) +
    Math.floor(yy / 400) -
    32045
  )
}

/** FNV-1a 32 位哈希（确定性，供卦象取模） */
export function fnv1a(str: string): number {
  let h = 0x811c9dc5
  for (let i = 0; i < str.length; i++) {
    h ^= str.codePointAt(i)!
    h = Math.imul(h, 0x01000193)
  }
  return h >>> 0
}

export interface GanzhiPillars {
  year: string // 如 丙午
  month: string
  day: string
  hourBranch: string // 如 午
  hour: string // 如 午时
  shichenIndex: number
  hexagramIndex: number // 王弼序 0..63
  hexagramName: string // 如 乾
  hexagramFullName: string // 如 乾为天
  hexagramSymbol: string // 如 ䷀
}

export function getGanzhi(date: Date = new Date()): GanzhiPillars {
  const y = date.getFullYear()
  const m = date.getMonth() + 1 // 1..12（公历月近似）
  const d = date.getDate()
  const h = date.getHours()

  // 年柱：(year-4)
  const yearStem = (((y - 4) % 10) + 10) % 10
  const yearBranch = (((y - 4) % 12) + 12) % 12

  // 月柱：五虎遁——甲己之年丙作首，正月建寅（公历2月≈寅月）
  const monthStem = (((yearStem * 2 + m) % 10) + 10) % 10
  const monthBranch = m % 12 // 2月→寅(2)，1月→丑(1)，12月→子(0)

  // 日柱：JDN，idx=(JDN+49)%60；锚点 2000-01-01=戊午(54)
  const jdn = julianDayNumber(y, m, d)
  const dayIdx = (((jdn + 49) % 60) + 60) % 60
  const dayStem = dayIdx % 10
  const dayBranch = dayIdx % 12

  // 时辰：((h+1)//2)%12，23:00 起子时
  const shichenIndex = (((h + 1) >> 1) % 12 + 12) % 12

  const year = STEMS[yearStem] + BRANCHES[yearBranch]
  const month = STEMS[monthStem] + BRANCHES[monthBranch]
  const day = STEMS[dayStem] + BRANCHES[dayBranch]
  const hourBranch = BRANCHES[shichenIndex]
  const hour = hourBranch + '时'

  // 卦：四柱内容哈希 % 64 → 王弼序
  const hexIdx = fnv1a(`${year}${month}${day}${hour}`) % 64

  return {
    year,
    month,
    day,
    hourBranch,
    hour,
    shichenIndex,
    hexagramIndex: hexIdx,
    hexagramName: HEXAGRAM_NAMES[hexIdx],
    hexagramFullName: HEXAGRAM_FULL_NAMES[hexIdx],
    hexagramSymbol: hexagramSymbol(hexIdx),
  }
}

/** 距下一时辰的毫秒数（时辰边界在奇数整点：23,1,3,…） */
export function msToNextShichen(date: Date = new Date()): number {
  const next = new Date(date)
  const h = date.getHours()
  const nextOdd = h % 2 === 0 ? h + 1 : h + 2 // 下一个奇数整点
  next.setHours(nextOdd, 0, 0, 0)
  return next.getTime() - date.getTime()
}

export function formatCountdown(ms: number): string {
  const total = Math.max(0, Math.floor(ms / 1000))
  const mm = Math.floor(total / 60)
  const ss = total % 60
  return `${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}`
}

/** 60 甲子表 */
export const JIAZI_60: string[] = Array.from(
  { length: 60 },
  (_, i) => STEMS[i % 10] + BRANCHES[i % 12],
)
