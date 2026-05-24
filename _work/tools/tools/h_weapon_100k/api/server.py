# -*- coding: utf-8 -*-
"""
H武器 MVP API · 仅 127.0.0.1:8765 · 不对外
DNA: #龍芯⚡️2026-05-16-08:10-MVP-API-v1.0
"""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[3]
EVENTS_DB = REPO_ROOT / "tools/h_weapon_100k/db/events.db"
FOOTPRINT_DB = REPO_ROOT / "tools/h_weapon_100k/db/footprint.db"
RUNNER = REPO_ROOT / "tools/h_weapon_100k/core/h_weapon_runner.py"
MINER = REPO_ROOT / "tools/h_weapon_100k/scripts/footprint_miner.py"
IMPRINT_SCRIPT = REPO_ROOT / "tools/h_weapon_100k/core/dna_imprint_renderer.py"
DNA_TRACE_DB = REPO_ROOT / "tools/h_weapon_100k/db/dna_trace.db"
IMPRINT_AGG = REPO_ROOT / "tools/h_weapon_100k/out/latest_imprint_aggregate.json"


def _subp_py(script: Path, args: list) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT)
    log = REPO_ROOT / "tools/h_weapon_100k/out/api_subprocess.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a", encoding="utf-8") as lf:
        lf.write(f"\n--- {sys.argv} {args}\n")
        subprocess.Popen(
            [sys.executable, str(script), *args],
            cwd=str(REPO_ROOT),
            env=env,
            stdout=lf,
            stderr=subprocess.STDOUT,
        )


class Handler(BaseHTTPRequestHandler):
    server_version = "CNSW-HWeapon/1.1"

    def log_message(self, fmt: str, *args: object) -> None:
        return

    def _hdr(self) -> None:
        o = self.headers.get("Origin") or "*"
        self.send_header("Access-Control-Allow-Origin", o)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self._hdr()
        self.end_headers()

    def _json(self, data: object, code: int = 200) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._hdr()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        u = urlparse(self.path)
        if u.path == "/api/stats":
            self._json(self._stats())
        elif u.path == "/api/footprints":
            self._json(self._footprints())
        elif u.path == "/api/health":
            self._json({"ok": True, "service": "h_weapon", "repo": str(REPO_ROOT)})
        elif u.path == "/api/imprint/stats":
            self._json(self._imprint_stats())
        elif u.path == "/api/imprint/aggregate":
            if IMPRINT_AGG.exists():
                self._json(json.loads(IMPRINT_AGG.read_text(encoding="utf-8")))
            else:
                self._json({"error": "no latest_imprint_aggregate.json"}, 404)
        elif u.path == "/api/aggregate":
            p = REPO_ROOT / "tools/h_weapon_100k/out/latest_aggregate.json"
            if p.exists():
                self._json(json.loads(p.read_text(encoding="utf-8")))
            else:
                self._json({"error": "no latest_aggregate.json yet"}, 404)
        else:
            self.send_error(404, "Not Found")
        u = urlparse(self.path)
        n = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(n) if n else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            payload = {}
        if u.path == "/api/h_weapon/run":
            trials = int(payload.get("n", 1000))
            max_loops = int(payload.get("max_loops", 3))
            _subp_py(RUNNER, ["--n", str(trials), "--max-loops", str(max_loops)])
            self._json({"started": True, "n": trials, "max_loops": max_loops, "log": "tools/h_weapon_100k/out/api_subprocess.log"})
        elif u.path == "/api/footprint/scan":
            _subp_py(MINER, [])
            self._json({"started": True, "log": "tools/h_weapon_100k/out/api_subprocess.log"})
        elif u.path == "/api/imprint/run":
            trials = int(payload.get("n", 10_000))
            _subp_py(IMPRINT_SCRIPT, ["--n", str(trials)])
            self._json(
                {
                    "started": True,
                    "n": trials,
                    "log": "tools/h_weapon_100k/out/api_subprocess.log",
                    "dna": "#龍芯⚡️2026-05-16-08:28-DNA-TRACE-WATERMARK-100K-v1.0",
                }
            )
        else:
            self.send_error(404, "Not Found")

    def _stats(self) -> dict:
        if not EVENTS_DB.exists():
            return {"error": "no events.db", "hint": "先 POST /api/h_weapon/run 或命令行跑 runner"}
        conn = sqlite3.connect(str(EVENTS_DB))
        c = conn.cursor()
        c.execute("SELECT COUNT(*), AVG(F18_SI), SUM(CASE WHEN F18_SI<0.34 THEN 1 ELSE 0 END) FROM trials")
        row = c.fetchone()
        total, si_mean, si_lost = row[0] or 0, row[1] or 0, row[2] or 0
        c.execute("SELECT sancai_color, COUNT(*) FROM trials GROUP BY sancai_color")
        colors = dict(c.fetchall())
        c.execute(
            "SELECT detected_drift, COUNT(*) FROM trials GROUP BY detected_drift ORDER BY 2 DESC"
        )
        drifts = dict(c.fetchall())
        out = {
            "total": total,
            "F18_mean": si_mean,
            "sovereignty_lost": si_lost,
            "colors": colors,
            "drifts": drifts,
        }
        cols = {r[1] for r in c.execute("PRAGMA table_info(trials)").fetchall()}
        if "f19_isi" in cols:
            c.execute("SELECT AVG(f19_isi), COUNT(*) FROM trials WHERE f19_isi IS NOT NULL")
            r2 = c.fetchone()
            if r2 and r2[0] is not None:
                out["F19_ISI_mean_trials"] = round(r2[0], 6)
                out["trials_with_imprint"] = r2[1]
        conn.close()
        return out

    def _footprints(self) -> dict:
        if not FOOTPRINT_DB.exists():
            return {"error": "no footprint.db", "hint": "先 POST /api/footprint/scan"}
        conn = sqlite3.connect(str(FOOTPRINT_DB))
        c = conn.cursor()
        c.execute("SELECT product, COUNT(*), COALESCE(SUM(size),0) FROM footprints GROUP BY product")
        items = [{"product": r[0], "count": r[1], "total_size": r[2]} for r in c.fetchall()]
        conn.close()
        return {"targets": items}

    def _imprint_stats(self) -> dict:
        if not DNA_TRACE_DB.exists():
            return {"error": "no dna_trace.db", "hint": "先 POST /api/imprint/run 或命令行跑 dna_imprint_renderer.py"}
        conn = sqlite3.connect(str(DNA_TRACE_DB))
        c = conn.cursor()
        c.execute("SELECT COUNT(*), AVG(F19_ISI) FROM imprints")
        row = c.fetchone()
        total, avg_isi = row[0] or 0, row[1] or 0
        c.execute(
            "SELECT SUM(reverse_traceable), SUM(survival_deepseek), SUM(survival_doubao) FROM imprints"
        )
        r2 = c.fetchone()
        conn.close()
        return {
            "imprint_trials": total,
            "F19_ISI_mean": avg_isi,
            "reverse_traceable_total": r2[0] or 0,
            "survival_deepseek_hits": r2[1] or 0,
            "survival_doubao_hits": r2[2] or 0,
            "db": str(DNA_TRACE_DB),
        }


def main() -> None:
    host = "127.0.0.1"
    port = 8765
    print(f"龍魂 H武器 MVP API · http://{host}:{port}  （仅本机）", flush=True)
    HTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
