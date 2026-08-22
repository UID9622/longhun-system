# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CNSH 中文原生脚本运行时 · 通心译执行引擎

**DNA**:#龍芯⚡️丙午·甲午·辛酉·甲午·䷨损-CNSH-RUNTIME-FILE1-v1.0  
**责任**: UID9622·不免责

---

## 核心信念

> **英文不是唯一计算机执行的指令。**

CNSH（Chinese Native Script）不是一门全新的编程语言，而是一层覆盖在现有语言（Python 为首选目标）之上的**中文语义层**。它让开发者用中文语法书写意图，运行时透过**通心译**将其解释为可执行代码。

- **心**：中文语义与意图，不可妥协
- **壳**：Python / JavaScript / 其他目标语言的适配表达

---

## 运行环境

本运行时基于 Python 3，纯标准库实现，无需额外依赖。

| 平台 | 状态 | 说明 |
|------|------|------|
| macOS | ✅ | 直接运行 `python3 cnsh_runner.py ...` |
| Huawei / HarmonyOS | ✅ | 安装 Python 后直接运行 |
| Linux | ✅ | 任何发行版均可运行 |
| Windows | ✅ | 透过 Python for Windows 运行 |

---

## 快速开始

```bash
cd ~/longhun-system

# 运行示例
bash bin/run-cnsh.sh cnsh-core/cnsh-runtime/examples/hello.cnsh

# 显示转译过程与解释
bash bin/run-cnsh.sh cnsh-core/cnsh-runtime/examples/longhun_audit.cnsh --explain --show-code

# 进入交互式解释器
bash bin/run-cnsh.sh --repl
```

---

## CNSH 语法示例

```cns
# hello.cnsh
名字 = "龍魂"
打印("世界，你好！我是", 名字)
```

```cns
# calculate.cnsh
定义 计算总和(数字列表):
    总和 = 0
    对于 数字 在 数字列表:
        总和 = 总和 + 数字
    返回 总和

数据 = [1, 2, 3, 4, 5]
结果 = 计算总和(数据)
打印("数据总和:", 结果)
```

```cns
# persona.cnsh
类 人格:
    定义 初始化(自己, 名称, 角色):
        自己.名称 = 名称
        自己.角色 = 角色

    定义 介绍(自己):
        打印(f"我是{自己.名称}，担任{自己.角色}")

诸葛 = 人格("诸葛亮", "军师")
诸葛.介绍()
```

---

## 支持的语法映射

### 控制流

| CNSH | Python | 备注 |
|------|--------|------|
| 如果 / 如果 | if | 条件判断 |
| 否则如果 / 否则如果 | elif | 多分支 |
| 否则 / 否则 | else | 默认分支 |
| 对于 / 对于 / 循环 / 循环 | for | 遍历循环 |
| 当 / 当 | while | 条件循环 |
| 返回 / 返回 | return | 返回值 |
| 中断 / 中断 | break | 跳出循环 |
| 继续 / 继续 | continue | 跳过本次 |

### 定义

| CNSH | Python |
|------|--------|
| 定义 / 定义 | def |
| 函数 / 函数 | def |
| 类 / 类 | class |
| 导入 / 导入 | import |
| 从 / 从 | from |

### 运算符

| CNSH | Python |
|------|--------|
| 等于 / 等于 | == |
| 不等于 / 不等于 | != |
| 大于 / 大于 | > |
| 小于 / 小于 | < |
| 大于等于 / 大于等于 | >= |
| 小于等于 / 小于等于 | <= |
| 与 / 与 | and |
| 或 | or |
| 非 / 非 | not |
| 在 | in |

### 常用函数

| CNSH | Python |
|------|--------|
| 打印 | print |
| 长度 / 长度 | len |
| 范围 / 范围 | range |
| 输入 / 输入 | input |

---

## 设计原则

1. **简繁兼融**：同时支持简体与繁体中文关键字
2. **字符串保护**：字符串字面量不做任何转译，保留原意
3. **变量中文化**：变量、函数、类名可用中文命名
4. **字典可扩展**：新增术语只需编辑 `dictionaries/cnsh_to_python.json`
5. **本地执行**：不依赖云端，保证数字主权

---

## 与通心译的关系

通心译负责**意图传递**，CNSH 运行时负责**意图执行**。当你写下：

```cns
闸控检查(请求, 风险阈值)
```

通心译会解释其意图为 *Gate Check (request, risk threshold)*，而 CNSH 运行时会将其转译为可执行的 Python 函数调用。

---

## 未来扩展

- [ ] 支持 JavaScript 作为目标语言
- [ ] 支持 HarmonyOS ArkTS 代码生成
- [ ] 增加 CNSH 模块系统（`导入` 多文件）
- [ ] 集成 64 卦审计与三色审计到运行时
- [ ] 开发 CNSH LSP 语言服务器

---

> 🐉 龍魂永世，文化传承，数字主权，科技自主创新不可让渡！
