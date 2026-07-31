# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_QIYE_DENG-v1.0-4b72ad6f
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍芯企业灯·三生三世引擎 v2.0
================================
前生灯(镜) → 今世灯(秤) → 未来灯(路)
基于 LoongArch + KaihongOS 全栈自主底座

用法:
    # 前生灯·因果追溯
    python3 bin/lh_qiye_deng.py qiansheng 0.5 0.7 0.9 0.3 0.6     # 5个历史节点权重
    python3 bin/lh_qiye_deng.py qiansheng-chain "战略失误=0.9" "激励失效=0.7" "执行断层=0.5" "现金流断裂=0.8"

    # 今世灯·压力指数
    python3 bin/lh_qiye_deng.py jinshi 7 5 6 8 4                     # F/T/M/D/P 五维分
    python3 bin/lh_qiye_deng.py jinshi-health 800000 450000 6 85 12  # 人效/行业均值/现金流/留存率/增速

    # 未来灯·路径推演
    python3 bin/lh_qiye_deng.py weilai 0.7 0.6 0.8 0.5 --path A     # 现金流/市场/团队/杠杆 断臂求生
    python3 bin/lh_qiye_deng.py weilai-compare 0.7 0.6 0.8 0.5       # 三条路径对比

    # 企业注册
    python3 bin/lh_qiye_deng.py register 企业名 行业 规模

    # 认路费
    python3 bin/lh_qiye_deng.py renlufei 企业ID "核心难题" "A" 7 "承诺做的事"

    # 还账记录
    python3 bin/lh_qiye_deng.py huanzhang 企业ID "行动了什么" "结果是什么" "下一步"

    # 综合报告
    python3 bin/lh_qiye_deng.py report 企业ID

