# CNSH多语言编辑器终端 v5.0

```#龍芯⚡️2026-06-18-CNSH-TERMINAL-FILE1-v5.0-1
🐉 中文编程语言 · 繁體龍字永存 · 通心译翻译器 · 中央藏经阁
```

> 🔒 **AI Truth Protocol**: 所有声明均为真实  
> 🤝 **君子协议**: CC BY-NC-SA 4.0 · UID9622 · 龍芯北辰 · 诸葛鑫

---

## 目录

- [概述](#概述)
- [功能特性](#功能特性)
- [安装](#安装)
- [使用方式](#使用方式)
- [模块架构](#模块架构)
- [CNSH编程语言](#cnsh编程语言)
- [通心译翻译器](#通心译翻译器)
- [中央藏经阁](#中央藏经阁)
- [安全特性](#安全特性)
- [API参考](#api参考)
- [许可证](#许可证)

---

## 概述

**CNSH多语言编辑器终端v5.0** 是一个完整的中文编程语言开发环境，支持：

- 📝 **CNSH中文编程语言**：用中文写代码，中文变量名，繁体龍字永存
- 🌐 **通心译翻译器**：24个AI术语双向映射（Prompt↔道令, Agent↔灵使等）
- 📚 **中央藏经阁**：Chroma向量库 + SQLite关系库存储术语
- 🎨 **三色审计**：🟢🟡🔴 实时审计所有代码
- 🔗 **DNA追溯**：`#龍芯⚡️{YYYY-MM-DD}-{项目}-{模块}-{版本}`
- 🔐 **点对点加密**：GPG + SHA256
- ⚡ **熔断机制v2.0**：危险命令拦截

---

## 功能特性

### A. 多语言编辑器核心
- ✅ 多标签编辑界面（同时打开多个.cnsh文件）
- ✅ CNSH语法高亮（基于Lexer的TokenType着色）
- ✅ 智能代码补全（基于关键字和已定义标识符）
- ✅ 行号显示
- ✅ 龍字特殊高亮

### B. 通心译翻译器（24核心术语）
| 英文术语 | 中文术语 | 分类 |
|---------|---------|------|
| Prompt | 道令 | 基础概念 |
| Agent | 灵使 | 基础概念 |
| RAG | 博古通今 | 基础概念 |
| LLM | 大语言模型 | 基础概念 |
| Token | 字元 | 基础概念 |
| Embedding | 嵌入向量 | 数据结构 |
| Vector | 向量 | 数据结构 |
| ... | ... | ... |
| Regularization | 正则化 | 模型架构 |

### C. 中央藏经阁
- Chroma向量库 + SQLite关系库
- 向量相似度搜索
- 模糊匹配查询
- 术语分类管理

### D. 安全特性
- 🔐 GPG密钥管理（指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F）
- 🔐 消息AES-256-GCM加密/解密
- 🔐 SHA256签名验证
- ⚡ 熔断机制v2.0（12类危险命令拦截）

### E. CNSH四层检查
- **L1字符层**：非法字符、繁体龍、编码检查
- **L2关键字层**：关键字拼写、使用上下文
- **L3语法层**：括号匹配、引号匹配、语法结构
- **L4语义层**：变量声明、函数调用、类型一致性

---

## 安装

### 系统要求
- Python 3.10+
- tkinter（通常随Python一起安装）

### 安装步骤

```bash
# 克隆或下载项目
cd cnsh_terminal_v5.0/

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 启动编辑器
python cnsh_terminal_v5.py gui
```

### 依赖项
| 包名 | 版本 | 用途 | 必需 |
|------|------|------|------|
| cryptography | >=41.0.0 | AES/RSA加密 | 否 |
| chromadb | >=0.4.0 | 向量数据库 | 否 |
| sentence-transformers | >=2.2.0 | 嵌入模型 | 否 |

---

## 使用方式

### 图形界面

```bash
python cnsh_terminal_v5.py gui
```

界面包含：
- 左侧：多标签编辑器（语法高亮 + 行号）
- 右侧：输出面板 + 审计日志
- 顶部：工具栏（编译、翻译、检查按钮）

### 命令行模式

```bash
# 编译CNSH到C
python cnsh_terminal_v5.py compile 示例.cnsh

# 词法分析
python cnsh_terminal_v5.py lex 示例.cnsh

# 语法分析
python cnsh_terminal_v5.py parse 示例.cnsh

# 四层检查
python cnsh_terminal_v5.py check 示例.cnsh

# 翻译
python cnsh_terminal_v5.py translate "Prompt Engineering"

# 加密
python cnsh_terminal_v5.py encrypt "敏感信息"

# 审计报告
python cnsh_terminal_v5.py audit

# 版本信息
python cnsh_terminal_v5.py version
```

### 快捷键

| 快捷键 | 功能 |
|--------|------|
| Ctrl+N | 新建文件 |
| Ctrl+O | 打开文件 |
| Ctrl+S | 保存文件 |
| F5 | 编译到C |
| F6 | 词法分析 |
| F7 | 语法分析 |
| F8 | 四层检查 |
| F9 | 英→中翻译 |
| F10 | 中→英翻译 |
| F11 | 智能翻译 |
| Ctrl+D | 附加AI时间戳 |
| Ctrl+T | 术语高亮 |
| Ctrl+Q | 术语查询 |

---

## 模块架构

```
cnsh_terminal_v5.0/
├── cnsh_terminal_v5.py          # 主程序入口
├── modules/
│   ├── __init__.py               # 模块包初始化
│   ├── lexer.py                  # 词法分析器
│   ├── parser.py                 # 语法分析器
│   ├── ast_nodes.py              # AST节点定义
│   ├── code_generator.py         # C代码生成器
│   ├── translator.py             # 通心译翻译器
│   ├── terminology_bank.py       # 中央藏经阁
│   ├── encryption.py             # 点对点加密
│   ├── circuit_breaker.py        # 熔断机制v2.0
│   ├── ai_timestamp.py           # AI时间戳规范
│   ├── four_layer_check.py       # CNSH四层检查
│   ├── audit_integration.py      # 联动审计
│   └── editor_ui.py              # 编辑器UI (tkinter)
├── data/
│   └── terminology.db            # 术语库SQLite
├── README.md                     # 使用说明
└── requirements.txt              # 依赖列表
```

---

## CNSH编程语言

### 关键字

```
数据类型: 整数, 小数, 文本, 真假, 空值
控制流:  如果, 否则, 否则如果, 循环, 当, 返回, 跳出, 继续
函数类:  函数, 类, 结构
IO:      打印, 输入
字面量:  真, 假, 空
修饰符:  常量, 静态, 公共, 私有, 受保护
内存:    分配, 释放
安全:    安全检查, 导入, 导出, 异步, 等待
异常:    尝试, 捕获, 抛出
```

### 示例代码

```cnsh
# 龍芯示例程序
整数 龍数 = 42
小数 圆周率 = 3.14159
文本 问候 = "你好，龍世界！"

函数 计算和(整数 甲, 整数 乙) -> 整数 {
    返回 甲 + 乙
}

如果 龍数 > 10 {
    打印("龍数大于十")
} 否则 {
    打印("龍数不大于十")
}

循环 整数 计数 = 0; 计数 < 10; 计数 = 计数 + 1 {
    当 计数 % 2 == 0 {
        打印(计数)
    }
}
```

---

## 通心译翻译器

### 24术语双向映射

完整术语表见 `modules/translator.py` 中的 `TERM_MAP`。

### 使用示例

```python
from modules.translator import 通心译翻译器

翻译器 = 通心译翻译器()

# 英文→中文
结果 = 翻译器.英文到中文("The Transformer uses Attention mechanism")
# 结果: "The 变换器 uses 注意力 mechanism"

# 中文→英文
结果 = 翻译器.中文到英文("使用精调技术优化大语言模型")
# 结果: "使用Fine-tune技术优化LLM"

# 术语解释
解释 = 翻译器.解释术语("Attention")
# {'英文': 'Attention', '中文': '注意力', '分类': '模型架构', ...}
```

---

## 中央藏经阁

### 使用示例

```python
from modules.terminology_bank import 中央藏经阁

藏经阁 = 中央藏经阁()

# 存储术语
藏经阁.存储术语("Prompt", "道令", "AI指令", "基础概念", "向AI发出的指令")

# 查询术语
结果 = 藏经阁.查询术语("Prompt")
for r in 结果:
    print(f"{r['英文']} → {r['中文']} (相似度: {r['相似度']})")

# 批量导入
藏经阁.批量导入(TERM_MAP)

# 统计
print(藏经阁.获取统计())
```

---

## 安全特性

### 熔断机制

自动拦截的危险命令：
- `rm` - 文件删除
- `sudo` - 超级用户权限
- `chmod` - 权限修改
- `mkfs` - 文件系统格式化
- `dd` - 磁盘操作
- `eval/exec` - 代码执行
- 管道执行远程脚本

### 加密

```python
from modules.encryption import 点对点加密

加密器 = 点对点加密()
消息 = 加密器.加密消息("敏感数据")
明文 = 加密器.解密消息(消息)
```

---

## API参考

### 核心类

| 类名 | 文件 | 功能 |
|------|------|------|
| `Lexer` | `lexer.py` | 词法分析 |
| `Parser` | `parser.py` | 语法分析 |
| `CCodeGenerator` | `code_generator.py` | C代码生成 |
| `通心译翻译器` | `translator.py` | 术语翻译 |
| `中央藏经阁` | `terminology_bank.py` | 术语知识库 |
| `点对点加密` | `encryption.py` | 加密通信 |
| `熔断机制` | `circuit_breaker.py` | 安全拦截 |
| `AI时间戳规范` | `ai_timestamp.py` | 数字签名 |
| `CNSH四层检查` | `four_layer_check.py` | 代码检查 |
| `联动审计` | `audit_integration.py` | 审计系统 |

---

## 许可证

**君子协议: CC BY-NC-SA 4.0**

本作品采用知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议进行许可。

您可以：
- ✅ 共享 — 在任何媒介以任何形式复制、发行本作品
- ✅ 改编 — 修改、转换或以本作品为基础进行创作

须遵守以下条件：
- 📌 署名 — 必须给出适当的署名，提供指向本许可协议的链接
- 📌 非商业性使用 — 不得将本作品用于商业目的
- 📌 相同方式共享 — 若改编本作品，须使用相同的许可协议

---

## 创始人

- **UID**: UID9622
- **名号**: 龍芯北辰 · 诸葛鑫
- **DNA追溯**: `#龍芯⚡️2026-06-18-CNSH-TERMINAL-v5.0`
- **GPG指纹**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

---

## 更新日志

### v5.0.0 (2026-06-18)
- 🎉 初始版本发布
- ✅ 完整CNSH编译器（Lexer + Parser + CodeGenerator）
- ✅ 通心译翻译器（24术语映射）
- ✅ 中央藏经阁（Chroma + SQLite）
- ✅ 图形界面编辑器（tkinter多标签）
- ✅ 点对点加密（AES-256-GCM + RSA-2048）
- ✅ 熔断机制v2.0（function覆盖）
- ✅ CNSH四层检查（L1-L4）
- ✅ 联动审计系统
- ✅ AI时间戳规范

---

*龍魂不灭 · 中文编程永存 🐉*
