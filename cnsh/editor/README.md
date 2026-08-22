# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CNSH Editor · 龍魂中文编辑器统一模块

**生成时间**: 2026-06-22 13:17:01

**DNA**:`#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-CNSH-EDITOR-v1.0`

## 模块定位

`cnsh-editor` 是龍魂体系中所有编辑器能力的统一入口，把原先分散在 `cnsh-terminal`、`cnsh-core`、`web`、`docs`、`Downloads` 导入区的编辑器相关文件整合为一处，减少重复、便于维护。

## 目录结构

| 目录 | 内容 |
|---|---|
| `core/` | 编辑器引擎 (`cnsh_editor_engine_v2.0.py`) |
| `ui/` | 终端 UI (`editor_ui.py`) |
| `docs/` | 中文编辑关键字登记册、使用指南、完成报告、PDF 手册 |
| `web/` | Web 端编辑器页面 (`CNSH编辑器.html`, `memory-editor.html`) |
| `scripts/` | 构建脚本 (`build-chinese-editor.sh`) |
| `platforms/harmonyos/` | 鸿蒙 ArkTS 编辑器页面 (`CNSHEditor.ets`) |
| `platforms/ios/` | iOS 日记本编辑器 (`DiaryEditor.swift`, `ContentView.swift`) |
| `legacy/` | 历史版本/替代实现 (`cnsh_terminal_v5_editor_ui.py`) |

## 使用方式

- Python 引擎：`from cnsh_editor.core.cnsh_editor_engine_v2_0 import ...`
- 终端 UI：直接运行或 import `cnsh_editor/ui/editor_ui.py`
- 鸿蒙：将 `platforms/harmonyos/CNSHEditor.ets` 复制到 ArkTS 项目 pages 目录
- iOS：将 `platforms/ios/*.swift` 加入 Xcode 项目

## 来源与压缩

本模块通过 `build_cnsh_editor_module.py` 自动构建：
- 项目核心文件复制到本模块
- `cnsh-terminal/downloads-imports/` 中大量重复的 `CNSHEditor.ets`、`cnsh_editor_engine_v2.0.py`、`editor_ui.py` 等副本被迁移或删除
- 详细清单见 `03_KNOWLEDGE_GRAPH/cnsh_editor_build_report.md`

---

**自动生成于**: 2026-06-22T13:17:01.835167
