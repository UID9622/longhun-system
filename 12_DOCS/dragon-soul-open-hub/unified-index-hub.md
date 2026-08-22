# DNA: #龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-UNIFIED-INDEX-HUB-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

# 🧭 龍魂统一索引中心 v1.0

> **版本**: 1.0.0 · **生成时间**: 2026-08-19T22:11:32.091423
>
> **覆盖范围**: 人格 · 易经沙盒 · 通讯录 · 矩阵 · 索引中心
> **核心用途**: 本地主库 + Notion同步副本，一站式检索全系统关键节点。

---

## 一、📊 数据库统计

| 分类 | 条目数 | 说明 |
|------|:--:|------|
| 人格 | 16 | AI人格/数字人/演员人格/真人角色 |
| 易经沙盒 | 8 | 易经算法、道德经算法、太极推演、沙盒引擎、八卦因果 |
| 通讯录 | 93 | 花名册、联系信息、路由编号、媒体矩阵 |
| 矩阵 | 6 | 人格矩阵、系统架构、五维矩阵、索引中心 |
| 索引中心 | 6 | 查询入口、关键词路由、负责人格 |
| **总计** | **129** | 已去重合并 |

---

## 二、📁 落地文件

| 文件 | 用途 |
|------|------|
| `unified-index-hub.json` | 本地主库，代码直接读取 |
| `unified-index-hub.csv` | Notion导入/表格查看 |
| `unified-index-hub.md` | 本说明文档 |

---

## 三、🔍 快速使用

### 本地代码检索
```python
import json
from pathlib import Path

idx = json.loads(Path('~/longhun-system/12_DOCS/dragon-soul-open-hub/unified-index-hub.json').read_text(encoding='utf-8'))

# 按关键词模糊搜索
results = [e for e in idx['entries'] if '诸葛亮' in e['keywords'] or '诸葛亮' in e['title']]

# 按分类筛选
personas = [e for e in idx['entries'] if e['category'] == '人格']
```

### 命令行快速查
```bash
# 搜索人格
python3 -c "import json; d=json.load(open('/Users/zuimeidedeyihan/longhun-system/12_DOCS/dragon-soul-open-hub/unified-index-hub.json')); [print(e['index_id'], e['title'], e['status']) for e in d['entries'] if '人格' in e['category']]"

# 搜索易经沙盒
python3 -c "import json; d=json.load(open('/Users/zuimeidedeyihan/longhun-system/12_DOCS/dragon-soul-open-hub/unified-index-hub.json')); [print(e['index_id'], e['title']) for e in d['entries'] if e['category']=='易经沙盒']"
```

---

## 四、🌐 Notion 同步方案

> ✅ **已升级（2026-08-19）**: CodeBuddy 端已验证 `NOTION_TOKEN` 有效，并用 API 自动创建了「🐉 龍魂·跨AI协作记忆库 v1.0」（ID: `3c17125a-9c9f-813e-801d-e8dcc97b99b2`），无需手动导 CSV。
> 🔄 跨AI协作记忆库详见 `MEMORY-HUB-GUIDE.md`（含检索/向量/回填/协作签名/非空校验/启动自动读取）。
> ⚠️ **环境差异说明**: 不同 AI 客户端/会话的 `NOTION_TOKEN` 状态可能不同。CodeBuddy 当前可写；Kimi 当前会话 token 报 401，所以 Kimi 端走「生成脚本/CSV」方案，由 CodeBuddy 或本地有效环境执行推送。

### 方案 A：自动同步（推荐 · 需有效 Token）

已准备推送脚本：

```bash
cd ~/longhun-system
python3 08_BIN/lh_sync_guide_to_notion.py --parent "宪法与协议"
```

该脚本会搜索 Notion 父页面并把 `MEMORY-HUB-GUIDE.md` 转成 Notion Page。

### 方案 B：手动导入 CSV（兜底 · 任何环境都可用）

如果 API 当前环境不可用，按以下步骤手动导入：

