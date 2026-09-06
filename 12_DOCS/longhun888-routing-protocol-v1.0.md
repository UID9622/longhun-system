---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# longhun888.com 路由与入口协议 v1.0

**DNA:** `#龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-LONGHUN888-ROUTING-PROTOCOL-v1.0`  
**CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**生效日期:** 2026-07-05

---

## 1. 设计目标

1. **无僵尸按钮**：`portal/` 与 `web/` 根目录下所有入口页面必须指向真实存在的文件或服务。
2. **所有创作可访问**：P0 创作工具、文章、协议、IP 资产、外部入口统一收敛到 `longhun-unified-v9.html`。
3. **协议路由清晰**：顶层路由、代理路径、静态文件三者边界明确，便于排查与扩展。

---

## 2. 服务架构

```
Internet
   │
   ▼
Cloudflare Tunnel
   │
   ▼
longhun-system/tools/longhun_portal_server.py :8777
   │
   ├── 静态服务 portal/ 根目录（longhun888.com/）
   │   ├── /index.html
   │   ├── /longhun-master-control.html
   │   ├── /longhun-unified-v9.html
   │   ├── /longhun-flow-field-v9.html
   │   ├── /longhun-28mansions-v1.html
   │   ├── /dragon_soul_9622.html
   │   ├── /current.html
   │   ├── /p0-controls/*.html
   │   ├── /articles/*.md
   │   ├── /docs/private-shared-imports/ip-assets/*.md
   │   ├── /public-content/*
   │   └── /data/*.json
   │
   ├── /editor  → 代理到 http://127.0.0.1:18000/editor（CNSH 中文编辑器）
   ├── /docs    → 精确代理到 http://127.0.0.1:18000/docs（Swagger / API 文档）
   │             /docs/ 子路径若存在本地静态文件则优先服务，避免与 Swagger 冲突
   ├── /console → 重定向到 /web/CNSH_龍魂操作台v4.0.html 或 portal/CNSH_龍魂控制台v4.0.html
   ├── /papers/ → 映射到 longhun-system/papers/（论文与协议原文）
   │
   └── 静态服务 /web/ 路径（longhun888.com/web/）
       ├── /web/CNSH_龍魂操作台v4.0.html
       ├── /web/longhun-master-control.html
       ├── /web/longhun-unified-v9.html
       ├── /web/longhun-flow-field-v9.html
       ├── /web/longhun-28mansions-v1.html
       ├── /web/dragon_soul_9622.html
       ├── /web/current.html
       └── /web/p0-controls/*.html
```

> 说明：`:18000` 为 CNSH Editor 后端；`:8777` 为门户统一入口。

---

## 3. 路由表

| 路由 | 目标文件/服务 | 状态 |
|---|---|---|
| `/` | `portal/index.html` | ✅ 就绪 |
| `/console` | 门户服务器重定向到 v4 控制台 | ✅ 就绪（服务器处理） |
| `/console?workspace=kg3d` | v4 控制台并自动嵌入 3D 矩阵 | ✅ 就绪（服务器处理） |
| `/editor/` | `:18000/editor` 代理 | ✅ 就绪（服务器代理） |
| `/docs` | `:18000/docs` 精确代理（Swagger） | ✅ 就绪（服务器代理） |
| `/docs/<subdir>/*` | 本地静态文件优先服务 | ✅ 就绪（避免 Swagger 冲突） |
| `/papers/*` | `longhun-system/papers/*` 静态映射 | ✅ 就绪（服务器处理） |
| `/longhun-master-control.html` | `portal/longhun-master-control.html` | ✅ 就绪 |
| `/longhun-unified-v9.html` | `portal/longhun-unified-v9.html` | ✅ 就绪 |
| `/longhun-flow-field-v9.html` | `portal/longhun-flow-field-v9.html` | ✅ 就绪 |
| `/longhun-28mansions-v1.html` | `portal/longhun-28mansions-v1.html` | ✅ 就绪 |
| `/dragon_soul_9622.html` | `portal/dragon_soul_9622.html` | ✅ 就绪 |
| `/current.html` | `portal/current.html` | ✅ 就绪 |
| `/web/longhun-master-control.html` | `web/longhun-master-control.html` | ✅ 就绪 |
| `/web/longhun-unified-v9.html` | `web/longhun-unified-v9.html` | ✅ 就绪 |
| `/web/longhun-flow-field-v9.html` | `web/longhun-flow-field-v9.html` | ✅ 就绪 |
| `/web/longhun-28mansions-v1.html` | `web/longhun-28mansions-v1.html` | ✅ 就绪 |
| `/web/dragon_soul_9622.html` | `web/dragon_soul_9622.html` | ✅ 就绪 |
| `/web/current.html` | `web/current.html` | ✅ 就绪 |
| `/web/CNSH_龍魂操作台v4.0.html` | `web/CNSH_龍魂操作台v4.0.html` | ✅ 就绪 |
| `/p0-controls/*.html` | `portal/p0-controls/*.html` | ✅ 就绪 |
| `/web/p0-controls/*.html` | `web/p0-controls/*.html` | ✅ 就绪 |
| `/articles/*.md` | `portal/articles/*.md` | ✅ 就绪 |
| `/docs/private-shared-imports/ip-assets/*.md` | `portal/docs/private-shared-imports/ip-assets/*.md` | ✅ 就绪 |
| `/data/*.json` | `portal/data/*.json` | ✅ 就绪 |
| `/public-content/*` | `portal/public-content/*` | ✅ 就绪 |

