# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-19-DNA-REPAIR-AGENT-v5.2
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂DNA修復器
DNA Repair Agent — 自動為缺失DNA的文件生成追溯碼·拆分重複DNA·修復格式

DNA: #龍芯⚡️2026-06-19-DNA-REPAIR-AGENT-v5.2
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import hashlib

# ═══════════════════════════════════════════════════════
# 常量與配置
# ═══════════════════════════════════════════════════════

DNA正則模式 = re.compile(
    r'[\s"\']?#龍芯[\u26a1\ufe0f]*(\d{4}-\d{2}-\d{2})-(.+?)-v([\d.]+)'
)

DNA完整格式模式 = re.compile(
    r'^#龍芯⚡️\d{4}-\d{2}-\d{2}-[A-Z][A-Z0-9_-]*-v[\d.]+$'
)

文件類型前綴映射 = {
    '.py': 'ENGINE',
    '.md': 'DOC',
    '.sh': 'TOOL',
    '.json': 'CONFIG',
    '.yaml': 'CONFIG',
    '.yml': 'CONFIG',
    '.toml': 'CONFIG',
    '.txt': 'DOC',
    '.js': 'ENGINE',
    '.ts': 'ENGINE',
    '.html': 'UI',
    '.css': 'STYLE',
}

目錄前綴映射 = {
    'scripts': 'SCRIPT',
    'protocols': 'PROTOCOL',
    'cnsh-core': 'CORE',
    'cnsh': 'CNSH',
    'governance': 'GOVERNANCE',
    'registry': 'REGISTRY',
    'dna': 'DNA-MODULE',
    'ai-tools': 'AI-TOOL',
    'multicurrency': 'MULTI',
    'cloud': 'CLOUD',
    'local': 'LOCAL',
    'references': 'REF',
    'assets': 'ASSET',
    'rules': 'RULE',
    'semantic': 'SEMANTIC',
    'language': 'LANG',
    'compiler': 'COMPILER',
    'skill-standards': 'SKILL',
    'wuxing_calculator': 'WUXING',
    'audit-constitution': 'AUDIT',
    'brain': 'BRAIN',
    'mobile-monitoring': 'MOBILE',
}

三色狀態 = {
    'red': '🔴',
    'yellow': '🟡',
    'green': '🟢',
    'blue': '🔵',
}


# ═══════════════════════════════════════════════════════
# 數據結構
# ═══════════════════════════════════════════════════════

@dataclass
class 修復記錄:
    """單次修復操作記錄"""
    操作類型: str  # 'add' | 'fix_duplicate' | 'fix_format' | 'skip'
    文件路徑: str
    原DNA: str = ""
    新DNA: str = ""
    狀態: str = "pending"  # pending | success | failed
    備註: str = ""


@dataclass
class 修復報告:
    """完整修復報告"""
    修復時間: str = ""
    掃描目錄: str = ""
    新增DNA數: int = 0
    修復重複數: int = 0
    修復格式數: int = 0
    跳過數: int = 0
    失敗數: int = 0
    修復記錄列表: List[修復記錄] = field(default_factory=list)
    修復前對齐率: float = 0.0
    修復後對齐率: float = 0.0
    修復前重複數: int = 0
    修復後重複數: int = 0


# ═══════════════════════════════════════════════════════
# DNA生成器
# ═══════════════════════════════════════════════════════

