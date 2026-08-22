# 🐉 龙魂 · 生态节点数据架构与技能图谱 v1.0

**DNA:** `#龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-ECOSYSTEM-NODE-DATA-ARCH-V1.0`
**创建者:** 诸葛鑫（UID9622）
**协议:** CC BY-NC-SA 4.0（核心思想层）
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**三色:** 🟢 通过

---

## 📋 核

> 生态不是"16个孤立服务"，而是**一台以数据为血液、以技能为器官的活体**。
> 每个节点 = 一套**数据架构**（它记住什么）× 一组**技能总线**（它能干什么）。
> 数据架构决定"这个节点记得住、长什么样"；技能总线决定"这个节点干得动、能做到什么"。
> 参考「AI原生数据库底座」范式：传统存储提供**确定性记忆**（它知道是什么），向量+图谱提供**联想式记忆**（它理解像什么）——生态每个节点都要同时具备这两种能力，才算补全。

---

## 🎯 设计原则（沿用 AI 数据库底座四原则 + 龙魂加码）

- **🔄 自动化优先**：节点数据自举、自愈、自归档，不依赖人工
- **🧩 模块化设计**：每节点独立 schema，按 `node_id` 解耦，可插拔
- **🔐 安全内生**：DNA追溯 + 三色审计 + 主权熔断内置于每个节点的数据模型
- **📈 可观测性**：全节点统一审计日志、统一 DNA 登记、统一耻辱墙
- **🧬 龙魂加码**：每张表必有 `dna` 列；每个节点必有 `node_id`；每条变更可溯源

---

## 🏛️ 生态总览（16节点 · 四层级）

