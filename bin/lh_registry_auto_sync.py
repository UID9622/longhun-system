#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·注册表自动同步引擎 v1.0
==============================
DNA: #龍芯⚡️丙午·辛未·乙酉·REGISTRY-AUTO-SYNC-v1.0
用途: 监控关键目录文件变更，自动提取新术语，增量更新语义统一注册表
设计: 扫描→提取→比对→补丁→写入 五步闭环
     支持 --scan 全量 / --watch 监听 / --quick N小时增量 / --auto 自动应用

用法:
  python3 bin/lh_registry_auto_sync.py --scan              # 全量扫描+生成补丁
  python3 bin/lh_registry_auto_sync.py --scan --auto       # 全量扫描+自动应用
  python3 bin/lh_registry_auto_sync.py --watch             # 守护模式·定期扫描
  python3 bin/lh_registry_auto_sync.py --quick 24          # 只扫最近24小时变更
  python3 bin/lh_registry_auto_sync.py --status            # 查看同步状态
  python3 bin/lh_registry_auto_sync.py --diff              # 显示待同步差异
"""

import sys, os, json, re, hashlib, time, subprocess, argparse
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple, Optional, Any

HOME = Path.home()
ROOT = HOME / "longhun-system"

# ═══════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════
REGISTRY_PATH = ROOT / "01_技能庫" / "semantic_unified_registry.json"
STATE_PATH = ROOT / "data" / "registry_sync" / "sync_state.json"
STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

# 监控目录及权重（越核心权重越高）
WATCH_DIRS = {
    "bin/":       {"weight": 1.5, "glob": "*.py",   "cat": "ENGINE"},
    "engine/":    {"weight": 1.5, "glob": "*.py",   "cat": "ENGINE"},
    "engines/":   {"weight": 1.5, "glob": "*.py",   "cat": "ENGINE"},
    "skills/":    {"weight": 1.2, "glob": "*.md",   "cat": "SKILL"},
    "skills.backup/": {"weight": 0.8, "glob": "*.md", "cat": "SKILL"},
    "01_protocols/": {"weight": 1.3, "glob": "*.md","cat": "PROTOCOL"},
    "protocols/": {"weight": 1.3, "glob": "*.md",   "cat": "PROTOCOL"},
    "02_rules/":  {"weight": 1.2, "glob": "*.md",   "cat": "GOVERNANCE"},
    "personas/":  {"weight": 1.2, "glob": "*.md",   "cat": "PERSONA"},
    "docs/":      {"weight": 0.7, "glob": "*.md",   "cat": "DOMAIN"},
    "config/":    {"weight": 0.8, "glob": "*.json", "cat": "INFRA"},
    "deploy/":    {"weight": 0.8, "glob": "*.sh",   "cat": "INFRA"},
    "crypto-stack/": {"weight": 1.4, "glob": "*.py","cat": "CRYPTO"},
    "articles/":  {"weight": 0.6, "glob": "*.md",   "cat": "CULTURE"},
    "papers/":    {"weight": 1.0, "glob": "*.md",   "cat": "BIBLIOGRAPHY"},
    "L1_内核层/":  {"weight": 1.5, "glob": "*",      "cat": "ENGINE"},
    "L7_数据层/":  {"weight": 1.0, "glob": "*",      "cat": "DOMAIN"},
    "L8_治理层/":  {"weight": 1.3, "glob": "*",      "cat": "GOVERNANCE"},
    "integrations/": {"weight": 0.9, "glob": "*.md","cat": "INFRA"},
    "agents/":    {"weight": 1.1, "glob": "*.md",   "cat": "PERSONA"},
}

# 术语提取正则模式（复用Notion提取引擎+文件头专用）
HEADER_PATTERNS = [
    # DNA追溯码
    r'#龍芯⚡️[^\s#]{5,}',
    r'DNA:\s*.+',
    r'#CONFIRM🌌\d+-[\w-]+',
    # 标题/用途
    r'用途[：:]\s*(.+?)(?:\n|$)',
    r'描述[：:]\s*(.+?)(?:\n|$)',
    r'Description[：:]\s*(.+?)(?:\n|$)',
    # 版本号
    r'v\d+\.\d+(?:\.\d+)?',
]

TERM_PATTERNS = [
    # 密码学与安全
    r'(SM[2349]|AES-\d{3}|SHA-\d{3}|HMAC|ECC|RSA|EdDSA|ECDSA|GPG|OpenPGP)',
    r'(数字签名|数字指纹|哈希|散列|加密|解密|密钥|证书|PKI|公钥|私钥)',
    r'(零知识证明|同态加密|多方计算|安全多方|不经意传输|环签名|盲签名)',
    r'(国密|商密|密码机|密码模块|密码算法|SM系列)',
    # 治理与协议
    r'(一票否决|三色审计|三色治理|熔断|硬失败|软降级|降级策略)',
    r'(北辰协议|宪法|L\d+层|P\d+级|M\d+|D-GATE|前置闸门)',
    r'(DNA追溯|DNA签名|DNA验证|DNA绑定|DNA分层|DNA焊死)',
    r'(铁律|不可修订|伦理边界|伦理熔断|IWCB|IW-ECB)',
    # 算法与数学
    r'(三才|模\d+|数字根|369|洛书|河图|五行|阴阳|太极|八卦|六十四卦)',
    r'(七因子|权重|F\d_\w+|态矢量|纠缠|叠加|量子)',
    r'(信息素|蚁群|涌现|自组织|群体智能|蚁后|哨兵蚁)',
    # 系统架构
    r'(神经网络|知识图谱|语义分析|语义解析|NLP|自然语言)',
    r'(微服务|API网关|消息队列|事件溯源|CQRS|DDD)',
    r'(Docker|Kubernetes|SQLite|PostgreSQL|向量数据库|图数据库)',
    r'(FastAPI|Flask|Django|Express|Spring|Vue|React|Next\.js)',
    # CNSH语言
    r'(CNSH|中文编程|字元|关键字|编译器|解释器|运行时|通心译)',
    r'(语义翻译|自然语言编程|意图识别|变量隔离|中文编程)',
    # 哲学与文化
    r'(道德经|易经|周易|孙子兵法|黄帝内经|曾仕强|知行合一)',
    r'(原生态知识|文化输出|文化主权|文化根脉|28星宿|天人合一)',
    r'(道法自然|阴阳调和|中庸|太极图|九宫|四象)',
    # 人物体系
    r'(文心|诸葛亮|宝宝|雯雯|鲁班|管仲|仓颉|孙思邈|苏东坡|李白|屈原|吕蒙|姜子牙)',
    r'(UID9622|诸葛鑫|Lucky|龍芯北辰|老大|乔前辈)',
    # 数据主权
    r'(数据主权|数据归集|数据所有权|数字身份|数字遗产|数字永生)',
    r'(GDPR|个人信息保护法|数据安全法|网络安全法|中国法律)',
    # 特殊术语
    r'(时空织网|ST-GNN|边缘计算|昇腾|鲲鹏|华为云)',
    r'(量子触角|量子路由器|量子熔断|量子态|Bra-Ket)',
    r'(人格矩阵|人格路由|人格切换|人格叠加|人格签章)',
    r'(确认封印|行为签名|设备指纹|主权派生|生态通行证)',
    r'(声影桥|数字甲骨文|语义注册表|语义统一|联动感知)',
    # 拔水军体系
    r'(拔水军|恶意剪辑|虚假评论|举报材料|水军检测|阈值触发)',
    # 文件操作
    r'(\.py|\.md|\.json|\.sh|\.html|\.css|\.js)',
]

# 编译正则
HEADER_RE = re.compile('|'.join(f'({p})' for p in HEADER_PATTERNS), re.IGNORECASE | re.MULTILINE)
TERM_RE = re.compile('|'.join(f'({p})' for p in TERM_PATTERNS), re.IGNORECASE)

# 分类→术语子类型映射
CAT_SUB_MAP = {
    "CRYPTO": "core_concepts",
    "SEVEN_FACTOR": "factors",
    "SEMANTIC": "modules",
    "AI_CREATION": "tools",
    "ENGINE": "engines",
    "SKILL": "skill_locations",
    "PERSONA": "matrix",
    "ALGORITHM": "key_concepts",
    "QUANTUM": "engines",
    "SPACETIME": "engines",
    "GOVERNANCE": "key_concepts",
    "CNSH": "key_modules",
    "CULTURE": "key_concepts",
    "INFRA": "key_modules",
    "PROTOCOL": "key_protocols",
    "DOMAIN": "sample_terms",
    "NOTION": "top_pages",
    "BIBLIOGRAPHY": "papers",
}

# 已知噪音词（文件名/路径中常见但非术语）
NOISE_TERMS = {
    'py', 'md', 'json', 'sh', 'html', 'css', 'js', 'ts', 'tsx', 'jsx',
    'main', 'test', 'index', 'init', 'config', 'setup', 'utils', 'common',
    'readme', 'todo', 'backup', 'old', 'temp', 'tmp', 'draft',
    'bin', 'src', 'lib', 'dist', 'build', 'node_modules',
}


def compute_file_hash(filepath: Path) -> str:
    """计算文件内容哈希"""
    try:
        return hashlib.sha256(filepath.read_bytes()).hexdigest()[:16]
    except:
        return ""


def extract_terms_from_file(filepath: Path) -> Dict[str, List[str]]:
    """从单个文件提取术语"""
    try:
        content = filepath.read_text(errors='replace')
    except:
        return {"terms": [], "headers": []}

    # 提取文件头信息（前100行）
    head = '\n'.join(content.split('\n')[:100])
    headers = [m.group(0).strip() for m in HEADER_RE.finditer(head)]
    headers = [h for h in headers if len(h) > 2 and len(h) < 200]

    # 提取术语
    terms = []
    for m in TERM_RE.finditer(content[:50000]):
        t = m.group(0).strip()
        if t and len(t) >= 2 and len(t) <= 60:
            terms.append(t)

    return {"terms": terms, "headers": headers}


def load_registry() -> dict[str, Any]:
    """加载注册表"""
    if not REGISTRY_PATH.exists():
        print(f"  ❌ 注册表不存在: {REGISTRY_PATH}")
        return {}
    # 移除尾部注释
    lines = REGISTRY_PATH.read_text().split('\n')
    clean = []
    for line in lines:
        if line.strip().startswith('//'):
            break
        clean.append(line)
    return json.loads('\n'.join(clean))


def get_existing_terms(registry: dict[str, Any]) -> Set[str]:
    """从注册表提取已有术语集合"""
    existing = set()
    for cat_key, cat_data in registry.get("categories", {}).items():
        for sub_type in CAT_SUB_MAP.values():
            sub_data = cat_data.get(sub_type, {})
            if isinstance(sub_data, dict):
                for k in sub_data.keys():
                    existing.add(k.lower())
                    existing.add(k)
        # 特殊子类型
        for st in ["stack_layers", "scenarios", "formula", "thresholds",
                    "gates", "layers", "published", "crypto_references",
                    "philosophy_references", "naming_convention", "locations",
                    "full_lexicon", "sync_status", "term_category_index",
                    "top_terms", "page_term_coverage"]:
            sd = cat_data.get(st, {})
            if isinstance(sd, dict):
                for k in sd.keys():
                    existing.add(k.lower())
                    existing.add(k)
        # key_files
        for kf in cat_data.get("key_files", []):
            existing.add(str(kf).lower())
    return existing


def load_sync_state() -> dict[str, Any]:
    """加载同步状态"""
    if STATE_PATH.exists():
        lines = STATE_PATH.read_text().split('\n')
        clean = []
        for line in lines:
            if line.strip().startswith('//'):
                break
            clean.append(line)
        return json.loads('\n'.join(clean))
    return {"last_full_scan": None, "last_quick_scan": None, "file_hashes": {}, "total_scans": 0}


def save_sync_state(state: dict[str, Any]):
    """保存同步状态"""
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def scan_directories(quick_hours: int | None = None) -> Dict[str, dict]:
    """扫描监控目录，返回文件→术语映射"""
    results = {}
    state = load_sync_state()
    old_hashes = state.get("file_hashes", {})
    cutoff = None
    if quick_hours:
        cutoff = time.time() - quick_hours * 3600

    total_files = 0
    changed_files = 0
    new_files = 0

    for dir_path, cfg in WATCH_DIRS.items():
        full_dir = ROOT / dir_path
        if not full_dir.exists():
            continue

        files = list(full_dir.rglob(cfg["glob"]))
        # 排除常见噪音目录
        files = [f for f in files 
                 if '__pycache__' not in str(f) 
                 and 'node_modules' not in str(f)
                 and '.git' not in str(f)
                 and '.codebuddy' not in str(f)
                 and '.venv' not in str(f)
                 and 'venv' not in str(f)]

        for fpath in files:
            total_files += 1
            rel = str(fpath.relative_to(ROOT))

            # Quick模式：按修改时间过滤
            if quick_hours and cutoff:
                try:
                    mtime = fpath.stat().st_mtime
                    if mtime < cutoff:
                        continue
                except:
                    pass

            fhash = compute_file_hash(fpath)
            old_hash = old_hashes.get(rel, "")

            if fhash != old_hash or not old_hash:
                if old_hash:
                    changed_files += 1
                else:
                    new_files += 1

                extracted = extract_terms_from_file(fpath)
                results[rel] = {
                    "hash": fhash,
                    "terms": extracted["terms"],
                    "headers": extracted["headers"],
                    "category": cfg["cat"],
                    "weight": cfg["weight"],
                    "dir": dir_path,
                }

            # 更新哈希
            old_hashes[rel] = fhash

    # 更新状态
    state["file_hashes"] = old_hashes
    state["total_scans"] = state.get("total_scans", 0) + 1
    if quick_hours:
        state["last_quick_scan"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        state["last_quick_hours"] = quick_hours
    else:
        state["last_full_scan"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    save_sync_state(state)

    return results


def aggregate_terms(scanned: Dict[str, dict]) -> Dict[str, dict]:
    """聚合术语 → {term: {files: [...], categories: [...], count: N}}"""
    aggregated = defaultdict(lambda: {"files": [], "categories": set(), "count": 0})

    for fpath, data in scanned.items():
        seen_in_file = set()
        for term in data["terms"]:
            t_clean = term.strip().lower()
            if t_clean in NOISE_TERMS or len(t_clean) < 2:
                continue
            if t_clean not in seen_in_file:
                seen_in_file.add(t_clean)
                aggregated[t_clean]["files"].append(fpath)
                aggregated[t_clean]["categories"].add(data["category"])
                aggregated[t_clean]["count"] += 1

    return dict(aggregated)


def build_patch(aggregated: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    """生成增量补丁——只保留注册表中不存在的新术语"""
    existing = get_existing_terms(registry)
    new_terms = {}
    updated_terms = {}

    for term, info in aggregated.items():
        if term in existing:
            continue  # 已存在，跳过

        # 确定归属分类（categories 是 set，取排序后第一个作为主分类）
        cats = info["categories"]
        primary_cat = sorted(cats)[0] if cats else "DOMAIN"

        # 高频术语才入库（>=2个文件）
        if info["count"] >= 2:
            new_terms[term] = {
                "occurrence": info["count"],
                "files": info["files"][:10],
                "primary_category": primary_cat,
                "all_categories": list(cats) if isinstance(cats, set) else list(cats),
            }

    # 排序：按出现次数降序
    new_terms = dict(sorted(new_terms.items(), key=lambda x: x[1]["occurrence"], reverse=True))

    return {
        "scan_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "new_terms_count": len(new_terms),
        "new_terms": new_terms,
        "total_files_scanned": len(aggregated) if not aggregated else 0,
    }


def apply_patch_to_registry(patch: dict[str, Any], dry_run: bool = False) -> dict[str, Any]:
    """将补丁写入注册表"""
    registry = load_registry()
    if not registry:
        print("  ❌ 无法加载注册表，放弃写入")
        return {"applied": 0, "errors": ["registry load failed"]}

    applied = 0
    errors = []
    new_terms = patch.get("new_terms", {})

    for term, info in new_terms.items():
        cat = info["primary_category"]
        if cat not in CAT_SUB_MAP:
            cat = "DOMAIN"

        sub_type = CAT_SUB_MAP[cat]
        cat_data = registry.setdefault("categories", {}).setdefault(cat, {})
        sub_data = cat_data.setdefault(sub_type, {})

        if term in sub_data:
            continue  # 已有

        sub_data[term] = {
            "name_zh": term,
            "source": "auto_sync",
            "occurrence": info["occurrence"],
            "files": info["files"][:5],
            "added": datetime.now().strftime("%Y-%m-%d"),
        }
        applied += 1

    if not dry_run and applied > 0:
        registry["meta"]["updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        if "auto_sync" not in registry["meta"]:
            registry["meta"]["auto_sync"] = {
                "last_sync": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                "total_terms_added": applied,
                "engine": "lh_registry_auto_sync.py v1.0",
            }

        # 写回
        backup = REGISTRY_PATH.read_text()
        REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2))

    return {"applied": applied, "errors": errors, "dry_run": dry_run}


def cmd_scan(args):
    """全量扫描"""
    print("=" * 60)
    print("🔍 龍魂·注册表自动同步引擎 v1.0 — 全量扫描")
    print("=" * 60)

    if args.quick:
        print(f"  ⚡ 增量模式：只扫描最近 {args.quick} 小时内变更的文件")
        scanned = scan_directories(quick_hours=args.quick)
    else:
        scanned = scan_directories()

    changed = sum(1 for d in scanned.values() if d.get("terms"))
    print(f"  📁 扫描文件: {len(scanned)} 个（{changed} 个含术语）")

    # 聚合
    aggregated = aggregate_terms(scanned)
    print(f"  🏷️  提取术语(去重): {len(aggregated)} 条")

    # 比对注册表
    registry = load_registry()
    patch = build_patch(aggregated, registry)
    print(f"  🆕 新术语(注册表未收录): {patch['new_terms_count']} 条")

    if patch["new_terms_count"] > 0:
        print(f"\n  📋 TOP 20 新术语:")
        for i, (term, info) in enumerate(list(patch["new_terms"].items())[:20]):
            files_preview = ', '.join([f.split('/')[-1][:30] for f in info["files"][:3]])
            print(f"    {i+1:2d}. {term:<30s} ({info['occurrence']}文件) → {info['primary_category']}")
            print(f"        └─ {files_preview}")

    # 保存补丁
    patch_path = ROOT / "data" / "registry_sync" / f"patch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    patch_path.parent.mkdir(parents=True, exist_ok=True)
    patch_path.write_text(json.dumps(patch, ensure_ascii=False, indent=2))
    print(f"\n  💾 补丁已保存: {patch_path}")

    # 自动应用
    if args.auto and patch["new_terms_count"] > 0:
        result = apply_patch_to_registry(patch)
        print(f"  ✅ 自动应用: {result['applied']} 条新术语已写入注册表")
    elif patch["new_terms_count"] > 0:
        print(f"  💡 使用 --auto 自动应用，或手动: python3 bin/lh_registry_auto_sync.py --apply {patch_path.name}")

    state = load_sync_state()
    print(f"\n  📊 同步状态: 总扫描 {state.get('total_scans', 0)} 次 | "
          f"上次全量: {state.get('last_full_scan', 'N/A')} | "
          f"上次增量: {state.get('last_quick_scan', 'N/A')}")


def cmd_watch(args):
    """守护模式·定期扫描"""
    interval = args.interval or 3600
    print("=" * 60)
    print("👁️  龍魂·注册表自动同步引擎 v1.0 — 守护模式")
    print(f"   扫描间隔: {interval}秒 ({interval/60:.0f}分钟)")
    print(f"   按 Ctrl+C 停止")
    print("=" * 60)

    scan_count = 0
    try:
        while True:
            scan_count += 1
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 第 {scan_count} 次扫描...")

            scanned = scan_directories()
            changed = sum(1 for d in scanned.values() if d.get("terms"))
            aggregated = aggregate_terms(scanned)
            registry = load_registry()
            patch = build_patch(aggregated, registry)

            if patch["new_terms_count"] > 0:
                print(f"  🆕 发现 {patch['new_terms_count']} 条新术语")
                if args.auto:
                    result = apply_patch_to_registry(patch)
                    print(f"  ✅ 自动应用: {result['applied']} 条写入注册表")

                # 显示TOP5
                for i, (term, info) in enumerate(list(patch["new_terms"].items())[:5]):
                    print(f"    {i+1}. {term} ({info['occurrence']}文件 → {info['primary_category']})")
            else:
                print(f"  ✅ 无新术语 ({changed}文件变动)")

            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n\n👋 守护模式已停止。共执行 {scan_count} 次扫描。")


def cmd_status(args):
    """查看同步状态"""
    state = load_sync_state()
    registry = load_registry()
    existing = get_existing_terms(registry)

    print("=" * 60)
    print("📊 龍魂·注册表同步状态")
    print("=" * 60)
    print(f"  注册表版本: {registry.get('meta', {}).get('version', 'N/A')}")
    print(f"  注册表条目: {sum(1 for _ in registry.get('categories', {}))}分类 / {len(existing)}已知术语")
    print(f"  总扫描次数: {state.get('total_scans', 0)}")
    print(f"  上次全量扫描: {state.get('last_full_scan', '从未')}")
    print(f"  上次增量扫描: {state.get('last_quick_scan', '从未')}")
    print(f"  文件哈希缓存: {len(state.get('file_hashes', {}))} 文件")
    print(f"  自动同步引擎: v1.0 (lh_registry_auto_sync.py)")


def cmd_diff(args):
    """显示未同步差异"""
    scanned = scan_directories()
    aggregated = aggregate_terms(scanned)
    registry = load_registry()
    existing = get_existing_terms(registry)

    new_terms = {t: i for t, i in aggregated.items() if t not in existing and i["count"] >= 2}

    print("=" * 60)
    print("🔄 注册表差异分析")
    print("=" * 60)
    print(f"  注册表已知术语: {len(existing)}")
    print(f"  文件提取术语: {len(aggregated)}")
    print(f"  🆕 新术语(>=2文件): {len(new_terms)}")

    if new_terms:
        print(f"\n  📋 待同步术语:")
        for i, (term, info) in enumerate(sorted(new_terms.items(), key=lambda x: x[1]["count"], reverse=True)):
            print(f"    {i+1:3d}. {term:<35s} ({info['count']}文件) → {max(info['categories'], key=lambda c: list(info['categories']).count(c))}")
            if i >= 30:
                remaining = len(new_terms) - 30
                if remaining > 0:
                    print(f"    ... 还有 {remaining} 条")
                break
    else:
        print(f"  ✅ 注册表已是最新，无待同步术语")


def main():
    parser = argparse.ArgumentParser(description="龍魂·注册表自动同步引擎 v1.0")
    parser.add_argument("--scan", action="store_true", help="全量扫描所有监控目录")
    parser.add_argument("--watch", action="store_true", help="守护模式·定期扫描")
    parser.add_argument("--quick", type=int, default=None, help="快速模式·只扫描最近N小时内变更的文件")
    parser.add_argument("--auto", action="store_true", help="自动应用补丁到注册表")
    parser.add_argument("--interval", type=int, default=3600, help="守护模式扫描间隔(秒)·默认3600")
    parser.add_argument("--status", action="store_true", help="查看同步状态")
    parser.add_argument("--diff", action="store_true", help="显示注册表差异")
    parser.add_argument("--apply", type=str, default=None, help="手动应用指定补丁文件")

    args = parser.parse_args()

    if args.apply:
        patch_path = ROOT / "data" / "registry_sync" / args.apply
        if not patch_path.exists():
            patch_path = Path(args.apply)
        if not patch_path.exists():
            print(f"❌ 补丁文件不存在: {args.apply}")
            sys.exit(1)
        lines = patch_path.read_text().split('\n')
        clean = []
        for line in lines:
            if line.strip().startswith('//'):
                break
            clean.append(line)
        patch = json.loads('\n'.join(clean))
        result = apply_patch_to_registry(patch)
        print(f"✅ 已应用: {result['applied']} 条术语写入注册表")
    elif args.status:
        cmd_status(args)
    elif args.diff:
        cmd_diff(args)
    elif args.watch:
        cmd_watch(args)
    elif args.scan or args.quick:
        cmd_scan(args)
    else:
        # 默认：quick diff + scan
        print("龍魂·注册表自动同步引擎 v1.0")
        print("用法: python3 bin/lh_registry_auto_sync.py [--scan|--watch|--status|--diff|--quick N]")
        print()
        cmd_status(args)

if __name__ == "__main__":
    main()
