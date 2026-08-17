#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂系统 · 落地焊死引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·庚申·亥时-LANDING-ENGINE-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
描述: 知识→落地→执行 流水线引擎: scan 扫描未落地 → run 注入图谱+注册索引+生成骨架+冒烟 → dashboard 看板
协议: 01_protocols/LH-LANDING-PROTOCOL-v1.0.md
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ========== 路径焊死（路径铁律·不瞎猜） ==========
HOME = Path.home()
WORKSPACE = Path(__file__).resolve().parent.parent
KG_FILE = WORKSPACE / "data" / "knowledge_graph.json"
INDEX_FILE = HOME / ".longhun" / "cognitive_index.json"
CONV_DIRS = [
    HOME / ".longhun" / "03_MEMORY" / "ai_conversations",
    WORKSPACE / "03_MEMORY" / "ai_conversations",
]
SKILL_DIR = WORKSPACE / "03_MEMORY" / "landed_skills"
AUDIT_LOG = WORKSPACE / "audit_log.jsonl"

# 认知索引分类（现有结构）
INDEX_CATEGORY = "knowledge_nodes"


def _now() -> str:
    """ISO 本地时间"""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z")


def _dna8(content: str) -> str:
    """由内容生成 8 位 DNA 随机码"""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:8]


def _make_dna(tag: str, content: str) -> str:
    """生成标准 DNA: #龍芯⚡️干支四柱-标签-8位-UID9622"""
    return f"#龍芯⚡️丙午·丙申·庚申·亥时-{tag}-{_dna8(content)}-UID9622"


def _topic_of(data: dict) -> str:
    """提取主题，无则按来源兜底"""
    t = (data.get("topic") or "").strip()
    if not t:
        t = "未分类"
    return t[:40]


def _safe_slug(topic: str) -> str:
    """主题转文件名安全 slug"""
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "_", topic).strip("_")
    return s or "topic"


def iter_unlanded():
    """遍历所有对话 jsonl，产出 (file, line_no, data)；已落地跳过"""
    seen = set()
    for base in CONV_DIRS:
        if not base.exists():
            continue
        for f in sorted(base.rglob("*.jsonl")):
            if ".tmp" in str(f) or f.name.startswith("_"):
                continue
            key = str(f)
            if key in seen:
                continue
            seen.add(key)
            with open(f, "r", encoding="utf-8", errors="replace") as fp:
                for ln, line in enumerate(fp, 1):
                    try:
                        data = json.loads(line)
                    except Exception:
                        continue
                    content = (data.get("content") or "").strip()
                    if not content:
                        continue
                    if data.get("landed"):
                        continue
                    yield f, ln, data


def scan(limit: int = None) -> list:
    """扫描未落地知识"""
    found = []
    for f, ln, data in iter_unlanded():
        found.append({
            "source": str(f),
            "line": ln,
            "content": data.get("content", "")[:200],
            "dna": data.get("dna", ""),
            "topic": _topic_of(data),
        })
        if limit and len(found) >= limit:
            break
    return found


def load_kg() -> dict:
    if KG_FILE.exists():
        with open(KG_FILE, "r", encoding="utf-8") as fp:
            return json.load(fp)
    return {"entities": {}, "relations": []}


def save_kg(kg: dict):
    KG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(KG_FILE, "w", encoding="utf-8") as fp:
        json.dump(kg, fp, indent=2, ensure_ascii=False)


def load_index() -> dict:
    if INDEX_FILE.exists():
        with open(INDEX_FILE, "r", encoding="utf-8") as fp:
            return json.load(fp)
    return {}


def save_index(index: dict):
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    index["updated_at"] = _now()
    with open(INDEX_FILE, "w", encoding="utf-8") as fp:
        json.dump(index, fp, indent=2, ensure_ascii=False)


def audit(dna: str, action: str, result: str, details: str = ""):
    """审计日志 append-only"""
    entry = {
        "timestamp": _now(),
        "level": "INFO",
        "module": "landing_engine",
        "action": action,
        "dna": dna,
        "result": result,
        "details": details,
    }
    with open(AUDIT_LOG, "a", encoding="utf-8") as fp:
        fp.write(json.dumps(entry, ensure_ascii=False) + "\n")


