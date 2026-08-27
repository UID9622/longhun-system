# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * DNA 验证器（design/dna.md §S4）
 * 逐段解析格式 v2.0：#龍芯⚡️{年}·{月}·{日}·{时辰}·{卦符卦名}-{动作}-{版本}-{日序号}-{哈希8}
 * 自洽性校验：干支须为合法甲子（干支配对同奇偶）、月柱与年柱须符合五虎遁、
 * 卦符（U+4DC0+i）与卦名须同王弼序一致、版本/序号/哈希须合规。
 */
import { STEMS, BRANCHES, HEXAGRAM_NAMES } from '@/lib/ganzhi'

export interface ParsedFields {
  year: string
  month: string
  day: string
  hour: string
  hexSymbol: string
  hexName: string
  hexIndex: number
  action: string
  version: string
  serial: string
  hash: string
}

export interface FieldIssue {
  field: string
  message: string
  segment?: string
}

export interface VerifyResult {
  status: 'ok' | 'fail'
  fields: Partial<ParsedFields>
  issues: FieldIssue[]
  /** 首个不合规字段原文（供标红下划线） */
  badSegment?: string
}

function ganzhiPair(s: string): { stem: number; branch: number } | null {
  const chars = Array.from(s)
  if (chars.length !== 2) return null
  const stem = STEMS.indexOf(chars[0])
  const branch = BRANCHES.indexOf(chars[1])
  if (stem < 0 || branch < 0) return null
  return { stem, branch }
}

/** 合法六十甲子：天干序与地支序同奇偶 */
function isValidJiazi(p: { stem: number; branch: number }): boolean {
  return p.stem % 2 === p.branch % 2
}

export function verifyDna(input: string): VerifyResult {
  const raw = input.trim()
  const fields: Partial<ParsedFields> = {}
  const issues: FieldIssue[] = []
  let badSegment: string | undefined

  const fail = (field: string, message: string, segment?: string) => {
    issues.push({ field, message, segment })
    if (badSegment === undefined && segment !== undefined) badSegment = segment
  }

  if (!raw) {
    fail('整体', '空串无码可验')
    return { status: 'fail', fields, issues, badSegment }
  }

  // 族徽前缀（⚡ 可带 U+FE0F 变体选择符）
  const mPrefix = raw.match(/^#龍芯⚡️?/u)
  if (!mPrefix) {
    fail('族徽前缀', '须以 #龍芯⚡️ 起首', raw.slice(0, 6))
    return { status: 'fail', fields, issues, badSegment }
  }
  const body = raw.slice(mPrefix[0].length)

  // 「·」分五段：年 月 日 时辰 (卦+尾链)
  const dotParts = body.split('·')
  if (dotParts.length !== 5) {
    fail('分隔符之礼', `四柱与卦应以 4 枚「·」分出 5 段，实为 ${dotParts.length} 段`, body)
    return { status: 'fail', fields, issues, badSegment }
  }
  const [ySeg, mSeg, dSeg, hSeg, tail] = dotParts

  // 年柱
  const yPair = ganzhiPair(ySeg)
  if (!yPair) {
    fail('年柱', '非合法干支二字', ySeg)
  } else if (!isValidJiazi(yPair)) {
    fail('年柱', '干支配对不在六十甲子之内', ySeg)
  } else {
    fields.year = ySeg
  }

  // 月柱 + 五虎遁交叉校验
  const mPair = ganzhiPair(mSeg)
  if (!mPair) {
    fail('月柱', '非合法干支二字', mSeg)
  } else if (!isValidJiazi(mPair)) {
    fail('月柱', '干支配对不在六十甲子之内', mSeg)
  } else {
    fields.month = mSeg
    if (yPair && isValidJiazi(yPair)) {
      // 支序反推公历月：子(0)→12月，丑(1)→1月 … 亥(11)→11月
      const mNum = mPair.branch === 0 ? 12 : mPair.branch
      const expectedStem = (((yPair.stem * 2 + mNum) % 10) + 10) % 10
      if (expectedStem !== mPair.stem) {
        fail('月柱', `与年柱不符五虎遁（${ySeg}年${BRANCHES[mPair.branch]}月当为${STEMS[expectedStem]}）`, mSeg)
      }
    }
  }

  // 日柱
  const dPair = ganzhiPair(dSeg)
  if (!dPair) {
    fail('日柱', '非合法干支二字', dSeg)
  } else if (!isValidJiazi(dPair)) {
    fail('日柱', '干支配对不在六十甲子之内', dSeg)
  } else {
    fields.day = dSeg
  }

  // 时辰
  if (!/^[子丑寅卯辰巳午未申酉戌亥]时$/u.test(hSeg)) {
    fail('时辰', '须为「地支+时」，如 午时', hSeg)
  } else {
    fields.hour = hSeg
  }

  // 尾链：卦-动作-版本-序号-哈希（动作自身可含「-」，自右向左定界）
  const chain = tail.split('-')
  if (chain.length < 5) {
    fail('尾链', '卦符卦名之后应有 动作-版本-序号-哈希 四段', tail)
    return { status: 'fail', fields, issues, badSegment }
  }
  const hexSeg = chain[0]
  const hash = chain[chain.length - 1]
  const serial = chain[chain.length - 2]
  const version = chain[chain.length - 3]
  const action = chain.slice(1, -3).join('-')

  // 卦符卦名：符号 U+4DC0+i 与卦名须同序
  const hexChars = Array.from(hexSeg)
  const sym = hexChars[0] ?? ''
  const cp = sym.codePointAt(0) ?? 0
  if (cp < 0x4dc0 || cp > 0x4dff) {
    fail('卦符卦名', '卦符须在 U+4DC0–U+4DFF', hexSeg)
  } else {
    const idx = cp - 0x4dc0
    const name = hexChars.slice(1).join('')
    if (name !== HEXAGRAM_NAMES[idx]) {
      fail('卦符卦名', `卦符为王弼序第 ${idx + 1} 卦「${HEXAGRAM_NAMES[idx]}」，与所署卦名不合`, hexSeg)
    } else {
      fields.hexSymbol = sym
      fields.hexName = name
      fields.hexIndex = idx
    }
  }

  // 动作标签
  if (!/^[A-Z][A-Z0-9-]{1,31}$/.test(action)) {
    fail('动作标签', '须为大写拉丁/数字/连字符（如 CREATE、AUDIT-REPORT）', action)
  } else {
    fields.action = action
  }

  // 版本号
  if (!/^v\d+\.\d+$/.test(version)) {
    fail('版本号', '须形如 v1.0', version)
  } else {
    fields.version = version
  }

  // 日序号
  if (!/^\d{4}$/.test(serial)) {
    fail('日序号', '须为 4 位数字（0001 起）', serial)
  } else {
    fields.serial = serial
  }

  // 哈希 8 位
  if (!/^[0-9a-fA-F]{8}$/.test(hash)) {
    fail('内容哈希', '须为 8 位 hex', hash)
  } else {
    fields.hash = hash.toLowerCase()
  }

  return { status: issues.length === 0 ? 'ok' : 'fail', fields, issues, badSegment }
}
