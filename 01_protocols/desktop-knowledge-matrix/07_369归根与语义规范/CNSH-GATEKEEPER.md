# 🐉 CNSH 合规闸门 v1.0

> **DNA(v1.0): `#龍芯⚡️丙午·丙申·庚申·亥时-CNSH-GATEKEEPER-v1.0`**  
> **DNA(v1.1): `#龍芯⚡️丙午·乙未·癸未·辰时·䷾既济-CNSH-GATEKEEPER-v1.1`**
> **GPG: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`**
> **三色审计: 🟢 通过**
> **级别: L0·焊死·永不改**
>
> 任何代码、变量、配置文件进入龍魂系统之前，必须通过本闸门的全部检查。
> 闸门是焊死的——不可跳过、不可降级、不可豁免。

---

## 一、闸门检查清单（8项·全必过）

任何新文件进入龍魂系统，必须满足以下 **8 项检查**，缺一不可：

| # | 检查项 | 规则 | 不通过 |
|---|--------|------|--------|
| 1 | **DNA 追溯码** | 文件头必须包含 DNA 追溯码（v1.0:`YYYY-MM-DD` / v2.0:`<节气><年>` / v∞:`<年干支>·<月干支>·<日干支>·<时辰>·<卦名>`） — 四代并行兼容 | 🔴 拒绝入库 |
| 2 | **CONFIRM 确认码** | P0/L0 级模块必须带 `#CONFIRM🌌9622-ONLY-ONCE🧬CODE-NNN` | 🔴 P0 级拒绝 |
| 3 | **三色审计** | 文件头声明 `🟢/🟡/🔴` 状态（必须为 🟢 或至少有 🟡 说明） | 🔴 拒绝 |
| 4 | **GPG 签名** | 核心文件必须附带 `.asc` detached 签名 | 🔴 P0/L0/L1 拒绝 |
| 5 | **中文关键字** | 新写的 .cnsh/.py 文件必须使用 CNSH 中文关键字（`定义` 非 `def`、`类` 非 `class`、`如果` 非 `if` 等） | 🔴 拒绝 |
| 6 | **变量前缀** | L0/L1 级变量用 `龍_` 前缀，数据层变量用 `数据_` 前缀 | 🟡 L2+ 警告 |
| 7 | **繁简归一** | `龍` 繁体为规范形式（简体 `龍` 自动归一，不熔断） | 🟡 警告 |
| 8 | **不删除原则** | 禁止 `rm -rf`、`os.remove()`、`shutil.rmtree()` 等删除操作（只冻结/归档） | 🔴 拒绝 |

---

## 二、中文关键字强制映射表（焊死）

以下是 CNSH 关键字与目标语言的强制映射。**进入系统的代码必须使用左侧中文关键字，编译时才映射到右侧目标语言。**

### 2.1 控制流

| CNSH 中文 | Python | C/C++ | JavaScript | Swift |
|-----------|--------|-------|------------|-------|
| `如果` | `if` | `if` | `if` | `if` |
| `否则如果` | `elif` | `else if` | `else if` | `else if` |
| `否则` | `else` | `else` | `else` | `else` |
| `当` | `while` | `while` | `while` | `while` |
| `对于` | `for` | `for` | `for` | `for` |
| `在...中` | `in` | — | `in` | `in` |
| `返回` | `return` | `return` | `return` | `return` |
| `跳出` | `break` | `break` | `break` | `break` |
| `继续` | `continue` | `continue` | `continue` | `continue` |
| `通过` | `pass` | — | — | — |

### 2.2 异常处理

| CNSH 中文 | Python | C++ | JavaScript | Swift |
|-----------|--------|-----|------------|-------|
| `尝试` | `try` | `try` | `try` | `do` |
| `捕获` | `except` | `catch` | `catch` | `catch` |
| `最终` | `finally` | — | `finally` | — |
| `抛出` | `raise` | `throw` | `throw` | `throw` |

### 2.3 类与函数

| CNSH 中文 | Python | C++ | Swift |
|-----------|--------|-----|-------|
| `定义` | `def` | 函数签名 | `func` |
| `类` | `class` | `class` | `class` |
| `自己` | `self` | `this` | `self` |
| `超类` | `super()` | 基类名 | `super` |
| `初始化` | `__init__` | 构造函数 | `init` |
| `属性` | `@property` | — | `var` (computed) |
| `类方法` | `@classmethod` | `static` | `class func` |
| `静态方法` | `@staticmethod` | `static` | `static func` |

