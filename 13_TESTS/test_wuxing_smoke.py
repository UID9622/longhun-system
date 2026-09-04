"""
龍魂五行计算器 v4.0 · 冲烟测试套件
DNA: #龍芯⚡️2026-08-31-五行计算器-v4.0-WELD-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

黄金标准测试 T04：甲子丙午庚申壬戌 -> H=0.927 🟢
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.wuxing.core import 龍魂五行完整计算
from modules.wuxing.node import 生成节点, 校验节点
from modules.wuxing.constants import (
    H_THRESHOLD_GREEN, H_THRESHOLD_YELLOW, OVERWHELM_THRESHOLD,
    天干五行表, 地支五行表, 位置权重表, H权重,
)


# ══ T01 常量加载 ══
def test_constants_loaded():
    assert len(天干五行表) == 10
    assert len(地支五行表) == 12
    assert len(位置权重表) == 4
    assert abs(sum(H权重.values()) - 1.0) < 1e-9
    assert H_THRESHOLD_GREEN  == 0.80
    assert H_THRESHOLD_YELLOW == 0.50
    assert OVERWHELM_THRESHOLD == 0.40
    print("✅ T01 常量校验通过")


# ══ T02 五行强度计分 ══
def test_wuxing_qiang_du_jiazi():
    from modules.wuxing.core import 计算五行强度
    四柱 = {
        "年柱": {"天干": "甲", "地支": "子"},
        "月柱": {"天干": "甲", "地支": "子"},
        "日柱": {"天干": "甲", "地支": "子"},
        "时柱": {"天干": "甲", "地支": "子"},
    }
    r = 计算五行强度(四柱)
    得分 = r["五行得分"]
    assert 得分["木"] > 0
    assert 得分["水"] > 0
    assert 得分["火"] == 0.0
    assert 得分["金"] == 0.0
    assert 得分["土"] == 0.0
    print("✅ T02 五行强度计分通过")


# ══ T03 节点12字段校验 ══
def test_node_generation_and_validation():
    node = 生成节点("甲子丙午庚申壬戌", title="龍魂冲烟标准节点", raw_type="rule")
    ok, errors = 校验节点(node)
    assert ok, f"节点校验失败：{errors}"
    assert node["node_id"].startswith("FLOW-9622-")
    assert node["element"] in {"金", "木", "水", "火", "土"}
    assert node["action"] in {"enter", "hold", "fuse"}
    print(f"✅ T03 节点校验通过 | 五行={node['element']} action={node['action']}")


# ══ T04 黄金标准 甲子丙午庚申壬戌 -> H=0.927 🟢 ══
def test_T04_gold_standard_jiazi_bingwu_gengshen_renxu():
    """
    黄金标准 T04：甲子 丙午 庚申 壬戌 -> H=0.927 🟢
    DNA: #龍芯⚡️2026-08-31-五行计算器-v4.0-WELD-UID9622
    """
    r = 龍魂五行完整计算(
        年天干="甲", 年地支="子",
        月天干="丙", 月地支="午",
        日天干="庚", 日地支="申",
        时天干="壬", 时地支="戌",
    )
    H = r["对冲指数"]["对冲指数H"]
    三色 = r["对冲指数"]["三色"]
    print(f"\n🐉 T04 黄金标准测试")
    print(f"   四柱：甲子丙午庚申壬戌")
    print(f"   H = {H}  {三色}")
    print(f"   DNA = {r['DNA追溯']}")
    assert abs(H - 0.927) < 0.011, (
        f"🔴 T04 失败！H={H}，预期0.927±0.011\n"
        f"分项：{r['对冲指数']['分项']}\n"
        f"五行得分：{r['五行强度']['五行得分']}"
    )
    assert "🟢" in 三色, f"T04 预期🟢，实得{三色}"
    print("✅ T04 黄金标准通过 🟢 H=0.927")


# ══ T05 全火极考 -> H<0.80 ══
def test_T05_extreme_all_fire():
    r = 龍魂五行完整计算(
        年天干="丙", 年地支="午",
        月天干="丙", 月地支="午",
        日天干="丙", 日地支="午",
        时天干="丙", 时地支="午",
    )
    H = r["对冲指数"]["对冲指数H"]
    print(f"\n🔥 T05 全火极考：H={H}")
    assert H < H_THRESHOLD_GREEN, f"全火极端情况H应<0.80，实得{H}"
    print("✅ T05 全火极考通过")


# ══ T06 补益建议不为空 ══
def test_T06_buyi_not_empty_for_extreme():
    r = 龍魂五行完整计算(
        年天干="丙", 年地支="午",
        月天干="丙", 月地支="午",
        日天干="丙", 日地支="午",
        时天干="丙", 时地支="午",
    )
    assert len(r["补益建议"]) > 0
    print(f"✅ T06 补益建议数量={len(r['补益建议'])}，通过")


# ══ 入口 ══
if __name__ == "__main__":
    test_constants_loaded()
    test_wuxing_qiang_du_jiazi()
    test_node_generation_and_validation()
    test_T04_gold_standard_jiazi_bingwu_gengshen_renxu()
    test_T05_extreme_all_fire()
    test_T06_buyi_not_empty_for_extreme()
    print("\n🐉🟢 所有冲烟测试全部通过！")
    print("DNA: #龍芯⚡️2026-08-31-五行计算器-v4.0-WELD-UID9622")
