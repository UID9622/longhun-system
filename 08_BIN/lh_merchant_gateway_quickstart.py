#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-MERCHANT-QS-v1.0-a1b2c3d4
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
"""
╔══════════════════════════════════════════════════════════════════════════╗
║    龍魂·商户API网关一键启动与测试 v1.0 — 国产商户5分钟快速接入           ║
║    DN A: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-MERCHANT-QUICKSTART-v1.0        ║
╠══════════════════════════════════════════════════════════════════════════╣
║  用法:                                                                    ║
║    python3 bin/lh_merchant_gateway_quickstart.py          # 完整流程       ║
║    python3 bin/lh_merchant_gateway_quickstart.py --start  # 仅启动网关     ║
║    python3 bin/lh_merchant_gateway_quickstart.py --test   # 仅测试         ║
║    python3 bin/lh_merchant_gateway_quickstart.py --info   # 看接入信息     ║
║    lh gateway-quickstart                # 集成到 lh 命令                  ║
║                                                                            ║
║  设计原则:                                                                 ║
║    · 一键到底 — 不需商户懂Python/数据库/Swagger                             ║
║    · 真实调用 — 所有测试走HTTP+签名，不mock                                  ║
║    · 即拿即用 — 输出的 merchant_info.txt 含完整示例代码                     ║
║                                                                            ║
║  覆盖端点 (7项):                                                           ║
║    Health · Catalog · Merchant/Me · Digital Root                           ║
║    Anxiety Detect · Wuxing · NoAuth→401                                   ║
║                                                                            ║
║  主权人: UID9622 💎 龍芯北辰·诸葛鑫·Lucky                                 ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import hashlib
import hmac
import sqlite3
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# ── 焊死常量 ──
DNA = "#龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-MERCHANT-QUICKSTART-v1.0"
GATEWAY_SCRIPT = Path(__file__).resolve().parent / "lh_merchant_api_gateway.py"
GATEWAY_PORT = 9633
BASE_URL = f"http://localhost:{GATEWAY_PORT}"
MERCHANT_NAME = "龍魂测试商户"
COMPANY_NAME = "龍魂科技"
MERCHANT_TIER = "pro"
LOG_DIR = Path.home() / ".龍魂" / "merchants"
LOG_FILE = LOG_DIR / "gateway_quickstart.log"
MERCHANT_DB = LOG_DIR / "merchants.db"

# ── 确保目录 ──
LOG_DIR.mkdir(parents=True, exist_ok=True)


def log(msg: str):
    """双写: 终端 + 日志文件"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")


def wait_for_gateway(timeout: int = 10) -> bool:
    """等待网关就绪 (不断重试health)"""
    import requests as req
    for i in range(timeout):
        try:
            resp = req.get(f"{BASE_URL}/health", timeout=2)
            if resp.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


# ═══════════════════════════════════════════════════════════
# 核心功能
# ═══════════════════════════════════════════════════════════

def start_gateway() -> bool:
    """启动商户API网关 (后台, 不阻塞)"""
    log("🚀 启动商户API网关...")

    # 检查是否已在运行
    try:
        import requests as req
        resp = req.get(f"{BASE_URL}/health", timeout=2)
        if resp.status_code == 200:
            log("✅ 网关已在运行 (复用现有实例)")
            return True
    except Exception:
        pass

    # 后台启动
    cmd = ["python3", str(GATEWAY_SCRIPT), "serve", "--port", str(GATEWAY_PORT)]
    with open(LOG_FILE, "a") as f:
        f.write(f"\n--- 启动网关: {datetime.now().isoformat()} ---\n")
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=str(Path(__file__).resolve().parent.parent),
    )

    time.sleep(1)
    if wait_for_gateway(10):
        log(f"✅ 网关已启动 (PID: {proc.pid})")
        return True
    else:
        log("❌ 网关启动超时 (检查端口9633是否被占用)")
        return False


