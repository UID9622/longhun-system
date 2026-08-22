# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂浏览器扩展

本目录收录龍魂系统的浏览器扩展（Chrome / Edge / 基于 Chromium）。

| 扩展 | 目录 | 状态 | 说明 |
|------|------|------|------|
| 龍魂宝宝 · LongHunWidget | `LongHunWidget/` | ✅ 已修复 | MV3 侧边栏 · DNA / 记忆 / 审计 / 五行 / MCP 桥接 |
| CNSH · 龍魂语法引擎 | `cnsh-chrome-plugin/` | ✅ 已纳入 | MV3 快速入库 · Notion Inbox / DNA / 人心算法 |

---

## LongHunWidget 修复记录（2026-06-16）

1. **manifest.json**
   - 新增 `"alarms"`、`"notifications"` 权限（background.js 使用）
   - 移除 `action.default_popup`，让图标点击正确打开 sidePanel
2. **sidepanel.html**
   - 修复 MCP 面板被错误放在 `.content` 外部的结构问题
   - 标签栏改为 6 列，适配 6 个标签页
3. **sidepanel.js**
   - 补上 `hmacSHA256()` 实现，修复 MCP L0 签到时的未定义错误

## CNSH 插件纳入（2026-06-16）

- 从 `~/Desktop/cnsh-chrome-plugin` 复制到本目录
- 已检查无硬编码密钥，Notion Token 与 DB ID 均透过 options 页面由使用者配置

---

**DNA**:#龍芯⚡️丙午·甲午·辛酉·甲午·䷨损-EXTENSIONS-v1.1
