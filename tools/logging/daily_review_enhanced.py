#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""龍魂每日复盘增强版 · P03雯雯主理 / P04鲁班安全 / P05上帝之眼裁决
DNA:#龍芯⚡️2026-06-09-DAILY-REVIEW-ENHANCED-v2.0
增强功能: 完整日志审计·操作统计·人格调度验证·API服务检查
"""
import os, sys, json, smtplib, subprocess, datetime, sqlite3, socket
from email.mime.text import MIMEText
from email.header import Header
from pathlib import Path

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
        8000: "Longhun API",
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

def build_report():
    """生成三色裁决报告"""
    checks = {
        "文件完整": check_files(),
        "安全(鲁班)": check_security(),
        "KFPP心跳": check_db_heartbeat(),
        "测试": check_tests(),
        "操作日志": check_action_logs(),        # ⭐ 新增
        "人格调度": check_persona_scheduler(),   # ⭐ 新增
        "API服务": check_api_services(),        # ⭐ 新增
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

    return overall, checks, "\n".join(lines)

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

def send_email(subject, body):
    """发送复盘邮件到 ProtonMail"""
    user = os.environ.get("LONGHUN_GMAIL")
    pw = _get_app_pw()
    to = "luckyoathnotlog@proton.me"

    if not (user and pw):
        print("🟡 未配 LONGHUN_GMAIL 或 keychain 无 LONGHUN_GMAIL_APPPW,跳过邮件")
        return

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = user
    msg["To"] = to

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(user, pw)
            s.sendmail(user, [to], msg.as_string())
        print("🟢 复盘已发 proton")
    except Exception as e:
        print(f"🔴 邮件发送失败:{e}")

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
    overall, checks, report = build_report()
    print(report)

    # 保存到日志
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(report + "\n" + "-"*60 + "\n")

    # 发送邮件
    send_email(f"龍魂日复盘 {overall} {datetime.date.today()}", report)

    # 写入日历
    write_calendar(overall, report)

    sys.exit(1 if overall == "🔴" else 0)
