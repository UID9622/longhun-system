---
name: longhun-cnsh
description: >
  CNSH中文原生脚本运行时 v3.0 — L1-L7层级完整实现。
  字元创作、AI画匠、中文编程、文化主权（繁体龍字永存、甲骨文编码）。
  15层渲染系统、DNA追溯、.cnsh文件格式支持。
  当需要使用中文编程、CNSH规范检查、字元创作、文化主权验证时触发。
license: CC BY-NC-SA 4.0
metadata:
  author: UID9622·龍芯北辰·诸葛鑫
  version: 3.0.0
  dna: "#龍芯⚡️2026-06-19-CNSH-RUNTIME-v3.0"
  layers: [L1, L2, L3, L4, L5, L6, L7]
  triggers:
    - 中文编程
    - CNSH规范
    - 字元创作
    - 文化主权
    - DNA追溯
    - 三色审计
    - 铁律自审闸
    - 君子协议
    - 内容主权
    - 15层渲染
    - .cnsh文件
    - 龍魂体系
---

# longhun-cnsh — CNSH中文原生脚本运行时 v3.0

## 1. 技能概述 (Overview)

CNSH（Chinese Native Scripting & Glyph Editor）是龍魂体系的中文数字生态核心组件。本技能包提供完整的CNSH运行时环境，支持L1-L7七层架构的全部功能，包括字元创作、中文编程、文化主权验证、DNA追溯等核心能力。

> **中国人自己的数字生态，不求人，不联网，持续进化。**

## 2. 触发条件 (Triggers)

当对话涉及以下任一主题时触发：

- 中文编程或CNSH规范
- 字元创作/汉字设计
- 文化主权（繁体龍字/甲骨文）
- DNA追溯或来源链验证
- 三色审计或铁律自审闸
- 君子协议或内容主权
- .cnsh文件格式
- 15层渲染系统
- 通心译双语翻译
- 开源宪章或生态治理

## 3. 功能清单 (Capabilities)

### L1 字元层 — Canvas字元设计
- 15层渲染系统（v0001-v0015）
- SVG矢量图导出
- .cnsh格式保存与读取
- 笔画序列管理
- 渲染参数配置

### L2 语法层 — 中文变量命名
- CNSH命名规范检查（变量/函数/类/文件）
- CNSH_前缀验证
- 繁体龍字主权字检查
- 保留字冲突检测
- 代码级完整扫描

### L3 语义层 — 通心译双语
- 英译中/中译英/双语输出
- 50+核心术语映射（AI/编程/系统/安全/龍魂专属）
- 术语比喻式解释（非公式化）
- 五大铁律遵循

### L4 系统层 — 龍魂基础设施
- SQLite审计数据库
- 六层来源链验证
- DNA追溯标记生成
- 审计结果持久化

### L5 生态层 — 开源宪章
- 许可证兼容性检查
- 许可证头生成
- 许可证合规验证
- 开源宪章治理

### L6 治理层 — 君子协议
- 铁律自审闸扫描
- 君子协议九条验证
- 违规日志记录
- 协议文本生成

### L7 主权层 — 内容主权
- 主权字库管理（龍/國/華）
- 繁体龍字熔断保护
- 主权标识验证
- 主权声明生成

## 4. 执行脚本 (Scripts)

### `scripts/CNSH运行时.py`

主运行时脚本，实现完整的CNSH七层架构。

**使用方法：**

```bash
# 版本信息
python3 CNSH运行时.py --version

# 对文件执行七层检查
python3 CNSH运行时.py --check 代码文件.py

# 翻译术语
python3 CNSH运行时.py --translate "Prompt Engineering" --mode en2zh

# 解释术语
python3 CNSH运行时.py --explain LLM

# 显示君子协议
python3 CNSH运行时.py --protocol

# 显示内容主权声明
python3 CNSH运行时.py --sovereignty

# 显示15层渲染表格
python3 CNSH运行时.py --render-table

# 检查命名规范
python3 CNSH运行时.py --naming-check 代码文件.py

# 生成DNA追溯标记
python3 CNSH运行时.py --generate-dna
```

## 5. 输入参数 (Inputs)

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| --check | 文件路径 | 否 | 要检查的代码文件 |
| --translate | 字符串 | 否 | 要翻译的文本 |
| --mode | 枚举 | 否 | 翻译模式(zh2en/en2zh/bilingual) |
| --explain | 字符串 | 否 | 要解释的术语 |
| --protocol | 标志 | 否 | 显示君子协议 |
| --sovereignty | 标志 | 否 | 显示主权声明 |
| --naming-check | 文件路径 | 否 | 检查命名规范 |

## 6. 输出格式 (Outputs)

