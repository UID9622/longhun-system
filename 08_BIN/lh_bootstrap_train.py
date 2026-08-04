#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 共生体数据自举训练集成 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-BOOTSTRAP-TRAIN-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

自举四步走（一条命令执行）:
  1. pool → train_bootstrap.jsonl
  2. merge  → 与现有训练数据混合
  3. verify → 验证格式完整性
  4. train  → 微调模型（可选）

用法:
  python3 bin/lh_bootstrap_train.py status     # 自举池状态
  python3 bin/lh_bootstrap_train.py merge      # 合并自举数据→训练集
  python3 bin/lh_bootstrap_train.py train      # merge + train
  python3 bin/lh_bootstrap_train.py demo       # 生成演示样本
"""

import json, os, sys, subprocess
from pathlib import Path
from datetime import datetime

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from engines.lh_symbiotic_bootstrap_engine import (
    SymbioticBootstrapEngine, BOOTSTRAP_DIR, POOL_FILE
)

TRAINER_SCRIPT = SYSTEM_ROOT / "bin" / "lh_lora_trainer_v4.py"
MODEL_DIR = SYSTEM_ROOT / "models" / "longhun-v4.1"
LORA_OUTPUT = MODEL_DIR / "lora_output"
DEFAULT_TRAIN_DATA = LORA_OUTPUT / "data" / "train.jsonl"
BOOTSTRAP_EXPORT = BOOTSTRAP_DIR / "train_bootstrap.jsonl"
MERGED_TRAIN = BOOTSTRAP_DIR / "train_merged.jsonl"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 命令
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def cmd_status():
    engine = SymbioticBootstrapEngine()
    st = engine.status()
    print("╔══════════════════════════════════════════╗")
    print("║  龍魂共生体 · 数据自举训练池              ║")
    print("╚══════════════════════════════════════════╝")
    print(f"\n自举池: {st['pool']['total_samples']} 条样本 · {st['pool']['total_messages']} 条消息 · avg Q={st['pool']['avg_quality']:.3f}")
    if st['pool']['by_team']:
        print("\n  按团队:")
        for t, c in sorted(st['pool']['by_team'].items()):
            print(f"    {t:10s} {c:4d}")
    if st['pool']['by_source']:
        print("\n  按类型:")
        for s, c in sorted(st['pool']['by_source'].items()):
            print(f"    {s:18s} {c:4d}")
    if st['pool']['by_audit']:
        print("\n  按审计:")
        for a, c in sorted(st['pool']['by_audit'].items()):
            print(f"    {a} {c:4d}")
    print(f"\n捕获器: {st['capture']['captured']} 次 · 待入库 {st['pending']} · 错误 {st['capture']['errors']}")
    if DEFAULT_TRAIN_DATA.exists():
        existing = sum(1 for _ in open(DEFAULT_TRAIN_DATA))
        print(f"现有训练数据: {existing} 条")
        if st['pool']['total_samples'] > 0:
            pct = st['pool']['total_samples'] / max(existing, 1) * 100
            print(f"自举贡献率: {pct:.1f}% ({st['pool']['total_samples']}/{existing})")
    else:
        print("现有训练数据: 未找到（先运行 lh_lora_trainer_v4.py prepare）")
    engine.shutdown()


def cmd_merge(existing_path=None, output_path=None):
    existing = Path(existing_path) if existing_path else DEFAULT_TRAIN_DATA
    output = Path(output_path) if output_path else MERGED_TRAIN

    engine = SymbioticBootstrapEngine()
    boot_samples = engine.pool.sample_count()

    if boot_samples == 0:
        print("⚠️ 自举池为空，请先生成样本: python3 bin/lh_bootstrap_train.py demo")
        return

    print("╔══════════════════════════════════════════╗")
    print("║  合并自举数据 → 训练集                    ║")
    print("╚══════════════════════════════════════════╝")

    # 1. 导出纯训练格式
    boot_export, boot_count = engine.pool.export_training_jsonl(BOOTSTRAP_EXPORT)
    print(f"\n[1/3] 自举数据导出: {boot_count} 条 → {boot_export}")

    # 2. 合并
    merged, exist_cnt, boot_cnt = engine.pool.export_merged(existing, output)
    total = exist_cnt + boot_cnt
    pct = boot_cnt / max(total, 1) * 100
    print(f"[2/3] 合并完成: {total} 条 (现有 {exist_cnt} + 自举 {boot_cnt} = {pct:.1f}% 自举)")
    print(f"      → {merged}")

    # 3. 验证格式
    print(f"[3/3] 格式验证...")
    errs = 0
    with open(merged, 'r') as f:
        for i, line in enumerate(f, 1):
            try:
                obj = json.loads(line)
                msgs = obj.get('messages', [])
                if not msgs or not all('role' in m and 'content' in m for m in msgs):
                    print(f"  行{i} 格式错误")
                    errs += 1
            except json.JSONDecodeError:
                print(f"  行{i} JSON解析错误")
                errs += 1

    if errs:
        print(f"\n⚠️ {errs} 条格式异常")
    else:
        print(f"   ✅ {total} 条全部通过ChatML验证")

    engine.pool.create_snapshot("merge")
    engine.shutdown()
    print(f"\n✅ 合并完成。下一步: python3 bin/lh_bootstrap_train.py train")


def cmd_train():
    """合并 + 训练"""
    # 先合并
    if not MERGED_TRAIN.exists():
        print("先合并数据...")
        cmd_merge()

    print("\n╔══════════════════════════════════════════╗")
    print("║  自举训练启动                              ║")
    print("╚══════════════════════════════════════════╝")

    # 备份原训练数据
    if DEFAULT_TRAIN_DATA.exists():
        bak = DEFAULT_TRAIN_DATA.with_suffix('.jsonl.bak_bootstrap')
        import shutil
        shutil.copy2(DEFAULT_TRAIN_DATA, bak)
        print(f"\n[备份] {DEFAULT_TRAIN_DATA} → {bak}")

    # 用合并数据替换训练数据
    import shutil
    DEFAULT_TRAIN_DATA.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(MERGED_TRAIN, DEFAULT_TRAIN_DATA)
    print(f"[替换] 训练数据已替换为合并数据 ({MERGED_TRAIN} → {DEFAULT_TRAIN_DATA})")

    # 统计
    total = sum(1 for _ in open(MERGED_TRAIN))
    engine = SymbioticBootstrapEngine()
    boot = engine.pool.sample_count()
    engine.shutdown()
    print(f"\n训练集统计: {total} 条 (含 {boot} 条自举数据 · {boot/max(total,1)*100:.1f}%)")

    # 跑训练
    print(f"\n{'='*50}")
    print(f"启动 MLX LoRA 微调...")
    print(f"{'='*50}\n")
    try:
        subprocess.run([sys.executable, str(TRAINER_SCRIPT), "train"], check=True)
        print(f"\n✅ 自举训练完成")
        print(f"备份恢复: cp {DEFAULT_TRAIN_DATA.with_suffix('.jsonl.bak_bootstrap')} {DEFAULT_TRAIN_DATA}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 训练失败 (exit={e.returncode})")
        print(f"恢复原训练数据: cp {DEFAULT_TRAIN_DATA.with_suffix('.jsonl.bak_bootstrap')} {DEFAULT_TRAIN_DATA}")


def cmd_demo():
    """生成演示样本"""
    print("╔══════════════════════════════════════════╗")
    print("║  共生体自举 · 演示模式                    ║")
    print("╚══════════════════════════════════════════╝")

    engine = SymbioticBootstrapEngine()
    before = engine.pool.sample_count()

    # 用 demo 子命令
    from engines.lh_symbiotic_bootstrap_engine import BootstrapConverter
    from engines.lh_team_orchestrator import TeamRun

    # 审计链演示
    run_audit = TeamRun(
        run_id="demo_bootstrap_audit",
        team_name="audit", task="审计 data/bootstrap/ 目录完整性",
        chain=["P05","P06","P13","P15"],
        start_time=datetime.now().isoformat(),
        end_time=datetime.now().isoformat(),
        results=[
            {"persona":"P05","chain_step":True,"status":"ok",
             "result":"【三色审计】data/bootstrap/ 目录文件完整，pool.jsonl 格式正确，index.json 存在且有效。🟢 全通过。"},
            {"persona":"P06","chain_step":True,"status":"ok",
             "result":"【数字根验证】pool.jsonl 行数→2+2→4(震)。sha256一致。P05审计结论数字根匹配。✅"},
            {"persona":"P13","chain_step":True,"status":"ok",
             "result":"【权限审查】data/bootstrap/ 权限: P05读√ P06读√ P03写√ P15读√。无越权。建议加锁文件防止并发写。"},
            {"persona":"P15","chain_step":True,"status":"ok",
             "result":"【DNA签章】四签: 身份√ 权限√ 数字根√ 伦理√。DNA: #龍芯⚡️丙午·乙未·BOOTSTRAP-AUDIT-7f3a1c2b。签章完成。"},
        ],
        blackboard_keys=[],
        audit={"status":"🟢","total":4,"ok":4,"error":0,"duration_ms":210}
    )

    # 开发链演示
    run_dev = TeamRun(
        run_id="demo_bootstrap_dev",
        team_name="dev", task="开发共生体自举引擎的Clippy通知功能",
        chain=["P00","P01","P04","P03"],
        start_time=datetime.now().isoformat(),
        end_time=datetime.now().isoformat(),
        results=[
            {"persona":"P00","chain_step":True,"status":"ok",
             "result":"【意图解析】用户需要'数据自举'进度通知。意图: 状态透明度 | 置信度95%。建议用简洁命令行输出+可选Bark推送，不引入重量级通知系统。"},
            {"persona":"P01","chain_step":True,"status":"ok",
             "result":"【战略推演】三路径: A) Bark推送(快,依赖外部) B) 飞书Webhook(稳,需配置) C) 本地toast(无依赖,仅Mac)。推荐C作为默认+B作为可选。推演结论: 低耦合,高可用。"},
            {"persona":"P04","chain_step":True,"status":"ok",
             "result":"【代码实现】Clippy通知: `bin/lh_bootstrap_train.py notify --type bark|feishu|cli`。用subprocess调用,超时3秒,失败无阻塞。三行核心代码,零新依赖。"},
            {"persona":"P03","chain_step":True,"status":"ok",
             "result":"【归档记录】结构化归档: 需求→意图→推演→实现四级全记录。存档路径: governance/audit/bootstrap_tasks/demo_20260724.md。四签齐全。"},
        ],
        blackboard_keys=[],
        audit={"status":"🟢","total":4,"ok":4,"error":0,"duration_ms":195}
    )

    conv = BootstrapConverter()
    s1 = conv.convert_team_run(run_audit, "audit", "安全审计")
    s2 = conv.convert_team_run(run_dev, "dev", "系统开发")
    all_s = s1 + s2

    deposited = engine.pool.deposit(all_s)
    engine.pool.save_index()
    engine.pool.create_snapshot("demo")

    after = engine.pool.sample_count()
    print(f"\n审计链 → {len(s1)} 条 | 开发链 → {len(s2)} 条")
    print(f"入库: {deposited} 条 (过滤 {len(all_s)-deposited} 条)")
    print(f"训练池: {before} → {after} ({after-before:+d} 条)")

    engine.shutdown()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 入口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="龍魂·共生体数据自举训练集成 v1.0")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("status", help="自举池状态")
    merge_p = sub.add_parser("merge", help="合并自举数据→训练集")
    merge_p.add_argument("--existing", type=str, help="现有训练数据路径（默认v4.1路径）")
    merge_p.add_argument("--output", type=str, help="合并输出路径")
    sub.add_parser("train", help="merge + 训练一步到位")
    sub.add_parser("demo", help="生成演示样本")

    args = p.parse_args()

    if args.cmd == "status":
        cmd_status()
    elif args.cmd == "merge":
        cmd_merge(args.existing, args.output)
    elif args.cmd == "train":
        cmd_train()
    elif args.cmd == "demo":
        cmd_demo()
    else:
        cmd_status()
