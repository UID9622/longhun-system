# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 底座重组 CLI v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-BASE-REORGANIZE-CLI-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

核心理念：
  参数是内功，模板是外挂。我们不偷外挂，只借别人的内功（开源权重），
  用我们自己的心法（数据/协议/场景）重炼，产出我们自己的真气（龍魂模型）。

三大铁律：
  1. 底座必须是中文的 — Qwen/DeepSeek-CN/Yi/GLM
  2. 内核必须是CNSH的 — 代码生成·审计报告·暗色鎏金·DNA追溯
  3. 关系线必须是我们的 — 概念关联注入 + DNA全链路追溯

用法:
  python3 bin/lh_reorganize.py scan                            # 扫描可用中文底座
  python3 bin/lh_reorganize.py register --base qwen2.5:7b      # 注册中文底座
  python3 bin/lh_reorganize.py overwrite --base qwen2.5:7b     # 覆盖训练（干运行预览）
  python3 bin/lh_reorganize.py overwrite --base qwen2.5:7b --live  # 实战训练
  python3 bin/lh_reorganize.py inject                          # 注入概念关系+CNSH场景
  python3 bin/lh_reorganize.py verify                          # 验证重组效果
  python3 bin/lh_reorganize.py pipeline --base qwen2.5:7b      # 一键全管线（干运行）
  python3 bin/lh_reorganize.py pipeline --base qwen2.5:7b --live # 一键全管线（实战）
  python3 bin/lh_reorganize.py trace                           # DNA追溯链
  python3 bin/lh_reorganize.py concepts                        # 查看概念关系定义
  python3 bin/lh_reorganize.py cnsh-scenarios                  # 生成CNSH场景数据
