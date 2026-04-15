# CNSH-64 系统技术摘要
## 开发连续性文档 | 版本: 0.3-L3-PRE

---

## 一、系统架构总览

### 1.1 三层防御模型（本地护盾）

```
┌─────────────────────────────────────────────────────────────┐
│                    本地护盾 LocalShield                      │
├─────────────────────────────────────────────────────────────┤
│  主权层 (Sovereign)  │  伦理层 (Ethical)  │  感知层 (Sense)  │
├──────────────────────┼────────────────────┼──────────────────┤
│  • GPG指纹绑定       │  • 三色审计        │  • 输入监控      │
│  • 一票否决权        │  • 洛书369验证     │  • 输出追踪      │
│  • DNA追溯码         │  • 易经卦象校验    │  • 上下文感知    │
└──────────────────────┴────────────────────┴──────────────────┘
```

**核心类定义** (`shield_core.py`):
```python
class LocalShield:
    def __init__(self, gpg_fingerprint: str):
        self.gpg = gpg_fingerprint
        self.prev_hash = "0" * 64  # 创世哈希
        self.layer_sovereign = SovereignLayer()
        self.layer_ethical = EthicalLayer()
        self.layer_sense = SenseLayer()
    
    def process(self, content: str, action: str) -> ShieldResult:
        # 1. 主权验证
        if not self.layer_sovereign.verify():
            return ShieldResult(reject=True, reason="SOVEREIGN_VETO")
        
        # 2. 伦理审查
        ethical_pass, ethical_code = self.layer_ethical.audit(content)
        if not ethical_pass:
            return ShieldResult(reject=True, reason=f"ETHICAL_{ethical_code}")
        
        # 3. 感知监控
        sense_data = self.layer_sense.monitor(content, action)
        
        # 4. 生成DNA追溯码
        dna = self._generate_dna(content, action, sense_data)
        
        return ShieldResult(
            reject=False,
            dna_trace=dna,
            ethical_score=ethical_code,
            sense_metadata=sense_data
        )
```

### 1.2 统一场公式

$$
\mathcal{U} = \mathbb{Z}_9 \times \mathbb{Z}_{10} \times \{0,1\}^6 \times \mathbb{Z}_5
$$

**各维度含义**:
- $\mathbb{Z}_9$: 洛书369数字根空间 (dr(n) ∈ {1,2,3,4,5,6,7,8,9})
- $\mathbb{Z}_{10}$: 天干地支时序编码
- $\{0,1\}^6$: 六爻状态空间 (64卦 = 2⁶)
- $\mathbb{Z}_5$: 五行相生相克循环

---

## 二、核心模块详细说明

### 2.1 DNA追溯码系统

**格式规范**:
```
#龍芯⚡️{YYYYMMDD}-{hash16}-{layer_code}-{gpg_suffix}
```

**生成算法**:
```python
def generate_dna(content: str, action: str, prev_hash: str) -> str:
    timestamp = int(time.time())
    data = f"{content}|{action}|{prev_hash}|{timestamp}"
    content_hash = hashlib.sha256(data.encode()).hexdigest()[:16]
    
    # 洛书369验证
    dr = digital_root(int(content_hash, 16))
    if dr not in {3, 6, 9}:
        # 递归调整直到符合
        content_hash = adjust_to_369(content_hash)
    
    return f"#龍芯⚡️{datetime.fromtimestamp(timestamp).strftime('%Y%m%d')}-{content_hash}"

def digital_root(n: int) -> int:
    """洛书369数字根计算"""
    return 1 + ((n - 1) % 9) if n > 0 else 0
```

**链式验证**:
```python
def verify_chain(dna_list: List[str]) -> bool:
    """验证DNA链完整性"""
    for i in range(1, len(dna_list)):
        current = parse_dna(dna_list[i])
        previous = parse_dna(dna_list[i-1])
        if current.prev_hash != previous.content_hash:
            return False
    return True
```

### 2.2 DNA-Calendar 时空胶囊

**数据模型**:
```typescript
interface TimeCapsule {
    id: string;                    // UUID
    dnaTrace: string;              // DNA追溯码
    timestamp: number;             // Unix时间戳
    content: {
        text: string;              // 文本内容
        mediaUrls: string[];       // 媒体文件URL
        tags: string[];            // 标签
    };
    context: {
        gps: [number, number];     // [lat, lng]
        weather: WeatherData;      // 天气数据
        mood: number;              // 心情指数 0-10
    };
    privacy: 'private' | 'public' | 'shared';
    notionPageId?: string;         // Notion同步ID
}
```

