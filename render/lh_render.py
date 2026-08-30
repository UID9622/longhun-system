# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""M75 渲染引擎 CLI · lh render 子命令入口。"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from render.orchestrator import LHRenderOrchestrator

_engine = None


def get_engine(headless: bool = True) -> LHRenderOrchestrator:
    global _engine
    if _engine is None:
        _engine = LHRenderOrchestrator({"headless": headless})
    return _engine


def _print(d: dict):
    print(json.dumps(d, ensure_ascii=False, indent=2, default=str))


def cmd_status(args):
    _print(get_engine(args.headless).status())


def cmd_open(args):
    engine = get_engine(args.headless)
    r = engine.navigate(args.url)
    print("=" * 56)
    print(f"🌐 {r.get('title') or '(无标题)'}  |  {r.get('url')}")
    print(f"   DNA: {r.get('dna')}  三色: {r.get('audit', {}).get('color')}")
    text = (r.get('text') or '')[:400].replace('\n', ' | ')
    print(f"   文本: {text}")
    print(f"   链接: {len(r.get('links') or [])} 表单: {len(r.get('forms') or [])} 表格: {len(r.get('tables') or [])}")
    print(f"   截图: {r.get('screenshot_path')}")
    print("=" * 56)


def cmd_run(args):
    engine = get_engine(args.headless)
    # 支持分号/换行分隔的多指令会话（同一引擎内顺序执行，保持状态）
    raw = args.command.replace("；", ";")
    commands = [c.strip() for c in re.split(r"[;\n]+", raw) if c.strip()]
    results = []
    for c in commands:
        r = engine.execute(c)
        results.append(r)
        if r["status"] not in ("ok",):
            break
    _print(results if len(results) > 1 else results[0])


def cmd_batch(args):
    engine = get_engine(args.headless)
    urls = args.urls
    if args.file:
        urls = [l.strip() for l in Path(args.file).read_text().splitlines() if l.strip()]
    results = engine.batch(urls, args.concurrency, args.interval)
    ok = sum(1 for x in results if x.get("status") == "ok")
    print(f"批量完成: {ok}/{len(results)} 🟢")
    for x in results:
        if x.get("status") == "ok":
            r = x.get("result") or {}
            print(f"  🟢 {x['url']} | {r.get('title')} | {r.get('audit', {}).get('color')}")
        else:
            print(f"  🔴 {x['url']} | {x.get('error')}")


def cmd_server(args):
    import uvicorn
    from render.server import app
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


def cmd_log(args):
    engine = get_engine(args.headless)
    for e in engine.status().get("audit_log", [])[-int(args.n):]:
        print(f"{e['timestamp']} {e['color']} {e['command']}")


def main():
    p = argparse.ArgumentParser(prog="lh render", description="M75 龍魂渲染引擎")
    p.add_argument("--headless", action="store_true", default=True, help="无头模式")
    sub = p.add_subparsers(dest="op", required=True)

    s = sub.add_parser("status"); s.set_defaults(func=cmd_status)
    s = sub.add_parser("open"); s.add_argument("url"); s.set_defaults(func=cmd_open)
    s = sub.add_parser("run"); s.add_argument("command"); s.set_defaults(func=cmd_run)
    s = sub.add_parser("batch"); s.add_argument("urls", nargs="*"); s.add_argument("--file"); s.add_argument("--concurrency", type=int, default=4); s.add_argument("--interval", type=float, default=0.5); s.set_defaults(func=cmd_batch)
    s = sub.add_parser("server"); s.add_argument("--host", default="127.0.0.1"); s.add_argument("--port", type=int, default=8788); s.set_defaults(func=cmd_server)
    s = sub.add_parser("log"); s.add_argument("-n", type=int, default=10); s.set_defaults(func=cmd_log)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
