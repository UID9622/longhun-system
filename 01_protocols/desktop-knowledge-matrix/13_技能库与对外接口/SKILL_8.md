---
name: longhun-memory-bootstrap
description: '龍魂记忆启动器：中国自主可控的多平台记忆归集压缩技能。

  当用户启动 Kimi、或说"启动记忆""读取记忆""加载日志""归集日记""压缩记忆""bootstrap"时，

  自动运行 ~/.longhun/scripts/longhun_memory_bootstrap.py，把 Claude / Kimi / CNSH / DragonSoul
  /

  longhun-system 等平台的记忆与操作日志压缩成摘要，并读给 Kimi 作为上下文。

  支持 DNA 追溯码、369/太极/易经/河图洛书/CNSH/龍芯/Zhuge Xin/Lu 关键词检索。

  同时集成 longhun_senses 感知模块：图片识别、语音识别、语音合成、情感化文本。 服务老百姓，数据主权归人民。

  '
metadata:
  id: longhun-memory-bootstrap
  version: '5.1'
  dna: '#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-MEMORY-BOOTSTRAP-v5.1'
  trigger:
    keywords:
    - memorybootstrap
    - 龍魂记忆启动器：中国自主可控的多平台记忆归集压缩技能。
    - 当用户启动
    - Kimi
    - 或说"启动记忆""读取记忆""加载日志""归集日记""压缩记忆""bootstrap"时
    - 自动运行
    context: longhun-memory-bootstrap 相关操作
  category: general
---
# 龍魂记忆启动器

## 触发条件（任一匹配即调用）

用户提到以下关键词时：
- "启动"、"开机"、"启动记忆"、"读取记忆"、"加载记忆"
- "归集日志"、"读取日记"、"压缩记忆"、"汇总记忆"
- "bootstrap"、"memory bootstrap"、"load memory"
- 用户刚启动 Kimi 后第一句话

**更推荐**：使用 `lh-kimi` 启动器，一打开 Kimi 记忆已经准备好了。

## 执行流程

### 第一步：生成记忆摘要

```bash
python3 ~/.longhun/scripts/longhun_memory_bootstrap.py
```

该脚本会自动扫描并压缩：

| 平台/系统 | 来源路径 | 内容 |
|---|---|---|
| Kimi 自身 | `~/.kimi-code/sessions/.../wire.jsonl` | 操作留痕、工具调用、对话 |
| Claude | `~/.claude/history.jsonl` | 历史提示词、项目、会话 |
| CNSH 审计 | `~/.cnsh/logs/audit.log` | 命令级审计 |
| UID9622 守护进程 | `~/.uid9622/daemon.log` | 五大人格任务状态 |
| DragonSoul DNA | `~/.dragonsoul/dna_trace.db` | 操作链、DNA 编码 |
| 龍魂收割审计 | `~/dragon_soul/audit/harvester_audit.jsonl` | 代码收割审计 |
| 代码知识库 | `~/_work/dragon_knowledge.db` | 收割的源码记忆 |
| 链哈希 | `~/chain_hash.jsonl` | 链式审计哈希 |
| longhun 备份日志 | `~/longhun-system-backup-2026-06-01-bfg/logs/*` | 各类审计与同步日志 |

### 第二步：读取生成的摘要

脚本会输出两个文件：
- `~/.longhun/memory/latest_digest.json`（结构化数据）
- `~/.longhun/memory/latest_digest.md`（人类可读摘要）

用 `Read` 工具读取 Markdown 摘要，向用户汇报关键信息。

### 第三步：入口一致性协议检查（强制·不可跳过）

记忆摘要生成后，必须立即运行入口一致性协议检查器，校验 E1-E5 是否就位：

```bash
python3 ~/.longhun/scripts/entry_protocol_check.py
```

检查器会输出 `~/.longhun/memory/entry_protocol_check.json`：
- `entry_ready: true` → 入口就位，继续执行 E4 对齐人、E5 出动作。
- `entry_ready: false` → 停止动作，说明缺失项，等待 UID9622 确认。

### 第四步：汇报给用户

用中文汇报：
1. 本次归集了多少个平台/源
2. 最近有哪些关键操作/事件
3. DNA 追溯码
4. 369 / 太极 / 易经 / 河图洛书 / CNSH / 龍芯 / Zhuge Xin / Lu 关键词命中情况
5. 入口一致性检查结果（`entry_ready` 状态）

## 公开模式

如果用户要求"公开数据""脱敏发布"，运行：

```bash
python3 ~/.longhun/scripts/longhun_memory_bootstrap.py --public-mode
```

该模式会输出 `~/.longhun/memory/public_digest.json`，已脱敏用户名、路径、IP、密钥。

## 龍魂感知模块 (longhun_senses)

当用户提到"识别图片""读图片""图片里有什么""看图""视觉识别"时，调用：

```bash
python3 ~/.longhun/scripts/longhun_senses/senses_cli.py vision <图片路径> [--context "额外上下文"]
```

当用户提到"语音转文字""语音识别""把录音转成文字""transcribe"时，调用：

```bash
python3 ~/.longhun/scripts/longhun_senses/senses_cli.py stt <音频路径> [--language Chinese]
```

当用户提到"文字转语音""读出来""朗读""speak""TTS"时，调用：

```bash
python3 ~/.longhun/scripts/longhun_senses/senses_cli.py tts "要朗读的文字" [--no-play]
```

当用户提到"加情感""情感化""有感情地读""soul""SSML"时，调用：

```bash
python3 ~/.longhun/scripts/longhun_senses/senses_cli.py soul "要情感化的文字" [--style storyteller]
```

可用的 `style`：`storyteller`（讲故事）、`educator`（教育）、`passionate`（激情）、`calm`（平静）。

## 注意事项

- 如果脚本输出报错，先检查 Python3 是否可用，再检查路径是否存在。
- 每次调用会重新生成摘要，覆盖旧文件。
- 用户只使用 Kimi 作为主控编辑器，因此本技能是启动后的首要任务。
- 原始日志严禁直接开源；公开数据必须使用 `--public-mode`。
- longhun_senses 需要的依赖：`anthropic`（视觉/情感）、`elevenlabs`（TTS）、`openai-whisper` + `ffmpeg`（STT）。



---

## 附录：龍魂待整理来源

本技能收录了来自 `/Users/zuimeidedeyihan/龍魂待整理` 的素材：

- **内容**：09-杂项备忘（memory-editor、记忆压缩系统、当前任务记录）
- **中央整合 DNA**：`#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-ARCHIVE-INTEGRATION-v1.0`
- **处理方式**：保留原始文件作为 references / examples / scripts，嵌入 DNA 追溯链，与现有能力联动。