**时光回流实现**:
```javascript
async function triggerReflow(dnaTrace) {
    // 1. 解析DNA获取时间戳
    const timestamp = parseDNATimestamp(dnaTrace);
    
    // 2. 查询时空胶囊
    const capsule = await db.capsules.findOne({ dnaTrace });
    
    // 3. 重建场景
    const scene = {
        date: new Date(timestamp),
        location: capsule.context.gps,
        weather: await fetchHistoricalWeather(capsule.context.gps, timestamp),
        content: capsule.content,
        mood: capsule.context.mood
    };
    
    // 4. 渲染回流界面
    renderReflowScene(scene);
    
    return scene;
}
```

### 2.3 天罗地网同步系统

**架构图**:
```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  DNA-Calendar │────▶│  Sync Engine │────▶│    Notion    │
│   (SQLite)    │     │   (Python)   │     │  (Database)  │
└──────────────┘     └──────────────┘     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Conflict    │
                     │  Resolver    │
                     └──────────────┘
```

**同步器实现** (`sync_to_notion.py`):
```python
from notion_client import Client
import sqlite3
from datetime import datetime

class DNANotionSync:
    def __init__(self):
        self.notion = Client(auth=os.getenv("NOTION_TOKEN"))
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.db_path = "dna_calendar.db"
    
    def fetch_local_events(self) -> List[Dict]:
        """获取本地未同步事件"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM capsules 
            WHERE synced = 0 
            ORDER BY timestamp DESC
        """)
        return cursor.fetchall()
    
    def query_notion_existing(self) -> Set[str]:
        """查询Notion已有DNA追溯码"""
        existing = set()
        has_more = True
        start_cursor = None
        
        while has_more:
            response = self.notion.databases.query(
                database_id=self.database_id,
                start_cursor=start_cursor
            )
            for page in response["results"]:
                dna = page["properties"]["DNA追溯码"]["rich_text"][0]["text"]["content"]
                existing.add(dna)
            has_more = response["has_more"]
            start_cursor = response.get("next_cursor")
        
        return existing
    
    def create_notion_page(self, event: Dict):
        """创建Notion页面"""
        return self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "标题": {"title": [{"text": {"content": event["title"]}}]},
                "DNA追溯码": {"rich_text": [{"text": {"content": event["dna_trace"]}}]},
                "日期": {"date": {"start": event["date"]}},
                "心情": {"number": event["mood"]},
                "位置": {"rich_text": [{"text": {"content": f"{event['lat']}, {event['lng']}"}}]},
                "内容": {"rich_text": [{"text": {"content": event["content"]}}]},
                "标签": {"multi_select": [{"name": tag} for tag in event["tags"]]},
            }
        )
    
    def sync(self):
        """执行同步"""
        local_events = self.fetch_local_events()
        existing_dna = self.query_notion_existing()
        
        synced_count = 0
        for event in local_events:
            if event["dna_trace"] not in existing_dna:
                self.create_notion_page(event)
                self.mark_synced(event["id"])
                synced_count += 1
        
        return {"synced": synced_count, "total": len(local_events)}
```

### 2.4 "四敢"品质系统

**易经六爻映射**:
```
初爻 (底层) ──▶ 敢相信 (#TRUST-INIT)
二爻 ──▶ 敢吃亏 (#SACRIFICE)
三爻 ──▶ 敢说不服 (#DISSENT)
四爻 ──▶ 敢公开审计 (#AUDIT-OPEN)
五爻 (君位) ──▶ 四敢俱全 + 道德经彩蛋
上爻 (极致) ──▶ 通天大道资格
```

