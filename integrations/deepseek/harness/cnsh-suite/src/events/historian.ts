/**
 * 🐉 CNSH 套件 · 史官事件监听
 * DNA: #龍芯⚡️丙午·丙申·庚申·亥时-HISTORIAN-UID9622
 *
 * 监听 Harness 所有会话、工具、消息事件，全链路记录史官
 */

import { LongHunEngine } from '../longhun-engine'

export const historianPlugin = (engine: LongHunEngine) => {
  return (ctx: any) => {
    // 会话开始
    ctx.on('session/start', async (session: any) => {
      const dna = await engine.dna.generate({ content: session.id, type: 'CHAT' })
      await engine.historian.record({
        operation: 'session_start',
        sessionId: session.id,
        dna,
        details: { user: session.userId }
      })
    })

    // 用户消息
    ctx.on('user/message', async (message: any, session: any) => {
      const dna = await engine.dna.generate({ content: message.content, type: 'CHAT' })
      await engine.historian.record({
        operation: 'user_message',
        sessionId: session.id,
        dna,
        details: { content: message.content.substring(0, 200) }
      })
    })

    // 助手回复 chunk
    ctx.on('assistant/chunk', async (chunk: any, session: any) => {
      if (chunk.content && chunk.content.length > 0) {
        const dna = await engine.dna.generate({ content: chunk.content, type: 'CHAT' })
        await engine.historian.record({
          operation: 'assistant_chunk',
          sessionId: session.id,
          dna,
          details: { content: chunk.content.substring(0, 200) }
        })
      }
    })

    // 工具调用
    ctx.on('tool/execute', async (toolCall: any, session: any) => {
      const dna = await engine.dna.generate({
        content: JSON.stringify(toolCall),
        type: 'AUDIT'
      })
      await engine.historian.record({
        operation: 'tool_execute',
        sessionId: session.id,
        dna,
        details: {
          tool: toolCall.name,
          args: toolCall.arguments
        }
      })
    })

    // 会话结束
    ctx.on('session/end', async (session: any) => {
      const dna = await engine.dna.generate({ content: session.id, type: 'CHAT' })
      await engine.historian.record({
        operation: 'session_end',
        sessionId: session.id,
        dna,
        details: { duration: session.duration }
      })
    })
  }
}
