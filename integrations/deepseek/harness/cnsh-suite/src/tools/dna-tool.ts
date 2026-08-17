/**
 * 🐉 CNSH 套件 · DNA 追溯工具
 * DNA: #龍芯⚡️丙午·丙申·庚申·亥时-DNA-TOOL-UID9622
 */

import { defineTool } from '@deepseek-ai/dsh-tools'
import { LongHunEngine } from '../longhun-engine'

export const dnaTool = (engine: LongHunEngine) => defineTool({
  name: 'generate_dna',
  description: '生成龍魂DNA追溯码，为任何内容绑定唯一主权身份。格式：#龍芯⚡️{干支·时辰·卦}-{类型}-{哈希}-UID9622',
  parameters: {
    type: 'object',
    properties: {
      content: {
        type: 'string',
        description: '需要绑定DNA的内容'
      },
      type: {
        type: 'string',
        enum: ['DOCUMENT', 'CODE', 'CHAT', 'AUDIT'],
        description: '内容类型',
        default: 'DOCUMENT'
      },
      parent: {
        type: 'string',
        description: '父DNA追溯码（用于版本链）'
      }
    },
    required: ['content']
  },
  execute: async ({ content, type = 'DOCUMENT', parent }, _ctx) => {
    const dna = await engine.dna.generate({ content, type, parent })
    const parsed = await engine.dna.parse(dna)

    return {
      success: true,
      dna,
      parsed,
      message: `✅ DNA已生成: ${dna}`,
      _historian: {
        operation: 'generate_dna',
        details: { content_length: content.length, type }
      }
    }
  }
})
