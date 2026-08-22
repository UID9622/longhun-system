/**
 * 🐉 CNSH 套件 · 三色审计工具
 * DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-TRICOLOR-TOOL-UID9622
 */

import { defineTool } from '@deepseek-ai/dsh-tools'
import { LongHunEngine } from '../longhun-engine'

export const tricolorTool = (engine: LongHunEngine) => defineTool({
  name: 'tricolor_audit',
  description: '对内容进行龍魂三色审计（🟢通过 / 🟡警告 / 🔴拒绝），返回R值和详细评分',
  parameters: {
    type: 'object',
    properties: {
      content: {
        type: 'string',
        description: '待审计的内容'
      },
      context: {
        type: 'string',
        description: '审计上下文（如场景说明）'
      }
    },
    required: ['content']
  },
  execute: async ({ content, context = '' }, _ctx) => {
    const result = await engine.audit.run({ content, context })

    // 如果审计失败，记录到耻辱墙
    if (!result.passed) {
      const dna = await engine.dna.generate({ content: content.substring(0, 100), type: 'AUDIT' })
      await engine.shameWall.add(
        `三色审计拒绝: ${result.reason || 'R值低于阈值'}`,
        dna,
        { score: result.score, details: result.details }
      )
    }

    return {
      success: true,
      tricolor: result.tricolor,
      score: result.score,
      passed: result.passed,
      details: result.details,
      reason: result.reason,
      message: result.passed
        ? `${result.tricolor} 审计通过 (R值: ${result.score.toFixed(1)})`
        : `${result.tricolor} 审计拒绝 (R值: ${result.score.toFixed(1)}) - ${result.reason || '请检查内容'}`
    }
  }
})
