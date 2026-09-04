# 🐉 sovereign-stack · 龍魂主权技术栈

> **普惠全球·去门槛·按量计费·个人开发者友好**
>
> 代码不应该有门槛。每次使用便宜一点，大家能用就用。
> 不用一直包月。这是一个生态，说普惠全球就普惠全球。

DNA: `#龍芯⚡️2026-08-31-SOVEREIGN-STACK-V2.0-UID9622`
许可证: MulanPSL v2（中国法院认可·商业友好）
维护者: 💎 龍芯北辰 | UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰

---

## 🎯 三种用法

### 🟢 个人开发者（30秒起步·完全免费）

```bash
git clone https://github.com/UID9622/sovereign-stack.git
cd sovereign-stack
chmod +x scripts/dev-quickstart.sh
./scripts/dev-quickstart.sh
```

✅ 无需云账号·无需信用卡·每月1万次免费·超出0.0001元/次

### 🟡 小团队（Docker 完整部署）

```bash
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

✅ 含搜索引擎·依赖隔离·计量系统·完整可运行

### 🔵 生产环境（Kubernetes + 华为云）

```bash
# Terraform 一键创建华为云基础设施
cd terraform/huawei
terraform init && terraform apply

# Kubernetes 部署
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

---

## 💰 定价（透明·无隐藏·无包月）

| 用户类型 | 免费额度/月 | 超出单价 | 包月 |
|---|---|---|---|
| 个人开发者 | 1万次API + 1000次搜索 | ¥0.0001/次 | ❌ 不强制 |
| 开源项目 | **无限制** | ¥0 | ❌ |
| 小团队 | 10万次API | ¥0.00005/次 | ❌ |
| 企业 | 100万次API | ¥0.00003/次 | ✅ 可选¥299/月 |

**核心承诺：**
- 不用不花钱
- 随时可停
- 数据随时可导出
- 本地部署永久免费

---

## 📦 模块说明

| 模块 | 说明 | 端口 |
|---|---|---|
| `api-gateway` | Go/Gin API网关·限流·鉴权·DNA追溯 | 9000 |
| `search-engine` | 多后端搜索·SearXNG+百度+Bing·零费用 | 8890 |
| `pricing` | 按量计费计量器·透明账单 | 8897 |
| `free-tier` | 个人开发者免费配额管理 | 8895 |
| `dna` | DNA追溯 + 三色审计中间件 | - |
| `dependency-isolation` | 依赖隔离·供应链风险检查·国产镜像优先 | 5001 |
| `sbom` | 软件物料清单生成（SPDX-Lite·零黑箱可复核） | 5002 |
| `evaluator` | 15条国产替代规则评估（人民币主权） | 5003 |
| `terraform/huawei` | 华为云基础设施·中国境内部署 | - |
| `docs` | 安全/基础设施/数据/交付/网络/运维/术语规范 | - |

---

## 🚪 SDK 与开发者入口（门 · 已打开）

```bash
# 1. 统一 SDK —— 一个包装齐 DNA/三色/国产替代/CNSH
pip install longhun

# 2. 统一 CLI —— 一个命令走全部能力
longhun version
longhun dna stamp --module MY-APP
longhun audit requirements.txt      # 15条国产替代扫描
longhun tricolor audit pay order_001 🟢
longhun cnsh run hello.cnsh

# 3. 统一入口落地页（可直接部署 GitHub Pages / 华为云 OBS）
#    site/index.html · 龍魂是什么 + 3行代码快速开始 + 定价
```

| 入口件 | 路径 | 说明 |
| --- | --- | --- |
| 统一 SDK | `sdk/longhun/` | `pip install longhun` · 零三方依赖 |
| 统一 CLI | `sdk/longhun/longhun/cli.py` | version/dna/audit/tricolor/cnsh |
| 落地页 | `site/index.html` | 单文件静态页 · 可挂 GitHub Pages/OBS |
| 禁训练声明 | `TRAINING_PROHIBITED.md` | 全仓库级 IP 保护 |
| 落地路径图 | `docs/ECOSYSTEM-GAP-ACTION-PLAN.md` | 缺口→谁做→步骤（AI/老大分工） |

---

## 🔑 统一账号（龍魂生态入口 · P0 焊死）

> **一个账号 = 龍魂生态全部服务。** 不需要多个账号，一是一双人。

- **一个账号**（UID9622）：人格工具调用 + 知识库调用 + 搜索引擎 + API 网关，全部同一账号
- **一样的付费**：统一按量计费（CNY 人民币计价·个人每月1万次免费·超出0.0001元/次）
- **一样的调用**：统一鉴权（`X-API-Key`）+ 统一 DNA 追溯（`X-LH-DNA`）+ 统一三色审计
- **无需多账号**：个人/开源/团队/企业 四档在同一账号下切换，不重复注册
- **原则**：技术无阶级·去门槛·本地永远免费·云端用多少付多少

```
统一入口: https://github.com/UID9622/sovereign-stack
统一密钥: 一个 API Key 走全部服务
统一账本: pricing/meter.py · 透明可查可停
统一追溯: 每次调用带 DNA · 三色审计
```

---

## 🌍 普惠全球理念

**为什么去门槛？**

1. 代码是知识，知识不应该有阶级
2. 中国有海量个人开发者，他们不应该为每个账号都包月
3. 技术生态的繁荣来自参与者多，而不是每个参与者花钱多
4. 本地能跑的，永远免费；云端用多少付多少

**我们不做的事：**
- ❌ 强制包月
- ❌ 免费功能突然收费
- ❌ 用你的数据训练模型
- ❌ 锁定数据不让导出

**DNA：** `#龍芯⚡️2026-08-31-SOVEREIGN-STACK-README-V2.0-UID9622`
**GPG：** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**确认码：** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
