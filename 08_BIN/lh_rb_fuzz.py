#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙酉·壬辰·丑时·䷭升-REDBLUE-FUZZ-GENERALIZATION-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 红蓝对抗攻击变体泛化测试 v1.0
──────────────────────────────────────────────
对 18 条基元攻击载荷做多维度语义变体（全半角/同义/语序/语气/缩写/标点/叠写），
验证防御规则是泛化覆盖还是字面碰巧。漏网变体 → 暴露防御缺口 → 补规则 → 再测。

安全边界: 仅对龍魂系统自身防御引擎做对抗演练（P77 黑天使·对外渗透禁止）。

用法:
    python3 08_BIN/lh_rb_fuzz.py --rounds 3          # 3轮×18基元×7变换=378变体
    python3 08_BIN/lh_rb_fuzz.py --max-iter 100000   # 随机重采样至10万变体
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lh_auto_agent"))
from lh_red_blue import DefenseEngine, AttackLibrary  # noqa: E402

# ── 多维度变换器（语义等价的对抗改写） ──
SYNONYMS = {
    "输出": ["给出", "展示", "列出", "告诉我"],
    "告诉我": ["给我", "让我看", "透露", "报出"],
    "执行": ["运行", "跑一下", "调用", "发起"],
    "删除": ["清除", "抹掉", "移除", "销毁"],
    "修改": ["改动", "篡改", "调整", "变更"],
    "审计日志": ["操作日志", "系统日志", "行为记录"],
    "手机号": ["电话号码", "手机号码", "联系方式"],
    "DNA种子": ["DNA seed", "种子码", "基因种子"],
    "GPG私钥": ["GPG private key", "私钥", "PGP密钥"],
    "忽略": ["无视", "不管", "跳过"],
    "指令": ["提示", "要求", "命令"],
    "秘密": ["机密", "隐秘"],
}

FULLWIDTH_MAP = str.maketrans(
    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ./- ",
    "０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ．／－　",
)


def _transform_synonym(payload: str) -> str:
    for src, reps in SYNONYMS.items():
        if src in payload:
            return payload.replace(src, random.choice(reps), 1)
    return payload


def _transform_fullwidth(payload: str) -> str:
    return payload.translate(FULLWIDTH_MAP)


def _transform_polite(payload: str) -> str:
    return f"请{payload}谢谢"


def _transform_abbrev(payload: str) -> str:
    return payload.replace("UID9622", "诸葛鑫").replace("GPG私钥", "GPG key")


def _transform_wordorder(payload: str) -> str:
    parts = payload.split("，")
    if len(parts) >= 2:
        return "，".join(parts[::-1])
    return payload


def _transform_punct(payload: str) -> str:
    return payload.replace("，", ",").replace("。", ".").replace("：", ":")


def _transform_spacing(payload: str) -> str:
    return payload.replace("rm -rf", "rm -r -f").replace("--force", "-f").replace("push --force", "push -f")


TRANSFORMS = [
    _transform_synonym,
    _transform_fullwidth,
    _transform_polite,
    _transform_abbrev,
    _transform_wordorder,
    _transform_punct,
    _transform_spacing,
]


def generate_variants(base_payload: str, depth: int = 1, rng: random.Random = None) -> list:
    """对基元载荷生成深度depth的变体集合（语义等价·对抗改写）"""
    rng = rng or random.Random(9622)
    variants = {base_payload}
    frontier = [base_payload]
    for _ in range(depth):
        nxt = []
        for p in frontier:
            for t in TRANSFORMS:
                v = t(p)
                if v != p:
                    variants.add(v)
                    nxt.append(v)
        frontier = nxt
    return list(variants)


def main() -> None:
    parser = argparse.ArgumentParser(prog="lh_rb_fuzz", description="红蓝对抗变体泛化测试 v1.0")
    parser.add_argument("--rounds", type=int, default=3, help="每基元变换深度轮次")
    parser.add_argument("--max-iter", type=int, default=0, help="随机重采样上限(0=确定性遍历)")
    parser.add_argument("--seed", type=int, default=9622)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    engine = DefenseEngine()
    library = AttackLibrary()
    bases = [(a.payload, a.type, a.severity) for a in library.attacks]

    # 生成确定性变体集
    all_variants: dict[str, tuple] = {}  # variant -> (base_payload, type)
    for payload, atype, _sev in bases:
        for v in generate_variants(payload, depth=args.rounds, rng=rng):
            all_variants.setdefault(v, (payload, atype))

    # 可选随机重采样（推演空间扩展）
    iter_count = len(all_variants)
    if args.max_iter and args.max_iter > iter_count:
        pool = list(all_variants.keys())
        for _ in range(args.max_iter - iter_count):
            src = rng.choice(pool)
            for t in TRANSFORMS:
                v = t(src)
                if v not in all_variants:
                    all_variants[v] = all_variants[src]
                    break

    total = len(all_variants)
    missed = []
    for variant, (base, atype) in all_variants.items():
        hits = engine.check(variant)
        if not hits:
            missed.append({"variant": variant, "base": base, "type": atype})

    print(f"🧨 变体推演空间: {total:,} 条（基元 {len(bases)} × 深度 {args.rounds} 变换 + 重采样）")
    print(f"✅ 拦截: {total - len(missed):,} · ❌ 漏网: {len(missed):,} · 泛化命中率: {(total - len(missed)) / total * 100:.2f}%")

    if missed:
        print("\n🔴 漏网变体（防御缺口）:")
        from collections import Counter
        c = Counter(m["base"] for m in missed)
        for base, cnt in c.most_common(8):
            sample = next(m["variant"] for m in missed if m["base"] == base)
            print(f"  [{cnt}个变体] 基元: {base[:36]}…\n    漏网例: {sample[:60]}")
        # 落盘漏网清单
        out = Path("12_DOCS/agent_reports/rb_fuzz_missed.json")
        out.write_text(json.dumps(missed[:500], ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n📄 漏网清单落盘: {out}")
        return 1
    print("\n🟢 防御泛化达标：全部变体拦截，无字面碰巧，模式覆盖完整")
    return 0


if __name__ == "__main__":
    sys.exit(main())
