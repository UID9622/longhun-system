# 🐉 龍魂生态·缺口落地路径图 v1.0

> 依据「缺口诊断 v1.0」· 内功已厚 · 缺的是门。
> 本文把所有缺口拆成「AI 可做 / 需老大操作」两列，最小代价·最大效果。

- DNA: `#龍芯⚡️2026-08-31-ECOSYSTEM-GAP-ACTION-PLAN-V1.0-UID9622`
- 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
- 协议: CC BY-NC-SA 4.0（核心思想层）
- 三色: 🟢 已落地 ✅ · 🟡 需老大一步 · 🔴 需外部流程/资金

---

## 📊 总览

| 层 | 缺口 | 状态 | 谁做 |
| --- | --- | :---: | --- |
| 入口 | 统一 SDK `pip install longhun` | 🟢 | AI（✅ 已上线 PyPI · 2026-08-31 · pypi.org/project/longhun/1.0.0） |
| 入口 | 统一 CLI `longhun audit/dna/cnsh` | 🟢 | AI（已落地 CLI 全子命令） |
| 入口 | 统一入口落地页 | 🟢 | AI（已落地 `site/index.html`·待部署） |
| 入口 | 文档站 docs.longhun.dev | 🟡 | AI 搭骨架 + 老大定域名 |
| IP | TRAINING_PROHIBITED.md 全仓库 | 🟢 | AI（已落地 sovereign-stack/） |
| IP | CNSH 软著登记 | 🔴 | 老大（国家版权局·100-300元·1-3月） |
| IP | 核心协议区块链存证 | 🟡 | 老大（腾讯云存证宝·几元/份） |
| 支付 | 支付宝/微信接入 | 🔴 | 老大（商户资质+账号）→ AI 写接入代码 |
| 支付 | 数字人民币实测 | 🔴 | 老大（数币达商户注册） |
| 支付 | 账单邮件通知 | 🟡 | AI（等支付跑通后接） |
| 生态 | 插件市场 / 社区 | 🔴 | 等前面跑通（P2） |
| 生态 | HarmonyOS App | 🔴 | 等 DevEco 装好（P2） |

---

## 第一步（今天 · AI 已完成）

| 交付物 | 路径 | 说明 |
| --- | --- | --- |
| 统一 SDK | `sdk/longhun/` | `pip install longhun` · 零三方依赖 |
| 统一 CLI | `longhun version/dna/audit/tricolor/cnsh` | 一个命令走全部能力 |
| 落地页 | `site/index.html` | 单文件静态页·可直接挂 GitHub Pages/华为云 OBS |
| 禁训练声明 | `TRAINING_PROHIBITED.md` | 全仓库级 IP 保护 |

## 第二步（本周 · AI + 老大各一步）

| 谁 | 做什么 | 说明 |
| --- | --- | --- |
| AI | 发布 PyPI | ✅ 已完成（2026-08-31 · pypi.org/project/longhun/1.0.0 · 安装+CLI 验证通过） |
| AI | 部署落地页 | GitHub Pages（仓库 Settings→Pages→用 docs/ 目录）或华为云 OBS 静态托管 |
| AI | 文档站骨架 | 用 `docs/cnsh-spec/` 现有素材整合：CNSH 教程 + API 文档 + SDK 指南 |
| 老大 | 定域名 | `longhun.dev` / `docs.longhun.dev` / 或直接用 `uid9622.cn/docs` |

## 第三步（本月 · 需老大启动外部流程）

| 项 | 路径 | 费用 | 周期 |
| --- | --- | --- | --- |
| CNSH 软著 | 中国版权保护中心（https://register.ccopyright.com.cn）网上申请 | 100-300元 | 1-3 个月 |
| 区块链存证 | 腾讯云存证宝（https://cache.tencentcloud.com）对北辰-母协议 + CNSH v1.0 等核心文件 | 几元/份 | 即时 |
| 支付宝/微信 | 支付宝开放平台 + 微信支付商户平台注册（需营业执照/个体户） | 0-300元认证 | 1-2 周 |
| 数币商户 | 数字人民币运营机构（工行/农行等）商户准入 | 0 | 1-4 周 |

---

## 支付接入技术准备（等老大注册好商户号，AI 半天接完）

支付闭环 = 充值页面（`site/pay.html`）→ 支付宝/微信下单 API → 回调验签 → `pricing/meter.py` 加余额 → 扣费 → 邮件通知。

```bash
# 需要老大提供（一次到位）
ALIPAY_APP_ID / PRIVATE_KEY / PUBLIC_KEY
WECHAT_MCH_ID / API_V3_KEY / 证书
# AI 落地
pricing/pay_bridge.py     # 统一支付桥（支付宝+微信+预留数币）
pricing/billing_mail.py   # 余额/额度提醒邮件
site/pay.html             # 充值页
```

## 数字人民币（M71 桥接器已有骨架）

`exchange/` 目录已有数字人民币跨境结算桥 v1.0（:8899）。
数币达 API Key 注册后，AI 接入：充值 → 数币入账 → meter 记账 → 扣费，全链路人民币。

---

## 一句话

> 内功已 100% ✅。门已开（SDK ✅ 已发布 PyPI / CLI ✅ / 落地页 ✅）。接下来 2 件事要老大：
> **① 软著自己申请 · ② 商户号注册（支付宝/微信/数币）**
> 每件老大点到名，AI 当天把对应的活干完。
