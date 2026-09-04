#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-08-30-TONGXINYI-LEXICON-BUILD-v1.0-b8e3c9f1
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂·门户词库构建工具 v1.0
把权威词库（tongxinyi-semantic 交付包 8 抽屉 YAML + tongxinyi_config.json 映射）
合并生成门户可加载的 `10_PORTAL/tongxinyi/lexicon.json`。

用法: python3 08_BIN/lh_tongxinyi_lexicon_build.py [--out 路径]
"""
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parent.parent
SEMANTIC = ROOT / "15_LABS" / "kimi-deliverables" / "Kimi_Agent_DNA生成器网站搭建 (1)" / "tongxinyi-semantic"
CONFIG = ROOT / "08_BIN" / "tongxinyi_config.json"
DEFAULT_OUT = ROOT / "10_PORTAL" / "tongxinyi" / "lexicon.json"


def build() -> dict:
    if yaml is None:
        print("❌ 需要 PyYAML（pip install pyyaml）")
        sys.exit(1)
    if not SEMANTIC.exists():
        print(f"❌ 交付包不存在: {SEMANTIC}")
        sys.exit(1)

    drawers = []
    for d in range(1, 9):
        f = SEMANTIC / "drawers" / f"D0{d}_*.yaml"
        files = sorted(SEMANTIC.glob(f"drawers/D0{d}_*.yaml"))
        if not files:
            continue
        data = yaml.safe_load(files[0].read_text(encoding="utf-8"))
        entries = []
        for e in data.get("entries", []):
            entries.append({
                "term": e.get("term", ""),
                "alias": e.get("alias", []),
                "en": e.get("en", ""),
                "cnsh": e.get("cnsh", ""),
                "gua": e.get("gua", ""),
                "status": e.get("status", "种子"),
                "note": e.get("note", ""),
            })
        drawers.append({
            "id": data.get("drawer", f"D0{d}"),
            "name": data.get("name", ""),
            "persona": data.get("persona", ""),
            "entries": entries,
        })

    config_mappings = []
    if CONFIG.exists():
        cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
        config_mappings = cfg.get("mappings", [])

    total = sum(len(d["entries"]) for d in drawers)
    return {
        "meta": {
            "name": "龍魂语义库",
            "version": "v0.1",
            "uid": "UID9622",
            "source": "tongxinyi-semantic 交付包(8抽屉) + tongxinyi_config v2.0",
            "drawers": len(drawers),
            "entries": total,
            "config_mappings": len(config_mappings),
            "built_at": datetime.now().isoformat(timespec="seconds"),
            "dna": "#龍芯⚡️2026-08-30-TONGXINYI-LEXICON-v0.1-b8e3c9f1",
        },
        "drawers": drawers,
        "config_mappings": config_mappings,
    }


if __name__ == "__main__":
    out = DEFAULT_OUT
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
    data = build()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    m = data["meta"]
    print(f"✅ 词库已生成: {out}")
    print(f"   抽屉 {m['drawers']} · 词元 {m['entries']} · 映射 {m['config_mappings']}")
    print(f"   DNA: {m['dna']}")
