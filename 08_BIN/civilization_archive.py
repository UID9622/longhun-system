#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·庚申·丙寅·未时·䷐随-CIVILIZATION-ARCHIVE-v1.1-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
🐉 龍魂 · DNA 文明档案馆 v1.1

为世界文明、历史事件、非遗技艺、古籍文献等提供不可篡改的 DNA 追溯存储：
  - 每份文明记录生成唯一 DNA 追溯码
  - SHA-256 内容哈希 + 哈希链（Chain of Hashes）防篡改
  - 多语言索引与跨文明关联
  - 支持文本、图片哈希、音视频指纹
  - 公开可查询，只存 DNA，不干涉文明本身

v1.1 新增:
  - 哈希链验证 (--verify)
  - 完整性报告 (--report)
  - 贵州云备份 (--backup --remote guizhou-cloud)

用法:
  python3 08_BIN/civilization_archive.py --demo
  python3 08_BIN/civilization_archive.py --store "活字印刷术" --civilization CN --tags 非遗,印刷
  python3 08_BIN/civilization_archive.py --serve
  python3 08_BIN/civilization_archive.py --verify
  python3 08_BIN/civilization_archive.py --report
  python3 08_BIN/civilization_archive.py --backup --remote guizhou-cloud
"""

import argparse
import hashlib
import json
import os
import platform
import shutil
import sqlite3
import subprocess
import tarfile
from datetime import datetime
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

ARCHIVE_DB = Path.home() / ".cnsh" / "civilization_archive.db"


def generate_dna(tag: str) -> str:
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S-%f")
    h = hashlib.md5(f"{tag}{ts}{UID}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{tag}-{h}-{UID}"


@dataclass
class CivilizationRecord:
    entry_id: str
    dna: str
    title: str
    content: str
    civilization: str  # CN, EU, IN, EG, GR 等文明代码
    category: str      # event, text, craft, oral, artifact, site
    tags: List[str]
    content_hash: str
    prev_hash: str     # 哈希链：指向前一条记录的 content_hash
    lang: str
    source: str
    created_at: str
    media_hashes: Dict[str, str]  # image_hash, audio_hash, video_hash
    metadata: Dict[str, any]


class CivilizationArchive:
    """DNA 文明档案馆"""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or ARCHIVE_DB
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self.dna = generate_dna("CIVILIZATION-ARCHIVE")

    def _init_db(self):
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS archive_records (
                    entry_id TEXT PRIMARY KEY,
                    dna TEXT UNIQUE,
                    title TEXT,
                    content TEXT,
                    civilization TEXT,
                    category TEXT,
                    tags TEXT,
                    content_hash TEXT,
                    prev_hash TEXT,
                    lang TEXT,
                    source TEXT,
                    created_at TEXT,
                    media_hashes TEXT,
                    metadata TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_civ ON archive_records(civilization)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_tag ON archive_records(tags)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_hash ON archive_records(content_hash)
            """)
            conn.commit()

    def _get_latest_hash(self) -> str:
        with sqlite3.connect(str(self.db_path)) as conn:
            row = conn.execute(
                "SELECT content_hash FROM archive_records ORDER BY created_at DESC LIMIT 1"
            ).fetchone()
            return row[0] if row else "0" * 64

    def store(
        self,
        title: str,
        content: str,
        civilization: str,
        category: str = "text",
        tags: Optional[List[str]] = None,
        lang: str = "zh",
        source: str = "manual",
        media_hashes: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict] = None
    ) -> CivilizationRecord:
        """存储一条文明记录"""
        tags = tags or []
        media_hashes = media_hashes or {}
        metadata = metadata or {}

        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        prev_hash = self._get_latest_hash()
        # 哈希链：把前一条哈希也混入当前记录哈希
        chain_hash = hashlib.sha256(f"{content_hash}:{prev_hash}".encode()).hexdigest()

        # entry_id 需全局唯一：混入微秒时间戳，避免并发/重复内容导致 UNIQUE 冲突
        ts_nonce = datetime.now().isoformat()
        entry_id = hashlib.sha256(f"{chain_hash}:{ts_nonce}".encode()).hexdigest()[:16]
        dna = generate_dna(f"CIV-{civilization}-{category}-{entry_id}")

        record = CivilizationRecord(
            entry_id=entry_id,
            dna=dna,
            title=title,
            content=content,
            civilization=civilization,
            category=category,
            tags=tags,
            content_hash=content_hash,
            prev_hash=prev_hash,
            lang=lang,
            source=source,
            created_at=datetime.now().isoformat(),
            media_hashes=media_hashes,
            metadata=metadata
        )

        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("""
                INSERT INTO archive_records
                (entry_id, dna, title, content, civilization, category, tags,
                 content_hash, prev_hash, lang, source, created_at, media_hashes, metadata)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                record.entry_id, record.dna, record.title, record.content,
                record.civilization, record.category, json.dumps(record.tags, ensure_ascii=False),
                record.content_hash, record.prev_hash, record.lang, record.source,
                record.created_at, json.dumps(record.media_hashes, ensure_ascii=False),
                json.dumps(record.metadata, ensure_ascii=False)
            ))
            conn.commit()

        return record

    def get(self, entry_id: str) -> Optional[CivilizationRecord]:
        with sqlite3.connect(str(self.db_path)) as conn:
            row = conn.execute(
                "SELECT * FROM archive_records WHERE entry_id=?", (entry_id,)
            ).fetchone()
            if not row:
                return None
            return self._row_to_record(row)

    def search(self, query: str, civilization: Optional[str] = None, top_k: int = 10) -> List[Dict]:
        """简单关键词检索"""
        with sqlite3.connect(str(self.db_path)) as conn:
            sql = "SELECT * FROM archive_records WHERE (title LIKE ? OR content LIKE ? OR tags LIKE ?)"
            params = [f"%{query}%", f"%{query}%", f"%{query}%"]
            if civilization:
                sql += " AND civilization=?"
                params.append(civilization)
            sql += " ORDER BY created_at DESC LIMIT ?"
            params.append(top_k)
            rows = conn.execute(sql, params).fetchall()
            return [asdict(self._row_to_record(r)) for r in rows]

    def verify_chain(self) -> Dict:
        """验证整个哈希链完整性"""
        with sqlite3.connect(str(self.db_path)) as conn:
            rows = conn.execute("SELECT * FROM archive_records ORDER BY created_at").fetchall()

        tampered = []
        prev = "0" * 64
        for row in rows:
            rec = self._row_to_record(row)
            if rec.prev_hash != prev:
                tampered.append({"entry_id": rec.entry_id, "reason": "prev_hash 不匹配"})
            expected = hashlib.sha256(rec.content.encode("utf-8")).hexdigest()
            if rec.content_hash != expected:
                tampered.append({"entry_id": rec.entry_id, "reason": "content_hash 不匹配"})
            # entry_id 现在是带时间戳的唯一句柄，不直接等于链式哈希截断
            # 链式完整性由 prev_hash 与 content_hash 共同保证
            prev = rec.content_hash

        return {
            "total": len(rows),
            "tampered": len(tampered),
            "integrity": "🟢 完整" if not tampered else "🔴 被篡改",
            "details": tampered,
            "dna": generate_dna("CHAIN-VERIFY")
        }

    def stats(self) -> Dict:
        with sqlite3.connect(str(self.db_path)) as conn:
            total = conn.execute("SELECT COUNT(*) FROM archive_records").fetchone()[0]
            by_civ = conn.execute("SELECT civilization, COUNT(*) FROM archive_records GROUP BY civilization").fetchall()
            by_cat = conn.execute("SELECT category, COUNT(*) FROM archive_records GROUP BY category").fetchall()
        return {
            "total": total,
            "by_civilization": {k: v for k, v in by_civ},
            "by_category": {k: v for k, v in by_cat},
            "dna": self.dna
        }

    def _row_to_record(self, row) -> CivilizationRecord:
        return CivilizationRecord(
            entry_id=row[0],
            dna=row[1],
            title=row[2],
            content=row[3],
            civilization=row[4],
            category=row[5],
            tags=json.loads(row[6]) if row[6] else [],
            content_hash=row[7],
            prev_hash=row[8],
            lang=row[9],
            source=row[10],
            created_at=row[11],
            media_hashes=json.loads(row[12]) if row[12] else {},
            metadata=json.loads(row[13]) if row[13] else {}
        )


# ═══════════════════════════════════════════════════════
# 备份与验证辅助函数
# ═══════════════════════════════════════════════════════

GUIZHOU_ICLOUD_DIR = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "龍魂系统备份" / "P0_文明DNA"
KUNPENG_HOST = "119.13.90.27"
KUNPENG_USER = "root"
KUNPENG_KEY = Path.home() / ".ssh" / "longhun_kunpeng_ed25519"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def gpg_encrypt_file(src: Path, dst: Path) -> bool:
    """用 UID9622 的 GPG 公钥加密文件（非对称，无需口令）"""
    try:
        subprocess.run(
            ["gpg", "--batch", "--yes", "--recipient", GPG_KEY,
             "--trust-model", "always", "--encrypt", "--output", str(dst), str(src)],
            check=True, capture_output=True, text=True
        )
        return True
    except Exception as e:
        print(f"  ❌ GPG 加密失败: {e}")
        return False


def run_ssh(cmd: str, timeout: int = 60) -> Tuple[int, str, str]:
    """在鲲鹏上执行命令"""
    key = KUNPENG_KEY if KUNPENG_KEY.exists() else None
    if not key:
        return 1, "", f"鲲鹏私钥不存在: {KUNPENG_KEY}"
    full = ["ssh", "-i", str(key), "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10",
            f"{KUNPENG_USER}@{KUNPENG_HOST}", cmd]
    r = subprocess.run(full, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def backup_to_guizhou_cloud(db_path: Path) -> Optional[Path]:
    """
    备份文明档案馆到贵州云（iCloud 云上贵州）。
    在 macOS 上：从鲲鹏拉取 DB → 加密 → 存 iCloud
    在 Linux 上：把本地 DB 复制到 /backup/guizhou_archive/ 待后续拉取
    """
    system = platform.system()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    manifest_id = f"CIVILIZATION_ARCHIVE_{ts}"

    if system == "Darwin":
        # macOS：从鲲鹏拉取并加密到 iCloud
        GUIZHOU_ICLOUD_DIR.mkdir(parents=True, exist_ok=True)
        work_dir = Path.home() / ".cnsh" / "archive_backup_work"
        work_dir.mkdir(parents=True, exist_ok=True)

        remote_db = f"/root/.cnsh/{db_path.name}"
        local_raw = work_dir / db_path.name

        print(f"🌐 从鲲鹏拉取 {remote_db}...")
        code, out, err = run_ssh(f"test -f {remote_db} && echo exists || echo missing", timeout=10)
        if code != 0 or "exists" not in out:
            print(f"❌ 鲲鹏上不存在 {remote_db}: {err}")
            return None

        scp_cmd = f"scp -i {KUNPENG_KEY} -o StrictHostKeyChecking=no -o ConnectTimeout=10 {KUNPENG_USER}@{KUNPENG_HOST}:{remote_db} {local_raw}"
        r = subprocess.run(scp_cmd, shell=True, capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            print(f"❌ scp 拉取失败: {r.stderr}")
            return None

        # 打包 DB + manifest
        tar_path = work_dir / f"{manifest_id}.tar"
        with tarfile.open(tar_path, "w") as tar:
            tar.add(local_raw, arcname=db_path.name)

        # 加密
        cipher_path = GUIZHOU_ICLOUD_DIR / f"{manifest_id}.tar.gpg"
        if not gpg_encrypt_file(tar_path, cipher_path):
            return None

        # 生成 manifest
        manifest = {
            "manifest_id": manifest_id,
            "dna": generate_dna("CIVILIZATION-BACKUP"),
            "confirm": CONFIRM,
            "created_at": datetime.now().isoformat(),
            "source_host": KUNPENG_HOST,
            "source_path": str(remote_db),
            "backup_type": "civilization_archive_to_guizhou_icloud",
            "cipher_file": str(cipher_path),
            "cipher_sha256": sha256_file(cipher_path),
            "db_sha256": sha256_file(local_raw),
            "size_bytes": cipher_path.stat().st_size,
        }
        manifest_path = GUIZHOU_ICLOUD_DIR / f"{manifest_id}.manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

        # 清理明文
        local_raw.unlink(missing_ok=True)
        tar_path.unlink(missing_ok=True)

        print(f"✅ 已备份到 iCloud 云上贵州: {cipher_path}")
        print(f"📄 Manifest: {manifest_path}")
        return cipher_path

    else:
        # Linux / 鲲鹏：复制到 /backup/guizhou_archive/ 等待 Mac 端拉取
        stage_dir = Path("/backup/guizhou_archive")
        stage_dir.mkdir(parents=True, exist_ok=True)
        dst = stage_dir / f"{manifest_id}_{db_path.name}"
        shutil.copy2(db_path, dst)

        manifest = {
            "manifest_id": manifest_id,
            "dna": generate_dna("CIVILIZATION-BACKUP-STAGE"),
            "confirm": CONFIRM,
            "created_at": datetime.now().isoformat(),
            "source_host": "localhost",
            "source_path": str(db_path),
            "backup_type": "civilization_archive_stage_for_guizhou",
            "staged_file": str(dst),
            "db_sha256": sha256_file(dst),
            "size_bytes": dst.stat().st_size,
        }
        manifest_path = stage_dir / f"{manifest_id}.manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"✅ 已暂存到 {dst}")
        print(f"📄 Manifest: {manifest_path}")
        print("💡 请在 Mac 上运行 backup_to_guizhou_cloud.py 拉取到 iCloud 云上贵州")
        return dst


def generate_integrity_report(arch: CivilizationArchive, out_dir: Path) -> Tuple[Path, Path]:
    """生成完整性报告（JSON + Markdown）"""
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    verify = arch.verify_chain()
    stats = arch.stats()

    report = {
        "dna": generate_dna("ARCHIVE-INTEGRITY"),
        "confirm": CONFIRM,
        "generated_at": datetime.now().isoformat(),
        "db_path": str(arch.db_path),
        "verify": verify,
        "stats": stats,
    }

    json_path = out_dir / f"archive_integrity_{ts}.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    md_path = out_dir / f"archive_integrity_{ts}.md"
    lines = [
        "# 🐉 龍魂 · DNA 文明档案馆完整性报告",
        "",
        f"**DNA:** `{report['dna']}`",
        f"**确认码:** `{report['confirm']}`",
        f"**生成时间:** {report['generated_at']}",
        f"**数据库:** `{report['db_path']}`",
        "",
        "## 🔗 哈希链验证",
        "",
        f"| 总记录 | 篡改数 | 完整性 |",
        f"|---:|---:|:---|",
        f"| {verify['total']} | {verify['tampered']} | {verify['integrity']} |",
        "",
        "## 📊 统计",
        "",
        f"| 总记录 | 文明数 | 类别数 |",
        f"|---:|---:|---:|",
        f"| {stats['total']} | {len(stats['by_civilization'])} | {len(stats['by_category'])} |",
        "",
        "### 按文明分布",
        "",
        "| 文明 | 数量 |",
        "|:---|---:|",
    ]
    for civ, cnt in sorted(stats['by_civilization'].items()):
        lines.append(f"| {civ} | {cnt} |")

    lines.extend(["", "### 按类别分布", "", "| 类别 | 数量 |", "|:---|---:|"])
    for cat, cnt in sorted(stats['by_category'].items()):
        lines.append(f"| {cat} | {cnt} |")

    lines.extend(["", "---", "", f"**DNA:** `{report['dna']}`", f"**确认码:** `{report['confirm']}`"])
    md_path.write_text("\n".join(lines), encoding="utf-8")

    return json_path, md_path


# ═══════════════════════════════════════════════════════
# FastAPI 服务
# ═══════════════════════════════════════════════════════

app = FastAPI(title="龍魂 DNA 文明档案馆 API", version="1.0")
archive = CivilizationArchive()


class StoreRequest(BaseModel):
    title: str
    content: str
    civilization: str
    category: str = "text"
    tags: Optional[List[str]] = None
    lang: str = "zh"
    source: str = "api"
    media_hashes: Optional[Dict[str, str]] = None
    metadata: Optional[Dict] = None


class SearchRequest(BaseModel):
    query: str
    civilization: Optional[str] = None
    top_k: int = 10


@app.post("/api/civilization/store")
def api_store(req: StoreRequest):
    rec = archive.store(
        title=req.title,
        content=req.content,
        civilization=req.civilization,
        category=req.category,
        tags=req.tags,
        lang=req.lang,
        source=req.source,
        media_hashes=req.media_hashes,
        metadata=req.metadata
    )
    return asdict(rec)


@app.get("/api/civilization/get/{entry_id}")
def api_get(entry_id: str):
    rec = archive.get(entry_id)
    if not rec:
        return {"error": "记录不存在"}
    return asdict(rec)


@app.post("/api/civilization/search")
def api_search(req: SearchRequest):
    return {"results": archive.search(req.query, req.civilization, req.top_k)}


@app.get("/api/civilization/verify")
def api_verify():
    return archive.verify_chain()


@app.get("/api/civilization/stats")
def api_stats():
    return archive.stats()


def demo():
    arch = CivilizationArchive()
    samples = [
        ("活字印刷术", "毕昇发明胶泥活字印刷，改变世界文明传播方式。", "CN", "craft", ["非遗", "印刷", "宋代"]),
        ("罗塞塔石碑", "刻有古埃及象形文字、世俗体与古希腊文，是文明解码钥匙。", "EG", "artifact", ["石碑", "多语言", "古埃及"]),
        ("敦煌莫高窟", "丝绸之路上的佛教艺术宝库，融合多民族文明。", "CN", "site", ["敦煌", "佛教", "壁画"]),
        ("汉谟拉比法典", "古巴比伦成文法典，刻于黑色玄武岩石柱。", "IQ", "text", ["法典", "古巴比伦", "法律"]),
        ("印度摩诃婆罗多", "古印度两大史诗之一，蕴含哲学、伦理与战争智慧。", "IN", "text", ["史诗", "印度", "哲学"]),
    ]
    for title, content, civ, cat, tags in samples:
        rec = arch.store(title, content, civ, category=cat, tags=tags, source="demo")
        print(f"🧬 {rec.dna} [{civ}] {title} → {rec.entry_id}")

    print("\n" + "=" * 70)
    print("📊 档案馆统计")
    print(json.dumps(arch.stats(), ensure_ascii=False, indent=2))

    print("\n🔍 搜索 '印刷'")
    for r in arch.search("印刷"):
        print(f"  [{r['civilization']}] {r['title']} ({r['entry_id']})")

    print("\n🔗 哈希链验证")
    print(json.dumps(arch.verify_chain(), ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · DNA 文明档案馆")
    parser.add_argument("--demo", action="store_true", help="运行示例")
    parser.add_argument("--store", type=str, help="存储标题")
    parser.add_argument("--content", type=str, default="", help="存储内容")
    parser.add_argument("--civilization", type=str, default="CN", help="文明代码")
    parser.add_argument("--category", type=str, default="text", help="类别")
    parser.add_argument("--tags", type=str, default="", help="标签，逗号分隔")
    parser.add_argument("--serve", action="store_true", help="启动 API 服务")
    parser.add_argument("--port", default=8853, type=int, help="API 端口")

    # v1.1 新增：验证/报告/备份
    parser.add_argument("--verify", action="store_true", help="验证哈希链完整性")
    parser.add_argument("--report", action="store_true", help="生成完整性报告")
    parser.add_argument("--export", action="store_true", help="与 --report 配合，导出报告到文件")
    parser.add_argument("--backup", action="store_true", help="执行备份")
    parser.add_argument("--remote", type=str, help="备份目标，如 guizhou-cloud")
    parser.add_argument("--output-dir", default="12_DOCS/agent_reports", help="报告输出目录")
    args = parser.parse_args()

    if args.serve:
        uvicorn.run(app, host="0.0.0.0", port=args.port)
    elif args.store:
        arch = CivilizationArchive()
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        rec = arch.store(args.store, args.content, args.civilization, args.category, tags=tags)
        print(json.dumps(asdict(rec), ensure_ascii=False, indent=2))
    elif args.verify:
        arch = CivilizationArchive()
        result = arch.verify_chain()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.report:
        arch = CivilizationArchive()
        if args.export:
            json_path, md_path = generate_integrity_report(arch, Path(args.output_dir))
            print(f"✅ 报告已导出:")
            print(f"   JSON: {json_path}")
            print(f"   Markdown: {md_path}")
        else:
            result = arch.verify_chain()
            stats = arch.stats()
            print(json.dumps({"verify": result, "stats": stats}, ensure_ascii=False, indent=2))
    elif args.backup:
        if args.remote == "guizhou-cloud":
            backup_to_guizhou_cloud(ARCHIVE_DB)
        else:
            print("❌ 请指定 --remote guizhou-cloud")
            print("   示例: python3 08_BIN/civilization_archive.py --backup --remote guizhou-cloud")
    else:
        demo()


if __name__ == "__main__":
    main()
