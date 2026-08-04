# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂中文编辑开发环境

> **本地闭环 · 中文优先 · 不依赖外部编辑器与渲染环境**
>
> DNA: `#龍芯⚡️2026-06-26-LONGHUN-CHINESE-EDITOR-v1.1`

## 项目定位

`longhun-chinese-editor` 是一个可独立发布的 Python 包，提供：

- **中文母语编程**：CNSH 脚本本地编辑、渲染、运行
- **闭环运行环境**：不依赖 VS Code、浏览器或外部中文渲染
- **DNA 追溯**：每个文件、每个动作都带 DNA 签名
- **三色审计**：🟢 通过 / 🟡 提醒 / 🔴 熔断
- **龍魂字体支持**：内置 LonghunFont 字体文件

## 目录结构

```
dev-env/chinese-editor/
├── src/longhun_chinese_editor/   # Python 包核心
│   ├── __init__.py
│   ├── compiler/                 # 完整 CNSH 编译器（lexer/parser/codegen）
│   │   ├── lexer.py
│   │   ├── parser.py
│   │   ├── ast_nodes.py
│   │   ├── python_codegen.py
│   │   └── pipeline.py
│   ├── runtime.py                # CNSH → Python 运行时（编译器默认，正则兼容）
│   ├── editor.py                 # 本地编辑器/渲染
│   └── cli.py                    # 命令行入口
├── tests/                        # pytest 单元测试
├── examples/                     # CNSH 示例程序
├── fonts/                        # 龍魂字体
├── cnsh/                         # CNSH 规范与 DNA 模板
├── scripts/                      # 一键启动脚本
├── pyproject.toml                # 包配置（可 pip install -e .）
├── MANIFEST.in                   # 发布清单
├── LICENSE                       # CC BY-NC-SA 4.0
└── README.md                     # 本文件
```

## 安装

```bash
# 克隆或解压本目录后
pip install -e .

# 或安装开发依赖
pip install -e ".[dev,web]"
```

## 命令行使用

```bash
# 运行 CNSH 脚本（默认使用完整编译器）
cnsh-runtime run examples/hello.cnsh

# 只查看翻译后的 Python 代码
cnsh-runtime run examples/hello.cnsh --dry-run

# 使用旧版正则翻译器（兼容模式）
cnsh-runtime run examples/hello.cnsh --legacy

# 编译为独立 .py 文件
cnsh-runtime compile examples/hello.cnsh -o hello.py

# 显示分词结果
cnsh-runtime tokenize examples/hello.cnsh

# 显示版本信息
cnsh-runtime version

# 启动 CNSH 交互式解释器
cnsh-runtime repl

# 启动本地中文编辑器（渲染）
longhun-editor examples/hello.cnsh

# 启动本地中文编辑器并运行 CNSH 脚本
longhun-editor examples/hello.cnsh --run

# 运行 CNSH 脚本并查看中间代码
longhun-editor examples/hello.cnsh --run --dry-run

# 强制使用正则翻译器
longhun-editor examples/hello.cnsh --run --legacy

# 启动 REPL
longhun-editor --repl
```

## 支持的 CNSH 主干语法

- 函数 / 返回 / 返回类型 / 参数类型
- 如果 / 否则如果 / 否则（支持 elif 链）
- 循环【n】（固定次数循环）
- 当（条件循环）
- 对于 ... 在 范围(...)
- 打印（支持无括号与字符串插值 `{变量}`）
- 输入、长度、范围等内置函数
- 变量声明、赋值（含索引赋值 `arr[0] = 1`）
- 列表 `[...]`、字典 `{...}`、索引访问 `arr[0]`、`d["key"]`
- 成员访问 `obj.字段`
- 尝试 / 捕获 / 最终（try/except/finally）
- 导入 / 导入 ... 作为 ...
- 真 / 假 / 空
- 中文标点符号自动标准化

## Python API

```python
import longhun_chinese_editor as ce

# 编译源码
py = ce.compile_source('函数 主函数(){ 打印 "hello" }')

# 语法检查
ok, msg = ce.check_source(source)

# 运行源码
ns = ce.run_source(source)

# 运行文件
status = ce.run_file("examples/hello.cnsh")
```

## 龍魂字体

本环境内置龍魂字体，可直接用于中文渲染：

- `fonts/LonghunFont-Regular.otf` —— 常规字形
- `fonts/LonghunFont-WuwuColor.otf` —— 五色特殊字形

## 一键搭建（传统脚本方式）

```bash
# macOS / Linux
./scripts/setup-dev-env.sh

# Windows
./scripts/setup-dev-env.ps1
```

## 运行测试

```bash
pytest
```

## 核心特性

1. **中文母语编程**：类名、函数名、注释、文档全部中文可读
2. **DNA 追溯**：每个配置、每个脚本都带 DNA 签名
3. **三色审计**：🟢 通过 / 🟡 提醒 / 🔴 熔断
4. **本地闭环**：编辑器、渲染器、运行环境全部本地
5. **可发布为独立包**：`pip install longhun-chinese-editor`

## 与龍魂主干的集成

本开发环境已合并到 `longhun-system/dev-env/chinese-editor/`，
可直接用于开发 `longhun-system/tools/` 和 `longhun-system/skills/` 下的工具；
同时也是一个可单独发布的模块，可独立仓库运行。

---

**主权声明**: 数据根留本地，中文优先，反对 AI 平台记忆绑架。详见 [SOVEREIGNTY.md](SOVEREIGNTY.md)。
**MVP 范围**: 详见 [MVP.md](MVP.md)。
**授权协议**: CC BY-NC-SA 4.0（署名-非商业性使用-相同方式共享）
