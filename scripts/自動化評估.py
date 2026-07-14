#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂自動化日評估引擎 v5.1
DNA: #龍芯⚡️2026-06-29-LONGHUN-AUTOMATION-v5.1
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬AUTOMATION-001 ✅

6維度系統健康評估：環境、代碼、數據、可運行性、文檔、安全
"""

import os
import sys
import json
import time
import hashlib
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Any

try:
    import feishu_bot
except ImportError:
    feishu_bot = None


# ============================================================
# 配置
# ============================================================

龍魂目錄 = Path.home() / ".龍魂"
評估目錄 = 龍魂目錄 / "assessments"
日誌目錄 = 評估目錄 / "logs"
報告目錄 = 龍魂目錄 / "reports"
CNSH目錄 = Path.home() / "longhun-system" / "cnsh"

for d in [評估目錄, 日誌目錄, 報告目錄]:
    d.mkdir(parents=True, exist_ok=True)


def 加載環境文件(path: Path = Path.home() / ".longhun" / "webhooks.env") -> None:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            if line.startswith("export "):
                line = line[len("export "):]
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                os.environ.setdefault(key, value)


# ============================================================
# DNA 追溯
# ============================================================

def 生成DNA(模塊: str, 動作: str) -> str:
    時間戳 = time.strftime("%Y-%m-%d-%H%M%S")
    熵 = hashlib.sha256(f"{模塊}-{動作}-{time.time_ns()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{時間戳}-{模塊}-{動作}-HASH{熵}"


# ============================================================
# 飛書通知
# ============================================================

def _飛書請求(url: str, *, method: str = "GET", headers: dict | None = None, data: dict | None = None) -> dict:
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    body = json.dumps(data, ensure_ascii=False).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode('utf-8')}") from e


def 獲取飛書TenantToken() -> str:
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    if not app_id or not app_secret:
        raise RuntimeError("缺少 FEISHU_APP_ID / FEISHU_APP_SECRET")
    resp = _飛書請求(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        method="POST",
        data={"app_id": app_id, "app_secret": app_secret},
    )
    if resp.get("code") != 0:
        raise RuntimeError(f"獲取 tenant_token 失敗: {resp}")
    return resp["tenant_access_token"]


def 發送飛書評估報告(報告: Dict[str, Any]) -> bool:
    """將自動化評估摘要以卡片+文件形式發送到飛書群，失敗不阻斷主流程。"""
    chat_id = os.environ.get("FEISHU_CHAT_ID")
    if not chat_id:
        print("🟡 未設置 FEISHU_CHAT_ID，跳過飛書推送")
        return False
    if feishu_bot is None:
        print("🟡 未找到 feishu_bot 模塊，跳過飛書推送")
        return False

    try:
        # 構建交互式卡片
        elements: List[Dict[str, Any]] = [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**狀態**：{報告['status']}\n**總分**：{報告['total_score']} / {報告['max_score']}",
                },
            }
        ]
        for item in 報告["assessments"]:
            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**{item['category']}**：{item['score']} / {item['max_score']}",
                },
            })
        elements.append({
            "tag": "note",
            "elements": [{"tag": "plain_text", "content": 報告['執行DNA']}],
        })
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": f"🐉 龍魂自動化日評估 · {報告['timestamp']}"},
                "template": "blue",
            },
            "elements": elements,
        }
        feishu_bot.send_card(chat_id, card)
        print("🟢 評估卡片已發飛書")

        # 同時上傳並發送完整報告 JSON 文件
        report_file = 報告.get("report_file")
        if report_file and Path(report_file).exists():
            feishu_bot.send_file(chat_id, report_file)
            print("🟢 評估報告文件已發飛書")
        return True
    except Exception as e:
        print(f"🔴 飛書推送異常: {e}")
    return False


# ============================================================
# 6 維度評估
# ============================================================

class 自動化評估器:
    def __init__(self):
        self.維度權重 = {
            "環境檢查": 0.10,
            "代碼文件": 0.10,
            "數據完整性": 0.10,
            "可運行性": 0.25,
            "文檔完整性": 0.10,
            "安全性": 0.15,
            "反詐套路監控": 0.10,
            "DNA流程審計": 0.10,
        }
        self.評估結果: List[Dict[str, Any]] = []

    def 評估_環境檢查(self) -> Dict[str, Any]:
        python_version = sys.version.split()[0]
        longhun_exists = 龍魂目錄.exists()
        cnsh_exists = CNSH目錄.exists()
        shell_config = Path.home() / ".zshrc"

        score = 10.0 if (longhun_exists and cnsh_exists and shell_config.exists()) else 5.0
        return {
            "category": "環境檢查",
            "weight": self.維度權重["環境檢查"],
            "results": {
                "python_version": python_version,
                "longhun_dir": str(龍魂目錄),
                "cnsh_dir": str(CNSH目錄),
                "shell_config": str(shell_config),
                "longhun_exists": longhun_exists,
                "cnsh_exists": cnsh_exists,
            },
            "score": score,
            "max_score": 10.0,
        }

    def 評估_代碼文件(self) -> Dict[str, Any]:
        core_files = {
            "cnsh_runner.py": CNSH目錄 / "cnsh_runner.py",
            "cnsh_redlines.py": CNSH目錄 / "cnsh_redlines.py",
            "cnsh_redline_boot.py": CNSH目錄 / "cnsh_redline_boot.py",
            "cnsh_redline_client.py": CNSH目錄 / "cnsh_redline_client.py",
            "redlines.cnsh": CNSH目錄 / "redlines.cnsh",
        }
        results = {}
        all_exist = True
        for name, path in core_files.items():
            exists = path.exists()
            results[name] = {
                "exists": exists,
                "size_bytes": path.stat().st_size if exists else 0,
                "path": str(path),
            }
            if not exists:
                all_exist = False

        # 語法檢查
        syntax_ok = True
        for name, path in core_files.items():
            if name.endswith(".py") and path.exists():
                try:
                    subprocess.run(
                        [sys.executable, "-m", "py_compile", str(path)],
                        check=True,
                        capture_output=True,
                        timeout=10,
                    )
                except subprocess.CalledProcessError:
                    syntax_ok = False
                    results[name]["syntax_ok"] = False
                else:
                    results[name]["syntax_ok"] = True

        score = 10.0 if all_exist and syntax_ok else 5.0
        return {
            "category": "代碼文件",
            "weight": self.維度權重["代碼文件"],
            "results": results,
            "score": score,
            "max_score": 10.0,
        }

    def 評估_數據完整性(self) -> Dict[str, Any]:
        results = {}
        total_score = 10.0

        # CNSH 紅線詞組定義
        redlines_file = CNSH目錄 / "redlines.cnsh"
        if redlines_file.exists():
            content = redlines_file.read_text(encoding="utf-8")
            results["redlines_definition"] = {
                "exists": True,
                "has_dna": "#龍芯⚡️" in content,
                "size_bytes": redlines_file.stat().st_size,
            }
        else:
            results["redlines_definition"] = {"exists": False}
            total_score -= 5.0

        # 評估歷史
        assessments = sorted(評估目錄.glob("local_assessment_*.json"))
        results["assessment_history"] = {
            "count": len(assessments),
            "latest": str(assessments[-1]) if assessments else None,
        }

        # 日誌目錄
        results["logs_dir"] = {
            "exists": 日誌目錄.exists(),
            "file_count": len(list(日誌目錄.glob("*"))) if 日誌目錄.exists() else 0,
        }

        return {
            "category": "數據完整性",
            "weight": self.維度權重["數據完整性"],
            "results": results,
            "score": max(0.0, total_score),
            "max_score": 10.0,
        }

    def 評估_可運行性(self) -> Dict[str, Any]:
        results = {}
        score = 10.0

        # CNSH 基本執行
        try:
            output = subprocess.run(
                [sys.executable, str(CNSH目錄 / "cnsh_runner.py"), '打印「評估測試」'],
                capture_output=True,
                text=True,
                timeout=15,
            )
            results["cnsh_basic"] = {
                "command": 'cnsh_runner.py "打印「評估測試」"',
                "runs_successfully": output.returncode == 0 and "評估測試" in output.stdout,
                "returncode": output.returncode,
            }
            if not results["cnsh_basic"]["runs_successfully"]:
                score -= 3.0
        except Exception as e:
            results["cnsh_basic"] = {"runs_successfully": False, "error": str(e)}
            score -= 3.0

        # 紅線引擎執行
        try:
            output = subprocess.run(
                [sys.executable, str(CNSH目錄 / "cnsh_redlines.py"), "生态锁定"],
                capture_output=True,
                text=True,
                timeout=15,
            )
            results["redlines_engine"] = {
                "command": "cnsh_redlines.py \"生态锁定\"",
                "runs_successfully": output.returncode == 0 and "🔴" in output.stdout,
                "returncode": output.returncode,
            }
            if not results["redlines_engine"]["runs_successfully"]:
                score -= 3.0
        except Exception as e:
            results["redlines_engine"] = {"runs_successfully": False, "error": str(e)}
            score -= 3.0

        # 守護進程狀態
        socket_path = CNSH目錄 / "redlines.sock"
        results["redline_daemon"] = {
            "socket_exists": socket_path.exists(),
        }
        if not socket_path.exists():
            score -= 2.0

        return {
            "category": "可運行性",
            "weight": self.維度權重["可運行性"],
            "results": results,
            "score": max(0.0, score),
            "max_score": 10.0,
        }

    def 評估_文檔完整性(self) -> Dict[str, Any]:
        docs = {
            "README.md": Path.home() / "longhun-system" / "README.md",
            "CNSH轉譯器": CNSH目錄 / "cnsh_runner.py",
            "紅線詞組": CNSH目錄 / "redlines.cnsh",
        }
        results = {}
        exists_count = 0
        for name, path in docs.items():
            exists = path.exists()
            results[name] = {"exists": exists, "path": str(path)}
            if exists:
                exists_count += 1

        score = 10.0 * (exists_count / len(docs))
        return {
            "category": "文檔完整性",
            "weight": self.維度權重["文檔完整性"],
            "results": results,
            "score": score,
            "max_score": 10.0,
        }

    def 評估_安全性(self) -> Dict[str, Any]:
        results = {}
        score = 10.0

        # CNSH 目錄權限
        if CNSH目錄.exists():
            mode = oct(CNSH目錄.stat().st_mode)[-3:]
            results["cnsh_dir_permissions"] = {
                "permissions": mode,
                "secure": mode in ("755", "700", "750"),
            }
            if not results["cnsh_dir_permissions"]["secure"]:
                score -= 2.0

        # 紅線文件含 DNA
        redlines_file = CNSH目錄 / "redlines.cnsh"
        if redlines_file.exists():
            content = redlines_file.read_text(encoding="utf-8")
            results["redlines_dna"] = {
                "has_dna": "#龍芯⚡️" in content,
                "has_confirm": "#CONFIRM🌌9622-ONLY-ONCE" in content,
            }
            if not results["redlines_dna"]["has_dna"]:
                score -= 3.0
        else:
            results["redlines_dna"] = {"exists": False}
            score -= 5.0

        # 套接字權限
        socket_path = CNSH目錄 / "redlines.sock"
        if socket_path.exists():
            mode = oct(socket_path.stat().st_mode)[-3:]
            results["socket_permissions"] = {
                "permissions": mode,
                "secure": mode in ("600", "700"),
            }
        else:
            results["socket_permissions"] = {"exists": False}

        return {
            "category": "安全性",
            "weight": self.維度權重["安全性"],
            "results": results,
            "score": max(0.0, score),
            "max_score": 10.0,
        }

    def 評估_反詐套路監控(self) -> Dict[str, Any]:
        """調用龍智守套路分析腳本，監控近7天詐騙/營銷套路趨勢。"""
        results: Dict[str, Any] = {"log_exists": False}
        score = 10.0
        analyzer = Path.home() / "longhun-system" / "scripts" / "龍智守_套路分析.py"
        log_file = Path.home() / "longhun-system" / "logs" / "龍智守_套路识别日志.jsonl"
        results["log_exists"] = log_file.exists()
        results["analyzer_exists"] = analyzer.exists()

        if not analyzer.exists() or not log_file.exists():
            score = 5.0
            return {
                "category": "反詐套路監控",
                "weight": self.維度權重["反詐套路監控"],
                "results": results,
                "score": score,
                "max_score": 10.0,
            }

        try:
            output = subprocess.run(
                [sys.executable, str(analyzer), "--days", "7", "--top", "10"],
                capture_output=True,
                text=True,
                timeout=60,
            )
            data = json.loads(output.stdout) if output.returncode == 0 else {}
        except Exception as e:
            data = {}
            results["error"] = str(e)

        total = data.get("total_records", 0)
        categories = data.get("categories", {})
        fraud_count = categories.get("詐騙", 0)
        marketing_count = categories.get("營銷套路", 0)
        gray_count = categories.get("灰色話術", 0)

        results.update({
            "total_records": total,
            "fraud_count": fraud_count,
            "marketing_count": marketing_count,
            "gray_count": gray_count,
            "top_patterns": data.get("top_patterns", {}),
            "intents": data.get("intents", {}),
            "risks": data.get("risks", {}),
        })

        if fraud_count > 0:
            score = 5.0
        elif total == 0:
            score = 6.0
        else:
            score = 8.0

        return {
            "category": "反詐套路監控",
            "weight": self.維度權重["反詐套路監控"],
            "results": results,
            "score": score,
            "max_score": 10.0,
        }

    def 評估_DNA流程審計(self) -> Dict[str, Any]:
        """檢查龍魂 DNA 流程審計庫的完整性與覆蓋率。"""
        results: Dict[str, Any] = {}
        score = 10.0
        audit_log = Path.home() / "longhun-system" / "logs" / "龍魂流程審計庫.jsonl"
        results["audit_log_exists"] = audit_log.exists()

        if not audit_log.exists():
            score = 5.0
            return {
                "category": "DNA流程審計",
                "weight": self.維度權重["DNA流程審計"],
                "results": results,
                "score": score,
                "max_score": 10.0,
            }

        try:
            sys.path.insert(0, str(Path.home() / "longhun-system" / "scripts"))
            import 龍魂DNA審計門戶 as dna_portal
            records = dna_portal.load_records()
        except Exception as e:
            records = []
            results["load_error"] = str(e)
            score = 5.0

        total = len(records)
        results["total_records"] = total
        if total == 0:
            score = min(score, 6.0)

        missing_card_hash = sum(1 for r in records if not r.get("output_card_hash"))
        missing_file_hash = sum(
            1 for r in records
            if r.get("output_files") and any(h is None for h in r["output_files"].values())
        )
        results["missing_card_hash"] = missing_card_hash
        results["missing_file_hash"] = missing_file_hash

        if missing_card_hash or missing_file_hash:
            score = min(score, 6.0)

        # 近7天是否有🔴記錄（作為提醒，不直接扣到不及格）
        fraud_records = [r for r in records if r.get("three_color", {}).get("status") == "🔴"]
        results["fraud_records_total"] = len(fraud_records)

        return {
            "category": "DNA流程審計",
            "weight": self.維度權重["DNA流程審計"],
            "results": results,
            "score": score,
            "max_score": 10.0,
        }

    def 執行全面評估(self) -> Dict[str, Any]:
        self.評估結果 = [
            self.評估_環境檢查(),
            self.評估_代碼文件(),
            self.評估_數據完整性(),
            self.評估_可運行性(),
            self.評估_文檔完整性(),
            self.評估_安全性(),
            self.評估_反詐套路監控(),
            self.評估_DNA流程審計(),
        ]

        total = sum(r["score"] * r["weight"] for r in self.評估結果)
        max_total = sum(r["max_score"] * r["weight"] for r in self.評估結果)

        if total >= 8.0:
            status = "✅ 生產級可用"
        elif total >= 6.0:
            status = "🟡 需要改進"
        else:
            status = "🔴 不推薦使用"

        return {
            "timestamp": time.strftime("%Y%m%d_%H%M%S"),
            "dna": "#龍芯⚡️2026-06-29-LONGHUN-AUTOMATION-v5.1",
            "執行DNA": 生成DNA("LONGHUN-AUTOMATION", "RUN"),
            "assessments": self.評估結果,
            "total_score": round(total, 2),
            "max_score": round(max_total, 2),
            "status": status,
            "report_file": "",
        }


# ============================================================
# 報告生成
# ============================================================

def 生成Markdown報告(報告: Dict[str, Any]) -> str:
    lines = [
        "# 龍魂自動化日評估報告",
        "",
        f"**時間**: {報告['timestamp']}",
        f"**DNA**: {報告['dna']}",
        f"**執行DNA**: {報告['執行DNA']}",
        f"**總分**: {報告['total_score']} / {報告['max_score']}",
        f"**狀態**: {報告['status']}",
        "",
        "## 6 維度評估明細",
        "",
        "| 維度 | 權重 | 得分 | 滿分 |",
        "|------|------|------|------|",
    ]
    for item in 報告["assessments"]:
        lines.append(f"| {item['category']} | {item['weight']:.0%} | {item['score']} | {item['max_score']} |")

    lines.append("")
    lines.append("## 詳細結果")
    lines.append("")
    for item in 報告["assessments"]:
        lines.append(f"### {item['category']}（{item['score']}/{item['max_score']}）")
        lines.append(f"```json")
        lines.append(json.dumps(item["results"], ensure_ascii=False, indent=2))
        lines.append(f"```")
        lines.append("")

    return "\n".join(lines)


# ============================================================
# CLI 入口
# ============================================================

def main():
    加載環境文件()
    import argparse
    parser = argparse.ArgumentParser(description="龍魂自動化日評估引擎")
    parser.add_argument("--setup", action="store_true", help="設置目錄結構與 Cron")
    parser.add_argument("--status", action="store_true", help="查看狀態")
    parser.add_argument("--cron", action="store_true", help="Cron 靜默模式")
    parser.add_argument("--weekly", action="store_true", help="生成周報")
    parser.add_argument("--trend", type=int, help="趨勢分析天數")
    parser.add_argument("--feishu", action="store_true", help="執行完畢後發送飛書群消息")
    args = parser.parse_args()

    if args.setup:
        # 創建目錄
        for d in [評估目錄, 日誌目錄, 報告目錄]:
            d.mkdir(parents=True, exist_ok=True)
        print("✅ 目錄結構已設置")
        print(f"   評估目錄: {評估目錄}")
        print(f"   日誌目錄: {日誌目錄}")
        print(f"   報告目錄: {報告目錄}")
        return

    if args.status:
        assessments = sorted(評估目錄.glob("local_assessment_*.json"))
        print(f"🐉 龍魂自動化評估狀態")
        print(f"   歷史評估數: {len(assessments)}")
        if assessments:
            print(f"   最新評估: {assessments[-1].name}")
        return

    評估器 = 自動化評估器()
    報告 = 評估器.執行全面評估()

    # 保存 JSON
    timestamp = 報告["timestamp"]
    json_path = 評估目錄 / f"local_assessment_{timestamp}.json"
    報告["report_file"] = str(json_path)
    json_path.write_text(json.dumps(報告, ensure_ascii=False, indent=2), encoding="utf-8")

    # 保存 Markdown 摘要
    md_path = 評估目錄 / "ASSESSMENT_SUMMARY.md"
    md_path.write_text(生成Markdown報告(報告), encoding="utf-8")

    if not args.cron:
        print(生成Markdown報告(報告))
    else:
        print(f"[{timestamp}] 自動化評估完成: {報告['status']} 總分 {報告['total_score']}/{報告['max_score']}")

    if args.feishu:
        發送飛書評估報告(報告)


if __name__ == "__main__":
    main()
