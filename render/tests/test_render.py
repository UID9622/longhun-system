# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""M75 冒烟测试 T1-T6 · python3 render/tests/test_render.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from render.orchestrator import LHRenderOrchestrator
from render.core.boundary import SovereigntyBoundary

PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, cond, extra=""):
    results.append((name, bool(cond)))
    print(f"  [{PASS if cond else FAIL}] {name} {extra}")


def _dom_depth(dom):
    if not isinstance(dom, dict):
        return 0
    cs = dom.get("children") or []
    if not cs:
        return 1
    return 1 + max(_dom_depth(c) for c in cs)


def main():
    print("M75 smoke tests T1-T6")
    engine = LHRenderOrchestrator({"headless": True})

    print("[T1] CNSH parser")
    from render.core.cnsh_parser import parse_command
    cmd = parse_command('渲染.点击(文本="登录", 坐标=[320, 480])')
    check("click parse", cmd["method"] == "click" and cmd["kwargs"].get("text") == "登录")
    cmd2 = parse_command('渲染.打开("https://example.com")')
    check("navigate parse", cmd2["method"] == "navigate" and cmd2["args"][0] == "https://example.com")

    print("[T2] boundary")
    b = SovereigntyBoundary(allow_domains=["*.gov.cn", "huawei.com"], deny_domains=["tracking.com"])
    check("allow hit", b.check("https://www.gov.cn/news") == "www.gov.cn")
    try:
        b.check("https://evil.tracking.com")
        check("deny raises", False)
    except PermissionError:
        check("deny raises", True)
    try:
        b.check("https://evil.example.org")
        check("allowlist raises", False)
    except PermissionError:
        check("allowlist raises", True)

    print("[T3] audit")
    from render.core.audit import audit_text
    check("red", audit_text("兼职刷单 日赚500")["color"] == "🔴")
    check("yellow", audit_text("请输入银行卡号")["color"] == "🟡")
    check("green", audit_text("今天天气不错")["color"] == "🟢")

    print("[T4] real render example.com")
    ctx = engine.navigate("https://example.com")
    check("dna", (ctx.get("dna") or "").startswith("#") and "RENDER" in (ctx.get("dna") or ""))
    check("title", bool(ctx.get("title")))
    check("text", bool(ctx.get("text")))
    check("dom depth>=2", _dom_depth(ctx.get("dom")) >= 2)
    check("audit field", ctx.get("audit", {}).get("color") in ("🟢", "🟡", "🔴"))
    check("screenshot saved", bool(ctx.get("screenshot_path")))

    print("[T5] CNSH execute")
    r = engine.execute('渲染.提取文本(选择器="p", 模式="DOM")')
    check("execute ok", r["status"] == "ok")
    r2 = engine.execute('渲染.设置边界(拒绝域名=["evil.com"])')
    check("set boundary", r2["status"] == "ok")
    r3 = engine.execute('渲染.点击(文本="不存在的按钮XYZ")')
    check("error path", r3["status"] in ("error", "blocked"))

    print("[T6] batch")
    rs = engine.batch(["https://example.com", "https://example.org"], concurrency=2)
    check("batch all ok", len(rs) == 2 and all(x.get("status") == "ok" for x in rs))

    print("[T7] M73 hash registry")
    ctx = engine.navigate("https://example.com")
    hrec = ctx.get("hash_rec")
    check("auto register on navigate", bool(hrec) and len(hrec.get("sha256", "")) == 64)
    check("dna bound", bool(hrec and hrec.get("dna")))
    check("chain hash", bool(hrec and hrec.get("chain_hash")))
    v = engine.verify_hash(sha256=hrec["sha256"]) if hrec else {}
    check("verify hit", v.get("registered") is True)
    r = engine.execute('渲染.验证哈希(哈希="deadbeef")')
    check("cnsh verify miss", r.get("status") == "ok" and r.get("context", {}).get("registered") is False)
    vf = engine.verify_hash(path=hrec.get("extra", {}).get("path")) if hrec and hrec.get("extra", {}).get("path") else {}
    check("verify by file", vf.get("registered") is True)

    engine.close()
    ok = sum(1 for _, c in results if c)
    print(f"RESULT {ok}/{len(results)}")
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
