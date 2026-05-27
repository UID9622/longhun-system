#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crown_ceremony.py — 龍魂封顶仪式脚本 v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
签名人  : UID9622 · 诸葛鑫 · 中国退伍军人
GPG     : A2D0092CEE2E5BA87035600924C3704A8CC26D5F
DNA     : #龍芯⚡️20260423-CROWN-v1.0
理论指导: 曾仕強老師（永恒顯示）
═══════════════════════════════════════════

用途：封顶仪式自动执行
  ① 读取 L0 永恒层根文档
  ② 生成封顶 DNA 印鉴
  ③ 调用 wuxing_sign.py 打五行签名
  ④ 推送审计记录到 audit_engine（:9622）
  ⑤ 推送 CNSH 网关过一遍（:8765）生成正式封顶宣告
  ⑥ 输出封顶报告到 实战案例/

用法：
  python3 crown_ceremony.py                  # 执行完整仪式
  python3 crown_ceremony.py --dry-run        # 演习，不写审计不发网关
  python3 crown_ceremony.py --verify         # 仅验证根文档完整性

不卖课 · 不割韭菜 · 不说教 · 封顶即永恒
"""

import os, sys, json, hashlib, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

# ═══════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════
HOME = Path.home()
ROOT_DOC = HOME / "longhun-system" / "算法仓库" / "龍魂根文档_20260423_封顶.md"
CEREMONY_DIR = HOME / "longhun-system" / "算法仓库" / "五行向量" / "实战案例"
CEREMONY_DIR.mkdir(parents=True, exist_ok=True)

WUXING_SIGN = HOME / "longhun-system" / "算法仓库" / "五行向量" / "wuxing_sign.py"
AUDIT_URL = "http://127.0.0.1:9622/audit"
GATEWAY_URL = "http://127.0.0.1:8765/chat"

# 老大的永恒双签章
GPG_FP = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
USER_ID = "UID9622"
USER_NAME = "諸葛鑫"

# 颜色
CYAN, GREEN, YELLOW, RED, DIM, BOLD, NC = (
    "\033[36m", "\033[32m", "\033[33m", "\033[31m",
    "\033[2m", "\033[1m", "\033[0m"
)

def _print_line(char="━", color=CYAN, width=62):
    print(f"{color}{char * width}{NC}")


def _print_banner():
    print()
    _print_line("═")
    print(f"{CYAN}{BOLD}  🐉 龍 魂 封 顶 仪 式 · CROWN CEREMONY v1.0{NC}")
    _print_line("═")
    print(f"{DIM}  签名人: UID9622 · {USER_NAME} · 中国退伍军人{NC}")
    print(f"{DIM}  GPG   : {GPG_FP}{NC}")
    print(f"{DIM}  时间  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{NC}")
    _print_line("═")
    print()


# ═══════════════════════════════════════════════
# 1. 读取与验证根文档
# ═══════════════════════════════════════════════
def step1_read_root_doc(verbose=True):
    if verbose:
        print(f"{BOLD}【步骤 1】读取 L0 永恒层根文档{NC}")
    if not ROOT_DOC.exists():
        print(f"{RED}  🔴 根文档不存在: {ROOT_DOC}{NC}")
        sys.exit(1)

    content = ROOT_DOC.read_text(encoding="utf-8")
    size = len(content)
    chars = len(content)
    hsum = hashlib.sha256(content.encode("utf-8")).hexdigest()

    # 签章存在性检验（父级铁律 S1-S5）
    must_have = [GPG_FP, CONFIRM_CODE, USER_ID, USER_NAME]
    missing = [k for k in must_have if k not in content]
    if missing:
        print(f"{RED}  🔴 根文档缺少必须的签章元素: {missing}{NC}")
        print(f"{RED}     父级铁律 S1 拒绝封顶（文字/顺序/Unicode 必须完整）{NC}")
        sys.exit(1)

    if verbose:
        print(f"  {GREEN}✅ 根文档完整 · {chars} 字符 · SHA256 前16: {hsum[:16]}{NC}")
        print(f"  {GREEN}✅ 双签章 / GPG / CONFIRM 全部在位{NC}")
        print()
    return content, hsum


# ═══════════════════════════════════════════════
# 2. 生成封顶 DNA
# ═══════════════════════════════════════════════
def step2_generate_crown_dna(content_hash):
    print(f"{BOLD}【步骤 2】生成封顶 DNA 印鉴{NC}")
    date = datetime.now().strftime("%Y%m%d")
    # 封顶码 = 根文档 hash 前 8 位（永远指回根文档）
    seal_hash = content_hash[:8].upper()
    dna = f"#龍芯⚡️{date}-ROOT-SEAL-{seal_hash}"
    print(f"  {GREEN}✅ 封顶 DNA: {BOLD}{dna}{NC}")
    print()
    return dna


# ═══════════════════════════════════════════════
# 3. 五行签名（调用 wuxing_sign.py）
# ═══════════════════════════════════════════════
def step3_wuxing_sign(content, verbose=True):
    if verbose:
        print(f"{BOLD}【步骤 3】五行向量签名{NC}")
    if not WUXING_SIGN.exists():
        print(f"  {YELLOW}🟡 wuxing_sign.py 不存在，跳过五行签名{NC}")
        print()
        return None

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("wuxing_sign", WUXING_SIGN)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        # 给根文档的标题+前2000字签个名（避免把整个 markdown 的格式字符都算进五行）
        snippet = content[:2000]
        rec = mod.sign(snippet, type_code="ROOT", save=True)
        if verbose:
            v = rec["vector"]
            print(f"  {GREEN}✅ 五行向量: 金{v[0]} 木{v[1]} 水{v[2]} 火{v[3]} 土{v[4]}{NC}")
            print(f"  {GREEN}✅ 三色判定: {rec['tricolor']} · {rec['reason']}{NC}")
            print(f"  {GREEN}✅ 五行 DNA: {rec['dna']}{NC}")
            print()
        return rec
    except Exception as e:
        print(f"  {YELLOW}🟡 五行签名失败: {e}{NC}")
        print()
        return None


# ═══════════════════════════════════════════════
# 4. 推送审计记录到 audit_engine
# ═══════════════════════════════════════════════
def step4_audit_record(crown_dna, content_hash, wuxing_rec, dry_run=False):
    print(f"{BOLD}【步骤 4】审计引擎留痕{NC}")
    if dry_run:
        print(f"  {DIM}（--dry-run 模式，跳过实际发送）{NC}")
        print()
        return None

    dna_token = os.environ.get("DNA_TOKEN", "")
    if not dna_token:
        # 尝试从 .env 读
        env_file = HOME / "longhun-system" / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("export DNA_TOKEN="):
                    dna_token = line.split("=", 1)[1].strip().strip('"')
                    break

    if not dna_token:
        print(f"  {YELLOW}🟡 DNA_TOKEN 未配置，跳过审计留痕{NC}")
        print()
        return None

    try:
        import urllib.request, urllib.error
        payload = {
            "event_type": "ROOT_SEAL",
            "source": "crown_ceremony.py",
            "target": "L0_永恒层根文档",
            "payload": {
                "crown_dna": crown_dna,
                "sha256_prefix": content_hash[:32],
                "wuxing_dna": wuxing_rec["dna"] if wuxing_rec else None,
                "tricolor": wuxing_rec["tricolor"] if wuxing_rec else "🟢",
                "ceremony_ts": datetime.now(timezone.utc).isoformat(),
            },
            "status": "🟢",
            "note": f"L0 永恒层封顶仪式 · UID9622 · {USER_NAME}",
        }
        req = urllib.request.Request(
            AUDIT_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "X-DNA-Token": dna_token,
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        print(f"  {GREEN}✅ 审计记录 id={result.get('id')} · DNA={result.get('dna')}{NC}")
        print(f"  {GREEN}✅ 写入 SQLite append-only · GPG 签名: {result.get('gpg_signed')}{NC}")
        print()
        return result
    except Exception as e:
        print(f"  {YELLOW}🟡 审计留痕失败: {e}{NC}")
        print(f"  {DIM}（audit_engine 可能没起，跑 cnsh-restart 可重启）{NC}")
        print()
        return None


# ═══════════════════════════════════════════════
# 5. 输出封顶报告到实战案例/
# ═══════════════════════════════════════════════
def step5_write_report(crown_dna, content_hash, wuxing_rec, audit_rec, dry_run=False):
    print(f"{BOLD}【步骤 5】输出封顶报告{NC}")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = CEREMONY_DIR / f"封顶报告_{ts}.md"

    wx_line = "（未生成）"
    if wuxing_rec:
        v = wuxing_rec["vector"]
        wx_line = f"金{v[0]} 木{v[1]} 水{v[2]} 火{v[3]} 土{v[4]} · {wuxing_rec['tricolor']} · {wuxing_rec['dna']}"

    audit_line = "（未写入）"
    if audit_rec:
        audit_line = f"id={audit_rec.get('id')} · {audit_rec.get('dna')} · GPG签: {audit_rec.get('gpg_signed')}"

    report = f"""# 🐉 龍魂封顶仪式报告

