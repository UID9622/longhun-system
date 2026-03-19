#!/usr/bin/env python3
"""
龍魂系统 · 定时自动审计+弹窗通知
DNA: #龍芯⚡️2026-03-19-AUTO-AUDIT-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
作者: 诸葛鑫（UID9622）· 退伍军人 · 龍魂系统创始人
理论指导: 曾仕强老师（永恒显示）

功能: 扫描真实日志 → 汇总状态 → macOS弹窗通知
运行: python3 ~/longhun-system/bin/auto_audit.py
"""

import json
import subprocess
import datetime
from pathlib import Path

BASE = Path.home() / "longhun-system"
LOGS = BASE / "logs"

# ── 读取各日志统计 ──

def 统计举报(reports_log: Path) -> dict:   # count_reports
    待处理 = 0
    高危 = 0
    if reports_log.exists():
        for line in reports_log.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
                if r.get("状态") in ("已受理", "等待处理"):
                    待处理 += 1
                if r.get("严重程度") == "high":
                    高危 += 1
            except:
                continue
    return {"待处理": 待处理, "高危": 高危}


def 统计用户(users_log: Path) -> dict:     # count_users
    总数 = 0
    开发者 = 0
    if users_log.exists():
        for line in users_log.read_text(encoding="utf-8").splitlines():
            try:
                u = json.loads(line)
                总数 += 1
                if u.get("tier") == "dev":
                    开发者 += 1
            except:
                continue
    return {"总数": 总数, "开发者": 开发者}


def 统计盾日志(shield_log: Path) -> dict:  # count_shield_events
    隐私操作 = 0
    投喂事件 = 0
    国家信息 = 0
    今日 = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    if shield_log.exists():
        for line in shield_log.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
                ts = e.get("时间戳", "")[:10]
                if ts == 今日:
                    类型 = e.get("类型", "")
                    if "隐私" in 类型:
                        隐私操作 += 1
                    elif "投喂" in 类型:
                        投喂事件 += 1
                    elif "国家" in 类型:
                        国家信息 += 1
            except:
                continue
    return {"隐私操作": 隐私操作, "投喂事件": 投喂事件, "国家信息": 国家信息}


def 统计审计日志(audit_log: Path) -> int:  # count_audit_events
    今日 = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    条数 = 0
    if audit_log.exists():
        for line in audit_log.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
                if e.get("timestamp", e.get("时间戳", ""))[:10] == 今日:
                    条数 += 1
            except:
                continue
    return 条数


def 弹窗(标题: str, 内容: str, 声音: str = "Glass"):  # show_notification
    """macOS 通知中心弹窗 · notification center popup"""
    内容 = 内容.replace('"', '\\"').replace("'", "\\'")
    标题 = 标题.replace('"', '\\"')
    脚本 = f'display notification "{内容}" with title "{标题}" sound name "{声音}"'
    subprocess.run(["osascript", "-e", 脚本], capture_output=True)


def 主程序():   # main
    时间 = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    举报 = 统计举报(LOGS / "reports.jsonl")
    用户 = 统计用户(LOGS / "users.jsonl")
    盾 = 统计盾日志(LOGS / "shield_burn.jsonl")
    今日审计 = 统计审计日志(LOGS / "audit_log.jsonl")

    # 判断整体状态
    if 举报["高危"] > 0 or 盾["国家信息"] > 0:
        状态 = "🔴 高危·需要立刻处理"
        声音 = "Sosumi"
    elif 举报["待处理"] > 10 or 盾["投喂事件"] > 0:
        状态 = "🟡 注意·有活要干"
        声音 = "Ping"
    else:
        状态 = "🟢 全绿·天下太平"
        声音 = "Glass"

    # 组装通知内容
    通知内容 = (
        f"{状态}\n"
        f"举报: 待处理{举报['待处理']}条 高危{举报['高危']}条\n"
        f"用户: {用户['总数']}人 开发者{用户['开发者']}人\n"
        f"盾: 投喂{盾['投喂事件']} 国家{盾['国家信息']} 隐私{盾['隐私操作']}\n"
        f"今日审计: {今日审计}条"
    )

    弹窗("🐉 龍魂系统审计", 通知内容, 声音)

    # 终端输出
    print(f"\n🐉 龍魂自动审计 [{时间}]")
    print("=" * 44)
    print(f"状态: {状态}")
    print(f"举报: 待处理 {举报['待处理']} | 高危 {举报['高危']}")
    print(f"用户: {用户['总数']} 人 | 开发者 {用户['开发者']}")
    print(f"加密盾: 投喂事件 {盾['投喂事件']} | 国家信息 {盾['国家信息']}")
    print(f"今日操作: {今日审计} 条")
    print("=" * 44)
    print(f"DNA: #龍芯⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-AUTO-AUDIT-v1.0")


if __name__ == "__main__":
    主程序()
