#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·LU压缩引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-LU压缩-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：一颗钻石11切面，一条能跑的压缩链，本地回填规则，DNA双签。
人话：把任何长东西压成四样——①一页看懂 ②机器能解析 ③短码能召回 ④未来能复现

核心能力：
  1. 压缩链 — 吞入→分流→翻译→压缩→归类→判分→封条→压缩率→归档→召回→固化→对外
  2. 短码生成 — 一喊就跑
  3. DNA双签 — 不可篡改
  4. 时间胶囊 — 阶段封存
  5. 本地回填 — 一条条对齐
"""

import os
import sys
import re
import json
import hashlib
import sqlite3
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
import argparse
import uuid

# ============================================================
# 一、配置与常量
# ============================================================

BASE_DIR = Path.home() / ".longhun/lu_compressor"
BASE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = BASE_DIR / "lu_registry.db"
CAPSULE_DIR = BASE_DIR / "capsules"
CAPSULE_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR = BASE_DIR / "archive"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
TEMPORAL_DIR = BASE_DIR / "temporal"
TEMPORAL_DIR.mkdir(parents=True, exist_ok=True)

CONFIG = {
    "version": "1.0",
    "dna": "#龍芯⚡️丙午·乙未·甲辰·离为火-LU压缩-v1.0",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
    "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "compression_levels": ["轻量", "标准", "深度"],
    "wuxing": ["金", "木", "水", "火", "土"],
    "guas": ["乾", "坤", "屯", "蒙", "需", "讼", "师", "比"],
}

# 短码表（从核心引擎抽出）
SHORTCODES = {
    "/全文压缩": "把长内容压成结构卡",
    "/旧文回收": "把旧对话/旧页面/旧草稿变成可召回资产",
    "/归集": "自动分到语义抽屉 + 八卦分区 + 项目模块",
    "/DNA封装": "生成DNA、版本、来源、状态",
    "/投喂净化": "去废话、去重复、去噪音，保留原创语义",
    "/系统入库": "写入龙魂/CNSH规则库或知识库",
    "/封存归档": "旧版本封存，不污染当前系统",
    "/召回": "用短码恢复旧内容核心，不重复投喂全文",
    "/时间胶囊": "把某阶段封成未来可复现包",
}

# 11切面对齐表
FACETS = {
    "核心引擎": {"page": "LU全文压缩归集器 v1.1", "phase": "主干·贯穿全链"},
    "计算骨架": {"page": "计算公式对准表 v1.5", "phase": "步⑥ 三色+收口判定"},
    "公式母册": {"page": "龙魂数学公式总册 v1.0", "phase": "步⑧ 算压缩率"},
    "协议层": {"page": "CNSH语义接入规范 v2.0", "phase": "步⑦ DNA封条 + 步⑨ 归档"},
    "前置翻译": {"page": "通心译×CNSH-DOC主干 v1.0", "phase": "步③ 先翻译"},
    "五行归类": {"page": "五行计算器 v1.0", "phase": "步⑤ 五行归类"},
    "资产固化": {"page": "Web3-DNA记忆主权交易算法 v8.0", "phase": "步⑪ 量子态固化"},
    "来源追溯": {"page": "Behavioral Cryptography v1.1", "phase": "步⑦ 封条·认证位"},
    "入口安全": {"page": "窗口加密护盾 v1.7", "phase": "步② 分流脱敏"},
    "公开边界": {"page": "个人创作IP公开索引 v1.1", "phase": "步⑫ 对外·时间优先"},
    "跨窗口召回": {"page": "宝宝系统 v1.3", "phase": "步⑩ 短码召回"},
}

# ============================================================
# 二、数据结构
# ============================================================

@dataclass
class CompressionResult:
    """压缩结果"""
    id: str
    original_content: str
    compressed_content: str
    title: str
    summary: str
    wuxing: str
    gua: str
    shortcode: str
    dna: str
    confirm: str
    seal: str
    compression_ratio: float
    tags: List[str]
    source: str
    created_at: str
    status: str  # active, archived, temporal
    facet: str
    gpg: str

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# ============================================================
# 三、核心压缩引擎
# ============================================================

class LUCompressor:
    """LU压缩引擎 — 一颗钻石11切面，一条能跑的压缩链"""

    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()
        self.facet_alignments = []

    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS capsules (
                id TEXT PRIMARY KEY,
                original_content TEXT,
                compressed_content TEXT,
                title TEXT,
                summary TEXT,
                wuxing TEXT,
                gua TEXT,
                shortcode TEXT,
                dna TEXT,
                confirm TEXT,
                seal TEXT,
                compression_ratio REAL,
                tags TEXT,
                source TEXT,
                created_at TEXT,
                status TEXT,
                facet TEXT,
                gpg TEXT,
                version TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS temporal_capsules (
                id TEXT PRIMARY KEY,
                capsule_id TEXT,
                freeze_date TEXT,
                reason TEXT,
                restored_at TEXT,
                notes TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS alignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                local_file TEXT,
                facet TEXT,
                aligned_at TEXT,
                status TEXT,
                notes TEXT
            )
        """)
        conn.commit()
        conn.close()

    # ---------- 步① 吞入 ----------
    def ingest(self, content: str, source: str = "manual") -> Dict:
        """吞入原始内容"""
        return {
            "content": content,
            "source": source,
            "length": len(content),
            "lines": len(content.split('\n')),
            "timestamp": datetime.now().isoformat()
        }

    # ---------- 步② 分流脱敏 ----------
    def sanitize(self, content: str) -> str:
        """简单脱敏 — 移除敏感模式"""
        # 移除邮箱
        content = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '[EMAIL]', content)
        # 移除手机号（中国）
        content = re.sub(r'1[3-9]\d{9}', '[PHONE]', content)
        # 移除身份证
        content = re.sub(r'\d{17}[\dXx]', '[ID]', content)
        return content

    # ---------- 步③ 先翻译（简化版）----------
    def translate(self, content: str) -> str:
        """简化翻译 — 实际应调用通心译"""
        # 保留原样，标记已处理
        return content

    # ---------- 步④ 压缩 ----------
    def compress(self, content: str, title: str = "") -> Dict:
        """五步归集法压缩"""
        if len(content) < 100:
            return {"compressed": content, "summary": content, "preserved": True,
                    "original_length": len(content), "compressed_length": len(content)}

        # 1. 去噪：移除多余空白和重复
        cleaned = re.sub(r'\s+', ' ', content)
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)

        # 2. 提取骨架：保留首段 + 每段首句
        paragraphs = content.split('\n\n')
        skeleton = []
        for p in paragraphs[:5]:
            if p.strip():
                # 取每段第一句
                first_sentence = p.split('。')[0] + '。' if '。' in p else p[:100]
                skeleton.append(first_sentence)

        # 3. 提取关键句（含核心词）
        core_keywords = ['核心', '关键', '目标', '结论', '建议', '风险', '决策', '协议']
        key_sentences = []
        for line in content.split('\n'):
            if any(kw in line for kw in core_keywords):
                key_sentences.append(line[:100])

        # 4. 构建压缩版
        compressed_parts = []
        if title:
            compressed_parts.append(f"# {title}")
        compressed_parts.append("\n## 摘要")
        compressed_parts.append(' '.join(skeleton[:3]))
        compressed_parts.append("\n## 关键点")
        compressed_parts.extend([f"- {s}" for s in key_sentences[:5]])
        compressed_parts.append("\n## 原文本")
        compressed_parts.append(content[:500] + "..." if len(content) > 500 else content)

        compressed = '\n'.join(compressed_parts)
        summary = skeleton[0][:200] if skeleton else content[:200]

        return {
            "compressed": compressed,
            "summary": summary,
            "preserved": len(compressed) < len(content),
            "original_length": len(content),
            "compressed_length": len(compressed)
        }

    # ---------- 步⑤ 五行归类 ----------
    def classify_wuxing(self, content: str) -> str:
        """按关键词归类五行"""
        wuxing_keywords = {
            "金": ["规则", "审计", "边界", "裁决", "安全", "法律", "宪法", "主权"],
            "木": ["成长", "创新", "扩展", "学习", "开发", "构建", "设计"],
            "水": ["记忆", "追溯", "存储", "档案", "历史", "记录", "DNA"],
            "火": ["表达", "创作", "传播", "价值", "文明", "宣传", "品牌"],
            "土": ["承载", "普惠", "基础", "民生", "容器", "平台", "根基"]
        }

        scores = {w: 0 for w in wuxing_keywords}
        for w, keywords in wuxing_keywords.items():
            for kw in keywords:
                scores[w] += content.count(kw) * 2
                if kw in content:
                    scores[w] += 1

        return max(scores, key=scores.get) if max(scores.values()) > 0 else "土"

    # ---------- 步⑥ 三色+收口判定 ----------
    def audit(self, content: str, wuxing: str) -> Dict:
        """三色审计 + 守恒分数"""
        # 简单评分
        score = 0
        score += len(content) / 100 * 0.1
        score += content.count('。') / 10 * 0.2
        score += min(content.count('核心'), 5) * 0.2
        score += min(content.count('关键'), 5) * 0.2
        score = min(1.0, score)

        if score >= 0.7:
            color = "🟢"
            action = "收口"
        elif score >= 0.4:
            color = "🟡"
            action = "待补"
        else:
            color = "🔴"
            action = "截链·封存"

        return {
            "score": round(score, 3),
            "color": color,
            "action": action,
            "wuxing": wuxing
        }

    # ---------- 步⑦ DNA封条+双签 ----------
    def seal(self, content: str, title: str) -> Dict:
        """DNA双签"""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-LU压缩-{content_hash}"
        confirm = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
        seal = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
        gpg = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

        return {
            "dna": dna,
            "confirm": confirm,
            "seal": seal,
            "gpg": gpg,
            "hash": content_hash,
            "timestamp": timestamp
        }

    # ---------- 步⑧ 算压缩率 ----------
    def compression_ratio(self, original_len: int, compressed_len: int) -> float:
        """计算压缩率 F23 ρ = 1 - 压缩后/原始"""
        if original_len == 0:
            return 0.0
        return round(1 - compressed_len / original_len, 4)

    # ---------- 步⑨ 归档两层仓 ----------
    def archive(self, result: Dict) -> Dict:
        """归档：PAGE（人看）+ ROUTE（机器找）"""
        capsule_id = f"capsule_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{result.get('hash', uuid.uuid4().hex[:8])}"

        # 人看层
        page_path = CAPSULE_DIR / f"{capsule_id}_page.md"
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(f"""
# {result.get('title', '压缩胶囊')}

**ID:** {capsule_id}
**DNA:** {result.get('dna')}
**CONFIRM:** {result.get('confirm')}
**SEAL:** {result.get('seal')}
**GPG:** {result.get('gpg')}
**五行:** {result.get('wuxing')}
**卦:** {result.get('gua')}
**压缩率:** {result.get('compression_ratio')}
**时间:** {datetime.now().isoformat()}

## 摘要
{result.get('summary')}

## 压缩内容
{result.get('compressed_content')}

## 短码召回
{result.get('shortcode')}
""")

        # 机器层
        route_path = CAPSULE_DIR / f"{capsule_id}_route.json"
        with open(route_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        return {
            "capsule_id": capsule_id,
            "page_path": str(page_path),
            "route_path": str(route_path)
        }

    # ---------- 步⑩ 短码召回 ----------
    def generate_shortcode(self, content: str) -> str:
        """生成短码"""
        shortcode = f"/{hashlib.md5(content[:100].encode()).hexdigest()[:6]}"
        return shortcode

    def recall(self, shortcode: str) -> Optional[Dict]:
        """短码召回"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("""
            SELECT * FROM capsules WHERE shortcode = ?
        """, (shortcode,))
        row = cur.fetchone()
        conn.close()

        if row:
            return {
                "id": row[0],
                "original_content": row[1],
                "compressed_content": row[2],
                "title": row[3],
                "summary": row[4],
                "wuxing": row[5],
                "gua": row[6],
                "shortcode": row[7],
                "dna": row[8],
                "compression_ratio": row[11],
                "tags": row[12].split(',') if row[12] else [],
                "source": row[13],
                "created_at": row[14],
                "status": row[15],
                "facet": row[16]
            }
        return None

    # ---------- 步⑪ 量子态固化 ----------
    def quantum_seal(self, capsule_id: str) -> Dict:
        """量子态固化 — 算一次焊死"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            UPDATE capsules SET status = 'quantum_sealed'
            WHERE id = ?
        """, (capsule_id,))
        conn.commit()
        conn.close()

        return {
            "capsule_id": capsule_id,
            "status": "quantum_sealed",
            "timestamp": datetime.now().isoformat(),
            "note": "已固化，不重复重算"
        }

    # ---------- 步⑫ 对外·时间优先索引 ----------
    def generate_index(self) -> Dict:
        """生成对外索引（按时间降序）"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("""
            SELECT id, title, summary, dna, created_at, compression_ratio
            FROM capsules
            WHERE status = 'quantum_sealed'
            ORDER BY created_at DESC
            LIMIT 100
        """)
        rows = cur.fetchall()
        conn.close()

        return {
            "total": len(rows),
            "timestamp": datetime.now().isoformat(),
            "entries": [
                {
                    "id": r[0],
                    "title": r[1],
                    "summary": r[2][:200],
                    "dna": r[3],
                    "created_at": r[4],
                    "compression_ratio": r[5]
                }
                for r in rows
            ]
        }

    # ---------- 完整压缩链 ----------
    def run_chain(self, content: str, title: str = "", source: str = "manual") -> Dict:
        """
        完整压缩链：吞入→分流→翻译→压缩→归类→判分→封条→压缩率→归档→召回→固化→对外
        """
        print(f"\n🐉 LU压缩链启动: {title or '未命名'}")
        print("-" * 40)

        # ① 吞入
        print("  ① 吞入...")
        ingested = self.ingest(content, source)

        # ② 分流脱敏
        print("  ② 脱敏...")
        sanitized = self.sanitize(ingested["content"])

        # ③ 翻译
        print("  ③ 翻译...")
        translated = self.translate(sanitized)

        # ④ 压缩
        print("  ④ 压缩...")
        compressed_result = self.compress(translated, title)

        # ⑤ 五行归类
        print("  ⑤ 五行归类...")
        wuxing = self.classify_wuxing(compressed_result["compressed"])

        # ⑥ 三色+收口判定
        print("  ⑥ 三色审计...")
        audit_result = self.audit(compressed_result["compressed"], wuxing)

        if audit_result["action"] == "截链·封存":
            print(f"  🔴 截链: {audit_result['color']} 分数{audit_result['score']}")
            return {
                "status": "截链",
                "audit": audit_result,
                "message": "内容质量不足，已封存等待确认"
            }

        # ⑦ DNA封条
        print("  ⑦ DNA封条...")
        seal_result = self.seal(compressed_result["compressed"], title)

        # ⑧ 算压缩率
        print("  ⑧ 计算压缩率...")
        ratio = self.compression_ratio(
            compressed_result["original_length"],
            compressed_result["compressed_length"]
        )

        # ⑨ 短码生成
        print("  ⑨ 生成短码...")
        shortcode = self.generate_shortcode(compressed_result["compressed"])

        # ⑩ 归档
        print("  ⑩ 归档...")
        capsule_id = (f"capsule_{datetime.now().strftime('%Y%m%d_%H%M%S')}_"
                      f"{seal_result['hash']}")

        result = {
            "id": capsule_id,
            "original_content": content[:10000],
            "compressed_content": compressed_result["compressed"],
            "title": title or "未命名压缩",
            "summary": compressed_result["summary"],
            "wuxing": wuxing,
            "gua": "乾",  # 简化
            "shortcode": shortcode,
            "dna": seal_result["dna"],
            "confirm": seal_result["confirm"],
            "seal": seal_result["seal"],
            "gpg": seal_result["gpg"],
            "compression_ratio": ratio,
            "tags": ["压缩", wuxing],
            "source": source,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "facet": "核心引擎",
            "version": CONFIG["version"]
        }

        # 存储到数据库
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT OR REPLACE INTO capsules
            (id, original_content, compressed_content, title, summary,
             wuxing, gua, shortcode, dna, confirm, seal,
             compression_ratio, tags, source, created_at, status, facet, gpg, version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result["id"],
            result["original_content"],
            result["compressed_content"],
            result["title"],
            result["summary"],
            result["wuxing"],
            result["gua"],
            result["shortcode"],
            result["dna"],
            result["confirm"],
            result["seal"],
            result["compression_ratio"],
            ",".join(result["tags"]),
            result["source"],
            result["created_at"],
            result["status"],
            result["facet"],
            result["gpg"],
            result["version"]
        ))
        conn.commit()
        conn.close()

        # 归档
        archive_result = self.archive(result)

        # ⑪ 量子态固化
        print("  ⑪ 量子态固化...")
        quantum_result = self.quantum_seal(capsule_id)
        result["quantum_seal"] = quantum_result

        print("-" * 40)
        print(f"✅ 压缩完成!")
        print(f"  🧬 DNA: {result['dna']}")
        print(f"  📌 短码: {result['shortcode']}")
        print(f"  📊 压缩率: {result['compression_ratio']:.2%}")
        if archive_result.get('page_path'):
            print(f"  🗂️ 归档: {archive_result['page_path']}")

        return result

    # ---------- 本地回填规则 ----------
    def align_local(self, local_file: str, facet: str, notes: str = "") -> Dict:
        """本地回填 — 一条条对齐"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT INTO alignments (local_file, facet, aligned_at, status, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (
            local_file,
            facet,
            datetime.now().isoformat(),
            "🟢已对齐",
            notes
        ))
        conn.commit()
        conn.close()

        return {
            "local_file": local_file,
            "facet": facet,
            "status": "🟢已对齐",
            "timestamp": datetime.now().isoformat()
        }

    def get_alignments(self) -> List[Dict]:
        """获取对齐状态"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("""
            SELECT * FROM alignments ORDER BY aligned_at DESC
        """)
        rows = cur.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "local_file": r[1],
                "facet": r[2],
                "aligned_at": r[3],
                "status": r[4],
                "notes": r[5]
            }
            for r in rows
        ]

    # ---------- 时间胶囊 ----------
    def create_temporal_capsule(self, capsule_id: str, reason: str = "阶段封存") -> Dict:
        """创建时间胶囊"""
        capsule_file = TEMPORAL_DIR / f"{capsule_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT * FROM capsules WHERE id = ?", (capsule_id,))
        row = cur.fetchone()
        conn.close()

        if not row:
            return {"error": "胶囊不存在"}

        capsule_data = {
            "capsule_id": capsule_id,
            "freeze_date": datetime.now().isoformat(),
            "reason": reason,
            "data": {
                "id": row[0],
                "title": row[3],
                "summary": row[4],
                "dna": row[8],
                "created_at": row[14]
            }
        }

        with open(capsule_file, 'w', encoding='utf-8') as f:
            json.dump(capsule_data, f, ensure_ascii=False, indent=2)

        # 更新状态
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            UPDATE capsules SET status = 'temporal'
            WHERE id = ?
        """, (capsule_id,))
        conn.commit()
        conn.close()

        return {
            "capsule_id": capsule_id,
            "status": "temporal",
            "freeze_date": datetime.now().isoformat(),
            "file": str(capsule_file)
        }

    def restore_temporal(self, capsule_id: str) -> Dict:
        """恢复时间胶囊"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            UPDATE capsules SET status = 'active'
            WHERE id = ?
        """, (capsule_id,))
        conn.commit()
        conn.close()

        return {
            "capsule_id": capsule_id,
            "status": "active",
            "restored_at": datetime.now().isoformat()
        }


