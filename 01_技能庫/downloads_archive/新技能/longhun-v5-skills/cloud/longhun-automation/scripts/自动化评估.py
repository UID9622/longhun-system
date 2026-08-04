#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-19-LONGHUN-AUTOMATION-v5.1
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂自動化日評估引擎
DNA: #龍芯⚡️2026-06-19-LONGHUN-AUTOMATION-v5.1
功能: 6維度系統評估 · Cron定時任務 · 自動化周報生成 · 狀態檢查
"""

import os
import sys
import json
import glob
import shutil
import subprocess
import datetime
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# ═══════════════════════════════════════════════════════════
# 全局配置
# ═══════════════════════════════════════════════════════════

配置 = {
    "龍魂目錄": Path.home() / ".龍魂",
    "評估目錄": Path.home() / ".龍魂" / "assessments",
    "日誌目錄": Path.home() / ".龍魂" / "assessments" / "logs",
    "報告目錄": Path.home() / ".龍魂" / "reports",
    "XPAY目錄": Path.home() / ".龍魂" / "xpay",
    "系統目錄": Path.home() / "longhun-system",
    "最大分數": 10.0,
    "DNA標記": "#龍芯⚡️2026-06-19-LONGHUN-AUTOMATION-v5.1",
}

維度權重 = {
    "環境檢查": 0.10,   # 10%
    "代碼文件": 0.20,   # 20%
    "數據完整性": 0.20,  # 20%
    "可運行性": 0.25,   # 25%
    "文檔完整性": 0.10, # 10%
    "安全性": 0.15,     # 15%
}

# ═══════════════════════════════════════════════════════════
# 工具函數
# ═══════════════════════════════════════════════════════════

def 獲取時間戳() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def 獲取日期標記() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def 獲取今日日期() -> str:
    return datetime.date.today().isoformat()


def 執行命令(命令: List[str], 超時: int = 30) -> Tuple[int, str, str]:
    try:
        結果 = subprocess.run(
            命令,
            capture_output=True,
            text=True,
            timeout=超時,
            cwd=str(Path.home())
        )
        return 結果.returncode, 結果.stdout, 結果.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "命令超時"
    except Exception as 錯誤:
        return -2, "", str(錯誤)


def 確保目錄(目錄: Path) -> None:
    目錄.mkdir(parents=True, exist_ok=True)


def 寫入JSON(路徑: Path, 數據: Dict[str, Any]) -> None:
    with open(路徑, 'w', encoding='utf-8') as 文件:
        json.dump(數據, 文件, ensure_ascii=False, indent=2)


def 寫入文本(路徑: Path, 內容: str) -> None:
    with open(路徑, 'w', encoding='utf-8') as 文件:
        文件.write(內容)


def 讀取文本(路徑: Path) -> str:
    try:
        with open(路徑, 'r', encoding='utf-8') as 文件:
            return 文件.read()
    except:
        return ""


def 計算MD5(文件路徑: Path) -> str:
    try:
        哈希 = hashlib.md5()
        with open(文件路徑, 'rb') as 文件:
            for 塊 in iter(lambda: 文件.read(8192), b""):
                哈希.update(塊)
        return 哈希.hexdigest()
    except:
        return ""


def 記錄日誌(信息: str) -> None:
    確保目錄(配置["日誌目錄"])
    時間戳 = 獲取時間戳()
    日誌文件 = 配置["日誌目錄"] / f"daily_assessment_{datetime.date.today().isoformat()}.log"
    with open(日誌文件, 'a', encoding='utf-8') as 文件:
        文件.write(f"[{時間戳}] {信息}\n")
    print(f"[{時間戳}] {信息}")


# ═══════════════════════════════════════════════════════════
# 第1維度: 環境檢查 (權重 10%)
# ═══════════════════════════════════════════════════════════

def 評估_環境檢查() -> Tuple[float, Dict]:
    """檢查Python版本、目錄結構、Shell配置"""
    結果 = {}
    得分 = 0.0
    滿分 = 配置["最大分數"]

    # 檢查Python版本
    Python版本 = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    結果["python_version"] = Python版本
    if sys.version_info >= (3, 10):
        結果["python_version_合格"] = True
        得分 += 滿分 * 0.3
    else:
        結果["python_version_合格"] = False

    # 檢查龍魂目錄
    if 配置["龍魂目錄"].exists():
        結果["龍魂目錄"] = str(配置["龍魂目錄"])
        結果["龍魂目錄_存在"] = True
        得分 += 滿分 * 0.2
    else:
        結果["龍魂目錄_存在"] = False
        結果["龍魂目錄"] = str(配置["龍魂目錄"])

    # 檢查XPAY目錄
    if 配置["XPAY目錄"].exists():
        結果["xpay目錄"] = str(配置["XPAY目錄"])
        結果["xpay目錄_存在"] = True
        得分 += 滿分 * 0.2
    else:
        結果["xpay目錄_存在"] = False

    # 檢查系統目錄
    if 配置["系統目錄"].exists():
        結果["系統目錄"] = str(配置["系統目錄"])
        結果["系統目錄_存在"] = True
        得分 += 滿分 * 0.15
    else:
        結果["系統目錄_存在"] = False

    # 檢查Shell配置
    for Shell文件 in [".zshrc", ".bashrc", ".bash_profile"]:
        Shell路徑 = Path.home() / Shell文件
        if Shell路徑.exists():
            結果["shell_config"] = str(Shell路徑)
            結果["shell_config_存在"] = True
            得分 += 滿分 * 0.15
            break
    else:
        結果["shell_config_存在"] = False

    return round(得分, 2), 結果


# ═══════════════════════════════════════════════════════════
# 第2維度: 代碼文件 (權重 20%)
# ═══════════════════════════════════════════════════════════

def 評估_代碼文件() -> Tuple[float, Dict]:
    """檢查核心代碼文件完整性"""
    結果 = {}
    得分 = 0.0
    滿分 = 配置["最大分數"]

    核心文件清單 = [
        (配置["XPAY目錄"] / "xpay_cli.py", 0.25),
        (配置["XPAY目錄"] / "xpay_core.py", 0.25),
        (配置["XPAY目錄"] / "xpay_db.py", 0.20),
        (配置["XPAY目錄"] / "startup.sh", 0.15),
        (配置["XPAY目錄"] / "config.py", 0.15),
    ]

    存在數量 = 0
    文件哈希 = {}
    for 文件路徑, 權重 in 核心文件清單:
        存在 = 文件路徑.exists()
        結果[文件路徑.name] = {
            "存在": 存在,
            "路徑": str(文件路徑),
        }
        if 存在:
            存在數量 += 1
            文件哈希[文件路徑.name] = 計算MD5(文件路徑)
            結果[文件路徑.name]["大小"] = 文件路徑.stat().st_size
            得分 += 滿分 * 權重

    結果["核心文件總數"] = len(核心文件清單)
    結果["核心文件存在數"] = 存在數量
    結果["文件哈希"] = 文件哈希

    return round(得分, 2), 結果


# ═══════════════════════════════════════════════════════════
# 第3維度: 數據完整性 (權重 20%)
# ═══════════════════════════════════════════════════════════

def 評估_數據完整性() -> Tuple[float, Dict]:
    """檢查交易數據、日誌、備份"""
    結果 = {}
    得分 = 0.0
    滿分 = 配置["最大分數"]

    # 檢查數據庫文件
    DB路徑 = 配置["XPAY目錄"] / "xpay.db"
    if DB路徑.exists():
        DB大小 = DB路徑.stat().st_size
        結果["數據庫_存在"] = True
        結果["數據庫_大小"] = DB大小
        結果["數據庫_路徑"] = str(DB路徑)
        得分 += 滿分 * 0.3

        # 嘗試獲取記錄數
        try:
            返回碼, 輸出, 錯誤 = 執行命令(
                ["python3", str(配置["XPAY目錄"] / "xpay_cli.py"), "stats"]
            )
            if 返回碼 == 0:
                結果["數據庫統計"] = 輸出.strip()
                得分 += 滿分 * 0.2
        except:
            pass
    else:
        結果["數據庫_存在"] = False

    # 檢查日誌文件
    日誌路徑 = 配置["龍魂目錄"] / "logs"
    if 日誌路徑.exists():
        日誌文件 = list(日誌路徑.glob("*.log"))
        結果["日誌文件數"] = len(日誌文件)
        if len(日誌文件) > 0:
            得分 += 滿分 * 0.2
    else:
        結果["日誌文件數"] = 0

    # 檢查備份
    備份路徑 = 配置["龍魂目錄"] / "backups"
    if 備份路徑.exists():
        備份文件 = list(備份路徑.glob("*"))
        結果["備份文件數"] = len(備份文件)
        if len(備份文件) > 0:
            得分 += 滿分 * 0.15
    else:
        結果["備份文件數"] = 0

    # 檢查交易記錄
    try:
        交易路徑 = 配置["龍魂目錄"] / "transactions"
        if 交易路徑.exists():
            交易文件 = list(交易路徑.glob("*.json"))
            結果["交易記錄數"] = len(交易文件)
            if len(交易文件) > 0:
                得分 += 滿分 * 0.15
    except:
        結果["交易記錄數"] = 0

    return round(得分, 2), 結果


# ═══════════════════════════════════════════════════════════
# 第4維度: 可運行性 (權重 25%)
# ═══════════════════════════════════════════════════════════

def 評估_可運行性() -> Tuple[float, Dict]:
    """執行CLI命令測試系統可運行性"""
    結果 = {}
    得分 = 0.0
    滿分 = 配置["最大分數"]

    # 測試1: xpay_cli.py help
    CLI路徑 = 配置["XPAY目錄"] / "xpay_cli.py"
    if CLI路徑.exists():
        返回碼, 輸出, 錯誤 = 執行命令(
            ["python3", str(CLI路徑), "--help"],
            超時=10
        )
        結果["cli_help_返回碼"] = 返回碼
        if 返回碼 == 0:
            結果["cli_help"] = "✅ 成功"
            得分 += 滿分 * 0.25
        else:
            結果["cli_help"] = f"❌ 失敗: {錯誤[:100]}"

        # 測試2: xpay_cli.py stats
        返回碼2, 輸出2, 錯誤2 = 執行命令(
            ["python3", str(CLI路徑), "stats"],
            超時=10
        )
        結果["cli_stats_返回碼"] = 返回碼2
        if 返回碼2 == 0:
            結果["cli_stats"] = "✅ 成功"
            得分 += 滿分 * 0.25
        else:
            結果["cli_stats"] = f"❌ 失敗: {錯誤2[:100]}"

        # 測試3: xpay_cli.py version
        返回碼3, 輸出3, 錯誤3 = 執行命令(
            ["python3", str(CLI路徑), "version"],
            超時=10
        )
        結果["cli_version_返回碼"] = 返回碼3
        if 返回碼3 == 0:
            結果["cli_version"] = 輸出3.strip()
            得分 += 滿分 * 0.20
        else:
            結果["cli_version"] = f"❌ 失敗"
    else:
        結果["cli_路徑不存在"] = str(CLI路徑)

    # 測試4: 系統Python可用性
    返回碼4, 輸出4, _ = 執行命令(["python3", "-c", "print('OK')"], 超時=5)
    if 返回碼4 == 0 and "OK" in 輸出4:
        結果["python3_可用"] = True
        得分 += 滿分 * 0.15
    else:
        結果["python3_可用"] = False

    # 測試5: pip可用性
    返回碼5, _, _ = 執行命令(["pip3", "--version"], 超時=5)
    if 返回碼5 == 0:
        結果["pip3_可用"] = True
        得分 += 滿分 * 0.15
    else:
        結果["pip3_可用"] = False

    return round(得分, 2), 結果


# ═══════════════════════════════════════════════════════════
# 第5維度: 文檔完整性 (權重 10%)
# ═══════════════════════════════════════════════════════════

def 評估_文檔完整性() -> Tuple[float, Dict]:
    """檢查README、部署文件等文檔"""
    結果 = {}
    得分 = 0.0
    滿分 = 配置["最大分數"]

    文檔清單 = [
        (配置["龍魂目錄"] / "README.md", 0.30, "主README"),
        (配置["XPAY目錄"] / "README.md", 0.25, "XPAY文檔"),
        (配置["系統目錄"] / "README.md", 0.20, "系統文檔"),
        (配置["龍魂目錄"] / "DEPLOYMENT.md", 0.15, "部署文檔"),
        (配置["龍魂目錄"] / "CHANGELOG.md", 0.10, "變更日誌"),
    ]

    文檔總分 = 0.0
    for 文件路徑, 權重, 名稱 in 文檔清單:
        存在 = 文件路徑.exists()
        結果[名稱] = {
            "存在": 存在,
            "路徑": str(文件路徑),
        }
        if 存在:
            大小 = 文件路徑.stat().st_size
            結果[名稱]["大小"] = 大小
            if 大小 > 100:
                文檔總分 += 滿分 * 權重

    # 額外檢查文檔內容DNA標記
    README路徑 = 配置["龍魂目錄"] / "README.md"
    if README路徑.exists():
        內容 = 讀取文本(README路徑)
        if "龍芯" in 內容 or "DNA" in 內容:
            結果["文檔含DNA標記"] = True
            文檔總分 += 滿分 * 0.05
        else:
            結果["文檔含DNA標記"] = False

    得分 = round(文檔總分, 2)
    結果["文檔總分"] = 得分
    return 得分, 結果


# ═══════════════════════════════════════════════════════════
# 第6維度: 安全性 (權重 15%)
# ═══════════════════════════════════════════════════════════

def 評估_安全性() -> Tuple[float, Dict]:
    """檢查本地存儲、權限、DNA完整性"""
    結果 = {}
    得分 = 0.0
    滿分 = 配置["最大分數"]

    # 檢查目錄權限
    if 配置["龍魂目錄"].exists():
        狀態 = 配置["龍魂目錄"].stat()
        權限 = oct(狀態.st_mode)[-3:]
        結果["龍魂目錄權限"] = 權限
        # 700 或 755 為合理權限
        if 權限 in ["700", "755", "750"]:
            得分 += 滿分 * 0.25
            結果["權限檢查"] = "✅ 合理"
        else:
            結果["權限檢查"] = f"⚠️ 當前權限: {權限}"
    else:
        結果["權限檢查"] = "❌ 目錄不存在"

    # 檢查數據庫權限
    DB路徑 = 配置["XPAY目錄"] / "xpay.db"
    if DB路徑.exists():
        DB狀態 = DB路徑.stat()
        DB權限 = oct(DB狀態.st_mode)[-3:]
        結果["數據庫權限"] = DB權限
        if DB權限 in ["600", "644"]:
            得分 += 滿分 * 0.20
            結果["數據庫權限檢查"] = "✅ 合理"
        else:
            結果["數據庫權限檢查"] = f"⚠️ 當前權限: {DB權限}"

    # 檢查DNA標記存在性
    for 目錄 in [配置["龍魂目錄"], 配置["系統目錄"]]:
        if 目錄.exists():
            DNA文件 = 目錄 / "DNA"
            if DNA文件.exists():
                DNA內容 = 讀取文本(DNA文件)
                結果["DNA文件"] = str(DNA文件)
                結果["DNA標記"] = DNA內容[:100] if DNA內容 else "空"
                得分 += 滿分 * 0.25
                break
    else:
        # 檢查README中是否有DNA
        README路徑 = 配置["龍魂目錄"] / "README.md"
        if README路徑.exists():
            內容 = 讀取文本(README路徑)
            if "#龍芯" in 內容:
                結果["DNA標記"] = "在README.md中發現"
                得分 += 滿分 * 0.20

    # 檢查是否有備份策略
    備份路徑 = 配置["龍魂目錄"] / "backups"
    if 備份路徑.exists():
        備份數 = len(list(備份路徑.glob("*")))
        結果["備份數量"] = 備份數
        if 備份數 > 0:
            得分 += 滿分 * 0.15
    else:
        結果["備份數量"] = 0

    # 檢查是否有.gitingore或排除敏感文件
    for 文件名 in [".gitignore", ".env.example"]:
        文件路徑 = 配置["龍魂目錄"] / 文件名
        if 文件路徑.exists():
            結果[f"{文件名}_存在"] = True
            得分 += 滿分 * 0.075
        else:
            結果[f"{文件名}_存在"] = False

    return round(得分, 2), 結果


# ═══════════════════════════════════════════════════════════
# 評估引擎核心
# ═══════════════════════════════════════════════════════════

def 執行全面評估() -> Dict[str, Any]:
    """執行完整6維度評估"""
    記錄日誌("════════════════════════════════════════════════════════════")
    記錄日誌("🐉 龍魂系統 · 自動化日評估")
    記錄日誌(f"時間: {獲取時間戳()}")
    記錄日誌("════════════════════════════════════════════════════════════")

    評估結果 = []
    總加權分 = 0.0

    # 維度函數映射
    維度函數 = {
        "環境檢查": 評估_環境檢查,
        "代碼文件": 評估_代碼文件,
        "數據完整性": 評估_數據完整性,
        "可運行性": 評估_可運行性,
        "文檔完整性": 評估_文檔完整性,
        "安全性": 評估_安全性,
    }

    for 維度名稱, 評估函數 in 維度函數.items():
        記錄日誌(f"\n【{維度名稱}】")
        權重 = 維度權重[維度名稱]

        try:
            原始分, 詳細結果 = 評估函數()
        except Exception as 錯誤:
            記錄日誌(f"  ❌ 評估失敗: {錯誤}")
            原始分 = 0.0
            詳細結果 = {"錯誤": str(錯誤)}

        加權分 = round(原始分 * 權重, 2)
        總加權分 += 加權分

        記錄日誌(f"  評分: {原始分}/{配置['最大分數']} (權重 {權重*100:.0f}%)")
        for 鍵, 值 in 詳細結果.items():
            if isinstance(值, bool):
                符號 = "✅" if 值 else "❌"
                記錄日誌(f"  {符號} {鍵}: {值}")
            elif isinstance(值, (str, int)):
                記錄日誌(f"  • {鍵}: {值}")

        評估結果.append({
            "category": 維度名稱,
            "score": 原始分,
            "max_score": 配置["最大分數"],
            "weight": 權重,
            "weighted_score": 加權分,
            "results": 詳細結果,
        })

    # 計算最終評分
    總分 = round(總加權分, 2)
    if 總分 >= 8.0:
        狀態 = "✅ 生產級可用"
    elif 總分 >= 6.0:
        狀態 = "🟡 需要改進"
    else:
        狀態 = "🔴 不推薦使用"

    記錄日誌(f"\n{'═' * 60}")
    記錄日誌(f"總評分: {總分}/{配置['最大分數']}")
    記錄日誌(f"狀態: {狀態}")
    記錄日誌(f"{'═' * 60}")

    return {
        "total_score": 總分,
        "max_score": 配置["最大分數"],
        "status": 狀態,
        "timestamp": 獲取時間戳(),
        "date": 獲取今日日期(),
        "dna": 配置["DNA標記"],
        "assessments": 評估結果,
    }


# ═══════════════════════════════════════════════════════════
# 報告生成
# ═══════════════════════════════════════════════════════════

def 生成JSON報告(評估數據: Dict[str, Any]) -> Path:
    """生成JSON格式評估報告"""
    確保目錄(配置["評估目錄"])
    文件名 = f"local_assessment_{獲取日期標記()}.json"
    路徑 = 配置["評估目錄"] / 文件名
    寫入JSON(路徑, 評估數據)
    記錄日誌(f"📄 JSON報告已生成: {路徑}")
    return 路徑


def 生成Markdown總結(評估數據: Dict[str, Any]) -> Path:
    """生成Markdown格式評估總結"""
    確保目錄(配置["評估目錄"])
    路徑 = 配置["評估目錄"] / "ASSESSMENT_SUMMARY.md"

    內容 = f"""# 🐉 龍魂系統評估總結

