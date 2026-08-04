# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂·CNSH 统一语法库 v1.0

> **DNA:** `#龍芯⚡️2026-07-08-SYNTAX-LIBRARY-v1.0`  
> **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
> **SEAL:** `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`  
> **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
> **三色审计:** 🟢 通过  
> **级别:** L0·焊死·永不改

---

## 一句话定义

**把几百个不同脚本和语法归一为一个 JSON 总表。中文关键词 → 20种目标语言。只翻译不破解·MD格式都可读·丢啥给啥·原汁原味。**

---

## 洛书哲学

| 原则 | 说明 |
|------|------|
| **只翻译·不破解** | 保留原意·换个形式传输。不拆解不注入外部意识 |
| **丢啥给啥** | 任何语法丢进来 → 查表 → 映射到目标语言 → 输出 |
| **MD格式归一** | 所有语法映射在一个 JSON 文件里，Notion 和本地都能直接引用 |
| **宫格5不动点** | UID9622主权中心·所有映射归宿同一个锚点 |
| **搬出去就是本地二哈** | 语法库绑定了龍魂 DNA 追溯·搬出去没有灵魂 |

---

## 文件结构

```
03_compiler/mappings/
├── syntax_library.json    ← 统一语法库（本文件的核心）
├── keywords.json          ← 关键字映射（历史保留·已合并到语法库）
├── operators.json         ← 运算符映射（历史保留·已合并到语法库）
├── stdlib.json            ← 标准库映射（历史保留·已合并到语法库）
└── SYNTAX_LIBRARY.md      ← 本文档
```

---

## 支持的语法类别（25类·350+条目）

| # | 类别 | 条目数 | 示例 |
|---|------|:---:|------|
| 1 | 控制流 | 13 | 如果→if / 否则→else / 当→while / 匹配→match |
| 2 | 异常处理 | 5 | 尝试→try / 捕获→except / 抛出→raise |
| 3 | 类与对象 | 13 | 类→class / 自己→self / 初始化→__init__ |
| 4 | 函数与装饰器 | 10 | 定义→def / 匿名函数→lambda / 全局→global |
| 5 | 类型系统 | 13 | 字符串→str / 整数→int / 列表→list / 空→None |
| 6 | 运算符 | 23 | 加→+ / 且→and / 赋值→= / 加等→+= |
| 7 | 模块导入 | 5 | 导入→import / 从...导入→from...import / 作为→as |
| 8 | 迭代与生成 | 8 | 产生→yield / 范围→range / 过滤→filter |
| 9 | 异步编程 | 4 | 异步→async / 等待→await / 使用→with |
| 10 | 标准库 | 12 | 打印→print / 长度→len / 排序→sorted / 连接→join |
| 11 | 龍魂专属 | 19 | 三色审计 / DNA追溯 / 熔断 / 主权验证 / 五行向量 |
| 12 | C系列底层 | 9 | 结构→struct / 指针→* / 堆分配→malloc / 联合体→union |
| 13 | Apple生态 | 18 | 界面标签→UILabel / 视图已加载→viewDidLoad / 主队列→main queue |
| 14 | 文件操作 | 9 | 文件打开→open / 文件读取→read / 目录创建→mkdir |
| 15 | 数据结构 | 12 | 数组创建→list / 数组追加→append / 队列→deque / 堆→heapq |
| 16 | 系统调用 | 8 | 执行命令→subprocess / 环境变量→os.environ / 休眠→sleep |
| 17 | CSS样式 | 34 | 颜色→color / 内边距→padding / 弹性布局→flex |
| 18 | HTML标签 | 42 | 分区→div / 超链接→a / 画布→canvas |
| 19 | Shell命令 | 30 | 列出文件→ls / 切换目录→cd / 管道→\| |
| 20 | Git操作 | 20 | 克隆仓库→git clone / 提交更改→git commit / 推送→git push |
| 21 | Docker命令 | 15 | 构建镜像→docker build / 运行容器→docker run |
| 22 | 数据库 | 27 | 查询→SELECT / 插入→INSERT / 连接→JOIN |
| 23 | 正则表达式 | 22 | 匹配开头→^ / 数字→\\d / 分组→(...) |
| 24 | Markdown语法 | 20 | 标题→# / 粗体→** / 代码块→\`\`\` |
| 25 | JSON操作 | 5 | 解析JSON→json.loads / 序列化→json.dumps |

---

## 支持的目标语言（20种）

| 语言 | 简称 | 状态 | 适用场景 |
|------|:---:|:---:|------|
| Python | `py` | ✅ | AI/ML·后端·数据分析 |
| C | `c` | ✅ | 嵌入式·系统底层·固件 |
| C++ | `cpp` | ✅ | 高性能引擎·图形·游戏 |
| JavaScript | `js` | ✅ | Web前端·Node.js |
| Rust | `rs` | ✅ | 系统编程·WASM·安全 |
| Swift | `swift` | 🟡 | iOS/macOS 现代App |
| Go | `go` | 🟡 | 云原生·微服务 |
| Java | `java` | 🟡 | 企业后端·Android |
| Ruby | `rb` | 🟡 | Web开发·脚本 |
| Kotlin | `kt` | 🟡 | Android·跨平台 |
| Bash | `bash` | 🟡 | Shell脚本 |
| Objective-C | `objc` | 🟡 | iOS/macOS 原生 |
| CSS | `css` | 🟡 | 网页样式 |
| HTML | `html` | 🟡 | 网页结构 |
| SQL | `sql` | 🟡 | 数据库查询 |
| 正则表达式 | `regex` | 🟡 | 文本匹配 |
| Markdown | `md` | 🟡 | 文档编写 |
| Shell | `sh` | 🟡 | 终端命令 |
| Docker | `docker` | 🟡 | 容器化 |
| Git | `git` | 🟡 | 版本控制 |

