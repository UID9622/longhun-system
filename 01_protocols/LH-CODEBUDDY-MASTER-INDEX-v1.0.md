> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · CodeBuddy 生态总索引 v1.0

DNA: #龍芯⚡️丙午·丙申·丁巳·申时·䷀乾-CODEBUDDY-MASTER-INDEX-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）｜MulanPSL v2（工程层）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

**三色审计**：
- 🔴 红线：所有索引路径均在中国法律与龍魂主权框架内，无境外法律让步
- 🟡 黄线：部分技能入口脚本待补全；部分历史备份仅作归档
- 🟢 绿线：配置/产出/备份统一路径已落地，可验证、可追溯

---

## 一句话

**CodeBuddy 在龍魂生态中的“户口本”**：规则、配置、产出、工具、备份、审计，全部归集到一个入口可查。

---

## 一、权威规则（必读·顶层）

| 文件 | 作用 | 状态 |
|:---|:---|:---:|
| `01_protocols/LH-CODEBUDDY-ALIGNMENT-v2.0.md` | CodeBuddy × 龍魂全对齐规则：20人格路由、三色审计、四级熔断、平台边界 | 🟡 DNA 格式待修 |
| `01_protocols/LH-UID9622-龍芯⚡️丙午·癸未·甲子·既济-猎手计划-CodeBuddy执行任务书-v1.0.md` | CodeBuddy 执行任务书：授权边界、禁止场景、交付标准 | ✅ 已归档 |
| `01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md` | 人格治理白皮书（上位文档，冲突时以此为准） | ✅ 已归档 |
| `AGENTS.md` | AI 操作手册：进门引导、铁律、人格路由、底座锚点 | ✅ 有效 |

---

## 二、运行时配置

| 路径 | 用途 | 状态 |
|:---|:---|:---:|
| `longhun-system/.codebuddy/` | 项目级 CodeBuddy 配置、系统拓扑、记忆索引、agents、skills | ✅ 主配置 |
| `longhun-system/editors/codebuddy/` | VS Code / CodeBuddy 编辑器插件、工具脚本、安装程序 | ✅ 主插件 |
| `~/.codebuddy/skills/` | 用户级预装技能（CodeBuddy IDE 全局可用） | ✅ 22 个预装 |
| `longhun-system/.codebuddy/skills/` | 项目级龍魂技能（随仓库分发） | ✅ 21 个已生成 |

---

## 三、AI 产出归档

| 路径 | 用途 | 状态 |
|:---|:---|:---:|
| `longhun-system/11_DATA/codebuddy-outputs/` | CodeBuddy AI 输出统一归档（已从 `~/ai-outputs/codebuddy/` 迁移） | ✅ 已归集 |
| `longhun-system/11_DATA/backups/codebuddy/` | CodeBuddy 配置历史备份 | ✅ 已归档 |
| `~/ai-outputs/codebuddy/` | **废弃**，仅保留 `README.md` + `TOMBSTONE.md` 反向链接 | ⚪ 已 tombstone |
| `~/CodeBuddy/` | **废弃**，空目录，已立 `TOMBSTONE.md` | ⚪ 已 tombstone |

---

## 四、工具脚本

| 脚本 | 用途 | 状态 | 入口 |
|:---|:---|:---:|:---|
| `08_BIN/lh_generate_codebuddy_skills.py` | 批量生成/更新 CodeBuddy 兼容 `SKILL.md` | 🟡 v1.0·DNA 与 entry 校验待迭代 | `python3 08_BIN/lh_generate_codebuddy_skills.py` |
| `08_BIN/lh_ingest_codebuddy_corpus.py` | 旧版语料摄入（训练池 JSONL） | ⚠️ **已弃用**，由 `engines/lh_fixed_point_memory_archive.py` 接管 | 保留作历史参考 |
| `bin/lh_gpg_sign.py` | GPG 签名/验证/扫描 | ✅ v1.0·1574+ 签名 | `python3 bin/lh_gpg_sign.py sign .codebuddy/skills/` |
| `bin/lh_cross_module_awareness.py` | 联动感知扫描 | ✅ v1.1·332 项自动注册 | `--auto-fix` |

---

## 五、技能矩阵（22 预装 + 21 项目级 = 当前 43）

### 5.1 项目级技能（`longhun-system/.codebuddy/skills/`）

