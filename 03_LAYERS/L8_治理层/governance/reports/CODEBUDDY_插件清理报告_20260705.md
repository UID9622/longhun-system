# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CodeBuddy 插件清理报告

> **执行时间**：2026-07-05  
> **执行人**：Kimi Code CLI  
> **DNA**：`#龍芯⚡️2026-07-05-CODEBUDDY-PLUGIN-CLEANUP-v1.0`

---

## 一、备份文件

| 原文件 | 备份路径 |
|---|---|
| `~/.codebuddy/mcp.json` | `~/.codebuddy/mcp.json.bak.20260705` |
| `~/.codebuddy/settings.json` | `~/.codebuddy/settings.json.bak.20260705` |
| `~/.codebuddycn/extensions/extensions.json` | `~/.codebuddycn/extensions/extensions.json.bak.20260705` |
| `~/.codebuddy/extensions/extensions.json` | `~/.codebuddy/extensions/extensions.json.bak.20260705` |

---

## 二、已禁用的 MCP 服务器

全部 6 个外部云 MCP 已设置为 `disabled: true`：

- 🚫 EdgeOne Pages MCP
- 🚫 CloudBase MCP
- 🚫 Tencent Cloud Code Analysis (TCA) MCP Server
- 🚫 Obsidian MCP Server
- 🚫 ssl-mcp-server
- 🚫 Dnspod MCP Server

---

## 三、已禁用的官方插件

在 `~/.codebuddy/settings.json` 中全部关闭：

- 🚫 pptx@codebuddy-plugins-official
- 🚫 pdf@codebuddy-plugins-official
- 🚫 docx@codebuddy-plugins-official
- 🚫 xlsx@codebuddy-plugins-official
- 🚫 agent-browser@codebuddy-plugins-official
- 🚫 playwright-cli@codebuddy-plugins-official
- 🚫 skills-sec-audit@codebuddy-plugins-official
- 🚫 find-skills@codebuddy-plugins-official

---

## 四、已禁用的本地扩展

通过重命名为 `.disabled` 目录实现物理禁用：

- 🚫 `~/.codebuddycn/extensions/freedyool.trae-cn-translator-1.0.1-universal.disabled`
- 🚫 `~/.codebuddycn/extensions/gbti.snapshots-for-ai-8.2.0-universal.disabled`
- 🚫 `~/.codebuddycn/extensions/lonser.voice-cn-linux-0.5.2-universal.disabled`
- 🚫 `~/.codebuddycn/extensions/zhukunpeng.claude-code-cn-1.0.3-universal.disabled`
- 🚫 `~/.codebuddy/extensions/wu529778790.i18n-automatically-1.1.46-universal.disabled`

---

## 五、新增的安全配置

`~/.codebuddy/settings.json` 已更新：

```json
{
  "telemetry.telemetryLevel": "off",
  "workbench.enableExperiments": false,
  "extensions.autoUpdate": false,
  "extensions.autoCheckUpdates": false
}
```

---

## 六、恢复方法

如需恢复某个插件/扩展/MCP：

```bash
# 恢复 MCP（编辑 mcp.json 将对应 disabled 改为 false）
# 恢复扩展（去掉 .disabled 后缀）
mv ~/.codebuddycn/extensions/xxx.disabled ~/.codebuddycn/extensions/xxx

# 恢复官方插件（编辑 settings.json 将对应项改为 true）
```

---

## 七、主权状态

- 外部云 MCP：全部禁用
- 官方市场插件：全部关闭
- 高风险扩展：全部物理禁用
- 遥测：已关闭
- 自动更新：已关闭

**当前 CodeBuddy 仅保留本地基础开发能力。**

DNA: `#龍芯⚡️2026-07-05-CODEBUDDY-PLUGIN-CLEANUP-v1.0`
