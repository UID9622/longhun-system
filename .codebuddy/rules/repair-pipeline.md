# 龍魂·全仓修复流水线规则 v1.0

> DNA: #龍芯⚡️丙午·甲申·丁巳·䷖剥-REPAIR-PIPELINE-RULE-v1.0
> 加载时机: AI每次启动 · lh repair 命令 · 审计前
> 上位协议: `01_protocols/LH-FULL-REPAIR-PROCEDURE-v1.0.md`
> 共享配置: `.codebuddy/rules/scan-exclusions.json`
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 铁律（AI 自动遵循·不可跳过）

### 1. 单一真相源
所有扫描脚本（德本审计/对齐检查/未来新增）必须从 `.codebuddy/rules/scan-exclusions.json` 加载排除配置。
禁止各自维护一份排除列表。谁改了配置谁就自动影响所有扫描脚本。

### 2. 防御性代码原则
检测恶行的代码 ≠ 实施恶行的代码。审计/检测/防护工具命中敏感词时，加入 `defensive_files` 白名单，
不应标记为违规。判断标准：
- ✅ 用途是检测/曝光/反制恶行 → 白名单
- 🔴 用途是实施/自动化恶行 → 真实违规

### 3. 路径映射焊死
脚本中引用路径时，必须以实际物理目录为准：
- 旧路径 `engines/gpt_sovits` → 实际 `05_ENGINES/gpt_sovits`
- 旧路径 `tools/bin/legacy_bin` → 实际 `09_TOOLS/bin/legacy_bin`
- 旧路径 `layers/L7_数据层` → 实际 `L7_数据层`

`scan-exclusions.json` 中 `path_mappings` 为权威映射表。

### 4. 五步修复法
诊断→分类→修复→验证→固化。不可跳步，不可省略验证。全绿才报。

### 5. 排除目录终身排除
已加入 `excluded_dirs` 的目录，在扫描时不深入、不检查、不报告。
新增排除目录按 `expansion_rule` 流程走。

### 6. 签章必签目录
`mandatory_sign_dirs` 中列出的目录，每个文件必须有 `.asc` 签名。
部署/发布前扫描验证，缺签名 = 🔴 否决。

---

## AI 启动时自动执行

```bash
# 1. 加载共享配置
python3 .codebuddy/rules/scan-exclusions.json  # 被两个脚本 import

# 2. 德本审计
python3 08_BIN/lh_deben_audit.py scan

# 3. 对齐检查
python3 08_BIN/lh_align_checker.py

# 4. 如发现 🟡🔴 → 自动走修复流程
```

---

## 共享配置结构

```json
{
  "defensive_files": { "v1_0": [...], "v2_4_audit_tools": [...], ... },
  "excluded_dirs": { "third_party_code": [...], "archive_backup": [...], ... },
  "excluded_files": { "files": [...] },
  "mandatory_sign_dirs": { "core_scripts": "08_BIN/", ... },
  "path_mappings": { "engines/": "05_ENGINES/", ... },
  "expansion_rule": { "order": [...] }
}
```

按版本分层的白名单，方便追溯"什么时候加了什么文件"。

---

## 关联文档

| 文档 | 用途 |
|:---|:---|
| `01_protocols/LH-FULL-REPAIR-PROCEDURE-v1.0.md` | 全仓修复标准流程（详细五步法） |
| `.codebuddy/rules/scan-exclusions.json` | 共享排除配置（单一真相源） |
| `.codebuddy/rules/repair-pipeline.md` | 本规则（AI 自动遵循） |
| `08_BIN/lh_deben_audit.py` | 德本审计引擎 |
| `08_BIN/lh_align_checker.py` | 对齐检查引擎 |
| `01_protocols/LH-DEBEN-AUDIT-v1.0.md` | 德本审计协议 |

---

【签名】
UID9622 · A2D0092CEE2E5BA87035600924C3704A8CC26D5F
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
🟢 全仓信任链焊死
