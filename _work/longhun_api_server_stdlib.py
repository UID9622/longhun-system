#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂 · HTTP API 服务器 (标准库版本) v1.0
Dragon Soul API Server - Pure Python stdlib (no FastAPI required)

DNA追溯碼：#龍芯⚡️2026-05-27-API-SERVER-STDLIB-v1.0
CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 提供 REST API 接口（使用 http.server）
  2. 支持移动端远程触发排序算法
  3. 与 longhun_notion_pow.py 集成（PoW 记账）
  4. HTML5 移动控制面板
  5. CORS 支持（跨域访问）

运行：
  python3 longhun_api_server_stdlib.py

访问：
  本地：http://localhost:5000
  移动面板：http://localhost:5000/control
  API调用：http://localhost:5000/run_sort

内网穿透：
  ngrok http 5000
"""

import json
import sys
import random
import signal
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict

# 导入配置管理器
sys.path.insert(0, str(Path(__file__).parent))
try:
    from 配置读取器 import CONFIG
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    print("⚠️  警告: 配置读取器不可用，使用默认端口")

# 导入 PoW 系统
try:
    from longhun_notion_pow import log_sorting_work
    POW_AVAILABLE = True
except ImportError:
    POW_AVAILABLE = False
    print("⚠️  警告: longhun_notion_pow 不可用，PoW 功能已禁用")


class SortAlgorithms:
    """排序算法实现"""

    @staticmethod
    def bubble_sort(arr: list) -> Tuple[int, int]:
        """冒泡排序"""
        comparisons = 0
        swaps = 0
        arr = arr.copy()
        n = len(arr)

        for i in range(n):
            for j in range(0, n - i - 1):
                comparisons += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swaps += 1
        return comparisons, swaps

    @staticmethod
    def insertion_sort(arr: list) -> Tuple[int, int]:
        """插入排序"""
        comparisons = 0
        swaps = 0
        arr = arr.copy()

        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0:
                comparisons += 1
                if arr[j] > key:
                    arr[j + 1] = arr[j]
                    swaps += 1
                    j -= 1
                else:
                    break
            arr[j + 1] = key
        return comparisons, swaps

    @staticmethod
    def selection_sort(arr: list) -> Tuple[int, int]:
        """选择排序"""
        comparisons = 0
        swaps = 0
        arr = arr.copy()
        n = len(arr)

        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                comparisons += 1
                if arr[j] < arr[min_idx]:
                    min_idx = j
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                swaps += 1
        return comparisons, swaps

    @staticmethod
    def quick_sort(arr: list) -> Tuple[int, int]:
        """快速排序"""

        def partition(low, high):
            stats = {"comparisons": 0, "swaps": 0}
            pivot = arr[high]
            i = low - 1

            for j in range(low, high):
                stats["comparisons"] += 1
                if arr[j] < pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    stats["swaps"] += 1
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            stats["swaps"] += 1
            return i + 1, stats

        def quick_sort_helper(low, high):
            total_stats = {"comparisons": 0, "swaps": 0}
            if low < high:
                pi, stats = partition(low, high)
                total_stats["comparisons"] += stats["comparisons"]
                total_stats["swaps"] += stats["swaps"]

                left_stats = quick_sort_helper(low, pi - 1)
                right_stats = quick_sort_helper(pi + 1, high)

                total_stats["comparisons"] += (
                    left_stats["comparisons"] + right_stats["comparisons"]
                )
                total_stats["swaps"] += left_stats["swaps"] + right_stats["swaps"]

            return total_stats

        arr = arr.copy()
        stats = quick_sort_helper(0, len(arr) - 1)
        return stats["comparisons"], stats["swaps"]

    @staticmethod
    def merge_sort(arr: list) -> Tuple[int, int]:
        """合并排序"""

        def merge_sort_helper(arr):
            stats = {"comparisons": 0, "swaps": 0}
            if len(arr) <= 1:
                return arr, stats

            mid = len(arr) // 2
            left, left_stats = merge_sort_helper(arr[:mid])
            right, right_stats = merge_sort_helper(arr[mid:])

            stats["comparisons"] = left_stats["comparisons"] + right_stats["comparisons"]
            stats["swaps"] = left_stats["swaps"] + right_stats["swaps"]

            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                stats["comparisons"] += 1
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
                stats["swaps"] += 1

            merged.extend(left[i:])
            merged.extend(right[j:])
            stats["swaps"] += len(left[i:]) + len(right[j:])

            return merged, stats

        arr = arr.copy()
        _, stats = merge_sort_helper(arr)
        return stats["comparisons"], stats["swaps"]

    @staticmethod
    def shell_sort(arr: list) -> Tuple[int, int]:
        """希尔排序"""
        comparisons = 0
        swaps = 0
        arr = arr.copy()
        n = len(arr)
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap:
                    comparisons += 1
                    if arr[j - gap] > temp:
                        arr[j] = arr[j - gap]
                        swaps += 1
                        j -= gap
                    else:
                        break
                arr[j] = temp
            gap //= 2

        return comparisons, swaps


class APIHandler(BaseHTTPRequestHandler):
    """HTTP 请求处理器"""

    def log_message(self, format, *args):
        """简化日志输出"""
        print(f"[{self.client_address[0]}] {format % args}")

    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # 路由: GET /
        if path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>🐉 龍魂 API 服务器</title>
                <style>
                    body { font-family: Arial; margin: 40px; background: #0a0714; color: #fff; }
                    h1 { color: #ffd700; }
                    .api-info { background: #1a1a2e; padding: 15px; border-radius: 5px; }
                    code { background: #0d0d1a; padding: 5px 10px; border-radius: 3px; }
                    a { color: #00d4ff; text-decoration: none; }
                    a:hover { text-decoration: underline; }
                </style>
            </head>
            <body>
                <h1>🐉 龍魂 · HTTP API 服务器</h1>
                <p>DNA: <code>#龍芯⚡️2026-05-27-API-SERVER-STDLIB-v1.0</code></p>

                <h2>📱 快速开始</h2>
                <ul>
                    <li><a href="/control">移动控制面板</a></li>
                    <li><a href="/docs">API 文档</a></li>
                    <li><a href="/status">服务器状态</a></li>
                </ul>

                <h2>🔌 API 端点</h2>
                <div class="api-info">
                    <p><strong>GET /status</strong> - 服务器状态检查</p>
                    <p><strong>POST /run_sort</strong> - 执行排序 (JSON: {"algorithm": "bubble_sort", "array_size": 100})</p>
                    <p><strong>GET /algorithms</strong> - 列出支持的算法</p>
                    <p><strong>GET /control</strong> - 移动控制面板</p>
                </div>

                <h2>🚀 外网访问</h2>
                <pre>ngrok http 5000</pre>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))

        # 路由: GET /control（移动面板）
        elif path == "/control":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = self._generate_control_panel()
            self.wfile.write(html.encode("utf-8"))

        # 路由: GET /status
        elif path == "/status":
            self.send_json(200, {"status": "running", "timestamp": datetime.now().isoformat()})

        # 路由: GET /algorithms
        elif path == "/algorithms":
            algos = [
                "bubble_sort",
                "insertion_sort",
                "selection_sort",
                "quick_sort",
                "merge_sort",
                "shell_sort",
            ]
            self.send_json(200, {"algorithms": algos})

        # 路由: GET /docs
        elif path == "/docs":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>API 文档</title>
                <style>
                    body { font-family: monospace; margin: 20px; background: #0a0714; color: #fff; }
                    pre { background: #1a1a2e; padding: 10px; border-radius: 5px; overflow-x: auto; }
                </style>
            </head>
            <body>
                <h1>🐉 龍魂 API 文档</h1>
                <h2>POST /run_sort</h2>
                <p>执行排序算法</p>
                <h3>请求体:</h3>
                <pre>{
  "algorithm": "bubble_sort",
  "array_size": 100,
  "description": "Test sorting"
}</pre>
                <h3>响应:</h3>
                <pre>{
  "algorithm": "bubble_sort",
  "array_size": 100,
  "comparisons": 4950,
  "swaps": 2475,
  "pow_hash": "abc123...",
  "local_id": "local_123456",
  "notion_page_id": null,
  "timestamp": "2026-05-27T12:00:00"
}</pre>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode("utf-8"))

    def do_POST(self):
        """处理 POST 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # 读取请求体
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            request_data = json.loads(body)
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Invalid JSON"})
            return

        # 路由: POST /run_sort
        if path == "/run_sort":
            algorithm = request_data.get("algorithm", "bubble_sort")
            array_size = request_data.get("array_size", 100)

            # 验证参数
            if array_size < 1 or array_size > 1000:
                self.send_json(400, {"error": "array_size 应在 1-1000 之间"})
                return

            # 获取算法
            algo_func = getattr(SortAlgorithms, algorithm, None)
            if not algo_func:
                self.send_json(400, {"error": f"未知算法: {algorithm}"})
                return

            # 执行排序
            test_array = [random.randint(1, 10000) for _ in range(array_size)]
            try:
                comparisons, swaps = algo_func(test_array)
            except Exception as e:
                self.send_json(500, {"error": f"排序执行失败: {str(e)}"})
                return

            # 生成 PoW 记录（如果可用）
            pow_hash = "mock_" + str(random.randint(100000, 999999))
            local_id = f"local_{int(datetime.now().timestamp() * 1000)}"
            notion_page_id = None

            if POW_AVAILABLE:
                try:
                    record = log_sorting_work(
                        comparisons=comparisons,
                        swaps=swaps,
                        algorithm_name=algorithm,
                        array_size=array_size,
                    )
                    pow_hash = record.pow_hash
                    local_id = record.local_id
                    notion_page_id = record.notion_page_id
                except Exception as e:
                    print(f"⚠️  PoW 记录失败: {e}")

            # 返回结果
            response = {
                "algorithm": algorithm,
                "array_size": array_size,
                "comparisons": comparisons,
                "swaps": swaps,
                "pow_hash": pow_hash,
                "local_id": local_id,
                "notion_page_id": notion_page_id,
                "timestamp": datetime.now().isoformat(),
            }
            self.send_json(200, response)

        else:
            self.send_json(404, {"error": "Not Found"})

    def do_OPTIONS(self):
        """处理 CORS preflight"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def send_json(self, status_code: int, data: Dict):
        """发送 JSON 响应"""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _generate_control_panel(self) -> str:
        """生成移动控制面板 HTML"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🐉 龍魂 移动控制面板</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #0a0714 0%, #1a1a2e 100%);
                    color: #fff;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                .container {
                    max-width: 500px;
                    width: 100%;
                    background: rgba(26, 26, 46, 0.9);
                    border: 2px solid #ffd700;
                    border-radius: 10px;
                    padding: 30px;
                    box-shadow: 0 0 30px rgba(255, 215, 0, 0.1);
                }
                h1 {
                    color: #ffd700;
                    margin-bottom: 10px;
                    font-size: 24px;
                }
                .subtitle {
                    color: #00d4ff;
                    margin-bottom: 30px;
                    font-size: 14px;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 8px;
                    color: #00d4ff;
                    font-weight: bold;
                    font-size: 14px;
                }
                select, input {
                    width: 100%;
                    padding: 12px;
                    border: 1px solid #ffd700;
                    border-radius: 5px;
                    background: #0a0714;
                    color: #fff;
                    font-size: 14px;
                }
                select:focus, input:focus {
                    outline: none;
                    border-color: #00d4ff;
                    box-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
                }
                .slider-value {
                    color: #ffd700;
                    margin-top: 5px;
                    text-align: center;
                }
                button {
                    width: 100%;
                    padding: 14px;
                    background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
                    color: #0a0714;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 16px;
                    cursor: pointer;
                    margin-top: 10px;
                    transition: transform 0.2s, box-shadow 0.2s;
                }
                button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 20px rgba(255, 215, 0, 0.3);
                }
                button:active {
                    transform: translateY(0);
                }
                button:disabled {
                    opacity: 0.5;
                    cursor: not-allowed;
                    transform: none;
                }
                .results {
                    margin-top: 30px;
                    padding: 20px;
                    background: rgba(0, 212, 255, 0.1);
                    border: 1px solid #00d4ff;
                    border-radius: 5px;
                    display: none;
                }
                .results.show {
                    display: block;
                }
                .result-item {
                    margin-bottom: 12px;
                    font-size: 14px;
                }
                .result-label {
                    color: #ffd700;
                    font-weight: bold;
                }
                .result-value {
                    color: #00d4ff;
                    word-break: break-all;
                    margin-top: 4px;
                    font-family: monospace;
                }
                .status {
                    text-align: center;
                    margin-top: 20px;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 14px;
                }
                .status.loading {
                    background: rgba(255, 215, 0, 0.1);
                    color: #ffd700;
                }
                .status.success {
                    background: rgba(0, 212, 255, 0.1);
                    color: #00d4ff;
                }
                .status.error {
                    background: rgba(255, 0, 0, 0.1);
                    color: #ff6b6b;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🐉 龍魂控制面板</h1>
                <p class="subtitle">远程排序算法调度系统</p>

                <div class="form-group">
                    <label for="algorithm">选择算法</label>
                    <select id="algorithm">
                        <option value="bubble_sort">冒泡排序</option>
                        <option value="insertion_sort">插入排序</option>
                        <option value="selection_sort">选择排序</option>
                        <option value="quick_sort">快速排序</option>
                        <option value="merge_sort">合并排序</option>
                        <option value="shell_sort">希尔排序</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="array_size">数组大小: <span id="size_display">100</span></label>
                    <input type="range" id="array_size" min="10" max="500" value="100" step="10">
                    <div class="slider-value">当前值: <span id="slider_value">100</span></div>
                </div>

                <button id="run_btn" onclick="runSort()">🚀 执行排序</button>
                <button onclick="resetForm()" style="background: #555;">🔄 重置</button>

                <div id="status" class="status"></div>

                <div id="results" class="results">
                    <h3 style="color: #ffd700; margin-bottom: 15px;">📊 排序结果</h3>

                    <div class="result-item">
                        <div class="result-label">算法</div>
                        <div class="result-value" id="result_algorithm">-</div>
                    </div>

                    <div class="result-item">
                        <div class="result-label">数组大小</div>
                        <div class="result-value" id="result_size">-</div>
                    </div>

                    <div class="result-item">
                        <div class="result-label">比较次数</div>
                        <div class="result-value" id="result_comparisons">-</div>
                    </div>

                    <div class="result-item">
                        <div class="result-label">交换次数</div>
                        <div class="result-value" id="result_swaps">-</div>
                    </div>

                    <div class="result-item">
                        <div class="result-label">PoW 哈希</div>
                        <div class="result-value" id="result_hash">-</div>
                    </div>

                    <div class="result-item">
                        <div class="result-label">本地 ID</div>
                        <div class="result-value" id="result_local_id">-</div>
                    </div>

                    <div class="result-item">
                        <div class="result-label">时间戳</div>
                        <div class="result-value" id="result_timestamp">-</div>
                    </div>
                </div>
            </div>

            <script>
                const sizeInput = document.getElementById('array_size');
                const sizeDisplay = document.getElementById('size_display');
                const sliderValue = document.getElementById('slider_value');

                sizeInput.addEventListener('input', (e) => {
                    sizeDisplay.textContent = e.target.value;
                    sliderValue.textContent = e.target.value;
                });

                function showStatus(message, type) {
                    const status = document.getElementById('status');
                    status.textContent = message;
                    status.className = 'status ' + type;
                    status.style.display = 'block';
                }

                function hideStatus() {
                    document.getElementById('status').style.display = 'none';
                }

                function runSort() {
                    const algorithm = document.getElementById('algorithm').value;
                    const arraySize = parseInt(document.getElementById('array_size').value);
                    const runBtn = document.getElementById('run_btn');

                    runBtn.disabled = true;
                    showStatus('⏳ 执行排序中...', 'loading');

                    fetch('/run_sort', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            algorithm: algorithm,
                            array_size: arraySize
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            showStatus('❌ 错误: ' + data.error, 'error');
                        } else {
                            showStatus('✅ 排序完成！', 'success');
                            displayResults(data);
                        }
                        runBtn.disabled = false;
                    })
                    .catch(error => {
                        showStatus('❌ 请求失败: ' + error.message, 'error');
                        runBtn.disabled = false;
                    });
                }

                function displayResults(data) {
                    document.getElementById('result_algorithm').textContent = data.algorithm;
                    document.getElementById('result_size').textContent = data.array_size;
                    document.getElementById('result_comparisons').textContent = data.comparisons;
                    document.getElementById('result_swaps').textContent = data.swaps;
                    document.getElementById('result_hash').textContent = data.pow_hash.substring(0, 32) + '...';
                    document.getElementById('result_local_id').textContent = data.local_id;
                    document.getElementById('result_timestamp').textContent = data.timestamp;

                    document.getElementById('results').classList.add('show');
                }

                function resetForm() {
                    document.getElementById('algorithm').value = 'bubble_sort';
                    document.getElementById('array_size').value = 100;
                    sizeDisplay.textContent = '100';
                    sliderValue.textContent = '100';
                    document.getElementById('results').classList.remove('show');
                    hideStatus();
                }
            </script>
        </body>
        </html>
        """


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🐉 龍魂 · HTTP API 服务器 (标准库版本)")
    print("=" * 80)
    print(f"DNA: #龍芯⚡️2026-05-27-API-SERVER-STDLIB-v1.0")
    print(f"启动时间: {datetime.now().isoformat()}")

    # 服务器配置（从统一配置文件读取）
    if CONFIG_AVAILABLE:
        HOST = CONFIG.get('MAIN_API_HOST', '0.0.0.0')
        PORT = CONFIG.get('THREE_SYSTEM_API_PORT', 5000)
    else:
        HOST = "0.0.0.0"
        PORT = 5000

    server = HTTPServer((HOST, PORT), APIHandler)

    def signal_handler(sig, frame):
        print("\n\n🛑 服务器正在关闭...")
        server.shutdown()
        print("✅ 已停止")

    signal.signal(signal.SIGINT, signal_handler)

    print(f"\n✅ 服务器启动成功！")
    print(f"\n📱 访问地址:")
    print(f"   - 本地: http://localhost:{PORT}")
    print(f"   - 移动面板: http://localhost:{PORT}/control")
    print(f"   - API 文档: http://localhost:{PORT}/docs")
    print(f"   - 服务器状态: http://localhost:{PORT}/status")

    print(f"\n🌐 外网穿透 (使用 ngrok):")
    print(f"   ngrok http {PORT}")

    print(f"\n📝 API 示例:")
    print(f"   curl -X POST http://localhost:{PORT}/run_sort \\")
    print(f"     -H 'Content-Type: application/json' \\")
    print(f"     -d '{json.dumps({'algorithm': 'bubble_sort', 'array_size': 100})}'")

    print(f"\n⌨️  按 Ctrl+C 停止服务器\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
