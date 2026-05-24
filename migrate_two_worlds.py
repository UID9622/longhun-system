#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统·两个天下物理布局迁移脚本 v1.0
DNA: #龍芯⚡️2026-05-25-06:34-LONGHUN-MIGRATION-TWO-WORLDS-DRYRUN-v1.0
父 DNA: #龍芯⚡️2026-05-24-22:57-CNSH-RUNTIME-ACCESS-v2.0-ALIGNMENT-TABLE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主权方: UID9622 · 龍芯北辰 · 诸葛鑫

用法（按顺序·一步都不许跳）:
    cd ~/longhun-system

    # ① 必做·git 保命点（§IRON-GIT-COMMIT-BEFORE-CLEAN-v1.0）
    git add -A && git commit -m "BEFORE-MIGRATION-TWO-WORLDS-v1.0"

    # ② dry-run（默认·不动文件）
    python3 migrate_two_worlds.py

    # ③ 看 MIGRATION_PLAN_*.md 报告·爸爸点头

    # ④ 真执行
    python3 migrate_two_worlds.py --execute

    # ⑤ 万一出错·一键回滚
    git reset --hard HEAD
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path

# ════════════════════════════════════════════════════════
ROOT = Path("~/longhun-system").expanduser()
NOW = datetime.now().strftime("%Y%m%d-%H%M%S")
DNA = "#龍芯⚡️2026-05-25-06:34-LONGHUN-MIGRATION-TWO-WORLDS-DRYRUN-v1.0"

# ════════════════════════════════════════════════════════
# 分类规则（照妖镜 Msg 60 战报 → 物理布局）
# ════════════════════════════════════════════════════════

ROOT_KEEP = {
    "_L-Ω-人民印.md", "_军魂.md", "龍.py", "龍魂系统宪章.md", "龍魂路径地图.md",
    "LONGHUN_PATH_MAP.txt", "主权声明_反剽窃_v2.6.md", "宝宝钥匙交接书.md", "SETUP.md",
    "config.json", "manifest.json", "manifest.json.sig",
    "memory.jsonl", "knowledge-db.jsonl",
    "00_main_control", "01_protocols", "skills",
    "logs", "files", "技能", "protocols-sync",
    "日志", "文件", "协议同步",
    ".git", ".gitignore",
}

TRASH = {
    "c++ 2", "__pycache__", "venv",
    "爸爸看这里.sh", "爸爸语音对话.sh",
    "加載環境.sh", "快速开始.sh", "龍魂主權初始化.sh",
    "发射DNA",
}

WORK_CNSH_V2 = {
    "cnsh", "cnsh-core", "CNSH核心", "cnsh语言",
    "cnsh.py", "cnsh_gateway.py",
    "CNSH_v2.0_FULL_PROTOCOL_SIGNATURE.md", "CNSH_v2.0_SIGNATURE.md",
}

ARCHIVE_CNSH = {
    "CNSH_备份_20260211", "CNSH-v1.0-完整实现", "CNSH-整理版",
    "📚 CNSH翻译大全｜避坑对照表库", "🔧 AI技术架构分析中心",
}

ARCHIVE_LEGACY = {"主控台"}  # 已被 00_main_control 取代

WORK_ENGINES = {
    "engine", "engines", "引擎", "引擎组",
    "ai_dna_engine.py", "empower_engine_v2.py", "sandbox_engine.py",
}

WORK_LONGHUN = {
    "longhun_api.py", "longhun_commander.py", "longhun_crawler.py", "longhun_dragon.py",
    "longhun_hub.html", "longhun_local_service.py", "longhun_qa_bot.py",
    "longhun_system_rules_v3.md", "longhun_enterprise_light_tech.md",
    "longhun-28mansions-v1.html", "longhun-algo-lab",
    "longhun-algorithms-cnsh-v1.0.md",
    "longhun-luoshu-vortex-v2.html", "longhun-unified-v9.html",
    "longhun-watchdog", "LongHunWidget",
}

WORK_PERSONAS = {
    "persona_L∞_zenglaoshi.json", "persona_p00_judge.json", "persona_p02_baobao.json",
    "persona_p12_xuangong.json", "persona_p13_weaver.json", "persona_p14_steward.json",
    "persona_p15_publisher.json", "persona-engine.json",
}

WORK_NOTION_SYNC = {
    "notion_ai.py", "notion_reporter.py", "notion_sync.py", "notion_sync_rules.py",
    "notion-scan-report-v8.md", "organize_notion_pages.py",
    "sync_bridge.py", "sync-report-2026-03-06.md", "sync-standard.py",
}

