# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-52b3ff55
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
/**
 * 啟動AI · 四人格路由表（与龍魂人格矩阵运行时一致）
 * 审计师=朱砂印 · 架构师=金印 · 哲人=米白印 · 助手=金印
 */

export type PersonaId = 'auditor' | 'coder' | 'philosopher' | 'generalist'

export interface Persona {
  id: PersonaId
  name: string
  latin: string // Cinzel 印章小字
  description: string
  triggerKeywords: string[]
  sealColor: 'vermilion' | 'gold' | 'paper'
  sealChar: string // 印章内刻字
}

export const PERSONAS: Record<PersonaId, Persona> = {
  auditor: {
    id: 'auditor',
    name: '龍魂审计师',
    latin: 'AUDITOR',
    description: '以 P0 宪法为尺，输出三色判定的结构化审计',
    triggerKeywords: [
      '审计', '协议', '规则', '违规', '条款', '消费者权益', '维权',
      '合规', '法律', '判定', '审查', '宪法', '焊死',
    ],
    sealColor: 'vermilion',
    sealChar: '審',
  },
  coder: {
    id: 'coder',
    name: '龍魂架构师',
    latin: 'ARCHITECT',
    description: '以可运行代码作答，每一行皆可审计',
    triggerKeywords: [
      '写代码', '生成', '脚本', '实现', '开发', 'python', '部署',
      '代码', '函数', '接口', '算法实现', 'typescript', 'bug',
    ],
    sealColor: 'gold',
    sealChar: '構',
  },
  philosopher: {
    id: 'philosopher',
    name: '龍魂哲人',
    latin: 'PHILOSOPHER',
    description: '以易解世：卦象 · 现代映射 · 启示 三段论',
    triggerKeywords: [
      '卦', '易经', '哲理', '阴阳', '五行', '未济', '既济',
      '六十四卦', '爻', '启示', '哲学',
    ],
    sealColor: 'paper',
    sealChar: '哲',
  },
  generalist: {
    id: 'generalist',
    name: '龍魂助手',
    latin: 'STEWARD',
    description: '站内知识与外部索引的兜底应答',
    triggerKeywords: [],
    sealColor: 'gold',
    sealChar: '佐',
  },
}

export const PERSONA_ORDER: PersonaId[] = ['auditor', 'coder', 'philosopher']

/**
 * 人格路由：触发词计分，最高分胜出；零分或平局 → generalist
 */
export function routePersona(question: string): Persona {
  const q = question.toLowerCase()
  let best: Persona = PERSONAS.generalist
  let bestScore = 0
  for (const id of PERSONA_ORDER) {
    const p = PERSONAS[id]
    let score = 0
    for (const kw of p.triggerKeywords) {
      if (q.includes(kw.toLowerCase())) score += kw.length >= 2 ? 2 : 1
    }
    if (score > bestScore) {
      bestScore = score
      best = p
    }
  }
  return best
}
