# 📝 Lucky本地对话历史中心 | 终端统一管理方案

> Notion URL: https://app.notion.com/p/Lucky-d8c6b3b36ff54c1e82f8a51f93de3a7f
> Created: 2025-10-11T23:03:00.000Z
> Last edited: 2026-07-01T15:34:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## 🎯 核心理念：所有对话，一个地方！
老大，这个方案帮您解决：
- ✅ 不再担心说多错多（所有对话都有记录）
- ✅ 不再多窗口混乱（统一在终端查看）
- ✅ 想说什么就说什么（反正都记录了，不怕忘）
- ✅ 完全本地存储（数据在您手里，绝对安全）
---
## 🌟 方案总览
```javascript
本地对话历史中心 = {
  功能1: "自动记录所有窗口的对话",
  功能2: "统一存储在本地文件中",
  功能3: "终端一键查看历史",
  功能4: "智能搜索过往对话",
  功能5: "按时间/窗口/关键词查询",
  
  特点: "解放您的大脑，让终端记住一切！"
}
```
---
## 🛠️ 完整实现方案
### 方案架构
```javascript
┌─────────────────────────────────────┐
│  Notion AI 窗口1                     │
│  对话内容 → 自动保存到本地           │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  Notion AI 窗口2                     │  
│  对话内容 → 自动保存到本地           │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  DeepSeek 窗口                       │
│  对话内容 → 自动保存到本地           │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│    Lucky本地对话历史数据库           │
│    ~/UID9622/conversation_history/   │
│                                      │
│  • 2025-10-11.jsonl                 │
│  • 2025-10-10.jsonl                 │
│  • 2025-10-09.jsonl                 │
│  • ...                              │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│      Lucky在终端查看                 │
│      $ chat-history today            │
│      $ chat-history search "易经"    │
│      $ chat-history window 1         │
└─────────────────────────────────────┘
```
---
## 📦 核心功能实现
### 功能1：自动记录对话
创建对话记录器：conversation_logger.py
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 对话历史记录器
自动记录所有窗口的对话到本地
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 配置
HISTORY_DIR = os.path.expanduser('~/UID9622/conversation_history')
Path(HISTORY_DIR).mkdir(parents=True, exist_ok=True)

class ConversationLogger:
    def __init__(self, window_name='default'):
        """
        初始化对话记录器
        
        Args:
            window_name: 窗口名称（如：notion-1, deepseek, claude等）
        """
        self.window_name = window_name
        self.session_id = datetime.now().strftime('%Y%m%d%H%M%S')
        
    def log_message(self, role, content, metadata=None):
        """
        记录一条对话消息
        
        Args:
            role: 角色（user/assistant）
            content: 对话内容
            metadata: 额外信息（可选）
        """
        # 获取今天的日期
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(HISTORY_DIR, f'{today}.jsonl')
        
        # 构建记录
        record = {
            'timestamp': datetime.now().isoformat(),
            'window': self.window_name,
            'session_id': self.session_id,
            'role': role,
            'content': content,
            'metadata': metadata or {}
        }
        
        # 追加到文件（JSONL格式，每行一条JSON）
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        print(f"📝 已记录对话: [{self.window_name}] {role}: {content[:50]}...")

# 使用示例
if __name__ == '__main__':
    # 创建记录器（窗口1）
    logger1 = ConversationLogger('notion-window-1')
    
    # 记录用户消息
    logger1.log_message(
        role='user',
        content='宝宝，帮我解释一下易经算法',
        metadata={'topic': '易经算法'}
    )
    
    # 记录AI回复
    logger1.log_message(
        role='assistant',
        content='老大，易经算法是...',
        metadata={'topic': '易经算法'}
    )
