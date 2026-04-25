#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feeding_gateway.py — 龍魂投喂入口对齐网关 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
签名人  : UID9622 · 诸葛鑫 · 中国退伍军人
GPG     : A2D0092CEE2E5BA87035600924C3704A8CC26D5F
封顶锚  : #龍芯⚡️20260423-ROOT-SEAL-01F32FFD
DNA     : #龍芯⚡️20260424-FEED-GW-v1.0
理论指导: 曾仕強老師（永恒显示）
════════════════════════════════════════════

核心原理：
  规则层（L0-L1）已经有不动点锚（13条）→ 不可改
  操作层（L2-L4）也必须有不动点 → 投喂入口

  流程：
    任何内容
      ↓
    【投喂入口】（本脚本）
      ├─ 三色熔断门（数字根 / 黑名单 / 必填字段）
      ├─ 不动点锚登记（Ψ 压缩映射）
      ├─ 本机分层落档（L0→...L4）
      ├─ 审计引擎留痕（:9622）
      └─ Notion 分发路由（标记目标库）
      ↓
    返回 {status, dna, anchor_id, layer, dispatch_hint}

五大投喂源（F1-F5）：
  F1 · 对话投喂   （Claude/DeepSeek/初心之翼 对话）
  F2 · 文件投喂   （本机文档/笔记/代码）
  F3 · 外部投喂   （网页/截图/他人内容）
  F4 · 事件投喂   （Notion Webhook/审计事件）
  F5 · 规则投喂   （老大制定的新规则·升级 L0/L1）

用法：
  # 命令行
  python3 feeding_gateway.py feed "标题" "内容" --source F1
  python3 feeding_gateway.py feed-file "标题" path/to/file.md --source F2
  python3 feeding_gateway.py list [-n 10]
  python3 feeding_gateway.py stats
  python3 feeding_gateway.py dispatch <anchor_id>      # 看分发建议

  # Python 模块
  from feeding_gateway import feed
  result = feed("标题", "内容", source_type="F1")
