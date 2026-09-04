# Home 散落内容 → 深度集成追踪 v1.2

> 抬头模板: [6] 💡 追踪型 · v1.2
> DNA(v∞): `#龍芯⚡️丙午·丁酉·辛巳-HOME-DEEP-INTEGRATION-TRACK-v1.2-9d4b1a6e`
> 父DNA: `#龍芯⚡️丙午·丁酉·辛巳-HOME-DEEP-INTEGRATION-TRACK-v1.1-5c8e2b7f`
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> License: CC BY-NC-SA 4.0（核心思想层）
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 背景: 2026-09-04 老大指示「你看着办 /Users/zuimeidedeyihan」+「深度集成我们系统…格式不统一、语法不统一、还没修复的都按标准整理…还有很多功能」

---

## 一、现状盘点（2026-09-04）

| 对象 | 内容 | 状态 |
|------|------|------|
| `~/longhun-system` | 主仓 50 万文件 | 系统本体 |
| `~/龍魂待整理/` | 36 md + 7 py + 92 html + pdf | **缺口大**：md 无 1 个含「归属名」字段·仅 1 个含许可证·20 个旧 DNA 格式 |
| `~/claude搭建待整理/` | 已大部分落地 skills/（INDEX 声明 v3 主干已迁） | 历史留档·不用再搬 |
| `~/既检查代码底座/` | 审计集成引擎 | 已入库 `skills/longhun-audit-integrated/` + home_absorb 快照 |
| `~/龍盾宝宝/` | 防护盾 v1 | 已被系统 `lh_shield_v3` 等取代 + home_absorb 快照 |
| `~/龍魂浏览器插件.zip` | **longhun-ext 浏览器插件（功能）** | ✅ 本批深度集成（见下） |
| `11_DATA/training/home_absorb/` | 45 sources 快照 + 139 loose_files | 训练源快照·**不原地改**（保持语料原样） |

### CNSH 语法不统一实证（关键样本）
- 旧示例 `claude搭建待整理/02_CNSH语言/hello.cnsh`: `函数 主函数() 返回类型 整数` + `打印“...”` 无括号
- 现行基线 `tests/cnsh_samples/test_fibonacci.cnsh`: `功能 主()` + `打印("...")` + `循环 i 在 范围()`
- 处置: 历史文件冻结留档（不删除只冻结）·新写/迁移文档一律走现行基线语法

---

## 二、批次计划

| 批次 | 内容 | 状态 |
|------|------|------|
| **批 1** | 龍魂浏览器插件 longhun-ext 深度集成（源码级） | ✅ 完成（见三） |
| **批 2** | 龍魂待整理 核心文档迁移+规范化 | ✅ 完成（见三·B） |
| **批 3** | 流场可视化最新版 html → portal flow 区域 | ✅ 勘察即结（v9/v10 已在） |
| **批 4** | 门户/工作台原型 html 甄别（05 AI人格 / 04 审计 等） | ✅ 全留档（portal 已覆盖·见三·C） |
| **批 5** | loose_files 分类归档 | ✅ 登记即结（快照已在·不搬动） |

原则: 不删除原始文件·只迁最新版·DNA v∞ 统一·迁移后加来源链接·GPG 全签。

---

## 三、批 1 完成清单（longhun-ext · 2026-09-04）

来源: `~/龍魂浏览器插件.zip`(2026-05-21) → `extensions/longhun-ext/`

| 动作 | 详情 |
|------|------|
| 解压与结构规范化 | 清除 zip 内坏目录 `{icons,engine` 空壳·嵌套 `longhun-ext/longhun-ext` 提升一层 |
| 10 文件全标准化 | 统一补: DNA(v∞ 干支卦格式) + 创建者: 诸葛鑫（UID9622）+ 归属名 + License(MulanPSL v2)·文件: manifest.json / background.js / content.js / popup.html / popup.js / install.sh / LonghunApp.swift / README.md / engine/main.py / engine/notion_sync.py |
| manifest 修复 | 加 `author` 字段·移除死引用 `sidebar.html`(web_accessible_resources)·icons 三尺寸补齐（源自 `brand/seals/seal_9622_square_160.png`·sips 缩放） |
| 语法验证 | manifest JSON ✓ · main.py/notion_sync.py py_compile ✓ · popup.js/background.js/content.js node --check ✓ |
| 登记 | `extensions/README.md` 目录表新增条目 |
| 端口注意 | ⚠️ 9622 现由系统 `bin/lh_api.py --port 9622`(PID 94987) 占用·已注 README/main.py（自跑引擎需改端口 9633 并同步 JS） |
| 签名 | GPG 6 文件新签 + extensions/README.md 重签 ✅ |

---

## 三·B、批 2 完成清单（龍魂待整理 核心文档 · 2026-09-04）

