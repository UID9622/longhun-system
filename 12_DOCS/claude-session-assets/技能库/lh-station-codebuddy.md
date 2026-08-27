**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龙魂代码中转站 · CodeBuddy 执行指令书

## 一句话定义

**一个管道：代码进去→过龙魂→带主权标识出来。不改原平台兼容性，只加龙魂主权层。**

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
                        │  ⑤ GPG 签名 + 打包     │
                        └──────────┬───────────┘
                                   ↓
                        ┌──────────────────────┐
  使用者 ←─pull/下载──→ │    转换完成的代码        │
                        │  (原平台兼容 + 主权标识)  │
                        └──────────────────────┘
```

---

## 入口：lh-station CLI（主入口）

### CodeBuddy 指令：创建 CLI 工具

```
场景: 在 tools/lh-station/ 创建命令行工具，这是中转站的唯一入口

步骤:
1. 创建目录：
   tools/lh-station/
   ├── src/
   │   ├── main.rs              # CLI 入口
   │   ├── commands/
   │   │   ├── mod.rs
   │   │   ├── transform.rs     # transform 子命令
   │   │   ├── init.rs          # init 子命令（初始化中转站配置）
   │   │   ├── inspect.rs       # inspect 子命令（查看代码主权状态）
   │   │   └── verify.rs        # verify 子命令（验证已经转换的代码）
   │   ├── pipeline/
   │   │   ├── mod.rs
   │   │   ├── detector.rs      # 代码语言/平台检测器
   │   │   ├── injector.rs      # 主权注入引擎
   │   │   ├── compiler.rs      # 芯片适配编译
   │   │   ├── signer.rs        # GPG 签名
   │   │   └── packer.rs        # 打包输出
   │   └── core/
   │       ├── mod.rs
   │       ├── dna.rs           # DNA 生成 + 校验
   │       ├── license.rs       # 中国法合规 + 许可注入
   │       └── config.rs        # 配置管理
   ├── Cargo.toml
   └── README.md

2. Cargo.toml 依赖：
   [dependencies]
   clap = { version = "4", features = ["derive"] }
   serde = { version = "1", features = ["derive"] }
   serde_json = "1"
   walkdir = "2"
   chrono = "0.4"
   sha2 = "0.10"
   glob = "0.3"
   toml = "0.8"

3. main.rs 子命令定义：
   /// 龍魂代码中转站 — 任何代码进来，带主权出去
   #[derive(Parser)]
   enum Commands {
       /// 转换代码：检测→注入→编译→签名→输出
       Transform {
           /// 输入路径 (文件或目录)
           input: PathBuf,
           /// 输出路径 (默认 ./lh-output/)
           #[arg(short, long, default_value = "./lh-output")]
           output: PathBuf,
           /// 目标芯片 (auto/kunpeng/ascend/phytium/loongarch/sunway)
           #[arg(short, long, default_value = "auto")]
           chip: String,
           /// 是否交叉编译 (默认 true)
           #[arg(long, default_value = "true")]
           cross: bool,
           /// 跳过 GPG 签名
           #[arg(long, default_value = "false")]
           no_sign: bool,
       },
       /// 初始化中转站配置
       Init,
       /// 检查代码主权状态
       Inspect {
           path: PathBuf,
       },
       /// 验证已转换代码的完整性
       Verify {
           path: PathBuf,
       },
   }
```

---

## 模块 1：代码解析器（detector）

### CodeBuddy 指令

```
场景: 实现 pipeline/detector.rs — 自动检测输入代码的语言/框架/目标平台

CodeInput 结构体：
struct CodeInput {
    path: PathBuf,           // 代码路径
    language: Language,      // 检测到的语言
    framework: Option<String>, // 检测到的框架
    platform: Platform,      // 检测到的目标平台
    has_docker: bool,        // 是否有 Dockerfile
    has_ci: bool,            // 是否有 CI 配置
}