class DNA生成器:
    """為文件生成唯一DNA追溯碼"""

    def __init__(self):
        self.已使用DNA: set = set()
        self.DNA衝突計數: Dict[str, int] = defaultdict(int)

    def 從路徑提取組件(self, 文件路徑: Path) -> Tuple[str, str]:
        """從文件路徑提取模塊名和功能名"""
        後綴 = 文件路徑.suffix.lower()
        文件名 = 文件路徑.stem
        父目錄 = 文件路徑.parent

        # 確定前綴
        前綴 = 'MODULE'

        # 先檢查目錄映射
        for 目錄名, 映射前綴 in 目錄前綴映射.items():
            if 目錄名 in str(父目錄):
                前綴 = 映射前綴
                break

        # 如果沒有匹配，使用文件類型前綴
        if 前綴 == 'MODULE' and 後綴 in 文件類型前綴映射:
            前綴 = 文件類型前綴映射[後綴]

        # 生成模塊名（從文件名）
        模塊名 = self._文件名轉模塊名(文件名)

        return 前綴, 模塊名

    def _文件名轉模塊名(self, 文件名: str) -> str:
        """將文件名轉換為DNA模塊名（大寫，使用連字符）"""
        # 移除非字母數字字符，轉為連字符
        結果 = re.sub(r'[^\w\u4e00-\u9fff]', '-', 文件名)
        結果 = re.sub(r'-+', '-', 結果).strip('-')

        # 如果是中文，使用拼音風格的大寫
        if not 結果 or 結果.startswith('_'):
            結果 = 'UNNAMED'

        return 結果.upper()

    def 生成DNA(
        self,
        文件路徑: Path,
        基礎目錄: Path,
        指定前綴: Optional[str] = None,
        指定模塊: Optional[str] = None
    ) -> str:
        """為文件生成唯一DNA碼"""
        日期 = datetime.now().strftime('%Y-%m-%d')

        if 指定前綴 and 指定模塊:
            前綴 = 指定前綴.upper()
            模塊 = 指定模塊.upper()
        else:
            前綴, 模塊 = self.從路徑提取組件(文件路徑)

        # 確保唯一性
        基礎DNA = f"#龍芯⚡️{日期}-{前綴}-{模塊}-v1.0"
        最終DNA = 基礎DNA

        計數器 = 1
        while 最終DNA in self.已使用DNA:
            計數器 += 1
            最終DNA = f"#龍芯⚡️{日期}-{前綴}-{模塊}-v1.0-{計數器}"

        self.已使用DNA.add(最終DNA)
        return 最終DNA

    def 註冊已有DNA(self, dna碼: str):
        """註冊已存在的DNA碼（避免衝突）"""
        self.已使用DNA.add(dna碼)


# ═══════════════════════════════════════════════════════
# 文件修復器
# ═══════════════════════════════════════════════════════

