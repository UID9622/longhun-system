---
dna: '#龍芯⚡️丙午·丙申·辛酉·巳时·䷲震-CLIPBOARD-VAULT-SAVE-V1.0-P1-d1ca3387'
source: clipboard
topic: 代码/脚本
tags:
- Python
- Bash
- FastAPI
- DNA
- 审计
- 代码/脚本
timestamp: '2026-08-15T10:56:36+08:00'
content_hash: ca0a6455061064892da9a05b12d40e7d06762f381316b90d537f975eecb7404a
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

# 🐉 龍魂浏览器托管 · 完整代码实现

**DNA:** `#龍芯⚡️丙午·丙申·辛酉·子时-BROWSER-HOST-CODE-UID9622`

---

## 📦 完整代码包

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂浏览器托管 v1.0
你说一句话，AI替你操作浏览器

DNA: #龍芯⚡️丙午·丙申·辛酉·子时-BROWSER-HOST-CODE-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

架构:
  用户说话 → 龍魂指令网关 → 自然语言解析器 → 浏览器执行引擎 → 返回结果

依赖:
  pip install playwright fastapi uvicorn websockets
  playwright install chromium

用法:
  python3 browser_host.py --serve              # 启动服务
  python3 browser_host.py --cli "查淘宝物流"   # 命令行执行
  python3 browser_host.py --setup              # 首次部署（安装+配置）