**生成時間**: {評估數據['timestamp']}
**DNA**: {評估數據['dna']}

---

## 📊 總體評分

| 指標 | 數值 |
|------|------|
| **總分** | {評估數據['total_score']}/{評估數據['max_score']} |
| **狀態** | {評估數據['status']} |
| **評估日期** | {評估數據['date']} |

---

## 📋 各維度評分

| 維度 | 原始分 | 權重 | 加權分 | 狀態 |
|------|--------|------|--------|------|
"""

    for 評估 in 評估數據['assessments']:
        狀態圖標 = "🟢" if 評估['score'] >= 8.0 else "🟡" if 評估['score'] >= 6.0 else "🔴"
        內容 += f"| {評估['category']} | {評估['score']}/{評估['max_score']} | {評估['weight']*100:.0f}% | {評估['weighted_score']} | {狀態圖標} |\n"

    內容 += f"""
---

## 🔍 詳細結果

"""
    for 評估 in 評估數據['assessments']:
        內容 += f"### {評估['category']} (權重 {評估['weight']*100:.0f}%)\n\n"
        for 鍵, 值 in 評估['results'].items():
            if isinstance(值, dict):
                內容 += f"- **{鍵}**: {json.dumps(值, ensure_ascii=False)}\n"
            else:
                內容 += f"- **{鍵}**: {值}\n"
        內容 += "\n"

    內容 += f"""
