# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·丙辰·己丑·需-DESIRE-INVERTED-GROWTH-v1.0-0248CF46
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂·欲望倒逼成长引擎 v1.0
以欲为饵·逼人向上
DNA: #龍芯⚡️丙午·丙申·丙辰·己丑·需-DESIRE-INVERTED-GROWTH-v1.0-0248CF46
"""
import json, os, sys, hashlib, time
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".龍魂" / "desire_growth"
DATA_DIR.mkdir(parents=True, exist_ok=True)

TASKS_FILE = DATA_DIR / "tasks.json"
SCORES_FILE = DATA_DIR / "scores.json"
LOG_FILE = DATA_DIR / "log.jsonl"

# ── 六类任务权重 ──
TASK_TYPES = {
    "knowledge": {"name": "知识学习", "weight": 1.0, "icon": "📚"},
    "skill":     {"name": "技能训练", "weight": 1.2, "icon": "💻"},
    "reality":   {"name": "现实KPI", "weight": 1.5, "icon": "🎯"},
    "health":    {"name": "身体健康", "weight": 1.0, "icon": "💪"},
    "family":    {"name": "家庭责任", "weight": 1.5, "icon": "👨‍👩‍👧"},
    "contribute":{"name": "社会贡献", "weight": 1.3, "icon": "🌍"},
}

# ── 体验等级 ──
TIERS = [
    {"level": 0, "name": "基础", "min_score": 0,    "unlocks": "基础AI对话"},
    {"level": 1, "name": "入门", "min_score": 10,   "unlocks": "AI私教辅导 + 知识卡片"},
    {"level": 2, "name": "进阶", "min_score": 50,   "unlocks": "3D沉浸场景 + 深度交互"},
    {"level": 3, "name": "高级", "min_score": 150,  "unlocks": "全感官体验(嗅觉+触觉) + 专属人格"},
    {"level": 4, "name": "顶级", "min_score": 500,  "unlocks": "私人定制感官舱 + 社区荣誉"},
    {"level": 5, "name": "传奇", "min_score": 2000, "unlocks": "一切解锁 + 许愿池额度 + 信任积分簿白名单"},
]

# ── 每日体验限制 ──
MAX_DAILY_UNLOCKS = 3
MAX_SESSION_MINUTES = 45
COOLDOWN_MINUTES = 30

def _load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}

def _save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def _log(user_id, action, detail=""):
    entry = {
        "ts": datetime.now().isoformat(),
        "user": user_id,
        "action": action,
        "detail": detail,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def register_task(user_id, task_type, title, difficulty=1):
    """登记一个成长任务"""
    if task_type not in TASK_TYPES:
        return f"❌ 未知任务类型: {task_type}。可选: {', '.join(TASK_TYPES.keys())}"

    tasks = _load_json(TASKS_FILE)
    uid = user_id.upper()

    task_id = hashlib.sha256(f"{uid}{title}{time.time()}".encode()).hexdigest()[:12]

    if uid not in tasks:
        tasks[uid] = []

    tasks[uid].append({
        "id": task_id,
        "type": task_type,
        "title": title,
        "difficulty": max(1, min(5, difficulty)),
        "status": "pending",
        "created": datetime.now().isoformat(),
        "completed": None,
    })
    _save_json(TASKS_FILE, tasks)
    _log(uid, "register_task", f"{task_type}:{title}")

    tp = TASK_TYPES[task_type]
    expected_score = difficulty * tp["weight"] * 10
    return (
        f"📋 任务已登记\n"
        f"   ID: {task_id}\n"
        f"   类型: {tp['icon']} {tp['name']}\n"
        f"   内容: {title}\n"
        f"   难度: {'⭐'*difficulty}\n"
        f"   预期积分: +{expected_score:.0f}"
    )

def complete_task(user_id, task_id, quality=1.0):
    """完成任务，获得积分。quality ∈ [0, 1]，作弊=0"""
    tasks = _load_json(TASKS_FILE)
    uid = user_id.upper()

    if uid not in tasks:
        return "❌ 没有找到你的任务。先用 register_task 登记。"

    for t in tasks[uid]:
        if t["id"] == task_id and t["status"] == "pending":
            tp = TASK_TYPES[t["type"]]
            score = t["difficulty"] * tp["weight"] * 10 * quality
            t["status"] = "done"
            t["completed"] = datetime.now().isoformat()
            t["score"] = score
            _save_json(TASKS_FILE, tasks)

            # 累积积分
            scores = _load_json(SCORES_FILE)
            if uid not in scores:
                scores[uid] = {"total": 0, "by_type": {}, "history": []}
            scores[uid]["total"] += score
            scores[uid]["by_type"][t["type"]] = scores[uid]["by_type"].get(t["type"], 0) + score
            scores[uid]["history"].append({
                "task_id": task_id,
                "type": t["type"],
                "title": t["title"],
                "score": score,
                "ts": datetime.now().isoformat(),
            })
            _save_json(SCORES_FILE, scores)
            _log(uid, "complete_task", f"{task_id} +{score:.0f}")

            current_tier = _get_tier(scores[uid]["total"])
            return (
                f"✅ 任务完成！\n"
                f"   {tp['icon']} {t['title']}\n"
                f"   +{score:.0f} 积分 (质量={quality*100:.0f}%)\n"
                f"   当前总分: {scores[uid]['total']:.0f}\n"
                f"   当前等级: Lv.{current_tier['level']} {current_tier['name']}\n"
                f"   已解锁: {current_tier['unlocks']}\n"
                f"   下一级还差: {_next_tier_gap(scores[uid]['total'])}"
            )

    return "❌ 未找到该任务或已完成。"

def _get_tier(score):
    current = TIERS[0]
    for t in TIERS:
        if score >= t["min_score"]:
            current = t
    return current

def _next_tier_gap(score):
    for t in TIERS:
        if score < t["min_score"]:
            return f"{t['min_score'] - score:.0f} 分 → Lv.{t['level']} {t['name']}"
    return "已是最高等级 🏆"

def check_balance(user_id):
    """查看用户积分余额"""
    scores = _load_json(SCORES_FILE)
    uid = user_id.upper()

    if uid not in scores:
        return "📊 还没有积分。先用 register_task + complete_task 开始赚积分吧。"

    s = scores[uid]
    tier = _get_tier(s["total"])

    lines = [
        f"📊 {uid} 积分报告",
        f"",
        f"   🏆 等级: Lv.{tier['level']} {tier['name']}",
        f"   💰 总积分: {s['total']:.1f}",
        f"   🔓 已解锁: {tier['unlocks']}",
        f"   📈 下一级: {_next_tier_gap(s['total'])}",
        f"",
        f"   分类积分:",
    ]
    for k, v in sorted(s.get("by_type", {}).items(), key=lambda x: x[1], reverse=True):
        tp = TASK_TYPES.get(k, {"icon": "❓", "name": k})
        lines.append(f"     {tp['icon']} {tp['name']}: {v:.1f}")

    lines.append(f"")
    lines.append(f"   完成任务数: {len(s.get('history', []))}")

    # 今日已解锁次数
    today = datetime.now().strftime("%Y-%m-%d")
    today_unlocks = sum(1 for h in s.get("unlock_history", []) if h.get("date") == today)
    lines.append(f"   今日已解锁: {today_unlocks}/{MAX_DAILY_UNLOCKS}")

    return "\n".join(lines)

def unlock_experience(user_id, experience_name):
    """尝试解锁体验"""
    scores = _load_json(SCORES_FILE)
    uid = user_id.upper()

    if uid not in scores:
        return "❌ 没有积分。先完成任务赚积分。"

    s = scores[uid]
    today = datetime.now().strftime("%Y-%m-%d")

    if "unlock_history" not in s:
        s["unlock_history"] = []

    today_unlocks = sum(1 for h in s["unlock_history"] if h.get("date") == today)
    if today_unlocks >= MAX_DAILY_UNLOCKS:
        return f"🛑 今日已解锁 {MAX_DAILY_UNLOCKS} 次，已达上限。明天再来。"

    # 模拟消耗积分解锁
    cost = 10  # 基础解锁消耗
    if s["total"] < cost:
        return f"❌ 积分不足。解锁「{experience_name}」需要 {cost} 积分，当前 {s['total']:.0f}。"

    s["total"] -= cost
    s["unlock_history"].append({
        "experience": experience_name,
        "cost": cost,
        "date": today,
        "ts": datetime.now().isoformat(),
    })
    _save_json(SCORES_FILE, s)
    _log(uid, "unlock_experience", f"{experience_name} -{cost}")

    tier = _get_tier(s["total"])
    return (
        f"🔓 体验已解锁！\n"
        f"   「{experience_name}」\n"
        f"   消耗: -{cost} 积分\n"
        f"   剩余积分: {s['total']:.0f}\n"
        f"   等级: Lv.{tier['level']} {tier['name']}\n"
        f"   今日剩余解锁: {MAX_DAILY_UNLOCKS - today_unlocks - 1} 次"
    )

def status():
    """引擎状态"""
    tasks = _load_json(TASKS_FILE)
    scores = _load_json(SCORES_FILE)

    total_users = len(scores)
    total_tasks = sum(len(v) for v in tasks.values())
    done_tasks = sum(1 for v in tasks.values() for t in v if t["status"] == "done")
    pending_tasks = total_tasks - done_tasks

    return (
        f"🧬 欲望倒逼成长引擎 v1.0\n"
        f"   DNA: #龍芯⚡️丙午·丙申·丙辰·己丑·需-DESIRE-INVERTED-GROWTH-v1.0-0248CF46\n"
        f"   用户数: {total_users}\n"
        f"   总任务: {total_tasks} (已完成 {done_tasks} | 待完成 {pending_tasks})\n"
        f"   数据目录: {DATA_DIR}"
    )

# ── CLI ──
def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  register <用户ID> <类型> <任务描述> [难度1-5]    登记任务")
        print("  complete <用户ID> <任务ID> [质量0-1]               完成任务")
        print("  balance <用户ID>                                   查看积分")
        print("  unlock <用户ID> <体验名称>                          解锁体验")
        print("  status                                             引擎状态")
        print("")
        print("任务类型:", ", ".join(f"{v['icon']}{k}" for k, v in TASK_TYPES.items()))
        return

    cmd = sys.argv[1]

    if cmd == "register" and len(sys.argv) >= 5:
        uid = sys.argv[2]
        ttype = sys.argv[3]
        title = sys.argv[4]
        diff = int(sys.argv[5]) if len(sys.argv) >= 6 else 1
        print(register_task(uid, ttype, title, diff))

    elif cmd == "complete" and len(sys.argv) >= 4:
        uid = sys.argv[2]
        tid = sys.argv[3]
        quality = float(sys.argv[4]) if len(sys.argv) >= 5 else 1.0
        print(complete_task(uid, tid, quality))

    elif cmd == "balance" and len(sys.argv) >= 3:
        print(check_balance(sys.argv[2]))

    elif cmd == "unlock" and len(sys.argv) >= 4:
        print(unlock_experience(sys.argv[2], sys.argv[3]))

    elif cmd == "status":
        print(status())

    else:
        print(f"❌ 未知命令: {cmd}")

if __name__ == "__main__":
    main()
