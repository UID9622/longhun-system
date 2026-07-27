#!/usr/bin/env python3
"""
龍魂·知识库扩展自动化引擎 v1.1（精修版）
DNA: #龍芯⚡️丙午·乙未·戊戌·巳时·☵坎-KB-EXPAND-AUTO-v1.1
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

一键自动化: 爬取 → 索引 → 训练
   lh_kb_expand.py crawl                 # 爬取P0+P1知识源
   lh_kb_expand.py index                 # 生成网站索引
   lh_kb_expand.py train                 # 准备数据+训练模型（一步到位）
   lh_kb_expand.py all                   # 一键全流程
   lh_kb_expand.py status                # 查看知识库状态

设计原则:
  - P0协议: 摘要只取·全文人工确认
  - 数据主权归本地·不传云
  - 每步DNA绑定·全程可追溯
  - 网站索引自动生成·搜得到·看得见
  - 重试不退让·失败不沉默
"""

import json
import os
import sys
import hashlib
import argparse
import subprocess
import time
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

CST = timezone(timedelta(hours=8))

# ━━━━━━━━━━ 路径常量 ━━━━━━━━━━
PROJECT_ROOT = Path(__file__).parent.parent
SOURCES_DIR = PROJECT_ROOT / "data" / "sources"
KNOWLEDGE_DIR = PROJECT_ROOT / "data" / "knowledge"
INDEX_DIR = PROJECT_ROOT / "portal" / "knowledge"
AUDIT_DIR = PROJECT_ROOT / "audit"
FETCH_SCRIPT = SOURCES_DIR / "lh_fetch_engine.py"
CLEAN_SCRIPT = SOURCES_DIR / "lh_data_cleaner.py"
SOURCE_MANAGER = SOURCES_DIR / "lh_source_manager.py"
BRIDGE_SCRIPT = PROJECT_ROOT / "bin" / "lh_data_to_train_bridge.py"
TRAIN_SCRIPT = PROJECT_ROOT / "bin" / "lh_lora_trainer_v4.py"

# ━━━━━━━━━━ DNA/身份 ━━━━━━━━━━
DNA = "#龍芯⚡️丙午·乙未·戊戌·巳时·☵坎-KB-EXPAND-AUTO-v1.1"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
CREATOR = "诸葛鑫（UID9622·龍芯北辰）"

# ━━━━━━━━━━ 可配阈值 ━━━━━━━━━━
DEFAULT_QUALITY_MIN = 0.4       # 索引最低质量分
DEFAULT_CRAWL_LIMIT = 50        # 每源最多篇数
DEFAULT_RETRY = 3               # 网络操作重试次数
DEFAULT_RETRY_BACKOFF = 2.0     # 退避基数（秒）
STEP_TIMEOUT = 900              # 单步超时（秒）
TRAIN_TIMEOUT = 3600            # 训练超时（秒）


# ═══════════════════════════════════════════
# Audit trail
# ═══════════════════════════════════════════

@dataclass
class AuditEntry:
    """审计记录"""
    step: str
    status: str          # OK / FAIL / WARN / SKIP
    started_at: str
    duration_sec: float
    details: str = ""
    dna: str = DNA

_audit_trail: list[AuditEntry] = []


def audit_log(step: str, status: str, started: float, details: str = ""):
    """记录审计条目"""
    dur = round(time.time() - started, 2)
    entry = AuditEntry(
        step=step, status=status,
        started_at=datetime.fromtimestamp(started, CST).isoformat(),
        duration_sec=dur, details=details
    )
    _audit_trail.append(entry)
    # 落盘追加
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    audit_file = AUDIT_DIR / "kb_expand_audit.jsonl"
    with open(audit_file, 'a') as f:
        f.write(json.dumps({
            "step": entry.step, "status": entry.status,
            "started_at": entry.started_at, "duration_sec": entry.duration_sec,
            "details": entry.details, "dna": entry.dna
        }, ensure_ascii=False) + "\n")


def audit_summary():
    """审计摘要 → stdout"""
    if not _audit_trail:
        return
    ok = sum(1 for e in _audit_trail if e.status == "OK")
    fail = sum(1 for e in _audit_trail if e.status == "FAIL")
    warn = sum(1 for e in _audit_trail if e.status == "WARN")
    total_dur = sum(e.duration_sec for e in _audit_trail)
    print(f"\n📋 审计摘要: {ok}✅ {fail}🔴 {warn}🟡 · 总耗时 {total_dur:.1f}s")


