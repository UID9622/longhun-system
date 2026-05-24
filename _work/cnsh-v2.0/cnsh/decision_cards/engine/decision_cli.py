# -*- coding: utf-8 -*-
"""
UID9622 责任卡 CLI — 默认根目录为仓库内 cnsh/decision_cards；
可通过 CNSH_DECISION_CARDS_HOME 指向 ~/cnsh/决策卡片 等路径。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from responsibility_router import decision_level, route_card_type


def _base_dir() -> Path:
    env = (os.environ.get("CNSH_DECISION_CARDS_HOME") or "").strip()
    if env:
        return Path(env).expanduser()
    return Path(__file__).resolve().parent.parent


BASE_DIR = _base_dir()
TEMPLATE_DIR = BASE_DIR / "templates"
DAILY_DIR = BASE_DIR / "cards" / "daily"
MAJOR_DIR = BASE_DIR / "cards" / "major"
DB_PATH = BASE_DIR / "db" / "decision_cards.sqlite"
LOG_PATH = BASE_DIR / "logs" / "decision_trace.log"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def today_compact() -> str:
    return datetime.now().strftime("%Y%m%d")


def hash8(text: str) -> str:
    raw = f"{text}|{now_iso()}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:8].upper()


def make_dna(h: str) -> str:
    return f"#龍芯⚡️{today_compact()}-DEC-{h}"


def ensure_dirs() -> None:
    for d in (DAILY_DIR, MAJOR_DIR, DB_PATH.parent, LOG_PATH.parent):
        d.mkdir(parents=True, exist_ok=True)


def ensure_db() -> None:
    ensure_dirs()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS decision_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dna TEXT NOT NULL UNIQUE,
            hash8 TEXT NOT NULL,
            created_at TEXT NOT NULL,
            card_type TEXT NOT NULL,
            decision_level TEXT NOT NULL,
            title TEXT,
            trigger_input TEXT,
            selected_option TEXT,
            color TEXT,
            file_path TEXT,
            raw_json TEXT,
            final_authority TEXT DEFAULT 'UID9622'
        );
        """
    )
    conn.commit()
    conn.close()


def log_line(message: str) -> None:
    ensure_dirs()
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] {message}\n")


def load_template(card_type: str) -> str:
    name = "light_card.md" if card_type == "light" else "full_card.md"
    path = TEMPLATE_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"缺少模板: {path}")
    return path.read_text(encoding="utf-8")


def replace_placeholders(template: str, data: dict[str, Any]) -> str:
    out = template
    for k, v in data.items():
        out = out.replace("{{" + k + "}}", str(v))
    return out


def tri_color_for_card(card_type: str, level: str) -> str:
    if card_type == "full" and level in ("L0", "L1"):
        return "🟢"
    if card_type == "light":
        return "🟡"
    return "🟢"


def build_light_payload(text: str, h: str, dna: str, level: str, color: str) -> str:
    data = {
        "DNA": dna,
        "CREATED_AT": now_iso(),
        "LEVEL": level,
        "COLOR": color,
        "TRIGGER": text,
        "SOURCES": "UID9622 主控规则 / 责任卡 v2.0 摘要 / 本仓库 PROTOCOL__CNSH-TOOLCHAIN-FUSION",
        "OPTION_A": "仅回复，不生成责任卡",
        "OPTION_B": "生成轻量责任卡",
        "OPTION_C": "升级为完整责任卡",
        "SELECTED_OPTION": "B",
        "CHOICE_REASON": "日常判断先留轻量痕",
        "COLOR_REASON": "结构完整，主控仍可覆写",
        "RESPONSIBILITY": "AI 生成 · UID9622 定盘",
    }
    return replace_placeholders(load_template("light"), data)


def build_full_payload(text: str, h: str, dna: str, level: str, color: str) -> tuple[str, str]:
    anchor = f"ANCHOR-DEC-{today_compact()}-{h}"
    fp_placeholder = str(MAJOR_DIR / f"RESPONSIBILITY_CARD_{today_compact()}_{level}_{h}.md")
    data = {
        "DNA": dna,
        "CREATED_AT": now_iso(),
        "LEVEL": level,
        "COLOR": color,
        "ANCHOR_ID": anchor,
        "TRIGGER": fs_section(text),
        "SOURCES": "- 用户触发原文\n- PROTOCOL__CNSH-TOOLCHAIN-FUSION-v1.0\n- 本机决策卡引擎",
        "RULES": "UID9622 主控 + 三色审计 + 备选不得为空（重大 🔴）",
        "OPTION_A": "推迟，不生成文件",
        "OPTION_B": "轻量卡-only",
        "OPTION_C": "完整卡 + 归档路径",
        "A_BEN": "最快",
        "A_COST": "无留痕",
        "A_RISK": "不可追溯",
        "B_BEN": "快",
        "B_COST": "字段少",
        "B_RISK": "重大决策不足",
        "C_BEN": "链完整",
        "C_COST": "篇幅长",
        "C_RISK": "需人审",
        "OPTIONS_OK": "🟢 充分（示例三选）",
        "SELECTED": "C",
        "CHOICE_REASON": "工程/网关类触发默认完整留痕",
        "REJECT_NOTE": "未选 A/B：因需可追溯责任链",
        "COLOR_REASON": "模板字段齐；若真实场景缺源或备选应人工降为 🟡/🔴",
        "EXEC_ACTOR": "AI + 本机脚本",
        "AUDIT_NOTE": "AI 标色 · UID9622 验收",
        "ROLLBACK": "删除本文件或生成纠错卡；已登锚则需登记废止",
        "FILE_PATH": fp_placeholder,
        "NOTION_HINT": "主控母页 / CNSH 规则库（仅建议，不自动写入）",
    }
    body = replace_placeholders(load_template("full"), data)
    return body, anchor


