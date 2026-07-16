#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂每日復盤引擎
DNA: #龍芯⚡️2026-06-19-LONGHUN-REVIEW-v5.1
功能: 三色審計 · 郵件發送 · 復盤報告生成 · 歷史趨勢追蹤 · 改進建議生成
"""

import os
import sys
import json
import glob
import smtplib
import subprocess
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dataclasses import dataclass, asdict

# ═══════════════════════════════════════════════════════════
# 全局配置
# ═══════════════════════════════════════════════════════════

配置 = {
    "龍魂目錄": Path.home() / ".龍魂",
    "系統目錄": Path.home() / "longhun-system",
    "復盤目錄": Path.home() / ".龍魂" / "reviews",
    "日誌目錄": Path.home() / ".龍魂" / "reviews" / "logs",
    "報告目錄": Path.home() / ".龍魂" / "reports",
    "評估目錄": Path.home() / ".龍魂" / "assessments",
    "XPAY目錄": Path.home() / ".龍魂" / "xpay",
    "郵件發件人": os.environ.get("LONGHUN_GMAIL", ""),
    "郵件密碼": os.environ.get("LONGHUN_GMAIL_APPPW", ""),
    "郵件收件人": os.environ.get("LONGHUN_EMAIL_TO", ""),
    "SMTP服務器": "smtp.gmail.com",
    "SMTP端口": 587,
    "DNA標記": "#龍芯⚡️2026-06-19-LONGHUN-REVIEW-v5.1",
}

# ═══════════════════════════════════════════════════════════
# 數據類
# ═══════════════════════════════════════════════════════════

@dataclass
class 三色結果:
    """三色審計結果: 🟢通過 🟡警告 🔴失敗"""
    顏色: str  # 🟢 🟡 🔴
    狀態: str  # 通過/警告/失敗
    詳情: str
    分值: float = 0.0  # 0-10


@dataclass
class 復盤日誌:
    """單條復盤日誌記錄"""
    時間: str
    類別: str
    三色: str
    信息: str


# ═══════════════════════════════════════════════════════════
# 工具函數
# ═══════════════════════════════════════════════════════════

def 獲取時間戳() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def 獲取日期標記() -> str:
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def 獲取今日日期() -> str:
    return datetime.date.today().isoformat()


def 確保目錄(目錄: Path) -> None:
    目錄.mkdir(parents=True, exist_ok=True)


def 寫入JSON(路徑: Path, 數據: Any) -> None:
    with open(路徑, 'w', encoding='utf-8') as 文件:
        if isinstance(數據, dict) or isinstance(數據, list):
            json.dump(數據, 文件, ensure_ascii=False, indent=2, default=str)
        else:
            json.dump(asdict(數據) if hasattr(數據, '__dataclass_fields__') else 數據, 文件, ensure_ascii=False, indent=2, default=str)


def 寫入文本(路徑: Path, 內容: str) -> None:
    with open(路徑, 'w', encoding='utf-8') as 文件:
        文件.write(內容)


def 讀取文本(路徑: Path) -> str:
    try:
        with open(路徑, 'r', encoding='utf-8') as 文件:
            return 文件.read()
    except:
        return ""


def 讀取JSONL(路徑: Path) -> List[Dict]:
    """讀取JSON Lines格式文件"""
    記錄 = []
    if not 路徑.exists():
        return 記錄
    try:
        with open(路徑, 'r', encoding='utf-8') as 文件:
            for 行 in 文件:
                行 = 行.strip()
                if 行:
                    try:
                        記錄.append(json.loads(行))
                    except:
                        pass
    except:
        pass
    return 記錄


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


def 記錄日誌(信息: str) -> None:
    確保目錄(配置["日誌目錄"])
    時間戳 = 獲取時間戳()
    日誌文件 = 配置["日誌目錄"] / f"daily_review_{datetime.date.today().isoformat()}.log"
    with open(日誌文件, 'a', encoding='utf-8') as 文件:
        文件.write(f"[{時間戳}] {信息}\n")
    print(f"[{時間戳}] {信息}")


# ═══════════════════════════════════════════════════════════
# 三色審計核心
# ═══════════════════════════════════════════════════════════

def 審計_文件完整性() -> 三色結果:
    """檢查核心文件完整性"""
    核心文件 = [
        配置["XPAY目錄"] / "xpay_cli.py",
        配置["XPAY目錄"] / "xpay_core.py",
        配置["XPAY目錄"] / "xpay_db.py",
        配置["XPAY目錄"] / "startup.sh",
    ]

    存在數 = sum(1 for f in 核心文件 if f.exists())
    總數 = len(核心文件)

    if 存在數 == 總數:
        return 三色結果("🟢", "通過", f"核心文件齊 {存在數}/{總數}", 10.0)
    elif 存在數 >= 總數 // 2:
        return 三色結果("🟡", "警告", f"核心文件缺失 {總數 - 存在數} 個", 5.0)
    else:
        return 三色結果("🔴", "失敗", f"核心文件嚴重缺失 {存在數}/{總數}", 2.0)


def 審計_安全性() -> 三色結果:
    """安全審計: pip-audit 檢查"""
    返回碼, 輸出, 錯誤 = 執行命令(["pip-audit", "--format=json"], 超時=60)

    if 返回碼 != 0:
        # pip-audit 未安裝或執行失敗
        return 三色結果("🟡", "警告", "pip-audit 未安裝或執行失敗", 5.0)

    try:
        漏洞 = json.loads(輸出) if 輸出 else []
        嚴重數 = sum(1 for v in 漏洞 if v.get("severity") in ["critical", "high"])
        中度數 = sum(1 for v in 漏洞 if v.get("severity") == "moderate")

        if 嚴重數 > 0:
            return 三色結果("🔴", "失敗", f"發現 {嚴重數} 個嚴重漏洞", 3.0)
        elif 中度數 > 0:
            return 三色結果("🟡", "警告", f"發現 {中度數} 個中度漏洞", 6.0)
        else:
            return 三色結果("🟢", "通過", "無 critical/high 漏洞", 10.0)
    except:
        return 三色結果("🟡", "警告", "無法解析pip-audit輸出", 5.0)


def 審計_系統心跳() -> 三色結果:
    """檢查系統心跳 (KFPP DB記錄數)"""
    DB路徑 = 配置["XPAY目錄"] / "xpay.db"
    if not DB路徑.exists():
        return 三色結果("🟡", "警告", "數據庫不存在", 3.0)

    try:
        返回碼, 輸出, _ = 執行命令(
            ["python3", str(配置["XPAY目錄"] / "xpay_cli.py"), "stats"],
            超時=10
        )
        if 返回碼 == 0:
            行數 = 0
            for 行 in 輸出.split("\n"):
                if "record" in 行.lower() or "row" in 行.lower() or "transaction" in 行.lower():
                    try:
                        行數 = int(''.join(c for c in 行 if c.isdigit()))
                    except:
                        pass
            if 行數 > 0:
                return 三色結果("🟢", "通過", f"今日心跳 {行數} 行", 10.0)
            else:
                return 三色結果("🟡", "警告", "數據庫無記錄", 5.0)
        else:
            return 三色結果("🟡", "警告", "無法獲取數據庫統計", 4.0)
    except Exception as 錯誤:
        return 三色結果("🟡", "警告", f"心跳檢查異常: {錯誤}", 4.0)


def 審計_測試狀態() -> 三色結果:
    """檢查 pytest 測試狀態"""
    測試目錄 = 配置["系統目錄"] / "tests"
    if not 測試目錄.exists():
        return 三色結果("🟡", "警告", "測試目錄不存在", 5.0)

    返回碼, 輸出, 錯誤 = 執行命令(
        ["pytest", str(測試目錄), "-v", "--tb=short", "-q"],
        超時=60
    )

    if 返回碼 == 0:
        return 三色結果("🟢", "通過", "pytest 通過", 10.0)
    elif 返回碼 == 5:
        return 三色結果("🟡", "警告", "pytest 未發現測試", 5.0)
    else:
        # 解析失敗數
        失敗數 = 0
        for 行 in 輸出.split("\n"):
            if "failed" in 行.lower():
                try:
                    失敗數 = int(''.join(c for c in 行.split("failed")[0].split()[-1] if c.isdigit()))
                except:
                    pass
        return 三色結果("🔴" if 失敗數 > 3 else "🟡", "警告" if 失敗數 <= 3 else "失敗",
                       f"pytest {失敗數} 個失敗", 4.0 if 失敗數 <= 3 else 2.0)


def 審計_操作日誌() -> 三色結果:
    """審計 action_log.jsonl 中今天的所有操作"""
    日誌文件 = 配置["系統目錄"] / "logs" / "action_log.jsonl"
    今日日期 = 獲取今日日期()
    操作數 = 0

    if not 日誌文件.exists():
        return 三色結果("🟡", "警告", "action_log.jsonl 不存在", 5.0)

    try:
        記錄列表 = 讀取JSONL(日誌文件)
        for 記錄 in 記錄列表:
            記錄日期 = 記錄.get("date", 記錄.get("timestamp", ""))[:10]
            if 記錄日期 == 今日日期:
                操作數 += 1

        if 操作數 > 0:
            return 三色結果("🟢", "通過", f"今日操作 {操作數} 筆", 10.0)
        else:
            return 三色結果("🟡", "警告", "今日無操作記錄", 5.0)
    except Exception as 錯誤:
        return 三色結果("🟡", "警告", f"日誌審計失敗: {錯誤}", 4.0)


def 審計_評估報告() -> 三色結果:
    """檢查今日評估報告是否已生成"""
    模式 = str(配置["評估目錄"] / f"local_assessment_{獲取今日日期().replace('-', '')}*.json")
    報告列表 = glob.glob(模式)

    if 報告列表:
        try:
            with open(報告列表[0], 'r', encoding='utf-8') as 文件:
                數據 = json.load(文件)
                評分 = 數據.get("total_score", 0)
                狀態 = 數據.get("status", "")
                return 三色結果("🟢", "通過", f"評估完成 評分:{評分}/10 {狀態}", min(10.0, 評分))
        except:
            return 三色結果("🟢", "通過", f"評估報告已生成 ({len(報告列表)}份)", 8.0)
    else:
        return 三色結果("🟡", "警告", "今日評估報告尚未生成", 4.0)


def 審計_API服務() -> 三色結果:
    """檢查API服務健康狀態"""
    服務列表 = [
        ("http://localhost:8443/kimi/health", "Kimi"),
        ("http://localhost:8080/health", "通用"),
    ]

    健康數 = 0
    檢查數 = 0
    for 地址, 名稱 in 服務列表:
        try:
            返回碼, _, _ = 執行命令(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 地址], 超時=5)
            if 返回碼 == 0:
                健康數 += 1
            檢查數 += 1
        except:
            檢查數 += 1

    if 檢查數 == 0:
        return 三色結果("🟡", "警告", "無API服務可檢查", 5.0)

    if 健康數 == 檢查數:
        return 三色結果("🟢", "通過", f"API服務正常 {健康數}/{檢查數}", 10.0)
    elif 健康數 > 0:
        return 三色結果("🟡", "警告", f"API服務部分異常 {健康數}/{檢查數}", 5.0)
    else:
        return 三色結果("🔴", "失敗", "API服務全部異常", 2.0)


def 審計_備份狀態() -> 三色結果:
    """檢查備份狀態"""
    備份目錄 = 配置["龍魂目錄"] / "backups"
    if not 備份目錄.exists():
        return 三色結果("🟡", "警告", "備份目錄不存在", 3.0)

    今日日期 = 獲取今日日期()
    備份文件 = list(備份目錄.glob("*"))
    今日備份 = [f for f in 備份文件 if 今日日期.replace("-", "") in f.name]

    if 今日備份:
        return 三色結果("🟢", "通過", f"今日備份已完成 ({len(今日備份)}個)", 10.0)
    elif 備份文件:
        最新備份 = max(備份文件, key=lambda f: f.stat().st_mtime)
        修改時間 = datetime.datetime.fromtimestamp(最新備份.stat().st_mtime)
        return 三色結果("🟡", "警告", f"最近備份: {修改時間.strftime('%Y-%m-%d')}", 6.0)
    else:
        return 三色結果("🔴", "失敗", "無備份文件", 2.0)


# ═══════════════════════════════════════════════════════════
# 復盤報告生成
# ═══════════════════════════════════════════════════════════

def 執行全面復盤() -> Dict:
    """執行完整的三色審計復盤"""
    記錄日誌("════════════════════════════════════════════════════════════")
    記錄日誌("🐉 龍魂系統 · 每日復盤")
    記錄日誌(f"時間: {獲取時間戳()}")
    記錄日誌("════════════════════════════════════════════════════════════")

    # 執行所有審計
    審計項目 = {
        "文件完整": 審計_文件完整性(),
        "安全(魯班)": 審計_安全性(),
        "系統心跳": 審計_系統心跳(),
        "測試": 審計_測試狀態(),
        "操作日誌": 審計_操作日誌(),
        "評估報告": 審計_評估報告(),
        "API服務": 審計_API服務(),
        "備份狀態": 審計_備份狀態(),
    }

    # 計算三色總評
    通過數 = sum(1 for r in 審計項目.values() if r.顏色 == "🟢")
    警告數 = sum(1 for r in 審計項目.values() if r.顏色 == "🟡")
    失敗數 = sum(1 for r in 審計項目.values() if r.顏色 == "🔴")
    總數 = len(審計項目)

    if 失敗數 > 0:
        三色總評 = "🔴"
        總評狀態 = "需立即關注"
    elif 警告數 > 總數 // 3:
        三色總評 = "🟡"
        總評狀態 = "需改進"
    else:
        三色總評 = "🟢"
        總評狀態 = "正常"

    # 計算綜合評分
    平均分 = round(sum(r.分值 for r in 審計項目.values()) / len(審計項目), 2) if 審計項目 else 0

    記錄日誌(f"\n{'═' * 60}")
    記錄日誌(f"三色總評: {三色總評} ({總評狀態})")
    記錄日誌(f"綜合評分: {平均分}/10")
    記錄日誌(f"🟢 {通過數} | 🟡 {警告數} | 🔴 {失敗數}")
    記錄日誌(f"{'═' * 60}")

    # 序列化審計結果
    審計數據 = {}
    for 名稱, 結果 in 審計項目.items():
        審計數據[名稱] = {
            "顏色": 結果.顏色,
            "狀態": 結果.狀態,
            "詳情": 結果.詳情,
            "分值": 結果.分值,
        }
        記錄日誌(f"  {結果.顏色} {名稱}: {結果.詳情}")

    return {
        "三色總評": 三色總評,
        "總評狀態": 總評狀態,
        "綜合評分": 平均分,
        "通過數": 通過數,
        "警告數": 警告數,
        "失敗數": 失敗數,
        "時間戳": 獲取時間戳(),
        "日期": 獲取今日日期(),
        "dna": 配置["DNA標記"],
        "審計結果": 審計數據,
    }


def 生成改進建議(復盤數據: Dict) -> List[str]:
    """基於復盤結果生成改進建議"""
    建議 = []
    審計 = 復盤數據.get("審計結果", {})

    for 名稱, 結果 in 審計.items():
        顏色 = 結果.get("顏色", "")
        詳情 = 結果.get("詳情", "")

        if 顏色 == "🔴":
            if 名稱 == "文件完整":
                建議.append("🔴 [緊急] 核心文件缺失，請檢查XPAY系統完整性")
            elif 名稱 == "安全(魯班)":
                建議.append("🔴 [緊急] 發現嚴重安全漏洞，請立即執行 pip-audit --fix")
            elif 名稱 == "測試":
                建議.append("🔴 [重要] 測試失敗較多，請檢查代碼質量")
            elif 名稱 == "API服務":
                建議.append("🔴 [重要] API服務異常，請檢查服務狀態")
            elif 名稱 == "備份狀態":
                建議.append("🔴 [重要] 無備份文件，請建立備份策略")
            else:
                建議.append(f"🔴 [{名稱}] {詳情}")

        elif 顏色 == "🟡":
            if 名稱 == "操作日誌":
                建議.append("🟡 今日無操作記錄，確認是否正常工作")
            elif 名稱 == "評估報告":
                建議.append("🟡 今日評估報告尚未生成，請檢查自動化任務")
            elif 名稱 == "系統心跳":
                建議.append("🟡 數據庫記錄異常，請檢查系統狀態")
            else:
                建議.append(f"🟡 [{名稱}] {詳情}")

    if not 建議:
        建議.append("✅ 所有檢查項通過，系統運行良好")

    return 建議


def 生成復盤報告(復盤數據: Dict) -> Path:
    """生成復盤報告文件"""
    確保目錄(配置["復盤目錄"])

    # JSON報告
    JSON路徑 = 配置["復盤目錄"] / f"daily_review_{獲取日期標記()}.json"
    寫入JSON(JSON路徑, 復盤數據)
    記錄日誌(f"📄 JSON復盤報告: {JSON路徑}")

    # Markdown報告
    MD路徑 = 配置["復盤目錄"] / f"daily_review_{獲取今日日期()}.md"
    改進建議 = 生成改進建議(復盤數據)

    內容 = f"""# 🐉 龍魂每日復盤

