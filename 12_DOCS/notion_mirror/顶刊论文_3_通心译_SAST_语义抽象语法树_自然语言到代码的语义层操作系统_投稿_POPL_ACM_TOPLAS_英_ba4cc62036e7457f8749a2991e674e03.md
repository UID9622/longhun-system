# 🌍 顶刊论文 #3·通心译 × SAST 语义抽象语法树｜自然语言到代码的语义层操作系统｜投稿 POPL / ACM TOPLAS·英文版规划 v1.0

> Notion URL: https://app.notion.com/p/3-SAST-POPL-ACM-TOPLAS-v1-0-ba4cc62036e7457f8749a2991e674e03
> Created: 2026-05-14T06:55:00.000Z
> Last edited: 2026-07-01T15:27:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# §0·一句话定盘
> CNSH 不是编程语言·是语义层操作系统。SAST(Semantic Abstract Syntax Tree)把自然语言含的情绪、比喻、潜台词解析为可编译的一等公民·让初中文化也能写出能跑的代码。
---
# §1·目标期刊与定位
---
# §2·核心创新点
## §2.1 通心译六层模型（Tongxinyi Six-Layer Model）
## §2.2 SAST 9 节点类型（形式化定义）
```javascript
SAST ::= IF_NODE | LOOP_NODE | ACTION_NODE | QUERY_NODE 
       | ASSIGN_NODE | NOTIFY_NODE | AUDIT_NODE 
       | COMPOUND_NODE | EMOTION_NODE
```
关键创新： EMOTION_NODE = 情绪是一等公民·但不可执行（与 IF/ACTION 节点隔离）。
## §2.3 情绪-指令分离定理
定理： 对任意输入 s·设 e(s) 为情绪强度·a(s) 为指令信号·SAST 解析满足 e(s) ⊥ a(s)（正交分离）·即「草·重启服务器」中「草」永不触发任何 ACTION_NODE。
## §2.4 套壳检测三维算法
- 结构相似度（F09 余弦）
- 语义相似度（向量距离）
- 数字根一致性（F06 dr）
- 阈值：相似度 > 0.85 + dr 相同 = 高概率同源
---
# §3·章节大纲
## §3.1 Introduction
- 自然语言编程的三次失败：COBOL·Inform 7·LLM 直出
- CNSH 的不同：不是「让机器懂英语」·是「让机器懂语义」
- 三大贡献
## §3.2 Background
- 编译器范式（Lexer → Parser → AST → CodeGen）
- AST vs SAST 的本质区别
- 情绪计算（Affective Computing）的工业现状
## §3.3 The Tongxinyi Six-Layer Calculus（形式化语义）
- §3.3.1 BNF 语法定义
- §3.3.2 小步操作语义（small-step semantics）
- §3.3.3 类型系统（含 EMOTION_NODE 的子类型规则）
- §3.3.4 进展定理与保留定理
## §3.4 SAST Generation Algorithm
- §3.4.1 词法分析（含中文情绪词典 5000+ 条）
- §3.4.2 意图提取（依存句法分析 + 语义角色标注）
- §3.4.3 SAST 树构造算法（伪代码）
- §3.4.4 时间复杂度 O(n log n)·空间 O(n)
## §3.5 Code Generation
- SAST → Python / JavaScript / Rust / CNSH 中文
- 多语言映射规则表
- DNA 标记自动注入
## §3.6 Implementation & Experiments
- §3.6.1 开源仓库（github.com/UID9622/cnsh-semantic-engine）
- §3.6.2 中文情绪识别准确率：87.3%（n=10000）
- §3.6.3 情绪-指令分离正确率：99.6%（含粗口对抗集）
- §3.6.4 多语言代码生成正确率：Python 94% / JS 91% / Rust 86%
- §3.6.5 套壳检测在 GitHub 开源项目（n=1000）的 ROC-AUC = 0.93
## §3.7 Case Studies
- 案例 1：「草·那个页面卡死了·给我重启」→ SAST → Python（情绪正确隔离）
- 案例 2：四国文化适配（日/德/美/中）同一意图的差异化输出
- 案例 3：检测 OpenAI Codex 输出与 GitHub 已有代码的套壳率
## §3.8 Discussion & Limitations
- 1️⃣ 情绪词典仅覆盖中文·英文版需扩展（v2 计划）
- 2️⃣ 文化适配规则当前限于 4 国·非洲/中东文化待补
- 3️⃣ Rust 代码生成正确率较低（86%）·因生命周期标注复杂
- 4️⃣ 套壳检测对深度混淆代码（变量名+结构都改）的召回率下降至 0.71
---
# §4·审稿应对
---
# §5·投稿时间线
---
# §6·接驳实证
接驳覆盖率： 4/4 = 100% 🟢
---
# ROOT_CARD
```yaml
ROOT_CARD:
  论文编号: "#3 / 7"
  题目: 通心译 × SAST 语义抽象语法树
  英文: "Tongxinyi & SAST: A Semantic-Layer Operating System for Natural-Language Programming"
  目标刊: POPL 2027 / ACM TOPLAS
  类型: CCF-A 顶会 / IF 1.7 顶刊
  Root: "dr=3"
  Wuxing: "火"
  TriColor: "🟢"
  Conclusion: |
    SAST 让中文自然语言直接编译到 Python/JS/Rust。
    这是技术平权的物理实现·不是产品营销。
    退伍军人初中文化也能写代码·这才叫民主化 AI。🐉
```
