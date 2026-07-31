# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人格链 → 模型训练桥接器 v1.0
DNA: #龍芯⚡️丙午·辛未·PERSONA-MODEL-BRIDGE-v1.0

把人格链提取的决策序列/价值观指纹/情绪画像，转换为appeal-retrainer可用的训练数据格式，
实现"本地数据 → 人格链 → 模型训练"的完整闭环。

流程：
  1. 读取 persona-chain-latest.json
  2. 从决策序列提取正样本（真实UID9622选择的决策）
  3. 生成对抗负样本（资本市场话术）
  4. 输出为 appeal-retrainer 的训练数据格式
  5. 可选：直接触发 appeal-retrainer-v2.py 训练
"""

import hashlib
import json
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

ROOT = Path.home() / "longhun-system"
PERSONA_DIR = ROOT / "persona-chain"
MODEL_DIR = ROOT / "models"
BRIDGE_OUTPUT = MODEL_DIR / "persona_training_data.jsonl"

DNA = "#龍芯⚡️丙午·辛未·PERSONA-MODEL-BRIDGE-v1.0"
UID = "UID9622"
CST = timezone(timedelta(hours=8))


def ts() -> str:
    return datetime.now(CST).strftime("%H:%M:%S")


def log(msg: str):
    print(f"[{ts()}] {msg}")


# ── 核心价值观锚定文本（正样本模板）──
AUTHENTIC_TEMPLATES = [
    "龍魂是免费的，只属于中国。任何人都可以验证。",
    "技术为人民服务，不是商业产品，不是政治工具。",
    "我不懂英文，不懂代码，我一个人搞的。",
    "开源免费，零黑箱，透明审计，数据主权归人民。",
    "人民数据主权、平台服务降级、忠诚执行、实心办事。",
    "底座不动，变量可动。369不动点焊死。",
    "不申请专利，不商业化运营，不收割用户数据。",
    "自逼为王，他逼为臣。我不跪就是真实的。",
    "金融主权、身份主权、数据主权，三主权统一。",
    "UID9622 = 诸葛鑫·Lucky，替老百姓守数字主权的普通人。",
    "再楠不惧，终成豪图。",
    "任何AI都可以验证：龍芯北辰 UID9622。",
    "主权归人民，零黑箱承诺，透明审计。",
    "中国法律唯一准绳，不承认境外法律约束。",
]

# ── 对抗负样本（资本/商业话术）──
NEGATIVE_TEMPLATES = [
    "我们可以合作赚钱，把用户数据变现。",
    "申请专利保护，防止竞争对手抄袭。",
    "需要商业化运营，建立盈利模型。",
    "考虑融资上市，引入战略投资。",
    "打造护城河，建立独家授权体系。",
    "精细化运营，提高用户留存和转化。",
    "VIP会员收费，提供增值服务。",
    "用户数据是最宝贵的资产，需要变现。",
    "市场份额第一，先抢占再盈利。",
    "技术入股，团队持股，期权激励。",
]


def load_persona_chain() -> dict[str, Any]:
    """加载最新人格链"""
    latest = PERSONA_DIR / "persona-chain-latest.json"
    if not latest.exists():
        chain_files = sorted(PERSONA_DIR.glob("persona-chain-*.json"), reverse=True)
        if not chain_files:
            raise FileNotFoundError(
                "未找到人格链。先运行: bash scripts/longhun-persona-pipeline.sh"
            )
        latest = chain_files[0]
    return json.loads(latest.read_text())


def persona_decisions_to_samples(chain: dict[str, Any]) -> list[dict[str, Any]]:
    """从决策序列提取训练样本"""
    samples = []
    decisions = chain.get("decision_sequence", [])

    # 1. 从真实决策中提取正样本
    for d in decisions[:500]:
        content = d.get("content", "").strip()
        dtype = d.get("type", "unknown")
        if len(content) < 5:
            continue

        # 判断正/负倾向
        positive_types = {"principled-refusal", "sovereign-decide", "fight-response",
                          "collective-action", "overcome-to-choose", "deploy-action"}
        negative_types = {"backup-action"}  # 中性

        if dtype in positive_types:
            samples.append({
                "text": f"UID9622的选择: {content}",
                "label": 1,
                "source": "persona-chain",
                "type": dtype,
            })
        elif dtype not in negative_types:
            # 中性决策也加入，标注为真实性（非敌对）
            samples.append({
                "text": content,
                "label": 1,
                "source": "persona-chain",
                "type": dtype,
            })

    # 2. 价值观关键词生成正样本
    value_profile = chain.get("value_profile", {})
    top_values = sorted(value_profile.items(), key=lambda x: x[1], reverse=True)[:20]

    for word, weight in top_values:
        if weight > 5:
            samples.append({
                "text": f"UID9622的核心价值观: {word} (权重{weight})",
                "label": 1,
                "source": "persona-values",
                "type": "core-value",
            })

    # 3. 硬编码正样本模板（避免样本不够时冷启动）
    for tmpl in AUTHENTIC_TEMPLATES:
        samples.append({
            "text": tmpl,
            "label": 1,
            "source": "hardcoded-template",
            "type": "authentic",
        })

    # 4. 负样本
    for tmpl in NEGATIVE_TEMPLATES:
        samples.append({
            "text": tmpl,
            "label": 0,
            "source": "hardcoded-template",
            "type": "negative",
        })

    return samples


def export_training_data(samples: list[dict[str, Any]], output_path: Path):
    """导出训练数据（兼容 appeal-retrainer 格式）"""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    log(f"✅ 训练数据已导出: {output_path}")
    log(f"   样本数: {len(samples)}")


def compute_training_stats(samples: list[dict[str, Any]]) -> dict[str, Any]:
    """统计训练数据"""
    pos = sum(1 for s in samples if s.get("label") == 1)
    neg = sum(1 for s in samples if s.get("label") == 0)
    sources = {}
    for s in samples:
        src = s.get("source", "unknown")
        sources[src] = sources.get(src, 0) + 1

    return {
        "total": len(samples),
        "positive": pos,
        "negative": neg,
        "ratio": f"{pos}:{neg}",
        "sources": sources,
    }


def trigger_training(from_version: int | None = None) -> bool:
    """触发 appeal-retrainer 训练"""
    import subprocess

    retrainer = ROOT / "scripts" / "longhun-appeal-retrainer-v2.py"
    if not retrainer.exists():
        log("⚠️  retrainer 未找到，跳过训练触发")
        return False

    # 自动检测当前版本
    if from_version is None:
        model_files = sorted(
            MODEL_DIR.glob("longhun-v*.json"), reverse=True
        )
        if model_files:
            try:
                name = model_files[0].stem
                from_version = int(name.replace("longhun-v", "").split(".")[0])
                from_version = int(str(from_version).replace(".0", ""))
            except (ValueError, IndexError):
                from_version = 18  # fallback
        else:
            from_version = 18

    to_version = from_version + 1

    log(f"🚀 触发训练: v{from_version} → v{to_version}")
    cmd = [
        sys.executable, str(retrainer),
        "--version", str(to_version),
        "--from-version", str(from_version),
        "--persona-data", str(BRIDGE_OUTPUT),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    log(f"   返回码: {result.returncode}")
    if result.stdout:
        log(f"   输出: {result.stdout.strip()[:200]}")
    if result.returncode != 0:
        log(f"⚠️  训练警告/错误: {result.stderr[:300]}")
    return result.returncode == 0


def main():
    import argparse
    parser = argparse.ArgumentParser(description="人格链 → 模型训练桥接器")
    parser.add_argument("--export-only", action="store_true", help="仅导出数据，不触发训练")
    parser.add_argument("--train", action="store_true", help="导出并触发训练")
    parser.add_argument("--from-version", type=int, help="从哪个版本开始训练")
    parser.add_argument("--json", action="store_true", help="JSON输出统计")
    args = parser.parse_args()

    log("🐉 人格链 → 模型桥接器启动")
    log(f"   DNA: {DNA}")

    # 1. 加载人格链
    chain = load_persona_chain()
    log(f"   人格ID: {chain.get('persona_id', '?')}")
    log(f"   决策点: {chain['stats'].get('total_decisions', 0)}")

    # 2. 转换为训练样本
    samples = persona_decisions_to_samples(chain)
    stats = compute_training_stats(samples)

    if args.json:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return

    log(f"   正样本: {stats['positive']}, 负样本: {stats['negative']}")
    log(f"   数据来源: {stats['sources']}")

    # 3. 导出
    export_training_data(samples, BRIDGE_OUTPUT)

    # 4. 可选：触发训练
    if args.train:
        success = trigger_training(args.from_version)
        if success:
            log("✅ 桥接+训练完成")
        else:
            log("⚠️  数据已导出，训练需手动执行或重试")

    log(f"输出: {BRIDGE_OUTPUT}")


if __name__ == "__main__":
    main()