DNA: #龍芯⚡️丙午·丙申·丙辰·己丑·需-QIYE-DENG-TECH-ARCH-v2.0-F045F504
"""

import json
import math
import os
import sys
from datetime import datetime
from typing import Optional, Any

# ── 路径 ──────────────────────────────────────────────
DATA_DIR = os.path.expanduser("~/.龍魂/qiye_deng")
os.makedirs(DATA_DIR, exist_ok=True)
REGISTRY_FILE = os.path.join(DATA_DIR, "registry.json")
RENLUFEI_FILE = os.path.join(DATA_DIR, "renlufei.jsonl")
HUANZHANG_FILE = os.path.join(DATA_DIR, "huanzhang.jsonl")

# ── 常量 ──────────────────────────────────────────────
DNA = "#龍芯⚡️丙午·丙申·丙辰·己丑·需-QIYE-DENG-TECH-ARCH-v2.0-F045F504"
HEALTH_BENCHMARKS = {
    "人效_行业均值": 500000,  # 元/人/年 默认值
    "现金流_健康线": 6,       # 月
    "核心团队留存率": 80,     # %
    "主营业务增速": 0,         # %
}

# ── 工具函数 ──────────────────────────────────────────

def load_json(path: str) -> dict[str, Any]:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}

def save_json(path: str, data: dict[str, Any]):
    with open(path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def append_jsonl(path: str, record: dict[str, Any]):
    with open(path, "a") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

def read_jsonl(path: str) -> list[Any]:
    if not os.path.exists(path):
        return []
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records

def tricolor(value: float, green: float = 0.7, yellow: float = 0.4) -> str:
    """三色判定"""
    if value >= green:
        return "🟢"
    elif value >= yellow:
        return "🟡"
    return "🔴"

def tricolor_label(value: float, green: float = 0.7, yellow: float = 0.4) -> str:
    color = tricolor(value, green, yellow)
    labels = {"🟢": "良好·可行动", "🟡": "需关注·谨慎", "🔴": "危机·立即处理"}
    return f"{color} {labels[color]}"


# ══════════════════════════════════════════════════════
#  🪞 前生灯（镜）·因果追溯引擎
# ══════════════════════════════════════════════════════

def qiansheng_trace(*weights: float) -> dict[str, Any]:
    """
    因果追溯度 P = Σ(节点权重 × 时间衰减) / 链长度
    输入: 按时间顺序（最近到最远）的历史节点权重
    """
    if not weights:
        return {"error": "请提供至少1个历史节点权重"}

    n = len(weights)
    total = 0.0
    nodes = []

    for i, w in enumerate(weights):
        w = max(0.0, min(1.0, w))
        decay = math.exp(-0.3 * i)  # λ=0.3 时间衰减
        contribution = w * decay
        total += contribution
        nodes.append({
            "序号": i + 1,  # 1=最近
            "权重": round(w, 2),
            "时间衰减系数": round(decay, 4),
            "贡献值": round(contribution, 4),
        })

    p = total / n
    return {
        "因果追溯度": round(p, 4),
        "判定": tricolor_label(p),
        "追溯深度": f"{n}个历史节点",
        "总贡献": round(total, 4),
        "节点明细": nodes,
    }


def qiansheng_chain(*nodes_str: str) -> dict[str, Any]:
    """带标签的历史节点追溯"""
    nodes = []
    total = 0.0

    for i, s in enumerate(nodes_str):
        label, weight_str = s.rsplit("=", 1) if "=" in s else (f"节点{i+1}", "0.5")
        w = max(0.0, min(1.0, float(weight_str)))
        decay = math.exp(-0.3 * i)
        contribution = w * decay
        total += contribution
        nodes.append({
            "序号": i + 1,
            "事件": label.strip(),
            "权重": round(w, 2),
            "时间衰减": round(decay, 4),
            "贡献值": round(contribution, 4),
        })

    n = len(nodes)
    p = total / n if n > 0 else 0.0

    return {
        "因果追溯度": round(p, 4),
        "判定": tricolor_label(p),
        "追溯链长度": n,
        "节点明细": nodes,
    }


# ══════════════════════════════════════════════════════
#  ⚖️ 今世灯（秤）·压力算法
# ══════════════════════════════════════════════════════

def jinshi_pressure(f: float, t: float, m: float, d: float, p: float) -> dict[str, Any]:
    """
    今世压力指数 J = F×0.35 + T×0.25 + M×0.20 + D×0.15 + P×0.05
    """
    f, t, m, d, p = [max(0, min(10, x)) for x in (f, t, m, d, p)]

    j = f * 0.35 + t * 0.25 + m * 0.20 + d * 0.15 + p * 0.05

    # 三色判定（压力指数阈值不同：越低越好）
    if j < 3.0:
        color_label = "🟢 健康·继续保持"
    elif j < 5.0:
        color_label = "🟢 可控·正常经营压力"
    elif j < 8.0:
        color_label = "🟡 高压·需要外部介入"
    else:
        color_label = "🔴 红色警报·立即启动危机模式"

    dimensions = {
        "资金压力 F": {"分": f, "权重": 0.35, "贡献": round(f * 0.35, 2)},
        "团队压力 T": {"分": t, "权重": 0.25, "贡献": round(t * 0.25, 2)},
        "市场压力 M": {"分": m, "权重": 0.20, "贡献": round(m * 0.20, 2)},
        "决策压力 D": {"分": d, "权重": 0.15, "贡献": round(d * 0.15, 2)},
        "个人状态 P": {"分": p, "权重": 0.05, "贡献": round(p * 0.05, 2)},
    }

    return {
        "今世压力指数 J": round(j, 2),
        "判定": color_label,
        "五维明细": dimensions,
    }


def jinshi_health(
    rexiao: float,      # 人均产出（元）
    hangye_junzhi: float,  # 行业均值
    xianjinliu: float,  # 现金流（月）
    liucunlv: float,    # 核心团队留存率（%）
    zengsu: float,      # 主营业务增速（%）
) -> dict[str, Any]:
    """关键健康指标对比"""
    indicators = {}

    # 人效
    gap_pct = round((rexiao - hangye_junzhi) / hangye_junzhi * 100, 1)
    indicators["人效"] = {
        "当前": f"¥{rexiao:,.0f}",
        "行业基准": f"¥{hangye_junzhi:,.0f}",
        "差距": f"{gap_pct:+.1f}%",
        "状态": "🟢 高于行业" if gap_pct >= 0 else "🟡 低于行业",
    }

    # 现金流
    cf_status = "🟢 健康" if xianjinliu >= 6 else ("🟡 偏紧" if xianjinliu >= 3 else "🔴 危急")
    indicators["现金流"] = {
        "当前": f"{xianjinliu:.1f}个月",
        "健康基准": "≥6个月",
        "差距": f"{6 - xianjinliu:+.1f}个月",
        "状态": cf_status,
    }

    # 留存率
    rt_status = "🟢 健康" if liucunlv >= 80 else ("🟡 需关注" if liucunlv >= 60 else "🔴 流失严重")
    indicators["核心团队留存率"] = {
        "当前": f"{liucunlv:.1f}%",
        "健康基准": "≥80%",
        "差距": f"{liucunlv - 80:+.1f}%",
        "状态": rt_status,
    }

    # 增速
    gs_status = "🟢 增长" if zengsu > 0 else ("🟡 持平" if zengsu == 0 else "🔴 萎缩")
    indicators["主营业务增速"] = {
        "当前": f"{zengsu:+.1f}%",
        "健康基准": "正增长",
        "差距": f"{zengsu:+}",
        "状态": gs_status,
    }

    return {"健康指标对比": indicators}


# ══════════════════════════════════════════════════════
#  🔦 未来灯（路）·强化学习路径推演
# ══════════════════════════════════════════════════════

def weilai_project(
    c: float, m: float, t: float, l: float,
    path: str = "A",
    months: int = 6,
) -> dict[str, Any]:
    """
    生存概率 S(t) = C(t) × M(t) × T(t) × L(t)
    每条路径有不同衰减因子
    """
    c, m, t, l = [max(0.0, min(1.0, x)) for x in (c, m, t, l)]

    # 路径特征参数
    path_params = {
        "A": {"name": "🅰️ 断臂求生", "C_decay": 0.02, "M_decay": 0.05, "T_decay": 0.08, "L_decay": 0.01,
              "desc": "快速收缩·砍非核心·现金流优先"},
        "B": {"name": "🅱️ 渐进改革", "C_decay": 0.04, "M_decay": 0.02, "T_decay": 0.03, "L_decay": 0.02,
              "desc": "边跑边改·保留主干·时间换空间"},
        "AB": {"name": "🆎 借势突围", "C_decay": 0.06, "M_decay": 0.03, "T_decay": 0.02, "L_decay": 0.04,
               "desc": "找外部合作杠杆·借力打力"},
    }

    if path not in path_params:
        return {"error": f"未知路径: {path}，可选: A/B/AB"}

    pp = path_params[path]
    curve = []
    final_s = None

    for month in range(1, months + 1):
        ct = max(0.0, c * (1 - pp["C_decay"] * month))
        mt = max(0.0, m * (1 - pp["M_decay"] * month))
        tt = max(0.0, t * (1 - pp["T_decay"] * month))
        lt_val = max(0.0, l * (1 - pp["L_decay"] * month))
        s = ct * mt * tt * lt_val
        curve.append({
            "月份": month,
            "现金流 C": round(ct, 4),
            "市场 M": round(mt, 4),
            "团队 T": round(tt, 4),
            "杠杆 L": round(lt_val, 4),
            "生存概率 S": round(s, 4),
        })
        if month == months:
            final_s = s

    return {
        "路径": pp["name"],
        "路径说明": pp["desc"],
        "初始状态": {"C": c, "M": m, "T": t, "L": l},
        f"{months}个月生存概率": round(final_s, 4) if final_s is not None else 0,
        "判定": tricolor_label(final_s) if final_s else "N/A",
        "逐月曲线": curve,
    }


def weilai_compare(c: float, m: float, t: float, l: float, months: int = 6) -> dict[str, Any]:
    """三条路径平行对比"""
    results = {}
    for path in ["A", "B", "AB"]:
        r = weilai_project(c, m, t, l, path, months)
        results[path] = {
            "路径名": r["路径"],
            "说明": r.get("路径说明", ""),
            f"{months}个月生存概率": r[f"{months}个月生存概率"],
            "判定": r["判定"],
        }

    return {"路径对比": results}


# ══════════════════════════════════════════════════════
#  📋 企业注册
# ══════════════════════════════════════════════════════

def register_qiye(qiye_id: str, name: str, industry: str, scale: str) -> dict[str, Any]:
    registry = load_json(REGISTRY_FILE)
    if qiye_id in registry:
        return {"error": f"企业 {qiye_id} 已注册", "existing": registry[qiye_id]}

    record = {
        "企业ID": qiye_id,
        "企业名称": name,
        "行业": industry,
        "规模": scale,
        "注册时间": datetime.now().isoformat(),
        "DNA": DNA,
        "前生灯记录": 0,
        "今世灯记录": 0,
        "未来灯记录": 0,
        "认路费记录": 0,
        "还账记录": 0,
    }
    registry[qiye_id] = record
    save_json(REGISTRY_FILE, registry)
    return {"状态": "✅ 注册成功", "企业信息": record}


# ══════════════════════════════════════════════════════
#  💰 认路费（数字契约·智能合约记录）
# ══════════════════════════════════════════════════════

def renlufei_commit(qiye_id: str, problem: str, path: str, days: int, action: str) -> dict[str, Any]:
    """认路费承诺·打上DNA追溯"""
    registry = load_json(REGISTRY_FILE)
    if qiye_id not in registry:
        return {"error": f"企业 {qiye_id} 未注册，请先 register"}

    record = {
        "企业ID": qiye_id,
        "承诺时间": datetime.now().isoformat(),
        "核心难题": problem,
        "选择路径": path,
        "承诺天数": days,
        "承诺行动": action,
        "DNA": DNA,
        "状态": "🟡 待完成",
        "是否已还账": False,
    }
    append_jsonl(RENLUFEI_FILE, record)

    registry[qiye_id]["认路费记录"] += 1
    save_json(REGISTRY_FILE, registry)

    return {
        "状态": "✅ 认路费已提交·数字契约已生成",
        "契约详情": record,
        "提醒": f"请在 {days} 日内完成承诺行动，完成后执行 huanzhang 还账",
    }


# ══════════════════════════════════════════════════════
#  📝 还账记录
# ══════════════════════════════════════════════════════

def huanzhang_log(qiye_id: str, action: str, result: str, next_step: str) -> dict[str, Any]:
    registry = load_json(REGISTRY_FILE)
    if qiye_id not in registry:
        return {"error": f"企业 {qiye_id} 未注册"}

    record = {
        "企业ID": qiye_id,
        "还账时间": datetime.now().isoformat(),
        "执行了什么": action,
        "结果是什么": result,
        "下一步": next_step,
        "DNA": DNA,
    }
    append_jsonl(HUANZHANG_FILE, record)

    registry[qiye_id]["还账记录"] += 1

    # 关联认路费中的最近一条未还账记录
    renlufei_records = read_jsonl(RENLUFEI_FILE)
    matched = False
    if renlufei_records:
        for rec in reversed(renlufei_records):
            if rec["企业ID"] == qiye_id and not rec.get("是否已还账", False):
                rec["是否已还账"] = True
                rec["状态"] = "🟢 已完成"
                matched = True
                break

    save_json(REGISTRY_FILE, registry)
    # 重写认路费记录
    write_jsonl(RENLUFEI_FILE, renlufei_records)

    return {
        "状态": "✅ 已还账·契约履行完毕",
        "还账记录": record,
        "关联认路费": "已匹配并标记完成" if matched else "未找到对应认路费·独立记录",
    }


def write_jsonl(path: str, records: list[Any]):
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


# ══════════════════════════════════════════════════════
#  📊 综合报告
# ══════════════════════════════════════════════════════

def report(qiye_id: str) -> dict[str, Any]:
    registry = load_json(REGISTRY_FILE)
    if qiye_id not in registry:
        return {"error": f"企业 {qiye_id} 未注册"}

    qiye = registry[qiye_id]
    renlufei_records = [r for r in read_jsonl(RENLUFEI_FILE) if r["企业ID"] == qiye_id]
    huanzhang_records = [r for r in read_jsonl(HUANZHANG_FILE) if r["企业ID"] == qiye_id]

    return {
        "企业ID": qiye_id,
        "企业名称": qiye.get("企业名称", "未知"),
        "行业": qiye.get("行业", "未知"),
        "规模": qiye.get("规模", "未知"),
        "注册时间": qiye.get("注册时间", "未知"),
        "三灯统计": {
            "前生灯": qiye.get("前生灯记录", 0),
            "今世灯": qiye.get("今世灯记录", 0),
            "未来灯": qiye.get("未来灯记录", 0),
        },
        "契约统计": {
            "认路费承诺": len(renlufei_records),
            "已还账": sum(1 for r in renlufei_records if r.get("是否已还账")),
            "未还账": sum(1 for r in renlufei_records if not r.get("是否已还账")),
            "还账记录": len(huanzhang_records),
        },
        "DNA": DNA,
    }


# ══════════════════════════════════════════════════════
#  路标指南
# ══════════════════════════════════════════════════════

def summary() -> dict[str, Any]:
    registry = load_json(REGISTRY_FILE)
    renlufei_records = read_jsonl(RENLUFEI_FILE)
    huanzhang_records = read_jsonl(HUANZHANG_FILE)

    return {
        "系统": "龍芯企业灯·三生三世引擎 v2.0",
        "DNA": DNA,
        "底座": "LoongArch + KaihongOS 全栈自主",
        "已注册企业": len(registry),
        "认路费总数": len(renlufei_records),
        "已还账": sum(1 for r in renlufei_records if r.get("是否已还账")),
        "未还账": sum(1 for r in renlufei_records if not r.get("是否已还账")),
        "还账记录总数": len(huanzhang_records),
        "可用命令": [
            "qiansheng <权重1> <权重2> ...     → 前生灯·因果追溯",
            "qiansheng-chain '事件1=权重' ...  → 前生灯·带标签追溯",
            "jinshi <F> <T> <M> <D> <P>        → 今世灯·压力指数",
            "jinshi-health <人效> <行业均值> <现金流> <留存率> <增速>",
            "weilai <C> <M> <T> <L> --path A/B/AB → 未来灯·路径推演",
            "weilai-compare <C> <M> <T> <L>    → 未来灯·三路径对比",
            "register <企业ID> <名称> <行业> <规模> → 注册企业",
            "renlufei <企业ID> '<难题>' '<路径>' <天数> '<行动>'",
            "huanzhang <企业ID> '<行动了>' '<结果>' '<下一步>'",
            "report <企业ID>                    → 综合报告",
            "summary                             → 系统概览",
        ],
    }


# ══════════════════════════════════════════════════════
#  CLI入口
# ══════════════════════════════════════════════════════

def print_result(data: dict[str, Any]):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print_result(summary())
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    try:
        # 🪞 前生灯
        if cmd == "qiansheng":
            if not args:
                print_result({"error": "用法: qiansheng <权重1> <权重2> ..."})
                return
            weights = [float(a) for a in args]
            print_result(qiansheng_trace(*weights))

        elif cmd == "qiansheng-chain":
            if not args:
                print_result({"error": "用法: qiansheng-chain '事件1=权重' ..."})
                return
            print_result(qiansheng_chain(*args))

        # ⚖️ 今世灯
        elif cmd == "jinshi":
            if len(args) < 5:
                print_result({"error": "用法: jinshi <F资金> <T团队> <M市场> <D决策> <P个人>"})
                return
            f, t, m, d, p = [float(a) for a in args[:5]]
            print_result(jinshi_pressure(f, t, m, d, p))

        elif cmd == "jinshi-health":
            if len(args) < 5:
                print_result({"error": "用法: jinshi-health <人效> <行业均值> <现金流> <留存率> <增速>"})
                return
            rx, hy, xj, lc, zs = [float(a) for a in args[:5]]
            print_result(jinshi_health(rx, hy, xj, lc, zs))

        # 🔦 未来灯
        elif cmd == "weilai":
            if len(args) < 4:
                print_result({"error": "用法: weilai <C> <M> <T> <L> [--path A/B/AB]"})
                return
            c, m, t, l = [float(a) for a in args[:4]]
            path = "A"
            if "--path" in args:
                idx = args.index("--path")
                if idx + 1 < len(args):
                    path = args[idx + 1]
            print_result(weilai_project(c, m, t, l, path))

        elif cmd == "weilai-compare":
            if len(args) < 4:
                print_result({"error": "用法: weilai-compare <C> <M> <T> <L>"})
                return
            c, m, t, l = [float(a) for a in args[:4]]
            print_result(weilai_compare(c, m, t, l))

        # 📋 注册
        elif cmd == "register":
            if len(args) < 4:
                print_result({"error": "用法: register <企业ID> <企业名称> <行业> <规模>"})
                return
            print_result(register_qiye(args[0], args[1], args[2], args[3]))

        # 💰 认路费
        elif cmd == "renlufei":
            if len(args) < 5:
                print_result({"error": "用法: renlufei <企业ID> '<核心难题>' '<路径A/B/AB>' <天数> '<承诺行动>'"})
                return
            print_result(renlufei_commit(args[0], args[1], args[2], int(args[3]), args[4]))

        # 📝 还账
        elif cmd == "huanzhang":
            if len(args) < 4:
                print_result({"error": "用法: huanzhang <企业ID> '<行动了什么>' '<结果是什么>' '<下一步>'"})
                return
            print_result(huanzhang_log(args[0], args[1], args[2], args[3]))

        # 📊 报告
        elif cmd == "report":
            if not args:
                print_result({"error": "用法: report <企业ID>"})
                return
            print_result(report(args[0]))

        # 概览
        elif cmd == "summary":
            print_result(summary())

        else:
            err_msg = "未知命令: " + str(cmd)
            print_result({"error": err_msg, "帮助": "执行 summary 查看可用命令"})

    except ValueError as e:
        print_result({"error": "参数格式错误: " + str(e)})
    except Exception as e:
        print_result({"error": str(e)})


if __name__ == "__main__":
    main()
