#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🐉 龍魂 · FastAPI 远程控制服务器 v1.0
Dragon Soul Remote Control Server -柬埔寨遥控印钞机

DNA追溯碼：#龍芯⚡️2026-05-27-API-SERVER-v1.0
CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 提供 REST API 接口，让手机端可以远程触发排序
  2. 自动生成排序的完整帧序列和统计数据
  3. 支持 CORS 跨域请求（手机访问）
  4. 与 Notion PoW 系统集成，自动记账
  5. 支持内网穿透（ngrok）配置

安装与运行：
  pip install fastapi uvicorn python-dotenv pydantic
  python3 longhun_api_server.py

访问：
  本地：http://localhost:5000
  手机控制面板：http://localhost:5000/control
  API文档：http://localhost:5000/docs

内网穿透（让手机在外网访问）：
  1. 下载 ngrok: https://ngrok.com/download
  2. 运行: ngrok http 5000
  3. 复制给出的URL，在手机上访问
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
import json
from datetime import datetime
import os

# 导入算法帧生成器
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from longhun_notion_pow import log_sorting_work, hash_work

# ============================================================================
# L0 数据模型
# ============================================================================

class SortAlgoEnum(str, Enum):
    """支持的排序算法"""
    bubble = "冒泡排序"
    insertion = "插入排序"
    selection = "选择排序"
    quick = "快速排序"
    merge = "归并排序"
    shell = "希尔排序"


class SortRequest(BaseModel):
    """排序请求"""
    algorithm: SortAlgoEnum
    array_size: int = 100
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "algorithm": "快速排序",
                "array_size": 100,
                "description": "测试快速排序"
            }
        }


class SortResponse(BaseModel):
    """排序结果"""
    algorithm: str
    array_size: int
    comparisons: int
    swaps: int
    pow_hash: str
    local_id: str
    notion_page_id: Optional[str]
    timestamp: str


class StatusResponse(BaseModel):
    """服务器状态"""
    status: str
    version: str
    api_url: str
    control_panel_url: str


# ============================================================================
# L1 排序算法实现（简化版）
# ============================================================================

class SortAlgorithms:
    """排序算法库"""

    @staticmethod
    def bubble_sort(arr: List[int]) -> tuple:
        """冒泡排序"""
        arr = arr.copy()
        n = len(arr)
        cmp, swp = 0, 0

        for i in range(n):
            for j in range(n - i - 1):
                cmp += 1
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swp += 1

        return cmp, swp

    @staticmethod
    def insertion_sort(arr: List[int]) -> tuple:
        """插入排序"""
        arr = arr.copy()
        n = len(arr)
        cmp, swp = 0, 0

        for i in range(1, n):
            key = arr[i]
            j = i
            while j > 0:
                cmp += 1
                if arr[j - 1] > key:
                    arr[j] = arr[j - 1]
                    swp += 1
                    j -= 1
                else:
                    break
            arr[j] = key

        return cmp, swp

    @staticmethod
    def selection_sort(arr: List[int]) -> tuple:
        """选择排序"""
        arr = arr.copy()
        n = len(arr)
        cmp, swp = 0, 0

        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                cmp += 1
                if arr[j] < arr[min_idx]:
                    min_idx = j
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                swp += 1

        return cmp, swp

    @staticmethod
    def quick_sort(arr: List[int]) -> tuple:
        """快速排序"""
        cmp, swp = 0, 0
        arr = arr.copy()

        def partition(lo, hi):
            nonlocal cmp, swp
            pv = arr[hi]
            i = lo - 1
            for j in range(lo, hi):
                cmp += 1
                if arr[j] <= pv:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    swp += 1
            arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
            swp += 1
            return i + 1

        def qs(lo, hi):
            if lo < hi:
                p = partition(lo, hi)
                qs(lo, p - 1)
                qs(p + 1, hi)

        qs(0, len(arr) - 1)
        return cmp, swp

    @staticmethod
    def merge_sort(arr: List[int]) -> tuple:
        """归并排序"""
        cmp, swp = 0, 0
        arr = arr.copy()

        def merge(lo, mid, hi):
            nonlocal cmp, swp
            temp = []
            i, j = lo, mid + 1
            while i <= mid and j <= hi:
                cmp += 1
                if arr[i] <= arr[j]:
                    temp.append(arr[i])
                    i += 1
                else:
                    temp.append(arr[j])
                    j += 1
            temp.extend(arr[i:mid + 1])
            temp.extend(arr[j:hi + 1])
            for k, v in enumerate(temp):
                arr[lo + k] = v
                swp += 1

        def ms(lo, hi):
            if lo < hi:
                mid = (lo + hi) // 2
                ms(lo, mid)
                ms(mid + 1, hi)
                merge(lo, mid, hi)

        ms(0, len(arr) - 1)
        return cmp, swp

    @staticmethod
    def shell_sort(arr: List[int]) -> tuple:
        """希尔排序"""
        arr = arr.copy()
        n = len(arr)
        cmp, swp = 0, 0
        gap = n // 2

        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap:
                    cmp += 1
                    if arr[j - gap] > temp:
                        arr[j] = arr[j - gap]
                        swp += 1
                        j -= gap
                    else:
                        break
                arr[j] = temp
            gap //= 2

        return cmp, swp


