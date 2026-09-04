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