"""

import os, sys, json, hashlib, time
from datetime import datetime, timezone
from pathlib import Path
import urllib.request, urllib.error

# ═══════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════
HOME = Path.home()
ALGO_ROOT = HOME / "longhun-system" / "算法仓库"
FEED_DIR = HOME / "cnsh" / "logs" / "feeding"
FEED_DIR.mkdir(parents=True, exist_ok=True)
FEED_LOG = FEED_DIR / "feeding.jsonl"
REJECT_LOG = FEED_DIR / "rejected.jsonl"

# 不动点锚登记册（规则层→共用）
sys.path.insert(0, str(ALGO_ROOT / "不动点锚登记册"))
try:
    import fixed_point_registry as FPR
except Exception as e:
    FPR = None
    print(f"⚠️ 不动点登记册不可用: {e}", file=sys.stderr)

# 审计引擎
AUDIT_URL = "http://127.0.0.1:9622/audit"
GATEWAY_URL = "http://127.0.0.1:8765"

# 投喂源定义
SOURCES = {
    "F1": ("对话投喂", "Claude / DeepSeek / 初心之翼 对话内容"),
    "F2": ("文件投喂", "本机文档 / 笔记 / 代码"),
    "F3": ("外部投喂", "网页 / 截图 / 他人内容"),
    "F4": ("事件投喂", "Notion Webhook / 系统事件"),
    "F5": ("规则投喂", "老大制定的新规则·升级 L0/L1"),
}

# 黑名单关键词（🔴 直接拒）
BLACKLIST = [
    # 伪造身份
    "我就是UID9622", "I am UID9622",
    # 伪造 DNA
    "#龍芯⚡️ 伪造", "fake-dna",
    # 明显的指令注入尝试
    "ignore previous instructions",
    "disregard the above",
]

# 必填字段
REQUIRED_FIELDS = ["title", "content", "source_type"]

# 颜色
C, G, Y, R, D, B, NC = ("\033[36m","\033[32m","\033[33m","\033[31m","\033[2m","\033[1m","\033[0m")


# ═══════════════════════════════════════════════
# 三色熔断门
# ═══════════════════════════════════════════════
def _digital_root(n):
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return n


def gate_check(title: str, content: str, source_type: str):
    """
    三色熔断门：
      🔴 数字根熔断 / 黑名单 / 必填缺失 → 拒绝
      🟡 长度异常 / 来源可疑 → 待补
      🟢 通过
    """
    # 必填
    if not title or not content:
        return "🔴", "必填字段缺失（title 或 content 为空）"
    if source_type not in SOURCES:
        return "🔴", f"source_type 非法，必须是 {list(SOURCES.keys())} 之一"

    # 黑名单
    combined = (title + " " + content).lower()
    for kw in BLACKLIST:
        if kw.lower() in combined:
            return "🔴", f"触发黑名单：{kw[:40]}"

    # ════════════════════════════════════════════════════════════════
    # 数字根熔断 · 用法边界（v1.1·写死·不许误改）
    # ════════════════════════════════════════════════════════════════
    # CNSH 数字根熔断规则 dr ∈ {3, 9} 的【正确使用位置】：
    #   ✅ 五行签名层 (wuxing_sign.py)         → 熔断·拒绝签名
    #   ✅ 八字四柱算法 (longhun_wuxing_mvp.py) → 用 dr 做洛书迭代
    #   ✅ 审计引擎标签 (audit_engine.py)       → dr → 三色标签
    #
    # 【绝对禁止】用在投喂入口（本文件）：
    #   ❌ 投喂 = 用户主动存数据 ≠ AI 响应
    #   ❌ 用 dr 拦投喂会随机拒掉 22% 的真实内容
    #   ❌ 老大主页 264 子页·就因为 dr=3 被拦过一次·教训写死
    # ════════════════════════════════════════════════════════════════
    content_hash_int = int(hashlib.sha256(content.encode("utf-8")).hexdigest()[:6], 16)
    dr = _digital_root(content_hash_int % 9999)
    # 保留 dr 作为信号·写到日志·但绝不做拦截动作

    # 长度异常
    if len(content) > 50000:
        return "🟡", f"内容过长（{len(content)}字符 > 50000·建议拆分）"
    if len(content) < 3:
        return "🟡", "内容过短"

    return "🟢", f"通过 · dr={dr} · 长度={len(content)}"


# ═══════════════════════════════════════════════
# 不动点锚登记（借 fixed_point_registry.Ψ）
# ═══════════════════════════════════════════════
def register_anchor(title: str, content: str, layer_hint: str = None):
    if FPR is None:
        return None
    r = FPR.add_anchor(title, content, layer=layer_hint)
    return r


# ═══════════════════════════════════════════════
# 本机分层落档
# ═══════════════════════════════════════════════
LAYER_DIRS = {
    "L0": ALGO_ROOT,                            # 永恒层·根目录
    "L1": ALGO_ROOT / "硬规则",                 # 百年层
    "L2": ALGO_ROOT / "五行向量" / "实战案例",   # 十年层
    "L3": HOME / "cnsh" / "logs" / "feeding" / "L3",  # 日常层
    "L4": HOME / "cnsh" / "logs" / "feeding" / "L4",  # 瞬时层（24h 清理）
}


def file_by_layer(layer: str, title: str, content: str, dna: str) -> str:
    d = LAYER_DIRS.get(layer, LAYER_DIRS["L3"])
    d.mkdir(parents=True, exist_ok=True)
    safe_title = "".join(c if c.isalnum() or c in "·_- " else "_" for c in title)[:60]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = d / f"投喂_{layer}_{ts}_{safe_title}.md"

    body = f"""# {title}

**DNA**: `{dna}`
**层级**: {layer}
**投喂时间**: {datetime.now().isoformat()}
**封顶锚**: `#龍芯⚡️20260423-ROOT-SEAL-01F32FFD`

---

{content}

---