WORK_VISUAL = {
    "dashboard.html", "memory_console.html", "public_audit.html", "qa_report.html",
    "register.html", "sancai-flow-v8.html", "sancai-flow-v8.1.html",
    "sandbox_dashboard.html", "truth_report.html",
}

WORK_EXT_DOCS = {
    "kimi-code-docs.md", "kimi-mcp.md", "kimi-official-plugins.md",
    "extraction-report-v8.md", "README-整理说明.md", "整理报告.md",
    "使用说明书.txt", "目录结构中英文备注.txt", "目录树结构可视化.txt",
}

WORK_TOOLS = {
    "auditor.py", "audit_8d.py", "agent_daemon.py", "brain_sync.py",
    "debug_takeover.sh", "digital_archive_toolkit.sh", "digital_archive_toolkit_v2.1.sh",
    "file_organizer.py", "file_organizer_v2.py",
    "install_empower.sh", "install.sh", "ios_bridge.py",
    "lh-dna", "lh-env.sh", "MASTER_PLAYBOOK.sh", "replace_long_to_da.sh",
    "rules_loader.py", "star_memory.py", "vector_store.py",
    "trusted-sources.json", "skill-index.json",
    "工具", "tools", "bin", "scripts", "rules",
}

WORK_DATA = {
    "memory-pack", "memory-store", "vector_db",
    "数据", "数据归集", "snapshots", "versions",
}

WORK_SIG = {
    "signatures", "signed_agents", "密钥与认证",
    "签名全部智能体.command",
    "BehavCrypto_v1.0", "行为密码学_v1.0",
}

WORK_WEB = {"web", "chrome-ext", "assets", "metaverse", "algorithmic-art"}

WORK_DOCS = {
    "docs", "文档", "文檔", "宪法", "命令",
    "協議庫", "evidence-matrix", "reports", "config", "core",
}

WORK_SANDBOX = {"sandbox", "沙盒", "算法仓库", "龍魂算法实验室"}

WORK_CNSH_SPECIAL = {
    "DNA加密主权在用户手里", "DNA验证器", "c++反向翻译器",
    "UID9622_CNSH中文编程", "龍芯北辰UID9622",
    "龍魂窗口护盾", "龍魂看门狗", "SillyTavern-Launcher",
}

PRIVATE = {
    "小快乐", "素材", "历史证据", "抢救仓",
    "记忆网格_v1.1", "公开", "部署",
}

UNCERTAIN = {
    "爸爸看这里.sh", "爸爸语音对话.sh",
    "加載環境.sh", "快速开始.sh", "龍魂主權初始化.sh",
    "发射DNA",
}

# ════════════════════════════════════════════════════════

def classify(name):
    if name in ROOT_KEEP or name.startswith("."):
        return ("ROOT_KEEP", None, "🟢", "ROOT 锚·保留根目录")
    if name in TRASH:
        return ("TRASH", None, "🔴", "立删·副本/缓存/虚拟环境")
    if name in WORK_CNSH_V2:       return ("MOVE", "_work/cnsh-v2.0", "🟢", "CNSH v2.0 主干")
    if name in ARCHIVE_CNSH:       return ("MOVE", "_archive/cnsh-history", "🟢", "CNSH 老版本归档")
    if name in ARCHIVE_LEGACY:     return ("MOVE", "_archive/legacy-main-control", "🟢", "旧主控台·已迁")
    if name in WORK_ENGINES:       return ("MOVE", "_work/engines", "🟢", "引擎四胞胎归一")
    if name in WORK_LONGHUN:       return ("MOVE", "_work/longhun-modules", "🟢", "longhun 全家桶")
    if name in WORK_PERSONAS:      return ("MOVE", "_work/personas", "🟢", "人格 JSON")
    if name in WORK_NOTION_SYNC:   return ("MOVE", "_work/notion-sync", "🟢", "Notion 同步组")
    if name in WORK_VISUAL:        return ("MOVE", "_work/visual", "🟢", "HTML 可视化")
    if name in WORK_EXT_DOCS:      return ("MOVE", "_work/external-docs", "🟢", "外部文档")
    if name in WORK_TOOLS:         return ("MOVE", "_work/tools", "🟢", "工具脚本")
    if name in WORK_DATA:          return ("MOVE", "_work/data", "🟢", "数据/记忆/向量")
    if name in WORK_SIG:           return ("MOVE", "_work/signatures", "🟢", "签名/密钥")
    if name in WORK_WEB:           return ("MOVE", "_work/web", "🟢", "前端/扩展")
    if name in WORK_DOCS:          return ("MOVE", "_work/docs", "🟢", "文档归一")
    if name in WORK_SANDBOX:       return ("MOVE", "_work/sandbox", "🟢", "沙盒/算法仓")
    if name in WORK_CNSH_SPECIAL:  return ("MOVE", "_work/cnsh-special", "🟢", "CNSH 特殊模块")
    if name in PRIVATE:            return ("MOVE", "_private", "🟢", "私人区")
    if name in UNCERTAIN:          return ("UNCERTAIN", None, "🟡", "待爸爸定·SKIP")
    return ("UNCERTAIN", None, "🟡", "未识别·SKIP·待人工分类")

