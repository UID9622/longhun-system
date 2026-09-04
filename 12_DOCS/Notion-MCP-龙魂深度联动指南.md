# 🐉 龍魂 · Notion Master MCP 深度联动指南 v1.0

> DNA: #龍芯⚡️2026-09-04-NOTION-MCP-DEEP-LINKAGE-GUIDE-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622） · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F · 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 1. 一句话

把 Notion 从「外部知识库」变成龍魂生态的**数据主控层**：5 个新工具把 Notion 页面/评论/树 ↔ 龍魂的拓扑 / 审计 / 耻辱墙 / 记忆 / 镜像 **五个引擎** 直连，全部子进程/import 复用 `lh topo` / `lh gov` / `lh judge` / `lh brain`，不重复造轮子。

## 2. 架构总览

```
Notion (云端·D2机密正文)
   │  (Mac主控层·唯一持 token)
   ▼
Notion Master MCP Server (20 工具·含 5 生态联动)
   ├─ lh topo    ← notion_sync_to_topo / notion_export_topo   (拓扑注册/导出)
   ├─ lh gov     ← notion_audit_page                           (三色红线审计)
   ├─ lh judge   ← notion_archive_to_shamewall                 (🔴红线上耻辱墙)
   ├─ lh brain   ← notion_comment_to_memory                    (评论→长期记忆)
   └─ append-only 审计链 ~/.longhun/notion_audit.jsonl         (一切操作留痕)
   │
   ▼ 目录快照(catalog.json·id/标题/URL/审计尾·零正文) rsync
鲲鹏 8768 只读镜像端点 (lh_mcp_notion.py·零 token·供鸿蒙等外部只读)
```

## 3. 五个生态联动工具

| 工具 | 作用 | 联动引擎 | 副作用 |
|:---|:---|:---|:---|
| `notion_sync_to_topo` | 页面注册/更新为拓扑节点 | `lh_topo.py node` | 写拓扑 JSON |
| `notion_audit_page` | 页面内容三色审计 | `lh_governance.py redline check` + 轻量本地规则 | 只读 + 审计链 |
| `notion_archive_to_shamewall` | 归档页双留痕 | `lh_judge.py 记录剽窃`（仅🔴） | PATCH 归档 + 审计链 |
| `notion_comment_to_memory` | 评论(对话)→长期记忆 | `lh_brain.py remember` | 写记忆库 |
| `notion_export_topo` | 整树导出拓扑 JSON | 内建 `_render_tree` | 写 `docs/topology/` |

## 4. 数据主权铁律（本层焊死）

1. **正文不出主控**：推到鲲鹏/鸿蒙的只有**目录快照**（无正文、无 token）。8768 端点零 token。
2. **耻辱墙只收红线**：普通归档走 append-only 审计链；仅内容判 `🔴` 才 `记录剽窃` 上墙，保耻辱墙公信。
3. **不删除只冻结**：归档=软删除（`archived: true`），可 `restore` 恢复；操作全部留 `~/.longhun/notion_audit.jsonl`（append-only）。
4. **演练先行**：所有写动作支持 `dry_run: true` → 只记 `*_dry` 审计，不动远端/不落盘/不写库。

## 5. dry_run 演练模式

```json
// 演练：不注册拓扑
{"name": "notion_sync_to_topo", "arguments": {"page_id": "…", "dry_run": true}}

// 演练：不归档不写墙，先看判色
{"name": "notion_archive_to_shamewall", "arguments": {"page_id": "…", "reason": "整理", "dry_run": true}}

// 演练：不落盘，先看节点数
{"name": "notion_export_topo", "arguments": {"page_id": "…", "name": "xx", "dry_run": true}}
```

审计链会记 `sync_to_topo_dry` / `archive_to_wall_dry` / `export_topo_dry` / `comments_to_brain_dry` / `audit_page_dry`。

## 6. 镜像链路（Mac 主控 → 鲲鹏 8768）

```bash
lh notion status                  # 本地镜像概况（~/.longhun/notion_mirror/）
lh notion sync --no-push          # 重建 catalog.json（本地·不推）
lh notion sync                    # 重建并 rsync 推鲲鹏 /srv/…/notion/
lh notion sync --topo             # 附推 docs/topology/ 摘要
lh health                         # 含 Notion 镜像/审计链检查（v1.2）
```

鲲鹏侧 `lh-notion-mcp.service`（端口 8768·127.0.0.1）工具：
`get_mirror_status` / `search_catalog` / `list_catalog` / `recent_audit` / `topo_snapshot`。

> 部署到鲲鹏：`bash deploy/longhun-mcp/deploy_to_kunpeng.sh`（4.5 步安装 8768）——✅ **已于 2026-09-04 上线**（确认码批准）。
> 外部访问模型见 `docs/鲲鹏MCP接入指南-v1.0.md`（默认 SSH 隧道，不裸奔端口）。

**在线状态（2026-09-04 实测）**：`systemctl status lh-notion-mcp` active · 127.0.0.1:8768 MCP ping OK · `get_mirror_status` = 2054 页 · `search_catalog` 主控命中 13 · `recent_audit` 11 条 · 快照目录 `/opt/longhun-system/deploy/longhun-mcp/notion/`（Mac 侧 `lh notion sync` 推送）。

## 7. 验证记录（2026-09-04 实测）

| 项 | 结果 |
|:---|:---|
| `notion_export_topo` 主控台 depth=1 | ✅ 57 节点 · JSON 可读 |
| `notion_audit_page` | ✅ 🟢 通过（标题解析修复后中文正常） |
| `notion_sync_to_topo` 通心译 | ✅ 23→24 节点 |
| 镜像 sync / status | ✅ 2049 页 · 8768 本地 smoke 通过 |
| dry_run × 4 | ✅ 全部只记 `*_dry` 无真改 |

## 8. 排障

| 症状 | 处置 |
|:---|:---|
| 工具报 `lh 调用失败` | 确认 `08_BIN/lh_*.py` 在位；`LH_ROOT` 推导正确（第 3 级父目录） |
| 标题显示 `(xxxx… )` | 旧版 `_title_of` 只认 `rich_text` 键；已修复支持 `title` 键 + 库顶层 title |
| 审计链不写 | `~/.longhun/notion_audit.jsonl` 是否可写；非 append 勿手改 |
| 8768 不可达 | 鲲鹏 `systemctl status lh-notion-mcp`；本地联调先起 `python3 deploy/longhun-mcp/lh_mcp_notion.py` |

---

🐉 丙午·丁酉·辛巳·午时·䷞咸 · 🟡


---

## 💛 支持龍魂（纯自愿 · 零黑箱）

龍魂的一切免费开放。若你认可「让技术为人、为普通人生长」，可自愿支持——款项仅用于服务器与开发成本，不留一分私账。

- **收款方式**: SOL / USDC（Solana）
- **实时地址与二维码**: 见官网 [uid9622.cn](https://uid9622.cn) 底部「支持龍魂」区 — 地址由 `lh wallet` 统一管理（公司账户落地后自动切换 · 以官网为准）

> 龍魂不诱导、不施压、不道德绑架。捐与不捐，开放与尊重不变。

<!-- LH-WALLET-SUPPORT -->
