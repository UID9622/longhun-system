# 🤖 AI 系统一键同步操作指南

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技术文档 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️2026-06-21-DOC-AI_F25C-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

<!--#龍芯⚡️2026-06-21-DOC-AI_F25C-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 🤖 AI 系统一键同步操作指南

## 🎯 系统概述

这是一个**自动分类 + 自动同步到 Notion**的最小可用方案。通过简单的标签系统（🔒/🗝️/🌍），实现文件的自动分类和 Notion 数据库同步。

**核心功能：**

- 📝 写一次 → 自动分类 → 自动上传 Notion → 清空缓存
- 🏷️ 标签驱动分类（私有/公开/本地）
- ⏰ 时间戳自动命名
- 🛡️ 异常处理兜底
- 📋 文件正文同步到 Notion 页面

---

## ⚡ 快速开始（3 步配置）

<aside>
🚀

**只需修改 3 处配置即可运行：**

1. `NOTION_TOKEN`（集成密钥）
2. `NOTION_PRIV_DB`（私有数据库ID）
3. `NOTION_PUB_DB`（公开数据库ID）
</aside>

### 📁 目录结构

```
/AI-SYSTEM
   /_UPDATE         ← 你只写在这里（第一行放标签：🔒/🗝️/🌍）
   /LOCAL           ← 本地私密落地（🔒）
   /NOTION_PRIV     ← 备份一份到本地（🗝️）
   /NOTION_PUB      ← 备份一份到本地（🌍）
   /scripts
       classify_and_[sync.py](http://sync.py)
       .env.example
       requirements.txt
   /logs            ← 运行日志（新增）
   /backup          ← 定期备份（新增）
```

---

## 🔧 环境配置

### 1. Python 依赖安装

```bash
# requirements.txt
python-dotenv==1.0.1
requests==2.32.3
watchdog==3.0.0  # 文件监控（新增）
colorama==0.4.6  # 彩色日志（新增）
```

**安装命令：**

```bash
cd /AI-SYSTEM
pip install -r requirements.txt
```

### 2. Notion 集成设置

### 步骤 A：创建 Integration