# ━━━━━━━━━━ 工具函数 ━━━━━━━━━━

def now_ts(fmt: str = "%H:%M:%S") -> str:
    return datetime.now(CST).strftime(fmt)


def now_full() -> str:
    return datetime.now(CST).isoformat()


def log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "STEP": "⚙️"}
    prefix = markers.get(level, "ℹ️")
    print(f"[{now_ts()}] {prefix} {msg}")


def run_step(
    cmd: list[str],
    desc: str,
    cwd: Optional[str] = None,
    timeout: int = STEP_TIMEOUT,
    retry: int = DEFAULT_RETRY,
    halt: bool = False
) -> tuple[bool, str]:
    """
    执行一步，支持重试+指数退避。
    返回 (成功, 详情)。
    halt=True 时失败即抛异常。
    """
    log(f"执行: {desc}", "STEP")
    started = time.time()
    last_err = ""

    for attempt in range(1, retry + 1):
        try:
            result = subprocess.run(
                cmd,
                cwd=cwd or str(PROJECT_ROOT),
                capture_output=True, text=True, timeout=timeout
            )
            if result.returncode == 0:
                log(f"{desc} → 完成", "OK")
                audit_log(desc, "OK", started, f"attempt={attempt}")
                return True, result.stdout[:1000]
            else:
                last_err = result.stderr.strip()[:500] or f"exit code={result.returncode}"
                log(f"{desc} → 失败 (attempt {attempt}/{retry})", "ERROR" if attempt == retry else "WARN")
                if attempt < retry:
                    wait = DEFAULT_RETRY_BACKOFF ** attempt
                    log(f"   {wait:.0f}s 后重试...", "WARN")
                    time.sleep(wait)

        except subprocess.TimeoutExpired:
            last_err = f"超时 ({timeout}s)"
            log(f"{desc} → 超时 (attempt {attempt}/{retry})", "ERROR" if attempt == retry else "WARN")
            if attempt < retry:
                time.sleep(DEFAULT_RETRY_BACKOFF ** attempt)

        except Exception as e:
            last_err = str(e)
            log(f"{desc} → 异常: {e}", "ERROR")
            break  # 非网络异常不重试

    audit_log(desc, "FAIL", started, last_err[:200])
    if halt:
        raise RuntimeError(f"关键步骤失败: {desc} → {last_err}")
    return False, last_err


def count_lines(path: Path) -> int:
    """快速计行（jsonl文件行数）"""
    if not path.exists():
        return 0
    try:
        with open(path) as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


# ═══════════════════════════════════════════
# Step 1: 爬取
# ═══════════════════════════════════════════

def crawl_sources(
    priority: str = "P0,P1",
    limit: int = DEFAULT_CRAWL_LIMIT,
    dry_run: bool = False,
    parallel: bool = False
) -> bool:
    """爬取知识源 · 支持P0/P1/P2优先级"""
    log(f"🕷️ 知识爬取启动 · 优先级: {priority} · 每源最多 {limit} 篇")
    log(f"   DNA: {DNA}")

    if not FETCH_SCRIPT.exists():
        log("拉取引擎不存在: data/sources/lh_fetch_engine.py", "ERROR")
        log("  请确保项目完整", "ERROR")
        return False

    if dry_run:
        return _crawl_dry_run(priority, limit)

    priorities = [p.strip() for p in priority.split(",")]
    all_ok = True

    for p in priorities:
        ok, output = run_step(
            [sys.executable, str(FETCH_SCRIPT), "--priority", p],
            f"拉取 {p} 优先级源",
            timeout=STEP_TIMEOUT
        )
        if not ok:
            all_ok = False
        else:
            # 显示拉取摘要
            fetched_dir = SOURCES_DIR / "fetched"
            if fetched_dir.exists():
                recent = sorted(fetched_dir.glob("*.jsonl"), key=lambda x: x.stat().st_mtime, reverse=True)
                if recent:
                    lines = count_lines(recent[0])
                    log(f"  {p}: 最新文件 {recent[0].name} ({lines} 条)")

    # 拉取统计
    fetched_dir = SOURCES_DIR / "fetched"
    if fetched_dir.exists():
        files = list(fetched_dir.glob("*.jsonl"))
        total_lines = sum(count_lines(f) for f in files)
        log(f"拉取汇总: {len(files)} 文件 · {total_lines} 条")

    return all_ok


