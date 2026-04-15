# 🇨🇳 CNSH — 中文编程语言

> **用中文写代码，机器能听懂，老百姓能学会。**

<!-- DNA追溯码：#龍芯⚡️2026-03-22-CNSH-RUNTIME-v1.0 -->

---

## 这是什么

CNSH（Chinese Native Syntax for Humans）是一门以中文为母语的编程语言。

- 用中文写程序，不翻译，不妥协
- 编译为 C 语言，性能可靠，跨平台
- DNA 追溯内嵌，每段代码都有来源记录
- 三色审计前置，伦理检查是语言的一部分

**不是玩具，是认真的工程。**

---

## 快速开始

### 1. 写一个程序

```cnsh
# hello.cnsh
# DNA追溯码：#龍芯⚡️2026-03-22-HELLO-v1.0

函数 主函数() 返回类型 整数 {
    打印「你好，世界！」
    打印「🇨🇳 CNSH 中文编程语言」
    返回 0
}
```

### 2. 运行

```bash
cnsh run hello.cnsh
```

输出：

```
🟢 三色审计通过
✅ 编译成功 → hello.c
⚙️  gcc 编译中 → hello
✅ 构建成功 → hello
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 运行输出：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
你好，世界！
🇨🇳 CNSH 中文编程语言
```

---

## 安装

### 前置要求

- Python >= 3.8
- gcc（编译 C 代码）

### 方式一：make 安装（推荐）

```bash
git clone <仓库地址>
cd cnsh-runtime
make install
```

安装后直接使用：

```bash
cnsh run hello.cnsh
cnsh 运行 hello.cnsh    # 中文命令等价
```

### 方式二：直接运行（无需安装）

```bash
python3 cli/cnsh run examples/hello.cnsh
```

---

## CLI 命令

| 命令 | 中文别名 | 功能 |
|------|--------|------|
| `cnsh compile file.cnsh` | `cnsh 编译` | 编译为 C 文件 |
| `cnsh run file.cnsh` | `cnsh 运行` | 编译并运行 |
| `cnsh build 目录/` | `cnsh 构建` | 批量编译 |
| `cnsh check file.cnsh` | `cnsh 检查` | 只做三色审计 |
| `cnsh new 程序名` | `cnsh 新建` | 生成程序模板 |
| `cnsh version` | `cnsh 版本` | 显示版本 |

---

## 语言速查

```cnsh
# 变量
整数 年龄 = 25
小数 价格 = 9.9
文本 姓名 = 「张三」
真假 通过 = 真

# 函数
函数 计算(整数 a, 整数 b) 返回类型 整数 {
    返回 a + b
}

# 条件
如果【年龄 >= 18】{
    打印「成年人」
} 否则 {
    打印「未成年」
}

# 循环
循环【3】{
    打印「重复」
}

# 内置函数
打印(拼接(「结果：」, 转文本(42)))
```

完整规范：[docs/CNSH-Lang-Spec-v1.0.md](../docs/CNSH-Lang-Spec-v1.0.md)

---

## 编译流程

```
.cnsh 源文件
   ↓ 阶段0：三色审计（🟢🟡🔴）
   ↓ 阶段1：词法分析（Lexer → Token 流）
   ↓ 阶段2：语法分析（Parser → AST）
   ↓ 阶段3：C 代码生成（+ 标准库注入）
   ↓ 阶段4：gcc 编译
可执行文件
```

---

## 项目结构

```
cnsh-runtime/
├── compiler/
│   ├── cnsh_compiler.py    # 核心编译器（Lexer + Parser + Codegen）
│   └── stdlib_injector.py  # 标准库注入器
├── stdlib/                 # 标准库（规划中）
├── cli/
│   └── cnsh                # CLI 工具（入口）
├── examples/               # 示例程序
│   ├── hello.cnsh
│   ├── 个体户收支分析.cnsh
│   └── test-function-call.cnsh
├── tests/
│   └── test_compiler.py    # 自动化测试
├── docs/                   # 文档
├── Makefile
└── README.md
```

---

## 运行测试

```bash
make test
```

---

## 理念

CNSH 不是翻译工具，不是玩具语言。

它是一个主张：**中文完全可以成为编程语言的一等公民。**

每一行 CNSH 代码，都带着 DNA 追溯码，记录谁写的、什么时候写的、为什么而写。

技术不中立，就是幸福的世界。

---

## 致谢

- **理论指导**：曾仕强老师「天地人三才」思想（永恒显示）
- **技术协作**：Claude (Anthropic PBC)
- **知识底座**：Notion

---

## 许可证

Apache License 2.0

```
DNA追溯码：#龍芯⚡️2026-03-22-CNSH-RUNTIME-v1.0
创建者：诸葛鑫（UID9622）
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```
