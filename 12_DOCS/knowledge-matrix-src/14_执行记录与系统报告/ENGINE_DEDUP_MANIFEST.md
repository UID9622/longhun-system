# 🔧 龍魂引擎去重清单

> DNA: #龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-ENGINE-DEDUP-MANIFEST-v1.0
> 操作者: CodeBuddy
> 原则: 不删除，只标记权威源与副本关系

## 规则

- 权威源标记为 `⭐权威` — 所有引用应指向此文件
- 副本标记为 `📋副本` — 建议统一引用后逐步废弃
- 副本文件中添加 `# DUPLICATE_OF: <权威路径>` 头部注释

---

## 1. cnsh_editor_engine_v2.0.py (5 份)

| 状态 | MD5 | 大小 | 路径 |
|------|-----|------|------|
| ⭐权威 | 26540043 | 68,046 B | `cnsh-terminal/engines/cnsh_editor_engine_v2.0.py` |
| 📋副本 | 687bf962 | 68,041 B | `cnsh-editor/cnsh_editor_engine_v2.0.py` |
| 📋副本 | 73de30fc | 68,052 B | `cnsh-editor/core/cnsh_editor_engine_v2.0.py` |
| 📋副本 | c4f226ea | 68,046 B | `imports/v7/cnsh_editor_engine_v2.0.py` |
| 📋副本 | d61d5c1a | 68,040 B | `releases/v5.1/staging/cnsh-terminal/engines/cnsh_editor_engine_v2.0.py` |

## 2. cnsh_translator_engine_v2.0.py (5 份)

| 状态 | MD5 | 大小 | 路径 |
|------|-----|------|------|
| ⭐权威 | 6c00d6f5 | 89,605 B | `cnsh-terminal/engines/cnsh_translator_engine_v2.0.py` |
| 📋副本 | 8d154792 | 89,608 B | `cnsh-editor/cnsh_translator_engine_v2.0.py` |
| 📋副本 | d3fe0080 | 89,605 B | `imports/v7/cnsh_translator_engine_v2.0.py` |
| 📋副本 | 93703726 | 89,599 B | `releases/v5.1/staging/cnsh-terminal/engines/cnsh_translator_engine_v2.0.py` |
| 📋副本 | b6eb6bda | 89,601 B | `cnsh-terminal/downloads-imports/Kimi_Agent_终端升级与结构优化 6/cnsh_translator_engine_v2.0.py` |

## 3. audit_engine.py (5 份)

| 状态 | MD5 | 大小 | 路径 |
|------|-----|------|------|
| ⭐权威 | ac8884e0 | 20,155 B | `cnsh-core/engines/audit_engine.py` |
| 📋副本 | a1b89e9a | 19,995 B | `engines/audit_engine.py` |
| 📋副本 | 0f0b63e4 | 20,147 B | `cnsh-core.backup/engines/audit_engine.py` |
| 📋副本 | d3cba74c | 72,865 B | `skills/warehouse-audit/scripts/audit_engine.py` |
| 📋副本 | d6892853 | 72,847 B | `releases/v5.1/staging/skills/warehouse-audit/scripts/audit_engine.py` |

## 4. longhun_skill_auto_completion_engine.py (4 份)

| 状态 | MD5 | 大小 | 路径 |
|------|-----|------|------|
| ⭐权威 | c1e19d77 | 19,933 B | `skills/core/longhun_skill_auto_completion_engine.py` |
| 📋副本 | 36bc18ff | 19,929 B | `skills/longhun_skill_auto_completion_engine.py` |
| 📋副本 | d6a20d8f | 1,263 B | `integrated-modules/skills.integrated/longhun_skill_auto_completion_engine.py` |
| 📋副本 | 634a4b21 | 19,929 B | `releases/v5.1/staging/skills/longhun_skill_auto_completion_engine.py` |

## 5. longhun-skill-auto-completion-engine.py (4 份, 不同命名变体)

| 状态 | MD5 | 大小 | 路径 |
|------|-----|------|------|
| ⭐权威 | — | — | 建议统一为 `longhun_skill_auto_completion_engine.py` (下划线版) |
| 📋副本 | — | — | `skills/longhun-skill-auto-completion-engine.py` |
| 📋副本 | — | — | `skill-standards.integrated/longhun-skill-auto-completion-engine.py` |
| 📋副本 | — | — | `releases/v5.1/staging/skills/longhun-skill-auto-completion-engine.py` |
| 📋副本 | — | — | `01_技能库/downloads-imports/龍魂 10 Skill 標準化完成/longhun-skill-auto-completion-engine.py` |

## 6. m04_yijing_engine.py (2 份)

| 状态 | MD5 | 大小 | 路径 |
|------|-----|------|------|
| ⭐权威 | 7ffc3dce | 9,998 B | `cnsh-core/m04_yijing_engine.py` |
| 📋副本 | 5fe93a2e | 9,990 B | `cnsh-core.backup/m04_yijing_engine.py` |

## 7. 其他重复引擎

- **rule_engine.py**: 权威 `cnsh-core/rules/rule_engine.py` / 副本 `cnsh-core.backup/rules/rule_engine.py`
- **sync_engine.py**: 权威 `cnsh-core/ai-tools/operation_log_engine/core/sync_engine.py` / 副本 `cnsh-core.backup/...`
- **lineage_verification_engine_v1.0.py**: 权威 `longhun_mvp_reviewed/lineage_verification_engine_v1.0.py` / 副本 `cnsh-terminal/downloads-imports/...`
- **longhun_mvp_execution_engine_v2.0.py**: 权威 `longhun_mvp_reviewed/longhun_mvp_execution_engine_v2.0.py` / 副本 `cnsh-terminal/downloads-imports/...`
- **cnsh_core_engine.py**: 权威 `integrated-modules/kimi_agent/cnsh_core_engine.py` / 副本 `_quarantine/...`

---

## 总结

| 引擎名 | 副本数 | 权威路径 |
|--------|--------|----------|
| cnsh_editor_engine_v2.0 | 4 | `cnsh-terminal/engines/` |
| cnsh_translator_engine_v2.0 | 4 | `cnsh-terminal/engines/` |
| audit_engine | 4 | `cnsh-core/engines/` |
| longhun_skill_auto_completion_engine | 3+4 | `skills/core/` |
| m04_yijing_engine | 1 | `cnsh-core/` |
| 其他 (6 组) | 各 1-3 | 见上表 |

**共 30 个不同名称的引擎文件，其中 11 组有副本冗余。**