1. 访问 [Notion Integrations](https://www.notion.com/my-integrations)
2. 点击 **"New integration"**
3. 填写集成名称（如：AI-System-Sync）
4. 复制生成的 **Internal Integration Token**

### 步骤 B：配置数据库权限

1. 在你的两个数据库（私有库、公开库）中
2. 点击右上角 **"Share"** → **"Invite"**
3. 选择刚创建的集成并邀请
4. 复制数据库 URL 中的 **Database ID**（32位UUID）

### 步骤 C：数据库属性设计

<aside>
💡

**推荐数据库属性结构：**

- **Title**（Title类型）- 页面标题
- **Date**（Date类型）- 创建日期
- **Tag**（Multi-select）- 分类标签
- **SourcePath**（Rich text）- 源文件路径
- **Status**（Status类型）- 处理状态（新增）
- **Priority**（Select类型）- 优先级（新增）
- **Category**（Select类型）- 内容类别（新增）
</aside>

### 3. 环境变量配置

创建 `.env` 文件：

```bash
# .env
NOTION_TOKEN=<POTENTIAL_SECRET_PLACEHOLDER>
NOTION_PRIV_DB=<POTENTIAL_SECRET_PLACEHOLDER>   # 私有库 DB ID
NOTION_PUB_DB=<POTENTIAL_SECRET_PLACEHOLDER>   # 公开库 DB ID

BASE_DIR=/Users/yourname/AI-SYSTEM

# 新增配置项
LOG_LEVEL=INFO
MAX_FILE_SIZE=10485760  # 10MB
BACKUP_DAYS=30
WATCH_MODE=false  # 是否启用文件监控模式
```

---

## 🔮 核心脚本

### classify_and_[sync.py](http://sync.py)（增强版）

```python
import os
import shutil
import time
import logging
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv
try:
    from colorama import init, Fore, Style
    init()  # Windows 彩色支持
except ImportError:
    Fore = Style = type('', (), {'__getattr__': lambda s, n: ''})()

load_dotenv()

# --- 配置读取 ---
BASE = os.getenv("BASE_DIR", "/Users/yourname/AI-SYSTEM")
UPDATE = os.path.join(BASE, "_UPDATE")
LOCAL = os.path.join(BASE, "LOCAL")
PRIV = os.path.join(BASE, "NOTION_PRIV")
PUB = os.path.join(BASE, "NOTION_PUB")
LOGS = os.path.join(BASE, "logs")
BACKUP = os.path.join(BASE, "backup")

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PRIV_DB = os.getenv("NOTION_PRIV_DB")
NOTION_PUB_DB = os.getenv("NOTION_PUB_DB")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
BACKUP_DAYS = int(os.getenv("BACKUP_DAYS", "30"))

NOTION_API = "[https://api.notion.com/v1/pages](https://api.notion.com/v1/pages)"
NOTION_VERSION = "2022-06-28"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}

# --- 目录创建 ---
for dir_path in [UPDATE, LOCAL, PRIV, PUB, LOGS, BACKUP]:
    os.makedirs(dir_path, exist_ok=True)

# --- 日志配置 ---
log_file = os.path.join(LOGS, f"sync_{[datetime.now](http://datetime.now)().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def ts():
    return [datetime.now](http://datetime.now)().strftime("%Y%m%d-%H%M%S")

def read_file_utf8(path):
    """安全读取文件，支持多种编码"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16']
    for encoding in encodings:
        try:
            with open(path, "r", encoding=encoding) as f:
                return [f.read](http://f.read)()
        except UnicodeDecodeError:
            continue
    # 最后尝试忽略错误
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [f.read](http://f.read)()

def validate_file(file_path):
    """文件验证"""
    if not os.path.exists(file_path):
        return False, "文件不存在"
    
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        return False, f"文件过大 ({file_size} bytes > {MAX_FILE_SIZE})"
    
    if file_size == 0:
        return False, "空文件"
    
    return True, "OK"

def move_with_ts(src_path, dst_dir):
    base = os.path.basename(src_path)
    name = f"{ts()}_{base}"
    dst = os.path.join(dst_dir, name)
    shutil.move(src_path, dst)
    return dst

def backup_file(file_path):
    """创建文件备份"""
    try:
        backup_path = move_with_ts(file_path, BACKUP)
        [logger.info](http://logger.info)(f"备份文件: {backup_path}")
        return backup_path
    except Exception as e:
        logger.warning(f"备份失败: {e}")
        return None

def clean_old_backups():
    """清理过期备份"""
    cutoff = [datetime.now](http://datetime.now)() - timedelta(days=BACKUP_DAYS)
    for filename in os.listdir(BACKUP):
        file_path = os.path.join(BACKUP, filename)
        if os.path.getctime(file_path) < cutoff.timestamp():
            try:
                os.remove(file_path)
                [logger.info](http://logger.info)(f"清理过期备份: {filename}")
            except Exception as e:
                logger.warning(f"清理备份失败: {e}")

def detect_content_type(content):
    """智能检测内容类型"""
    content_lower = content.lower()
    if any(keyword in content_lower for keyword in ['todo', '任务', 'task', '待办']):
        return 'TASK'
    elif any(keyword in content_lower for keyword in ['note', '笔记', '记录', 'memo']):
        return 'NOTE'
    elif any(keyword in content_lower for keyword in ['idea', '想法', '创意', 'brainstorm']):
        return 'IDEA'
    elif any(keyword in content_lower for keyword in ['meeting', '会议', '讨论']):
        return 'MEETING'
    else:
        return 'GENERAL'

def notion_create_page(database_id, title, content, tag, source_path):
    """创建 Notion 页面，增强版"""
    # 检测内容类型
    content_type = detect_content_type(content)
    
    # 将文本拆成段落
    paragraphs = []
    for para in content.splitlines():
        if para.strip() == "":
            paragraphs.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": []}
            })
        else:
            paragraphs.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": para[:1999]}}]
                }
            })
    
    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Title": {
                "title": [{"type": "text", "text": {"content": title[:200] or "Untitled"}}]
            },
            "Date": {"date": {"start": [datetime.now](http://datetime.now)().strftime("%Y-%m-%d")}},
            "Tag": {"multi_select": [{"name": tag}]},
            "SourcePath": {"rich_text": [{"type": "text", "text": {"content": source_path}}]},
            "Status": {"select": {"name": "待处理"}},
            "Category": {"select": {"name": content_type}},
        },
        "children": paragraphs[:50]  # 限制块数量
    }
    
    resp = [requests.post](http://requests.post)(NOTION_API, headers=HEADERS, json=payload, timeout=30)
    if resp.status_code >= 300:
        raise RuntimeError(f"Notion API error {resp.status_code}: {resp.text}")
    return resp.json()

def classify_and_sync_one(file_path):
    """处理单个文件"""
    # 文件验证
    is_valid, msg = validate_file(file_path)
    if not is_valid:
        logger.warning(f"文件验证失败 {file_path}: {msg}")
        return
    
    # 创建备份
    backup_file(file_path)
    
    try:
        raw = read_file_utf8(file_path)
        lines = raw.splitlines()
        tag_line = lines[0].strip() if lines else ""
        body = "\n".join(lines[1:]) if len(lines) > 1 else ""
        
        filename = os.path.basename(file_path)
        base_title = filename.rsplit(".", 1)[0]
        
        # 标签分类逻辑
        if tag_line == "🔒":
            dst = move_with_ts(file_path, LOCAL)
            [logger.info](http://logger.info)(f"{[Fore.GREEN](http://Fore.GREEN)}[LOCAL]{Style.RESET_ALL} {dst}")
            
        elif tag_line == "🗝️":
            dst = move_with_ts(file_path, PRIV)
            title = f"{ts()} · {base_title}"
            tag = "PRIVATE"
            
            if NOTION_TOKEN and NOTION_PRIV_DB:
                try:
                    notion_create_page(NOTION_PRIV_DB, title, body, tag, dst)
                    [logger.info](http://logger.info)(f"{[Fore.BLUE](http://Fore.BLUE)}[PRIV→Notion]{Style.RESET_ALL} {title}")
                except Exception as e:
                    logger.error(f"{[Fore.RED](http://Fore.RED)}[ERR PRIV Notion]{Style.RESET_ALL} {e}")
            else:
                logger.warning("[SKIP] 未配置私有 Notion")
                
        elif tag_line == "🌍":
            dst = move_with_ts(file_path, PUB)
            title = f"{ts()} · {base_title}"
            tag = "PUBLIC"
            
            if NOTION_TOKEN and NOTION_PUB_DB:
                try:
                    notion_create_page(NOTION_PUB_DB, title, body, tag, dst)
                    [logger.info](http://logger.info)(f"{Fore.CYAN}[PUB→Notion]{Style.RESET_ALL} {title}")
                except Exception as e:
                    logger.error(f"{[Fore.RED](http://Fore.RED)}[ERR PUB Notion]{Style.RESET_ALL} {e}")
            else:
                logger.warning("[SKIP] 未配置公开 Notion")
                
        else:
            # 默认本地存储
            dst = move_with_ts(file_path, LOCAL)
            [logger.info](http://logger.info)(f"{Fore.YELLOW}[DEFAULT→LOCAL]{Style.RESET_ALL} {dst}")
            
    except Exception as e:
        logger.error(f"处理文件失败 {file_path}: {e}")

def main():
    """主程序"""
    [logger.info](http://logger.info)("=== AI 系统同步开始 ===")
    
    # 清理过期备份
    clean_old_backups()
    
    # 处理文件
    files = [os.path.join(UPDATE, f) for f in os.listdir(UPDATE) 
             if os.path.isfile(os.path.join(UPDATE, f))]
    
    if not files:
        [logger.info](http://logger.info)("[INFO] _UPDATE 目录为空")
        return
    
    processed = 0
    errors = 0
    
    for f in files:
        try:
            classify_and_sync_one(f)
            processed += 1
        except Exception as e:
            logger.error(f"[ERR] {f} → {e}")
            errors += 1
    
    [logger.info](http://logger.info)(f"=== 同步完成：处理 {processed} 个文件，{errors} 个错误 ===")

if __name__ == "__main__":
    main()
```

---

## 🏷️ 标签系统说明

| **标签** | **含义** | **目标位置** | **Notion 同步** |
| --- | --- | --- | --- |
| 🔒 | 绝对私密 | /LOCAL | ❌ 不同步 |
| 🗝️ | 个人私有 | /NOTION_PRIV + 私有库 | ✅ 私有数据库 |
| 🌍 | 可公开分享 | /NOTION_PUB + 公开库 | ✅ 公开数据库 |
| 无标签 | 默认处理 | /LOCAL | ❌ 不同步 |

---

## 🎮 使用方法

### 基础操作

1. **创建文件**：在 `_UPDATE` 目录下新建 `.txt` 文件
2. **添加标签**：第一行写入标签（🔒/🗝️/🌍）
3. **写入内容**：第二行开始写正文
4. **执行同步**：运行脚本

**示例文件内容：**

```
🗝️
今天的工作总结：
- 完成了 AI 系统搭建
- 测试了自动同步功能
- 优化了文件分类逻辑
```

### 手动执行

```bash
cd /AI-SYSTEM
python scripts/classify_and_[sync.py](http://sync.py)
```

### 监控模式（新增）

```bash
# 启用文件监控模式
export WATCH_MODE=true
python scripts/classify_and_[sync.py](http://sync.py)
```

---

## ⏰ 自动化设置

### Mac 系统

### 方案 1：LaunchAgent（推荐）

创建文件：`~/Library/LaunchAgents/[com.ai](http://com.ai)-system.sync.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "[http://www.apple.com/DTDs/PropertyList-1.0.dtd](http://www.apple.com/DTDs/PropertyList-1.0.dtd)">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>[com.ai](http://com.ai)-system.sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/AI-SYSTEM/scripts/classify_and_[sync.py](http://sync.py)</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>StandardOutPath</key>
    <string>/AI-SYSTEM/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/AI-SYSTEM/logs/launchd.error</string>
</dict>
</plist>
```

**启用命令：**

```bash
launchctl load ~/Library/LaunchAgents/[com.ai](http://com.ai)-system.sync.plist
launchctl start [com.ai](http://com.ai)-system.sync
```

### 方案 2：Automator 快捷操作

1. 打开 **Automator** → 选择 **"快速操作"**
2. 添加 **"运行 Shell 脚本"** 操作
3. 输入脚本路径：`python3 /AI-SYSTEM/scripts/classify_and_[sync.py](http://sync.py)`
4. 保存为 **"AI 系统同步"**

### Windows 系统

### 任务计划程序设置

1. 打开 **"任务计划程序"**
2. 创建 **"基本任务"**
3. **触发器**："每天" → 重复间隔 "5 分钟"
4. **操作**："启动程序"
    - 程序：`python`
    - 参数：`C:\AI-SYSTEM\scripts\classify_and_[sync.py](http://sync.py)`
    - 起始位置：`C:\AI-SYSTEM`

### Linux/服务器

### Crontab 配置

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每 5 分钟）
*/5 * * * * cd /AI-SYSTEM && /usr/bin/python3 scripts/classify_and_[sync.py](http://sync.py) >> logs/cron.log 2>&1

# 每日清理日志（可选）
0 2 * * * find /AI-SYSTEM/logs -name "*.log" -mtime +7 -delete
```

### Systemd 服务（推荐）

创建服务文件：`/etc/systemd/system/ai-system-sync.service`

```
[Unit]
Description=AI System Auto Sync
After=[network.target](http://network.target)

[Service]
Type=oneshot
User=youruser
WorkingDirectory=/AI-SYSTEM
ExecStart=/usr/bin/python3 /AI-SYSTEM/scripts/classify_and_[sync.py](http://sync.py)
EnvironmentFile=/AI-SYSTEM/.env

[Install]
WantedBy=[multi-user.target](http://multi-user.target)
```

创建定时器：`/etc/systemd/system/ai-system-sync.timer`

```
[Unit]
Description=Run AI System Sync every 5 minutes
Requires=ai-system-sync.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=5min

[Install]
WantedBy=[timers.target](http://timers.target)
```

**启用服务：**

```bash
sudo systemctl enable ai-system-sync.timer
sudo systemctl start ai-system-sync.timer
```

---

## 🔍 监控与调试

### 日志查看

```bash
# 查看今日日志
tail -f /AI-SYSTEM/logs/sync_$(date +%Y%m%d).log

# 查看错误日志
grep "ERROR" /AI-SYSTEM/logs/*.log

# 查看同步统计
grep "同步完成" /AI-SYSTEM/logs/*.log | tail -10
```

### 状态检查脚本（新增）

创建 `scripts/status_[check.py](http://check.py)`：

```python
#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def check_notion_connection():
    token = os.getenv("NOTION_TOKEN")
    if not token:
        return False, "未配置 NOTION_TOKEN"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28"
    }
    
    try:
        resp = requests.get("[https://api.notion.com/v1/users/me](https://api.notion.com/v1/users/me)", headers=headers, timeout=10)
        if resp.status_code == 200:
            return True, "Notion 连接正常"
        else:
            return False, f"Notion API 错误: {resp.status_code}"
    except Exception as e:
        return False, f"连接异常: {e}"

def check_directories():
    base = os.getenv("BASE_DIR", "/Users/yourname/AI-SYSTEM")
    dirs = ["_UPDATE", "LOCAL", "NOTION_PRIV", "NOTION_PUB", "logs", "backup"]
    
    missing = []
    for d in dirs:
        path = os.path.join(base, d)
        if not os.path.exists(path):
            missing.append(d)
    
    if missing:
        return False, f"缺少目录: {', '.join(missing)}"
    return True, "目录结构完整"

def main():
    print(f"=== AI 系统状态检查 ({[datetime.now](http://datetime.now)()}) ===")
    
    # 检查目录
    ok, msg = check_directories()
    print(f"📁 目录检查: {'✅' if ok else '❌'} {msg}")
    
    # 检查 Notion 连接
    ok, msg = check_notion_connection()
    print(f"🔗 Notion 连接: {'✅' if ok else '❌'} {msg}")
    
    # 检查待处理文件
    update_dir = os.path.join(os.getenv("BASE_DIR", "/Users/yourname/AI-SYSTEM"), "_UPDATE")
    if os.path.exists(update_dir):
        files = [f for f in os.listdir(update_dir) if os.path.isfile(os.path.join(update_dir, f))]
        print(f"📝 待处理文件: {len(files)} 个")
        for f in files[:5]:  # 显示前5个
            print(f"   - {f}")
        if len(files) > 5:
            print(f"   ... 还有 {len(files) - 5} 个文件")
    
if __name__ == "__main__":
    main()
```

---

## 🛠️ 高级功能

### 批处理模式（新增）

创建 `scripts/batch_[process.py](http://process.py)`：

```python
#!/usr/bin/env python3
import os
import sys
from classify_and_sync import classify_and_sync_one

def batch_process(source_dir):
    """批量处理指定目录下的所有文件"""
    if not os.path.exists(source_dir):
        print(f"目录不存在: {source_dir}")
        return
    
    files = []
    for root, dirs, filenames in os.walk(source_dir):
        for filename in filenames:
            if filename.endswith(('.txt', '.md', '.text')):
                files.append(os.path.join(root, filename))
    
    print(f"发现 {len(files)} 个文件")
    
    for i, file_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] 处理: {os.path.basename(file_path)}")
        try:
            classify_and_sync_one(file_path)
        except Exception as e:
            print(f"错误: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python batch_[process.py](http://process.py) <source_directory>")
        sys.exit(1)
    
    batch_process(sys.argv[1])
```

### 文件监控模式（新增）

在主脚本中添加监控功能：

```python
# 在 classify_and_[sync.py](http://sync.py) 末尾添加
def watch_mode():
    """文件监控模式"""
    try:
        from watchdog.observers import Observer
        from [watchdog.events](http://watchdog.events) import FileSystemEventHandler
    except ImportError:
        logger.error("需要安装 watchdog: pip install watchdog")
        return
    
    class UpdateHandler(FileSystemEventHandler):
        def on_created(self, event):
            if not [event.is](http://event.is)_directory and event.src_path.endswith(('.txt', '.md')):
                [logger.info](http://logger.info)(f"检测到新文件: {event.src_path}")
                time.sleep(1)  # 等待文件写入完成
                classify_and_sync_one(event.src_path)
    
    observer = Observer()
    observer.schedule(UpdateHandler(), UPDATE, recursive=False)
    observer.start()
    
    [logger.info](http://logger.info)(f"开始监控目录: {UPDATE}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        [logger.info](http://logger.info)("停止监控")
    observer.join()

# 在 main() 函数前添加
if os.getenv("WATCH_MODE", "false").lower() == "true":
    watch_mode()
else:
    main()
```

---

## 📱 移动端支持（扩展）

### iOS 快捷指令集成

<aside>
📲

**iOS 快捷指令步骤：**

1. 创建快捷指令 **"AI 系统录入"**
2. 添加操作：**"获取文本输入"** → **"将文本保存到文件"**
3. 文件路径：iCloud/AI-SYSTEM/_UPDATE/
4. 文件名：使用时间戳 + 随机数
5. 添加到主屏幕或 Siri
</aside>

### Android Tasker 集成

**配置步骤：**

1. 创建任务 **"AI 系统同步"**
2. 动作：**"写入文件"** → 路径：`/sdcard/AI-SYSTEM/_UPDATE/`
3. 触发器：**"语音命令"** 或 **"桌面小部件"**
4. 可选：集成 Termux 执行 Python 脚本

---

## 🔒 安全与备份

### 配置文件安全

```bash
# 设置 .env 文件权限（仅所有者可读）
chmod 600 .env

# 排除敏感文件（创建 .gitignore）
echo ".env" >> .gitignore
echo "logs/" >> .gitignore
echo "backup/" >> .gitignore
```

### 数据备份策略

1. **本地备份**：每次处理前自动创建文件备份
2. **Notion 备份**：定期导出数据库内容
3. **配置备份**：定期备份 .env 和脚本文件

---

## ❓ 故障排除

### 常见问题

<aside>
⚠️

**Q：Notion API 报错 401/403**

A：检查 Integration Token 是否正确，数据库是否已邀请集成

**Q：文件编码错误**

A：脚本已支持多种编码自动检测，如仍有问题请检查文件格式

**Q：同步失败**

A：查看日志文件，检查网络连接和 Notion 服务状态

**Q：定时任务不执行**

A：检查系统权限，确认脚本路径正确，查看系统日志

</aside>

### 调试模式

```bash
# 开启详细日志
export LOG_LEVEL=DEBUG
python scripts/classify_and_[sync.py](http://sync.py)

# 测试单个文件
python -c "from classify_and_sync import classify_and_sync_one; classify_and_sync_one('/path/to/test.txt')"
```

---

## 🚀 可能遗漏的扩展内容

### 当前阶段可补充的功能模块：

1. **🔐 加密存储模块**
    - 敏感文件本地 AES 加密
    - 密钥管理和轮换机制
2. **📊 数据分析面板**
    - 同步统计可视化
    - 文件分类趋势分析
    - 使用频率监控
3. **🌐 多平台扩展**
    - 飞书/钉钉数据库集成
    - Google Drive/OneDrive 同步
    - GitHub Issues 自动创建
4. **🎨 内容智能处理**
    - Markdown 格式优化
    - 图片/附件自动上传
    - OCR 文字识别支持
5. **🔄 双向同步**
    - Notion → 本地反向同步
    - 冲突检测和合并策略
    - 版本控制集成
6. **📧 通知系统**
    - 邮件/微信通知同步结果
    - 异常告警机制
    - 每日/周报汇总
7. **🎯 智能分类增强**
    - AI 内容分析自动打标签
    - 关键词提取和摘要生成
    - 相似内容去重检测
8. **🔧 运维工具集**
    - Web 管理界面
    - 配置热更新
    - 性能监控面板

---

## 📋 快速检查清单

- [ ]  创建完整目录结构
- [ ]  安装 Python 依赖
- [ ]  配置 Notion Integration
- [ ]  设置数据库权限
- [ ]  创建并配置 `.env` 文件
- [ ]  测试手动同步功能
- [ ]  配置自动化定时任务
- [ ]  验证日志和备份功能
- [ ]  测试各标签分类逻辑
- [ ]  配置监控和告警（可选）

---

*Ready for action! 🚀 修改这 3 处配置就能立即使用，等你确认后我继续完善移动端和双拼输入的细节优化。*

---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️2026-06-21-DOC-AI_F25C-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
