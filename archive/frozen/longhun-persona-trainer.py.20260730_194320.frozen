#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人格链训练器 v1.0
DNA: #龍芯⚡️丙午·辛未·PERSONA-TRAINER-v1.0

从本地数据提取决策序列 → 价值观指纹 → 情绪画像 → 人格链JSON
"""
import hashlib
import json
import os
import re
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Any

ROOT = Path.home() / "longhun-system"
MINER_DIR = ROOT / ".data-miner"
PERSONA_DIR = ROOT / "persona-chain"
PERSONA_DIR.mkdir(parents=True, exist_ok=True)

DNA = "#龍芯⚡️丙午·辛未·PERSONA-TRAINER-v1.0"
UID = "UID9622"
CST = timezone(timedelta(hours=8))


def ts() -> str:
    return datetime.now(CST).strftime("%H:%M:%S")


def log(msg: str):
    print(f"[{ts()}] {msg}")


class PersonaChainTrainer:
    """人格链训练器 — 从原始数据提取决策序列"""

    def __init__(self):
        self.decisions: list[Any] = []
        self.choices: Counter = Counter()
        self.values: Counter = Counter()
        self.emotions: Counter = Counter()
        self.sources: Counter = Counter()
        self.temporal_decisions: list[Any] = []  # 带时间戳的决策

        # ── 决策模式正则（中文自然语言） ──
        self.choice_patterns = [
            (r'(?:选|做|用|搞|干|走|上)\s*\S{0,6}\s*(?:还是|或者|要么)\s*\S{0,6}\s*(?:选|做|用|搞|干)', "A-or-B"),
            (r'(?:不|没|别)\s*\S{0,6}\s*(?:但|但是|然而|可是)\s*\S{0,6}\s*(?:要|还是|最终|决定)', "reject-then-choose"),
            (r'(?:拒绝|反对|不要|不行)\s*\S{0,10}\s*(?:因为|为了|底线)\s*\S{0,10}\s*(?:坚持|选择|守住)', "principled-refusal"),
            (r'(?:虽然|尽管)\s*\S{0,15}\s*(?:但是|但)\s*\S{0,10}\s*(?:我选|我要|我干|我搞|走)', "overcome-to-choose"),
            (r'(?:硬刚|不服|干他|弄他|跟他拼)', "fight-response"),
            (r'(?:我说了算|老子|朕)\s*\S{0,10}\s*(?:决定|定|拍板)', "sovereign-decide"),
            (r'(?:兄弟们|大家|咱们|一起)\s*\S{0,10}\s*(?:上|干|冲)', "collective-action"),
            # frp/部署相关决策
            (r'(?:部署|同步|推到?|拉到?|转到?)\s*\S{0,6}\s*(?:鲲鹏|华为云|服务器|VPS)', "deploy-action"),
            (r'(?:保存|备份|兜底|冷备)\s*\S{0,10}', "backup-action"),
        ]

        # ── 价值观关键词（优先级加权）───
        self.value_words = {
            # 主权类 (weight 3)
            "主权": 3, "人民": 3, "数据主权": 3, "自主": 3, "国产": 3, "自研": 3,
            # 军人/硬气类 (weight 2)
            "军人": 2, "当兵": 2, "退伍": 2, "硬刚": 2, "不跪": 2, "不妥协": 2,
            "老子": 2, "他妈的": 2, "咬牙": 2, "撑住": 2,
            # 开源/透明类 (weight 2)
            "开源": 2, "免费": 2, "透明": 2, "审计": 2, "零黑箱": 2,
            # 责任类 (weight 1)
            "责任": 1, "担当": 1, "老百姓": 1, "后人": 1, "下一代": 1,
            "女儿": 1, "家人": 1, "底线": 1, "原则": 1,
            # 技术类 (weight 1)
            "CNSH": 1, "龍魂": 1, "Python": 1, "FastAPI": 1, "Ollama": 1,
            "MLX": 1, "docker": 1, "frp": 1, "CodeBuddy": 1,
            # 金融类 (weight 1)
            "金融": 1, "货币": 1, "资产": 1, "数字人民币": 1,
        }

        # ── 情绪标记 ──
        self.emotion_markers = {
            "愤怒": [
                r'操\b', r'他妈\b', r'狗日', r'傻逼', r'草\b', r'妈的',
                r'滚\b', r'妈的逼', r'操蛋', r'完蛋',
            ],
            "坚定": [
                r'必须', r'一定', r'绝对', r'绝不', r'永远', r'打死',
                r'焊死', r'不动', r'死守', r'底线',
            ],
            "自豪": [
                r'牛逼', r'厉害', r'老子', r'服不服', r'强的', r'极致',
                r'无敌', r'完美', r'天下第一',
            ],
            "关怀": [
                r'人民', r'老百姓', r'大家', r'后人', r'娃', r'女儿',
                r'孩子', r'下一代', r'穷人', r'弱者',
            ],
            "务实": [
                r'干就完了', r'直接', r'不废话', r'落地', r'执行',
                r'开搞', r'开始', r'动手',
            ],
            "孤独": [
                r'没人', r'没人理', r'一个人', r'孤独', r'独自',
                r'扛着', r'撑住', r'自己来',
            ],
            "信仰": [
                r'信仰', r'信念', r'中国', r'祖国', r'人民军队',
                r'道德经', r'易经', r'龍魂', r'北辰',
            ],
            "黑色幽默": [
                r'哈哈哈', r'笑死', r'滑稽', r'逗比', r'搁这',
                r'绷不住', r'绷', r'整笑了',
            ],
        }

    # ──────────────── 核心提取 ────────────────

    def extract_from_text(self, text: str, source: str):
        """从文本提取决策点、价值观、情绪"""
        if not text or len(text) < 10:
            return

        # 1. 决策模式提取
        for pattern, dtype in self.choice_patterns:
            for m in re.finditer(pattern, text, re.IGNORECASE):
                decision_text = m.group(0)
                if 3 < len(decision_text) < 200:
                    self.decisions.append({
                        "type": dtype,
                        "content": decision_text,
                        "source": source,
                        "length": len(decision_text),
                    })
                    self.choices[decision_text] += 1
                    self.sources[source] += 1

        # 2. 价值观关键词（加权计数）
        for word, weight in self.value_words.items():
            count = text.count(word)
            if count > 0:
                self.values[word] += count * weight

        # 3. 情绪检测
        for emotion, patterns in self.emotion_markers.items():
            for pat in patterns:
                if re.search(pat, text):
                    self.emotions[emotion] += 1

    def process_file(self, filepath: Path):
        """处理单个文件"""
        try:
            # 跳过二进制和大文件
            if filepath.stat().st_size > 50 * 1024 * 1024:  # >50MB
                return
            text = filepath.read_text(errors="ignore")
            source = filepath.name[:40]
            before = len(self.decisions)
            self.extract_from_text(text, source)
            after = len(self.decisions)
            if after - before > 0:
                log(f"  {source}: +{after - before}决策点")
        except Exception:
            pass  # 静默跳过不可读文件

    def train(self) -> dict[str, Any]:
        """执行训练，返回人格链"""
        log("🐉 龍魂人格链训练启动")
        log(f"   数据目录: {MINER_DIR}")

        if not MINER_DIR.exists():
            log("⚠️ 数据目录不存在，使用龍魂协议层数据")
            # 降级：直接读龍魂系统文件
            alt_dirs = [
                ROOT / "01_protocols",
                ROOT / "02_執行記錄",
                ROOT / "04_決策日誌",
                ROOT / ".codebuddy" / "memory",
            ]
            for d in alt_dirs:
                if d.exists():
                    for f in d.rglob("*"):
                        if f.is_file() and f.suffix in (".md", ".json", ".py", ".txt"):
                            self.process_file(f)

        miner_files = list(MINER_DIR.rglob("*")) if MINER_DIR.exists() else []
        # 过滤非文件
        miner_files = [f for f in miner_files if f.is_file()]
        log(f"   发现 {len(miner_files)} 个数据文件")

        for f in miner_files:
            self.process_file(f)

        # ── 构建人格链 ──
        persona_chain = {
            "dna": DNA,
            "uid": UID,
            "version": "1.0",
            "trained_at": int(time.time()),
            "trained_at_human": datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S CST"),
            "stats": {
                "total_files_scanned": len(miner_files),
                "total_decisions": len(self.decisions),
                "unique_choices": len(self.choices),
                "source_distribution": dict(self.sources.most_common(20)),
            },
            "value_fingerprint": self._compute_value_fingerprint(),
            "emotion_fingerprint": self._compute_emotion_fingerprint(),
            "decision_sequence": self.decisions[-2000:],
            "value_profile": dict(self.values.most_common(50)),
            "emotion_profile": dict(self.emotions.most_common()),
            "choice_patterns": dict(self.choices.most_common(100)),
            "persona_id": self._compute_persona_id(),
        }

        # 保存
        output_file = PERSONA_DIR / f"persona-chain-{int(time.time())}.json"
        output_file.write_text(
            json.dumps(persona_chain, ensure_ascii=False, indent=2)
        )

        # 创建 latest 软链接
        latest_link = PERSONA_DIR / "persona-chain-latest.json"
        if latest_link.exists() or latest_link.is_symlink():
            latest_link.unlink()
        latest_link.symlink_to(output_file.name)

        # 生成摘要
        summary = self._generate_summary(persona_chain)
        summary_file = PERSONA_DIR / "persona-summary.md"
        summary_file.write_text(summary)

        log(f"✅ 人格链: {output_file.name}")
        log(f"✅ 摘要:   persona-summary.md")
        log(f"✅ latest: persona-chain-latest.json")

        return persona_chain

    # ──────────────── 指纹计算 ────────────────

    def _compute_value_fingerprint(self) -> str:
        """价值观指纹: SHA256(values排序)截断16位"""
        raw = json.dumps(dict(self.values.most_common(100)), sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _compute_emotion_fingerprint(self) -> str:
        """情绪指纹: SHA256(emotions排序)截断16位"""
        raw = json.dumps(dict(self.emotions.most_common()), sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _compute_persona_id(self) -> str:
        """完整人格ID: 价值观指纹+情绪指纹+决策哈希"""
        val = self._compute_value_fingerprint()
        emo = self._compute_emotion_fingerprint()
        decisions_raw = json.dumps([d["type"] for d in self.decisions[-500:]])
        dec_hash = hashlib.sha256(decisions_raw.encode()).hexdigest()[:8]
        return f"{val}-{emo}-{dec_hash}"

    # ──────────────── 摘要生成 ────────────────

    def _generate_summary(self, chain: dict[str, Any]) -> str:
        stats = chain["stats"]
        top_values = sorted(
            chain["value_profile"].items(), key=lambda x: x[1], reverse=True
        )[:15]
        top_emotions = sorted(
            chain["emotion_profile"].items(), key=lambda x: x[1], reverse=True
        )
        top_choices = sorted(
            chain["choice_patterns"].items(), key=lambda x: x[1], reverse=True
        )[:5]

        # 情绪占比
        total_emotion = sum(v for _, v in top_emotions) or 1

        def value_bar(count: int, max_v: int) -> str:
            pct = count / max_v if max_v else 0
            bar_len = int(pct * 20)
            return "█" * bar_len + "░" * (20 - bar_len)

        max_val = top_values[0][1] if top_values else 1

        return f"""# 🐉 龍魂人格链摘要

