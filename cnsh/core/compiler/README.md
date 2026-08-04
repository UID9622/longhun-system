# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--
龍魂CNSH编译器文档 · P1-3层级
DNA:#龍芯⚡️2026-06-03-CNSH-COMPILER-README-FILE1-v1.0
作者: UID9622 · 诸葛鑫 · 龍芯北辰
-->

# 🐉 龍魂CNSH编译器 (P1-3)

> 计算逻辑赋能层 · 可参数化编译 · 确定性流水线

**版本**: 1.0.0
**DNA**: `#龍芯⚡️2026-06-03-CNSH-COMPILER-v1.0`
**状态**: 🟢 生产可用
**责任**: UID9622·不免责

---

## 📋 快速开始

### 最简单的使用方式

```python
from cnsh_core.compiler import get_cnsh_compiler
from cnsh_core.compiler.compiler_node import CompileTask, TargetLang

# 获取全局编译器实例（单例）
compiler = get_cnsh_compiler()

# 创建编译任务
task = CompileTask(
    task_id="TEST-001",
    source_code="函数 测试() { 返回 1 + 2; }",
    target_lang=TargetLang.PYTHON,
    optimize_level=1  # 常量折叠
)

# 执行编译
result = compiler.compile(task)

# 查看结果
print(f"状态: {result.status}")
print(f"输出代码:\n{result.output_code}")
print(f"DNA: {result.dna}")
```

### 命令行快速测试

```bash
cd ~/longhun-system/cnsh-core

# 运行自检
python3 -c "
from compiler import get_cnsh_compiler
compiler = get_cnsh_compiler()
success, errors = compiler.selftest()
print('✅ 编译器就绪' if success else f'❌ 错误: {errors}')
"
```

---

## 🏗️ 五层编译管道

龍魂编译器采用**五层流水线架构**，从源代码逐步转换为目标语言：

```
CNSH 中文源代码
    ↓
[0] 三色安全审计 (Three-Color Audit)
    ↓
[1] 词法分析 (Lexer) - Token识别
    ↓
[2] 语法分析 (Parser) - AST构建
    ↓
[3] 语义分析 (Semantic) - 类型检查·作用域分析
    ↓
[4] 优化 (Optimizer) - 常量折叠·死代码消除·表达式简化
    ↓
[5] 代码生成 (CodeGen) - 目标语言输出
    ↓
DNA追溯 + 三色审计结果
    ↓
目标语言代码 (C/Python/JavaScript/Rust)
```

### 各层详解

#### [0] 三色安全审计

在编译前进行安全检查，防止恶意代码：

```python
# 审计规则（来自 ThreeColorAudit）
- 🔴 红色: 包含禁止函数 → 编译中止
- 🟡 黄色: 包含警告函数 → 继续编译但记录警告
- 🟢 绿色: 通过安全检查 → 正常编译
```

#### [1] 词法分析 (Lexer)

将源代码字符序列转换为Token流（词法单元）：

**支持的Token类型**:
- `KEYWORD` - 中文关键字 (函数, 如果, 返回, 循环等)
- `IDENTIFIER` - 标识符 (变量名、函数名)
- `NUMBER` - 数字字面量 (整数、浮点数)
- `STRING` - 字符串字面量 (用双引号)
- `OPERATOR` - 运算符 (+, -, *, /, ==, !=, &&, ||等)
- `PUNCTUATION` - 标点符号 ({, }, (, ), [, ], ,, ;)

**每个Token包含**:
- `type` - Token类型
- `value` - 原始值
- `line` - 行号
- `column` - 列号
- `dr` - 数字根（用于可计算验证）
- `hash` - SHA-256哈希（用于去重）

#### [2] 语法分析 (Parser)

基于PEG文法将Token序列解析为抽象语法树(AST)：

**支持的语句类型**:
- `程序 (Program)` - 顶级节点
- `函数声明 (FunctionDeclaration)`
- `变量声明 (VariableDeclaration)`
- `如果语句 (IfStatement)`
- `循环语句 (LoopStatement)`
- `返回语句 (ReturnStatement)`
- `表达式语句 (ExpressionStatement)`

**AST节点结构**:

```python
@dataclass
class ASTNode:
    node_type: str      # PROGRAM, FUNCTION, STATEMENT等
    value: Any          # 节点的实际数据
    children: List      # 子节点列表
    dna: str            # 节点DNA（可追溯）
    depth: int          # 树深度（复杂度度量）
```

