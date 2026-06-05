#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""龍魂每日复盘 · P03雯雯主理 / P04鲁班安全 / P05上帝之眼裁决
DNA: #龍芯⚡️2026-06-05-DAILY-REVIEW-v1.0
"""
import os, sys, json, smtplib, subprocess, datetime, sqlite3
from email.mime.text import MIMEText
from email.header import Header
from pathlib import Path

HOME = os.path.expanduser("~/longhun-system")
KFPP_DB = os.path.expanduser("~/.龍魂/kfpp/kfpp_execution.db")
LOG = os.path.join(HOME, "操作草日志.log")

# ---- 三色裁决:每项交不出证据 = 自动降级 ----
def check_files():
    need = ["daily_review.py", "longhun_self_check_v1.0.py"]
    existing = [f for f in need if os.path.exists(os.path.join(HOME, f))]
    return ("🟢", f"核心文件齐 {len(existing)}/{len(need)}") if len(existing) >= len(need)-1 else ("🟡", f"缺:{[f for f in need if f not in existing]}")

def check_security():
    try:
        out = subprocess.run(["pip-audit"], capture_output=True, text=True, timeout=180).stdout
        bad = out.lower().count("critical") + out.lower().count("high")
        return ("🟢", "无 critical/high") if bad == 0 else ("🔴", f"残留高危 {bad} 处")
    except Exception as e:
        return ("🟡", f"pip-audit 未装:{e}")

def check_db_heartbeat():
    try:
        con = sqlite3.connect(KFPP_DB)
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM contamination_events WHERE date(timestamp)=date('now','localtime')")
        n = cur.fetchone()[0]
        con.close()
        return ("🟢", f"今日心跳 {n} 行") if n > 0 else ("🟡", "今日 0 行=无证据")
    except Exception as e:
        return ("🟡", f"KFPP 库读不到:{e}")

def check_tests():
    try:
        r = subprocess.run(["pytest", "-q"], cwd=HOME, capture_output=True, text=True, timeout=300)
        if r.returncode == 0:
            return ("🟢", "pytest 通过")
        elif r.returncode == 5:
            # pytest 找不到测试文件 = 项目无测试,非失败
            return ("🟡", "无测试(找不到test_*.py)")
        else:
            # 其他非0码 = 真正失败
            return ("🔴", f"pytest 失败(code {r.returncode})")
    except FileNotFoundError:
        return ("🟡", "pytest 未装")
    except Exception as e:
        return ("🟡", f"测试检查异常:{e}")

def build_report():
    checks = {
        "文件完整": check_files(),
        "安全(鲁班)": check_security(),
        "KFPP心跳": check_db_heartbeat(),
        "测试": check_tests(),
    }
    reds = sum(1 for c,_ in checks.values() if c == "🔴")
    yellows = sum(1 for c,_ in checks.values() if c == "🟡")
    overall = "🔴" if reds else ("🟡" if yellows else "🟢")
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"⏱️ {ts}  🧭 P03雯雯·日复盘  🟢三色总评:{overall}", ""]
    for k,(c,msg) in checks.items():
        lines.append(f"  {c} {k}:{msg}")
    lines.append("")
    lines.append(f"#龍芯⚡️{datetime.date.today()}-DAILY-REVIEW")
    return overall, "\n".join(lines)

# ---- 通知:Gmail SMTP → proton(密码走 keychain,不入 git) ----
def _get_app_pw():
    # 先看环境变量,再从 keychain 取 —— 明文永不落 plist/git
    pw = os.environ.get("LONGHUN_GMAIL_APPPW")
    if pw:
        return pw
    try:
        r = subprocess.run(["security", "find-generic-password",
                            "-s", "LONGHUN_GMAIL_APPPW", "-w"],
                           capture_output=True, text=True, check=True)
        return r.stdout.strip()
    except Exception:
        return None

def send_email(subject, body):
    user = os.environ.get("LONGHUN_GMAIL")          # 例:baofuahao@gmail.com
    pw   = _get_app_pw()                            # 先环境变量,再 keychain
    to   = "luckyoathnotlog@proton.me"
    if not (user and pw):
        print("🟡 未配 LONGHUN_GMAIL 或 keychain 无 LONGHUN_GMAIL_APPPW,跳过邮件"); return
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8"); msg["From"] = user; msg["To"] = to
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(user, pw)
            s.sendmail(user, [to], msg.as_string())
        print("🟢 复盘已发 proton")
    except Exception as e:
        print(f"🔴 邮件发送失败:{e}")

# ---- 日历:写进 macOS 日历(AppleScript) ----
def write_calendar(overall, summary):
    title = f"龍魂日复盘 {overall}"
    script = f'''tell application "Calendar"
  try
    tell calendar "龍魂"
      make new event with properties {{summary:"{title}", start date:(current date), end date:(current date) + 30 * minutes, description:"{summary[:200]}"}}
    end tell
  end try
end tell'''
    try:
        subprocess.run(["osascript", "-e", script], timeout=30, check=True)
        print("🟢 已写 macOS 日历")
    except Exception as e:
        print(f"🟡 日历写入跳过(先在日历建『龍魂』日历):{e}")

if __name__ == "__main__":
    overall, report = build_report()
    print(report)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(report + "\n" + "-"*40 + "\n")
    send_email(f"龍魂日复盘 {overall} {datetime.date.today()}", report)
    write_calendar(overall, report)
    sys.exit(1 if overall == "🔴" else 0)
