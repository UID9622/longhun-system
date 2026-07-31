# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#龍芯⚡️2026-06-21-ENGINE-ORGANIZE_LONGHUN_TECH-FILE1-v1.0-2
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-ORGANIZE_LONGHUN_TECH-FILE1-v1.0-2
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
"""
整理 Notion 导出工作区 `龍魂技术全站` 到 docs/longhun-tech/。
只复制非敏感、公开技术文档，并生成 README 与扫描 JSON。
"""

import json
import os
import re
import shutil
from collections import Counter
from pathlib import Path

EXPORT_DIR = Path("/Users/zuimeidedeyihan/龍魂待整理/Export-6a2fd9c8-4e14-4110-8b5e-452cc1be5daa/龍魂技术全站")
DEST_DIR = Path("/Users/zuimeidedeyihan/longhun-system/docs/longhun-tech")

DEST_DIR.mkdir(parents=True, exist_ok=True)

# 分类规则：按关键词匹配文件名+内容
CATEGORY_RULES = [
    ("metaverse", ["元宇宙", "metaverse", "dragon-soul", "穿越战略", "愿景闭环", "终极愿景", "world lore", "gameplay", "经济与玩法"]),
    ("personas", ["人格矩阵", "persona", "personas", "思维模式", "职位会议", "人格职位", "人格协同", "interaction protocol"]),
    ("governance", ["治理", "governance", "决策", "合规", "合作标准", "运行框架", "冲突消解", "中枢总则", "权限管理", "权限矩阵", "边界管理", "规则", "价值观筛选"]),
    ("audit", ["审计", "audit", "净土", "净化", "容错机制", "指纹检测", "清理中心", "质量监控", "真伪判断", "边界中心", "审计追踪"]),
    ("roadmap", ["roadmap", "路线图", "里程碑", "milestone", "开源", "gitee", "releases", "changelog", "PRD", "requirements", "issues", "bugs", "开发规划", "未来功能"]),
    ("database", ["智能数据库", "数据库管理", "database", "数据管理", "关联架构", "备份系统", "备份恢复", "数据可视化"]),
    ("navigation", ["功能清单", "系统功能", "导航", "万里长城", "徽章", "入口", "基层接口"]),
    ("integration", ["集成", "integration", "第三方", "api", "接口", "对外展示", "链接管理", "一键同步", "通知系统", "邮件安全", "微信小程序"]),
    ("operations", ["工作流", "workflow", "自动化", "运营仪表板", "更新同步", "情报分析", "协同工作台", "监控系统", "性能优化", "工作流引擎", "操作指南", "运行监控", "性能监控", "任务管理", "移动端", "无限智能增长"]),
    ("general", ["技术全站", "配置指南", "工程师", "用户手册", "培训课程", "标识系统", "视觉标识", "设计规范", "术语知识库", "创新实验室", "知识产权保护"]),
]

# 排除规则（文件名/路径）—— 将统一按 ignorecase 匹配
EXCLUDE_NAME_PATTERNS = [
    r"私人",
    r"对话",
    r"conversation",
    r"chat",
    r"chats",
    r"情感",
    r"家庭",
    r"宝宝",
    r"^.*家[^/]*$",
    r"密钥",
    r"激活码",
    r"activation",
    r"password",
    r"api.?key",
    r"token",
    r"dna",
    r"身份",
    r"主权",
    r"个人资产",
    r"个人经历",
    r"简历",
    r"产品测算",
    r"小说",
    r"防拖延",
    r"文集",
    r"untitled",
    r"无标题",
    r"software_audit",
    r"transactions",
    r"Import Sep",
    r"哈哈",
    r"别慌",
    r"说得太",
    r"你当前系统推进",
    r"小学数学",
    r"用户设备档案",
    r"搬砖",
    r"荣誉墙模板示例",
    r"邮件颜色分类",
    r"邮件签名",
    r"两步验证",
    r"完成任务",
    r"任务完成记录",
    r"我的链接",
    r"域名白名单",
    r"ChatGPT数据导出",
    r"Sharing",
    r"成长记录",
    r"账号.*整理",
    r"测试.*csv",
    r"测试.*csv",
    r"整理.*app",
    r"从移动端开始",
    r"邮箱.*颜色",
    r"想法收集",
    r"尝试设计",
    r"Stay Updated",
    r"OpenAI News",
    r"思维分类待办",
    r"Teamspace Home",
    # 排除具体个人/商业运营记录，但保留矩阵/框架类文档
    r"^((?!矩阵).)*权限\.(md|csv)$",
    r"授权\.(md|csv)$",
    r"SaaS服务\.(md|csv)$",
    r"商业化\.(md|csv)$",
]