**時間**: {復盤數據['時間戳']}
**日期**: {復盤數據['日期']}
**DNA**: {復盤數據['dna']}

---

## 🚦 三色總評

| 指標 | 數值 |
|------|------|
| **三色總評** | {復盤數據['三色總評']} {復盤數據['總評狀態']} |
| **綜合評分** | {復盤數據['綜合評分']}/10 |
| 🟢 通過 | {復盤數據['通過數']} |
| 🟡 警告 | {復盤數據['警告數']} |
| 🔴 失敗 | {復盤數據['失敗數']} |

---

## 🔍 詳細審計

| 審計項 | 結果 | 狀態 | 詳情 |
|--------|------|------|------|
"""

    for 名稱, 結果 in 復盤數據['審計結果'].items():
        內容 += f"| {名稱} | {結果['顏色']} | {結果['狀態']} | {結果['詳情']} |\n"

    內容 += f"""
---

## 💡 改進建議

"""
    for 建議 in 改進建議:
        內容 += f"- {建議}\n"

    內容 += f"""
---

## 📊 歷史對比

"""

    # 查找歷史數據
    歷史 = 獲取歷史趨勢(7)
    if 歷史 and "錯誤" not in 歷史:
        內容 += "| 日期 | 綜合評分 | 三色評級 |\n"
        內容 += "|------|----------|----------|\n"
        for 日 in 歷史.get("歷史數據", [])[-7:]:
            內容 += f"| {日['日期']} | {日['綜合評分']} | {日['三色總評']} |\n"
    else:
        內容 += "暫無歷史數據\n"

    內容 += f"""
