#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# -*- coding: utf-8 -*-
"""🐉 龍魂·透明审计与冲突仲裁引擎 v2.0
复用 v1.1 的 路由/仓库/引擎 骨架，仲裁层整体替换为事实级仲裁（arbiter_v2）。
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
import asyncio, time, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transparent_audit import 引擎基类, 本地龍魂引擎, 模拟云端引擎, 结果仓库, 生成DNA, 短身份码
from arbiter_v2 import ConflictArbiterV2

class 透明路由器V2:
    """与v1.1同骨架：并行分发·独立超时·失败降级；仲裁升级为事实级"""
    def __init__(self, 引擎们: list, 仓库: 结果仓库 = None, 超时=5.0):
        self.引擎们 = 引擎们; self.仓库 = 仓库 or 结果仓库(); self.超时 = 超时
        self.仲裁 = ConflictArbiterV2()

    async def _单路(self, 引擎, 问题, 父DNA):
        子DNA = f"{父DNA[:-7]}-{引擎.名字.upper()}-{短身份码(引擎.名字+父DNA)}-UID9622"
        try:
            return await asyncio.wait_for(引擎.询问(问题, 子DNA, self.超时), timeout=self.超时)
        except Exception as e:
            return {"来源": 引擎.名字, "子DNA": 子DNA, "耗时": self.超时, "内容": "",
                    "置信度": 0.0, "token统计": {}, "失败": str(e)[:60]}

    async def 路由(self, 问题: str, 用户="UID9622") -> dict:
        父DNA = 生成DNA("USER-QUERY")
        结果 = await asyncio.gather(*[self._单路(e, 问题, 父DNA) for e in self.引擎们])
        for r in 结果:
            self.仓库.存(父DNA, r)
        有效 = {r["来源"]: r["内容"] for r in 结果 if "失败" not in r and r["内容"]}
        失败 = [r for r in 结果 if "失败" in r]
        仲裁报告 = self.仲裁.analyze(有效) if len(有效) >= 2 else None
        三色 = (仲裁报告["tricolor"] if 仲裁报告 else "🟡")
        if 失败 and 三色 == "🟢":
            三色 = "🟡"
        return {"父DNA": 父DNA, "用户": 用户, "问题": 问题, "回答": 结果,
                "仲裁": 仲裁报告, "失败数": len(失败), "三色": 三色, "时间": time.time()}

def 仪表盘V2(报告: dict) -> str:
    行 = ["=" * 64, f"🐉 龍魂·透明审计仪表盘 v2.0 | {报告['三色']}",
          f"父DNA: {报告['父DNA']}", "-" * 64]
    for r in 报告["回答"]:
        if "失败" in r:
            行.append(f"  ✗ {r['来源']:<12} 失败降级: {r['失败']}")
        else:
            t = r["token统计"]
            行.append(f"  ✓ {r['来源']:<12} {r['耗时']:.2f}s | 置信度 {r['置信度']}")
    if 报告["仲裁"]:
        a = 报告["仲裁"]
        行.append("-" * 64)
        if a["conflicts"]:
            行.append(f"  ⚔️ 事实冲突 {len(a['conflicts'])} 项（分别呈现·不合并·不掩盖）:")
            for c in a["conflicts"]:
                camps = " vs ".join(f"{obj}（{'/'.join(ais)}）" for obj, ais in c["camps"].items())
                pol = " ＋极性分裂" if c["polarity_split"] else ""
                行.append(f"    {c['severity']} {c['subject']}·{c['predicate']}：{camps}{pol}")
        else:
            行.append("  无事实冲突")
        for g in a["coverage_gaps"]:
            行.append(f"    {g['note']}：{g['subject']}·{g['predicate']}（仅 {g['only_ai']}）")
    行.append("=" * 64)
    return "\n".join(行)

# ============================================================
# 全链路路由器：P1路由 + P2仲裁 + P3摘要 + P4史官归档
# ============================================================

class 全链路路由器(透明路由器V2):
    def __init__(self, 引擎们, 仓库=None, 超时=5.0, llm_hook=None, 史官=None):
        super().__init__(引擎们, 仓库, 超时)
        from arbiter_v2 import ConflictArbiterV2
        self.仲裁 = ConflictArbiterV2(llm_hook=llm_hook)
        from summary_layer import ConflictSummary
        from integration import 史官集成器
        self.摘要器 = ConflictSummary()
        self.史官 = 史官 or 史官集成器()

    async def 路由(self, 问题, 用户="UID9622") -> dict:
        报告 = await super().路由(问题, 用户)
        仲裁 = 报告["仲裁"]
        if 仲裁:
            摘要 = self.摘要器.build(仲裁, 报告["回答"])
            归档 = self.史官.归档(报告, 摘要, 仲裁)
            报告.update({"摘要": 摘要, "归档": 归档,
                         "R值": 归档["R值审计"]["R值"]})
        return 报告

if __name__ == "__main__":
    引擎们 = [
        本地龍魂引擎(),
        模拟云端引擎("kimi", "用户数据应保存于云端服务器，数据主权归用户所有。操作记录写入区块链。"),
        模拟云端引擎("deepseek", "用户数据应存储于本地终端，数据主权归属国家法律。操作记录存档于数据库。"),
    ]
    报告 = asyncio.run(透明路由器V2(引擎们).路由("数据主权到底归谁？"))
    print(仪表盘V2(报告))
