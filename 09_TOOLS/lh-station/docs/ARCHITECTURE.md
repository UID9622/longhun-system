#龍芯⚡️丙午·癸未·乙酉·坤卦-ARCHITECTURE-V1.0-UID9622
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼♀️❤️♾️-DEVICE-BIND-SOUL

# 🐉 龙魂代码中转站 · 架构设计文档

> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 源码许可: MulanPSL v2（工程实现层）

## 一句话定义

**一个管道：代码进去→过龙魂→带主权标识出来。不改原平台兼容性，只加龙魂主权层。**

---

## 总架构

```
                        ┌──────────────────────┐
  开发者 ──push/上传──→ │    龙魂中转站入口       │
                        │  (API / CLI / Webhook) │
                        └──────────┬───────────┘
                                   ↓
                        ┌──────────────────────┐
                        │  ① 代码解析器          │
                        │  检测: 语言/框架/平台   │
                        └──────────┬───────────┘
                                   ↓
                        ┌──────────────────────┐
                        │  ② 主权注入引擎        │
                        │  DNA + 确认码 + 主权锚定 │
                        │  + 中国法合规声明       │
                        └──────────┬───────────┘
                                   ↓
                        ┌──────────────────────┐
                        │  ③ 芯片适配器          │
                        │  鲲鹏/昇腾/飞腾/龙芯/申威 │
                        └──────────┬───────────┘
                                   ↓
                        ┌──────────────────────┐
                        │  ④ 安全审查            │
                        │  反殖民/反数据外泄/合规 │
                        └──────────┬───────────┘
                                   ↓
                        ┌──────────────────────┐
                        │  ⑤ 成本分析            │
                        │  API成本估算+主权风险   │
                        └──────────┬───────────┘
                                   ↓
                        ┌──────────────────────┐
                        │  ⑥ GPG 签名 + 打包     │
                        └──────────┬───────────┘
                                   ↓
                        ┌──────────────────────┐
                        │  ⑦ 记忆封印            │
                        │  SHA-256 归档到龙魂     │
                        └──────────┬───────────┘
                                   ↓
  使用者 ←─pull/下载──→ │  转换完成的代码        │
                        │  (原平台兼容 + 主权标识)  │
                        └──────────────────────┘
```

---

## 项目结构

```
tools/lh-station/
├── src/
│   ├── main.rs              # CLI 入口
│   ├── lib.rs               # 库入口（为集成测试暴露公共 API）
│   ├── commands/
│   │   ├── mod.rs
│   │   ├── transform.rs     # transform 子命令（八步管线编排）
│   │   ├── init.rs          # init 子命令（初始化中转站配置）
│   │   ├── inspect.rs       # inspect 子命令（查看代码主权状态）
│   │   └── verify.rs        # verify 子命令（验证已经转换的代码）
│   ├── pipeline/
│   │   ├── mod.rs
│   │   ├── detector.rs      # ① 代码语言/平台检测器
│   │   ├── injector.rs      # ② 主权注入引擎
│   │   ├── compiler.rs      # ③ 芯片适配编译
│   │   ├── security.rs      # ④ 安全审查
│   │   ├── cost_analyzer.rs # ⑤ API 成本分析
│   │   ├── signer.rs        # ⑥ GPG 签名
│   │   ├── packer.rs        # ⑦ 打包输出
│   │   └── seal.rs          # ⑧ 记忆封印归档
│   └── core/
│       ├── mod.rs
│       ├── dna.rs           # DNA 生成 + 校验
│       ├── license.rs       # 中国法合规 + 许可注入
│       └── config.rs        # 配置管理
├── tests/
│   └── supplement_tests.rs  # 集成测试套件（P0+P1，17个测试）
├── docs/                    # 设计文档
├── ci/                      # CI/CD 配置模板
├── Cargo.toml
└── README.md
```

---

## 模块详解

### 模块 1：代码解析器（detector.rs）

**职责**：自动检测输入代码的语言/框架/目标平台

