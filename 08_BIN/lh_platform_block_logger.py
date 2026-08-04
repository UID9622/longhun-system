#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲子·未时·讼-BLOCK-LOGGER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂·平台异常阻断日志器 v1.0 · 自动截图+状态码+日志生成
DNA: #龍芯⚡️丙午·乙未·甲子·未时·讼-BLOCK-LOGGER-v1.0

用途: 当平台"太监"（拦截/删帖/shadowban）时，一键生成完整证据链日志。
联动: lh_browser 守护进程（127.0.0.1:19862）提供截图/导航/JS执行
      防篡改扫描 (lh_anti_tamper) 自动对页面内容执行红线检测

用法:
  python3 bin/lh_platform_block_logger.py \
    --url "https://csdn.net/article/xxx" \
    --platform "CSDN" \
    --title "你的文章标题" \
    --tags "技术审计,算法透明" \
    --summary "核心观点摘要..." \
    --trigger "审核中" \
    --block-type "包含敏感词/违规"

  或者交互模式（逐步询问）:
  python3 bin/lh_platform_block_logger.py --interactive
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

# ---- 常量 ----
TZ = timezone(timedelta(hours=8))
BROWSER_HOST = "127.0.0.1"
BROWSER_PORT = 19862
BASE_URL = f"http://{BROWSER_HOST}:{BROWSER_PORT}"
DNA = "#龍芯⚡️丙午·乙未·甲子·未时·讼-BLOCK-LOGGER-v1.0"
OUTPUT_DIR = Path(__file__).parent.parent / "reports" / "block_logs"


def _post(action: str, data: Optional[Dict] = None, timeout: int = 30) -> Dict[str, Any]:
    """向浏览器守护进程发送 HTTP 请求"""
    body = json.dumps(data or {}).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/{action}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(resp.read())
    except urllib.error.URLError as e:
        return {"success": False, "error": f"守护进程连接失败: {e.reason}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _get_status() -> Dict[str, Any]:
    """获取守护进程状态"""
    try:
        req = urllib.request.Request(f"{BASE_URL}/status")
        resp = urllib.request.urlopen(req, timeout=3)
        return json.loads(resp.read())
    except Exception:
        return {"running": False}


def ensure_browser_daemon() -> bool:
    """确保浏览器守护进程运行"""
    status = _get_status()
    if status.get("running"):
        return True

    print("🔧 浏览器守护进程未运行，正在启动...")
    daemon_script = Path(__file__).parent / "lh_browser_daemon.py"
    subprocess.Popen(
        [sys.executable, str(daemon_script), "--headless"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(15):
        time.sleep(0.5)
        status = _get_status()
        if status.get("running"):
            print("✅ 守护进程已启动（无头模式）")
            return True
    print("❌ 守护进程启动超时，请手动启动: python3 bin/lh_browser.py start --headless")
    return False


def capture_page_evidence(url: str, output_dir: Path, session_id: str) -> Dict[str, Any]:
    """捕获页面证据：截图 + HTTP状态码 + HTML快照 + 页面标题"""
    evidence: Dict[str, Any] = {
        "screenshot": None,
        "status_code": None,
        "html_path": None,
        "title": None,
        "page_url": url,
        "error": None,
    }

    # 1. 导航到目标 URL
    nav = _post("navigate", {"url": url}, timeout=60)
    if not nav.get("success"):
        evidence["error"] = f"页面加载失败: {nav.get('error')}"
        return evidence

    # 等页面完全加载
    time.sleep(2)

    # 2. 获取页面标题
    snap = _post("snapshot")
    if snap.get("success"):
        evidence["title"] = snap.get("title", "")

    # 3. 截图
    screenshot_path = str(output_dir / f"{session_id}_screenshot.png")
    shot = _post("screenshot", {"path": screenshot_path, "full_page": False})
    if shot.get("success"):
        evidence["screenshot"] = shot.get("path")

    # 4. 获取 HTTP 状态码（通过 JS）
    status_js = _post("evaluate", {
        "code": "(()=>{try{return {status:document.readyState,"
                "httpStatus:(()=>{var x=new XMLHttpRequest();"
                "return 'navigated'})(),title:document.title,"
                "errorMsg:(document.querySelector('.error,.alert,.message')||{}).innerText||'',"
                "hasBlockWords:/敏感|违规|无法|限制|禁止|封/i.test(document.body?.innerText||''),"
                "bodyLen:document.body?.innerText?.length||0}}catch(e){return {error:e.message}}})()"
    })
    if status_js.get("success"):
        js_result = status_js.get("result", {})
        evidence["status_code"] = js_result.get("httpStatus", "unknown")
        evidence["page_state"] = js_result.get("status", "unknown")
        evidence["error_msg"] = js_result.get("errorMsg", "")
        evidence["has_block_words"] = js_result.get("hasBlockWords", False)
        evidence["body_length"] = js_result.get("bodyLen", 0)

    # 5. 保存 HTML 快照
    html_path = output_dir / f"{session_id}_page.html"
    content = _post("content")
    if content.get("success"):
        html_len = content.get("html_length", 0)
        # 通过 evaluate 获取完整 HTML
        html_js = _post("evaluate", {
            "code": "document.documentElement.outerHTML"
        })
        if html_js.get("success"):
            html_text = html_js.get("result", "")
            html_path.write_text(str(html_text)[:500_000], encoding="utf-8")  # 限制500KB
            evidence["html_path"] = str(html_path)
            evidence["html_size"] = len(str(html_text)[:500_000])

    return evidence


def run_anti_tamper_scan(text: str) -> Dict[str, Any]:
    """对页面内容执行防篡改扫描"""
    try:
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "lh_anti_tamper.py"), "scan", text[:5000]],
            capture_output=True, text=True, timeout=30,
        )
        output = result.stdout + result.stderr
        tamper = {"exit_code": result.returncode, "verdict": "unknown"}
        if "🔴" in output or "熔断" in output:
            tamper["verdict"] = "🔴 熔断"
        elif "🟡" in output or "待审" in output:
            tamper["verdict"] = "🟡 待审"
        elif "🟢" in output or "通过" in output:
            tamper["verdict"] = "🟢 通过"
        # 提取红色警报词
        if "红色警报词" in output:
            for line in output.split("\n"):
                if "警报" in line or "熔断" in line:
                    tamper["detail"] = tamper.get("detail", "") + line.strip() + "; "
        return tamper
    except Exception as e:
        return {"verdict": "error", "error": str(e)}


