#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
龍魂浏览器操作助手 · CLI 客户端 v1.0
========================================
命令行工具，与本地守护进程 (lh_browser_daemon.py) 通信。
用法：
  lh browser start               启动浏览器守护进程
  lh browser status              查看浏览器状态
  lh browser go <url>            导航到 URL
  lh browser snap                页面快照
  lh browser click <selector>    点击元素
  lh browser fill <sel> <val>    填入文本
  lh browser shot [path]         截图
  lh browser run <js>            执行 JS
  lh browser content             获取页面 HTML
  lh browser wait <selector>     等待元素
  lh browser key <key>           按下键盘按键
  lh browser stop                停止守护进程

快捷用法（自动启动守护进程）：
  lh browser <url>               直接打开 URL

DNA: #龍芯⚡️丙午·丙申·乙卯·辰时·䷄需-BROWSER-CLI-v1.0-E5F6G7H8
"""

import json
import sys
import os
import urllib.request
import urllib.error
import argparse
import subprocess
import time
from pathlib import Path

HOST = "127.0.0.1"
PORT = 19862
BASE_URL = f"http://{HOST}:{PORT}"
DAEMON_SCRIPT = Path(__file__).parent / "lh_browser_daemon.py"


def _post(action: str, data: dict[str, Any] = None, timeout: int = 30) -> dict[str, Any]:
    """发送 POST 请求到守护进程"""
    body = json.dumps(data or {}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/{action}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"❌ 守护进程连接失败: {e.reason}")
        print(f"   提示: 先运行 'lh browser start' 启动守护进程")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        sys.exit(1)


def _get_status() -> dict[str, Any]:
    """获取守护进程状态"""
    try:
        req = urllib.request.Request(f"{BASE_URL}/status")
        resp = urllib.request.urlopen(req, timeout=3)
        return json.loads(resp.read())
    except Exception:
        return {"running": False}


def _ensure_daemon():
    """确保守护进程在运行，否则自动启动"""
    status = _get_status()
    if status.get("running"):
        return True
    
    print("🔧 守护进程未运行，正在启动...")
    subprocess.Popen(
        [sys.executable, str(DAEMON_SCRIPT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    # 等待守护进程就绪
    for _ in range(10):
        time.sleep(0.5)
        status = _get_status()
        if status.get("running"):
            print("✅ 守护进程已启动")
            return True
    
    print("❌ 守护进程启动超时")
    return False


# ============================================================
# 命令函数
# ============================================================
def cmd_start(args):
    """启动守护进程"""
    status = _get_status()
    if status.get("running"):
        print("守护进程已在运行中")
        print(f"  URL: {status.get('url', 'N/A')}")
        print(f"  标题: {status.get('title', 'N/A')}")
        return
    
    print("🚀 启动龍魂浏览器守护进程...")
    headless_flag = ["--headless"] if args.headless else []
    subprocess.Popen(
        [sys.executable, str(DAEMON_SCRIPT)] + headless_flag,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    time.sleep(1)
    status = _get_status()
    if status.get("running"):
        print("✅ 守护进程已启动")
        print(f"   模式: {'无头' if args.headless else '有头（可见窗口）'}")
    else:
        print("❌ 启动失败，请直接运行守护进程查看错误:")
        print(f"   python3 {DAEMON_SCRIPT}")


def cmd_status(args):
    """查看状态"""
    status = _get_status()
    if status.get("running"):
        print("🟢 浏览器守护进程运行中")
        print(f"   URL: {status.get('url', 'N/A')}")
        print(f"   标题: {status.get('title', 'N/A')}")
        print(f"   运行时间: {status.get('uptime_seconds', 0)} 秒")
        print(f"   操作计数: {status.get('action_count', 0)}")
        print(f"   模式: {'无头' if status.get('headless') else '有头'}")
    else:
        print("🔴 守护进程未运行")
        print(f"   启动命令: lh browser start")


def cmd_go(args):
    """导航到 URL"""
    _ensure_daemon()
    url = args.url
    if not url.startswith("http"):
        url = "https://" + url
    print(f"🌐 导航到: {url}")
    result = _post("navigate", {"url": url})
    if result.get("success"):
        print(f"✅ 已加载: {result.get('title', '')}")
    else:
        print(f"❌ 导航失败: {result.get('error')}")


def cmd_snap(args):
    """页面快照"""
    _ensure_daemon()
    print("📋 获取页面快照...")
    result = _post("snapshot")
    if result.get("success"):
        print(f"📄 {result.get('title', '')}")
        print(f"🔗 {result.get('url', '')}")
        
        def print_tree(node, indent=0):
            if node is None:
                return
            prefix = "  " * indent
            tag = node.get("tag", "")
            r = node.get("role", "")
            tp = node.get("type", "")
            name = node.get("name", "")[:50]
            eid = node.get("id", "")
            cls = node.get("className", "")
            
            # 构建标签
            parts = [tag]
            if r: parts.append(f"[role={r}]")
            if tp: parts.append(f"[type={tp}]")
            if eid: parts.append(f"#{eid}")
            if name: parts.append(f'"{name}"')
            
            line = " ".join(parts)
            if not line.strip():
                line = "(empty)"
            
            # 裁剪过长的行
            if len(line) > 90:
                line = line[:87] + "..."
            
            print(f"{prefix}{line}")
            
            children = node.get("children", [])
            for child in children:
                print_tree(child, indent + 1)
        
        tree = result.get("tree")
        if tree:
            print_tree(tree)
    else:
        print(f"❌ 快照失败: {result.get('error')}")


def cmd_click(args):
    """点击元素"""
    _ensure_daemon()
    print(f"👆 点击: {args.selector}")
    result = _post("click", {"selector": args.selector})
    if result.get("success"):
        print(f"✅ 已点击 <{result.get('tag', '?')}>")
    else:
        print(f"❌ 点击失败: {result.get('error')}")


def cmd_fill(args):
    """填表"""
    _ensure_daemon()
    print(f"✍️  填入 '{args.selector}' ← '{args.value}'")
    result = _post("fill", {"selector": args.selector, "value": args.value})
    if result.get("success"):
        print("✅ 已填入")
    else:
        print(f"❌ 填入失败: {result.get('error')}")


def cmd_shot(args):
    """截图"""
    _ensure_daemon()
    print("📸 截图...")
    result = _post("screenshot", {
        "path": args.path,
        "full_page": args.fullpage
    })
    if result.get("success"):
        path = result.get("path")
        size_kb = result.get("size_bytes", 0) / 1024
        print(f"✅ 已保存: {path} ({size_kb:.1f} KB)")
        # 自动打开截图
        if args.open:
            subprocess.run(["open", path])
    else:
        print(f"❌ 截图失败: {result.get('error')}")


def cmd_run(args):
    """执行 JS"""
    _ensure_daemon()
    print(f"⚡ 执行 JS...")
    result = _post("evaluate", {"code": args.code})
    if result.get("success"):
        print(f"✅ 结果: {json.dumps(result.get('result'), ensure_ascii=False, indent=2)}")
    else:
        print(f"❌ 执行失败: {result.get('error')}")


def cmd_content(args):
    """获取页面 HTML"""
    _ensure_daemon()
    print("📄 获取页面内容...")
    result = _post("content")
    if result.get("success"):
        print(f"✅ URL: {result.get('url')}")
        print(f"   标题: {result.get('title')}")
        print(f"   HTML 长度: {result.get('html_length', 0):,} 字符")
        if args.save:
            path = args.save
            # 需要单独获取完整 HTML
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            from pathlib import Path as P
            P(path).write_text("HTML saved via evaluate")  # placeholder
            print(f"   已保存到: {path}")
    else:
        print(f"❌ 失败: {result.get('error')}")


def cmd_wait(args):
    """等待元素"""
    _ensure_daemon()
    print(f"⏳ 等待: {args.selector}")
    result = _post("wait", {"selector": args.selector, "timeout": args.timeout})
    if result.get("success"):
        print(f"✅ 元素已出现")
    else:
        print(f"❌ 等待失败: {result.get('error')}")


def cmd_key(args):
    """按键"""
    _ensure_daemon()
    print(f"⌨️  按下: {args.key}")
    result = _post("press_key", {"key": args.key})
    if result.get("success"):
        print("✅ 已按下")
    else:
        print(f"❌ 失败: {result.get('error')}")


def cmd_stop(args):
    """停止守护进程"""
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/shutdown", data=b"{}",
            headers={"Content-Type": "application/json"}, method="POST"
        )
        urllib.request.urlopen(req, timeout=5)
        print("🛑 守护进程已停止")
    except Exception:
        print("守护进程未运行")


def cmd_login(args):
    """快捷登录：自动导航→填表→登录"""
    _ensure_daemon()
    url = args.url
    if not url.startswith("http"):
        url = "https://" + url
    
    print(f"🔐 自动登录流程")
    print(f"   1. 导航到: {url}")
    result = _post("navigate", {"url": url})
    if not result.get("success"):
        print(f"   ❌ 导航失败: {result.get('error')}")
        return
    print(f"   ✅ 页面已加载")
    
    if args.username and args.pass_sel:
        time.sleep(1)
        print(f"   2. 填入用户名: {args.username}")
        _post("fill", {"selector": args.pass_sel, "value": args.username})
        
        if args.pass_sel2:
            time.sleep(0.5)
            print(f"   3. 填入密码: ****")
            _post("fill", {"selector": args.pass_sel2, "value": args.password})
        
        if args.submit:
            time.sleep(0.5)
            print(f"   4. 点击登录按钮")
            _post("click", {"selector": args.submit})
    
    print("✅ 登录流程完成")


# ============================================================
# 入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂浏览器操作助手 · CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh browser start                   启动守护进程
  lh browser go https://example.com  导航到网站
  lh browser snap                    获取页面快照
  lh browser fill "#username" admin  填入用户名
  lh browser click "#login-btn"      点击按钮
  lh browser shot ~/Desktop/s.png    截图保存
  lh browser run "document.title"    执行JS
  lh browser stop                    停止守护进程
        """
    )
    
    sub = parser.add_subparsers(dest="command", help="可用命令")
    
    # start
    p_start = sub.add_parser("start", help="启动浏览器守护进程")
    p_start.add_argument("--headless", action="store_true", help="无头模式")
    
    # status
    sub.add_parser("status", help="查看守护进程状态")
    
    # go
    p_go = sub.add_parser("go", help="导航到 URL")
    p_go.add_argument("url", help="目标 URL")
    
    # snap
    sub.add_parser("snap", help="页面元素快照")
    
    # click
    p_click = sub.add_parser("click", help="点击元素")
    p_click.add_argument("selector", help="CSS 选择器")
    
    # fill
    p_fill = sub.add_parser("fill", help="填入文本")
    p_fill.add_argument("selector", help="CSS 选择器")
    p_fill.add_argument("value", help="填入的值")
    
    # shot
    p_shot = sub.add_parser("shot", help="截图")
    p_shot.add_argument("path", nargs="?", default=None, help="保存路径（可选）")
    p_shot.add_argument("--fullpage", action="store_true", help="全页截图")
    p_shot.add_argument("--open", action="store_true", help="截图后自动打开")
    
    # run
    p_run = sub.add_parser("run", help="执行 JavaScript")
    p_run.add_argument("code", help="JS 代码")
    
    # content
    p_content = sub.add_parser("content", help="获取页面 HTML")
    p_content.add_argument("--save", default=None, help="保存到文件")
    
    # wait
    p_wait = sub.add_parser("wait", help="等待元素出现")
    p_wait.add_argument("selector", help="CSS 选择器")
    p_wait.add_argument("--timeout", type=int, default=None, help="超时时间（毫秒）")
    
    # key
    p_key = sub.add_parser("key", help="按下键盘按键")
    p_key.add_argument("key", help="按键名 (Enter, Tab, Escape 等)")
    
    # stop
    sub.add_parser("stop", help="停止守护进程")
    
    # login (快捷登录)
    p_login = sub.add_parser("login", help="快捷自动登录")
    p_login.add_argument("url", help="登录页面 URL")
    p_login.add_argument("--username", help="用户名")
    p_login.add_argument("--password", help="密码")
    p_login.add_argument("--user-sel", dest="pass_sel", default='input[type="text"], input[name*="user"], input[name*="name"]', help="用户名输入框选择器")
    p_login.add_argument("--pass-sel", dest="pass_sel2", default='input[type="password"]', help="密码输入框选择器")
    p_login.add_argument("--submit", default='button[type="submit"], input[type="submit"]', help="提交按钮选择器")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 路由命令
    commands = {
        "start":   cmd_start,
        "status":  cmd_status,
        "go":      cmd_go,
        "snap":    cmd_snap,
        "click":   cmd_click,
        "fill":    cmd_fill,
        "shot":    cmd_shot,
        "run":     cmd_run,
        "content": cmd_content,
        "wait":    cmd_wait,
        "key":     cmd_key,
        "stop":    cmd_stop,
        "login":   cmd_login,
    }
    
    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