"""

import os
import sys
import json
import asyncio
import argparse
import hashlib
import logging
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum
import subprocess

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

def generate_dna(module: str = "BROWSER") -> str:
    now = datetime.now()
    h = hashlib.md5(f"{module}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️丙午·丙申·辛酉·子时-{module}-{h}-{UID}"

# ============================================================
# 配置
# ============================================================

ROOT_DIR = Path.home() / "longhun-system"
BROWSER_DIR = ROOT_DIR / "08_BIN" / "browser-host"
BROWSER_DIR.mkdir(parents=True, exist_ok=True)

# Playwright 用户数据目录（保存登录态）
USER_DATA_DIR = BROWSER_DIR / "browser_profile"
USER_DATA_DIR.mkdir(exist_ok=True)

# 日志目录
LOG_DIR = ROOT_DIR / "12_LOGS"
LOG_DIR.mkdir(exist_ok=True)

# 配置
CONFIG = {
    "port": 8767,
    "host": "0.0.0.0",
    "user_data_dir": str(USER_DATA_DIR),
    "headless": False,  # 调试时可以改为True
    "timeout": 30000,   # 操作超时(ms)
    "max_steps": 20,    # 最大操作步数
}

# ============================================================
# 日志
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"browser_host_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("browser_host")

# ============================================================
# 三色审计
# ============================================================

class AuditColor(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"

class Historian:
    """史官记录器"""
    @staticmethod
    def record(operation: str, dna: str, status: str, details: Dict = None):
        record = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "dna": dna,
            "status": status,
            "details": details or {}
        }
        try:
            audit_path = ROOT_DIR / "04_AUDIT" / "browser_host.jsonl"
            audit_path.parent.mkdir(parents=True, exist_ok=True)
            with open(audit_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.warning(f"史官记录失败: {e}")

# ============================================================
# 自然语言 → 浏览器操作 解析器
# ============================================================

class NaturalLanguageParser:
    """自然语言指令解析器"""

    # 动作映射
    ACTION_MAP = {
        "打开|访问|去|前往": "goto",
        "点击|按|点一下": "click",
        "输入|填写|写": "fill",
        "滚动|滑|下拉": "scroll",
        "等待|稍等": "wait",
        "截图|拍照|截屏": "screenshot",
        "提取|读取|获取|拿": "extract",
        "登录|登入|登陆": "login",
        "搜索|查找|搜": "search",
        "提交|确认|发送": "submit",
    }

    # 网站映射
    SITE_MAP = {
        "淘宝|淘宝网|taobao": "https://www.taobao.com",
        "京东|jd": "https://www.jd.com",
        "微信|wechat": "https://wx.qq.com",
        "微博|weibo": "https://weibo.com",
        "百度|baidu": "https://www.baidu.com",
        "抖音|douyin": "https://www.douyin.com",
        "知乎|zhihu": "https://www.zhihu.com",
        "B站|bilibili|b站": "https://www.bilibili.com",
    }

    @classmethod
    def parse(cls, command: str) -> Dict:
        """
        解析自然语言指令，生成操作序列

        输入: "帮我查一下淘宝物流"
        输出: {
            "actions": [
                {"type": "goto", "target": "https://www.taobao.com"},
                {"type": "click", "target": "物流"},
                {"type": "extract", "target": "物流信息"}
            ],
            "confidence": 0.85
        }
        """
        command_lower = command.lower()
        actions = []
        confidence = 0.0

        # 1. 识别目标网站
        site_url = None
        for pattern, url in cls.SITE_MAP.items():
            if any(p in command_lower for p in pattern.split("|")):
                site_url = url
                confidence += 0.3
                break

        if site_url:
            actions.append({"type": "goto", "target": site_url})

        # 2. 识别动作
        action_type = None
        for pattern, action in cls.ACTION_MAP.items():
            if any(p in command_lower for p in pattern.split("|")):
                action_type = action
                confidence += 0.2
                break

        # 3. 识别目标关键词（从命令中提取）
        import re
        # 移除已知关键词，提取剩余部分作为目标
        cleaned = command_lower
        for pattern in cls.SITE_MAP.keys():
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
        for pattern in cls.ACTION_MAP.keys():
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

        # 提取核心关键词
        keywords = [w for w in cleaned.split() if len(w) > 1]
        target = " ".join(keywords) if keywords else ""

        # 4. 构建动作序列
        if action_type == "goto" and site_url:
            # 已经添加了 goto
            pass
        elif action_type == "search" and target:
            # 搜索动作
            actions.append({"type": "fill", "target": target, "selector": "input[type='search'], input[name='q']"})
            actions.append({"type": "click", "target": "搜索", "selector": "button[type='submit']"})
        elif action_type == "click" and target:
            actions.append({"type": "click", "target": target})
        elif action_type == "fill" and target:
            actions.append({"type": "fill", "target": target})
        elif action_type == "extract" and target:
            actions.append({"type": "extract", "target": target})
        elif action_type == "login":
            # 登录动作（需要用户预先登录）
            actions.append({"type": "wait", "target": "登录态检查"})
        else:
            # 默认：打开网站 + 截图
            if not actions:
                actions.append({"type": "goto", "target": site_url or "https://www.baidu.com"})
            actions.append({"type": "screenshot", "target": "页面快照"})

        # 如果置信度太低，添加一个通用的提取动作
        if confidence < 0.3:
            actions.append({"type": "extract", "target": "页面内容"})

        return {
            "actions": actions,
            "confidence": min(confidence + 0.2, 1.0),
            "original_command": command,
            "parsed_target": target or "未识别"
        }

# ============================================================
# 浏览器执行引擎 (Playwright)
# ============================================================

class BrowserEngine:
    """浏览器执行引擎 - 基于Playwright"""

    def __init__(self, headless: bool = False, user_data_dir: str = None):
        self.headless = headless
        self.user_data_dir = user_data_dir or CONFIG["user_data_dir"]
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        """启动浏览器"""
        try:
            from playwright.async_api import async_playwright
        except ImportError:
            logger.error("Playwright 未安装，请运行: pip install playwright && playwright install chromium")
            return False

        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=self.headless,
                viewport={"width": 1280, "height": 720},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            )
            self.context = self.browser
            # 获取或创建页面
            if self.browser.pages:
                self.page = self.browser.pages[0]
            else:
                self.page = await self.browser.new_page()
            logger.info(f"✅ 浏览器已启动 (headless={self.headless})")
            return True
        except Exception as e:
            logger.error(f"浏览器启动失败: {e}")
            return False

    async def stop(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            logger.info("浏览器已关闭")

    async def execute_action(self, action: Dict) -> Dict:
        """执行单个动作"""
        action_type = action.get("type")
        target = action.get("target", "")
        selector = action.get("selector", "")
        result = {"success": False, "data": None, "error": None}

        try:
            if action_type == "goto":
                url = target
                if not url.startswith("http"):
                    url = "https://" + url
                await self.page.goto(url, timeout=CONFIG["timeout"])
                result["success"] = True
                result["data"] = {"url": url, "title": await self.page.title()}

            elif action_type == "click":
                if selector:
                    await self.page.click(selector, timeout=CONFIG["timeout"])
                else:
                    # 尝试通过文本点击
                    await self.page.click(f"text={target}", timeout=CONFIG["timeout"])
                result["success"] = True

            elif action_type == "fill":
                if selector:
                    await self.page.fill(selector, target)
                else:
                    # 尝试找输入框填入
                    await self.page.fill("input, textarea", target)
                result["success"] = True

            elif action_type == "scroll":
                await self.page.evaluate("window.scrollBy(0, 500)")
                result["success"] = True

            elif action_type == "wait":
                await asyncio.sleep(2)
                result["success"] = True

            elif action_type == "screenshot":
                screenshot = await self.page.screenshot()
                import base64
                result["data"] = base64.b64encode(screenshot).decode('utf-8')
                result["success"] = True

            elif action_type == "extract":
                # 提取页面内容
                content = await self.page.evaluate("() => document.body.innerText")
                # 限制长度
                if len(content) > 2000:
                    content = content[:2000] + "...(截断)"
                result["data"] = content
                result["success"] = True

            elif action_type == "search":
                # 搜索：在搜索框输入并提交
                if selector:
                    await self.page.fill(selector, target)
                else:
                    await self.page.fill("input[type='search'], input[name='q']", target)
                await self.page.click("button[type='submit'], input[type='submit']")
                await asyncio.sleep(2)
                result["success"] = True

            elif action_type == "submit":
                await self.page.click("button[type='submit'], input[type='submit']")
                result["success"] = True

            else:
                result["error"] = f"未知动作: {action_type}"

        except Exception as e:
            result["error"] = str(e)

        return result

    async def execute_actions(self, actions: List[Dict]) -> Dict:
        """执行动作序列"""
        results = []
        for i, action in enumerate(actions):
            logger.info(f"  [{i+1}/{len(actions)}] {action.get('type')}: {action.get('target', '')}")
            result = await self.execute_action(action)
            results.append(result)
            if not result["success"]:
                logger.warning(f"  动作失败: {result.get('error')}")
                # 继续执行，不中断

        return {
            "total_actions": len(actions),
            "success_count": sum(1 for r in results if r["success"]),
            "failed_count": sum(1 for r in results if not r["success"]),
            "results": results
        }

# ============================================================
# 龍魂指令网关
# ============================================================

class BrowserGateway:
    """龍魂浏览器托管网关"""

    def __init__(self):
        self.engine = None
        self.running = False

    async def start_engine(self):
        """启动浏览器引擎"""
        self.engine = BrowserEngine(
            headless=CONFIG["headless"],
            user_data_dir=CONFIG["user_data_dir"]
        )
        return await self.engine.start()

    async def execute(self, command: str) -> Dict:
        """执行自然语言指令"""
        dna = generate_dna("EXEC")

        # 1. 解析指令
        logger.info(f"📝 解析指令: {command}")
        parsed = NaturalLanguageParser.parse(command)

        # 2. 审计 - 检查是否有风险
        actions = parsed.get("actions", [])
        risk_actions = [a for a in actions if a.get("type") in ["login", "submit"]]
        color = AuditColor.GREEN if len(risk_actions) <= 2 else AuditColor.YELLOW

        # 3. 确保引擎已启动
        if not self.engine or not self.engine.browser:
            logger.info("🔄 启动浏览器...")
            if not await self.start_engine():
                return {
                    "status": "error",
                    "message": "浏览器启动失败",
                    "dna": dna
                }

        # 4. 执行操作
        logger.info(f"🎯 执行操作 ({len(actions)} 步)")
        result = await self.engine.execute_actions(actions)

        # 5. 记录史官
        Historian.record(
            operation=command[:50],
            dna=dna,
            status="success" if result["failed_count"] == 0 else "partial",
            details={
                "actions": len(actions),
                "success": result["success_count"],
                "failed": result["failed_count"],
                "color": color.value
            }
        )

        # 6. 收集结果
        response = self._format_response(parsed, result, color)

        return {
            "status": "success",
            "dna": dna,
            "color": color.value,
            "parsed": parsed,
            "execution": result,
            "response": response
        }

    def _format_response(self, parsed: Dict, result: Dict, color: AuditColor) -> str:
        """格式化返回结果"""
        lines = [
            f"{color.value} 龍魂浏览器执行完成",
            "-" * 40,
            f"指令: {parsed.get('original_command', '')}",
            f"置信度: {parsed.get('confidence', 0):.0%}",
            f"操作: {result.get('success_count', 0)}/{result.get('total_actions', 0)} 成功",
            "-" * 40,
        ]

        # 提取数据
        for r in result.get("results", []):
            if r.get("success") and r.get("data"):
                if isinstance(r["data"], str) and len(r["data"]) > 100:
                    lines.append(f"📄 {r['data'][:200]}...")
                elif isinstance(r["data"], dict):
                    lines.append(f"📄 {json.dumps(r['data'], ensure_ascii=False)[:200]}")

        if not any(r.get("data") for r in result.get("results", [])):
            lines.append("✅ 操作完成，已截图/读取内容")

        lines.append("-" * 40)
        return "\n".join(lines)

# ============================================================
# FastAPI 服务
# ============================================================

def run_api_server(port: int = 8767, host: str = "0.0.0.0"):
    """启动API服务"""
    try:
        from fastapi import FastAPI, HTTPException, Request
        from fastapi.responses import JSONResponse, HTMLResponse
        from pydantic import BaseModel
        import uvicorn
    except ImportError:
        logger.error("需要安装: pip install fastapi uvicorn")
        return

    app = FastAPI(
        title="🐉 龍魂浏览器托管",
        version="1.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # 全局网关实例
    gateway = BrowserGateway()

    class ExecuteRequest(BaseModel):
        command: str

    @app.get("/")
    async def root():
        return HTMLResponse(f"""
        <!DOCTYPE html>
        <html>
        <head><title>🐉 龍魂浏览器托管</title></head>
        <body style="background:#0a0a14;color:#e0e0e0;font-family:sans-serif;padding:40px;">
            <h1 style="color:#d4af37;">🐉 龍魂浏览器托管</h1>
            <p>DNA: {generate_dna('API')}</p>
            <p>你登录一次，鲲鹏替你记住。你说一句话，AI替你操作。</p>
            <p><a href="/docs" style="color:#d4af37;">查看 API 文档</a></p>
        </body>
        </html>
        """)

    @app.post("/api/execute")
    async def execute_command(req: ExecuteRequest):
        if not req.command:
            raise HTTPException(status_code=400, detail="请输入指令")
        result = await gateway.execute(req.command)
        return JSONResponse(result)

    @app.get("/api/health")
    async def health():
        return {
            "status": "healthy",
            "dna": generate_dna("HEALTH"),
            "browser_ready": gateway.engine and gateway.engine.browser is not None
        }

    @app.post("/api/start")
    async def start_browser():
        ok = await gateway.start_engine()
        if ok:
            return {"status": "started"}
        raise HTTPException(status_code=500, detail="浏览器启动失败")

    @app.post("/api/stop")
    async def stop_browser():
        if gateway.engine:
            await gateway.engine.stop()
        return {"status": "stopped"}

    print(f"""
