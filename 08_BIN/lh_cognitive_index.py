#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 認知索引系統 v1.0（對齊版）

AI大腦地圖：密鑰在哪？記憶在哪？協議在哪？功能在哪？代碼在哪？
AI自己看這張地圖就知道去哪找東西——不理解的先查地圖，不準瞎猜路徑。

對齊說明（2026-08-15·UID9622）：
  Kimi 原稿含多處假路徑（~/bin/lh 不存在、~/.longhun/03_MEMORY 為空、
  LH-DNA-STANDARD.md 不存在），本版全部對齊真實系統：
  - 協議 = 動態掃描 01_protocols/*.md（真實206+個）
  - 引擎 = 動態掃描 05_ENGINES/*.py + bin/*.py（真實62+個）
  - 記憶 = ~/.longhun/memory/ + .codebuddy/memory/ + 03_MEMORY/ai_conversations/
  - 互通 = ~/.longhun/event_bus/event_bus.db（LCB事件總線·AI互通消息池）
  - 入口 = ~/longhun-system/bin/lh
  - 密鑰 = ~/.longhun/env/（API Keys）· ~/.gnupg/（GPG）· ~/.ssh/（SSH）

DNA: #龍芯⚡️丙午·丙申·庚申·亥時-COGNITIVE-INDEX-ALIGN-v1.0-UID9622
創建者: 諸葛鑫（UID9622）
確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
三色: 🟢
"""

import os
import sys
import json
import hashlib
import time
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
import argparse

# ============================================================
# 主權錨定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def generate_dna(suffix: str = "INDEX") -> str:
    """生成 DNA 追溯碼"""
    timestamp = datetime.now().strftime("%Y-%m-%d")
    rand = hashlib.sha256(f"{suffix}{timestamp}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️丙午·丙申·庚申·亥時-{suffix}-{rand}-{UID}"


# ============================================================
# 真實路徑對齊（2026-08-15 盤查結果）
# ============================================================

HOME = Path.home()
LONGHUN_HOME = HOME / ".longhun"


def find_repo_root() -> Path:
    """定位龍魂倉庫根目錄：優先環境變量，其次向上探測，兜底 ~/longhun-system"""
    env_root = os.environ.get("LONGHUN_SYSTEM")
    if env_root and Path(env_root).exists():
        return Path(env_root)
    # 從當前工作目錄向上探測
    cur = Path.cwd()
    for parent in [cur, *cur.parents]:
        if (parent / "01_protocols").is_dir() and (parent / "bin").is_dir():
            return parent
    # 兜底
    fallback = HOME / "longhun-system"
    if fallback.exists():
        return fallback
    return Path.cwd()


REPO_ROOT = find_repo_root()

COGNITIVE_INDEX = LONGHUN_HOME / "cognitive_index.json"
COGNITIVE_BACKUP = LONGHUN_HOME / "cognitive_index.backup.json"

LONGHUN_HOME.mkdir(parents=True, exist_ok=True)

# 真實錨點（已驗證存在）
ANCHOR_KEYS = {
    "api_keys": str(LONGHUN_HOME / "env"),            # API Keys（真實存在）
    "gpg_pubring": str(HOME / ".gnupg" / "public-keys.d"),  # GPG 2.4+ 公鑰目錄（真實存在）
    "gpg_secret": "🔒 物理隔離·永不入雲·不可訪問",     # 私鑰規矩
    "ssh_keys": str(HOME / ".ssh"),                   # SSH Keys（真實）
    "kunpeng_ssh": str(HOME / ".ssh" / "longhun_kunpeng_ed25519"),  # 鯤鵬 SSH key
}

ANCHOR_MEMORY = {
    "longhun_memory": str(LONGHUN_HOME / "memory"),                # 長期記憶（latest_digest.json 等·真實）
    "event_bus_db": str(LONGHUN_HOME / "event_bus" / "event_bus.db"),  # AI互通消息池（LCB·真實）
    "codebuddy_memory": str(REPO_ROOT / ".codebuddy" / "memory"),  # CodeBuddy 工作記憶（真實）
    "ai_conversations": str(REPO_ROOT / "03_MEMORY" / "ai_conversations"),  # AI對話池（真實）
    "historian_audit": str(REPO_ROOT / "04_AUDIT"),               # 史官審計（真實）
    "ai_mesh_agents": str(LONGHUN_HOME / "ai_mesh" / "agents.json"),  # AI互通節點註冊（真實）
}

ANCHOR_CODE = {
    "core_bin": str(REPO_ROOT / "08_BIN"),      # 核心引擎
    "engines": str(REPO_ROOT / "05_ENGINES"),   # 高階引擎
    "protocols": str(REPO_ROOT / "01_protocols"),  # 協議層
    "bin_scripts": str(REPO_ROOT / "bin"),      # 命令腳本
    "memory_pool": str(REPO_ROOT / "03_MEMORY"),  # 記憶層
    "config": str(REPO_ROOT / "config"),        # 配置
    "tests": str(REPO_ROOT / "tests"),          # 測試
    "deploy": str(REPO_ROOT / "deploy"),        # 部署
}

ANCHOR_CONFIGS = {
    "main_config": str(REPO_ROOT / "config"),
    "longhun_configs": str(LONGHUN_HOME / "configs"),          # ~/.longhun/configs（真實存在）
    "env_example": str(REPO_ROOT / "deploy" / ".env.kunpeng.example"),  # 鯤鵬環境變量模板
    "command_index": str(REPO_ROOT / ".codebuddy" / "COMMAND_INDEX.md"),  # 命令總目
    "neural_net": str(REPO_ROOT / ".codebuddy" / "longhun_neural_net.json"),  # 系統拓撲
}

ANCHOR_TOOLS = {
    "lh": str(REPO_ROOT / "bin" / "lh"),        # 統一入口（真實·~/.longhun/bin/lh 不存在）
    "python3": shutil.which("python3") or "/usr/bin/python3",
    "gpg": shutil.which("gpg") or "/usr/bin/gpg",
    "git": shutil.which("git") or "/usr/bin/git",
}

ANCHOR_DOCS = {
    "readme": str(REPO_ROOT / "README.md"),
    "command_index": str(REPO_ROOT / ".codebuddy" / "COMMAND_INDEX.md"),
    "codebuddy_cfg": str(REPO_ROOT / ".codebuddy" / "CODEBUDDY.md"),
    "state": str(REPO_ROOT / "STATE.md"),       # 統一實時狀態入口
    "agp_guide": str(REPO_ROOT / "AGENTS.md"),  # AI操作手冊
}

ANCHOR_EXTERNAL = {
    "kunpeng_web": "https://uid9622.cn",        # 鯤鵬官網/API/onboarding
    "notion": "https://uid9622.notion.site",    # Notion 知識庫
    "csdn": "https://uid9622-01.blog.csdn.net", # CSDN 博客
    "onboarding": "https://uid9622.cn/api/onboarding/bootstrap",  # AI進門引導API
    "deepseek_api": "https://api.deepseek.com/v1",
    "kimi_api": "https://api.moonshot.cn/v1",
}

ANCHOR_CUSTOM = {
    "owner": "諸葛鑫",
    "uid": UID,
    "confirm_code": CONFIRM,
    "gpg_fingerprint": GPG,
    "system": "龍魂系統",
    "language": "CNSH",
    "sovereignty": "中國",
    "dna_standard": "v∞干支卦追溯碼",
    "iron_law": "不理解的先查認知索引·不準瞎猜路徑",
}


# ============================================================
# 認知索引數據結構
# ============================================================

@dataclass
class CognitiveIndex:
    """認知索引 - AI的大腦地圖"""
    version: str = "1.0"
    dna: str = field(default_factory=lambda: generate_dna("INDEX"))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    changelog: List[Dict] = field(default_factory=list)

    keys: Dict[str, str] = field(default_factory=dict)
    memory: Dict[str, str] = field(default_factory=dict)
    protocols: Dict[str, str] = field(default_factory=dict)
    functions: Dict[str, str] = field(default_factory=dict)
    code: Dict[str, str] = field(default_factory=dict)
    configs: Dict[str, str] = field(default_factory=dict)
    tools: Dict[str, str] = field(default_factory=dict)
    docs: Dict[str, str] = field(default_factory=dict)
    external: Dict[str, str] = field(default_factory=dict)
    custom: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'CognitiveIndex':
        if "changelog" not in data:
            data["changelog"] = []
        if "meta" not in data:
            data["meta"] = {}
        return cls(**data)


# ============================================================
# 認知索引管理器
# ============================================================

class CognitiveIndexManager:
    """認知索引管理器 - 讓AI知道去哪找東西"""

    def __init__(self, index_path: Path = COGNITIVE_INDEX):
        self.index_path = index_path
        self._index: Optional[CognitiveIndex] = None
        self._load_or_create()

    def _load_or_create(self) -> CognitiveIndex:
        if self.index_path.exists():
            try:
                with open(self.index_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._index = CognitiveIndex.from_dict(data)
                return self._index
            except Exception as e:
                print(f"⚠️ 索引加載失敗: {e}，重建索引")
        self._index = self._build_default_index()
        self.save()
        return self._index

    def _build_default_index(self) -> CognitiveIndex:
        """構建默認索引：真實錨點 + 動態掃描，拒絕假路徑"""
        idx = CognitiveIndex()

        # 1. 密鑰（真實錨點）
        idx.keys = dict(ANCHOR_KEYS)

        # 2. 記憶（真實錨點）
        idx.memory = dict(ANCHOR_MEMORY)

        # 3. 協議（動態掃描 01_protocols/*.md）
        protocol_dir = REPO_ROOT / "01_protocols"
        if protocol_dir.is_dir():
            for f in sorted(protocol_dir.glob("*.md")):
                idx.protocols[f.stem] = str(f)

        # 4. 功能（動態掃描 05_ENGINES/*.py + bin/*.py）
        for d in [REPO_ROOT / "05_ENGINES", REPO_ROOT / "bin"]:
            if d.is_dir():
                for f in sorted(d.glob("*.py")):
                    if f.stem in ("__init__",):
                        continue
                    idx.functions[f.stem] = str(f)

        # 5. 代碼（真實錨點）
        idx.code = dict(ANCHOR_CODE)

        # 6. 配置（真實錨點）
        idx.configs = dict(ANCHOR_CONFIGS)

        # 7. 工具（真實錨點）
        idx.tools = dict(ANCHOR_TOOLS)

        # 8. 文檔（真實錨點）
        idx.docs = dict(ANCHOR_DOCS)

        # 9. 外部集成（真實錨點）
        idx.external = dict(ANCHOR_EXTERNAL)

        # 10. 自定義
        idx.custom = dict(ANCHOR_CUSTOM)

        # 11. 元數據
        idx.meta = {
            "repo_root": str(REPO_ROOT),
            "protocol_count": len(idx.protocols),
            "function_count": len(idx.functions),
            "total_entries": sum(len(getattr(idx, c)) for c in
                                 ["keys", "memory", "protocols", "functions",
                                  "code", "configs", "tools", "docs", "external", "custom"]),
            "last_scan": datetime.now().isoformat(),
            "scan_mode": "realpath_aligned",
        }

        return idx

    def save(self) -> bool:
        if not self._index:
            return False
        self._index.updated_at = datetime.now().isoformat()
        if self.index_path.exists():
            try:
                shutil.copy2(self.index_path, COGNITIVE_BACKUP)
            except Exception:
                pass
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(self._index.to_dict(), f, indent=2, ensure_ascii=False)
        print(f"✅ 認知索引已保存: {self.index_path}")
        return True

    def query(self, category: str, key: str = None) -> Any:
        if not self._index:
            return {"error": "索引未加載"}
        index_dict = self._index.to_dict()
        if category not in index_dict:
            return {"error": f"類別 '{category}' 不存在，可用: {list(index_dict.keys())}"}
        if key:
            if key in index_dict[category]:
                return index_dict[category][key]
            return {"error": f"在 '{category}' 中找不到 '{key}'"}
        return index_dict[category]

    def update(self, category: str, key: str, value: str) -> Dict:
        if not self._index:
            return {"error": "索引未加載"}
        if not hasattr(self._index, category):
            return {"error": f"類別 '{category}' 不存在"}
        old_value = getattr(self._index, category).get(key)
        getattr(self._index, category)[key] = value
        self._index.changelog.append({
            "timestamp": datetime.now().isoformat(),
            "action": "update",
            "category": category,
            "key": key,
            "old_value": old_value,
            "new_value": value,
            "dna": generate_dna("CHANGE"),
        })
        self.save()
        return {"status": "updated", "category": category, "key": key, "value": value}

    def search(self, keyword: str) -> List[Dict]:
        if not self._index:
            return []
        results = []
        index_dict = self._index.to_dict()
        for category, items in index_dict.items():
            if category in ["version", "dna", "created_at", "updated_at", "changelog", "meta", "custom"]:
                continue
            if isinstance(items, dict):
                for key, value in items.items():
                    if (keyword.lower() in key.lower() or
                            keyword.lower() in str(value).lower()):
                        results.append({"category": category, "key": key, "value": value})
        return results

    def health_check(self) -> Dict:
        """健康檢查：索引中每個路徑是否真實存在"""
        if not self._index:
            return {"status": "error", "message": "索引未加載"}
        results = {"total": 0, "valid": 0, "invalid": 0, "invalid_paths": []}
        index_dict = self._index.to_dict()
        for category, items in index_dict.items():
            if category in ["version", "dna", "created_at", "updated_at", "changelog", "meta", "custom", "external"]:
                continue
            if isinstance(items, dict):
                for key, value in items.items():
                    if not isinstance(value, str):
                        continue
                    p = value
                    # 跳過非路徑內容（規矩/鏈接/占位）
                    if "://" in p or p.startswith("🔒") or "不可訪問" in p:
                        continue
                    results["total"] += 1
                    if Path(p).exists():
                        results["valid"] += 1
                    else:
                        results["invalid"] += 1
                        results["invalid_paths"].append({"category": category, "key": key, "path": p})
        results["status"] = "healthy" if results["invalid"] == 0 else "degraded"
        return results

    def refresh(self) -> Dict:
        """重新掃描並重建索引（目錄變了自動更新）"""
        self._index = self._build_default_index()
        self.save()
        return {"status": "refreshed", "protocols": len(self._index.protocols),
                "functions": len(self._index.functions)}

    def get_summary(self) -> str:
        if not self._index:
            return "索引未加載"
        index_dict = self._index.to_dict()
        lines = [
            "🧠 龍魂 · 認知索引摘要",
            "=" * 54,
            f"版本: {index_dict.get('version')}",
            f"DNA: {index_dict.get('dna')}",
            f"倉庫根: {self._index.meta.get('repo_root')}",
            f"更新: {index_dict.get('updated_at')}",
            "",
            "📂 索引類別統計:",
        ]
        for cat in ["keys", "memory", "protocols", "functions", "code", "configs", "tools", "docs", "external", "custom"]:
            if cat in index_dict:
                lines.append(f"  {cat}: {len(index_dict[cat])} 項")
        lines.append("")
        lines.append("🔧 查詢方式:")
        lines.append("  lh index --query '密鑰在哪'     # 問問題")
        lines.append("  lh index --search dna         # 關鍵詞搜索")
        lines.append("  lh index --health             # 路徑有效性檢查")
        lines.append("  lh index --refresh            # 重新掃描更新")
        lines.append("  lh index --list               # 看完整地圖")
        lines.append("")
        lines.append("⚡ 鐵律: 不理解的先查地圖·不準瞎猜路徑")
        return "\n".join(lines)


# ============================================================
# 認知AI接口
# ============================================================

class CognitiveAI:
    """認知AI - AI通過這個接口自我檢索"""

    def __init__(self):
        self.index = CognitiveIndexManager()

    def ask(self, question: str) -> str:
        q = question.lower()
        answers = []

        # 簡體/繁體/英文 關鍵詞均匹配
        category_map = [
            (["密钥", "密鑰", "key"], "keys", "🔑 密鑰位置:"),
            (["记忆", "記憶", "memory"], "memory", "🧠 記憶位置:"),
            (["协议", "協議", "protocol"], "protocols", "📜 協議位置:"),
            (["功能", "function"], "functions", "⚡ 功能位置:"),
            (["代码", "代碼", "code"], "code", "💻 代碼位置:"),
            (["配置", "config"], "configs", "⚙️ 配置位置:"),
            (["工具", "tool"], "tools", "🔧 工具位置:"),
            (["文档", "文檔", "doc"], "docs", "📚 文檔位置:"),
            (["外部", "external", "api"], "external", "🌐 外部集成:"),
            (["自定义", "自定義", "custom"], "custom", "🏷️ 自定義標籤:"),
        ]

        for kws, cat, title in category_map:
            if any(kw in q for kw in kws):
                result = self.index.query(cat)
                if isinstance(result, dict) and not result.get("error"):
                    lines = [title]
                    items = list(result.items())
                    # 協議/功能太多只顯示前 15 條
                    shown = items[:15]
                    for k, v in shown:
                        lines.append(f"  {k}: {v}")
                    if len(items) > 15:
                        lines.append(f"  … 共 {len(items)} 項（用 lh index --list 看全部）")
                    answers.append("\n".join(lines))

        if answers:
            return "\n\n".join(answers)

        results = self.index.search(q)
        if results:
            return "🔍 搜索結果:\n" + "\n".join(
                [f"  [{r['category']}] {r['key']}: {r['value']}" for r in results[:12]]
            )
        return "🤔 沒找到相關信息。試試問：密鑰在哪？記憶在哪？協議在哪？功能在哪？代碼在哪？配置在哪？"

    def show_health(self) -> str:
        result = self.index.health_check()
        if result["status"] == "healthy":
            return f"🟢 索引健康（{result['valid']}/{result['total']} 路徑有效）"
        head = f"🟡 索引降級（{result['invalid']} 個路徑無效 / 共 {result['total']}）\n"
        for p in result["invalid_paths"][:10]:
            head += f"  ❌ [{p['category']}] {p['key']}: {p['path']}\n"
        if result["invalid"] > 10:
            head += f"  … 共 {result['invalid']} 個\n"
        head += "  → 執行 lh index --refresh 重新掃描"
        return head


# ============================================================
# 命令行列接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 認知索引系統 v1.0（AI大腦地圖·對齊版）",
        epilog="你問它答：密鑰在哪？記憶在哪？協議在哪？功能在哪？代碼在哪？不理解的先查地圖！",
    )
    parser.add_argument("--query", "-q", type=str, help="查詢索引（如: '密鑰在哪'）")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有索引")
    parser.add_argument("--search", "-s", type=str, help="搜索關鍵詞")
    parser.add_argument("--update", "-u", nargs=3, metavar=("CATEGORY", "KEY", "VALUE"), help="更新索引（填空）")
    parser.add_argument("--summary", action="store_true", help="顯示摘要")
    parser.add_argument("--health", action="store_true", help="路徑有效性健康檢查")
    parser.add_argument("--refresh", action="store_true", help="重新掃描更新索引")
    parser.add_argument("--save", action="store_true", help="保存索引")

    args = parser.parse_args()
    cognitive = CognitiveAI()

    if args.query:
        print(cognitive.ask(args.query))
        return
    if args.list:
        data = cognitive.index._index.to_dict() if cognitive.index._index else {}
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return
    if args.search:
        results = cognitive.index.search(args.search)
        print(f"🔍 搜索 '{args.search}': 找到 {len(results)} 個結果")
        for r in results:
            print(f"  [{r['category']}] {r['key']}: {r['value']}")
        return
    if args.update:
        result = cognitive.index.update(args.update[0], args.update[1], args.update[2])
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    if args.summary:
        print(cognitive.index.get_summary())
        return
    if args.health:
        print(cognitive.show_health())
        return
    if args.refresh:
        result = cognitive.index.refresh()
        print(f"✅ 已重新掃描: 協議 {result['protocols']} 個 · 功能 {result['functions']} 個")
        return
    if args.save:
        cognitive.index.save()
        return

    # 交互模式
    print("""
╔══════════════════════════════════════════════════════════════╗
║  🧠 龍魂 · 認知索引系統（AI大腦地圖）                        ║
║  你問它答：密鑰在哪？記憶在哪？協議在哪？功能在哪？          ║
╠══════════════════════════════════════════════════════════════╣
║  lh index --query '密鑰在哪'    lh index --search dna        ║
║  lh index --health              lh index --refresh           ║
║  lh index --list                lh index --summary           ║
╚══════════════════════════════════════════════════════════════╝
    """)
    while True:
        try:
            q = input("\n🧠 你問: ")
            if q.lower() in ("exit", "quit", "q"):
                break
            print(cognitive.ask(q))
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()