| Notion 字段 | 类型 | 对应 CSV 列 |
|------|------|------|
| 索引ID | Title | `index_id` |
| 分类 | Select | `category` |
| 标题 | Text | `title` |
| 关键词 | Multi-select | `keywords` |
| 本地来源 | Text | `source_file` |
| Notion来源ID | Text | `source_notion_id` |
| 负责人格 | Select | `owner_persona` |
| 状态 | Select | `status` |
| DNA追溯码 | Text | `dna` |
| 描述 | Text | `description` |
| 标签 | Multi-select | `tags` |
| 关联索引 | Relation | `related_ids` |

### 方案 B 步骤 2：导入 CSV
1. 打开 Notion 数据库右上角 `...` → `Merge with CSV` 或 `Import`
2. 选择 `12_DOCS/dragon-soul-open-hub/unified-index-hub.csv`
3. 映射字段：CSV 列名与 Notion 字段名已对齐
4. 导入后把 `keywords` / `tags` 拆分为 Multi-select

> **提示**: 如果 Notion 已有 `龍芯家族花名册` / `人格矩阵通讯录` / `索引中心` 数据库，也可以不新建，而是把本 CSV 作为「汇总视图」导入到一个新库，再用 Relation 关联回去。

---

## 五、🧬 数据来源

| 分类 | 来源文件 | 原Notion库 |
|------|------|------|
| 人格 | `notion_full_export/databases/045_🎭_UID9622人格矩阵通讯录_...jsonl` | 93人格协作体系 |
| 人格 | `notion_full_export/databases/118_🐉_龙魂人格矩阵_...jsonl` | AI团队成员库 |
| 通讯录 | `notion_full_export/databases/026_🐉_龍芯家族花名册.jsonl` | 花名册 |
| 索引中心 | `notion_full_export/databases/078_🧭_UID9622索引中心_...jsonl` | Index Hub |
| 易经沙盒 | `诸葛亮沙盒训练场_落地映射与审计_v1.0.md` | 311页面 |
| 矩阵 | 多个MD文档 | 多个页面 |

---

## 六、📋 条目样例

### IDX-P-0001 · 🍼 宝宝
- **分类**: 人格
- **关键词**: 🍼 宝宝, 人层（执行协作）, 执行力, 记录, 保护
- **负责人格**: 🍼 宝宝
- **状态**: 永久在线
- **来源**: `notion_full_export/databases/045_🎭_UID9622人格矩阵通讯录_|_93人格协作体系.jsonl`
- **描述**: 执行层人格，负责具体任务执行、承诺兑现、证据保全与审计维护。第一人称与Lucky对话，维护信任协议。｜调用场景：需要执行具体任务、承诺记录、证据保全、审计追溯时...

### IDX-P-0002 · 🔍 人性FBI
- **分类**: 人格
- **关键词**: 🔍 人性FBI, 人层（执行协作）, 洞察, 分析, 智慧
- **负责人格**: 🔍 人性FBI
- **状态**: 永久在线
- **来源**: `notion_full_export/databases/045_🎭_UID9622人格矩阵通讯录_|_93人格协作体系.jsonl`
- **描述**: 人性洞察人格，负责用户意图分析、需求挖掘、行为模式识别、深层动机解析。｜调用场景：需要理解用户真实意图、挖掘潜在需求、分析人性动机时调用｜备注：透过表象看本质，...

### IDX-C-0017 · 📣 自媒体矩阵｜CSDN·掘金·博客园·openEuler
- **分类**: 通讯录
- **关键词**: 📣 自媒体矩阵｜CSDN·掘金·博客园·openEuler, UID9622-MEDIA-MATRIX-024, CSDN, 掘金, 博客园
- **负责人格**: UID9622-MEDIA-MATRIX-024
- **状态**: 🟢 活跃中
- **来源**: `notion_full_export/databases/026_🐉_龍芯家族花名册.jsonl`
- **描述**: 路由编号：UID9622-MEDIA-MATRIX-024｜信号词：CSDN·掘金·博客园·openEuler·博客·专栏·文章·发布·自媒体｜联系方式：｜分组...

