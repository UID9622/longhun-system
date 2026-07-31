# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂本地训练引擎 · 训练主程序
DNA: #龍芯⚡️2026-06-28-LONGHUN-TRAINER-v1.1
"""
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

# 把 src 加入路径
sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import Config
from tokenizer import CharTokenizer
from dataset import LonghunDataset
from model import LonghunLM
from collect_corpus import CorpusCollector


def choose_device():
    """自动选设备：cuda > mps > cpu"""
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def build_dna():
    seed = f"{datetime.now().isoformat()}-LONGHUN-TRAIN-{torch.__version__}"
    h = hashlib.sha256(seed.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-TRAIN-{h}"


def collate_fn(batch):
    """把 list of (x,y) 堆成 tensor。"""
    xs, ys = zip(*batch)
    return torch.tensor(xs, dtype=torch.long), torch.tensor(ys, dtype=torch.long)


def main():
    cfg = Config()
    cfg.device = choose_device()

    dna = build_dna()
    print("=" * 60)
    print("🐉 龍魂本地训练引擎启动")
    print(f"   DNA: {dna}")
    print(f"   模型: {cfg.model_name}")
    print(f"   设备: {cfg.device}")
    print("=" * 60)

    # 1. 自动收集语料
    data_dirs = [cfg.data_dir]
    if cfg.auto_corpus_enabled:
        collector = CorpusCollector(
            sources=cfg.auto_corpus_sources,
            output_dir=cfg.auto_corpus_dir,
            exclude_patterns=cfg.auto_corpus_exclude,
            max_files=cfg.auto_corpus_max_files,
            max_total_mb=cfg.auto_corpus_max_total_mb,
        )
        collected = collector.collect()
        report = collector.report()
        print(f"   自动收集语料: {len(collected)} 个文件 / {report['total_bytes'] / 1e6:.1f} MB -> {cfg.auto_corpus_dir}")
        data_dirs.append(cfg.auto_corpus_dir)

    # 2. 读取全部语料训练分词器
    all_files = []
    for d in data_dirs:
        d = Path(d)
        if d.exists():
            all_files.extend(d.rglob("*.txt"))
            all_files.extend(d.rglob("*.md"))

    if not all_files:
        print("🔴 未找到任何 .txt 或 .md 语料。请先放语料到 data/raw/，或开启 auto_corpus_enabled。")
        sys.exit(1)

    print(f"   发现语料文件: {len(all_files)} 个")
    texts = []
    for f in all_files:
        try:
            texts.append(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"⚠️ 跳过 {f}: {e}")

    tokenizer = CharTokenizer(vocab_size=cfg.vocab_size)
    tokenizer.fit(texts)
    tokenizer.save(cfg.tokenizer_path)
    print(f"   词表大小: {len(tokenizer)} / {cfg.vocab_size}")

    # 3. 数据集 / 数据加载器
    dataset = LonghunDataset(
        data_dirs,
        tokenizer,
        max_seq_len=cfg.max_seq_len,
        max_samples=cfg.dataset_max_samples,
    )
    if len(dataset) == 0:
        print("🔴 数据集为空，无法训练。")
        sys.exit(1)

    dataloader = DataLoader(
        dataset,
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=cfg.num_workers,
        collate_fn=collate_fn,
    )
    print(f"   训练样本数: {len(dataset)}")

    # 4. 模型
    cfg.vocab_size = len(tokenizer)
    model = LonghunLM(cfg).to(cfg.device)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"   模型参数量: {total_params:,} ({total_params / 1e6:.2f} M)")

    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.learning_rate)

    # 5. 训练循环
    model.train()
    global_step = 0
    history = []

    for epoch in range(1, cfg.epochs + 1):
        epoch_loss = 0.0
        pbar = tqdm(dataloader, desc=f"Epoch {epoch}/{cfg.epochs}")

        for x, y in pbar:
            x, y = x.to(cfg.device), y.to(cfg.device)

            optimizer.zero_grad()
            logits, loss = model(x, y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.gradient_clip)
            optimizer.step()

            epoch_loss += loss.item()
            global_step += 1
            pbar.set_postfix({"loss": f"{loss.item():.4f}"})

        avg_loss = epoch_loss / len(dataloader)
        history.append({"epoch": epoch, "loss": avg_loss})
        print(f"   Epoch {epoch}/{cfg.epochs} 平均 Loss: {avg_loss:.4f}")

    # 6. 保存模型
    cfg.model_dir.mkdir(parents=True, exist_ok=True)
    model_path = cfg.model_dir / f"{cfg.model_name}.pt"
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "config": {k: v for k, v in vars(cfg).items() if not k.startswith("_")},
            "tokenizer_path": str(cfg.tokenizer_path),
            "dna": dna,
            "history": history,
        },
        model_path,
    )

    # 7. 保存训练报告
    report_path = cfg.output_dir / f"{cfg.model_name}_train_report.json"
    report_path.write_text(
        json.dumps(
            {
                "dna": dna,
                "model_name": cfg.model_name,
                "model_path": str(model_path),
                "tokenizer_path": str(cfg.tokenizer_path),
                "device": cfg.device,
                "total_params": total_params,
                "vocab_size": len(tokenizer),
                "train_samples": len(dataset),
                "epochs": cfg.epochs,
                "history": history,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("=" * 60)
    print("✅ 训练完成")
    print(f"   模型权重: {model_path}")
    print(f"   词表文件: {cfg.tokenizer_path}")
    print(f"   训练报告: {report_path}")
    print(f"   DNA: {dna}")
    print("=" * 60)


if __name__ == "__main__":
    main()
