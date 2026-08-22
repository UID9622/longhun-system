# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-eb92cc52
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 P4 · 史官/三色审计/DNA链 集成层
每次路由仲裁完毕：史官落笔（年轮链）→ 三色R值审计 → 随时可验链。
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
import sys, os, time, json
sys.path.insert(0, "/mnt/agents/output/龍魂低算力内核/core")
from longhun_core.historian import 年轮链
from longhun_core.tricolor_audit import 审计 as R值审计

class 史官集成器:
    """把透明仲裁的每一次运行写进年轮链，附R值审计；篡改必断链"""

    # 审计规则：指标超过阈值即扣分
    规则 = {"事实冲突数": (0, 25),      # 有冲突扣25
            "极性分裂数": (0, 15),      # 有极性分裂再扣15
            "引擎失败数": (0, 10),      # 有降级扣10
            "覆盖率缺口": (2, 5)}       # 单人作证超过2处扣5

    def __init__(self, 链: 年轮链 = None):
        self.链 = 链 or 年轮链()

    def 归档(self, 路由报告: dict, 摘要: dict, 仲裁: dict) -> dict:
        指标 = {
            "事实冲突数": len(仲裁.get("conflicts", [])) if 仲裁 else 0,
            "极性分裂数": sum(1 for c in (仲裁.get("conflicts", []) if 仲裁 else [])
                          if c["polarity_split"]),
            "引擎失败数": 路由报告.get("失败数", 0),
            "覆盖率缺口": len(仲裁.get("coverage_gaps", [])) if 仲裁 else 0,
        }
        审计结果 = R值审计(指标, self.规则)
        条目 = self.链.落笔("透明仲裁归档", {
            "父DNA": 路由报告.get("父DNA"),
            "问题": 路由报告.get("问题", "")[:50],
            "三色": 路由报告.get("三色"),
            "R值": 审计结果["R值"],
            "指标": 指标,
            "一句话结论": 摘要.get("一句话结论", ""),
        })
        return {"史官条目序号": 条目["序号"], "条目哈希": 条目["哈希"],
                "条目DNA": 条目["DNA"], "R值审计": 审计结果}

    def 验链(self) -> dict:
        return self.链.验链()
