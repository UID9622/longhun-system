# 龍魂系统·依赖清单总览 / Longhun System · Dependency Overview

> DNA: #龍芯⚡️2026-09-05-依赖清单-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 代码: MulanPSL v2
> 文档版本: v5.2.0
> 三色: 🟢 依赖与平台矩阵 2026-09-05 实测 · 见 12_DOCS/龍魂能力归集-2026-09-05.md

---

## [中文] 依赖清单

### 一、必需依赖（所有平台·本机实测 2026-09-05）

| 依赖 | 最低版本 | 实测版本 | 用途 | 验证命令 |
|---|---|---|---|---|
| Python | 3.8+ | 3.12.13 | 核心运行时（lh 主控 v1.3） | `python3 --version` |
| Git | 2.30+ | 2.54.0 | 版本控制·DNA 追溯 | `git --version` |
| GPG | 2.2+ | 2.4.9 | 签名·身份验证（KEY `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`） | `gpg --version` |
| curl | 7.68+ | 8.7.1 | HTTP/API 调用 | `curl --version` |
| jq | 1.6+ | 1.8.1 | JSON 处理 | `jq --version` |
| git-lfs | 3.0+ | 3.7.1 | 大文件存储 | `git lfs version` |
| pyyaml | 6.0+ | ✅ | 配置解析 | `python3 -c "import yaml"` |
| pytest | 7.0+ | 9.1.1 | 测试框架 | `pytest --version` |

### 二、可选依赖（本机实测已装 ✅）

| 依赖 | 实测 | 功能模块 | 说明 |
|---|---|---|---|
| Ollama | ✅ | `lh model` 本地模型·离线推理 | `ollama run <model>` |
| ffmpeg | ✅ | 视频/音频处理 | 4.4+ |
| whisper | ✅ | 语音识别（sense） | `pip install openai-whisper` |
| tesseract | 按需 | OCR 文字识别 | 无则跳过 OCR 分支 |
| docker/nginx/systemd | 按需 | 容器/网关/守护 | 部署场景 |

### 三、离线模式（🟢 已焊死·2026-09-05 确认）

- 核心 100% 离线：lh 命令 · 三色审计 · 账本(ledger) · 日历记忆(calmem) · 计费(billing) · 本地模型 —— 零外部依赖
- 一键切换：`export LONGHUN_OFFLINE_MODE=1` → `python3 08_BIN/lh.py health --json`
- 唯一需联网项：Notion MCP（降级=本地 Markdown 存储，联网后 `lh workspace-sync` 补齐）

### 四、平台矩阵

| 平台 | 支持 | 说明 |
|---|---|---|
| macOS | 🟢 原生推荐 | Homebrew / Xcode CLT |
| Linux (Ubuntu/Debian) | 🟢 | build-essential + python3-dev |
| 鲲鹏 ARM64 (欧拉OS/openEuler) | 🟢 零适配 | 纯 Python 天然跨架构 · `uname -m` → `aarch64` · `dnf install python39` |
| 鸿蒙 HarmonyOS NEXT | 🟡 API 层 | lh CLI 不支持原生，走 uid9622.cn API |
| Windows (WSL2) | 🟢 | `wsl --install -d Ubuntu-22.04` |

---

## [English] Dependency Overview

### 1. Required (all platforms, verified 2026-09-05)
Python ≥3.8 (3.12.13 tested) · Git ≥2.30 (2.54.0) · GPG ≥2.2 (2.4.9) · curl 8.7.1 · jq 1.8.1 · git-lfs 3.7.1 · pyyaml ✅ · pytest 9.1.1

### 2. Optional (installed on this Mac)
Ollama (local model) · ffmpeg · whisper · tesseract (on demand)

### 3. Offline Mode (zero external calls)
`export LONGHUN_OFFLINE_MODE=1` → all `lh` core commands, ledger, calendar-memory, billing, tri-color audit work 100% offline. Only Notion MCP requires internet (falls back to local Markdown).

### 4. Platforms
- macOS native · Linux · Kunpeng/ARM64 (EulerOS/openEuler, `aarch64`, pure-Python zero adaptation) · HarmonyOS via API only · Windows via WSL2

---
🐉 2026-09-05 · 丙午年·壬申月·庚戌日 · UID9622 · 🟢