---

## 4. 页面清单

### 4.1 portal/*.html

| 文件 | 用途 |
|---|---|
| `index.html` | longhun888.com 首页，能力展示、控制台入口、CSDN/Notion/文章聚合 |
| `longhun-master-control.html` | 路由矩阵主控台，8 条核心路由状态 |
| `longhun-unified-v9.html` | 统一入口，展示全部 P0 创作、文章、协议、外部入口 |
| `longhun-flow-field-v9.html` | 决策流场，嵌入 `p0-controls/sancai-flow-v8.1.html` |
| `longhun-28mansions-v1.html` | 二十八宿，嵌入 `p0-controls/CNSH_龍魂星宿知识图.html` |
| `dragon_soul_9622.html` | 龍魂本体身份页，UID9622 / 龍芯北辰 / 诸葛鑫 |
| `current.html` | 当前状态仪表板，嵌入 `CNSH_龍魂控制台v4.0.html` |
| `CNSH_龍魂控制台v4.0.html` | v4 控制台（portal 版） |

### 4.2 web/*.html

| 文件 | 用途 |
|---|---|
| `index.html` | web 根入口 |
| `longhun-master-control.html` | web 路由矩阵主控台 |
| `longhun-unified-v9.html` | web 统一入口（链接到 `../portal/` 资源） |
| `longhun-flow-field-v9.html` | web 决策流场 |
| `longhun-28mansions-v1.html` | web 二十八宿 |
| `dragon_soul_9622.html` | web 龍魂本体 |
| `current.html` | web 当前状态，嵌入 `CNSH_龍魂操作台v4.0.html` |
| `CNSH_龍魂操作台v4.0.html` | v4 控制台（web 版） |
| `龍魂操作台v2.0.html` / `v3.0.html` | 历史版本保留 |

### 4.3 p0-controls/*.html（节选）

| 文件 | 用途 |
|---|---|
| `cnsh_examples.html` | CNSH 示例库 |
| `longhun-braket.html` | Bra-Ket 人格协作 |
| `longhun_hub.html` | 龍魂智能中枢 |
| `memory-editor.html` | 记忆编辑器 |
| `sancai-flow-v8.1.html` | 三才流场可视化 |
| `龍魂知识矩阵-3D-沉浸式.html` | 3D 知识矩阵 |
| `龍魂知识矩阵-沉浸式AI播音员.html` | 沉浸式 AI 播音员 |
| `CNSH_龍魂星宿知识图.html` | 龍魂星宿图 / 二十八宿 |
| `龍魂-daodejing.html` / `龍魂-yijing.html` / `龍魂-taiji.html` 等 | 中国文化章节页 |
| `龍魂-daodejing-v4.1.html` | 道德經 81 章全本 · L0 倫理錨定層 · 五級衰減模型 |
| `notion_alignment_dashboard.html` | Notion 核心页对齐看板 · L0/L1/宪法/北辰/CNSH/动态协议 |
| `cnsh_semantic_dashboard.html` | CNSH 语义接入规范 v2.0+ · 协作宣言 · 八条铁律 · §32/37/38/39 |
| `uid9622_ip_dashboard.html` | UID9622 公开 IP 展示看板 · 龍芯北辰 · 作品清单 · 对外入口 |
| `p0_feed_dashboard.html` | P0 专用投喂入口看板 · 沙盒分拣 · 五大P0交叉验证 |

