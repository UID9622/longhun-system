#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂每日復盤引擎 v5.1
DNA: #龍芯⚡️2026-06-29-LONGHUN-REVIEW-v5.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬REVIEW-001 ✅

8項三色審計：文件完整、安全、系統心跳、測試、操作日誌、評估報告、API服務、備份狀態
"""

import os
import sys
import json
import time
import hashlib
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Any, Optional


# ============================================================
# 配置
# ============================================================

龍魂目錄 = Path.home() / ".龍魂"
復盤目錄 = 龍魂目錄 / "reviews"
報告目錄 = 龍魂目錄 / "reports"
CNSH目錄 = Path.home() / "longhun-system" / "cnsh"
LONGHUN系統 = Path.home() / "longhun-system"

for d in [復盤目錄, 報告目錄]:
    d.mkdir(parents=True, exist_ok=True)


# ============================================================
# DNA 追溯
# ============================================================

def 生成DNA(模塊: str, 動作: str) -> str:
    時間戳 = time.strftime("%Y-%m-%d-%H%M%S")
    熵 = hashlib.sha256(f"{模塊}-{動作}-{time.time_ns()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{時間戳}-{模塊}-{動作}-HASH{熵}"


# ============================================================
# 三色結果結構
# ============================================================

@dataclass
class 三色結果:
    顏色: str
    狀態: str
    詳情: str
    分值: float = 0.0


# ============================================================
# 8 項審計
# ============================================================

class 復盤引擎:
    def __init__(self):
        self.審計項: List[Dict[str, Any]] = []

    def 審計_文件完整性(self) -> 三色結果:
        core_files = [
            CNSH目錄 / "cnsh_runner.py",
            CNSH目錄 / "cnsh_redlines.py",
            CNSH目錄 / "cnsh_redline_boot.py",
            CNSH目錄 / "cnsh_redline_client.py",
            CNSH目錄 / "redlines.cnsh",
            LONGHUN系統 / "scripts" / "自動化評估.py",
            LONGHUN系統 / "scripts" / "復盤引擎.py",
        ]
        exists = sum(1 for f in core_files if f.exists())
        total = len(core_files)

        if exists == total:
            return 三色結果("🟢", "通過", f"核心文件齊全 {exists}/{total}", 10.0)
        elif exists >= total // 2:
            return 三色結果("🟡", "警告", f"核心文件缺失 {total - exists} 個", 5.0)
        else:
            return 三色結果("🔴", "失敗", f"核心文件嚴重缺失 {total - exists}/{total}", 2.0)

    def 審計_安全性(self) -> 三色結果:
        try:
            # 抑制 requests/urllib3 版本警告污染 stderr
            env = os.environ.copy()
            env["PYTHONWARNINGS"] = "ignore"
            result = subprocess.run(
                [sys.executable, "-m", "pip_audit", "--desc"],
                capture_output=True,
                text=True,
                timeout=300,
                env=env,
            )
            標準輸出 = result.stdout or ""
            標準錯誤 = result.stderr or ""
            # pip-audit 成功且無漏洞
            if result.returncode == 0 and "No known vulnerabilities" in 標準輸出:
                return 三色結果("🟢", "通過", "pip-audit 未發現已知漏洞", 10.0)
            # 發現已知漏洞（退出碼可能非零，stdout 含 CVE/PYSEC/GHSA）
            if any(k in 標準輸出 for k in ["CVE-", "PYSEC-", "GHSA-"]):
                return 三色結果("🟡", "警告", "pip-audit 發現潛在漏洞，請查看詳情", 5.0)
            # pip-audit 成功但僅有跳過項（無漏洞）
            if result.returncode == 0:
                return 三色結果("🟢", "通過", "pip-audit 未發現已知漏洞", 10.0)
            # pip-audit 未安裝
            if "No module named pip_audit" in 標準錯誤 or "No module named pip-audit" in 標準錯誤:
                return 三色結果("🟡", "警告", "pip-audit 未安裝，跳過安全掃描", 5.0)
            return 三色結果("🟡", "警告", f"pip-audit 執行異常: {標準錯誤[:100]}", 5.0)
        except FileNotFoundError:
            return 三色結果("🟡", "警告", "pip-audit 未安裝，跳過安全掃描", 5.0)
        except Exception as e:
            return 三色結果("🔴", "失敗", f"安全掃描異常: {e}", 2.0)

    def 審計_系統心跳(self) -> 三色結果:
        socket_path = CNSH目錄 / "redlines.sock"
        status_file = 龍魂目錄 / ".." / "longhun-system" / "logs" / "cnsh_redlines.status"
        status_file = status_file.resolve()

        daemon_alive = socket_path.exists()
        status_ok = status_file.exists()

        if daemon_alive and status_ok:
            return 三色結果("🟢", "通過", "CNSH 紅線守護進程運行中", 10.0)
        elif daemon_alive or status_ok:
            return 三色結果("🟡", "警告", "守護進程狀態部分可用", 5.0)
        else:
            return 三色結果("🔴", "失敗", "CNSH 紅線守護進程未運行", 2.0)

    def 審計_測試狀態(self) -> 三色結果:
        tests = [
            ("CNSH基本執行", [sys.executable, str(CNSH目錄 / "cnsh_runner.py"), '打印「復盤測試」']),
            ("紅線引擎", [sys.executable, str(CNSH目錄 / "cnsh_redlines.py"), "生态锁定"]),
            ("自動化評估", [sys.executable, str(LONGHUN系統 / "scripts" / "自動化評估.py"), "--status"]),
        ]
        passed = 0
        details = []
        for name, cmd in tests:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                ok = result.returncode == 0
                passed += int(ok)
                details.append(f"{name}: {'通過' if ok else '失敗'}")
            except Exception as e:
                details.append(f"{name}: 異常 {e}")

        if passed == len(tests):
            return 三色結果("🟢", "通過", f"所有測試通過 {passed}/{len(tests)}", 10.0)
        elif passed >= len(tests) // 2:
            return 三色結果("🟡", "警告", f"部分測試失敗 {passed}/{len(tests)}: {'; '.join(details)}", 5.0)
        else:
            return 三色結果("🔴", "失敗", f"測試嚴重失敗 {passed}/{len(tests)}: {'; '.join(details)}", 2.0)

    def 審計_操作日誌(self) -> 三色結果:
        action_log = 龍魂目錄 / "action_log.jsonl"
        if action_log.exists():
            lines = action_log.read_text(encoding="utf-8").strip().split("\n")
            lines = [l for l in lines if l.strip()]
            return 三色結果("🟢", "通過", f"操作日誌存在，共 {len(lines)} 條記錄", 10.0)
        else:
            return 三色結果("🟡", "警告", "操作日誌不存在", 5.0)

    def 審計_評估報告(self) -> 三色結果:
        assessments = sorted((龍魂目錄 / "assessments").glob("local_assessment_*.json"))
        if assessments:
            latest = assessments[-1]
            try:
                data = json.loads(latest.read_text(encoding="utf-8"))
                score = data.get("total_score", 0)
                return 三色結果("🟢", "通過", f"最新評估報告 {latest.name} 總分 {score}", 10.0)
            except Exception:
                return 三色結果("🟡", "警告", "最新評估報告解析失敗", 5.0)
        else:
            return 三色結果("🔴", "失敗", "未找到評估報告", 2.0)

    def 審計_API服務(self) -> 三色結果:
        socket_path = CNSH目錄 / "redlines.sock"
        if socket_path.exists():
            return 三色結果("🟢", "通過", f"CNSH 紅線本地 API 可用: {socket_path}", 10.0)
        else:
            return 三色結果("🔴", "失敗", "CNSH 紅線本地 API 不可用", 2.0)

    def 審計_備份狀態(self) -> 三色結果:
        backups = list((龍魂目錄 / "backups").glob("*")) if (龍魂目錄 / "backups").exists() else []
        dna_backups = list((龍魂目錄 / "xpay").glob("longhun_dna_backup_*.json")) if (龍魂目錄 / "xpay").exists() else []

        total = len(backups) + len(dna_backups)
        if total > 0:
            return 三色結果("🟢", "通過", f"備份文件存在 {total} 個", 10.0)
        else:
            return 三色結果("🟡", "警告", "未找到備份文件", 5.0)

    def 執行全面復盤(self) -> Dict[str, Any]:
        審計項 = [
            ("文件完整性", self.審計_文件完整性()),
            ("安全性", self.審計_安全性()),
            ("系統心跳", self.審計_系統心跳()),
            ("測試狀態", self.審計_測試狀態()),
            ("操作日誌", self.審計_操作日誌()),
            ("評估報告", self.審計_評估報告()),
            ("API服務", self.審計_API服務()),
            ("備份狀態", self.審計_備份狀態()),
        ]

        self.審計項 = [
            {"項": name, "顏色": r.顏色, "狀態": r.狀態, "詳情": r.詳情, "分值": r.分值}
            for name, r in 審計項
        ]

        green = sum(1 for r in self.審計項 if r["顏色"] == "🟢")
        yellow = sum(1 for r in self.審計項 if r["顏色"] == "🟡")
        red = sum(1 for r in self.審計項 if r["顏色"] == "🔴")
        avg_score = sum(r["分值"] for r in self.審計項) / len(self.審計項)

        if red > 0:
            overall = "🔴 需立即關注"
        elif yellow > len(self.審計項) / 3:
            overall = "🟡 需改進"
        else:
            overall = "🟢 系統正常"

        改進建議 = self.生成改進建議()

        return {
            "timestamp": time.strftime("%Y%m%d_%H%M%S"),
            "date": time.strftime("%Y-%m-%d"),
            "dna": "#龍芯⚡️2026-06-29-LONGHUN-REVIEW-v5.1",
            "執行DNA": 生成DNA("LONGHUN-REVIEW", "RUN"),
            "審計項": self.審計項,
            "統計": {"綠色": green, "黃色": yellow, "紅色": red, "平均分": round(avg_score, 2)},
            "綜合狀態": overall,
            "改進建議": 改進建議,
        }

    def 生成改進建議(self) -> List[str]:
        建議 = []
        for item in self.審計項:
            if item["顏色"] in ("🟡", "🔴"):
                建議.append(f"[{item['顏色']}] {item['項']}: {item['詳情']}")
        return 建議


# ============================================================
# 報告生成
# ============================================================

def 生成Markdown報告(報告: Dict[str, Any]) -> str:
    lines = [
        f"# 龍魂每日復盤報告 · {報告['date']}",
        "",
        f"**執行時間**: {報告['timestamp']}",
        f"**DNA**: {報告['dna']}",
        f"**執行DNA**: {報告['執行DNA']}",
        f"**綜合狀態**: {報告['綜合狀態']}",
        f"**統計**: 🟢 {報告['統計']['綠色']}  🟡 {報告['統計']['黃色']}  🔴 {報告['統計']['紅色']}  平均分 {報告['統計']['平均分']}",
        "",
        "## 審計明細",
        "",
        "| 審計項 | 狀態 | 詳情 | 分值 |",
        "|--------|------|------|------|",
    ]
    for item in 報告["審計項"]:
        lines.append(f"| {item['項']} | {item['顏色']} {item['狀態']} | {item['詳情']} | {item['分值']} |")

    lines.append("")
    lines.append("## 改進建議")
    lines.append("")
    if 報告["改進建議"]:
        for suggestion in 報告["改進建議"]:
            lines.append(f"- {suggestion}")
    else:
        lines.append("- 無，系統狀態良好")

    return "\n".join(lines)


# ============================================================
# CLI 入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂每日復盤引擎")
    parser.add_argument("--setup", action="store_true", help="設置目錄結構")
    parser.add_argument("--cron", action="store_true", help="Cron 靜默模式")
    parser.add_argument("--email", action="store_true", help="發送郵件報告")
    parser.add_argument("--trend", type=int, help="趨勢分析天數")
    parser.add_argument("--install-agent", action="store_true", help="安裝 LaunchAgent")
    args = parser.parse_args()

    if args.setup:
        for d in [復盤目錄, 報告目錄]:
            d.mkdir(parents=True, exist_ok=True)
        print("✅ 復盤目錄結構已設置")
        return

    引擎 = 復盤引擎()
    報告 = 引擎.執行全面復盤()

    timestamp = 報告["timestamp"]
    date = 報告["date"]
    json_path = 復盤目錄 / f"daily_review_{timestamp}.json"
    md_path = 復盤目錄 / f"daily_review_{date}.md"

    json_path.write_text(json.dumps(報告, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(生成Markdown報告(報告), encoding="utf-8")

    if not args.cron:
        print(生成Markdown報告(報告))
        print(f"\n報告已保存:")
        print(f"  JSON: {json_path}")
        print(f"  Markdown: {md_path}")
    else:
        print(f"[{timestamp}] 每日復盤完成: {報告['綜合狀態']}")


if __name__ == "__main__":
    main()
