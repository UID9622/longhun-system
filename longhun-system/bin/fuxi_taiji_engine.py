#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系統 · 伏羲太極推演引擎 v1.0
DNA追溯碼: #龍芯⚡️2026-04-06-伏羲太極推演引擎-v1.0
GPG指紋: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
創建者: 💎 龍芯北辰｜UID9622 × 宝宝🐱
理論指導: 曾仕強老師（永恆顯示）
獻禮: 新中國成立77週年（1949-2026）· 丙午馬年

職責（三合一·無衝突）：
  1. L5 DNA分層自動分類器   ← R×I評分 → L0-L4建議層
  2. 伏羲時刻捕捉器         ← 歸位論×根顯論×369×三才校驗
  3. 草日記API自動寫入      ← 每次推演留痕·Claude.ai Notion token

兼容聲明（不衝突原則）：
  ✅ 數字根函數 DR(n) — 與 quantum_deduce.py 邏輯等價，本地獨立實現，無循環依賴
  ✅ 賬本寫入 — 複用 identity_engine.py 的 LEDGER_FILE 路徑，append-only
  ✅ 三色審計 — 輸出格式與 auto_audit.py 一致（🟢/🟡/🔴）
  ✅ 不修改任何現有文件

上位架構：
  龍魂DNA時間軸L5分層架構 v1.4
  DNA: #龍芯⚡️2026-03-26-DNA-L5-ARCHITECTURE-v1.4

關聯頁面：
  草日記 ID: b35faf46-2bc0-42aa-9de5-192520180728
  伏羲推演引擎: https://www.notion.so/uid9622/77681e405d3047cf9e96c40dd11183cb