# 内容敏感词（出现则替换为占位符）
SENSITIVE_CONTENT_PATTERNS = [
    (r"\b(sk-[a-zA-Z0-9]{20,80})\b", "<OPENAI_API_KEY_PLACEHOLDER>"),
    (r"\b([a-zA-Z0-9_-]{32,64})\b", "<POTENTIAL_SECRET_PLACEHOLDER>"),
]

SKIP_EMPTY_THRESHOLD = 80


def clean_uuid_suffix(name: str) -> str:
    base, ext = os.path.splitext(name)
    base = re.sub(r"\s+[a-f0-9]{32}(_all)?$", "", base)
    base = re.sub(r"\s+[a-f0-9]{8}-[a-f0-9]{4}$", "", base)
    base = re.sub(r"\s+[a-f0-9]{8}$", "", base)
    return base.strip() + ext


def classify(filename: str, content: str) -> str:
    title = clean_uuid_suffix(filename).lower()
    content_sample = content[:2500].lower()

    scores = []
    for cat, keywords in CATEGORY_RULES:
        title_score = sum(2 for kw in keywords if kw.lower() in title)
        content_score = sum(1 for kw in keywords if kw.lower() in content_sample)
        total = title_score + content_score
        if total:
            scores.append((cat, total))

    if not scores:
        return "other"
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[0][0]


def should_exclude(rel_path: str, filename: str, clean_name: str, content: bytes, text: str) -> tuple[bool, str]:
    targets = [rel_path.lower(), filename.lower(), clean_name.lower()]
    for pat in EXCLUDE_NAME_PATTERNS:
        for target in targets:
            if re.search(pat, target, re.IGNORECASE):
                return True, f"匹配排除规则: {pat}"
    if len(content) < SKIP_EMPTY_THRESHOLD:
        return True, "文件过小/空"
    return False, ""


def sanitize_text(text: str) -> str:
    for pat, repl in SENSITIVE_CONTENT_PATTERNS:
        text = re.sub(pat, repl, text)
    return text


