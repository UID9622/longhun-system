#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-08-30-KB-COMMON-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂 · 知识库入库公共模块 v1.0
──────────────────────────────────────────────
lh_kb_ingest / lh_kb_ingest_core / lh_kb_daemon / lh_asi_feed 共享工具。
统一: jsonl 读取容错 · 时间戳 · DNA/ID 生成 · 内容指纹(幂等键) · 原子追加 · 索引重建 · 配额审计。

幂等设计(2026-08-30 工程审查):
  - 幂等键 = 内容指纹(sha256 of user+assistant)，与 DNA 无关；
    DNA 日期动态生成(语义=创建时间)，即使跨天运行 DNA 变化也不重复入库。
  - 兼容库中无 metadata.dna 的旧格式行(指纹从 messages 计算)。
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SYSTEM_PROMPT = (
    "你是龍魂系统助手，核心原则：人民数据主权、平台服务降级、创作者主权优先。"
    "回答需符合龍魂君子协议、CNSH 语义规范和 DNA 追溯要求。"
)

# 域目录名白名单：防 --domain 路径逃逸（P77 #6）
_DOMAIN_SAFE = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff_-]")


def sanitize_domain(domain: str) -> str:
    """域目录名清洗：只留 中英数字/下划线/连字符，杜绝 ../ 等路径逃逸。"""
    d = _DOMAIN_SAFE.sub("", domain or "")
    return d or "misc"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_jsonl(path: Path) -> list:
    """统一 jsonl 读取：空行跳过、坏行计数并打印 warning（不静默吞、不整批抛）。"""
    recs, bad = [], 0
    if not path.exists():
        return recs
    # 🔴 三关判定(2026-08-30·文件身份协议v1.1): 前8KB含NUL→二进制拒绝
    try:
        with open(path, "rb") as f:
            if b"\x00" in f.read(8192):
                return recs
    except OSError:
        return recs
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            recs.append(json.loads(line))
        except Exception as e:
            bad += 1
            if bad <= 3:
                print(f"  ⚠️ {path.name} 坏行跳过: {e}")
    if bad > 3:
        print(f"  ⚠️ {path.name} 共跳过 {bad} 坏行")
    return recs


def gen_dna(content: str, tag: str) -> str:
    """DNA 生成：日期动态(YYYY-MM-DD·本地时间=创建时间)·内容哈希8位。
    注意: 幂等判断用 content_fingerprint，不依赖 DNA 中的日期。"""
    day = datetime.now().strftime("%Y-%m-%d")
    h = hashlib.sha256(content.encode()).hexdigest()[:8]
    return f"#龍芯⚡️{day}-KB-{tag}-{h}-UID9622"


def gen_id(tag: str, content: str) -> str:
    """ID 生成：内容哈希 → 全局唯一·确定性·不随调用序号漂移。
    旧序号 id(story-0000/core-000) 与新哈希 id(story-xxxx/core-xxxx) 不冲突，md 卡永不覆盖旧卡。"""
    h = hashlib.sha256(content.encode()).hexdigest()[:10]
    return f"{tag}-{h}"


def _user_assistant_text(rec: dict) -> str:
    msgs = rec.get("messages", [])
    user = next((m.get("content", "") for m in msgs if m.get("role") == "user"), "")
    assis = next((m.get("content", "") for m in msgs if m.get("role") == "assistant"), "")
    return f"{user}{assis}"


def content_fingerprint(rec: dict) -> str:
    """幂等键：user+assistant 内容指纹（排除固定 system prompt）。
    兼容无 metadata.dna 的旧入库行。"""
    return hashlib.sha256(_user_assistant_text(rec).encode()).hexdigest()


def existing_fingerprints(path: Path) -> set:
    """读取已入库样本内容指纹集（幂等防重复）"""
    return {content_fingerprint(r) for r in read_jsonl(path)}


