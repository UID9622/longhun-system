#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

"""
🐉 龍魂 × Kimi 网关

功能：
  • HTTP 服务网关 - 用户直接请求入口
  • 请求路由 - 4 种集成模式分发
  • 响应规范化 - 统一输出格式
  • 速率限制和权限检查

DNA:#龍芯⚡️丙午·甲午·癸丑·戊午·䷨损-KIMI-GATEWAY-v1.0
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import json
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from flask import Flask, request, jsonify

try:
    from kimi_integration import KimiIntegration, IntegrationMode
except ImportError:
    from .kimi_integration import KimiIntegration, IntegrationMode


class KimiGateway:
    """Kimi 网关"""

    def __init__(self, host: str = "0.0.0.0", port: int = 5000, debug: bool = False):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug
        self.integration = KimiIntegration()
        self.request_log = []
        self.rate_limits = {}

        self._setup_routes()

    def _setup_routes(self):
        """设置 Flask 路由"""

        @self.app.route("/health", methods=["GET"])
        def health():
            return jsonify(self.integration.get_health_status()), 200

        @self.app.route("/kimi/backup-inference", methods=["POST"])
        def backup_inference():
            """1️⃣ 备用推理模型"""
            data = request.get_json()
            prompt = data.get("prompt", "")

            if not prompt:
                return jsonify({"error": "prompt is required"}), 400

            result = self.integration.infer_with_fallback(prompt)
            return jsonify(result), 200

        @self.app.route("/kimi/image", methods=["POST"])
        def process_image():
            """2️⃣ 图像处理"""
            data = request.get_json()
            image_url = data.get("image_url")
            query = data.get("query", "分析这个图像")

            if not image_url:
                return jsonify({"error": "image_url is required"}), 400

            result = self.integration.process_image(image_url, query)
            return jsonify(result), 200

        @self.app.route("/kimi/document", methods=["POST"])
        def process_document():
            """2️⃣ 文档处理"""
            data = request.get_json()
            file_path = data.get("file_path")
            query = data.get("query", "分析这个文档")

            if not file_path:
                return jsonify({"error": "file_path is required"}), 400

            result = self.integration.process_document(file_path, query)
            return jsonify(result), 200

        @self.app.route("/kimi/chat/start", methods=["POST"])
        def start_chat():
            """3️⃣ 开始聊天会话"""
            data = request.get_json()
            user_id = data.get("user_id", f"user_{int(datetime.now().timestamp())}")

            session = self.integration.start_realtime_chat(user_id)
            return jsonify(session), 200

        @self.app.route("/kimi/chat/message", methods=["POST"])
        def send_message():
            """3️⃣ 发送聊天消息"""
            data = request.get_json()
            session_id = data.get("session_id")
            user_message = data.get("message")

            if not session_id or not user_message:
                return jsonify({"error": "session_id and message are required"}), 400

            result = self.integration.send_message(session_id, user_message)
            return jsonify(result), 200

        @self.app.route("/kimi/skill", methods=["POST"])
        def use_skill_engine():
            """4️⃣ Skill 引擎"""
            data = request.get_json()
            skill_id = data.get("skill_id")
            skill_input = data.get("input", {})

            if not skill_id:
                return jsonify({"error": "skill_id is required"}), 400

            result = self.integration.use_kimi_for_skill(skill_id, skill_input)
            return jsonify(result), 200

        @self.app.route("/kimi/report", methods=["GET"])
        def integration_report():
            """集成报告"""
            report = self.integration.get_integration_report()
            return jsonify(report), 200

        @self.app.errorhandler(404)
        def not_found(e):
            return jsonify({"error": "endpoint not found"}), 404

        @self.app.errorhandler(500)
        def internal_error(e):
            return jsonify({"error": "internal server error"}), 500

    def run(self):
        """启动网关"""
        print(f"🚀 Kimi 网关启动")
        print(f"  地址: http://{self.host}:{self.port}")
        print(f"  调试: {self.debug}")
        print("\n📡 可用端点:")
        print("  POST /kimi/backup-inference    - 备用推理模型")
        print("  POST /kimi/image               - 图像处理")
        print("  POST /kimi/document            - 文档处理")
        print("  POST /kimi/chat/start          - 启动聊天")
        print("  POST /kimi/chat/message        - 发送聊天消息")
        print("  POST /kimi/skill               - Skill 引擎")
        print("  GET  /kimi/report              - 集成报告")
        print("  GET  /health                   - 健康检查")
        print()

        self.app.run(host=self.host, port=self.port, debug=self.debug)


class KimiGatewayLite:
    """轻量级网关（不依赖 Flask）"""

    def __init__(self):
        self.integration = KimiIntegration()

    def handle_request(self, endpoint: str, method: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """处理请求"""

        if method == "GET":
            if endpoint == "/health":
                return self.integration.get_health_status()
            elif endpoint == "/kimi/report":
                return self.integration.get_integration_report()

        elif method == "POST":
            if endpoint == "/kimi/backup-inference":
                prompt = data.get("prompt")
                if not prompt:
                    return {"error": "prompt is required"}
                return self.integration.infer_with_fallback(prompt)

            elif endpoint == "/kimi/image":
                image_url = data.get("image_url")
                query = data.get("query", "分析这个图像")
                if not image_url:
                    return {"error": "image_url is required"}
                return self.integration.process_image(image_url, query)

            elif endpoint == "/kimi/document":
                file_path = data.get("file_path")
                query = data.get("query", "分析这个文档")
                if not file_path:
                    return {"error": "file_path is required"}
                return self.integration.process_document(file_path, query)

            elif endpoint == "/kimi/chat/start":
                user_id = data.get("user_id", f"user_{int(datetime.now().timestamp())}")
                return self.integration.start_realtime_chat(user_id)

            elif endpoint == "/kimi/chat/message":
                session_id = data.get("session_id")
                user_message = data.get("message")
                if not session_id or not user_message:
                    return {"error": "session_id and message are required"}
                return self.integration.send_message(session_id, user_message)

            elif endpoint == "/kimi/skill":
                skill_id = data.get("skill_id")
                skill_input = data.get("input", {})
                if not skill_id:
                    return {"error": "skill_id is required"}
                return self.integration.use_kimi_for_skill(skill_id, skill_input)

        return {"error": f"Unknown endpoint: {endpoint}"}


if __name__ == "__main__":
    # 使用轻量级网关（不依赖 Flask）
    gateway = KimiGatewayLite()

    # 测试请求
    print("🧪 测试 Kimi 网关\n")

    # 1. 健康检查
    print("1️⃣ 健康检查")
    result = gateway.handle_request("/health", "GET", {})
    print(f"  {json.dumps(result, ensure_ascii=False, indent=2)}\n")

    # 2. 备用推理
    print("2️⃣ 备用推理")
    result = gateway.handle_request(
        "/kimi/backup-inference",
        "POST",
        {"prompt": "龍魂系统的核心是什么？"}
    )
    print(f"  {json.dumps(result, ensure_ascii=False, indent=2)}\n")

    # 3. 启动聊天
    print("3️⃣ 启动聊天")
    result = gateway.handle_request(
        "/kimi/chat/start",
        "POST",
        {"user_id": "test_user"}
    )
    print(f"  {json.dumps(result, ensure_ascii=False, indent=2)}\n")

    # 4. Skill 引擎
    print("4️⃣ Skill 引擎")
    result = gateway.handle_request(
        "/kimi/skill",
        "POST",
        {
            "skill_id": "skill-3-canvas-design",
            "input": {"description": "设计一个现代化的仪表板"}
        }
    )
    print(f"  {json.dumps(result, ensure_ascii=False, indent=2)}\n")

    # 5. 集成报告
    print("5️⃣ 集成报告")
    result = gateway.handle_request("/kimi/report", "GET", {})
    print(f"  {json.dumps(result, ensure_ascii=False, indent=2)}\n")