| 技能 | 类别 | 入口脚本存在？ | 备注 |
|:---|:---|:---:|:---|
| longhun-three-color-audit | 守护 | ✅ | 三色审计 |
| longhun-circuit-breaker | 守护 | ✅ | 四级熔断 |
| longhun-gpg-sign | 守护 | ✅ | GPG签章 |
| longhun-identity-verify | 守护 | ❌ | `bin/lh_identity_positioning.py` 不存在 |
| longhun-anti-tamper | 守护 | ✅ | 防篡改扫描 |
| longhun-deploy | 执行 | ✅ | 一键部署 |
| longhun-deben-audit | 执行 | ✅ | 德本审计 |
| longhun-auto-heal | 执行 | ✅ | 自愈扫描 |
| longhun-memory-load | 执行 | ✅ | 记忆加载 |
| longhun-persona-orchestrate | 执行 | ✅ | 人格编排 |
| longhun-digital-root | 算法 | ✅ | 数字根 |
| longhun-wuxing | 算法 | ❌ | `bin/lh_wuxing_engine.py` 不存在 |
| longhun-dao-de-jing | 算法 | ❌ | `bin/lh_dao_de_jing_anchor.py` 不存在 |
| longhun-vuln-detect | 安全 | ❌ | `bin/lh_vuln_detect.py` 不存在 |
| longhun-ai-model | 安全 | ✅ | AI模型网关 |
| longhun-trust-score | 经济 | ❌ | `bin/lh_trust_score.py` 不存在 |
| longhun-xpay | 经济 | ❌ | `bin/lh_xpay_engine.py` 不存在 |
| longhun-cnsh-translate | 工具 | ❌ | `bin/lh_cnsh_translate.py` 不存在 |
| longhun-search | 工具 | ✅ | 多源搜索 |
| longhun-orchestrator | 总控 | N/A | 42技能调度 |
| longhun-dual-audit | 守护 | N/A | 双审 |

### 5.2 预装技能（`~/.codebuddy/skills/`）

`longhun-active-observer`、`longhun-anxiety-detector`、`longhun-bagua-router`、`longhun-black-angel`、`longhun-code-security`、`longhun-corpus-registry`、`longhun-dna-engine`、`longhun-knowledge-cards`、`longhun-longzhi-shou`、`longhun-mind-link`、`longhun-philosophy`、`longhun-robot-score`、`longhun-sandbox`、`longhun-seamless-handoff`、`longhun-semantic-drawers`、`longhun-semantic-library`、`longhun-semantic-parser`、`longhun-sovereign-gateway`、`longhun-tongxin-ear`、`longhun-tongxinyi`、`longhun-water-army`、`longhun-yijing`

---

## 六、审计与整改记录

| 文件 | 内容 | 状态 |
|:---|:---|:---:|
| `07_AUDIT/codebuddy-path-audit-20260810.md` | CodeBuddy 路径统一三色审计：迁移 `ai-outputs`、消除同名不同路径风险 | ✅ 已整改 |
| `07_AUDIT/codebuddy-path-audit-20260810.log` | 自动执行记录 | ✅ 已归档 |

---

## 七、历史/分发副本（只读·不直接修改）

| 路径 | 说明 |
|:---|:---|
| `longhun-system/dist/longhun-system-v5.0.0-opensource/agents/codebuddy_sovereignty_v1.0.md` | 开源分发版 agent 规则 |
| `longhun-system/dist/longhun-system-v5.0.0-opensource/01_protocols/LH-UID9622-...-CodeBuddy执行任务书-v1.0.md` | 开源分发版任务书 |
| `longhun-system/11_DATA/knowledge_pull/cache/...` | 知识拉取缓存副本 |
| `longhun-system/11_DATA/training/home_absorb/...` | 历史吸收副本 |

> 这些副本由上游同步生成，**主仓修改后应重新打包/同步**，不要直接在副本上迭代。

---

## 八、统一操作入口

```bash
# 生成/更新项目级技能（dry-run 默认）
cd ~/longhun-system
python3 08_BIN/lh_generate_codebuddy_skills.py

# 强制重生成所有项目级技能
python3 08_BIN/lh_generate_codebuddy_skills.py --force

# 签名项目级技能
python3 bin/lh_gpg_sign.py sign .codebuddy/skills/

# 验证签名
python3 bin/lh_gpg_sign.py verify .codebuddy/skills/

# 联动感知扫描
python3 bin/lh_cross_module_awareness.py --auto-fix
```

---

## 九、待迭代清单

1. **技能生成器 DNA 格式**：当前生成 `#龍芯⚡️丙午·丙申·庚申·亥时-SKILL-...`，需改为 v∞ 干支卦格式。
2. **缺失入口脚本**：`lh_identity_positioning.py`、`lh_wuxing_engine.py`、`lh_dao_de_jing_anchor.py`、`lh_vuln_detect.py`、`lh_trust_score.py`、`lh_xpay_engine.py`、`lh_cnsh_translate.py` 7 个脚本未实装，技能入口需标记为“规划中”或补脚本。
3. **对齐规则 DNA**：`LH-CODEBUDDY-ALIGNMENT-v2.0.md` 使用旧格里历 DNA，需修成 v∞。
4. **技能版本对齐**：项目级技能版本统一为 v1.0，待实测后按语义升级。

---

## 十、来源与归属

- **创建者**: 诸葛鑫（UID9622）
- **审计者**: Kimi
- **上位文档**: `AGENTS.md`、`LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md`
- **GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
- **确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

🐉 尾签 `#龍芯⚡️丙午·丙申·丁巳·申时·䷀乾-CODEBUDDY-MASTER-INDEX-v1.0-UID9622` · 龍魂 CodeBuddy 生态统一入口