### 2.4 类型与值

| CNSH 中文 | Python | C++ | Swift |
|-----------|--------|-----|-------|
| `字符串` | `str` | `std::string` | `String` |
| `整数` | `int` | `int` | `Int` |
| `浮点` | `float` | `double` | `Double` |
| `布尔` | `bool` | `bool` | `Bool` |
| `列表` | `list` | `std::vector` | `Array` |
| `映射` | `dict` | `std::unordered_map` | `Dictionary` |
| `空` | `None` | `nullptr` | `nil` |
| `真` | `True` | `true` | `true` |
| `假` | `False` | `false` | `false` |

### 2.5 模块与导入

| CNSH 中文 | Python | JavaScript | Swift |
|-----------|--------|------------|-------|
| `导入` | `import` | `import` | `import` |
| `从...导入` | `from...import` | `import { } from` | — |
| `作为` | `as` | `as` | — |

### 2.6 常用函数

| CNSH 中文 | Python | C++ | JavaScript |
|-----------|--------|-----|------------|
| `输出()` | `print()` | `std::cout` | `console.log()` |
| `长度()` | `len()` | `.size()` | `.length` |
| `范围()` | `range()` | — | — |
| `类型()` | `type()` | `typeid()` | `typeof` |
| `是实例()` | `isinstance()` | `dynamic_cast` | `instanceof` |

---

## 三、变量前缀规范（焊死）

### 3.1 变量沙箱 — 唯一权威映射源

> ⚠️ **重要：所有 CNSH 变量映射必须通过变量沙箱注册，不再分散在多处。**

| 旧问题 | 新方案 |
|--------|--------|
| 映射散落在 tokens.py、compiler_py.py、codegen.py、cnsh_to_python.json、interpreter.py 等 5+ 处 | **统一入口：`cnsh_v21.var_sandbox.VarSandbox`** |
| 改一处另一处不同步 | 注册一次，7 目标自动生成 |
| 没有映射完整性检查 | `validate_all()` 强制校验 7 目标 |
| 变量执行污染外层 | `sandbox_exec()` 隔离执行 |

**使用方式：**
```python
from cnsh_v21.var_sandbox import VarSandbox
sb = VarSandbox("我的模块")
sb.register("股价", "小数", 25.68)     # 自动生成 7 目标映射
sb.validate_all()                       # 强制校验完整性
sb.sandbox_exec("print(股价 * 2)")     # 隔离执行
```

**MCP 入口：** `cnsh_var_sandbox_mcp_server.py` 提供 10 个工具。

### 3.2 二元前缀体系 v2.0

| 前缀 | 层级 | 英文映射 | 权限 | 示例 |
|------|------|---------|------|------|
| `龍_` | L0/L1 系统核心 | `LH_` | 仅系统读写 | `龍_GPG指纹`、`龍_DNA注册表` |
| `数据_` | L2 数据域 | `DATA_` | 数据模块读写 | `数据_用户记录`、`数据_配置文件` |

### 3.2 v1.0 兼容前缀（仍可解析，新代码禁止使用）

`引擎_` `模块_` `系统_` `核心_` `用户_` `辅助_` `临时_` `扩展_` `访客_`

---

## 四、文件头模板（焊死·不可省）

