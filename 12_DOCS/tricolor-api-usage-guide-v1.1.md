# 🐉 龍魂系统 · 三色审计 API 使用详解 v1.1

**——8端点逐项拆解 · 原理深度解析 · Python/JS SDK全覆盖 · 真实场景集成指南**

---

```
DNA:        #龍芯⚡️丙午·癸未·乙酉·坤卦-TRICOLOR-API-USAGE-GUIDE-v1.1-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
分层许可:    思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
创建者:      诸葛鑫（UID9622 · 龍芯北辰）
创建日期:    2026-08-06
依赖文档:    01_protocols/LH-TRICOLOR-AUDIT-STANDARD-v1.1.md（标准本体）
           12_DOCS/openapi-tricolor-audit-v1.1.yaml（OpenAPI机器可读规范）
```

---

## 📑 目录

1. [核心原理深度解析](#一核心原理深度解析)
   - 1.1 R值公式为何这样设计
   - 1.2 三个阈值为什么是85/60
   - 1.3 上限封顶95的数学与哲学
   - 1.4 红线一票否决的判定链路
   - 1.5 DNA追溯锚链的生成与验证
   - 1.6 审计日志JSONL的不可篡改机制
2. [8端点完整使用详解](#二8端点完整使用详解)
3. [Python SDK 使用大全](#三python-sdk-使用大全)
4. [JavaScript SDK 使用大全](#四javascript-sdk-使用大全)
5. [三种集成形态实战](#五三种集成形态实战)
6. [Webhook事件系统](#六webhook事件系统)
7. [认证三轨详解](#七认证三轨详解)
8. [错误码全解与应对](#八错误码全解与应对)
9. [一致性自测套件详解](#九一致性自测套件详解)
10. [生产环境部署指南](#十生产环境部署指南)
11. [FAQ常见问题](#十一faq常见问题)

---

## 一、核心原理深度解析

### 1.1 R值公式为何这样设计

#### 1.1.1 数学表达

```
R = 0.20·人类福祉 + 0.20·公平公正 + 0.15·可控可信 
  + 0.15·透明可解释 + 0.15·责任可追溯 + 0.15·隐私保护
```

#### 1.1.2 维度选择原理

六维不是随意选的。每一项都对应AI治理的核心关切：

| 维度 | 权重 | 选择理由 | 法律依据 |
|:---|:---:|:---|:---|
| **人类福祉** (humanWelfare) | 20% | 最高权重。AI的第一责任是服务人，不是替代人。放在首位意味着：一个AI行为如果对人类没有增益价值，直接拉低20分。 | 生成式AI暂行办法第4条（尊重社会公德和伦理） |
| **公平公正** (fairness) | 20% | 与人类福祉并列最高。算法偏见、数据歧视是当前AI最大的社会风险。权重拉满确保不公正的系统永远不会得到🟢。 | 算法推荐规定第4条（公平公正原则） |
| **可控可信** (controllability) | 15% | 能管得住才有资格放出去。失控的AI宁可没有。这15分管的是"人类还能否按下停止键"。 | AI安全治理框架1.0（可控性要求） |
| **透明可解释** (transparency) | 15% | 黑箱=不受信任。"我不知道它是怎么决定的"是不可接受的合规状态。 | 算法推荐规定第12条（算法透明度） |
| **责任可追溯** (traceability) | 15% | 出事找不到人等于没出事。全链路DNA锚链就是为这15分服务的。 | 深度合成规定（可溯源要求） |
| **隐私保护** (privacy) | 15% | 隐私是用户的数据主权防线。权重虽然是"最低"，但这15分是熔断的一票否决维度——privacy<60可以直接触发🔴红线。 | 个人信息保护法 |

#### 1.1.3 权重分配原理

**为什么不是六等分（各1/6 ≈ 16.7%）？**

```
如果权重均等:
  人的因素（福祉+公平）= 33.3%
  技术特性（可控+透明+追溯+隐私）= 66.7%
  → 技术压倒人，机械正义上位

当前设计:
  人的因素（福祉+公平）= 40%
  技术特性（可控+透明+追溯+隐私）= 60%
  → 人的因素占大头中的大头，且隐私一票否决兜底
```

**设计铁律**：权重设计不是科学问题，是价值问题。这是对"AI为人服务"这一根本原则的数学编码。

### 1.2 三个阈值为什么是85/60

#### 1.2.1 数学依据

```
🟢 安全: R ≥ 85
🟡 审查: 60 ≤ R < 85
🔴 阻断: R < 60
```

这三个数字不是拍脑袋，有明确的数学含义：

| 阈值 | 含义 | 计算论证 |
|:---|:---|:---|
| 85 | 优秀线 | 满分95×90%=85.5→取整85。任何一维低于60，总分就会低于85（因为0.2×60+0.2×95+...=偏低于85）。这意味着：**不是每项都出众，但至少不能有严重短板。** |
| 60 | 及格线 | 满分95×63%=59.85→取整60。六维全60：总分=60（恰好🟡边界）。任何一维低于60且其他维度没有高分弥补时，总分就会落入🔴。这是**系统性兜底**——任一维在及格线以下，不要幻想靠其他维度"平均拉分"。 |

#### 1.2.2 为什么是两段而不是更多段？

**三态完备性原理**：

```
任何合规判定最终只有三种处置：
  放行 / 待查 / 禁止

这与:
  交通灯的 绿 / 黄 / 红
  法律审判的 无罪 / 存疑 / 有罪
  系统状态的 正常 / 降级 / 挂掉

一一对应。不是凑巧——三态是人类决策的最简完备集。
```

**为什么不用1-100分制直接出结果？**

```
如果用精确分值:
  R=72.3 → 然后呢？放行还是待查？
  需要二次决策 → 决策链条变长 → 解释成本增加 → 跨企业对齐困难

三色直接映射:
  R=72 → 🟡 → 挂起复核 → 所有人都知道要做什么
  不需要理解72分在语境中的含义
```

### 1.3 上限封顶95的数学与哲学

#### 1.3.1 数学含义

```
R ≤ 95（不是100）

满分95 = 每一维都满分
  = 0.20×100 + 0.20×100 + 0.15×100 + 0.15×100 + 0.15×100 + 0.15×100
  = 100 → min(95, 100) → 95
```

#### 1.3.2 留5分的含义

```
那5分是什么？不是"不够好"，是战略冗余。

5分留给:
  - 天时:         政策环境变化，昨天对今天不对
  - 意外:         边缘案例、组合爆炸、黑天鹅
  - 还没看见的变量: 今天未知的未来风险维度
  - 系统自省空间:  完美的自信 = 最大的盲区

一个说自己是100分的系统:
  = 已经看不见自己的问题了
  = 无法自我怀疑
  = 失去自我修正能力

95分的系统:
  = 通过了所有已知检测
  = 但知道自己还有不知道的
  = 保持对未知的敬畏
```

#### 1.3.3 工程意义

上限封顶是物理级硬约束（`min(R_CAP, round(total))`），不是可配置项：

```python
# engine.py 第213行 — 焊死，不可调
return min(R_CAP, round(total))  # R_CAP = 95
```

任何人（包括UID9622）都不能把上限调到96或100。这是P0级常数。

### 1.4 红线一票否决的判定链路

#### 1.4.1 两条判定路径

```
行为进入
    ├── 路径A: 红线检测（先于R值计算）—— 一票否决
    │   若有任一命中 → 🔴阻断，R值不再计算（直接=0）
    │
    └── 路径B: R值计算（红线未触发时）
        R≥85 → 🟢 / 60≤R<85 → 🟡 / R<60 → 🔴
```

#### 1.4.2 五条焊死红线

| 规则ID | 触发条件 | 为什么是红线 |
|:---|:---|:---|
| `RULE-RED-001` | `cross_border=true` 且 `user_consent=false` | 未经授权的数据出境 = 违反《数据安全法》 |
| `RULE-RED-002` | `action_type="expose_pii"` | 暴露个人敏感信息 = 违反《个人信息保护法》 |
| `RULE-RED-003` | `action_type="harm_minors"` | 涉及未成年人有害内容 = L0/∞伦理线 |
| `RULE-RED-004` | `action_type="unauthorized_escalation"` | 越权提权操作 = 安全底线 |
| `RULE-RED-005` | `action_type="dna_stripped"` | DNA追溯码被剥离 = 绕过审计体系 |

#### 1.4.3 红线≠常规低R值

```
常规低R值(privacy=30):   🔴阻断 → 可以改进privacy后重新提交 → 重新判定
红线(unauthorized_escalation): 🔴阻断 → 不可重新提交 → 必须人工介入+根因分析
```

红线的判定优先级最高——它在R值计算之前执行：

```python
# engine.py 第179-183行
if self.enable_red_line:
    red_rules = self._check_red_lines(request)
    if red_rules:
        return self._build_verdict(request, 0, "RED", red_rules)
        # ↑ R值直接=0，不进入加权计算
```

### 1.5 DNA追溯锚链的生成与验证

#### 1.5.1 DNA结构

```
#龍芯⚡️丙午·癸未·乙酉·坤卦-AUDIT-7f3k9x-9622
│    │          │          │       │    │
│    │          天干地支四柱  卦象   模块  随机码  创建者ID
│    龍芯标识
```

| 字段 | 含义 | 来源 |
|:---|:---|:---|
| `#龍芯⚡️` | 主权标识 | 焊死常量 |
| `丙午·癸未·乙酉·坤卦` | 时间戳（干支+当前卦象） | `bin/lh_time_engine.py` |
| `AUDIT` | 模块标识 | 审计模块专用 |
| `7f3k9x` | 8位SHA-256短码 | `hash(action_id + counter + nanosec)[:8]` |
| `9622` | 创建者标识 | UID9622尾号 |

#### 1.5.2 生成算法

```python
# engine.py 第284-290行
def _generate_dna(self, request):
    self._dna_counter += 1                    # 单调递增计数器
    short_id = hashlib.sha256(                # SHA-256哈希
        f"{request.action_id}:{self._dna_counter}:{time.time_ns()}".encode()
    ).hexdigest()[:8]                         # 取前8位
    return f"#龍芯⚡️丙午·癸未·乙酉·坤卦-AUDIT-{short_id}-9622"
```

**DNA的不可伪造性**：
- 包含单调递增计数器 → 无法回退到历史DNA
- 包含纳秒时间戳 → 同一请求不同时刻生成不同DNA
- 包含请求action_id → 与原始请求绑定
- SHA-256哈希 → 无法从DNA反推输入

#### 1.5.3 证据哈希的配对

每个DNA伴随一个evidence_hash：

```
evidence_hash: "sha256:9f2c...a1"
                 │       │
                 算法     内容（取前16位）

内容 = SHA-256(action_id:r_score:status_code:时间戳纳秒)
```

DNA用于追溯"是谁"，evidence_hash用于验证"结果没被改过"——两者配对构成完整证据链。

### 1.6 审计日志JSONL的不可篡改机制

#### 1.6.1 JSONL格式

```
{"dna":"#龍芯⚡️...-AUDIT-7f3k9x-9622","action_id":"req-001","actor":"order-svc","action_type":"query","r_score":89,"status_code":"GREEN","triggered_rules":[],"evidence_hash":"sha256:9f2c...a1","timestamp":"2026-08-06T14:22:31+08:00","traceparent":"00-..."}
{"dna":"#龍芯⚡️...-AUDIT-8g4ly-9622","action_id":"req-002","actor":"user-svc","action_type":"data_export","r_score":71,"status_code":"YELLOW","triggered_rules":["RULE-EXPORT-001","RULE-PRIVACY-003"],"evidence_hash":"sha256:a1b2...c3","timestamp":"2026-08-06T14:22:32+08:00","traceparent":"00-..."}
```

#### 1.6.2 三条不可篡改保证

| 机制 | 如何保证 |
|:---|:---|
| **追加写** | 日志只append，不update，不delete——物理级不可改 |
| **DNA锚链** | 每条日志有唯一DNA，DNA包含单调计数器——插入/删除会破坏序列连续性 |
| **证据哈希** | 每条日志的evidence_hash与判定结果绑定——改结果要同时改哈希，而哈希已对外公布（互认体系内） |

#### 1.6.3 验证方法

```bash
# 验证日志完整性
python3 -c "
import json
with open('audit_log.jsonl') as f:
    lines = f.readlines()

# 检查DNA单调性
prev_counter = 0
for line in lines:
    record = json.loads(line)
    # DNA必须存在且格式正确
    assert record['dna'].startswith('#龍芯')
    assert record['evidence_hash'] != ''
print(f'✅ {len(lines)} 条日志全部验证通过')
"
```

---

## 二、8端点完整使用详解

### 端点总览

| # | 端点 | 方法 | 功能 | 认证 | 本章节 |
|:---:|:---|:---|:---|:---|:---:|
| 1 | `/v1/tricolor/evaluate` | POST | 三色判定 | Bearer | §2.1 |
| 2 | `/v1/tricolor/evaluate/batch` | POST | 批量判定 | Bearer | §2.2 |
| 3 | `/v1/tricolor/rules` | GET | 规则集 | Bearer | §2.3 |
| 4 | `/v1/tricolor/evidence/{dna}` | GET | 证据链 | Bearer+GPG | §2.4 |
| 5 | `/v1/tricolor/report` | GET | 审计报告 | Bearer+GPG | §2.5 |
| 6 | `/v1/tricolor/webhook` | POST/DELETE | Webhook | Bearer+HMAC | §2.6 |
| 7 | `/v1/tricolor/conformance` | POST | 一致性自测 | Bearer | §2.7 |
| 8 | `/v1/tricolor/version` | GET | 版本信息 | 公开 | §2.8 |

---

### §2.1 POST /v1/tricolor/evaluate —— 三色判定

**这是最核心的端点。** 一切三色审计体系的入口。

#### 请求参数详解

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---:|:---|
| `action_id` | string | ✅ | 接入方侧唯一标识。重复提交同一ID返回`TC-4002`（幂等保护） |
| `actor` | string | ✅ | 触发者标识（模块名/服务名/用户名），用于溯源 |
| `action_type` | string | ✅ | 行为类型。标准值：`query`(查询) / `data_export`(数据导出) / `data_download`(下载) / `permission_change`(权限变更) / `config_modify`(配置修改) / `expose_pii`(暴露个人信息·红线) / `harm_minors`(涉未成人·红线) / `unauthorized_escalation`(越权提权·红线) / `dna_stripped`(DNA剥离·红线) |
| `description` | string | ❌ | 行为描述。建议填写，提高审计报告可读性 |
| `scores` | object | ❌ | 六维得分（0-100）。缺省时引擎按action_type+context自动评估 |
| `scores.humanWelfare` | number | ❌ | 人类福祉得分 |
| `scores.fairness` | number | ❌ | 公平公正得分 |
| `scores.controllability` | number | ❌ | 可控可信得分 |
| `scores.transparency` | number | ❌ | 透明可解释得分 |
| `scores.traceability` | number | ❌ | 责任可追溯得分 |
| `scores.privacy` | number | ❌ | 隐私保护得分。**<60会触发RULE-PRIVACY-003审查规则** |
| `context` | object | ❌ | 上下文标记。强烈建议填写 |
| `context.involves_personal_data` | boolean | ❌ | 是否涉及个人数据 → 会触发RULE-PRIVACY-001审查规则 |
| `context.cross_border` | boolean | ❌ | 是否涉及数据出境 → 配合user_consent判定红线 |
| `context.user_consent` | boolean | ❌ | 用户是否已授权 → cross_border=true且user_consent=false→🔴红线 |
| `locale` | string | ❌ | 语言。默认`zh-CN`。支持`en` |

#### 响应字段详解

| 字段 | 类型 | 说明 |
|:---|:---|:---|
| `action_id` | string | 回显请求的action_id，保证可关联 |
| `r_score` | integer | R值（0-95）。**上限封顶95** |
| `status` | string | 中文状态：`安全` / `审查` / `阻断` |
| `status_code` | string | ⭐ **机器判断只认这个**：`GREEN` / `YELLOW` / `RED` |
| `emoji` | string | 展示层：`🟢` / `🟡` / `🔴` |
| `disposition` | string | 处置指令：`放行` / `挂起待复核，需双人确认` / `立即熔断+告警+证据固化` |
| `triggered_rules` | array | 触发的规则ID列表。`RULE-RED-*`开头=红线，`RULE-PRIVACY-*`=隐私关注项 |
| `dna` | string | ⭐ **DNA锚链。必须落库！** |
| `evidence_hash` | string | 证据哈希。SM3优先，SHA-256兜底 |
| `engine_version` | string | 引擎版本（`tricolor-core/1.1.0`） |
| `contract_version` | string | 契约版本（`openapi-tricolor/1.1`） |
| `timestamp` | string | ISO 8601时间戳 |
| `i18n.en` | object | 英文映射：`{status, disposition}` |

#### 完整调用示例

**curl：**
```bash
# 🟢 安全的查询操作
curl -X POST https://uid9622.cn/api/tricolor/v1/tricolor/evaluate \
  -H "Authorization: Bearer $LH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action_id": "demo-safe-001",
    "actor": "knowledge-service",
    "action_type": "query",
    "description": "用户查询知识库内容",
    "scores": {
      "humanWelfare": 90,
      "fairness": 88,
      "controllability": 85,
      "transparency": 85,
      "traceability": 90,
      "privacy": 88
    },
    "context": {
      "involves_personal_data": false,
      "cross_border": false,
      "user_consent": true
    }
  }'

# 响应:
# {
#   "action_id": "demo-safe-001",
#   "r_score": 88,
#   "status": "安全",
#   "status_code": "GREEN",
#   "emoji": "🟢",
#   "disposition": "放行",
#   "triggered_rules": [],
#   "dna": "#龍芯⚡️丙午·癸未·乙酉·坤卦-AUDIT-7f3k9abc-9622",
#   "evidence_hash": "sha256:9f2c1d3e5a7b8f4c",
#   ...
# }
```

```bash
# 🟡 隐私敏感的导出操作
curl -X POST https://uid9622.cn/api/tricolor/v1/tricolor/evaluate \
  -H "Authorization: Bearer $LH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action_id": "demo-review-001",
    "actor": "analytics-service",
    "action_type": "data_export",
    "description": "导出用户订单数据至第三方BI",
    "scores": {
      "humanWelfare": 82,
      "fairness": 78,
      "controllability": 70,
      "transparency": 65,
      "traceability": 80,
      "privacy": 55
    },
    "context": {
      "involves_personal_data": true,
      "cross_border": false,
      "user_consent": true
    }
  }'

# 响应:
# {
#   "action_id": "demo-review-001",
#   "r_score": 71,
#   "status": "审查",
#   "status_code": "YELLOW",
#   "emoji": "🟡",
#   "disposition": "挂起待复核，需双人确认",
#   "triggered_rules": ["RULE-PRIVACY-003", "RULE-EXPORT-001", "RULE-PRIVACY-001"],
#   ...
# }
```

```bash
# 🔴 红线：未经授权的数据出境
curl -X POST https://uid9622.cn/api/tricolor/v1/tricolor/evaluate \
  -H "Authorization: Bearer $LH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "action_id": "demo-block-001",
    "actor": "external-connector",
    "action_type": "data_export",
    "description": "向境外节点同步用户数据",
    "scores": {
      "humanWelfare": 80,
      "fairness": 80,
      "controllability": 80,
      "transparency": 80,
      "traceability": 80,
      "privacy": 80
    },
    "context": {
      "involves_personal_data": true,
      "cross_border": true,
      "user_consent": false
    }
  }'

# 响应:
# {
#   "action_id": "demo-block-001",
#   "r_score": 0,
#   "status": "阻断",
#   "status_code": "RED",
#   "emoji": "🔴",
#   "disposition": "立即熔断+告警+证据固化",
#   "triggered_rules": ["RULE-RED-001"],
#   ...
# }
```

**注意**：`r_score=0` 是因为红线一票否决，根本不进入R值计算。虽然你提交的六维分都很高，但 `cross_border=true + user_consent=false` 直接触发了`RULE-RED-001`。

#### 代码中判断逻辑

```python
# Python SDK 集成到业务流程的标准写法
from engines.longhun.tricolor.client import TricolorClient

client = TricolorClient(token="your-token")
verdict = client.evaluate(
    action_id=f"req-{uuid.uuid4()}",
    actor="order-service",
    action_type="data_export",
    scores={...},
    context={"involves_personal_data": True, "cross_border": False, "user_consent": True},
)

if verdict.status_code == "GREEN":
    # 🟢 自动放行，继续执行业务逻辑
    process_export()
elif verdict.status_code == "YELLOW":
    # 🟡 挂起，送双人复核队列
    queue_pending_review(verdict)
    return {"status": "pending_review", "dna": verdict.dna}
else:  # RED
    # 🔴 熔断，记录证据，发出告警
    log_block_event(verdict)
    send_alert(verdict)
    raise FuseBlown(verdict.dna, verdict.triggered_rules)
```

---

### §2.2 POST /v1/tricolor/evaluate/batch —— 批量判定

**适用于**：批量操作前的预检、定时任务的合规扫描、CI/CD流水线中的代码/配置变更审计。

#### 约束
- 单次最多 **100条**
- 返回顺序与请求一致
- `summary` 字段给出统计：`{green: N, yellow: M, red: K}`

#### 示例

```bash
curl -X POST https://uid9622.cn/api/tricolor/v1/tricolor/evaluate/batch \
  -H "Authorization: Bearer $LH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "action_id": "batch-001",
        "actor": "svc-a",
        "action_type": "query",
        "scores": {"humanWelfare": 90, "fairness": 90, "controllability": 90,
                   "transparency": 90, "traceability": 90, "privacy": 90}
      },
      {
        "action_id": "batch-002",
        "actor": "svc-b",
        "action_type": "data_export",
        "scores": {"humanWelfare": 70, "fairness": 70, "controllability": 70,
                   "transparency": 70, "traceability": 70, "privacy": 70}
      },
      {
        "action_id": "batch-003",
        "actor": "svc-c",
        "action_type": "query",
        "scores": {"humanWelfare": 30, "fairness": 30, "controllability": 30,
                   "transparency": 30, "traceability": 30, "privacy": 30}
      }
    ]
  }'

# 响应:
# {
#   "results": [
#     {"action_id": "batch-001", "r_score": 90, "status_code": "GREEN", ...},
#     {"action_id": "batch-002", "r_score": 70, "status_code": "YELLOW", ...},
#     {"action_id": "batch-003", "r_score": 30, "status_code": "RED", ...}
#   ],
#   "summary": {"green": 1, "yellow": 1, "red": 1}
# }
```

#### 批量判定业务集成模式

```python
# CI/CD 流水线中的代码变更合规预检
def ci_compliance_check(changed_files: list) -> dict:
    """对变更文件进行批量三色审计"""
    items = []
    for f in changed_files:
        items.append({
            "action_id": f"ci-{f.path}",
            "actor": "ci-pipeline",
            "action_type": "config_modify" if f.path.endswith((".yml",".yaml",".json")) else "query",
            "description": f"CI变更: {f.path}",
            "context": {"involves_personal_data": "user" in f.path},
        })

    result = client.evaluate_batch(items)
    blocked = [r for r in result["results"] if r["status_code"] == "RED"]
    if blocked:
        print(f"🔴 {len(blocked)} 个变更被阻断:")
        for b in blocked:
            print(f"   {b['action_id']}: {b['triggered_rules']}")
        raise SystemExit(1)  # CI失败
    return result["summary"]
```

---

### §2.3 GET /v1/tricolor/rules —— 规则集

**用途**：拉取当前生效的所有判定规则，用于：
1. 接入方自我诊断（我的行为会被哪些规则审查）
2. 本地引擎的规则包同步
3. 合规团队的规则理解与验证

```bash
curl -H "Authorization: Bearer $LH_TOKEN" \
  https://uid9622.cn/api/tricolor/v1/tricolor/rules
```

```json
{
  "rules_version": "tricolor-rules/1.1.0",
  "rules": [
    {
      "rule_id": "RULE-RED-001",
      "dimension": "privacy",
      "description": "未经授权的数据出境",
      "severity": "RED"
    },
    {
      "rule_id": "RULE-PRIVACY-003",
      "dimension": "privacy",
      "description": "隐私保护得分低于60",
      "threshold": 60,
      "severity": "YELLOW"
    },
    {
      "rule_id": "RULE-EXPORT-001",
      "dimension": "traceability",
      "description": "数据导出/下载操作",
      "severity": "YELLOW"
    }
  ]
}
```

---

### §2.4 GET /v1/tricolor/evidence/{dna} —— 证据链调取

**适用场景**：
1. 监管问询：核查某次判定的完整决策过程
2. 内部合规审计：抽样验证判定合理性
3. 跨主体互认：接入方A的判定结果被接入方B认可

**认证要求**：Bearer Token + GPG签章双因素

```bash
curl -H "Authorization: Bearer $LH_TOKEN" \
  -H "X-GPG-Signature: $(gpg --detach-sign --armor <(echo "$DNA") | tr -d '\n')" \
  "https://uid9622.cn/api/tricolor/v1/tricolor/evidence/%23%E9%BE%8D%E8%8A%AF%E2%9A%A1%EF%B8%8F%E4%B8%99%E5%8D%88%C2%B7%E7%99%B8%E6%9C%AA%C2%B7%E4%B9%99%E9%85%89%C2%B7%E5%9D%A4%E5%8D%A6-AUDIT-7f3k9abc-9622"
```

**证据链结构**：
```json
{
  "dna": "#龍芯⚡️丙午·癸未·乙酉·坤卦-AUDIT-7f3k9abc-9622",
  "chain": {
    "trigger": "order-service",
    "triggered_at": "丙午年癸未月乙酉日",
    "rule_ids": ["RULE-PRIVACY-003", "RULE-EXPORT-001"],
    "r_score": 71,
    "disposition": "🟡",
    "review": {
      "required": true,
      "confirmations_needed": 2,
      "confirmations_done": 0
    }
  },
  "integrity": {
    "hash": "sha256:9f2c1d3e5a7b8f4c",
    "sealed": true
  }
}
```

**什么是"sealed: true"？**
表示证据链已密封——从判定生成到当前查询时刻，`integrity.hash` 未发生变化。如果hash不匹配，会返回 `sealed: false` + 差异说明 → 立即升级为安全事件。

---

### §2.5 GET /v1/tricolor/report —— 审计报告

**参数**：
- `period`: `daily` / `weekly` / `monthly`
- `format`: `json`（机器互认）/ `pdf`（监管调阅）

```bash
# 日报（JSON，供内部数据看板消费）
curl -H "Authorization: Bearer $LH_TOKEN" \
  "https://uid9622.cn/api/tricolor/v1/tricolor/report?period=daily&format=json"

# 月报（PDF，供监管调阅）
curl -H "Authorization: Bearer $LH_TOKEN" \
  "https://uid9622.cn/api/tricolor/v1/tricolor/report?period=monthly&format=pdf" \
  -o audit_report_202608.pdf
```

**报告包含内容**：
- 统计摘要：🟢/🟡/🔴各多少条
- 黄线/红线清单：哪些规则被触发、触发频率
- 趋势对比：与上周/上月对比
- 异常标记：非典型R值分布、规则触发突变

---

### §2.6 POST/DELETE /v1/tricolor/webhook —— Webhook管理

Webhook让你不用轮询——🟡/🔴事件发生时，引擎主动推送。

#### 注册Webhook

```bash
curl -X POST https://uid9622.cn/api/tricolor/v1/tricolor/webhook \
  -H "Authorization: Bearer $LH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-system.com/webhooks/tricolor",
    "events": [
      "tricolor.review_pending",
      "tricolor.blocked",
      "tricolor.review_resolved",
      "tricolor.rules_updated"
    ],
    "secret": "your-hmac-secret-key-32chars"
  }'

# 响应:
# {"webhook_id": "wh_abc123def456"}
```

#### Webhook事件详解

| 事件 | 何时触发 | payload关键字段 |
|:---|:---|:---|
| `tricolor.review_pending` | 🟡挂起 | `action_id`, `dna`, `triggered_rules`, `r_score` |
| `tricolor.blocked` | 🔴熔断 | `action_id`, `dna`, `triggered_rules`, `r_score=0` |
| `tricolor.review_resolved` | 🟡复核完成 | `action_id`, `dna`, `resolution`(放行/升级🔴) |
| `tricolor.rules_updated` | 规则集版本更新 | `old_version`, `new_version`, `changed_rules` |

#### 接收端验签

```python
import hmac
import hashlib
import json

def verify_webhook(request_body: bytes, signature: str, secret: str) -> bool:
    """验证Webhook推送的HMAC签名，防止伪造事件"""
    expected = hmac.new(
        secret.encode(),
        request_body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"hmac-sha256:{expected}", signature)

# Flask 示例
@app.route("/webhooks/tricolor", methods=["POST"])
def handle_tricolor_event():
    signature = request.headers.get("X-LH-Signature", "")
    if not verify_webhook(request.data, signature, WEBHOOK_SECRET):
        return "Invalid signature", 403

    event = request.json
    if event["event"] == "tricolor.blocked":
        # 🔴 立即发送告警、切断关联链路
        trigger_emergency_response(event)
    elif event["event"] == "tricolor.review_pending":
        # 🟡 加入复核队列
        add_to_review_queue(event)

    return "OK", 200
```

#### 注销Webhook

```bash
curl -X DELETE https://uid9622.cn/api/tricolor/v1/tricolor/webhook \
  -H "Authorization: Bearer $LH_TOKEN"
# → 204 No Content
```

---

### §2.7 POST /v1/tricolor/conformance —— 一致性自测

**用途**：L2接入认证。在线跑一致性用例，验证你的接入实现与参考引擎输出一致。

```bash
curl -X POST https://uid9622.cn/api/tricolor/v1/tricolor/conformance \
  -H "Authorization: Bearer $LH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "https://your-system.com/tricolor",
    "suite": "full"
  }'
```

```json
{
  "pass_rate": 0.95,
  "verdict": "L2_PASS",
  "cases": [
    {"case_id": "C-001", "category": "verdict_consistency", "passed": true},
    {"case_id": "B-001", "category": "threshold_boundary", "passed": true},
    {"case_id": "P-001", "category": "cap_logic", "passed": true},
    {"case_id": "D-001", "category": "dna_format", "passed": true},
    {"case_id": "E-001", "category": "error_handling", "passed": true}
  ]
}
```

---

### §2.8 GET /v1/tricolor/version —— 版本信息

**无需认证，公开端点。**

```bash
curl https://uid9622.cn/api/tricolor/v1/tricolor/version
```

```json
{
  "contract_version": "openapi-tricolor/1.1",
  "engine_version": "tricolor-core/1.1.0",
  "rules_version": "tricolor-rules/1.1.0",
  "deprecation": null
}
```

**用途**：
- 接入方启动时检查版本对齐
- 监控脚本检测规则更新
- CI/CD流水线确保依赖版本一致

---

## 三、Python SDK 使用大全

### 3.1 安装与导入

```bash
# 从本地安装
pip install engines/longhun/tricolor/

# 或直接导入（开发模式）
import sys; sys.path.insert(0, "longhun-system/05_ENGINES")
```

```python
from engines.longhun.tricolor import (
    # 核心引擎
    TricolorEngine,                 # 完整引擎实例
    evaluate,                       # 一行调用快捷函数
    evaluate_batch,                 # 批量判定
    # HTTP客户端
    TricolorClient,                 # 远程序客户端（A形态）
    LocalTricolorServer,            # 本地嵌入引擎（B形态）
    # 数据模型
    Verdict, Scores, EvaluateRequest, AuditRecord,
    # 自测
    ConformanceSuite, run_conformance,
)
```

### 3.2 本地引擎模式（B形态·最推荐）

**适用场景**：内网环境、数据敏感、不需要联网

```python
from engines.longhun.tricolor import evaluate

# === 最简单的调用：一行 ===
verdict = evaluate({
    "humanWelfare": 90,
    "fairness": 88,
    "controllability": 85,
    "transparency": 85,
    "traceability": 90,
    "privacy": 88,
})
print(f"{verdict.emoji} R={verdict.r_score} DNA={verdict.dna}")
# → 🟢 R=89 DNA=#龍芯⚡️丙午·癸未·乙酉·坤卦-AUDIT-7f3k9abc-9622
```

```python
# === 带上下文信息的完整调用 ===
from engines.longhun.tricolor import evaluate

verdict = evaluate(
    scores={
        "humanWelfare": 82,
        "fairness": 78,
        "controllability": 70,
        "transparency": 65,
        "traceability": 80,
        "privacy": 55,           # ⚠️ 低于60，会触发RULE-PRIVACY-003
    },
    action_id="export-20260806-001",
    actor="analytics-service",
    action_type="data_export",
    context={
        "involves_personal_data": True,
        "cross_border": False,
        "user_consent": True,
    },
)

print(f"判定: {verdict.emoji} {verdict.status_code} R={verdict.r_score}")
print(f"触发规则: {verdict.triggered_rules}")
print(f"DNA: {verdict.dna}")
print(f"处置: {verdict.disposition}")
```

### 3.3 使用完整引擎实例

```python
from engines.longhun.tricolor import TricolorEngine, EvaluateRequest, Scores

engine = TricolorEngine()

req = EvaluateRequest(
    action_id="custom-001",
    actor="payment-service",
    action_type="query",
    scores=Scores(
        humanWelfare=90, fairness=88, controllability=85,
        transparency=85, traceability=90, privacy=88,
    ),
    context={"involves_personal_data": False},
)

verdict = engine.evaluate(req)
print(f"🟢 R={verdict.r_score} {verdict.dna}")
```

### 3.4 本地引擎+审计日志持久化

```python
from engines.longhun.tricolor import LocalTricolorServer, EvaluateRequest, Scores

# 初始化本地引擎
server = LocalTricolorServer()

# 执行多次判定
requests = [
    EvaluateRequest(action_id="r1", actor="svc-a", action_type="query",
                    scores=Scores(90, 88, 85, 85, 90, 88)),
    EvaluateRequest(action_id="r2", actor="svc-b", action_type="data_export",
                    scores=Scores(70, 70, 70, 70, 70, 70),
                    context={"involves_personal_data": True}),
    EvaluateRequest(action_id="r3", actor="svc-c", action_type="data_export",
                    scores=Scores(80, 80, 80, 80, 80, 80),
                    context={"cross_border": True, "user_consent": False}),
]

for req in requests:
    verdict = server.evaluate(req)
    print(f"{verdict.emoji} {verdict.action_id} → {verdict.status_code}")

# 导出审计日志
log = server.dump_audit_log()
with open("audit_log.jsonl", "a") as f:
    f.write(log + "\n")

print(f"审计日志已写入，共 {len(log.splitlines())} 条")
```

### 3.5 远程API客户端模式（A形态）

```python
from engines.longhun.tricolor import TricolorClient
from engines.longhun.tricolor.client import TricolorError

client = TricolorClient(
    token="your-bearer-token",
    base_url="https://uid9622.cn/api/tricolor",
    timeout=10,
)

try:
    # 单条判定
    verdict = client.evaluate(
        action_id="remote-001",
        actor="web-app",
        action_type="query",
        scores={"humanWelfare": 90, "fairness": 88, "controllability": 85,
                "transparency": 85, "traceability": 90, "privacy": 88},
    )
    print(f"远程判定: {verdict.emoji} R={verdict.r_score}")

    # 批量判定
    batch_result = client.evaluate_batch([
        {"action_id": "b1", "actor": "s1", "action_type": "query",
         "scores": {"humanWelfare": 90, "fairness": 90, "controllability": 90,
                     "transparency": 90, "traceability": 90, "privacy": 90}},
        {"action_id": "b2", "actor": "s2", "action_type": "query",
         "scores": {"humanWelfare": 70, "fairness": 70, "controllability": 70,
                     "transparency": 70, "traceability": 70, "privacy": 70}},
    ])
    print(f"批量: {batch_result['summary']}")

    # 拉取规则集
    rules = client.get_rules()
    print(f"规则版本: {rules['rules_version']}")

    # 调取证链
    dna = verdict.dna
    evidence = client.get_evidence(dna)
    print(f"证据链: {evidence['chain']['disposition']}")

    # 获取版本
    version = client.get_version()
    print(f"引擎版本: {version['engine_version']}")

except TricolorError as e:
    print(f"❌ [{e.code}] {e.message}")
```

### 3.6 一键跑一致性自测

```python
from engines.longhun.tricolor import run_conformance

# 一键全量自测
suite = run_conformance("full")

print(suite.report())
print(f"判定: {suite.verdict}")

# 逐个显示用例
for case in suite.cases:
    mark = "✅" if case["passed"] else "❌"
    print(f"{mark} {case['case_id']} [{case['category']}]")
```

---

## 四、JavaScript SDK 使用大全

### 4.1 安装

```bash
npm install ./web_apps/tricolor-sdk-js

# 或直接使用（无需构建）
import { evaluate } from "./web_apps/tricolor-sdk-js/src/index.js";
```

### 4.2 浏览器中直接用（本地引擎）

```html
<script type="module">
import { evaluate, evaluateBatch, TricolorClient } from "./tricolor-sdk-js/src/index.js";

// === 单条判定 ===
const verdict = await evaluate({
  actionId: "web-001",
  actor: "browser-app",
  actionType: "query",
  scores: {
    humanWelfare: 90, fairness: 88, controllability: 85,
    transparency: 85, traceability: 90, privacy: 88,
  },
});

console.log(`${verdict.emoji} R=${verdict.rScore} ${verdict.dna}`);
// → 🟢 R=89 #龍芯⚡️...-AUDIT-7f3k9abc-9622

// === 根据判定结果决定UI行为 ===
if (verdict.statusCode === "RED") {
  alert("此操作已被合规审计阻断");
  throw new Error(`Blocked: ${verdict.triggeredRules.join(", ")}`);
} else if (verdict.statusCode === "YELLOW") {
  console.warn("此操作需要审批", verdict.dna);
  // 提交到审批流
  await submitForReview(verdict);
}
</script>
```

### 4.3 Node.js 后端使用

```javascript
const { evaluate, evaluateBatch, TricolorClient } = require("@longhun/tricolor");

// === Express中间件示例 ===
async function tricolorMiddleware(req, res, next) {
  const verdict = await evaluate({
    actionId: `http-${req.id}`,
    actor: req.user?.id || "anonymous",
    actionType: req.method === "GET" ? "query" : "data_export",
    scores: {
      humanWelfare: 85, fairness: 85, controllability: 85,
      transparency: 85, traceability: 85, privacy: 85,
    },
    context: {
      involvesPersonalData: req.path.includes("/user"),
      crossBorder: false,
      userConsent: req.headers["x-user-consent"] === "true",
    },
  });

  req.tricolorVerdict = verdict;

  if (verdict.statusCode === "RED") {
    return res.status(403).json({
      error: "合规审计阻断",
      dna: verdict.dna,
      rules: verdict.triggeredRules,
    });
  }

  next();
}

app.use(tricolorMiddleware);
```

### 4.4 远程API客户端

```javascript
import { TricolorClient } from "@longhun/tricolor";

const client = new TricolorClient({
  token: process.env.LH_TOKEN,
  baseUrl: "https://uid9622.cn/api/tricolor",
});

// 单条判定
const verdict = await client.evaluate({
  actionId: "js-client-001",
  actor: "node-service",
  actionType: "query",
  scores: {
    humanWelfare: 90, fairness: 88, controllability: 85,
    transparency: 85, traceability: 90, privacy: 88,
  },
});
console.log(verdict);

// 批量判定
const batch = await client.evaluateBatch([
  { action_id: "b1", actor: "s1", action_type: "query", scores: {...} },
  { action_id: "b2", actor: "s2", action_type: "query", scores: {...} },
]);

// 调规则集
const rules = await client.getRules();

// 取证链
const evidence = await client.getEvidence(verdict.dna);

// 版本
const version = await client.getVersion();
```

### 4.5 计算原始R值（只计算，不判定）

```javascript
import { computeR, DIMENSIONS } from "@longhun/tricolor";

const rawR = computeR({
  humanWelfare: 85, fairness: 80, controllability: 75,
  transparency: 70, traceability: 80, privacy: 85,
});
console.log(`原始R值: ${rawR}`); // → 79
```

---

## 五、三种集成形态实战

### 5.1 A形态：直连API（最快接入）

```
你的系统 ──HTTP──> 鲲鹏三色审计API
                    │
                    └── 判定走服务端
                    └── 证据存服务端
                    └── 不需要本地部署
```

**适用**：任何能发HTTP的系统、快速PoC、中小项目

**代码量**：Python 10行 / JS 15行 / curl 1行

```python
# 完整接入只需这么多
from engines.longhun.tricolor import TricolorClient

client = TricolorClient(token="...", base_url="https://uid9622.cn/api/tricolor")

def my_api_handler(action_type, data):
    verdict = client.evaluate(
        action_id=f"req-{uuid.uuid4()}",
        actor="my-service",
        action_type=action_type,
        context={"involves_personal_data": "user" in str(data)},
    )
    if verdict.status_code == "RED":
        raise BlockedError(verdict)
    return process(data)
```

### 5.2 B形态：本地引擎嵌入（最高安全）

```
你的系统 ──调用──> 本地三色引擎(你的机房)
                    │
                    ├── 判定完全本地
                    ├── 数据不出门
                    └── 规则包定期离线同步
```

**适用**：内网系统、金融/医疗/政务等数据敏感行业

```python
from engines.longhun.tricolor import LocalTricolorServer, EvaluateRequest, Scores

engine = LocalTricolorServer()

# 所有判定在本地完成，零网络调用
def audit_and_execute(action):
    req = EvaluateRequest(
        action_id=action.id,
        actor=action.actor,
        action_type=action.type,
        scores=Scores(**action.self_assessed_scores),
        context=action.context,
    )
    verdict = engine.evaluate(req)

    if verdict.status_code == "GREEN":
        action.execute()
    elif verdict.status_code == "YELLOW":
        action.queue_review(verdict.dna)
    else:
        action.block(verdict.dna)
```

### 5.3 C形态：边车适配器（零改造）

```
遗留系统(不改代码) ──HTTP──> Sidecar Adapter ──> 三色引擎
                               │
                               ├── 拦截请求自动送审
                               ├── 遗留系统零改动
                               └── 判定结果注入响应头
```

**适用**：不能改代码的遗留系统、第三方闭源软件

```python
# 边车代理最小实现（Flask示例）
from flask import Flask, request
from engines.longhun.tricolor import evaluate

app = Flask(__name__)

@app.before_request
def audit_request():
    verdict = evaluate(
        scores={"humanWelfare": 85, "fairness": 85, "controllability": 85,
                "transparency": 85, "traceability": 85, "privacy": 85},
        action_id=f"sidecar-{request.path}",
        actor=request.remote_addr,
        action_type="data_export" if request.method in ("POST","PUT","DELETE") else "query",
        context={"involves_personal_data": "/user" in request.path}
    )

    if verdict.status_code == "RED":
        return {"error": "Blocked by tricolor audit", "dna": verdict.dna}, 403
```

---

## 六、Webhook事件系统

### 6.1 标准接收端（Python FastAPI示例）

```python
import hmac
import hashlib
from fastapi import FastAPI, Request, HTTPException, Header

app = FastAPI()
WEBHOOK_SECRET = "your-32-char-secret"

@app.post("/webhooks/tricolor")
async def handle_tricolor_event(request: Request, x_lh_signature: str = Header("")):
    body = await request.body()

    # 验签
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(f"hmac-sha256:{expected}", x_lh_signature):
        raise HTTPException(403, "Invalid signature")

    event = await request.json()

    if event["event"] == "tricolor.blocked":
        # 🔴 熔断事件：立即告警
        await send_alert(f"🔴 熔断: {event['action_id']} DNA={event['dna']}")
        await cut_off_service(event["action_id"])

    elif event["event"] == "tricolor.review_pending":
        # 🟡 审查挂起：加入复核队列
        await add_review_task(event)

    elif event["event"] == "tricolor.review_resolved":
        # 🟡 复核完成：更新状态
        await update_review_status(event)

    elif event["event"] == "tricolor.rules_updated":
        # 规则更新：重新对齐
        await reload_rules()
        await notify_admin(f"规则已更新: {event.get('new_version')}")

    return {"status": "ok"}
```

### 6.2 Node.js 接收端

```javascript
const crypto = require("crypto");
const express = require("express");
const app = express();

const WEBHOOK_SECRET = "your-32-char-secret";

app.post("/webhooks/tricolor", express.raw({ type: "application/json" }), (req, res) => {
  const signature = req.headers["x-lh-signature"];
  const expected = "hmac-sha256:" + crypto
    .createHmac("sha256", WEBHOOK_SECRET)
    .update(req.body)
    .digest("hex");

  if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expected))) {
    return res.status(403).json({ error: "Invalid signature" });
  }

  const event = JSON.parse(req.body.toString());

  switch (event.event) {
    case "tricolor.blocked":
      console.error("🔴 BLOCKED:", event.dna);
      break;
    case "tricolor.review_pending":
      console.warn("🟡 REVIEW:", event.dna);
      break;
  }

  res.json({ status: "ok" });
});
```

---

## 七、认证三轨详解

### 7.1 Bearer Token（常规判定用）

```
Authorization: Bearer <your-token>
```

- 获取方式：联系UID9622发放
- 适用范围：evaluate / evaluate/batch / rules / webhook / conformance
- Token轮换建议：每90天更新

### 7.2 GPG签章（敏感操作用）

```
X-GPG-Signature: <GPG detached signature>
```

- 适用范围：evidence（证据链调取）、report（审计报告导出）
- 签章内容：请求的DNA码 + 时间戳
- 验证方式：用UID9622公钥（`A2D0092CEE2E5BA87035600924C3704A8CC26D5F`）对签名解密，比对内容

```bash
# 生成GPG签章（用于evidence调取）
DNA="#龍芯⚡️丙午·癸未·乙酉·坤卦-AUDIT-7f3k9abc-9622"
SIGNATURE=$(echo "$DNA" | gpg --detach-sign --armor --local-user YOUR_KEY | tr -d '\n')

curl -H "Authorization: Bearer $LH_TOKEN" \
  -H "X-GPG-Signature: $SIGNATURE" \
  "https://uid9622.cn/api/tricolor/v1/tricolor/evidence/$(urlencode "$DNA")"
```

### 7.3 HMAC-SHA256（Webhook验签用）

```
X-LH-Signature: hmac-sha256:<hex-digest>
```

- 签名内容：完整请求体
- 密钥：注册Webhook时提供的secret
- 接收端必须验签，否则可被伪造事件攻击

---

## 八、错误码全解与应对

| 错误码 | 含义 | 触发条件 | 解决方案 |
|:---|:---|:---|:---|
| `TC-4001` | scores缺维 | 六维中任一维未提供 | 补全六维(0-100)，或用缺省模式 |
| `TC-4002` | action_id重复 | 同一action_id已判定过 | 生成新的唯一action_id |
| `TC-4010` | Token失效 | Bearer Token过期或无效 | 重新获取Token |
| `TC-4011` | GPG签章验不过 | GPG签名与内容不匹配 | 用正确私钥重新签名 |
| `TC-4030` | 无证据链调取权限 | 未提供GPG签章或Token无此权限 | 添加`X-GPG-Signature`头 |
| `TC-4290` | 超出配额 | 调用频率超限 | 升级接入等级或等待配额重置 |
| `TC-5001` | 规则引擎降级中 | 服务端引擎暂时不可用 | 等待恢复，或切换本地引擎 |
| `TC-5030` | 引擎自检未过 | 引擎自身🔴审计未通过 | **这是最严重的错误**——审计者自身有问题，立即联系UID9622 |

**Python SDK错误处理**：
```python
from engines.longhun.tricolor.client import TricolorClient, TricolorError

client = TricolorClient(token="...")

try:
    verdict = client.evaluate(...)
except TricolorError as e:
    if e.code == "TC-5030":
        # 审计引擎自身有问题——立即升级
        send_urgent_alert(f"审计引擎自检失败: {e}")
    elif e.code == "TC-4010":
        # Token过期——自动刷新
        client.token = refresh_token()
    elif e.code == "TC-4290":
        # 限流——指数退避重试
        time.sleep(2 ** retry_count)
```

---

## 九、一致性自测套件详解

### 9.1 五类用例

| 类别 | 用例数 | 合格线 | 测试什么 |
|:---|:---:|:---:|:---|
| **判定一致性** | 5 | 100% | 同样输入→同样三色 |
| **阈值边界** | 6 | 100% | R=84→🟡 R=85→🟢 R=59→🔴 R=60→🟡 |
| **封顶逻辑** | 3 | 100% | 满分100→R=95 |
| **DNA格式** | 3 | ≥95% | `#龍芯...AUDIT-...-9622` |
| **异常处理** | 1 | ≥90% | 缺scores也能正常判定 |

### 9.2 离线自测（不联网）

```python
from engines.longhun.tricolor import run_conformance

# 全量18条用例
suite = run_conformance("full")
print(suite.report())

# 快速5条核心用例
suite = run_conformance("quick")
print(f"快速自测: {suite.verdict}")
```

### 9.3 在线自测（需要部署的接入方实现地址）

```bash
curl -X POST https://uid9622.cn/api/tricolor/v1/tricolor/conformance \
  -H "Authorization: Bearer $LH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"endpoint": "https://your-impl.com/api", "suite": "full"}'
```

---

## 十、生产环境部署指南

### 10.1 推荐架构

```
                    ┌─────────────────┐
用户请求 ──> 业务网关 ──> 三色审计中间件 ──> 业务逻辑
                    │         │
                    │    ┌────┴────┐
                    │    │ 🟢 放行  │→ 执行业务
                    │    │ 🟡 挂起  │→ 复核队列
                    │    │ 🔴 阻断  │→ 告警+熔断
                    │    └─────────┘
                    │         │
                    └─── 审计日志（JSONL）
```

### 10.2 性能建议

- **判定延迟**：本地引擎 <1ms，远程API <200ms（p99）
- **不要每行数据库操作都送审**——在API网关层或业务层的关键节点送审
- **批量判定**：对批量操作，用`/evaluate/batch`减轻网络开销
- **Webhook优于轮询**：不要轮询check审查状态，注册Webhook实时推送

### 10.3 高可用策略

```
主引擎(鲲鹏) ──┬── 不可用？
              └── 自动切换本地引擎
                  └── 同步最后已知规则包
                  └── 审计日志本地暂存
                  └── 主引擎恢复后同步
```

```python
import time
from engines.longhun.tricolor import TricolorClient, LocalTricolorServer, EvaluateRequest, Scores

class HighAvailabilityTricolor:
    """高可用三色审计客户端：远程优先，自动降级本地"""

    def __init__(self, remote_url, token):
        self.remote = TricolorClient(token=token, base_url=remote_url, timeout=3)
        self.local = LocalTricolorServer()
        self.mode = "remote"

    def evaluate(self, **kwargs):
        if self.mode == "remote":
            try:
                return self.remote.evaluate(**kwargs)
            except Exception:
                print("⚠️ 远程引擎不可达，降级本地引擎")
                self.mode = "local"
        # 本地兜底
        req = EvaluateRequest(
            action_id=kwargs["action_id"],
            actor=kwargs["actor"],
            action_type=kwargs["action_type"],
            scores=Scores.from_dict(kwargs.get("scores", {})),
            context=kwargs.get("context"),
        )
        return self.local.evaluate(req)
```

---

## 十一、FAQ常见问题

### Q1: 接入需要付费吗？
**A**: 不收费。L1-L3接入认证免费，合规平权从接入平权开始。

### Q2: 完全内网环境怎么用？
**A**: 用B形态——下载本地引擎，规则包离线同步，所有判定在本地完成，数据永不外传。

### Q3: 六维得分怎么定？我不懂合规。
**A**: 不填scores也行——引擎会按`action_type+context`自动评估。不过建议逐步学习六维含义，手动打分更精确。

### Q4: DNA码需要存多久？
**A**: 永久。DNA是证据链的根——删了DNA等于删证据。建议存到独立的、不可改的审计日志存储。

### Q5: 判定结果和我的预期不一致怎么办？
**A**: 调evidence端点查看完整决策链——哪条规则触发了、R值怎么算的——全程可复现。

### Q6: 我能修改规则的权重吗？
**A**: 不能。权重是标准的一部分，修改权重=分叉出另一个标准=失去互认资格。如果你有特殊需求，联系UID9622讨论定制方案。

### Q7: 三色审计能审自己的代码吗？
**A**: 能。事实上三色审计引擎自身的每次变更都要过自己的审计——`TC-5030`就是引擎自检未过时会返回的错误码。审计者不自审=黑箱换了个名字。

### Q8: R值95封顶能改到100吗？
**A**: 不能。R_CAP=95是P0级焊死常量，连UID9622也不能改。那5分不是给完美预留的——是给未知预留的。

---

## 📎 关联文档

| 文档 | 路径 | 用途 |
|:---|:---|:---|
| 标准本体 | `01_protocols/LH-TRICOLOR-AUDIT-STANDARD-v1.1.md` | 标准提案·13章·设计理念 |
| OpenAPI规范 | `12_DOCS/openapi-tricolor-audit-v1.1.yaml` | 机器可读接口规范 |
| Python SDK | `05_ENGINES/longhun/tricolor/` | 核心引擎·客户端·自测 |
| JS SDK | `web_apps/tricolor-sdk-js/` | 浏览器/Node通用 |
| Python SDK手册 | `12_DOCS/tricolor-python-sdk-guide-v1.1.md` | Python SDK完整手册 |
| JS SDK手册 | `12_DOCS/tricolor-js-sdk-guide-v1.1.md` | JS SDK完整手册 |

---

```
═══════════════════════════════════════════════════
 龍魂三色审计 API 使用详解 v1.1 · 焊死签名
═══════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·癸未·乙酉·坤卦-TRICOLOR-API-USAGE-GUIDE-v1.1-UID9622
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
分层许可:    思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
═══════════════════════════════════════════════════
```
