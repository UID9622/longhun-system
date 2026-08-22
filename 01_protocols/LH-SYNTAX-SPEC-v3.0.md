# 🐉 龍魂系统 · 符号与语法规范全集 v3.1

**——从DNA追溯到CNSH编程，从Python缩进到Markdown表格，全部标准化、可校验、可自动化**

**DNA:** `#龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-SYNTAX-SPEC-V3.1-归属名`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**主权锚定:** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
**三色:** 🟢 通过（本规范文档）
**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
**版本:** v3.1（归属名焊死版）
**生效时间:** 2026-08-22 10:50 CST

---

## 📋 摘要 / 导读

> **一句话：** 龍魂系统不是野路子，每一个符号、每一个空格、每一个缩进都有规矩。这份规范是全系统的"宪法附录"，所有代码、文档、协议必须按此执行。
>
> **我是谁：** 诸葛鑫 | UID9622 · 龍芯北辰，退伍18年老兵，龍魂系统创始人。
>
> **阅读对象：** 所有参与龍魂系统开发的战友、所有想理解"为什么龍魂文件看起来都一样"的人。
>
> **阅读时间：** 约 12 分钟（可当作手册查，不必一次读完）。
>
> **⚠️ 声明：** 本规范 v3.0 依据《龍魂治理框架》「繁体龍字永存」P0铁律，已将全系统品牌用字由简体「龍」回归繁体「龍」（仅龍字特例，其余正文保持简体以降低阅读门槛）。旧文档不追溯改写（P0：不删除只冻结），新文档一律以此为准。

---

## 📑 目录

