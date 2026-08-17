#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·甲申·己亥·䷁坤-AI-HUB-MANAGER-v2.0
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""龍魂 AI 输出归集 Hub 管理器 v2.0

统一管理 Cursor / Claude Code / Kimi / CodeBuddy / Copilot / Grok 等 AI 工具的输出。
文件层归集 + 内容层索引 + KFPP七因子过滤 + 跨工具搜索。
"""

import json
import os
import re
import sys
import hashlib
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HUB_ROOT = Path.home() / "ai-outputs"
INDEX_DIR = HUB_ROOT / "_index"
INDEX_FILE = INDEX_DIR / "master_index.json"
STATS_FILE = INDEX_DIR / "stats.json"

# 工具→默认输出路径映射
TOOL_PATHS = {
    "cursor":    Path.home() / ".cursor",
    "claude":    Path.home() / ".claude",
    "codebuddy": Path.home() / ".codebuddy",
    "kimi":      HUB_ROOT / "kimi",    # 已设 KIMI_OUTPUT_DIR
    "copilot":   Path.home() / ".github" / "copilot",
    "grok":      Path.home() / ".grok",
}

# KIMI_OUTPUT_DIR 是环境变量，优先使用
KIMI_ENV = os.environ.get("KIMI_OUTPUT_DIR", "")
if KIMI_ENV:
    TOOL_PATHS["kimi"] = Path(KIMI_ENV)

# 索引的文件类型
INDEX_EXTENSIONS = {".py", ".js", ".ts", ".html", ".css", ".md", ".json",
                     ".yaml", ".yml", ".toml", ".sh", ".txt", ".rs", ".go",
                     ".swift", ".kt", ".java", ".vue", ".jsx", ".tsx", ".c", ".h"}

# === KFPP 七因子过滤配置（v2.0加固新增） ===
# KFPP: Knowledge File Purity Protocol — AI归集入库前质量门
KFPP_MIN_CONFIDENCE = 0.5  # 最低可信度阈值
KFPP_MAX_FILE_SIZE = 10_000_000  # 10MB上限
KFPP_BLOCKED_PATTERNS = [
    # 🔴 明文凭证（知识安全黑洞）
    r'(?:api[_-]?key|apikey|api_secret|secret[_-]?key|private[_-]?key)\s*[:=]\s*[\'"][^\'"]{8,}[\'"]',
    r'(?:password|passwd|token|auth[_-]?token)\s*[:=]\s*[\'"][^\'"]{4,}[\'"]',
    r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----',
    r'-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----',
    # 🟡 内部配置（知识设卡）
    r'(?:\.env|\.npmrc|\.pypirc|\.dockercfg)',
    r'(?:access[_-]?token|client[_-]?secret)\s*[:=]\s*[\'"][^\'"]+[\'"]',
    # 🟡 二进制/编译产物（不可读）
    r'^\.DS_Store$',
    r'\.(?:pyc|pyo|so|dll|exe|bin)$',
]
KFPP_MIN_CONTENT_LENGTH = 10  # 内容少于10字符视为空文件
KFPP_QUALITY_KEYWORDS = [
    "TODO", "FIXME", "HACK", "WORKAROUND",  # 未完成标记暗示低质量
    "test", "temp", "tmp", "draft", "备份", "副本",  # 临时/草稿
]


def kfpp_scan(filepath: Path, content: str) -> dict:
    """KFPP七因子质量扫描
    返回: {passed: bool, score: float, blocked_by: str|None, tags: list}
    """
    filename = filepath.name.lower()

    # 因子1: 文件大小
    if filepath.stat().st_size > KFPP_MAX_FILE_SIZE:
        return {"passed": False, "score": 0.0, "blocked_by": "超大文件(>10MB)", "tags": []}

    # 因子2: 内容长度
    if len(content.strip()) < KFPP_MIN_CONTENT_LENGTH:
        return {"passed": False, "score": 0.0, "blocked_by": "内容过短", "tags": []}

    # 因子3: 凭证/敏感信息（最高优先级拦截）
    for pattern in KFPP_BLOCKED_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return {"passed": False, "score": 0.0, "blocked_by": f"命中安全模式: {pattern[:30]}...", "tags": ["🔴安全-凭证泄露"]}
        if re.search(pattern, filename, re.IGNORECASE):
            return {"passed": False, "score": 0.0, "blocked_by": f"文件名命中安全模式: {pattern[:30]}...", "tags": ["🔴安全-敏感文件"]}

    # 因子4: 内容质量评分
    score = 0.5  # 基础分
    lines = content.split("\n")
    if len(lines) > 5:
        score += 0.1  # 有一定长度
    non_empty = [l for l in lines if l.strip()]
    if len(non_empty) / max(len(lines), 1) > 0.5:
        score += 0.1  # 非空行比例高
    if any(kw.lower() in content.lower() for kw in KFPP_QUALITY_KEYWORDS):
        score -= 0.2  # 低质量标记扣分

    # 因子5: 结构化检查（代码文件有import/function等标志）
    if filepath.suffix in {".py", ".js", ".ts", ".rs", ".go", ".java", ".swift", ".kt"}:
        has_structure = bool(re.search(r'(?:import|def |function|class |fn |func |let |const |var )', content))
        if has_structure:
            score += 0.15

    # 因子6: 去重指纹（简化版 — 基于前256字符哈希）
    # 完整版应由 SevenFactorModel.extract_all() 提供
    fingerprint = hashlib.sha256(content[:256].encode()).hexdigest()[:12]

    # 因子7: 终判
    tags = []
    if score >= 0.8:
        tags.append("🟢高质量")
    elif score >= 0.5:
        tags.append("🟡一般")
    else:
        tags.append("🟡低质量")

    passed = score >= KFPP_MIN_CONFIDENCE

    return {
        "passed": passed,
        "score": round(score, 2),
        "blocked_by": None if passed else f"质量评分过低({score:.2f}<{KFPP_MIN_CONFIDENCE})",
        "tags": tags,
        "fingerprint": fingerprint,
    }


def file_hash(path: Path) -> str:
    """快速内容哈希"""
    try:
        h = hashlib.blake2b(digest_size=8)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return "0000000000000000"


def extract_tags(content: str) -> list:
    """从内容中提取龍魂标签"""
    tags = set()
    keywords = ["dna", "确认码", "龍芯", "cnsh", "审计", "签章", "人格",
                "GPG", "三色", "德本", "离火运", "熔断", "鲲鹏", "UID9622"]
    lower = content.lower()
    for kw in keywords:
        if kw.lower() in lower:
            tags.add(kw)
    return list(tags)


def scan_tool(tool_name: str, tool_path: Path) -> tuple:
    """扫描单个工具的输出目录，返回 (通过列表, 拦截列表)"""
    entries = []
    blocked = []
    if not tool_path.exists():
        return entries, blocked

    for f in tool_path.rglob("*"):
        if not f.is_file():
            continue
        if f.suffix.lower() not in INDEX_EXTENSIONS:
            continue
        if f.stat().st_size > KFPP_MAX_FILE_SIZE:
            blocked.append({"file": str(f), "reason": f"超大文件({f.stat().st_size/1024/1024:.1f}MB)"})
            continue

        try:
            # 读取前5000字符用于分析
            content = f.read_text(encoding="utf-8", errors="ignore")[:5000]

            # 🔥 KFPP 七因子过滤（v2.0加固）
            kfpp_result = kfpp_scan(f, content)
            if not kfpp_result["passed"]:
                blocked.append({
                    "file": str(f),
                    "reason": kfpp_result["blocked_by"],
                    "score": kfpp_result["score"],
                    "tags": kfpp_result["tags"],
                })
                continue

            # 通过 KFPP → 入索引
            rel = f.relative_to(HUB_ROOT if tool_name != "claude" else tool_path)
            entry = {
                "tool": tool_name,
                "path": str(rel),
                "name": f.name,
                "stem": f.stem,
                "suffix": f.suffix,
                "size": f.stat().st_size,
                "mtime": datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).isoformat(),
                "content_hash": file_hash(f),
                "tags": extract_tags(content) + kfpp_result["tags"],
                "kfpp_score": kfpp_result["score"],
                "kfpp_fingerprint": kfpp_result["fingerprint"],
                "char_count": len(content),
            }
            entries.append(entry)
        except Exception:
            continue
    return entries, blocked


def build_index(force: bool = False):
    """构建/更新全量索引（含KFPP过滤）"""
    all_entries = []
    all_blocked = []
    stats = {"tools": {}, "total_files": 0, "total_size": 0,
             "blocked_count": 0, "last_scan": ""}

    for tool_name, tool_path in TOOL_PATHS.items():
        entries, blocked = scan_tool(tool_name, tool_path)
        all_entries.extend(entries)
        all_blocked.extend(blocked)
        stats["tools"][tool_name] = {
            "files": len(entries),
            "blocked": len(blocked),
            "size": sum(e["size"] for e in entries),
        }
        stats["total_files"] += len(entries)
        stats["blocked_count"] += len(blocked)
        stats["total_size"] += sum(e["size"] for e in entries)

    stats["last_scan"] = datetime.now(timezone.utc).isoformat()

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    with open(INDEX_FILE, "w") as f:
        json.dump({"entries": all_entries}, f, ensure_ascii=False, indent=2)

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    # 输出拦截摘要
    if all_blocked:
        print(f"\n🛡️ KFPP 拦截 {len(all_blocked)} 个文件:")
        for b in all_blocked[:10]:
            print(f"  🔴 {b['file']} → {b['reason']}")

    return stats


def search_index(query: str):
    """搜索索引"""
    if not INDEX_FILE.exists():
        print("索引不存在，先 build")
        return

    with open(INDEX_FILE) as f:
        data = json.load(f)

    query_lower = query.lower()
    matches = []
    for e in data["entries"]:
        score = 0
        if query_lower in e["name"].lower():
            score += 10
        if query_lower in e.get("stem", "").lower():
            score += 8
        for tag in e.get("tags", []):
            if query_lower in tag.lower():
                score += 5
        if score > 0:
            matches.append((score, e))

    matches.sort(key=lambda x: x[0], reverse=True)
    for score, e in matches[:30]:
        print(f" [{e['tool']:10s}] {e['path']}  ({score})")


def setup_symlinks():
    """设置符号链接：将各工具默认输出链到 Hub"""
    print("🔗 设置符号链接归集...")
    for tool_name, tool_path in TOOL_PATHS.items():
        hub_dir = HUB_ROOT / tool_name
        if tool_name == "claude":
            # Claude 已经直接在 hub 里
            print(f"  ✅ claude: 已在 Hub 内 ({hub_dir})")
            continue
        if tool_name == "kimi":
            print(f"  ✅ kimi: KIMI_OUTPUT_DIR 已指向 {hub_dir}")
            continue
        hub_dir.mkdir(parents=True, exist_ok=True)
        if tool_path.exists() and not tool_path.is_symlink():
            print(f"  ⚠️  {tool_name}: {tool_path} 存在但不是符号链接，需手动迁移")
            print(f"      建议: mv {tool_path} {tool_path}.bak && "
                  f"ln -s {hub_dir} {tool_path}")
        elif tool_path.is_symlink():
            print(f"  ✅ {tool_name}: 已链接 → {os.readlink(tool_path)}")
        else:
            print(f"  📁 {tool_name}: 工具目录尚不存在 ({tool_path})")
    print()


def show_status():
    """显示 Hub 状态"""
    if STATS_FILE.exists():
        with open(STATS_FILE) as f:
            stats = json.load(f)
        print(f"🐉 AI 归集 Hub 状态")
        print(f"━━━━━━━━━━━━━━━━━━━━━━")
        print(f" 总文件:   {stats['total_files']:,}")
        print(f" 总大小:   {stats['total_size']/1024/1024:.1f} MB")
        last = stats.get('last_scan', stats.get('updated', '未知'))[:19]
        print(f" 最后扫描: {last}")
        print(f" 工具分布:")
        for tool, info in stats.get("tools", {}).items():
            if isinstance(info, dict):
                cnt = info.get("files", info.get("count", 0))
            else:
                cnt = info
            bar = "█" * min(int(cnt / 100), 30) if cnt else ""
            print(f"   {tool:12s} {cnt:>6,} 文件  {bar}")
    else:
        print("索引尚未构建")


def main():
    if len(sys.argv) < 2:
        print("用法: lh hub <build|search|link|status>")
        print()
        print("  build   - 构建/更新全量索引")
        print("  search  - 搜索索引 (lh hub search <关键词>)")
        print("  link    - 设置符号链接归集")
        print("  status  - 显示 Hub 状态")
        return

    cmd = sys.argv[1]

    if cmd == "build":
        stats = build_index()
        print(f"✅ 索引完成: {stats['total_files']:,} 文件, "
              f"{stats['total_size']/1024/1024:.1f} MB")
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("请提供搜索关键词")
            return
        search_index(sys.argv[2])
    elif cmd == "link":
        setup_symlinks()
    elif cmd == "status":
        show_status()
    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()

# ⛓️ 龍魂DNA接龍链 ──────────────────────────────
# DNA:V1|丙午·丙申·癸丑·亥时·䷓观|P04鲁班|创建|KFPP七因子过滤升级·v2.0|bhash:3e9c6804|chash:4bf98a09|←GENESIS
# DNA:V2|丙午·丙申·癸丑·亥时·䷓观|P04鲁班|优化|KFPP七因子嵌入·扫描函数重构·索引统计新增blocked_count|bhash:99122311|chash:9cc98b18|←4bf98a09
# ⛓️ 龍魂DNA接龍末端 ──────────────────────────────
