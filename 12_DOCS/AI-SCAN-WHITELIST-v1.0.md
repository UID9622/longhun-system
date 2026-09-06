---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丙申·丙寅·子时·䷓观-AI-SCAN-WHITELIST-UID9622`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# ⚡ 龍魂 · AI 扫描白名单 v1.0

**DNA:** `#龍芯⚡️丙午·丙申·丙寅·子时·䷓观-AI-SCAN-WHITELIST-UID9622`
**三色:** 🟢 通过（2026-08-20 实测盘点：真实文件 54 万，核心活跃仅约 6 万）

> **给所有 AI 的提速焊死**：全库搜索/扫描前，先按本名单跳过黑名单目录，只扫白名单核心层。
> 效果：跳过约 45 万噪音文件，搜索提速 5~8 倍。

---

## 🚫 黑名单（搜索时用 ignore_globs 一律跳过）

| 目录 | 内容 | 为什么不扫 |
|:---|:---|:---|
| `.venv` `.venv_tts` `node_modules` `__pycache__` | 虚拟环境/依赖 | 第三方代码·与本系统无关 |
| `11_DATA` | 运行时数据(13.7万) | 数据·非源码·grep 结果看 git 即可 |
| `_work` | 工作缓存(6.5万) | 临时产物·不进 git |
| `dist` `build_ide` | 构建产物 | 由源码生成·可再建 |
| `models` | 模型权重(1780) | 二进制·禁入 git |
| `archive` `_archive` `backups` `backup` | 归档/备份 | 已冻结历史·不进 git |
| `.daoyin_workspace` `tombstone_vault` `test_logs` `test_reports` `test_results` | 工具/测试产物 | 噪音 |

## ✅ 白名单（AI 重点活跃区·全库扫描优先扫这些）

| 目录 | 内容 |
|:---|:---|
| `01_protocols` (2.8K) | 协议·白皮书·铁律 |
| `02_SKILLS` (1K) | 技能定义 |
| `03_LAYERS` (1.5K) | 分层治理 |
| `08_BIN` (8.4K) | 引擎·脚本 |
| `09_TOOLS` (12.7K) | 工具 |
| `12_DOCS` (13K) | 文档 |
| `deploy` (1.5K) | 部署 |
| `personas` `agents` | 人格·AI定义 |
| `.codebuddy` | 项目配置·记忆·规则 |
| `state` `config` `20_CONFIG` | 状态·配置 |
| `web` `web_apps` | 前端 |

## 📋 用法（AI 全库搜索标准姿势）

```bash
# 搜索前先读本文件，然后：
search_content(pattern="xxx",
  ignore_globs=["**/.venv/**","**/.venv_tts/**","**/node_modules/**",
                "**/11_DATA/**","**/_work/**","**/dist/**","**/models/**",
                "**/archive/**","**/_archive/**","**/backups/**","**/backup/**"])
```

## 📌 记忆速查（并入 lh_memory_load）

- 软链双名目录（engines↔05_ENGINES、docs↔12_DOCS、tools↔09_TOOLS、bin↔08_BIN、portal↔10_PORTAL、audit↔07_AUDIT、tests↔13_TESTS、services↔04_SERVICES、layers↔03_LAYERS、cnsh.integrated↔cnsh、skills↔02_SKILLS 等）→ **无害·保留·不要当重复合并**
- `web` 与 `web_apps` → **不是重复**（前端资源 vs 独立小应用）
- git 跟踪文件 ≈ 2 万内（大目录全部已 gitignore）→ git 仓库干净，不用瘦身
- 重复/冗余判断流程：`ls -ld` → `readlink` → `stat -f %i` → 再决定，禁凭目录名判断

```json
{
  "dna": "#龍芯⚡️丙午·丙申·丙寅·子时·䷓观-AI-SCAN-WHITELIST-UID9622",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