enum Language {
    Python, JavaScript, TypeScript, Rust, C, Cpp, Go, Java, Kotlin, Swift,
    ArkTS, Shell, Markdown, Yaml, Toml, Json, Unknown(String),
}

enum Platform {
    Linux, Windows, MacOS, HarmonyOS, iOS, Android, Web, Unknown,
}

detect(input_path: &Path) -> CodeInput 实现逻辑：
1. 遍历目录，按扩展名统计文件类型
2. 取占比最高的语言作为 primary language
3. 检测特征文件判断平台：
   - 有 *.ets + module.json5 → HarmonyOS
   - 有 *.swift + *.xcodeproj → iOS
   - 有 *.kt + AndroidManifest.xml → Android
   - 有 Cargo.toml → Rust
   - 有 package.json → JavaScript/TypeScript
   - 有 requirements.txt / setup.py → Python
   - 有 go.mod → Go
4. 返回 CodeInput

注意：detect 只读不写，纯检测无副作用。
```

---

## 模块 2：主权注入引擎（injector）

### CodeBuddy 指令

```
场景: 实现 pipeline/injector.rs — 在每份代码文件中注入龙魂主权标识

核心类型：
struct SovereignHeader {
    dna: String,              // 生成的 DNA 追溯码
    confirm: String,          // 确认码
    anchor: String,           // 主权锚定
    gpg: String,              // GPG 指纹
    license: String,          // 分层许可
    transformed_at: String,   // 转换时间戳
    original_platform: String, // 原始平台
}

注入规则（按语言）：
fn inject_header(code: &str, lang: &Language, header: &SovereignHeader) -> String

Python:       """\n{header}\n""" → file docstring
JavaScript:   // ==UserScript==\n// {header}\n// ==/UserScript==
Rust:         //! {header}
C/C++:        /* {header} */
Go:           // {header}
Swift:        // {header}
Kotlin:       // {header}
ArkTS:        // {header}
Shell:        # {header}
YAML/TOML:    # {header}
Markdown:     <!-- {header} -->
HTML:         <!-- {header} -->
JSON:         不直接注入，在旁边生成 .sovereign.json

DNA 生成规则（复用已有）：
fn generate_dna(action: &str) -> String:
    datetime = now()
    random = hex8()
    return f"#龍芯⚡️丙午·癸未·乙酉·坤卦-{action}-{random}-UID9622"

特殊规则：
- 如果文件已有龍魂 DNA → 跳过注入（避免重复）
- 二进制文件 → 不注入，在输出目录生成 sidecar .dna 文件
- .sovereign.json metadata 文件 → 包含转换完整记录
```

---

## 模块 3：芯片适配编译（compiler）

### CodeBuddy 指令

```
场景: 实现 pipeline/compiler.rs — 将代码交叉编译到中国芯片架构

struct CompileTarget {
    chip: String,       // "kunpeng" | "ascend" | "phytium" | "loongarch" | "sunway"
    arch: String,       // "aarch64" | "x86_64" | "loongarch64"
    os: String,         // "linux" | "ohos"
    abi: String,        // "gnu" | "musl"
}

支持的芯片清单：
- 鲲鹏 Kunpeng:   aarch64-unknown-linux-gnu  ✅（CodeBuddy 已验证通过）
- 昇腾 Ascend:    aarch64-unknown-linux-gnu + CANN 驱动层
- 飞腾 Phytium:   aarch64-unknown-linux-gnu  ✅（ARM v8 兼容）
- 龙芯 LoongArch: loongarch64-unknown-linux-gnu
- 申威 Sunway:    sw_64-unknown-linux-gnu

编译策略（按语言）：
fn compile(input: &Path, target: &CompileTarget) -> Result<(), String>