---

*由龍魂每日復盤引擎生成*
*DNA: {復盤數據['dna']}*
"""

    寫入文本(MD路徑, 內容)
    記錄日誌(f"📝 Markdown復盤報告: {MD路徑}")

    return MD路徑


# ═══════════════════════════════════════════════════════════
# 郵件發送
# ═══════════════════════════════════════════════════════════

def 發送復盤郵件(復盤數據: Dict) -> bool:
    """發送復盤報告郵件"""
    發件人 = 配置["郵件發件人"]
    密碼 = 配置["郵件密碼"]
    收件人 = 配置["郵件收件人"] or 發件人

    if not 發件人 or not 密碼:
        記錄日誌("⚠️ 郵件配置不完整，跳過郵件發送")
        記錄日誌("  請設置 LONGHUN_GMAIL 和 LONGHUN_GMAIL_APPPW 環境變量")
        return False

    try:
        改進建議 = 生成改進建議(復盤數據)

        # 構建郵件內容
        主題 = f"龍魂每日復盤 {復盤數據['日期']} {復盤數據['三色總評']}"

        正文 = f"""龍魂每日復盤 {復盤數據['日期']}

═══════════════════════════════════════
三色總評: {復盤數據['三色總評']} {復盤數據['總評狀態']}
綜合評分: {復盤數據['綜合評分']}/10
═══════════════════════════════════════