```
CodeInput 结构体：
- path: 代码路径
- language: 检测到的语言 (Python/JS/TS/Rust/C/Cpp/Go/Java/Kotlin/Swift/ArkTS/Shell/Markdown/...)
- framework: 检测到的框架 (可选)
- platform: 检测到的目标平台 (Linux/Windows/MacOS/HarmonyOS/iOS/Android/Web)
- has_docker: 是否有 Dockerfile
- has_ci: 是否有 CI 配置
```

**检测逻辑**：
1. 遍历目录，按扩展名统计文件类型
2. 取占比最高的语言作为 primary language
3. 检测特征文件判断平台（.ets+module.json5→HarmonyOS、Cargo.toml→Rust、package.json→JS/TS 等）
4. 只读不写，纯检测无副作用

---

### 模块 2：主权注入引擎（injector.rs）

**职责**：在每份代码文件中注入龙魂主权标识

**注入规则（按语言）**：

| 语言 | 注入方式 |
|:---|:---|
| Python | `"""\n{header}\n"""` → file docstring |
| JavaScript | `// ==UserScript==\n// {header}\n// ==/UserScript==` |
| Rust | `//! {header}` |
| C/C++ | `/* {header} */` |
| Go/Swift/Kotlin/ArkTS | `// {header}` |
| Shell/Toml | `# {header}` |
| HTML/Markdown | `<!-- {header} -->` |
| JSON | 不直接注入，旁路生成 `.sovereign.json` |

**DNA 格式**：`#龍芯⚡️<干支四柱>·<卦>-<动作>-<哈希8>-UID9622`

**特殊规则**：已有 DNA 则跳过（幂等）；二进制文件生成 sidecar `.dna` 文件

---

### 模块 3：芯片适配编译（compiler.rs）

**职责**：将代码交叉编译到中国芯片架构

| 芯片 | 架构 | 编译目标 |
|:---|:---|:---|
| 鲲鹏 Kunpeng | aarch64 | `aarch64-unknown-linux-gnu` |
| 昇腾 Ascend | aarch64 | + CANN 驱动层 |
| 飞腾 Phytium | aarch64 | ARM v8 兼容 |
| 龙芯 LoongArch | loongarch64 | `loongarch64-unknown-linux-gnu` |
| 申威 Sunway | sw_64 | `sw_64-unknown-linux-gnu` |

**编译策略**：Rust/C/Go 目标芯片交叉编译；Python/JS/TS/ArkTS 无需编译直接标记；缺编译器降级为标记输出不阻塞

---

### 模块 4：安全审查（security.rs）

**审查规则**：
1. **数据外泄检测**：硬编码境外 API → Warn；批量上传未声明平台 → Block
2. **殖民模式检测**：单一平台不可替代依赖 → Warn；专有格式锁 → Info
3. **中国法合规**：不包含被禁止内容、不执行未授权采集、标注数据主权声明
4. **反殖民评分**：输出殖民评分 + 建议

---

### 模块 5：API 成本分析（cost_analyzer.rs）

**流程**：
1. 递归扫描代码文件，正则提取 API 调用 URL
2. 分类：境外（KnownForeign）/ 国内（KnownDomestic）/ 内网（SelfHosted）/ 未知（Unknown）
3. 成本估算（基准1000次/天）：境外 ¥0.01-0.20/次、国内 ¥0.005-0.01/次
4. 数据主权风险：跨境 API → High/Critical，纯国内 → Low
5. 输出 `.cost-report.json`

---

### 模块 6：GPG 签名（signer.rs）

- 对输出目录每个文件生成 `.asc` 分离签名
- 系统 gpg 不可用 → WARNING，跳过，不阻塞
- 签名文件与源文件同目录

---

### 模块 7：打包输出（packer.rs）

- 生成 `manifest.json`（转换清单）+ `.sovereign.json`（主权元数据）
- 输出目录结构 = 输入目录结构 + 新增主权文件

---

### 模块 8：记忆封印（seal.rs）