def _crawl_dry_run(priority: str, limit: int) -> bool:
    """模拟爬取 · 只检查源可用性不实际拉取"""
    log("🔍 干跑模式 · 检查源配置...")
    sources_file = SOURCES_DIR / "sources.json"
    if not sources_file.exists():
        log("sources.json 不存在", "ERROR")
        return False

    with open(sources_file) as f:
        config = json.load(f)

    priorities = [p.strip() for p in priority.split(",")]
    sources = config.get("sources", [])

    matched = [s for s in sources if s.get("priority", "") in priorities]
    log(f"匹配 {len(matched)} 个源 ({len(sources)} 个总源)")

    for s in matched[:20]:  # 只显示前20个
        name = s.get("name", s.get("id", "?"))
        url = s.get("url", "?")
        pri = s.get("priority", "?")
        cat = s.get("category", "?")
        enabled = s.get("enabled", True)
        status = "🟢" if enabled else "🔴禁用"
        print(f"  {status} [{pri}] {name} → {url[:60]}...")
        print(f"       分类: {cat}")

    if len(matched) > 20:
        print(f"  ... 还有 {len(matched)-20} 个源")
    print(f"\n  干跑完成 · 未实际爬取")
    return True


# ═══════════════════════════════════════════
# Step 2: 索引生成
# ═══════════════════════════════════════════

def generate_index(quality_min: float = DEFAULT_QUALITY_MIN, dry_run: bool = False) -> bool:
    """从清洗数据构建网站知识索引 JSON"""
    log(f"📇 生成知识索引 · 质量阈值 ≥ {quality_min}")

    cleaned_dir = SOURCES_DIR / "cleaned"
    if not cleaned_dir.exists() or not list(cleaned_dir.glob("*_cleaned.jsonl")):
        log("没有清洗数据，先执行 crawl（含清洗）", "WARN")
        return False

    # 加载来源配置
    sources_file = SOURCES_DIR / "sources.json"
    source_map: dict[str, dict] = {}
    if sources_file.exists():
        with open(sources_file) as f:
            src_config = json.load(f)
        cats = src_config.get("categories", {})
        for s in src_config.get("sources", []):
            sid = s.get("id", "")
            cat_id = s.get("category", "")
            cat_name = cats.get(cat_id, {}).get("name", cat_id) if cat_id else ""
            source_map[sid] = {
                "name": s.get("name", sid),
                "category_id": cat_id,
                "category_name": cat_name
            }

    # 读取清洗数据
    articles = []
    for cf in sorted(cleaned_dir.glob("*_cleaned.jsonl")):
        with open(cf) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    art = json.loads(line)
                    articles.append(art)
                except json.JSONDecodeError:
                    continue

    log(f"读取 {len(articles)} 条清洗数据")

    if not articles:
        log("无数据可索引", "WARN")
        return False

    # 构建索引
    kb_index = {
        "dna": DNA,
        "confirm": CONFIRM,
        "generated_at": now_full(),
        "total_articles": 0,
        "categories": {},
        "articles": [],
        "source_stats": {},
        "index_version": "v1.1",
        "quality_threshold": quality_min,
    }

    source_counts: Counter = Counter()
    category_counts: Counter = Counter()
    indexed = 0
    filtered_low_quality = 0

    for art in articles:
        q = art.get("quality", {})
        score = q.get("score", 0)
        if score < quality_min:
            filtered_low_quality += 1
            continue

        source_id = art.get("metadata", {}).get("source_id", "")
        source_name = art.get("source_name", "未知来源")
        sm = source_map.get(source_id, {})
        category_name = sm.get("category_name", "")
        category_id = sm.get("category_id", "")

        source_counts[source_name] += 1
        if category_name:
            category_counts[category_name] += 1

        entry = {
            "title": art.get("title", ""),
            "summary": (art.get("content", "") or "")[:200],
            "source": source_name,
            "source_id": source_id,
            "category": category_name,
            "category_id": category_id,
            "url": art.get("url", ""),
            "fetched_at": art.get("metadata", {}).get("fetched_at", ""),
            "dna": art.get("metadata", {}).get("dna", ""),
            "quality": round(score, 2),
        }
        kb_index["articles"].append(entry)
        indexed += 1

    kb_index["total_articles"] = indexed
    kb_index["categories"] = {
        cat: {"count": cnt, "label": cat}
        for cat, cnt in category_counts.most_common()
    }
    kb_index["source_stats"] = dict(source_counts.most_common(50))
    kb_index["filtered_low_quality"] = filtered_low_quality

    if dry_run:
        log(f"干跑: 将生成 {indexed} 条索引 (过滤 {filtered_low_quality} 条低质量)", "OK")
        print(f"  分类: {', '.join(f'{k}({v})' for k, v in category_counts.most_common(10))}")
        print(f"  来源 Top5: {dict(source_counts.most_common(5))}")
        return True

    # 写入
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    index_file = INDEX_DIR / "kb_index.json"
    with open(index_file, 'w') as f:
        json.dump(kb_index, f, ensure_ascii=False, indent=2)

    size_kb = index_file.stat().st_size / 1024
    log(f"索引已生成: {index_file}", "OK")
    log(f"  条目: {indexed} · 分类: {len(kb_index['categories'])} · 来源: {len(kb_index['source_stats'])} · 大小: {size_kb:.1f}KB")
    log(f"  过滤低质量: {filtered_low_quality} 条")

    return True


