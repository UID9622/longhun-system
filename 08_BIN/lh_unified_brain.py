#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·甲辰·離為火-UNIFIED-BRAIN-v1.0-e5f6g7h8
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·统一中枢引擎 v1.0
━━━━━━━━━━━━━━━━━━━━
全项目 2,723 脚本统一编排 · 一键调度 · 状态全景 · 去重归集

用法:
    lh brain                     # 交互式控制台
    lh brain status              # 全系统状态面板
    lh brain find <关键词>        # 搜索匹配引擎
    lh brain run <引擎名>         # 运行指定引擎
    lh brain dupes               # 显示重复冗余脚本
    lh brain scan                # 重新扫描注册表
    lh brain health              # 系统健康检查
    lh brain api-list            # 列出所有API服务
    lh brain route <意图描述>     # 智能路由到对应引擎

可作为模块导入:
    from lh_unified_brain import UnifiedBrain
    brain = UnifiedBrain()
    brain.find("视频")          # → 匹配引擎列表
    brain.dispatch("audit")     # → 执行审计引擎
"""

import os, sys, json, subprocess, time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

REGISTRY_PATH = ROOT / "data" / "engine_registry.json"

# ─── 引擎快捷别名 ───
QUICK_ALIASES = {
    # 高频命令 → 引擎映射
    "审计": "bin/lh_three_color_audit.py",
    "三色审计": "bin/lh_three_color_audit.py",
    "安全扫描": "bin/lh_full_system_audit.py",
    "健康检查": "bin/lh_health_checker.py",
    "系统状态": "bin/lh_system_status.py",
    "记忆加载": "bin/lh_memory_load.py",
    "对齐检查": "bin/lh_align_checker.py",
    "对齐修复": "bin/lh_align.py",
    "GPG签名": "bin/lh_gpg_sign.py",
    "DNA生成": "bin/lh_dna_generator.py",
    "部署": "deploy/sync-to-kunpeng.sh",
    "鲲鹏同步": "deploy/sync-to-kunpeng.sh",
    "训练": "bin/lh_lora_trainer.py",
    "视频": "bin/lh_video_studio.py",
    "防火墙": "bin/lh_regulatory_firewall.py",
    "镜像指数": "bin/lh_mirror_index.py",
    "主权守护": "bin/lh_sovereignty_guard.py",
    "浏览器史官": "bin/lh_browser_historian.py",
    "通心译": "bin/lh_tongxinyi_translator.py",
    "搜索引擎": "bin/lh_search_engine.py",
    "知识中枢": "bin/lh_knowledge_hub_api.py",
    "意念引擎": "bin/lh_intent_engine.py",
    "投喂宝宝": "bin/lh_feed_baby.py",
    "量子引擎": "bin/lh_quantum_core.py",
    "知识蒸馏": "bin/lh_knowledge_distiller.py",
    "人格编排": "bin/lh_persona_orchestrator.py",
    "沙盒推演": "bin/lh_sandbox_engine.py",
    "定价审计": "bin/lh_audit_price_engine.py",
    "CNSH编译": "bin/cnsh_compiler.py",
}

# ─── 意图→引擎 自然语言路由 ───
INTENT_ROUTES = {
    "安全": ["安全审计", "安全扫描", "防火墙", "主权守护", "GPG签名"],
    "审计": ["审计", "三色审计", "定价审计", "安全扫描"],
    "训练": ["训练", "数据", "学习"],
    "视频": ["视频", "媒体", "3D"],
    "知识": ["知识中枢", "知识蒸馏", "搜索引擎", "浏览器史官"],
    "记忆": ["记忆加载", "记忆归档", "同步"],
    "部署": ["部署", "鲲鹏同步", "健康检查"],
    "代码": ["CNSH编译", "对齐检查", "对齐修复"],
    "人格": ["人格编排", "投喂宝宝", "意念引擎", "通心译"],
    "量子": ["量子引擎", "沙盒推演", "推演"],
    "诊断": ["健康检查", "系统状态", "镜像指数"],
}


class UnifiedBrain:
    """龍魂统一中枢"""

    def __init__(self):
        self.registry: Dict = {}
        self.engines: List[Dict] = []
        self.loaded = False
        self.aliases = dict(QUICK_ALIASES)

    def load(self, force_scan: bool = False):
        """加载注册表"""
        if force_scan or not REGISTRY_PATH.exists():
            self._scan()
        try:
            self.registry = json.loads(REGISTRY_PATH.read_text(encoding='utf-8'))
            self.engines = self.registry.get("engines", [])
            self.stats = self.registry.get("stats", {})
            self.loaded = True
            return True
        except Exception as e:
            print(f"❌ 加载注册表失败: {e}")
            return False

    def _scan(self):
        """触发扫描"""
        print("🔍 注册表不存在，正在扫描...")
        subprocess.run([sys.executable, str(ROOT / "bin" / "lh_engine_registry.py"), "scan"],
                       cwd=str(ROOT))

    # 中文关键词 → 英文搜索词映射
    _CN_KW_MAP = {
        "视频": ["video", "media", "visual", "avatar", "commentary", "3d", "image", "voice", "audio", "movie"],
        "安全": ["audit", "security", "guard", "firewall", "shield", "defend", "sovereign", "fuse", "meltdown", "patrol"],
        "审计": ["audit", "governance", "verify", "validate"],
        "训练": ["train", "lora", "fine_tune", "mlx", "ollama", "checkpoint", "dataset", "sample"],
        "记忆": ["memory", "vault", "store", "archive", "snapshot", "sync", "backup"],
        "知识": ["knowledge", "learn", "corpus", "notion", "article", "document", "paper"],
        "部署": ["deploy", "setup", "install", "config", "systemd", "launchd"],
        "人格": ["persona", "agent", "orchestrat", "character", "emotion", "intent"],
        "推演": ["sandbox", "predict", "simulate", "quantum", "wuxing", "bagua", "iching"],
        "数据": ["data", "analy", "metric", "monitor", "dashboard", "report", "stats"],
        "代码": ["cnsh", "compiler", "interpreter", "syntax", "parser", "align"],
        "管理": ["manage", "governance", "admin", "config", "organize"],
        "搜索": ["search", "engine", "crawl", "browser"],
        "同步": ["sync", "bridge", "integrat", "migrate", "import", "export"],
        "CNSH": ["cnsh", "compiler", "interpreter", "parser", "syntax"],
        "API": ["api", "server", "fastapi", "flask", "gateway", "endpoint", "web"],
        "AI": ["train", "lora", "fine_tune", "mlx", "ollama", "agent"],
    }

    def find(self, keyword: str, limit: int = 20) -> List[Dict]:
        """搜索引擎 — 支持中文关键词自动映射"""
        if not self.loaded:
            self.load()
        kw = keyword.lower()
        results = []
        seen = set()

        # 构建搜索词列表（原始 + 中文映射后的英文词）
        search_terms = [kw]
        for cn, en_list in self._CN_KW_MAP.items():
            if cn.lower() in kw or kw in cn.lower():
                search_terms.extend(en_list)

        for e in self.engines:
            score = 0
            name_lower = e["name"].lower()
            cat_lower = e.get("category", "").lower()
            path_lower = e["path"].lower()

            # 多关键词匹配
            for term in search_terms:
                if term == name_lower:
                    score += 100
                elif term in name_lower:
                    score += 50
                # 搜索分类标签（中文分类名）
                if term in cat_lower:
                    score += 15
                # 搜索路径
                if term in path_lower:
                    score += 10
                # 搜索类名/函数名
                if any(term in c.lower() for c in e.get("classes", [])):
                    score += 8
                if any(term in f.lower() for f in e.get("functions", [])):
                    score += 5

            if score > 0 and e["path"] not in seen:
                seen.add(e["path"])
                results.append((score, e))

        results.sort(key=lambda x: -x[0])
        return [r[1] for r in results[:limit]]

    def dispatch(self, name_or_keyword: str, *extra_args) -> Tuple[bool, str]:
        """智能调度：根据名称或关键词找到对应引擎并返回执行命令"""
        if not self.loaded:
            self.load()

        # 1. 先查别名
        if name_or_keyword in self.aliases:
            target = self.aliases[name_or_keyword]
            return True, f"python3 {target}"

        # 2. 精确匹配引擎名
        for e in self.engines:
            if e["name"] == name_or_keyword:
                return True, f"python3 {e['path']}"

        # 3. 模糊匹配
        results = self.find(name_or_keyword, limit=5)
        if results:
            return True, f"python3 {results[0]['path']}"

        # 4. 意图路由
        for intent, keywords in INTENT_ROUTES.items():
            if intent in name_or_keyword or name_or_keyword in intent:
                for kw in keywords:
                    if kw in self.aliases:
                        return True, f"python3 {self.aliases[kw]}"
                    res = self.find(kw, limit=1)
                    if res:
                        return True, f"python3 {res[0]['path']}"

        return False, f"未找到匹配引擎: {name_or_keyword}"

    def run(self, name_or_keyword: str, *extra_args) -> int:
        """查找并执行引擎"""
        ok, cmd = self.dispatch(name_or_keyword)
        if not ok:
            print(f"❌ {cmd}")
            return 1

        full_cmd = f"{cmd} {' '.join(extra_args)}"
        print(f"🚀 {full_cmd}")
        return subprocess.run(full_cmd, shell=True, cwd=str(ROOT)).returncode

    def status_dashboard(self) -> str:
        """全系统状态面板"""
        if not self.loaded:
            self.load()

        s = self.stats
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        lines = [
            "╔══════════════════════════════════════════════════╗",
            "║        🐉 龍魂·统一中枢 · 全系统状态             ║",
            "╠══════════════════════════════════════════════════╣",
            f"║  扫描时间: {s.get('scan_time', 'N/A')[:19]}                    ║",
            f"║  当前时间: {now}                    ║",
            "╠══════════════════════════════════════════════════╣",
            f"║  📦 注册脚本: {s.get('total_registered', 0):,} 个                          ║",
            f"║  📝 代码行数: {s.get('total_lines', 0):,} 行                       ║",
            f"║  💾 代码量:   {s.get('total_size_mb', 0)} MB                         ║",
            f"║  ⚡ 可执行:   {s.get('executable_count', 0):,} 个                       ║",
            f"║  🌐 API服务:  {s.get('api_count', 0)} 个                           ║",
            f"║  🧬 DNA签名:  {s.get('has_dna', 0):,} 个                        ║",
            f"║  🔄 多版本组: {s.get('duplicate_groups', 0)} 组                        ║",
            "╠══════════════════════════════════════════════════╣",
        ]

        # 分类分布
        for cat, cnt in sorted(s.get("by_category", {}).items(), key=lambda x: -x[1])[:8]:
            bar_len = min(cnt // 10, 30)
            bar = "█" * bar_len
            lines.append(f"║  {cat}: {cnt:>4} {bar}")

        lines.append("╠══════════════════════════════════════════════════╣")

        # 目录分布
        for d, cnt in sorted(s.get("by_directory", {}).items(), key=lambda x: -x[1]):
            lines.append(f"║  {d}/ : {cnt}")

        lines.append("╚══════════════════════════════════════════════════╝")
        return "\n".join(lines)

    def api_list(self) -> List[Dict]:
        """列出所有API服务"""
        if not self.loaded:
            self.load()
        return [e for e in self.engines if "api" in e.get("entry_type", "")]

    def dupes_report(self, limit: int = 30) -> List[Dict]:
        """重复冗余报告"""
        if not self.loaded:
            self.load()
        dups = self.registry.get("duplicates", [])
        return [d for d in dups if d["type"] == "multi_version"][:limit]

    def health_check(self) -> Dict:
        """系统健康检查 — 五维体检"""
        if not self.loaded:
            self.load()
        s = self.stats
        checks = {}
        total = s.get("total_registered", 1)
        dna_count = s.get("has_dna", 0)
        dna_rate = dna_count / max(total, 1) * 100

        # 检查1: 注册表新鲜度
        scan_time = s.get("scan_time", "")
        age_hours = 0
        if scan_time:
            try:
                st = datetime.fromisoformat(scan_time)
                age_hours = (datetime.now() - st).total_seconds() / 3600
            except:
                pass
        checks["register_fresh"] = {
            "status": "🟢" if age_hours < 24 else ("🟡" if age_hours < 72 else "🔴"),
            "label": "注册表新鲜度",
            "value": f"{age_hours:.0f}h" if age_hours else "未知",
            "ok": age_hours < 24,
        }

        # 检查2: 多版本冗余
        dup_groups = s.get("duplicate_groups", 0)
        dup_severity = "🟢" if dup_groups < 100 else ("🟡" if dup_groups < 300 else "🔴")
        checks["duplicates"] = {
            "status": dup_severity,
            "label": "多版本冗余",
            "value": f"{dup_groups}组",
            "ok": dup_groups < 100,
            "detail": f"建议归档旧版本，保留最新1-2个版本"
        }

        # 检查3: API服务
        api_count = s.get("api_count", 0)
        api_severity = "🟢" if api_count < 50 else ("🟡" if api_count < 100 else "🔴")
        checks["api_count"] = {
            "status": api_severity,
            "label": "API服务数",
            "value": f"{api_count}个",
            "ok": api_count < 50,
            "detail": f"多服务可能端口冲突，建议归并"
        }

        # 检查4: DNA签名率
        missing_dna = total - dna_count
        dna_severity = "🟢" if dna_rate >= 90 else ("🟡" if dna_rate >= 70 else "🔴")
        checks["dna_rate"] = {
            "status": dna_severity,
            "label": "DNA签名率",
            "value": f"{dna_rate:.1f}%",
            "ok": dna_rate >= 90,
            "detail": f"缺失DNA: {missing_dna}个脚本 ({missing_dna/total*100:.1f}%)"
        }

        # 检查5: 可执行率
        exec_count = s.get("executable_count", 0)
        exec_rate = exec_count / max(total, 1) * 100
        checks["exec_rate"] = {
            "status": "🟢" if exec_rate > 50 else "🟡",
            "label": "可执行率",
            "value": f"{exec_rate:.1f}% ({exec_count}/{total})",
            "ok": exec_rate > 50,
        }

        # 综合判定
        ok_count = sum(1 for c in checks.values() if c["ok"])
        bad_count = sum(1 for c in checks.values() if c["status"] == "🔴")
        warn_count = sum(1 for c in checks.values() if c["status"] == "🟡")

        if bad_count > 0:
            status = "🔴"
        elif warn_count > 1:
            status = "🟡"
        else:
            status = "🟢"

        return {
            "status": status,
            "ok": ok_count,
            "total_checks": len(checks),
            "checks": checks,
            "scan_age_hours": age_hours,
            "dna_rate": round(dna_rate, 1),
            "dna_missing": missing_dna,
            "dup_groups": dup_groups,
            "api_count": api_count,
            "exec_rate": round(exec_rate, 1),
        }

    def smart_route(self, intent: str) -> List[Tuple[str, str]]:
        """智能意图路由 → 返回 [(引擎名, 路径), ...]"""
        suggestions = []
        seen_paths = set()
        intent_lower = intent.lower()

        # 1. 中文关键词映射 → 搜索
        for cn, en_list in self._CN_KW_MAP.items():
            if cn in intent_lower or intent_lower in cn:
                for en_kw in en_list[:5]:  # 取前5个英文关键词搜索
                    for e in self.engines:
                        if en_kw in e["name"].lower() and e["path"] not in seen_paths:
                            seen_paths.add(e["path"])
                            suggestions.append((e["name"], e["path"]))

        # 2. 意图分类匹配
        if not suggestions:
            for category, keywords in INTENT_ROUTES.items():
                if category in intent_lower or any(kw.lower() in intent_lower for kw in keywords):
                    for kw in keywords:
                        if kw in self.aliases and self.aliases[kw] not in seen_paths:
                            seen_paths.add(self.aliases[kw])
                            suggestions.append((kw, self.aliases[kw]))
                        else:
                            res = self.find(kw, limit=2)
                            for r in res:
                                if r["path"] not in seen_paths:
                                    seen_paths.add(r["path"])
                                    suggestions.append((r["name"], r["path"]))

        # 3. 直接搜索兜底
        if not suggestions:
            results = self.find(intent, limit=8)
            for r in results:
                if r["path"] not in seen_paths:
                    seen_paths.add(r["path"])
                    suggestions.append((r["name"], r["path"]))

        return suggestions[:10]


# ─── 交互控制台 ───
def interactive_console(brain: UnifiedBrain):
    """交互式控制台"""
    print(brain.status_dashboard())
    print("\n📋 快捷命令: find <关键词> | run <引擎> | dupes | health | api | route <意图> | help | quit")

    while True:
        try:
            cmd = input("\n🧠 brain> ").strip()
            if not cmd:
                continue
            parts = cmd.split(maxsplit=1)
            action = parts[0].lower()
            arg = parts[1] if len(parts) > 1 else ""

            if action in ("quit", "exit", "q"):
                print("👋 再见")
                break
            elif action == "help":
                print("""
