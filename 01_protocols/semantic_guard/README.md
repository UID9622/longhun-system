> DNA: #龍芯⚡️丙午·丙申·癸酉·乙卯·临-SEMANTIC-GUARD-README-v∞-5E93CB9A
> CREATOR: UID9622
> PROTOCOL: 龍魂君子协议 · CC BY-NC-SA 4.0 · L0 世界老百姓最高

# 龍魂语义安全闸规则库

项目规范源目录，所有语义安全闸规则必须按 `rule_template_schema.json` 填写，并通过 `bin/lh_sg_auditor.py` 审核。Agent/ASI 加载规则前必须先跑审核，不通过则拒绝加载。

## 文件说明

| 文件 | 用途 |
|------|------|
| `rule_template_schema.json` | JSON Schema v1.1，强制字段、DNA格式、动作注册表、十闸审计链 |
| `rule_template.example.json` | 最细模板示例，新增规则库时复制并按字段填写 |
| `tongxin_guard_rules.json` | 当前生效的通心译语义安全闸规则库 |
| `bin/lh_sg_auditor.py` | 规则审核脚本 |
| `bin/lh_sg_generator.py` | 规则生成器，按模板生成单条规则并可追加 |
| `bin/lh_sg_normalize.py` | 旧规则迁移/归一化脚本 |
| `bin/lh_sg_sync.py` | 同步项目源到 `~/.longhun/` 与 `~/.kimi-code/` 技能目录 |
| `bin/lh_sg_startup_guard.py` | Agent/ASI 启动守卫：5秒内审核，失败 Exit 1 |

## 快速使用

```bash
# 审核项目源规则库
python3 bin/lh_sg_auditor.py

# 生成单条规则（输出到控制台）
python3 bin/lh_sg_generator.py \
  --id MY_NEW_RULE \
  --category anti_revisionism \
  --name "规则名称" \
  --description "不少于20字的规则说明，阐明识别场景与处置方式。" \
  --patterns "示例正则.*风险"

# 生成并追加到规则库
python3 bin/lh_sg_generator.py ... --output append

# 迁移旧规则
python3 bin/lh_sg_normalize.py --source ~/.longhun/config/semantic_guard/tongxin_guard_rules.json

# 同步到共享/技能目录
python3 bin/lh_sg_sync.py
```

## 模板必填字段

### 规则库级别

- `dna`：v∞ 干支卦格式，如 `#龍芯⚡️丙午·丙申·癸酉·乙卯·临-MODULE-ACTION-HASH8`
- `version`：SemVer
- `description`：不少于 20 字
- `updated_at`：ISO 8601
- `confirm_code`：`#CONFIRM🌌9622-ONLY-ONCE🧬...`
- `categories`：每个分类必须有 `name`、`description`（≥10 字）、`default_severity`、`default_action`
- `actions`：动作注册表，每个动作必须有 `name`、`description`、`target_engine`
- `agent_chain`：GATE-01 ~ GATE-10 十闸审计链
- `rules`：至少一条规则

### 单条规则级别

- `id`：大写字母、数字、下划线，首字符大写
- `category`：必须存在于 `categories`
- `name`：规则中文名称
- `description`：不少于 20 字
- `patterns`：至少一个有效正则
- `severity`：`🟢`、`🟡`、`🔴`
- `action`：必须存在于 `actions`
- `priority`：0-100 整数
- `enabled`：布尔值
- `version`：SemVer
- `metadata.evidence_examples`：至少一条示例
- `audit.reviewer`：审核通过时必须是 `UID9622`

## 铁律

- 任何 Agent/ASI 加载规则前 → `lh_sg_auditor.py` 不通过 = 拒绝加载。
- 新增规则必须走 `lh_sg_generator.py`，确保格式永远一致。
- 规则变更后必须 `lh_sg_sync.py` 同步到共享/技能目录。