def fs_section(text: str) -> str:
    t = (text or "").strip()
    if len(t) > 800:
        t = t[:800] + "…"
    return t


def save_card(card_type: str, content: str, h: str, level: str) -> Path:
    ensure_dirs()
    directory = DAILY_DIR if card_type == "light" else MAJOR_DIR
    prefix = "DECISION_CARD" if card_type == "light" else "RESPONSIBILITY_CARD"
    path = directory / f"{prefix}_{today_compact()}_{level}_{h}.md"
    path.write_text(content, encoding="utf-8")
    return path


def insert_row(
    *,
    dna: str,
    h: str,
    card_type: str,
    level: str,
    trigger: str,
    color: str,
    file_path: Path,
) -> None:
    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    payload = {
        "dna": dna,
        "hash8": h,
        "card_type": card_type,
        "level": level,
        "path": str(file_path),
    }
    cur.execute(
        """
        INSERT OR IGNORE INTO decision_cards
        (dna, hash8, created_at, card_type, decision_level, title, trigger_input,
         selected_option, color, file_path, raw_json, final_authority)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            dna,
            h,
            now_iso(),
            card_type,
            level,
            trigger[:80],
            trigger,
            "AUTO",
            color,
            str(file_path),
            json.dumps(payload, ensure_ascii=False),
            "UID9622",
        ),
    )
    conn.commit()
    conn.close()


def run_generate(
    text: str,
    *,
    force_light: bool = False,
    force_full: bool = False,
) -> dict[str, Any]:
    text = text.strip()
    if not text:
        raise ValueError("触发文本为空")
    force = "light" if force_light else "full" if force_full else ""
    card_type = route_card_type(text, force)
    level = decision_level(text, card_type)
    h = hash8(text)
    dna = make_dna(h)
    color = tri_color_for_card(card_type, level)

    if card_type == "light":
        body = build_light_payload(text, h, dna, level, color)
    else:
        body, _anchor = build_full_payload(text, h, dna, level, color)

    path = save_card(card_type, body, h, level)
    insert_row(
        dna=dna,
        h=h,
        card_type=card_type,
        level=level,
        trigger=text,
        color=color,
        file_path=path,
    )
    log_line(f"card {dna} {card_type} {path}")
    return {
        "dna": dna,
        "hash8": h,
        "card_type": card_type,
        "level": level,
        "color": color,
        "path": str(path),
    }


def cmd_list() -> None:
    ensure_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT created_at, hash8, card_type, decision_level, color, file_path
        FROM decision_cards ORDER BY id DESC LIMIT 30
        """
    )
    for row in cur.fetchall():
        print(" | ".join(str(x) for x in row))
    conn.close()


def cmd_show(key: str) -> None:
    key_u = key.strip().upper()
    matches = list(BASE_DIR.rglob(f"*{key_u}*.md"))
    if not matches:
        print(f"未找到: {key}", file=sys.stderr)
        sys.exit(1)
    print(matches[0].read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="UID9622 责任卡生成器")
    ap.add_argument("text", nargs="*", help="触发文本")
    ap.add_argument("--light", action="store_true")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--show", metavar="HASH", default="")
    args = ap.parse_args(argv)

    if args.list:
        cmd_list()
        return 0
    if args.show:
        cmd_show(args.show)
        return 0

    text = " ".join(args.text).strip()
    if not text:
        ap.print_help()
        return 2

    try:
        rec = run_generate(text, force_light=args.light, force_full=args.full)
    except Exception as e:
        print(f"🔴 {e}", file=sys.stderr)
        return 1

    print("【责任卡生成回执】")
    print(f"类型: {'轻量' if rec['card_type'] == 'light' else '完整'}")
    print(f"等级: {rec['level']}")
    print(f"DNA: {rec['dna']}")
    print(f"路径: {rec['path']}")
    print(f"三色: {rec['color']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
