# 🧬 龍魂统一DNA登记册 · 统一操作手册

<!--
╔════════════════════════════════════════════════════════════════╗
║  🐉 龍魂体系 | 底座锚点 A-029 · 统一入口说明书                  ║
╠════════════════════════════════════════════════════════════════╣
║  📦 文档：龍魂统一DNA登记册 · 统一操作手册                      ║
║  📌 版本：v1.0                                                  ║
║  🧬 DNA(v∞)：#龍芯⚡️丙午·丙申·甲寅·癸酉-A029-DNA-REGISTRY-ENTRY-v1.0 ║
║  👤 主权者：💎 UID9622 · 龍芯北辰                                ║
║  ⚠️ 性质：底座锚点文件 · 任何 AI 修改必须先读此文件              ║
║  ⛓️ 锚定：AGENTS.md A-029                                       ║
╚════════════════════════════════════════════════════════════════╝
-->

> **统一入口宣言**：以后无论 Kimi、CodeBuddy 还是任何 AI 修改龍魂 DNA 登记册，
> 都只改这一个入口目录。CLI 是底层引擎，Web UI 是统一界面，所有协同都围绕本目录进行。

---

## 🚪 统一入口（焊死）

| 入口 | 路径 / 地址 | 说明 |
|:---|:---|:---|
| **Web 统一界面** | `http://localhost:8778/` | 浏览器直接访问，按钮式操作 |
| **前端源码** | `L5_服务层/services/portal/portal/dna-registry/index.html` | 唯一官方前端 |
| **API 服务** | `L5_服务层/services/api/dna-registry/main.py` | FastAPI，端口 8778 |
| **CLI 引擎** | `bin/lh_unified_dna_registry.py` | ../脚本 |
| **人格路由** | `01_技能庫/dna-registry-persona.md` | P18/P19/P20 职责 |
| **审计人格** | `01_技能庫/dna-registry-audit.md` | P19 极简审计清单 |

⚠️ **旧位置**：`L5_服务层/services/dashboard/web/unified_dna_register_v1.0.html` 已冻结，仅作备份，不再维护。

---

## ⚡ 快速启动

```bash
# 1. 进入项目根
zuimeidedeyihan/longhun-system

# 2. 启动 API（自动挂载前端）
python3 L5_服务层/services/api/dna-registry/main.py

# 3. 浏览器打开统一入口
open http://localhost:8778/
```

看到页面标题为 **"龍魂 · 物理虚拟统一DNA登记册"** 即启动成功。

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                     统一入口 http://localhost:8778/          │
│                     (index.html · 按钮式 Web UI)             │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP
┌───────────────────────────▼─────────────────────────────────┐
│           FastAPI 桥接 (main.py · port 8778)                 │
│           /api/types  /api/register  /api/list  /api/verify  │
└───────────────────────────┬─────────────────────────────────┘
                            │ import
┌───────────────────────────▼─────────────────────────────────┐
│           CLI 核心引擎 (bin/lh_unified_dna_registry.py)      │
│           哈希计算 · Merkle 根 · 本地 JSON 存储              │
└─────────────────────────────────────────────────────────────┘
```

设计原则：**Web 是统一入口，CLI 是底层引擎，两者共用同一个核心，同一个数据目录。**

---

## 👥 人格分工

| 人格 | 职责 | 触发词 |
|:---|:---|:---|
| **P18 基因登记官** | 资产登记 · 格式校验 · 黑户检测 · Merkle 根哈希 | `DNA登记` `注册资产` `查归属` `基因登记` `registry` `asset dna` |
| **P19 极简审计官** | UI 极简审计 · 无障碍 · 格式标准化一票否决 | `DNA审计` `极简审计` `无障碍检查` `格式标准化` `minimalist audit` |
| **P20 贡献公证官** | 贡献积分计算 · 三分桶公证 · ../国际互认 | `信任积分` `贡献分` `功德分` `公益分` `贡献公证` `trust ledger` |

P18 负责收，P19 负责审，P20 负责公证。三个桶不混着溜大街。

---

## 📦 四大资产类别（32种）

| 类别 | 数量 | 类型 |
|:---|:---:|:---|
| 🔵 物理资产 | 12 | watch / patent / ip / engine / computer / phone / sim / card / contract / deed / vehicle / device |
| 🟣 虚拟资产 | 10 | email / domain / social / wallet / gpg / api / ssl / repo / game / nft |
| 🔴 身份资产 | 4 | id_card / passport / driver / military |
| 🌟 社会贡献 | 6 | oss_code / tech_doc / oss_maintain / community / welfare / intl_bridge |

⚠️ 身份资产**仅存 SHA256 哈希**，永不明文存储。哈希可对人不可见。

---

## 🏛️ 信任积分三分桶规则（P20）

```
信任指数 T = 技术贡献分 + 社会功德分 + 公益服务分  (≤100)

