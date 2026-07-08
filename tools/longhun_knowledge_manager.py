#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂知识库管理器 · Knowledge Manager v1.1

专门用于：
1. 扫描外部目录（如 Kimi_Agent）中的技能/知识库模块
2. 与现有龍魂体系去重对比（目录名 + 内容哈希）
3. 龍盾主权防火墙检查（DNA / 君子协议 / 外网 URL）
4. 清洗并写入 dragon_knowledge.db
5. 安装新增技能到 ~/.kimi-code/skills/
6. 注册到 longhun-system/agents/manifest.json
7. 生成提炼报告 + 龍盾审计日志

DNA: #龍芯⚡️2026-06-26-LONGHUN-KNOWLEDGE-MANAGER-v1.1
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sqlite3
import sys
import zipfile
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HOME = Path.home()
DEFAULT_DB = HOME / "_work" / "dragon_knowledge.db"
DEFAULT_KA = HOME / "Downloads" / "Kimi_Agent"
SKILLS_DIR = HOME / ".kimi-code" / "skills"
AGENTS_DIR = HOME / "longhun-system" / "agents"
MANIFEST_PATH = AGENTS_DIR / "manifest.json"
DRAGON_SHIELD_AUDIT_PATH = HOME / "dragon_soul" / "audit" / "harvester_audit.jsonl"

CST = timezone(timedelta(hours=8))

DNA_SIGNATURE = "#龍芯⚡️2026-06-26-LONGHUN-KNOWLEDGE-MANAGER-v1.1"

# 明显不是技能包的目录
IGNORE_DIRS = {"__pycache__", "checkpoints", "logs", "CNSH", "longhun_mvp_reviewed",
               "zeng-extraction", "longhun-v5-skills", "龍魂日记本-iOS"}

# 龍盾：敏感外网域名白名单检查
SENSITIVE_DOMAINS = {
    "github.com", "gitlab.com", "bitbucket.org",
    "huggingface.co", "openai.com", "anthropic.com",
    "google.com", "microsoft.com", "amazon.com",
    "twitter.com", "x.com", "facebook.com", "meta.com",
}


def now_iso() -> str:
    return datetime.now(CST).isoformat()


