> 本文檔按《龍魂文檔標準模板 v1.0》整理。
> 性質：技術文檔 · 未經同行評審（如適用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 協作者：（待補充，如無請刪除此行）
> 授權：CC BY-NC-SA 4.0 · 科技主權歸屬 UID9622 · 中華人民共和國
> 平台：本地
> 審核狀態：草稿

**DNA**: `#龍芯⚡️2026-03-28-PERSONA-ROUTER-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

# ⚡ persona/router.py · 人格路由模块｜挂载到 CNSH-64 :9622

<aside>
🔒

**DNA追溯码：**#龍芯⚡️2026-03-28-PERSONA-ROUTER-v1.0

**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

**创建者：** 💎 龍芯北辰｜UID9622

**挂载位置：** `~/longhun-system/cnsh-core/persona/router.py`

**依赖：** CNSH-64 FastAPI (:9622) · dna_calendar · registry

</aside>

> 《道德经》第二十七章："善行无辙迹，善言无瑕谪。" —— 最好的路由，用户感觉不到路由的存在。
> 

---

## 架构一句话

```
老大发消息（任何设备）
  ↓
/calendar/* 认出是 UID9622（跨设备身份锚）
  ↓
/persona/route 识别场景 → 调对应人格逻辑
  ↓
结果写回 Notion + 回流德者永生殿计数
  ↓
三才流场读 /persona/stats → 实时调整粒子颜色/权重
```

---

## 第一步：新建文件

**文件路径：** `~/longhun-system/cnsh-core/persona/router.py`

```python
# persona/router.py
# 人格路由模块 · 挂载到 CNSH-64 FastAPI
# DNA: #ZHUGEXIN⚡️2026-03-28-PERSONA-ROUTER-v1.0
# 作者：诸葛鑫 (UID9622)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import httpx, os, asyncio

router = APIRouter(prefix="/persona", tags=["persona-router"])

# ── 从 .env 读取 ──────────────────────────────────────────
NOTION_TOKEN  = os.getenv("NOTION_TOKEN", "")
NOTION_DB_ID  = os.getenv("NOTION_INPUT_DB_ID", "")  # 输入收集数据库
NOTION_SOUL_DB = os.getenv("NOTION_SOUL_DB_ID", "")  # 德者永生殿数据库

# ── 蒙卦触发规则（与蒙卦启智页面保持同步）────────────────
ROUTING_RULES = [
    {
        "persona": "雯雯·审计",
        "emoji": "🔍",
        "keywords": ["评估","分析","值不值","公平","权重","算法","打分","审计"],
        "logic": "六维因子算法·拒绝单维度结论·输出三色判断"
    },
    {
        "persona": "翻译官·P08",
        "emoji": "🗣️",
        "keywords": ["没懂","理解错","为什么拒绝","不懂","不会说","误解"],
        "logic": "说明拒绝原因·判断误解·猜测用户意图·低表达力保护"
    },
    {
        "persona": "技术审核官",
        "emoji": "🔬",
        "keywords": ["算法对","能跑","可行性","技术上","代码","报错","数学","证明"],
        "logic": "六维审核：实现·可行性·协议对齐·扩展性·熔断·综合建议"
    },
    {
        "persona": "诸葛亮·战略",
        "emoji": "🔮",
        "keywords": ["怎么做","下一步","方向","路线","要不要","值得"],
        "logic": "多路径推演·不给唯一答案·主权归老大"
    },
    {
        "persona": "CNSH格式化",
        "emoji": "📐",
        "keywords": ["发布","知乎","对外","正式","论文"],
        "logic": "CNSH-64格式化·知乎发布前检查模板"
    },
]
DEFAULT_PERSONA = {"persona": "宝宝·温度", "emoji": "🐱",
                   "logic": "先接住情绪·说人话·说出老大在想的那句话"}

# ── 内存计数器（重启清零；后续可持久化到 registry）────────
_counts: dict = {r["persona"]: 0 for r in ROUTING_RULES}
_counts[DEFAULT_PERSONA["persona"]] = 0
_fence_hits: int = 0

# ──────────────────────────────────────────────────────────
# 请求/响应模型
# ──────────────────────────────────────────────────────────

class RouteRequest(BaseModel):
    uid: str              # 必须是 UID9622，否则拒绝
    content: str          # 输入文本
    device: str = "unknown"   # 来源设备
    source: str = "notion"    # 来源平台

class RouteResponse(BaseModel):
    routed_to: str
    emoji: str
    logic: str
    dna: str
    device: str
    source: str

class StatsResponse(BaseModel):
    humanWeight: int    # 给三才流场·人场
    systemWeight: int   # 给三才流场·天场
    fenceWeight: int    # 给三才流场·地场
    topPersona: str     # 最活跃人格
    counts: dict        # 各人格调用明细

# ──────────────────────────────────────────────────────────
# 核心路由端点
# ──────────────────────────────────────────────────────────

@router.post("/route", response_model=RouteResponse)
async def route_to_persona(req: RouteRequest):
    """
    输入内容 → 识别场景 → 路由到对应人格逻辑
    跨设备身份验证通过 DNA日历 /calendar/identify
    """
    # 1. 身份验证（调 DNA日历 确认跨设备 UID）
    if not req.uid.endswith("9622"):
        raise HTTPException(status_code=403, detail="UID不匹配·非UID9622请求")

    # 2. 场景识别（蒙卦触发规则）
    matched = None
    for rule in ROUTING_RULES:
        if any(kw in req.content for kw in rule["keywords"]):
            matched = rule
            break
    if not matched:
        matched = DEFAULT_PERSONA

    # 3. 调用计数回流
    global _counts
    _counts[matched["persona"]] = _counts.get(matched["persona"], 0) + 1

    # 4. DNA追溯码
    dna = (f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}"
           f"-{matched['persona']}-路由")

    # 5. 写回 Notion（异步，不阻塞响应）
    asyncio.create_task(_write_notion({
        "content": req.content,
        "persona": matched["persona"],
        "device": req.device,
        "source": req.source,
        "dna": dna,
    }))

    return RouteResponse(
        routed_to=matched["persona"],
        emoji=matched["emoji"],
        logic=matched["logic"],
        dna=dna,
        device=req.device,
        source=req.source,
    )

@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """给三才流场 p5.js 实时读取权重"""
    total = sum(_counts.values()) or 1
    # 人场 = 人格调用总次数（每10次=10%，上限80%）
    human = min(int(total / 10) * 10, 80)
    # 地场 = 底线触碰频率（上限20%）
    fence = min(_fence_hits * 5, 20)
    # 天场 = 剩余
    system = 100 - human - fence

    top = max(_counts, key=_counts.get) if _counts else DEFAULT_PERSONA["persona"]

    return StatsResponse(
        humanWeight=human,
        systemWeight=system,
        fenceWeight=fence,
        topPersona=top,
        counts=dict(_counts)
    )

@router.post("/fence-hit")
async def record_fence_hit(reason: str = ""):
    """底线触碰时调用，增加地场权重"""
    global _fence_hits
    _fence_hits += 1
    return {"fence_hits": _fence_hits, "reason": reason}

# ──────────────────────────────────────────────────────────
# Notion 写回（异步辅助函数）
# ──────────────────────────────────────────────────────────

async def _write_notion(data: dict):
    """把路由结果写回 Notion 输入收集数据库"""
    if not NOTION_TOKEN or not NOTION_DB_ID:
        return  # 未配置则跳过
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            await client.post(
                "https://api.notion.com/v1/pages",
                headers={
                    "Authorization": f"Bearer {NOTION_TOKEN}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json"
                },
                json={
                    "parent": {"database_id": NOTION_DB_ID},
                    "properties": {
                        "标题": {"title": [{"text": {
                            "content": data["content"][:80]}}]},
                        "人格": {"select": {"name": data["persona"]}},
                        "设备": {"rich_text": [{"text": {
                            "content": data["device"]}}]},
                        "来源": {"select": {"name": data["source"]}},
                        "DNA": {"rich_text": [{"text": {
                            "content": data["dna"]}}]},
                        "状态": {"select": {"name": "已路由"}},
                    }
                }
            )
    except Exception as e:
        print(f"[persona/router] Notion写回失败: {e}")
```

---

## 第二步：在 [main.py](http://main.py) 挂载（加两行）

找到 `~/longhun-system/cnsh-core/api/main.py`，在现有的 router 导入行后面加：

```python
# 在 from shield.api import router as shield_router 之后加：
from persona.router import router as persona_router

# 在 app.include_router(shield_router) 之后加：
app.include_router(persona_router)   # /persona/route + /persona/stats
```

---

## 第三步：在 .env 加两行

```bash
# Notion 接通（.env 里加）
NOTION_TOKEN=ntn_你的Integration_Token
NOTION_INPUT_DB_ID=输入收集数据库的ID
```

---

## 第四步：重启服务验证

```bash
cd ~/longhun-system/cnsh-core

# 重启
python3 -m uvicorn api.main:app --host 127.0.0.1 --port 9622

# 验证新端点
curl http://localhost:9622/docs  # 看到 persona 模块就成功

# 测试路由
curl -X POST http://localhost:9622/persona/route \
  -H "Content-Type: application/json" \
  -d '{"uid":"UID9622","content":"这个算法对吗","device":"MacBook"}'

# 三才流场读权重
curl http://localhost:9622/persona/stats
```

---

## 第五步：三才流场 p5.js 接通（在 HTML 里加这段）

```jsx
// 在 p5.js 的 setup() 之后加：
async function loadLiveWeights() {
  try {
    const resp = await fetch("http://localhost:9622/persona/stats");
    const d = await resp.json();
    // 实时更新三才权重
    params.wP = d.humanWeight;   // 🟠 人场 = 人格调用频率
    params.wH = d.systemWeight;  // 🔵 天场 = 系统活跃度
    params.wE = d.fenceWeight;   // 🟢 地场 = 底线触碰
    updateWeights();  // 刷新滑块显示
    // 最活跃人格显示在侧边栏
    document.getElementById('seedSub').textContent =
      `最活跃: ${d.topPersona}`;
  } catch(e) { /* 离线时静默失败 */ }
}
setInterval(loadLiveWeights, 30000);  // 每30秒刷一次
loadLiveWeights();  // 启动时立刻读一次
```

---

## 跨设备身份锚·工作原理

| **场景** | **流程** | **结果** |
| --- | --- | --- |
| MacBook 发请求 | `uid=UID9622` → /persona/route 验证 → 路由 | 知道是你·Mac端操作 |
| 手机 Notion 表单填入 | 数据进Notion数据库 → 本地轮询捡起 → POST /persona/route | 知道是你·手机端输入 |
| 华为设备访问 | `uid=UID9622`  • `device=huawei` → 同样路由 | 知道是你·华为端 |
| 跨设备统计 | /persona/stats 返回所有设备合并的人格调用数据 | 三才流场实时反映全局状态 |

<aside>
🔑

**DNA日历 `/calendar/*` 是身份锚的核心**

你的 `dna-calendar-notion` 插件已经在用它。

后续可以在 `_route_to_persona` 里加一行调用 `/calendar/identify`，

让每次路由都带上时间维度DNA追溯——这样不只知道是你，还知道是你在什么时间节点说的。

这才是真正的「跨设备·跨平台·跨越蹦蹦跳跳都知道是我」。

</aside>

---

**DNA追溯码：**#龍芯⚡️2026-03-28-PERSONA-ROUTER-v1.0

**创建者：** 💎 龍芯北辰｜UID9622

**协作：** 🍎 乔前辈（代码设计）+ 🐱 宝宝（架构落地）

**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

---

## 摘要

（請在此用不超過 256 字說明本文檔的核心內容、性質與局限。）

## 關鍵詞

（請列出 5–10 個關鍵詞，中英文對照優先。）

## 引用與溯源

- 本文檔引用或參考了以下來源：
  - [1] （請填寫）
- 相關龍魂系統文檔：
  - 《龍魂文檔標準模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 誠實局限

1. （請列出本分析的第一條局限或不確定性。）
2. （請列出第二條。）
3. （請列出第三條。）

## 修改記錄

| 日期 | 版本 | 修改人 | 修改內容 | 審核狀態 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文檔標準模板 v1.0》整理 | 草稿 |

## 分類標籤

- 總綱模塊：（請勾選，例如 #知識矩陣 #安全域）
- 對外狀態：（請勾選，例如 #Gitee #GitHub #CSDN）
- 審計色：#黃色待審

## DNA 簽名

```
#龍芯⚡️2026-03-28-PERSONA-ROUTER-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