詳細檢查項:
"""
        for 名稱, 結果 in 復盤數據['審計結果'].items():
            正文 += f"\n  {結果['顏色']} {名稱}: {結果['詳情']}"

        正文 += "\n\n改進建議:\n"
        for 建議 in 改進建議:
            正文 += f"\n  {建議}"

        正文 += f"""

---
{復盤數據['dna']}
"""

        # 創建郵件
        郵件 = MIMEMultipart()
        郵件["From"] = 發件人
        郵件["To"] = 收件人
        郵件["Subject"] = 主題
        郵件.attach(MIMEText(正文, "plain", "utf-8"))

        # 發送郵件
        with smtplib.SMTP(配置["SMTP服務器"], 配置["SMTP端口"]) as 服務器:
            服務器.starttls()
            服務器.login(發件人, 密碼)
            服務器.send_message(郵件)

        記錄日誌(f"📧 復盤郵件已發送至 {收件人}")
        return True

    except Exception as 錯誤:
        記錄日誌(f"❌ 郵件發送失敗: {錯誤}")
        return False


# ═══════════════════════════════════════════════════════════
# 歷史趨勢追蹤
# ═══════════════════════════════════════════════════════════

def 獲取歷史趨勢(天數: int = 30) -> Dict:
    """獲取歷史復盤趨勢數據"""
    模式 = str(配置["復盤目錄"] / "daily_review_*.json")
    報告列表 = sorted(glob.glob(模式))

    if not 報告列表:
        return {"錯誤": "沒有歷史復盤數據"}

    最近報告 = 報告列表[-天數:]
    趨勢數據 = []

    for 報告路徑 in 最近報告:
        try:
            with open(報告路徑, 'r', encoding='utf-8') as 文件:
                數據 = json.load(文件)
                趨勢數據.append({
                    "日期": 數據.get("日期", "未知"),
                    "綜合評分": 數據.get("綜合評分", 0),
                    "三色總評": 數據.get("三色總評", "⚪"),
                    "通過數": 數據.get("通過數", 0),
                    "警告數": 數據.get("警告數", 0),
                    "失敗數": 數據.get("失敗數", 0),
                })
        except:
            continue

    if not 趨勢數據:
        return {"錯誤": "無法解析歷史數據"}

    評分列表 = [d["綜合評分"] for d in 趨勢數據]

    return {
        "數據點": len(趨勢數據),
        "平均評分": round(sum(評分列表) / len(評分列表), 2),
        "最高評分": max(評分列表),
        "最低評分": min(評分列表),
        "最新評分": 評分列表[-1],
        "趨勢": "上升" if len(評分列表) >= 2 and 評分列表[-1] > 評分列表[0] else "下降" if len(評分列表) >= 2 and 評分列表[-1] < 評分列表[0] else "持平",
        "歷史數據": 趨勢數據,
    }


def 生成趨勢報告(天數: int = 30) -> Path:
    """生成趨勢分析報告"""
    確保目錄(配置["報告目錄"])

    趨勢 = 獲取歷史趨勢(天數)
    if "錯誤" in 趨勢:
        記錄日誌(f"⚠️ {趨勢['錯誤']}")
        return None

    報告日期 = 獲取今日日期()
    文件名 = f"REVIEW_TREND_{報告日期}.md"
    路徑 = 配置["報告目錄"] / 文件名

    內容 = f"""# 🐉 龍魂復盤趨勢報告 - {報告日期}