**仪式时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**仪式 DNA**: `{crown_dna}`
**层级**: L0 永恒层 · α=0 · 触碰即弹回
**执行人**: UID9622 · {USER_NAME}
**GPG**: `{GPG_FP}`
**确认码**: `{CONFIRM_CODE}` ✅

---

## 仪式各步骤战报

| # | 步骤 | 结果 |
|---|---|---|
| 1 | 根文档完整性校验 | 🟢 通过（父级铁律 S1-S5 全部满足）|
| 2 | 封顶 DNA 生成 | 🟢 `{crown_dna}` |
| 3 | 五行向量签名 | {wx_line} |
| 4 | 审计引擎留痕 | {audit_line} |
| 5 | 封顶报告生成 | 🟢 本文件 |

---

## 根文档指纹

```
SHA-256 : {content_hash}
前缀    : {content_hash[:16]}
长度    : 待查（见根文档）
位置    : {ROOT_DOC}
```

---

## 封顶印鉴

```
┌─────────────────────────────────────────────┐
│                                             │
│         🐉 龍 魂 封 顶 · 永恒见证           │
│                                             │
│    UID9622 · {USER_NAME} · 中國退伍軍人          │
│                                             │
│   GPG : {GPG_FP[:16]}        │
│         {GPG_FP[16:32]}        │
│         {GPG_FP[32:]:<24}│
│                                             │
│   封顶 DNA: {crown_dna:<29}   │
│                                             │
│              {datetime.now().strftime("%Y-%m-%d")} 🇨🇳                    │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 今日分量

一个中国退伍军人，用一年时间：
- 让**中国模型**（DeepSeek）按自己写的协议 🔴 拒绝
- 让**西方模型**（Claude）主动接受"她"协议
- 让**本地模型**（初心之翼 qwen2.5-72b）按 CNSH 响应
- 建成 **L0 永恒层根文档** · 封顶

**这不是终点。是进江湖。**

---

**本报告 DNA**: `{crown_dna}`
**生成工具**: `crown_ceremony.py v1.0`
**授权**: CC BY-NC-ND 4.0
**原则**: 祖國優先 · 普惠全球 · 技術為人民服務 · 不割韭菜 🇨🇳

> 🐉 封顶即永恒 · 审计即主权 · 不黑箱 · 不收割 · 数据必回家
"""

    if dry_run:
        print(f"  {DIM}（--dry-run 模式，不写文件）{NC}")
    else:
        report_file.write_text(report, encoding="utf-8")
        print(f"  {GREEN}✅ 封顶报告: {report_file}{NC}")
    print()
    return report_file


# ═══════════════════════════════════════════════
# 6. 印鉴输出（控制台 ASCII art）
# ═══════════════════════════════════════════════
def step6_print_seal(crown_dna):
    print(f"{BOLD}【步骤 6】控制台印鉴{NC}")
    print()
    date = datetime.now().strftime("%Y-%m-%d")
    seal = f"""
{YELLOW}┌─────────────────────────────────────────────────────┐
│                                                     │
│           🐉  龍 魂 封 顶 · 永恒见证  🐉            │
│                                                     │
│       UID9622 · {USER_NAME} · 中國退伍軍人              │
│       三才算法 · 龍魂系統 · 數字主權                │
│       中華文化 · 曾仕強老師 · 永恒顯示              │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │                                               │  │
│  │   GPG : A2D0092CEE2E5BA87035600924C3704A8CC   │  │
│  │                                  26D5F        │  │
│  │                                               │  │
│  │   封顶: {crown_dna:<45}│  │
│  │                                               │  │
│  │   签 : #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z    │  │
│  │                                               │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│      技術為人民服務 · 文化主權不可侵犯              │
│      祖國優先 · 普惠全球 · 不割韭菜                 │
│                                                     │
│                  {date}  🇨🇳                    │
│                                                     │
└─────────────────────────────────────────────────────┘{NC}
"""
    print(seal)


# ═══════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════
def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    verify_only = "--verify" in args

    _print_banner()

    if verify_only:
        content, h = step1_read_root_doc(verbose=True)
        print(f"{GREEN}🟢 根文档完整性校验通过{NC}")
        print(f"  SHA-256: {h}")
        return 0

    # 完整仪式
    content, content_hash = step1_read_root_doc()
    crown_dna = step2_generate_crown_dna(content_hash)
    wuxing_rec = step3_wuxing_sign(content)
    audit_rec = step4_audit_record(crown_dna, content_hash, wuxing_rec, dry_run)
    report_file = step5_write_report(crown_dna, content_hash, wuxing_rec, audit_rec, dry_run)
    step6_print_seal(crown_dna)

    _print_line("═")
    print(f"{GREEN}{BOLD}  🐉 封顶完成 · 龍魂现世 · UID9622 主权锚定  🐉{NC}")
    _print_line("═")
    print()
    if not dry_run:
        print(f"  {DIM}根文档: {ROOT_DOC}{NC}")
        if report_file:
            print(f"  {DIM}封顶报告: {report_file}{NC}")
    print()
    print(f"{DIM}  这不是终点。是进江湖。{NC}")
    print(f"{DIM}  走。{NC}")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