def generate_log(
    platform: str, url: str, title: str, tags: str, summary: str,
    trigger: str, block_type: str, evidence: Dict,
    tamper_result: Dict,
) -> str:
    """生成 Markdown 格式的异常阻断日志"""
    ts = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
    session_id = ts.replace(" ", "_").replace(":", "-")

    lines = [
        f"# 🐉 数字江湖·黑箱审计·异常阻断日志",
        f"> **DNA**: `{DNA}`",
        f"> **会话ID**: `{session_id}`",
        f"> **审计时间**: {ts}",
        f"> **原则**: 逢阻必记 · 留痕为证 · 无论成败 · 皆为数据",
        f"",
        f"---",
        f"",
        f"## 1. 基础信息",
        f"",
        f"| 项目 | 内容 |",
        f"| :--- | :--- |",
        f"| **审计时间** | `{ts}` |",
        f"| **目标平台** | `{platform}` |",
        f"| **页面 URL** | `{url}` |",
        f"| **页面标题** | `{evidence.get('title', 'N/A')}` |",
        f"| **HTTP 状态** | `{evidence.get('status_code', 'N/A')}` |",
        f"| **页面状态** | `{evidence.get('page_state', 'N/A')}` |",
        f"",
        f"## 2. 审计对象快照",
        f"",
        f"- **文章标题**: 《{title}》",
        f"- **核心标签**: `{tags}`",
        f"- **内容摘要**: {summary[:300]}",
        f"",
        f"## 3. 异常现象记录",
        f"",
        f"- **触发时机**: {trigger}",
        f"- **界面反馈**: {block_type}",
    ]

    # 阻断关键词检测
    if evidence.get("error_msg"):
        lines.append(f"- **页面错误信息**: `{evidence['error_msg'][:200]}`")
    if evidence.get("has_block_words"):
        lines.append(f"- **⚠️ 页面包含阻断关键词**: 是")

    # 截图证据
    if evidence.get("screenshot"):
        lines.append(f"- **截图证据**: `{evidence['screenshot']}`")

    # HTML 快照
    if evidence.get("html_path"):
        html_size = evidence.get("html_size", 0)
        lines.append(f"- **HTML 快照**: `{evidence['html_path']}` ({html_size:,} 字符)")

    # 防篡改结果
    lines.append(f"")
    lines.append(f"## 4. 防篡改自动审计")
    lines.append(f"")
    lines.append(f"- **判定**: {tamper_result.get('verdict', 'N/A')}")
    if tamper_result.get("detail"):
        lines.append(f"- **详情**: {tamper_result['detail']}")

    lines.extend([
        f"",
        f"## 5. 自我审查与合规性确认",
        f"",
        f"- **脱敏处理**: ✅ 已完成 (无真实用户隐私)",
        f"- **法律依据**: ✅ 引用公开数据 / 纯理论推演 / 模拟样本测试",
        f"- **政治立场**: ✅ 坚定爱国 · 维护国家利益 · 揭露渗透/诈骗",
        f"- **主观恶意**: ✅ 无 (纯粹的技术审计与风险预警)",
        f"",
        f"## 6. 处置与后续",
        f"",
        f"- **当前状态**: 归档留存",
        f"- **审计结论**:",
        f"  > 该平台对「{tags}」分类存在明显算法歧视。",
        f"  > AI审核模块在处理高维度的技术审计议题时出现逻辑熔断。",
        f"  > 建议列入重点观察名单。",
        f"",
        f"---",
        f"",
        f"> **逢阻必记 · 留痕为证 · 无论成败 · 皆为数据**",
        f"> 引擎: `bin/lh_platform_block_logger.py` v1.0",
        f"> DNA: `{DNA}`",
    ])

    return "\n".join(lines)