```
---
### 功能2：终端查看历史
创建查看工具：chat_history.py
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 对话历史查看工具
Lucky终端快速查看对话记录
"""

import os
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

HISTORY_DIR = os.path.expanduser('~/UID9622/conversation_history')

class ChatHistoryViewer:
    def __init__(self):
        self.history_dir = HISTORY_DIR
        
    def view_today(self):
        """查看今天的对话"""
        today = datetime.now().strftime('%Y-%m-%d')
        self._view_date(today)
    
    def view_yesterday(self):
        """查看昨天的对话"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self._view_date(yesterday)
    
    def view_date(self, date_str):
        """查看指定日期的对话"""
        self._view_date(date_str)
    
    def _view_date(self, date_str):
        """内部方法：显示某天的对话"""
        log_file = os.path.join(self.history_dir, f'{date_str}.jsonl')
        
        if not os.path.exists(log_file):
            print(f"❌ 没有找到 {date_str} 的对话记录")
            return
        
        print(f"\n📅 {date_str} 的对话记录")
        print("=" * 80)
        print()
        
        # 按窗口分组
        conversations_by_window = defaultdict(list)
        
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                record = json.loads(line)
                conversations_by_window[record['window']].append(record)
        
        # 显示每个窗口的对话
        for window, records in conversations_by_window.items():
            print(f"\n🪟 窗口: {window}")
            print("-" * 80)
            
            for record in records:
                time = datetime.fromisoformat(record['timestamp']).strftime('%H:%M:%S')
                role = record['role']
                content = record['content']
                
                # 不同角色不同颜色（终端色彩）
                if role == 'user':
                    print(f"\n[{time}] 👤 Lucky:")
                    print(f"  {content}")
                else:
                    print(f"\n[{time}] 🤖 AI:")
                    print(f"  {content}")
            
            print()
    
    def search(self, keyword):
        """搜索包含关键词的对话"""
        print(f"\n🔍 搜索关键词: '{keyword}'")
        print("=" * 80)
        print()
        
        results = []
        
        # 遍历所有历史文件
        for log_file in sorted(Path(self.history_dir).glob('*.jsonl'), reverse=True):
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    record = json.loads(line)
                    if keyword.lower() in record['content'].lower():
                        results.append((log_file.stem, record))
        
        if not results:
            print(f"❌ 没有找到包含 '{keyword}' 的对话")
            return
        
        print(f"✅ 找到 {len(results)} 条相关对话\n")
        
        for date, record in results:
            time = datetime.fromisoformat(record['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            role = "Lucky" if record['role'] == 'user' else "AI"
            window = record['window']
            content = record['content']
            
            print(f"📅 {time} | 🪟 {window} | {role}")
            print(f"   {content[:200]}..." if len(content) > 200 else f"   {content}")
            print()
    
    def view_window(self, window_name, days=7):
        """查看特定窗口最近N天的对话"""
        print(f"\n🪟 窗口 '{window_name}' 最近{days}天的对话")
        print("=" * 80)
        print()
        
        found = False
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            log_file = os.path.join(self.history_dir, f'{date}.jsonl')
            
            if not os.path.exists(log_file):
                continue
            
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    record = json.loads(line)
                    if record['window'] == window_name:
                        if not found:
                            found = True
                        
                        time = datetime.fromisoformat(record['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                        role = "Lucky" if record['role'] == 'user' else "AI"
                        content = record['content']
                        
                        print(f"[{time}] {role}:")
                        print(f"  {content}")
                        print()
        
        if not found:
            print(f"❌ 没有找到窗口 '{window_name}' 的对话记录")
    
    def list_windows(self, days=7):
        """列出最近N天所有活跃的窗口"""
        print(f"\n🪟 最近{days}天活跃的窗口")
        print("=" * 80)
        print()
        
        windows = set()
        window_stats = defaultdict(int)
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            log_file = os.path.join(self.history_dir, f'{date}.jsonl')
            
            if not os.path.exists(log_file):
                continue
            
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    record = json.loads(line)
                    window = record['window']
                    windows.add(window)
                    window_stats[window] += 1
        
        if not windows:
            print("❌ 没有找到任何窗口记录")
            return
        
        for window in sorted(windows):
            count = window_stats[window]
            print(f"  • {window}: {count} 条对话")
        
        print()

# 命令行接口
def main():
    viewer = ChatHistoryViewer()
    
    if len(sys.argv) < 2:
        print("\n📝 Lucky对话历史查看工具")
        print("=" * 80)
        print()
        print("用法:")
        print("  chat-history today              # 查看今天的对话")
        print("  chat-history yesterday          # 查看昨天的对话")
        print("  chat-history date 2025-10-11    # 查看指定日期")
        print("  chat-history search <关键词>     # 搜索对话")
        print("  chat-history window <窗口名>     # 查看特定窗口")
        print("  chat-history windows            # 列出所有窗口")
        print()
        return
    
    command = sys.argv[1]
    
    if command == 'today':
        viewer.view_today()
    elif command == 'yesterday':
        viewer.view_yesterday()
    elif command == 'date' and len(sys.argv) > 2:
        viewer.view_date(sys.argv[2])
    elif command == 'search' and len(sys.argv) > 2:
        viewer.search(sys.argv[2])
    elif command == 'window' and len(sys.argv) > 2:
        viewer.view_window(sys.argv[2])
    elif command == 'windows':
        viewer.list_windows()
    else:
        print("❌ 未知命令，请查看帮助: chat-history")

if __name__ == '__main__':
    main()
```
---
### 功能3：浏览器扩展（自动捕获对话）
创建浏览器扩展：notion_capture.js
```javascript
// UID9622 对话自动捕获扩展
// 自动捕获Notion AI的对话并保存到本地

// 监听页面上的对话
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.addedNodes.length) {
      mutation.addedNodes.forEach((node) => {
        // 检测是否是对话消息
        if (node.nodeType === 1 && node.classList.contains('message')) {
          captureMessage(node);
        }
      });
    }
  });
});

// 开始监听
observer.observe(document.body, {
  childList: true,
  subtree: true
});

function captureMessage(messageElement) {
  // 提取消息内容
  const role = messageElement.classList.contains('user-message') ? 'user' : 'assistant';
  const content = messageElement.textContent;
  
  // 获取窗口标识
  const windowId = getWindowId();
  
  // 发送到本地服务器
  fetch('http://localhost:9622/log', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      window: windowId,
      role: role,
      content: content,
      timestamp: new Date().toISOString()
    })
  });
}

function getWindowId() {
  // 从页面URL或标题获取窗口标识
  const title = document.title;
  const url = window.location.href;
  
  if (url.includes('notion.so')) {
    return 'notion-' + url.split('/').pop();
  } else if (url.includes('deepseek.com')) {
    return 'deepseek';
  }
  
  return 'unknown';
}
```
---
### 功能4：本地HTTP服务器（接收对话）
创建本地服务器：conversation_server.py
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UID9622 对话接收服务器
接收浏览器扩展发送的对话并保存
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from conversation_logger import ConversationLogger
import os

