# 📊 龍魂 · 顶层目录分类定案 v1.0

**DNA:** `#龍芯⚡️丙午·丙申·壬戌·申时·䷕贲-DIRECTORY-CLASSIFICATION-V1.0-UID9622`
**创建者:** 诸葛鑫（UID9622）
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
**License:** MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
**三色:** 🟢 分类定案（2026-08-22 全盘盘点） · 归集动作分步执行

> 依据：`12_DOCS/AI-SCAN-WHITELIST-v1.0.md` · 顶层 ~180 目录实测盘点
> 铁律：不物理删除，只冻结+索引。删除须 UID9622 显式指令+DNA 记录。

---

## 一、分类总览

| 类别 | 数量 | 处置 |
|:---|:---:|:---|
| ✅ 软链双名对 | ~20对(40目录) | 无害保留·禁当重复合并 |
| ✅ 核心层白名单 | ~20 | 本就该在这·不动 |
| ✅ 归档/数据/构建产物 | ~15 | 本就该冻结·不动 |
| ⚠️ 疑似外部项目 | ~15 | 待 UID9622 判定归属 |
| 🔍 散落待归集 | 60~80 | 逐个归位/软链/索引 |
| 🧹 垃圾嫌疑 | 4类~2.6万文件 | 冻结到 `_work/garbage-*` |

## 二、软链双名对（无害·保留）

`engines↔05_ENGINES` `docs↔12_DOCS` `tools↔09_TOOLS` `bin↔08_BIN`
`portal↔10_PORTAL` `audit↔07_AUDIT` `tests↔13_TESTS` `services↔04_SERVICES`
`layers↔03_LAYERS` `skills↔02_SKILLS` `cnsh↔cnsh.integrated` `logs↔日志`
`train↔training` `editor↔editors` `字体↔longhun-font` `03_後土OS↔06_HOUTU_OS`

### 内容镜像双名对（物理重复·以顶层为准·2026-08-22 登记）
`articles↔knowledge/articles`（290/348 重叠）· `papers↔knowledge/papers`（35/38 重叠）
规则: 只维护顶层 `articles/` `papers/`；knowledge 侧视为历史镜像冻结不更新（不删除只冻结）
佐证: `12_DOCS/agent_reports/知识入库_20260822.md`
`01_技能庫↔02_SKILLS` `03_知識圖譜↔03_KNOWLEDGE_GRAPH`

判定流程（白名单焊死）：`ls -ld` → `readlink` → `stat -f %i` 确认，禁凭目录名判断。

## 三、核心层白名单（活跃区·不动）

`01_protocols` `02_SKILLS` `03_LAYERS` `08_BIN` `09_TOOLS` `12_DOCS`
`10_PORTAL` `07_AUDIT` `13_TESTS` `deploy` `personas` `agents`
`web` `web_apps` `state` `.codebuddy` `config` `20_CONFIG`

## 四、归档/数据/构建产物（本来就该冻结·不动）

`_archive` `archive` `backups` `backup` `_QUARANTINE` `tombstone_vault`
`_private` `_work` `11_DATA` `models` `dist` `build_ide` `dist_ide` `fused_model`

## 五、疑似外部项目（待 UID9622 判定）

| 目录 | 文件数 | 特征 | 判定状态 |
|:---|:---:|:---|:---|
| `baobao-guardian` | 21.7K | 全是 js/ts·独立前端 | 🟡 待判定 |
| `rust` | 6.7K | rust 工程 | 🟡 待判定 |
| `sdk` | 6.1K | SDK 包 | 🟡 待判定 |
| `integrations` | 18.3K | 集成层 | 🟡 待判定 |
| `harmonyos` / `harmonyos-universe` / `harmony` | 277/44/103 | 鸿蒙 | 🟡 待判定 |
| `android` `ios` `android-auto` | 11/4/4 | 移动端 | 🟡 待判定 |
| `LongHunCarOS` `car_index` | 58/0 | 车载 | 🟡 待判定 |
| `cnsh-editor-mac` `memory_editor` `cloud-browser` | 34/25/26 | 独立工具 | 🟡 待判定 |
| `龙魂日记本-iOS` | 4 | iOS | 🟡 待判定 |

判定标准：是否龍魂体系产物 → 是则归集进标准骨架；否则冻结标注+索引，不动原内容。

## 六、散落待归集（60~80·真正的归并对象）

待归目标：`core` `longhun-core` `governance` `sovereignty` `sovereign-registry`
`knowledge` `knowledge-graph` `systems` `library` `multicurrency`
`price_audit_tool` `luoshu_369_engine` `xpay` `longhun-dev-ecosystem`
`backend` `registry` `brain` `digital_humans` `articles` `papers` `research`
`control-panel` `dashboard` `dev-env` `executors` `extensions` `editors`
`capabilities` `experiments` `packages` `reports` `templates` `software_dna`
`output` `widgets` `imports` `src` `lib` `static` `www` `launchd` `kimi`
`mvp_config` `apps` `ai-outputs` `container` `demo` `docker`
`05_系統報告` `06_技術文檔` `02_執行記錄` `04_決策日誌` `08_STATE`
`03_MEMORY` `EVIDENCE` `zeng-extraction` `public-content` + L0-L9 顶层零散层

归集规则：
1. 先判软链（软链则保留）
2. 有标准骨架归属 → 移动/软链到骨架（`03_LAYERS`/`12_DOCS`/`08_BIN`…）
3. 无法判定 → 建索引文档，冻结待判

## 七、垃圾嫌疑（冻结候选·已统计）

| 类型 | 位置 | 数量 |
|:---|:---|:---:|
| `.bak` | `04_AUDIT` | 11973 |
| `.o` | `09_TOOLS` | 9574 |
| `.o`+`.pyc` | `05_ENGINES` | 182+178 |
| `.pyc` | `08_BIN` | 3054 |
| `.pyc` | 全库 `__pycache__` | 待扫 |

冻结目标：`_work/garbage-YYYYMMDD/`（保持相对路径·出 manifest 清单）

## 八、执行记录

| 日期 | 动作 | 结果 |
|:---|:---|:---|
| 2026-08-22 | 顶层盘点·分类定案 | 🟢 完成 |
| 2026-08-22 | 垃圾冻结 `.bak/.o/.pyc` | 进行中 |
| 2026-08-22 | 知识三层导航落位：`03_KNOWLEDGE_GRAPH/README.md` 重写（171项）· `knowledge/README.md` 新建（14子目录）· 空壳目录 `architecture/` `cnsh/` 标注镜像位置 | 🟢 完成 |

---
> GPG 签名：`A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