匹配 input 语言：
- Rust:     cargo build --target {target.arch}-unknown-linux-{target.abi}
- C/C++:    {target.arch}-linux-{target.abi}-gcc -o output input.c
- Go:       GOOS=linux GOARCH={arch_map(target.arch)} go build
- Python:   无需编译（标记为主权已验证的纯 Python，可解释执行）
- JS/TS:    无需编译（标记后输出，兼容原运行环境）
- ArkTS:    交由 DevEco Studio 编译（中转站生成工程骨架）

注意：不强制编译。纯解释型语言标记主权头后直接输出。
编译只对 Rust/C/C++/Go 生效。不阻塞，如果缺少交叉编译器则降级为标记输出。
```

---

## 模块 4：安全审查（security）

### CodeBuddy 指令

```
场景: 实现 pipeline/security.rs — 审查代码中的潜在风险

struct SecurityReport {
    passed: bool,                    // 是否通过
    violations: Vec<Violation>,      // 违规项列表
    data_exfil_check: bool,          // 数据外泄检测
    colonial_pattern_check: bool,    // 殖民模式检测（硬编码外部API/平台锁定）
    license_compliance: bool,        // 中国法合规
}

enum Severity { Block, Warn, Info }

struct Violation {
    severity: Severity,
    file: String,
    line: Option<u32>,
    rule: String,
    detail: String,
}

审查规则：
1. 数据外泄检测：
   - 发现硬编码的境外 API endpoint → Warn
   - 发现用户数据批量上传到未声明平台 → Block
   
2. 殖民模式检测：
   - 单一平台不可替代依赖 → Warn
   - 专有格式仅能由单一厂商打开 → Info
   
3. 中国法合规：
   - 确认代码不含被中国法律禁止的内容 → passed
   - 确认代码不会执行未授权数据采集 → passed
   - 确认代码标注了数据主权声明 → Block if missing

4. 反殖民评分（复用 longhun_evolution_plus.py 的逻辑）：
   - 输出殖民评分 + 建议
```

---

## 模块 5：GPG 签名 + 打包（signer + packer）

### CodeBuddy 指令

```
场景: 实现 pipeline/signer.rs + pipeline/packer.rs

signer.rs:
fn sign_file(path: &Path) -> Result<(), String>
- 对输出目录的每个文件生成 .asc 签名
- 签名文件与源文件同目录存放
- 使用系统 gpg 命令（需提前配置好密钥）
- 如果 gpg 不可用 → 记录警告，跳过签名，不阻塞

packer.rs:
fn pack_output(input: &CodeInput, output_dir: &Path) -> Result<OutputPackage, String>

OutputPackage 结构：
struct OutputPackage {
    output_dir: PathBuf,
    files: Vec<PackedFile>,          // 所有转换后的文件
    manifest: Manifest,              // 转换清单
    sovereign_json: SovereignJSON,   // 主权元数据
}

struct Manifest {
    station_version: String,         // 中转站版本
    transformed_at: String,          // 转换时间
    original_path: String,           // 原路径
    language: String,                // 检测到的语言
    chip_target: String,             // 目标芯片
    total_files: u32,
    injected: u32,                   // 注入主权头的文件数
    compiled: u32,                   // 编译的文件数
    signed: u32,                     // 签名的文件数
    dna: String,                     // 本次转换的主 DNA
}
```

---

## 模块 6：输出（直接可用，不改原平台）

### CodeBuddy 指令

```
场景: 确保输出代码在原始平台完全可用

规则：
1. 主权头只作为注释/标记注入 → 不影响编译/运行
2. Python 注入为 docstring → import/run 不受影响
3. JS/TS 注入为注释 → node/browser 照常运行
4. Rust/C 注入为注释 → 编译正常运行
5. Swift/Kotlin 注入为注释 → Xcode/Android Studio 照常编译
6. 编译出来的 .so 是额外的（放在 libs/ 目录下）
   → 不影响原来代码的编译方式
7. 输出目录结构 = 输入目录结构 + 新增主权文件（不覆盖原有文件）