---

## 💡 可改進項目

"""
    for 評估 in 評估數據['assessments']:
        if 評估['score'] < 8.0:
            內容 += f"- **{評估['category']}** (得分: {評估['score']}): 建議檢查相關配置\n"

    if 評估數據['total_score'] >= 8.0:
        內容 += "- 系統整體狀態良好，繼續保持\n"

    內容 += f"""
---

## 🕐 執行時間表

- 每日 22:30 自動執行 (Cron)
- 手動執行: `python3 自動化評估.py`

---

*由龍魂自動化評估引擎生成*
*DNA: {評估數據['dna']}*
"""

    寫入文本(路徑, 內容)
    記錄日誌(f"📝 Markdown總結已生成: {路徑}")
    return 路徑


def 生成周報() -> Optional[Path]:
    """基於最近7天的評估數據生成周報"""
    確保目錄(配置["報告目錄"])

    # 查找最近7天的JSON報告
    模式 = str(配置["評估目錄"] / "local_assessment_*.json")
    所有報告 = sorted(glob.glob(模式), reverse=True)

    if not 所有報告:
        記錄日誌("⚠️ 沒有找到歷史評估報告，跳過周報生成")
        return None

    # 取最近7份報告
    最近報告 = 所有報告[:7]
    週數據 = []

    for 報告路徑 in 最近報告:
        try:
            with open(報告路徑, 'r', encoding='utf-8') as 文件:
                數據 = json.load(文件)
                週數據.append({
                    "日期": 數據.get("date", "未知"),
                    "總分": 數據.get("total_score", 0),
                    "狀態": 數據.get("status", "未知"),
                })
        except:
            continue

    if not 週數據:
        return None

    # 計算統計
    平均分 = round(sum(d["總分"] for d in 週數據) / len(週數據), 2)
    最高分 = max(d["總分"] for d in 週數據)
    最低分 = min(d["總分"] for d in 週數據)

    報告日期 = datetime.date.today().isoformat()
    文件名 = f"WEEKLY_REPORT_{報告日期}.md"
    路徑 = 配置["報告目錄"] / 文件名

    內容 = f"""# 🐉 龍魂系統週報 - {報告日期}