# ═══════════════════════════════════════════
# Step 3: 训练（数据准备 + 训练 → 一步到位）
# ═══════════════════════════════════════════

def run_training(dry_run: bool = False, halt: bool = True) -> bool:
    """train = 桥接数据 + 触发训练，一步完成"""
    log("🏋️ 训练流程启动 · 数据准备 → 模型训练")

    # 3a. 检查清洗数据
    cleaned_dir = SOURCES_DIR / "cleaned"
    if not cleaned_dir.exists():
        log("清洗目录不存在", "ERROR")
        return False
    cleaned_files = list(cleaned_dir.glob("*_cleaned.jsonl"))
    if not cleaned_files:
        log("无清洗数据可训练", "WARN")
        return False

    cleaned_count = sum(count_lines(f) for f in cleaned_files)
    log(f"清洗数据: {cleaned_count} 条 ({len(cleaned_files)} 文件)")

    if cleaned_count < 10:
        log(f"数据量太少 ({cleaned_count}条)，至少需要10条", "WARN")
        return False

    # 检查现有训练数据
    train_file = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output" / "data" / "train.jsonl"
    existing_count = count_lines(train_file)
    if existing_count > 0:
        log(f"现有训练数据: {existing_count} 条")
        new_count = cleaned_count - existing_count
        if new_count <= 0:
            log("无新数据需训练", "INFO")
            return True
        log(f"新增: {new_count} 条")

    # 3b. 桥接（训练数据准备）
    if dry_run:
        log("干跑: 将桥接 {cleaned_count} 条 → 训练格式", "OK")
        return True

    ok, output = run_step(
        [sys.executable, str(BRIDGE_SCRIPT)],
        "训练数据桥接",
        timeout=STEP_TIMEOUT,
        halt=False  # 桥接失败不终止，给用户看具体原因
    )
    if not ok:
        log("数据桥接失败 · 请检查清洗数据格式", "ERROR" if halt else "WARN")
        if halt:
            return False

    # 3c. 触发训练
    if not TRAIN_SCRIPT.exists():
        log(f"训练脚本不存在: {TRAIN_SCRIPT}", "ERROR")
        log("请确认 lh_lora_trainer_v4.py 路径正确或在鲲鹏端执行", "INFO")
        return False

    log("🔥 触发 LoRA 训练...")
    ok, output = run_step(
        [sys.executable, str(BRIDGE_SCRIPT), "--train"],
        "触发模型训练",
        timeout=TRAIN_TIMEOUT,
        halt=False
    )
    if ok:
        log("训练已触发 · 查看训练输出确认进度", "OK")
        log("  训练完成后: python3 bin/lh_data_to_train_bridge.py --full-pipeline", "INFO")
    else:
        log("训练触发异常 · 检查 GPU/MLX 环境", "ERROR" if halt else "WARN")

    return ok


# ═══════════════════════════════════════════
# Status
# ═══════════════════════════════════════════

