#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
龍魂·知识库扩展自动化引擎 v1.0
DNA: #龍芯⚡️2026-07-21-KB-EXPAND-AUTO-v1.0
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

一键自动化: 爬取 → 清洗 → 索引 → 训练
   lh_kb_expand.py crawl                 # 爬取新知识
   lh_kb_expand.py index                 # 生成网站索引
   lh_kb_expand.py train-prep            # 准备训练数据
   lh_kb_expand.py train                 # 全量训练流程
   lh_kb_expand.py all                   # 一键全流程
   lh_kb_expand.py status                # 查看知识库状态

设计原则:
  - P0协议: 摘要只取·全文人工确认
  - 数据主权归本地·不传云
  - 每步DNA绑定·全程可追溯
  - 网站索引自动生成·搜得到·看得见
"""

import json
import os
import sys
import hashlib
import argparse
import subprocess
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import Counter

CST = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).parent.parent
SOURCES_DIR = PROJECT_ROOT / "data" / "sources"
KNOWLEDGE_DIR = PROJECT_ROOT / "data" / "knowledge"
INDEX_DIR = PROJECT_ROOT / "portal" / "knowledge"
CRAWLER_SCRIPT = PROJECT_ROOT / "bin" / "lh_summary_crawler.py"
FETCH_SCRIPT = SOURCES_DIR / "lh_fetch_engine.py"
CLEAN_SCRIPT = SOURCES_DIR / "lh_data_cleaner.py"
BRIDGE_SCRIPT = PROJECT_ROOT / "bin" / "lh_data_to_train_bridge.py"
TRAIN_SCRIPT = PROJECT_ROOT / "bin" / "lh_lora_trainer_v4.py"

DNA = "#龍芯⚡️2026-07-21-KB-EXPAND-AUTO-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def log(msg: str, level: str = "INFO"):
    ts = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
    prefix = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴"}.get(level, "ℹ️")
    print(f"[{ts}] {prefix} {msg}")


def run_step(cmd: list[str], desc: str, cwd=None, timeout: int | None = 600) -> bool:
    """执行一个步骤，返回成功/失败"""
    log(f"执行: {desc}")
    try:
        result = subprocess.run(cmd, cwd=cwd or str(PROJECT_ROOT),
                                capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0:
            log(f"{desc} → 完成", "OK")
            return True
        else:
            log(f"{desc} → 失败 (code={result.returncode})", "ERROR")
            if result.stderr.strip():
                print(f"  stderr: {result.stderr[:500]}")
            return False
    except subprocess.TimeoutExpired:
        log(f"{desc} → 超时", "ERROR")
        return False
    except Exception as e:
        log(f"{desc} → 异常: {e}", "ERROR")
        return False


# ━━━━━━━━━━ Step 1: 爬取 ━━━━━━━━━━

def crawl_sources(priority: str = "P0,P1", limit: int = 50):
    """用拉取引擎爬取知识源"""
    log(f"🕷️ 知识爬取启动 · 优先级: {priority} · 每源最多 {limit} 篇")
    log(f"   DNA: {DNA}")

    # 检查拉取引擎是否存在
    if not FETCH_SCRIPT.exists():
        log("拉取引擎不存在: data/sources/lh_fetch_engine.py", "ERROR")
        log("请确保项目完整，缺少 fetch engine", "ERROR")
        return False

    # 遍历优先级
    priorities = [p.strip() for p in priority.split(",")]
    all_ok = True
    for p in priorities:
        ok = run_step(
            [sys.executable, str(FETCH_SCRIPT), "--priority", p],
            f"拉取 {p} 优先级源"
        )
        if not ok:
            all_ok = False

    # 统计结果
    fetched_dir = SOURCES_DIR / "fetched"
    if fetched_dir.exists():
        files = list(fetched_dir.glob("*.jsonl"))
        log(f"拉取完成: {len(files)} 个文件")

    return all_ok


# ━━━━━━━━━━ Step 2: 清洗 ━━━━━━━━━━

def clean_data():
    """清洗拉取的原始数据"""
    log("🧹 数据清洗")

    if not CLEAN_SCRIPT.exists():
        log("清洗脚本不存在，尝试用 fetch engine 内置清洗", "WARN")
        return run_step(
            [sys.executable, str(FETCH_SCRIPT), "--clean-only"],
            "内置数据清洗"
        )

    return run_step(
        [sys.executable, str(CLEAN_SCRIPT)],
        "数据清洗"
    )


# ━━━━━━━━━━ Step 3: 生成网站索引 ━━━━━━━━━━

def generate_index():
    """从清洗数据生成网站知识索引"""
    log("📇 生成知识索引")

    cleaned_dir = SOURCES_DIR / "cleaned"
    if not cleaned_dir.exists():
        log("没有清洗数据，先执行 crawl + clean", "WARN")
        return False

    # 加载来源配置（用于分类映射）
    sources_file = SOURCES_DIR / "sources.json"
    source_map = {}  # source_id -> {name, category_id, category_name}
    if sources_file.exists():
        with open(sources_file) as f:
            src_config = json.load(f)
        cats = src_config.get("categories", {})
        for s in src_config.get("sources", []):
            sid = s.get("id", "")
            cat_id = s.get("category", "")
            cat_name = cats.get(cat_id, {}).get("name", cat_id)
            source_map[sid] = {
                "name": s.get("name", sid),
                "category_id": cat_id,
                "category_name": cat_name
            }

    # 读取所有已清洗数据
    articles = []
    for cf in sorted(cleaned_dir.glob("*_cleaned.jsonl")):
        with open(cf) as f:
            for line in f:
                try:
                    art = json.loads(line.strip())
                    articles.append(art)
                except json.JSONDecodeError:
                    continue

    log(f"读取 {len(articles)} 条清洗数据")

    if not articles:
        log("无数据可索引", "WARN")
        return False

    # 构建索引
    kb_index = {
        "dna": DNA,
        "confirm": CONFIRM,
        "generated_at": datetime.now(CST).isoformat(),
        "total_articles": len(articles),
        "categories": {},
        "articles": []
    }

    # 按来源分组
    source_counts = Counter()
    category_counts = Counter()

    for art in articles:
        q = art.get("quality", {})
        if q.get("score", 0) < 0.4:
            continue  # 跳过低质量

        source_id = art.get("metadata", {}).get("source_id", "")
        source_name = art.get("source_name", "未知来源")

        # 从 source_map 获取分类信息
        sm = source_map.get(source_id, {})
        category_name = sm.get("category_name", "")
        category_id = sm.get("category_id", "")

        source_counts[source_name] += 1
        if category_name:
            category_counts[category_name] += 1

        # 轻量索引条目（网站前端用）
        entry = {
            "title": art.get("title", ""),
            "summary": (art.get("content", "") or "")[:200],
            "source": source_name,
            "source_id": source_id,
            "category": category_name,
            "category_id": category_id,
            "url": art.get("url", ""),
            "fetched_at": art.get("metadata", {}).get("fetched_at", ""),
            "dna": art.get("metadata", {}).get("dna", ""),
            "quality": round(q.get("score", 0), 2),
        }
        kb_index["articles"].append(entry)

    # 分类统计
    kb_index["categories"] = {
        cat: {"count": cnt, "label": cat}
        for cat, cnt in category_counts.most_common()
    }
    kb_index["source_stats"] = {
        src: cnt for src, cnt in source_counts.most_common(50)
    }

    # 写入索引文件
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    index_file = INDEX_DIR / "kb_index.json"
    with open(index_file, 'w') as f:
        json.dump(kb_index, f, ensure_ascii=False, indent=2)

    log(f"索引已生成: {index_file}", "OK")
    log(f"  总条目: {len(kb_index['articles'])}")
    log(f"  分类数: {len(kb_index['categories'])}")
    log(f"  来源数: {len(kb_index['source_stats'])}")

    return True


# ━━━━━━━━━━ Step 4: 准备训练数据 ━━━━━━━━━━

def prepare_training():
    """桥接清洗数据到训练格式"""
    log("🏋️ 准备训练数据")

    return run_step(
        [sys.executable, str(BRIDGE_SCRIPT)],
        "训练数据桥接 (干跑·不触发训练)"
    )


# ━━━━━━━━━━ Step 5: 执行训练 ━━━━━━━━━━

def run_training():
    """触发全量训练流程"""
    log("🔥 启动模型训练")

    # 先桥接
    ok = run_step(
        [sys.executable, str(BRIDGE_SCRIPT), "--train"],
        "训练数据桥接 + 触发训练",
        timeout=3600
    )
    if not ok:
        log("训练数据准备失败，终止训练", "ERROR")
        return False

    log("训练已触发，查看训练输出确认进度", "OK")
    log("  训练完成后: python3 bin/lh_data_to_train_bridge.py --full-pipeline", "INFO")
    return True


# ━━━━━━━━━━ Status: 知识库状态 ━━━━━━━━━━

def show_status():
    """展示知识库当前状态"""
    print(f"\n{'='*60}")
    print(f"  🐉 龍魂知识库状态")
    print(f"  {DNA}")
    print(f"{'='*60}")

    # 拉取统计
    fetched_count = 0
    fetched_dir = SOURCES_DIR / "fetched"
    if fetched_dir.exists():
        fetched_files = list(fetched_dir.glob("*.jsonl"))
        for ff in fetched_files:
            with open(ff) as f:
                fetched_count += sum(1 for _ in f)
        print(f"\n📥 原始拉取: {fetched_count} 条 ({len(fetched_files)} 文件)")
    else:
        print(f"\n📥 原始拉取: 无数据")

    # 清洗统计
    cleaned_count = 0
    cleaned_dir = SOURCES_DIR / "cleaned"
    if cleaned_dir.exists():
        cleaned_files = list(cleaned_dir.glob("*_cleaned.jsonl"))
        for cf in cleaned_files:
            with open(cf) as f:
                cleaned_count += sum(1 for _ in f)
        print(f"🧹 已清洗:   {cleaned_count} 条 ({len(cleaned_files)} 文件)")
    else:
        print(f"🧹 已清洗:   无数据")

    # 索引统计
    index_file = INDEX_DIR / "kb_index.json"
    if index_file.exists():
        with open(index_file) as f:
            idx = json.load(f)
        print(f"📇 网站索引: {idx.get('total_articles', 0)} 条")
        print(f"   生成时间: {idx.get('generated_at', '未知')}")
        cats = idx.get("categories", {})
        if cats:
            cats_str = ', '.join(f'{k}({v.get("count",0)})' for k, v in sorted(cats.items()))
            print(f"   分类分布: {cats_str}")
        else:
            print(f"   分类分布: 按来源统计 (无分类标签)")
    else:
        print(f"📇 网站索引: 未生成")

    # 训练数据统计
    train_count = 0
    train_file = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output" / "data" / "train.jsonl"
    if train_file.exists():
        with open(train_file) as f:
            train_count = sum(1 for _ in f)
        print(f"🏋️ 训练数据: {train_count} 条")
    else:
        print(f"🏋️ 训练数据: 未准备")

    # 爬虫记录
    crawler_log = PROJECT_ROOT / "data" / "sources" / "crawler_state.json"
    if crawler_log.exists():
        with open(crawler_log) as f:
            cs = json.load(f)
        print(f"\n🕷️ 爬虫状态:")
        print(f"   上次运行: {cs.get('last_crawl', '未知')}")
        print(f"   总爬取次数: {cs.get('total_crawls', 0)}")
        source_count = len(cs.get("sources", {}))
        print(f"   已配置源: {source_count}")

    print(f"\n📊 操作建议:")
    if cleaned_count == 0:
        print(f"   → 还没有数据，运行: python3 bin/lh_kb_expand.py crawl")
    elif not index_file.exists():
        print(f"   → 索引未生成，运行: python3 bin/lh_kb_expand.py index")
    elif not train_file.exists():
        print(f"   → 训练数据未准备，运行: python3 bin/lh_kb_expand.py train-prep")
    else:
        diff = cleaned_count - train_count
        if diff > 0:
            print(f"   → 有 {diff} 条新数据未入训练集，运行: python3 bin/lh_kb_expand.py train-prep")
        else:
            print(f"   → 数据已同步，可以运行训练: python3 bin/lh_kb_expand.py train")

    print(f"{'='*60}\n")


# ━━━━━━━━━━ Main ━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(
        description="龍魂知识库扩展自动化引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s crawl              爬取P0+P1优先级知识源
  %(prog)s crawl -p P0        只爬取P0优先级
  %(prog)s index              生成网站知识索引
  %(prog)s train-prep         准备训练数据(不训练)
  %(prog)s train              全量训练流程
  %(prog)s all                一键全流程: 爬取→清洗→索引→训练
  %(prog)s status             查看知识库状态
        """
    )

    sub = parser.add_subparsers(dest="command", help="操作命令")

    # crawl
    p_crawl = sub.add_parser("crawl", help="爬取知识源")
    p_crawl.add_argument("-p", "--priority", default="P0,P1",
                         help="优先级 (默认: P0,P1)")
    p_crawl.add_argument("-l", "--limit", type=int, default=50,
                         help="每源最多篇数 (默认: 50)")

    # index
    p_index = sub.add_parser("index", help="生成网站知识索引")

    # train-prep
    p_tp = sub.add_parser("train-prep", help="准备训练数据")

    # train
    p_train = sub.add_parser("train", help="执行模型训练")

    # all
    p_all = sub.add_parser("all", help="一键全流程")
    p_all.add_argument("-p", "--priority", default="P0,P1",
                       help="优先级 (默认: P0,P1)")
    p_all.add_argument("-l", "--limit", type=int, default=50,
                       help="每源最多篇数 (默认: 50)")
    p_all.add_argument("--skip-train", action="store_true",
                       help="跳过训练，只到索引")

    # status
    p_status = sub.add_parser("status", help="查看知识库状态")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    print(f"\n🐉 龍魂知识库扩展引擎 v1.0")
    print(f"🐉 {DNA}")
    print(f"🐉 {CONFIRM}\n")

    if args.command == "status":
        show_status()

    elif args.command == "crawl":
        crawl_sources(args.priority, args.limit)
        show_status()

    elif args.command == "index":
        generate_index()

    elif args.command == "train-prep":
        prepare_training()

    elif args.command == "train":
        run_training()

    elif args.command == "all":
        log("🚀 一键全流程启动")

        # Step 1: 爬取
        if not crawl_sources(args.priority, args.limit):
            log("爬取阶段有问题，但继续后续步骤", "WARN")

        # Step 2: 清洗
        if not clean_data():
            log("清洗阶段有问题，但继续后续步骤", "WARN")

        # Step 3: 索引
        generate_index()

        # Step 4: 训练数据准备
        prepare_training()

        # Step 5: 训练 (可选跳过)
        if args.skip_train:
            log("跳过训练 (--skip-train)", "INFO")
        else:
            run_training()

        show_status()


if __name__ == "__main__":
    main()
