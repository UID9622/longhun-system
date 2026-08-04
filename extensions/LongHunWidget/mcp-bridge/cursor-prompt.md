# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--#龍芯⚡️2026-06-21-DOC-CURSOR-PROMPT-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# Cursor 一键提示词 · 龍魂 MCP 认证桥接 v0.1

## 任务

帮我在本机集成 Chrome DevTools MCP Server v0.21.0 + 龍魂主控台认证。

## 文件位置

这些文件在 `~/Desktop/LongHunWidget/mcp-bridge/` 里：
- `longhun-mcp-auth.json` — 认证配置
- `longhun-mcp-wrapper.js` — 拦截层
- `install.sh` — 一键安装脚本

## 执行步骤

1. 打开终端，cd 到你要装的项目目录
2. 把上面3个文件拷进去（或 symlink）
3. 跑 `bash install.sh`
4. 在 `.env` 文件里加：`LONGHUN_GPG=A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
5. 创建 `test-gate.js`：

```js
const { LonghunMcpGate } = require('./longhun-mcp-wrapper')

async function test() {
  // 模拟一个 MCP client（实际使用时连真实的 Chrome DevTools MCP）
  const mockClient = {
    callTool: async ({ name, arguments: args }) => {
      console.log(`  [MCP] ${name} 被调用`, args)
      return { ok: true }
    }
  }

  const gate = new LonghunMcpGate(mockClient)

  // 必须先签到
  await gate.signL0('test-agent-001')
  console.log('✅ L0 签到成功')

  // 测试绿灯工具
  try {
    await gate.callTool('read_page', { url: 'https://example.com' })
    console.log('✅ read_page 通过（绿灯）')
  } catch (e) {
    console.log('❌', e.message)
  }

  // 测试红灯熔断
  try {
    await gate.callTool('evaluate_script', { script: 'alert(1)' })
    console.log('❌ 熔断没触发！')
  } catch (e) {
    console.log('✅ 红灯熔断生效：', e.message)
  }

  console.log('\n📊 审计统计:', gate.getStats())
}

test().catch(console.error)
```

6. 跑 `node test-gate.js`
7. 把终端输出的 `longhun-audit.log` 和 `shame-wall.log` 内容贴回来

## 预期结果

- `read_page` → 🟢 通过
- `evaluate_script` → 🔴 熔断
- `longhun-audit.log` 有绿记录
- `shame-wall.log` 有红记录
