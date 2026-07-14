# 更新日志

## v2.1.0 (2026-07-11) · 内联引擎·零依赖可用

### 🚀 核心突破
- **Auditor.scan()** — 三色安全审计已对接内联引擎，零外部依赖即可运行
  - 14 红色警报词（一票否决）· 15 黄色警报词 · 10 行话/黑话检测
  - 支持 `source="external"`(全量) / `source="self"`(自研·黄警豁免)
  - `engine="native"` 模式可对接 `bin/lh_anti_tamper.py` 完整引擎
- **PersonaRouter.route()** — 内联路由表 30+ 意图域 · 10 人格 · 零依赖可用
  - 支持自动匹配 + `persona` 强制指定
  - 兜底：未匹配 → P02 龍芯
- **CNSHParser.parse()** — 内联语义域映射 40+ 意图域 · 零依赖可用

### 🔧 改进
- 所有 Preview 方法从 `NotImplementedError` 升级为内联引擎可运行
- `__init__` 公开导出不变，`AuditReport` 新增 `dna`/`red_count`/`yellow_count`/`jargon_count`/`plain_language_ok` 字段
- 移除 `FutureWarning` — 内联引擎已就绪，不再警告

### 🛡️ 安全
- Auditor 内联规则从 `bin/lh_anti_tamper.py` 同步
- 红色警报词一票否决，无论属主
- 自研文档模式黄色警报仅记录不判定

---

## v2.0.0 (2026-07-10) · Gitee 首发

### 全模态发布
- 🎙️ **真声克隆** — UID9622 本人声音 · XTTS-v2 微调 · 31分钟训练数据
- 🔐 **声纹DNA** — 声纹哈希链 · 身份固化 · Fernet加密 · 321备份
- 👁️ **视觉识别** — 文化符号识别 · 图像分析 · 本地视觉桥
- 🧠 **人格体系** — 20+ 人格 · 语义自动路由 · 独立音色/形象
- 🎨 **文化资产** — 伏羲/老子/禅师/黄帝/曾仕强 等形象 SVG

### 语言/协议
- CNSH 语言规范 v2.0 公开发布
- 中英双轨语义路由 · 50+ 意图域

### SDK
- Python SDK 全模态：PersonaRouter / CNSHParser / DNA / Auditor
- 语音模块：VoiceSynthesizer / PersonaVoice / VoiceDNA
- 视觉模块：VisionAnalyzer / VisionBridge
- 5 个可运行示例

### 基础设施
- 本地 AI 中继桥 v1.0（零外部依赖）
- API 接入指南完整版
- REST API 端点文档

---

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)