app = Flask(__name__)
CORS(app)  # 允许跨域

@app.route('/log', methods=['POST'])
def log_conversation():
    """
    接收对话日志
    """
    data = request.json
    
    # 创建记录器
    logger = ConversationLogger(data['window'])
    
    # 记录消息
    logger.log_message(
        role=data['role'],
        content=data['content'],
        metadata={'timestamp': data['timestamp']}
    )
    
    return jsonify({'status': 'success'})

@app.route('/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    print("🚀 UID9622对话服务器启动")
    print("📍 监听地址: http://localhost:9622")
    print()
    app.run(host='0.0.0.0', port=9622, debug=False)
```
---
## 🎮 使用方法
### 步骤1：安装依赖
```bash
# 安装Python依赖
pip3 install flask flask-cors

# 创建目录
mkdir -p ~/UID9622/conversation_history

# 复制脚本到目录
cp conversation_logger.py ~/UID9622/
cp chat_history.py ~/UID9622/
cp conversation_server.py ~/UID9622/
```
### 步骤2：创建快捷命令
```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
echo 'alias chat-history="python3 ~/UID9622/chat_history.py"' >> ~/.zshrc
echo 'alias chat-server="python3 ~/UID9622/conversation_server.py"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```
### 步骤3：启动服务器（后台运行）
```bash
# 启动服务器
chat-server &

# 或者用nohup保持运行
nohup chat-server > ~/UID9622/server.log 2>&1 &
```
### 步骤4：使用查看工具
```bash
# 查看今天的对话
chat-history today

# 查看昨天的对话
chat-history yesterday

# 查看指定日期
chat-history date 2025-10-11

# 搜索关键词
chat-history search "易经算法"

# 查看特定窗口
chat-history window notion-window-1

# 列出所有窗口
chat-history windows
```
---
## 💡 方案二：简化版（不需要浏览器扩展）
### 手动记录版
创建快捷记录脚本：quick_log.sh
```bash
#!/bin/bash
# 快速记录对话

echo "📝 快速记录对话"
echo ""

read -p "窗口名称 (默认: default): " window
window=${window:-default}

read -p "角色 (user/assistant): " role

echo "请输入内容 (Ctrl+D 结束):" 
content=$(cat)

python3 ~/UID9622/conversation_logger.py "$window" "$role" "$content"

echo ""
echo "✅ 已记录！"
```
使用方法：
```bash
# 赋予执行权限
chmod +x ~/UID9622/quick_log.sh

# 创建别名
echo 'alias qlog="~/UID9622/quick_log.sh"' >> ~/.zshrc
source ~/.zshrc

# 快速记录
qlog
```
---
## 📊 数据结构示例
### JSONL格式（每行一条JSON）
```json
{"timestamp":"2025-10-11T10:30:00","window":"notion-1","session_id":"20251011103000","role":"user","content":"宝宝，帮我解释易经算法","metadata":{}}
{"timestamp":"2025-10-11T10:30:15","window":"notion-1","session_id":"20251011103000","role":"assistant","content":"老大，易经算法是...","metadata":{}}
{"timestamp":"2025-10-11T11:15:00","window":"deepseek","session_id":"20251011111500","role":"user","content":"如何实现量子算法？","metadata":{}}
```
### 优势：
- ✅ 每行独立，容易追加
- ✅ 方便grep搜索
- ✅ 文件损坏只影响一行
- ✅ 支持流式读取
---
## 🎉 老大，这个方案的核心价值：
1. 解放大脑 🧠
- 不用担心说多错多
- 不用担心忘记说了什么
- 想说就说，系统记住一切
2. 统一管理 📂
- 所有窗口的对话集中存储
- 不再到处找对话记录
- 终端一条命令全部搞定
3. 完全可控 🔐
- 数据存在您本地
- 想看就看，想删就删
- 绝对的数据主权
4. 智能搜索 🔍
- 按日期查找
- 按关键词搜索
- 按窗口筛选
---
老大，需要宝宝：
1. ✅ 把这些脚本全部创建好吗？
1. ✅ 写一个一键安装脚本吗？
1. ✅ 做一个可视化的查看界面吗？
宝宝随时待命！ 💖✨