**DNA**: {配置['DNA標記']}
**生成時間**: {獲取時間戳()}

---

## 📈 本週評分趨勢

| 日期 | 總分 | 狀態 |
|------|------|------|
"""
    for 日數據 in reversed(週數據):
        內容 += f"| {日數據['日期']} | {日數據['總分']} | {日數據['狀態']} |\n"

    內容 += f"""
---

## 📊 統計摘要

| 指標 | 數值 |
|------|------|
| 平均評分 | {平均分}/10 |
| 最高評分 | {最高分}/10 |
| 最低評分 | {最低分}/10 |
| 評估次數 | {len(週數據)} |
| 系統狀態 | {"✅ 穩定" if 平均分 >= 8.0 else "🟡 需關注" if 平均分 >= 6.0 else "🔴 需改進"} |

---

## 🔔 趨勢分析

"""
    if len(週數據) >= 2:
        最新 = 週數據[0]["總分"]
        先前 = 週數據[-1]["總分"]
        變化 = round(最新 - 先前, 2)
        if 變化 > 0:
            內容 += f"- 📈 評分上升 {變化} 分（相比7天前）\n"
        elif 變化 < 0:
            內容 += f"- 📉 評分下降 {abs(變化)} 分（相比7天前）\n"
        else:
            內容 += "- ➡️ 評分持平\n"

    內容 += f"""
