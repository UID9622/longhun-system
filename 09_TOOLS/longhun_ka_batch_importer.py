#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Kimi_Agent 批量提炼脚本
把 Kimi_Agent 目录中所有含龍魂/UID9622/DNA 标记的 .py/.md/.skill 文件
导入 dragon_knowledge.db 并注册到 manifest.json
DNA: #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-KIMI-AGENT-BATCH-IMPORT-v1.0
"""

import hashlib
import json
import re
import sqlite3
import zipfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Any

HOME = Path.home()
KA_DIR = HOME / "Downloads" / "Kimi_Agent"
DB_PATH = HOME / "_work" / "dragon_knowledge.db"
MANIFEST_PATH = HOME / "longhun-system" / "agents" / "manifest.json"
SKILLS_DIR = HOME / ".kimi-code" / "skills"
WORK_DIR = Path("/tmp") / "longhun_ka_batch_work"
WORK_DIR.mkdir(parents=True, exist_ok=True)

CST = timezone(timedelta(hours=8))
DNA_SIGNATURE = "#龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-KIMI-AGENT-BATCH-IMPORT-v1.0"

SENSITIVE_DOMAINS = {
    "github.com", "gitlab.com", "bitbucket.org",
    "huggingface.co", "openai.com", "anthropic.com",
    "google.com", "microsoft.com", "amazon.com",
    "twitter.com", "x.com", "facebook.com", "meta.com",
}


def now_iso():
    return datetime.now(CST).isoformat()


def sha256_short(text: str, length=16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def sha256_full(data) -> str:
    if isinstance(data, bytes):
        return hashlib.sha256(data).hexdigest()
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def extract_meta(text: str, filename: str) -> Dict[str, Any]:
    """从文件头提取元数据"""
    meta = {
        "dna": "",
        "version": "",
        "description": "",
        "author": "",
        "title": filename,
    }
    # DNA
    dna_match = re.search(r'#龍芯[⚡️][^\s\n]+', text)
    if dna_match:
        meta["dna"] = dna_match.group(0)
    # 版本
    ver_match = re.search(r'v(\d+\.\d+(?:\.\d+)?)', text[:2000])
    if ver_match:
        meta["version"] = ver_match.group(1)
    # 描述：取前 5 行非空注释/文本
    lines = []
    for line in text.split('\n')[:30]:
        line = line.strip()
        if line.startswith('#') or line.startswith('//'):
            cleaned = line.lstrip('#').lstrip('/').strip()
            if cleaned and len(cleaned) > 5:
                lines.append(cleaned)
        elif line and not line.startswith('```') and len(lines) < 3:
            if len(line) > 10:
                lines.append(line)
    if lines:
        meta["description"] = " | ".join(lines[:3])[:200]
    # 作者
    if "UID9622" in text:
        meta["author"] = "UID9622"
    return meta


def compute_bloodline_score(text: str) -> int:
    """
    血脉识别：判断文件内容是否属于龍魂体系。
    不依赖显式 DNA/UID 标记，而是读内容语义。
    """
    strong_markers = [
        "龍魂", "龍芯", "CNSH", "UID9622", "君子协议", "DNA", "河图洛书",
        "易经", "太极", "五行", "八卦", "六十四卦", "洛书", "通心译",
        "longhun", "LongHun", "德者永生殿", "铁律", "主权",
        "魂灵", "星闪", "鸿蒙", "北斗", "龍芯", "数字人", "曾老师",
    ]
    weak_markers = [
        "python", "script", "module", "skill", "知识库", "协议", "规范",
        "审计", "追溯", "检查", "引擎", "计算", "公式", "算法",
    ]
    score = 0
    text_lower = text.lower()
    for m in strong_markers:
        if m.lower() in text_lower:
            score += 3
    for m in weak_markers:
        if m.lower() in text_lower:
            score += 1
    return score


def dragon_shield_check(file_path: Path, text: str) -> Dict[str, Any]:
    """
    龍盾检查 v2：内容血脉识别。
    Kimi_Agent 目录是老大私产，默认读内容认血脉，不因缺少 DNA/UID 就熔断。
    """
    has_dna = bool(re.search(r'#龍芯[⚡️][^\s\n]+', text))
    dna_match = re.search(r'#龍芯[⚡️][^\s\n]+', text)
    has_uid = "UID9622" in text
    has_junzi = "君子协议" in text or "君子" in text
    bloodline = compute_bloodline_score(text)
    
    sensitive_urls = []
    for domain in SENSITIVE_DOMAINS:
        if domain in text:
            sensitive_urls.append(domain)
    
    checks = {
        "dna": {"passed": has_dna, "detail": dna_match.group(0) if dna_match else "内容未显式标注 DNA，但经血脉识别认可"},
        "sovereignty": {"passed": has_uid or bloodline >= 3, "detail": "含 UID9622" if has_uid else f"血脉分 {bloodline}，判定为 UID9622 私产"},
        "junzi": {"passed": has_junzi or bloodline >= 3, "detail": "含君子协议" if has_junzi else "内容属龍魂体系，默认受君子协议约束"},
        "bloodline": {"passed": bloodline >= 3, "detail": f"血脉识别分 {bloodline}"},
        "external_url": {"passed": len(sensitive_urls) == 0, "detail": f"发现外网域名: {sensitive_urls}" if sensitive_urls else "未发现敏感外网域名"},
    }
    
    # 有敏感外网域名且非龍魂强关联 → 红
    if sensitive_urls and bloodline < 6:
        level = "RED"
        passed = False
    elif bloodline < 3:
        # 完全看不出龍魂血脉 → 红
        level = "RED"
        passed = False
    elif has_dna and has_uid and not sensitive_urls:
        level = "GREEN"
        passed = True
    else:
        level = "YELLOW"
        passed = True
    
    return {"passed": passed, "level": level, "checks": checks}


def init_tables(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ka_files (
            entry_id TEXT PRIMARY KEY,
            file_path TEXT UNIQUE,
            file_name TEXT,
            file_hash TEXT,
            file_size INTEGER,
            module_id TEXT,
            title TEXT,
            description TEXT,
            version TEXT,
            dna_code TEXT,
            author TEXT,
            shield_level TEXT,
            shield_passed INTEGER,
            content_snippet TEXT,
            imported_at TEXT
        )
    """)
    conn.commit()


