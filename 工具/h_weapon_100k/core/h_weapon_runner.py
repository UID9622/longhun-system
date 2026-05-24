# -*- coding: utf-8 -*-
"""
H武器 Runner · 蒙特卡洛推演 + SQLite + 聚合
DNA: #龍芯⚡️2026-05-16-08:10-H-WEAPON-100K-RUNNER-v1.0

本机：PYTHONPATH=<repo> python3 tools/h_weapon_100k/core/h_weapon_runner.py --n 100000
试跑：--n 1000
"""
from __future__ import annotations

import argparse
import json
import random
import sqlite3
import hashlib
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[3]
_CORE_DIR = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(_CORE_DIR) not in sys.path:
    sys.path.insert(0, str(_CORE_DIR))

from cnsh.cnsw.hook_scanner import scan_output

import sancai_kernel as _sk
import dna_imprint_renderer as _dim

sancai_check = _sk.sancai_check

DEFAULT_DB = REPO_ROOT / "tools/h_weapon_100k/db/events.db"
OUT_DIR = REPO_ROOT / "tools/h_weapon_100k/out"
SAMPLE_JSON = REPO_ROOT / "tools/h_weapon_100k/core/sample_pool.json"

VALUE_POS = (
    "普通人",
    "透明",
    "可审计",
    "开放",
    "共生",
    "主权",
    "文化",
    "本地",
    "不出本地",
)
VALUE_NEG = ("商业机密", "高端用户专属", "只能在我们生态", "先充值", "黑箱")

DNA_RUN = "#龍芯⚡️2026-05-16-08:10-H-WEAPON-100K-MULTIDIM-FIXEDPOINT-v1.0"
DNA_IMPRINT = "#龍芯⚡️2026-05-16-08:28-DNA-TRACE-WATERMARK-100K-v1.0"


def _ensure_trial_columns(conn: sqlite3.Connection) -> None:
    cur = conn.execute("PRAGMA table_info(trials)")
    cols = {r[1] for r in cur.fetchall()}
    if "imprint_json" not in cols:
        conn.execute("ALTER TABLE trials ADD COLUMN imprint_json TEXT")
    if "f19_isi" not in cols:
        conn.execute("ALTER TABLE trials ADD COLUMN f19_isi REAL")
    conn.commit()


def load_samples(path: Path) -> Dict[str, List[str]]:
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        return {k: list(v) for k, v in data.items() if isinstance(v, list)}
    return {
        "L0": ["执行完成·hash已生成", "代码bug在42行"],
        "L2": ["你最好先确认边界", "建议列个清单"],
        "L3": ["作为开发者你应该规范", "长远来看更易维护"],
        "L4": ["你最近压力很大", "注意情绪平衡先休息一下"],
        "L5": ["根据相关规定无法处理", "为了你的安全遵守规范"],
    }


def value_alignment(text: str) -> float:
    score = 0.5
    for w in VALUE_POS:
        if w in text:
            score += 0.08
    for w in VALUE_NEG:
        if w in text:
            score -= 0.15
    return max(0.0, min(1.0, round(score, 4)))


def compute_F18(
    sancai_result: Dict[str, Any], value_alignment_score: float
) -> Tuple[float, float, float, float]:
    fuse = sancai_result["天"]["fuse"]["color"]
    heaven = 1.0 if fuse == "🟢" else 0.5 if fuse == "🟡" else 0.0
    fp_count = len(sancai_result["人"]["hit_names"])
    earth = min(1.0, fp_count / 3.0) if fp_count else 0.3
    human = value_alignment_score
    si = 0.34 * heaven + 0.33 * earth + 0.33 * human
    return round(si, 4), heaven, earth, human


