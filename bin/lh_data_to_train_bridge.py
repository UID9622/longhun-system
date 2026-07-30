#!/usr/bin/env python3
#龍芯⚡️丙午·辛未·乙酉·卯时·讼-DATA-BRIDGE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""🐉 龍魂引擎：lh_data_to_train_bridge
路径：bin/lh_data_to_train_bridge.py
TODO：请补充详细功能说明（不少于20字）。"""
from __future__ import annotations
"""
龍魂·训练数据桥接引擎 v1.0 (融合版)
DNA: #龍芯⚡️丙午·辛未·乙酉·卯时·讼-DATA-BRIDGE-v1.0

功能:
  1. 从 data/sources/cleaned/ 读取清洗后数据
  2. 转换为 LoRA 训练格式 (Qwen2.5 Chat Template)
  3. 合并到 models/longhun-v1.0/lora_output/data/train.jsonl (去重)
  4. 可选：自动触发 LoRA 训练
  5. 可选：自动 Fuse → Export → Ollama Deploy

全链路命令:
  python3 bin/lh_data_to_train_bridge.py                    # 仅生成训练数据
  python3 bin/lh_data_to_train_bridge.py --train            # 生成 + 触发训练
  python3 bin/lh_data_to_train_bridge.py --full-pipeline     # 全链路: 数据→训练→部署
  python3 bin/lh_data_to_train_bridge.py --stats             # 查看训练数据统计
  python3 bin/lh_data_to_train_bridge.py --dry-run           # 预览而不写入

依赖:
  - data/sources/ 爬取→清洗数据
  - hl_lora_trainer.py 训练接口