def load_existing_hashes(conn: sqlite3.Connection) -> set[str]:
    cursor = conn.cursor()
    cursor.execute("SELECT file_hash FROM ka_files")
    return {row[0] for row in cursor.fetchall()}


def load_manifest() -> Dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {"version": "1.0.0", "agents": [], "dna": ""}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(manifest: Dict[str, Any]):
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def register_file_in_manifest(manifest: Dict[str, Any], rel_path: str, meta: Dict[str, Any], shield: Dict[str, Any]) -> bool:
    agent_id = rel_path.replace('/', '-').replace(' ', '_').replace('.', '_')
    for a in manifest.get("agents", []):
        if a.get("id") == agent_id:
            return False
    
    agent = {
        "id": agent_id,
        "name": meta["title"],
        "file_name": rel_path,
        "layer": "L3",
        "type": "knowledge_file",
        "version": meta["version"],
        "description": meta["description"],
        "dna": meta["dna"] or DNA_SIGNATURE,
        "source": "Kimi_Agent",
        "shield_level": shield["level"],
        "registered_at": now_iso(),
    }
    manifest.setdefault("agents", []).append(agent)
    
    # 升级版本号
    version = manifest.get("version", "1.0.0")
    try:
        major, minor = version.rsplit(".", 1)
        manifest["version"] = f"{major}.{int(minor) + 1}"
    except ValueError:
        manifest["version"] = "1.1.0"
    manifest["last_updated"] = now_iso()
    manifest["dna"] = f"#龍芯⚡️{datetime.now(CST).strftime('%Y-%m-%d')}-AGENT-MANIFEST-{manifest['version']}"
    return True


def main():
    print("🐉 龍魂 · Kimi_Agent 批量提炼\n")
    print(f"来源: {KA_DIR}")
    print(f"数据库: {DB_PATH}")
    print(f"Manifest: {MANIFEST_PATH}\n")
    
    # 收集文件
    files: List[Path] = []
    for f in KA_DIR.rglob('*'):
        if not f.is_file():
            continue
        if f.suffix not in ('.py', '.md', '.skill'):
            continue
        if '__pycache__' in str(f):
            continue
        # 忽略已处理的 skill bundle（由 knowledge_manager 处理）
        if f.suffix == '.skill' and (SKILLS_DIR / f.stem).exists():
            continue
        files.append(f)
    
    print(f"扫描到 {len(files)} 个待处理文件\n")
    
    conn = sqlite3.connect(DB_PATH)
    init_tables(conn)
    existing_hashes = load_existing_hashes(conn)
    manifest = load_manifest()
    
    imported = 0
    skipped = 0
    rejected = 0
    shield_summary = {"GREEN": 0, "YELLOW": 0, "RED": 0}
    
    for f in files:
        try:
            content = f.read_bytes()
            text = content.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"⚠️ 读取失败 {f}: {e}")
            continue
        
        file_hash = sha256_full(content)
        if file_hash in existing_hashes:
            skipped += 1
            continue
        
        rel = f.relative_to(KA_DIR).as_posix()
        meta = extract_meta(text, f.name)
        shield = dragon_shield_check(f, text)
        shield_summary[shield["level"]] += 1
        
        if not shield["passed"]:
            rejected += 1
            print(f"🔴 拒绝: {rel} ({shield['level']})")
            continue
        
        # 写入 DB
        entry_id = f"KA-{sha256_short(rel)}-{file_hash[:8]}"
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ka_files (entry_id, file_path, file_name, file_hash, file_size,
                                  module_id, title, description, version, dna_code, author,
                                  shield_level, shield_passed, content_snippet, imported_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            entry_id,
            str(f),
            f.name,
            file_hash,
            len(content),
            f.parent.name,
            meta["title"],
            meta["description"],
            meta["version"],
            meta["dna"],
            meta["author"],
            shield["level"],
            1 if shield["passed"] else 0,
            text[:500].replace('\x00', ''),
            now_iso(),
        ))
        conn.commit()
        
        # 注册 manifest
        register_file_in_manifest(manifest, rel, meta, shield)
        imported += 1
        print(f"✅ 导入: {rel} ({shield['level']})")
    
    save_manifest(manifest)
    conn.close()
    
    print(f"\n=== 批量提炼完成 ===")
    print(f"扫描文件: {len(files)}")
    print(f"新增导入: {imported}")
    print(f"跳过重复: {skipped}")
    print(f"龍盾拒绝: {rejected}")
    print(f"龍盾统计: 🟢{shield_summary['GREEN']} 🟡{shield_summary['YELLOW']} 🔴{shield_summary['RED']}")
    print(f"Manifest 版本: {manifest['version']}")
    print(f"Manifest agents 总数: {len(manifest['agents'])}")
    print(f"\nDNA: {DNA_SIGNATURE}")


if __name__ == "__main__":
    main()
