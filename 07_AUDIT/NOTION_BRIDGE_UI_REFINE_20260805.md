# 🐲 龍魂 · Notion 对话桥 Web 面板精修报告 v2.2.1

> DNA: #龍芯⚡️丙午·癸未·甲申·庚午·䷙大畜-NOTION-BRIDGE-UI-v2.2.1-UID9622
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 执行时间: 2026-08-05
> 范围: web/notion_bridge.html 对话墙视觉精修 + 服务重启
> 三色: 🟢 4 项完成 · 🟡 0 项 · 🔴 0 项

---

## 1. 修复内容

### 1.1 对话墙从「Notion 块」改造为「聊天气泡」

**问题**: 消息显示为带拖拽手柄（⋮⋮）的文档块，不像对话，视觉上杂乱。

**修复**:
- 隐藏默认拖拽手柄，仅在悬停时显示小圆点提示
- 用户消息：右上角圆角气泡，右对齐，最大宽度 82%
- AI 消息：左上角圆角气泡，左对齐，带金色/朱砂/玉绿左边框（对应三色审计状态）
- 增加消息间距，减少视觉拥挤

### 1.2 AI 模型信息徽章精简

**修复前**: provider / model / mode / 审计状态全部挤在一行，model 名称过长时换行混乱。

**修复后**:
- provider 与 mode 使用圆角胶囊标签
- model 名称截断显示，hover 显示完整
- fallback_chain 单独小标签
- 三色审计状态右对齐显示

### 1.3 Markdown 渲染增强

**问题**: `**粗体**`、列表等 Markdown 原样显示或渲染错误。

**修复**: `markdownToHtml()` 新增支持：
- 粗体 `**text**` / `__text__`
- 斜体 `*text*` / `_text_`
- 删除线 `~~text~~`
- 链接 `[text](url)`
- 列表：连续 `- ` 或 `1. ` 行合并为单个 `<ul>` / `<ol>`
- 代码块占位还原，避免内部被二次转义

### 1.4 多模型协作显示验证

五行议事会模式下，各委员（土/水/金/木/火）及其 provider（local / deepseek / kimi）以徽章条展示，合成结果以气泡形式输出，列表渲染正确。

---

## 2. 服务重启

| 环境 | 命令 | 状态 |
|:---|:---|:---:|
| Mac 本地 | `launchctl unload/load com.longhun.notion-bridge.plist` | 🟢 8779 已重启 |
| 鲲鹏公网 | `systemctl restart longhun-notion-bridge.service` | 🟢 服务运行中 |

验证地址：
- 本地: `http://127.0.0.1:8779/`
- 公网: `https://uid9622.cn/notion-bridge/`

---

## 3. 文件变更

- `web/notion_bridge.html`（已重新 GPG 签名）
- `web/notion_bridge.html.asc`

已同步到鲲鹏 `/opt/longhun-system/web/` 与 `/root/longhun-system/web/`。

---

## 4. 签名

```
DNA: #龍芯⚡️丙午·癸未·甲申·庚午·䷙大畜-NOTION-BRIDGE-UI-v2.2.1-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

> 🐉 对话墙清爽了，多模型协作才看得清。