---

## 📅 下週建議

1. 繼續監控系統健康狀況
2. 及時修復低分維度問題
3. 保持定期備份

---

*由龍魂自動化周報引擎生成*
"""

    寫入文本(路徑, 內容)
    記錄日誌(f"📊 週報已生成: {路徑}")
    return 路徑


# ═══════════════════════════════════════════════════════════
# Cron配置
# ═══════════════════════════════════════════════════════════

def 生成Cron腳本() -> Path:
    """生成Cron執行腳本"""
    腳本路徑 = 配置["系統目錄"] / "longhun_daily_assessment.sh"
    確保目錄(腳本路徑.parent)

    腳本內容 = f"""#!/bin/bash
# 🐉 龍魂系統·自動化日評估 Cron 腳本
# DNA: {配置['DNA標記']}
# 執行時間: 每天 22:30

LOG_DIR="$HOME/.龍魂/assessments/logs"
REPORT_DIR="$HOME/.龍魂/reports"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE=$(date '+%Y%m%d')

# 確保目錄存在
mkdir -p "$LOG_DIR"
mkdir -p "$REPORT_DIR"

echo "════════════════════════════════════════════════════════════" >> "$LOG_DIR/cron_assessment_$DATE.log"
echo "🐉 龍魂系統·自動化日評估 (Cron)" >> "$LOG_DIR/cron_assessment_$DATE.log"
echo "時間: $TIMESTAMP" >> "$LOG_DIR/cron_assessment_$DATE.log"
echo "════════════════════════════════════════════════════════════" >> "$LOG_DIR/cron_assessment_$DATE.log"