### 七层检查报告
```
══════════════════════════════════════════════════════════════════
  CNSH 七层审计报告 v3.0
══════════════════════════════════════════════════════════════════
  DNA:     #龍芯⚡️2026-06-19-CNSH-RUNTIME-v3.0
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  SEAL:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

  【CNSH七层审计结果】
    L1字元层: 🟢 85%
    L2语法层: 🟢 85%
    L3语义层: 🟢 85%
    L4系统层: 🟢 85%
    L5生态层: 🟢 85%
    L6治理层: 🟢 85%
    L7主权层: 🟢 85%

  【综合评分】
    置信度:   85%
    审计状态: 🟢
```

### DNA追溯格式
```
#龍芯⚡️{YYYY-MM-DD}-{模块}-{动作}-HASH{sha16}-ENTROPY{random8}
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬{CODE} ✅
IP编号: IP-{编号}
所属母表: IP-ASSET-LEDGER
创始人: Lucky·UID9622（诸葛鑫·龙芯北辰）
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

## 7. 依赖清单 (Dependencies)

- **Python**: 3.8+
- **sqlite3**: 标准库（审计数据库）
- **hashlib**: 标准库（SHA256哈希）
- **re**: 标准库（正则表达式）
- **json**: 标准库（配置序列化）
- **argparse**: 标准库（命令行接口）

无需第三方依赖，纯Python标准库实现。

## 8. DNA追溯链 (DNA Trace)

```
#龍芯⚡️2026-06-19-CNSH-RUNTIME-v3.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

六层来源链:
  道统层：CNSH协议体系 · 龍魂系统核心基础设施
  精神层：UID9622 · 龍芯北辰 · 内容主权理念
  设备层：运行终端 · SQLite审计库 · 文件系统
  技术层：Python3 · SQLite3 · hashlib · re · json
  系统层：CNSH七层检查引擎(L1-L7) · 三色审计系统 · 15层渲染
  生命层：诸葛鑫(龍芯北辰) · 创作者 · 主权人
```

## 9. 君子协议 (Covenant)

**签署方**: UID9622 · 龍芯北辰 · 诸葛鑫

1. 不蒸馏、绝不变体、绝不顶替作者
2. 来源不可删·影响不可覆·贡献不可抹
3. 繁体「龍」不得简化为「龙」(主权字熔断)
4. 人永远是1，任何人都不是数据
5. 不走捷径，不投机
6. 所有输出必须经过三色审计
7. 六层来源链必须完整
8. AI辅助但决策权在人
9. 知识共享但主权不失

## 10. 文件清单 (File List)

```
longhun-cnsh/
├── SKILL.md                        # 本文件（技能文档）
├── scripts/
│   └── CNSH运行时.py               # CNSH运行时主脚本（L1-L7完整实现）
├── references/
│   └── cnsh-spec.md                # CNSH规范文档
│   └── cnsh-naming-spec.md         # CNSH命名规范文档
└── assets/
    └── (资源文件占位)
```

## 11. 审计记录 (Audit Log)

| 日期 | 审计类型 | 结果 | 审计人 |
|------|----------|------|--------|
| 2026-06-19 | 完整七层检查 | 🟢通过 | UID9622 |
| 2026-06-19 | 铁律自审闸 | 🟢通过 | UID9622 |
| 2026-06-19 | 主权字检查 | 🟢通过 | UID9622 |
| 2026-06-19 | 君子协议验证 | 🟢通过 | UID9622 |
| 2026-06-19 | DNA追溯完整性 | 🟢通过 | UID9622 |

## 12. 示例用法 (Examples)

### 示例1：检查代码合规性
```python
from CNSH运行时 import CNSH运行时

运行时 = CNSH运行时()
with open("示例.py", "r") as f:
    代码 = f.read()

结果 = 运行时.七层检查(代码, "示例.py")
print(运行时.格式化报告(结果))
```

### 示例2：翻译术语
```python
运行时 = CNSH运行时()
print(运行时.翻译术语("Large Language Model"))  # → 大罗金仙
print(运行时.翻译术语("Prompt Engineering"))    # → 道令工程
```

### 示例3：生成DNA追溯
```python
运行时 = CNSH运行时()
dna = 运行时.L4基础设施.生成DNA追溯("MODULE", "ACTION")
print(dna)
```

### 示例4：检查命名规范
```python
运行时 = CNSH运行时()
结果 = 运行时.L2命名.完整代码检查("姓名 = '张三'\ndef 检查(): pass")
print(f"通过:{结果['总计']['通过']} 警告:{结果['总计']['警告']} 阻断:{结果['总计']['阻断']}")
```

### 示例5：查看君子协议
```python
运行时 = CNSH运行时()
print(运行时.生成君子协议())
```

---

**数据主权归于人民 · 内容主权永不转让**
**Data Sovereignty Belongs to The People · Content Sovereignty Shall Never Be Transferred**