"""

import sys, os, json
from pathlib import Path

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))


def cmd_scan():
    """扫描可用的中文底座模型"""
    from engines.lh_base_reorganizer import BaseReorganizer, CHINESE_BASE_WHITELIST

    print("=" * 60)
    print("🔍 龍魂中文底座扫描")
    print("=" * 60)

    reorganizer = BaseReorganizer()
    result = reorganizer.scan()

    # 本地Ollama模型
    print("\n📦 本地Ollama模型:")
    ollama_models = result["local_models"].get("ollama", [])
    if ollama_models:
        for m in ollama_models:
            badge = "🇨🇳" if m.get("is_chinese") else "🇺🇸"
            status = "✅ 白名单" if m.get("in_whitelist") else ("⚠️ 非中文底座" if not m.get("is_chinese") else "❓ 未在白名单")
            print(f"  {badge} {m['name']:30s} {status}")
    else:
        print("  (未检测到Ollama模型，请先安装Ollama)")

    # 本地MLX模型
    print("\n💾 本地MLX权重:")
    mlx_models = result["local_models"].get("mlx", [])
    if mlx_models:
        for m in mlx_models:
            badge = "🇨🇳" if m.get("is_chinese") else ("🇺🇸" if m.get("is_english") else "❓")
            size = f"{m.get('size_gb', '?')}GB" if 'size_gb' in m else ""
            print(f"  {badge} {m['name']:40s} {size}")
    else:
        print("  (未检测到本地MLX权重)")

    # 已注册底座
    registered = result["registered_bases"]
    if registered:
        print(f"\n📋 已注册底座 ({len(registered)} 个):")
        for r in registered:
            print(f"  ✅ {r['model_id']:25s} {r['family']}·{r['params']}·{r['lang']}")
    else:
        print("\n📋 已注册底座: (无)")

    # 推荐
    print(f"\n🌟 推荐底座 ({len(result['recommended'])} 个):")
    for rec in result["recommended"]:
        print(f"  • {rec}")

    # 白名单总计
    print(f"\n📊 白名单中文底座: {result['whitelist_count']} 个")
    print(f"   系列: Qwen2.5({sum(1 for k in CHINESE_BASE_WHITELIST if 'qwen2.5' in k)}) + "
          f"Qwen3({sum(1 for k in CHINESE_BASE_WHITELIST if 'qwen3' in k)}) + "
          f"DeepSeek({sum(1 for k in CHINESE_BASE_WHITELIST if 'deepseek' in k)}) + "
          f"Yi({sum(1 for k in CHINESE_BASE_WHITELIST if 'yi' in k)}) + "
          f"GLM({sum(1 for k in CHINESE_BASE_WHITELIST if 'glm' in k)})")


def cmd_register(base: str):
    """注册中文底座"""
    from engines.lh_base_reorganizer import BaseReorganizer

    reorganizer = BaseReorganizer()
    try:
        model = reorganizer.register(base)
        print(f"\n✅ 底座注册成功")
        print(f"   ID: {model.model_id}")
        print(f"   系列: {model.family}")
        print(f"   参数: {model.params}")
        print(f"   语言: {model.lang}")
        print(f"   HF: {model.hf_model_id}")
        print(f"   DNA: {model.dna}")
    except ValueError as e:
        print(f"\n🔴 注册失败: {e}")
        sys.exit(1)


def cmd_overwrite(base: str, live: bool = False):
    """覆盖训练 — 用我们的数据重炼底座"""
    from engines.lh_base_reorganizer import BaseReorganizer

    reorganizer = BaseReorganizer()
    record = reorganizer.overwrite(base, dry_run=not live)

    if not live:
        print(f"\n💡 这是干运行预览。要实际训练请加 --live 参数。")
        print(f"   实际训练会调用 MLX LoRA，需要 Mac Apple Silicon。")
    else:
        print(f"\n⚔️ 实战训练已启动")
        print(f"   审计标记: {record.audit_mark}")
        if record.val_loss is not None:
            print(f"   Val Loss: {record.val_loss}")
        if record.errors:
            print(f"   ⚠️ 错误: {record.errors}")


def cmd_inject():
    """注入概念关系 + CNSH场景"""
    from engines.lh_base_reorganizer import BaseReorganizer

    reorganizer = BaseReorganizer()
    record = reorganizer.inject()

    print(f"\n✅ 概念关系注入完成")
    print(f"   概念对: {record.concept_pairs_injected}")
    print(f"   CNSH场景: {record.cnsh_scenarios_generated}")
    print(f"   DNA: {record.dna}")
    print(f"\n💡 概念关系数据已存入 data/reorganize/concept_relations/")
    print(f"   CNSH场景数据已存入 data/reorganize/cnsh_scenarios/")
    print(f"   下次覆盖训练时会自动包含这些数据。")


def cmd_verify():
    """验证重组效果"""
    from engines.lh_base_reorganizer import BaseReorganizer

    reorganizer = BaseReorganizer()
    record = reorganizer.verify()
    integrity = reorganizer.trace_chain.verify_integrity()

    print(f"\n📊 验证结果:")
    print(f"   审计标记: {record.audit_mark}")
    print(f"   DNA链完整: {'✅' if integrity['chain_integrity'] else '🔴'}")
    print(f"   追溯记录: {integrity['total_records']} 条")
    print(f"   覆盖阶段: {integrity['phases_covered']}")
    print(f"   Merkle根: {integrity['merkle_root'][:16]}...")

    if integrity['broken_links']:
        print(f"\n🔴 断裂链接:")
        for bl in integrity['broken_links']:
            print(f"   位置: {bl['at']}")
            print(f"   期望: {bl['expected_parent']}")
            print(f"   实际: {bl['actual_parent']}")


def cmd_pipeline(base: str, live: bool = False):
    """一键全管线"""
    from engines.lh_base_reorganizer import BaseReorganizer

    reorganizer = BaseReorganizer()
    report = reorganizer.pipeline(base, dry_run=not live)

    if not live:
        print(f"\n💡 这是干运行预览。要实战请加 --live。")

    return report


def cmd_trace():
    """DNA追溯链"""
    from engines.lh_base_reorganizer import DNATraceChain

    chain = DNATraceChain()
    integrity = chain.verify_integrity()

    print("=" * 60)
    print("🔗 DNA全链路追溯")
    print("=" * 60)

    records = chain.get_full_chain()
    if not records:
        print("\n(尚无追溯记录，请先执行 pipeline)")
        return

    print(f"\n追溯记录: {len(records)} 条")
    print(f"链完整性: {'✅' if integrity['chain_integrity'] else '🔴'}")
    print(f"Merkle根: {integrity['merkle_root'][:16]}...\n")

    for i, r in enumerate(records):
        phase_icon = {"register": "📋", "overwrite": "⚔️", "inject": "💉", "verify": "🔍"}.get(r.phase.value, "❓")
        print(f"  [{i+1}] {phase_icon} {r.phase.value:12s} | 底座: {r.base_model:20s} | {r.audit_mark}")
        print(f"      DNA: {r.dna}")
        if r.concept_pairs_injected:
            print(f"      概念对: {r.concept_pairs_injected} | CNSH场景: {r.cnsh_scenarios_generated}")
        if r.val_loss is not None:
            print(f"      Val Loss: {r.val_loss}")
        if r.parent_dna:
            print(f"      上游DNA: {r.parent_dna}")
        print()

    if integrity['broken_links']:
        print(f"🔴 链断裂: {len(integrity['broken_links'])} 处")


def cmd_concepts():
    """查看龍魂概念关系定义"""
    from engines.lh_base_reorganizer import LONGHUN_CONCEPT_RELATIONS

    print("=" * 60)
    print("🧠 龍魂概念关系体系")
    print("=" * 60)

    for concept, relations in LONGHUN_CONCEPT_RELATIONS.items():
        print(f"\n## {concept}")
        print(f"  上位概念: {', '.join(relations['parents'])}")
        print(f"  下位概念: {', '.join(relations['children'])}")
        print(f"  对立面:   {', '.join(relations['opposites'])}")
        print(f"  铁律:")
        for ax in relations['axioms']:
            print(f"    • {ax}")

    print(f"\n总概念数: {len(LONGHUN_CONCEPT_RELATIONS)}")
    total_pairs = sum(
        len(r['parents']) + len(r['children']) + len(r['opposites'])
        for r in LONGHUN_CONCEPT_RELATIONS.values()
    )
    print(f"总关系对数: {total_pairs}")


def cmd_cnsh_scenarios():
    """生成CNSH场景训练数据"""
    from engines.lh_base_reorganizer import CNSHScenarioGenerator

    gen = CNSHScenarioGenerator()
    scenarios = gen.generate_scenarios(count_per_type=20)

    # 统计
    from collections import Counter
    by_type = Counter(s.scenario_type for s in scenarios)

    print("=" * 60)
    print("🎬 CNSH场景训练数据生成")
    print("=" * 60)

    print(f"\n总场景数: {len(scenarios)}")
    print(f"\n按类型分布:")
    for stype, count in by_type.most_common():
        type_names = {
            "code_generation": "代码生成（CNSH→Python）",
            "audit_report": "审计报告（三色+德本五问）",
            "dark_golden_page": "暗色鎏金页面（HTML）",
            "dna_trace": "DNA追溯报告",
            "protocol_query": "协议查询（CNSH格式）",
        }
        print(f"  {type_names.get(stype, stype)}: {count} 条")

    # 导出
    out = gen.export_training_jsonl(scenarios)
    print(f"\n✅ 已导出到: {out}")

    # 展示示例
    print(f"\n📋 示例（前2条）:")
    for i, s in enumerate(scenarios[:2]):
        print(f"\n  [{i+1}] {s.scenario_type}")
        print(f"    User: {s.user_prompt[:100]}...")
        print(f"    DNA: {s.dna}")


def cmd_cnsh_corpus(count: int = 100):
    """生成CNSH启蒙语料库（任务/规则/审计）"""
    from engines.lh_base_reorganizer import CNSHTrainingCorpusGenerator

    gen = CNSHTrainingCorpusGenerator()
    out = gen.export_corpus(count_per_domain=count)

    print("=" * 60)
    print("📚 CNSH启蒙语料库生成")
    print("=" * 60)
    print(f"\n每个领域: {count} 条")
    print(f"领域: task_definition / rule_definition / audit_execution")
    print(f"总条数: {count * 3}")
    print(f"\n✅ 已导出到: {out}")
    print("\n💡 这套语料是教AI『用CNSH思考』的启蒙教材。")
    print("   覆盖：任务定义 · 规则定义 · 审计执行")


def cmd_auto_distill(dry_run: bool = False, smoke: bool = False,
                     skip_train: bool = False, skip_audit: bool = False):
    """自动蒸馏循环入口 — 调用 bin/lh_auto_distill.py"""
    import subprocess
    import sys

    cmd = [sys.executable, str(SYSTEM_ROOT / "bin" / "lh_auto_distill.py")]
    if dry_run:
        cmd.append("--dry-run")
    if smoke:
        cmd.append("--smoke")
    if skip_train:
        cmd.append("--skip-train")
    if skip_audit:
        cmd.append("--skip-audit")

    print("=" * 60)
    print("🐉 启动自动蒸馏循环")
    print("=" * 60)
    print(f"命令: {' '.join(cmd)}")
    print()

    result = subprocess.run(cmd, cwd=SYSTEM_ROOT)
    sys.exit(result.returncode)


# ═══════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════

def main():
    import argparse

    p = argparse.ArgumentParser(
        description="龍魂底座重组 CLI v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s scan                              # 扫描可用底座
  %(prog)s register --base qwen2.5:7b        # 注册中文底座
  %(prog)s overwrite --base qwen2.5:7b       # 覆盖训练（干运行预览）
  %(prog)s overwrite --base qwen2.5:7b --live # 实战训练
  %(prog)s inject                            # 注入概念关系
  %(prog)s pipeline --base qwen2.5:7b        # 一键全管线（干运行）
  %(prog)s pipeline --base qwen2.5:7b --live  # 一键全管线（实战）
  %(prog)s trace                             # DNA追溯链
  %(prog)s concepts                          # 查看概念关系
        """,
    )

    sp = p.add_subparsers(dest="cmd", help="子命令")

    # scan
    sp.add_parser("scan", help="扫描可用中文底座模型")

    # register
    reg = sp.add_parser("register", help="注册中文底座模型")
    reg.add_argument("--base", required=True, help="底座模型ID，如 qwen2.5:7b, deepseek-r1:7b")

    # overwrite
    ow = sp.add_parser("overwrite", help="覆盖训练 — 用龍魂数据重炼底座")
    ow.add_argument("--base", required=True, help="底座模型ID")
    ow.add_argument("--live", action="store_true", help="实战训练（不加则干运行预览）")

    # inject
    sp.add_parser("inject", help="注入概念关系 + CNSH场景训练数据")

    # verify
    sp.add_parser("verify", help="验证重组效果 + DNA追溯链完整性")

    # pipeline
    pipe = sp.add_parser("pipeline", help="一键执行完整重组管线")
    pipe.add_argument("--base", required=True, help="底座模型ID")
    pipe.add_argument("--live", action="store_true", help="实战模式（不加则干运行预览）")

    # trace
    sp.add_parser("trace", help="查看DNA全链路追溯")

    # concepts
    sp.add_parser("concepts", help="查看龍魂概念关系定义体系")

    # cnsh-scenarios
    sp.add_parser("cnsh-scenarios", help="生成CNSH场景训练数据")

    # cnsh-corpus
    corpus = sp.add_parser("cnsh-corpus", help="生成CNSH启蒙语料库（任务/规则/审计）")
    corpus.add_argument("--count", type=int, default=100, help="每个领域生成条数，默认100")

    # auto-distill
    distill = sp.add_parser("auto-distill", help="自动蒸馏循环：修复→测试→训练→审计→v4.1.9")
    distill.add_argument("--dry-run", action="store_true", help="干运行预览")
    distill.add_argument("--smoke", action="store_true", help="冒烟模式（5 iter）")
    distill.add_argument("--skip-train", action="store_true", help="跳过训练")
    distill.add_argument("--skip-audit", action="store_true", help="跳过审计")

    args = p.parse_args()

    if args.cmd == "scan":
        cmd_scan()
    elif args.cmd == "register":
        cmd_register(args.base)
    elif args.cmd == "overwrite":
        cmd_overwrite(args.base, live=getattr(args, 'live', False))
    elif args.cmd == "inject":
        cmd_inject()
    elif args.cmd == "verify":
        cmd_verify()
    elif args.cmd == "pipeline":
        cmd_pipeline(args.base, live=getattr(args, 'live', False))
    elif args.cmd == "trace":
        cmd_trace()
    elif args.cmd == "concepts":
        cmd_concepts()
    elif args.cmd == "cnsh-scenarios":
        cmd_cnsh_scenarios()
    elif args.cmd == "cnsh-corpus":
        cmd_cnsh_corpus(args.count)
    elif args.cmd == "auto-distill":
        cmd_auto_distill(
            dry_run=args.dry_run,
            smoke=args.smoke,
            skip_train=args.skip_train,
            skip_audit=args.skip_audit,
        )
    else:
        p.print_help()


if __name__ == "__main__":
    main()