# ============================================================
# 四、命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·LU压缩引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 压缩一段内容
  python3 lh_lu_compressor.py compress "长文本内容" --title "我的思考"

  # 从文件压缩
  python3 lh_lu_compressor.py compress-file ./my_notes.md --title "旧笔记"

  # 短码召回
  python3 lh_lu_compressor.py recall /abc123

  # 本地回填对齐
  python3 lh_lu_compressor.py align ./local_note.md --facet "五行归类" --notes "已完成"

  # 查看对齐状态
  python3 lh_lu_compressor.py align-status

  # 创建时间胶囊
  python3 lh_lu_compressor.py temporal create --id capsule_xxx --reason "阶段封存"

  # 恢复时间胶囊
  python3 lh_lu_compressor.py temporal restore --id capsule_xxx

  # 生成对外索引
  python3 lh_lu_compressor.py index

  # 查看短码表
  python3 lh_lu_compressor.py shortcodes
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # compress
    comp_parser = subparsers.add_parser("compress", help="压缩内容")
    comp_parser.add_argument("content", type=str, help="要压缩的内容")
    comp_parser.add_argument("--title", type=str, default="", help="标题")
    comp_parser.add_argument("--source", type=str, default="manual", help="来源")

    # compress-file
    file_parser = subparsers.add_parser("compress-file", help="从文件压缩")
    file_parser.add_argument("file", type=str, help="文件路径")
    file_parser.add_argument("--title", type=str, default="", help="标题")

    # recall
    recall_parser = subparsers.add_parser("recall", help="短码召回")
    recall_parser.add_argument("shortcode", type=str, help="短码")

    # align
    align_parser = subparsers.add_parser("align", help="本地回填对齐")
    align_parser.add_argument("local_file", type=str, help="本地文件路径")
    align_parser.add_argument("--facet", type=str, default="核心引擎", help="所属切面")
    align_parser.add_argument("--notes", type=str, default="", help="备注")

    # align-status
    subparsers.add_parser("align-status", help="查看对齐状态")

    # temporal
    temporal_parser = subparsers.add_parser("temporal", help="时间胶囊")
    temporal_sub = temporal_parser.add_subparsers(dest="temporal_action")
    create_t = temporal_sub.add_parser("create", help="创建时间胶囊")
    create_t.add_argument("--id", required=True, help="胶囊ID")
    create_t.add_argument("--reason", type=str, default="阶段封存", help="原因")
    restore_t = temporal_sub.add_parser("restore", help="恢复时间胶囊")
    restore_t.add_argument("--id", required=True, help="胶囊ID")

    # index
    subparsers.add_parser("index", help="生成对外索引")

    # shortcodes
    subparsers.add_parser("shortcodes", help="查看短码表")

    args = parser.parse_args()

    engine = LUCompressor()

    if args.command == "compress":
        result = engine.run_chain(args.content, args.title, args.source)
        print("\n📊 压缩结果:")
        if isinstance(result, dict) and "dna" in result:
            print(f"  ID: {result['id']}")
            print(f"  DNA: {result['dna']}")
            print(f"  短码: {result['shortcode']}")
            print(f"  压缩率: {result['compression_ratio']:.2%}")
            print(f"  五行: {result['wuxing']}")
            if result.get('quantum_seal'):
                print(f"  固化: {result['quantum_seal']['status']}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "compress-file":
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
            result = engine.run_chain(content, args.title or Path(args.file).stem, args.file)
            print("\n📊 压缩结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"❌ 读取文件失败: {e}")

    elif args.command == "recall":
        result = engine.recall(args.shortcode)
        if result:
            print("\n📌 召回复:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"❌ 短码不存在: {args.shortcode}")

    elif args.command == "align":
        result = engine.align_local(args.local_file, args.facet, args.notes)
        print(f"✅ 已对齐: {args.local_file} → {args.facet}")

    elif args.command == "align-status":
        alignments = engine.get_alignments()
        print("\n📋 本地对齐状态:")
        print("-" * 50)
        for a in alignments:
            print(f"  {a['status']} {a['local_file']} → {a['facet']}")
            if a['notes']:
                print(f"    备注: {a['notes']}")
        print(f"\n总计: {len(alignments)} 条")

    elif args.command == "temporal":
        if args.temporal_action == "create":
            result = engine.create_temporal_capsule(args.id, args.reason)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.temporal_action == "restore":
            result = engine.restore_temporal(args.id)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            temporal_parser.print_help()

    elif args.command == "index":
        index = engine.generate_index()
        print("\n📇 对外索引（时间优先）")
        print("-" * 40)
        print(f"总数: {index['total']}")
        print(f"更新时间: {index['timestamp']}")
        print("\n条目:")
        for entry in index['entries'][:10]:
            print(f"  🧬 {entry['dna']}")
            print(f"  📌 {entry['title']}")
            if entry.get('compression_ratio') is not None:
                print(f"  📊 压缩率: {entry['compression_ratio']:.2%}")
            print()

    elif args.command == "shortcodes":
        print("\n📌 LU压缩短码表")
        print("-" * 30)
        for code, desc in SHORTCODES.items():
            print(f"  {code}: {desc}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
