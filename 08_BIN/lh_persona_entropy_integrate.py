#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-30-丙午·甲申·乙巳·未时-ENTROPY-INTEGRATE-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 功能: 人格测试×熵减集成器 —— 批量任务路由 → 人格分布熵 H_route
#       熵高=路由发散(需消歧收敛) · 熵低=过度集中(部分人格闲置)
#       集成反熵增思想: 修复缺陷后 H_norm 应回落至健康带 0.5~0.85

"""龍魂 · 人格测试 × 熵减集成器 v1.0

对一组覆盖全部能力域的任务批量路由（复用 lh_persona_evolve.route），
统计主人格分布熵，量化人格系统有序度。修复缺陷后再跑，熵应下降 = 熵减闭环。
"""

import math
import sys
from collections import Counter
from typing import Dict, List, Tuple

# 复用既有路由引擎（毫秒级·不调 LLM）
sys.path.insert(0, "/Users/zuimeidedeyihan/longhun-system/08_BIN")
try:
    from lh_persona_evolve import route, PERSONA_PROFILE
except ImportError as e:
    print(f"🔴 熵减集成器依赖缺失: {e} · 请确认 08_BIN/lh_persona_evolve.py 存在")
    sys.exit(1)

# 覆盖全部能力域的典型任务集（W1-W3 / R1-R9 / D1-D3 / E1-E2 / G1-G2 / UNKNOWN）
TASK_SET: List[str] = [
    # 写作创作域
    "帮我写一首关于数字主权的诗",
    "给我们的产品起个名字",
    "帮我写个演讲稿",
    "写一份双方合作协议",
    "起草一份白皮书",
    "这个词用CNSH怎么命名",
    "帮我解释一下这个专业术语",
    # 识别理解域
    "帮我统筹安排一下今天的任务",
    "帮我分派一下工作",
    "帮我测测网站的安全性",
    "这段代码有漏洞吗",
    "帮我算一下数字根",
    "帮我算一下五行权重",
    "帮我做个三才算法判定",
    "帮我做一次算法宪法检查",
    "帮我做一次数字主权审计",
    "数据主权怎么守护",
    "帮我做个系统健康检查",
    "给我做个系统体检",
    "我心情不好安慰我一下",
    "这段话是不是PUA",
    "帮我验证一下这个DNA签名",
    "做个身份验证",
    "帮我审计下这个页面UI",
    "帮我做个极简审计",
    # 推理决策域
    "帮我做个战略推演",
    "这个方案值不值",
    "这件事能不能做",
    "帮我做个底线判定",
    "帮我算下成本预算",
    "做个ROI分析",
    # 执行部署域
    "帮我写个Python脚本",
    "帮我修个bug",
    "帮我部署上线",
    "帮我发布一下",
    # 守护熔断域
    "帮我审计这段代码",
    "帮我检查一下有没有问题",
    "帮我调解一下矛盾",
    # 守护层专属可达性（P13/P15/P20/P72）
    "帮我分配一下新模块的权限",
    "帮我注册一个新的模块",
    "帮我签章盖章验收",
    "帮我做个贡献公证",
    "帮我算下我的信任积分",
    "帮我熔断这个风险",
    # 未知任务（应回退总控 X0）
    "今天天气怎么样",
    "中午吃什么",
]


def shannon_entropy(counts: Counter) -> float:
    """Shannon 熵 H = -Σ p·log2(p)。"""
    total = sum(counts.values())
    if total == 0:
        return 0.0
    h = 0.0
    for c in counts.values():
        p = c / total
        if p > 0:
            h -= p * math.log2(p)
    return h


def run() -> int:
    # 双维度熵: H_top1 主人格路由熵 · H_act 激活人格(top3)熵
    top1_counter: Counter = Counter()
    act_counter: Counter = Counter()
    unknown = 0
    for task in TASK_SET:
        r = route(task)
        top = r["personas"][0] if r["personas"] else {
            "persona": "X0", "name": "龙魂执行器", "weight": 0, "reason": "空路由"}
        top1_counter[top["persona"]] += 1
        for p in r["personas"][:3]:
            act_counter[p["persona"]] += 1
        if r["verdict"] == "UNKNOWN":
            unknown += 1

    n = len(TASK_SET)
    h1 = shannon_entropy(top1_counter)
    ha = shannon_entropy(act_counter)
    h_max = math.log2(n) if n > 1 else 1.0
    h1_norm = h1 / h_max if h_max > 0 else 0.0
    ha_norm = ha / h_max if h_max > 0 else 0.0
    order = h_max - h1  # 主人格维度负熵 = 有序度(bits)

    # 三色判定（以主人格归一熵为准）
    if h1_norm > 0.85:
        mark = "🟡"
        verdict = "路由发散 · 熵超限 · 需关键词消歧收敛"
    elif h1_norm >= 0.50:
        mark = "🟢"
        verdict = "路由健康 · 主路由聚焦且覆盖均衡"
    else:
        mark = "🟡"
        verdict = "路由过度集中 · 部分人格闲置 · 需补触发覆盖"

    # 覆盖分析
    all_personas = set(PERSONA_PROFILE.keys()) if PERSONA_PROFILE else set()
    triggered = set(act_counter.keys())
    idle = sorted(all_personas - triggered)

    print("⚡ 人格测试 × 熵减集成 · v1.1")
    print("=" * 62)
    print(f"任务样本数       : {n}（激活 {len(triggered)}/{len(all_personas)} 个人格）")
    print(f"主路由熵 H_top1  : {h1:.4f} bits · 归一 {h1_norm:.4f}")
    print(f"激活熵  H_act    : {ha:.4f} bits · 归一 {ha_norm:.4f}")
    print(f"最大熵 H_max     : {h_max:.4f} bits")
    print(f"有序度(负熵)     : +{order:.4f} bits（越高越有序）")
    print(f"未匹配任务       : {unknown} → 回退总控 X0（设计内·低熵兜底）")
    print(f"三色判定         : {mark} {verdict}")
    print("-" * 62)
    print("主人格分布 TOP6:")
    for pid, c in top1_counter.most_common(6):
        bar = "█" * int(c)
        print(f"  {pid:<6} x{c:<3} {bar}")
    if idle:
        print(f"⚠️ 未激活人格({len(idle)}): {', '.join(idle)}")
    print("=" * 62)
    if h1_norm > 0.85:
        print(f"熵减建议: 收敛路由关键词，减少跨域误命中（{h1_norm:.2f} > 0.85）")
    elif h1_norm < 0.5:
        print(f"熵减建议: 补充闲置人格触发词，提升覆盖（{h1_norm:.2f} < 0.50）")
    elif idle:
        print(f"熵减建议: 熵健康，但 {', '.join(idle)} 未激活，补充任务样本后可提升覆盖")
    else:
        print("熵减建议: 当前熵值健康，无需干预")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