def main():
    files = []
    for root, dirs, filenames in os.walk(EXPORT_DIR):
        for fn in filenames:
            full = Path(root) / fn
            rel = full.relative_to(EXPORT_DIR)
            files.append((full, rel))

    total_md = sum(1 for _, rel in files if rel.suffix.lower() == ".md")
    total_csv = sum(1 for _, rel in files if rel.suffix.lower() == ".csv")

    copied = []
    excluded = []
    category_counter = Counter()

    for full, rel in files:
        suffix = rel.suffix.lower()
        if suffix not in (".md", ".csv"):
            continue

        content = full.read_bytes()
        try:
            text = content.decode("utf-8", errors="ignore")
        except Exception:
            text = ""

        clean_name = clean_uuid_suffix(rel.name)
        exclude, reason = should_exclude(str(rel), rel.name, clean_name, content, text)
        if exclude:
            excluded.append({"source": str(rel), "reason": reason})
            continue

        category = classify(rel.name, text)

        if category == "other":
            excluded.append({"source": str(rel), "reason": "未命中任何核心分类"})
            continue

        # CSV 过滤
        if suffix == ".csv":
            if category not in ("database", "operations", "navigation", "metaverse", "personas", "governance", "audit", "integration"):
                excluded.append({"source": str(rel), "reason": "CSV 未命中核心技术分类"})
                continue
            if any(k in str(rel).lower() for k in ["个人资产", "产品测算", "小说", " untitled", "无标题", "commercial", "sharing", "待办"]):
                excluded.append({"source": str(rel), "reason": "CSV 为个人/商业/待办碎片"})
                continue

        safe_text = sanitize_text(text)
        secrets_found = safe_text != text

        cat_dir = DEST_DIR / category
        cat_dir.mkdir(exist_ok=True)
        dest_path = cat_dir / clean_name

        counter = 1
        original_dest = dest_path
        while dest_path.exists():
            stem, ext = os.path.splitext(original_dest)
            dest_path = Path(f"{stem}_{counter}{ext}")
            counter += 1

        if secrets_found:
            dest_path.write_text(safe_text, encoding="utf-8")
        else:
            shutil.copy2(full, dest_path)

        copied.append({
            "source": str(rel),
            "destination": str(dest_path.relative_to(DEST_DIR)),
            "category": category,
            "sanitized": secrets_found,
        })
        category_counter[category] += 1

    # 控制在 80-120 文件；深度越深、标题越泛的越优先裁剪
    if len(copied) > 120:
        def priority(item):
            cat_order = {"metaverse": 0, "personas": 1, "governance": 2, "audit": 3,
                         "roadmap": 4, "database": 5, "navigation": 6, "integration": 7,
                         "operations": 8, "general": 9, "other": 10}
            depth = item["source"].count("/")
            return (cat_order.get(item["category"], 10), depth)

        copied_sorted = sorted(copied, key=priority)
        kept = copied_sorted[:120]
        removed = copied_sorted[120:]
        for item in removed:
            (DEST_DIR / item["destination"]).unlink(missing_ok=True)
            excluded.append({"source": item["source"], "reason": "超出 120 文件上限，按优先级裁剪"})
        copied = kept
        category_counter = Counter(item["category"] for item in copied)

    # README
    readme_lines = [
        "# 龍魂技术全站文档整合",
        "",
        "本目录收录自 Notion 工作区 `龍魂技术全站` 的公开技术文档，",
        "已做去敏感化处理，仅保留系统架构、人格矩阵、治理机制、净土审计、",
        "开源路线图、智能数据库管理中心、系统功能清单等核心资料。",
        "",
        f"- 扫描文件总数：{len(files)}（.md {total_md}，.csv {total_csv}）",
        f"- 本次复制文件数：{len(copied)}",
        f"- 排除文件数：{len(excluded)}",
        "",
        "## 目录结构",
        "",
    ]
    for cat in sorted(category_counter.keys()):
        count = category_counter[cat]
        readme_lines.append(f"### {cat}/（{count} 个文件）")
        readme_lines.append("")
        for item in copied:
            if item["category"] == cat:
                readme_lines.append(f"- `{item['destination']}`")
        readme_lines.append("")

    readme_lines.extend([
        "## 排除示例",
        "",
        "以下类型文件已被过滤：",
        "",
    ])
    for ex in excluded[:15]:
        readme_lines.append(f"- `{ex['source']}` → {ex['reason']}")
    readme_lines.append("")

    (DEST_DIR / "README.md").write_text("\n".join(readme_lines), encoding="utf-8")

    # scan JSON
    scan_report = {
        "source_workspace": "龍魂技术全站",
        "source_path": str(EXPORT_DIR),
        "destination_path": str(DEST_DIR),
        "total_scanned": len(files),
        "total_md": total_md,
        "total_csv": total_csv,
        "copied_count": len(copied),
        "excluded_count": len(excluded),
        "category_stats": dict(category_counter.most_common()),
        "copied_files": copied,
        "excluded_samples": excluded[:50],
    }
    (DEST_DIR / "longhun-tech-scan.json").write_text(
        json.dumps(scan_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Total scanned: {len(files)} (md={total_md}, csv={total_csv})")
    print(f"Copied: {len(copied)}")
    print(f"Excluded: {len(excluded)}")
    print("Categories:", dict(category_counter))


if __name__ == "__main__":
    main()