def atomic_append_jsonl(path: Path, records: list) -> int:
    """批量追加：先拼 batch 字符串再单次写入，降低半途失败留半条的概率。
    半截行防护(P00 P1·2026-08-30): 写前检查文件尾字节；非换行结尾说明存在历史半截行
    (进程中断/异常退出残留)，先补 \\n 再追加，防止新记录被拼进坏行在解析层永久丢失
    (坏行持续吞新追加→幂等重试也永远失败)。
    注: jsonl 训练库量级小，单次 write 为工程折中；真正原子需 temp+replace(代价=全库重写)。"""
    if not records:
        return 0
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0:
        with open(path, "rb") as f:
            f.seek(-1, 2)  # SEEK_END: 定位最后一个字节
            if f.read(1) != b"\n":
                with open(path, "ab") as f2:
                    f2.write(b"\n")
                print(f"  ⚠️ {path.name} 尾部缺换行(半截行残留)，已补 \\n 再追加")
    batch = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records)
    with open(path, "a", encoding="utf-8") as f:
        f.write(batch)
    return len(records)


def dna_hash_ok(rec: dict) -> bool:
    """DNA 一致性校验（P77 #2）：不采信外部 DNA，按内容重算哈希段比对。
    格式: #龍芯⚡️YYYY-MM-DD-KB-{tag}-{h8}-UID9622；提取 {h8} 与 sha256(user+assistant)[:8] 比对。"""
    dna = (rec.get("metadata") or {}).get("dna", "")
    m = re.search(r"-KB-[^-]+-([0-9a-f]{8})-UID9622$", dna)
    if not m:
        return False
    return m.group(1) == content_fingerprint(rec)[:8]


def _extract_dna_from_card(text: str) -> str:
    m = re.search(r"^> DNA:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def rebuild_index(root: Path) -> int:
    """全量扫描 knowledge_base 子目录所有 md 卡 → 重建 INDEX.md（含多域·幂等安全）。
    节能: 仅读卡文件头部文本，不读训练库。"""
    cards = sorted(p for p in root.glob("*/[!I]*.md") if p.stem != "INDEX")
    lines = [
        "# 龍魂 · 通用知识库索引",
        "",
        f"> 重建: {now_utc()} · 全量扫描 {len(cards)} 张知识卡",
        "",
        "| 知识卡 | 领域 | DNA |",
        "|:---|:---|:---|",
    ]
    for p in cards:
        text = p.read_text(encoding="utf-8", errors="replace")
        lines.append(f"| [{p.stem}]({p.parent.name}/{p.name}) | {p.parent.name} | `{_extract_dna_from_card(text)}` |")
    root.mkdir(parents=True, exist_ok=True)
    (root / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(cards)


def quota_report(train_merged: Path) -> dict:
    """全库配额审计（只读 train_merged → lh_triple_guard.quota → 打印）"""
    from lh_triple_guard import quota
    recs = read_jsonl(train_merged)
    q = quota(recs)
    mark = "🟢" if q["quota_ok"] else "🟡 核心域偏低，建议后续补充"
    print(f"✅ 全库配额审计: 核心域占比 {q['core_ratio']:.1%} (阈值 {q['core_min']:.0%}) → {mark} · 库总 {q['total']} 条")
    return q


if __name__ == "__main__":
    # 冒烟自检
    assert sanitize_domain("../../etc") == "etc", "domain 逃逸未拦截"
    assert sanitize_domain("八卦路由") == "八卦路由"
    rec = {"messages": [{"role": "user", "content": "你好"}, {"role": "assistant", "content": "你好！"}]}
    dna = gen_dna("你好你好！", "TEST")
    assert dna_hash_ok({**rec, "metadata": {"dna": dna}}), "DNA 校验自反失败"
    assert content_fingerprint(rec) == content_fingerprint(rec), "指纹不稳定"
    print(f"✅ lh_kb_common 自检通过 · sample_dna={dna}")