# ============================================================================
# L2 FastAPI 应用
# ============================================================================

app = FastAPI(
    title="🐉 龍魂·远程排序API",
    description="远程触发排序算法，自动记账到Notion",
    version="1.0.0"
)

# CORS 中间件（允许手机跨域请求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# L3 API 端点
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """主页：跳转到控制面板"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>🐉 龍魂·远程排序</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #1a0f3a 0%, #2d1b50 100%);
                color: #e0e0e0;
                padding: 40px;
                margin: 0;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                text-align: center;
            }
            h1 {
                font-size: 48px;
                margin: 20px 0;
                color: #ffd700;
            }
            .link {
                display: inline-block;
                padding: 15px 30px;
                background: linear-gradient(135deg, #d4af37 0%, #ffd700 100%);
                color: #1a0f3a;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
                margin: 10px;
                transition: transform 0.3s;
            }
            .link:hover {
                transform: scale(1.05);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐉 龍魂·远程排序服务</h1>
            <p>UID9622 · 柬埔寨遥控印钞机</p>
            <div style="margin-top: 40px;">
                <a href="/control" class="link">📱 手机控制面板</a>
                <a href="/docs" class="link">📖 API文档</a>
            </div>
            <hr style="margin-top: 40px; border-color: #444;">
            <p style="font-size: 12px; color: #666;">
                DNA: #龍芯⚡️2026-05-27-API-SERVER-v1.0<br>
                本地运行: http://localhost:5000
            </p>
        </div>
    </body>
    </html>
    """


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """获取服务器状态"""
    return StatusResponse(
        status="🟢 运行中",
        version="1.0.0",
        api_url="http://localhost:5000",
        control_panel_url="http://localhost:5000/control"
    )


@app.post("/run_sort", response_model=SortResponse)
async def run_sort(request: SortRequest):
    """
    执行排序并自动记账

    参数：
        algorithm: 排序算法 (bubble, insertion, selection, quick, merge, shell)
        array_size: 数组大小 (10-1000)
        description: 描述（可选）

    返回：
        comparisons: 比较次数
        swaps: 交换次数
        pow_hash: 工作量证明哈希
        notion_page_id: Notion页面ID（若成功上传）
    """

    # 验证输入
    if request.array_size < 10 or request.array_size > 1000:
        raise HTTPException(status_code=400, detail="array_size 必须在 10-1000 之间")

    # 生成数组
    arr = list(range(1, request.array_size + 1))
    import random
    random.shuffle(arr)

    # 选择算法
    algo_map = {
        "冒泡排序": SortAlgorithms.bubble_sort,
        "插入排序": SortAlgorithms.insertion_sort,
        "选择排序": SortAlgorithms.selection_sort,
        "快速排序": SortAlgorithms.quick_sort,
        "归并排序": SortAlgorithms.merge_sort,
        "希尔排序": SortAlgorithms.shell_sort,
    }

    algo_func = algo_map.get(request.algorithm.value)
    if not algo_func:
        raise HTTPException(status_code=400, detail=f"未知算法: {request.algorithm}")

    # 执行排序
    comparisons, swaps = algo_func(arr)

    # 记账到Notion
    record = log_sorting_work(
        comparisons=comparisons,
        swaps=swaps,
        algorithm_name=request.algorithm.value,
        array_size=request.array_size
    )

    return SortResponse(
        algorithm=request.algorithm.value,
        array_size=request.array_size,
        comparisons=comparisons,
        swaps=swaps,
        pow_hash=record.pow_hash,
        local_id=record.local_id,
        notion_page_id=record.notion_page_id,
        timestamp=record.timestamp
    )


@app.get("/algorithms")
async def list_algorithms():
    """列出所有支持的算法"""
    return {
        "algorithms": [
            {
                "name": "冒泡排序",
                "code": "bubble",
                "complexity": "O(n²)",
                "emoji": "🫧"
            },
            {
                "name": "插入排序",
                "code": "insertion",
                "complexity": "O(n²)",
                "emoji": "🃏"
            },
            {
                "name": "选择排序",
                "code": "selection",
                "complexity": "O(n²)",
                "emoji": "🎯"
            },
            {
                "name": "快速排序",
                "code": "quick",
                "complexity": "O(n㏒n)",
                "emoji": "⚡️"
            },
            {
                "name": "归并排序",
                "code": "merge",
                "complexity": "O(n㏒n)",
                "emoji": "🔀"
            },
            {
                "name": "希尔排序",
                "code": "shell",
                "complexity": "O(n^1.3)",
                "emoji": "🐚"
            },
        ]
    }