### 4.4 articles/*.md（节选）

| 文件 | 用途 |
|---|---|
| `INDEX.md` | 龍魂系统文章总索引 · 民生觉醒 · 协议论文 · CSDN 发布版 |
| `2026-07-05-提前消费的真相-离火运觉醒.md` | 民生觉醒 · 离火运/提前消费/虚假销售/道德经锚定 |
| `2026-07-04-龍魂隐私白皮书_v2.0.md` | 隐私白皮书 · 数据主权 |
| `2026-07-04-UID9622-IP展示页-龍芯北辰.md` | UID9622 公开身份与作品清单 |

---

## 5. 维护规则

### 5.1 新增页面

1. 若页面属于对外门户，同时创建 `portal/<name>.html` 与 `web/<name>.html`。
2. 新页面必须：
   - 内联 CSS/JS，无外部依赖；
   - 使用统一暗色主题（`#0a0a0f` 背景，`#00d4ff` / `#a78bfa` 强调色）；
   - 顶部/底部包含 DNA 与 CONFIRM 码；
   - 提供返回 `index.html` 与 `longhun-master-control.html` 的导航。
3. 同步更新 `portal/longhun-master-control.html` 与 `web/longhun-master-control.html` 的路由卡片、统计数字、状态文案。
4. 若页面应在统一入口展示，同步更新 `longhun-unified-v9.html` 的对应卡片列表。

### 5.2 验证无僵尸链接

运行本地检查脚本（从 `longhun-system/` 目录执行）：

```bash
cd longhun-system
python3 - <<'PY'
import re
from pathlib import Path
roots = ['portal', 'web']
for root in roots:
    for f in Path(root).rglob('*.html'):
        text = f.read_text(encoding='utf-8', errors='ignore')
        links = set(re.findall(r'href=["\']([^"\']+)["\']', text))
        for link in sorted(links):
            if link.startswith(('http','#','mailto','data:','about:','javascript:')):
                continue
            if link.startswith('/'):
                target = Path('.') / link.lstrip('/')
            else:
                target = (f.parent / link).resolve().relative_to(Path('.').resolve())
            if not target.exists():
                print(f'{f}: MISSING {link} -> {target}')
PY
```

输出为空即表示无僵尸相对链接。以 `/` 开头的路由（如 `/console`、`/editor/`、`/docs`）由门户服务器处理，不纳入文件存在性检查。

### 5.3 JSON 数据文件缓存策略

门户服务器对所有 `.json` 文件响应头强制附加：

```
Cache-Control: no-store, no-cache, must-revalidate, max-age=0
Pragma: no-cache
```

避免 `data/papers.json`、`data/notion_nav.json`、`data/csdn_articles.json` 等配置更新后客户端仍用旧缓存。前端调用这些数据时应带版本戳，如 `data/papers.json?v=2`。

### 5.4 更新本协议

每次路由结构变更后：
1. 更新第 3 节路由表；
2. 更新第 4 节页面清单；
3. 追加新的 DNA 时间戳行；
4. 重新运行验证脚本。

---

## 6. DNA 与签名

- **协议 DNA:** `#龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-LONGHUN888-ROUTING-PROTOCOL-v1.1`
- **操作台 DNA:** `#龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-LONGHUN-CONSOLE-V4-0-v1.1`
- **对齐看板 DNA:** `#龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-NOTION-ALIGNMENT-DASHBOARD-v1.0`
- **主控台 DNA:** `#龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-ROUTER-MATRIX-MASTER-CONTROL-v1.1`
- **统一入口 DNA:** `#龍芯⚡️丙午·甲午·庚辰·壬午·䷑蛊-LONGHUN-UNIFIED-v9.0`
- **CONFIRM:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
- **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
- **签名原则：** 来源可查、去向可追、责任可究。

---

> “无僵尸按钮，所有创作可访问。” —— longhun888.com 入口一致性协议

```json
{
  "dna": "#龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622",
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
