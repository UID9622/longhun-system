#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""龍魂每日复盘增强版 · P03雯雯主理 / P04鲁班安全 / P05上帝之眼裁决
DNA:#龍芯⚡️2026-06-09-DAILY-REVIEW-ENHANCED-v2.0
增强功能: 完整日志审计·操作统计·人格调度验证·API服务检查
"""
import os, sys, json, smtplib, subprocess, datetime, sqlite3, socket
import urllib.request
import urllib.error
import hmac, hashlib, base64, time as _time
from email.mime.text import MIMEText
from email.header import Header
from pathlib import Path
from typing import Optional

try:
    import feishu_bot
except ImportError:
    feishu_bot = None

HOME = os.path.expanduser("~/longhun-system")
KFPP_DB = os.path.expanduser("~/.龍魂/kfpp/kfpp_execution.db")
ACTION_LOG = os.path.join(HOME, "logs", "action_log.jsonl")
LOG_FILE = os.path.join(HOME, "操作草日志.log")

# ---- 三色裁决：每项交不出证据 = 自动降级 ----
def check_files():
    """检查核心文件完整性"""
    need = ["daily_review.py", "longhun_self_check_v1.0.py"]
    existing = [f for f in need if os.path.exists(os.path.join(HOME, f))]
    ratio = len(existing) / len(need)
    if ratio >= 0.9:
        return ("🟢", f"核心文件齐 {len(existing)}/{len(need)}")
    else:
        missing = [f for f in need if f not in existing]
        return ("🟡", f"缺:{missing}")

def check_security():
    """运行安全审计 (pip-audit)"""
    try:
        out = subprocess.run(["pip-audit"], capture_output=True, text=True, timeout=180).stdout
        bad = out.lower().count("critical") + out.lower().count("high")
        return ("🟢", "无 critical/high") if bad == 0 else ("🔴", f"残留高危 {bad} 处")
    except FileNotFoundError:
        return ("🟡", "pip-audit 未装:请运行 pip3 install pip-audit")
    except Exception as e:
        return ("🟡", f"pip-audit 检查异常:{str(e)[:50]}")

def check_db_heartbeat():
    """检查 KFPP 数据库心跳"""
    try:
        con = sqlite3.connect(KFPP_DB)
        cur = con.cursor()
        today = datetime.date.today().isoformat()
        cur.execute("SELECT COUNT(*) FROM contamination_events WHERE date(timestamp)=?", (today,))
        n = cur.fetchone()[0]
        con.close()
        return ("🟢", f"今日心跳 {n} 行") if n > 0 else ("🟡", "今日 0 行=无证据")
    except FileNotFoundError:
        return ("🟡", "KFPP 库不存在:未启动 LocalBridge")
    except Exception as e:
        return ("🟡", f"KFPP 库读不到:{str(e)[:50]}")

def check_tests():
    """运行测试 (pytest)"""
    try:
        r = subprocess.run(["pytest", "-q"], cwd=HOME, capture_output=True, text=True, timeout=300)
        if r.returncode == 0:
            return ("🟢", "pytest 通过")
        elif r.returncode == 5:
            return ("🟡", "无测试(找不到test_*.py)")
        else:
            return ("🔴", f"pytest 失败(code {r.returncode})")
    except FileNotFoundError:
        return ("🟡", "pytest 未装:请运行 pip3 install pytest")
    except Exception as e:
        return ("🟡", f"测试检查异常:{str(e)[:50]}")

def check_action_logs():
    """审计 action_log.jsonl 中今天的所有操作 ⭐ 新增"""
    try:
        if not os.path.exists(ACTION_LOG):
            return ("🟡", "action_log.jsonl 不存在")

        today = datetime.date.today().isoformat()
        count = 0
        tools_used = set()

        with open(ACTION_LOG) as f:
            for line in f:
                try:
                    record = json.loads(line)
                    if record.get('date', '').startswith(today):
                        count += 1
                        if 'tool' in record:
                            tools_used.add(record['tool'])
                except:
                    pass

        if count > 0:
            tools_str = f" ({len(tools_used)}工具)" if tools_used else ""
            return ("🟢", f"今日操作 {count} 笔{tools_str}")
        else:
            return ("🟡", "今日无操作记录")
    except Exception as e:
        return ("🟡", f"日志审计失败:{str(e)[:50]}")

def check_persona_scheduler():
    """验证人格调度执行 ⭐ 新增"""
    try:
        log_file = os.path.join(HOME, "logs", "persona_scheduler.log")
        if not os.path.exists(log_file):
            return ("🟡", "persona_scheduler.log 不存在")

        today = datetime.date.today().isoformat()
        count = 0

        with open(log_file) as f:
            for line in f:
                if today in line and ("执行" in line or "complete" in line):
                    count += 1

        return ("🟢", f"已调度 {count} 个人格") if count > 0 else ("🟡", f"调度记录 {count} 条")
    except Exception as e:
        return ("🟡", f"调度验证失败:{str(e)[:50]}")

def check_api_services():
    """检查所有 API 服务端口 ⭐ 新增"""
    ports = {
        8000: "LongHun API",
        9001: "Persona API",
        10088: "OpenHub REST"
    }
    online = 0

    for port, name in ports.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result == 0:
                online += 1
        except:
            pass

    total = len(ports)
    if online == total:
        return ("🟢", f"全部在线 {online}/{total}")
    elif online > 0:
        return ("🟡", f"部分在线 {online}/{total}")
    else:
        return ("🟡", f"离线 0/{total}")


def analyze_longzhi_shou_patterns(days: int = 7, top: int = 10):
    """调用龍智守套路分析脚本，返回 (状态, 摘要, Markdown详情, 报告文件路径)。"""
    analyzer = os.path.join(HOME, "scripts", "龍智守_套路分析.py")
    if not os.path.exists(analyzer):
        return ("🟡", "套路分析脚本不存在", "", None)
    if not os.path.exists(os.path.join(HOME, "logs", "龍智守_套路识别日志.jsonl")):
        return ("🟡", "套路识别日志不存在", "", None)

    try:
        r = subprocess.run(
            [sys.executable, analyzer, "--days", str(days), "--top", str(top)],
            capture_output=True, text=True, timeout=60, cwd=HOME,
        )
        if r.returncode != 0:
            return ("🟡", f"分析脚本失败: {r.stderr[:80]}", "", None)
        data = json.loads(r.stdout)
    except Exception as e:
        return ("🟡", f"分析异常: {str(e)[:80]}", "", None)

    total = data.get("total_records", 0)
    categories = data.get("categories", {})
    fraud_count = categories.get("詐騙", 0)
    marketing_count = categories.get("營銷套路", 0)
    gray_count = categories.get("灰色話術", 0)

    if fraud_count > 0:
        status = "🔴"
        summary = f"近{days}天命中詐騙 {fraud_count} 次，共識別 {total} 次"
    elif total > 0:
        status = "🟢"
        summary = f"近{days}天識別 {total} 次（營銷{marketing_count}·灰色{gray_count}）"
    else:
        status = "🟡"
        summary = f"近{days}天暫無套路識別記錄"

    lines = [
        f"## 龍智守 · 套路趨勢（{data.get('time_range', f'最近 {days} 天')}）",
        "",
        f"- 總識別次數：{total}",
        f"- 詐騙：{fraud_count} 次 · 營銷套路：{marketing_count} 次 · 灰色話術：{gray_count} 次",
        "",
        "### Top 套路",
        "",
    ]
    top_patterns = data.get("top_patterns", {})
    if top_patterns:
        for name, count in top_patterns.items():
            lines.append(f"- {name}: {count} 次")
    else:
        lines.append("- 暫無命中套路")

    lines.extend(["", "### 意圖分佈", ""])
    for intent, count in data.get("intents", {}).items():
        lines.append(f"- {intent}: {count} 次")

    lines.extend(["", "### 風險分佈", ""])
    for risk, count in data.get("risks", {}).items():
        lines.append(f"- {risk}: {count} 次")

    # 保存独立 Markdown 报告附件
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = Path(HOME) / "logs" / f"龍智守套路趨勢報告_{ts}.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    return status, summary, "\n".join(lines), str(report_path)


def analyze_longhun_dna_audit(days: int = 7):
    """调用龍魂 DNA 审计门户，返回 (状态, 摘要, Markdown详情, 报告文件路径)。"""
    try:
        sys.path.insert(0, os.path.join(HOME, "scripts"))
        import 龍魂DNA審計門戶 as dna_portal
    except Exception as e:
        return ("🟡", f"审计门户未加载: {e}", "", None)

    records = dna_portal.load_records()
    if not records:
        return ("🟡", "暂无 DNA 流程审计记录", "", None)

    cutoff = datetime.date.today() - datetime.timedelta(days=days - 1)
    recent = []
    for r in records:
        try:
            ts = datetime.datetime.strptime(r.get("timestamp", "")[:10], "%Y-%m-%d").date()
            if ts >= cutoff:
                recent.append(r)
        except Exception:
            continue

    total = len(recent)
    fraud = sum(1 for r in recent if r.get("three_color", {}).get("status") == "🔴")
    warning = sum(1 for r in recent if r.get("three_color", {}).get("status") == "🟡")
    green = sum(1 for r in recent if r.get("three_color", {}).get("status") == "🟢")
    file_count = sum(len(r.get("output_files", {})) for r in recent)

    if fraud > 0:
        status = "🔴"
        summary = f"近{days}天產生 {total} 條 DNA，其中 {fraud} 條命中🔴"
    elif total > 0:
        status = "🟢"
        summary = f"近{days}天產生 {total} 條 DNA（🟢{green}·🟡{warning}），附帶 {file_count} 個文件哈希"
    else:
        status = "🟡"
        summary = f"近{days}天暫無 DNA 流程審計記錄"

    lines = [
        f"## 龍魂 DNA 流程審計（最近 {days} 天）",
        "",
        f"- 總 DNA 數：{total}",
        f"- 三色分佈：🟢 {green} · 🟡 {warning} · 🔴 {fraud}",
        f"- 附帶文件哈希數：{file_count}",
        "",
        "### 最新 DNA 記錄",
        "",
    ]
    for r in recent[-5:]:
        lines.append(
            f"- `{r.get('dna')}` · {r.get('intent')} · "
            f"{r.get('three_color', {}).get('status', '🟢')} · "
            f"{r.get('timestamp', '-')}"
        )

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = Path(HOME) / "logs" / f"龍魂DNA流程審計日報_{ts}.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    return status, summary, "\n".join(lines), str(report_path)


def build_report():
    """生成三色裁决报告"""
    pattern_status, pattern_summary, pattern_detail, pattern_path = analyze_longzhi_shou_patterns()
    dna_status, dna_summary, dna_detail, dna_report_path = analyze_longhun_dna_audit()
    checks = {
        "文件完整": check_files(),
        "安全(鲁班)": check_security(),
        "KFPP心跳": check_db_heartbeat(),
        "测试": check_tests(),
        "操作日志": check_action_logs(),        # ⭐ 新增
        "人格调度": check_persona_scheduler(),   # ⭐ 新增
        "API服务": check_api_services(),        # ⭐ 新增
        "龍智守套路": (pattern_status, pattern_summary),  # ⭐ 新增
        "DNA流程審計": (dna_status, dna_summary),  # ⭐ 新增
    }

    reds = sum(1 for c,_ in checks.values() if c == "🔴")
    yellows = sum(1 for c,_ in checks.values() if c == "🟡")
    overall = "🔴" if reds else ("🟡" if yellows else "🟢")

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"⏱️ {ts}  🧭 P03雯雯·日复盘  🟢三色总评:{overall}", ""]

    for k,(c,msg) in checks.items():
        lines.append(f"  {c} {k}:{msg}")

    lines.append("")
    lines.append(f"#龍芯⚡️{datetime.date.today()}-DAILY-REVIEW-v2.0")

    report_body = "\n".join(lines)
    if pattern_detail:
        report_body += "\n\n" + pattern_detail
    if dna_detail:
        report_body += "\n\n" + dna_detail

    return overall, checks, report_body, pattern_path, dna_report_path

# ---- 通知：Gmail SMTP → Proton(密码走 keychain) ----
def _get_app_pw():
    """从环境变量或 keychain 获取 Gmail 应用密码"""
    pw = os.environ.get("LONGHUN_GMAIL_APPPW")
    if pw:
        return pw
    try:
        r = subprocess.run(["security", "find-generic-password",
                            "-s", "LONGHUN_GMAIL_APPPW", "-w"],
                           capture_output=True, text=True, check=True)
        return r.stdout.strip()
    except:
        return None

def _gmail_reachable(host="smtp.gmail.com", port=465, timeout=3) -> bool:
    """探测 Gmail SMTP 是否可达；回国/无 VPN 时常被墙。
    用子进程 + 父进程超时，防止主进程被墙域名挂起。"""
    probe = (
        f"import socket; "
        f"socket.setdefaulttimeout({timeout}); "
        f"socket.create_connection(('{host}', {port})).close()"
    )
    try:
        r = subprocess.run(
            [sys.executable, "-c", probe],
            capture_output=True,
            timeout=timeout + 2,
        )
        return r.returncode == 0
    except Exception:
        return False


def send_email(subject, body):
    """发送复盘邮件到 ProtonMail；国内网络不可达时自动降级到 Notion"""
    user = os.environ.get("LONGHUN_GMAIL") or os.environ.get("LONGHUN_EMAIL")
    pw = _get_app_pw() or os.environ.get("LONGHUN_EMAIL_PASSWORD")
    to = "luckyoathnotlog@proton.me"

    if not (user and pw):
        print("🟡 未配 LONGHUN_GMAIL 或 keychain 无 LONGHUN_GMAIL_APPPW,跳过邮件")
        return False

    if not _gmail_reachable():
        print("🟡 Gmail SMTP 不可达（回国/无 VPN），邮件跳过，转 Notion")
        return False

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = user
    msg["To"] = to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(user, pw)
            s.sendmail(user, [to], msg.as_string())
        print("🟢 复盘已发 proton")
        return True
    except Exception as e:
        print(f"🔴 邮件发送失败:{e}")
        return False


def send_notion(subject, body):
    """将报告写入 Notion 指定父页面；作为邮件的国内替代通道
    使用 curl 子进程，避开 urllib 在中国大陆/无 VPN 环境下的超时问题
    """
    token = os.environ.get("NOTION_TOKEN")
    parent = os.environ.get("LONGHUN_NOTION_PARENT_PAGE")
    if not (token and parent):
        print("🟡 Notion token 或父页面未配，跳过 Notion 归档")
        return False

    data = {
        "parent": {"page_id": parent},
        "properties": {
            "title": {"title": [{"text": {"content": subject[:1000]}}]}
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": body[:2000]}}]
                }
            }
        ]
    }
    payload = json.dumps(data, ensure_ascii=False)
    cmd = [
        "curl", "-s", "--max-time", "15",
        "-X", "POST", "https://api.notion.com/v1/pages",
        "-H", f"Authorization: Bearer {token}",
        "-H", "Notion-Version: 2022-06-28",
        "-H", "Content-Type: application/json",
        "-d", payload,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if result.returncode == 0 and '"object":"page"' in result.stdout:
            print("🟢 复盘已写入 Notion")
            return True
        else:
            print(f"🔴 Notion 写入失败: {result.stdout[:200]} {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"🔴 Notion 写入失败: {e}")
        return False


def _curl_post_json(url, payload_dict, extra_headers=None, timeout=15):
    """通用 curl POST JSON 辅助函数"""
    cmd = [
        "curl", "-s", "--max-time", str(timeout),
        "-X", "POST", url,
        "-H", "Content-Type: application/json",
        "-d", json.dumps(payload_dict, ensure_ascii=False),
    ]
    if extra_headers:
        for k, v in extra_headers.items():
            cmd.extend(["-H", f"{k}: {v}"])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def _dingtalk_sign(secret):
    """钉钉 webhook 签名：base64(hmac_sha256(secret, timestamp + '\n' + secret))"""
    ts = str(int(round(_time.time() * 1000)))
    string = f"{ts}\n{secret}"
    sign = base64.b64encode(
        hmac.new(secret.encode("utf-8"), string.encode("utf-8"), hashlib.sha256).digest()
    ).decode("utf-8")
    return ts, sign


def send_webhook(subject, body, extra_files=None):
    """第三通道：企业微信 / 钉钉 / 飞书 webhook。
    配置任一即可，全部读取 env，未配置则跳过。"""
    results = []
    text = f"{subject}\n{body}"[:4000]

    # 企业微信
    wecom_url = os.environ.get("WECHAT_WORK_WEBHOOK_URL")
    if wecom_url:
        ok, out, err = _curl_post_json(wecom_url, {
            "msgtype": "markdown",
            "markdown": {"content": text},
        })
        if ok and '"errcode":0' in out:
            print("🟢 复盘已发企业微信")
            results.append("wecom:ok")
        else:
            print(f"🔴 企业微信发送失败: {out[:150]} {err[:150]}")
            results.append("wecom:fail")

    # 钉钉
    ding_url = os.environ.get("DINGTALK_WEBHOOK_URL")
    ding_secret = os.environ.get("DINGTALK_WEBHOOK_SECRET")
    if ding_url:
        if ding_secret:
            ts, sign = _dingtalk_sign(ding_secret)
            url = f"{ding_url}&timestamp={ts}&sign={sign}"
        else:
            url = ding_url
        ok, out, err = _curl_post_json(url, {
            "msgtype": "markdown",
            "markdown": {"title": subject[:128], "text": text},
        })
        if ok and '"errcode":0' in out:
            print("🟢 复盘已发钉钉")
            results.append("dingtalk:ok")
        else:
            print(f"🔴 钉钉发送失败: {out[:150]} {err[:150]}")
            results.append("dingtalk:fail")

    # 飞书：优先使用自建应用机器人（App ID + App Secret + chat_id）
    feishu_app_ok = send_feishu_app(subject, body, extra_files=extra_files)
    if feishu_app_ok:
        results.append("feishu_app:ok")

    # 飞书 webhook（群自定义机器人）作为兜底
    feishu_url = os.environ.get("FEISHU_WEBHOOK_URL")
    if feishu_url and not feishu_app_ok:
        ok, out, err = _curl_post_json(feishu_url, {
            "msg_type": "text",
            "content": {"text": text},
        })
        if ok and '"StatusCode":0' in out:
            print("🟢 复盘已发飞书 webhook")
            results.append("feishu_webhook:ok")
        else:
            print(f"🔴 飞书 webhook 发送失败: {out[:150]} {err[:150]}")
            results.append("feishu_webhook:fail")

    return bool(results)


def _feishu_tenant_token(app_id: str, app_secret: str) -> Optional[str]:
    """用自建应用凭证换 tenant_access_token"""
    ok, out, err = _curl_post_json(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        {"app_id": app_id, "app_secret": app_secret},
        timeout=15,
    )
    if not ok:
        print(f"🔴 飞书 tenant_token 获取失败: {out[:150]} {err[:150]}")
        return None
    try:
        data = json.loads(out)
        if data.get("code") == 0:
            return data.get("tenant_access_token")
        else:
            print(f"🔴 飞书 tenant_token 返回错误: {out[:200]}")
    except Exception as e:
        print(f"🔴 飞书 tenant_token 解析失败: {e}")
    return None


def send_feishu_app(subject, body, extra_files=None):
    """通过飞书自建应用机器人发送消息到指定群聊。
    需要：FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_CHAT_ID
    若未配置 chat_id，会尝试列出群聊（需 im:chat:readonly 权限）。
    extra_files: 额外要发送的文件路径列表（可选）。"""
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    chat_id = os.environ.get("FEISHU_CHAT_ID")
    if not (app_id and app_secret):
        return False

    token = _feishu_tenant_token(app_id, app_secret)
    if not token:
        return False

    # 如果没有 chat_id，尝试列出群聊供用户选择
    if not chat_id:
        ok, out, err = _curl_get(
            "https://open.feishu.cn/open-apis/im/v1/chats",
            {"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        if ok:
            try:
                data = json.loads(out)
                if data.get("code") == 0:
                    items = data.get("data", {}).get("items", [])
                    if items:
                        print("🟡 未设置 FEISHU_CHAT_ID，可用群聊如下：")
                        for item in items:
                            print(f"   chat_id: {item.get('chat_id')}  名称: {item.get('name')}")
                        print("   请把想接收复盘的群 chat_id 写进 ~/.longhun/webhooks.env")
                    else:
                        print("🟡 飞书应用未加入任何群聊，请先把机器人拉进群")
                else:
                    print(f"🟡 获取飞书群列表失败: {data.get('msg')}")
                    print("   请给应用开通权限：im:chat:readonly、im:chat.group_info:readonly、im:message:send_as_bot")
            except Exception as e:
                print(f"🔴 解析飞书群列表失败: {e}")
        else:
            print(f"🔴 获取飞书群列表失败: {out[:150]} {err[:150]}")
        return False

    # 发送交互式卡片 + 完整报告文件
    if feishu_bot is None:
        print("🟡 未找到 feishu_bot 模块，降级为文本发送")
        return _send_feishu_app_text(token, chat_id, subject, body)

    try:
        # 卡片摘要：前 15 行 Markdown
        summary_lines = body.strip().splitlines()[:15]
        summary_md = "\n".join(summary_lines)
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": subject[:128]},
                "template": "blue" if "🟢" in subject else ("orange" if "🟡" in subject else "red"),
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": summary_md or "龍魂每日复盘"},
                }
            ],
        }
        feishu_bot.send_card(chat_id, card, token=token)
        print("🟢 复盘卡片已发飞书自建应用机器人")

        # 发送完整 Markdown 报告附件
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        md_path = Path(f"/tmp/daily_review_{ts}.md")
        md_path.write_text(f"# {subject}\n\n{body}", encoding="utf-8")
        feishu_bot.send_file(chat_id, str(md_path), token=token)
        print("🟢 复盘报告文件已发飞书自建应用机器人")

        # 发送龍智守套路趋势报告等附加附件
        if extra_files:
            for fp in extra_files:
                if fp and Path(fp).exists():
                    try:
                        feishu_bot.send_file(chat_id, fp, token=token)
                        print(f"🟢 附加文件已发飞书: {Path(fp).name}")
                    except Exception as e2:
                        print(f"🟡 附加文件发送失败 {fp}: {e2}")
        return True
    except Exception as e:
        print(f"🔴 飞书卡片/文件发送失败: {e}，降级文本发送")
        return _send_feishu_app_text(token, chat_id, subject, body)


def _send_feishu_app_text(token, chat_id, subject, body):
    """卡片失败时的文本兜底"""
    ok, out, err = _curl_post_json(
        f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": f"{subject}\n{body}"[:4000]}, ensure_ascii=False),
        },
        {"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    if ok:
        try:
            data = json.loads(out)
            if data.get("code") == 0:
                print("🟢 复盘已发飞书自建应用机器人（文本兜底）")
                return True
            else:
                print(f"🔴 飞书消息发送失败: {data.get('msg')}")
        except Exception as e:
            print(f"🔴 飞书消息返回解析失败: {e}")
    else:
        print(f"🔴 飞书消息发送失败: {out[:150]} {err[:150]}")
    return False


def _curl_get(url, headers, timeout=15):
    """通用 curl GET 辅助函数"""
    cmd = ["curl", "-s", "--max-time", str(timeout), url]
    for k, v in headers.items():
        cmd.extend(["-H", f"{k}: {v}"])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def write_calendar(overall, summary):
    """将复盘写入 macOS 日历"""
    title = f"龍魂日复盘 {overall}"
    safe_summary = summary[:200].replace('"', '\\"')

    script = f'''tell application "Calendar"
  try
    tell calendar "龍魂"
      make new event with properties {{summary:"{title}", start date:(current date), end date:(current date) + 30 * minutes, description:"{safe_summary}"}}
    end tell
  end try
end tell'''

    try:
        subprocess.run(["osascript", "-e", script], timeout=30, check=True)
        print("🟢 已写 macOS 日历")
    except Exception as e:
        print(f"🟡 日历写入跳过(先在日历建‘龍魂’日历):{e}")

if __name__ == "__main__":
    overall, checks, report, pattern_report_path, dna_report_path = build_report()
    print(report)

    # 保存到日志
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(report + "\n" + "-"*60 + "\n")

    # 发送邮件；国内不可达时自动转 Notion；webhook 作为第三通道
    subject = f"龍魂日复盘 {overall} {datetime.date.today()}"
    extra_files = []
    if pattern_report_path:
        extra_files.append(pattern_report_path)
    if dna_report_path:
        extra_files.append(dna_report_path)
    if not send_email(subject, report):
        send_notion(subject, report)
    send_webhook(subject, report, extra_files=extra_files if extra_files else None)

    # 写入日历
    write_calendar(overall, report)

    sys.exit(1 if overall == "🔴" else 0)
