#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·命令索引更新器 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-索引更新-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

自动扫描 bin/ engines/ deploy/ 目录，更新 COMMAND_INDEX.md 的触发词表。
铁律#11: 新增任何命令全部塞进去。
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# ===== 路径 =====
ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / ".codebuddy/COMMAND_INDEX.md"
BIN_DIR = ROOT / "bin"
ENGINES_DIR = ROOT / "engines"
DEPLOY_DIR = ROOT / "deploy"

# ===== 触发词映射表（手动维护的核心词 → 触发词） =====
# 格式: 文件名关键词 → 触发词 + 简短说明
TRIGGER_MAP = {
    # === 核心工具 ===
    "lh_web_health_check": ("健康检查,网站检查,监控", "网站可用性监控"),
    "lh_align_checker": ("对齐复盘,代码检查,对齐", "扫描重复函数·缺失DNA·缺失GPG"),
    "lh_auto_align_daemon": ("自动对齐,闭环修复", "自动修复代码对齐问题"),
    "lh_digital_root": ("数字根,五行数字,369", "计算数字根·五行映射·369熔断"),
    "lh_wuxing_core": ("五行计算,五行分析,五行", "五行强度·补益分析·对冲指数"),
    "lh_link_parser": ("链接解析,URL解析,解析链接", "解析URL·提取元数据/正文/链接"),
    "lh_tongxinyi_translator": ("通心译,翻译,文化翻译", "文化锚点保护翻译·SQLite记忆"),
    "lh_browser_historian": ("浏览史官,采集历史,浏览器史官,历史采集", "四道防线·设备金库·导出签名"),
    "lh_xuanji_engine": ("璇玑,推演,记忆溯源", "记忆溯源推演·四象闭环"),
    "lh_herbal_rag": ("本草,人参,甘草,中药", "本草知识检索增强"),

    # === 审计 & 安全 ===
    "lh_full_system_audit": ("全系统审计,系统审计,安全审计", "全系统安全扫描"),
    "lh_deben_audit": ("德本审计,五问,离火运", "德本五问·审计扫描"),
    "lh_anti_fraud_detector": ("反诈,防骗,弯弯绕绕,套路检测", "14维度·话术分析·反制话术"),
    "lh_anti_tamper": ("防篡改,篡改检测", "文件一致性防篡改扫描"),
    "lh_code_audit": ("代码审计,漏洞扫描", "代码安全审计"),
    "lh_self_heal": ("自愈,修复,自动修复", "自助修复系统问题"),
    "lh_memory_load": ("记忆加载,加载记忆", "焊死记忆加载"),
    "lh_system_eval": ("系统评估,健康评分", "系统健康度评分"),
    "lh_safeai": ("SafeAI,安全AI,上下文安全", "意图分类·七因子审计·分层熔断"),
    "lh_judge": ("公正总裁,裁决,公正裁决", "公正裁决·三色审计"),
    "lh_seq": ("序列执行,流水线审计", "SafeAI→KFPP→CSDN→公正总裁"),

    # === 部署 & 同步 ===
    "sync-to-kunpeng": ("同步鲲鹏,同步服务器,代码同步", "同步代码到鲲鹏119.13.90.27"),
    "deploy-now": ("一键部署,部署", "一键部署全部服务"),
    "health_check": ("鲲鹏健康,Bark告警,服务器监控", "鲲鹏健康检查·Bark推送"),
    "lh_auto_cannon": ("Git推送,推远端,全量推送", "GitHub+Gitee+GitCode三端推送"),
    "deploy_deepseek": ("部署DeepSeek,DeepSeek部署", "一键部署DeepSeek-V3"),

    # === 多媒体 ===
    "lh_video_studio": ("做视频,视频制作,视频工坊", "文本→配音+AI图示+字幕 v3.0"),
    "lh_3d_pipeline": ("做3D,3D,图生三维", "图生三维管线"),
    "lh_verify": ("验证主权,验视频,DNA水印", "提取DNA盲水印·公开可用"),
    "lh_tts_xtts": ("真声配音,配音,语音合成", "XTTS v2真声配音"),

    # === 搜索 & 知识 ===
    "lh_search_engine": ("搜索,搜索引擎,查资料", "Bing搜→缓存→审计 :9631"),
    "lh_knowledge": ("知识中枢,知识检索", "知识中枢服务 :8766"),

    # === 模型训练 ===
    "lh_lora_trainer_v4": ("训练模型,LoRA训练,微调", "MLX LoRA rank=16"),
    "lh_download_v40_bases": ("拉取数据,训练数据,数据下载", "80中国源+65国际"),

    # === 人格 & 编排 ===
    "lh_persona_orchestrator": ("人格编排,人格调度", "20人格任务分发"),
    "lh_persona_report": ("人格报告,人格统计", "人格活跃度/贡献统计"),

    # === DNA & 追溯 ===
    "hetu_luoshu_dna": ("生成DNA,DNA追溯码", "DNA生成·河图洛书"),
    "lh_gpg_sign": ("GPG签名,签名,签章", "GPG分离签名·扫描验证"),
    "lh_batch_confirm_sign": ("批量签章,全量签名", "批量GPG签章确认"),

    # === CNSH ===
    "cnsh_compiler": ("CNSH编译,编译CNSH", "CNSH→Python四阶段编译"),
    "lh_cnsh_run": ("运行CNSH,CNSH执行", "CNSH脚本解释执行"),

    # === 底座铁律 ===
    "lh_source_vetting": ("源头校验,数据校验,入站检查", "五问·80分门槛·硬性拒绝"),
    "lh_crawler_ethics": ("爬虫伦理,爬虫检查", "6项爬虫伦理检查"),
    "lh_civil_defense_samples": ("民间防御,水军识别,样本收集", "正向/负向自动分类收集"),
    "lh_archive_vague_comments": ("无为归档,评论归档,检测无为", "15个无为模式特征词检测"),

    # === 管理工具 ===
    "start_all": ("启动全部,全部启动,启动服务", "一键启动所有52个服务"),
    "monitor_setup": ("监控配置,systemd配置", "systemd+cron+告警"),
    "lh_install": ("安装,系统安装", "龍魂系统安装向导"),
    "lh_network_05_network_fix_all": ("网络修复,网络限流,网络检查", "一键检测+修复限流"),
}