def show_status():
    """知识库全景状态"""
    print(f"\n{'='*62}")
    print(f"  🐉 龍魂知识库状态")
    print(f"  {DNA}")
    print(f"{'='*62}")

    # ── 拉取 ──
    fetched_count = 0
    fetched_dir = SOURCES_DIR / "fetched"
    if fetched_dir.exists():
        fetched_files = sorted(fetched_dir.glob("*.jsonl"))
        fetched_count = sum(count_lines(f) for f in fetched_files)
        # 最后拉取时间
        last_fetch_ts = max((f.stat().st_mtime for f in fetched_files), default=0)
        last_fetch = datetime.fromtimestamp(last_fetch_ts, CST).strftime("%Y-%m-%d %H:%M") if last_fetch_ts else "从未"
        print(f"\n📥 拉取状态: {fetched_count} 条 ({len(fetched_files)} 文件)")
        print(f"   最后拉取: {last_fetch}")
    else:
        print(f"\n📥 拉取状态: 无数据")

    # ── 清洗 ──
    cleaned_count = 0
    cleaned_dir = SOURCES_DIR / "cleaned"
    if cleaned_dir.exists():
        cleaned_files = sorted(cleaned_dir.glob("*_cleaned.jsonl"))
        cleaned_count = sum(count_lines(f) for f in cleaned_files)
        last_clean_ts = max((f.stat().st_mtime for f in cleaned_files), default=0)
        last_clean = datetime.fromtimestamp(last_clean_ts, CST).strftime("%Y-%m-%d %H:%M") if last_clean_ts else "从未"
        # 质量分布
        quality_scores = []
        for cf in cleaned_files[:5]:  # 抽样前5文件
            with open(cf) as f:
                for line in f:
                    try:
                        q = json.loads(line.strip()).get("quality", {}).get("score")
                        if q is not None:
                            quality_scores.append(q)
                    except (json.JSONDecodeError, AttributeError):
                        pass
                    if len(quality_scores) >= 200:
                        break
            if len(quality_scores) >= 200:
                break
        print(f"🧹 清洗状态: {cleaned_count} 条 ({len(cleaned_files)} 文件)")
        print(f"   最后清洗: {last_clean}")
        if quality_scores:
            avg_q = sum(quality_scores) / len(quality_scores)
            high_q = sum(1 for s in quality_scores if s >= 0.7)
            print(f"   质量抽样: 均值 {avg_q:.2f} · ≥0.7: {high_q}/{len(quality_scores)}")
    else:
        print(f"🧹 清洗状态: 无数据")

    # ── 索引 ──
    index_file = INDEX_DIR / "kb_index.json"
    if index_file.exists():
        with open(index_file) as f:
            idx = json.load(f)
        idx_count = idx.get("total_articles", 0)
        idx_time = idx.get("generated_at", "未知")
        idx_ver = idx.get("index_version", "?")
        cats = idx.get("categories", {})
        print(f"📇 索引状态: {idx_count} 条 (v{idx_ver})")
        print(f"   生成时间: {idx_time}")
        if cats:
            cats_str = ', '.join(f'{k}({v.get("count",0)})' for k, v in sorted(cats.items()))
            print(f"   分类: {cats_str}")
        filtered = idx.get("filtered_low_quality", 0)
        if filtered:
            print(f"   过滤低质量: {filtered} 条")
    else:
        print(f"📇 索引状态: 未生成")

    # ── 训练数据 ──
    train_file = PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output" / "data" / "train.jsonl"
    train_count = count_lines(train_file)
    if train_count:
        train_mtime = datetime.fromtimestamp(train_file.stat().st_mtime, CST).strftime("%Y-%m-%d %H:%M")
        print(f"🏋️ 训练数据: {train_count} 条 · 更新: {train_mtime}")
    else:
        print(f"🏋️ 训练数据: 未准备")

    # ── 爬虫状态 ──
    crawler_log = SOURCES_DIR / "crawler_state.json"
    if crawler_log.exists():
        with open(crawler_log) as f:
            cs = json.load(f)
        print(f"\n🕷️ 爬虫追踪:")
        print(f"   上次运行: {cs.get('last_crawl', '未知')}")
        print(f"   累计爬取: {cs.get('total_crawls', 0)}")
        print(f"   已配源:   {len(cs.get('sources', {}))}")

    # ── 源配置 ──
    sources_file = SOURCES_DIR / "sources.json"
    if sources_file.exists():
        with open(sources_file) as f:
            cfg = json.load(f)
        src_list = cfg.get("sources", [])
        enabled = sum(1 for s in src_list if s.get("enabled", True))
        disabled = len(src_list) - enabled
        p0 = sum(1 for s in src_list if s.get("priority") == "P0")
        p1 = sum(1 for s in src_list if s.get("priority") == "P1")
        print(f"\n🔧 源配置: {len(src_list)} 总源 · 启用 {enabled} · 禁用 {disabled}")
        print(f"   P0: {p0} · P1: {p1}")

    # ── 磁盘 ──
    data_dir = PROJECT_ROOT / "data"
    if data_dir.exists():
        total_size = sum(f.stat().st_size for f in data_dir.rglob("*") if f.is_file())
        size_mb = total_size / (1024 * 1024)
        print(f"\n💾 数据目录: {size_mb:.1f} MB")

    # ── 数据新鲜度 ──
    freshness = _calc_freshness(fetched_count, cleaned_count, train_count)
    print(f"\n📊 数据流转: 拉取{_ratio_str(cleaned_count, fetched_count)}→清洗{_ratio_str(train_count, cleaned_count)}→训练")

    # ── 操作建议 ──
    print(f"\n💡 操作建议:")
    if cleaned_count == 0:
        print(f"   python3 bin/lh_kb_expand.py crawl")
    elif not index_file.exists():
        print(f"   python3 bin/lh_kb_expand.py index")
    elif train_count == 0:
        print(f"   python3 bin/lh_kb_expand.py train")
    else:
        diff = cleaned_count - train_count
        if diff > 10:
            print(f"   → {diff} 条新数据待入训: python3 bin/lh_kb_expand.py train")
        elif diff > 0:
            print(f"   → {diff} 条（少量）等待下次批量训练")
        else:
            print(f"   → 数据已同步 · 可重新训练: python3 bin/lh_kb_expand.py train")

    # ── 审计 ──
    audit_file = AUDIT_DIR / "kb_expand_audit.jsonl"
    if audit_file.exists():
        audit_lines = count_lines(audit_file)
        print(f"\n📋 审计记录: {audit_lines} 条 → audit/kb_expand_audit.jsonl")

    print(f"{'='*62}\n")