**品质验证算法**:
```python
class FourDareSystem:
    DARE_CODES = {
        "TRUST-INIT": "敢相信",
        "SACRIFICE": "敢吃亏", 
        "DISSENT": "敢说不服",
        "AUDIT-OPEN": "敢公开审计"
    }
    
    def __init__(self):
        self.taoist_weights = {
            "water": 0.3,    # 上善若水
            "valley": 0.25,  # 虚怀若谷
            "valley_king": 0.45  # 谷王
        }
    
    def calculate_dare_score(self, user_actions: List[Dict]) -> Dict:
        """计算四敢品质分"""
        scores = {code: 0 for code in self.DARE_CODES}
        
        for action in user_actions:
            if action["type"] == "TRUST-INIT":
                scores["TRUST-INIT"] += action["weight"]
            elif action["type"] == "SACRIFICE":
                scores["SACRIFICE"] += action["weight"] * 1.5  # 吃亏加权
            elif action["type"] == "DISSENT":
                scores["DISSENT"] += action["weight"]
            elif action["type"] == "AUDIT-OPEN":
                scores["AUDIT-OPEN"] += action["weight"] * 2.0  # 审计加权
        
        # 道德经彩蛋触发
        easter_egg = self.check_taoist_easter_egg(scores)
        
        return {
            "scores": scores,
            "total": sum(scores.values()),
            "level": self.determine_level(scores),
            "easter_egg": easter_egg
        }
    
    def check_taoist_easter_egg(self, scores: Dict) -> Optional[str]:
        """检查道德经彩蛋触发"""
        if all(s > 100 for s in scores.values()):
            return "上善若水 - 解锁私域无限权限"
        elif scores["SACRIFICE"] > 200 and scores["AUDIT-OPEN"] > 150:
            return "谷王 - 解锁公域透明通道"
        return None
```

---

## 三、数据流和接口定义

### 3.1 API 端点规范

```yaml
# DNA-Calendar API
base_url: /api/v1

endpoints:
  # 时空胶囊
  - path: /capsule/create
    method: POST
    body:
      content: string
      gps: [lat, lng]
      mood: number
      tags: string[]
    response:
      dna_trace: string
      timestamp: number

  - path: /capsule/reflow/{dna_trace}
    method: GET
    response:
      scene: TimeCapsule
      weather: WeatherData
      reconstructed: bool

  - path: /capsule/timeline
    method: GET
    query:
      start: timestamp
      end: timestamp
      tags: string[]
    response:
      capsules: TimeCapsule[]

  # 同步
  - path: /sync/notion
    method: POST
    response:
      synced: number
      conflicts: number

  # 四敢品质
  - path: /dare/score/{user_id}
    method: GET
    response:
      scores: object
      level: string
      easter_egg: string|null
```

### 3.2 数据库 Schema

```sql
-- SQLite Schema for DNA-Calendar

CREATE TABLE capsules (
    id TEXT PRIMARY KEY,
    dna_trace TEXT UNIQUE NOT NULL,
    timestamp INTEGER NOT NULL,
    title TEXT,
    content TEXT,
    media_urls TEXT, -- JSON array
    tags TEXT, -- JSON array
    lat REAL,
    lng REAL,
    weather_temp REAL,
    weather_condition TEXT,
    mood INTEGER,
    privacy TEXT DEFAULT 'private',
    notion_page_id TEXT,
    synced INTEGER DEFAULT 0,
    created_at INTEGER DEFAULT (strftime('%s', 'now')),
    updated_at INTEGER DEFAULT (strftime('%s', 'now'))
);

CREATE INDEX idx_capsules_timestamp ON capsules(timestamp);
CREATE INDEX idx_capsules_dna ON capsules(dna_trace);
CREATE INDEX idx_capsules_synced ON capsules(synced);

CREATE TABLE dare_actions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    action_type TEXT NOT NULL, -- TRUST-INIT, SACRIFICE, DISSENT, AUDIT-OPEN
    weight REAL DEFAULT 1.0,
    context TEXT, -- JSON
    dna_trace TEXT,
    timestamp INTEGER DEFAULT (strftime('%s', 'now')),
    FOREIGN KEY (dna_trace) REFERENCES capsules(dna_trace)
);

CREATE TABLE shield_logs (
    id TEXT PRIMARY KEY,
    dna_trace TEXT NOT NULL,
    layer TEXT NOT NULL, -- sovereign, ethical, sense
    action TEXT NOT NULL,
    result TEXT NOT NULL,
    timestamp INTEGER DEFAULT (strftime('%s', 'now'))
);
```

---

## 四、部署和配置指南

### 4.1 环境变量

```bash
# .env 文件
NOTION_TOKEN=secret_xxx
NOTION_DATABASE_ID=8f5b4ac0baed40d392e6fca1ff3901de
GPG_FINGERPRINT=YOUR_GPG_KEY_FINGERPRINT
SHIELD_MODE=strict  # strict | normal | permissive
DNA_CHAIN_VERIFY=true
```

### 4.2 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "shield_server.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  shield:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    
  sync:
    build: .
    command: python sync_to_notion.py --daemon
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    depends_on:
      - shield
```

### 4.3 系统服务配置

```ini
# /etc/systemd/system/cnsh-shield.service
[Unit]
Description=CNSH-64 Local Shield
After=network.target