**DNA**: {配置['DNA標記']}
**統計週期**: 最近{天數}天

---

## 📈 趨勢摘要

| 指標 | 數值 |
|------|------|
| 平均評分 | {趨勢['平均評分']}/10 |
| 最高評分 | {趨勢['最高評分']}/10 |
| 最低評分 | {趨勢['最低評分']}/10 |
| 最新評分 | {趨勢['最新評分']}/10 |
| 趨勢方向 | {趨勢['趨勢']} |
| 數據點 | {趨勢['數據點']} |

---

## 📊 歷史數據

| 日期 | 評分 | 三色 | 🟢 | 🟡 | 🔴 |
|------|------|------|----|----|----|
"""
    for 日 in 趨勢["歷史數據"]:
        內容 += f"| {日['日期']} | {日['綜合評分']} | {日['三色總評']} | {日['通過數']} | {日['警告數']} | {日['失敗數']} |\n"

    內容 += f"""
---

## 💡 分析建議

"""
    if 趨勢["趨勢"] == "上升":
        內容 += "- 📈 系統整體趨勢向好，繼續保持\n"
    elif 趨勢["趨勢"] == "下降":
        內容 += "- 📉 系統評分出現下降趨勢，需要關注\n"
        內容 += "- 建議檢查近期變更，找出評分下降原因\n"
    else:
        內容 += "- ➡️ 評分趨勢平穩\n"

    if 趨勢["平均評分"] >= 8.0:
        內容 += "- 系統整體運行良好\n"
    elif 趨勢["平均評分"] >= 6.0:
        內容 += "- 系統存在一些問題需要改進\n"
    else:
        內容 += "- 系統健康度較低，需要全面檢修\n"

    內容 += f"""
