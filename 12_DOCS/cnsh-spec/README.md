# CNSH · 中文结构化 AI 交互语法规范

> **CNSH（Chinese Natural Shell）** 是一种面向人机协作的中文结构化语法，兼具自然语言可读性与机器可解析性，覆盖 **AI 指令 · 审计追溯 · 脚本执行** 三个层次。

---

## 目录

- [INDEX.md](./INDEX.md) — 完整目录索引
- [intro/](./intro/) — 入门篇（第 0-3 章）
- [reference/](./reference/) — 语法参考（第 4-8 章）
- [audit/](./audit/) — 审计层（第 9-12 章）
- [shell/](./shell/) — 执行层（第 13-16 章）
- [appendix/](./appendix/) — 附录（A-D）
- [examples/](./examples/) — 示例代码
- [spec/](./spec/) — 机器可读规范（JSON Schema / BNF / 关键字）

---

## 一句话

> 会写中文句子，就能与 AI 协作编程。

## 三条铁律

1. **中文第一**：关键字、语法、错误信息全部中文
2. **可追溯**：每行代码可绑定 DNA 追溯码
3. **可执行**：结构化解析，可编译为 Python / Shell

## 快速上手

```cnsh
# 第一个 CNSH 程序
输出 "Hello, 龍魂"
DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-HELLO
确认: ✅
```

---

## 与龙魂体系的关系

| 文档 | 层级 | 说明 |
|------|------|------|
| 本仓库 | CNSH 公开语法规范 v1.0 | 人机协作语法 · 面向社区发布 |
| `CNSH-v3.1-OPTIMIZED-v2.1-enhanced.md` | 内部论文 | 数学语义液压（EUV 语境）· 底层算法 |
| `CNSH_命令与变量命名规范-v2.0.md` | 内部规范 | `lh6`/`lh` 命令 · 变量二元体系 · 八卦分类 |
| `LH-SYNTAX-SPEC-v3.0.md` | P0 协议 | DNA/确认码/缩进/三色/GPG 全系统语法标准 |

> 命名说明：`CNSH` 全称在不同语境下取不同扩展——人机交互层为 **Natural Shell**（本仓库），数学语义层为 **Native Semantic Hydraulics**（内部论文）。两者同属 CNSH 体系，前者是后者的对外语法呈现。

---

## 设计原则

1. **中文第一**：关键字、语法、错误信息全部中文
2. **机器可读**：结构化解析，不依赖语义理解
3. **可追溯**：每行代码可绑定 DNA
4. **零门槛**：会写中文的人 10 分钟上手

## 核心特性

### 1. 中文自然语序
```cnsh
宝宝 输出 "Hello, 龍魂"
系统 审计 本次操作 用三色判定
```

### 2. DNA 追溯
```cnsh
#龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-申时-CNSH-SPEC-CREATE-v1.0-UID9622-A7B8C9D0
```

### 3. 三色审计
```cnsh
审计 当前状态 → 🟢 通过 / 🟡 待审 / 🔴 拒绝
```

### 4. P0 熔断
```cnsh
熔断条件: P0铁律被触发 → 立即停止执行
```

---

## 快速导航

| 场景 | 去哪 |
|------|------|
| 第一次接触 | [第0章：CNSH是什么](./intro/00_what_is_cnsh.md) |
| 想立刻跑起来 | [第1章：Hello, 龍魂](./intro/01_hello_longhun.md) |
| 查语法规则 | [第5章：指令结构](./reference/05_command_structure.md) |
| 查 DNA 格式 | [第9章：DNA语法规范](./audit/09_dna_syntax.md) |
| 查保留关键字 | [附录A](./appendix/A_reserved_keywords.md) |
| 机器可读定义 | [spec/cnsh_schema.json](./spec/cnsh_schema.json) |

---

## 许可证

**CC BY-NC-SA 4.0 + Longhun DNA Inheritance Clause**

本仓库为龍魂体系**思想层**产出，采用知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议。
附加条款：任何派生作品必须保留 DNA 追溯链和原始创作者署名。

**DNA**: `#龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-CNSH-SPEC-v1.0`
**创建者**: 诸葛鑫（UID9622）
**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