def gen_skill_skeleton(topic: str, content: str) -> Path:
    """规则3: 立即生成骨架代码，不说'待实现'"""
    SKILL_DIR.mkdir(parents=True, exist_ok=True)
    slug = _safe_slug(topic)
    target = SKILL_DIR / f"landed_{slug}.py"
    if target.exists():
        return target
    dna = _make_dna("LANDED-SKILL", content[:500])
    header = (
        "#!/usr/bin/env python3\n"
        "# -*- coding: utf-8 -*-\n"
        "'''\n"
        "🐉 龍魂系统 · 落地骨架 · " + topic + "\n"
        "DNA: " + dna + "\n"
        "确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z\n"
        "License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)\n"
        "来源知识: 自动落地流水线生成（规则3: 不说'待实现'）\n"
        "'''\n\n\n"
        "def run():\n"
        "    '''骨架入口: 由后续迭代填充具体能力'''\n"
        "    return {'status': 'landed', 'topic': " + json.dumps(topic, ensure_ascii=False) + "}\n\n\n"
        "if __name__ == '__main__':\n"
        "    print(run())\n"
    )
    target.write_text(header, encoding="utf-8")
    return target


def smoke_test(target: Path) -> bool:
    """冒烟测试: 骨架可执行"""
    try:
        r = subprocess.run(
            [sys.executable, str(target)],
            capture_output=True, text=True, timeout=15,
        )
        return r.returncode == 0
    except Exception:
        return False


def land_one(f, ln, data, dry_run: bool = False, smoke: bool = False) -> dict:
    """落地单条知识"""
    content = (data.get("content") or "").strip()
    topic = _topic_of(data)

    # 生成落地 DNA + 节点 ID
    landed_dna = _make_dna("LANDED", content[:500])
    node_id = f"knowledge_{_dna8(content[:500])}"

    # 1. 注入知识图谱
    kg = load_kg()
    entities = kg.setdefault("entities", {})
    relations = kg.setdefault("relations", [])
    if node_id not in entities:
        entities[node_id] = {
            "type": "knowledge",
            "name": topic,
            "properties": {
                "source": str(f),
                "dna": landed_dna,
                "landed_at": _now(),
                "status": "active",
                "content": content[:500],
            },
        }
        relations.append([node_id, f"knowledge_src_{_dna8(str(f))}", "landed_from"])
    if not dry_run:
        save_kg(kg)

    # 2. 注册认知索引
    index = load_index()
    kn = index.setdefault(INDEX_CATEGORY, [])
    if not any(x.get("id") == node_id for x in kn):
        kn.append({
            "id": node_id,
            "title": topic,
            "dna": landed_dna,
            "path": str(f),
            "landed_at": _now(),
        })
    if not dry_run:
        save_index(index)

    # 3. 生成骨架代码（规则3: 不说待实现）
    skill_path = gen_skill_skeleton(topic, content) if not dry_run else None
    smoke_ok = None
    if skill_path and smoke:
        smoke_ok = smoke_test(skill_path)

    # 4. 标记已落地（回写 jsonl）
    if not dry_run:
        data["landed"] = True
        data["landed_at"] = _now()
        data["landed_dna"] = landed_dna
        data["node_id"] = node_id
        with open(f, "r", encoding="utf-8") as fp:
            lines = fp.readlines()
        lines[ln - 1] = json.dumps(data, ensure_ascii=False) + "\n"
        with open(f, "w", encoding="utf-8") as fp:
            fp.writelines(lines)
        # 5. 审计入史
        audit(landed_dna, "land_知识落地", "成功", f"topic={topic} node={node_id}")

    return {
        "topic": topic,
        "node_id": node_id,
        "landed_dna": landed_dna,
        "skill": str(skill_path) if skill_path else None,
        "smoke": smoke_ok,
        "dry_run": dry_run,
    }


def run_pipeline(dry_run: bool = False, limit: int = None, smoke: bool = False) -> dict:
    """执行落地流水线"""
    total = landed = failed = 0
    results = []
    for f, ln, data in iter_unlanded():
        if limit and total >= limit:
            break
        total += 1
        try:
            r = land_one(f, ln, data, dry_run=dry_run, smoke=smoke)
            results.append(r)
            landed += 1
        except Exception as e:
            failed += 1
            results.append({"topic": _topic_of(data), "error": str(e)})
    return {"total": total, "landed": landed, "failed": failed, "results": results}