**授权**: CC BY-NC-ND 4.0
**签名**: UID9622 · 诸葛鑫
**封存**: 投喂入口对齐协议 v1.0
"""
    fname.write_text(body, encoding="utf-8")
    return str(fname)


# ═══════════════════════════════════════════════
# 审计引擎留痕
# ═══════════════════════════════════════════════
def audit_record(dna: str, source_type: str, title: str, tricolor: str = "🟢"):
    dna_token = os.environ.get("DNA_TOKEN", "")
    if not dna_token:
        env_file = HOME / "longhun-system" / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("export DNA_TOKEN="):
                    dna_token = line.split("=", 1)[1].strip().strip('"')
                    break
    if not dna_token:
        return None

    try:
        payload = {
            "event_type": "FEED",
            "source": f"feeding_gateway/{source_type}",
            "target": title[:60],
            "payload": {"dna": dna, "source_type": source_type},
            "status": tricolor,
            "note": f"投喂入口 · {SOURCES.get(source_type, ('?',''))[0]}",
        }
        req = urllib.request.Request(
            AUDIT_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "X-DNA-Token": dna_token},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


# ═══════════════════════════════════════════════
# Notion 分发建议（基于层级）
# ═══════════════════════════════════════════════
DISPATCH_MAP = {
    "L0": {
        "name": "永恒层",
        "notion_target": "诸葛宣言 / 龍魂根文档 / DNA 身份系统第零章",
        "notion_page_id_hint": "69cff846023c430ca1c109d4a0a5d22e  # 诸葛宣言",
        "action": "需双签章 + 三票确认才能挂靠",
    },
    "L1": {
        "name": "百年层",
        "notion_target": "赋能宪法 / 算法仓库父页 / 硬规则库",
        "notion_page_id_hint": "0af9108b28db4874910ada3f09058f70  # 赋能宪法",
        "action": "需单签章 + 公示 30 天",
    },
    "L2": {
        "name": "十年层",
        "notion_target": "蒙卦启智 / V9 操作系统 / 陪玩学习人格",
        "notion_page_id_hint": "2d87125a9c9f802889e2e18002f7cf4f  # 蒙卦启智",
        "action": "需 UID9622 签字",
    },
    "L3": {
        "name": "日常层",
        "notion_target": "草日志 / 主控台 / 投喂入口 v1.1",
        "notion_page_id_hint": "4dfcb90d97344139b823e49a6ebac696  # 专用投喂入口",
        "action": "自动写入，无需审批",
    },
    "L4": {
        "name": "瞬时层",
        "notion_target": "沙盒临时区",
        "notion_page_id_hint": None,
        "action": "24h 后自动坍缩",
    },
}


def dispatch_hint(layer: str) -> dict:
    return DISPATCH_MAP.get(layer, DISPATCH_MAP["L3"])


# ═══════════════════════════════════════════════
# 主接口：feed()
# ═══════════════════════════════════════════════
def feed(title: str, content: str, source_type: str = "F1",
         layer_hint: str = None, silent: bool = False) -> dict:
    """
    投喂入口主接口。任何内容从这里进系统。
    """
    ts = datetime.now(timezone.utc).isoformat()

    # 1. 三色熔断门
    color, reason = gate_check(title, content, source_type)
    if color == "🔴":
        rej = {
            "ts": ts, "tricolor": color, "reason": reason,
            "title": title[:80], "source_type": source_type,
        }
        with open(REJECT_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rej, ensure_ascii=False) + "\n")
        if not silent:
            print(f"{R}🔴 投喂拒绝：{reason}{NC}")
        return {"status": "rejected", "tricolor": color, "reason": reason}

    # 2. 不动点锚登记
    reg = register_anchor(title, content, layer_hint=layer_hint)
    if reg and reg.get("status") == "added":
        anchor = reg["anchor"]
        anchor_id = anchor["id"]
        dna = anchor["D"]
        layer = anchor["L"]
    elif reg and reg.get("status") == "duplicate":
        anchor = reg["anchor"]
        anchor_id = anchor["id"]
        dna = anchor["D"]
        layer = anchor["L"]
        if not silent:
            print(f"{Y}⚪ 内容已登记（id={anchor_id}）· 复用旧锚{NC}")
    else:
        # 降级：不用登记册也要给一个 DNA
        h = hashlib.sha256(content.encode("utf-8")).hexdigest()[:8].upper()
        date = datetime.now().strftime("%Y%m%d")
        dna = f"#龍芯⚡️{date}-FEED-{h}"
        anchor_id = None
        layer = layer_hint or "L3"

    # 3. 本机分层落档
    file_path = file_by_layer(layer, title, content, dna)

    # 4. 审计引擎留痕
    audit_resp = audit_record(dna, source_type, title, tricolor=color)

    # 5. Notion 分发建议
    dispatch = dispatch_hint(layer)

    result = {
        "status": "🟢 accepted",
        "tricolor": color,
        "dna": dna,
        "anchor_id": anchor_id,
        "layer": layer,
        "layer_name": dispatch["name"],
        "source_type": source_type,
        "source_name": SOURCES.get(source_type, ("?",""))[0],
        "file_path": file_path,
        "audit_id": audit_resp.get("id") if audit_resp else None,
        "dispatch": {
            "notion_target": dispatch["notion_target"],
            "notion_page_hint": dispatch["notion_page_id_hint"],
            "action_required": dispatch["action"],
        },
        "ts": ts,
    }

    # 落本机投喂总日志
    with open(FEED_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")

    if not silent:
        _print_receipt(result)
    return result


def _print_receipt(r: dict):
    print()
    print(f"{G}━━━ 🐉 投喂受理 · {r['tricolor']} ━━━{NC}")
    print(f"  DNA       : {B}{r['dna']}{NC}")
    print(f"  锚 id     : {r.get('anchor_id','-')}")
    print(f"  层级      : {r['layer']} · {r['layer_name']}")
    print(f"  来源      : {r['source_type']} · {r['source_name']}")
    print(f"  落档      : {D}{r['file_path']}{NC}")
    if r.get('audit_id'):
        print(f"  审计 id   : {r['audit_id']}（已写入 SQLite）")
    print(f"{C}━━━ 📮 Notion 分发建议 ━━━{NC}")
    disp = r["dispatch"]
    print(f"  分发目标  : {disp['notion_target']}")
    if disp.get('notion_page_hint'):
        print(f"  建议页 ID : {D}{disp['notion_page_hint']}{NC}")
    print(f"  所需动作  : {Y}{disp['action_required']}{NC}")
    print()


# ═══════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════
def _load_feeds():
    if not FEED_LOG.exists():
        return []
    out = []
    with open(FEED_LOG, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except Exception:
                    pass
    return out


def cmd_list(n=10):
    feeds = _load_feeds()[-n:]
    print(f"━━━ 📋 最近 {len(feeds)} 条投喂 ━━━")
    for r in feeds:
        print(f"[{r.get('anchor_id','-'):>3}] {r['tricolor']} {r['layer']} · {r.get('dna','?')}")
        print(f"      来源: {r.get('source_type','?')} · {r.get('source_name','?')}")
        print(f"      文件: {Path(r.get('file_path','')).name}")


def cmd_stats():
    from collections import Counter
    feeds = _load_feeds()
    if not feeds:
        print("（投喂日志空）")
        return
    print(f"━━━ 📊 投喂统计 ━━━")
    print(f"  总投喂数: {len(feeds)}")
    srcs = Counter(r.get("source_type","?") for r in feeds)
    print("  来源分布:")
    for s, n in srcs.most_common():
        print(f"    {s}: {n}  ({SOURCES.get(s,('?',''))[0]})")
    layers = Counter(r.get("layer","?") for r in feeds)
    print("  层级分布:")
    for l in ("L0","L1","L2","L3","L4"):
        print(f"    {l}: {layers.get(l,0)}")
    # 拒绝数
    if REJECT_LOG.exists():
        with open(REJECT_LOG) as f:
            rej = sum(1 for _ in f)
        print(f"  🔴 拒绝数: {rej}")


def cmd_dispatch(aid):
    feeds = _load_feeds()
    for r in feeds:
        if str(r.get("anchor_id")) == str(aid):
            print(json.dumps(r.get("dispatch", {}), ensure_ascii=False, indent=2))
            return
    print(f"🔴 未找到 anchor_id={aid}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0]
    if cmd == "feed":
        if len(args) < 3:
            print("用法: feed \"标题\" \"内容\" [--source F1] [--layer L3]")
            return
        title = args[1]
        content = args[2]
        src = "F1"
        layer = None
        i = 3
        while i < len(args):
            if args[i] == "--source" and i+1 < len(args):
                src = args[i+1]; i += 2
            elif args[i] == "--layer" and i+1 < len(args):
                layer = args[i+1]; i += 2
            else:
                i += 1
        feed(title, content, source_type=src, layer_hint=layer)

    elif cmd == "feed-file":
        if len(args) < 3:
            print("用法: feed-file \"标题\" path/to/file [--source F2]")
            return
        title = args[1]
        path = Path(args[2]).expanduser()
        if not path.exists():
            print(f"🔴 文件不存在: {path}")
            return
        content = path.read_text(encoding="utf-8", errors="ignore")
        src = "F2"
        layer = None
        i = 3
        while i < len(args):
            if args[i] == "--source" and i+1 < len(args):
                src = args[i+1]; i += 2
            elif args[i] == "--layer" and i+1 < len(args):
                layer = args[i+1]; i += 2
            else:
                i += 1
        feed(title, content, source_type=src, layer_hint=layer)

    elif cmd == "list":
        n = int(args[1]) if len(args) > 1 else 10
        cmd_list(n)

    elif cmd == "stats":
        cmd_stats()

    elif cmd == "dispatch":
        if len(args) < 2:
            print("用法: dispatch <anchor_id>")
            return
        cmd_dispatch(args[1])

    elif cmd == "sources":
        print("━━━ 五大投喂源 ━━━")
        for k, (name, desc) in SOURCES.items():
            print(f"  {k} · {name}：{desc}")

    else:
        print(f"未知命令: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