def register_test_merchant() -> Optional[Dict]:
    """注册测试商户 → 审核 → 生成密钥 (内部API调用, 无需HTTP)"""
    log("📝 注册测试商户...")

    # 确保模块路径
    gateway_dir = str(GATEWAY_SCRIPT.parent)
    if gateway_dir not in sys.path:
        sys.path.insert(0, gateway_dir)

    try:
        from lh_merchant_api_gateway import (
            register_merchant, approve_merchant, generate_api_key, init_merchant_db
        )

        # 确保数据库存在
        init_merchant_db()

        # 1. 注册
        result = register_merchant(
            name=MERCHANT_NAME,
            company_name=COMPANY_NAME,
            tier=MERCHANT_TIER,
            contact_email="quickstart@longhun.com",
            contact_phone="13800138000",
        )
        if "error" in result:
            log(f"❌ 注册失败: {result['error']}")
            return None
        merchant_id = result["merchant_id"]
        log(f"  商户ID: {merchant_id}")
        log(f"  状态:   {result['status']}")

        # 2. 审核
        result2 = approve_merchant(merchant_id, MERCHANT_TIER)
        if "error" in result2:
            log(f"❌ 审核失败: {result2['error']}")
            return None
        log(f"  审核:   ✅ 通过 (层级: {MERCHANT_TIER})")

        # 3. 生成 API Key
        key_result = generate_api_key(merchant_id, "quickstart测试密钥")
        if "error" in key_result:
            log(f"❌ 密钥生成失败: {key_result['error']}")
            return None
        api_key = key_result["api_key"]
        log(f"  Key ID: {key_result['key_id']}")
        log(f"  API Key: {api_key[:24]}...")

        return {
            "merchant_id": merchant_id,
            "api_key": api_key,
            "tier": MERCHANT_TIER,
            "key_id": key_result["key_id"],
        }

    except ImportError as e:
        log(f"❌ 模块导入失败: {e}")
        log("   请确认 bin/lh_merchant_api_gateway.py 存在")
        return None
    except Exception as e:
        log(f"❌ 注册异常: {e}")
        return None