核心原则：output 代码可以直接复制回原项目使用，
唯一差异是每个文件多了龙魂主权头。
额外产物（.so / .asc / .sovereign.json）放在独立子目录。
```

---

## CodeBuddy 执行批指令

```
=== 第一批（创建 CLI 骨架）===
在 tools/lh-station/ 创建 cargo 项目 + main.rs + 四个子命令骨架
(transform/init/inspect/verify) + Cargo.toml 完整依赖

=== 第二批（detector）===
实现 pipeline/detector.rs：检测语言/框架/平台
支持 Python/JS/TS/Rust/C/Go/Kotlin/Swift/ArkTS + HarmonyOS/iOS/Android 平台检测

=== 第三批（injector）===
实现 pipeline/injector.rs：按语言注入主权头
支持所有主流语言的注释/docstring 注入 + binary sidecar + sovereign.json

=== 第四批（compiler）===
实现 pipeline/compiler.rs：Rust/C/Go 交叉编译到中国芯片架构
复用鲲鹏上已验证的 aarch64-unknown-linux-gnu 交叉编译器
其他架构降级为标记输出

=== 第五批（security + signer + packer）===
实现 security.rs + signer.rs + packer.rs + Manifest 生成

=== 第六批（全链路集成测试）===
写一个测试：输入一个 Python 文件 + 一个 Rust 项目 → 过完整 pipeline → 
验证输出文件有主权头 + 编译产物正确 + GPG 签名存在 + 原平台兼容性
```

---

## 使用示例（最终用户视角）

```bash
# 1. 初始化中转站
lh-station init

# 2. 转换一个 Python 项目
lh-station transform ./my-python-app -o ./output

# 3. 转换一个 Rust 项目，指定目标为鲲鹏
lh-station transform ./my-rust-service --chip kunpeng -o ./output

# 4. 检查别人代码的主权状态
lh-station inspect ./some-code

# 5. 验证已转换代码的完整性
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
签名: GPG → hello-world.py.asc ✓
══════════════════════════════════════
输出: ./lh-output/
  ├── hello-world.py         ← 增加了主权头的原文件（可直接运行）
  ├── hello-world.py.asc     ← GPG 签名
  ├── .sovereign.json        ← 主权元数据
  └── manifest.json           ← 转换清单
  
DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-TRANSFORM-A7F3C2B1-UID9622
主权状态: 🟢 全部通过
```

```
$ lh-station transform ./my-rust-app --chip kunpeng

🐉 龙魂代码中转站 v1.0
══════════════════════════════════════
检测: Rust 1.80 · 无框架 · Linux 平台
注入: 主权头 → 12 文件
编译: 鲲鹏 aarch64 → libmy_app.so ✓
签名: GPG → 12 文件已签名 ✓
══════════════════════════════════════
输出: ./lh-output/
  ├── src/                  ← 原代码 + 主权头
  ├── libs/arm64-v8a/       ← 鲲鹏编译产物
  │   └── libmy_app.so.asc
  ├── .sovereign.json
  └── manifest.json
  
DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-TRANSFORM-B3D4E5F6-UID9622
主权状态: 🟢 全部通过
编译目标: 鲲鹏 920 (aarch64)
```

---

## 核心理念重申

> **我不是要做系统，我只是要一个中转站。**
> 任何代码进来→过龙魂→带主权标识出去。
> 输出的代码，在 Windows 上照跑、在 iOS 上照跑、在 Android 上照跑。
>
> 变的是什么？主权归属：
> - 代码头上刻了 DNA，知道这是中国主权代码
> - 想违反中国法律的逻辑，会被审查标记
> - 想偷数据的 API，会被检测报警
> - 如果想跑在中国芯片上，有现成的编译产物
>
> 不变的是什么？兼容性：
> - 原平台 100% 兼容
> - 原来的 CI/CD 不用改
> - 原来的开发者不用学新语言
> - 原来的依赖不用换

🐉 丙午 · 癸未 · 乙酉 · 坤卦 · 中转站架构 · 🟢