# ===== 要扫描的脚本目录 =====
SCAN_DIRS = [BIN_DIR, ENGINES_DIR, DEPLOY_DIR]


def extract_description(filepath: Path) -> str:
    """从脚本中提取功能描述"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(2000)  # 读前2000字符足够了
    except Exception:
        return ""

    # 策略1: 功能[：:] 描述
    m = re.search(r'功能[：:]\s*([^\n]+)', content)
    if m:
        return m.group(1).strip()
    # 策略2: docstring 首行
    m = re.search(r'"""(.+?)"""', content, re.DOTALL)
    if m:
        lines = m.group(1).strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('DNA') and not line.startswith('🐉'):
                return line[:60]
    # 策略3: 第二行注释（第一行通常是shebang）
    lines = content.split('\n')
    for line in lines[1:5]:
        line = line.strip()
        if line.startswith('#') and not line.startswith('##') and not line.startswith('#!'):
            desc = line.lstrip('#').strip()
            if desc and len(desc) > 3:
                return desc[:60]
    return ""


# 跳过目录/文件名模式
SKIP_PATTERNS = [
    "archive", "__pycache__", "tests", "test", "training_data",
    "downloads_archive", ".frozen", "node_modules", ".git",
    "CNSH_颜色历史", "personas",  # 这些是非脚本目录
]


def should_skip(path: Path) -> bool:
    """检查路径是否应跳过"""
    parts = path.parts
    for part in parts:
        for pattern in SKIP_PATTERNS:
            if pattern in part:
                return True
    return False


def scan_scripts() -> List[Tuple[str, str, str, str]]:
    """
    扫描 bin/（非递归） + engines/（一层） + deploy/（两层），
    返回 (file_stem, file_path, trigger, desc)
    """
    results = []
    seen = set()

    # 1. bin/ 只扫一层（不递归子目录）
    if BIN_DIR.exists():
        for f in sorted(BIN_DIR.glob("*.py")):
            stem = f.stem
            if stem in seen or stem.startswith("__") or stem.startswith("test_"):
                continue
            if should_skip(f):
                continue
            seen.add(stem)
            trigger, desc = _match_trigger(stem, f)
            if desc or trigger:
                results.append((stem, str(f.relative_to(ROOT)), trigger, desc))

        for f in sorted(BIN_DIR.glob("*.sh")):
            stem = f.stem
            if stem in seen or should_skip(f):
                continue
            seen.add(stem)
            trigger, desc = _match_trigger(stem, f)
            if not desc:
                desc = f"Shell脚本: {stem}"
            if not trigger:
                trigger = stem.replace("_", " ")[:20]
            results.append((stem, str(f.relative_to(ROOT)), trigger, desc))

    # 2. engines/ 只扫一层
    if ENGINES_DIR.exists():
        for f in sorted(ENGINES_DIR.glob("*.py")):
            stem = f.stem
            if stem in seen or stem.startswith("__") or stem.startswith("test_"):
                continue
            if should_skip(f):
                continue
            seen.add(stem)
            trigger, desc = _match_trigger(stem, f)
            if desc or trigger:
                results.append((stem, str(f.relative_to(ROOT)), trigger, desc))

    # 3. deploy/ 只扫两层（脚本 + scripts/ 子目录）
    if DEPLOY_DIR.exists():
        for f in sorted(DEPLOY_DIR.glob("*.sh")):
            stem = f.stem
            if stem in seen or should_skip(f):
                continue
            seen.add(stem)
            trigger, desc = _match_trigger(stem, f)
            if not desc:
                desc = f"部署脚本: {stem}"
            if not trigger:
                trigger = stem.replace("_", " ")[:20]
            results.append((stem, str(f.relative_to(ROOT)), trigger, desc))

        # deploy/scripts/ 子目录
        scripts_dir = DEPLOY_DIR / "scripts"
        if scripts_dir.exists():
            for f in sorted(scripts_dir.glob("*.sh")):
                stem = f.stem
                if stem in seen or should_skip(f):
                    continue
                seen.add(stem)
                trigger, desc = _match_trigger(stem, f)
                if not desc:
                    desc = f"部署脚本: {stem}"
                if not trigger:
                    trigger = stem.replace("_", " ")[:20]
                results.append((stem, str(f.relative_to(ROOT)), trigger, desc))

    return results


def _match_trigger(stem: str, f: Path) -> Tuple[str, str]:
    """匹配触发词映射表"""
    trigger = ""
    desc = ""
    for key, (trig, d) in TRIGGER_MAP.items():
        if key in stem or stem in key:
            trigger = trig
            desc = d
            break
    if not desc:
        desc = extract_description(f)
    if not trigger:
        trigger = stem.replace("lh_", "").replace("cnsh_", "").replace("_", " ")[:20]
    return trigger, desc


def _format_cmd(rel_path: str) -> str:
    """格式化命令"""
    if rel_path.endswith('.py'):
        return f"`python3 {rel_path}`"
    elif rel_path.endswith('.sh'):
        return f"`bash {rel_path}`"
    return f"`{rel_path}`"


def build_full_index(scripts: List[Tuple]) -> str:
    """构建完整索引：🎯核心触发词表 + 📦完整清单"""
    mapped = []
    unmapped = []

    for stem, rel_path, trigger, desc in scripts:
        is_mapped = any(key in stem or stem in key for key in TRIGGER_MAP)
        if is_mapped:
            mapped.append((stem, rel_path, trigger, desc))
        else:
            unmapped.append((stem, rel_path, trigger, desc))

    lines = [
        "## 🎯 自然语言触发词",
        "",
        "> **铁律#11**: 老大不记命令，AI自己挑。新增任何命令全部塞进此表。",
        "> 你说\"健康检查\"→AI匹配→自动执行。`lh-run \"健康检查\"` 或 AI 直接挑命令。",
        f"> 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')} · 核心 {len(mapped)} 条 · 全量 {len(scripts)} 条",
        "",
        "| 触发词（说这些→匹配） | 自动执行命令 | 说明 |",
        "|:---|:---|:---|",
    ]

    for stem, rel_path, trigger, desc in mapped:
        cmd = _format_cmd(rel_path)
        lines.append(f"| {trigger} | {cmd} | {desc} |")

    # 未映射脚本按前缀分组
    if unmapped:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"## 📦 完整脚本清单 ({len(unmapped)} 个)")
        lines.append("")
        lines.append("> 以下脚本可通过文件名模糊匹配。AI 看到文件名即可直接执行。")
        lines.append("")

        groups = {"lh_": [], "CNSH_": [], "engines_": [], "deploy_": [], "其他": []}
        for stem, rel_path, trigger, desc in unmapped:
            if stem.startswith("lh_"):
                groups["lh_"].append((stem, rel_path, trigger, desc))
            elif stem.startswith("CNSH_"):
                groups["CNSH_"].append((stem, rel_path, trigger, desc))
            elif "engines/" in rel_path:
                groups["engines_"].append((stem, rel_path, trigger, desc))
            elif "deploy/" in rel_path:
                groups["deploy_"].append((stem, rel_path, trigger, desc))
            else:
                groups["其他"].append((stem, rel_path, trigger, desc))

        labels = {
            "lh_": f"🐉 lh_ 工具脚本 ({len(groups['lh_'])} 个)",
            "CNSH_": f"🔤 CNSH 中文脚本 ({len(groups['CNSH_'])} 个)",
            "engines_": f"⚙️ engines/ 引擎 ({len(groups['engines_'])} 个)",
            "deploy_": f"🚀 deploy/ 部署脚本 ({len(groups['deploy_'])} 个)",
            "其他": f"📁 其他脚本 ({len(groups['其他'])} 个)",
        }

        for gkey in ["lh_", "engines_", "CNSH_", "deploy_", "其他"]:
            items = groups[gkey]
            if not items:
                continue
            lines.append(f"### {labels[gkey]}")
            lines.append("")
            lines.append("| 触发词 | 命令 | 说明 |")
            lines.append("|:---|:---|:---|")
            for stem, rel_path, trigger, desc in items:
                cmd = _format_cmd(rel_path)
                lines.append(f"| {trigger} | {cmd} | {desc[:50] if desc else '-'} |")

    return '\n'.join(lines)


def update_index():
    """主函数：扫描并更新 COMMAND_INDEX.md"""
    print("🔍 扫描脚本目录...")
    scripts = scan_scripts()

    if not scripts:
        print("❌ 未找到脚本")
        return 1

    mapped = sum(1 for s in scripts if any(key in s[0] or s[0] in key for key in TRIGGER_MAP))
    unmapped = len(scripts) - mapped
    print(f"📊 找到 {len(scripts)} 个脚本 (核心: {mapped}, 其他: {unmapped})")

    # 构建索引
    index_section = build_full_index(scripts)

    # 读取现有索引
    if INDEX_PATH.exists():
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            old_content = f.read()
    else:
        old_content = ""

    # 插到 📂 分类索引 之前
    marker = "## 🎯 自然语言触发词"
    next_major = old_content.find("\n## 📂 分类索引")

    if marker in old_content and next_major > old_content.find(marker):
        # 替换已有章节
        before = old_content[:old_content.find(marker)]
        after = old_content[next_major:]
        new_content = before + index_section + "\n\n" + after
    elif next_major > 0:
        before = old_content[:next_major]
        after = old_content[next_major:]
        new_content = before + index_section + "\n\n---\n\n" + after
    else:
        # 追加到末尾
        new_content = old_content + "\n\n---\n\n" + index_section

    # 写入
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ 已更新: {INDEX_PATH}")
    print(f"🎯 核心: {mapped} · 📦 完整: {unmapped}")
    return 0


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·命令索引更新器 v1.0\n自动扫描bin/engines/deploy/，更新触发词表",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--dry-run", action="store_true", help="只扫描不写入")
    parser.add_argument("--stats", action="store_true", help="仅显示扫描统计")
    parser.add_argument("--missing", action="store_true", help="列出未映射的脚本")

    args = parser.parse_args()

    scripts = scan_scripts()
    mapped = sum(1 for s in scripts if any(
        key in s[0] or s[0] in key for key in TRIGGER_MAP
    ))

    if args.stats:
        print(f"📊 脚本总数: {len(scripts)}")
        print(f"   已映射: {mapped}")
        print(f"   未映射: {len(scripts) - mapped}")
        return

    if args.missing:
        print("📋 未映射的脚本:")
        for stem, path, trigger, desc in scripts:
            if not any(key in stem or stem in key for key in TRIGGER_MAP):
                print(f"   {stem:40s} → {desc[:40] if desc else '(无描述)'}")
        return

    if args.dry_run:
        print("🔍 [干运行] 将更新以下触发词表:")
        for stem, path, trigger, desc in scripts[:20]:
            print(f"   {trigger:25s} → {desc[:40] if desc else '(无描述)'}")
        if len(scripts) > 20:
            print(f"   ... 还有 {len(scripts) - 20} 条")
        print(f"\n   总计: {len(scripts)} 条触发词")
        return

    return update_index()


if __name__ == "__main__":
    sys.exit(main())
