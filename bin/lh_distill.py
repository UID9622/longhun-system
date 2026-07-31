# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 知识蒸馏 CLI v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-DISTILL-CLI-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

统一蒸馏入口。四步走：侦察 → 蒸馏 → 炼化 → 入库。

用法:
  python3 bin/lh_distill.py scan                          # 侦察蒸馏源
  python3 bin/lh_distill.py distill --source deepseek     # 蒸馏DeepSeek
  python3 bin/lh_distill.py distill --source kimi         # 蒸馏Kimi
  python3 bin/lh_distill.py distill --source all --refine # 全蒸馏+炼化
  python3 bin/lh_distill.py refine                        # 炼化入库
  python3 bin/lh_distill.py status                        # 蒸馏状态
  python3 bin/lh_distill.py import-kimi                   # 导入Kimi对话
  python3 bin/lh_distill.py pipeline                      # 一键全管线
"""

import argparse, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))


def cmd_scan():
    """侦察所有蒸馏源"""
    from engines.lh_knowledge_distiller import DistillOrchestrator
    orch = DistillOrchestrator()
    sources = orch.scan()
    
    print(f"\n{'='*60}")
    print("📡 知识蒸馏源侦察")
    print(f"{'='*60}")
    
    for name, info in sources.items():
        print(f"\n── {name} ──")
        for k, v in info.items():
            print(f"  {k}: {v}")
    
    # 总结
    ds_ready = "🟢" if "🟢" in sources["deepseek"]["weights"] else "🟡"
    kimi_ready = "🟢" if "🟢" in sources["kimi"]["status"] else "🔴"
    
    print(f"\n📊 综合评估:")
    print(f"   DeepSeek: {ds_ready} | Kimi: {kimi_ready} | 小米: 无数据")
    print(f"   可蒸馏源: {sum(1 for s in ['deepseek','kimi'] if '🟢' in str(sources.get(s,{})))} / 2")
    print(f"{'='*60}")


def cmd_distill(args):
    """执行蒸馏"""
    from engines.lh_knowledge_distiller import DistillOrchestrator
    orch = DistillOrchestrator()
    
    if args.source == "all":
        orch.distill_all(max_per_source=args.max)
    else:
        orch.distill_source(args.source, max_samples=args.max)
    
    orch.print_report()
    
    if args.refine:
        print("\n🔧 自动炼化入库...")
        result = orch.refine_and_merge()
        _print_refine_result(result)
    
    # 保存报告
    _save_report(orch)


def cmd_refine(args):
    """炼化入库"""
    from engines.lh_knowledge_distiller import DistillOrchestrator
    orch = DistillOrchestrator()
    
    # 如果指定了输入文件，加载到 orch
    if args.input and Path(args.input).exists():
        from engines.lh_knowledge_distiller import DistillSample, Deduplicator
        with open(args.input, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    meta = record.get("metadata", {})
                    msgs = record.get("messages", [])
                    if msgs:
                        sample = DistillSample(
                            sample_id=meta.get("dna", ""),
                            source=meta.get("source", ""),
                            source_model=meta.get("source_model", ""),
                            messages=msgs,
                            quality_score=meta.get("quality", 0.5),
                            domain=meta.get("domain", ""),
                            dna=meta.get("dna", ""),
                            tags=meta.get("tags", []),
                        )
                        orch.all_samples.append(sample)
    
    result = orch.refine_and_merge(quality_threshold=args.quality)
    _print_refine_result(result)


def cmd_status():
    """蒸馏状态"""
    from engines.lh_knowledge_distiller import DistillOrchestrator, DISTILL_DIR, TRAINING_DATA_DIR
    orch = DistillOrchestrator()
    status = orch.get_status()
    
    print(f"\n{'='*50}")
    print("🧬 知识蒸馏状态")
    print(f"{'='*50}")
    print(f"\n📂 蒸馏输出: {status['distill_dir']}")
    print(f"   导出批次数: {status['export_files']}")
    print(f"   总蒸馏样本: {status['total_distilled']}")
    print(f"   已入训练集: {status['train_merged']}")
    
    if status["domains"]:
        print(f"\n📊 领域分布:")
        for domain, count in status["domains"].items():
            bar = "█" * min(count // 5, 40)
            print(f"   {domain}: {count} {bar}")
    
    if status["last_reports"]:
        print(f"\n📈 最近批次:")
        for src, r in status["last_reports"].items():
            print(f"   {src}: 候选{r['candidates']} → 过闸{r['passed']} → 去重后{r['final']} | 均质{r['avg_quality']:.3f}")
    
    # 训练集统计
    train_count = 0
    if TRAINING_DATA_DIR.exists():
        for tf in TRAINING_DATA_DIR.glob("*.jsonl"):
            try:
                with open(tf, 'r', encoding='utf-8') as f:
                    train_count += sum(1 for _ in f)
            except:
                pass
    print(f"\n📚 训练集总量: {train_count} 条")
    print(f"{'='*50}")


def cmd_import_kimi(args):
    """导入 Kimi 对话"""
    print("🔄 导入 Kimi 对话历史...")
    from bin.lh_chat_importer import ChatImporter
    importer = ChatImporter()
    sessions = importer.import_kimi_conversations(max_sessions=args.max)
    
    if sessions:
        stats = importer.get_stats()
        print(f"\n📊 导入统计:")
        print(f"   会话: {stats['total_sessions']} | 总轮次: {stats['total_turns']} | 均质: {stats['avg_quality']:.2f}")
        for src, cnt in stats["by_source"].items():
            print(f"   {src}: {cnt}")
        
        if not args.no_export:
            importer.export_chatml()
    else:
        print("⚠️ 未导入任何 Kimi 会话")


def cmd_pipeline(args):
    """一键全管线：导入 → 蒸馏 → 炼化"""
    print(f"\n{'='*60}")
    print("🧬 龍魂·知识蒸馏全管线")
    print(f"   启动时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"{'='*60}")
    
    # Step 1: 导入 Kimi
    print(f"\n── 第一步: 导入对话 ──")
    if args.skip_import:
        print("  ⏭️ 跳过")
    else:
        from bin.lh_chat_importer import ChatImporter
        importer = ChatImporter()
        importer.import_deepseek_conversations()
        importer.import_kimi_conversations(max_sessions=args.max_import)
        importer.export_chatml()
    
    # Step 2: 蒸馏
    print(f"\n── 第二步: 蒸馏 ──")
    from engines.lh_knowledge_distiller import DistillOrchestrator
    orch = DistillOrchestrator()
    orch.distill_all(max_per_source=args.max_distill)
    orch.print_report()
    
    # Step 3: 炼化
    print(f"\n── 第三步: 炼化入库 ──")
    result = orch.refine_and_merge()
    _print_refine_result(result)
    
    # 总结
    print(f"\n{'='*60}")
    print(f"✅ 全管线完成")
    print(f"   总蒸馏样本: {result.get('after_requality', 0)}")
    print(f"   已入训练集: {result.get('merged', 0)}")
    print(f"{'='*60}")


def _print_refine_result(result: dict):
    print(f"   原始: {result.get('total_raw', 0)}")
    print(f"   去重后: {result.get('after_global_dedup', 0)}")
    print(f"   质量筛: {result.get('after_requality', 0)}")
    print(f"   导出: {result.get('exported', 0)}")
    print(f"   入库: {result.get('merged', 0)}")
    if result.get("errors"):
        print(f"   ⚠️ 错误: {len(result['errors'])}")


def _save_report(orch):
    """保存蒸馏报告"""
    from engines.lh_knowledge_distiller import DISTILL_DIR
    report_path = DISTILL_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sources": {},
    }
    for src, r in orch.reports.items():
        report_data["sources"][src] = {
            "candidates": r.total_candidates,
            "passed_quality": r.passed_quality,
            "after_dedup": r.after_dedup,
            "avg_quality": round(r.avg_quality, 3),
            "domains": r.domains,
            "reasoning_samples": r.reasoning_samples,
            "dna": r.dna,
            "started": r.started_at,
            "finished": r.finished_at,
        }
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    print(f"\n📋 报告已保存: {report_path.name}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI 入口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    p = argparse.ArgumentParser(
        description="龍魂·知识蒸馏CLI v1.0 — 别人的大豆·我们的油",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s scan                        侦察蒸馏源
  %(prog)s distill --source deepseek   蒸馏DeepSeek
  %(prog)s distill --source kimi       蒸馏Kimi
  %(prog)s distill --source all --refine  全蒸馏+炼化
  %(prog)s import-kimi                 导入Kimi对话
  %(prog)s pipeline                    一键全管线
        """
    )
    sub = p.add_subparsers(dest="cmd")
    
    sub.add_parser("scan", help="侦察所有蒸馏源")
    
    dist_p = sub.add_parser("distill", help="执行蒸馏")
    dist_p.add_argument("--source", choices=["deepseek", "kimi", "all"],
                        default="all", help="蒸馏源 (默认: all)")
    dist_p.add_argument("--max", type=int, default=500, help="每源最大样本数")
    dist_p.add_argument("--refine", action="store_true", help="蒸馏后立即炼化入库")
    
    refine_p = sub.add_parser("refine", help="炼化入库")
    refine_p.add_argument("--input", type=str, help="指定输入文件")
    refine_p.add_argument("--quality", type=float, default=0.7, help="质量阈值")
    
    sub.add_parser("status", help="蒸馏状态")
    
    imp_p = sub.add_parser("import-kimi", help="导入Kimi对话历史")
    imp_p.add_argument("--max", type=int, default=100, help="最大会话数")
    imp_p.add_argument("--no-export", action="store_true", help="不导出ChatML")
    
    pipe_p = sub.add_parser("pipeline", help="一键全管线（导入→蒸馏→炼化）")
    pipe_p.add_argument("--skip-import", action="store_true", help="跳过导入步骤")
    pipe_p.add_argument("--max-import", type=int, default=100, help="最大导入会话数")
    pipe_p.add_argument("--max-distill", type=int, default=500, help="最大蒸馏样本数")
    
    args = p.parse_args()
    
    if args.cmd == "scan":
        cmd_scan()
    elif args.cmd == "distill":
        cmd_distill(args)
    elif args.cmd == "refine":
        cmd_refine(args)
    elif args.cmd == "status":
        cmd_status()
    elif args.cmd == "import-kimi":
        cmd_import_kimi(args)
    elif args.cmd == "pipeline":
        cmd_pipeline(args)
    else:
        # 无参数默认 scan
        cmd_scan()


if __name__ == "__main__":
    main()
