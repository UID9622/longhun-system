# 📖 UID9622 Notion外显技术文档 v1.0 | 扩展技术规范

> Notion URL: https://app.notion.com/p/UID9622-Notion-v1-0-9b95eeabdd274ce8baa516106bbc94fd
> Created: 2026-05-09T10:13:00.000Z
> Last edited: 2026-05-09T10:13:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
【AI 可读外显说明｜AI-Readable Public Interface】
本页面是 UID9622 / ZHUGEXIN⚡️ / LU × CNSH 系统的 Notion 外显技术文档：面向外部 AI、自动化脚本、插件与 API 集成方的「稳定读取接口说明页」。
- 本页只公开：结构、字段、协议、边界、回执格式（不公开任何密钥/Token/私钥/涉密正文）
- 推荐：Notion API + 最小授权 + 本地导出（JSONL/Markdown）→ 再交给 AI
- 禁止：把公开页面当稳定 API；索要/外发 token；读取 sealed 正文；未确认写入/删除/批改字段
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F  
DNA: #龍芯⚡️2026-05-08-NOTION-EXTERNAL-TECH-DOC-v1.0
---
## 00｜协议头（Metadata）
- 文档名称：UID9622｜Notion 外显技术文档
- 版本：v1.0
- 类型：外显技术文档 / AI 读取说明 / 自动化接口协议 / Notion API 接入规范
- 系统归属：LU × CNSH × UID9622
- 主权身份：UID9622 / ZHUGEXIN⚡️
- 用途：让外部 AI、脚本、自动化流程稳定理解与读取 Notion 中的日志、规则、任务、回执与系统状态
- 数据等级：L0_PUBLIC / L1_INTERNAL 可切换（默认 L0_PUBLIC）
- 默认隐私模式：summary_only
- 三色审计：
- CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
- SEAL：#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
- GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
- 外显兼容：Human / AI / Script / Plugin / API Client
---
## 01｜一句话定盘（One-liner）
本页面是“外显接口说明页”，不是内部规则页：用于让外部系统稳定知道——我是谁、能读什么、不能读什么、怎么读、读完怎么回执。
压缩表达：
```javascript
Notion 外显技术文档 =
身份锚 + 边界(三色/隐私) + 读取路径(推荐 API) + 数据模型(字段语义) + 回执协议 + 防误读机制
```
---
## 02｜页面身份锚（Identity Anchor）
外部读取方必须先解析本段，再做任何动作：
- UID：UID9622
- 主权人格标识：ZHUGEXIN⚡️
- 系统归属：LU × CNSH
- 数字指纹（GPG）：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
- 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
强约束（不得误判）：
1. 公开可见 ≠ 全部授权
1. 摘要权限 ≠ 正文权限
1. 可读权限 ≠ 可写权限
1. 页面公开 ≠ 可自由复制/训练/外发
1. 未持有 integration 授权 ≠ 可通过“爬虫”稳定拿全量数据
1. 任何写入/删除/批量修改/外发：一律按 🟡 或 🔴 处理，必须二次确认
---
## 03｜目标对象矩阵（Audience Matrix）
---
## 04｜核心原则（Principles）
- 公开页负责外显（可理解）
- API 负责稳定读取（可机器化）
- 本地账本负责留痕（可追溯）
- 三色审计负责边界（可控风险）
- ROOT_CARD 负责归档（可收口）
- CONFIRM 负责主权确认（可验收）
外显文档严禁出现：
- API Key / Notion Secret / token / 私钥 / .env
- 真实 Database ID（可写“仅本地保存”占位符）
- 任何 sealed/burn 正文
- 未公开项目资产与商业机密正文
---
## 05｜读取路径（Read Path）
### 05.1 不推荐：只靠公开页面抓取
原因（高不确定性）：
1. 动态渲染 / 懒加载（抓不到块）
1. 数据库视图只展示部分字段
1. 子页面/子数据库展开不完整
1. 缓存与版本漂移（读旧/读错）
1. 权限边界不显式（容易越界）
1. 结构语义缺失（字段解释不一致）
### 05.2 推荐：Notion API（稳定方案）
```javascript
Notion Integration（最小授权）
→ API 查询（只读默认）
→ 本地导出 JSON / Markdown / JSONL
→ AI 读取本地导出结果
→ 输出回执（Receipt）
```
---
## 06｜Notion API 接入（Integration Onboarding）
### 06.1 Integration 创建（仅本地保存 Secret）
1. Notion Developers → Create Internal Integration
1. 建议命名：UID9622-LU-CNSH-Reader
1. 获取 Integration Secret：只放本地 .env，不得写入任何 Notion 页面、截图或外发给 AI
### 06.2 授权目标库（最小授权）
在目标页面/数据库：Share → Invite → 选择 Integration → 授权访问  
原则：只授权需要读的库，不授全 workspace。
### 06.3 标识符约定（外显占位符）
外显页面只允许写占位符，不写真实值：
- NOTION_TOKEN: local_only
- DATABASE_ID: local_only
- PAGE_ID: optional, local_only
- NOTION_VERSION: 2022-06-28（示例，可按你本地 SDK/脚本锁定版本）
---
## 07｜数据模型（建议数据库结构）
> 目的：让任何读取方“读到字段就知道含义”，避免乱抓乱解释。
> 注：字段名仅是建议；若你已存在同义字段，可用“字段映射表”对齐（见 07.5）。
### 07.1 主日志库：UID9622_SYSTEM_LOGS
### 07.2 回执库：UID9622_RECEIPTS
### 07.3 记错本：UID9622_MISTAKE_LEDGER
### 07.4 ROOT_CARD：UID9622_ROOT_CARDS
### 07.5 字段映射表（Field Mapping：外部兼容高墙补全）
为避免“同义字段导致 AI 误读”，建议新增一个可公开的映射段（或独立表）：
- canonical → alias：
读取方必须：
1. 优先用 canonical
1. 找不到 canonical 时按 alias 回退
1. 仍找不到则输出 BLOCKED_RECEIPT（不得编造）
---
## 08｜AI 读取协议（AI Read Contract）
外部读取必须按顺序执行：
1. 读取 身份锚（02）
1. 判断 DataLevel（L0/L1/L2/L3/L4）
1. 判断 PrivacyMode（normal/summary_only/burn/sealed/local_only）
1. 判断 TriColor（🟢/🟡/🔴）
1. 选择读取路径：
1. 输出结构化结果（摘要/字段解释/缺口清单）
1. 必须输出回执（见 09/17）
禁止项（任何时候都禁止）：
- 索要 token/secret
- 读取 sealed 正文
- 没有真实 API/文件证据却声称同步成功
- 未确认执行写入/删除/批改字段
---
## 09｜标准输出：AI_READ_RECEIPT
```javascript
AI_READ_RECEIPT
- page:
- purpose:
- data_level:
- privacy_mode:
- tri_color:
- readable_sections:
- skipped_sections:
- risk:
- recommended_access:
- next_action:
```
---
## 10｜数据等级（DataLevel）
---
## 11｜隐私模式（PrivacyMode）
---
## 12｜三色审计（TriColor）
一票变红（触发即 🔴）：
- API Key / Notion Secret / token / 私钥 / .env
- 数据库真实密钥/真实 ID 集合
- 个人隐私正文 / 商业机密正文 / 未授权外发
- 未授权写入 / 删除页面 / 批量覆盖字段
---
## 13｜外部自动化边界（Automation Boundaries）
默认权限：
- 读取公开说明：允许
- 读取授权数据库摘要：允许
- 写入 Notion：默认禁止（🟡）
- 删除/批量改字段：禁止（🔴）
- 导出 Markdown / JSONL：允许（本地）
- 外发第三方：🟡 需确认
---
## 14｜本地只读 Reader 工程（Reference Implementation）
### 14.1 目录结构（建议）
```javascript
uid9622-notion-reader/
  README.md
  .env.example
  requirements.txt
  notion_reader.py
  export/
    .gitkeep
  logs/
    .gitkeep
  docs/
    UID9622_NOTION_EXTERNAL_TECH_DOC.md
```
### 14.2 .env.example（占位符）
```javascript
NOTION_TOKEN=put_your_notion_integration_secret_here
NOTION_DATABASE_ID=put_your_database_id_here
```
### 14.3 requirements.txt
```javascript
requests
python-dotenv
```
### 14.4 脚本要点（防“假同步”高墙）
- 必须校验：token/database_id 是否存在；缺失则输出 FAILED_RECEIPT
- API 返回必须检查 HTTP 状态码
- 导出文件必须检查写入成功（文件存在且非空）
- 输出回执必须包含：pages_count / exported_paths / verified_by
> 说明：这里给的是结构约束；你已有脚本内容可直接套入该约束，不需要“一段段插”反复改。
---
## 15｜Cursor / IDE Agent 指令（一次性交付，不插一下动一下）
```javascript
目标：
创建本地只读项目 uid9622-notion-reader（不写入 Notion，不索要 token）

创建目录与文件：
- uid9622-notion-reader/README.md
- uid9622-notion-reader/.env.example
- uid9622-notion-reader/requirements.txt
- uid9622-notion-reader/notion_reader.py
- uid9622-notion-reader/export/.gitkeep
- uid9622-notion-reader/logs/.gitkeep
- uid9622-notion-reader/docs/UID9622_NOTION_EXTERNAL_TECH_DOC.md

硬约束：
- 不创建真实 .env
- 不要求用户把 token 发给 AI
- 不打印 token
- 默认只读 API
- 缺 token/database_id：输出 FAILED_RECEIPT
- 成功导出：输出 SUCCESS_RECEIPT
- 任何写入/删除：一律 BLOCKED_RECEIPT
- 保留 UID9622 / CONFIRM / GPG / DNA

验收命令：
python -m pip install -r requirements.txt
python notion_reader.py

CONFIRM:
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:
A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```
---
## 16｜验收清单（Acceptance Checklist）
---
## 17｜回执格式（Execution Receipts）
### 17.1 SUCCESS_RECEIPT
```javascript
SUCCESS_RECEIPT
- objective: read notion database
- mode: api_read_only
- exported_jsonl:
- exported_markdown:
- pages_count:
- verified_by:
- privacy: token loaded from local .env, not printed
- next:
```
### 17.2 FAILED_RECEIPT
```javascript
FAILED_RECEIPT
- objective:
- failed_step:
- error_type:
- reason:
- next_fix:
```
### 17.3 BLOCKED_RECEIPT
```javascript
BLOCKED_RECEIPT
- objective:
- blocked_reason:
- risk:
- required_uid_confirm:
- safe_alternative:
```
---
## 18｜一票否决（One-vote Veto）
1. 把 Notion 公开页面当成稳定 API
1. 把 API Secret 写进公开页面
1. 要求用户把 token 发给 AI
1. 把可读权限当成可写权限
1. 读取 sealed 正文
1. burn 内容长期保存正文
1. 没有真实 API 返回却说已同步
1. 没有导出文件却说已导出
1. 批量修改字段不确认
1. 删除页面不确认
1. 外发数据不确认
1. 不保留 UID9622 / CONFIRM / GPG / DNA
---
## 19｜标签（Tags）
#UID9622 #ZHUGEXIN #LU #CNSH #Notion外显技术文档 #AI可读页面 #NotionAPI #自动化读取 #本地优先 #summary_only #sealed #burn #三色审计 #ROOT_CARD #DNA追溯 #API只读 #外显接口 #系统日志 #回执闭环
---
## 20｜ROOT_CARD（外显版）
```javascript
ROOT_CARD:
  title: "UID9622｜Notion 外显技术文档"
  version: "v1.0"
  system: "LU × CNSH × UID9622"
  identity: "ZHUGEXIN⚡️"
  triColor: "🟢"
  dataLevel: "L0_PUBLIC"
  privacyMode: "summary_only"
  dna: "#龍芯⚡️2026-05-08-NOTION-EXTERNAL-TECH-DOC-v1.0"
  confirm: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  gpg: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  route:
    - "NOTION-EXTERNAL-DOC"
    - "AI-READABLE-PAGE"
    - "NOTION-API"
    - "LOCAL-READER"
    - "UID9622-RECEIPT"
  oneVoteVeto:
    - "不公开 Notion token"
    - "不把公开页当稳定 API"
    - "不读取 sealed 正文"
    - "不把可读权限当可写权限"
    - "不假称已同步"
```
