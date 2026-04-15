#!/bin/bash
# 龍魂AI统一调度中枢 + Siri API 部署脚本
# 在服务器上执行

echo "═══════════════════════════════════════════════════════════════"
echo "🐉 龍魂AI统一调度中枢 + Siri API 部署"
echo "   UID9622 专用"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# 检查目录
if [ ! -d "/root/cnsh" ]; then
    echo "❌ /root/cnsh 目录不存在！"
    exit 1
fi

cd /root/cnsh

echo "📦 步骤1/4: 创建调度中枢..."

# 创建调度中枢文件
cat > /root/cnsh/dragon_soul_commander.py << 'PYEOF'
#!/usr/bin/env python3
"""龍魂AI统一调度中枢 - UID9622专用"""

import json
import time
import random
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

class AIPriority(Enum):
    CHINA_FIRST = "china_first"
    BALANCED = "balanced"
    PERFORMANCE = "performance"
    COST = "cost"

class TaskType(Enum):
    CREATIVE = "creative"
    CODE = "code"
    ANALYSIS = "analysis"
    CHAT = "chat"
    IMAGE = "image"
    VOICE = "voice"
    RESEARCH = "research"
    URGENT = "urgent"

@dataclass
class AIWorker:
    name: str
    endpoint: str
    is_domestic: bool
    capabilities: List[TaskType]
    cost_per_token: float
    speed_score: float
    quality_score: float
    reliability: float
    daily_quota: int
    used_quota: int = 0
    is_online: bool = True
    
    def available(self) -> bool:
        return self.is_online and self.used_quota < self.daily_quota
    
    def score_for_task(self, task_type: TaskType, priority: AIPriority) -> float:
        if task_type not in self.capabilities:
            return 0
        base_score = self.quality_score * 0.4 + self.speed_score * 0.3 + self.reliability * 0.3
        if priority == AIPriority.CHINA_FIRST and self.is_domestic:
            base_score *= 1.5
        if priority == AIPriority.COST:
            base_score /= (self.cost_per_token + 0.001)
        return base_score

@dataclass
class Task:
    id: str
    type: TaskType
    content: str
    priority: AIPriority
    user_dna: str
    created_at: float = field(default_factory=time.time)
    assigned_to: Optional[str] = None
    status: str = "pending"
    result: Optional[str] = None