> **DNA**: `{chain['dna']}`
> **训练时间**: {chain['trained_at_human']}
> **数据文件**: {stats['total_files_scanned']} 个
> **决策点**: {stats['total_decisions']} 个
> **人格ID**: `{chain['persona_id']}`

---

## ⚖️ 价值观指纹

| # | 价值观 | 权重 | 强度 |
|---|--------|------|------|
{chr(10).join(f"| {i+1} | **{k}** | {v} | `{value_bar(v, max_val)}` |" for i, (k, v) in enumerate(top_values))}

> 指纹: `{chain['value_fingerprint']}`

---

## 🎭 情绪画像

| 情绪 | 频次 | 占比 |
|------|------|------|
{chr(10).join(f"| **{k}** | {v} | {v/total_emotion*100:.1f}% |" for k, v in top_emotions)}

> 指纹: `{chain['emotion_fingerprint']}`

---

## 🧠 决策模式

| 场景 | 次数 |
|------|------|
{chr(10).join(f"| {k[:60]} | {v} |" for k, v in top_choices)}

---

## 🛡️ 人格IP验证

```
价值观指纹  + 情绪指纹  + 决策序列  = 唯一人格ID
{chain['value_fingerprint']} + {chain['emotion_fingerprint']} + [{stats['total_decisions']}个决策点]
= {chain['persona_id']}
```