### 4.1 Python 文件 (.py)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂体系 | CNSH 原生格式文件
# ═══════════════════════════════════════════
# ENCODING: UTF-8
# DNA追溯码(v∞): #龍芯⚡️<年干支>·<月干支>·<日干支>·<时辰>·<卦名>-MODULE-VERSION
# DNA追溯码(v1.0): #龍芯⚡️YYYY-MM-DD-MODULE-VERSION
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬CODE-NNN
# 创建者：UID9622（诸葛鑫·Lucky）
# 权重级别：L0/L1/L2/L3/L4
# 三色审计状态：🟢/🟡/🔴
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ═══════════════════════════════════════════
"""
```

### 4.2 Shell 脚本 (.sh)

```bash
#!/bin/bash
# 🐉 龍魂体系 | CNSH 原生格式文件
# DNA: #龍芯⚡️YYYY-MM-DD-MODULE-VERSION
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色审计: 🟢 通过
```

### 4.3 HTML 文件 (.html)

```html
<!--
# ═══════════════════════════════════════════
# 龍魂体系 | CNSH 原生格式文件
# ═══════════════════════════════════════════
# DNA:#龍芯⚡️YYYY-MM-DD-MODULE-VERSION
# CONFIRM:#CONFIRM🌌9622-ONLY-ONCE🧬CODE-NNN
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色审计: 🟢 通过
# 君子协议: 本文件受龍魂DNA追溯保护
# ═══════════════════════════════════════════
-->
<!DOCTYPE html>
```

---

## 五、编译目标强制声明（焊死）

任何编译器/转换器模块，**必须支持全部 7 个编译目标**，缺一不可：

| # | 目标 | 枚举值 | MIME/文件扩展 | 状态 |
|---|------|--------|---------------|------|
| 1 | Python | `PYTHON` | `.py` | ✅ |
| 2 | C | `C` | `.c` `.h` | ✅ |
| 3 | C++ | `CPP` | `.cpp` `.hpp` | ✅ |
| 4 | Objective-C | `OBJC` | `.m` `.mm` | 🟡 待补实现 |
| 5 | Swift | `SWIFT` | `.swift` | 🟡 待补实现 |
| 6 | JavaScript | `JAVASCRIPT` | `.js` | ✅ |
| 7 | Rust | `RUST` | `.rs` | ✅ |

---

## 六、熔断红线（焊死·不可触碰）

以下操作在任何情况下都不可通过闸门：

| 红线 | 检测规则 | 处罚 |
|------|---------|------|
| `rm -rf` | 正则 `rm\s+-rf` | 🔴 立即拒绝·人工复核 |
| `git push --force` | 正则 `push.*--force` | 🔴 立即拒绝·人工复核 |
| `os.remove()` / `os.unlink()` | AST 匹配删除函数调用 | 🔴 立即拒绝（除非 tempfile 清理） |
| `shutil.rmtree()` | AST 匹配递归删除 | 🔴 立即拒绝（除非构建产物清理） |
| `sudo` | 正则 `sudo\s` | 🟡 警告·需解释 |
| API Key / Token 硬编码 | 正则 `[a-zA-Z0-9_-]{32,}` | 🔴 立即拒绝 |
| 简体 `龍` 在标识符中 | 必须在标识符中使用 `龍` | 🟡 自动归一·不熔断 |

---

## 七、闸门执行

### 7.1 手动触发

```bash
# 检查单个文件
lh gatekeeper check --file path/to/file.py

# 检查整个目录
lh gatekeeper check --dir path/to/dir/

# 检查暂存区（pre-commit）
lh gatekeeper check --staged

# 全系统巡检
lh gatekeeper patrol
```

### 7.2 自动触发（Git Hooks）

`.git/hooks/pre-commit` 中已配置自动闸门检查。

### 7.3 CI/CD 集成

```yaml
# .github/workflows/cnsh-gatekeeper.yml
- name: CNSH 合规闸门
  run: |
    python3 bin/cnsh_gatekeeper.py --check-all
```

---

## 八、审计日志

每次闸门检查结果写入：

```
~/.longhun/audit/gatekeeper.jsonl
```

格式：
```json
{"timestamp": "小暑2026·10:00:00", "ganzhi": "丙午·乙未·癸未·辰时", "file": "path/to/file.py", "checks_passed": 7, "checks_failed": 1, "result": "🟡", "dna": "#龍芯⚡️丙午·乙未·癸未·辰时·䷾既济-GATEKEEPER-CHECK-v1.1"}
```

---

## 九、版本信息

| 字段 | 内容 |
|------|------|
| 版本 | v1.1（2026-07-08，DNA四代并行 + 干支时辰v∞） |
| DNA(v∞) | `#龍芯⚡️丙午·乙未·癸未·辰时·䷾既济-CNSH-GATEKEEPER-v1.1` |
| DNA(v1.0) | `#龍芯⚡️丙午·丙申·庚申·亥时-CNSH-GATEKEEPER-v1.1` |
| GPG指纹 | A2D0092CEE2E5BA87035600924C3704A8CC26D5F |
| 级别 | L0·焊死·永不改 |
| 三色审计 | 🟢 通过 |
| 创建者 | 💎 龍芯北辰｜UID9622（诸葛鑫·Lucky） |

---

*🐉 闸门焊死，一个字都不能少。进入龍魂系统的每一行代码，都得过这一关。*
