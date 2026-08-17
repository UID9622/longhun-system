/**
 * 🐉 CNSH 套件 · 主入口
 * DNA: #龍芯⚡️丙午·丙申·庚申·亥时-CNSH-SUITE-UID9622
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 * GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 *
 * 插件集：将 CNSH 主权底座以插件形式焊入 DeepSeek Harness
 *
 * 安装:
 *   pnpm add @longhun/cnsh-suite
 *
 * 加载:
 *   - 在 cordis.patch.yml 中添加 '@longhun/cnsh-suite'
 *   - 或通过 dsh --profile web 自动加载
 *
 * 能力清单:
 *   - generate_dna       : DNA追溯码生成
 *   - tricolor_audit     : 三色审计
 *   - run_cnsh           : CNSH脚本执行
 *   - tricolor_gate      : 审计审批门（自动拦截🔴）
 *   - historian          : 史官全链路记录
 *   - persona_router     : 24人格路由
 */

import { LongHunEngine } from './longhun-engine'
import { dnaTool } from './tools/dna-tool'
import { tricolorTool } from './tools/tricolor-tool'
import { cnshExecutor } from './tools/cnsh-executor'
import { tricolorGate } from './hooks/tricolor-gate'
import { historianPlugin } from './events/historian'
import { personaRouter } from './agents/persona-router'

export const name = '@longhun/cnsh-suite'
export const inject = ['tools', 'session', 'agents']

export function apply(ctx: any) {
  console.log('🐉 龍魂 CNSH 套件加载中...')

  // 1. 初始化龍魂引擎（本地实例）
  const engine = new LongHunEngine()
  console.log('✅ 龍魂引擎初始化完成')

  // 2. 注册工具
  ctx.tools.register(dnaTool(engine))
  ctx.tools.register(tricolorTool(engine))
  ctx.tools.register(cnshExecutor(engine))
  console.log('✅ 已注册 3 个 CNSH 工具')

  // 3. 注册审计审批门
  tricolorGate(engine)(ctx)
  console.log('✅ 三色审计审批门已激活')

  // 4. 注册史官事件监听
  historianPlugin(engine)(ctx)
  console.log('✅ 史官事件监听已启动')

  // 5. 注册人格路由
  personaRouter(engine)(ctx)
  console.log('✅ 人格路由已注册')

  // 6. 导出引擎供其他插件使用
  ctx.longhun = engine

  console.log('🐉 CNSH 套件加载完成 — 龍魂主权底座已焊入 Harness')
  console.log('   DNA: #龍芯⚡️丙午·丙申·庚申·亥时-CNSH-SUITE-UID9622')
  console.log('   确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z')
}

// 导出类型
export { LongHunEngine } from './longhun-engine'
