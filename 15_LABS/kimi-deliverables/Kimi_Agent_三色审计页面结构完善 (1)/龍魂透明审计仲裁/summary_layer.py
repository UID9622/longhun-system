# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-4b84bf6c
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 P3 · 冲突摘要层（ConflictSummary）—— "分别呈现"的阅读负担解法
输入：arbiter_v2 仲裁报告 + 路由层原始回答
输出：共识清单 / 分歧点卡片 / Token明细 / 一句话结论
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
from typing import Dict, List
from collections import defaultdict

class ConflictSummary:
    """把仲裁结果压成用户一眼能看懂的摘要"""

    def build(self, 仲裁报告: Dict, 路由回答: List[Dict]) -> Dict:
        # ---------- 1. 共识：所有有效AI 同(主语,谓语)→同取值 ----------
        # 从仲裁报告的证据里反推：没有出现在冲突里的(主语,谓语)且多AI作证 → 共识
        冲突键 = {(c["subject"], c["predicate"]) for c in 仲裁报告.get("conflicts", [])}
        共识 = []
        # 重新从各AI断言聚合（仲裁报告里只有冲突和gap，共识需从冲突外推）
        # 用 conflicts 的 camps 之外的信息不可得 → 要求传入归一化断言
        # 设计：analyze 返回里加 _normed（见 arbiter_v2 集成说明）
        normed = 仲裁报告.get("_normed")
        if normed:
            组 = defaultdict(dict)
            for ai, claims in normed.items():
                for c in claims:
                    组[(c["subject"], c["predicate"])][ai] = c["object"]
            for (s, p), ai_obj in 组.items():
                if (s, p) in 冲突键 or len(ai_obj) < 2:
                    continue
                if len(set(ai_obj.values())) == 1:
                    共识.append({"事实": f"{s}·{p} → {next(iter(ai_obj.values()))}",
                                 "作证AI": sorted(ai_obj.keys())})

        # ---------- 2. 分歧点卡片 ----------
        分歧 = []
        for c in 仲裁报告.get("conflicts", []):
            camps = "；".join(f"「{obj}」由 {'/'.join(ais)} 主张" for obj, ais in c["camps"].items())
            分歧.append({
                "分歧点": f"{c['subject']}·{c['predicate']}",
                "各执一词": camps,
                "极性分裂": c["polarity_split"],
                "级别": c["severity"],
                "建议": "需老大裁决" if c["polarity_split"] else "建议以龍魂本地引擎为准·其余存档",
            })

        # ---------- 3. Token明细 ----------
        明细 = []
        总输入 = 总输出 = 0
        for r in 路由回答:
            if "失败" in r:
                明细.append({"引擎": r["来源"], "状态": "✗失败降级", "输入": 0, "输出": 0})
                continue
            t = r.get("token统计", {})
            总输入 += t.get("输入", 0); 总输出 += t.get("输出", 0)
            明细.append({"引擎": r["来源"], "状态": "✓",
                         "输入": t.get("输入", 0), "输出": t.get("输出", 0),
                         "缓存命中率": t.get("缓存命中率", 0)})
        token汇总 = {"明细": 明细, "总输入": 总输入, "总输出": 总输出,
                     "并行成本提示": f"本次并行 {len(明细)} 路，Token ≈ 单路的 {len(明细)} 倍（透明化承诺）"}

        # ---------- 4. 一句话结论 ----------
        n共, n分 = len(共识), len(分歧)
        三色 = 仲裁报告.get("tricolor", "🟡")
        if n分 == 0:
            结论 = f"{三色} 全员一致：{n共} 项共识，无分歧，可直接采信。"
        else:
            首 = 分歧[0]
            结论 = (f"{三色} {n共} 项共识 + {n分} 项分歧。"
                    f"最要紧：{首['分歧点']}（{首['各执一词']}）——{首['建议']}。")

        return {"一句话结论": 结论, "共识": 共识, "分歧点": 分歧,
                "token明细": token汇总, "三色": 三色}

    def render(self, s: Dict) -> str:
        L = ["┌" + "─" * 58 + "┐",
             "│ 🐉 冲突摘要 · 一眼看懂" + " " * 34 + "│",
             "└" + "─" * 58 + "┘",
             f"📌 {s['一句话结论']}"]
        if s["共识"]:
            L.append(f"\n🤝 共识（{len(s['共识'])} 项）:")
            for c in s["共识"]:
                L.append(f"   ✓ {c['事实']}  （{'/'.join(c['作证AI'])}）")
        if s["分歧点"]:
            L.append(f"\n⚔️ 分歧（{len(s['分歧点'])} 项）:")
            for d in s["分歧点"]:
                L.append(f"   {d['级别']} {d['分歧点']} → {d['各执一词']}")
                L.append(f"      💡 {d['建议']}")
        t = s["token明细"]
        L.append(f"\n💰 Token: 总输入 {t['总输入']} · 总输出 {t['总输出']}（{t['并行成本提示']}）")
        return "\n".join(L)
