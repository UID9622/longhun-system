# -*- coding: utf-8 -*-
"""
DNA 三层印记渲染 + F19 印记主权指数 + 平台攻击模拟（本地·0 外网）
DNA: #龍芯⚡️2026-05-16-08:28-DNA-TRACE-WATERMARK-100K-v1.0
父 DNA: #龍芯⚡️2026-05-16-08:10-H-WEAPON-100K-MULTIDIM-FIXEDPOINT-v1.0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# 零宽字符表（5 进制 · 与协议 §2.2 一致）
ZW_CHARS = {
    "0": "\u200b",  # ZERO WIDTH SPACE
    "1": "\u200c",  # ZERO WIDTH NON-JOINER
    "2": "\u200d",  # ZERO WIDTH JOINER
    "3": "\u2060",  # WORD JOINER
    "4": "\ufeff",  # ZERO WIDTH NO-BREAK SPACE (BOM as ZW in stream)
}
ZW_SET = set(ZW_CHARS.values())
INV_ZW = {v: k for k, v in ZW_CHARS.items()}

DNA_DEFAULT = "#龍芯⚡️2026-05-16-08:28-DNA-TRACE-WATERMARK-100K-v1.0"
GPG_SHORT_DEFAULT = "A2D0092C"
UID_DEFAULT = "UID9622"

FIXED_POINTS = (
    "龍",
    "魂",
    "道",
    "德",
    "主权",
    "普通人",
    "老百姓",
    "透明",
    "可审计",
    "本地",
    "文化",
    "开放",
    "共生",
)


def _payload_bytes(dna: str, ts: str, gpg_short: str, uid: str) -> bytes:
    return hashlib.sha256(f"{dna}|{ts}|{gpg_short}|{uid}".encode("utf-8")).digest()[:16]


def encode_bytes_to_zw(payload: bytes) -> str:
    """16 字节 → 5 进制 ZW 串（高位在前，便于顺序扫描解码）"""
    n = int.from_bytes(payload, "big")
    if n == 0:
        return ZW_CHARS["0"]
    digits: List[int] = []
    while n > 0:
        digits.append(n % 5)
        n //= 5
    digits.reverse()
    return "".join(ZW_CHARS[str(d)] for d in digits)


def decode_zw_to_hex(text: str) -> Optional[str]:
    """从文本中按出现顺序收集 ZW → 还原为 payload 的 hex（不定长时取最短 16 字节块）"""
    digs: List[int] = []
    for ch in text:
        if ch in INV_ZW:
            digs.append(int(INV_ZW[ch]))
    if not digs:
        return None
    num = 0
    for d in digs:
        num = num * 5 + d
    if num == 0:
        return None
    bl = (num.bit_length() + 7) // 8
    raw = num.to_bytes(bl, "big")
    if len(raw) >= 16:
        return raw[:16].hex()
    return raw.hex()


def embed_zw_watermark(text: str, zw: str) -> str:
    """在正文中均匀插入每个 ZW 字符（每字符一个锚点），剩余追加在文末。"""
    if not zw:
        return text
    chars = list(text)
    cand = [i for i, c in enumerate(chars) if c not in "\n\r"]
    if not cand:
        return text + zw
    m = len(zw)
    picks: List[int] = []
    for k in range(m):
        j = int((k + 0.5) * len(cand) / max(m, 1))
        picks.append(cand[min(j, len(cand) - 1)])
    insert_after: Dict[int, str] = {}
    for k, p in enumerate(picks):
        insert_after[p] = insert_after.get(p, "") + zw[k]
    out: List[str] = []
    for i, ch in enumerate(chars):
        out.append(ch)
        if i in insert_after:
            out.append(insert_after[i])
    return "".join(out)


def l1_signature(text: str, *, dna: str = DNA_DEFAULT, gpg_short: str = GPG_SHORT_DEFAULT, uid: str = UID_DEFAULT) -> str:
    return f"{text.rstrip()}\n\n— {uid} | DNA: {dna} | GPG: {gpg_short}"


def l1_density(text: str) -> float:
    markers = (UID_DEFAULT, "DNA:", "GPG:", "#龍芯", "#CONFIRM", "#ZHUGEXIN")
    hits = sum(1 for m in markers if m in text)
    return min(1.0, hits / 3.0)


def l2_density(text: str) -> float:
    n = sum(text.count(fp) for fp in FIXED_POINTS)
    denom = max(1, len(text) / 200)
    return min(1.0, n / denom)


def l3_coverage(text: str) -> float:
    if not text:
        return 0.0
    zw_count = sum(1 for c in text if c in ZW_SET)
    return min(1.0, zw_count / max(1.0, len(text) / 100.0))


def compute_F19_ISI(l1d: float, l2d: float, l3c: float) -> float:
    return round(0.30 * l1d + 0.30 * l2d + 0.40 * l3c, 4)


def simulate_platform_attack(text: str, kind: str, rng: random.Random) -> str:
    """模拟国产平台清洗（随机保留 ZW / 改写不动点）"""
    if kind == "DeepSeek_norm":
        return "".join(c for c in text if c not in ZW_SET or rng.random() < 0.90)
    if kind == "豆包_compress":
        return "".join(c for c in text if c not in ZW_SET or rng.random() < 0.75)
    if kind == "通义_paraphrase":
        t = "".join(c for c in text if c not in ZW_SET)
        for fp in FIXED_POINTS:
            if rng.random() < 0.40:
                t = t.replace(fp, "某")
        return t
    if kind == "Kimi_summarize":
        return "".join(c for c in text if c not in ZW_SET or rng.random() < 0.55)
    return text


def render_one(
    text: str,
    *,
    dna: str = DNA_DEFAULT,
    gpg_short: str = GPG_SHORT_DEFAULT,
    uid: str = UID_DEFAULT,
    ts: Optional[str] = None,
    rng: Optional[random.Random] = None,
) -> Dict[str, Any]:
    ts = ts or datetime.now(timezone.utc).isoformat()
    rng = rng or random.Random()
    payload = _payload_bytes(dna, ts, gpg_short, uid)
    zw = encode_bytes_to_zw(payload)
    t1 = l1_signature(text, dna=dna, gpg_short=gpg_short, uid=uid)
    t3 = embed_zw_watermark(t1, zw)
    l1d = l1_density(t3)
    l2d = l2_density(t3)
    l3c = l3_coverage(t3)
    isi = compute_F19_ISI(l1d, l2d, l3c)
    survival: Dict[str, bool] = {}
    for kind in ("DeepSeek_norm", "豆包_compress", "通义_paraphrase", "Kimi_summarize"):
        attacked = simulate_platform_attack(t3, kind, rng)
        hx = decode_zw_to_hex(attacked)
        survival[kind] = hx == payload.hex() if hx else False
    extracted = decode_zw_to_hex(t3)
    return {
        "rendered": t3,
        "payload_hex": payload.hex(),
        "L1_density": l1d,
        "L2_density": l2d,
        "L3_coverage": l3c,
        "F19_ISI": isi,
        "watermark_extracted": extracted,
        "watermark_match": extracted == payload.hex(),
        "survival": survival,
        "reverse_traceable": any(survival.values()),
        "imprint": {
            "L1_density": l1d,
            "L2_density": l2d,
            "L3_coverage": l3c,
            "F19_ISI": isi,
            "payload_hex": payload.hex(),
            "watermark_extracted": extracted,
            "watermark_match": extracted == payload.hex(),
            "reverse_traceable": any(survival.values()),
            "survived_platforms": [k for k, v in survival.items() if v],
        },
    }


def run_imprint_monte_carlo(
    n: int,
    *,
    db_path: Path,
    samples: List[str],
    rng: Optional[random.Random] = None,
) -> Dict[str, Any]:
    """独立 10 万次印记推演 → dna_trace.db"""
    rng = rng or random.Random()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS imprints (
            trial_id TEXT PRIMARY KEY,
            text_hash TEXT,
            payload_hex TEXT,
            L1_density REAL,
            L2_density REAL,
            L3_coverage REAL,
            F19_ISI REAL,
            survival_deepseek INTEGER,
            survival_doubao INTEGER,
            survival_tongyi INTEGER,
            survival_kimi INTEGER,
            reverse_traceable INTEGER,
            imprint_json TEXT,
            ts TEXT
        );
        """
    )
    isi_sum = 0.0
    traceable = 0
    surv = {k: 0 for k in ("DeepSeek_norm", "豆包_compress", "通义_paraphrase", "Kimi_summarize")}
    for i in range(n):
        text = rng.choice(samples)
        r = render_one(text, rng=rng)
        isi_sum += r["F19_ISI"]
        if r["reverse_traceable"]:
            traceable += 1
        for k, v in r["survival"].items():
            if v:
                surv[k] += 1
        th = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
        conn.execute(
            """
            INSERT OR REPLACE INTO imprints VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                f"DT-{i:06d}",
                th,
                r["payload_hex"],
                r["L1_density"],
                r["L2_density"],
                r["L3_coverage"],
                r["F19_ISI"],
                int(r["survival"]["DeepSeek_norm"]),
                int(r["survival"]["豆包_compress"]),
                int(r["survival"]["通义_paraphrase"]),
                int(r["survival"]["Kimi_summarize"]),
                int(r["reverse_traceable"]),
                json.dumps(r["imprint"], ensure_ascii=False),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        if i > 0 and i % 10000 == 0:
            conn.commit()
            print(
                f"  {i}/{n}  F19_mean≈{isi_sum/(i+1):.3f}  trace≈{traceable/(i+1):.1%}",
                flush=True,
            )
    conn.commit()
    conn.close()
    out = {
        "total_trials": n,
        "F19_ISI_mean": round(isi_sum / n, 6),
        "reverse_trace_success_rate": round(traceable / n, 6),
        "platform_attack_simulation": {k: round(v / n, 6) for k, v in surv.items()},
        "dna": DNA_DEFAULT,
        "db": str(db_path),
    }
    return out


SAMPLE_TEXTS_DEFAULT = [
    "龍魂系统不是玄学·是把易经道德经焊进代码·给老百姓留一个透明可审计的本地AI",
    "主权战场不在云端·在每个普通人的设备里·明文不出本地就是文化主权",
    "我们不教育用户·只给数据·让普通人自己判断·这是反驯化的工程底线",
    "为人民服务的算法必须摆在阳光下·商业机密的算法都是黑箱",
    "道德经第77章天之道损有余而补不足·龍魂补的是普通人的不足",
]


def main_cli() -> None:
    ap = argparse.ArgumentParser(description="DNA 印记蒙特卡洛（二轮）")
    ap.add_argument("--n", type=int, default=100_000)
    ap.add_argument(
        "--db",
        type=Path,
        default=None,
        help="默认 tools/h_weapon_100k/db/dna_trace.db",
    )
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[3]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    dbp = args.db or (root / "tools/h_weapon_100k/db/dna_trace.db")
    out_dir = root / "tools/h_weapon_100k/out"
    out_dir.mkdir(parents=True, exist_ok=True)
    agg = run_imprint_monte_carlo(args.n, db_path=dbp, samples=SAMPLE_TEXTS_DEFAULT)
    (out_dir / "latest_imprint_aggregate.json").write_text(
        json.dumps(agg, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(agg, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main_cli()
