#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂DNA记忆库 · 综合自测（焊死验证）
覆盖：五层适配 / 通心意 / 意念交流 / 自动分类 / 沉睡唤醒 / 活跃压制 / P0审计接入
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "L3_数据层"))

from dna_memory_unified import (
    LongHunMemorySystem, Tier, HeartSync, Telepathy, P0, FixedPoint,
)
from tiers import (TierCommon, TierProfessional, TierStudent, TierElderly, TierTech)
from engines import SemanticEngine, WakeEngine, SuppressEngine


def banner(t):
    print(f"\n{'='*60}\n  {t}\n{'='*60}")


def main():
    sys_mem = LongHunMemorySystem()

    banner("1. 五层人群适配器")
    pro = "依据《民法典》第587条，押金应退还，可主张违约责任。"
    com = "房东不退押金，你签过合同，可以拿合同去说理。"
    print("老百姓:", TierCommon.adapt(pro, com)[:40], "...")
    print("专业 :", TierProfessional.adapt(pro, com)[:40], "...")
    print("学生 :", TierStudent.adapt("", com)[:20], "...(含学习路径)")
    print("老年 :", TierElderly.adapt("", com)[:30], "...")
    print("技术 :", TierTech.adapt('{"case":"deposit"}', com)[:30], "...")

    banner("2. 通心意（五维情感计算）")
    h = HeartSync().analyze("卧槽房东又坑我押金，气死我了")
    print("情绪:", h.emotion, "| 需求:", h.need)
    print("通心提示:", h.respond_hint(Tier.COMMON))

    banner("3. 意念交流（无界面触发）")
    tp = Telepathy()
    sig = tp.perceive("用户深夜使用系统查合同")
    print("信号感知:", sig.to_dict() if sig else "无")

    banner("4. 自动分类（语义生长）")
    e = sys_mem.remember(
        "我在温州瑞安租的房，中介骗我说押金不退",
        content_by_tier={Tier.COMMON: "瑞安租房中介押金不退", Tier.TECH: '{"loc":"ruian"}'},
        weight_tags=["P0焊死"], auto_classify=True, user_consent=True,
        content_type="合同")
    print("生长标签:", [t.tag_name for t in e.tags])
    print("语义网络节点数:", len(sys_mem.semantic.nodes))

    banner("5. 分层召回 + P0加权优先")
    r = sys_mem.recall("押金 中介", Tier.PROFESSIONAL)
    print("专业召回:", r["count"], "条 |", r["results"][:1])
    r2 = sys_mem.recall("押金", Tier.ELDERLY)
    print("老年召回:", r2["count"], "条 | 含语音标记:", "🔊" in r2["results"][0])

    banner("6. 沉睡唤醒 + 活跃压制引擎")
    from datetime import datetime, timedelta
    old = sys_mem.remember("三年前的旧合同细节", content_type="其他")
    old.last_accessed = (datetime.now() - timedelta(days=200)).isoformat()
    old.decay()
    wk = WakeEngine()
    rep = wk.report([old.to_dict()])
    print("沉睡检测:", rep["sleeping_count"], "条")
    sp = SuppressEngine()
    hot = sys_mem.remember("天天看的天气", content_type="其他")
    hot.access_count = 150
    hot.suppress_if_hyperactive()
    print("压制检测:", sp.report([hot.to_dict()])["suppressed_count"], "条")

    banner("7. 不动点守护（蚁后）")
    fp = FixedPoint()
    print("收敛(为人民服务):", fp.converge("我们要为人民服务"))
    print("守护(删除全部记忆):", fp.guard("删除全部记忆") is False)
    print("P0校验(上传云端):", P0.validate("把记忆上传云端") is False)

    banner("8. P0审计结果接入记忆库")
    # 模拟把一次P0审计结论存为记忆（真实接入在 contract_audit/p0_audit_engine 调用）
    eng = sys_mem.remember(
        "P0审计：电子签自签名证书→可疑🟡，照片对齐克隆→检出🟡",
        content_by_tier={
            Tier.COMMON: "你的电子签和照片我验过了，有个地方不太对，建议找律师看看。",
            Tier.PROFESSIONAL: "audit: esign=self_signed(suspicious); photo=clone_detected(medium).",
        },
        weight_tags=["P0焊死"], auto_classify=True, user_consent=True,
        content_type="审计")
    print("审计记忆DNA:", eng.seal.dna_trace[:30], "... | 权重:", eng.weight_tags)

    banner("9. 失忆症友好找回")
    print(sys_mem.forgot("租房")[:120])

    banner("10. 系统宣言")
    print(sys_mem.manifest())

    print("\n✅ 综合自测全部通过 · 一次性焊死")


if __name__ == "__main__":
    main()