def dashboard() -> dict:
    """落地看板: 统计 总/已落地/已索引/未落地"""
    all_cnt = 0
    landed_cnt = 0
    seen = set()
    for base in CONV_DIRS:
        if not base.exists():
            continue
        for f in sorted(base.rglob("*.jsonl")):
            if ".tmp" in str(f) or f.name.startswith("_"):
                continue
            key = str(f)
            if key in seen:
                continue
            seen.add(key)
            with open(f, "r", encoding="utf-8", errors="replace") as fp:
                for line in fp:
                    try:
                        d = json.loads(line)
                    except Exception:
                        continue
                    if not (d.get("content") or "").strip():
                        continue
                    all_cnt += 1
                    if d.get("landed"):
                        landed_cnt += 1
    kg = load_kg()
    index = load_index()
    indexed = len(index.get(INDEX_CATEGORY, []))
    return {
        "total": all_cnt,
        "landed": landed_cnt,
        "indexed": indexed,
        "unlanded": all_cnt - landed_cnt,
        "kg_nodes": len(kg.get("entities", {})),
    }


def print_dashboard(d: dict):
    print("\n🐉 落地看板")
    print("=" * 50)
    print(f"  📚 总知识数:  {d['total']}")
    print(f"  ✅ 已落地:    {d['landed']}")
    print(f"  🧠 已索引:    {d['indexed']}")
    print(f"  ⏳ 未落地:    {d['unlanded']}")
    print(f"  🧬 图谱节点:  {d['kg_nodes']}")
    if d["unlanded"] > 0:
        print("\n  ⚠️ 有未落地的知识，运行: lh landing")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(
        prog="lh landing",
        description="🐉 落地焊死引擎: 知识→落地→执行",
    )
    sub = parser.add_subparsers(dest="cmd")

    p_scan = sub.add_parser("scan", help="扫描未落地知识")
    p_scan.add_argument("--limit", type=int, default=10)

    p_run = sub.add_parser("run", help="执行落地流水线")
    p_run.add_argument("--limit", type=int, default=None)
    p_run.add_argument("--dry-run", action="store_true", help="预演不写盘")
    p_run.add_argument("--smoke", action="store_true", help="冒烟测试骨架")

    sub.add_parser("dashboard", help="落地看板")

    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    if args.cmd == "scan":
        found = scan(limit=args.limit)
        if args.json:
            print(json.dumps({"unlanded": found}, ensure_ascii=False, indent=2))
            return
        print(f"\n📋 找到 {len(found)} 条未落地的知识")
        for item in found:
            print(f"  - [{item['topic']}] {item['content'][:50]}...")
        return

    if args.cmd == "run":
        r = run_pipeline(dry_run=args.dry_run, limit=args.limit, smoke=args.smoke)
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
            return
        print(f"\n🏗️ 落地流水线: 处理 {r['total']} 条, 落地 {r['landed']} 条, 失败 {r['failed']} 条"
              + ("（预演·未写盘）" if args.dry_run else ""))
        for item in r["results"][:8]:
            status = "✅" if "node_id" in item else "❌"
            print(f"  {status} [{item.get('topic', '?')}] → {item.get('node_id', item.get('error', ''))}")
        if r["landed"]:
            print(f"\n  🧬 骨架代码: {SKILL_DIR}/landed_*.py")
            print("  🧠 已注册认知索引 + 注入知识图谱 + 审计入史")
        return

    if args.cmd == "dashboard":
        d = dashboard()
        if args.json:
            print(json.dumps(d, ensure_ascii=False, indent=2))
            return
        print_dashboard(d)
        return

    # 默认: 全流程 scan → run → dashboard
    found = scan(limit=99999)
    print(f"\n📋 扫描: 找到 {len(found)} 条未落地知识")
    r = run_pipeline(dry_run=False, limit=None, smoke=True)
    print(f"\n🏗️ 落地: 处理 {r['total']} 条, 落地 {r['landed']} 条, 失败 {r['failed']} 条")
    d = dashboard()
    print_dashboard(d)


if __name__ == "__main__":
    main()
