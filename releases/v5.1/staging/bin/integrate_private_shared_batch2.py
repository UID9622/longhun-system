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

EXPORT_DIR = Path("/Users/zuimeidedeyihan/龍魂待整理/Export-6a2fd9c8-4e14-4110-8b5e-452cc1be5daa/私人与共享")
DEST_DIR = Path("/Users/zuimeidedeyihan/longhun-system/docs/private-shared-imports")

DEST_DIR.mkdir(parents=True, exist_ok=True)

# 分类规则：按关键词匹配文件名+内容（優先級從上到下，governance 放最後作兜底）
CATEGORY_RULES = [
    ("ai-behavior", ["AI行为", "AI 行为", "回复", "执行标准", "强制执行", "智能回复", "prompt", "人格召唤", "意图识别"]),
    ("cnsh-protocols", ["CNSH", "协议", "路由", "语言规范", "语义", "任务流场", "流場", "一句話", "北辰", "母协议", "通心譯", "共建宪章"]),
    ("architecture", ["架构", "系统架构", "三层隔离", "龙魂OS", "OS", "元宇宙", "Metaverse", "入口", "网关", "中台", "协同中枢"]),
    ("persona-tools", ["人格", "persona", "personas", "诸葛亮", "93人格", "人格库", "思维模式", "职位会议", "人格职位", "人格协同"]),
    ("api-integration", ["FastAPI", "Webhook", "文档中心", "一键同步"]),
    ("memory-dna", ["DNA", "记忆", "追溯", "归集", "归檔", "归集引擎", "归檔引擎"]),
    ("security-audit", ["审计", "audit", "净土", "安全防护", "数字身份", "熔断", "监督", "指纹检测", "清理中心", "质量监控", "真伪判断", "边界中心"]),
    ("documentation", ["README", "术语", "白皮书", "龙智守", "使用说明", "操作指南", "知识库总索引", "文档中心"]),
    ("decision-records", ["DECISION", "决策日志", "选择记录", "决定"]),
    ("developer-tools", ["编辑器", "脚本工具", "vscode", "IDE插件", "code-audit", "编译器", "runtime"]),
    ("governance", ["治理", "governance", "宪章", "底线协议", "冲突消解", "中枢总则", "权限管理", "权限矩阵", "价值观筛选", "伦理", "合规"]),
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
    r"个人资产",
    r"个人经历",
    r"简历",
    r"小说",
    r"防拖延",
    r"文集",
    r"untitled",
    r"无标题",
    r"software_audit",
    r"Import Sep",
    r"哈哈",
    r"别慌",
    r"说得太",
    r"你当前系统推进",
    r"小学数学",
    r"搬砖",
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
    r"測試.*csv",
    r"整理.*app",
    r"从移动端开始",
    r"邮箱.*颜色",
    r"想法收集",
    r"嘗試設計",
    r"Stay Updated",
    r"OpenAI News",
    r"思维分类待办",
    r"Teamspace Home",
    r"个人.*故事",
    r"和.*对话",
    r"灵魂传承",
    r"个人.*档案",
    r"Lucky原话",
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

    # README update note
    # scan JSON
    scan_report = {
        "source_workspace": "私人与共享",
        "source_path": str(EXPORT_DIR),
        "destination_path": str(DEST_DIR),
        "batch": 2,
        "total_scanned": len(files),
        "total_md": total_md,
        "total_csv": total_csv,
        "copied_count": len(copied),
        "excluded_count": len(excluded),
        "category_stats": dict(category_counter.most_common()),
        "copied_files": copied,
        "excluded_samples": excluded[:50],
    }
    (DEST_DIR / "private-shared-batch2-scan.json").write_text(
        json.dumps(scan_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"Total scanned: {len(files)} (md={total_md}, csv={total_csv})")
    print(f"Copied: {len(copied)}")
    print(f"Excluded: {len(excluded)}")
    print("Categories:", dict(category_counter))


if __name__ == "__main__":
    main()
