#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·記憶固化與自適應升級引擎 v1.0
功能：統一提取全系統記憶 · 生成升級快照 · 支持路徑漂移自適應

DNA: #龍芯⚡️2026-04-04-記憶固化引擎-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F1E3B8A4C6D0F2E4A6B8C0D2E4F6A8B0C2
創建者: UID9622 諸葛鑫（龍芯北辰）
理論指導: 曾仕強老師（永恆顯示）

保存為: ~/longhun-system/bin/memory_upgrade_engine.py

【核心約定】
1. 本引擎路徑永遠不變（相對於龍魂根目錄）
2. 根目錄可通過環境變量 LONGBUN_HOME 自適應
3. 若未設置，默認為 ~/longhun-system
4. 最多只變「文件夾名」，不變內部結構
5. 每次提取 = 掃描 + 哈希 + 生成 manifest + 寫入升級鏈
"""

import os
import sys
import json
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


# ══════════════════════════════════════════════════════════
# 定錨層：不可變配置
# ══════════════════════════════════════════════════════════

class MemoryAnchor:
    """記憶定錨層"""
    
    # 根目錄自適應（最多變文件夾名）
    LONGBUN_HOME = Path(os.environ.get("LONGBUN_HOME", Path.home() / "longhun-system"))
    
    # 本引擎固定相對路徑（永不變）
    ENGINE_PATH = LONGBUN_HOME / "bin" / "memory_upgrade_engine.py"
    
    # 記憶源相對路徑（結構永不變）
    MEMORY_SOURCES = {
        "constitution":      "CLAUDE.md",                    # 項目憲法
        "runtime_memory":    "memory.jsonl",                 # 運行時追加記憶
        "knowledge_db":      "knowledge.db",                 # 結構化知識庫
        "plans":             "plans/",                       # 計劃目錄
        "sessions":          "sessions/",                    # 會話歸檔
        "logs_immutable":    "logs/immutable_ledger.jsonl",  # 不可變賬本
        "logs_emotion":      "logs/emotion_log.jsonl",       # 情緒時間線
        "logs_health":       "logs/health.log",              # 健康日誌
        "cs_cards":          "bin/cs_cards_cache.json",      # CS知識卡緩存
        "rules":             "rules/",                       # 規則目錄
        "notion_index":      "notion-index/out/index.jsonl", # Notion索引
    }
    
    # 輸出路徑（相對於根目錄）
    OUTPUT_DIR = LONGBUN_HOME / "memory_manifests"
    MANIFEST_FILE = OUTPUT_DIR / "latest_manifest.json"
    CHAIN_FILE = OUTPUT_DIR / "upgrade_chain.jsonl"


# ══════════════════════════════════════════════════════════
# 記憶提取器
# ══════════════════════════════════════════════════════════

class MemoryExtractor:
    """記憶提取器：只讀不写源文件"""
    
    def __init__(self, anchor: MemoryAnchor = None):
        self.anchor = anchor or MemoryAnchor()
        self.root = self.anchor.LONGBUN_HOME
        self.errors = []
        self.warnings = []
    
    def resolve(self, relative_path: str) -> Path:
        """解析相對路徑為絕對路徑"""
        return self.root / relative_path
    
    def extract_file_info(self, relative_path: str) -> Dict[str, Any]:
        """提取單個文件信息"""
        path = self.resolve(relative_path)
        
        if not path.exists():
            return {"path": str(path), "exists": False, "size": 0}
        
        stat = path.stat()
        
        # 計算文件哈希（前1MB）
        file_hash = self._compute_hash(path)
        
        return {
            "path": str(path),
            "exists": True,
            "size": stat.st_size,
            "mtime": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "hash": file_hash,
            "relative": relative_path
        }
    
    def _compute_hash(self, path: Path) -> str:
        """計算文件SHA256（前1MB）"""
        h = hashlib.sha256()
        try:
            with open(path, "rb") as f:
                h.update(f.read(1024 * 1024))
        except Exception as e:
            return f"ERROR:{e}"
        return h.hexdigest()[:16]
    
    def extract_directory_info(self, relative_path: str) -> Dict[str, Any]:
        """提取目錄信息"""
        path = self.resolve(relative_path)
        
        if not path.exists():
            return {"path": str(path), "exists": False, "files": 0, "total_size": 0}
        
        files = list(path.rglob("*"))
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        file_count = sum(1 for f in files if f.is_file())
        
        # 只取最近5個文件的摘要
        recent_files = sorted(
            [f for f in files if f.is_file()],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )[:5]
        
        return {
            "path": str(path),
            "exists": True,
            "files": file_count,
            "total_size": total_size,
            "relative": relative_path,
            "recent_files": [
                {
                    "name": f.name,
                    "size": f.stat().st_size,
                    "mtime": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                }
                for f in recent_files
            ]
        }
    
    def extract_knowledge_db_stats(self) -> Dict[str, Any]:
        """提取 knowledge.db 統計"""
        db_path = self.resolve("knowledge.db")
        if not db_path.exists():
            return {"exists": False}
        
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            cursor = conn.cursor()
            
            # 獲取所有表
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            stats = {"exists": True, "tables": {}}
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                stats["tables"][table] = count
            
            conn.close()
            return stats
        except Exception as e:
            return {"exists": True, "error": str(e)}
    
    def extract_memory_jsonl_tail(self, n: int = 5) -> List[Dict]:
        """提取 memory.jsonl 最後 N 條"""
        path = self.resolve("memory.jsonl")
        if not path.exists():
            return []
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            records = []
            for line in lines[-n:]:
                try:
                    records.append(json.loads(line))
                except:
                    records.append({"raw": line.strip()})
            return records
        except Exception as e:
            return [{"error": str(e)}]
    
    def extract_constitution_dna(self) -> str:
        """從 CLAUDE.md 提取 DNA"""
        path = self.resolve("CLAUDE.md")
        if not path.exists():
            return "NOT_FOUND"
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if "DNA:" in line and "龍芯" in line:
                        return line.split("DNA:")[1].strip()
        except Exception:
            pass
        return "UNKNOWN"
    
    def run_full_extraction(self) -> Dict[str, Any]:
        """執行完整記憶提取"""
        timestamp = datetime.now().isoformat()
        
        print(f"\n🐉 記憶固化引擎啟動")
        print(f"   根目錄: {self.root}")
        print(f"   時間: {timestamp}")
        print("=" * 50)
        
        manifest = {
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-記憶固化-{hashlib.sha256(timestamp.encode()).hexdigest()[:8].upper()}",
            "timestamp": timestamp,
            "root": str(self.root),
            "engine_version": "v1.0",
            "sources": {}
        }
        
        # 遍歷所有記憶源
        for source_name, relative_path in self.anchor.MEMORY_SOURCES.items():
            print(f"\n📂 提取: {source_name} → {relative_path}")
            
            if relative_path.endswith("/"):
                info = self.extract_directory_info(relative_path)
            else:
                info = self.extract_file_info(relative_path)
            
            manifest["sources"][source_name] = info
            
            if info.get("exists"):
                if "size" in info:
                    print(f"   ✅ 存在 | 大小: {info['size']} bytes | 哈希: {info.get('hash', 'N/A')}")
                else:
                    print(f"   ✅ 存在 | 文件數: {info.get('files', 0)} | 總大小: {info.get('total_size', 0)} bytes")
            else:
                print(f"   ⚠️ 不存在")
                self.warnings.append(f"{source_name} 未找到")
        
        # 特殊提取：knowledge.db 統計
        print(f"\n🗃️  提取 knowledge.db 統計")
        manifest["knowledge_db_stats"] = self.extract_knowledge_db_stats()
        print(f"   {manifest['knowledge_db_stats']}")
        
        # 特殊提取：memory.jsonl 尾部
        print(f"\n🧠 提取 memory.jsonl 最近5條")
        manifest["memory_tail"] = self.extract_memory_jsonl_tail(5)
        print(f"   讀取 {len(manifest['memory_tail'])} 條")
        
        # 特殊提取：憲法 DNA
        print(f"\n📜 提取 CLAUDE.md 憲法 DNA")
        manifest["constitution_dna"] = self.extract_constitution_dna()
        print(f"   {manifest['constitution_dna']}")
        
        # 生成整體哈希
        manifest_str = json.dumps(manifest, ensure_ascii=False, sort_keys=True)
        manifest["manifest_hash"] = hashlib.sha256(manifest_str.encode()).hexdigest()[:16]
        
        print(f"\n🔐 本次快照哈希: {manifest['manifest_hash']}")
        print("=" * 50)
        
        return manifest


# ══════════════════════════════════════════════════════════
# 升級鏈寫入器
# ══════════════════════════════════════════════════════════

class UpgradeChainWriter:
    """將記憶快照寫入升級鏈"""
    
    def __init__(self, anchor: MemoryAnchor = None):
        self.anchor = anchor or MemoryAnchor()
        self.output_dir = self.anchor.OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def write_manifest(self, manifest: Dict[str, Any]):
        """寫入最新 manifest JSON"""
        manifest_path = self.anchor.MANIFEST_FILE
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f"\n💾 manifest 已寫入: {manifest_path}")
    
    def append_chain(self, manifest: Dict[str, Any]):
        """追加到升級鏈（append-only）"""
        chain_path = self.anchor.CHAIN_FILE
        with open(chain_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(manifest, ensure_ascii=False) + "\n")
        print(f"💾 升級鏈已追加: {chain_path}")
    
    def get_chain_length(self) -> int:
        """獲取升級鏈長度"""
        chain_path = self.anchor.CHAIN_FILE
        if not chain_path.exists():
            return 0
        with open(chain_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)


# ══════════════════════════════════════════════════════════
# 自適應升級接口
# ══════════════════════════════════════════════════════════

def adaptive_upgrade(auto_write: bool = True) -> Dict[str, Any]:
    """
    自適應升級入口。
    每次調用都會：
    1. 掃描全系統記憶源
    2. 生成記憶快照
    3. 寫入 manifest + 升級鏈
    4. 返回快照供上層（如 app.py / CLAUDE.md）讀取
    """
    anchor = MemoryAnchor()
    extractor = MemoryExtractor(anchor)
    writer = UpgradeChainWriter(anchor)
    
    # 執行提取
    manifest = extractor.run_full_extraction()
    
    # 寫入存儲
    if auto_write:
        writer.write_manifest(manifest)
        writer.append_chain(manifest)
        chain_len = writer.get_chain_length()
        print(f"\n📈 升級鏈總長度: {chain_len} 個快照")
    
    # 輸出摘要
    print(f"\n🐉 記憶固化完成")
    print(f"   DNA: {manifest['dna']}")
    print(f"   快照哈希: {manifest['manifest_hash']}")
    print(f"   憲法版本: {manifest['constitution_dna']}")
    print("   下次升級時，直接讀取本文件即可自適應")
    print("")
    
    return manifest


# ══════════════════════════════════════════════════════════
# 主程序
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="龍魂·記憶固化與自適應升級引擎")
    parser.add_argument("--dry-run", "-d", action="store_true", help="只提取不寫入")
    parser.add_argument("--source", "-s", type=str, help="指定單個記憶源提取")
    
    args = parser.parse_args()
    
    if args.source:
        # 單源提取模式
        anchor = MemoryAnchor()
        extractor = MemoryExtractor(anchor)
        info = extractor.extract_file_info(args.source)
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        # 完整固化模式
        manifest = adaptive_upgrade(auto_write=not args.dry_run)
        
        # 輸出簡潔 JSON 到 stdout（供其他程序捕獲）
        summary = {
            "dna": manifest["dna"],
            "manifest_hash": manifest["manifest_hash"],
            "constitution_dna": manifest["constitution_dna"],
            "timestamp": manifest["timestamp"],
            "root": manifest["root"],
            "sources_count": len(manifest["sources"]),
            "status": "UPGRADE_READY"
        }
        print(json.dumps(summary, ensure_ascii=False))
