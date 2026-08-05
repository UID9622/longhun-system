#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-07-11-CS-LEARNING-ENGINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     龍魂·计算机知识卡片学习引擎 v1.0 — 142张卡片·智能学习路径·进度追踪        ║
║     CS Knowledge Card Learning Engine · SQLite+FTS5+CNSH Router         ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️2026-07-11-CS-LEARNING-ENGINE-v1.0                          ║
║  源矿: backups/cs-kb-enhanced-20260701/cs_kb.db (306条知识卡片)           ║
║  引擎: cnsh/core/longhun_cs_kb.py (FTS5全文搜索·分类查询·公式路由)          ║
║  铁律: 本地数据·不联网·学习路径基于龍魂算法                                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║  用法:                                                                   ║
║    python3 bin/lh_cs_learning_engine.py --interactive                    ║
║    python3 bin/lh_cs_learning_engine.py --search "路由算法"               ║
║    python3 bin/lh_cs_learning_engine.py --category "数据与人工智能"        ║
║    python3 bin/lh_cs_learning_engine.py --path "机器学习" --level 3       ║
║    python3 bin/lh_cs_learning_engine.py --stats                          ║
║    python3 bin/lh_cs_learning_engine.py --quiz 5                         ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import argparse
import json
import random
import sqlite3
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field

# 确保能 import cnsh/core 模块
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cnsh" / "core"))

try:
    from cnsh_core.longhun_cs_kb import load_db, search, query_by_category, query_by_id, embed_summary