💻 技术贡献分 = oss_code×3.0 + tech_doc×2.0 + oss_maintain×2.5
   → 算力优先调用权 · 技术话语权威

⚖️ 社会功德分 = community×1.5 + welfare×2.0 + intl_bridge×1.8
   → 政审参考 · 国资入职 · 要职审查

🤝 公益服务分 = welfare + intl_bridge
   → 国际互认 · 信任桥梁 · 不图回报
```

**铁律**：
- 积分 **≠ 信誉分** · **≠ 免支付** · **≠ 消费券** · **≠ 商业信用分**
- 不参与信贷评估 · 不可交易 · 不可转让 · 不与商业平台互通

---

## 🔌 API 端点速查

| 方法 | 端点 | 说明 |
|:---|:---|:---|
| GET | `/` | 返回 Web UI（统一入口） |
| GET | `/api/types` | 获取所有资产类型 |
| POST | `/api/register` | 注册资产 |
| GET | `/api/list/{uid}` | 列出某 UID 资产 |
| GET | `/api/verify` | 验证资产归属 |
| GET | `/api/master/{uid}` | 获取主 DNA |
| GET | `/api/status/{uid}` | 获取统计 + 信任积分 |
| GET | `/api/public` | 获取公开资产清单 |

完整请求体见 `L5_服务层/services/api/dna-registry/main.py` 中的 Pydantic 模型。

---

## 📂 相关文件索引

```
longhun-system/
├── bin/lh_unified_dna_registry.py          # CLI 核心引擎
├── bin/lh_unified_dna_audit.py             # 审计脚本
├── L5_服务层/services/api/dna-registry/main.py      # API 桥接
├── L5_服务层/services/portal/portal/dna-registry/
│   ├── index.html                          # 唯一官方前端（本文件所在目录）
│   └── README.md                           # 本操作手册
├── 01_技能庫/dna-registry-persona.md       # P18 基因登记官人格
├── 01_技能庫/dna-registry-audit.md         # P19 极简审计官人格
└── L8_治理层/governance/dna/
    ├── 物理虚拟统一DNA登记册_v1.0.md
    └── unified_dna_persona_router_v1.0.md
```

---

## 🛡️ 操作铁律

1. **统一入口优先**：改 UI 只改 `portal/portal/dna-registry/index.html`，改 API 只改 `api/dna-registry/main.py`，改引擎只改 `bin/lh_unified_dna_registry.py`。
2. **格式不对不收**：所有资产必须先过格式校验，格式不统一不能当证明。
3. **原始编号永不明文**：本地只存 SHA256 哈希，不可逆。
4. **不删除只冻结**：争议资产标记，不物理删除。
5. **每条动作绑 DNA**：任何修改必须生成 `#龍芯⚡️...` 追溯码。
6. **积分不混用**：../公益三分桶，不与商业信用挂钩。

---

## 🧬 DNA 追溯

```
DNA(v∞): #龍芯⚡️丙午·丙申·甲寅·癸酉-A029-DNA-REGISTRY-ENTRY-v1.0
锚定: AGENTS.md A-029
统一入口: http://localhost:8778/
引擎: bin/lh_unified_dna_registry.py
API桥: L5_服务层/services/api/dna-registry/main.py
前端: L5_服务层/services/portal/portal/dna-registry/index.html
操作手册: L5_服务层/services/portal/portal/dna-registry/README.md
```

> CONFIRM: `#CONFIRM🌌9622-ONLY-ONCE🧬A029-ENTRY`
