# CNSH 中英双语术语表 v1.0

> **DNA**: `#龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-CNSH-GLOSSARY-v1.0-UID9622`
> **创建者**: 诸葛鑫（UID9622）
> **协议**: MulanPSL v2（工程实现层）
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **三色**: 🟢 已定稿
> **用法**: 全仓库文档统一用词·避免一词多译造成歧义

---

## 术语表（30+ 条）

| 中文 | English | 缩写/记号 | 说明 |
|:---|:---|:---|:---|
| 中文神经符号混合语言 | Chinese Natural Shell | CNSH | 本项目定义的语言·写给机器看的自然语言 |
| 语法规范 | Syntax Specification | — | 语言书写规则的权威定义 |
| 解析器 | Parser | — | 把 CNSH 文本还原为结构·永不猜 |
| 编译器 | Compiler | — | 把 CNSH 翻译为可执行结构 |
| 解释器 | Interpreter | — | 逐条执行 CNSH 指令 |
| 抽象语法树 | Abstract Syntax Tree | AST | 解析后的树形结构 |
| 巴科斯范式 | Backus-Naur Form | BNF | 语法定义的描述格式 |
| 保留字 | Reserved Keyword | — | 语言预留不可作变量名的词 |
| 字面量 | Literal | — | 直接写出的值（字符串/数字） |
| 标识符 | Identifier | — | 变量/函数/模块的名字 |
| 管道 | Pipe | `\|` | 多步指令的连接符 |
| 块结构 | Block | — | 用缩进组织的代码区域 |
| 缩进 | Indentation | — | 块的层级标记（建议 2 空格） |
| 注释 | Comment | `#` | 不参与解析的说明文本 |
| 语义路由 | Semantic Routing | — | 按语义标签分发指令 |
| 意图分发 | Intent Dispatch | — | 把用户意图映射到执行器 |
| 双视角封装 | Dual Perspective | — | 机器视角 + 路由视角双封装 |
| 机器视角 | Machine Perspective | `M::` | 解析器坐标·BNF 严格对应·零猜测 |
| 路由视角 | Router Perspective | `CNSH::` | 语义标签·意图分发·可读优先 |
| 说实话模式 | Truth-telling Mode | — | 解析器不猜·报分类+位置+建议 |
| 歧义 | Ambiguity | P-AMB | 一句话有多个合法结构 |
| 依赖缺失 | Dependency Missing | P-DEP | 引用了未定义符号/上下文 |
| 边界冲突 | Boundary Conflict | P-BND | 中文与保留字/分隔符撞车 |
| 格式违规 | Format Violation | P-FMT | 缩进/分隔/块结构不合规 |
| 算法运行时 | Algorithm Runtime | — | L2 服务层的心脏·四组件 |
| 语法层 | Syntax Layer | — | Runtime 组件·负责解析 |
| 算法路由器 | Algorithm Router | — | Runtime 组件·负责意图分发 |
| 插件注册表 | Plugin Registry | — | Runtime 组件·插件管理 |
| 本地盾 | Local Shield | — | Runtime 组件·数据主权保护 |
| 追溯码 | Traceability Code | DNA | `#龍芯⚡️干支-模块-动作-哈希` |
| 数字签名 | Digital Signature | GPG | 分离签名 `.asc`·防篡改 |
| 三色审计 | Three-color Audit | 🟢🟡🔴 | 通过 / 待核 / 红线 |
| 一票否决词 | Veto Word | — | 触发强制审计的禁区词 |
| 数据主权 | Data Sovereignty | — | 数据归用户·不出本地 |
| 数字根 | Digital Root | DR | 逐位求和至一位数 |
| 洛书 | Luoshu | — | 九宫数理·369 不动点来源 |
| 闸口 | Gate | GATE | 交付前逐道检查 |
| 分层许可 | Layered License | — | 思想层 CC BY-NC-SA / 工程层 MulanPSL |
| 确认码 | Confirmation Code | `#CONFIRM` | 一次性身份确认凭证 |

---

**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