**任何人可以复制代码，但无法复制这个指纹。**
指纹来源：真实选择历史，不是训练数据。

---

## 下一步

```bash
# 可视化报告
python3 scripts/longhun-persona-visualizer.py
open ~/longhun-system/persona-visual/persona-report.html

# 部署人格验证服务
python3 L6_同步层/longhun-persona-verify.py &

# 节点定时上报
python3 scripts/longhun-node-reporter.py
```

---
> 龍魂系统 v1.7 | 龍芯北辰 UID9622 | 主权归人民
"""


# ═══════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂人格链训练器")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--summary", action="store_true", help="仅显示摘要")
    args = parser.parse_args()

    trainer = PersonaChainTrainer()
    chain = trainer.train()

    if args.json:
        print(json.dumps({
            "persona_id": chain["persona_id"],
            "value_fingerprint": chain["value_fingerprint"],
            "emotion_fingerprint": chain["emotion_fingerprint"],
            "total_decisions": chain["stats"]["total_decisions"],
            "top_values": list(chain["value_profile"].items())[:10],
            "top_emotions": list(chain["emotion_profile"].items()),
        }, ensure_ascii=False, indent=2))
    elif args.summary:
        summary_file = PERSONA_DIR / "persona-summary.md"
        if summary_file.exists():
            print(summary_file.read_text())
        else:
            print("未找到摘要文件")
    else:
        print(f"\n{'='*50}")
        print(f"  人格ID: {chain['persona_id']}")
        print(f"  价值观指纹: {chain['value_fingerprint']}")
        print(f"  情绪指纹:   {chain['emotion_fingerprint']}")
        print(f"  决策点:     {chain['stats']['total_decisions']}")
        print(f"{'='*50}")
        print("运行可视化: python3 scripts/longhun-persona-visualizer.py")


if __name__ == "__main__":
    main()
