#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# ═══════════════════════════════════════════
# 龍魂体系 | 压缩卡模块 v1.0
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-COMPRESSION-CARD-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: UID9622（诸葛鑫·Lucky）
# 三色审计: 🟢 通过
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 上游协议: 记忆永存与外脑压缩总协议 v1.0 · 第七章7.3
# ═══════════════════════════════════════════
# M::机器块 + CNSH::路由块 双封装标准
# 用法:
#   python3 bin/lh_compression_card.py create <来源文件>     # 从文件生成压缩卡
#   python3 bin/lh_compression_card.py show <卡ID>           # 展示压缩卡
#   python3 bin/lh_compression_card.py index                 # 索引所有压缩卡
#   python3 bin/lh_compression_card.py search <关键词>       # 搜索
# ═══════════════════════════════════════════
"""

import json
import sys
import time
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict

# ─── 项目路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = PROJECT_ROOT / "state" / "exobrain"
STATE_DIR.mkdir(parents=True, exist_ok=True)
CARDS_DIR = STATE_DIR / "cards"
CARDS_DIR.mkdir(parents=True, exist_ok=True)
INDEX_FILE = STATE_DIR / "card_index.json"

# ─── 八卦分区映射（继承LU归集器） ───
BAGUA_MAP = {
    "协议": "☰乾", "安全": "☶艮", "审计": "☲离", "训练": "☳震",
    "部署": "☴巽", "数据": "☵坎", "记忆": "☷坤", "知识": "☱兑",
    "人格": "☲离", "哲学": "☰乾", "经济": "☴巽", "工程": "☳震",
    "默认": "☷坤",
}


@dataclass
class 压缩卡:
    """标准压缩卡 · 继承LU归集器§05 + v1.0新增字段"""
    # ── 基础字段 ──
    一句话: str = ""
    核心结论: List[str] = field(default_factory=list)
    核心骨架: str = ""
    系统价值: str = ""
    归档分类: str = ""
    语义抽屉: str = ""
    八卦分区: str = "☷坤"
    三色: str = "🟢"
    项目模块: str = ""
    风险级: str = "低"
    状态: str = "active"
    短码: str = ""
    下一步: str = ""

    # ── v1.0 新增字段（协议7.3） ──
    sigma: float = 0.0
    舍弃清单: List[str] = field(default_factory=list)
    simhash: int = 0
    重要性I: float = 0.0
    档级: str = "常规"
    迭代代数: int = 0
    原始长度: int = 0
    压缩后长度: int = 0
    压缩率: float = 0.0

    # ── 元数据 ──
    id: str = ""
    dna: str = ""
    时间戳: str = ""
    来源文件: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "压缩卡":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})

    # ═══════════════════════════════════════
    # M:: 机器块（结构化·可程序解析）
    # ═══════════════════════════════════════
    def M块(self) -> dict:
        return {
            "id": self.id,
            "一句话": self.一句话,
            "核心结论": self.核心结论,
            "核心骨架": self.核心骨架,
            "系统价值": self.系统价值,
            "归档分类": self.归档分类,
            "语义抽屉": self.语义抽屉,
            "八卦分区": self.八卦分区,
            "三色": self.三色,
            "项目模块": self.项目模块,
            "风险级": self.风险级,
            "状态": self.状态,
            "短码": self.短码,
            "下一步": self.下一步,
            "sigma": self.sigma,
            "舍弃清单": self.舍弃清单,
            "simhash": f"{self.simhash:#018x}",
            "重要性I": self.重要性I,
            "档级": self.档级,
            "迭代代数": self.迭代代数,
            "原始长度": self.原始长度,
            "压缩后长度": self.压缩后长度,
            "压缩率": self.压缩率,
            "dna": self.dna,
            "时间戳": self.时间戳,
        }

    # ═══════════════════════════════════════
    # CNSH:: 路由块（语义路由·八卦定位）
    # ═══════════════════════════════════════
    def CNSH块(self) -> dict:
        return {
            "路由": {
                "八卦": self.八卦分区,
                "语义抽屉": self.语义抽屉,
                "档级": self.档级,
                "三色": self.三色,
            },
            "定位": {
                "短码": self.短码,
                "归档分类": self.归档分类,
                "项目模块": self.项目模块,
            },
            "溯源": {
                "dna": self.dna,
                "来源文件": self.来源文件,
                "时间戳": self.时间戳,
            },
        }

    # ═══════════════════════════════════════
    # 完整卡面（Markdown）
    # ═══════════════════════════════════════
    def 卡面(self) -> str:
        lines = [
            f"# 全文压缩卡 `{self.id}`",
            "",
            f"**一句话**: {self.一句话}",
            f"**核心结论**: {' | '.join(self.核心结论) if self.核心结论 else '—'}",
            f"**骨架**: {self.核心骨架[:200]}",
            f"**价值**: {self.系统价值}",
            "",
            f"## 归档信息",
            f"- 分类: `{self.归档分类}` · `{self.语义抽屉}` · `{self.八卦分区}`",
            f"- 状态: {self.三色} {self.状态}",
            f"- 模块: {self.项目模块} · 风险: {self.风险级}",
            f"- 档级: {self.档级} | I={self.重要性I:.3f} | σ={self.sigma:.4f}",
            "",
            f"## 压缩数据",
            f"- 原始: {self.原始长度}B → 压缩: {self.压缩后长度}B (ρ={self.压缩率:.2f})",
            f"- 迭代: {self.迭代代数}轮 · simhash: `{self.simhash:#018x}`",
            f"- 舍弃: {', '.join(self.舍弃清单) if self.舍弃清单 else '无'}",
            "",
            f"## 路由",
            f"- 短码: `{self.短码}`",
            f"- 下一步: {self.下一步}",
            "",
            f"## 溯源",
            f"- DNA: `{self.dna}`",
            f"- 时间: {self.时间戳}",
            f"- 来源: {self.来源文件}",
        ]
        return "\n".join(lines)

    def 双封装(self) -> dict:
        """M:: + CNSH:: 双封装输出"""
        return {
            "M::": self.M块(),
            "CNSH::": self.CNSH块(),
        }


class 压缩卡管理器:
    """压缩卡的全生命周期管理 v1.0"""

    DNA = "#龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-COMPRESSION-CARD-v1.0"

    def __init__(self, state_dir: Path = None):
        self.state_dir = state_dir or STATE_DIR
        self.cards_dir = self.state_dir / "cards"
        self.cards_dir.mkdir(parents=True, exist_ok=True)
        self.index = self._load_index()
        # v1.1: 内存缓存，避免每次查卡都读磁盘
        self._card_cache: Dict[str, dict] = {}

    def _load_index(self) -> dict:
        if INDEX_FILE.exists():
            return json.loads(INDEX_FILE.read_text())
        return {"cards": {}, "total": 0, "dna": self.DNA}

    def _save_index(self):
        self.index["total"] = len(self.index["cards"])
        INDEX_FILE.write_text(json.dumps(self.index, ensure_ascii=False, indent=2))

    def _生成ID(self, 摘要: str) -> str:
        ts = int(time.time())
        h = hashlib.sha256(f"{ts}{摘要}".encode()).hexdigest()[:8]
        return f"CARD-{ts}-{h}"

    def _八卦分类(self, 文本: str) -> str:
        for keyword, gua in BAGUA_MAP.items():
            if keyword in 文本:
                return gua
        return BAGUA_MAP["默认"]

    def 创建压缩卡(self, 来源文件: str = "", 原文: str = "", 档: str = "常规",
                   压缩引擎=None, 用户标记: int = 5, 情感: float = 0.5) -> dict:
        """从原文生成一张完整压缩卡"""
        if 压缩引擎 is None:
            from bin.lh_exobrain_engine import CNSH_记忆外脑引擎, 压缩卡 as EC
            压缩引擎 = CNSH_记忆外脑引擎()

        # 跑压缩管线
        result = 压缩引擎.完整压缩管线(原文, 档, 来源=来源文件,
                                         用户标记=用户标记, 情感=情感)
        if "error" in result:
            return result

        # 构建压缩卡
        card_data = result.get("压缩卡", {})
        card = 压缩卡(
            id=self._生成ID(原文[:40]),
            **{k: v for k, v in card_data.items() if k in 压缩卡.__dataclass_fields__},
        )
        card.八卦分区 = self._八卦分类(原文)
        card.短码 = f"/压缩 n={card.迭代代数}"
        card.下一步 = "归档入库" if result.get("状态", "").startswith("🟢") else "人工复审"
        card.来源文件 = 来源文件

        # 持久化
        card_path = self.cards_dir / f"{card.id}.json"
        card_path.write_text(json.dumps(card.to_dict(), ensure_ascii=False, indent=2))

        # v1.1: 同步更新缓存
        self._card_cache[card.id] = card.to_dict()

        # Markdown 卡面
        md_path = self.cards_dir / f"{card.id}.md"
        md_path.write_text(card.卡面())

        # 索引
        self.index["cards"][card.id] = {
            "一句话": card.一句话,
            "八卦分区": card.八卦分区,
            "档级": card.档级,
            "重要性I": card.重要性I,
            "sigma": card.sigma,
            "三色": card.三色,
            "短码": card.短码,
            "时间戳": card.时间戳,
        }
        self._save_index()

        return {
            "id": card.id,
            "卡": card.to_dict(),
            "路径": str(card_path),
            "双封装": card.双封装(),
        }

    def 查卡(self, card_id: str) -> Optional[dict]:
        """查询单张卡（优先缓存）"""
        if card_id in self._card_cache:
            return self._card_cache[card_id]
        path = self.cards_dir / f"{card_id}.json"
        if path.exists():
            data = json.loads(path.read_text())
            self._card_cache[card_id] = data
            return data
        return None

    def 列表(self) -> List[dict]:
        cards = []
        for card_id in self.index["cards"]:
            c = self.查卡(card_id)
            if c:
                cards.append(c)
        return sorted(cards, key=lambda c: c.get("重要性I", 0), reverse=True)

    def 搜索(self, 关键词: str) -> List[dict]:
        """v1.1: 轻量搜索——索引元数据优先，命中才加载卡体"""
        results = []
        for cid, meta in self.index.get("cards", {}).items():
            # 一级过滤：从索引元数据快速筛（纯内存，0次IO）
            quick_hits = [cid, meta.get("一句话",""), meta.get("短码","")]
            if not any(关键词 in str(h).lower() for h in quick_hits):
                continue
            # 二级：加载卡体全字段验证（缓存兜底）
            c = self.查卡(cid)
            if c:
                text = json.dumps(c, ensure_ascii=False)
                if 关键词.lower() in text.lower():
                    results.append(c)
        return results

    def 导出索引CSV(self, path: str = None) -> Path:
        if path is None:
            path = self.state_dir / "card_index.csv"
        else:
            path = Path(path)
        with open(path, "w") as f:
            f.write("ID,一句话,八卦,档级,I值,σ,三色,时间\n")
            for cid, info in self.index["cards"].items():
                f.write(f"{cid},{info.get('一句话','')},{info.get('八卦分区','')},"
                        f"{info.get('档级','')},{info.get('重要性I',0):.3f},"
                        f"{info.get('sigma',0):.4f},{info.get('三色','')},{info.get('时间戳','')}\n")
        return Path(path)


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

def main():
    mgr = 压缩卡管理器()

    if len(sys.argv) < 2:
        print(__doc__)
        print(f"\n📊 压缩卡总数: {mgr.index.get('total', 0)}")
        for c in mgr.列表()[:5]:
            print(f"  [{c.get('八卦分区','?')}] {c.get('一句话','')[:60]}")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "create":
        if len(sys.argv) < 3:
            print("用法: python3 bin/lh_compression_card.py create <文件路径> [档级]")
            sys.exit(1)
        src = sys.argv[2]
        tier = sys.argv[3] if len(sys.argv) > 3 else "常规"

        if Path(src).exists():
            text = Path(src).read_text(encoding="utf-8")
        else:
            text = src

        result = mgr.创建压缩卡(来源文件=src, 原文=text, 档=tier)
        if "error" in result:
            print(f"❌ {result['error']}")
            sys.exit(1)
        print(f"✅ 压缩卡已创建: {result['id']}")
        print(f"   路径: {result['路径']}")
        print(f"   双封装: M:: + CNSH::")

    elif cmd == "show":
        if len(sys.argv) < 3:
            print("用法: python3 bin/lh_compression_card.py show <卡ID>")
            sys.exit(1)
        card = mgr.查卡(sys.argv[2])
        if not card:
            print(f"❌ 卡不存在: {sys.argv[2]}")
            sys.exit(1)
        c = 压缩卡.from_dict(card)
        print(c.卡面())

    elif cmd == "index":
        print(f"📊 压缩卡索引 ({mgr.index.get('total', 0)}张)")
        for cid, info in sorted(mgr.index["cards"].items()):
            print(f"  [{info.get('八卦分区','?')}] {cid[:20]}... | {info.get('一句话','')[:40]}")

    elif cmd == "search":
        if len(sys.argv) < 3:
            print("用法: python3 bin/lh_compression_card.py search <关键词>")
            sys.exit(1)
        results = mgr.搜索(sys.argv[2])
        print(f"🔍 找到 {len(results)} 张卡")
        for c in results:
            print(f"  [{c.get('八卦分区','?')}] {c.get('id','')[:20]}... | {c.get('一句话','')[:60]}")

    elif cmd == "export-csv":
        path = mgr.导出索引CSV(sys.argv[2] if len(sys.argv) > 2 else None)
        print(f"✅ CSV导出: {path}")

    elif cmd == "dual":
        """输出双封装格式"""
        if len(sys.argv) < 3:
            print("用法: python3 bin/lh_compression_card.py dual <卡ID>")
            sys.exit(1)
        card = mgr.查卡(sys.argv[2])
        if not card:
            print(f"❌ 卡不存在: {sys.argv[2]}")
            sys.exit(1)
        c = 压缩卡.from_dict(card)
        print(json.dumps(c.双封装(), ensure_ascii=False, indent=2))

    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
