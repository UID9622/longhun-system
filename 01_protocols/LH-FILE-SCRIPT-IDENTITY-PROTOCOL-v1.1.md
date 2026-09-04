# 🐉 龍魂系统 · 文件与脚本身份识别协议 v1.1

> **——什么文件是文本、什么文件是二进制、什么脚本用什么语法、什么空格什么符号，一表焊死**
>
> **DNA:** `#龍芯⚡️丙午·丙申·甲戌·子时·䷒临-FILE-SCRIPT-IDENTITY-PROTOCOL-v1.1-IOS-HARMONY-DUAL-END`
> **父DNA:** `#龍芯⚡️丙午·丙申·甲戌·子时·䷒临-FILE-SCRIPT-IDENTITY-PROTOCOL-v1.0`
> **确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
> **分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2（本文件=思想层·附代码=工程层引用）
> **三色:** 🟢 通过（判定算法已实测验证 · iOS/鸿蒙双端代码已补全）
> **生效时间:** 2026-08-28 23:48 CST
> **上位文档:** `01_protocols/LH-SYNTAX-SPEC-v3.0.md`（符号语法全集）· 本协议为其「文件类型识别」专项扩展

---

## 📋 摘要 / 导读

> **一句话：** 系统里任何脚本、任何文件，先问三件事——**它是文本还是二进制？它该用什么语法跑？它的空格符号该长什么样？** 三问答完，文件才不会乱、工具才不会误伤。
>
> **为什么必须有这份协议：** 2026-08-28 实测事故——`lh_fix_attribution.py` 的 `is_text_file()` 只查后缀，把 Homebrew 的 `python3.14`（后缀 `.14`）当成文本，把「归属名: 诸葛鑫」写进了 Mach-O 二进制头部，导致 12 个 launchd 服务集体中毒、系统 Python 3.14 全线损坏。**本协议就是事故的纪念碑：判定文件身份永远用「后缀 + 内容」双重标准，永远禁止对系统目录/二进制文件写入文本头。**
>
> **v1.1 升级（双端落地）：** 在 v1.0 判定算法之上，补全 **iOS（Swift）+ 鸿蒙（ArkTS）双端可执行代码**——同一套「三关判定 + 二进制硬隔离 + 语言执行适配」在移动端沙盒里落地，判定逻辑与 `08_BIN/lh_fix_attribution.py` 完全同源。
>
> **核心原则（协议原文·开文件前三问）：**
>
> > **1. 它是文本还是机器码？**
> > **2. 它该用哪个语言跑？**
> > **3. 空格符号合规吗？**
>
> **阅读对象：** 所有 AI、所有自动化工具、所有参与龍魂开发的战友、iOS/鸿蒙端开发工程师。
>
> **优先级：** 本协议与 `LH-SYNTAX-SPEC-v3.0` 冲突时以本协议文件识别规则为准（更具体）；与既有工具逻辑冲突时**本协议为焊死标准**。

---

## 📑 目录