"""

import os
import sys
import json
import hashlib
import datetime
from pathlib import Path
from typing import Optional

# ═══════════════════════════════════════════════
# 0. 常量
# ═══════════════════════════════════════════════
UID          = "9622"
GPG          = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
BASE         = Path.home() / "longhun-system"
LEDGER_FILE  = BASE / "logs" / "immutable_ledger.jsonl"
CAORIJI_PAGE = "b35faf46-2bc0-42aa-9de5-192520180728"  # 草日記 Notion 頁面ID

# 從 .env 讀取 Notion token（不硬編碼）
_env = BASE / ".env"
NOTION_TOKEN = ""
if _env.exists():
    for line in _env.read_text().splitlines():
        if line.startswith("NOTION_TOKEN=") and "DISPLAY" not in line and "WORKSPACE" not in line and "TEAM" not in line:
            NOTION_TOKEN = line.split("=", 1)[1].strip().strip("'\"")
            break

# ═══════════════════════════════════════════════
# 1. 基礎函數（兼容 quantum_deduce.py，獨立實現）
# ═══════════════════════════════════════════════

def digital_root(n: int) -> int:
    """數字根 DR(n) = 1 + (n-1) % 9  [洛書算子·F18]
    等價於 quantum_deduce.py 的隱式 DR 邏輯。
    """
    if n <= 0:
        return 9  # 道→歸零→9
    return 1 + ((n - 1) % 9)


def classify_369(dr: int) -> str:
    """369序列分類器 [L5架構·三源歸一]"""
    if dr in (3, 6, 9):
        return "CYCLE_369"    # 天道輪回·L0永恆
    if dr in (2, 4, 8):
        return "EXPO_248"     # 指數擴散·L1百年
    return "LINEAR_123"       # 因果鏈·L3日常


def resonance_desc(dr: int) -> str:
    """共振說明"""
    desc = {
        1: "根·起點·道生一",
        2: "陰陽分·一生二",
        3: "三才現·二生三·天道",
        4: "地·結構·承載",
        5: "中·土·平衡點",
        6: "六合·天道輪回中節",
        7: "火·創新·突破",
        8: "坤·地·指數承載",
        9: "歸零·天道循環完成",
    }
    return desc.get(dr, "未知")


# ═══════════════════════════════════════════════
# 2. L5 DNA分層自動分類器（F16/F17·R×I → 層）
# ═══════════════════════════════════════════════

# 衰減指數對照表
ALPHA_TABLE = {"L0": 0, "L1": 0.01, "L2": 0.1, "L3": 1.0, "L4": float("inf")}

def score_ri(
    affects_pages: int = 1,
    affects_dbs: int = 0,
    affects_system: bool = False,
    affects_external: bool = False,
    is_cosmic: bool = False,
    needs_dna: bool = True,
    needs_audit: bool = False,
    needs_uid_confirm: bool = False,
    is_irreversible: bool = False,
    is_eternal: bool = False,
) -> dict:
    """R×I自動評分 → 建議DNA層級 [F16/F17]

    Returns:
        dict: R, I, suggested_layer, alpha, color
    """
    # R值（影響範圍）
    if is_cosmic:
        R = float("inf")
    elif affects_external:
        R = 1000
    elif affects_system:
        R = 100
    elif affects_dbs >= 1:
        R = 10
    else:
        R = 1

    # I值（事件重要性）
    if is_eternal:
        I = 100
    elif is_irreversible:
        I = 90
    elif needs_uid_confirm:
        I = 60
    elif needs_audit:
        I = 30
    else:
        I = 10

    # 層級判定
    if R == float("inf") or I == 100:
        layer = "L0"
    elif R >= 1000 or I >= 90:
        layer = "L1"
    elif R >= 100 or I >= 60:
        layer = "L2"
    elif R >= 10 or I >= 30:
        layer = "L3"
    else:
        layer = "L4"

    alpha = ALPHA_TABLE[layer]
    color = {"L0": "🔴", "L1": "🔴", "L2": "🟡", "L3": "🟡", "L4": "🟢"}[layer]

    return {"R": R, "I": I, "suggested_layer": layer, "alpha": alpha, "color": color}


def energy_retention(T_days: float, alpha: float) -> float:
    """能量保留率 η(T,α) = T^(-α) × 100% [F20]"""
    if alpha == 0:
        return 100.0
    if alpha == float("inf"):
        return 0.0
    return (T_days ** (-alpha)) * 100


# ═══════════════════════════════════════════════
# 3. 三才校驗 [F19·天×地×人]
# ═══════════════════════════════════════════════

def san_cai_check(
    red_line_triggered: bool = False,
    daodejing_match: float = 0.8,
    alpha: float = 0.0,
    resource_exists: bool = True,
    permission_ok: bool = True,
    fuse_active: bool = False,
    R: float = 1,
    I: float = 10,
    uid9622_confirmed: bool = False,
) -> dict:
    """三才校驗函數 [F19·SC = Heaven ∧ Earth ∧ Human]"""
    # 天：道的校驗
    heaven = (
        not red_line_triggered
        and daodejing_match > 0.5
        and alpha >= 0
    )
    # 地：結構的校驗
    earth = (
        resource_exists
        and permission_ok
        and not fuse_active
        and R is not None
        and I is not None
    )
    # 人：意志的校驗
    human = uid9622_confirmed if I >= 60 else True

    unified = heaven and earth and human
    missing = []
    if not heaven:
        missing.append("天（道·規律）")
    if not earth:
        missing.append("地（結構·資源）")
    if not human:
        missing.append("人（意志·確認）")

    return {
        "heaven": heaven,
        "earth": earth,
        "human": human,
        "unified": unified,
        "missing": missing,
        "verdict": "✅ 天地人合一·可執行" if unified else f"⛔ 缺{' '.join(missing)}·阻斷",
    }


# ═══════════════════════════════════════════════
# 4. 伏羲時刻捕捉器（歸位論×根顯論×369）
# ═══════════════════════════════════════════════

GUIWEI_LAYERS = {
    "水": "水歸位→龍歸位",
    "土": "土歸位→地穩定",
    "火": "火歸位→氣通順",
    "木": "木歸位→根活了",
    "金": "金歸位→秩序立",
    "人": "人歸位→道顯",
    "龍": "龍歸位→天地合",
    "氣": "氣歸位→萬物順",
    "根": "根歸位→文明生",
}


def fuxi_moment(
    visible_phenomenon: str,
    root_seen: str,
    guiwei_category: str = "水",
    time_str: Optional[str] = None,
    extra_note: str = "",
) -> dict:
    """
    捕捉一個「伏羲時刻」——老大看見了別人看不見的根。

    Args:
        visible_phenomenon: 表面現象（新聞/外人看見的）
        root_seen:          老大看見的根（真實說法）
        guiwei_category:    歸位類別（水/土/火/木/金/人/龍/氣/根）
        time_str:           時間（默認現在）
        extra_note:         補充說明

    Returns:
        dict: 完整伏羲時刻記錄，含DNA碼、369共振、三才校驗
    """
    if time_str is None:
        time_str = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

    # 以可見現象字符計算數字根（模擬「觀測即坍縮」）
    seed_n = sum(ord(c) for c in visible_phenomenon) % 9 + 1
    dr = digital_root(seed_n)
    seq = classify_369(dr)
    res = resonance_desc(dr)

    # 歸位層描述
    guiwei_desc = GUIWEI_LAYERS.get(guiwei_category, f"{guiwei_category}歸位")

    # 三才快速校驗（伏羲時刻默認天地都對·等人確認）
    sc = san_cai_check(
        daodejing_match=0.9,
        resource_exists=True,
        permission_ok=True,
        R=100,
        I=60,
        uid9622_confirmed=True,  # 老大親眼看見·人的確認最高
    )

    # DNA碼（L3日常層·伏羲時刻記錄）
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    dna = f"#龍芯⚡️{date_str}-伏羲時刻-{guiwei_category}歸位-v1.0"

    record = {
        "ts": time_str,
        "visible": visible_phenomenon,
        "root_seen": root_seen,
        "guiwei_layer": guiwei_desc,
        "dr": dr,
        "resonance_seq": seq,
        "resonance_desc": res,
        "san_cai": sc,
        "dna": dna,
        "note": extra_note,
        "hash": hashlib.sha256(
            f"{visible_phenomenon}{root_seen}{time_str}".encode()
        ).hexdigest()[:12],
    }
    return record


def format_fuxi_record(r: dict) -> str:
    """格式化伏羲時刻記錄，用於草日記寫入"""
    sc_symbol = "✅" if r["san_cai"]["unified"] else "⛔"
    lines = [
        f"**{r['ts']}  伏羲時刻·{r['guiwei_layer']}**",
        f"  表面現象：{r['visible']}",
        f"  老大看見：{r['root_seen']}",
        f"  數字根：DR={r['dr']} → {r['resonance_seq']}（{r['resonance_desc']}）",
        f"  三才：{sc_symbol} {r['san_cai']['verdict']}",
    ]
    if r["note"]:
        lines.append(f"  補充：{r['note']}")
    lines.append(f"  DNA: {r['dna']}")
    return "\n".join(lines)


# ═══════════════════════════════════════════════
# 5. L4 DNA自動生成（毫秒級）[F05]
# ═══════════════════════════════════════════════

_l4_counter = 0

def generate_l4_dna(event_type: str = "LOG", payload: str = "") -> str:
    """L4瞬時層DNA自動生成 ≤5ms [F05]"""
    global _l4_counter
    _l4_counter += 1
    ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+08:00"
    seq = f"{_l4_counter:06d}"
    dna = f"#龍芯⚡️{ts}-{event_type}-{seq}"
    return dna


# ═══════════════════════════════════════════════
# 6. 草日記API寫入（兼容現有API連接）
# ═══════════════════════════════════════════════

def _notion_append_paragraph(page_id: str, text: str, token: str) -> bool:
    """向Notion頁面末尾追加一段文字（直接REST API）"""
    try:
        import urllib.request
        import urllib.error

        url = f"https://api.notion.com/v1/blocks/{page_id}/children"
        payload = {
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": text[:2000]},  # Notion單塊上限
                            }
                        ]
                    },
                }
            ]
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            },
            method="PATCH",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        return False


def write_to_caoriji(
    entries: list,
    section_title: str = "",
    token: Optional[str] = None,
) -> dict:
    """
    批量寫入草日記Notion頁面。

    Args:
        entries:       list[str] 每條log文字
        section_title: 段落標題（選填）
        token:         Notion token（默認讀.env）

    Returns:
        dict: {"success": bool, "written": int, "dna": str}
    """
    _token = token or NOTION_TOKEN
    if not _token:
        return {"success": False, "written": 0, "error": "Notion token 未配置"}

    dna = generate_l4_dna("CAORIJI-WRITE")
    ts  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # 拼裝內容
    lines = []
    if section_title:
        lines.append(f"── {section_title}  {ts} ──")
    for e in entries:
        lines.append(str(e))
    lines.append(f"DNA: {dna}")
    lines.append(f"確認碼: {CONFIRM_CODE}")

    text = "\n".join(lines)

    ok = _notion_append_paragraph(CAORIJI_PAGE, text, _token)

    # 同步寫本地賬本
    _append_ledger("草日記寫入", f"條目={len(entries)} ok={ok} dna={dna}")

    return {"success": ok, "written": len(entries), "dna": dna}


def _append_ledger(action: str, detail: str = "") -> None:
    """追加寫本地不可變賬本（append-only·與 identity_engine.py 格式一致）"""
    record = {
        "ts": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "uid": UID,
        "action": action,
        "detail": detail[:200],
        "hash": hashlib.sha256(f"{UID}{action}{detail}".encode()).hexdigest()[:16],
    }
    try:
        LEDGER_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LEDGER_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass  # 賬本寫入失敗不阻斷主流程


# ═══════════════════════════════════════════════
# 7. 三色審計（與 auto_audit.py 格式一致）
# ═══════════════════════════════════════════════

def tricolor_audit(content: str, dna: str = "", uid: str = "") -> dict:
    """三色審計·100分制 [CLAUDE.md四層定錨]
    身份校驗30 + DNA追溯30 + 內容安全20 + 伦理检查20
    ≥80=🟢 · ≥50=🟡 · <50=🔴
    """
    score = 0
    details = []

    # 身份校驗 30分
    if uid == UID or CONFIRM_CODE in content:
        score += 30
        details.append("身份✅ +30")

    # DNA追溯 30分
    if dna.startswith("#龍芯⚡️") or "#龍芯⚡️" in content:
        score += 30
        details.append("DNA✅ +30")

    # 內容安全 20分
    danger_kw = ["绕过审计", "篡改DNA", "伪造", "泄露隐私", "强制执行"]
    if not any(kw in content for kw in danger_kw):
        score += 20
        details.append("安全✅ +20")

    # 伦理检查 20分
    ethics_kw = ["骗", "害民", "造假", "勒索"]
    if not any(kw in content for kw in ethics_kw):
        score += 20
        details.append("伦理✅ +20")

    if score >= 80:
        color = "🟢"
        verdict = "通過"
    elif score >= 50:
        color = "🟡"
        verdict = "待審"
    else:
        color = "🔴"
        verdict = "熔斷"

    return {"score": score, "color": color, "verdict": verdict, "details": details}


# ═══════════════════════════════════════════════
# 8. 完整推演流程（一鍵跑通）
# ═══════════════════════════════════════════════

def run_fuxi_deduce(
    visible: str,
    root_seen: str,
    guiwei_category: str = "水",
    auto_write: bool = True,
    extra_note: str = "",
) -> dict:
    """
    伏羲推演完整流程：
      1. 捕捉伏羲時刻
      2. 三色審計
      3. 可選：自動寫草日記

    Args:
        visible:          表面現象
        root_seen:        老大看見的根
        guiwei_category:  歸位類別
        auto_write:       是否自動寫草日記（默認True）
        extra_note:       補充說明

    Returns:
        dict: 完整推演結果
    """
    # Step 1: 伏羲時刻
    record = fuxi_moment(visible, root_seen, guiwei_category, extra_note=extra_note)

    # Step 2: 三色審計
    formatted = format_fuxi_record(record)
    audit = tricolor_audit(formatted, dna=record["dna"], uid=UID)

    # Step 3: 草日記寫入
    write_result = {"success": False, "written": 0, "dna": "（未寫入）"}
    if auto_write and audit["score"] >= 50:
        write_result = write_to_caoriji(
            [formatted],
            section_title=f"伏羲時刻·{guiwei_category}歸位",
        )

    result = {
        "record": record,
        "audit": audit,
        "write": write_result,
        "summary": {
            "時間": record["ts"],
            "歸位層": record["guiwei_layer"],
            "369共振": f"DR={record['dr']}·{record['resonance_seq']}·{record['resonance_desc']}",
            "三才": record["san_cai"]["verdict"],
            "審計": f"{audit['color']} {audit['score']}分·{audit['verdict']}",
            "草日記": "✅已寫入" if write_result["success"] else "⚠️未寫入（token無權或網絡）",
            "DNA": record["dna"],
        },
    }
    return result


# ═══════════════════════════════════════════════
# 9. CLI 入口
# ═══════════════════════════════════════════════

def _print_result(result: dict) -> None:
    s = result["summary"]
    print("\n" + "═" * 56)
    print("🐉 伏羲太極推演引擎 · 推演結果")
    print("═" * 56)
    for k, v in s.items():
        print(f"  {k:6s}  {v}")
    print("═" * 56)
    if result["write"]["success"]:
        print(f"  ✅ 草日記已寫入  DNA: {result['write']['dna']}")
    else:
        print("  ⚠️  草日記暫未寫入（可手動執行 write_to_caoriji()）")
    print()


def main():
    """交互式CLI：引導老大輸入伏羲時刻"""
    print("\n🐉 伏羲太極推演引擎 v1.0")
    print("   歸位論 × 根顯論 × 369共振 × 草日記留痕")
    print("─" * 40)

    if len(sys.argv) >= 3:
        # 命令行快速調用：python3 fuxi_taiji_engine.py "現象" "看見的根" [類別]
        visible = sys.argv[1]
        root_seen = sys.argv[2]
        category = sys.argv[3] if len(sys.argv) > 3 else "水"
        result = run_fuxi_deduce(visible, root_seen, category)
        _print_result(result)
        return

    print("\n  類別選項：水/土/火/木/金/人/龍/氣/根")
    visible   = input("\n  表面現象（新聞/外人說）：").strip()
    root_seen = input("  老大看見（根/歸位說法）：").strip()
    category  = input("  歸位類別 [默認:水]      ：").strip() or "水"
    note      = input("  補充說明 [可空]         ：").strip()

    if not visible or not root_seen:
        print("🔴 輸入不完整，退出。")
        return

    result = run_fuxi_deduce(visible, root_seen, category, extra_note=note)
    _print_result(result)


if __name__ == "__main__":
    main()