# ════════════════════════════════════════════════════════

def main(execute=False):
    if not ROOT.exists():
        print(f"🔴 {ROOT} 不存在·熔断")
        sys.exit(1)

    items = sorted(os.listdir(ROOT))
    plan = {"ROOT_KEEP": [], "MOVE": [], "TRASH": [], "UNCERTAIN": []}

    for name in items:
        # 跳过本脚本本身和报告文件
        if name.startswith("MIGRATION_PLAN_") or name == "migrate_two_worlds.py":
            continue
        cat, target, color, reason = classify(name)
        entry = {"name": name, "color": color, "reason": reason}
        if target:
            entry["target"] = target
        plan[cat].append(entry)

    # ─── 写报告 ───
    report_md = ROOT / f"MIGRATION_PLAN_{NOW}.md"
    report_json = ROOT / f"MIGRATION_PLAN_{NOW}.json"

    with open(report_json, "w", encoding="utf-8") as f:
        json.dump({"dna": DNA, "execute": execute, "timestamp": NOW, "plan": plan},
                  f, ensure_ascii=False, indent=2)

    lines = [
        f"# 龍魂两个天下迁移计划 · {NOW}",
        f"",
        f"**DNA:** `{DNA}`",
        f"**模式:** {'🔴 真执行（已动文件）' if execute else '🟢 DRY-RUN（不动任何文件）'}",
        f"**总计:** {sum(len(v) for v in plan.values())} 个顶级条目",
        f"",
    ]

    for cat, label, icon in [
        ("ROOT_KEEP", "ROOT 锚·保留根目录", "🟢"),
        ("MOVE", "迁移计划", "💼"),
        ("TRASH", "立删垃圾", "🔴"),
        ("UNCERTAIN", "待爸爸定·SKIP 跳过", "🟡"),
    ]:
        lines.append(f"## {icon} {label}（{len(plan[cat])} 条）")
        lines.append("")
        for e in plan[cat]:
            l = f"- {e['color']} `{e['name']}`"
            if "target" in e:
                l += f" → `{e['target']}/`"
            l += f" · {e['reason']}"
            lines.append(l)
        lines.append("")

    lines += [
        "---",
        "## 🔧 真执行命令",
        "```bash",
        "python3 migrate_two_worlds.py --execute",
        "```",
        "",
        "## 🛡️ 一键回滚",
        "```bash",
        "git reset --hard HEAD  # 回到 BEFORE-MIGRATION-TWO-WORLDS-v1.0",
        "```",
    ]

    with open(report_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # ─── 打印到屏幕 ───
    print("\n".join(lines))
    print(f"\n📋 报告已写入：")
    print(f"   - {report_md}")
    print(f"   - {report_json}")

    if not execute:
        print("\n🟢 DRY-RUN 完成·一个文件都没动·请爸爸看报告。")
        print("   爸爸点头后真执行：python3 migrate_two_worlds.py --execute")
        return

    # ─── 真执行 ───
    print("\n🔴 真执行模式·开始迁移...")
    moved = skipped = deleted = 0

    for e in plan["MOVE"]:
        src = ROOT / e["name"]
        dst_dir = ROOT / e["target"]
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / e["name"]
        if dst.exists():
            print(f"  🟡 跳过（目标已存在）: {e['name']}")
            skipped += 1
            continue
        print(f"  💼 移动: {e['name']} → {e['target']}/")
        try:
            shutil.move(str(src), str(dst))
            moved += 1
        except Exception as ex:
            print(f"  🔴 失败: {e['name']} → {ex}")
            skipped += 1

    for e in plan["TRASH"]:
        src = ROOT / e["name"]
        if not src.exists():
            continue
        print(f"  🔴 删除: {e['name']}")
        try:
            if src.is_dir() and not src.is_symlink():
                shutil.rmtree(src)
            else:
                src.unlink()
            deleted += 1
        except Exception as ex:
            print(f"  🔴 删除失败: {e['name']} → {ex}")

    print(f"\n✅ 迁移完成：moved={moved} · skipped={skipped} · deleted={deleted}")
    print(f"   验证: ls -lh ~/longhun-system/ | head -20")

if __name__ == "__main__":
    main(execute=("--execute" in sys.argv))