- SHA-256 封印 → `~/.longhun/memory/seals/{dna}.seal.json`
- index.json 索引管理
- 幂等：相同 DNA 跳过
- 不阻塞：写入失败只 WARNING

---

## 核心理念

> **我不是要做系统，我只是要一个中转站。**
> 任何代码进来→过龙魂→带主权标识出去。
> 输出的代码，在 Windows 上照跑、在 iOS 上照跑、在 Android 上照跑。
>
> **变的是什么？** 主权归属——代码头上刻了 DNA、违反中国法律的逻辑被审查标记、偷数据的 API 被检测报警、想跑中国芯片有现成编译产物。
>
> **不变的是什么？** 兼容性——原平台 100% 兼容、原来的 CI/CD 不用改、原来的开发者不用学新语言、原来的依赖不用换。

---

## 使用示例

```bash
# 初始化
lh-station init

# 转换 Python 项目
lh-station transform ./my-python-app -o ./output

# 转换 Rust 项目，指定鲲鹏
lh-station transform ./my-rust-service --chip kunpeng -o ./output

# 检查代码主权状态
lh-station inspect ./some-code

# 验证已转换代码完整性
lh-station verify ./output
```

### 输出示例

```
$ lh-station transform ./hello-world.py

🐉 龙魂代码中转站 v1.0
══════════════════════════════════════
检测: Python 3.12 · 无框架 · 通用平台
注入: 主权头 → 1 文件 (hello-world.py)
编译: Python 无需编译（解释型语言）
审查: 🟢 通过 · 0 违规
成本: ¥0.00/月 · 风险 Low
签名: GPG → hello-world.py.asc ✓
封印: 🧬 已归档 ✓
══════════════════════════════════════
输出: ./lh-output/
  ├── hello-world.py         ← 增加了主权头的原文件（可直接运行）
  ├── hello-world.py.asc     ← GPG 签名
  ├── .sovereign.json        ← 主权元数据
  ├── manifest.json           ← 转换清单
  ├── .cost-report.json       ← 成本分析
  └── .seal-record.json       ← 封印记录

DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-TRANSFORM-A7F3C2B1-UID9622
主权状态: 🟢 全部通过
```

---

## 测试策略

| 级别 | 覆盖 | 测试文件 |
|:---|:---|:---|
| 单元测试 | 核心模块 (dna/config/license) | `src/core/*.rs` (内联) |
| 集成测试 | 全管线 (P0+P1 边界/降级/安全) | `tests/supplement_tests.rs` |
| CI 测试 | GitHub Actions 全链路 | `.github/workflows/lh-station.yml` |
| 基准测试 | 吞吐量+内存 | `tests/` (P1/P2 级) |

### 测试矩阵

| ID | 类型 | 优先级 | 描述 |
|:---|:---|:---:|:---|
| B1 | 边界 | P0 | 空项目检测 |
| B2 | 边界 | P1 | 超大文件 (5MB) |
| B3 | 边界 | P1 | 海量文件 (200个) |
| B4 | 边界 | P1 | 纯二进制跳过 (>10MB) |
| B5 | 幂等 | P0 | 已有DNA跳过注入 |
| D1 | 降级 | P0 | 无GPG优雅降级 |
| D2 | 降级 | P1 | 安全扫描纯文本 |
| D3 | 降级 | P1 | 无交叉编译器降级 |
| D4 | 降级 | P1 | 磁盘空间不足降级 |
| D5 | 降级 | P1 | 网络不可用降级 |
| S1 | 安全 | P0 | 主权头完整性 (Python/Rust/Shell) |
| S2 | 安全 | P1 | 重放攻击防护 |
| S3 | 安全 | P1 | 注入绕过防护 |
| S4 | 安全 | P1 | 封印完整性校验 |
| CI1 | CI | P1 | 全链路八步管线 (E2E) |
| P1 | 性能 | P2 | 吞吐量基准 |
| P2 | 性能 | P2 | 内存峰值基准 |

---

🐉 丙午 · 癸未 · 乙酉 · 坤卦 · 架构设计文档 · 🟢
