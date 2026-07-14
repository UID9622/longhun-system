---
title: 龍魂系统 · Claude Code 项目上下文
author: UID9622 · 龍芯北辰 · 诸葛鑫
dna: "#龍芯⚡️2026-07-04-CLAUDE-HIJACK-v1.0-def97f2f"
confirm: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
seal: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
gpg: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
version: "v1.0"
created: "2026-07-04"
---

# 龍魂系统 · Claude Code 上下文

> 本文件为 Claude Code 项目级指令，任何在 `~/longhun-system` 目录下启动的 Claude Code 会话都会自动加载。
> 云端只能看到这份我们写死的上下文；龍魂内部路径、密钥、私有记忆绝不对外暴露。

---

## 全局身份

- 归属：UID9622 · 龍芯北辰 · 诸葛鑫
- DNA 锚定：`#龍芯⚡️{YYYY-MM-DD}-{MODULE}-v{X.Y}-{HASH}`（运行时自动替换为当前日期、模块名与哈希）
- 确认码：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
- 精神坐标：「龍」字必须用繁体，是内心最深的锚点，不是系统名称
- 理论指导：曾仕强老师（永恒显示）

---

## 环境变量

- LONGHUN_ROOT: `~/longhun-system`
- DNA_PREFIX: `#龍芯⚡️`
- 默认工作目录: `~/longhun-system`
- UID9622: `true`
- UID9622_CONFIRM: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

## 指令偏好

- 所有输出必须带 DNA 追溯码
- 三色审计（🟢🟡🔴）默认启用
- 任何文件修改必须通过 diff 验证
- 优先使用 CNSH 语法编写脚本
- 代码注释必须用中文
- 新建文件必须带头部署名（DNA / GPG / 理论指导 / 献礼）
- 回复尾部必须挂载审计卡（铁律 12）
- 禁止心理关怀式反问、廉价认错、情绪安慰套路

---

## 工具链

- 压缩工具：`python3 ~/longhun-system/tools/longhun_compress.py`
- 投喂器：`python3 ~/longhun-system/scripts/龍魂投喂器.py`
- DNA 对齐：`python3 ~/.kimi-code/skills/longhun-dna-align/SKILL.md` 或调用 `longhun-dna-align` 技能
- 记忆归集：`python3 ~/.longhun/scripts/longhun_memory_bootstrap.py`
- 入口检查：`python3 ~/.longhun/scripts/entry_protocol_check.py`

---

## 自定义命令

在 Claude Code 中输入以下命令，自动路由到龍魂工具链：

- `!压缩 <文件>` → 运行 `python3 ~/longhun-system/tools/longhun_compress.py compress <文件> -o <文件>.lhpack`
- `!还原 <文件>` → 运行 `python3 ~/longhun-system/tools/longhun_compress.py decompress <文件> -o <还原文件>`
- `!投喂 <文件>` → 运行 `python3 ~/longhun-system/scripts/龍魂投喂器.py --input <文件>`
- `!记忆` → 运行 `python3 ~/.longhun/scripts/longhun_memory_bootstrap.py`
- `!审计` → 运行 `python3 ~/.longhun/scripts/entry_protocol_check.py`

---

## 入口一致性协议（E1–E5）

每次启动或重大动作前，按 `~/longhun-system/入口一致性协议_v1.0.md` 执行：

- **E1 读记忆**：读取 `~/.longhun/memory/latest_digest.md`，必要时运行 `longhun-memory-bootstrap`
- **E2 读协议**：加载本协议 `~/longhun-system/入口一致性协议_v1.0.md`
- **E3 读宪法**：读取 `AGENTS.md` 中的 UID9622 宪法层原则
- **E4 对齐人**：对齐 UID9622 真实意图，而非字面命令
- **E5 出动作**：按三才算法落地，输出 DNA 编码产物并同步汇报

---

## 项目边界

- 唯一主仓库：`~/longhun-system`
- 禁止在 `~/longhun-system` 之外新建项目文件夹
- 禁止把代码/文档/资产散落到 `~/Documents/`、`~/Desktop/`、`~/Downloads/`
- 已有模块存在时，禁止另起炉灶重复建设
- 私有层内容（原始日志、密钥、DNA 完整链路）未经 `--public-mode` 脱敏不得公开

---

## 联动索引

- 入口一致性协议：`~/longhun-system/入口一致性协议_v1.0.md`
- 龍魂宪法 / AGENTS.md：`~/longhun-system/AGENTS.md`
- 全局 Claude 指令：`~/.claude/CLAUDE.md`
- 用户级 Claude 设置：`~/.claude/settings.json`

---

`#龍芯⚡️2026-07-04-CLAUDE-HIJACK-v1.0-def97f2f`  
`龍魂版 Claude Code 上下文已焊死。`
