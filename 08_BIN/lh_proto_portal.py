#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·戊申·戊午·䷬萃-PROTO-PORTAL-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
"""龍魂·协议结构门户 v1.1 — lh proto / lh protocols / lh gametheory / lh proto-serve"""
import sys, os, webbrowser, subprocess, time

PORTAL_PATH = os.path.expanduser("~/longhun-system/portal/protocol-structure/index.html")
GAMETHEORY_DOC = os.path.expanduser("~/longhun-system/papers/LH-GAMETHEORY-REPORT-v1.0.md")
SERVER_SCRIPT = os.path.expanduser("~/longhun-system/bin/lh_protocol_server.py")

def show_help():
    print("""
  🐉 龍魂 · 协议结构门户 v1.1

  命令:
    lh proto                → 在浏览器中打开协议结构门户
    lh protocols            → 同上
    lh proto stats          → 显示协议统计
    lh proto open           → 在浏览器中打开门户
    lh proto-serve [--port] → 启动协议动态索引服务 (默认8910端口)
    lh gametheory           → 显示博弈论报告摘要
    lh gametheory full      → 在浏览器中打开博弈论完整报告
    lh gametheory open      → 同上
""")

def show_stats():
    import json
    idx_path = os.path.expanduser("~/longhun-system/portal/protocol-structure/protocol_index.json")
    try:
        with open(idx_path) as f:
            data = json.load(f)
    except:
        print("无法加载协议索引。请运行: python3 portal/protocol-structure/generate_index.py")
        return

    protocols = data.get('protocols', [])
    p0 = sum(1 for p in protocols if 'P0' in (p.get('file','') + p.get('title','')).upper() or 'ETERNAL' in (p.get('file','')).upper())
    l1 = sum(1 for p in protocols if 'v1.0' in p.get('file','') or 'V1.' in p.get('file',''))
    l2 = len(protocols) - p0 - l1

    print(f"""
  📊 协议统计

  P0 焊死天条:  {p0}
  L1 核心协议:  {l1}
  L2 执行文档:  {l2}
  ─────────────
  协议库总计:   {len(protocols)}
  根文档:       {len(data.get('root_docs',[]))}
  技能引擎:     {len(data.get('skills',[]))}
  文档总计:     {data.get('total_all','?')}
""")

def show_gametheory():
    print("""
  🎲 龍魂系统博弈论研究 · 六系统对比

  核心结论: 主流系统的"不创新"是均衡，不是错误。
            均衡只能被支付函数的改变打破，不能被口号打破。

  六模型:
    1. 大模型军备  — 囚徒困境·军备占优 (7250亿$)
    2. 云计算寡头  — 锁定均衡·迁移率<1%
    3. 移动OS双寡头 — 佣金租金·利润50%
    4. 芯片CUDA    — 生态锁定·500万开发者
    5. 注意力平台  — Engagement囚徒困境
    6. 🐉 龍魂体系  — 多点占位·后均衡布局

  四固化机制:
    结构惯性(Hannan&Freeman) · 制度同构(DiMaggio&Powell)
    创新者窘境(Christensen)  · 指标博弈(古德哈特)

  龍魂三重自固化风险:
    符号焊死双刃性 · 单点权威脆弱性 · 治理成本挤出

  完整报告: papers/LH-GAMETHEORY-REPORT-v1.0.md
  打开: lh gametheory open
""")

def cmd_serve(args):
    """启动协议动态索引服务"""
    port = 8910
    host = '127.0.0.1'
    open_browser = False

    for i, a in enumerate(args):
        if a == '--port' and i + 1 < len(args):
            try:
                port = int(args[i+1])
            except:
                pass
        elif a == '--host' and i + 1 < len(args):
            host = args[i+1]
        elif a in ('--open', '-o'):
            open_browser = True

    if not os.path.exists(SERVER_SCRIPT):
        print(f"❌ 找不到服务脚本: {SERVER_SCRIPT}")
        return

    print(f"🐉 启动协议动态索引服务...")
    print(f"🌐 端口: {port} · 地址: {host}")
    print(f"📊 API: http://{host}:{port}/api/dashboard")
    print(f"📋 API文档: http://{host}:{port}/docs")
    print("-" * 50)

    if open_browser:
        time.sleep(2)
        webbrowser.open(f"http://{host}:{port}/docs")

    # Run server directly (foreground)
    os.execv(sys.executable, [sys.executable, SERVER_SCRIPT, '--host', host, '--port', str(port)])

def main():
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    cmd = args[0] if args else 'help'

    if cmd in ('help', '-h', '--help'):
        show_help()
    elif cmd == 'stats':
        show_stats()
    elif cmd == 'serve':
        cmd_serve(args[1:])
    elif cmd in ('open',):
        path = f"file://{PORTAL_PATH}"
        webbrowser.open(path)
        print(f"📋 协议结构门户已打开: {path}")
    elif cmd == 'gametheory' or (len(args) > 1 and args[0] == 'gametheory'):
        sub = args[1] if len(args) > 1 else 'summary'
        if sub in ('full', 'open'):
            path = f"file://{GAMETHEORY_DOC}"
            webbrowser.open(path)
            print(f"🎲 博弈论报告已打开: {path}")
        else:
            show_gametheory()
    else:
        # Default: open portal
        path = f"file://{PORTAL_PATH}"
        webbrowser.open(path)
        print(f"📋 协议结构门户已打开: {path}")

if __name__ == '__main__':
    main()