class DragonSoulCommander:
    VERSION = "3.0.0"
    CODENAME = "龍魂指挥官"
    MOTTO = "中国优先，自主可控"
    
    def __init__(self):
        self.workers: Dict[str, AIWorker] = {}
        self.task_queue: List[Task] = []
        self.task_history: Dict[str, Task] = {}
        self.default_priority = AIPriority.CHINA_FIRST
        self.is_running = False
        self._init_workers()
    
    def _init_workers(self):
        # 国产AI优先
        self.workers["kimi"] = AIWorker(
            name="Kimi", endpoint="http://localhost:9622/kimi",
            is_domestic=True,
            capabilities=[TaskType.CREATIVE, TaskType.CODE, TaskType.ANALYSIS, TaskType.CHAT, TaskType.RESEARCH, TaskType.URGENT],
            cost_per_token=0.001, speed_score=0.9, quality_score=0.9, reliability=0.95, daily_quota=10000
        )
        self.workers["wenxin"] = AIWorker(
            name="文心一言", endpoint="https://wenxin.baidu.com/api",
            is_domestic=True,
            capabilities=[TaskType.CREATIVE, TaskType.CHAT, TaskType.ANALYSIS],
            cost_per_token=0.002, speed_score=0.85, quality_score=0.85, reliability=0.9, daily_quota=5000
        )
        self.workers["tongyi"] = AIWorker(
            name="通义千问", endpoint="https://tongyi.aliyun.com/api",
            is_domestic=True,
            capabilities=[TaskType.CODE, TaskType.ANALYSIS, TaskType.RESEARCH],
            cost_per_token=0.002, speed_score=0.88, quality_score=0.87, reliability=0.92, daily_quota=5000
        )
        # 国外AI备选
        self.workers["claude"] = AIWorker(
            name="Claude", endpoint="https://api.anthropic.com/v1/messages",
            is_domestic=False,
            capabilities=[TaskType.CREATIVE, TaskType.CODE, TaskType.ANALYSIS, TaskType.RESEARCH, TaskType.URGENT],
            cost_per_token=0.008, speed_score=0.85, quality_score=0.95, reliability=0.9, daily_quota=2000
        )
        self.workers["gpt"] = AIWorker(
            name="GPT-4", endpoint="https://api.openai.com/v1/chat/completions",
            is_domestic=False,
            capabilities=[TaskType.CODE, TaskType.ANALYSIS, TaskType.RESEARCH],
            cost_per_token=0.01, speed_score=0.8, quality_score=0.95, reliability=0.85, daily_quota=1000
        )
    
    def submit_task(self, content: str, task_type: TaskType = TaskType.CHAT,
                   priority: AIPriority = None, user_dna: str = "UID9622", **kwargs) -> str:
        task_id = f"TASK-{int(time.time())}-{random.randint(1000, 9999)}"
        task = Task(
            id=task_id, type=task_type, content=content,
            priority=priority or self.default_priority, user_dna=user_dna
        )
        self.task_queue.append(task)
        self.task_history[task_id] = task
        self._schedule_task(task)
        return task_id
    
    def _schedule_task(self, task: Task):
        available_workers = [w for w in self.workers.values() if w.available() and task.type in w.capabilities]
        if not available_workers:
            task.status = "failed"
            task.result = "无可用AI节点"
            return
        scored_workers = [(w, w.score_for_task(task.type, task.priority)) for w in available_workers]
        scored_workers.sort(key=lambda x: x[1], reverse=True)
        best_worker = scored_workers[0][0]
        task.assigned_to = best_worker.name
        task.status = "running"
        best_worker.used_quota += 1
        # 模拟执行
        task.result = f"[{best_worker.name}] 已处理: {task.content[:30]}..."
        task.status = "completed"
    
    def query_task(self, task_id: str) -> Dict:
        task = self.task_history.get(task_id)
        if not task:
            return {"error": "任务不存在"}
        return {
            "id": task.id, "type": task.type.value, "status": task.status,
            "assigned_to": task.assigned_to, "result": task.result,
            "created_at": task.created_at
        }
    
    def get_worker_status(self) -> Dict:
        return {
            "total": len(self.workers),
            "online": sum(1 for w in self.workers.values() if w.is_online),
            "domestic": sum(1 for w in self.workers.values() if w.is_domestic),
            "workers": {name: {"name": w.name, "online": w.is_online, "available": w.available(),
                              "quota": f"{w.used_quota}/{w.daily_quota}", "domestic": w.is_domestic}
                       for name, w in self.workers.items()}
        }
    
    def get_stats(self) -> Dict:
        total = len(self.task_history)
        completed = sum(1 for t in self.task_history.values() if t.status == "completed")
        return {"total_tasks": total, "completed": completed, "pending": len(self.task_queue)}
    
    def start(self):
        self.is_running = True
        print(f"龍魂AI调度中枢 v{self.VERSION} 已启动")

# 全局实例
commander = DragonSoulCommander()
commander.start()
PYEOF

echo "✅ 调度中枢创建完成"
echo ""

echo "📦 步骤2/4: 创建Siri API..."