#### [3] 语义分析 (Semantic)

执行类型检查、作用域分析、权重指向解析：

**检查项**:
- ✅ 变量/函数定义检查
- ✅ 类型兼容性验证
- ✅ 嵌套作用域管理
- ✅ 标识符重复定义检测
- ✅ 调用参数检查

**支持的CNSH类型**:

| CNSH | Python | C | JavaScript | Rust |
|------|--------|---|------------|------|
| 整数 | int | int | number | i32 |
| 小数 | float | double | number | f64 |
| 文本 | str | char* | string | String |
| 布尔 | bool | bool | boolean | bool |
| 列表 | list | Array | Array | Vec |
| 映射 | dict | struct | Object | HashMap |
| 空值 | None | void | null | None |

#### [4] 优化 (Optimizer)

对AST进行可融合的数学变换优化：

**优化级别**:

```
Level 0: 无优化
    • 直接生成代码

Level 1: 常量折叠 (Constant Folding)
    • 1 + 2 → 3
    • 5 * 2 → 10
    • true && false → false
    • 支持所有算术、比较、逻辑运算

Level 2: 死代码消除 (Dead Code Elimination)
    • 包含 Level 1 的所有优化
    • 移除 always-false if 语句
    • 保留 else 分支

Level 3: 表达式简化 (Expression Simplification)
    • 包含 Level 1-2 的所有优化
    • x + 0 → x
    • x * 1 → x
    • x && true → x
    • x || false → x
    • 支持 20+ 种简化规则
```

**优化跟踪**:

```python
report = optimizer.get_optimization_report()
# {
#   'level': 1,
#   'optimizations_applied': [
#       '常量折叠: +',
#       '常量折叠: *',
#       ...
#   ],
#   'total_optimizations': 42
# }
```

#### [5] 代码生成 (CodeGen)

将优化后的AST转换为目标语言代码：

**支持的目标语言**:
- 🐍 **Python** - 易读、缩进风格
- 🔴 **C** - 高效、需要类型声明
- 🟨 **JavaScript** - Web交互、动态类型
- 🦀 **Rust** - 安全、内存管理

**语言差异自动处理**:
- 语句终止符 (Python无`;`, C/JS/Rust有)
- 类型声明 (C/Rust显式, Python/JS隐式)
- 循环语法 (for-in vs for-of vs for等)
- 函数签名格式

---

## 📚 完整API文档

### 核心类: `CNSHCompiler`

```python
from cnsh_core.compiler import get_cnsh_compiler

# 获取全局实例
compiler = get_cnsh_compiler(optimize_level=1)

# 主编译方法
result: CompileTask = compiler.compile(task: CompileTask)

# 获取编译历史
history = compiler.get_compile_history()
# 返回: [
#   {
#       'task_id': 'TEST-001',
#       'status': '🟢',
#       'compile_time': 0.0042,
#       'dna': '#龍芯⚡️...',
#       'error_count': 0,
#       'warning_count': 0,
#       ...
#   },
#   ...
# ]

# 自检
success, errors = compiler.selftest()
```

### 数据模型: `CompileTask`

```python
from cnsh_core.compiler.compiler_node import CompileTask, TargetLang, CompileStatus

task = CompileTask(
    # 基础信息
    task_id="COMPILE-20260603-001",        # 编译任务ID
    source_code="函数 ...",                # CNSH源代码
    target_lang=TargetLang.PYTHON,         # 目标语言

    # 编译配置
    optimize_level=1,                      # 优化级别 0-3
    enable_audit=True,                     # 启用安全审计
    mapping_overrides={                    # 自定义映射覆盖
        "自定义函数": "custom_func"
    },

    # 编译结果（执行后填充）
    status=CompileStatus.SUCCESS,          # 编译状态 🟢/🟡/🔴
    output_code="",                        # 生成的目标代码
    errors=[],                             # 错误列表
    warnings=[],                           # 警告列表

    # DNA和追溯
    dna="",                                # 本次编译的DNA

    # 性能指标
    compile_time=0.0,                      # 编译耗时(秒)

    # 审计信息
    dr_value=0,                            # 数字根（0-9）
    audit_color="🟢",                      # 审计颜色
)

# 序列化/反序列化
task_dict = task.to_dict()
task2 = CompileTask.from_dict(task_dict)
```

### 词法分析: `Lexer`