def sha256_short(text: str, length: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def sha256_full(data) -> str:
    if isinstance(data, bytes):
        return hashlib.sha256(data).hexdigest()
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def clean_text(t) -> str:
    return "" if t is None else str(t).strip()


@dataclass
class SkillMeta:
    name: str
    source_name: str
    source_path: Path
    skill_type: str  # 'skill_bundle' | 'skill_dir'
    version: str = ""
    description: str = ""
    dna: str = ""
    triggers: str = ""
    license: str = ""
    author: str = ""
    content_hash: str = ""
    local_skill_path: Optional[Path] = None


@dataclass
class DragonShieldResult:
    passed: bool
    level: str  # GREEN / YELLOW / RED
    checks: Dict[str, Dict]
    dna: str


def compute_directory_hash(path: Path) -> str:
    """计算目录内容哈希：遍历所有非忽略文件，按路径排序后拼接 SHA256"""
    if not path.exists():
        return ""
    hashes = []
    for f in sorted(path.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(path).as_posix()
        if "__pycache__" in rel or rel.endswith(".pyc") or rel.startswith("."):
            continue
        h = sha256_full(f.read_bytes())
        hashes.append(f"{rel}:{h}")
    return sha256_full("\n".join(hashes))


def extract_yaml_frontmatter(text: str) -> Dict[str, str]:
    """简易提取 SKILL.md 的 YAML frontmatter"""
    result: Dict[str, str] = {}
    if not text.startswith("---"):
        return result
    end = text.find("---", 3)
    if end == -1:
        return result
    fm = text[3:end]
    for key in ["name", "description", "dna", "version", "license", "author"]:
        # 支持顶层字段或 metadata 嵌套字段（如 metadata.dna）
        m = re.search(rf"^\s*{key}:\s*\"?(.+?)\"?$", fm, re.MULTILINE)
        if m:
            result[key] = m.group(1).strip().strip('"')
    m = re.search(r"triggers:\n((?:  - .+\n)+)", fm)
    if m:
        result["triggers"] = ", ".join(line.strip("- ") for line in m.group(1).strip().split("\n"))
    return result


def extract_skill_meta(path: Path, work_dir: Path) -> Optional[SkillMeta]:
    """提取 .skill bundle 或目录的元数据，并计算内容哈希"""
    if path.suffix == ".skill" and zipfile.is_zipfile(path):
        extract_dir = work_dir / path.stem
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        try:
            with zipfile.ZipFile(path, "r") as z:
                z.extractall(extract_dir)
        except Exception as e:
            print(f"⚠️ 解压失败 {path}: {e}")
            return None
        source_path = extract_dir
        skill_type = "skill_bundle"
    elif path.is_dir():
        source_path = path
        skill_type = "skill_dir"
    else:
        return None

    skill_md = source_path / "SKILL.md"
    if not skill_md.exists():
        for f in source_path.rglob("SKILL.md"):
            skill_md = f
            break

    name = path.stem
    description = ""
    version = ""
    dna = ""
    triggers = ""
    license_str = ""
    author = ""

    if skill_md.exists():
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
        fm = extract_yaml_frontmatter(text)
        name = fm.get("name", name)
        description = fm.get("description", "")
        version = fm.get("version", "")
        dna = fm.get("dna", "")
        triggers = fm.get("triggers", "")
        license_str = fm.get("license", "")
        author = fm.get("author", "")

    content_hash = compute_directory_hash(source_path)

    return SkillMeta(
        name=name,
        source_name=path.name,
        source_path=source_path,
        skill_type=skill_type,
        version=version,
        description=description,
        dna=dna,
        triggers=triggers,
        license=license_str,
        author=author,
        content_hash=content_hash,
    )


def discover_ka_modules(ka_dir: Path, work_dir: Path) -> List[SkillMeta]:
    """扫描外部目录中的潜在技能模块。
    支持两种结构：
    1. ka_dir 本身是技能目录（含 SKILL.md）
    2. ka_dir 是父目录，内含多个技能子目录 / .skill bundle
    """
    discovered: List[SkillMeta] = []

    # 情况1：来源目录本身就是技能包
    if (ka_dir / "SKILL.md").exists():
        meta = extract_skill_meta(ka_dir, work_dir)
        if meta:
            return [meta]

    # 情况2：来源目录内含多个技能包
    for f in sorted(ka_dir.glob("*.skill")):
        meta = extract_skill_meta(f, work_dir)
        if meta:
            discovered.append(meta)

    for d in sorted(ka_dir.iterdir()):
        if d.is_dir() and d.name not in IGNORE_DIRS and not d.name.endswith(".zip"):
            if (d / "SKILL.md").exists():
                meta = extract_skill_meta(d, work_dir)
                if meta:
                    discovered.append(meta)

    return discovered


def load_existing_skills() -> set:
    """加载现有技能名称"""
    existing = set()
    for base in [SKILLS_DIR, HOME / ".agents" / "skills"]:
        if base.exists():
            for d in base.iterdir():
                if d.is_dir():
                    existing.add(d.name)
    return existing


def hash_exists_in_db(conn: sqlite3.Connection, content_hash: str) -> bool:
    """检查内容哈希是否已在知识库 harvested_code 中存在"""
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM harvested_code WHERE content_hash = ? LIMIT 1", (content_hash,))
    return cursor.fetchone() is not None


def dragon_shield_check(source_path: Path, meta: SkillMeta) -> DragonShieldResult:
    """
    龍盾主权防火墙检查。
    返回 GREEN（通过）/ YELLOW（警告）/ RED（熔断）
    """
    checks: Dict[str, Dict] = {}
    level = "GREEN"

    # 1. DNA 追溯检查
    has_dna = bool(meta.dna) and meta.dna.startswith("#")
    checks["dna_trace"] = {
        "name": "DNA追溯检查",
        "passed": has_dna,
        "detail": f"DNA: {meta.dna}" if has_dna else "未找到有效 DNA 追溯码",
    }
    if not has_dna:
        level = "RED"

    # 2. 君子协议 / 六层来源链检查
    skill_md = source_path / "SKILL.md"
    md_text = ""
    if skill_md.exists():
        md_text = skill_md.read_text(encoding="utf-8", errors="ignore")
    has_zijun = "君子协议" in md_text or "Zijun Protocol" in md_text
    has_source_chain = "六层来源链" in md_text or "Source Chain" in md_text
    checks["sovereignty_protocol"] = {
        "name": "君子协议/来源链检查",
        "passed": has_zijun or has_source_chain,
        "detail": f"君子协议: {has_zijun}, 六层来源链: {has_source_chain}",
    }
    if not (has_zijun or has_source_chain):
        if level != "RED":
            level = "YELLOW"

    # 3. 作者/主权归属检查
    has_uid = "UID9622" in (meta.author + meta.dna + md_text)
    checks["owner_identity"] = {
        "name": "主权归属检查",
        "passed": has_uid or bool(meta.author),
        "detail": f"作者: {meta.author}, 含 UID9622: {has_uid}",
    }

    # 4. 敏感外网 URL 检查
    found_domains = set()
    if source_path.exists():
        for f in source_path.rglob("*"):
            if not f.is_file():
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                for domain in SENSITIVE_DOMAINS:
                    if domain in text:
                        found_domains.add(domain)
            except Exception:
                continue
    checks["external_url"] = {
        "name": "外网敏感域名检查",
        "passed": len(found_domains) == 0,
        "detail": f"发现域名: {sorted(found_domains)}" if found_domains else "未发现敏感外网域名",
    }
    if found_domains and level == "GREEN":
        level = "YELLOW"

    passed = level != "RED"
    dna = f"#龍芯⚡️{datetime.now(CST).strftime('%Y-%m-%d')}-DRAGON-SHIELD-{level}-{sha256_short(meta.name + meta.content_hash, 8)}"

    return DragonShieldResult(passed=passed, level=level, checks=checks, dna=dna)


def write_dragon_shield_audit(meta: SkillMeta, shield: DragonShieldResult, action: str) -> None:
    """写入龍盾审计日志"""
    DRAGON_SHIELD_AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": now_iso(),
        "dna": shield.dna,
        "module": meta.name,
        "content_hash": meta.content_hash,
        "action": action,
        "shield_level": shield.level,
        "shield_passed": shield.passed,
        "checks": shield.checks,
        "manager_dna": DNA_SIGNATURE,
    }
    with DRAGON_SHIELD_AUDIT_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def init_kb_tables(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_modules (
            module_id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            name TEXT NOT NULL,
            version TEXT,
            description TEXT,
            dna_code TEXT,
            triggers TEXT,
            license TEXT,
            author TEXT,
            extracted_at TEXT NOT NULL,
            entry_count INTEGER DEFAULT 0,
            metadata_json TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_entries (
            entry_id TEXT PRIMARY KEY,
            module_id TEXT NOT NULL,
            entry_type TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT,
            subcategory TEXT,
            status TEXT,
            priority TEXT,
            summary TEXT,
            content_json TEXT,
            tags TEXT,
            dna_code TEXT,
            source_path TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(module_id) REFERENCES knowledge_modules(module_id)
        )
    """)
    for idx in ["idx_ke_module", "idx_ke_category", "idx_ke_status", "idx_ke_tags"]:
        cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx} ON knowledge_entries(module_id, category, status, tags)")
    conn.commit()


def upsert_module(conn: sqlite3.Connection, meta: SkillMeta, entry_count: int, metadata: Dict) -> None:
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO knowledge_modules
        (module_id, source, name, version, description, dna_code, triggers, license, author, extracted_at, entry_count, metadata_json)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        meta.name,
        "Kimi_Agent",
        meta.name,
        meta.version,
        meta.description,
        meta.dna,
        meta.triggers,
        meta.license,
        meta.author,
        now_iso(),
        entry_count,
        json.dumps(metadata, ensure_ascii=False),
    ))
    conn.commit()


def insert_entries(conn: sqlite3.Connection, module_id: str, entries: List[Dict]) -> int:
    cursor = conn.cursor()
    inserted = 0
    for item in entries:
        title = clean_text(item.get("title", item.get("专栏标题", item.get("知识点名称", ""))))
        if not title:
            continue
        uid = sha256_short(title + json.dumps(item, sort_keys=True, ensure_ascii=False))
        entry_id = f"{module_id}-{uid}"
        content = {k: clean_text(v) for k, v in item.items()}
        cursor.execute("""
            INSERT OR REPLACE INTO knowledge_entries
            (entry_id, module_id, entry_type, title, category, subcategory, status, priority, summary, content_json, tags, dna_code, source_path, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            entry_id,
            module_id,
            item.get("entry_type", "entry"),
            title,
            clean_text(item.get("category", item.get("领域分类", ""))),
            clean_text(item.get("subcategory", item.get("子分类", ""))),
            clean_text(item.get("status", item.get("学习状态", ""))),
            clean_text(item.get("priority", item.get("重要程度", item.get("学习优先级", "")))),
            clean_text(item.get("summary", item.get("一句话摘要", item.get("描述", "")))),
            json.dumps(content, ensure_ascii=False),
            clean_text(item.get("tags", item.get("内容标签", ""))),
            clean_text(item.get("dna_code", item.get("DNA追溯码", item.get("短DNA·身份码", "")))),
            clean_text(item.get("source_path", "")),
            now_iso(),
        ))
        inserted += 1
    conn.commit()
    return inserted


def import_json_kb(module_id: str, json_path: Path, field_mapping: Dict[str, str]) -> Tuple[int, List[Dict]]:
    """通用 JSON 知识库导入"""
    if not json_path.exists():
        return 0, []
    data = json.loads(json_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return 0, []

    entries = []
    for raw in data:
        entry = dict(field_mapping)
        entry["source_path"] = str(json_path)
        for src_key, dst_key in [
            ("专栏标题", "title"), ("知识点名称", "title"), ("title", "title"),
            ("领域分类", "category"), ("分类", "category"),
            ("子分类", "subcategory"),
            ("状态", "status"), ("学习状态", "status"),
            ("重要程度", "priority"), ("学习优先级", "priority"), ("importance", "priority"),
            ("一句话摘要", "summary"), ("描述", "summary"), ("summary", "summary"),
            ("内容标签", "tags"), ("tags", "tags"),
            ("DNA追溯码", "dna_code"), ("短DNA·身份码", "dna_code"),
        ]:
            if src_key in raw and dst_key in entry and not entry[dst_key]:
                entry[dst_key] = raw[src_key]
        for k, v in raw.items():
            if k not in entry:
                entry[k] = v
        entries.append(entry)

    return len(entries), entries


def register_in_manifest(meta: SkillMeta, keywords: List[str], entrypoint: Path) -> bool:
    """注册到 manifest.json"""
    if not MANIFEST_PATH.exists():
        print(f"⚠️ manifest.json 不存在: {MANIFEST_PATH}")
        return False

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    agents = manifest.get("agents", [])

    existing_idx = next((i for i, a in enumerate(agents) if a.get("id") == meta.name), -1)
    agent = {
        "id": meta.name,
        "name": meta.name.replace("longhun-", "").replace("-", " ").title(),
        "layer": "L2",
        "type": "on-demand",
        "logic": "知识检索逻辑" if "knowledge" in meta.name else "索引导航逻辑",
        "keywords": keywords,
        "persona_code": f"P-{meta.name.replace('longhun-', '').replace('-', '_').upper()}",
        "entrypoint": str(entrypoint),
        "skill_path": str(SKILLS_DIR / meta.name),
        "description": meta.description[:120],
        "dna": meta.dna or DNA_SIGNATURE,
        "content_hash": meta.content_hash,
    }

    if existing_idx >= 0:
        # 保留旧 DNA 链，升级版本
        old_agent = agents[existing_idx]
        agent["previous_dna"] = old_agent.get("dna", "")
        agent["upgraded_at"] = now_iso()
        agents[existing_idx] = agent
        print(f"  🔄 升级 manifest 中已有条目")
        manifest_changed = True
    else:
        last_l2 = -1
        for i, a in enumerate(agents):
            if a.get("layer") == "L2":
                last_l2 = i
        insert_idx = last_l2 + 1 if last_l2 >= 0 else len(agents)
        agents.insert(insert_idx, agent)
        manifest_changed = True

    version = manifest.get("version", "1.0.0")
    try:
        major, minor = version.rsplit(".", 1)
        manifest["version"] = f"{major}.{int(minor) + 1}"
    except ValueError:
        manifest["version"] = "1.1.0"

    manifest["dna"] = f"#龍芯⚡️{datetime.now(CST).strftime('%Y-%m-%d')}-AGENT-MANIFEST-{manifest['version']}"
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return True


def install_skill(source: Path, target: Path) -> None:
    """安装技能到 .kimi-code/skills/"""
    if target.exists():
        # 备份旧版本
        backup = target.parent / f"{target.name}.backup.{datetime.now(CST).strftime('%Y%m%d_%H%M%S')}"
        shutil.copytree(target, backup)
        shutil.rmtree(target)
    if source.is_dir():
        shutil.copytree(source, target)
    else:
        raise ValueError(f"source must be a directory: {source}")


def generate_report(db_path: Path, output_dir: Path, discovered: List[SkillMeta], imported: List[str], shield_results: List[Dict]) -> Path:
    """生成提炼报告"""
    output_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT module_id, COUNT(*) as cnt FROM knowledge_entries GROUP BY module_id")
    stats = cursor.fetchall()
    conn.close()

    timestamp = datetime.now(CST).strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f'knowledge_import_report_{timestamp}.md'

    lines = [
        f"# 🐉 龍魂知识库提炼报告 · {timestamp}",
        f"\n**DNA**: `{DNA_SIGNATURE}`",
        f"**生成时间**: {now_iso()}",
        f"**来源目录**: {DEFAULT_KA}",
        f"**目标数据库**: {db_path}",
        f"\n> 本报告由龍魂知识库管理器生成，所有数据本地存储，含龍盾主权防火墙审计。",
        "\n## 一、扫描发现",
        f"\n发现潜在模块: {len(discovered)} 个",
        "\n| 模块名 | 类型 | 版本 | DNA | 内容哈希 |",
        "|--------|------|------|-----|----------|",
    ]
    for m in discovered:
        lines.append(f"| {m.name} | {m.skill_type} | {m.version} | `{m.dna}` | `{m.content_hash[:16]}...` |")

    lines.extend([
        "\n## 二、龍盾主权防火墙审计",
        f"\n已执行安全审计: {len(shield_results)} 个模块",
        "\n| 模块 | 结果 | 等级 | DNA检查 | 君子协议 | 主权归属 | 外网URL |",
        "|------|------|------|---------|----------|----------|---------|",
    ])
    for s in shield_results:
        checks = s["checks"]
        lines.append(
            f"| {s['module']} | {'通过' if s['passed'] else '熔断'} | {s['level']} | "
            f"{'✅' if checks.get('dna_trace', {}).get('passed') else '❌'} | "
            f"{'✅' if checks.get('sovereignty_protocol', {}).get('passed') else '⚠️'} | "
            f"{'✅' if checks.get('owner_identity', {}).get('passed') else '⚠️'} | "
            f"{'✅' if checks.get('external_url', {}).get('passed') else '⚠️'} |"
        )

    lines.extend([
        "\n## 三、已导入模块",
        f"\n已导入/升级: {len(imported)} 个",
        "\n| 模块 | 条目数 |",
        "|------|--------|",
    ])
    for row in stats:
        lines.append(f"| {row['module_id']} | {row['cnt']} |")

    lines.extend([
        "\n## 四、数据库状态",
        f"\n- knowledge_modules: {len(discovered)} 条",
        f"- knowledge_entries: {sum(r['cnt'] for r in stats)} 条",
        f"- 龍盾审计日志: {DRAGON_SHIELD_AUDIT_PATH}",
        "\n---",
        "*本报告由龍魂知识库管理器自动生成，数据全部本地存储，不上传。*",
    ])

    report_path.write_text('\n'.join(lines), encoding='utf-8')
    return report_path


def cmd_import(args):
    """导入命令"""
    ka_dir = Path(args.source) if args.source else DEFAULT_KA
    db_path = Path(args.db) if args.db else DEFAULT_DB
    work_dir = Path(args.work_dir) if args.work_dir else Path("/tmp") / "longhun_kb_work"
    work_dir.mkdir(parents=True, exist_ok=True)

    print(f"🐉 龍魂知识库管理器 v1.1")
    print(f"来源: {ka_dir}")
    print(f"数据库: {db_path}\n")

    existing = load_existing_skills()
    discovered = discover_ka_modules(ka_dir, work_dir)

    new_modules = [m for m in discovered if m.name not in existing]
    print(f"扫描发现 {len(discovered)} 个模块，其中新增 {len(new_modules)} 个")

    conn = sqlite3.connect(db_path)
    init_kb_tables(conn)

    imported: List[str] = []
    shield_results: List[Dict] = []

    kb_configs = {
        "longhun-cn-innovation-knowledge-base": {
            "json": ka_dir / "longhun-cn-innovation-kb" / "scripts" / "cn_innovation_kb.json",
            "entry_type": "column_article",
            "keywords": ["中国科技", "自主创新", "卡脖子技术", "国产替代", "科技自立自强", "新质生产力", "顶刊论文"],
        },
        "longhun-cs-knowledge-base": {
            "json": ka_dir / "longhun-cs-kb" / "scripts" / "cs_kb_complete.json",
            "entry_type": "cs_card",
            "keywords": ["计算机科学", "CS知识库", "知识卡片", "技术决策", "架构设计"],
        },
        "longhun-notion-portal": {
            "json": ka_dir / "longhun-notion-portal" / "scripts" / "notion_portal.json",
            "entry_type": "notion_page",
            "keywords": ["Notion整理", "Notion入口", "Notion导航", "空间治理", "页面归档"],
        },
    }

    for meta in new_modules:
        print(f"\n📦 处理: {meta.name}")
        print(f"  内容哈希: {meta.content_hash[:16]}...")

        # 1. 哈希碰撞检测
        if hash_exists_in_db(conn, meta.content_hash):
            print(f"  ⏭️ 内容哈希已存在，跳过（完全相同副本）")
            write_dragon_shield_audit(meta, DragonShieldResult(
                passed=True, level="GREEN", checks={"duplicate": {"passed": True, "detail": "内容哈希已存在，判定为重复导入"}},
                dna=DNA_SIGNATURE
            ), "SKIPPED_DUPLICATE")
            continue

        # 2. 龍盾主权防火墙
        shield = dragon_shield_check(meta.source_path, meta)
        shield_results.append({"module": meta.name, **asdict(shield)})
        write_dragon_shield_audit(meta, shield, "CHECKED")
        print(f"  🛡️ 龍盾: {shield.level} ({'通过' if shield.passed else '熔断'})")
        for check_name, check_result in shield.checks.items():
            icon = "✅" if check_result["passed"] else "⚠️" if shield.level == "YELLOW" else "❌"
            print(f"    {icon} {check_result['name']}: {check_result['detail'][:60]}")

        if not shield.passed:
            print(f"  🔴 龍盾熔断，拒绝导入")
            continue

        # 3. 数据导入
        config = kb_configs.get(meta.name)
        if not config:
            print(f"  ⚠️ 暂无可识别的 JSON 数据配置，跳过数据导入")
            continue

        count, entries = import_json_kb(meta.name, config["json"], {"entry_type": config["entry_type"]})
        if count == 0:
            print(f"  ⚠️ 未找到数据文件: {config['json']}")
            continue

        insert_entries(conn, meta.name, entries)
        upsert_module(conn, meta, count, {"source_path": str(config["json"]), "content_hash": meta.content_hash})

        # 4. 安装到 skills 目录（含旧版本备份）
        # 对于 .skill bundle，meta.source_path 已是解压后的目录
        source_dir = meta.source_path
        target_dir = SKILLS_DIR / meta.name
        install_skill(source_dir, target_dir)
        print(f"  ✅ 安装到: {target_dir}")

        # 5. 注册/升级 manifest
        registered = register_in_manifest(meta, config["keywords"], config["json"])
        if registered:
            print(f"  ✅ 注册/升级 manifest.json")

        imported.append(meta.name)

    conn.close()

    # 生成报告
    report_path = generate_report(db_path, AGENTS_DIR / "reports", discovered, imported, shield_results)
    print(f"\n📝 报告已生成: {report_path}")
    print(f"\n✅ 导入完成: {len(imported)} 个模块")
    print(f"🛡️ 龍盾审计: {DRAGON_SHIELD_AUDIT_PATH}")


def cmd_list(args):
    """列出知识库模块"""
    db_path = Path(args.db) if args.db else DEFAULT_DB
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM knowledge_modules ORDER BY extracted_at DESC")
    rows = cursor.fetchall()
    print(f"{'模块ID':<45} {'版本':<8} {'条目数':<8} {'DNA':<40}")
    print("-" * 110)
    for r in rows:
        print(f"{r['module_id']:<45} {r['version']:<8} {r['entry_count']:<8} {r['dna_code']:<40}")
    conn.close()


def cmd_search(args):
    """搜索知识条目"""
    db_path = Path(args.db) if args.db else DEFAULT_DB
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT module_id, title, category, status, summary
        FROM knowledge_entries
        WHERE title LIKE ? OR summary LIKE ? OR tags LIKE ?
        ORDER BY module_id, title
        LIMIT ?
    """, (f"%{args.query}%", f"%{args.query}%", f"%{args.query}%", args.limit or 20))
    rows = cursor.fetchall()
    print(f"搜索 '{args.query}' 找到 {len(rows)} 条结果:\n")
    for r in rows:
        print(f"[{r['module_id']}] {r['title']} ({r['category']})")
        if r['summary']:
            print(f"  {r['summary'][:120]}...")
        print()
    conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂知识库管理器：扫描、清洗、导入外部知识模块（含龍盾防火墙）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--db", help="知识库 SQLite 路径", default=str(DEFAULT_DB))
    parser.add_argument("--source", help="外部来源目录（默认 Kimi_Agent）", default=str(DEFAULT_KA))
    parser.add_argument("--work-dir", help="临时工作目录")

    sub = parser.add_subparsers(dest="command", required=True)

    p_import = sub.add_parser("import", help="扫描并导入新增模块")
    p_import.set_defaults(func=cmd_import)

    p_list = sub.add_parser("list", help="列出已导入模块")
    p_list.set_defaults(func=cmd_list)

    p_search = sub.add_parser("search", help="搜索知识条目")
    p_search.add_argument("query", help="搜索关键词")
    p_search.add_argument("--limit", type=int, default=20, help="返回数量上限")
    p_search.set_defaults(func=cmd_search)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