cat > /root/cnsh/siri_api.py << 'PYEOF2'
#!/usr/bin/env python3
"""Siri API服务器"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import sys
sys.path.insert(0, '/root/cnsh')
from dragon_soul_commander import commander, TaskType, AIPriority

class SiriHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {args[0]}")
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self._send_json({
                "system": "龍魂AI统一调度中枢",
                "version": commander.VERSION,
                "endpoints": ["/siri/command", "/task/{id}", "/workers", "/stats"]
            })
        elif self.path == '/workers':
            self._send_json(commander.get_worker_status())
        elif self.path == '/stats':
            self._send_json(commander.get_stats())
        elif self.path.startswith('/task/'):
            self._send_json(commander.query_task(self.path.split('/')[-1]))
        else:
            self._send_json({"error": "未知路径"}, 404)
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            body = json.loads(post_data.decode())
        except:
            self._send_json({"error": "无效的JSON"}, 400)
            return
        
        if self.path == '/siri/command':
            text = body.get('text', '').strip()
            user_dna = body.get('user_dna', 'UID9622')
            if not text:
                self._send_json({"error": "文本不能为空"}, 400)
                return
            
            # 识别任务类型
            task_type = TaskType.CHAT
            text_lower = text.lower()
            if any(kw in text_lower for kw in ["写代码", "编程", "code", "python"]):
                task_type = TaskType.CODE
            elif any(kw in text_lower for kw in ["分析", "数据", "统计"]):
                task_type = TaskType.ANALYSIS
            elif any(kw in text_lower for kw in ["紧急", "urgent", "马上"]):
                task_type = TaskType.URGENT
            elif any(kw in text_lower for kw in ["创意", "设计", "方案"]):
                task_type = TaskType.CREATIVE
            
            task_id = commander.submit_task(content=text, task_type=task_type, user_dna=user_dna)
            task_info = commander.query_task(task_id)
            
            self._send_json({
                "success": True,
                "task_id": task_id,
                "task_type": task_type.value,
                "siri_response": f"任务已完成，由{task_info.get('assigned_to')}处理。",
                "result": task_info.get('result')
            })
        else:
            self._send_json({"error": "未知路径"}, 404)

def run(port=9623):
    server = HTTPServer(('0.0.0.0', port), SiriHandler)
    print(f"🎙️ Siri API: http://0.0.0.0:{port}")
    print(f"   公网访问: http://119.13.90.27:{port}/siri/command")
    server.serve_forever()

if __name__ == "__main__":
    run()
PYEOF2

echo "✅ Siri API创建完成"
echo ""

echo "📦 步骤3/4: 创建systemd服务..."

cat > /etc/systemd/system/cnsh-siri.service << 'SVCEOF'
[Unit]
Description=CNSH Siri API - 龍魂AI调度中枢
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/cnsh
ExecStart=/usr/bin/python3 /root/cnsh/siri_api.py
Restart=always
RestartSec=5
Environment=PYTHONPATH=/root/cnsh

[Install]
WantedBy=multi-user.target
SVCEOF

echo "✅ 服务配置创建完成"
echo ""

echo "📦 步骤4/4: 启动服务..."

systemctl daemon-reload
systemctl enable cnsh-siri
systemctl start cnsh-siri

sleep 2

# 检查状态
if systemctl is-active cnsh-siri > /dev/null; then
    echo "✅ Siri API服务已启动"
else
    echo "❌ 启动失败，检查日志: journalctl -u cnsh-siri"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🎉 部署完成！"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📱 Siri快捷指令配置:"
echo "   1. 创建快捷指令"
echo "   2. 添加'获取文本输入'"
echo "   3. 添加'获取URL内容' POST到:"
echo "      http://119.13.90.27:9623/siri/command"
echo "   4. 请求体JSON:"
echo '      {"text": "输入的文本", "user_dna": "UID9622"}'
echo "   5. 添加'朗读文本'"
echo ""
echo "📊 管理命令:"
echo "   systemctl status cnsh-siri    # 查看状态"
echo "   systemctl restart cnsh-siri   # 重启服务"
echo "   journalctl -u cnsh-siri -f    # 查看日志"
echo ""
echo "🐉 UID9622 - 所有智能听你的！"
echo "═══════════════════════════════════════════════════════════════"
