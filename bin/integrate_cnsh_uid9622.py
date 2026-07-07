# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-INTEGRATE_CNSH_UID9622-FILE1-v1.0-2
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

EXPORT_DIR = Path("/Users/zuimeidedeyihan/龍魂待整理/Export-6a2fd9c8-4e14-4110-8b5e-452cc1be5daa/CNSH｜UID9622")
DEST_DIR = Path("/Users/zuimeidedeyihan/longhun-system/docs/cnsh-uid9622")

DEST_DIR.mkdir(parents=True, exist_ok=True)

# 分类规则：按关键词匹配文件名+内容
CATEGORY_RULES = [
    ("constitution", ["宪法", "constitution", "宪章", "宣言", "北辰", "母协议", "CNSH共建", "共创宪章", "原创性宣誓", "熔断触发器"]),
    ("anchors", ["锚点", "自然人身份", "设备锚", "生物锚", "社交锚", "创作锚", "审计日志", "跨平台容灾", "原创性"]),
    ("governance", ["治理", "governance", "七维", "七维", "AI治理", "数字主权", "数字主权", "执行表", "全球法律", "伦理", "合规", "权限管理", "权限矩阵"]),
    ("sancai", ["三才", "流场", "流场", "p5", "persona router", "人格路由", "router"]),
    ("runtime", ["runtime", "运行时", "编译器", "compiler", "CNSH语言", "LU指令", "字典", "dictionary", "语法", "一句话路由", "一句话路由", "指令集", "语义"]),
    ("templates", ["智能回复", "回复模板", "template", "prompt", "提示词"]),
    ("education", ["AI教育", "教程", "课程", "训练营", "学习路径"]),
    ("metaverse", ["元宇宙", "metaverse", "国民入口", "全能引擎"]),
    ("engine", ["思维主权", "易经预测", "元字引擎", "统一同步视图", "系统架构全景"]),
    ("ops", ["文档", "问题收集", "Goals", "目标", "升级清单", "重构清单", "文件转发"]),
]

# 排除规则（文件名/路径）—— 将统一按 ignorecase 匹配
EXCLUDE_NAME_PATTERNS = [
    r"私人",
    r"对话",
    r"conversation",
    r"chat",
    r"chats",
    r"灵魂传承",
    r"个人中枢档案",
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
    r"个人资产",
    r"个人经历",
    r"简历",
    r"小说",
    r"untitled",
    r"无标题",
    r"Import Sep",
    r"哈哈",
    r"别慌",
    r"说得太",
    r"小学数学",
    r"搬砖",
    r"邮件签名",
    r"两步验证",
    r"我的链接",
    r"域名白名单",
    r"ChatGPT数据导出",
    r"Sharing",
    r"成长记录",
    r"账号.*整理",
    r"测试.*csv",
    r"测试.*csv",
    r"整理.*app",
    r"想法收集",
    r"尝试设计",
    r"Stay Updated",
    r"OpenAI News",
    r"Teamspace Home",
    r"个人.*档案",
    r"个人.*经历",
    r"个人.*故事",
    r" Lucky.*中枢",
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
        "# CNSH｜UID9622 文档整合",
        "",
        "本目录收录自 Notion 工作区 `CNSH｜UID9622` 的公开技术文档，",
        "已做去敏感化处理，仅保留宪法锚点、CNSH 语言运行时、三才流场、",
        "AI 治理、智能回复模板、元宇宙国民入口等核心资料。",
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
        "source_workspace": "CNSH｜UID9622",
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
    (DEST_DIR / "cnsh-uid9622-scan.json").write_text(
        json.dumps(scan_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Total scanned: {len(files)} (md={total_md}, csv={total_csv})")
    print(f"Copied: {len(copied)}")
    print(f"Excluded: {len(excluded)}")
    print("Categories:", dict(category_counter))


if __name__ == "__main__":
    main()
