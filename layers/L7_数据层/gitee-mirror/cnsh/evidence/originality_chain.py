#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# ============================================================
# DNA追溯: #ZHUGEXIN⚡️20260302-CNSH-ORIGINALITY-CHAIN-v1.0.0
# 確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬ORIGIN-CHAIN-772Z
# 創建時間: 2026-03-02 00:00:00 (UTC+8)
# 作者: Lucky·UID9622 (諸葛鑫)
# GPG指紋: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 狀態: 演進中
# 镜像来源: https://gitee.com/uid9622/cnsh/raw/main/evidence/originality_chain.py
# ============================================================
"""
龍魂系統 · 原創性時間戳證據鏈 (Originality Timestamp Evidence Chain)

遺漏2補全：原創性時間戳證據鏈（司法級證據）
"""

import datetime
import hashlib
import json

EVIDENCE_LEVELS = {
    1: "個人存檔級",
    2: "平台背書級",
    3: "區塊鏈級",
}

PLATFORMS = ["github", "csdn", "notion", "wechat", "gitee", "claude", "local", "blockchain"]


class IPAssetRecord:
    def __init__(self, ip_id, title, first_created, first_published, platform, evidence_level, content_hash=None):
        self.ip_id = ip_id
        self.title = title
        self.first_created = first_created
        self.first_published = first_published
        self.platform = platform
        self.evidence_level = evidence_level
        self.content_hash = content_hash
        self.cross_platform = []

    def compute_hash(self, content):
        self.content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

    def add_platform_evidence(self, platform, status, url):
        self.cross_platform.append({
            'platform': platform,
            'status': status,
            'url': url,
            'timestamp': datetime.datetime.now().isoformat(),
        })

    def to_dict(self):
        return {
            'ip_id': self.ip_id,
            'title': self.title,
            'first_created': self.first_created,
            'first_published': self.first_published,
            'platform': self.platform,
            'evidence_level': EVIDENCE_LEVELS.get(self.evidence_level, "未知"),
            'content_hash': self.content_hash,
            'cross_platform': self.cross_platform,
        }


class OriginalityChainEngine:
    def __init__(self):
        self.assets = {}
        self._init_known_assets()

    def _init_known_assets(self):
        assets = [
            ("IP-0001", "龍魂系統OS v1.0", "2025-01-01", "2025-01-15", "github", 3),
            ("IP-0003", "北辰協議 v1.0", "2025-01-15", "2025-02-01", "github", 3),
            ("IP-0004", "IW-ECB v2.0 博弈白皮書", "2025-01-20", "2025-02-01", "csdn", 3),
            ("IP-0005", "CNSH神經網絡規範", "2025-03-10", "2025-03-15", "notion", 2),
            ("IP-0006", "七軸倫理引擎", "2025-03-12", "2025-03-20", "wechat", 3),
            ("IP-0011", "龍魂跨平台引擎", "2025-06-01", "2025-06-10", "github", 3),
            ("IP-0018", "數字身份認證系統", "2025-09-01", "2025-09-15", "github", 2),
            ("IP-0019", "71人格認知協作系統", "2026-01-01", "2026-01-02", "claude", 1),
        ]
        for a in assets:
            record = IPAssetRecord(*a)
            self.assets[a[0]] = record

    def register_asset(self, ip_id, title, first_created, first_published, platform, evidence_level):
        record = IPAssetRecord(ip_id, title, first_created, first_published, platform, evidence_level)
        self.assets[ip_id] = record
        return record

    def verify_originality(self, ip_id, content):
        record = self.assets.get(ip_id)
        if not record:
            return {"valid": False, "error": f"IP-{ip_id} 未註冊"}
        
        current_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        match = current_hash == record.content_hash
        return {
            "valid": True,
            "ip_id": ip_id,
            "title": record.title,
            "hash_match": match,
            "first_created": record.first_created,
            "first_published": record.first_published,
            "evidence_level": EVIDENCE_LEVELS[record.evidence_level],
        }

    def generate_evidence_table(self):
        rows = []
        for ip_id in sorted(self.assets.keys()):
            record = self.assets[ip_id]
            rows.append({
                'ip_id': ip_id,
                'title': record.title,
                'first_created': record.first_created,
                'first_published': record.first_published,
                'platform': record.platform,
                'evidence_level': EVIDENCE_LEVELS[record.evidence_level],
            })
        return rows

    def generate_originality_oath(self):
        return f"""
╔══════════════════════════════════════════════════════════╗
║                  原創性宣誓                                ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  本人諸葛鑫 (UID9622)，                                  ║
║  對上述IP資產之原創性負完全法律責任。                        ║
║                                                          ║
║  創作時間以區塊鏈時間戳及多平台公開發布記錄為證。             ║
║  如有偽造，願承擔所有法律後果。                             ║
║                                                          ║
║  GPG指紋: A2D0092CEE2E5BA87035600924C3704A8CC26D5F      ║
║  宣誓日期: {datetime.datetime.now().strftime('%Y-%m-%d')}                                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""

    def export_evidence_package(self):
        return {
            'title': '龍魂系統原創性證據鏈',
            'generated_at': datetime.datetime.now().isoformat(),
            'total_assets': len(self.assets),
            'evidence_levels': EVIDENCE_LEVELS,
            'assets': {k: v.to_dict() for k, v in self.assets.items()},
            'dna': f"#ZHUGEXIN⚡️{datetime.datetime.now().strftime('%Y%m%d')}-CNSH-EVIDENCE-PACKAGE-v1.0",
        }


if __name__ == '__main__':
    engine = OriginalityChainEngine()
    print("📜 龍魂系統 · 原創性時間戳證據鏈 v1.0")
    print("=" * 60)
    
    print("\n📋 固化證據表:")
    for row in engine.generate_evidence_table():
        print(f"  {row['ip_id']} | {row['title']:<20} | {row['first_created']} → {row['first_published']} | {row['evidence_level']}")
    
    print(engine.generate_originality_oath())