@app.get("/control", response_class=HTMLResponse)
async def control_panel():
    """手机控制面板"""
    return get_mobile_panel_html()


# ============================================================================
# L4 HTML控制面板
# ============================================================================

def get_mobile_panel_html() -> str:
    """生成移动端控制面板"""
    return """
<!DOCTYPE html>
<html lang="zh-Hans">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐉 龍魂·远程排序·手机控制</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a0f3a 0%, #2d1b50 100%);
            color: #e0e0e0;
            padding: 16px;
            min-height: 100vh;
        }

        .container {
            max-width: 500px;
            margin: 0 auto;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 32px;
            color: #ffd700;
            margin: 10px 0;
        }

        .header p {
            color: #888;
            font-size: 12px;
        }

        .section {
            background: rgba(85, 55, 130, 0.4);
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 16px;
            backdrop-filter: blur(10px);
        }

        .section-title {
            color: #ffd700;
            font-weight: bold;
            margin-bottom: 12px;
            font-size: 14px;
        }

        .control-group {
            margin-bottom: 16px;
        }

        label {
            display: block;
            font-size: 12px;
            color: #999;
            margin-bottom: 6px;
        }

        select, input {
            width: 100%;
            padding: 10px;
            background: rgba(30, 20, 60, 0.6);
            border: 1px solid rgba(212, 175, 55, 0.4);
            border-radius: 8px;
            color: #e0e0e0;
            font-size: 14px;
        }

        select:focus, input:focus {
            outline: none;
            border-color: #ffd700;
            box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
        }

        .button-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 16px;
        }

        button {
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-primary {
            background: linear-gradient(135deg, #d4af37 0%, #ffd700 100%);
            color: #1a0f3a;
            grid-column: 1 / -1;
            font-size: 16px;
        }

        .btn-primary:active {
            transform: scale(0.98);
        }

        .btn-secondary {
            background: rgba(38, 128, 255, 0.3);
            color: #26aaff;
            border: 1px solid #26aaff;
        }

        .btn-secondary:active {
            background: rgba(38, 128, 255, 0.5);
        }

        .result {
            background: rgba(0, 255, 83, 0.1);
            border: 1px solid rgba(0, 255, 83, 0.3);
            border-radius: 8px;
            padding: 12px;
            margin-top: 12px;
            font-size: 12px;
            line-height: 1.6;
            display: none;
        }

        .result.show {
            display: block;
        }

        .result-item {
            display: flex;
            justify-content: space-between;
            margin: 4px 0;
        }

        .result-label {
            color: #999;
        }

        .result-value {
            color: #00ff53;
            font-family: monospace;
            word-break: break-all;
        }

        .loading {
            text-align: center;
            display: none;
        }

        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(212, 175, 55, 0.3);
            border-top: 3px solid #ffd700;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .status-badge {
            display: inline-block;
            background: #00ff53;
            color: #1a0f3a;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: bold;
            margin-top: 8px;
        }

        .status-badge.error {
            background: #ff4444;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div style="font-size: 48px;">🐉</div>
            <h1>龍魂·远程排序</h1>
            <p>UID9622 · 柬埔寨遥控印钞机</p>
        </div>

        <div class="section">
            <div class="section-title">⚙️ 排序设置</div>

            <div class="control-group">
                <label>选择算法</label>
                <select id="algorithm">
                    <option value="bubble">🫧 冒泡排序 - O(n²)</option>
                    <option value="insertion">🃏 插入排序 - O(n²)</option>
                    <option value="selection">🎯 选择排序 - O(n²)</option>
                    <option value="quick" selected>⚡️ 快速排序 - O(n㏒n)</option>
                    <option value="merge">🔀 归并排序 - O(n㏒n)</option>
                    <option value="shell">🐚 希尔排序 - O(n^1.3)</option>
                </select>
            </div>

            <div class="control-group">
                <label>数组大小: <span id="sizeDisplay">100</span></label>
                <input type="range" id="arraySize" min="10" max="500" value="100" step="10">
            </div>

            <div class="button-group">
                <button class="btn-primary" id="runBtn">▶️ 开始排序</button>
                <button class="btn-secondary" id="resetBtn">🔄 重置</button>
                <button class="btn-secondary" id="statusBtn">📊 查状态</button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 8px;">排序中...</p>
            </div>
        </div>

        <div class="section">
            <div class="section-title">📊 结果</div>
            <div class="result" id="result">
                <div class="result-item">
                    <span class="result-label">比较次数:</span>
                    <span class="result-value" id="resultComparisons">-</span>
                </div>
                <div class="result-item">
                    <span class="result-label">交换次数:</span>
                    <span class="result-value" id="resultSwaps">-</span>
                </div>
                <div class="result-item">
                    <span class="result-label">PoW哈希:</span>
                    <span class="result-value" id="resultHash">-</span>
                </div>
                <div class="result-item">
                    <span class="result-label">本地ID:</span>
                    <span class="result-value" id="resultLocalId">-</span>
                </div>
                <div class="result-item">
                    <span class="result-label">Notion页:</span>
                    <span class="result-value" id="resultNotionId">-</span>
                </div>
                <div id="statusBadge"></div>
            </div>
        </div>

        <div style="text-align: center; margin-top: 40px; color: #666; font-size: 11px;">
            <p>DNA: #龍芯⚡️2026-05-27-API-SERVER-v1.0</p>
            <p>責任: UID9622·龍芯北辰</p>
        </div>
    </div>

    <script>
        const API_BASE = window.location.origin;
        const algorithmSelect = document.getElementById('algorithm');
        const arraySizeInput = document.getElementById('arraySize');
        const sizeDisplay = document.getElementById('sizeDisplay');
        const runBtn = document.getElementById('runBtn');
        const resetBtn = document.getElementById('resetBtn');
        const statusBtn = document.getElementById('statusBtn');
        const loading = document.getElementById('loading');
        const resultDiv = document.getElementById('result');
        const statusBadge = document.getElementById('statusBadge');

        // 同步数组大小显示
        arraySizeInput.addEventListener('input', () => {
            sizeDisplay.textContent = arraySizeInput.value;
        });

        // 开始排序
        runBtn.addEventListener('click', async () => {
            const algorithm = algorithmSelect.value;
            const arraySize = parseInt(arraySizeInput.value);

            runBtn.disabled = true;
            loading.style.display = 'block';
            resultDiv.classList.remove('show');

            try {
                const response = await fetch(`${API_BASE}/run_sort`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        algorithm: algorithm,
                        array_size: arraySize
                    })
                });

                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();

                // 显示结果
                document.getElementById('resultComparisons').textContent = data.comparisons;
                document.getElementById('resultSwaps').textContent = data.swaps;
                document.getElementById('resultHash').textContent = data.pow_hash.substring(0, 16) + '...';
                document.getElementById('resultLocalId').textContent = data.local_id;
                document.getElementById('resultNotionId').textContent = data.notion_page_id || '(待同步)';

                resultDiv.classList.add('show');
                statusBadge.innerHTML = '<div class="status-badge">✅ 排序完成·已记账</div>';

            } catch (error) {
                alert(`错误: ${error.message}`);
                statusBadge.innerHTML = `<div class="status-badge error">❌ ${error.message}</div>`;
            } finally {
                runBtn.disabled = false;
                loading.style.display = 'none';
            }
        });

        // 重置
        resetBtn.addEventListener('click', () => {
            arraySizeInput.value = 100;
            sizeDisplay.textContent = '100';
            algorithmSelect.value = 'quick';
            resultDiv.classList.remove('show');
            statusBadge.innerHTML = '';
        });

        // 查状态
        statusBtn.addEventListener('click', async () => {
            try {
                const response = await fetch(`${API_BASE}/status`);
                const data = await response.json();
                alert(`✅ 服务运行中\\n版本: ${data.version}\\n状态: ${data.status}`);
            } catch (error) {
                alert(`❌ 无法连接服务: ${error.message}`);
            }
        });
    </script>
</body>
</html>
    """


# ============================================================================
# L5 启动脚本
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    print("""
╔════════════════════════════════════════════════════════════════╗
║  🐉 龍魂·FastAPI 远程排序服务器                               ║
║  Dragon Soul Remote Control Server v1.0                       ║
║                                                                ║
║  UID9622 · 裸跑解压专用 · 柬埔寨遥控印钞机                 ║
║                                                                ║
║  DNA: #龍芯⚡️2026-05-27-API-SERVER-v1.0                    ║
╚════════════════════════════════════════════════════════════════╝

📍 本地访问:
   🌐 http://localhost:5000
   📱 手机控制: http://localhost:5000/control
   📖 API文档: http://localhost:5000/docs

🌍 外网访问 (用 ngrok):
   1. pip install ngrok
   2. ngrok http 5000
   3. 复制生成的URL在手机上访问

⌨️  快捷键:
   Ctrl+C     停止服务
   Ctrl+D     退出

🚀 启动中...
    """)

    # 从环境变量读取配置
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "5000"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"

    uvicorn.run(
        "longhun_api_server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
