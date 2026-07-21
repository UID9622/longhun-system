# 龍魂中文编辑器 · MVP 范围与 API 说明

> DNA: `#龍芯⚡️2026-06-26-LONGHUN-CHINESE-EDITOR-MVP-v1.0`

## 一、MVP 目标

龍魂中文编辑器的最小可用版本（MVP）必须满足：

- 普通人能用中文写脚本并跑起来；
- 不依赖 VS Code、浏览器或外部中文渲染；
- 所有转换过程可审计、可查看中间 Python；
- 数据根留本地，不暗箱收割。

## 二、已支持的 CNSH 语法

| 类别 | 语法示例 | 说明 |
|---|---|---|
| 函数 | `函数 加(整数 a, 整数 b) -> 整数 { 返回 a + b }` | 参数类型、返回类型可选 |
| 变量 | `整数 x = 10` / `文本 s = "hello"` | 声明时可选初始化 |
| 赋值 | `x = 20` / `arr[0] = 5` | 支持索引赋值 |
| 打印 | `打印 "hello"` / `打印(x)` | 支持无括号和 f-string 插值 |
| 输入 | `文本 name = 输入("提示")` | 映射到 Python `input` |
| 条件 | `如果 / 否则如果 / 否则` | 支持 elif 链 |
| 循环 | `循环(3)` / `当(x < 5)` / `对于 i 在 范围(10)` | 三种循环 |
| 列表 | `列表 arr = [1, 2, 3]` / `arr[0]` | 索引访问与赋值；`.添加()` 等中文方法映射 |
| 字典 | `字典 d = {"a": 1}` / `d["a"]` | 键值对访问；`.获取("key")` 等中文方法映射 |
| 成员 | `s.长度()` / `obj.字段` | 成员访问与调用 |
| 异常 | `尝试 { ... } 捕获 { ... } 最终 { ... }` | try/except/finally |
| 导入 | `导入 "math"` / `导入 os 作为 os` | 映射到 Python import |
| 常量 | `常量 整数 PI = 314` | 语义标记，运行时等同变量 |
| 字面量 | `真` / `假` / `空` / 数字 / 字符串 | 完整支持 |
| 注释 | `# 单行注释` | 与 Python 一致 |

### 关键字映射速查

| CNSH | Python |
|---|---|
| 函数 / 定义 | def |
| 类 | class |
| 如果 / 否则如果 / 否则 | if / elif / else |
| 对于 / 当 / 循环 | for / while / for-range |
| 返回 | return |
| 尝试 / 捕获 / 最终 | try / except / finally |
| 导入 / 作为 | import / as |
| 真 / 假 / 空 | True / False / None |

### 内置函数速查

| CNSH | Python |
|---|---|
| 打印 | print |
| 输入 | input |
| 长度 | len |
| 范围 | range |
| 枚举 | enumerate |
| 映射 / 过滤 | map / filter |
| 求和 / 最大值 / 最小值 | sum / max / min |
| 排序 / 反转 | sorted / reversed |
| 整数 / 浮点 / 字符串 / 布尔 | int / float / str / bool |
| 类型 | type |
| 打开 | open |

### 中文方法映射速查

| CNSH | Python |
|---|---|
| 添加 / 扩展 / 插入 | append / extend / insert |
| 移除 / 弹出 / 清空 | remove / pop / clear |
| 获取 / 更新 / 设置默认 | get / update / setdefault |
| 分割 / 去空白 / 替换文本 | split / strip / replace |
| 以大写 / 以小写 / 以开头 | upper / lower / startswith |
| 连接 / 查找文本 | join / find |

## 三、命令行接口（CLI）

```bash
# 运行脚本（默认完整编译器）
cnsh-runtime run examples/hello.cnsh

# 编译为 .py
cnsh-runtime compile examples/hello.cnsh -o hello.py

# 只查看中间 Python
cnsh-runtime run examples/hello.cnsh --dry-run

# 兼容模式（旧版正则翻译器）
cnsh-runtime run examples/hello.cnsh --legacy

# 交互式解释器
cnsh-runtime repl

# 本地编辑器/渲染
longhun-editor examples/hello.cnsh
longhun-editor examples/hello.cnsh --run
longhun-editor --repl
```

## 四、Python API

```python
import longhun_chinese_editor as ce

# 编译源码
py = ce.compile_source('函数 主函数(){ 打印 "hello" }')

# 检查语法
ok, msg = ce.check_source(source)

# 运行源码
ns = ce.run_source(source)

# 运行文件
status = ce.run_file("examples/hello.cnsh")

# 兼容模式翻译
py_legacy = ce.legacy_translate(source)
```

## 五、设计原则

1. **最小闭环**：普通人写一个 `.cnsh` 文件就能跑。
2. **双轨运行**：编译器优先，失败自动退回正则翻译器，不卡用户。
3. **中文优先**：标识符、关键字、错误信息均可用中文。
4. **可审计**：任何脚本都能 `--dry-run` 看到生成 Python。
5. **本地主权**：不联网、不上传、不收集用户代码。

## 六、使用注意事项

1. **文件编码**：所有 `.cnsh` 文件必须保存为 **UTF-8**，建议文件头包含 `# -*- coding: utf-8 -*-`。
2. **复合词保护**：分词器会识别上下文，因此 `主函数`、`函数名`、`分数` 等复合词不会被误替换为 `主def`、`def名`。
3. **避免关键字冲突**：不建议将 CNSH 关键字作为变量名的一部分，例如 `如果值` 可能被识别为 `如果` + `值`。
4. **f-string**：支持 `{变量}` 插值；表达式内的大括号必须匹配。

## 七、暂未纳入 MVP 的能力

以下能力后续版本逐步扩展，当前 MVP 不做承诺：

- 完整类型检查 / 静态分析
- 模块系统与包管理
- 异步 / 协程
- 面向对象高级特性（继承、多态）
- 图形界面编辑器
- 与龍魂云端服务的自动同步

---

**本文件随代码版本同步更新。**