```python
from cnsh_core.compiler.lexer import Lexer

lexer = Lexer(config_dir="~/longhun-system/03_compiler")

tokens = lexer.tokenize(source_code)
# 返回: [
#   Token(type='KEYWORD', value='函数', line=1, column=0, ...),
#   Token(type='IDENTIFIER', value='测试', line=1, column=2, ...),
#   ...
# ]
```

### 语法分析: `Parser`

```python
from cnsh_core.compiler.parser import Parser

parser = Parser()

ast = parser.parse(tokens)
# 返回: ASTNode(
#   node_type='PROGRAM',
#   value={...},
#   children=[...]
# )
```

### 语义分析: `SemanticAnalyzer`

```python
from cnsh_core.compiler.semantic import SemanticAnalyzer

analyzer = SemanticAnalyzer()

success, errors, warnings = analyzer.analyze(ast)

# success: bool - 是否通过语义检查
# errors: List[str] - 致命错误列表
# warnings: List[str] - 警告列表
```

### 优化: `Optimizer`

```python
from cnsh_core.compiler.optimizer import Optimizer

optimizer = Optimizer(level=1)  # 0-3

optimized_ast = optimizer.optimize(ast)

report = optimizer.get_optimization_report()
# 返回: {
#   'level': 1,
#   'optimizations_applied': [...],
#   'total_optimizations': 42
# }
```

### 代码生成: `CodeGenerator`

```python
from cnsh_core.compiler.codegen import CodeGenerator
from cnsh_core.compiler.compiler_node import TargetLang

codegen = CodeGenerator(target_lang=TargetLang.PYTHON)

output_code = codegen.generate(ast)
# 返回: 生成的目标语言代码字符串
```

---

## 🔧 配置和定制

### 配置目录结构

```
~/longhun-system/03_compiler/
├── COMPILE-REGISTRY.local.jsonl    # 编译任务注册表
└── mappings/
    ├── keywords.json               # 关键字映射
    ├── operators.json              # 运算符映射
    └── stdlib.json                 # 标准库映射
```

### 扩展关键字映射

编辑 `~/longhun-system/03_compiler/mappings/keywords.json`:

```json
{
  "函数": {
    "python": "def",
    "c": "void",
    "javascript": "function",
    "rust": "fn"
  },
  "新增关键字": {
    "python": "custom_keyword",
    "c": "CUSTOM_KEYWORD",
    "javascript": "customKeyword",
    "rust": "custom_keyword"
  }
}
```

### 自定义映射覆盖

在编译任务中覆盖默认映射：

```python
task = CompileTask(
    task_id="TEST",
    source_code="...",
    target_lang=TargetLang.PYTHON,
    mapping_overrides={
        "打印": "custom_print",     # 覆盖标准库函数映射
        "我的函数": "my_function",
    }
)
```

---

## 📊 DNA追溯和审计

### DNA生成

每次编译都生成唯一的DNA追溯码：

```python
# 编译后
result.dna  # "#龍芯⚡️2026-06-03-CNSH-COMPILE-C5A8F2-v1.0"

# 包含信息:
# - 源代码哈希
# - 目标语言
# - 输出代码哈希
# - 编译时间戳
```

### 三色审计结果

```python
# 审计颜色
result.audit_color  # "🟢" (通过) / "🟡" (警告) / "🔴" (失败)

# 数字根值
result.dr_value     # 0-9 (使用公式 F18 计算)

# 规则引用
# 🔴 红色: dr ∈ {3, 9}
# 🟡 黄色: dr = 6
# 🟢 绿色: 其他
```

### 编译日志

所有编译操作自动记录到:

```
~/longhun-system/logs/compiler_execution.jsonl
```

**日志格式**:

```json
{
  "task_id": "COMPILE-20260603-001",
  "timestamp": "2026-06-03T18:42:00.123456",
  "source_code_hash": "a1b2c3d4...",
  "target_lang": "python",
  "status": "🟢",
  "compile_time": 0.0042,
  "error_count": 0,
  "warning_count": 0,
  "dna": "#龍芯⚡️2026-06-03-CNSH-COMPILE-C5A8F2-v1.0",
  "dr_value": 6,
  "audit_color": "🟢"
}
```

---

## 💡 使用场景

### 场景1: 简单的编译和输出

