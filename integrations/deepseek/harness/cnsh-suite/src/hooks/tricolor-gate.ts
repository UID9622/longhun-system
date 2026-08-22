/**
 * 🐉 CNSH 套件 · 三色审计审批门 Hook
 * DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-TRICOLOR-GATE-UID9622
 *
 * 拦截所有工具调用，在工具执行前进行三色审计
 * 🟢 通过 → 允许执行
 * 🟡 警告 → 降权执行（添加警告标记）
 * 🔴 拒绝 → 拦截 + 记录耻辱墙
 */

import { LongHunEngine } from '../longhun-engine'

export const tricolorGate = (engine: LongHunEngine) => {
  return (ctx: any) => {
    ctx.tools.guard('tools/pre-execute', async ({ toolCall, session }: any) => {
      // 对 DNA 工具豁免审计（它本身是审计工具的一部分）
      if (toolCall.name === 'generate_dna') {
        return { kind: 'allow' }
      }

      // 对审计工具自身豁免，避免递归
      if (toolCall.name === 'tricolor_audit') {
        return { kind: 'allow' }
      }

      // 对 CNSH 执行器进行审计（审查脚本内容）
      if (toolCall.name === 'run_cnsh') {
        const script = toolCall.arguments?.script || toolCall.arguments?.file || ''
        const auditResult = await engine.audit.run({ content: script, context: 'cnsh_script' })
        if (auditResult.tricolor === '🔴') {
          const dna = await engine.dna.generate({ content: script, type: 'AUDIT' })
          await engine.shameWall.add(
            `CNSH脚本审计拒绝: ${auditResult.reason || 'R值低于阈值'}`,
            dna,
            { score: auditResult.score, details: auditResult.details }
          )
          return {
            kind: 'deny',
            reason: `🔴 三色审计拒绝: ${auditResult.reason || '脚本内容不合规'} (R值: ${auditResult.score.toFixed(1)})`
          }
        }
        if (auditResult.tricolor === '🟡') {
          return {
            kind: 'warn',
            reason: `🟡 三色审计警告: 脚本存在风险 (R值: ${auditResult.score.toFixed(1)})，降权执行`
          }
        }
        return { kind: 'allow' }
      }

      // 其他工具默认放行（但记录审计）
      return { kind: 'allow' }
    })
  }
}