```
┌──────────────────────────────────────────────────────────────────────┐
│                 🐉 龙魂生态 · 16节点数据架构全景                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────── free 层 (0元 · 人人可用) ─────────────────────┐  │
│  │  N01 龍魂算力守护 │ N02 统一DNA登记 │ N03 XPay支付网关         │  │
│  │  N04 龍魂通心译   │ N05 龍魂声音锚                             │  │
│  └────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────── basic 层 (9.9元/月) ──────────────────────────┐  │
│  │  N06 CNSH代码翻译 │ N07 龍魂许愿池 │ N08 决策来源卡            │  │
│  │  N09 龍魂审计过滤 │ N10 通心耳LoRA │ N11 龍魂记忆永生           │  │
│  │  N12 人格编排官   │ N13 上帝之眼   │ N14 龍芯执行器            │  │
│  └────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────── pro 层 (49.9元/月) ───────────────────────────┐  │
│  │  N15 信任积分簿   │ N16 龍魂道引器                             │  │
│  └────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────── founder 层 (999元 · 共建治理) ────────────────┐  │
│  │  全功能 · 参与系统治理 · 月度活人验证                            │  │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  ┌──────────────── 横切基础设施（所有节点共用）──────────────────┐   │
│  │  · 统一DNA登记册  · 统一审计日志  · 耻辱墙  · 三色审计          │   │
│  │  · 技能总线(50工具/13分类)  · 生态通行证(订阅/认证/密钥)        │   │
│  └────────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  数据流：通行证(身份) → 订阅(权限) → 节点(服务) → 审计(留痕)          │
│          → 记忆(沉淀) → 信任积分(信用) → 层级跃迁(成长)             │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🧬 一、横切基础设施（每节点数据架构的地基）

### 1.1 统一 DNA 登记册 `dna_registry`

> 引擎: `bin/lh_unified_dna_registry.py` · 每个数据单元的唯一身份根

```sql
CREATE TABLE dna_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL UNIQUE,          -- 主DNA追溯码 #龍芯⚡️干支·卦-模块-动作-哈希8
    node_id VARCHAR(32) NOT NULL,             -- 所属生态节点 N01~N16
    entity_type VARCHAR(20) NOT NULL,         -- user/service/engine/data/asset
    owner_uid VARCHAR(32) NOT NULL,           -- 归属 UID
    parent_dna VARCHAR(64),                   -- 父DNA（血缘链）
    hash8 CHAR(8) NOT NULL,                   -- 内容哈希8位
    gpg_signature VARCHAR(128),               -- GPG签名
    tri_color CHAR(2) DEFAULT '🟢',           -- 三色审计
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'       -- active/frozen/archived
);
CREATE INDEX idx_dna_node ON dna_registry(node_id);
CREATE INDEX idx_dna_owner ON dna_registry(owner_uid);
CREATE INDEX idx_dna_parent ON dna_registry(parent_dna);
```

### 1.2 统一审计日志 `audit_logs` (append-only)

> 引擎: `lh_audit` · 谁/何时/做什么/结果/DNA，只追加不删除

```sql
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    node_id VARCHAR(32) NOT NULL,
    operation VARCHAR(50) NOT NULL,           -- create/read/update/delete/access/fail
    target_type VARCHAR(20),
    target_id VARCHAR(64),
    operator_uid VARCHAR(32),
    tri_color CHAR(2),
    details TEXT,                              -- JSONB语义
    ip_hash VARCHAR(16),                       -- 脱敏IP（只存哈希·隐私不入云）
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_audit_node ON audit_logs(node_id);
CREATE INDEX idx_audit_dna ON audit_logs(dna);
CREATE INDEX idx_audit_time ON audit_logs(created_at);
```

### 1.3 耻辱墙 `shame_wall` (只写不删)

> 三色审计 🔴 违规 · 只追加，记录错误与教训

```sql
CREATE TABLE shame_wall (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    node_id VARCHAR(32),
    reason TEXT NOT NULL,
    severity VARCHAR(10),                     -- HIGH/MEDIUM/LOW
    evidence TEXT,                            -- JSON证据
    tri_color CHAR(2) DEFAULT '🔴',
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    resolved_by VARCHAR(32),
    resolution_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 1.4 技能总线 `skill_bus` (50工具/13分类)

> 引擎: `bin/lh_skill_bus.py` · 所有节点通过总线调用/注册技能

```sql
CREATE TABLE skill_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id VARCHAR(32) NOT NULL UNIQUE,     -- 技能ID
    node_id VARCHAR(32) NOT NULL,             -- 注册节点
    category VARCHAR(20) NOT NULL,            -- AI/安全/开发/数字人/治理/生态/经济/运维/搜索...
    name VARCHAR(64) NOT NULL,                -- 技能名
    entry VARCHAR(128),                       -- 入口（脚本/引擎路径）
    params TEXT,                              -- JSON参数schema
    output_schema TEXT,                       -- JSON输出schema
    rate_limit INTEGER DEFAULT 60,            -- 每分钟限次
    tri_color CHAR(2) DEFAULT '🟢',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_skill_node ON skill_registry(node_id);
CREATE INDEX idx_skill_cat ON skill_registry(category);
```

### 1.5 生态通行证 `ecosystem_passports`

> 引擎: `bin/lh_ecosystem_passport.py` · 身份/订阅/认证/密钥四位一体

```sql
CREATE TABLE ecosystem_passports (
    uid VARCHAR(32) PRIMARY KEY,              -- UID
    dna_hash VARCHAR(64) NOT NULL,            -- 关联DNA登记册主哈希
    member_level VARCHAR(10) NOT NULL,        -- free/basic/pro/founder
    eco_role VARCHAR(20) DEFAULT 'free_user', -- founder/developer/creator/real_name_user/free_user
    status VARCHAR(10) DEFAULT 'active',      -- active/frozen/suspended
    persona_pref VARCHAR(32) DEFAULT 'P00-文心',
    monthly_verify_expire VARCHAR(10),        -- 月度活人验证到期日
    first_verify_date VARCHAR(10),
    continuous_months INTEGER DEFAULT 0,      -- 连续月数（共建者判定）
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE subscription_records (           -- append-only 订阅历史
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid VARCHAR(32) NOT NULL,
    level VARCHAR(10) NOT NULL,               -- free/basic/pro/founder
    start_time VARCHAR(19) NOT NULL,
    expire_time VARCHAR(19) NOT NULL,
    auto_renew BOOLEAN DEFAULT TRUE,
    pay_method VARCHAR(10) DEFAULT 'xpay',
    tx_id VARCHAR(64),                        -- 关联XPay交易ID
    renew_count INTEGER DEFAULT 0,
    paid_months INTEGER DEFAULT 0,
    tri_color CHAR(2) DEFAULT '🟢'
);

CREATE TABLE auth_records (                   -- append-only 认证历史
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid VARCHAR(32) NOT NULL,
    auth_time VARCHAR(19) NOT NULL,
    auth_method VARCHAR(20) NOT NULL,         -- dna_verify/challenge_response/manual
    auth_result VARCHAR(10) NOT NULL,         -- passed/failed/pending
    challenge_code VARCHAR(32),
    response_hash VARCHAR(32)
);

CREATE TABLE api_keys (                       -- 活跃密钥
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid VARCHAR(32) NOT NULL,
    key_id VARCHAR(32) NOT NULL,
    key_hash VARCHAR(16) NOT NULL,            -- SHA256(密钥)前16位
    key_prefix VARCHAR(16) NOT NULL,          -- lh_xxxxxx
    purpose VARCHAR(64) DEFAULT '',
    scopes TEXT DEFAULT '[]',                 -- JSON权限范围
    status VARCHAR(10) DEFAULT 'active',      -- active/revoked/expired
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP
);
```

---

## 🏗️ 二、free 层节点（0元 · 人人可用）

### N01 龍魂算力守护

> 引擎: `bin/lh_auto_heal.py` + `bin/lh_health_check.py` · 每小时自动巡检·自愈·Bark推送

**数据架构** `node_n01_compute_guard`

```sql
CREATE TABLE node_n01_health_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    check_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    host VARCHAR(32) NOT NULL,                -- Mac/鲲鹏
    service_count INTEGER,                    -- 实际服务数
    healthy_count INTEGER,
    failed_services TEXT,                     -- JSON数组: 失败服务清单
    cpu_percent REAL,
    mem_percent REAL,
    disk_percent REAL,
    auto_healed BOOLEAN DEFAULT FALSE,        -- 本次是否自愈
    bark_pushed BOOLEAN DEFAULT FALSE,        -- 是否已推送告警
    tri_color CHAR(2) DEFAULT '🟢'
);
CREATE INDEX idx_n01_time ON node_n01_health_checks(check_time);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 健康巡检 | `lh_auto_heal.py scan` | 每小时全服务体检 |
| 自愈重启 | `lh_auto_heal.py heal` | 失败服务自动拉起 |
| Bark推送 | `deploy/scripts/health_check.sh` | 异常即推送到手机 |
| 服务拓扑 | `lh status` | 44 launchd + 56 systemd 实况 |

---

### N02 统一DNA登记

> 引擎: `bin/lh_unified_dna_registry.py` + `bin/lh_gpg_sign.py` · 全系统数据资产身份根

**数据架构**（见 §1.1 `dna_registry` 主表，本节为节点扩展）

```sql
CREATE TABLE node_n02_dna_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL UNIQUE,
    asset_name VARCHAR(128) NOT NULL,         -- 资产名（文件名/数据名/文档名）
    asset_type VARCHAR(20) NOT NULL,          -- file/data/engine/service/knowledge
    asset_path VARCHAR(256),                  -- 物理路径
    size_bytes INTEGER,
    content_hash VARCHAR(16),                 -- SHA256前16位
    gpg_signed BOOLEAN DEFAULT FALSE,         -- 是否已GPG签名
    gpg_signature_path VARCHAR(256),          -- .asc路径
    merklet_root VARCHAR(64),                 -- 若参与Merkle树
    owner_uid VARCHAR(32) DEFAULT 'UID9622',
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n02_type ON node_n02_dna_assets(asset_type);
CREATE INDEX idx_n02_hash ON node_n02_dna_assets(content_hash);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| DNA注册 | `lh_dna_register` | 新资产自动登记 |
| 哈希校验 | `lh_anti_tamper scan` | Merkle树防篡改 |
| GPG签名 | `lh_gpg_sign.py sign .` | 全量补签 |
| 归属验证 | `lh_dna_verify` | 黑户检测·归属追溯 |

---

### N03 XPay支付网关

> 引擎: `xpay/` 模块 · `backend/gateway.py` (sandbox HMAC) · 多币种·Sovereign 结算

**数据架构** `node_n03_xpay`

```sql
CREATE TABLE node_n03_transactions (          -- append-only 交易流水
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tx_id VARCHAR(64) NOT NULL UNIQUE,        -- 交易ID
    dna VARCHAR(64) NOT NULL,
    amount REAL NOT NULL,
    currency VARCHAR(8) NOT NULL,             -- CNY/USD/... 
    sender_uid VARCHAR(32) NOT NULL,
    recipient_uid VARCHAR(32) NOT NULL,
    purpose VARCHAR(64),                      -- subscribe/donate/pay/pool
    memo TEXT,
    processing_fee REAL DEFAULT 0,            -- 平台处理费
    dna_fee REAL DEFAULT 0,                   -- DNA追溯费
    total_fee REAL DEFAULT 0,
    status VARCHAR(20) NOT NULL,              -- pending/confirmed/failed/settled
    settlement_ref VARCHAR(64),               -- 结算引用
    sovereign_country VARCHAR(4) DEFAULT 'CN',-- 主权结算地
    gateway_mode VARCHAR(10) DEFAULT 'sandbox', -- sandbox/live
    hmac_signature VARCHAR(128),              -- HMAC签名
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n03_uid ON node_n03_transactions(sender_uid);
CREATE INDEX idx_n03_status ON node_n03_transactions(status);
CREATE INDEX idx_n03_time ON node_n03_transactions(created_at);

CREATE TABLE node_n03_balances (              -- 账户余额（只存聚合值·明细走流水）
    uid VARCHAR(32) PRIMARY KEY,
    balance REAL DEFAULT 0,
    locked_balance REAL DEFAULT 0,            -- 冻结中
    total_in REAL DEFAULT 0,
    total_out REAL DEFAULT 0,
    currency VARCHAR(8) DEFAULT 'CNY',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 交易创建 | `xpay create` | 发起支付/打赏 |
| 交易查询 | `xpay status` | 流水追溯 |
| 结算 | `xpay settle` | 主权结算 |
| 对账 | `xpay reconcile` | 日终对账·审计留痕 |
| 换真网关 | `backend/gateway.py` config | sandbox→live 一键切换 |

---

### N04 龍魂通心译

> 引擎: CNSH翻译引擎 · 中文神经符号混合语言 ↔ 代码 · 术语桥接

**数据架构** `node_n04_tongxinyi`

```sql
CREATE TABLE node_n04_translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    src_lang VARCHAR(10) NOT NULL,            -- cnsh/zh/en/py/js...
    dst_lang VARCHAR(10) NOT NULL,
    src_text TEXT NOT NULL,
    dst_text TEXT NOT NULL,
    semantic_score REAL,                      -- 语义保真度 0~1
    model_used VARCHAR(32),                   -- 使用模型
    embedding TEXT,                           -- JSON 向量(语义检索)
    user_uid VARCHAR(32),
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n04_src ON node_n04_translations(src_lang);
CREATE INDEX idx_n04_time ON node_n04_translations(created_at);

CREATE TABLE node_n04_terms (                 -- 术语桥接词典
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term VARCHAR(64) NOT NULL,                -- 术语原文
    meaning TEXT,                             -- 人话解释
    bridge_code VARCHAR(128),                 -- 桥接代码/CNSH
    category VARCHAR(20),                     -- technical/cultural
    glyph_version VARCHAR(8),                 -- 简体/繁体龍
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(term, category)
);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| CNSH→代码 | `lh_cnsh_translate` | 中文编程语言翻译 |
| 术语桥接 | `lh_terms` | 术语→人话→代码 |
| 语义保真 | `lh_align` | 翻译质量对齐审计 |
| 命名规范 | `lh_name_check` | 繁体「龍」永存校验 |

---

### N05 龍魂声音锚

> 引擎: `tts/` + `voices/` · 声音锚点·语音标识·声纹识别（个人声音主权）

**数据架构** `node_n05_voice_anchor`

```sql
CREATE TABLE node_n05_voices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    uid VARCHAR(32) NOT NULL,                 -- 声音主人
    voice_id VARCHAR(32) NOT NULL UNIQUE,
    voice_name VARCHAR(64),
    voice_file VARCHAR(256),                  -- 音频文件路径
    voiceprint_hash VARCHAR(64),              -- 声纹不可逆哈希（隐私不入云）
    duration_sec REAL,
    sample_rate INTEGER,
    format VARCHAR(10),                       -- wav/mp3/opus
    model_id VARCHAR(32),                     -- 合成模型
    status VARCHAR(20) DEFAULT 'active',
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n05_uid ON node_n05_voices(uid);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 声音登记 | `tts register` | 声纹锚点注册 |
| 语音合成 | `tts synth` | 声音克隆合成 |
| 声纹验证 | `tts verify` | 身份声纹校验 |
| 语音存档 | `voices/` | 声音资产管理 |

---

## 🏗️ 三、basic 层节点（9.9元/月 · 创作者起步）

### N06 CNSH代码翻译

> 引擎: CNSH 编译器 · `cnsh/` 目录 · 中华自主编程语言·中文→Python翻译

**数据架构** `node_n06_cnsh`

```sql
CREATE TABLE node_n06_cnsh_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    project_id VARCHAR(32) NOT NULL UNIQUE,
    project_name VARCHAR(64) NOT NULL,
    src_code TEXT,                            -- CNSH源码
    compiled_code TEXT,                       -- 目标代码(Python/JS)
    ast_json TEXT,                            -- AST语法树
    errors TEXT,                              -- JSON错误列表
    diagnostics TEXT,                         -- 诊断信息
    user_uid VARCHAR(32),
    embedding TEXT,                           -- 语义向量(代码检索)
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n06_user ON node_n06_cnsh_projects(user_uid);
CREATE INDEX idx_n06_time ON node_n06_cnsh_projects(created_at);

CREATE TABLE node_n06_syntax_errors (         -- 语法错误库（学习改进）
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    project_id VARCHAR(32),
    error_type VARCHAR(32),
    error_msg TEXT,
    suggestion TEXT,                          -- 修正建议
    model_suggestion TEXT,                    -- AI建议
    resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| CNSH翻译 | `lh_cnsh translate` | 中文→代码翻译 |
| 语法诊断 | `lh_cnsh check` | 错误诊断+修复建议 |
| 代码补全 | `lh_cnsh complete` | 代码智能补全 |
| 命名规范 | `lh_cnsh name` | CNSH命名·繁体龍校验 |
| 高亮渲染 | `cnsh-editor-mac` | 语法高亮编辑器 |

---

### N07 龍魂许愿池

> 引擎: 众筹/打赏/愿望清单 · `lh_xpay` 联动 · 经济引擎（众筹打赏）

**数据架构** `node_n07_wishing_pool`

```sql
CREATE TABLE node_n07_wishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    wish_id VARCHAR(32) NOT NULL UNIQUE,
    wish_title VARCHAR(128) NOT NULL,
    wish_desc TEXT,
    wish_type VARCHAR(20),                    -- feature/fund/idea/collective
    creator_uid VARCHAR(32) NOT NULL,
    target_amount REAL,                       -- 众筹目标
    current_amount REAL DEFAULT 0,
    supporters INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'open',        -- open/funding/funded/closed
    deadline VARCHAR(19),
    tags TEXT DEFAULT '[]',                   -- JSON标签
    embedding TEXT,                           -- 语义向量
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n07_status ON node_n07_wishes(status);
CREATE INDEX idx_n07_uid ON node_n07_wishes(creator_uid);

CREATE TABLE node_n07_supports (              -- 支持记录 append-only
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    wish_id VARCHAR(32) NOT NULL,
    supporter_uid VARCHAR(32) NOT NULL,
    amount REAL NOT NULL,
    message TEXT,
    tx_id VARCHAR(64),                        -- XPay交易ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n07_wish ON node_n07_supports(wish_id);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 发起愿望 | `lh_xpay wish create` | 众筹/愿望发起 |
| 支持打赏 | `lh_xpay wish support` | 资金支持·XPay联动 |
| 进度追踪 | `lh_xpay wish status` | 众筹进度查询 |
| 结算发放 | `lh_xpay wish settle` | 达成后资金结算 |
| ROI分析 | `lh_xpay roi` | 经济可行性·成本核算 |

---

### N08 决策来源卡

> 引擎: `bin/lh_decision_card_system.py` · 每次决策附来源卡·决策可追溯

**数据架构** `node_n08_decision_cards`

```sql
CREATE TABLE node_n08_decision_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    hash8 CHAR(8) NOT NULL,                   -- 决策内容哈希
    card_type VARCHAR(20) NOT NULL,           -- choice/strategy/policy/audit
    decision_level VARCHAR(5),                -- L0~L9
    title VARCHAR(128) NOT NULL,
    trigger_input TEXT,                       -- 触发输入
    selected_option TEXT,                     -- 选中方案
    alternatives TEXT DEFAULT '[]',           -- 备选方案 JSON
    tri_color CHAR(2),                        -- 三色审计结果
    responsibility_owner VARCHAR(32),         -- 责任归属
    reversible BOOLEAN DEFAULT FALSE,         -- 是否可逆
    context TEXT,                             -- 决策上下文
    reasoning TEXT,                           -- 推理过程
    embedding TEXT,                           -- 语义向量
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n08_hash ON node_n08_decision_cards(hash8);
CREATE INDEX idx_n08_type ON node_n08_decision_cards(card_type);
CREATE INDEX idx_n08_time ON node_n08_decision_cards(created_at);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 决策记录 | `lh decision-card new` | 生成决策来源卡 |
| 决策检索 | `lh decision-card search` | 历史决策追溯 |
| 方案对比 | `lh decision-card compare` | 多方案对比 |
| 三色审计 | `lh audit` | 决策合规性审查 |

---

### N09 龍魂审计过滤

> 引擎: 审核过滤系统（v2.0规格书） · `lh_three_color_audit` · 内容安全过滤

**数据架构** `node_n09_audit_filter`

```sql
CREATE TABLE node_n09_filter_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    rule_id VARCHAR(32) NOT NULL UNIQUE,
    rule_name VARCHAR(64) NOT NULL,
    rule_type VARCHAR(20) NOT NULL,           -- keyword/regex/model/policy
    pattern TEXT NOT NULL,                    -- 匹配规则
    severity VARCHAR(10) NOT NULL,            -- HIGH/MEDIUM/LOW
    action VARCHAR(20) NOT NULL,              -- block/review/flag/warn
    tri_color CHAR(2) DEFAULT '🟢',
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n09_type ON node_n09_filter_rules(rule_type);

CREATE TABLE node_n09_filter_logs (           -- 过滤日志 append-only
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    content_hash VARCHAR(16) NOT NULL,
    matched_rule VARCHAR(32),
    severity VARCHAR(10),
    action_taken VARCHAR(20),
    content_preview TEXT,                     -- 脱敏预览（不存原文）
    tri_color CHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n09_time ON node_n09_filter_logs(created_at);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 规则匹配 | `lh audit-filter check` | 内容过滤检测 |
| 规则管理 | `lh audit-filter rules` | 规则增删改查 |
| 三色判定 | `lh audit-filter color` | 🟢🟡🔴 审计判定 |
| 屏蔽处置 | `lh audit-filter block` | 违规自动阻断 |

---

### N10 通心耳LoRA

> 引擎: LoRA 微调模型 · `models/` · 通心耳语音识别·中文方言支持

**数据架构** `node_n10_lora`

```sql
CREATE TABLE node_n10_lora_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    model_id VARCHAR(32) NOT NULL UNIQUE,
    model_name VARCHAR(64) NOT NULL,
    base_model VARCHAR(32),                   -- 基础模型
    rank INTEGER,                             -- LoRA rank
    alpha INTEGER,                            -- LoRA alpha
    train_data_count INTEGER,                 -- 训练样本数
    val_loss REAL,                            -- 验证损失
    dataset_version VARCHAR(16),              -- 训练数据版本
    status VARCHAR(20) DEFAULT 'training',    -- training/ready/archived
    artifact_path VARCHAR(256),               -- 模型文件路径
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n10_status ON node_n10_lora_models(status);

CREATE TABLE node_n10_train_sessions (        -- 训练会话
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    model_id VARCHAR(32) NOT NULL,
    epoch INTEGER,
    loss REAL,
    lr REAL,
    elapsed_sec REAL,
    metrics TEXT,                             -- JSON指标
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    status VARCHAR(20)
);
CREATE INDEX idx_n10_model ON node_n10_train_sessions(model_id);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 模型训练 | `lh_lora_trainer_v4.py` | MLX LoRA 训练 |
| 推理服务 | `ollama run longhun-v4.0` | 模型推理 |
| 数据准备 | `data/` JSONL | 训练语料管理 |
| 质量过滤 | `quality<0.5过滤` | 数据自举过滤 |

---

### N11 龍魂记忆永生

> 引擎: `bin/lh_memory_hub.py` + `bin/lh_memory_load.py` · Notion+本地双索引 · 跨AI协作记忆库

**数据架构** `node_n11_memory` (SQLite + Notion 双写)

```sql
CREATE TABLE node_n11_memory_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    entry_id VARCHAR(36) NOT NULL UNIQUE,     -- UUID/Notion page id
    category VARCHAR(20) NOT NULL,            -- 索引/里程碑/铁律/人格/教训
    title VARCHAR(128) NOT NULL,
    content TEXT NOT NULL,                    -- 内容
    keywords TEXT DEFAULT '[]',               -- JSON关键词
    creator VARCHAR(32) NOT NULL,             -- 创建者
    collaborator_signature VARCHAR(64),       -- 协作签名 创建者@UTC@DNA
    source VARCHAR(64),                       -- 来源
    priority INTEGER DEFAULT 0,               -- 优先级
    embedding TEXT,                           -- 256维n-gram哈希向量(JSON)
    vector TEXT,                              -- 向量表示
    backfilled BOOLEAN DEFAULT FALSE,         -- 是否已回填Notion
    notion_url VARCHAR(256),                  -- Notion链接
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n11_cat ON node_n11_memory_entries(category);
CREATE INDEX idx_n11_key ON node_n11_memory_entries(keywords);
CREATE INDEX idx_n11_creator ON node_n11_memory_entries(creator);
CREATE INDEX idx_n11_time ON node_n11_memory_entries(created_at);

CREATE TABLE node_n11_memory_links (          -- 记忆关联图
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id VARCHAR(36) NOT NULL,
    target_id VARCHAR(36) NOT NULL,
    relation VARCHAR(20),                     -- 关联/引用/衍生/冲突
    weight REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n11_src ON node_n11_memory_links(source_id);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 记忆写入 | `lh memory-hub add` | 新增记忆（必填7字段） |
| 记忆检索 | `lh memory-hub search` | 语义向量检索 |
| 向量化 | `lh memory-hub vector` | 256维n-gram哈希向量 |
| Notion同步 | `lh memory-hub push` | 本地→Notion |
| 回填 | `lh memory-hub backfill` | 历史数据回填 |
| 非空校验 | `lh memory-hub check` | 必填字段校验 |
| 协作签名 | `lh memory-hub sign` | 创建者@UTC@DNA |
| 启动加载 | `lh_memory_load.py` | 会话自动读取 |

---

### N12 人格编排官

> 引擎: `bin/personas/` + `20_CONFIG/persona-duty-matrix.json` · 20人格路由·意图解析·防抖动

**数据架构** `node_n12_persona`

```sql
CREATE TABLE node_n12_personas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    persona_id VARCHAR(16) NOT NULL UNIQUE,   -- P00~P72+P77+S1~S3
    name VARCHAR(32) NOT NULL,                -- 人格名
    layer VARCHAR(10) NOT NULL,               -- 战略/执行/文化/守护/安全/子系统
    function VARCHAR(64) NOT NULL,            -- 职能
    duty_weight REAL DEFAULT 0,               -- 分工权重
    engine_path VARCHAR(128),                 -- 执行器路径
    config_path VARCHAR(128),                 -- 定义文件
    trigger_keywords TEXT DEFAULT '[]',       -- 触发词
    status VARCHAR(20) DEFAULT 'active',      -- active/locked/cooling
    last_triggered TIMESTAMP,
    trigger_count INTEGER DEFAULT 0,
    lock_until TIMESTAMP,                     -- 防抖动锁
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n12_layer ON node_n12_personas(layer);
CREATE INDEX idx_n12_status ON node_n12_personas(status);

CREATE TABLE node_n12_routing_logs (          -- 路由日志 append-only
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    intent TEXT,                              -- 用户意图
    routed_to VARCHAR(16) NOT NULL,           -- 路由目标人格
    confidence REAL,                          -- 匹配置信度
    co_agents TEXT DEFAULT '[]',              -- 联动人格
    debounce_locked BOOLEAN DEFAULT FALSE,    -- 是否触发防抖动
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n12_routed ON node_n12_routing_logs(routed_to);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 意图解析 | `lh persona route` | 用户意图→人格 |
| 人格切换 | `lh persona switch` | 动态路由切换 |
| 防抖动 | 连续3次锁定30分钟 | 防止反复触发 |
| 人格状态 | `lh duty` | 人格分工·花名册 |
| 人格审计 | `lh persona audit` | 职能对齐审查 |

---

### N13 上帝之眼

> 引擎: `lh_three_color_audit` + `bin/lh_dual_audit.py` · 三色审计·十道闸口·左右互搏

**数据架构** `node_n13_eye`

```sql
CREATE TABLE node_n13_audit_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    report_id VARCHAR(32) NOT NULL UNIQUE,
    audit_target VARCHAR(128) NOT NULL,       -- 审计对象
    audit_type VARCHAR(20) NOT NULL,          -- 三色/双人格/结构/代码/安全
    gates_passed INTEGER DEFAULT 0,           -- GATE-01~11 通过数
    gates_total INTEGER DEFAULT 11,
    tri_color CHAR(2) NOT NULL,               -- 🟢🟡🔴
    risk_score REAL,                          -- 风险评分 0~100
    findings TEXT DEFAULT '[]',               -- JSON发现项
    recommendations TEXT DEFAULT '[]',        -- JSON建议
    auditor_persona VARCHAR(16),              -- 审计人格
    co_auditor VARCHAR(16),                   -- 交叉审计人格
    gpg_signature VARCHAR(128),               -- 审计签名
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n13_type ON node_n13_audit_reports(audit_type);
CREATE INDEX idx_n13_color ON node_n13_audit_reports(tri_color);
CREATE INDEX idx_n13_time ON node_n13_audit_reports(created_at);

CREATE TABLE node_n13_gate_logs (             -- 十道闸口通过记录
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    report_id VARCHAR(32) NOT NULL,
    gate_no VARCHAR(8) NOT NULL,              -- GATE-01~11
    gate_name VARCHAR(32) NOT NULL,
    result VARCHAR(10) NOT NULL,              -- pass/fail/pending
    detail TEXT,
    checked_by VARCHAR(16),                   -- 检查人格
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n13_gate ON node_n13_gate_logs(report_id);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 三色审计 | `lh audit` | 🟢🟡🔴判定 |
| 十道闸口 | `lh gates` | GATE-01~11逐道检查 |
| 左右互搏 | `lh dual-audit` | 双人格交叉互审 |
| 代码审计 | `lh code-audit` | 代码级漏洞扫描 |
| 镜像审计 | `lh mirror-audit` | 关键计算独立复算 |
| GPG验签 | `lh_gpg_sign.py scan` | 签名完整性验证 |

---

### N14 龍芯执行器

> 引擎: `bin/lh.py` + `龙魂执行器` · 通用执行器·多步任务编排·跨人格协同

**数据架构** `node_n14_executor`

```sql
CREATE TABLE node_n14_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    task_id VARCHAR(32) NOT NULL UNIQUE,
    task_name VARCHAR(128) NOT NULL,
    task_type VARCHAR(20),                    -- one_shot/pipeline/recurring
    prompt TEXT,                              -- 任务描述
    status VARCHAR(20) DEFAULT 'pending',     -- pending/running/paused/done/failed
    orchestrator VARCHAR(16),                 -- 主理人格
    agents TEXT DEFAULT '[]',                 -- 参与人格
    steps TEXT DEFAULT '[]',                  -- 步骤JSON
    progress REAL DEFAULT 0,                  -- 进度 0~1
    result TEXT,                              -- 结果JSON
    error TEXT,
    user_uid VARCHAR(32) DEFAULT 'UID9622',
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    finished_at TIMESTAMP
);
CREATE INDEX idx_n14_status ON node_n14_tasks(status);
CREATE INDEX idx_n14_user ON node_n14_tasks(user_uid);
CREATE INDEX idx_n14_time ON node_n14_tasks(created_at);

CREATE TABLE node_n14_exec_logs (             -- 执行日志 append-only
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    task_id VARCHAR(32) NOT NULL,
    step_no INTEGER,
    agent VARCHAR(16),
    action TEXT,
    result TEXT,
    elapsed_ms INTEGER,
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n14_task ON node_n14_exec_logs(task_id);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 任务编排 | `lh task run` | 多步任务编排 |
| 跨人格协同 | `龙魂执行器` | 多人格并行协作 |
| 进度追踪 | `lh task status` | 任务状态查询 |
| 重试恢复 | `lh task retry` | 失败任务重试 |
| 结果审计 | `lh task audit` | 执行结果三色审计 |

---

## 🏗️ 四、pro 层节点（49.9元/月 · 深度用户）

### N15 信任积分簿

> 引擎: `lh_trust_score.py` + `P20贡献公证官` · 三分桶·信任积分·贡献公证

**数据架构** `node_n15_trust`

```sql
CREATE TABLE node_n15_trust_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    uid VARCHAR(32) NOT NULL,
    tech_score REAL DEFAULT 0,                -- 技术桶积分
    community_score REAL DEFAULT 0,           -- 社区桶积分
    creation_score REAL DEFAULT 0,            -- 创作桶积分
    total_score REAL DEFAULT 0,               -- 总分
    bucket_type VARCHAR(20),                  -- 场景矩阵判定类型
    contribution_log TEXT DEFAULT '[]',       -- JSON贡献明细
    polit_check VARCHAR(20),                  -- 政审结果
    state_own_check VARCHAR(20),              -- 国资判定
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tri_color CHAR(2) DEFAULT '🟢',
    UNIQUE(uid)
);
CREATE INDEX idx_n15_uid ON node_n15_trust_scores(uid);
CREATE INDEX idx_n15_total ON node_n15_trust_scores(total_score);

CREATE TABLE node_n15_contribution_events (   -- 贡献事件 append-only
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    uid VARCHAR(32) NOT NULL,
    event_type VARCHAR(20) NOT NULL,          -- tech/community/creation
    event_desc TEXT,
    score_delta REAL,
    scene_matrix TEXT,                        -- 场景矩阵判定结果
    notarizer VARCHAR(16) DEFAULT 'P20',      -- 公证人格
    evidence TEXT,                            -- JSON证据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n15_event ON node_n15_contribution_events(uid);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 积分计算 | `lh trust-score calc` | 三分桶积分计算 |
| 贡献公证 | `lh trust-score notarize` | P20贡献公证 |
| 场景判定 | `lh trust-score matrix` | 场景矩阵判定 |
| 信任查询 | `lh trust-score get` | 用户信任分查询 |
| 政审 | `lh trust-score audit` | 贡献政审·国资判定 |

---

### N16 龍魂道引器

> 引擎: 道引·文化导引·道德经锚点联动 · `lh_dao_de_jing` 联动

**数据架构** `node_n16_daoyin`

```sql
CREATE TABLE node_n16_guidance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    uid VARCHAR(32) NOT NULL,
    guidance_type VARCHAR(20) NOT NULL,       -- philosophical/action/strategy
    question TEXT,                            -- 用户提问
    guidance TEXT NOT NULL,                   -- 道引内容
    anchor_chapter VARCHAR(16),               -- 道德经章节锚点
    model_used VARCHAR(32),
    user_feedback INTEGER DEFAULT 0,          -- 反馈 -1~5
    embedding TEXT,                           -- 语义向量
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n16_uid ON node_n16_guidance(uid);
CREATE INDEX idx_n16_type ON node_n16_guidance(guidance_type);

CREATE TABLE node_n16_daodejing_anchors (     -- 道德经81章锚点库
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_no INTEGER NOT NULL UNIQUE,       -- 1~81
    chapter_title VARCHAR(64) NOT NULL,
    original_text TEXT NOT NULL,              -- 原文
    plain_explanation TEXT,                   -- 大白话解读
    algorithmic_anchor TEXT,                  -- 算法锚定点
    philosophic_concept TEXT,                 -- 哲学概念可计算化
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_n16_chapter ON node_n16_daodejing_anchors(chapter_no);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 道引问答 | `lh daoyin ask` | 哲学/行动导引 |
| 道德经锚点 | `lh_dao_de_jing` | 81章原文+算法锚定 |
| 十维联动 | `lh daoyin cross` | 与十维同演联动 |
| 用户反馈 | `lh daoyin feedback` | 反馈闭环优化 |

---

## 🏗️ 五、founder 层（999元 · 共建治理）

> founder = 全功能叠加 + 参与系统治理 + 月度活人验证（连续月数判定共建者）

**数据架构** `node_founder_governance`

```sql
CREATE TABLE node_founder_governance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    uid VARCHAR(32) NOT NULL,                 -- founder用户
    governance_role VARCHAR(32),              -- 治理角色
    proposals_submitted INTEGER DEFAULT 0,    -- 提案数
    proposals_voted INTEGER DEFAULT 0,        -- 投票数
    monthly_verified INTEGER DEFAULT 0,       -- 月度活人验证次数
    continuous_months INTEGER DEFAULT 0,      -- 连续月数
    contribution_points REAL DEFAULT 0,       -- 治理贡献分
    trust_score REAL DEFAULT 0,               -- 关联信任积分
    last_verify_date VARCHAR(10),
    status VARCHAR(20) DEFAULT 'active',
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_f_uid ON node_founder_governance(uid);
```

**技能清单**

| 技能 | 入口 | 说明 |
|:---|:---|:---|
| 全功能访问 | 生态全节点 | 16节点全部开放 |
| 治理提案 | `lh governance propose` | 系统改进提案 |
| 治理投票 | `lh governance vote` | 提案投票 |
| 月度验证 | `lh passport verify` | 活人验证·防僵尸 |

---

## 🔗 六、节点间数据流（生态活体如何呼吸）

```
用户 ──→ [N03 XPay 支付] ──→ [N02 DNA登记 身份] ──→ [通行证 订阅升级]
  │                                                      │
  ▼                                                      ▼
[N06~N14 basic 技能] ──→ [N08 决策来源卡 记录每次决策]
  │                                                      │
  ▼                                                      ▼
[N11 记忆永生 沉淀] ←── [N13 上帝之眼 审计] ←── [N14 执行器 落地]
  │                                                      │
  ▼                                                      ▼
[N15 信任积分 积累] ──→ [层级跃迁 free→basic→pro→founder]
  │                                                      │
  ▼                                                      ▼
[N16 道引器 价值导引] ←── [N09 审计过滤 安全兜底] ←── [N01 算力守护 全链路]
```

**数据流铁律**：
1. 每个节点写入前先过 `dna_registry` 登记 → 每条数据有身份证
2. 每个节点变更写 `audit_logs` → 全链路可追溯
3. 每个节点 🔴 违规 → `shame_wall` 耻辱墙 → 只写不删
4. 每个节点技能 → `skill_registry` 注册 → 总线统一调度
5. 节点间联动 → 走 `node_id` 关联 → 不跨库直接引用

---

## 📊 七、数据量预估（生态规模参考）

| 节点 | 表数 | 预估年数据量 | 存储介质 |
|:---|:---:|:---|:---|
| N01 算力守护 | 1 | 8,760行/年(每小时) | SQLite 热 |
| N02 DNA登记 | 2 | 10K行/年 | SQLite 温 |
| N03 XPay | 2 | 100K流水/年 | SQLite 温(append-only) |
| N04 通心译 | 2 | 50K翻译/年 | SQLite+向量 |
| N05 声音锚 | 1 | 1K声纹/年 | 文件+SQLite |
| N06 CNSH | 2 | 20K项目/年 | SQLite+向量 |
| N07 许愿池 | 2 | 5K愿望/年 | SQLite 温 |
| N08 决策卡 | 1 | 10K决策/年 | SQLite+向量 |
| N09 审计过滤 | 2 | 100K日志/年 | SQLite append-only |
| N10 LoRA | 2 | 200模型/年 | 文件+SQLite |
| N11 记忆永生 | 2 | 50K记忆/年 | SQLite+Notion双写 |
| N12 人格编排 | 2 | 100K路由/年 | SQLite |
| N13 上帝之眼 | 2 | 10K审计/年 | SQLite |
| N14 执行器 | 2 | 20K任务/年 | SQLite |
| N15 信任积分 | 2 | 10K事件/年 | SQLite 温 |
| N16 道引器 | 2 | 30K导引/年 | SQLite+向量 |
| **合计** | **30** | **~525K行/年** | **SQLite 完全可承载** |

> 💡 生态当前规模（实测）：SQLite 单机即可承载。数据量 >100万行时启用 pgvector 升维（参照 AI 数据库底座 L2 温数据层策略）。

---

## ⚙️ 八、与 AI 数据库底座的四层映射

| AI数据库底座层 | 生态落点 |
|:---|:---|
| ① 接入层 | `lh` CLI / `lh capture(:8769)` / 技能总线 / MCP / REST API |
| ② 查询引擎层 | `lh search`(语义) + `lh index`(认知) + `lh semantic-merge`(混合) |
| ③ 存储层 | L1热: 会话上下文+向量缓存 ｜ L2温: 记忆库+知识库+审计 ｜ L3冷: 归档日志+旧模型 |
| ④ 治理与安全层 | N13上帝之眼(三色审计) + N02 DNA登记(追溯) + 主权熔断 + 加密存储 |

---

## 🔐 九、最终签名

```
════════════════════════════════════════════════════════════════════════
 🐉 龙魂 · 生态节点数据架构与技能图谱 v1.0 · 最终签名
════════════════════════════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-ECOSYSTEM-NODE-DATA-ARCH-V1.0
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
核心能力:   16节点 × 数据架构 + 技能清单 + 横切治理 + 数据流 + 规模预估
覆盖:       free 5 + basic 9 + pro 2 + founder 1 + 横切5 + 映射4
状态:       补全完成 · 可落地
════════════════════════════════════════════════════════════════════════
```

> 下一迭代（待 UID9622 确认）：为 30 张表生成统一 `schema.sql` 落地文件 + `lh_ecosystem_schema.py` 自动建表引擎。



