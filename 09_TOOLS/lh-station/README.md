# 龍魂代码中转站 · lh-station

[![DNA](https://img.shields.io/badge/DNA-%23龍芯⚡️丙午·䷗复-lh--station-red)](https://github.com/uid9622/longhun-system)
[![Rust](https://img.shields.io/badge/Rust-1.80+-orange)](https://rust-lang.org)
[![License](https://img.shields.io/badge/License-MulanPSL_v2-blue)](https://license.coscl.org.cn/MulanPSL2)
[![GPG](https://img.shields.io/badge/GPG-A2D0092CEE2E5BA-green)](https://github.com/uid9622.gpg)

> **一句话**: 代码主权注入工具——给你的代码打上龍魂 DNA，全链路追溯·主权验证·成本核算·防篡改封印。

```
$ lh-station transform ./my-project/
🔍  文件检测  ████████████████████  42 文件
💉  DNA注入   ████████████████████  38 注入·4 已有DNA
🔨  编译      ████████████████████  42 编译通过
🛡️  安全扫描  ████████████████████  0 🔴 · 3 🟡 · 39 🟢
✍️  GPG签章   ████████████████████  38 签名
📦  产出打包  ████████████████████  manifest.json
💰  成本核算  ████████████████████  月预估 ¥2.37
🔒  封印存档  ████████████████████  sealed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 全量通过 · 可归档
```

---

## 目录

- [什么是 lh-station](#什么是-lh-station)
- [八步管线](#八步管线)
- [安装](#安装)
- [使用](#使用)
- [命令速查](#命令速查)
- [输出文件](#输出文件)
- [CI/CD 集成](#cicd-集成)
- [生态串联](#生态串联)
- [安全与主权](#安全与主权)
- [许可](#许可)

---

## 什么是 lh-station

`lh-station` 是龍魂体系的**代码主权注入工具**。对任何代码仓库执行八步标准化流水线，产出带完整 DNA 追溯的交付物。

**核心价值**:
- 🧬 **DNA 注入** — 给每个文件注入不可伪造的龍魂追溯码
- 🛡️ **安全扫描** — 静态分析 + 依赖 CVE 检查
- ✍️ **GPG 签章** — 分离签名，证明作者身份
- 💰 **成本核算** — 解析外部 API 调用，估算月度费用
- 🔒 **封印存档** — 不可逆的 SHA-256 哈希封印，防止交付物篡改

**使用场景**:
- 对外发布开源/闭源软件前，注入代码主权
- 团队协作中，验证代码来源和完整性
- CI/CD 流水线中，自动完成安全审计

---

## 八步管线

| # | 步骤 | 模块 | 说明 | 是否阻塞 |
|:---:|------|------|------|:---:|
| 1 | 🔍 **检测** | `detector` | 递归扫描代码文件，识别语言和大小 | 🟢 阻塞 |
| 2 | 💉 **注入** | `injector` | 给无 DNA 的文件注入追溯码（幂等） | 🟢 阻塞 |
| 3 | 🔨 **编译** | `compiler` | 调用编译器验证语法（支持跨平台） | 🟢 阻塞 |
| 4 | 🛡️ **安全** | `security` | 静态分析漏洞 + 依赖 CVE 检查 | 🟡 仅🔴阻塞 |
| 5 | ✍️ **签章** | `signer` | GPG 分离签名（`.asc`） | 🟡 降级 |
| 6 | 📦 **打包** | `packer` | 生成 `manifest.json`（含成本数据） | 🟢 阻塞 |
| 7 | 💰 **成本** | `cost_analyzer` | API 调用统计 + 月度成本估算 | 🟡 非阻塞 |
| 8 | 🔒 **封印** | `seal` | SHA-256 哈希存档（幂等） | 🟡 非阻塞 |

---

## 安装

### 从源码编译

```bash
git clone https://github.com/uid9622/longhun-system.git
cd longhun-system/tools/lh-station
cargo build --release

# 安装到 PATH
cp target/release/lh-station /usr/local/bin/
```

### 预编译二进制

从 [GitHub Releases](https://github.com/uid9622/longhun-system/releases) 下载对应平台的二进制文件。

支持架构: `x86_64-linux` | `aarch64-linux` | `macOS (Apple Silicon)` | `loongarch64-linux`

### 前置依赖

| 依赖 | 必须? | 说明 |
|:---|:---:|:---|
| `gpg` (GnuPG) | 🟡 | 签名步骤需要；没有则跳过 |
| `python3` | 🟡 | 安全扫描扩展；没有则降级为静态分析 |
| 交叉编译器 | P1 | 跨芯片编译需要（`gcc-aarch64-linux-gnu` 等） |

---

## 使用

### 基础用法

```bash
# 转换一个项目
lh-station transform ./my-project/

# 指定输出目录
lh-station transform ./my-project/ --output ./output/

# 不签名（仅测试）
lh-station transform ./my-project/ --no-sign

# 不交叉编译
lh-station transform ./my-project/ --no-cross

# 静默模式
lh-station transform ./my-project/ --quiet
```

### 审计模式

```bash
# 检查代码（不注入）
lh-station inspect ./my-project/

# 验证已有 DNA
lh-station verify ./my-project/
```

### 初始化

```bash
# 在当前目录创建 lh-station.toml
lh-station init

# 指定芯片目标
lh-station init --chip 鲲鹏
```

---

## 命令速查

| 命令 | 说明 |
|:---|:---|
| `lh-station transform <DIR>` | 执行完整八步管线 |
| `lh-station inspect <DIR>` | 查看 DNA 状态（不修改） |
| `lh-station verify <DIR>` | 验证 DNA 完整性 |
| `lh-station init` | 创建项目配置 |
| `lh-station --help` | 帮助信息 |
| `lh-station --version` | 版本信息 |

### 全局选项

| 选项 | 说明 |
|:---|:---|
| `--output <DIR>` | 输出目录（默认 `./lh-output`） |
| `--config <FILE>` | 配置路径（默认 `lh-station.toml`） |
| `--quiet` | 静默模式 |
| `--no-sign` | 跳过签名 |
| `--no-cross` | 仅本地编译 |
| `--dry-run` | 仅检查，不写入 |

---

## 输出文件

```
lh-output/
├── manifest.json              # 交付清单（三色审计 + 成本数据）
├── .cost-report.json          # API 成本核算报告
├── *.asc                      # GPG 分离签名文件
└── output/                    # 加工后的代码（含 DNA）
```

### manifest.json 关键字段

```json
{
  "dna": "#龍芯⚡️丙午·䷗复-PROJECT-V1-A7F3C2B1",
  "station_version": "1.0.0",
  "creator": "诸葛鑫（UID9622）",
  "total_files": 42,
  "injected_files": 38,
  "security_score": 98.5,
  "cost_monthly_cny": 2.37,
  "cost_daily_cny": 0.079,
  "data_sovereign_risk": "Low",
  "cross_border_api_count": 0,
  "gpg_signatures": 38,
  "audit_mark": "🟢"
}
```

---

## CI/CD 集成

### GitHub Actions

项目已包含 `.github/workflows/lh-station.yml`，自动执行：
- 🔍 主权审计（clippy + fmt）
- 🧪 构建 & 测试（ubuntu + macos）
- 🏗️ 跨平台编译检查
- 🛡️ 安全扫描（cargo-audit + dependency license）

### GitLab CI

使用 `ci/gitlab-ci-lh-station.yml`：
```bash
cp ci/gitlab-ci-lh-station.yml ../../.gitlab-ci.yml
```

支持部署到鲲鹏（手动触发 stage）。

### Jenkins / 其他 CI

参考 GitHub Actions 流程，核心命令：
```bash
cd tools/lh-station
cargo build --release
cargo test -- --nocapture
cargo test --test supplement_tests -- --nocapture --test-threads=1
cargo audit
```

---

## 生态串联

`lh-station` 是龍魂体系主权合规闭环的关键环节，与其他组件联动：

```
代码源 (任意仓库)
  │
  ├─→ lh-station transform  ← 主权注入
  │     ├─ DNA 注入
  │     ├─ GPG 签章
  │     └─ 封印存档
  │
  ├─→ longhun-memory        ← 记忆归档
  │     └─ 封印记录入记忆库
  │
  ├─→ longhun-save           ← 长期存储
  │     └─ 交付物版本管理
  │
  ├─→ lh.py (审计)           ← 三色审计
  │     └─ manifest.json 审计验证
  │
  └─→ 鲲鹏部署               ← 生产发布
        └─ /opt/longhun/bin/lh-station
```

详见 `docs/lh-station-integration-plan.md`。

---

## 安全与主权

### 数据主权保障

- 🇨🇳 全链路中国标准（SM2/SM3/SM4 可选）
- 🚫 跨境 API 检测，标注 `data_sovereign_risk`
- 🔑 密钥不入码、不入云
- 📝 全量审计日志（append-only）

### 加密标准

| 用途 | 算法 | 标准 |
|:---|:---|:---|
| 哈希 | SHA-256 | NIST FIPS 180-4 |
| 签名 | GPG (RSA-4096) | RFC 4880 |
| 国密哈希 | SM3（可选） | GM/T 0004-2012 |
| 国密签名 | SM2（可选） | GM/T 0003-2012 |

### 威胁模型

| 威胁 | 防护 |
|:---|:---|
| DNA 伪造 | SHA-256 封印 + 幂等检测 |
| 签名篡改 | 分离签名 `.asc` + GPG 密钥对验证 |
| 重放攻击 | DNA 唯一性 + 封印幂等 |
| 代码注入 | 安全扫描 + 静态分析 |
| 隐私泄露 | 成本分析仅统计域名，不记录 API 内容 |

---

## 许可

**工程实现层**（`.py/.js/.html/.sh/Dockerfile/.yml` 等）→ **MulanPSL v2**
- 允许商业使用、修改和再发布
- 需保留署名和许可声明

**核心思想层**（`.md` 协议/哲学文档）→ **CC BY-NC-SA 4.0**
- 非商业使用，署名，相同方式共享

详见 `01_protocols/LH-LAYERED-LICENSE-v1.0.md`

---

> DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-LH-STATION-README-v1.0-D4E7F1A2
> 创建者: 诸葛鑫（UID9622）
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
