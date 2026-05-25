#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·Web3-DNA MVP集成测试
Integration Test: MVP Landing Chain + Memory Asset + Payment Gateway

DNA: #龍芯⚡️2026-05-25-WEB3-DNA-MVP-INTEGRATION-TEST-v1.0
UID: 9622

完整流程演示：
  1️⃣ 创建DNA记忆资产并定价
  2️⃣ 构造支付请求
  3️⃣ 执行11步MVP落地链
  4️⃣ 生成完整报告
"""

import sys
from pathlib import Path

# 确保可以导入web3_dna模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from mvp_landing_chain import MVPLandingChain
from mvp_dna_memory_asset import DNAMemoryAssetPricingEngine
from mvp_payment_gateway import PaymentGateway, PaymentRequest, TransactionType
import hashlib


def test_mvp_integration():
    """完整的MVP集成测试"""
    print("\n" + "=" * 80)
    print("🔗 龍魂 Web3-DNA MVP 完整集成测试")
    print("=" * 80 + "\n")

    # ────────────────────────────────────────────────────
    # 阶段1：DNA记忆资产定价
    # ────────────────────────────────────────────────────
    print("📍 阶段1: DNA记忆资产创建 & 定价\n")

    asset_engine = DNAMemoryAssetPricingEngine()

    # 创建3个DNA记忆资产
    assets = []
    test_memories = [
        {
            "owner": "user-001",
            "content": "成功实现龍魂系统v2.0与Web3-DNA的完整融合",
            "category": "professional",
            "keywords": ["龍魂", "Web3", "融合", "系统"],
        },
        {
            "owner": "user-002",
            "content": "三年创业失败的经验与从中学到的管理智慧",
            "category": "personal",
            "keywords": ["创业", "失败", "学习", "管理"],
        },
        {
            "owner": "user-003",
            "content": "论中华文化如何在AI时代重新定义人与机器的关系",
            "category": "scientific",
            "keywords": ["文化", "AI", "人机关系"],
        },
    ]

    for mem in test_memories:
        asset = asset_engine.create_dna_memory_asset(
            owner_id=mem["owner"],
            memory_content=mem["content"],
            category=mem["category"],
            metadata={"keywords": mem["keywords"]}
        )
        assets.append(asset)

        print(f"✅ 创建资产: {asset.asset_id}")
        print(f"   所有者: {asset.owner_id}")
        print(f"   质量分数: {asset.memory_quality_score}/100")
        print(f"   DNA: {asset.dna[:50]}...\n")

    # ────────────────────────────────────────────────────
    # 阶段2：资产定价
    # ────────────────────────────────────────────────────
    print("📍 阶段2: 资产定价\n")

    pricing_results = []
    for asset in assets:
        pricing = asset_engine.calculate_price(asset.asset_id)
        pricing_results.append(pricing)

        print(f"资产: {asset.asset_id}")
        print(f"  价格: {pricing.current_price} e-CNY")
        print(f"  质量因子: {pricing.quality_factor}")
        print(f"  市场因子: {pricing.market_factor}")
        print(f"  稀缺性: {pricing.rarity_coefficient}")
        print(f"  DNA: {pricing.dna[:50]}...\n")

    # ────────────────────────────────────────────────────
    # 阶段3：支付请求构造
    # ────────────────────────────────────────────────────
    print("📍 阶段3: 构造支付请求\n")

    payment_requests = []
    for i, pricing in enumerate(pricing_results):
        asset = assets[i]
        payment_id = hashlib.sha256(
            f"payment-{asset.asset_id}-{asset.owner_id}".encode()
        ).hexdigest()[:8]

        req = PaymentRequest(
            payment_id=payment_id,
            payer_id=asset.owner_id,
            payee_id="UID9622_DNA_ASSET_VAULT",
            amount=pricing.current_price,
            transaction_type=TransactionType.PURCHASE,
            description=f"购买DNA记忆资产: {asset.asset_id}",
            reference_id=asset.asset_id,
        )
        payment_requests.append(req)

        print(f"✅ 支付请求: {req.payment_id}")
        print(f"   付款人: {req.payer_id}")
        print(f"   金额: {req.amount} e-CNY")
        print(f"   资产: {req.reference_id}\n")

    # ────────────────────────────────────────────────────
    # 阶段4: 执行MVP落地链（11步）
    # ────────────────────────────────────────────────────
    print("📍 阶段4: 执行MVP落地链（11步）\n")

    chain = MVPLandingChain()
    payment_gateway = PaymentGateway()

    all_transactions = []

    for i, req in enumerate(payment_requests):
        asset = assets[i]

        print(f"🔄 处理交易 {i+1}/3: {asset.asset_id}\n")

        # 执行11步MVP落地链
        mvp_tx = chain.execute_mvp_landing_chain(
            user_id=asset.owner_id,
            auth_token=f"auth_token_{asset.asset_id}",
            dna_asset_id=asset.asset_id,
            operation_type="buy"
        )

        all_transactions.append(mvp_tx)

        print(f"✅ MVP落地链完成")
        print(f"   交易ID: {mvp_tx.tx_id}")
        print(f"   状态: {mvp_tx.status}")
        print(f"   步骤完成: {len(mvp_tx.steps)}/11")
        print(f"   DNA链长: {len(mvp_tx.dna_chain)}\n")

        # 执行支付
        payment_tx = payment_gateway.execute_payment(
            req,
            payer_real_name=f"User_{asset.owner_id}",
            payer_id_number="110101199003071234"
        )

        print(f"✅ 支付执行完成")
        print(f"   支付ID: {payment_tx.payment_id}")
        print(f"   状态: {payment_tx.status.value}")
        print(f"   KYC: {'✅' if payment_tx.kyc_check_passed else '❌'}")
        print(f"   AML: {'✅' if payment_tx.aml_check_passed else '❌'}")
        print(f"   风险分数: {payment_tx.risk_score}/100\n")

    # ────────────────────────────────────────────────────
    # 阶段5: 生成报告
    # ────────────────────────────────────────────────────
    print("📍 阶段5: 生成完整报告\n")

    report_content = "# 🐉 龍魂 Web3-DNA MVP 集成测试报告\n\n"
    report_content += f"**测试时间**: {pricing_results[0].effective_date}\n"
    report_content += f"**测试资产数**: {len(assets)}\n"
    report_content += f"**测试交易数**: {len(all_transactions)}\n\n"

    report_content += "## 资产定价总结\n\n"
    total_price = 0
    for pricing in pricing_results:
        report_content += f"- **{pricing.asset_id}**: {pricing.current_price} e-CNY\n"
        total_price += pricing.current_price
    report_content += f"\n**总计**: {total_price} e-CNY\n\n"

    report_content += "## 11步MVP落地链执行\n\n"
    for i, tx in enumerate(all_transactions):
        report_content += f"### 交易 {i+1}: {tx.tx_id}\n\n"
        report_content += f"- **状态**: {tx.status}\n"
        report_content += f"- **步骤数**: {len(tx.steps)}/11\n"
        report_content += f"- **DNA链长**: {len(tx.dna_chain)}\n"
        report_content += f"- **最后步骤**: Step {len(tx.steps)-1}: {tx.steps[-1].step.value}\n\n"

    report_content += "## DNA链追溯\n\n"
    if all_transactions:
        tx = all_transactions[0]
        report_content += "### 第一笔交易的DNA链\n\n"
        for dna in tx.dna_chain[:5]:  # 仅显示前5个
            report_content += f"→ {dna}\n"
        if len(tx.dna_chain) > 5:
            report_content += f"... (还有 {len(tx.dna_chain)-5} 条)\n"

    report_file = Path("/tmp/mvp_integration_test_report.md")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"✅ 报告已生成: {report_file}\n")

    # ────────────────────────────────────────────────────
    # 总结
    # ────────────────────────────────────────────────────
    print("=" * 80)
    print("✅ MVP集成测试完成")
    print("=" * 80)
    print(f"\n📊 统计数据:")
    print(f"  资产总数: {len(assets)}")
    print(f"  资产定价总额: {total_price} e-CNY")
    print(f"  完成的11步链: {len(all_transactions)}")
    print(f"  所有步骤成功率: {sum(1 for tx in all_transactions if tx.status == 'completed')}/{len(all_transactions)}")
    print(f"\n🐉 龍魂 Web3-DNA · MVP落地链 · UID9622不免责\n")

    return {
        "assets": assets,
        "pricing_results": pricing_results,
        "mvp_transactions": all_transactions,
        "report_file": report_file,
    }


if __name__ == "__main__":
    results = test_mvp_integration()
    print(f"\n✅ 测试结果已保存到报告文件")