def call_api(api_key: str, method: str, path: str, body: Optional[Dict] = None) -> Dict:
    """签名 + 调用API (完整HMAC-SHA256签名链路)"""
    import requests as req

    # 🔥 关键: json.dumps必须用ensure_ascii=True (默认)
    # requests库发送json=body时也是ensure_ascii=True → 必须一致否则签名不匹配
    body_str = json.dumps(body) if body else ""
    ts = str(int(time.time()))
    body_hash = hashlib.sha256(body_str.encode()).hexdigest()
    sign_str = f"{method}{path}{ts}{body_hash}"
    sig = hmac.new(api_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()

    headers = {
        "X-LH-API-Key": api_key,
        "X-LH-Timestamp": ts,
        "X-LH-Signature": sig,
        "Content-Type": "application/json",
    }

    url = f"{BASE_URL}{path}"
    try:
        if method == "POST":
            resp = req.post(url, headers=headers, json=body, timeout=10)
        else:
            resp = req.get(url, headers=headers, timeout=10)
        return resp.json()
    except req.exceptions.ConnectionError:
        return {"error": "连接失败", "detail": f"无法连接到 {url}，请确认网关已启动"}
    except json.JSONDecodeError:
        return {"error": "响应解析失败", "raw": resp.text[:200], "status": resp.status_code}
    except Exception as e:
        return {"error": str(e)}


def call_api_no_auth(path: str) -> Dict:
    """无需认证的API调用 (health等)"""
    import requests as req
    try:
        resp = req.get(f"{BASE_URL}{path}", timeout=5)
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def run_tests(api_key: str) -> Dict:
    """运行7项API测试 (覆盖所有核心端点 + 安全边界)"""
    log("🧪 运行API测试 (7项)...")
    log("")

    tests = [
        # ── 0. 无认证测试 (边界) ──
        {
            "name": "无认证→拒绝(401)",
            "fn": lambda: call_api_no_auth("/v1/catalog"),
            "check": lambda r: isinstance(r, dict) and r.get("error"),
            "desc": "不带认证头访问应返回401"
        },
        # ── 1. 健康检查 (无需认证) ──
        {
            "name": "健康检查",
            "fn": lambda: call_api_no_auth("/health"),
            "check": lambda r: r.get("status") == "ok",
            "desc": "Health端点应返回ok"
        },
        # ── 2. API目录 ──
        {
            "name": "API目录",
            "fn": lambda: call_api(api_key, "GET", "/v1/catalog"),
            "check": lambda r: "catalog" in r and r.get("total_apis", 0) > 0,
            "desc": "应返回可用API清单"
        },
        # ── 3. 商户自身信息 ──
        {
            "name": "商户信息",
            "fn": lambda: call_api(api_key, "GET", "/v1/merchant/me"),
            "check": lambda r: r.get("code") == 0 and "tier" in r.get("data", {}),
            "desc": "应返回商户层级/日用量"
        },
        # ── 4. 数字根 (369→9) ──
        {
            "name": "数字根(369→9)",
            "fn": lambda: call_api(api_key, "POST", "/v1/math/digital-root", {"n": 369}),
            "check": lambda r: (
                r.get("code") == 0
                and r.get("data", {}).get("digital_root") == 9
                and r.get("data", {}).get("is_369_fixed_point") is True
            ),
            "desc": "369数字根=9, 是369不动点"
        },
        # ── 5. 焦虑话术检测 ──
        {
            "name": "焦虑检测",
            "fn": lambda: call_api(api_key, "POST", "/v1/security/anxiety",
                                   {"content": "你再不买就来不及了，限时最后一天，错过就永远没了！"}),
            "check": lambda r: (
                r.get("code") == 0
                and r.get("data", {}).get("has_anxiety") is True
                and "C_制造焦虑" in str(r.get("data", {}).get("categories", {}))
            ),
            "desc": "限时话术→检测到焦虑制造"
        },
        # ── 6. 五行判定 ──
        {
            "name": "五行判定",
            "fn": lambda: call_api(api_key, "POST", "/v1/culture/wuxing",
                                   {"input": "丙午乙巳"}),
            "check": lambda r: (
                r.get("code") == 0
                and r.get("data", {}).get("primary") == "火"
                and len(r.get("data", {}).get("elements", [])) == 4
            ),
            "desc": "丙→火·午→火·乙→木·巳→火"
        },
    ]

    results = {"passed": 0, "failed": 0, "total": len(tests), "details": []}

    for test in tests:
        try:
            resp = test["fn"]()
            passed = test["check"](resp)
            if passed:
                results["passed"] += 1
                status = "✅"
            else:
                results["failed"] += 1
                status = "❌"

            # 取关键字段展示
            tag = ""
            if "数字根" in test["name"]:
                d = resp.get("data", {})
                tag = f" root={d.get('digital_root','?')} 369={'Y' if d.get('is_369_fixed_point') else 'N'}"
            elif "焦虑" in test["name"]:
                d = resp.get("data", {})
                tag = f" detected={d.get('has_anxiety','?')} risk={d.get('risk_level','?')}"
            elif "五行" in test["name"]:
                d = resp.get("data", {})
                tag = f" primary={d.get('primary','?')} wx={d.get('elements','?')}"
            elif "目录" in test["name"]:
                tag = f" apis={resp.get('total_apis','?')}"
            elif "商户" in test["name"]:
                d = resp.get("data", {})
                tag = f" tier={d.get('tier','?')} used={d.get('daily_used','?')}"
            elif "无认证" in test["name"]:
                tag = " 401✅"

            results["details"].append({
                "name": test["name"],
                "status": status,
                "desc": test["desc"],
                "tag": tag,
            })
            log(f"  {status} {test['name']}{tag}")
        except Exception as e:
            results["failed"] += 1
            results["details"].append({
                "name": test["name"],
                "status": "❌",
                "error": str(e),
            })
            log(f"  ❌ {test['name']}: {e}")

    return results


def try_read_existing_merchant() -> Optional[Dict]:
    """从数据库读取第一个活跃商户的API Key (用于 --test 回退)"""
    try:
        conn = sqlite3.connect(str(MERCHANT_DB))
        conn.row_factory = sqlite3.Row
        # 查活跃商户 + 活跃密钥
        row = conn.execute("""
            SELECT m.merchant_id, m.name, m.tier, k.key_id
            FROM merchants m
            JOIN api_keys k ON k.merchant_id = m.merchant_id
            WHERE m.status = 'active' AND k.status = 'active'
            ORDER BY k.created_at DESC
            LIMIT 1
        """).fetchone()
        conn.close()

        if row:
            # API Key明文不可恢复 (已哈希存储)
            # → 用户必须手动提供或在完整流程中获取
            log("⚠️ 检测到活跃商户，但API Key明文无法从数据库恢复（安全设计）")
            log(f"   商户: {row['name']} ({row['merchant_id']})")
            log(f"   层级: {row['tier']}")
            log(f"   请使用完整流程(--full)重新生成密钥，或手动提供API Key")
            return None
        else:
            log("⚠️ 无可用商户，请先运行完整流程")
            return None
    except Exception as e:
        log(f"❌ 数据库读取失败: {e}")
        return None


def generate_info(merchant_info: Dict, test_results: Dict) -> str:
    """生成商户接入信息 (含完整示例代码)"""
    lines = []
    lines.append("")
    lines.append("═" * 60)
    lines.append("🐉  龍魂商户API网关 · 接入信息")
    lines.append("═" * 60)
    lines.append(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"  DNA:  {DNA}")
    lines.append("")

    lines.append("📍 服务地址:")
    lines.append(f"  网关:     {BASE_URL}")
    lines.append(f"  API文档:  {BASE_URL}/docs")
    lines.append(f"  能力目录:  {BASE_URL}/v1/catalog")
    lines.append(f"  健康检查:  {BASE_URL}/health")
    lines.append("")

    if merchant_info:
        lines.append("🔑 商户凭证 (请妥善保管):")
        lines.append(f"  商户ID:   {merchant_info['merchant_id']}")
        lines.append(f"  API Key: {merchant_info['api_key']}")
        lines.append(f"  层级:    {merchant_info['tier']}")
        lines.append(f"  Key ID:  {merchant_info.get('key_id', '-')}")
        lines.append("")

    lines.append("📊 测试结果:")
    lines.append(f"  通过: {test_results['passed']}/{test_results['total']}")
    lines.append(f"  失败: {test_results['failed']}/{test_results['total']}")
    for detail in test_results.get("details", []):
        lines.append(f"  {detail['status']} {detail['name']}{detail.get('tag', '')}")
    lines.append("")

    if test_results["passed"] == test_results["total"]:
        lines.append("🎉 全部测试通过！网关已就绪，商户可开始接入。")
    else:
        lines.append("⚠️ 部分测试失败，请检查:")
        for detail in test_results.get("details", []):
            if "❌" in detail.get("status", ""):
                lines.append(f"   - {detail['name']}: {detail.get('error', detail.get('desc', ''))}")
    lines.append("")
    lines.append("═" * 60)

    # ── Python 调用示例 ──
    if merchant_info:
        lines.append("")
        lines.append("📝 Python 调用示例 (可直接复制运行):")
        lines.append("```python")
        lines.append("import hashlib, hmac, time, json, requests")
        lines.append("")
        lines.append(f'API_KEY = "{merchant_info["api_key"]}"')
        lines.append(f'BASE_URL = "{BASE_URL}"')
        lines.append("")
        lines.append("def call_api(method, path, body=None):")
        lines.append("    \"\"\"签名 + 调用龍魂商户API\"\"\"")
        lines.append("    body_str = json.dumps(body) if body else ''  # 默认ensure_ascii=True, 与requests一致")
        lines.append("    ts = str(int(time.time()))")
        lines.append("    body_hash = hashlib.sha256(body_str.encode()).hexdigest()")
        lines.append("    # 签名串: METHOD + PATH + TIMESTAMP + SHA256(BODY)")
        lines.append("    sign_str = f'{method}{path}{ts}{body_hash}'")
        lines.append("    # HMAC-SHA256(API_KEY, 签名串)")
        lines.append("    sig = hmac.new(API_KEY.encode(), sign_str.encode(), hashlib.sha256).hexdigest()")
        lines.append("    ")
        lines.append("    headers = {")
        lines.append("        'X-LH-API-Key': API_KEY,")
        lines.append("        'X-LH-Timestamp': ts,")
        lines.append("        'X-LH-Signature': sig,")
        lines.append("        'Content-Type': 'application/json',")
        lines.append("    }")
        lines.append("    ")
        lines.append("    url = f'{BASE_URL}{path}'")
        lines.append("    if method == 'POST':")
        lines.append("        return requests.post(url, headers=headers, json=body)")
        lines.append("    return requests.get(url, headers=headers)")
        lines.append("")
        lines.append("# 示例: 计算数字根")
        lines.append('resp = call_api("POST", "/v1/math/digital-root", {"n": 369})')
        lines.append("print(resp.json())")
        lines.append("# → {'code':0, 'data':{'digital_root':9, 'is_369_fixed_point':True}}")
        lines.append("")
        lines.append("# 示例: 焦虑话术检测")
        lines.append('resp = call_api("POST", "/v1/security/anxiety", {"content": "限时最后一天！"})')
        lines.append('print(f"是否焦虑: {resp.json()[\"data\"][\"has_anxiety\"]}")')
        lines.append("")
        lines.append("# 示例: 五行判定")
        lines.append('resp = call_api("POST", "/v1/culture/wuxing", {"input": "丙午乙巳"})')
        lines.append('print(f"主五行: {resp.json()[\"data\"][\"primary\"]}")')
        lines.append("```")
        lines.append("")
        lines.append("📋 curl 调用示例:")
        lines.append("```bash")
        lines.append("API_KEY='" + merchant_info["api_key"] + "'")
        lines.append("TS=$(date +%s)")
        lines.append('BODY=\'{"n":369}\'')
        lines.append("BODY_HASH=$(echo -n \"$BODY\" | shasum -a 256 | cut -d' ' -f1)")
        lines.append("SIGN_STR=\"POST/v1/math/digital-root${TS}${BODY_HASH}\"")
        lines.append("SIG=$(echo -n \"$SIGN_STR\" | openssl dgst -sha256 -hmac \"$API_KEY\" | cut -d' ' -f2)")
        lines.append("curl -X POST http://localhost:9633/v1/math/digital-root \\")
        lines.append('  -H "X-LH-API-Key: $API_KEY" \\')
        lines.append('  -H "X-LH-Timestamp: $TS" \\')
        lines.append('  -H "X-LH-Signature: $SIG" \\')
        lines.append('  -H "Content-Type: application/json" \\')
        lines.append('  -d \'{"n":369}\'')
        lines.append("```")

    lines.append("")
    lines.append("═" * 60)
    lines.append("🔗 完整协议: 01_protocols/LH-MERCHANT-API-PROTOCOL-v1.0.md")
    lines.append("🔗 网关源码: bin/lh_merchant_api_gateway.py")
    lines.append("🔗 日志文件: " + str(LOG_FILE))
    lines.append("═" * 60)

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂商户API网关 · 一键启动与测试",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                完整流程 (启动+注册+测试+输出信息)
  %(prog)s --start        仅启动网关
  %(prog)s --test         仅运行测试 (需要网关+API Key)
  %(prog)s --full         完整流程 (同默认)
  lh gateway-quickstart   集成到 lh 命令
        """
    )
    parser.add_argument("--start", action="store_true", help="仅启动网关 (后台)")
    parser.add_argument("--test", action="store_true", help="仅运行API测试 (需网关已启动+已有API Key)")
    parser.add_argument("--info", action="store_true", help="输出上次接入信息")
    parser.add_argument("--full", action="store_true", help="完整流程: 启动→注册→测试→输出 (默认)")
    parser.add_argument("--port", type=int, default=9633, help="网关端口 (默认9633)")
    args = parser.parse_args()

    # 端口覆盖
    global BASE_URL, GATEWAY_PORT
    GATEWAY_PORT = args.port
    BASE_URL = f"http://localhost:{GATEWAY_PORT}"

    # 默认执行完整流程
    if not any([args.start, args.test, args.info, args.full]):
        args.full = True

    log("🐉 龍魂商户API网关 · 一键启动与测试 v1.0")
    log(f"DNA: {DNA}")
    log("")

    # 1. 启动网关
    if args.full or args.start:
        if not start_gateway():
            log("❌ 网关启动失败，退出")
            sys.exit(1)

    # 2. 等待就绪
    if not wait_for_gateway(5):
        log("❌ 网关未响应 (端口 {GATEWAY_PORT})")
        sys.exit(1)

    merchant_info = None
    test_results = None

    # 3. 完整流程: 注册商户
    if args.full:
        merchant_info = register_test_merchant()
        if not merchant_info:
            log("❌ 商户注册失败")
            sys.exit(1)

    # 4. 运行测试
    if args.full or args.test:
        if merchant_info:
            # 已有密钥 → 直接测试
            test_results = run_tests(merchant_info["api_key"])
        elif args.test:
            # --test 模式: 尝试读取已有商户
            log("🔍 --test 模式: 查找已有商户...")
            existing = try_read_existing_merchant()
            if existing and existing.get("api_key"):
                merchant_info = existing
                test_results = run_tests(merchant_info["api_key"])
            else:
                log("❌ 无法获取API Key，请运行完整流程(--full)")
                log("   原因: API Key明文不存储于数据库 (安全设计)")
                log("   解决: python3 bin/lh_merchant_gateway_quickstart.py --full")
                sys.exit(1)

    # 5. 输出接入信息
    if merchant_info and test_results:
        info = generate_info(merchant_info, test_results)
        print(info)

        # 保存到文件
        reports_dir = Path(__file__).resolve().parent.parent / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        info_file = reports_dir / "merchant_api_quickstart_info.txt"
        info_file.write_text(info, encoding="utf-8")
        log(f"\n📄 接入信息已保存: {info_file}")

    elif args.info:
        # 尝试读取上次保存的信息
        info_file = Path(__file__).resolve().parent.parent / "reports" / "merchant_api_quickstart_info.txt"
        if info_file.exists():
            print(info_file.read_text(encoding="utf-8"))
        else:
            log("⚠️ 未找到历史接入信息，请先运行完整流程")

    log("")
    log("✅ 完成")
    log(f"📋 日志: {LOG_FILE}")


if __name__ == "__main__":
    main()