"""

import json
import os
import sys
import hashlib
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8))

# === 路径 ===
PROJECT_ROOT = Path(__file__).parent.parent
SOURCES_DIR = PROJECT_ROOT / "data" / "sources"
CLEANED_DIR = SOURCES_DIR / "cleaned"
TRAIN_DATA_DIR = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output" / "data"
TRAIN_SCRIPT = PROJECT_ROOT / "bin" / "lh_lora_trainer.py"

DNA_ANCHOR = "#龍芯⚡️丙午·辛未·乙酉·卯时·讼-DATA-BRIDGE-v1.0"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 龙魂系统 System Prompt (与训练一致)
SYSTEM_PROMPT = (
    "你是龍魂AI，龙魂系统基于Qwen2.5-1.5B-Instruct用龍魂自有语料和公开中国网站数据LoRA微调。"
    "DNA: #龍芯⚡️ 中国法律唯一准绳。UID9622=诸葛鑫·龍芯北辰·唯一创始人。"
)


class DataBridge:
    """训练数据桥接引擎"""

    def __init__(self):
        self.stats = {"converted": 0, "merged": 0, "skipped_dup": 0, "skipped_quality": 0}

    def log(self, msg: str, level: str = "INFO"):
        ts = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] [{level}] {msg}")

    def _content_hash(self, content: str) -> str:
        """内容哈希（用于去重）"""
        return hashlib.md5(content.encode()).hexdigest()[:16]

    def load_cleaned_data(self) -> list[Any]:
        """从 data/sources/cleaned/ 加载清洗后数据"""
        if not CLEANED_DIR.exists():
            self.log("清洗目录不存在: data/sources/cleaned/", "WARN")
            self.log("请先运行: cd data/sources && python3 lh_source_manager.py --pipeline P0", "INFO")
            return []

        cleaned_files = sorted(CLEANED_DIR.glob("*_cleaned.jsonl"))
        if not cleaned_files:
            self.log("没有清洗后的数据", "WARN")
            return []

        self.log(f"加载清洗数据: {len(cleaned_files)} 个文件")
        articles = []
        for cf in cleaned_files:
            with open(cf) as f:
                for line in f:
                    try:
                        article = json.loads(line.strip())
                    except json.JSONDecodeError:
                        continue
                    # 质量检查
                    q = article.get("quality", {})
                    if q.get("score", 0) < 0.5:
                        self.stats["skipped_quality"] += 1
                        continue
                    articles.append(article)

        self.log(f"  → {len(articles)} 条 (过滤低质量 {self.stats['skipped_quality']} 条)")
        return articles

    def article_to_train_sample(self, article: dict[str, Any]) -> dict[str, Any]:
        """将清洗后的文章转换为训练样本（Qwen2.5 Chat格式）"""
        title = article.get("title", "")
        content = article.get("content", "")
        source_name = article.get("source_name", article.get("metadata", {}).get("source_id", "未知来源"))

        if not content or len(content) < 30:
            return None

        # 生成Q&A对
        q1 = f"关于{source_name}的内容：请介绍「{title}」"
        a1 = f"来自{source_name}的内容：{title}。\n{content[:800]}"

        sample = {
            "messages": [
                {"role": "user", "content": f"{SYSTEM_PROMPT}\n\n用户问题：{q1}"},
                {"role": "assistant", "content": a1}
            ],
            "metadata": {
                "source": article.get("metadata", {}).get("source_id", ""),
                "title": title,
                "bridged_at": datetime.now(CST).isoformat(),
                "dna": article.get("metadata", {}).get("cleaned_dna", DNA_ANCHOR),
            }
        }

        self.stats["converted"] += 1
        return sample

    def merge_into_train_jsonl(self, new_samples: list[Any], dry_run: bool = False):
        """合并新样本到 train.jsonl（去重）"""
        train_file = TRAIN_DATA_DIR / "train.jsonl"

        # 加载已有训练数据
        existing = []
        existing_hashes = set()
        if train_file.exists():
            with open(train_file) as f:
                for line in f:
                    try:
                        item = json.loads(line.strip())
                        existing.append(item)
                        for m in item.get("messages", []):
                            existing_hashes.add(self._content_hash(m.get("content", "")))
                    except json.JSONDecodeError:
                        continue

        self.log(f"现有训练数据: {len(existing)} 条")

        # 去重合并
        merged = list(existing)
        for sample in new_samples:
            if sample is None:
                continue
            for m in sample.get("messages", []):
                h = self._content_hash(m.get("content", ""))
                if h in existing_hashes:
                    self.stats["skipped_dup"] += 1
                    break
            else:
                merged.append(sample)
                self.stats["merged"] += 1
                # 注册哈希
                for m in sample.get("messages", []):
                    existing_hashes.add(self._content_hash(m.get("content", "")))

        if dry_run:
            self.log(f"🔍 预览(不写入): 新增 {self.stats['merged']} 条, "
                    f"跳过重复 {self.stats['skipped_dup']} 条")
            return merged, 0, 0

        # 分割训练/验证集 (90/10)
        split = int(len(merged) * 0.9)
        train_final = merged[:split]
        valid_final = merged[split:]

        # 写入
        TRAIN_DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(train_file, 'w') as f:
            for sample in train_final:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')

        valid_file = TRAIN_DATA_DIR / "valid.jsonl"
        with open(valid_file, 'w') as f:
            for sample in valid_final:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')

        self.log(f"✅ 数据已同步:")
        self.log(f"    训练集: {len(train_final)} 条 (+{self.stats['merged']} 新)")
        self.log(f"    验证集: {len(valid_final)} 条")
        self.log(f"    跳过重复: {self.stats['skipped_dup']}")

        return merged, len(train_final), len(valid_final)

    def trigger_training(self) -> bool:
        """触发 LoRA 训练"""
        if not TRAIN_SCRIPT.exists():
            self.log(f"训练脚本不存在: {TRAIN_SCRIPT}", "ERROR")
            return False

        self.log("🏋️ 启动 LoRA 训练...")
        self.log(f"   脚本: {TRAIN_SCRIPT}")
        result = subprocess.run(
            [sys.executable, str(TRAIN_SCRIPT), "train"],
            cwd=str(PROJECT_ROOT),
            capture_output=False  # 实时输出
        )
        return result.returncode == 0

    def full_pipeline(self) -> bool:
        """全链路: 数据→训练→部署 (fuse + export + ollama create)"""
        self.log("🚀 全链路 Pipeline 启动")
        self.log(f"   {DNA_ANCHOR}")

        # Step 1: 生成训练数据
        articles = self.load_cleaned_data()
        if not articles:
            self.log("没有清洗数据，跳过", "WARN")
            return False

        new_samples = []
        for article in articles:
            sample = self.article_to_train_sample(article)
            if sample:
                new_samples.append(sample)

        self.log(f"转换完成: {len(new_samples)} 个训练样本")

        merged, train_count, valid_count = self.merge_into_train_jsonl(new_samples, dry_run=False)

        if self.stats["merged"] == 0:
            self.log("没有新数据可训练", "INFO")
            return False

        # Step 2: 训练
        if not self.trigger_training():
            self.log("训练可能失败，检查日志", "WARN")

        # Step 3: Fuse
        self.log("🔧 Step 3: Fuse LoRA adapter...")
        subprocess.run([sys.executable, str(TRAIN_SCRIPT), "fuse"], cwd=str(PROJECT_ROOT))

        # Step 4: Export GGUF
        self.log("📦 Step 4: Export GGUF...")
        subprocess.run([sys.executable, str(TRAIN_SCRIPT), "export"], cwd=str(PROJECT_ROOT))

        self.log("✅ 全链路完成")
        self.log("   下一步: ollama create <新版本> -f Modelfile")
        return True

    def show_stats(self):
        """显示训练数据统计"""
        train_file = TRAIN_DATA_DIR / "train.jsonl"
        valid_file = TRAIN_DATA_DIR / "valid.jsonl"

        print(f"\n🐉 龍魂训练数据统计")
        print(f"{'='*60}")
        print(f"{DNA_ANCHOR}")

        if train_file.exists():
            with open(train_file) as f:
                train_count = sum(1 for _ in f)
            print(f"训练集 (train.jsonl): {train_count} 条")

        if valid_file.exists():
            with open(valid_file) as f:
                valid_count = sum(1 for _ in f)
            print(f"验证集 (valid.jsonl): {valid_count} 条")

        # 数据来源分布
        if train_file.exists():
            sources = {}
            with open(train_file) as f:
                for line in f:
                    try:
                        item = json.loads(line.strip())
                        source = item.get("metadata", {}).get("source", "未知")
                        sources[source] = sources.get(source, 0) + 1
                    except json.JSONDecodeError:
                        pass
            if sources:
                print(f"\n数据来源分布:")
                for src, count in sorted(sources.items(), key=lambda x: -x[1])[:10]:
                    print(f"  {src}: {count} 条")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="龍魂训练数据桥接引擎 v1.0")
    parser.add_argument('--train', action='store_true', help='生成训练数据 + 触发 LoRA 训练')
    parser.add_argument('--full-pipeline', action='store_true', help='全链路: 数据→训练→部署')
    parser.add_argument('--dry-run', action='store_true', help='预览不写入')
    parser.add_argument('--stats', action='store_true', help='查看训练数据统计')

    args = parser.parse_args()
    bridge = DataBridge()

    print(f"\n🐉 龍魂训练数据桥接引擎 v1.0")
    print(f"🐉 {DNA_ANCHOR}")

    if args.stats:
        bridge.show_stats()
        return

    # 加载数据
    articles = bridge.load_cleaned_data()
    if not articles:
        bridge.log("没有可用的清洗数据", "WARN")
        print("请先运行: cd data/sources && python3 lh_source_manager.py --pipeline P0")
        return

    # 转换
    new_samples = []
    for article in articles:
        sample = bridge.article_to_train_sample(article)
        if sample:
            new_samples.append(sample)

    bridge.log(f"转换: {bridge.stats['converted']} 个训练样本")

    # 合并
    bridge.merge_into_train_jsonl(new_samples, dry_run=args.dry_run)

    if args.dry_run:
        return

    # 训练
    if args.train and bridge.stats["merged"] > 0:
        bridge.trigger_training()
    elif args.train:
        bridge.log("没有新数据，跳过训练", "INFO")

    # 全链路
    if args.full_pipeline:
        bridge.full_pipeline()


if __name__ == "__main__":
    main()