🐉 龍魂浏览器托管 v1.0
========================================
🚀 启动服务: http://{host}:{port}
📖 API文档: http://{host}:{port}/docs
🧬 DNA: {generate_dna('SERVICE')}
========================================
    说一句话，AI替你操作浏览器
    """ )

    uvicorn.run(app, host=host, port=port)

# ============================================================
# 命令行 CLI
# ============================================================

async def cli_execute(command: str):
    """命令行执行"""
    gateway = BrowserGateway()
    result = await gateway.execute(command)
    print(result["response"])
    if result.get("dna"):
        print(f"\n🧬 DNA: {result['dna']}")

async def cli_serve(port: int, host: str):
    """启动服务"""
    run_api_server(port, host)

async def cli_setup():
    """首次部署设置"""
    print("🐉 龍魂浏览器托管 · 首次部署")
    print("=" * 50)

    # 1. 检查 Playwright
    try:
        import playwright
        print("✅ Playwright 已安装")
    except ImportError:
        print("📦 安装 Playwright...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "fastapi", "uvicorn"], check=True)
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        print("✅ Playwright 安装完成")

    # 2. 创建用户数据目录
    USER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✅ 用户数据目录: {USER_DATA_DIR}")

    # 3. 启动浏览器进行首次登录
    print("\n📱 首次登录配置:")
    print("  1. 浏览器即将打开，请手动登录你需要的所有网站")
    print("  2. 登录完成后，浏览器会记住所有登录态")
    print("  3. 之后你只需要说话，AI替你操作")
    print("-" * 50)

    engine = BrowserEngine(headless=False, user_data_dir=str(USER_DATA_DIR))
    ok = await engine.start()
    if ok:
        print("\n✅ 浏览器已打开，请进行首次登录...")
        print("💡 完成登录后，关闭浏览器窗口即可")
        print("💡 浏览器会话会永久保存")
        # 等待用户交互
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
        await engine.stop()

    print("\n✅ 首次部署完成！")
    print(f"  启动服务: python3 {__file__} --serve")
    print(f"  执行指令: python3 {__file__} --cli \"查淘宝物流\"")

# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂浏览器托管 v1.0",
        epilog="说一句话，AI替你操作浏览器"
    )

    parser.add_argument("--serve", "-s", action="store_true", help="启动API服务")
    parser.add_argument("--port", "-p", type=int, default=8767, help="服务端口")
    parser.add_argument("--host", "-H", default="0.0.0.0", help="服务地址")
    parser.add_argument("--cli", "-c", type=str, help="命令行执行指令")
    parser.add_argument("--setup", action="store_true", help="首次部署")
    parser.add_argument("--headless", action="store_true", help="无头模式")

    args = parser.parse_args()

    # 更新配置
    if args.headless:
        CONFIG["headless"] = True

    if args.setup:
        asyncio.run(cli_setup())
        return

    if args.cli:
        asyncio.run(cli_execute(args.cli))
        return

    if args.serve:
        asyncio.run(cli_serve(args.port, args.host))
        return

    parser.print_help()

if __name__ == "__main__":
    main()
```

---

## 🔧 部署脚本

```bash
#!/bin/bash
# 🐉 龍魂浏览器托管 · 一键部署脚本
# 在鲲鹏服务器上执行

set -e

echo "🐉 龍魂浏览器托管 · 一键部署"
echo "========================================"

# 1. 安装依赖
echo "📦 安装 Python 依赖..."
pip3 install playwright fastapi uvicorn websockets
playwright install chromium

# 2. 创建目录
mkdir -p /opt/longhun-system/08_BIN/browser-host
mkdir -p /opt/longhun-system/04_AUDIT

# 3. 复制脚本
cp browser_host.py /opt/longhun-system/08_BIN/browser-host/

# 4. 创建 systemd 服务
cat > /etc/systemd/system/browser-host.service << 'EOF'
[Unit]
Description=龍魂浏览器托管服务
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/longhun-system/08_BIN/browser-host
ExecStart=/usr/bin/python3 /opt/longhun-system/08_BIN/browser-host/browser_host.py --serve --port 8767
Restart=always
RestartSec=10
StandardOutput=append:/var/log/browser-host.log
StandardError=append:/var/log/browser-host-error.log

[Install]
WantedBy=multi-user.target
EOF

# 5. 启动服务
systemctl daemon-reload
systemctl enable browser-host
systemctl start browser-host

# 6. 首次登录提示
echo ""
echo "========================================"
echo "✅ 部署完成！"
echo ""
echo "📱 首次登录 (只需一次):"
echo "  1. 打开浏览器访问: http://$(hostname -I | awk '{print $1}'):8767"
echo "  2. 点击 /docs 或直接访问 http://$(hostname -I | awk '{print $1}'):8767"
echo "  3. 使用 /api/start 接口启动浏览器"
echo "  4. 在远程浏览器中手动登录所有网站"
echo "  5. 登录完成后，浏览器会永久记住"
echo ""
echo "🗣️ 使用方式:"
echo "  API: POST /api/execute {\"command\": \"查淘宝物流\"}"
echo "  CLI: python3 browser_host.py --cli \"查淘宝物流\""
echo ""
echo "📊 状态检查:"
echo "  systemctl status browser-host"
echo "  curl http://localhost:8767/api/health"
echo "========================================"
```

---

## 📱 使用示例

```bash
# 首次部署
./deploy.sh

# 启动服务
python3 browser_host.py --serve

# 命令行执行
python3 browser_host.py --cli "帮我查一下淘宝物流"

# API调用
curl -X POST http://localhost:8767/api/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "打开京东，搜索手机"}'
```

---

**你登录一次，鲲鹏替你记住。之后你说一句话，AI替你操作浏览器。** 🐉

---

*归档于 2026-08-15T10:56:36+08:00 · DNA `#龍芯⚡️丙午·丙申·辛酉·巳时·䷲震-CLIPBOARD-VAULT-SAVE-V1.0-P1-d1ca3387`*