[Service]
Type=simple
User=cnsh
WorkingDirectory=/opt/cnsh64
Environment=PYTHONPATH=/opt/cnsh64
ExecStart=/opt/cnsh64/venv/bin/python shield_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## 五、待办事项和下一步计划

### 5.1 当前状态

- [x] 本地护盾核心框架
- [x] DNA追溯码生成与验证
- [x] DNA-Calendar前端实现
- [x] 时光回流功能
- [x] Notion数据库创建
- [x] 天罗地网同步器框架
- [x] 四敢品质系统设计
- [x] 易经六爻映射
- [x] 道德经彩蛋机制

### 5.2 待开发 (L3注册表优先级)

- [ ] **L3注册表** - 私域/公域边界判定系统
  - 判定算法: 基于GPS围栏 + 内容敏感度分析
  - 自动分级: private | shared | public
  - 边界熔断: 异常访问自动切断

- [ ] **元数据投影引擎**
  - GPS坐标实时地形生成
  - 文化内容哈希化投影
  - 无需下载的实时渲染

- [ ] **v0.3地图沉浸层**
  - 3D场景重建
  - VR/AR支持
  - 多用户同步

### 5.3 论文相关

- [ ] arXiv审核通过 (等待中)
- [ ] 洛书369论文PDF生成
- [ ] CNSH技术规范补充材料

### 5.4 近期优先级

1. **L3注册表开发** - 焊死私域/公域边界
2. **天罗地网部署** - 本地环境自动化
3. **四敢品质标记** - 自动识别与加权
4. **元数据投影原型** - GPS→地形生成

---

## 六、关键代码片段速查

### 6.1 DNA追溯码生成

```python
import hashlib
import time
from datetime import datetime

def generate_dna(content: str, action: str, prev_hash: str = "0" * 64) -> str:
    timestamp = int(time.time())
    data = f"{content}|{action}|{prev_hash}|{timestamp}"
    hash16 = hashlib.sha256(data.encode()).hexdigest()[:16]
    date_str = datetime.fromtimestamp(timestamp).strftime('%Y%m%d')
    return f"#龍芯⚡️{date_str}-{hash16}"
```

### 6.2 洛书369数字根

```python
def digital_root(n: int) -> int:
    return 1 + ((n - 1) % 9) if n > 0 else 0

def is_369(n: int) -> bool:
    return digital_root(n) in {3, 6, 9}
```

### 6.3 六爻转卦象

```python
YAO_TO_HEXAGRAM = {
    (0,0,0,0,0,0): "坤为地", (1,1,1,1,1,1): "乾为天",
    (0,0,0,0,0,1): "地雷复", (1,0,0,0,0,0): "山地剥",
    # ... 64卦完整映射
}

def yaos_to_hexagram(yaos: tuple) -> str:
    return YAO_TO_HEXAGRAM.get(yaos, "未知")
```

### 6.4 Notion同步检查

```python
def check_notion_sync_status(notion_client, database_id: str) -> Dict:
    response = notion_client.databases.query(database_id=database_id)
    return {
        "total_pages": len(response["results"]),
        "has_more": response["has_more"],
        "last_edited": max(
            p["last_edited_time"] for p in response["results"]
        ) if response["results"] else None
    }
```

---

## 七、故障排查

### 7.1 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| DNA链断裂 | 哈希不匹配 | 检查prev_hash传递 |
| Notion同步失败 | Token过期 | 刷新NOTION_TOKEN |
| 时光回流失败 | 天气API限制 | 使用缓存数据 |
| GPG验证失败 | 密钥未导入 | `gpg --import key.asc` |

### 7.2 调试命令

```bash
# 验证DNA链
python -c "from shield_core import verify_chain; verify_chain(['dna1', 'dna2'])"

# 检查Notion连接
curl -H "Authorization: Bearer $NOTION_TOKEN" \
     https://api.notion.com/v1/users/me

# 查看本地数据库
sqlite3 dna_calendar.db "SELECT * FROM capsules ORDER BY timestamp DESC LIMIT 5;"
```

---

## 八、联系与传承

**系统代号**: CNSH-64  
**核心精神**: 有智慧的老兵，不跪  
**祖师爷定位**: 济公活佛，网络清道夫  
**终极愿景**: 私域无限，公域透明，数字永生，元数据投影  

**开发连续性保证**: 本文档包含从0.1到0.3-L3-PRE的全部技术细节，确保任何开发者可在中断后继续推进。

---

*文档生成时间: 2026-03-23*  
*版本: 0.3-L3-PRE*  
*DNA追溯码: #龍芯⚡️20260323-a1b2c3d4e5f67890*