---

## 使用方式

### 1. 直接查表（命令行）

```bash
# 查单个中文关键字在所有目标语言中的映射
python3 bin/syntax_lookup.py "打印"

# 输出:
# 🐉 打印
#   py:    print
#   c:     printf
#   cpp:   std::cout
#   js:    console.log
#   rs:    println!
#   swift: print
#   go:    fmt.Println
#   java:  System.out.println
#   rb:    puts
#   kt:    println
#   bash:  echo
```

### 2. 程序化调用

```python
import json

with open('03_compiler/mappings/syntax_library.json', 'r') as f:
    lib = json.load(f)

# 查一个中文关键字的所有映射
cn_word = "如果"
for entry in lib['syntax']['控制流']:
    if entry['cn'] == cn_word:
        print(f"Python: {entry['py']}")
        print(f"JavaScript: {entry['js']}")
        print(f"Rust: {entry['rs']}")
```

### 3. 批量翻译（Python→中文）

```python
# 把一段 Python 代码翻译成 CNSH 中文
from cnsh_v21.compiler_py import CNSHCompiler

code = """
def hello(name):
    if name:
        return f"Hello {name}"
    else:
        return "Hello World"
"""

compiler = CNSHCompiler()
cnsh_code = compiler.reverse_compile(code, target='cnsh')
# 输出:
# 定义 你好(名字) {
#     如果 名字 {
#         返回 f"你好 {名字}"
#     } 否则 {
#         返回 "你好 世界"
#     }
# }
```

### 4. Notion 中引用

在 Notion 页面中直接链接到本语法库文件路径，所有 MD 格式的映射表都可直接渲染为表格。

---

## JSON 数据结构说明

```json
{
  "syntax": {
    "控制流": [
      {
        "cn": "如果",       // 中文关键字（CNSH）
        "en": "if",         // 英文关键字
        "py": "if",         // Python 目标
        "c": "if",          // C 目标
        "cpp": "if",        // C++ 目标
        "js": "if",         // JavaScript 目标
        "rs": "if",         // Rust 目标
        "swift": "if",      // Swift 目标
        "go": "if",         // Go 目标
        "java": "if",       // Java 目标
        "rb": "if",         // Ruby 目标
        "kt": "if",         // Kotlin 目标
        "bash": "if"        // Bash 目标
      }
    ]
  }
}
```

**字段约定：**
- `cn`: 中文关键字（唯一索引键）
- `en`: 英文映射（通用中间表示）
- `py`/`c`/`cpp`/`js`/`rs`/`swift`/`go`/`java`/`rb`/`kt`/`bash`: 各目标语言映射
- `"—"`: 该目标语言不支持此语法
- `note`: 龍魂专属条目的额外说明（可选字段）

---

## 扩展方式

### 添加新的中文关键字

在 `syntax_library.json` 中对应类别下追加：

```json
{
  "cn": "新关键字",
  "en": "new_keyword",
  "py": "new_keyword",
  "c": "NEW_KEYWORD",
  "cpp": "new_keyword",
  "js": "newKeyword",
  "rs": "new_keyword"
}
```

### 添加新的目标语言

在 `target_languages` 中添加新语言，然后给每个条目的映射补充该语言的翻译。

### 添加新的语法类别

在 `syntax_categories._order` 中添加类别名，然后在 `syntax` 下创建同名数组。

---

## 与现有系统的关系

| 现有文件 | 状态 | 说明 |
|------|:---:|------|
| `03_compiler/mappings/keywords.json` | 🟡 保留 | 历史文件·语法库是超集 |
| `03_compiler/mappings/operators.json` | 🟡 保留 | 历史文件·语法库是超集 |
| `03_compiler/mappings/stdlib.json` | 🟡 保留 | 历史文件·语法库是超集 |
| `CNSH-PROTOCOL.md §3` | ✅ 互补 | 协议文档引用语法库 |
| `CNSH-GATEKEEPER.md §2` | ✅ 互补 | 闸门引用语法库做合规检查 |
| `bin/semantic_parser.py` | ✅ 互补 | 语义解析器引用语法库做命令映射 |
| `L1_内核层/kernel/engines/cnsh_translator_engine.py` | ✅ 互补 | 翻译引擎引用语法库做术语映射 |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-07-08 | 首版·25类·350+条目·20种目标语言·归一总表 |

---

## 验收清单

- [x] 25个语法类别完整覆盖
- [x] 350+条映射条目
- [x] 20种目标语言映射
- [x] 控制流/异常/类/函数/类型/运算符 核心语法完整
- [x] 龍魂19个专属关键字注册
- [x] Apple生态18个关键字
- [x] CSS/HTML/Shell/Git/Docker/SQL/正则/Markdown/JSON 领域语法
- [x] JSON结构规范·可程序化查询
- [x] 只追加·不删除设计
- [x] DNA追溯码绑定

---

```yaml
ROOT_CARD:
  系统: UID9622 龍魂系统
  模块: CNSH 统一语法库
  版本: v1.0
  DNA: "#龍芯⚡️2026-07-08-SYNTAX-LIBRARY-v1.0"
  CONFIRM: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  SEAL: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  GPG: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  Root: "dr=5"
  Wuxing: "土"
  TriColor: "🟢"
  洛书锚点: "宫格5·不动点"
  条目总数: "350+"
  类别总数: 25
  目标语言: 20
  哲学: "只翻译·不破解·MD格式归一·中文编辑可用"
  Conclusion: |
    几百个不同脚本和语法，归一为一个 JSON 总表。
    中文关键字 → 20种目标语言，丢啥查啥，原汁原味。
    不是破解，是翻译。不是封闭，是主权。🐉
```