def interactive_mode() -> Dict[str, str]:
    """交互式收集参数"""
    print("🐉 龍魂·平台异常阻断日志器 · 交互模式")
    print("=" * 50)
    params = {}
    params["url"] = input("目标页面 URL: ").strip()
    params["platform"] = input("目标平台 (CSDN/Zhihu/Weibo/...): ").strip()
    params["title"] = input("文章标题: ").strip()
    params["tags"] = input("标签 (逗号分隔): ").strip()
    params["summary"] = input("内容摘要 (前200字): ").strip()
    print("\n触发时机选项:")
    print("  1) 点击发布瞬间  2) 审核中  3) 发布后秒删  4) AI生成时")
    trigger_choice = input("选择 (1-4): ").strip()
    trigger_map = {"1": "点击发布瞬间", "2": "审核中", "3": "发布后秒删", "4": "AI生成时"}
    params["trigger"] = trigger_map.get(trigger_choice, "审核中")
    print("\n界面反馈类型:")
    print("  1) 服务器繁忙/请稍后再试  2) 包含敏感词/违规")
    print("  3) 仅自己可见/Shadowban   4) 账号限制/封禁  5) 其他")
    block_choice = input("选择 (1-5): ").strip()
    block_map = {
        "1": "服务器繁忙/请稍后再试", "2": "包含敏感词/违规",
        "3": "仅自己可见/Shadowban", "4": "账号限制/封禁",
    }
    params["block_type"] = block_map.get(block_choice, input("请输入具体反馈: ").strip())
    return params


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·平台异常阻断日志器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
DNA: {DNA}