---

*由龍魂趨勢分析引擎生成*
"""

    寫入文本(路徑, 內容)
    記錄日誌(f"📈 趨勢報告已生成: {路徑}")
    return 路徑


# ═══════════════════════════════════════════════════════════
# 日曆寫入 (macOS)
# ═══════════════════════════════════════════════════════════

def 寫入日曆(復盤數據: Dict) -> bool:
    """將復盤結果寫入macOS日曆"""
    try:
        標題 = f"龍魂復盤 {復盤數據['三色總評']} 評分:{復盤數據['綜合評分']}"
        備註 = f"三色審計: 🟢{復盤數據['通過數']} 🟡{復盤數據['警告數']} 🔴{復盤數據['失敗數']}"

        AppleScript = f'''
        tell application "Calendar"
            set 目標日曆 to calendar "龍魂"
            tell 目標日曆
                make new event at end with properties {{
                    summary: "{標題}",
                    start date: (current date),
                    end date: (current date) + 300,
                    description: "{備註}\\n{配置['DNA標記']}"
                }}
            end tell
        end tell
        '''

        返回碼, _, 錯誤 = 執行命令(["osascript", "-e", AppleScript], 超時=10)
        if 返回碼 == 0:
            記錄日誌("📅 日曆事件已寫入")
            return True
        else:
            記錄日誌(f"⚠️ 日曆寫入失敗: {錯誤}")
            return False

    except Exception as 錯誤:
        記錄日誌(f"⚠️ 日曆功能僅支持macOS: {錯誤}")
        return False


# ═══════════════════════════════════════════════════════════
# 三色審計日誌分析
# ═══════════════════════════════════════════════════════════

def 分析三色審計日誌(日誌路徑: Optional[Path] = None) -> Dict:
    """分析三色審計日誌文件"""
    if 日誌路徑 is None:
        日誌路徑 = 配置["日誌目錄"] / f"daily_review_{獲取今日日期()}.log"

    if not 日誌路徑.exists():
        return {"錯誤": f"日誌文件不存在: {日誌路徑}"}

    分析結果 = {
        "日誌路徑": str(日誌路徑),
        "總行數": 0,
        "🟢通過數": 0,
        "🟡警告數": 0,
        "🔴失敗數": 0,
        "時間範圍": {"開始": "", "結束": ""},
    }

    try:
        with open(日誌路徑, 'r', encoding='utf-8') as 文件:
            行列表 = 文件.readlines()
            分析結果["總行數"] = len(行列表)

            for 行 in 行列表:
                if "🟢" in 行:
                    分析結果["🟢通過數"] += 1
                if "🟡" in 行:
                    分析結果["🟡警告數"] += 1
                if "🔴" in 行:
                    分析結果["🔴失敗數"] += 1

            if 行列表:
                第一行 = 行列表[0].strip()
                最後行 = 行列表[-1].strip()
                if "]" in 第一行:
                    分析結果["時間範圍"]["開始"] = 第一行.split("]")[0][1:]
                if "]" in 最後行:
                    分析結果["時間範圍"]["結束"] = 最後行.split("]")[0][1:]

        return 分析結果

    except Exception as 錯誤:
        return {"錯誤": f"分析失敗: {錯誤}"}


# ═══════════════════════════════════════════════════════════
# 設置與配置
# ═══════════════════════════════════════════════════════════

def 生成LaunchAgent配置() -> Path:
    """生成macOS LaunchAgent plist文件"""
    plist路徑 = Path.home() / "Library/LaunchAgents/com.longhun.daily-review.plist"
    確保目錄(plist路徑.parent)

    plist內容 = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.daily-review</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{配置['系統目錄']}/scripts/復盤引擎.py</string>
        <string>--cron</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>23</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>{配置['日誌目錄']}/launchd_review.log</string>

    <key>StandardErrorPath</key>
    <string>{配置['日誌目錄']}/launchd_review_error.log</string>
</dict>
</plist>
"""

    寫入文本(plist路徑, plist內容)
    記錄日誌(f"📋 LaunchAgent配置已生成: {plist路徑}")
    return plist路徑