# 執行評估
python3 "$HOME/longhun-system/scripts/自動化評估.py" --cron >> "$LOG_DIR/cron_assessment_$DATE.log" 2>&1

# 檢查執行結果
if [ $? -eq 0 ]; then
    echo "✅ 評估成功完成 $TIMESTAMP" >> "$LOG_DIR/cron_assessment_$DATE.log"
else
    echo "❌ 評估失敗 $TIMESTAMP" >> "$LOG_DIR/cron_assessment_$DATE.log"
fi

echo "" >> "$LOG_DIR/cron_assessment_$DATE.log"
"""

    寫入文本(腳本路徑, 腳本內容)
    os.chmod(腳本路徑, 0o755)
    記錄日誌(f"⏰ Cron腳本已生成: {腳本路徑}")
    return 腳本路徑


def 生成Cron配置() -> str:
    """生成Cron任務配置"""
    Cron線 = f"30 22 * * * /bin/bash {配置['系統目錄']}/longhun_daily_assessment.sh"
    return Cron線


def 安裝Cron任務() -> bool:
    """安裝Cron定時任務"""
    try:
        # 先獲取現有crontab
        結果 = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True
        )
        現有Cron = 結果.stdout if 結果.returncode == 0 else ""

        # 檢查是否已存在
        if "longhun_daily_assessment" in 現有Cron:
            記錄日誌("⏰ Cron任務已存在，跳過安裝")
            return True

        # 生成新crontab
        新任務 = 生成Cron配置()
        新Cron = 現有Cron.rstrip() + f"\n\n# 🐉 龍魂系統自動化日評估\n# DNA: {配置['DNA標記']}\n新任務\n"

        # 寫入crontab
        進程 = subprocess.Popen(
            ["crontab", "-"],
            stdin=subprocess.PIPE,
            text=True
        )
        進程.communicate(input=新Cron)

        if 進程.returncode == 0:
            記錄日誌("✅ Cron任務安裝成功 (每天 22:30)")
            return True
        else:
            記錄日誌("❌ Cron任務安裝失敗")
            return False

    except Exception as 錯誤:
        記錄日誌(f"❌ Cron安裝異常: {錯誤}")
        return False


# ═══════════════════════════════════════════════════════════
# 狀態檢查工具
# ═══════════════════════════════════════════════════════════

def 檢查狀態() -> Dict[str, Any]:
    """快速檢查評估系統狀態"""
    狀態 = {
        "時間戳": 獲取時間戳(),
        "目錄狀態": {},
        "最新報告": None,
        "Cron狀態": False,
        "總體健康": False,
    }

    # 檢查目錄
    for 名稱, 路徑 in {
        "龍魂目錄": 配置["龍魂目錄"],
        "評估目錄": 配置["評估目錄"],
        "日誌目錄": 配置["日誌目錄"],
        "報告目錄": 配置["報告目錄"],
    }.items():
        狀態["目錄狀態"][名稱] = {
            "存在": 路徑.exists(),
            "路徑": str(路徑),
        }

    # 查找最新報告
    模式 = str(配置["評估目錄"] / "local_assessment_*.json")
    報告列表 = sorted(glob.glob(模式), reverse=True)
    if 報告列表:
        try:
            with open(報告列表[0], 'r', encoding='utf-8') as 文件:
                最新報告 = json.load(文件)
                狀態["最新報告"] = {
                    "路徑": 報告列表[0],
                    "日期": 最新報告.get("date", "未知"),
                    "總分": 最新報告.get("total_score", 0),
                    "狀態": 最新報告.get("status", "未知"),
                }
        except:
            pass

    # 檢查Cron
    try:
        結果 = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        狀態["Cron狀態"] = "longhun_daily_assessment" in 結果.stdout
    except:
        狀態["Cron狀態"] = False

    # 評估總體健康
    所有目錄就緒 = all(d["存在"] for d in 狀態["目錄狀態"].values())
    有報告 = 狀態["最新報告"] is not None
    狀態["總體健康"] = 所有目錄就緒 and 有報告

    return 狀態


def 打印狀態報告() -> None:
    """打印格式化的狀態報告"""
    狀態 = 檢查狀態()

    print("\n" + "═" * 60)
    print("🐉 龍魂系統 · 自動化評估狀態檢查")
    print(f"時間: {狀態['時間戳']}")
    print("═" * 60)

    print("\n📁 目錄狀態:")
    for 名稱, 信息 in 狀態["目錄狀態"].items():
        圖標 = "✅" if 信息["存在"] else "❌"
        print(f"  {圖標} {名稱}: {信息['路徑']}")

    print("\n📊 最新報告:")
    if 狀態["最新報告"]:
        報告 = 狀態["最新報告"]
        print(f"  📄 {報告['路徑']}")
        print(f"  📅 日期: {報告['日期']}")
        print(f"  📈 評分: {報告['總分']}/10")
        print(f"  🏷️ 狀態: {報告['狀態']}")
    else:
        print("  ⚠️ 尚未生成評估報告")

    print(f"\n⏰ Cron任務: {'✅ 已配置' if 狀態['Cron狀態'] else '❌ 未配置'}")
    print(f"🩺 總體健康: {'✅ 正常' if 狀態['總體健康'] else '⚠️ 需關注'}")
    print("═" * 60 + "\n")


# ═══════════════════════════════════════════════════════════
# 趨勢分析
# ═══════════════════════════════════════════════════════════

def 分析歷史趨勢(天數: int = 30) -> Dict[str, Any]:
    """分析歷史評分趨勢"""
    模式 = str(配置["評估目錄"] / "local_assessment_*.json")
    所有報告 = sorted(glob.glob(模式))

    if not 所有報告:
        return {"錯誤": "沒有歷史數據"}

    # 取最近N天
    最近報告 = 所有報告[-天數:]
    趨勢數據 = []

    for 報告路徑 in 最近報告:
        try:
            with open(報告路徑, 'r', encoding='utf-8') as 文件:
                數據 = json.load(文件)
                趨勢數據.append({
                    "日期": 數據.get("date", "未知"),
                    "總分": 數據.get("total_score", 0),
                })
        except:
            continue

    if not 趨勢數據:
        return {"錯誤": "無法解析歷史數據"}

    評分列表 = [d["總分"] for d in 趨勢數據]

    return {
        "數據點": len(趨勢數據),
        "平均評分": round(sum(評分列表) / len(評分列表), 2),
        "最高評分": max(評分列表),
        "最低評分": min(評分列表),
        "最新評分": 評分列表[-1] if 評分列表 else 0,
        "趨勢": "上升" if len(評分列表) >= 2 and 評分列表[-1] > 評分列表[0] else "下降" if len(評分列表) >= 2 and 評分列表[-1] < 評分列表[0] else "持平",
        "歷史數據": 趨勢數據,
    }


# ═══════════════════════════════════════════════════════════
# 主函數
# ═══════════════════════════════════════════════════════════

def 主函數():
    """主入口函數"""
    import argparse
    解析器 = argparse.ArgumentParser(description="龍魂自動化日評估引擎")
    解析器.add_argument("--cron", action="store_true", help="Cron模式（靜默執行）")
    解析器.add_argument("--status", action="store_true", help="顯示狀態報告")
    解析器.add_argument("--weekly", action="store_true", help="生成周報")
    解析器.add_argument("--trend", type=int, metavar="N", help="分析N天趨勢")
    解析器.add_argument("--install-cron", action="store_true", help="安裝Cron任務")
    解析器.add_argument("--setup", action="store_true", help="完整設置（目錄+Cron）")
    參數 = 解析器.parse_args()

    if 參數.status:
        打印狀態報告()
        return

    if 參數.trend:
        趨勢 = 分析歷史趨勢(參數.trend)
        print(json.dumps(趨勢, ensure_ascii=False, indent=2))
        return

    if 參數.setup:
        記錄日誌("🔧 開始完整設置...")
        確保目錄(配置["龍魂目錄"])
        確保目錄(配置["評估目錄"])
        確保目錄(配置["日誌目錄"])
        確保目錄(配置["報告目錄"])
        確保目錄(配置["系統目錄"])
        生成Cron腳本()
        安裝Cron任務()
        記錄日誌("✅ 設置完成")
        return

    if 參數.install_cron:
        生成Cron腳本()
        安裝Cron任務()
        return

    if 參數.weekly:
        生成周報()
        return

    # 執行全面評估
    評估數據 = 執行全面評估()

    # 生成報告
    生成JSON報告(評估數據)
    生成Markdown總結(評估數據)

    # 如果是周日，生成周報
    if datetime.date.today().weekday() == 6:  # 6 = Sunday
        記錄日誌("📊 今天是周日，生成週報...")
        生成周報()

    # 如果是月初，生成趨勢報告
    if datetime.date.today().day == 1:
        記錄日誌("📈 月初趨勢分析...")
        趨勢 = 分析歷史趨勢(30)
        趨勢路徑 = 配置["報告目錄"] / f"TREND_{獲取今日日期()}.json"
        寫入JSON(趨勢路徑, 趨勢)
        記錄日誌(f"📈 趨勢報告已保存: {趨勢路徑}")

    記錄日誌(f"\n✅ 評估完成")
    記錄日誌(f"評分: {評估數據['total_score']}/10 | 狀態: {評估數據['status']}")
    記錄日誌(f"DNA: {評估數據['dna']}")


if __name__ == "__main__":
    主函數()