def _ratio_str(a: int, b: int) -> str:
    """比率显示（处理0分母）"""
    if b == 0:
        return "—"
    pct = a / b * 100
    if pct >= 100:
        return f"{a}/{b}"
    return f"{a}/{b} ({pct:.0f}%)"


def _calc_freshness(fetched: int, cleaned: int, trained: int) -> dict:
    """数据新鲜度计算"""
    stale = max(0, fetched - cleaned)
    untrained = max(0, cleaned - trained)
    return {
        "fetched": fetched, "cleaned": cleaned, "trained": trained,
        "stale": stale, "untrained": untrained,
        "health": "🟢" if stale < 100 and untrained < 100 else
                  "🟡" if stale < 500 else "🔴"
    }


# ═══════════════════════════════════════════
# Main
# ═══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂知识库扩展自动化引擎 v1.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
快速上手:
  python3 bin/lh_kb_expand.py crawl              爬取P0+P1知识源
  python3 bin/lh_kb_expand.py index              生成网站索引
  python3 bin/lh_kb_expand.py train              准备数据+训练模型
  python3 bin/lh_kb_expand.py all                一键全流程
  python3 bin/lh_kb_expand.py status             查看状态

高级:
  python3 bin/lh_kb_expand.py crawl --dry-run    模拟爬取，不真实触网
  python3 bin/lh_kb_expand.py index --quality 0.6 提高索引质量阈值
  python3 bin/lh_kb_expand.py all --halt-on-error  遇错即停（默认继续）
  python3 bin/lh_kb_expand.py all --skip-train     只到索引，不训练
        """
    )

    subp = parser.add_subparsers(dest="command", help="操作命令")

    # ── crawl ──
    c = subp.add_parser("crawl", help="爬取知识源")
    c.add_argument("-p", "--priority", default="P0,P1", help="优先级 (默认: P0,P1)")
    c.add_argument("-l", "--limit", type=int, default=DEFAULT_CRAWL_LIMIT,
                   help=f"每源最多篇数 (默认: {DEFAULT_CRAWL_LIMIT})")
    c.add_argument("--dry-run", action="store_true", help="模拟爬取，不实际触网")

    # ── index ──
    i = subp.add_parser("index", help="生成网站知识索引")
    i.add_argument("-q", "--quality", type=float, default=DEFAULT_QUALITY_MIN,
                   help=f"质量阈值 (默认: {DEFAULT_QUALITY_MIN})")
    i.add_argument("--dry-run", action="store_true", help="预览索引不写入")

    # ── train ──
    t = subp.add_parser("train", help="准备训练数据+触发训练（一步到位）")
    t.add_argument("--dry-run", action="store_true", help="预览不执行")
    t.add_argument("--no-train", action="store_true", help="只准备数据·不触发训练")

    # ── all ──
    a = subp.add_parser("all", help="一键全流程")
    a.add_argument("-p", "--priority", default="P0,P1", help="优先级 (默认: P0,P1)")
    a.add_argument("-l", "--limit", type=int, default=DEFAULT_CRAWL_LIMIT,
                   help=f"每源最多篇数 (默认: {DEFAULT_CRAWL_LIMIT})")
    a.add_argument("-q", "--quality", type=float, default=DEFAULT_QUALITY_MIN,
                   help=f"索引质量阈值 (默认: {DEFAULT_QUALITY_MIN})")
    a.add_argument("--skip-train", action="store_true", help="跳过训练")
    a.add_argument("--halt-on-error", action="store_true", help="遇关键错误立即停止（默认继续）")

    # ── status ──
    _ = subp.add_parser("status", help="查看知识库状态")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 启动签名
    print(f"\n🐉 龍魂知识库扩展引擎 v1.1")
    print(f"🐉 {DNA}")
    print(f"🐉 {CONFIRM}")
    print(f"🐉 {CREATOR}\n")

    start_time = time.time()

    # ── status ──
    if args.command == "status":
        show_status()
        return

    # ── crawl ──
    elif args.command == "crawl":
        ok = crawl_sources(args.priority, args.limit, dry_run=args.dry_run)
        audit_summary()
        if args.dry_run:
            return
        show_status() if ok else log("爬取未完全成功", "WARN")

    # ── index ──
    elif args.command == "index":
        ok = generate_index(quality_min=args.quality, dry_run=args.dry_run)
        audit_summary()
        show_status()

    # ── train ──
    elif args.command == "train":
        if args.dry_run:
            cleaned_count = sum(
                count_lines(f) for f in (SOURCES_DIR / "cleaned").glob("*_cleaned.jsonl")
            ) if (SOURCES_DIR / "cleaned").exists() else 0
            train_count = count_lines(
                PROJECT_ROOT / "models" / "longhun-v1.0" / "lora_output" / "data" / "train.jsonl"
            )
            log(f"干跑: 清洗数据 {cleaned_count} 条 · 现有训练数据 {train_count} 条", "OK")
            if cleaned_count > train_count:
                log(f"  将新增 {cleaned_count - train_count} 条训练数据", "INFO")
            else:
                log("  无新数据需添加", "INFO")
            return
        ok = run_training()
        audit_summary()
        show_status()

    # ── all ──
    elif args.command == "all":
        halt = args.halt_on_error
        log("🚀 一键全流程启动")

        # Step 1: 爬取
        ok1 = crawl_sources(args.priority, args.limit)
        if not ok1 and halt:
            log("爬取失败 · --halt-on-error 触发停止", "ERROR")
            audit_summary()
            sys.exit(1)

        # Step 2: 索引
        ok2 = generate_index(quality_min=args.quality)
        if not ok2 and halt:
            log("索引生成失败 · --halt-on-error 触发停止", "ERROR")
            audit_summary()
            sys.exit(1)

        # Step 3: 训练
        if args.skip_train:
            log("跳过训练 (--skip-train)", "INFO")
        else:
            ok3 = run_training(halt=halt)
            if not ok3 and halt:
                log("训练失败 · --halt-on-error 触发停止", "ERROR")
                audit_summary()
                sys.exit(1)

        audit_summary()
        show_status()

    total_dur = time.time() - start_time
    log(f"总耗时: {total_dur:.1f}s", "OK")


if __name__ == "__main__":
    main()