def 安裝LaunchAgent() -> bool:
    """安裝LaunchAgent"""
    try:
        plist路徑 = 生成LaunchAgent配置()

        # 卸載舊的（如果存在）
        執行命令(["launchctl", "unload", str(plist路徑)], 超時=5)

        # 加載新的
        返回碼, _, 錯誤 = 執行命令(["launchctl", "load", str(plist路徑)], 超時=5)
        if 返回碼 == 0:
            記錄日誌("✅ LaunchAgent已安裝 (每天 23:30)")
            return True
        else:
            記錄日誌(f"❌ LaunchAgent安裝失敗: {錯誤}")
            return False

    except Exception as 錯誤:
        記錄日誌(f"⚠️ LaunchAgent僅支持macOS: {錯誤}")
        return False


def 完整設置() -> None:
    """執行完整設置"""
    記錄日誌("🔧 開始復盤引擎完整設置...")

    # 創建目錄
    確保目錄(配置["復盤目錄"])
    確保目錄(配置["日誌目錄"])
    確保目錄(配置["報告目錄"])

    # 生成配置
    生成LaunchAgent配置()

    記錄日誌("✅ 設置完成")
    記錄日誌("  目錄結構已創建")
    記錄日誌("  LaunchAgent配置已生成")
    記錄日誌("")
    記錄日誌("下一步:")
    記錄日誌("  1. 設置郵件環境變量: LONGHUN_GMAIL, LONGHUN_GMAIL_APPPW")
    記錄日誌("  2. 安裝依賴: pip3 install pip-audit pytest")
    記錄日誌("  3. 執行: python3 復盤引擎.py --install-agent")
    記錄日誌("  4. 測試: python3 復盤引擎.py")