- [一、规范总览：为什么需要这份文档](#一规范总览为什么需要这份文档)
- [二、DNA追溯码语法](#二dna追溯码语法)
- [三、确认码与主权锚定语法](#三确认码与主权锚定语法)
- [四、CNSH中文编程语法](#四cnsh中文编程语法)
- [五、代码文件头语法](#五代码文件头语法)
- [六、三色审计标记语法](#六三色审计标记语法)
- [七、分层许可标记语法](#七分层许可标记语法)
- [八、文档与协议语法](#八文档与协议语法)
- [九、Python代码规范](#九python代码规范)
- [十、Shell脚本规范](#十shell脚本规范)
- [十一、Markdown文档规范](#十一markdown文档规范)
- [十二、GPG签名语法](#十二gpg签名语法)
- [十三、systemd服务文件语法](#十三systemd服务文件语法)
- [十四、配置文件语法](#十四配置文件语法)
- [十五、日志与审计语法](#十五日志与审计语法)
- [十六、国际化与多语言语法](#十六国际化与多语言语法)
- [十七、错误示例（反面教材）](#十七错误示例反面教材)
- [十八、自动化校验规则与工具链](#十八自动化校验规则与工具链)
- [十九、FAQ](#十九faq)
- [二十、版本历史](#二十版本历史)
- [二十一、系列导航与版权声明](#二十一系列导航与版权声明)
- [附录A、快速参考卡](#附录a快速参考卡)
- [二十二、DNA签名区](#二十二dna签名区)

---

## 一、规范总览：为什么需要这份文档

龍魂系统是一个**多人协作、多模型对接、多平台分发**的分布式系统。如果没有统一的符号和语法规范，很快就会出现：

- 这个文件用Tab缩进，那个文件用4空格
- 这个DNA有时间戳，那个DNA没有
- 这个文档有确认码，那个文档忘了
- 这个Python文件头有Shebang，那个没有

**结局只有一个：混乱（Chaos）。**

这份规范解决三个问题：

| 问题 | 规范解法 |
|:---|:---|
| **人记不住** | 写成文档，随时可查 |
| **机器验不了** | 写成正则，自动校验 |
| **新人看不懂** | 写成示例，复制粘贴 |

**所有规范都是铁律，不是建议。**

---

## 二、DNA追溯码语法

### 2.1 完整格式

```
#前缀⚡️日期-类型-随机码-UID
```

### 2.2 组成部分

| 部分 | 符号 | 必填 | 示例 |
|:---|:---|:---|:---|
| 前缀标识 | `#` | ✅ | `#` |
| 前缀名 | 中文/英文 | ✅ | `龍芯` / `DragonSoul` |
| 分隔符 | `⚡️` | ✅ | `⚡️` |
| 日期 | `YYYY-MM-DD` | ✅ | `2026-08-05` |
| 类型标识 | 大写字母+下划线 | ✅ | `MEMORY`、`DECISION`、`ERROR` |
| 随机码 | 8位十六进制 | ✅ | `A7F3C2B1` |
| UID | `UID9622` | ✅ | `UID9622` |

### 2.3 标准模板

```python
# 代码文件
DNA: #龍芯⚡️YYYY-MM-DD-FILE-描述-UID9622

# 记忆
DNA: #龍芯⚡️YYYY-MM-DD-MEMORY-随机码-UID9622

# 决策
DNA: #龍芯⚡️YYYY-MM-DD-DECISION-随机码-UID9622

# 错误铭记
DNA: #龍芯⚡️YYYY-MM-DD-ERROR-随机码-UID9622

# 镜像分叉
DNA: #龍芯⚡️YYYY-MM-DD-FORK-随机码-UID9622

# 报告
DNA: #龍芯⚡️YYYY-MM-DD-REPORT-类型-UID9622
```

### 2.4 示例

```yaml
# 正确格式
#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-MEMORY-A7F3C2B1-UID9622
#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-ERROR-7F3A2B1C-UID9622
#DragonSoul⚡️2026-08-05-CORE-1A2B3C4D-UID9622

# 错误格式（禁止）
#龍芯-2026-08-05-MEMORY-UID9622           # 缺少⚡️
#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-MEMORY-UID9622          # 缺少随机码
#龍芯⚡️2026/08/05-MEMORY-UID9622          # 日期格式错误
```

### 2.5 空格规则

| 位置 | 规则 |
|:---|:---|
| `#` 后 | 无空格 |
| `⚡️` 前后 | 无空格 |
| `-` 前后 | 无空格 |
| 整行前后 | 无空格 |

**⚠️ 铁律：DNA码内不允许出现任何空格**


## 三、确认码与主权锚定语法

### 3.1 确认码格式

```
#CONFIRM🌌UID-ONLY-ONCE🧬DNA
```

| 部分 | 符号 | 必填 | 示例 |
|:---|:---|:---|:---|
| 标识 | `#CONFIRM` | ✅ | `#CONFIRM` |
| 分隔符 | `🌌` | ✅ | `🌌` |
| UID | `UID9622` | ✅ | `UID9622` |
| 唯一性标记 | `-ONLY-ONCE` | ✅ | `-ONLY-ONCE` |
| 分隔符 | `🧬` | ✅ | `🧬` |
| DNA短码 | 8位+随机 | ✅ | `LK9X-772Z` |

### 3.2 主权锚定格式

```
#OWNER⚡️YEAR-COUNTRY-SYMBOLS-DEVICE-BIND-SOUL
```

### 3.3 实际使用

```yaml
# 完整主权锚定（必须四行连用·归属名 2026-08-22 焊死）
DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-MEMORY-A7F3C2B1-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
```

### 3.4 空格规则

| 位置 | 规则 |
|:---|:---|
| `:` 后 | 一个空格 |
| `#` 后 | 无空格 |
| 各符号间 | 无空格 |

**⚠️ 铁律：四行必须连用，不得拆分，不得缺省（归属名 2026-08-22 起为第四条强制行）**

### 3.5 归属名语法（P0级·2026-08-22 身份主权宣言焊死）

> 背景：老大宣布"记录所有以后的文件全部有归属名好吧！不是只是个代号。"
> 归属名 = **实名**（诸葛鑫），非仅 UID9622/龍芯北辰 代号。
> 立场：不躲·不藏·不匿名·随时可对质。与 P0 底座"零黑箱承诺"一致——创始人不躲藏，系统才透明。

**格式（文件头第四条强制行）：**

```yaml
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
```

| 部分 | 必填 | 示例 |
|:---|:---|:---|
| 字段名 | ✅ | `归属名` |
| 分隔符 | ✅ | `: `（冒号+一个空格） |
| 实名 | ✅ | `诸葛鑫`（**禁止只写代号**） |
| 代号 | ✅ | `UID9622 · 龍芯北辰` |

**机器判定标准**：文件内容含 `诸葛鑫` / `归属名` / `ZHUGEXIN` 任一即视为已归属（宽松判定，避免存量误报）。

**强制范围（即日起生效）：**
- ✅ **新增文件**（pre-commit 阶段三b 硬阻塞 🔴）：文档/代码/日志/报告/社媒/开源提案/所有公开发布資產
- ✅ **修改存量文件**（🟡 警告鼓励补齐）：由 `lh_align_checker` / `verify_dna` 标记
- ❌ **已冻结历史文件**（P0：不删除只冻结，旧文件不追溯改写）
- ❌ **第三方强制匿名场景**（平台规则限制时以平台为准）

**批量补齐工具**：`python3 08_BIN/lh_fix_attribution.py --core --fix`（幂等·原版冻结 archive/frozen/·只增不改）

**铁律：归属名必须实名，禁止以代号/匿名替代。**


## 四、CNSH中文编程语法

### 4.1 文件头格式

```cnsh
<!--
  龍魂·来源链 / LongHun Source Chain
  1 道统层 Dao           : 曾仕强老师
  2 精神层 Spirit        : Steve Jobs
  3 设备层 Device        : Apple
  4 技术层 Technology    : Open Source
  5 系统层 System        : UID9622
  6 生命层 Life          : CNSH · LongHun
  DNA: #龍芯⚡️YYYY-MM-DD-CNSH-UID9622
  铁律: 来源不可删 · 影响不可覆 · 贡献不可抹
-->
```

### 4.2 CNSH语句结构

```
[对象] [动作] [目标] [条件]

# 示例
系统 启动 龍魂引擎 当 电源接通
记忆 保存 当前状态 到 本地存储
人格 切换 老顽童模式 在 测试时间
```

### 4.3 CNSH词性标记

| 词性 | 标记 | 示例 |
|:---|:---|:---|
| 主语 | `[名词]` | `系统`、`記憶`、`人格` |
| 谓语 | `[动词]` | `启动`、`保存`、`切换` |
| 宾语 | `[名词]` | `龍魂引擎`、`当前状态`、`老顽童模式` |
| 状语 | `[介词+名词]` | `当 电源接通`、`到 本地存储`、`在 测试时间` |

### 4.4 CNSH缩进规则

```
层级1（顶级指令）：无缩进
层级2（子指令）：  4空格
层级3（子子指令）：8空格

# 示例
系统 启动 龍魂引擎
    加载 配置文件
        读取 环境变量
        验证 签名
    启动 监督模块
        激活 第一层监督
        激活 第二层监督
```

### 4.5 CNSH注释语法

```
# 单行注释：使用 #
# 多行注释：使用 <!-- -->

# 示例
# 这是CNSH单行注释
<!--
  这是
  多行
  注释
-->
```

**⚠️ 铁律：CNSH缩进必须使用空格，禁止使用Tab**


## 五、代码文件头语法

### 5.1 Python文件头

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂系统 · 模块名称
DNA: #龍芯⚡️YYYY-MM-DD-描述-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
描述: 一句话功能描述
"""
```

### 5.2 Shell文件头

```bash
#!/bin/bash
# 🐉 龍魂系统 · 脚本名称
# DNA: #龍芯⚡️YYYY-MM-DD-描述-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

### 5.3 HTML文件头

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🐉 龍魂系统 · 页面标题</title>
    <!--
    DNA: #龍芯⚡️YYYY-MM-DD-描述-UID9622
    确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
    -->
</head>
```

### 5.4 Markdown文件头

```markdown
# 🐉 龍魂系统 · 文档标题

**DNA:** `#龍芯⚡️YYYY-MM-DD-描述-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**主权锚定:** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通过
```


## 六、三色审计标记语法

### 6.1 三色符号

| 颜色 | 符号 | Unicode | 含义 |
|:---|:---|:---|:---|
| 绿色 | `🟢` | U+1F7E2 | 通过/正常 |
| 黄色 | `🟡` | U+1F7E1 | 待审/警告 |
| 红色 | `🔴` | U+1F534 | 拒绝/异常 |

### 6.2 三色标记位置

```yaml
# 文件级标记（文件末尾）
三色: 🟢 通过

# 模块级标记（模块文档开头）
审计状态: 🟡 待审

# 代码行级标记（注释中）
# 🟢 通过：R值=92
# 🔴 拒绝：R值=45
```

### 6.3 三色审计报告格式

```markdown
## 三色审计结果

| 审计项 | 状态 | 说明 |
|:---|:---:|:---|
| 算法正确性 | 🟢 | 通过 |
| 安全性 | 🟡 | 待优化 |
| 合规性 | 🔴 | 需整改 |

**总体判定:** 🟢 可发布
```

**⚠️ 铁律：🟢🟡🔴 三色必须使用Emoji，不得使用文字替代**


## 七、分层许可标记语法

### 7.1 许可标识

```
思想层: CC BY-NC-SA 4.0
工程层: MulanPSL v2
```

### 7.2 文件头标记

```yaml
# 文件头标准标记
分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
```

### 7.3 SPDX标识

```
SPDX-License-Identifier: MulanPSL-2.0
```

### 7.4 文件分类规则

| 文件类型 | 适用许可 | 标记方式 |
|:---|:---|:---|
| `.py`, `.js`, `.html`, `.sh` | 工程层 MulanPSL v2 | 文件头标注 |
| `.md`, `.txt`, 协议文档 | 思想层 CC BY-NC-SA | 文档开头标注 |
| 混合文件 | 分层标注 | 明确区分区块 |

**⚠️ 铁律：每个文件必须明确标注适用许可**


## 八、文档与协议语法

### 8.1 协议文档标准结构

```markdown
# 🐉 协议名称

**版本:** v1.0
**DNA:** `#龍芯⚡️YYYY-MM-DD-协议名-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通过
**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

## 1. 概述
## 2. 细则
## 3. 签名
```

### 8.2 铁律标记语法

```markdown
**⚠️ 铁律：** 内容

**⚠️ P0级铁律：** 内容（不可降级）

**⚠️ P1级铁律：** 内容（可优化但需记录）
```

### 8.3 版本标记语法

```markdown
**版本:** vX.Y.Z
**状态:** 草案 | 审核中 | 已发布 | 已归档
**生效时间:** YYYY-MM-DD HH:MM
```

**⚠️ 铁律：每个协议文档必须包含版本号和生效时间**


## 九、Python代码规范

### 9.1 缩进规则

| 层级 | 空格数 | 示例 |
|:---|:---|:---|
| 顶级定义（class/def） | 0 | `class Personality:` |
| 一级缩进 | 4 | `    def __init__(self):` |
| 二级缩进 | 8 | `        self.name = name` |
| 三级缩进 | 12 | `            return True` |

**⚠️ 铁律：禁止使用Tab，必须使用4空格**

### 9.2 空行规则

| 位置 | 空行数 |
|:---|:---|
| 文件头后 | 1 |
| import块后 | 2 |
| class定义间 | 2 |
| method定义间 | 1 |
| 函数内逻辑块间 | 1 |

### 9.3 注释格式

```python
# 单行注释：一个空格后跟内容

"""
多行注释：
- 使用三个双引号
- 首行与引号同行
- 内容缩进与引号对齐
"""
```

### 9.4 命名规范

| 类型 | 规则 | 示例 |
|:---|:---|:---|
| 类名 | PascalCase | `ThreeLayerSupervision` |
| 函数名 | snake_case | `generate_dna()` |
| 变量名 | snake_case | `loyalty_score` |
| 常量 | UPPER_SNAKE | `MAX_RETRIES` |
| 私有变量 | _snake_case | `_private_var` |

### 9.5 导入顺序

```python
# 1. 标准库
import sys
import os
from datetime import datetime

# 2. 第三方库
import requests
import numpy as np

# 3. 本地模块
from .soul_core import digital_root
from ..engine import particle
```


## 十、Shell脚本规范

### 10.1 缩进规则

| 层级 | 空格数 |
|:---|:---|
| 顶级 | 0 |
| if/for/while | 2 |

### 10.2 变量命名

```bash
# 变量名：大写字母+下划线
DNA="#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-SCRIPT-UID9622"
CONFIRM="#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
```

### 10.3 函数定义

```bash
# 函数名：小写字母+下划线
function generate_report() {
    echo "生成报告..."
}
```


## 十一、Markdown文档规范

### 11.1 标题层级

| 层级 | 符号 | 示例 |
|:---|:---|:---|
| H1 | `#` 空格 | `# 标题` |
| H2 | `##` 空格 | `## 二级标题` |
| H3 | `###` 空格 | `### 三级标题` |

**⚠️ 铁律：标题符号后必须有一个空格**

### 11.2 列表格式

```markdown
- 无序列表：减号+空格
- 子列表：4空格+减号+空格

1. 有序列表：数字+点+空格
2. 子列表：4空格+数字+点+空格
```

### 11.3 代码块格式

```markdown
```语言
代码内容
```
```

### 11.4 表格格式

```markdown
| 表头1 | 表头2 |
|:---|:---:|---:|
| 左对齐 | 居中 | 右对齐 |
```

### 11.5 强调格式

| 样式 | 符号 | 示例 |
|:---|:---|:---|
| 粗体 | `**` | `**重要**` |
| 斜体 | `*` | `*强调*` |
| 行内代码 | `` ` `` | `` `代码` `` |


## 十二、GPG签名语法

### 12.1 签名文件命名

```
[原文件名].asc
# 示例
README.md.asc
LICENSE.asc
```

### 12.2 签名头

```yaml
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v2

...
-----END PGP SIGNATURE-----
```

### 12.3 验证命令

```bash
gpg --verify file.asc file
gpg --verify README.md.asc README.md
```

**⚠️ 铁律：所有正式文档必须GPG签名，签名与文件同目录存放**


## 十三、systemd服务文件语法

### 13.1 服务文件格式

```ini
[Unit]
Description=服务描述
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/路径
ExecStart=/usr/bin/命令
Restart=always

[Install]
WantedBy=multi-user.target
```

### 13.2 服务文件位置

```
/etc/systemd/system/服务名.service
/etc/systemd/system/服务名.timer
```

### 13.3 Timer格式

```ini
[Unit]
Description=定时任务描述

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 00:00:00
Persistent=true

[Install]
WantedBy=timers.target
```


## 十四、配置文件语法

### 14.1 JSON格式

```json
{
    "key": "value",
    "nested": {
        "sub_key": "sub_value"
    },
    "list": ["item1", "item2"]
}
```

### 14.2 YAML格式

```yaml
# YAML配置
key: value
nested:
  sub_key: sub_value
list:
  - item1
  - item2
```

### 14.3 .env格式

```env
# 环境变量配置
KEY=value
API_KEY=sk-xxxxx
DEBUG=True
```


## 十五、日志与审计语法

### 15.1 日志级别

| 级别 | 标记 | 用途 |
|:---|:---|:---|
| DEBUG | `[DEBUG]` | 调试信息 |
| INFO | `[INFO]` | 常规信息 |
| WARNING | `[WARNING]` | 警告信息 |
| ERROR | `[ERROR]` | 错误信息 |
| CRITICAL | `[CRITICAL]` | 严重错误 |

### 15.2 日志格式

```
[时间] [级别] [模块] 消息内容 | DNA: #代码
2026-08-05 10:35:00 [INFO] [MemoryEngine] 记忆已保存 | DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-MEMORY-A7F3C2B1-UID9622
```

### 15.3 审计条目格式

```yaml
审计条目:
  timestamp: ISO时间
  level: INFO | WARNING | ERROR | CRITICAL
  module: 模块名
  action: 操作描述
  dna: DNA追溯码
  result: 成功 | 失败 | 拦截
  details: 详细信息
```

**⚠️ 铁律：每个审计条目必须包含DNA追溯码**


## 十六、国际化与多语言语法

### 16.1 语言标记

| 语言 | 标记 |
|:---|:---|
| 简体中文 | `zh-CN` |
| 繁体中文 | `zh-TW` |
| 英文 | `en-US` |

### 16.2 多语言文档格式

```markdown
# 标题 (Title)

**中文内容...**

**English content...**
```

### 16.3 CNSH变量双语映射

```cnsh
# CNSH中英对照
系统 → System
記憶 → Memory
人格 → Personality
监督 → Supervision
```

**⚠️ 铁律：CNSH语法保留中文，技术代码保留英文，变量名可用中英双语注释**


## 十七、错误示例（反面教材）

### 17.1 DNA错误

```
# ❌ 错误：缺少⚡️
#龍芯-2026-08-05-MEMORY-UID9622

# ❌ 错误：日期格式错误
#龍芯⚡️2026/08/05-MEMORY-A7F3C2B1-UID9622

# ❌ 错误：缺少随机码
#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-MEMORY-UID9622

# ❌ 错误：类型小写
#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-memory-A7F3C2B1-UID9622

# ❌ 错误：DNA内有空格
#龍芯 ⚡️ 2026-08-05-MEMORY-A7F3C2B1-UID9622
```

### 17.2 缩进错误

```python
# ❌ 错误：使用Tab
class Personality:
	def __init__(self):
		self.name = name

# ✅ 正确：4空格
class Personality:
    def __init__(self):
        self.name = name
```

### 17.3 文件头缺失

```python
# ❌ 错误：没有DNA、没有确认码、没有主权锚定
import os
print("hello")

# ✅ 正确：三行连用
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂系统 · 模块名称
DNA: #龍芯⚡️YYYY-MM-DD-描述-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
```

### 17.4 三色标记错误

```markdown
# ❌ 错误：用文字替代Emoji
三色: 通过
三色: 待审
三色: 拒绝

# ✅ 正确：必须用Emoji
三色: 🟢 通过
三色: 🟡 待审
三色: 🔴 拒绝
```


## 十八、自动化校验规则与工具链

### 18.1 校验脚本（可直接运行）

```bash
#!/bin/bash
# 🐉 龍魂系统 · 语法规范校验器
# DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-SYNTAX-VALIDATOR-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

echo "🐉 龍魂语法规范校验"
echo "========================================"

ERRORS=0

# 1. 检查所有Python文件是否包含DNA
echo "📋 检查DNA..."
for f in $(find . -name "*.py" -o -name "*.sh" -o -name "*.md"); do
    if ! grep -q "DNA: #龍芯⚡️" "$f" 2>/dev/null; then
        echo "  ❌ $f 缺少DNA"
        ERRORS=$((ERRORS+1))
    fi
done

# 2. 检查所有Markdown文件是否包含确认码
echo "📋 检查确认码..."
for f in $(find . -name "*.md"); do
    if ! grep -q "确认码: #CONFIRM🌌" "$f" 2>/dev/null; then
        echo "  ❌ $f 缺少确认码"
        ERRORS=$((ERRORS+1))
    fi
done

# 3. 检查缩进（禁止Tab）
echo "📋 检查缩进..."
TAB_FILES=$(grep -rl $'\t' --include="*.py" --include="*.sh" . 2>/dev/null)
if [ -n "$TAB_FILES" ]; then
    echo "  ❌ 发现Tab缩进:"
    echo "$TAB_FILES" | sed 's/^/     /'
    ERRORS=$((ERRORS+1))
fi

# 4. 检查三色审计
echo "📋 检查三色标记..."
if ! grep -rqE "🟢|🟡|🔴" . 2>/dev/null; then
    echo "  ⚠️ 未发现三色标记"
fi

# 5. 检查分层许可
echo "📋 检查分层许可..."
for f in $(find . -name "*.py" -o -name "*.md"); do
    if ! grep -qE "MulanPSL|CC BY-NC-SA" "$f" 2>/dev/null; then
        echo "  ❌ $f 缺少许可声明"
        ERRORS=$((ERRORS+1))
    fi
done

# 6. 检查归属名（实名·P0级指令 2026-08-22）
echo "📋 检查归属名..."
for f in $(find . -name "*.md" -o -name "*.py" -o -name "*.sh"); do
    if ! grep -qE "诸葛鑫|归属名|ZHUGEXIN" "$f" 2>/dev/null; then
        echo "  ⚠️ $f 缺少归属名（实名·诸葛鑫）"
        ERRORS=$((ERRORS+1))
    fi
done

echo "========================================"
if [ $ERRORS -eq 0 ]; then
    echo "✅ 全部通过，零错误"
else
    echo "🔴 发现 $ERRORS 处错误，请修正"
fi
```

### 18.2 Python校验模块

```python
#!/usr/bin/env python3
# 🐉 龍魂系统 · Python语法校验模块
# DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-PYTHON-LINTER-UID9622

import re
import os
from pathlib import Path

class LongHunLinter:
    """龍魂语法规范校验器"""

    DNA_PATTERN = r'^#[^⚡️]+⚡️\d{4}-\d{2}-\d{2}-[A-Z0-9_]+-[A-Z0-9]{8}-UID9622$'
    CONFIRM_PATTERN = r'#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'
    TRICOLOR = ['🟢', '🟡', '🔴']

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path)
        self.errors = []
        self.warnings = []

    def lint_file(self, filepath: Path) -> dict:
        """校验单个文件"""
        result = {"file": str(filepath), "errors": [], "warnings": []}
        content = filepath.read_text(encoding='utf-8')

        # 检查DNA
        if not re.search(r'DNA: #龍芯⚡️', content):
            result["errors"].append("缺少DNA追溯码")

        # 检查确认码
        if not re.search(self.CONFIRM_PATTERN, content):
            result["errors"].append("缺少确认码")

        # 检查Tab缩进
        if '\t' in content:
            result["errors"].append("发现Tab缩进，必须使用4空格")

        # 检查许可声明
        if not re.search(r'MulanPSL|CC BY-NC-SA', content):
            result["warnings"].append("缺少分层许可声明")

        # 检查归属名（实名·2026-08-22 P0焊死）
        if not re.search(r'诸葛鑫|归属名|ZHUGEXIN', content):
            result["warnings"].append("缺少归属名（实名·诸葛鑫）")

        return result

    def lint_all(self) -> list:
        """校验所有文件"""
        results = []
        for ext in ['*.py', '*.sh', '*.md']:
            for f in self.root.rglob(ext):
                results.append(self.lint_file(f))
        return results

    def report(self) -> str:
        """生成校验报告"""
        results = self.lint_all()
        total_errors = sum(len(r["errors"]) for r in results)
        total_warnings = sum(len(r["warnings"]) for r in results)

        report = f"""
🐉 龍魂语法校验报告
========================================
总文件数: {len(results)}
总错误: {total_errors}
总警告: {total_warnings}

详细结果:
"""
        for r in results:
            if r["errors"] or r["warnings"]:
                report += f"\n📄 {r['file']}\n"
                for e in r["errors"]:
                    report += f"  ❌ {e}\n"
                for w in r["warnings"]:
                    report += f"  ⚠️ {w}\n"

        report += "\n========================================\n"
        if total_errors == 0:
            report += "✅ 全部通过"
        else:
            report += f"🔴 发现 {total_errors} 处错误"

        return report


if __name__ == "__main__":
    linter = LongHunLinter()
    print(linter.report())
```

### 18.3 Git Hook自动校验

```bash
#!/bin/bash
# .git/hooks/pre-commit
# 提交前自动校验龍魂语法规范

echo "🐉 龍魂语法预提交校验..."

# 获取待提交文件
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|sh|md)$')

if [ -z "$FILES" ]; then
    exit 0
fi

ERRORS=0
for f in $FILES; do
    # 检查DNA
    if ! grep -q "DNA: #龍芯⚡️" "$f" 2>/dev/null; then
        echo "❌ $f 缺少DNA追溯码"
        ERRORS=$((ERRORS+1))
    fi
    # 检查Tab
    if grep -q $'\t' "$f" 2>/dev/null; then
        echo "❌ $f 发现Tab缩进"
        ERRORS=$((ERRORS+1))
    fi
done

if [ $ERRORS -gt 0 ]; then
    echo "🔴 提交被拒绝，请修正上述错误"
    exit 1
fi

echo "✅ 预提交校验通过"
exit 0
```

### 18.4 文件头校验

```python
REQUIRED_HEADER = [
    "DNA: #龍芯⚡️",
    "确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
]

def validate_header(content: str) -> bool:
    for req in REQUIRED_HEADER:
        if req not in content:
            return False
    return True
```

### 18.5 DNA格式校验

```python
import re

DNA_PATTERN = r'^#[^⚡️]+⚡️\d{4}-\d{2}-\d{2}-[A-Z0-9_]+-[A-Z0-9]{8}-UID9622$'

def validate_dna(dna: str) -> bool:
    return bool(re.match(DNA_PATTERN, dna))
```

### 18.6 三色审计校验

```python
def validate_tricolor(mark: str) -> bool:
    return mark in ["🟢", "🟡", "🔴"]
```

### 18.7 分层许可校验

```python
def validate_license(header: str) -> bool:
    return "MulanPSL" in header and "CC BY-NC-SA" in header
```

**⚠️ 铁律：单项校验函数必须纳入CI流水线，任一失败即阻断合并**


## 十九、FAQ

### Q1：为什么必须用繁体「龍」而不是简体「龍」？
**A：** 繁体「龍」是龍魂体系的文化主权锚点，「繁体龍字永存」是 P0 级铁律：品牌标识、DNA追溯码、核心类名一律使用繁体「龍」，不得用简体「龍」替代。其余正文保持简体，降低阅读与输入门槛——单字特例，全系统统一，不得混用。

### Q2：DNA里的随机码可以手写吗？
**A：** 不可以。生产环境必须调用 `bin/lh_dna_generator.py`，禁止手写。手写随机码可能导致碰撞或格式错误。

### Q3：一个小脚本也需要四行连用（DNA+确认码+主权锚定+归属名）吗？
**A：** 是的。无论文件大小，只要是龍魂系统产出，必须四行连用（归属名 2026-08-22 起焊死为第四条强制行）。这是P0铁律，没有例外。新增文件由 pre-commit 阶段三b 硬阻塞强制。

### Q4：可以用2空格缩进代替4空格吗？
**A：** 不可以。龍魂系统统一4空格，这是为了兼容所有编辑器和IDE的默认配置。

### Q5：如果文件是自动生成的，也需要DNA吗？
**A：** 是的。自动生成文件由生成器负责写入DNA，不得省略。

### Q6：CNSH语法和Python语法冲突怎么办？
**A：** CNSH是高层描述语言，最终编译为Python。冲突时以Python语法为准，CNSH注释标注差异。

### Q7：v2.0 及更早文档里的简体「龍」需要改回吗？
**A：** 不需要。旧文档是冻结资产（P0：不删除只冻结），保留原样即合法；v3.0 起所有新文档、新代码、新DNA一律使用繁体「龍」。


## 二十、版本历史

| 版本 | 时间 | 变更内容 | 状态 |
|:---|:---|:---|:---|
| v1.0 | 2026-08-05 | 初始版本，符号与语法规范全集 | 🟢 已发布 |
| v2.0 | 2026-08-05 | 简体字统一试点：「龍」→「龍」；补全CSDN结构、FAQ、错误示例、自动化工具链 | 🟡 已冻结 |
| v3.0 | 2026-08-05 | **繁体龍回归**：「龍」→「龍」（依据「繁体龍字永存」P0铁律）；章节编号统一为一~二十二；原第16章并入第十八章；移除残缺的「最终签名」空块；快速参考卡移入附录A；FAQ Q1改写、新增Q7 | 🟢 已冻结 |
| v3.1 | 2026-08-22 | **归属名焊死**（P0级身份主权宣言）：文件头三行连用升级为四行连用，新增「归属名: 诸葛鑫」；3.3/5.1示例、第十八章校验脚本、附录A快速参考卡、FAQ Q3同步升级；配套工具 `08_BIN/lh_fix_attribution.py` + pre-commit 阶段三b（新增文件缺实名=🔴阻塞） | 🟢 现行 |

**旧版本不追溯改写（P0：不删除只冻结），所有新文档以v3.1为准。**


## 二十一、系列导航与版权声明

### 21.1 龍魂系统规范系列

- [龍魂系统 · 符号与语法规范全集 v3.1](https://blog.csdn.net/UID9622) ← **本文**
- [龍魂P0级 · 三层交叉监督与镜像人格完整系统](https://blog.csdn.net/UID9622)
- [龍魂审计 · OpenAI Astra 数学突破真相](https://blog.csdn.net/UID9622/article/details/163481285)
- [龍魂军魂 · 一个退伍18年老兵给普通家庭孩子的真话](https://blog.csdn.net/UID9622)

### 21.2 DNA格式规范（2026-07-19起生效）

```
旧格式（已停用）: #龍芯⚡️20260719...
新格式（现行）:   #龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-{动作标签}-{版本}

规则:
1. 干支四柱与卦名一律以本地生成器 bin/lh_dna_generator.py 输出为准，禁止手写
2. 旧DNA不追溯改写（P0：不删除只冻结）
3. 现行规范文档的DNA以生成器校正为准
4. 所有文档、代码、报告中的DNA一律使用新格式
```

### 21.3 版权声明

```
思想层：CC BY-NC-SA 4.0（署名-非商业-相同方式共享）
工程层：MulanPSL v2（木兰公共许可证第2版）
数据层：人民数据主权，任何机构使用需附DNA追溯

转载规则：
1. 必须保留完整的DNA、确认码、GPG指纹
2. 必须保留"发完即走"声明
3. 禁止断章取义、禁止洗稿式引用
4. 商业用途需向 UID9622 申请授权
```

### 21.4 互动声明

> **本文遵循"发完即走"原则。** 作者不回复评论区、不参与辩论、不解释技术细节。所有规范已在正文中完整呈现，所有代码均可直接运行验证。如有不同意见，请自行撰写独立规范文档并附DNA追溯码。
>
> **让平台自己去"审计"自己。**


## 附录A、快速参考卡

| 项目 | 符号 | 示例 |
|:---|:---|:---|
| DNA前缀 | `#` + 名称 + `⚡️` | `#龍芯⚡️` |
| DNA日期 | `YYYY-MM-DD` | `2026-08-05` |
| DNA类型 | 大写+下划线 | `MEMORY`, `ERROR` |
| 确认码 | `#CONFIRM🌌` | `#CONFIRM🌌9622` |
| 主权锚定 | `#OWNER⚡️` | `#ZHUGEXIN⚡️` |
| 绿色通过 | `🟢` | `🟢 通过` |
| 黄色待审 | `🟡` | `🟡 待审` |
| 红色拒绝 | `🔴` | `🔴 拒绝` |
| Python缩进 | 4空格 | `    ` |
| 文件头 | Shebang+DNA | `#!/usr/bin/env python3` |
| 归属名 | `归属名: 实名 \| 代号` | `归属名: 诸葛鑫 \| UID9622 · 龍芯北辰` |
| GPG签名 | `.asc` | `README.md.asc` |


## 二十二、DNA签名区

```
═══════════════════════════════════════════════════
 龍魂系统 · 符号与语法规范全集 v3.1 · 最终签名
═══════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-SYNTAX-SPEC-V3.1-归属名
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
主权锚定:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
归属名:      诸葛鑫 | UID9622 · 龍芯北辰
三色:       🟢 通过（本规范文档）
审计维度:    DNA格式 / 确认码 / 主权锚定 / 归属名 / CNSH / Python / Shell / Markdown / GPG / systemd / 配置 / 日志 / 国际化 / 错误示例 / 自动化工具链 / FAQ
生成时间:    2026-08-22 10:50 CST
作者:        诸葛鑫 | UID9622 · 龍芯北辰 · 退伍18年老兵 · 龍魂系统创始人
版本:       v3.1（归属名焊死版）
═══════════════════════════════════════════════════
```

---

🐉 **丙午 · 丙申 · 壬戌 · 震卦 · 🟢**