except ImportError:
    # fallback: 直接使用 sqlite3
    DB_PATH = ROOT / "backups" / "cs-kb-enhanced-20260701" / "cs_kb.db"
    
    def load_db():
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn
    
    def query_by_category(cat, limit=50, conn=None):
        should_close = conn is None
        if conn is None: conn = load_db()
        try:
            rows = conn.execute(
                'SELECT * FROM cs_kb WHERE "category" = ? LIMIT ?', (cat, limit)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            if should_close: conn.close()
    
    def query_by_id(cid, conn=None):
        should_close = conn is None
        if conn is None: conn = load_db()
        try:
            row = conn.execute(
                'SELECT * FROM cs_kb WHERE "card_id" = ?', (str(cid),)
            ).fetchone()
            return dict(row) if row else None
        finally:
            if should_close: conn.close()
    
    def search(q, limit=20, conn=None):
        should_close = conn is None
        if conn is None: conn = load_db()
        try:
            pattern = f"%{q}%"
            rows = conn.execute(
                '''SELECT * FROM cs_kb
                   WHERE "name" LIKE ? OR "description" LIKE ? OR "context_trigger" LIKE ?
                   LIMIT ?''',
                (pattern, pattern, pattern, limit),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            if should_close: conn.close()
    
    def embed_summary(conn=None):
        should_close = conn is None
        if conn is None: conn = load_db()
        try:
            total = conn.execute('SELECT COUNT(*) FROM cs_kb').fetchone()[0]
            分类 = {}
            rows = conn.execute('SELECT category, COUNT(*) FROM cs_kb GROUP BY category').fetchall()
            for r in rows:
                分类[r[0]] = r[1]
            return {"total_records": total, "by_category": 分类}
        finally:
            if should_close: conn.close()


# ═══════════════════════════════════════════════════════════
# §1 学习路径定义
# ═══════════════════════════════════════════════════════════

# 预置学习路径：按领域→推荐卡片ID序列
LEARNING_PATHS = {
    "Python入门": {
        "描述": "从零开始学Python编程",
        "卡片序列": ["10", "2", "3", "4", "5", "8", "12", "17", "18", "20"],
        "复杂度": "L1",
    },
    "数据结构与算法": {
        "描述": "核心数据结构+经典算法",
        "卡片序列": ["1", "3", "15", "23", "24", "25", "30", "31", "42", "45"],
        "复杂度": "L2",
    },
    "机器学习入门": {
        "描述": "从线性回归到神经网络",
        "卡片序列": ["60", "61", "62", "63", "64", "70", "75", "79", "80", "85"],
        "复杂度": "L2-L3",
    },
    "深度学习": {
        "描述": "神经网络·CNN·RNN·Transformer",
        "卡片序列": ["85", "86", "87", "88", "89", "90", "91", "95", "100", "105"],
        "复杂度": "L3",
    },
    "网络安全基础": {
        "描述": "密码学·渗透·防御·取证",
        "卡片序列": ["40", "41", "42", "43", "44", "45", "46", "47", "48", "49"],
        "复杂度": "L2-L3",
    },
    "操作系统": {
        "描述": "进程线程·内存管理·文件系统",
        "卡片序列": ["11", "13", "14", "25", "26", "27", "28", "29", "32", "33"],
        "复杂度": "L2",
    },
    "数据库": {
        "描述": "SQL·NoSQL·索引·事务",
        "卡片序列": ["50", "51", "52", "53", "54", "55", "56", "57", "58", "59"],
        "复杂度": "L2",
    },
    "网络协议": {
        "描述": "TCP/IP·HTTP·DNS·OSI",
        "卡片序列": ["34", "35", "36", "37", "38", "39", "40", "41", "46", "48"],
        "复杂度": "L2",
    },
}


# ═══════════════════════════════════════════════════════════
# §2 学习引擎类
# ═══════════════════════════════════════════════════════════

@dataclass
class 学习进度:
    """单个学习者的进度追踪"""
    已完成卡片: List[str] = field(default_factory=list)
    学习中卡片: List[str] = field(default_factory=list)
    当前路径: str = ""
    路径进度: int = 0  # 当前学到第几张
    总学习时间分钟: int = 0
    测验历史: List[Dict] = field(default_factory=list)


class 学习引擎:
    """知识卡片学习引擎·SQLite+FTS5驱动"""
    
    def __init__(self):
        self.db = load_db()
        self.progress = 学习进度()
    
    def 获取统计(self) -> Dict[str, Any]:
        return embed_summary(self.db)
    
    def 搜索卡片(self, 关键词: str, limit: int = 10) -> List[Dict]:
        return search(关键词, limit=limit, conn=self.db)
    
    def 按分类获取(self, 分类: str, limit: int = 50) -> List[Dict]:
        return query_by_category(分类, limit=limit, conn=self.db)
    
    def 获取卡片详情(self, 卡片ID: str) -> Optional[Dict]:
        return query_by_id(卡片ID, conn=self.db)
    
    def 获取所有分类(self) -> List[Dict[str, Any]]:
        统计 = self.获取统计()
        分类列表 = []
        for 名, 数量 in 统计.get("by_category", {}).items():
            分类列表.append({"名称": 名, "卡片数": 数量})
        return sorted(分类列表, key=lambda x: x["卡片数"], reverse=True)
    
    def 获取学习路径(self, 路径名: str) -> Optional[Dict]:
        if 路径名 not in LEARNING_PATHS:
            return None
        路径 = LEARNING_PATHS[路径名]
        卡片详情 = []
        for cid in 路径["卡片序列"]:
            card = self.获取卡片详情(cid)
            if card:
                卡片详情.append({
                    "id": card["card_id"],
                    "名称": card.get("name", "?"),
                    "分类": card.get("category", "?"),
                    "状态": card.get("status", "未开始"),
                    "dr": card.get("dr_wuxing_gong", "?"),
                    "公式": card.get("formula", "")[:80] if card.get("formula") else "",
                })
        return {
            "路径名": 路径名,
            "描述": 路径["描述"],
            "复杂度": 路径["复杂度"],
            "卡片总数": len(路径["卡片序列"]),
            "卡片列表": 卡片详情,
            "原始ID序列": 路径["卡片序列"],
        }
    
    def 列出所有路径(self) -> List[str]:
        return list(LEARNING_PATHS.keys())
    
    def 生成测验(self, 数量: int = 5, 分类过滤: Optional[str] = None) -> List[Dict]:
        """随机生成知识测验题"""
        if 分类过滤:
            cards = query_by_category(分类过滤, limit=100, conn=self.db)
        else:
            conn = self.db
            rows = conn.execute('SELECT * FROM cs_kb ORDER BY RANDOM() LIMIT ?', (数量 * 3,)).fetchall()
            cards = [dict(r) for r in rows]
        
        if len(cards) < 数量:
            数量 = len(cards)
        
        选题 = random.sample(cards, min(数量, len(cards)))
        测验 = []
        
        for card in 选题:
            # 生成一个简单问题
            name = card.get("name", "未知")
            desc = card.get("description", "")
            category = card.get("category", "")
            formula = card.get("formula", "")
            
            # 问题类型随机
            q_type = random.choice(["分类", "概念", "应用", "公式"])
            
            if q_type == "分类" and category:
                question = f"「{name}」属于哪个知识分类？"
                # 生成错误选项
                其他分类 = self.获取所有分类()
                错误选项 = [c["名称"] for c in 其他分类 if c["名称"] != category][:3]
                options = 错误选项 + [category]
                random.shuffle(options)
                answer = category
            elif q_type == "公式" and formula:
                question = f"「{name}」的核心公式/定理是什么？"
                answer = formula[:120]
                options = None
            elif q_type == "概念" and desc:
                question = f"以下哪个描述最符合「{name}」？"
                answer = desc[:80]
                options = None
            else:
                question = f"「{name}」主要应用在什么场景？"
                answer = card.get("context_trigger", desc)[:80]
                options = None
            
            测验.append({
                "卡片ID": card.get("card_id"),
                "知识点": name,
                "分类": category,
                "问题": question,
                "答案": answer,
                "选项": options,
                "dr": card.get("dr_wuxing_gong", ""),
                "类型": q_type,
            })
        
        return 测验
    
    def 推荐学习路径(self, 兴趣领域: str, 当前水平: str = "入门") -> List[Dict]:
        """根据兴趣关键词推荐学习路径"""
        # 先搜索匹配的卡片
        cards = self.搜索卡片(兴趣领域, limit=10)
        if not cards:
            return []
        
        推荐 = []
        for card in cards[:5]:
            推荐.append({
                "卡片ID": card.get("card_id"),
                "知识点": card.get("name"),
                "分类": card.get("category"),
                "dr五行": card.get("dr_wuxing_gong"),
                "状态": card.get("status", "未开始"),
                "描述": (card.get("description") or "")[:100],
            })
        
        return 推荐
    
    def 技能雷达(self, 已完成分类: Dict[str, int]) -> Dict[str, Any]:
        """输入每个分类学完的数量·输出雷达数据+缺口分析"""
        统计 = self.获取统计()
        总分类 = 统计.get("by_category", {})
        
        雷达数据 = {}
        缺口分析 = []
        
        for 分类名, 总数 in 总分类.items():
            已学 = 已完成分类.get(分类名, 0)
            覆盖率 = 已学 / 总数 if 总数 > 0 else 0
            雷达数据[分类名] = {
                "已学": 已学,
                "总数": 总数,
                "覆盖率": round(覆盖率, 2),
            }
            if 覆盖率 < 0.2 and 总数 > 5:
                缺口分析.append({
                    "分类": 分类名,
                    "缺口": 总数 - 已学,
                    "建议": f"建议优先学习{分类名}·已覆盖仅{覆盖率*100:.0f}%",
                })
        
        return {
            "雷达": 雷达数据,
            "缺口": 缺口分析,
            "总掌握度": round(
                sum(v["覆盖率"] for v in 雷达数据.values()) / max(len(雷达数据), 1), 2
            ),
        }
    
    def __del__(self):
        try:
            self.db.close()
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════
# §3 格式化输出
# ═══════════════════════════════════════════════════════════

def 打印统计(引擎: 学习引擎):
    统计 = 引擎.获取统计()
    print("\n" + "=" * 64)
    print("  📚 龍魂·计算机知识卡片库")
    print(f"  总卡片数: {统计.get('total_records', '?')}")
    print("=" * 64)
    
    print("\n  📂 分类分布:")
    for 分类, 数量 in sorted(统计.get("by_category", {}).items(), key=lambda x: x[1], reverse=True):
        bar = "█" * min(数量, 30)
        print(f"  {分类:　<14s} {bar} {数量}张")
    
    print("\n  📖 学习路径:")
    for 路径名 in LEARNING_PATHS:
        p = LEARNING_PATHS[路径名]
        print(f"  • {路径名} [{p['复杂度']}] — {p['描述']} ({len(p['卡片序列'])}张卡片)")
    
    print("\n" + "=" * 64 + "\n")


def 打印搜索结果(结果: List[Dict], 关键词: str):
    print(f"\n🔍 搜索「{关键词}」· 找到 {len(结果)} 条结果:\n")
    for i, card in enumerate(结果, 1):
        print(f"  [{i}] {card.get('card_id')}. {card.get('name', '?')}")
        print(f"      分类: {card.get('category', '?')}  |  {card.get('dr_wuxing_gong', '?')}")
        desc = card.get('description', '')
        if desc:
            print(f"      {desc[:100]}...")
        print()


def 打印分类卡片(结果: List[Dict], 分类名: str):
    print(f"\n📂 分类「{分类名}」· {len(结果)} 张卡片:\n")
    for card in 结果[:20]:
        print(f"  [{card.get('card_id'):>4s}] {card.get('name', '?'):　<30s} {card.get('dr_wuxing_gong', '?'):　<25s}")
    
    if len(结果) > 20:
        print(f"  ... 还有 {len(结果) - 20} 张卡片")


def 打印学习路径(路径: Dict):
    print("\n" + "=" * 64)
    print(f"  📖 学习路径: {路径['路径名']}")
    print(f"  描述: {路径['描述']}")
    print(f"  复杂度: {路径['复杂度']}")
    print(f"  卡片总数: {路径['卡片总数']}")
    print("=" * 64)
    
    print(f"\n  📋 学习序列:\n")
    for i, card in enumerate(路径["卡片列表"], 1):
        status_icon = {"已完成": "✅", "学习中": "📖", "未开始": "⬜"}.get(card.get("状态", "未开始"), "⬜")
        print(f"  {status_icon} {i:2d}. [{card['id']:>4s}] {card['名称']:　<30s} {card['dr']}")
        if card.get("公式"):
            print(f"       公式: {card['公式']}")
    
    print("\n" + "=" * 64 + "\n")


def 打印测验(测验: List[Dict]):
    print("\n" + "=" * 64)
    print(f"  📝 龍魂知识测验 · {len(测验)}题")
    print("=" * 64)
    
    for i, q in enumerate(测验, 1):
        print(f"\n  Q{i}. {q['问题']}")
        print(f"      知识点: {q['知识点']} ({q['分类']})")
        if q['选项']:
            for j, opt in enumerate(q['选项']):
                字母 = chr(65 + j)
                print(f"      {字母}) {opt}")
            print(f"  ✅ 正确答案: {q['答案']}")
        else:
            print(f"  ✅ 参考答案: {q['答案']}")
    
    print("\n" + "=" * 64)
    print("  💡 提示: 用 --quiz N 生成N道题·用 --save 保存到文件")
    print("=" * 64 + "\n")


def 打印推荐(推荐: List[Dict], 兴趣: str):
    print(f"\n🎯 根据「{兴趣}」·推荐以下学习路径:\n")
    for i, rec in enumerate(推荐, 1):
        print(f"  [{i}] [{rec['卡片ID']}] {rec['知识点']}")
        print(f"      分类: {rec['分类']}  |  {rec['dr五行']}")
        if rec.get('描述'):
            print(f"      {rec['描述']}...")
        print()


def 打印雷达(雷达结果: Dict):
    print("\n" + "=" * 64)
    print(f"  🎯 技能雷达 · 总掌握度: {雷达结果['总掌握度']*100:.0f}%")
    print("=" * 64)
    
    print("\n  各领域覆盖率:\n")
    for 分类, 数据 in sorted(雷达结果["雷达"].items(), key=lambda x: x[1]["覆盖率"], reverse=True):
        bar_len = int(数据["覆盖率"] * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {分类:　<14s} {bar} {数据['覆盖率']*100:5.1f}%  ({数据['已学']}/{数据['总数']})")
    
    if 雷达结果["缺口"]:
        print("\n  ⚠️ 知识缺口:\n")
        for gap in 雷达结果["缺口"][:5]:
            print(f"  • {gap['分类']}: 缺口{gap['缺口']}张 — {gap['建议']}")
    
    print("\n" + "=" * 64 + "\n")


# ═══════════════════════════════════════════════════════════
# §4 CLI
# ═══════════════════════════════════════════════════════════

def 主函数():
    parser = argparse.ArgumentParser(
        description="龍魂·计算机知识卡片学习引擎 — 142张卡片·智能路径·进度追踪",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_cs_learning_engine.py --stats
  python3 bin/lh_cs_learning_engine.py --search "排序算法"
  python3 bin/lh_cs_learning_engine.py --category "数据与人工智能"
  python3 bin/lh_cs_learning_engine.py --path "Python入门"
  python3 bin/lh_cs_learning_engine.py --quiz 10
  python3 bin/lh_cs_learning_engine.py --recommend "机器学习"
  python3 bin/lh_cs_learning_engine.py --radar '{"基础理论":5,"编程与开发":2}'
  python3 bin/lh_cs_learning_engine.py --interactive
        """,
    )
    parser.add_argument("--stats", "-s", action="store_true", help="显示卡片库统计信息")
    parser.add_argument("--search", "-q", help="全文搜索知识卡片")
    parser.add_argument("--category", "-c", help="按分类列出卡片")
    parser.add_argument("--path", "-p", choices=list(LEARNING_PATHS.keys()) if LEARNING_PATHS else None, help="显示学习路径")
    parser.add_argument("--list-paths", action="store_true", help="列出所有学习路径")
    parser.add_argument("--quiz", "-z", type=int, help="生成N道随机测验题")
    parser.add_argument("--recommend", "-r", help="根据兴趣推荐学习路径")
    parser.add_argument("--radar", help='输入已完成分类的JSON·输出技能雷达（格式: {"分类名":已学数量,...}）')
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式模式")
    parser.add_argument("--save", help="保存结果到JSON文件")
    parser.add_argument("--json", "-j", action="store_true", help="输出纯JSON")
    args = parser.parse_args()
    
    引擎 = 学习引擎()
    output = None
    
    try:
        if args.stats:
            if args.json:
                output = 引擎.获取统计()
                print(json.dumps(output, ensure_ascii=False, indent=2))
            else:
                打印统计(引擎)
        
        elif args.search:
            结果 = 引擎.搜索卡片(args.search)
            if args.json:
                print(json.dumps(结果, ensure_ascii=False, indent=2))
            else:
                打印搜索结果(结果, args.search)
            output = 结果
        
        elif args.category:
            结果 = 引擎.按分类获取(args.category)
            if args.json:
                print(json.dumps(结果, ensure_ascii=False, indent=2))
            else:
                打印分类卡片(结果, args.category)
            output = 结果
        
        elif args.path:
            路径 = 引擎.获取学习路径(args.path)
            if args.json:
                print(json.dumps(路径, ensure_ascii=False, indent=2))
            else:
                打印学习路径(路径)
            output = 路径
        
        elif args.list_paths:
            paths = 引擎.列出所有路径()
            print("\n📖 可用学习路径:\n")
            for p in paths:
                info = LEARNING_PATHS[p]
                print(f"  • {p} [{info['复杂度']}] — {info['描述']} ({len(info['卡片序列'])}张)")
            print()
        
        elif args.quiz:
            测验 = 引擎.生成测验(args.quiz)
            if args.json:
                print(json.dumps(测验, ensure_ascii=False, indent=2))
            else:
                打印测验(测验)
            output = 测验
        
        elif args.recommend:
            推荐 = 引擎.推荐学习路径(args.recommend)
            if args.json:
                print(json.dumps(推荐, ensure_ascii=False, indent=2))
            else:
                打印推荐(推荐, args.recommend)
            output = 推荐
        
        elif args.radar:
            try:
                已完成 = json.loads(args.radar)
            except json.JSONDecodeError:
                print('''⚠️ 雷达参数格式错误·请输入合法JSON如 {"分类":数量,...}''')
                return
            雷达结果 = 引擎.技能雷达(已完成)
            if args.json:
                print(json.dumps(雷达结果, ensure_ascii=False, indent=2))
            else:
                打印雷达(雷达结果)
            output = 雷达结果
        
        elif args.interactive:
            交互模式(引擎)
        
        else:
            parser.print_help()
        
        if args.save and output:
            with open(args.save, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
            print(f"✅ 已保存: {args.save}")
    
    finally:
        del 引擎


def 交互模式(引擎: 学习引擎):
    """简易交互式菜单"""
    print("\n" + "=" * 64)
    print("  🐉 龍魂·计算机知识卡片学习引擎 · 交互模式")
    print("=" * 64)
    
    while True:
        print("\n  选项:")
        print("    [1] 查看卡片库统计")
        print("    [2] 搜索知识卡片")
        print("    [3] 浏览分类")
        print("    [4] 查看学习路径")
        print("    [5] 生成知识测验")
        print("    [6] 兴趣推荐")
        print("    [7] 技能雷达")
        print("    [0] 退出")
        
        选择 = input("\n  请输入选项: ").strip()
        
        if 选择 == "0":
            print("  再见 🐉\n")
            break
        elif 选择 == "1":
            打印统计(引擎)
        elif 选择 == "2":
            关键词 = input("  搜索关键词: ").strip()
            if 关键词:
                结果 = 引擎.搜索卡片(关键词)
                打印搜索结果(结果, 关键词)
        elif 选择 == "3":
            分类列表 = 引擎.获取所有分类()
            print("\n  📂 知识分类:\n")
            for i, c in enumerate(分类列表, 1):
                print(f"  [{i}] {c['名称']} ({c['卡片数']}张)")
            子选择 = input("\n  选择分类编号（回车返回）: ").strip()
            if 子选择.isdigit():
                idx = int(子选择) - 1
                if 0 <= idx < len(分类列表):
                    结果 = 引擎.按分类获取(分类列表[idx]["名称"])
                    打印分类卡片(结果, 分类列表[idx]["名称"])
        elif 选择 == "4":
            paths = 引擎.列出所有路径()
            print("\n  📖 学习路径:\n")
            for i, p in enumerate(paths, 1):
                info = LEARNING_PATHS[p]
                print(f"  [{i}] {p} [{info['复杂度']}] — {info['描述']}")
            子选择 = input("\n  选择路径编号（回车返回）: ").strip()
            if 子选择.isdigit():
                idx = int(子选择) - 1
                if 0 <= idx < len(paths):
                    路径 = 引擎.获取学习路径(paths[idx])
                    打印学习路径(路径)
        elif 选择 == "5":
            数量 = input("  生成几道题？(默认5): ").strip()
            n = int(数量) if 数量.isdigit() else 5
            测验 = 引擎.生成测验(n)
            打印测验(测验)
        elif 选择 == "6":
            兴趣 = input("  你感兴趣的方向: ").strip()
            if 兴趣:
                推荐 = 引擎.推荐学习路径(兴趣)
                打印推荐(推荐, 兴趣)
        elif 选择 == "7":
            print("\n  输入每个分类已学数量（JSON格式）")
            print('  例: {"基础理论":5,"编程与开发":3}')
            雷达输入 = input("  > ").strip()
            try:
                已完成 = json.loads(雷达输入)
                雷达结果 = 引擎.技能雷达(已完成)
                打印雷达(雷达结果)
            except json.JSONDecodeError:
                print("  ⚠️ 格式错误")


if __name__ == "__main__":
    主函数()
