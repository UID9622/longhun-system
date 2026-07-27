#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
观澜浏览器AI联动 API服务 v1.0 · GuanLan Browser AI Integration API
═══════════════════════════════════════════════════════════
DNA: #龍芯⚡️丙午·乙未·丙申·酉时·☴巽-GUANLAN-API-V1.0-3f7a1c8e
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

端点:
  GET  /health               — 健康检查
  GET  /status               — 全系统状态报告
  POST /route                — 任务路由（M1）
  POST /circuit-breaker/fail — 记录失败（M2）
  POST /circuit-breaker/reset— 重置断路器
  GET  /circuit-breaker      — 断路器状态
  POST /privacy/scan         — 隐私出域扫描（M8）
  POST /plugin/audit         — 插件权限审计（M5）
  POST /engine/register      — AI引擎注册（M4）
  GET  /engines              — 已注册引擎列表
  POST /ledger/record        — 人机记账（M6）
  GET  /ledger               — 两本账看板
  POST /compare              — 多模型对比（M9）
  POST /annotate             — AI标注验证（M3）
  POST /chat                 — Chat透传端点 (M1·v2 unified format)
"""

import sys
import os
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Dict, Any

# 路径修复
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from lh_guanlan_router import (
    观澜总控, CNSH_断路器, CNSH_模型路由, CNSH_接口槽, CNSH_插件审计,
    CNSH_两本账, CNSH_网关, CNSH_出域闸门, CNSH_多模型对比,
    CNSH_AI标注, CNSH_标注验证, AI标注结果, 引擎位置, 审计色,
    熔断审计链
)

# ═══════════════════════════════════════════════════════════
# 全局实例
# ═══════════════════════════════════════════════════════════

ctrl = 观澜总控()

# 预注册示例引擎
ctrl.接口槽.注册AI引擎(
    "Ollama", {"dna": "local", "gate": True, "seal": True},
    lambda q: {"回答": f"Ollama回答: {q}", "引擎": "Ollama", "版本": "v3.7", "置信": 0.95}
)
ctrl.接口槽.注册AI引擎(
    "CodeBuddy", {"dna": "cb", "gate": True, "seal": True},
    lambda q: {"回答": f"CodeBuddy回答: {q}", "引擎": "CodeBuddy", "版本": "v1.0", "置信": 0.92}
)
ctrl.接口槽.注册AI引擎(
    "Kimi", {"dna": "cloud", "gate": True, "seal": True},
    lambda q: {"回答": f"Kimi回答: {q}", "引擎": "Kimi", "版本": "v1.0", "置信": 0.88}
)
ctrl.接口槽.注册AI引擎(
    "小艺", {"dna": "hms", "gate": True, "seal": True},
    lambda q: {"回答": f"小艺回答: {q}", "引擎": "小艺", "版本": "v1.0", "置信": 0.85}
)


# ═══════════════════════════════════════════════════════════
# HTTP Handler
# ═══════════════════════════════════════════════════════════

class GuanLanHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        """精简日志"""
        print(f"[{time.strftime('%H:%M:%S')}] {args[0]}")

    def _send_json(self, data: Dict[str, Any], status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))

    def _read_body(self) -> Dict:
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length))

    def _route_path(self):
        parsed = urlparse(self.path)
        return parsed.path.rstrip('/'), parse_qs(parsed.query)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        path, params = self._route_path()

        if path == '/health':
            self._send_json({
                "status": "🟢",
                "service": "观澜浏览器AI联动API",
                "version": "v1.0",
                "time": int(time.time()),
                "dna": "#龍芯⚡️丙午·乙未·丙申·酉时·☴巽-GUANLAN-API-V1.0-3f7a1c8e"
            })

        elif path == '/status':
            self._send_json(ctrl.状态报告())

        elif path == '/circuit-breaker':
            engine = params.get('engine', [None])[0]
            self._send_json({
                "断路器": ctrl.断路器.状态(engine),
                "审计链": ctrl.断路器.审计报告()
            })

        elif path == '/engines':
            self._send_json({
                "已注册引擎": ctrl.接口槽.引擎列表(),
                "引擎数": len(ctrl.接口槽.已注册引擎)
            })

        elif path == '/ledger':
            self._send_json(ctrl.账本.看板JSON())

        elif path == '/gateway':
            self._send_json(ctrl.网关.联网状态())

        else:
            self._send_json({"error": "Not found", "path": path}, 404)

    def do_POST(self):
        path, params = self._route_path()
        body = self._read_body()

        # ── M1 模型路由 ──
        if path == '/route':
            task = body.get('task', '通用')
            preference = body.get('preference')
            force_local = body.get('force_local', False)

            result = ctrl.处理请求(task, 用户偏好=preference, 强制本地=force_local)
            self._send_json({
                "任务": task,
                "路由": result.to_dict(),
                "路由字符串": result.标注.标注字符串()
            })

        # ── M2 断路器 ──
        elif path == '/circuit-breaker/fail':
            engine = body.get('engine', 'Ollama')
            reason = body.get('reason', '')
            triggered = ctrl.断路器.记失败(engine, reason)
            self._send_json({
                "引擎": engine,
                "触发熔断": triggered,
                "状态": ctrl.断路器.状态(engine)
            })

        elif path == '/circuit-breaker/reset':
            engine = body.get('engine')
            if engine:
                ctrl.断路器.记成功(engine)
            self._send_json({
                "引擎": engine,
                "状态": ctrl.断路器.状态(engine)
            })

        # ── M3 AI标注 ──
        elif path == '/annotate':
            engine = body.get('engine', 'Unknown')
            version = body.get('version', 'v1.0')
            confidence = body.get('confidence', 1.0)
            is_cloud = body.get('cloud', False)

            label = CNSH_AI标注(engine, version, 云=is_cloud, 置信度=confidence)
            valid, msg = CNSH_标注验证(label)
            self._send_json({
                "标注": label.to_dict(),
                "标注字符串": label.标注字符串(),
                "验证": {"合规": valid, "消息": msg}
            })

        # ── M4 引擎注册 ──
        elif path == '/engine/register':
            name = body.get('name', '')
            anchors = body.get('anchors', {})
            if not name:
                self._send_json({"error": "缺少引擎名"}, 400)
                return

            def mock_engine(q):
                return {"回答": f"[{name}] {q}", "引擎": name, "版本": "v1.0", "置信": 0.8}

            result = ctrl.接口槽.注册AI引擎(name, anchors, mock_engine)
            self._send_json({
                "引擎": name,
                "结果": {"过": result.过, "状态": result.状态, "原因": result.原因}
            })

        # ── M5 插件审计 ──
        elif path == '/plugin/audit':
            permissions = body.get('permissions', [])
            result = ctrl.插件审.审查(permissions)
            self._send_json({
                "权限": permissions,
                "结果": {"过": result.过, "状态": result.状态, "违规": result.违规权限}
            })

        # ── M6 人机记账 ──
        elif path == '/ledger/record':
            side = body.get('side', '人工')
            count = body.get('count', 1)
            url = body.get('url', '')
            try:
                ctrl.账本.记(side, count, url=url)
                self._send_json({"状态": "已记录", "账本": ctrl.账本.看板JSON()})
            except ValueError as e:
                self._send_json({"error": str(e)}, 400)

        # ── M8 隐私出域扫描 ──
        elif path == '/privacy/scan':
            text = body.get('text', '')
            strategy = body.get('strategy', '脱敏')
            result = ctrl.闸门.扫描(text, 策略=strategy)
            self._send_json({
                "结果": {"过": result.过, "状态": result.状态, "命中": result.命中模式},
                "脱敏后": result.脱敏后文本 if strategy == '脱敏' else None,
                "原始长度": len(text)
            })

        # ── M9 多模型对比 ──
        elif path == '/compare':
            question = body.get('question', '')
            engine_a = body.get('engine_a', 'Ollama')
            engine_b = body.get('engine_b', 'Kimi')

            # 模拟两个引擎回答
            ans_a = {"引擎": engine_a, "回答": f"[{engine_a}] 对'{question}'的回答", "标注": CNSH_AI标注(engine_a).to_dict()}
            ans_b = {"引擎": engine_b, "回答": f"[{engine_b}] 对'{question}'的另一个视角", "标注": CNSH_AI标注(engine_b, 云=True).to_dict()}

            result = ctrl.对比.对比(question, ans_a, ans_b)
            self._send_json({
                "问题": question,
                "回答A": ans_a,
                "回答B": ans_b,
                "分歧点": result.分歧点,
                "共识度": round(result.共识度, 3)
            })

        # ── M1 Chat 透传端点 (v2.0 unified format) ──
        elif path == '/chat':
            import urllib.request
            import urllib.error
            import hashlib

            query = body.get('query', '')
            if not query:
                self._send_json({"error": "missing 'query' field"}, 400)
                return

            route_id = body.get('route_id', hashlib.sha256(query.encode()).hexdigest()[:12])
            persona_code = body.get('persona_code', 'guanlan_m1')

            # M1: 透传到 Ollama
            ollama_body = json.dumps({
                "model": "qwen2.5:1.5b",
                "prompt": query,
                "stream": False,
            }).encode("utf-8")

            req = urllib.request.Request(
                "http://localhost:11434/api/generate",
                data=ollama_body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    raw = resp.read().decode("utf-8")
                    data = json.loads(raw)
                    answer = data.get("response", "")
                    self._send_json({
                        "answer": answer,
                        "model": "qwen2.5:1.5b",
                        "backend": "ollama_passthrough",
                        "milestone": "M1",
                        "route_id": route_id,
                        "persona_code": persona_code,
                        "dna": "#龍芯⚡️丙午·乙未·丙申·酉时·☴巽-GUANLAN-API-V1.0",
                        "audit_mark": "🟢",
                    })
            except urllib.error.URLError as e:
                self._send_json({
                    "answer": f"观澜M1: Ollama连接失败 ({e.reason})",
                    "backend": "none",
                    "milestone": "M1",
                    "dna": "#龍芯⚡️丙午·乙未·丙申·酉时·☴巽-GUANLAN-API-V1.0",
                    "audit_mark": "🔴",
                }, 503)

        else:
            self._send_json({"error": "Not found", "path": path}, 404)


# ═══════════════════════════════════════════════════════════
# 自测试
# ═══════════════════════════════════════════════════════════

def api_self_test() -> tuple[int, int, list]:
    """API端点自测试（用HTTP请求）"""
    import urllib.request
    import urllib.error

    base = "http://127.0.0.1:8770"
    passed = 0
    failed = 0
    details = []

    def test(name, method, path, body=None, check=None):
        nonlocal passed, failed
        try:
            data = json.dumps(body).encode() if body else None
            req = urllib.request.Request(
                f"{base}{path}", data=data,
                headers={"Content-Type": "application/json"} if data else {},
                method=method
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                result = json.loads(resp.read())
            if check:
                assert check(result), f"检查失败: {result}"
            passed += 1
            details.append({"端点": f"{method} {path}", "状态": "🟢"})
            return result
        except Exception as e:
            failed += 1
            details.append({"端点": f"{method} {path}", "状态": "🔴", "错误": str(e)})
            return None

    # 1. 健康检查
    r = test("健康检查", "GET", "/health", check=lambda r: r["status"] == "🟢")

    # 2. 系统状态
    test("系统状态", "GET", "/status", check=lambda r: "网关" in r and "断路器" in r)

    # 3. 任务路由 - 代码
    test("路由:代码", "POST", "/route", {"task": "代码"},
         check=lambda r: r["路由"]["引擎"] == "CodeBuddy")

    # 4. 任务路由 - 隐私（锁定本地）
    test("路由:隐私", "POST", "/route", {"task": "隐私"},
         check=lambda r: r["路由"]["引擎"] == "Ollama")

    # 5. 任务路由 - 长文档
    test("路由:长文档", "POST", "/route", {"task": "长文档"},
         check=lambda r: r["路由"]["引擎"] == "Kimi")

    # 6. 断路器 - 记录失败
    test("断路器:记失败", "POST", "/circuit-breaker/fail", {"engine": "TestEngine", "reason": "测试"},
         check=lambda r: "触发熔断" in r)

    # 7. 断路器状态
    test("断路器:状态", "GET", "/circuit-breaker", check=lambda r: "断路器" in r)

    # 8. 隐私扫描 - 脱敏
    test("隐私扫描:脱敏", "POST", "/privacy/scan",
         {"text": "我的手机13800138000，邮箱test@example.com", "strategy": "脱敏"},
         check=lambda r: r["结果"]["过"] and "手机号" in r["结果"]["命中"])

    # 9. 隐私扫描 - 拦截
    test("隐私扫描:拦截", "POST", "/privacy/scan",
         {"text": "身份证110101199001011234", "strategy": "拦截"},
         check=lambda r: not r["结果"]["过"])

    # 10. 插件审计 - 拒装
    test("插件审计:拒装", "POST", "/plugin/audit",
         {"permissions": ["读历史", "改页面", "发网络"]},
         check=lambda r: not r["结果"]["过"] and len(r["结果"]["违规"]) >= 2)

    # 11. 两本账 - 记账
    test("账本:记账", "POST", "/ledger/record", {"side": "人工", "count": 10, "url": "https://test.com"},
         check=lambda r: r["账本"]["人工"] >= 10)

    # 12. 两本账 - 看板
    test("账本:看板", "GET", "/ledger", check=lambda r: "人工" in r and "爬虫" in r)

    # 13. AI标注
    test("AI标注", "POST", "/annotate", {"engine": "Ollama", "confidence": 0.95},
         check=lambda r: "标注字符串" in r and r["验证"]["合规"])

    # 14. 多模型对比
    test("多模型对比", "POST", "/compare", {"question": "什么是观澜？"},
         check=lambda r: "共识度" in r)

    return passed, passed + failed, details


# ═══════════════════════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(description="观澜浏览器AI联动API服务 v1.0")
    parser.add_argument('--port', type=int, default=8770, help='端口 (默认8770)')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='绑定地址')
    parser.add_argument('--test', action='store_true', help='API自测试（需先启动服务）')

    args = parser.parse_args()

    if args.test:
        print("=" * 60)
        print("  观澜API · 自测试")
        print("=" * 60)
        # 先启动服务
        import threading
        server = HTTPServer((args.host, args.port), GuanLanHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        time.sleep(0.5)

        passed, total, details = api_self_test()
        for d in details:
            print(f"  {d['端点']:30s} {d['状态']} {d.get('错误', '')}")

        print("-" * 60)
        if passed == total:
            print(f"  🟢 全部通过: {passed}/{total}")
        else:
            print(f"  🔴 通过: {passed}/{total}  失败: {total-passed}")
        print("=" * 60)

        server.shutdown()
        return

    print("=" * 60)
    print("  观澜浏览器AI联动 API 服务 v1.0")
    print("  DNA: #龍芯⚡️丙午·乙未·丙申·酉时·☴巽-GUANLAN-API-V1.0")
    print("=" * 60)
    print(f"  地址: http://{args.host}:{args.port}")
    print(f"  健康: http://{args.host}:{args.port}/health")
    print(f"  状态: http://{args.host}:{args.port}/status")
    print(f"  端点: 14 个")
    print("=" * 60)

    server = HTTPServer((args.host, args.port), GuanLanHandler)
    try:
        print(f"\n  🟢 观澜API已就绪 · Ctrl+C 停止\n")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  🟡 观澜API已停止")
        server.shutdown()


if __name__ == "__main__":
    main()