class 文件修復器:
    """執行文件級別的DNA修復"""

    def __init__(self, 基礎目錄: Path, 模擬模式: bool = True):
        self.基礎目錄 = 基礎目錄
        self.模擬模式 = 模擬模式
        self.DNA生成器 = DNA生成器()
        self.修復記錄: List[修復記錄] = []

    def 讀取文件DNA(self, 文件路徑: Path) -> Optional[re.Match]:
        """讀取文件中的DNA標記"""
        try:
            with open(文件路徑, 'r', encoding='utf-8', errors='ignore') as f:
                內容 = f.read(10000)
            return DNA正則模式.search(內容)
        except Exception:
            return None

    def 讀取文件頭註釋區域(self, 文件路徑: Path) -> str:
        """讀取文件頭部的註釋區域（用於確定插入位置）"""
        try:
            with open(文件路徑, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(2000)
        except Exception:
            return ""

    def 插入DNA到文件(self, 文件路徑: Path, dna碼: str) -> bool:
        """將DNA碼插入文件頭部"""
        try:
            後綴 = 文件路徑.suffix.lower()

            with open(文件路徑, 'r', encoding='utf-8', errors='ignore') as f:
                原內容 = f.read()

            # 根據文件類型選擇註釋格式
            if 後綴 in ('.py', '.sh', '.js', '.ts', '.yml', '.yaml'):
                註釋開始 = '# -*- coding: utf-8 -*-\n' if 後綴 == '.py' else ''
                頭部 = f"""{註釋開始}""" if 註釋開始 and not 原內容.startswith('# -*-') else ""
                頭部 += f'# {dna碼}\n# 君子協議: 本文件受龍魂DNA追溯保護\n\n'

            elif 後綴 == '.md':
                頭部 = f'<!-- {dna碼} -->\n<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->\n\n'

            elif 後綴 in ('.html', '.htm'):
                頭部 = f'<!-- {dna碼} -->\n<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->\n\n'

            elif 後綴 == '.css':
                頭部 = f'/* {dna碼} */\n/* 君子協議: 本文件受龍魂DNA追溯保護 */\n\n'

            elif 後綴 == '.json':
                # JSON 不支持註釋，添加 _dna 字段
                try:
                    數據 = json.loads(原內容) if 原內容.strip() else {}
                    if isinstance(數據, dict):
                        數據['_dna'] = dna碼.replace('#龍芯⚡️', '')
                        新內容 = json.dumps(數據, ensure_ascii=False, indent=2)
                        if not self.模擬模式:
                            with open(文件路徑, 'w', encoding='utf-8') as f:
                                f.write(新內容)
                        return True
                except json.JSONDecodeError:
                    pass
                return False

            else:
                頭部 = f'# {dna碼}\n# 君子協議: 本文件受龍魂DNA追溯保護\n\n'

            if not self.模擬模式:
                with open(文件路徑, 'w', encoding='utf-8') as f:
                    f.write(頭部 + 原內容)

            return True

        except Exception as e:
            print(f"    ❌ 插入DNA失敗 {文件路徑}: {e}")
            return False

    def 替換文件DNA(
        self,
        文件路徑: Path,
        原DNA: str,
        新DNA: str
    ) -> bool:
        """替換文件中的DNA碼（用於拆分重複）"""
        try:
            with open(文件路徑, 'r', encoding='utf-8', errors='ignore') as f:
                內容 = f.read()

            新內容 = 內容.replace(原DNA, 新DNA, 1)

            if 新內容 == 內容:
                print(f"    ⚠️ 未找到原DNA: {文件路徑}")
                return False

            if not self.模擬模式:
                with open(文件路徑, 'w', encoding='utf-8') as f:
                    f.write(新內容)

            return True

        except Exception as e:
            print(f"    ❌ 替換DNA失敗 {文件路徑}: {e}")
            return False

    def 修復缺失DNA(
        self,
        文件路徑: Path,
        優先級: str = "normal"
    ) -> 修復記錄:
        """為缺失DNA的文件添加DNA"""
        記錄 = 修復記錄(
            操作類型='add',
            文件路徑=str(文件路徑.relative_to(self.基礎目錄))
        )

        # 檢查是否已有DNA
        dna匹配 = self.讀取文件DNA(文件路徑)
        if dna匹配:
            記錄.原DNA = dna匹配.group(0)
            記錄.狀態 = 'skip'
            記錄.備註 = '文件已有DNA'
            return 記錄

        # 生成新DNA
        新DNA = self.DNA生成器.生成DNA(文件路徑, self.基礎目錄)
        記錄.新DNA = 新DNA

        # 執行插入
        if self.插入DNA到文件(文件路徑, 新DNA):
            記錄.狀態 = 'success' if not self.模擬模式 else 'pending'
            記錄.備註 = f"{'[模擬] ' if self.模擬模式 else ''}已添加DNA"
        else:
            記錄.狀態 = 'failed'
            記錄.備註 = '插入失敗'

        self.修復記錄.append(記錄)
        return 記錄

    def 修復重複DNA(
        self,
        dna碼: str,
        文件列表: List[str],
        掃描器記錄
    ) -> List[修復記錄]:
        """拆分重複DNA（保留第一個，為其餘生成新DNA）"""
        記錄列表 = []

        # 保留第一個不變，為其餘生成新DNA
        for i, 文件相對路徑 in enumerate(文件列表):
            if i == 0:
                # 保留第一個
                記錄 = 修復記錄(
                    操作類型='fix_duplicate',
                    文件路徑=文件相對路徑,
                    原DNA=dna碼,
                    新DNA=dna碼,
                    狀態='skip',
                    備註='保留為主文件'
                )
                self.DNA生成器.註冊已有DNA(dna碼)
                記錄列表.append(記錄)
                self.修復記錄.append(記錄)
                continue

            # 為其餘文件生成新DNA
            完整路徑 = self.基礎目錄 / 文件相對路徑
            記錄 = 修復記錄(
                操作類型='fix_duplicate',
                文件路徑=文件相對路徑,
                原DNA=dna碼
            )

            # 解析原DNA組件
            匹配 = DNA正則模式.match(dna碼)
            if 匹配:
                日期 = 匹配.group(1)
                模塊 = 匹配.group(2)
                版本 = 匹配.group(3)
                # 添加後綴區分
                新模塊 = f"{模塊}-FILE{i}"
                新DNA = f"#龍芯⚡️{日期}-{新模塊}-v{版本}"

                # 檢查衝突
                計數器 = 1
                基礎新DNA = 新DNA
                while 新DNA in self.DNA生成器.已使用DNA:
                    新DNA = f"{基礎新DNA}-{計數器}"
                    計數器 += 1

                self.DNA生成器.註冊已有DNA(新DNA)
                記錄.新DNA = 新DNA

                if self.替換文件DNA(完整路徑, dna碼, 新DNA):
                    記錄.狀態 = 'success' if not self.模擬模式 else 'pending'
                    記錄.備註 = f"{'[模擬] ' if self.模擬模式 else ''}已重新分配DNA"
                else:
                    記錄.狀態 = 'failed'
                    記錄.備註 = '替換失敗'
            else:
                記錄.狀態 = 'failed'
                記錄.備註 = '無法解析原DNA格式'

            記錄列表.append(記錄)
            self.修復記錄.append(記錄)

        return 記錄列表


# ═══════════════════════════════════════════════════════
# 批量修復引擎
# ═══════════════════════════════════════════════════════

class 批量修復引擎:
    """執行批量DNA修復操作"""

    def __init__(
        self,
        目標目錄: str,
        模擬模式: bool = True,
        最大修復數: int = 0  # 0 = 無限制
    ):
        self.基礎目錄 = Path(目標目錄).expanduser().resolve()
        self.模擬模式 = 模擬模式
        self.最大修復數 = 最大修復數
        self.文件修復器 = 文件修復器(self.基礎目錄, 模擬模式)

    def 掃描並修復(
        self,
        優先級目錄: Optional[List[str]] = None,
        排除模式: Optional[List[str]] = None
    ) -> 修復報告:
        """掃描目錄並執行修復"""
        報告 = 修復報告(
            修復時間=datetime.now().strftime("%Y-%m-%d %H:%M CST"),
            掃描目錄=str(self.基礎目錄)
        )

        優先級目錄 = 優先級目錄 or []
        排除模式 = 排除模式 or ['__pycache__', '.git', 'node_modules', 'venv']

        # 第一步：收集所有文件和已有DNA
        print(f"\n{'='*60}")
        print("🔍 第一階段: 掃描所有文件...")
        print(f"{'='*60}")

        所有文件: List[Path] = []
        有DNA文件 = 0
        無DNA文件 = 0
        DNA到文件: Dict[str, List[str]] = defaultdict(list)

        for 根, 目錄們, 文件們 in os.walk(self.基礎目錄):
            # 過濾目錄
            目錄們[:] = [
                d for d in 目錄們
                if not any(忽略 in d for 忽略 in 排除模式)
                and not d.startswith('.')
            ]

            for 文件名 in 文件們:
                if 文件名.startswith('.'):
                    continue
                if any(文件名.endswith(ext) for ext in ('.pyc', '.pyo', '.so')):
                    continue

                完整路徑 = Path(根) / 文件名
                相對路徑 = str(完整路徑.relative_to(self.基礎目錄))

                所有文件.append(完整路徑)

                # 檢查DNA
                dna匹配 = self.文件修復器.讀取文件DNA(完整路徑)
                if dna匹配:
                    有DNA文件 += 1
                    dna碼 = dna匹配.group(0)
                    DNA到文件[dna碼].append(相對路徑)
                    self.文件修復器.DNA生成器.註冊已有DNA(dna碼)
                else:
                    無DNA文件 += 1

        總數 = len(所有文件)
        報告.修復前對齐率 = (有DNA文件 / 總數 * 100) if 總數 > 0 else 0
        報告.修復前重複數 = sum(1 for v in DNA到文件.values() if len(v) > 1)

        print(f"  總文件: {總數}")
        print(f"  有DNA: {三色狀態['green']} {有DNA文件}")
        print(f"  無DNA: {三色狀態['yellow'] if 無DNA文件 < 100 else 三色狀態['red']} {無DNA文件}")
        print(f"  重複DNA: {報告.修復前重複數}")

        # 第二步：修復重複DNA
        if 報告.修復前重複數 > 0:
            print(f"\n{'='*60}")
            print("🔄 第二階段: 修復重複DNA...")
            print(f"{'='*60}")

            for dna碼, 文件列表 in sorted(
                DNA到文件.items(),
                key=lambda x: -len(x[1])
            ):
                if len(文件列表) > 1:
                    print(
                        f"\n  🔴 `{dna碼}` → {len(文件列表)}個文件"
                    )
                    記錄列表 = self.文件修復器.修復重複DNA(
                        dna碼, 文件列表, None
                    )
                    成功數 = sum(1 for r in 記錄列表 if r.狀態 in ('success', 'pending'))
                    報告.修復重複數 += len(記錄列表) - 1  # 減去保留的主文件
                    print(f"     已處理: {成功數}/{len(記錄列表)}")

        # 第三步：為無DNA文件添加DNA
        print(f"\n{'='*60}")
        print("➕ 第三階段: 為缺失DNA文件添加追溯碼...")
        print(f"{'='*60}")

        # 排序：優先目錄的文件在前
        def 排序鍵(文件路徑: Path) -> int:
            相對 = str(文件路徑.relative_to(self.基礎目錄))
            for i, 優先 in enumerate(優先級目錄):
                if 優先 in 相對:
                    return i
            return len(優先級目錄)

        所有文件.sort(key=排序鍵)

        修復計數 = 0
        批次大小 = 50

        for i, 文件路徑 in enumerate(所有文件):
            相對路徑 = str(文件路徑.relative_to(self.基礎目錄))

            # 檢查是否已有DNA
            if self.文件修復器.讀取文件DNA(文件路徑):
                continue

            # 檢查最大修復數限制
            if self.最大修復數 > 0 and 修復計數 >= self.最大修復數:
                print(f"\n  ⏹️ 達到最大修復數限制 ({self.最大修復數})")
                break

            記錄 = self.文件修復器.修復缺失DNA(文件路徑)

            if 記錄.狀態 in ('success', 'pending'):
                修復計數 += 1
                報告.新增DNA數 += 1

                if 修復計數 % 批次大小 == 0:
                    print(f"    已處理 {修復計數} 個文件...")

        print(f"\n  ✅ 新增DNA: {報告.新增DNA數} 個文件")

        # 計算修復後對齐率
        新有DNA = 有DNA文件 + 報告.新增DNA數
        報告.修復後對齐率 = (新有DNA / 總數 * 100) if 總數 > 0 else 0
        報告.修復後重複數 = max(0, 報告.修復前重複數 - 報告.修復重複數)
        報告.修復記錄列表 = self.文件修復器.修復記錄

        return 報告


# ═══════════════════════════════════════════════════════
# 修復報告生成器
# ═══════════════════════════════════════════════════════

class 修復報告生成器:
    """生成修復前後對比報告"""

    @staticmethod
    def 生成Markdown報告(報告: 修復報告, 輸出路徑: Optional[str] = None) -> str:
        """生成Markdown格式的修復報告"""
        當前DNA = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-DNA-REPAIR-REPORT-v1.0"

        行 = []
        行.append("# 🐉 龍魂DNA修復報告")
        行.append("")
        行.append(f"**DNA**: {當前DNA}")
        行.append(f"**時間**: {報告.修復時間}")
        行.append(f"**模式**: {'模擬模式 (未實際修改)' if hasattr(報告, '_模擬') else '實際修復'}")
        行.append("")
        行.append("---")
        行.append("")

        # 修復前後對比
        行.append("## 📊 修復前後對比")
        行.append("")
        行.append("| 指標 | 修復前 | 修復後 | 改善 |")
        行.append("|------|--------|--------|------|")

        前對齐率 = 報告.修復前對齐率
        後對齐率 = 報告.修復後對齐率
        改善率 = 後對齐率 - 前對齐率

        行.append(
            f"| DNA對齐率 | {前對齐率:.1f}% | {後對齐率:.1f}% | "
            f"{三色狀態['green']} +{改善率:.1f}% |"
        )
        行.append(
            f"| 重複DNA數 | {報告.修復前重複數} | {報告.修復後重複數} | "
            f"{三色狀態['green']} -{報告.修復前重複數 - 報告.修復後重複數} |"
        )
        行.append(f"| 新增DNA數 | - | {報告.新增DNA數} | {三色狀態['green']} +{報告.新增DNA數} |")
        行.append(f"| 修復重複數 | - | {報告.修復重複數} | {三色狀態['green']} +{報告.修復重複數} |")
        行.append("")

        # 進度視覺化
        行.append("### 對齐率進度")
        行.append("")

        前填充 = int(前對齐率 / 5)
        前空 = 20 - 前填充
        後填充 = int(後對齐率 / 5)
        後空 = 20 - 後填充

        行.append(f"```")
        行.append(f"修復前 [{('█' * 前填充) + ('░' * 前空)}] {前對齐率:.1f}%")
        行.append(f"修復後 [{('█' * 後填充) + ('░' * 後空)}] {後對齐率:.1f}%")
        行.append(f"```")
        行.append("")
        行.append("---")
        行.append("")

        # 修復記錄詳情
        行.append("## 🔧 修復記錄詳情")
        行.append("")

        # 新增DNA記錄
        新增記錄 = [r for r in 報告.修復記錄列表 if r.操作類型 == 'add']
        if 新增記錄:
            行.append(f"### 新增DNA ({len(新增記錄)} 個文件)")
            行.append("")
            行.append("| # | 文件路徑 | DNA碼 | 狀態 |")
            行.append("|---|----------|-------|------|")
            for i, 記錄 in enumerate(新增記錄[:100], 1):  # 最多顯示100個
                狀態圖標 = {
                    'success': '✅',
                    'pending': '🟡',
                    'failed': '❌',
                    'skip': '⏭️'
                }.get(記錄.狀態, '❓')
                dna顯示 = f"`{記錄.新DNA}`" if 記錄.新DNA else "-"
                行.append(
                    f"| {i} | `{記錄.文件路徑}` | {dna顯示} | {狀態圖標} |"
                )
            if len(新增記錄) > 100:
                行.append(f"| ... | *還有 {len(新增記錄) - 100} 個文件* | | |")
            行.append("")

        # 重複修復記錄
        重複記錄 = [r for r in 報告.修復記錄列表 if r.操作類型 == 'fix_duplicate']
        if 重複記錄:
            行.append(f"### 重複DNA修復 ({len(重複記錄)} 條記錄)")
            行.append("")
            行.append("| 文件路徑 | 原DNA | 新DNA | 狀態 |")
            行.append("|----------|-------|-------|------|")
            for 記錄 in 重複記錄[:50]:
                狀態圖標 = {
                    'success': '✅',
                    'pending': '🟡',
                    'failed': '❌',
                    'skip': '⏭️'
                }.get(記錄.狀態, '❓')
                原DNA顯示 = f"`{記錄.原DNA}`" if 記錄.原DNA else "-"
                新DNA顯示 = f"`{記錄.新DNA}`" if 記錄.新DNA else "-"
                行.append(
                    f"| `{記錄.文件路徑}` | {原DNA顯示} | {新DNA顯示} | {狀態圖標} |"
                )
            行.append("")

        行.append("---")
        行.append("")
        行.append(f"**DNA**: {當前DNA}")
        行.append("**簽署**: DNA修復系統·不免責")
        行.append("")
        行.append("🐉 龍魂系統·DNA追溯·自動修復完成")

        結果 = "\n".join(行)

        if 輸出路徑:
            with open(輸出路徑, 'w', encoding='utf-8') as f:
                f.write(結果)
            print(f"  ✅ 修復報告已保存: {輸出路徑}")

        return 結果


# ═══════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════

def 主函數():
    """命令行入口"""
    import argparse

    解析器 = argparse.ArgumentParser(
        description='龍魂DNA修復器 — 自動為缺失DNA的文件生成追溯碼'
    )
    解析器.add_argument(
        '目標目錄',
        nargs='?',
        default='.',
        help='要修復的目標目錄 (默認: 當前目錄)'
    )
    解析器.add_argument(
        '-o', '--輸出',
        default=None,
        help='輸出報告目錄'
    )
    解析器.add_argument(
        '--執行',
        action='store_true',
        help='實際執行修復 (默認為模擬模式)'
    )
    解析器.add_argument(
        '--最大修復數',
        type=int,
        default=0,
        help='最大修復文件數 (0=無限制，默認: 0)'
    )
    解析器.add_argument(
        '--優先',
        nargs='+',
        default=[],
        help='優先修復的目錄名列表'
    )

    參數 = 解析器.parse_args()

    模擬模式 = not 參數.執行

    print(f"🐉 龍魂DNA修復器")
    print(f"{'='*60}")
    print(f"  目標目錄: {參數.目標目錄}")
    print(f"  運行模式: {'模擬 (預覽)' if 模擬模式 else '實際執行'}")
    print(f"  最大修復: {參數.最大修復數 if 參數.最大修復數 > 0 else '無限制'}")
    if 參數.優先:
        print(f"  優先目錄: {', '.join(參數.優先)}")
    print(f"{'='*60}")

    # 執行修復
    引擎 = 批量修復引擎(
        參數.目標目錄,
        模擬模式=模擬模式,
        最大修復數=參數.最大修復數
    )

    報告 = 引擎.掃描並修復(優先級目錄=參數.優先)

    # 輸出摘要
    print(f"\n{'='*60}")
    print("📊 修復摘要")
    print(f"{'='*60}")
    print(f"  新增DNA: {三色狀態['green']} {報告.新增DNA數}")
    print(f"  修復重複: {報告.修復重複數}")
    print(f"  修復前對齐率: {報告.修復前對齐率:.1f}%")
    print(f"  修復後對齐率: {報告.修復後對齐率:.1f}%")
    print(f"  改善: {三色狀態['green']} +{報告.修復後對齐率 - 報告.修復前對齐率:.1f}%")

    # 生成報告
    if 參數.輸出:
        輸出路徑 = Path(參數.輸出)
        輸出路徑.mkdir(parents=True, exist_ok=True)

        時間戳 = datetime.now().strftime("%Y%m%d_%H%M%S")
        md路徑 = 輸出路徑 / f"DNA_REPAIR_REPORT_{時間戳}.md"
        修復報告生成器.生成Markdown報告(報告, str(md路徑))
        print(f"\n📄 報告已保存: {輸出路徑}")

    return 0


if __name__ == '__main__':
    exit(主函數())