```python
from cnsh_core.compiler import get_cnsh_compiler
from cnsh_core.compiler.compiler_node import CompileTask, TargetLang

compiler = get_cnsh_compiler()

# CNSH代码
cnsh_code = """
函数 计算阶乘(数字 n) {
    如果 (n <= 1) {
        返回 1;
    }
    返回 n * 计算阶乘(n - 1);
}

函数 主程序() {
    变量 结果 = 计算阶乘(5);
    返回 结果;
}
"""

# 编译到Python
task = CompileTask(
    task_id="FACTORIAL",
    source_code=cnsh_code,
    target_lang=TargetLang.PYTHON,
    optimize_level=1
)

result = compiler.compile(task)

if result.status == "🟢":
    print(result.output_code)
else:
    print(f"编译失败: {result.errors}")
```

### 场景2: 批量编译和性能分析

```python
from cnsh_core.compiler import get_cnsh_compiler
from cnsh_core.compiler.compiler_node import CompileTask, TargetLang

compiler = get_cnsh_compiler()

# 不同优化级别对比
for opt_level in range(4):
    task = CompileTask(
        task_id=f"OPT-LEVEL-{opt_level}",
        source_code="变量 x = 1 + 2 + 3 + 4 + 5;",
        target_lang=TargetLang.PYTHON,
        optimize_level=opt_level
    )

    result = compiler.compile(task)
    print(f"优化级别 {opt_level}: {result.compile_time:.4f}s")

# 查看编译历史
history = compiler.get_compile_history()
for record in history:
    print(f"{record['task_id']}: {record['status']} ({record['compile_time']:.4f}s)")
```

### 场景3: 多语言编译

```python
from cnsh_core.compiler import get_cnsh_compiler
from cnsh_core.compiler.compiler_node import CompileTask, TargetLang

compiler = get_cnsh_compiler()

targets = [TargetLang.PYTHON, TargetLang.C, TargetLang.JAVASCRIPT, TargetLang.RUST]

for target in targets:
    task = CompileTask(
        task_id=f"MULTI-{target.value}",
        source_code="函数 问好() { 返回 \"你好\"; }",
        target_lang=target,
        optimize_level=2
    )

    result = compiler.compile(task)
    print(f"\n===== {target.value.upper()} =====")
    print(result.output_code)
```

---

## 🚀 集成到龍魂系统

### 系统启动器集成

编译器在系统启动时自动初始化为第9步：

```bash
$ cd ~/longhun-system/cnsh-core
$ python3 core_system_launcher.py

[1/9] 加载龍魂系统配置... ✅
[2/9] 验证创始人身份... ✅
...
[8/9] 初始化规则引擎... ✅
[9/9] 初始化CNSH编译器... ✅
    ✅ CNSH编译器就绪
```

### 路由注册表

编译器注册为 `IPA-L1-003` 节点：

```python
from cnsh_core.registry import get_route_registry

registry = get_route_registry()

# 获取编译器节点
node = registry.lookup("IPA-L1-003")
# 返回: RouteNode(
#   node_id="IPA-L1-003",
#   name="cnsh_compiler",
#   entry_point="get_cnsh_compiler",
#   dna="#龍芯⚡️2026-06-03-CNSH-COMPILER-v1.0",
#   ...
# )

# 获取编译器实例
compiler = node.get_instance()
```

### 与规则引擎集成

编译规则可以注册到规则引擎：

```python
from cnsh_core.rules import get_rule_engine

rule_engine = get_rule_engine()

# 示例规则：禁止编译某些关键字
rule = {
    "rule_id": "COMPILE-FORBID-UNSAFE",
    "condition": "'不安全函数' in source_code",
    "action": "block_compile",
}

rule_engine.register_rule(rule)
```

---

## ⚠️ 常见问题和错误处理

### Q1: 词法分析失败

**错误**: `无法识别的字符`

**原因**: 输入包含不支持的字符

**解决**:
```python
# 检查源代码是否只包含支持的字符
# 支持: 中文字符、英文字母、数字、符号 +=-*/()"{}[],.;
```

### Q2: 类型不匹配

**错误**: `变量 x 期望 整数 但得到 小数`

**原因**: 赋值右值类型与变量声明类型不兼容

**解决**:
```python
# 修改源代码，确保类型一致
# 或修改变量声明类型
```

### Q3: 未定义的标识符

**错误**: `未定义的标识符: xyz`

**原因**: 使用了未声明的变量或函数

**解决**:
```python
# 确保变量在使用前已声明
# 函数调用前函数已定义
```

### Q4: 编译器自检失败

