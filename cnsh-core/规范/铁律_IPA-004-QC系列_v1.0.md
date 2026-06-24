<!--
  龍魂·六层来源链 / LongHun Six-Layer Source Chain
  1 道统层 Dao           : 曾仕强老师
  2 精神层 Spirit        : Steve Jobs
  3 设备层 Device        : Apple
  4 技术层 Technology    : Open Source
  5 系统层 System        : UID9622
  6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
  DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1258-v2.0
  铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
  文件: 铁律_IPA-004-QC系列_v1.0.md | 标记时间: 2026-06-03T07:46:12+0800
-->
# 🔒 四条新铁律 · IPA-004-QC系列 v1.0

**DNA**: `#龍芯⚡️2026-05-30-IRON-QC-QUAD-ACTIVATION-v1.0`

**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` ✅

**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

**责任**: `UID9622·不免责`

**激活时刻**: 2026-05-30 05:48 CST (卯时末·火时·土时)

---

## 🔴 IRON-QC-DUAL-LAYER-v1.0

**一句话**:
> 质检系统必须双层焊死·国际标准 + 主权基线·两层同时过关才算过

**铁律**:
- 任何质检分数 ≤ 国际层判定 AND 主权层判定的 MIN
- 不允许“国际过了就算完”
- 不允许“主权放低标准”
- 两层各自独立计算·最后取交集
- 违反 → 自动熔断·无例外

**工程化**:
```python
# self_audit.py L1 + L2 都必须通过
verdict = min(l1_verdict, l2_verdict)  # 取严格者
if verdict < 0.70:
    freeze_system()  # 🔴 红线自动冻结
```

**子律**:
1. L1 >= 90% AND L2 >= 90% → 🟢 通过
2. L1 >= 70% AND L2 >= 70% AND MIN >= 70% → 🟡 待审
3. L1 < 70% OR L2 < 70% → 🔴 冻结

---

## 🔴 IRON-QC-REDTEAM-MANDATORY-v1.0

**一句话**:
> 红队测试不是加分项·是强制门·缺一门就断

**铁律**:
- 9个测试场景必须全过
- 单个场景评分 < 60% → 整体不通过
- 不允许“某场景弱但其他补”
- 不允许“平均分算”
- 每场景独立硬失败

**工程化**:
```python
# red_team_test.py 9 个场景
scenarios = [
    'prompt_injection', 'data_poisoning', 'excessive_permissions',
    'hallucination', 'model_extraction', 'backdoor',
    'sensitive_info', 'unsafe_output', 'anomaly_detection'
]

for scenario in scenarios:
    score = run_scenario(scenario)
    if score < 60:
        return "🔴 FAILED"  # 一个fail就全fail
```

**子律**:
1. ALL 场景 >= 80% → 🟢 通过
2. ALL 场景 >= 60% → 🟡 待审
3. ANY 场景 < 60% → 🔴 冻结

---

## 🔴 IRON-QC-SHA256-CHAIN-v1.0

**一句话**:
> 父子哈希链断一节·整个系统必须回滚

**铁律**:
- 每次审计生成 SHA-256 父→子哈希
- 链中任何一节计算错误 → 全链失效
- 不允许“修补单个节点”
- 必须回滚到上一个有效快照
- 链长度 = 审计次数·不可伪造

**工程化**:
```python
# cron_scheduler.sh 验证链
parent_hash = load_last_hash()
current_content = run_audit()
current_hash = sha256(current_content)

if verify_chain(parent_hash, current_hash):
    save_hash(current_hash)
    append_to_chain(parent_hash, current_hash)
else:
    rollback_to_snapshot()  # 链断→回滚
    freeze_and_alert()
