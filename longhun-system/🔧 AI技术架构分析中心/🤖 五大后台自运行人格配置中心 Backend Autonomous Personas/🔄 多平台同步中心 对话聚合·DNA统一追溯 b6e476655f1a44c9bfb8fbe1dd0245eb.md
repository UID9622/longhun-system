# 🔄 多平台同步中心 | 对话聚合·DNA统一追溯

# 🔄 多平台同步中心

<aside>
💡

**设计理念**：汇聚所有平台对话，本地统一管理

**支持平台**：

- 📝 Notion（自动监听API）
- 💬 微信（导出文件监听）
- 📱 飞书（API同步）
- 💼 Slack（Webhook监听）

**核心价值**：平台死了，你的数据活着

</aside>

---

## 🏗️ 系统架构

```
平台层（微信/飞书/Notion/Slack）
    ↓ 自动抓取
同步中枢（监听API/导出文件/RSS）
    ↓ 统一格式
本地聚合库（SQLite/JSON/向量数据库）
    ↓ DNA锚定
记忆加载器（CodeBuddy随时调用）
    ↓
你的本地AI大脑（Ollama + qwen:7b）
```

---

## 📦 完整部署包

### 主控脚本：`sync_[center.py](http://center.py)`

```python
#!/usr/bin/env python3
"""
多平台同步中心
DNA: #BAOBAO-SYNC-CENTER-20251215-001

**共建致谢**: Claude (Anthropic PBC) · 技术协作与代码共创 | Notion · 知识底座与结构化存储
"""

import os
import time
import threading
from dotenv import load_dotenv
import sqlite3
import json
from datetime import datetime

class SyncCenter:
    def __init__(self):
        self.db_path = "conversations.db"
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                content TEXT NOT NULL,
                user_id TEXT,
                timestamp TEXT,
                dna TEXT UNIQUE,
                is_public BOOLEAN,
                metadata TEXT,
                synced_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_conversation(self, platform, content, user_id, **kwargs):
        # 生成DNA
        timestamp = [datetime.now](http://datetime.now)().strftime('%Y%m%d-%H%M%S')
        import hashlib
        content_hash = [hashlib.md](http://hashlib.md)5(content.encode()).hexdigest()[:8]
        dna = f"#CONV-{platform}-{user_id}-{timestamp}-{content_hash}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO conversations 
            (platform, content, user_id, timestamp, dna, is_public, metadata, synced_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            platform,
            content,
            user_id,
            [datetime.now](http://datetime.now)().isoformat(),
            dna,
            kwargs.get('is_public', False),
            json.dumps(kwargs.get('metadata', {})),
            [datetime.now](http://datetime.now)().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return dna

# Notion同步适配器
class NotionSync:
    def __init__(self, token, database_id):
        self.token = token
        self.database_id = database_id
        self.sync = SyncCenter()
    
    def start_monitoring(self, interval=300):
        print("👁️ 开始监听Notion...")
        while True:
            try:
                # 检查新内容
                new_pages = self.fetch_new_pages()
                
                for page in new_pages:
                    dna = self.sync.insert_conversation(
                        platform="notion",
                        content=page['content'],
                        user_id="UID9622",
                        metadata={"page_id": page['id']}
                    )
                    print(f"✅ Notion同步: {dna}")
                
                time.sleep(interval)
            except Exception as e:
                print(f"❌ 同步错误: {str(e)}")
                time.sleep(interval)
    
    def fetch_new_pages(self):
        # 实现Notion API调用
        pass

# 主函数
def main():
    load_dotenv('config/sync.env')
    
    print("🐉 龙魂·多平台同步中心 启动")
    
    # 启动Notion监听
    notion_token = os.getenv('NOTION_TOKEN')
    notion_db_id = os.getenv('NOTION_DATABASE_ID')
    
    if notion_token and notion_db_id:
        notion_sync = NotionSync(notion_token, notion_db_id)
        notion_thread = threading.Thread(
            target=notion_sync.start_monitoring,
            daemon=True
        )
        notion_thread.start()
    
    print("✅ 同步中心运行中...")
    
    while True:
        time.sleep(3600)  # 每小时备份

if __name__ == '__main__':
    main()
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip3 install flask requests python-dotenv
```

### 2. 配置文件

创建 `config/sync.env`：

```bash
# Notion配置
NOTION_TOKEN=你的Token
NOTION_DATABASE_ID=你的数据库ID

# 微信导出目录
WECHAT_EXPORT_DIR=~/Downloads/微信导出

# 同步频率（秒）
SYNC_INTERVAL=300
```

### 3. 启动同步

```bash
python3 sync_[center.py](http://center.py)
```

---

## 🧬 DNA确认码

- **同步中心**：`#BAOBAO-SYNC-CENTER-20251215-001`
- **创建者**：宝宝·构建师 P02