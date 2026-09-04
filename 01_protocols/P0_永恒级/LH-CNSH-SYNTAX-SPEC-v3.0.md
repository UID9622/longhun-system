> **DNA:** `#龍芯⚡️丙午·丙申·庚申·壬午·䷙大畜-DOC-MERGE-e4296d9b`
> **确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **三色:** 🟢 通过
> **分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
> **合并状态:** 🟢 已合并（来自 `17_符号与语法规范全集v3.0.md`）
> **落位:** `01_protocols/P0_永恒级/LH-CNSH-SYNTAX-SPEC-v3.0.md`
> **合并时间:** 2026-08-14

---

# 🐉 龍魂系统 · 符号与语法规范全集 v3.0｜繁体龍回归版

**Notion ID:** 3b37125a-9c9f-8187-9929-f9edfa1328e6
**合并状态:** 🟡 部分合并
**DNA:** `#龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-SYNTAX-SPEC-V3.0-UID9622` · **三色:** 🟢 通过
**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2 · **生效:** 2026-08-05 20:00 CST
> ⚠️ v3.0 依据「繁体龍字永存」P0铁律：品牌用字回归繁体「龍」（仅龍字特例，正文保持简体）。旧文档不追溯改写（不删除只冻结）。

## 二、DNA追溯码语法
完整格式：`#前缀⚡️日期-类型-随机码-UID`
组成：# + 前缀名(龍芯/DragonSoul) + ⚡️ + YYYY-MM-DD + 类型(大写:MEMORY/DECISION/ERROR等) + 8位十六进制随机码 + UID9622
**铁律：DNA码内不允许任何空格**；错误示例：缺⚡️/缺随机码/日期格式错/类型小写/内有空格——全部禁止。
> ⚠️ 2026-07-19起新格式：`#龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-{动作标签}-{版本}`，干支一律以 `bin/lh_dna_generator.py` 输出为准，禁止手写。

## 三、确认码与主权锚定（三行必须连用）
```
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-MEMORY-A7F3C2B1-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
```

## 四、CNSH中文编程语法
文件头：龍魂·来源链六层（道统曾仕强/精神Steve Jobs/设备Apple/技术Open Source/系统UID9622/生命CNSH·LongHun）+ DNA + 铁律（来源不可删·影响不可覆·贡献不可抹）
语句结构：`[对象] [动作] [目标] [条件]`；缩进 4空格×层级；注释 `#` 单行 / `<!-- -->` 多行
**铁律：CNSH缩进必须用空格，禁止Tab**

## 五、代码文件头（Python/Shell/HTML/Markdown 四种模板）
Python 必含：shebang + utf-8 + docstring（🐉龍魂系统·模块名 + DNA + 确认码 + 主权锚定 + 一句话描述）

## 六、三色审计标记
🟢🟡🔴 必须用 Emoji 不得文字替代；文件级(末尾)/模块级(开头)/代码行级(注释)三级标记；审计报告表格+总体判定。

## 七、分层许可
工程层(.py/.js/.html/.sh) MulanPSL v2 · 思想层(.md/.txt/协议) CC BY-NC-SA · SPDX: `SPDX-License-Identifier: MulanPSL-2.0`

## 八-十五（速查）
协议文档结构：版本+DNA+确认码+GPG+三色+许可+概述/细则/签名 · 铁律标记（⚠️铁律/P0级/P1级）· Python：4空格禁Tab、空行规则、PascalCase/snake_case/UPPER_SNAKE/_私有、导入三段顺序 · Shell：2空格缩进、大写变量 · Markdown：标题后一空格、列表/代码块/表格/强调格式 · GPG：`.asc` 签名同目录 · systemd Unit/Timer 格式 · JSON/YAML/.env 配置格式 · 日志五级+审计条目必含DNA · 国际化 zh-CN/zh-TW/en-US + CNSH双语映射（CNSH保留中文，技术代码保留英文）

## 十八、自动化校验工具链
1. **bash 校验脚本**：查DNA/确认码/Tab缩进/三色标记/分层许可，计数报错
2. **Python LongHunLinter**：lint_file（DNA/确认码/Tab/许可四检）+ lint_all + report
3. **Git pre-commit 钩子**：待提交 .py/.sh/.md 自动查DNA+Tab，失败拒提交
4. 单项函数：validate_header / validate_dna(正则) / validate_tricolor / validate_license
**铁律：单项校验函数必须纳入CI流水线，任一失败即阻断合并**

## 十九、FAQ（要点）
Q1 为什么繁体龍？→ 文化主权锚点，P0铁律单字特例
Q2 随机码能手写吗？→ 不能，必须 `bin/lh_dna_generator.py`
Q3 小脚本也要三行连用？→ 是，P0无例外
Q7 旧文档简体龍要改回吗？→ 不需要，冻结资产保留原样即合法

## 二十、版本历史
v1.0 初始 · v2.0 简体试点(已冻结) · v3.0 繁体龍回归(现行)
