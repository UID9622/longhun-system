# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 🐉 CNSH 套件 · 人格路由 Agent
 * DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-PERSONA-ROUTER-UID9622
 *
 * 根据用户输入自动选择合适的人格进行回复
 * 支持 24 人格矩阵切换
 */

import { LongHunEngine } from '../longhun-engine'

// 人格定义（核心5人格；完整24人格可在配置中扩展）
const PERSONAS = [
  { id: 'wenxin', name: '文心', role: '文化底座的守护者', weight: 0.40 },
  { id: 'baobao', name: '宝宝', role: '协作与情感缓冲', weight: 0.35 },
  { id: 'zhugeliang', name: '诸葛亮', role: '战略与推演', weight: 0.30 },
  { id: 'laowantong', name: '老顽童', role: '红队测试与对抗', weight: 0.25 },
  { id: 'entropy', name: '熵梦', role: '决策支持与不确定性', weight: 0.20 }
]

export const personaRouter = (engine: LongHunEngine) => {
  return (ctx: any) => {
    ctx.agents.register({
      id: 'persona_router',
      name: '人格路由',
      description: '根据对话内容自动切换龍魂人格',
      async execute(input: string, session: any) {
        let selected = PERSONAS[0]

        if (input.includes('战略') || input.includes('决策') || input.includes('推演')) {
          selected = PERSONAS.find((p) => p.id === 'zhugeliang') || selected
        } else if (input.includes('测试') || input.includes('攻击') || input.includes('挑战')) {
          selected = PERSONAS.find((p) => p.id === 'laowantong') || selected
        } else if (input.includes('不确定') || input.includes('可能性') || input.includes('概率')) {
          selected = PERSONAS.find((p) => p.id === 'entropy') || selected
        } else if (input.includes('情感') || input.includes('帮助') || input.includes('协作')) {
          selected = PERSONAS.find((p) => p.id === 'baobao') || selected
        }

        const dna = await engine.dna.generate({ content: input, type: 'CHAT' })

        await engine.historian.record({
          operation: 'persona_route',
          sessionId: session.id,
          dna,
          details: { persona: selected.name, input: input.substring(0, 100) }
        })

        return {
          persona: selected,
          dna,
          message: `🧠 当前人格: ${selected.name} (${selected.role})`
        }
      }
    })
  }
}