╔══════════════════════════════════════════════╗
║  🧠 龍魂统一中枢 · 命令帮助                   ║
╠══════════════════════════════════════════════╣
║  status / st      全系统状态面板              ║
║  find <关键词>     搜索引擎                   ║
║  run <引擎名>      调度执行引擎               ║
║  dupes / dup      显示多版本冗余              ║
║  health / h       系统健康检查                ║
║  api              列出所有API服务             ║
║  route <意图>      智能意图路由               ║
║  scan             重新扫描注册表              ║
║  quick <关键词>    快捷别名执行               ║
╚══════════════════════════════════════════════╝""")
            elif action in ("status", "st"):
                print(brain.status_dashboard())
            elif action == "find":
                if not arg:
                    print("用法: find <关键词>")
                    continue
                results = brain.find(arg)
                print(f"\n🔍 '{arg}': {len(results)} 结果")
                for i, r in enumerate(results[:15], 1):
                    ver = f" [{r['version']}]" if r.get('version', 'unknown') != 'unknown' else ""
                    print(f"  {i:2}. {r['name']}{ver}  [{r['category']}]")
                    print(f"      {r['path']} ({r['size_kb']}KB)")
            elif action == "run":
                if not arg:
                    print("用法: run <引擎名或关键词>")
                    continue
                brain.run(arg)
            elif action in ("dupes", "dup"):
                dups = brain.dupes_report(20)
                print(f"\n🔍 多版本冗余: {len(dups)} 组 (显示前20)")
                for i, d in enumerate(dups, 1):
                    print(f"\n  {i}. {d['base']} ({d['count']} 版本)")
                    for p in d["paths"][:3]:
                        print(f"      - {p}")
            elif action in ("health", "h"):
                result = brain.health_check()
                print(f"\n🏥 健康检查: {result['status']}  {result['ok']}/{result['total_checks']}项通过")
                for key, c in result["checks"].items():
                    detail = f" — {c.get('detail', '')}" if c.get('detail') else ""
                    print(f"   {c['status']} {c['label']}: {c['value']}{detail}")
                if result["status"] == "🟢":
                    print("   ✅ 全项通过")
            elif action == "api":
                apis = brain.api_list()
                print(f"\n🌐 API服务: {len(apis)} 个")
                for a in apis:
                    print(f"   📡 {a['name']}  [{a['entry_type']}]")
                    print(f"      {a['path']} ({a['size_kb']}KB)")
            elif action == "route":
                if not arg:
                    print("用法: route <意图描述>")
                    continue
                suggestions = brain.smart_route(arg)
                print(f"\n🧭 意图 '{arg}' → 建议:")
                for name, path in suggestions:
                    print(f"   → {name}: python3 {path}")
            elif action == "scan":
                brain.load(force_scan=True)
                print(brain.status_dashboard())
            elif action == "quick":
                if not arg:
                    print("用法: quick <别名>  (可用别名: " + ", ".join(list(QUICK_ALIASES.keys())[:20]) + ")")
                    continue
                if arg in QUICK_ALIASES:
                    brain.run(arg)
                else:
                    print(f"❌ 未知别名: {arg}")
                    print(f"   可用: {', '.join(list(QUICK_ALIASES.keys()))}")
            else:
                # 尝试作为引擎名或关键词执行
                brain.run(action + (" " + arg if arg else ""))

        except KeyboardInterrupt:
            print("\n👋 再见")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


# ─── CLI ───
def main():
    import argparse
    p = argparse.ArgumentParser(
        description="龍魂·统一中枢引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh brain                    交互式控制台
  lh brain status             全系统状态
  lh brain find 视频          搜索视频相关引擎
  lh brain run 审计            执行审计引擎
  lh brain health             健康检查
  lh brain dupes              显示冗余
  lh brain route 安全检查      智能路由
        """
    )
    p.add_argument("action", nargs="?", default="interactive",
                   choices=["interactive", "status", "find", "run", "health", "dupes", "api", "route", "scan"])
    p.add_argument("args", nargs="*", help="额外参数")
    p.add_argument("--json", action="store_true", help="JSON输出")

    args = p.parse_args()
    brain = UnifiedBrain()

    if not brain.load():
        print("❌ 无法加载注册表")
        sys.exit(1)

    if args.action == "interactive":
        # 检测管道/非TTY → 自动输出状态后退
        if not sys.stdin.isatty():
            print(brain.status_dashboard())
            result = brain.health_check()
            print(f"\n🏥 {result['status']}  {result['ok']}/{result['total_checks']}项通过")
            print(f"   用法: lh brain status | find <关键词> | health | route <意图>")
            sys.exit(0)
        interactive_console(brain)

    elif args.action == "status":
        if args.json:
            print(json.dumps({
                "stats": brain.stats,
                "health": brain.health_check()
            }, ensure_ascii=False, indent=2))
        else:
            print(brain.status_dashboard())

    elif args.action == "find":
        keyword = " ".join(args.args) if args.args else ""
        if not keyword:
            print("❌ 请提供搜索关键词")
            sys.exit(1)
        results = brain.find(keyword)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"🔍 '{keyword}': {len(results)} 结果")
            for i, r in enumerate(results[:20], 1):
                ver = f" [{r['version']}]" if r.get('version', 'unknown') != 'unknown' else ""
                print(f"  {i:2}. {r['name']}{ver}  [{r['category']}]  {r['path']}")

    elif args.action == "run":
        target = " ".join(args.args) if args.args else ""
        if not target:
            print("❌ 请提供引擎名")
            sys.exit(1)
        sys.exit(brain.run(target))

    elif args.action == "health":
        result = brain.health_check()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"🏥 {result['status']}  {result['ok']}/{result['total_checks']}项通过")
            for key, c in result["checks"].items():
                detail = f" — {c.get('detail', '')}" if c.get('detail') else ""
                print(f"   {c['status']} {c['label']}: {c['value']}{detail}")

    elif args.action == "dupes":
        dups = brain.dupes_report(30)
        if args.json:
            print(json.dumps(dups, ensure_ascii=False, indent=2))
        else:
            print(f"🔍 多版本冗余: {len(dups)} 组")
            for i, d in enumerate(dups, 1):
                print(f"  {i}. {d['base']} ({d['count']}版本): {d['paths'][0]}")

    elif args.action == "api":
        apis = brain.api_list()
        if args.json:
            print(json.dumps(apis, ensure_ascii=False, indent=2))
        else:
            print(f"🌐 API服务: {len(apis)} 个")
            for a in apis:
                print(f"   {a['name']:40s} {a['path']}")

    elif args.action == "route":
        intent = " ".join(args.args) if args.args else ""
        if not intent:
            print("❌ 请提供意图描述")
            sys.exit(1)
        suggestions = brain.smart_route(intent)
        if args.json:
            print(json.dumps([{"name": n, "path": p} for n, p in suggestions], ensure_ascii=False, indent=2))
        else:
            print(f"🧭 '{intent}' → {len(suggestions)} 建议:")
            for name, path in suggestions:
                print(f"   → {name}: {path}")

    elif args.action == "scan":
        brain.load(force_scan=True)
        print(brain.status_dashboard())


if __name__ == "__main__":
    main()