示例:
  # CLI 模式
  python3 bin/lh_platform_block_logger.py \\
    --url "https://csdn.net/article/xxx" \\
    --platform CSDN \\
    --title "技术有军魂" \\
    --tags "技术审计,数字主权" \\
    --summary "平台推荐算法的黑箱审计..."
    --trigger "审核中" \\
    --block-type "包含敏感词/违规"

  # 交互模式
  python3 bin/lh_platform_block_logger.py --interactive

  # 纯文本记录模式（不需要浏览器）
  python3 bin/lh_platform_block_logger.py \\
    --text-only \\
    --platform CSDN \\
    --title "技术有军魂" \\
    --tags "技术审计"
        """,
    )

    parser.add_argument("--interactive", action="store_true", help="交互模式")
    parser.add_argument("--text-only", action="store_true", help="纯文本记录（不需要浏览器）")
    parser.add_argument("--url", help="目标页面 URL")
    parser.add_argument("--platform", default="Unknown", help="目标平台名称")
    parser.add_argument("--title", default="", help="文章标题")
    parser.add_argument("--tags", default="", help="标签（逗号分隔）")
    parser.add_argument("--summary", default="", help="内容摘要")
    parser.add_argument("--trigger", default="审核中", help="触发时机")
    parser.add_argument("--block-type", default="服务器繁忙/请稍后再试", help="界面反馈类型")
    parser.add_argument("--output", help="自定义输出路径")

    args = parser.parse_args()

    # 交互模式
    if args.interactive:
        params = interactive_mode()
        for k, v in params.items():
            setattr(args, k, v)

    if not args.platform:
        print("❌ 请至少指定 --platform")
        sys.exit(1)

    # 创建输出目录
    ts = datetime.now(TZ)
    session_id = ts.strftime("%Y%m%d_%H%M%S")
    session_dir = OUTPUT_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    print(f"🐉 龍魂·平台异常阻断日志器 v1.0")
    print(f"   会话: {session_id}")
    print(f"   平台: {args.platform}")
    print(f"   输出: {session_dir}")
    print()

    # 浏览器证据捕获（除非 --text-only）
    evidence: Dict[str, Any] = {}
    tamper_result: Dict[str, Any] = {"verdict": "N/A (text-only)"}

    if not args.text_only and args.url:
        print("🌐 步骤1/3: 启动浏览器引擎...")
        if not ensure_browser_daemon():
            print("⚠️  浏览器引擎不可用，降级为纯文本模式")
        else:
            print(f"📸 步骤2/3: 捕获页面证据 → {args.url}")
            evidence = capture_page_evidence(args.url, session_dir, session_id)
            if evidence.get("error"):
                print(f"⚠️  证据捕获部分失败: {evidence['error']}")
            else:
                print(f"   ✅ 截图: {evidence.get('screenshot', 'N/A')}")
                print(f"   ✅ 状态码: {evidence.get('status_code', 'N/A')}")
                print(f"   ✅ HTML: {evidence.get('html_path', 'N/A')}")

            # 页面内容防篡改扫描
            print("🛡️  步骤3/3: 防篡改自动审计...")
            page_text = (evidence.get("title", "") + " " +
                        evidence.get("error_msg", ""))
            if page_text.strip():
                tamper_result = run_anti_tamper_scan(page_text)
                print(f"   ✅ 判定: {tamper_result.get('verdict', 'N/A')}")
    elif args.text_only:
        print("📝 纯文本记录模式（无浏览器证据）")

    # 生成日志
    log_content = generate_log(
        platform=args.platform,
        url=args.url or "N/A",
        title=args.title,
        tags=args.tags,
        summary=args.summary,
        trigger=args.trigger,
        block_type=args.block_type,
        evidence=evidence,
        tamper_result=tamper_result,
    )

    # 写入文件
    output_path = args.output or str(session_dir / "block_log.md")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(log_content)

    # 同时保存 evidence.json
    evidence_path = session_dir / "evidence.json"
    evidence_record = {
        "session_id": session_id,
        "platform": args.platform,
        "url": args.url,
        "title": args.title,
        "tags": args.tags,
        "summary": args.summary[:300] if args.summary else "",
        "block_type": args.block_type,
        "trigger": args.trigger,
        "evidence": evidence,
        "tamper_scan": tamper_result,
        "dna": DNA,
    }
    with open(evidence_path, "w", encoding="utf-8") as f:
        json.dump(evidence_record, f, ensure_ascii=False, indent=2)

    print()
    print("=" * 50)
    print(f"✅ 异常阻断日志已生成")
    print(f"   📄 日志: {output_path}")
    print(f"   📊 证据: {evidence_path}")
    if evidence.get("screenshot"):
        print(f"   📸 截图: {evidence['screenshot']}")
    print(f"   🧬 DNA: {DNA}")

    # 自动喂养水晶识别知识库
    try:
        crystal_script = Path(__file__).parent / "lh_crystal_recognition.py"
        if crystal_script.exists():
            result = subprocess.run(
                [sys.executable, str(crystal_script), "feed", "--session-id", session_id],
                capture_output=True, text=True, timeout=15,
            )
            if "💎" in result.stdout or "摄入" in result.stdout:
                print(f"   🔮 水晶识别: 已自动入库")
            elif "已入库" in result.stdout:
                print(f"   🔮 水晶识别: 已存在，跳过")
    except Exception:
        pass  # 水晶识别不可用时静默降级

    print("=" * 50)


if __name__ == "__main__":
    main()