按 `~/龍魂待整理/README_龍魂待整理索引_v1.0.md` 迁移建议执行·源文件全部冻结保留·`cp -n` 防覆盖。

| 区 | 动作 | 落点 |
|----|------|------|
| 01 CNSH 协议规范 | 勘察确认 **已全量收纳** `docs/cnsh/`（中文语法全景/通心译/CNSH-64×2/术语对照×3/FIRST_PRINCIPLES/algorithms-cnsh） | 无增量 |
| 02 流场可视化 | 勘察确认 **已收纳** `10_PORTAL/flow/`（unified-v9/v10/flow-field/current） | 无增量 |
| 03 身份安全-DNA | ✅ 迁 3 文件 → `L8_治理层/governance/dna/`（规格书 html/CDNA 需求 md/网络户口本 html）+ README 来源登记 | dna/ |
| 03 DNA 学术 md | 龙魂数字主权体系论文 → 建议 `papers/`·本批留源目录（md 大件） | 留档 |
| 07 论文 PDF | ✅ 迁 4 小件（dragon-soul-fixed-point / longhun-zhongli / luoshu_369 / luoshu-vortex）→ `papers/` | papers/ |
| 07 大 PDF | 一级控万象×3(33+18+15MB)+太极易经(11MB) >10MB 铁律 → **不迁仓库**·冻结在 `~/龍魂待整理/07-论文PDF/` | 留档 |
| 09 杂项 | ✅ 迁 2 高价值 html：守住底线…公正公证 → `L8_治理层/governance/` · 龍魂数学公式体系 v2.0 → `governance/tech-docs/` | governance/ |
| 08 浏览器插件 | LongHunWidget 规格书早已在 `extensions/` | 无增量 |
| 06 工具脚本 | 龍魂API v1.0.py / parse_notion.py 均已被系统版本 superseded（lh_api.py 9622 在跑）→ 不迁 | 留档 |
| 05 AI人格 22 html | 大件原型（主控台/hub/中枢）→ portal 已有大量覆盖·留档待甄别 | 留档 |

LH-CDNA md 头已规范化（DNA v∞ + 归属名 + 许可证 + 来源）。GPG 全签：dna×4 · papers×4 · governance html×2。

---

## 三·C、批 3-5 甄别结果（2026-09-04 · 勘察即结）

### 批 3 · 流场可视化
`10_PORTAL/flow/` 已收纳 **longhun-unified-v9/v10 + longhun-flow-field-v9 + flow-field + current-flow**（含 .asc）→ 源目录 `02-流场可视化/` 冻结留档·无增量。sancai-flow-v8.1 属旧版（v9 已覆盖）不迁。

### 批 4 · 门户/原型 html 甄别（05-AI人格 + 04-审计 区）
| 源文件 | 甄别结论 |
|--------|---------|
| AI智能体术语对照表-龍魂版.html | ✅ **已在 `12_DOCS/`**（含 .asc）·留档 |
| IPA-200-宝宝人格配置.html | 旧原型 → portal console/ai-hub 覆盖·留档 |
| longhun_hub.html / main-console.html / 龍魂智能中枢_v5.0_全套一体化.html | 中枢/主控原型 → `10_PORTAL/console/`(glass/main-p0)·ai-hub/ 覆盖·留档 |
| Behavioral Cryptography…Collaborative Content.pdf | **md5 `1db8d52a…` 与 `papers/behavioral_crypto/BC-Paper-Full-v1.0.pdf` 完全一致** → 已迁·留档 |
| 行为密码学csdn.md | articles/ 已有规范版（8/23 已补 CONFIRM/SEAL 头）·留档 |
| longhun_brain.py / deploy_brain.sh | superseded by `lh brain`（超级大脑·brain/）·留档 |
| 04-审计治理: qa_report/truth_report/审计 html | 审核过滤规格书×2 早已在 `governance/`·审计报告为历史产出·留档 |

### 批 5 · loose_files
`11_DATA/training/home_absorb/loose_files/` 快照现存 **123 项**（训练源语料·`knowledge/sources/workspace/loose_files` 四区完整）→ 保持原样不搬动·本批登记即结。

**五批全部完结 · 源目录 `~/龍魂待整理/` 冻结保留 · 未迁项均有留档原因**

---

## 四、验收（批 1 三色）

🟢 语法全过 · 归属名/许可证/DNA 全齐 · GPG 全签 · 原 zip 保留冻结
🟡 引擎未实跑（9622 冲突·功能自测需另配端口）
🔴 无

---

**DNA(v∞)**: #龍芯⚡️丙午·丁酉·辛巳-HOME-DEEP-INTEGRATION-TRACK-v1.2-9d4b1a6e
**父DNA**: #龍芯⚡️丙午·丁酉·辛巳-HOME-DEEP-INTEGRATION-TRACK-v1.1-5c8e2b7f
**GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
🐉
