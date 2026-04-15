#!/usr/bin/env python3
"""
CNSH Siri快捷指令API
═══════════════════════════════════════════════════════════════════
Endpoint: http://119.13.90.27:9622/siri/command
Method: POST
Body: {"text": "你的指令", "user_dna": "UID9622"}

Siri快捷指令配置:
1. 创建快捷指令
2. 添加"获取文本输入"
3. 添加"获取URL内容" POST到 http://119.13.90.27:9622/siri/command
4. 添加"朗读文本"
═══════════════════════════════════════════════════════════════════
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time

# 导入调度器
from cnsh_dragon_soul_commander import DragonSoulCommander, TaskType, AIPriority

# 全局调度器实例
commander = DragonSoulCommander()
commander.start()


class SiriAPIHandler(BaseHTTPRequestHandler):
    """Siri API处理器"""
    
    def log_message(self, format, *args):
        """自定义日志"""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")
    
    def _send_json(self, data: dict, status=200):
        """发送JSON响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """处理CORS预检"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """处理GET请求"""
        path = self.path
        
        if path == '/':
            # 根路径 - 系统信息
            self._send_json({
                "system": "龍魂AI统一调度中枢",
                "version": commander.VERSION,
                "codename": commander.CODENAME,
                "motto": commander.MOTTO,
                "creator": "诸葛鑫（UID9622）",
                "endpoints": [
                    "/siri/command - Siri快捷指令",
                    "/task/submit - 提交任务",
                    "/task/{id} - 查询任务",
                    "/workers - AI节点状态",
                    "/stats - 统计信息"
                ]
            })
        
        elif path == '/workers':
            # AI节点状态
            self._send_json(commander.get_worker_status())
        
        elif path == '/stats':
            # 统计信息
            self._send_json(commander.get_stats())
        
        elif path.startswith('/task/'):
            # 查询任务
            task_id = path.split('/')[-1]
            result = commander.query_task(task_id)
            self._send_json(result)
        
        else:
            self._send_json({"error": "未知路径"}, 404)
    
    def do_POST(self):
        """处理POST请求"""
        path = self.path
        
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            body = json.loads(post_data.decode('utf-8'))
        except:
            self._send_json({"error": "无效的JSON"}, 400)
            return
        
        if path == '/siri/command':
            # Siri快捷指令
            self._handle_siri_command(body)
        
        elif path == '/task/submit':
            # 提交任务
            self._handle_task_submit(body)
        
        else:
            self._send_json({"error": "未知路径"}, 404)
    
    def _handle_siri_command(self, body: dict):
        """处理Siri命令"""
        text = body.get('text', '').strip()
        user_dna = body.get('user_dna', 'UID9622')
        
        if not text:
            self._send_json({"error": "文本不能为空"}, 400)
            return
        
        # 识别任务类型
        task_type = self._detect_task_type(text)
        
        # 提交任务
        task_id = commander.submit_task(
            content=text,
            task_type=task_type,
            user_dna=user_dna
        )
        
        # 等待任务完成（简化版，实际应异步）
        time.sleep(1)
        task_info = commander.query_task(task_id)
        
        # 生成Siri友好的回复
        response_text = self._generate_siri_response(task_info)
        
        self._send_json({
            "success": True,
            "task_id": task_id,
            "task_type": task_type.value,
            "siri_response": response_text,
            "assigned_to": task_info.get('assigned_to'),
            "result": task_info.get('result')
        })
    
    def _handle_task_submit(self, body: dict):
        """处理任务提交"""
        content = body.get('content', '').strip()
        task_type_str = body.get('type', 'chat')
        priority_str = body.get('priority', 'china_first')
        user_dna = body.get('user_dna', 'UID9622')
        
        if not content:
            self._send_json({"error": "内容不能为空"}, 400)
            return
        
        # 转换枚举
        try:
            task_type = TaskType(task_type_str)
        except:
            task_type = TaskType.CHAT
        
        try:
            priority = AIPriority(priority_str)
        except:
            priority = AIPriority.CHINA_FIRST
        
        # 提交任务
        task_id = commander.submit_task(
            content=content,
            task_type=task_type,
            priority=priority,
            user_dna=user_dna
        )
        
        self._send_json({
            "success": True,
            "task_id": task_id,
            "message": "任务已提交"
        })
    
    def _detect_task_type(self, text: str) -> TaskType:
        """识别任务类型"""
        text_lower = text.lower()
        
        keywords = {
            TaskType.CODE: ["写代码", "编程", "code", "函数", "script", "python", "javascript", "程序"],
            TaskType.ANALYSIS: ["分析", "数据", "统计", "图表", "分析", "计算"],
            TaskType.RESEARCH: ["研究", "论文", "报告", "调研", "research", "调查"],
            TaskType.URGENT: ["紧急", "urgent", "马上", "立刻", "现在", "快", "急"],
            TaskType.CREATIVE: ["创意", "想法", "设计", "方案", "creative", " slogan", "口号"],
            TaskType.IMAGE: ["图片", "图像", "画", "生成图", "image", "photo"],
            TaskType.VOICE: ["语音", "声音", "录音", "voice", "audio"]
        }
        
        for task_type, kw_list in keywords.items():
            if any(kw in text_lower for kw in kw_list):
                return task_type
        
        return TaskType.CHAT
    
    def _generate_siri_response(self, task_info: dict) -> str:
        """生成Siri友好的回复"""
        status = task_info.get('status')
        assigned = task_info.get('assigned_to', '未知')
        
        if status == 'completed':
            return f"任务已完成，由{assigned}处理。"
        elif status == 'running':
            return f"任务正在处理中，由{assigned}负责。"
        elif status == 'failed':
            return "任务处理失败，请稍后重试。"
        else:
            return f"任务已提交，正在分配给最优AI。"


def run_server(port=9623):
    """运行Siri API服务器"""
    server = HTTPServer(('0.0.0.0', port), SiriAPIHandler)
    print(f"🎙️ Siri API服务器已启动: http://0.0.0.0:{port}")
    print(f"   快捷指令Endpoint: http://119.13.90.27:{port}/siri/command")
    print("\n📱 Siri快捷指令配置:")
    print("   1. 创建快捷指令")
    print("   2. 添加'获取文本输入'")
    print(f"   3. POST到 http://119.13.90.27:{port}/siri/command")
    print("   4. 添加'朗读文本'")
    print("\n按Ctrl+C停止")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")


if __name__ == "__main__":
    run_server()