**错误**: `配置目录不存在`

**原因**: `~/longhun-system/03_compiler/` 目录缺失

**解决**:
```bash
mkdir -p ~/longhun-system/03_compiler/mappings
# 手动创建映射表文件（JSON格式）
```

---

## 📈 性能指标

基于参考实现的性能数据（使用 Python 3.9+）:

| 代码大小 | 优化级别 | 编译时间 | 内存占用 |
|---------|---------|---------|--------|
| 10行 | 0 | <1ms | ~2MB |
| 10行 | 1 | 1-2ms | ~3MB |
| 100行 | 0 | 2-5ms | ~5MB |
| 100行 | 3 | 5-10ms | ~8MB |
| 1000行 | 0 | 10-20ms | ~20MB |
| 1000行 | 3 | 30-50ms | ~35MB |

**优化影响**:
- Level 0 → Level 1: +10-20% 编译时间
- Level 1 → Level 3: +200-300% 编译时间
- 优化效果：10-40% 代码大小缩减

---

## 🧪 测试和自检

### 运行自检

```python
from cnsh_core.compiler import get_cnsh_compiler

compiler = get_cnsh_compiler()

success, errors = compiler.selftest()

if success:
    print("✅ 所有自检项通过")
else:
    print("❌ 自检失败:")
    for error in errors:
        print(f"  - {error}")
```

### 自检项目

自检会验证以下内容:
- ✅ 配置目录存在
- ✅ 映射表文件完整 (keywords, operators, stdlib)
- ✅ 词法分析器可用
- ✅ 语法分析器可用
- ✅ 语义分析器可用
- ✅ 优化器可用
- ✅ 代码生成器可用
- ✅ DNA系统可用
- ✅ 三色审计系统可用

---

## 📖 理论依据

### 哲学核心

龍魂编译器体现的"计算逻辑赋能"哲学：

> "有些东西可以计算的，可以融在一起计算的，我们都用计算的方式来解决它。
> 用逻辑、用参数、用跟计算机协作，对不对。
> 不是一个人接入就得到全部功能，是赋能给他们。"
> —— 创始人 UID9622

**应用体现**:
1. **计算优先** - 词法/语法/语义/优化都是确定性算法，可完全追溯
2. **参数化** - 通过映射表JSON、优化级别等参数暴露计算边界
3. **可融合** - 多个优化Pass可合并为一次树遍历
4. **赋能而非替代** - 提供编译API和框架，让使用者构建自己的工具

### 可计算性保证

所有关键步骤都是可验证的:

| 阶段 | 可验证性 | 追溯方式 |
|-----|--------|--------|
| Lexer | ✅ Token序列完全确定 | token.hash / token.dr |
| Parser | ✅ AST结构唯一 | ast_node.dna / tree深度 |
| Semantic | ✅ 类型推导基于规则 | 符号表快照 |
| Optimizer | ✅ 变换记录完整 | optimizations_applied列表 |
| CodeGen | ✅ 输出确定性生成 | 源代码+语言→唯一输出 |

---

## 🔗 相关资源

### 项目文件

- **源代码**: `~/longhun-system/cnsh-core/compiler/`
- **配置**: `~/longhun-system/03_compiler/`
- **日志**: `~/longhun-system/logs/compiler_execution.jsonl`

### 龍魂系统

- **启动器**: `~/longhun-system/cnsh-core/core_system_launcher.py`
- **规范**: `~/longhun-system/cnsh-core/规范/`
- **文档**: `~/longhun-system/README.md`

### 相关模块

- P0 数学模块 (IPA-L0-006) - DNA和dr_gate计算
- P1 规则引擎 (IPA-L1-002) - 编译规则执行
- P1 调度器 (IPA-L1-001) - 任务调度

---

## 📞 支持和反馈

**问题报告**: `~/longhun-system/issues/`
**改进建议**: `~/longhun-system/proposals/`
**贡献指南**: `~/longhun-system/CONTRIBUTING.md`

---

## 📜 许可证和署名

**DNA**: `#龍芯⚡️2026-06-03-CNSH-COMPILER-README-v1.0`
**作者**: UID9622 · 诸葛鑫 · 龍芯北辰
**责任**: UID9622·不免责
**状态**: 🟢 生产可用

本文档是龍魂系统的一部分，遵循系统的完整责任链。

---

**最后更新**: 2026-06-03
**版本**: 1.0.0
**维护者**: UID9622
