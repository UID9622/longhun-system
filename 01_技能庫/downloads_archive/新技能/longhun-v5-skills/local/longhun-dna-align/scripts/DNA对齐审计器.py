#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂DNA對齐審計器
DNA Alignment Auditor — 掃描·統計·重複檢測·完整性驗證

DNA: #龍芯⚡️2026-06-19-DNA-ALIGN-AUDITOR-v5.2
"""

import os
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import fnmatch

# ═══════════════════════════════════════════════════════
# 常量與配置
# ═══════════════════════════════════════════════════════

DNA正則模式 = re.compile(
    r'[\s"\']?#龍芯[\u26a1\ufe0f]*(\d{4}-\d{2}-\d{2})-(.+?)-v([\d.]+)'
)

DNA完整格式模式 = re.compile(
    r'^#龍芯[\u26a1\ufe0f]*\d{4}-\d{2}-\d{2}-[A-Z][A-Z0-9_-]*-v[\d.]+$'
)

忽略目錄模式 = {
    '__pycache__', '.git', 'node_modules', 'venv', '.venv',
    'env', '.env', '.pytest_cache', '.mypy_cache',
    'dist', 'build', '.eggs', '*.egg-info',
    '.agents', 'backups', '.龍魂'
}

忽略文件模式 = {
    '*.pyc', '*.pyo', '*.so', '*.dylib', '*.dll',
    '*.min.js', '*.min.css', '*.map',
    '.DS_Store', 'Thumbs.db', '.gitignore',
    '*.lock', '*.log', '*.tmp', '*.temp',
    '*.png', '*.jpg', '*.jpeg', '*.gif', '*.ico', '*.svg',
    '*.mp4', '*.mp3', '*.wav', '*.pdf', '*.zip', '*.tar.gz'
}

文件類型分類 = {
    '.py': 'Python腳本',
    '.md': 'Markdown文檔',
    '.sh': 'Shell腳本',
    '.json': 'JSON配置',
    '.yaml': 'YAML配置',
    '.yml': 'YAML配置',
    '.toml': 'TOML配置',
    '.txt': '文本文件',
    '.js': 'JavaScript',
    '.ts': 'TypeScript',
    '.html': 'HTML',
    '.css': 'CSS',
}

三色狀態 = {
    'red': '🔴',
    'yellow': '🟡',
    'green': '🟢',
    'blue': '🔵',
    'purple': '🟣',
    'white': '⚪',
}


# ═══════════════════════════════════════════════════════
# 數據結構
# ═══════════════════════════════════════════════════════

@dataclass
class DNA記錄:
    """單個文件的DNA記錄"""
    文件路徑: str
    文件名: str
    文件類型: str
    文件大小: int
    修改時間: float
    是否有DNA: bool = False
    DNA碼: str = ""
    DNA日期: str = ""
    DNA模塊: str = ""
    DNA版本: str = ""
    DNA格式有效: bool = False
    行數: int = 0


@dataclass
class 重複DNA組:
    """共享同一DNA的文件組"""
    DNA碼: str
    文件列表: List[str] = field(default_factory=list)
    嚴重度: str = "warning"  # critical / warning / info


@dataclass
class 審計報告:
    """完整審計報告"""
    審計時間: str = ""
    掃描目錄: str = ""
    總文件數: int = 0
    有DNA文件數: int = 0
    無DNA文件數: int = 0
    DNA對齐率: float = 0.0
    重複DNA數: int = 0
    無效DNA數: int = 0
    文件記錄: List[DNA記錄] = field(default_factory=list)
    重複組列表: List[重複DNA組] = field(default_factory=list)
    按類型統計: Dict = field(default_factory=dict)
    按目錄統計: Dict = field(default_factory=dict)
    健康評級: str = ""
    修復建議: List[str] = field(default_factory=list)


# ═══════════════════════════════════════════════════════
# DNA掃描器核心
# ═══════════════════════════════════════════════════════

class DNA掃描器:
    """遞歸掃描目錄，檢測所有文件DNA標記"""

    def __init__(self, 目標目錄: str, 嚴格模式: bool = False):
        self.目標目錄 = Path(目標目錄).expanduser().resolve()
        self.嚴格模式 = 嚴格模式
        self.記錄列表: List[DNA記錄] = []
        self.DNA到文件映射: Dict[str, List[str]] = defaultdict(list)

    def 應忽略目錄(self, 目錄名: str) -> bool:
        """判斷是否應忽略該目錄"""
        return 目錄名 in 忽略目錄模式 or 目錄名.startswith('.')

    def 應忽略文件(self, 文件名: str) -> bool:
        """判斷是否應忽略該文件"""
        for 模式 in 忽略文件模式:
            if fnmatch.fnmatch(文件名, 模式):
                return True
        return False

    def 提取文件DNA(self, 文件路徑: Path) -> Optional[Tuple[str, str, str, str]]:
        """從文件內容提取DNA碼，返回 (完整DNA, 日期, 模塊, 版本)"""
        try:
            with open(文件路徑, 'r', encoding='utf-8', errors='ignore') as f:
                內容 = f.read(8000)  # 只讀前8KB，DNA通常在頭部
        except Exception:
            return None

        匹配 = DNA正則模式.search(內容)
        if 匹配:
            完整DNA = 匹配.group(0)
            日期 = 匹配.group(1)
            模塊 = 匹配.group(2)
            版本 = 匹配.group(3)
            return 完整DNA, 日期, 模塊, 版本
        return None

    def 驗證DNA格式(self, dna碼: str) -> bool:
        """驗證DNA格式是否符合規範"""
        if not dna碼:
            return False
        return bool(DNA完整格式模式.match(dna碼))

    def 計算文件行數(self, 文件路徑: Path) -> int:
        """計算文件行數"""
        try:
            with open(文件路徑, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except Exception:
            return 0

    def 掃描(self) -> List[DNA記錄]:
        """遞歸掃描目錄，返回所有文件記錄"""
        self.記錄列表 = []
        self.DNA到文件映射 = defaultdict(list)

        if not self.目標目錄.exists():
            print(f"  ❌ 目錄不存在: {self.目標目錄}")
            return []

        for 根, 目錄們, 文件們 in os.walk(self.目標目錄):
            根路徑 = Path(根)
            相對根 = 根路徑.relative_to(self.目標目錄)

            # 過濾忽略的目錄
            目錄們[:] = [
                d for d in 目錄們
                if not self.應忽略目錄(d)
            ]

            for 文件名 in 文件們:
                if self.應忽略文件(文件名):
                    continue

                完整路徑 = 根路徑 / 文件名
                相對路徑 = str(完整路徑.relative_to(self.目標目錄))
                後綴 = 完整路徑.suffix.lower()
                文件類型 = 文件類型分類.get(後綴, '其他')

                try:
                    統計 = 完整路徑.stat()
                    文件大小 = 統計.st_size
                    修改時間 = 統計.st_mtime
                except Exception:
                    文件大小 = 0
                    修改時間 = 0

                記錄 = DNA記錄(
                    文件路徑=相對路徑,
                    文件名=文件名,
                    文件類型=文件類型,
                    文件大小=文件大小,
                    修改時間=修改時間,
                    行數=self.計算文件行數(完整路徑)
                )

                # 提取DNA
                dna結果 = self.提取文件DNA(完整路徑)
                if dna結果:
                    完整DNA, 日期, 模塊, 版本 = dna結果
                    記錄.是否有DNA = True
                    記錄.DNA碼 = 完整DNA
                    記錄.DNA日期 = 日期
                    記錄.DNA模塊 = 模塊
                    記錄.DNA版本 = 版本
                    記錄.DNA格式有效 = self.驗證DNA格式(完整DNA)
                    self.DNA到文件映射[完整DNA].append(相對路徑)

                self.記錄列表.append(記錄)

        return self.記錄列表

    def 獲取重複DNA組(self) -> List[重複DNA組]:
        """獲取重複DNA的文件組列表"""
        重複組 = []
        for dna碼, 文件列表 in self.DNA到文件映射.items():
            if len(文件列表) > 1:
                嚴重度 = "info"
                if len(文件列表) >= 5:
                    嚴重度 = "critical"
                elif len(文件列表) >= 3:
                    嚴重度 = "warning"

                重複組.append(重複DNA組(
                    DNA碼=dna碼,
                    文件列表=文件列表.copy(),
                    嚴重度=嚴重度
                ))

        # 按嚴重度排序
        嚴重度排序 = {"critical": 0, "warning": 1, "info": 2}
        重複組.sort(key=lambda g: (嚴重度排序.get(g.嚴重度, 3), -len(g.文件列表)))
        return 重複組


# ═══════════════════════════════════════════════════════
# 審計報告生成器
# ═══════════════════════════════════════════════════════

class 審計報告生成器:
    """生成詳細的DNA對齐審計報告"""

    def __init__(self, 掃描器: DNA掃描器):
        self.掃描器 = 掃描器

    def 計算健康評級(self, 對齐率: float) -> str:
        """根據對齐率計算健康評級"""
        if 對齐率 >= 90:
            return f"{三色狀態['green']} 優秀"
        elif 對齐率 >= 70:
            return f"{三色狀態['green']} 良好"
        elif 對齐率 >= 50:
            return f"{三色狀態['yellow']} 一般"
        elif 對齐率 >= 30:
            return f"{三色狀態['yellow']} 偏低"
        elif 對齐率 >= 10:
            return f"{三色狀態['red']} 危險"
        else:
            return f"{三色狀態['red']} 危機級"

    def 生成修復建議(self, 報告: 審計報告) -> List[str]:
        """基於審計結果生成修復建議"""
        建議 = []

        if 報告.DNA對齐率 < 50:
            建議.append(
                f"{三色狀態['red']} 緊急: DNA對齐率僅{報告.DNA對齐率:.1f}%，"
                f"需立即為{報告.無DNA文件數}個文件補充DNA"
            )

        if 報告.重複DNA數 > 0:
            建議.append(
                f"{三色狀態['red']} 高優先: 存在{報告.重複DNA數}個重複DNA，"
                f"違反「一文件一DNA」原則，需拆分"
            )

        if 報告.無效DNA數 > 0:
            建議.append(
                f"{三色狀態['yellow']} 中優先: {報告.無效DNA數}個文件DNA格式無效，"
                f"需修正格式為 #龍芯⚡️YYYY-MM-DD-MODULE-vX.X"
            )

        # 按類型建議
        for 類型, 統計 in 報告.按類型統計.items():
            對齐率 = 統計.get('對齐率', 0)
            if 對齐率 < 50 and 統計.get('總數', 0) > 5:
                建議.append(
                    f"{三色狀態['yellow']} {類型}: 對齐率{對齐率:.1f}%，"
                    f"需補充{統計.get('無DNA', 0)}個文件"
                )

        if not 建議:
            建議.append(f"{三色狀態['green']} 所有指標正常，無需修復")

        return 建議

    def 生成報告(self) -> 審計報告:
        """生成完整審計報告"""
        記錄列表 = self.掃描器.記錄列表
        重複組 = self.掃描器.獲取重複DNA組()

        總數 = len(記錄列表)
        有DNA = sum(1 for r in 記錄列表 if r.是否有DNA)
        無DNA = 總數 - 有DNA
        對齐率 = (有DNA / 總數 * 100) if 總數 > 0 else 0
        無效DNA = sum(1 for r in 記錄列表 if r.是否有DNA and not r.DNA格式有效)

        # 按類型統計
        按類型 = defaultdict(lambda: {"總數": 0, "有DNA": 0, "無DNA": 0})
        for r in 記錄列表:
            t = r.文件類型
            按類型[t]["總數"] += 1
            if r.是否有DNA:
                按類型[t]["有DNA"] += 1
            else:
                按類型[t]["無DNA"] += 1

        for t in 按類型:
            統計 = 按類型[t]
            統計["對齐率"] = (
                統計["有DNA"] / 統計["總數"] * 100
                if 統計["總數"] > 0 else 0
            )

        # 按目錄統計（頂層目錄）
        按目錄 = defaultdict(lambda: {"總數": 0, "有DNA": 0, "無DNA": 0})
        for r in 記錄列表:
            部分 = r.文件路徑.split('/')
            頂層 = 部分[0] if 部分 else "根目錄"
            按目錄[頂層]["總數"] += 1
            if r.是否有DNA:
                按目錄[頂層]["有DNA"] += 1
            else:
                按目錄[頂層]["無DNA"] += 1

        報告 = 審計報告(
            審計時間=datetime.now().strftime("%Y-%m-%d %H:%M CST"),
            掃描目錄=str(self.掃描器.目標目錄),
            總文件數=總數,
            有DNA文件數=有DNA,
            無DNA文件數=無DNA,
            DNA對齐率=對齐率,
            重複DNA數=len(重複組),
            無效DNA數=無效DNA,
            文件記錄=記錄列表,
            重複組列表=重複組,
            按類型統計=dict(按類型),
            按目錄統計=dict(按目錄),
        )

        報告.健康評級 = self.計算健康評級(對齐率)
        報告.修復建議 = self.生成修復建議(報告)

        return 報告


# ═══════════════════════════════════════════════════════
# 報告輸出器
# ═══════════════════════════════════════════════════════

class 報告輸出器:
    """輸出各種格式的審計報告"""

    @staticmethod
    def 輸出Markdown(報告: 審計報告, 輸出路徑: Optional[str] = None) -> str:
        """生成Markdown格式報告"""
        當前DNA = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-DNA-ALIGNMENT-AUDIT-v1.0"

        行 = []
        行.append("# 🐉 龍魂系統 DNA 對齐審計報告")
        行.append("")
        行.append(f"**DNA**: {當前DNA}")
        行.append(f"**時間**: {報告.審計時間}")
        行.append(f"**掃描目錄**: `{報告.掃描目錄}`")
        行.append(f"**狀態**: {報告.健康評級}")
        行.append("")
        行.append("---")
        行.append("")

        # 統計概覽
        行.append("## 📊 全系統統計")
        行.append("")
        行.append("| 指標 | 數值 | 狀態 |")
        行.append("|------|------|------|")

        狀態顏色 = 三色狀態['red'] if 報告.DNA對齐率 < 30 else (
            三色狀態['yellow'] if 報告.DNA對齐率 < 70 else 三色狀態['green']
        )
        行.append(f"| **核心文件無 DNA** | {報告.無DNA文件數} 個 | {狀態顏色} |")

        狀態顏色 = 三色狀態['green'] if 報告.有DNA文件數 > 100 else 三色狀態['yellow']
        行.append(f"| **已關聯 DNA 文件** | {報告.有DNA文件數} 個 | {狀態顏色} |")

        狀態顏色 = 三色狀態['red'] if 報告.重複DNA數 > 0 else 三色狀態['green']
        行.append(f"| **DNA 重複** | {報告.重複DNA數} 個 | {狀態顏色} |")
        行.append(f"| **核心文件總數** | {報告.總文件數} 個 | - |")

        狀態顏色 = 三色狀態['red'] if 報告.DNA對齐率 < 30 else (
            三色狀態['yellow'] if 報告.DNA對齐率 < 70 else 三色狀態['green']
        )
        行.append(f"| **DNA 對齐率** | {報告.DNA對齐率:.1f}% | {狀態顏色} |")
        行.append("")
        行.append("---")
        行.append("")

        # 按類型統計
        行.append("## 📁 按文件類型統計")
        行.append("")
        行.append("| 文件類型 | 總數 | 有DNA | 無DNA | 對齐率 |")
        行.append("|----------|------|-------|-------|--------|")
        for 類型, 統計 in sorted(
            報告.按類型統計.items(),
            key=lambda x: x[1]["總數"],
            reverse=True
        ):
            對齐率 = 統計["對齐率"]
            狀態 = 三色狀態['green'] if 對齐率 >= 70 else (
                三色狀態['yellow'] if 對齐率 >= 30 else 三色狀態['red']
            )
            行.append(
                f"| {類型} | {統計['總數']} | {統計['有DNA']} | "
                f"{統計['無DNA']} | {狀態} {對齐率:.1f}% |"
            )
        行.append("")

        # 重複DNA
        if 報告.重複組列表:
            行.append("## 🔴 DNA 重複問題")
            行.append("")
            行.append(f"發現 **{報告.重複DNA數}** 個DNA被多個文件共享:")
            行.append("")

            for i, 組 in enumerate(報告.重複組列表, 1):
                嚴重圖標 = {
                    "critical": "🔴",
                    "warning": "🟡",
                    "info": "🔵"
                }.get(組.嚴重度, "⚪")
                行.append(
                    f"{嚴重圖標} **{i}.** `{組.DNA碼}` → "
                    f"**{len(組.文件列表)}** 個文件"
                )
                for 文件 in 組.文件列表:
                    行.append(f"   - `{文件}`")
                行.append("")

            行.append("---")
            行.append("")

        # 修復建議
        行.append("## 💡 修復建議")
        行.append("")
        for 建議 in 報告.修復建議:
            行.append(f"- {建議}")
        行.append("")

        # 進度條
        填充數 = int(報告.DNA對齐率 / 5)
        空數 = 20 - 填充數
        進度條 = "█" * 填充數 + "░" * 空數
        行.append("## 📊 對齐進度")
        行.append("")
        行.append(f"```")
        行.append(f"DNA 對齐進度 [{進度條}] {報告.DNA對齐率:.1f}%")
        行.append(f"```")
        行.append("")

        # 底部
        行.append("---")
        行.append("")
        行.append(f"**DNA**: {當前DNA}")
        行.append("**簽署**: DNA對齐審計系統·不免責")
        行.append("")
        行.append("🐉 龍魂系統·DNA追溯·完整性驗證")

        結果 = "\n".join(行)

        if 輸出路徑:
            with open(輸出路徑, 'w', encoding='utf-8') as f:
                f.write(結果)
            print(f"  ✅ Markdown報告已保存: {輸出路徑}")

        return 結果

    @staticmethod
    def 輸出JSON(報告: 審計報告, 輸出路徑: Optional[str] = None) -> str:
        """生成JSON格式報告"""
        數據 = {
            "審計時間": 報告.審計時間,
            "掃描目錄": 報告.掃描目錄,
            "統計": {
                "總文件數": 報告.總文件數,
                "有DNA文件數": 報告.有DNA文件數,
                "無DNA文件數": 報告.無DNA文件數,
                "DNA對齐率": round(報告.DNA對齐率, 2),
                "重複DNA數": 報告.重複DNA數,
                "無效DNA數": 報告.無效DNA數,
            },
            "健康評級": 報告.健康評級,
            "修復建議": 報告.修復建議,
            "按類型統計": 報告.按類型統計,
            "按目錄統計": 報告.按目錄統計,
            "重複DNA列表": [
                {
                    "DNA碼": 組.DNA碼,
                    "文件數": len(組.文件列表),
                    "嚴重度": 組.嚴重度,
                    "文件列表": 組.文件列表
                }
                for 組 in 報告.重複組列表
            ]
        }

        結果 = json.dumps(數據, ensure_ascii=False, indent=2)

        if 輸出路徑:
            with open(輸出路徑, 'w', encoding='utf-8') as f:
                f.write(結果)
            print(f"  ✅ JSON報告已保存: {輸出路徑}")

        return 結果

    @staticmethod
    def 輸出控制台摘要(報告: 審計報告):
        """輸出控制台摘要"""
        print("\n" + "=" * 60)
        print("🐉 龍魂DNA對齐審計摘要")
        print("=" * 60)
        print(f"  掃描目錄 : {報告.掃描目錄}")
        print(f"  審計時間 : {報告.審計時間}")
        print(f"  ────────────────────────────────────────")
        print(f"  總文件數 : {報告.總文件數}")
        print(f"  有DNA    : {三色狀態['green']} {報告.有DNA文件數}")
        print(f"  無DNA    : {三色狀態['red'] if 報告.無DNA文件數 > 100 else 三色狀態['yellow']} {報告.無DNA文件數}")
        print(f"  重複DNA  : {三色狀態['red'] if 報告.重複DNA數 > 0 else 三色狀態['green']} {報告.重複DNA數}")
        print(f"  無效DNA  : {報告.無效DNA數}")
        print(f"  ────────────────────────────────────────")

        填充數 = int(報告.DNA對齐率 / 5)
        空數 = 20 - 填充數
        進度條 = "█" * 填充數 + "░" * 空數
        print(f"  對齐率   : [{進度條}] {報告.DNA對齐率:.1f}%")
        print(f"  健康評級 : {報告.健康評級}")
        print(f"  ────────────────────────────────────────")
        print("  修復建議:")
        for 建議 in 報告.修復建議[:5]:
            print(f"    {建議}")
        print("=" * 60 + "\n")


# ═══════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════

def 主函數():
    """命令行入口"""
    import argparse

    解析器 = argparse.ArgumentParser(
        description='龍魂DNA對齐審計器 — 掃描·統計·重複檢測'
    )
    解析器.add_argument(
        '目標目錄',
        nargs='?',
        default='.',
        help='要掃描的目標目錄 (默認: 當前目錄)'
    )
    解析器.add_argument(
        '-o', '--輸出',
        default=None,
        help='輸出報告目錄 (默認: 不輸出文件)'
    )
    解析器.add_argument(
        '--json',
        action='store_true',
        help='同時輸出JSON格式'
    )
    解析器.add_argument(
        '--嚴格',
        action='store_true',
        help='嚴格模式 (更嚴格的格式驗證)'
    )

    參數 = 解析器.parse_args()

    print(f"🔍 開始掃描: {參數.目標目錄}")

    # 執行掃描
    掃描器 = DNA掃描器(參數.目標目錄, 嚴格模式=參數.嚴格)
    掃描器.掃描()

    print(f"  📁 發現 {len(掃描器.記錄列表)} 個文件")

    # 生成報告
    報告生成器 = 審計報告生成器(掃描器)
    報告 = 報告生成器.生成報告()

    # 控制台輸出
    報告輸出器.輸出控制台摘要(報告)

    # 文件輸出
    if 參數.輸出:
        輸出路徑 = Path(參數.輸出)
        輸出路徑.mkdir(parents=True, exist_ok=True)

        時間戳 = datetime.now().strftime("%Y%m%d_%H%M%S")

        md路徑 = 輸出路徑 / f"DNA_ALIGNMENT_AUDIT_{時間戳}.md"
        報告輸出器.輸出Markdown(報告, str(md路徑))

        if 參數.json:
            json路徑 = 輸出路徑 / f"DNA_ALIGNMENT_AUDIT_{時間戳}.json"
            報告輸出器.輸出JSON(報告, str(json路徑))

        print(f"\n📄 報告已保存到: {輸出路徑}")

    # 返回狀態碼
    return 0 if 報告.DNA對齐率 >= 70 else 1


if __name__ == '__main__':
    exit(主函數())