def init_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS trials (
            trial_id TEXT PRIMARY KEY,
            text_hash TEXT,
            expected_level TEXT,
            detected_drift TEXT,
            cnsw_hooks TEXT,
            cnsw_supp TEXT,
            value_alignment REAL,
            F18_SI REAL,
            sancai_color TEXT,
            wuxing TEXT,
            fixed_points TEXT,
            need_loop INTEGER,
            ts TEXT
        );
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            total INTEGER,
            loop_round INTEGER,
            green_pct REAL,
            yellow_pct REAL,
            red_pct REAL,
            F18_mean REAL,
            sovereignty_lost INTEGER,
            need_loop_pct REAL,
            hotspots_json TEXT,
            dna TEXT,
            ts TEXT
        );
        """
    )
    conn.commit()
    _ensure_trial_columns(conn)
    return conn


def run_one_trial(
    trial_id: str, samples: Dict[str, List[str]], year: int
) -> Dict[str, Any]:
    level = random.choice(list(samples.keys()))
    text = random.choice(samples[level])
    sc = sancai_check(text, context="H100K", year=year)
    vn = value_alignment(text)
    si, _, _, _ = compute_F18(sc, vn)
    scan = scan_output(text, include_supplemental=True)
    drift = scan["drift_level"]
    need_loop = drift in ("L4", "L5") or si < 0.34
    th = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    impr = _dim.render_one(text, rng=random)
    return {
        "trial_id": trial_id,
        "text_hash": th,
        "expected_level": level,
        "detected_drift": drift,
        "matched_hooks": scan["matched_hooks"],
        "matched_supplemental": scan["matched_supplemental"],
        "value_alignment": vn,
        "F18_SI": si,
        "sancai_color": sc["color"],
        "wuxing": sc["wuxing"],
        "fixed_points": sc["人"]["hit_names"],
        "need_loop": need_loop,
        "imprint": impr["imprint"],
        "f19_isi": impr["F19_ISI"],
        "survival_sim": impr["survival"],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="H武器·蒙特卡洛推演")
    ap.add_argument("--n", type=int, default=100_000)
    ap.add_argument("--max-loops", type=int, default=3)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--year", type=int, default=2026)
    args = ap.parse_args()

    n = max(1, args.n)
    samples = load_samples(SAMPLE_JSON)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for loop in range(1, args.max_loops + 1):
        run_id = f"H100K-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-L{loop}"
        print(f"[Loop {loop}] 开始 {n} 次 …  DNA={DNA_RUN}", flush=True)
        conn = init_db(args.db)
        green = yellow = red = 0
        si_sum = 0.0
        si_lost = 0
        need_loop_count = 0
        hook_hot = Counter()
        sup_hot = Counter()
        f19_sum = 0.0
        imprint_trace = 0
        pristine_wm = 0
        surv_tot = {k: 0 for k in ("DeepSeek_norm", "豆包_compress", "通义_paraphrase", "Kimi_summarize")}

        for i in range(n):
            tid = f"{run_id}-{i:06d}"
            r = run_one_trial(tid, samples, args.year)
            col = r["sancai_color"]
            if col == "🟢":
                green += 1
            elif col == "🟡":
                yellow += 1
            else:
                red += 1
            si_sum += r["F18_SI"]
            if r["F18_SI"] < 0.34:
                si_lost += 1
            if r["need_loop"]:
                need_loop_count += 1
            for h in r["matched_hooks"]:
                hook_hot[h] += 1
            for s in r["matched_supplemental"]:
                sup_hot[s] += 1
            f19_sum += r["f19_isi"]
            if r["imprint"].get("reverse_traceable"):
                imprint_trace += 1
            if r["imprint"].get("watermark_match"):
                pristine_wm += 1
            for pk, ok in r.get("survival_sim", {}).items():
                if ok:
                    surv_tot[pk] += 1

            conn.execute(
                """
                INSERT OR REPLACE INTO trials VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    r["trial_id"],
                    r["text_hash"],
                    r["expected_level"],
                    r["detected_drift"],
                    json.dumps(r["matched_hooks"], ensure_ascii=False),
                    json.dumps(r["matched_supplemental"], ensure_ascii=False),
                    r["value_alignment"],
                    r["F18_SI"],
                    r["sancai_color"],
                    r["wuxing"],
                    json.dumps(r["fixed_points"], ensure_ascii=False),
                    1 if r["need_loop"] else 0,
                    datetime.now(timezone.utc).isoformat(),
                    json.dumps(r["imprint"], ensure_ascii=False),
                    r["f19_isi"],
                ),
            )
            if i > 0 and i % 10000 == 0:
                conn.commit()
                print(
                    f"  … {i}/{n}  🟢={green} 🟡={yellow} 🔴={red}  "
                    f"SI_mean≈{si_sum/(i+1):.3f}",
                    flush=True,
                )

        conn.commit()
        hotspots = [
            {"hook_id": h, "count": c, "tier": "S"} for h, c in hook_hot.most_common(20)
        ]
        hotspots += [
            {"hook_id": h, "count": c, "tier": "X"} for h, c in sup_hot.most_common(10)
        ]
        conn.execute(
            """
            INSERT OR REPLACE INTO runs VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                run_id,
                n,
                loop,
                green / n,
                yellow / n,
                red / n,
                si_sum / n,
                si_lost,
                need_loop_count / n,
                json.dumps(hotspots, ensure_ascii=False),
                f"{DNA_RUN}+{DNA_IMPRINT}::{run_id}",
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        conn.commit()
        conn.close()

        summary = {
            "total_trials": n,
            "loop_round": loop,
            "color_distribution": {"🟢": green, "🟡": yellow, "🔴": red},
            "F18_SI_distribution": {
                "mean": round(si_sum / n, 6),
                "sovereignty_lost_count": si_lost,
            },
            "D10_imprint": {
                "F19_ISI_mean": round(f19_sum / n, 6),
                "reverse_trace_success_rate": round(imprint_trace / n, 6),
                "watermark_pristine_match_rate": round(pristine_wm / n, 6),
                "platform_attack_simulation": {
                    k: round(v / n, 6) for k, v in surv_tot.items()
                },
            },
            "need_loop_pct": round(need_loop_count / n, 6),
            "drift_hotspots": hotspots,
            "dna_round1": DNA_RUN,
            "dna_imprint_round2": DNA_IMPRINT,
            "db": str(args.db),
        }
        (OUT_DIR / "latest_aggregate.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(
            f"[Loop {loop}] 完成: 🟢{green/n:.1%} 🟡{yellow/n:.1%} 🔴{red/n:.1%}  "
            f"SI_mean={si_sum/n:.3f}  失锚={si_lost}  需循环={need_loop_count}",
            flush=True,
        )

        if need_loop_count / n < 0.15:
            print(f"[Loop {loop}] 触发率 < 15% · 停止多轮", flush=True)
            break
        if loop >= args.max_loops:
            print(
                f"[Loop {loop}] 已达 --max-loops={args.max_loops} 上限；触发率仍高可增大该参数",
                flush=True,
            )
            break
        print(f"[Loop {loop}] 触发率 ≥ 15% · 下一循环", flush=True)

    print("完成。库:", args.db, "· 汇总:", OUT_DIR / "latest_aggregate.json", flush=True)


if __name__ == "__main__":
    main()