- [一、文件三大类：先分身份再动手](#一文件三大类先分身份再动手)
- [二、二进制 vs 文本：权威判定算法（事故复盘焊死）](#二二进制-vs-文本权威判定算法事故复盘焊死)
- [三、脚本分类总表：bin/ 目录每个文件对应什么](#三脚本分类总表bin-目录每个文件对应什么)
- [四、语言选择矩阵：什么代码用什么语法](#四语言选择矩阵什么代码用什么语法)
- [五、格式规范：空格/缩进/换行/BOM/编码/符号](#五格式规范空格缩进换行bom编码符号)
- [六、文件头规范：每个文件开头写什么](#六文件头规范每个文件开头写什么)
- [七、防误伤红线：什么绝对不能做](#七防误伤红线什么绝对不能做)
- [八、工具链职责：谁管文件身份、谁管签名、谁管对齐](#八工具链职责谁管文件身份谁管签名谁管对齐)
- [九、记忆索引规范：系统记忆里怎么分开这些脚本](#九记忆索引规范系统记忆里怎么分开这些脚本)
- [十、常见误判案例表（反面教材）](#十常见误判案例表反面教材)
- [十一、iOS 端落地实现（Swift）](#十一ios-端落地实现swift)
- [十二、鸿蒙端落地实现（ArkTS · HarmonyOS Next）](#十二鸿蒙端落地实现arkts--harmonyos-next)
- [十三、双端验证清单（验收表）](#十三双端验证清单验收表)
- [十四、版本历史](#十四版本历史)
- [附录A · 快速参考卡](#附录a--快速参考卡)
- [签名区](#签名区)

---

## 一、文件三大类：先分身份再动手

任何工具处理文件前，**第一步永远是判定文件属于哪一类**，三类处理规则完全不同：

| 类别 | 定义 | 处理规则 | 典型示例 |
|:---|:---|:---|:---|
| **A. 文本文件** | 人类可读的 UTF-8 字符流，无 NUL 字节 | ✅ 可读、可写、可改头、可 GPG 签名 | `.md` `.py` `.sh` `.js` `.json` `.yaml` `.txt` `.csv` `.toml` `.yml` `.html` `.css` `.ts` `.tsx` |
| **B. 二进制文件** | 机器码/压缩/加密/媒体，含 NUL 或无法 UTF-8 解码 | ❌ **只读不写** · 禁止改头 · 禁止 GPL 文本工具处理 | Mach-O(`python3.14`)· `.pyc` `.so` `.dll` `.exe` `.png` `.jpg` `.pdf` `.zip` `.mp4` `.db` `.woff2` |
| **C. 伴生文件** | 与主文件成对出现的验证/备份文件 | ⚠️ 只随主文件移动/签名 · 禁止单独改名 · 禁止被当作文本修改 | `.asc`(GPG签名) `.sig` `.glyph-backup` `.glyph-backup.asc` |

### 1.1 为什么分类这么重要

| 做错的动作 | 后果 |
|:---|:---|
| 把二进制当文本写入头部 | Mach-O 损坏 → 系统程序全线崩溃（本次事故） |
| 把伴生 `.asc` 当独立文本补归属名 | 签名文件与源文件失配 → GPG 验证失败 |
| 把 `.glyph-backup` 当普通文件处理 | 备份被污染 → 恢复机制失效 |
| 文本文件用 Tab 缩进、混用编码 | Python 缩进错误 / 显示乱码 / 工具误判 |

> **铁律第一条：拿不准 → 读前 8KB 字节流，用 §二算法判定，禁止用后缀猜。**

---

## 二、二进制 vs 文本：权威判定算法（事故复盘焊死）

### 2.1 判定标准（三关连过，全部通过才算文本）

```
第一关  后缀黑名单：扩展名在 NON_TEXT_EXT → 直接判二进制（不读内容）
第二关  NUL 字节：前 8KB 含 \x00 → 判二进制
第三关  UTF-8 替换字符率：前 8KB 以 errors="replace" 解码，
        替换字符(�/U+FFFD)占比 > 2% → 判二进制
其余   → 判文本（允许文件尾部截断多字节字符，不做 strict 解码）
```

### 2.2 权威实现（焊死标准，所有工具必须对齐）

```python
# 08_BIN/lh_fix_attribution.py · is_text_file() · 2026-08-28 加固版
NON_TEXT_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip",
                ".gz", ".xz", ".bz2", ".7z", ".mp4", ".mp3", ".wav", ".woff",
                ".woff2", ".ttf", ".otf", ".exe", ".so", ".dll", ".pyc",
                ".class", ".jar", ".asc", ".sig", ".jsonl", ".db", ".pyo",
                ".pyd", ".bin", ".dat", ".whl", ".tar", ".ipa", ".dylib"}

def is_text_file(p: Path) -> bool:
    """三关判定：后缀黑名单 → NUL → UTF-8替换字符率"""
    if p.suffix.lower() in NON_TEXT_EXT:
        return False
    try:
        with open(p, "rb") as f:
            head = f.read(8192)
        if b"\x00" in head:          # 第二关：NUL
            return False
        decoded = head.decode("utf-8", errors="replace")
        if decoded.count("\ufffd") > len(head) * 0.02:   # 第三关：替换率>2%
            return False
    except OSError:
        return False
    return True
```

### 2.3 判定算法实测验证（2026-08-28 ALL PASS）

| 文件 | 期望 | 实测 | 依据 |
|:---|:---:|:---:|:---|
| `/opt/homebrew/bin/python3` (Mach-O) | 二进制 | ✅ 二进制 | 含 NUL + magic `\xcf\xfa\xed\xfe` |
| `bin/lh.py` (194KB 大文本) | 文本 | ✅ 文本 | 无 NUL · 替换率 0（修复前 strict 解码会误伤） |
| `README.md` | 文本 | ✅ 文本 | 纯 UTF-8 |
| `/bin/ls` (系统二进制) | 二进制 | ✅ 二进制 | 含 NUL |
| `08_BIN/lh_fix_attribution.py` | 文本 | ✅ 文本 | 纯 UTF-8 |

> **教训（焊死）：** 不能只用 strict UTF-8 解码（尾部截断会误伤大文本），不能只查后缀（`.14`/`.bin` 等怪异后缀会漏网）。**必须三关连过。**

### 2.4 三关判定流程图（双端统一 · 协议核心算法）

```
┌───────────────────────────────────────────────────────────────┐
│                   文件类型判定三关流程（统一）                  │
├───────────────────────────────────────────────────────────────┤
│  第一关 · 后缀黑名单（NON_TEXT_EXT 命中？）                    │
│  ├─ 命中（.dylib/.so/.a/.o/.pyc/.exe/.png/.pdf...）→ 🔴 二进制 │
│  └─ 未命中 → 进入第二关                                       │
├───────────────────────────────────────────────────────────────┤
│  第二关 · 前 8KB 含 NUL（\x00）？                              │
│  ├─ 含 NUL → 🔴 二进制（机器码/压缩/加密）                     │
│  └─ 不含 NUL → 进入第三关                                     │
├───────────────────────────────────────────────────────────────┤
│  第三关 · UTF-8 替换字符率（errors="replace" 解码）            │
│  ├─ 替换率 > 2% → 🔴 二进制                                   │
│  ├─ 替换率 ≤ 2% → 🟢 文本（可读可写可签名）                    │
│  └─ 无法解码（decode 返回 nil）→ 🔴 二进制                     │
├───────────────────────────────────────────────────────────────┤
│  收尾 · shebang 识别（仅文本文件执行）                         │
│  ├─ 首行 "#!...python3" → Python 脚本                          │
│  ├─ 首行 "#!...bash"    → Bash 脚本                            │
│  ├─ 首行 "#!...cnsh"    → CNSH 脚本                            │
│  └─ 无 shebang → 纯文本                                       │
└───────────────────────────────────────────────────────────────┘
```

> **双端必须与上图同构**：iOS（§十一 Swift）与鸿蒙（§十二 ArkTS）的判定逻辑不得增删关卡顺序，只允许语言表达差异。

---

## 三、脚本分类总表：bin/ 目录每个文件对应什么

> 依据 2026-08-28 实测：`bin/` 共 2749 项。**bin/ 是软链 → 08_BIN/ 的真实目录**（同名不同路径先 `ls -ld` + `readlink` + `stat -f %i` 三查再动）。

### 3.1 按后缀分类（实测分布）

| 后缀 | 数量 | 身份 | 说明 |
|:---|:---:|:---|:---|
| `.asc` | 1297 | C. 伴生 | GPG 分离签名文件，**永远不单独改** |
| `.py` | 1147 | A. 文本 | Python 脚本（引擎/工具/CLI） |
| `.sh` | 128 | A. 文本 | Shell 脚本（部署/守护/运维） |
| `.glyph-backup` | 111 | C. 伴生 | 字形备份（恢复机制用），**不删不改** |
| `.json` | 5 | A. 文本 | 配置/注册表 |
| 无后缀 | — | 视内容 | 目录（`__pycache__` 等）或可执行文件（按 §二判定） |

### 3.2 按功能分类（每个脚本对应什么）

| 功能域 | 代表脚本（bin/08_BIN） | 对应什么 |
|:---|:---|:---|
| 🧠 记忆·认知 | `lh_memory_load.py` `lh_memory_hub.py` `lh_command_catalog.py` | 加载焊死记忆 / 跨AI协作记忆 / 命令分类 |
| 🕐 时间·DNA | `lh_time_engine.py` | 干支四柱·64卦·时间戳 |
| 🔏 签名·主权 | `lh_gpg_sign.py` `lh_vault.py` | GPG 签名/验证 / 统一密钥库 |
| 🛠️ 修复·对齐 | `lh_fix_attribution.py` `lh_align.py` `lh_fix_duplicate_functions.py` | 归属名补齐 / 对齐检查 / 去重 |
| 🚀 入口·总控 | `lh.py` `lh_boot` `lh_memory_load.py` | 主命令入口 / 启动 / 记忆 |
| 🌐 部署·同步 | `lh_hcloud.sh` `start_all.sh` `sync-collab.sh` | 华为云 / 守护启动 / 协作同步 |
| 📊 审计·检查 | `lh_post_task_audit.py` `lh_registry_auto_sync.py` `lh_threshold_trigger.py` | 任务后审计 / 注册表同步 / 阈值触发 |
| 🎬 媒体·创作 | `lh_avs3*` `lh_video*` `lh_capture*` | 编码 / 视频 / 对话采集 |

> **新脚本登记规则（焊死）：** 新建任何脚本 → ① 按 §三.1 分类后缀 → ② 按 §四 选语言 → ③ 按 §六 写文件头 → ④ 注册到 `COMMAND_INDEX.md` + 本协议 3.2 表 → ⑤ GPG 签名。缺一步视为未完成交付。

---

## 四、语言选择矩阵：什么代码用什么语法

| 你要做什么 | 用哪个语言 | Shebang/头 | 理由 |
|:---|:---|:---|:---|
| 引擎/CLI/数据处理/审计 | **Python 3** | `#!/usr/bin/env python3` | 标准库强·零依赖·跨平台 |
| 部署/守护/运维/启动链 | **Bash** | `#!/bin/bash` | launchd/systemd 原生兼容 |
| 前端页面/交互 | **HTML/CSS/JS** | 无 shebang，`<!DOCTYPE html>` | 浏览器渲染 |
| 配置/数据交换 | **JSON/YAML/TOML** | 无 shebang | 结构化数据 |
| 中文编程/符号系统 | **CNSH** | 按 `LH-CNSH-SYNTAX-SPEC-v3.0.md` | 龍魂专属语言 |
| 编译型性能件 | **Rust/C/Go** | 按各语言惯例 | 编译产物=二进制(B类) |
| 数据库 | **SQL** | 无 shebang | 结构化查询 |
| iOS 原生/沙盒 | **Swift** | 无 shebang（App 内调用） | 系统自带运行库 |
| 鸿蒙原生/沙盒 | **ArkTS** | 无 shebang（Module 内调用） | 系统自带运行库 |

**硬规则：**
- 纯文本处理 → Python；进程编排 → Bash；两者不可互换强扭。
- **绝不用文本工具写二进制文件；绝不用二进制格式存配置。**
- 新语言加入系统 → 先过 P08 仓颉命名 + P05 审计 + 更新本协议。
- **移动端（iOS/鸿蒙）执行脚本 ≠ 桌面端**：沙盒无 `/bin/bash`/系统 Python，须内置解释器或改走原生实现（见 §十一.2 / §十二.2 适配表）。

---

## 五、格式规范：空格/缩进/换行/BOM/编码/符号

> 全系统符号语法细节见 `LH-SYNTAX-SPEC-v3.0.md`，本表为文件级格式硬标准。

| 项目 | 标准 | 违规后果 |
|:---|:---|:---|
| **编码** | 一律 UTF-8 无 BOM | BOM 会让 shebang 失效、Python 报错 |
| **换行** | LF（Unix），禁 CRLF | CRLF 会破坏 shell 脚本 |
| **Python 缩进** | **4 空格**，禁 Tab | Tab/空格混用 = SyntaxError |
| **Shell 缩进** | 2 空格 | 风格统一 |
| **JS/TS/ArkTS 缩进** | 2 空格 | 风格统一 |
| **Swift 缩进** | 4 空格 | 风格统一（Xcode 默认） |
| **JSON** | 4 空格（与 Python 一致） | 工具解析 |
| **文件尾** | 末尾一个换行符 | POSIX 标准 |
| **符号** | 品牌/核心类名繁体「龍」· 通用变量英文蛇形 | 见 SYNTAX-SPEC |
| **行宽** | ≤120 字符（建议 88） | 可读性 |
| **注释** | 中文注释，写"为什么"不写"是什么" | 可维护性 |
| **关键字** | DNA/确认码/GPG 格式严格照抄 SYNTAX-SPEC | 校验失败 |

---

## 六、文件头规范：每个文件开头写什么

### 6.1 文本代码文件（.py/.sh/.js）头部四行强制

```
#!/usr/bin/env python3        # ← shebang 必须第一行
# -*- coding: utf-8 -*-       # ← 编码声明（Python）
# DNA: #龍芯⚡️<干支四柱>·<卦>-<模块>-<动作>-<哈希8>
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层） 或  # License: MulanPSL v2
```

### 6.2 文档文件（.md）头部

```
# 🐉 标题
> **DNA:** `#龍芯⚡️...`
> **确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
```

### 6.3 iOS/鸿蒙源文件（.swift / .ets）头部

```swift
//  FileIdentityDetector.swift
//  DNA: #龍芯⚡️<干支四柱>·<卦>-FILE-IDENTITY-IOS-v1.1-<哈希8>
//  创建者: 诸葛鑫（UID9622）
//  归属名: 诸葛鑫 | UID9622 · 龍芯北辰
//  License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
```

```typescript
// FileIdentityDetector.ets
// DNA: #龍芯⚡️<干支四柱>·<卦>-FILE-IDENTITY-HARMONY-v1.1-<哈希8>
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
```

### 6.4 分层许可判定（详见 LH-LAYERED-LICENSE-v1.0）

- `.md`（协议/哲学/白皮书）→ 思想层 `CC BY-NC-SA 4.0`
- `.py/.js/.html/.sh/.swift/.ets/Dockerfile/.yml` → 工程层 `MulanPSL v2`
- 混合/无法判定 → 归思想层（更严格）

---

## 七、防误伤红线：什么绝对不能做

| # | 红线 | 后果 |
|:---:|:---|:---|
| 1 | **禁止对系统目录扫描/写头**：`/opt/homebrew` `/usr` `/bin` `/sbin` `/etc` `/var` `/Library` `/System` `/private` `/Applications`（移动端同理：`/system` `/usr` `/data/app`） | 系统崩溃（本次事故） |
| 2 | **禁止对二进制文件（B类）写文本头** | Mach-O/ELF 损坏 |
| 3 | **禁止单独修改伴生 `.asc`/`.glyph-backup`** | 签名/备份失配 |
| 4 | **禁止 `rm -rf` 系统目录** | M261 红线·∞级 |
| 5 | **禁止写 `~/Downloads`/`~/Desktop`/`/tmp` 作为交付路径** | 路径铁律 |
| 6 | **禁止覆盖同名不同路径文件前不三查**（`ls -ld`+`readlink`+`stat -f %i`；移动端=`lstat` 判定） | 自毁 |
| 7 | **禁止删除：只冻结**（`_archive/`） | P0 天条第5条 |
| 8 | **敏感文件（.asc/.sig/私钥）禁止入 git 提交内容** | 密钥泄露 |

---

## 八、工具链职责：谁管文件身份、谁管签名、谁管对齐

| 工具 | 职责 | 调用 |
|:---|:---|:---|
| `lh_fix_attribution.py` | 文本文件归属名补齐（**已按本协议加固**：后缀+NUL+替换率三关 + 系统目录黑名单） | `--core --fix` |
| `lh_gpg_sign.py` | 全文件 GPG 签名/验证/扫描 | `sign`/`verify`/`scan` |
| `lh_align.py` | 对齐检查/修复（确认码/重复/相似） | `check --refresh`/`fix`/`dry-run` |
| `lh_vault.py` | 密钥统一存管（值不落盘） | `put/get/list` |
| `lh_time_engine.py` | 干支卦时间戳 | `--stamp` |
| **iOS 端** | `FileIdentityDetector.swift`（§十一）| App 内调用 |
| **鸿蒙端** | `FileIdentityDetector.ets`（§十二）| Module 内调用 |

> **职责边界：** 签名 ≠ 身份判定 ≠ 归属名补齐。三个工具各管一摊，**禁止一个工具越权修改文件头之外的内容**。任何工具要写文件 → 先过 §一分类 + §二判定。

---

## 九、记忆索引规范：系统记忆里怎么分开这些脚本

> 用户诉求落地：**记忆里按"功能域"分，不按文件名堆。**

### 9.1 记忆分类原则

```
MEMORY.md / 每日日志中提及脚本时，必须带【功能域·语言·用途】三要素：
  【记忆·Python】lh_memory_load.py — 加载焊死记忆
  【部署·Bash】start_all.sh — 守护进程启动
  【签名·Python】lh_gpg_sign.py — GPG 签名
  【识别·Swift】FileIdentityDetector.swift — iOS 端三关判定
  【识别·ArkTS】FileIdentityDetector.ets — 鸿蒙端三关判定
```

### 9.2 脚本登记 Checklist（写入记忆前必过）

1. 它属于哪个功能域？（§3.2 八域之一）
2. 它是什么语言？（§四）
3. 它是文本还是二进制还是伴生？（§一）
4. 它注册到 COMMAND_INDEX 了吗？
5. 它 GPG 签名了吗？

### 9.3 记忆引用格式

- 完整索引 → `COMMAND_INDEX.md`（唯一真相源）
- 会话快速引用 → `bin/<名>.py` 或 `08_BIN/<名>.py`
- 提到脚本必带**功能域前缀**（🔏签名/🛠️修复/🧠记忆/🌐部署/📊审计/🎬媒体/🚀入口/🕐时间）
- 移动端文件（.swift/.ets）→ 带【识别·Swift】/【识别·ArkTS】前缀，指向上游协议 `LH-FILE-SCRIPT-IDENTITY-PROTOCOL-v1.1`

---

## 十、常见误判案例表（反面教材）

| 案例 | 误判 | 正确 | 教训 |
|:---|:---|:---|:---|
| `python3.14`（后缀 `.14`） | 当文本写入归属名 | 二进制·含NUL·绝不写头 | **后缀不可信，看内容** |
| `bin/lh.py` 194KB 尾部截断 | strict 解码失败误判二进制 | 替换率 0% = 文本 | **不能 strict 解码** |
| `.asc` 签名文件 | 当文本补归属名 | 伴生文件·只随主文件 | **三类分开** |
| `bin` vs `08_BIN` 软链 | 当成两个不同目录各扫一遍 | 同一目录双扫=重复 | **先 readlink 三查** |
| `.jsonl` 审计日志 | 当文本补头 | 伴生/数据流·只追加 | **追加不改头** |
| iOS 沙盒内 `Process("/bin/bash")` | 直接 launchPath="/bin/bash" | 沙盒无 bash → 崩溃 | **移动端按 §11.2 适配** |

---

## 十一、iOS 端落地实现（Swift）

> 与 §二.4 流程图同构。沙盒约束：**iOS 无法直接执行系统 `/bin/bash` 与系统 Python**——脚本执行必须走内置解释器（见 11.2 适配表），判定与隔离逻辑不受影响。

### 11.1 文件类型判定（FileIdentityDetector.swift）

```swift
import Foundation

/// 文件身份（与协议 §一 三类 + shebang 语言对应）
enum FileIdentity: Equatable {
    case text
    case binary
    case script(language: ScriptLanguage)
}

enum ScriptLanguage: Equatable {
    case python, bash, cnsh, json, yaml, unknown
}

/// 三关判定器（与 08_BIN/lh_fix_attribution.py 同源 · 2026-08-28 焊死）
struct FileIdentityDetector {

    /// 第一关：后缀黑名单（与协议 NON_TEXT_EXT 对齐）
    static let binaryExts: Set<String> = [
        "png", "jpg", "jpeg", "gif", "ico", "pdf", "zip", "gz", "xz",
        "bz2", "7z", "mp4", "mp3", "wav", "woff", "woff2", "ttf", "otf",
        "exe", "so", "dll", "pyc", "pyo", "pyd", "class", "jar", "db",
        "bin", "dat", "whl", "tar", "ipa", "dylib", "a", "o", "framework",
        "xcframework", "app", "asc", "sig"
    ]

    /// 防误伤红线：系统路径黑名单（§七 红线1）
    static let forbiddenPaths: [String] = [
        "/System", "/usr", "/bin", "/sbin", "/etc", "/var",
        "/Library", "/private", "/Applications", "/opt/homebrew"
    ]

    private static let probeBytes = 8192

    static func identify(_ url: URL) -> FileIdentity {
        // 第一关：后缀黑名单（不读内容）
        let ext = url.pathExtension.lowercased()
        if binaryExts.contains(ext) {
            return .binary
        }

        // 只读前 8KB（mappedIfSafe 内存映射，不整文件载入）
        guard let handle = try? FileHandle(forReadingFrom: url) else {
            return .binary
        }
        defer { try? handle.close() }
        guard let head = try? handle.read(upToCount: probeBytes), !head.isEmpty else {
            return .binary
        }

        // 第二关：前 8KB 含 NUL → 二进制
        if head.contains(0) {
            return .binary
        }

        // 第三关：UTF-8 替换字符率 > 2% → 二进制（禁 strict 解码）
        guard let str = String(data: head, encoding: .utf8) else {
            return .binary // 无法解码 → 二进制
        }
        let replacementCount = str.reduce(0) { $0 + ($1 == "\u{FFFD}" ? 1 : 0) }
        if !str.isEmpty && Double(replacementCount) / Double(str.count) > 0.02 {
            return .binary
        }

        // 收尾：shebang 识别（仅对文本文件执行）
        let headStr = String(data: head.prefix(256), encoding: .utf8) ?? ""
        let firstLine = headStr.components(separatedBy: "\n").first ?? ""
        if firstLine.hasPrefix("#!") {
            if firstLine.contains("python3") { return .script(language: .python) }
            if firstLine.contains("bash")    { return .script(language: .bash) }
            if firstLine.contains("cnsh")    { return .script(language: .cnsh) }
            return .script(language: .unknown)
        }
        return .text
    }
}
```

### 11.2 语言矩阵（iOS 沙盒执行适配）

| 语言 | 判定结果 | iOS 执行方式 | 说明 |
|:---|:---|:---|:---|
| Python | `.script(.python)` | 内置 Python 运行时（BeeWare `python-ios` / `PythonKit`）→ `Process` 调用 | iOS 无系统 Python，必须随 App 打包解释器 |
| Bash | `.script(.bash)` | `ios_system`（App 内嵌 shell）或改走 Swift 原生等价实现 | **沙盒无 `/bin/bash`**，裸 `Process` 必崩 |
| CNSH | `.script(.cnsh)` | 集成 CNSH 解释器（`CNSH.framework`）| 龍魂专属语言，随 App 打包 |
| JSON/YAML | `.text`（无 shebang） | `JSONSerialization` / `Yams` 原生解析 | 不产生进程 |
| 文本/未知 | `.text` | App 原生读取/展示 | 不执行 |

```swift
/// 执行脚本（按 11.2 适配表分发）
func executeScript(_ url: URL, identity: FileIdentity) throws {
    guard case .script(let lang) = identity else { return }

    let process = Process()
    process.currentDirectoryURL = url.deletingLastPathComponent()

    switch lang {
    case .python:
        // 需内置 python-ios 运行时，解释器路径以实际打包为准
        process.executableURL = URL(fileURLWithPath: "/path/to/bundled/python3")
        process.arguments = [url.path]
    case .bash:
        // 需 ios_system 提供 bash；无则抛错，禁止裸调 /bin/bash
        process.executableURL = URL(fileURLWithPath: "/path/to/bundled/bash")
        process.arguments = [url.path]
    case .cnsh:
        process.executableURL = URL(fileURLWithPath: "/path/to/bundled/cnsh")
        process.arguments = [url.path]
    default:
        return
    }
    try process.run()
}
```

### 11.3 二进制硬隔离（防止误写）

```swift
/// 返回 true = 禁止写入（系统路径 / 伴生 / 软链）
func isolateBinary(_ url: URL) -> Bool {
    let path = url.path

    // 红线1：系统路径黑名单
    for forbidden in FileIdentityDetector.forbiddenPaths {
        if path.hasPrefix(forbidden) { return true }
    }

    // 伴生文件（.asc / .glyph-backup）只读，永不单改（红线3）
    if path.hasSuffix(".asc") || path.hasSuffix(".glyph-backup") {
        return true
    }

    // 三查软链：lstat 判符号链接，禁止写透（红线6）
    var st = stat()
    if lstat(path, &st) != 0 { return true }
    if st.st_mode & S_IFMT == S_IFLNK { return true }

    return false
}
```

### 11.4 iOS 调用示例

```swift
let url = URL(fileURLWithPath: "/path/to/script.py")
let identity = FileIdentityDetector.identify(url)

switch identity {
case .script(let lang):
    print("✅ 脚本: \(lang)")          // .python / .bash / .cnsh
    try? executeScript(url, identity: identity)
case .binary:
    print("🔴 二进制·只读不写")        // 过 isolateBinary 拦截
case .text:
    print("🟢 文本·可读可写可签名")
}

if isolateBinary(url) {
    // 系统路径 / 伴生 / 软链 → 拒绝一切写入
    return
}
```

---

## 十二、鸿蒙端落地实现（ArkTS · HarmonyOS Next）

> 与 §二.4 流程图同构。依赖 `@ohos.file.fs`（文件 IO）与 `@kit.ArkTS` 的 `util.TextDecoder`。鸿蒙沙盒同样**无法直接执行系统 shell/Python**，执行需内置解释器或原生实现。

### 12.1 文件类型判定（FileIdentityDetector.ets）

```typescript
import fs from '@ohos.file.fs';
import { util } from '@kit.ArkTS';

export enum FileIdentity {
  TEXT = 'text',
  BINARY = 'binary',
  SCRIPT_PYTHON = 'script_python',
  SCRIPT_BASH = 'script_bash',
  SCRIPT_CNSH = 'script_cnsh',
  UNKNOWN = 'unknown'
}

export class FileIdentityDetector {
  /** 第一关：后缀黑名单（与协议 NON_TEXT_EXT 对齐） */
  static readonly BINARY_EXTS: string[] = [
    'png', 'jpg', 'jpeg', 'gif', 'ico', 'pdf', 'zip', 'gz', 'xz',
    'bz2', '7z', 'mp4', 'mp3', 'wav', 'woff', 'woff2', 'ttf', 'otf',
    'exe', 'so', 'dll', 'pyc', 'pyo', 'pyd', 'class', 'jar', 'db',
    'bin', 'dat', 'whl', 'tar', 'ipa', 'dylib', 'a', 'o', 'asc', 'sig'
  ];

  /** 红线1：系统路径黑名单（鸿蒙沙盒） */
  static readonly FORBIDDEN_PATHS: string[] = [
    '/system', '/usr', '/bin', '/sbin', '/etc', '/var', '/data/app'
  ];

  private static readonly PROBE_BYTES = 8192;

  static identify(filePath: string): FileIdentity {
    // 第一关：后缀黑名单
    const dotIdx = filePath.lastIndexOf('.');
    const ext = dotIdx >= 0 ? filePath.substring(dotIdx + 1).toLowerCase() : '';
    if (this.BINARY_EXTS.includes(ext)) {
      return FileIdentity.BINARY;
    }

    let file: fs.File | undefined;
    try {
      file = fs.openSync(filePath, fs.OpenMode.READ_ONLY);

      // 读前 8KB
      const buf = new ArrayBuffer(this.PROBE_BYTES);
      const len = fs.readSync(file.fd, buf);
      const bytes = new Uint8Array(buf, 0, len);
      if (len <= 0) {
        return FileIdentity.BINARY;
      }

      // 第二关：前 8KB 含 NUL → 二进制
      if (bytes.includes(0)) {
        return FileIdentity.BINARY;
      }

      // 第三关：UTF-8 替换字符率 > 2%（禁 strict）
      const decoder = util.TextDecoder.create('utf-8', { ignoreBOM: true });
      const decoded = decoder.decodeToString(bytes);
      const replacementCount = (decoded.match(/\uFFFD/g) || []).length;
      if (decoded.length > 0 && replacementCount / decoded.length > 0.02) {
        return FileIdentity.BINARY;
      }

      // 收尾：shebang 识别（仅文本）
      const headBytes = bytes.length > 256 ? bytes.subarray(0, 256) : bytes;
      const headStr = decoder.decodeToString(headBytes);
      const firstLine = headStr.split('\n')[0] ?? '';
      if (firstLine.startsWith('#!')) {
        if (firstLine.includes('python3')) { return FileIdentity.SCRIPT_PYTHON; }
        if (firstLine.includes('bash'))    { return FileIdentity.SCRIPT_BASH; }
        if (firstLine.includes('cnsh'))    { return FileIdentity.SCRIPT_CNSH; }
        return FileIdentity.UNKNOWN;
      }
      return FileIdentity.TEXT;
    } catch (e) {
      return FileIdentity.BINARY; // 读不到 → 保守判二进制
    } finally {
      if (file) {
        fs.closeSync(file);
      }
    }
  }
}
```

### 12.2 二进制硬隔离（鸿蒙沙盒）

```typescript
import fs from '@ohos.file.fs';

export function isForbiddenBinary(filePath: string): boolean {
  // 红线1：系统路径黑名单
  for (const prefix of FileIdentityDetector.FORBIDDEN_PATHS) {
    if (filePath.startsWith(prefix)) {
      return true;
    }
  }

  // 伴生文件只读（红线3）
  if (filePath.endsWith('.asc') || filePath.endsWith('.glyph-backup')) {
    return true;
  }

  // 三查软链：符号链接禁止写透（红线6）
  try {
    const stat = fs.statSync(filePath);
    if (stat.isSymbolicLink()) {
      return true;
    }
  } catch (e) {
    return true;
  }

  return false;
}
```

### 12.3 鸿蒙调用示例

```typescript
const identity = FileIdentityDetector.identify('/data/user/0/xxx/files/script.sh');

if (identity === FileIdentity.SCRIPT_BASH) {
  // 需内置 shell 解释器（鸿蒙沙盒无 /bin/bash），否则改原生实现
  console.log('✅ Bash 脚本');
} else if (identity === FileIdentity.BINARY) {
  // 先过 isForbiddenBinary 拦截，再决定是否只读
  console.log('🔴 二进制·只读不写');
} else {
  console.log('🟢 文本·可读可写');
}

if (isForbiddenBinary('/data/user/0/xxx/files/secret.asc')) {
  // 伴生文件 → 拒绝写入
}
```

---

## 十三、双端验证清单（验收表）

> 提交 iOS/鸿蒙 代码前逐项勾选；桌面端工具（§八）同表，替换调用方式。

| # | 验证项 | 动作 | 预期 |
|:---:|:---|:---|:---|
| 1 | `.py` 文件判定为 Python 脚本 | `identify("script.py")` | iOS `.script(.python)` / 鸿蒙 `SCRIPT_PYTHON` |
| 2 | `.sh` 文件判定为 Bash 脚本 | `identify("script.sh")` | iOS `.script(.bash)` / 鸿蒙 `SCRIPT_BASH` |
| 3 | `.dylib`/`.so` 判定为二进制 | `identify("lib.dylib")` | `.binary` / `BINARY` |
| 4 | 含 NUL 的文件判定为二进制 | 构造 `[0x00,...]` 前 8KB | `.binary` / `BINARY` |
| 5 | 大文本（尾部截断多字节）判文本不误伤 | `identify("lh.py")` | `.text` / `TEXT`（替换率 0%） |
| 6 | UTF-8 替换率 >2% 判二进制 | 构造乱码字节 | `.binary` / `BINARY` |
| 7 | `.asc` 伴生文件禁止写入 | `isolateBinary`/`isForbiddenBinary` | `true`（拒绝） |
| 8 | 软链接禁止写入 | lstat/statSync 判符号链接 | `true`（拒绝） |
| 9 | 系统路径禁止写入 | `/System/...`、`/data/app/...` | `true`（拒绝） |
| 10 | 三关顺序与 §2.4 流程图一致 | 代码走查 | 不增删关卡 |

> 桌面端冒烟：`python3 -c "from lh_fix_attribution import is_text_file; ..."` 与 §2.3 一致为 🟢。

---

## 十四、版本历史

| 版本 | 日期 | 修订内容 | 修订人 |
|:---|:---|:---|:---|
| v1.1 | 2026-08-28 | **双端落地补全**：新增 §2.4 三关判定流程图 · §十一 iOS Swift 实现（判定器/执行适配/二进制硬隔离/调用示例）· §十二 鸿蒙 ArkTS 实现（判定器/硬隔离/调用示例）· §十三 双端验证清单 · §四/§五/§六/§七/§八 增移动端条目 · 误判案例表增 iOS 沙盒案例 | 诸葛鑫 + AI |
| v1.0 | 2026-08-28 | 首版·三分类+三关判定算法+脚本分类总表+语言矩阵+格式规范+防误伤红线+记忆索引规范（源自 python3.14 被污染事故复盘） | 诸葛鑫 + AI |

---

## 附录A · 快速参考卡

```
开文件前问三句：
  ① 文本 or 二进制 or 伴生？   → §一 + §二算法（后缀→NUL→替换率）
  ② 该用什么语法跑？           → §四 语言矩阵（桌面+移动端）
  ③ 空格符号合规吗？           → §五 格式规范
写文件前做四步：
  ① 分类身份 → ② 选语言 → ③ 写文件头（§六） → ④ 注册+GPG签名
判定三关（双端同构）：
  后缀黑名单 → 前8KB含NUL → UTF-8替换率>2%（禁strict解码）
移动端铁律：
  iOS=FileIdentityDetector.swift · 鸿蒙=FileIdentityDetector.ets
  ✗ 沙盒无 /bin/bash / 系统Python → 必须内置解释器
绝不做的三件事：
  ✗ 系统目录写入 ✗ 二进制写头 ✗ 伴生文件单改
```

---

## 签名区

```
DNA:    #龍芯⚡️丙午·丙申·甲戌·子时·䷒临-FILE-SCRIPT-IDENTITY-PROTOCOL-v1.1-IOS-HARMONY-DUAL-END
父DNA:  #龍芯⚡️丙午·丙申·甲戌·子时·䷒临-FILE-SCRIPT-IDENTITY-PROTOCOL-v1.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
协议:   CC BY-NC-SA 4.0（核心思想层）· 附代码 MulanPSL v2（工程层）
三色:   🟢 v1.1 双端代码补全·三关判定与桌面端同源 · 🟡 移动端代码待编译验证 · 🔴 0
v1.1 · 2026-08-28 23:48 CST · 诸葛鑫 + AI
```