# ═══════════════════════════════════════════════════════════
# 主函數
# ═══════════════════════════════════════════════════════════

def 主函數():
    """主入口函數"""
    import argparse
    解析器 = argparse.ArgumentParser(description="龍魂每日復盤引擎")
    解析器.add_argument("--cron", action="store_true", help="Cron模式（自動發送郵件）")
    解析器.add_argument("--status", action="store_true", help="顯示系統狀態")
    解析器.add_argument("--email", action="store_true", help="發送郵件報告")
    解析器.add_argument("--trend", type=int, metavar="N", default=0, help="生成N天趨勢報告")
    解析器.add_argument("--setup", action="store_true", help="完整設置")
    解析器.add_argument("--install-agent", action="store_true", help="安裝LaunchAgent")
    解析器.add_argument("--no-email", action="store_true", help="不發送郵件")
    解析器.add_argument("--analyze-logs", action="store_true", help="分析三色審計日誌")
    參數 = 解析器.parse_args()

    if 參數.setup:
        完整設置()
        return

    if 參數.install_agent:
        安裝LaunchAgent()
        return

    if 參數.status:
        狀態 = {
            "時間": 獲取時間戳(),
            "目錄就緒": (配置["復盤目錄"].exists() and 配置["日誌目錄"].exists()),
            "郵件配置": bool(配置["郵件發件人"] and 配置["郵件密碼"]),
            "今日日期": 獲取今日日期(),
        }
        print(json.dumps(狀態, ensure_ascii=False, indent=2))
        return

    if 參數.trend > 0:
        生成趨勢報告(參數.trend)
        return

    if 參數.analyze_logs:
        分析 = 分析三色審計日誌()
        print(json.dumps(分析, ensure_ascii=False, indent=2))
        return

    # 執行全面復盤
    復盤數據 = 執行全面復盤()

    # 生成報告
    生成復盤報告(復盤數據)

    # 發送郵件（默認發送，除非指定--no-email）
    if not 參數.no_email:
        if 參數.cron or 參數.email:
            發送復盤郵件(復盤數據)

    # 寫入日曆（僅macOS）
    if sys.platform == "darwin":
        寫入日曆(復盤數據)

    記錄日誌(f"\n✅ 復盤完成")
    記錄日誌(f"三色總評: {復盤數據['三色總評']} {復盤數據['總評狀態']}")
    記錄日誌(f"綜合評分: {復盤數據['綜合評分']}/10")
    記錄日誌(f"DNA: {復盤數據['dna']}")


if __name__ == "__main__":
    主函數()