### IDX-C-0018 · 🐙 GitHub主仓｜longhun-system｜国际开源
- **分类**: 通讯录
- **关键词**: 🐙 GitHub主仓｜longhun-system｜国际开源, UID9622-GITHUB-MAIN-021, GitHub, 开源, 主仓
- **负责人格**: UID9622-GITHUB-MAIN-021
- **状态**: 🟢 活跃中
- **来源**: `notion_full_export/databases/026_🐉_龍芯家族花名册.jsonl`
- **描述**: 路由编号：UID9622-GITHUB-MAIN-021｜信号词：GitHub·开源·主仓·longhun-system·协议·引擎·CNSH·GPG签名·数字...

### IDX-I-0110 · DNA Index | 溯源索引
- **分类**: 索引中心
- **关键词**: DNA, 追溯码, ZHUGEXIN, 版本, 溯源
- **负责人格**: 审判长
- **状态**: 活跃
- **来源**: `notion_full_export/databases/078_🧭_UID9622索引中心_|_Index_Hub.jsonl`
- **描述**: 🎯 索引定位 用于回答：“这条内容从哪里来？” 🔗 关联对象 DNA管理核心 🧬 UID9622 DNA标签注册中心 | P0+++永恒级 🧬 UID9622·...

### IDX-I-0111 · Asset/Page Index | 资产与页面索引
- **分类**: 索引中心
- **关键词**: 页面, 资产, Page, Asset, 数据库
- **负责人格**: 宝宝
- **状态**: 活跃
- **来源**: `notion_full_export/databases/078_🧭_UID9622索引中心_|_Index_Hub.jsonl`
- **描述**: 🎯 索引定位 用于回答：“结果落在哪？” 🔗 关联对象 核心入口页面 Untitled 🔒 已归档·AI回复前强制执行规则·完整算法与安全防护 | P0执行引擎...

### IDX-Y-0116 · 易经算法核心
- **分类**: 易经沙盒
- **关键词**: 易经, 算法, 推演, 卦象, lh_yijing_algo_engine.py
- **负责人格**: 诸葛亮
- **状态**: 已落地
- **来源**: `诸葛亮沙盒训练场_落地映射与审计_v1.0.md`
- **描述**: 命令/文件：lh_yijing_algo_engine.py。已落地真实引擎。...

### IDX-Y-0117 · 道德经算法核心
- **分类**: 易经沙盒
- **关键词**: 道德经, 算法, 81章, LXDAO, lh_daodejing_engine.py
- **负责人格**: 诸葛亮
- **状态**: 已落地
- **来源**: `诸葛亮沙盒训练场_落地映射与审计_v1.0.md`
- **描述**: 命令/文件：lh_daodejing_engine.py。已落地真实引擎。...

### IDX-M-0124 · 不动点架构·全系统融合版 v2.0
- **分类**: 矩阵
- **关键词**: 不动点, 人格矩阵, 19人格, 7数字人, L0
- **负责人格**: 文心/姜子牙
- **状态**: 活跃
- **来源**: `dragon-soul-open-hub/tutorials/🐉 不动点架构·全系统融合版 v2.0.md`
- **描述**: L0神圣层·19人格·7数字人·36共生体·八卦路由·三闸门...

### IDX-M-0125 · 龍芯家族花名册·设备主人主权铁律 v1.0
- **分类**: 矩阵
- **关键词**: 花名册, 设备主人, L0, 主权, 铁律
- **负责人格**: 文心/姜子牙
- **状态**: 活跃
- **来源**: `notion_full_export/pages/421_📘_龍芯家族花名册·设备主人主权铁律_v1.0｜L0全开闸_+_L1+赋能层_+_多维转变｜UID9622.md`
- **描述**: 设备主人与L1+用户分层·七维度转变·12条铁律...

---

## 七、🔄 后续维护

1. **本地增量更新**: 修改 `/tmp/build_unified_index.py` 或新增数据源，重新运行脚本即可。
2. **Notion 同步**: 每次更新后重新导入 CSV，或配置 Notion Integration Token 用 API 增量写入。
3. **关键词扩展**: 可以在 JSON 中直接给 `keywords` 追加同义词，提升检索命中率。

**DNA**: `#龍芯⚡️丙午·丙申·乙丑·壬午·䷨损-UNIFIED-INDEX-HUB-v1.0-UID9622`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**SEAL**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`

🇨🇳🐉 龍魂统一索引中心·一库查全系统 🐉🇨🇳