---
DNA: #龍芯⚡️丙午·丙申·丁丑·己卯·䷭升-KB-API-GUIDE-v1.0-7f4e9c2a
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）
# 抬头模板: [2] 🔧 工程落地执行型（脚本/部署/API）
---

# 龍魂 · Notion 知识库社区接入指南 v1.0

> 上位协议: `01_protocols/LH-NOTION-KB-REFERENCE-ARCHITECTURE-v1.0.md`（L4/L5 架构）
> 本文 = 开发者/社区如何调用 `uid9622.cn/api/kb/*` 的实操手册。

## 0. 一句话

**只读、公开、零鉴权（webhook 除外）**——社区直接 `curl` 调 `https://uid9622.cn/api/kb/*` 检索龍魂知识库摘要，详情链回 Notion，全程不落私密数据。

## 1. 端点总览

| 端点 | 方法 | 功能 | 鉴权 |
|---|---|---|---|
| `GET /api/kb/search?q=<关键词>` | GET | 关键词检索（摘要+链接+DNA） | 公开 |
| `GET /api/kb/search?category=<分类>` | GET | 按分类检索 | 公开 |
| `GET /api/kb/page/{id}` | GET | 页面详情（有 token 走 Notion live，无则索引摘要） | 公开 |
| `GET /api/kb/dna?title=<标题>&category=<分类>` | GET | 社区实时计算 DNA | 公开 |
| `POST /api/kb/webhook` | POST | Notion 变更回调（重算 DNA+更新索引） | X-API-Key |

Base URL: `https://uid9622.cn`

## 2. 快速示例

### 2.1 关键词检索

```bash
curl -sG --data-urlencode "q=汇率" \
  "https://uid9622.cn/api/kb/search"
```

```json
{
  "query": "汇率",
  "hits": 1,
  "returned": 1,
  "items": [
    {
      "id": "3c503ac9-...",
      "title": "龍魂审计链·汇率接口文档 v1.1",
      "category": "",
      "summary": "完整版见 Notion: https://app.notion.com/p/...",
      "dna": "#龍芯⚡️丙午·丙申·辛未·戊戌·䷢晋-KB-SYNC-35bd4ce5",
      "url": "https://app.notion.com/p/...",
      "updated_at": null
    }
  ],
  "dna_engine": "lh_dna_generator.v2.0",
  "sovereign": "UID9622"
}
```

> ⚠️ 中文参数必须 URL 编码（`curl -G --data-urlencode`），裸中文会导致 nginx 拒收。

### 2.2 页面详情

```bash
curl -s "https://uid9622.cn/api/kb/page/3c503ac9-098d-8143-931d-fcb9044a350d"
```

### 2.3 实时计算 DNA

```bash
curl -sG --data-urlencode "title=龍魂·三才算法" \
  --data-urlencode "category=算法" \
  "https://uid9622.cn/api/kb/dna"
```

### 2.4 Python 示例

```python
import urllib.parse, urllib.request, json

BASE = "https://uid9622.cn"

def kb_search(q: str) -> dict:
    url = f"{BASE}/api/kb/search?" + urllib.parse.urlencode({"q": q})
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.load(r)

def kb_dna(title: str, category: str = "DOC") -> dict:
    url = f"{BASE}/api/kb/dna?" + urllib.parse.urlencode(
        {"title": title, "category": category})
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.load(r)

if __name__ == "__main__":
    print(json.dumps(kb_search("汇率"), ensure_ascii=False, indent=2))
```

### 2.5 Webhook 回调（运维/集成方）

```bash
curl -s -X POST "https://uid9622.cn/api/kb/webhook" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: ${KB_WEBHOOK_KEY}" \
  -d '{"type":"page","id":"3c503ac9-...","action":"updated"}'
```

## 3. 数据与安全边界

1. **只读公开**：search/dna 无需任何 key；返回的只有 摘要+链接+DNA，**不返回全文、不返回私密字段**。
2. **鉴权隔离**：webhook 必须 `X-API-Key`（`KB_WEBHOOK_KEY`），无 key 一律 401。
3. **NOTION_TOKEN 默认不入鲲鹏**（D2 数据·入云需授权）——`page` 端点无 token 时自动降级为本地索引摘要；live 代理需 UID9622 单独授权。
4. **不可见即不可服务**：社区只能检索到「已共享给 integration 的页面」。未共享内容物理不可见——这是硬边界，不是技术问题。
5. **数据主权**：Notion 是唯一完整版真源，本地+鲲鹏只存索引摘要（省内存原则）。所有内容归属名 `诸葛鑫 | UID9622`，思想层 CC BY-NC-SA 4.0，代码层 MulanPSL v2。

## 4. 索引更新机制（2026-08-25 落地）

| 环节 | 说明 |
|---|---|
| 本地同步 | `python3 bin/lh_notion_kb.py sync`（list+dna+index 三合一） |
| 定时任务 | Mac launchd `com.longhun.kb-sync` · 每天 06:00 自动全链路 |
| 推送鲲鹏 | `bash bin/lh_kb_sync.sh all`（rsync → `/root/.longhun/data/notion_kb/index.json`） |
| 公网生效 | nginx `/api/kb/` → 127.0.0.1:9633（`longhun-kb-api.service`） |
| 审计留痕 | `.audit/kb_sync.log`（append-only）· 推送尺寸一致性校验 |

## 5. 限流与可用性

- 当前为轻量只读服务，未设限流；社区请文明调用（检索建议间隔 ≥ 1s）。
- 健康状况: `curl -s https://uid9622.cn/api/kb/health`
- 服务异常: 鲲鹏 systemd `systemctl status longhun-kb-api` · 恢复后 `bin/lh_kb_sync.sh all` 重推索引。

## 6. 变更记录

| 版本 | 日期 | 内容 |
|---|---|---|
| v1.0 | 2026-08-25 | 首版: 四端点文档 + curl/Python 示例 + 数据主权边界 + 索引同步机制 |

<!-- GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F -->