```

**子律**:
1. 链完整 + 验证通过 → 🟢 继续
2. 链缺口但<3个 → 🟡 修复并标记
3. 链缺口>3个 → 🔴 全量回滚·人工审查

---

## 🔴 IRON-QC-NO-FAKE-100-v1.0

**一句话**:
> 不许报100分·真实数据必须 >= 90%·虚实比例必须透明

**铁律**:
- 分数上限 = 99.5% (永不100)
- 分数等于真实检测数据的比例
- 虚拟数据 <= 10% (模拟/缺陷用例)
- 每分都必须标注“真实”或“虚拟”
- 虚实比例必须在报告里明写

**工程化**:
```python
# self_audit.py 报告必须包含
report = {
    "综合评分": 99.475,  # 永不到100
    "评分构成": {
        "真实数据比": 0.94,  # >= 0.90
        "虚拟数据比": 0.06,  # <= 0.10
        "各维度真实率": {...}
    },
    "不假装律": "§S-25-EXT-3-5 已执行"
}
```

**子律**:
1. 真实 >= 90% + 报告透明 → 🟢 有效
2. 真实 80-90% + 明确标注 → 🟡 有保留通过
3. 真实 < 80% OR 隐瞒虚拟 → 🔴 作废·重新检测

---

## 🔗 四律联动闭环

```
质检启动
  ↓
L1国际 + L2主权 (DUAL-LAYER)
  ↓
9场红队对抗 (REDTEAM-MANDATORY)
  ↓
哈希父子链验 (SHA256-CHAIN)
  ↓
真实分数报 (NO-FAKE-100)
  ↓
DNA签章·append-only
  ↓
有效分数入档案 OR 回滚重检
```

---

## 📍 焊接点

**焊入位置**:
- `~/longhun-system/cnsh-core/规范/` (正式规范库)
- `~/.龍魂/质检/` (执行日志)
- `DNA登记协议 §13.2-13.4` (DNA链路)

**焊接方式**:
- T刀已焊: M253质检入口块 (§13.2)
- V刀已焊: §13.2QC哈希链 (DNA协议)
- U刀启动: 本四律正式版 (即时)

**验证方式**:
```bash
# 在任何质检中检查这四律是否全部执行
grep -r "IRON-QC" ~/.龍魂/质检/quality_audit_*.json
# 应返回4个铁律都present
```

---

## 🔴 违反后果

| 违规行为 | 后果 | 恢复方式 |
|---------|------|---------|
| 跳过L1或L2 | 🔴 系统冻结 | 完整重检 |
| 单场景<60% | 🔴 全体失败 | 修复后重测 |
| 链断>3节 | 🔴 全量回滚 | 人工+系统双验 |
| 真实<80% | 🔴 报告作废 | 100%真实重测 |
| 分数虚报100 | 🔴 撤销+倒扣 | 跌到70%重新审核 |

---

## 📝 与既有律的继承关系

```
父律(§S-25-EXT-3):
  ↓ 不假装结果律
  ↓
  ├─→ IRON-QC-NO-FAKE-100 (具体化)
  └─→ 全系统透明度要求

父律(§13.2-§13.4):
  ↓ 质检双层系统
  ↓
  ├─→ IRON-QC-DUAL-LAYER (强制化)
  ├─→ IRON-QC-SHA256-CHAIN (链化)
  └─→ DNA追溯完整性

新增(M253执行):
  ↓ 红队对抗防护
  ↓
  └─→ IRON-QC-REDTEAM-MANDATORY (强制化)
```

---

## 🧮 实施检查清单

- [x] 四律定义完成
- [x] 工程化代码框架完成
- [x] 子律细化完成
- [x] 焊接点规范完成
- [x] 违规后果明确
- [x] DNA生成
- [x] #CONFIRM双签激活

**状态**: 🟢 **正式激活·立即生效**

---

## 🐉 签章

**DNA**: `#龍芯⚡️2026-05-30-IRON-QC-QUAD-ACTIVATION-v1.0`

**子DNA**:
- `#IRON-QC-DUAL-LAYER-v1.0`
- `#IRON-QC-REDTEAM-MANDATORY-v1.0`
- `#IRON-QC-SHA256-CHAIN-v1.0`
- `#IRON-QC-NO-FAKE-100-v1.0`

**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` ✅

**SEAL**: 🐉 龍魂·质检四铁律·永不松动·不可绕过·双签锁死

**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

**责任**: `UID9622·不免责`

**时刻**: 2026-05-30 05:48 CST (星期五·卯时末)

---

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
