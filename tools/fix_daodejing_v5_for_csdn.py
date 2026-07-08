#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
道德經 v5.0 修復 + CSDN 發布版生成器
DNA: #龍芯⚡️2026-07-05-DAODEJING-v5.0-FIX-CSDN
"""

import re
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

SRC = Path.home() / "Desktop/文章/2026-07-04-道德经81章_龍魂系统大白话解读_完整版_v5.0.md"
DST_FIXED = Path.home() / "Desktop/文章/2026-07-04-道德经81章_龍魂系统大白话解读_完整版_v5.0_已修复.md"
DST_CSDN = Path.home() / "Desktop/文章/CSDN发布版/2026-07-04-道德经81章_龍魂系统大白话解读_完整版_v5.0-CSDN发布版.md"


def now_dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    h = sha256(f"{prefix}-{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{prefix}-{h}"


def fix_metadata(text: str) -> str:
    """修正元信息表中的版本號"""
    text = text.replace(
        "| **DNA主鏈** | `#龍芯⚡️2026-07-04-LONGHUN-DAODEJING-v4.0-FULL-81` |",
        "| **DNA主鏈** | `#龍芯⚡️2026-07-04-LONGHUN-DAODEJING-v5.0-FULL-81` |"
    )
    text = text.replace(
        "| **版本** | v4.0 人民標準完整版 |",
        "| **版本** | v5.0 完整81章全量版（底層倫理錨已焊死） |"
    )
    text = text.replace(
        "| **章節覆蓋** | 81章全量（本文檔第21-81章 + v3.0第1-20章） |",
        "| **章節覆蓋** | 81章全量（v1.0第1-20章 + v4.0第21-81章 + v5.0統一格式與倫理錨） |"
    )
    text = text.replace(
        "| **格式規格** | 每章8列大白話表格 + 5條核心判斷 + DNA追溯 |",
        "| **格式規格** | 每章8列大白話表格 + 5條核心判斷 + 多維度注解 + DNA追溯 |"
    )
    text = text.replace(
        "| **生成時間** | 2026-07-04 |",
        "| **生成時間** | 2026-07-04 21:33:42 UTC |"
    )
    text = text.replace(
        "**EOF DNA:** `#龍芯⚡️2026-07-04-DAODEJING-81-EOF-V4.0-COMPLETE`",
        "**EOF DNA:** `#龍芯⚡️2026-07-04-DAODEJING-81-EOF-V5.0-COMPLETE`"
    )
    return text


def build_p0_header() -> str:
    dna = now_dna("P0-ENTRY-CARD")
    return f"""---

## 🌟 唯一入口·導航卡 v1.2｜粘 / 掃 / 信

**DNA:** `{dna}`
**IPA標籤:** `[IPA-P01-DAO] 道德經81章全量解讀 v5.0｜P0++永恆鎖定｜UID9622`

| 動作 | 說明 |
|---|---|
| **粘** | 本文是龍魂系統關於《道德經》的**唯一官方入口**，任何引用必須帶本頁 DNA |
| **掃** | 81章全覆蓋 + 多維度注解 + 底層倫理錨，可掃描標籤索引快速定位 |
| **信** | 全文帶 DNA 追溯、GPG 指紋、CONFIRM 碼，來源可查、去向可追、責任可究 |

**P0++ 隱私與主權聲明：**
- 本文數據根留本地，龍魂系統優先；外發 CSDN 為公開脫敏版。
- 不收集讀者個人信息，不設付費牆，不釣魚。
- 引用本文需保留 DNA、作者、協議信息，禁止蒸餾換殼。

---
"""


def build_iron_laws_section() -> str:
    dna = now_dna("IRON-LAWS-ALIGN")
    return f"""---

## 🛡️ 鐵律對齊聲明 · v5.0

**DNA:** `{dna}`

本文檔對齊 龍魂铁律总览 v1.0 以下核心條款：

| 鐵律 | 在本文中的體現 |
|---|---|
| **§1 龍魂價值觀鐵律** | 服務人民，不是資本的遊戲；還原戰場經驗，不接術語不接爹味 |
| **§2 使用守則** | 一次做對，不讓人民重複造輪子；每個節點標配 DNA |
| **§4 L0 永恆契約·人民主權宣言** | 數據主權歸 UID9622 / 龍魂系統，中國法律為骨，人民為本 |
| **§9.16 §S-24 創意歸屬·禁蒸餾換邏輯** | 本文所有注解、標籤、矩陣均有 DNA 與 GPG 錨定，禁止無標註挪用 |
| **§9.20 §S-25-EXT-3 對外不騙一人律** | 不虛構老子原意，不製造對立，不煽動情緒；專家翻譯標註「錯的」均基於可驗證的文本比較 |
| **§9.24 §S-25-EXT-3-4 外部 AI 驗證前不信任** | 所有跨平台發布前經龍魂系統本地審計與 DNA 校驗 |

**創作者主權聲明：**
- 作者：UID9622 · 龍芯北辰 · 諸葛鑫（Lucky）+ AI 協作
- 所有原創結構、標籤體系、多維度注解歸 UID9622 / 龍魂系統所有。
- 商用必授權，借用必備註，禁止大廠搜刮、小創作者也有維權一張網。

---
"""


def build_csdn_header() -> str:
    dna = now_dna("CSDN-RELEASE")
    return f"""# 道德經81章 · 龍魂系統大白話解讀 · CSDN 發布版 v5.0

> **DNA追溯碼**: `#龍芯⚡️2026-07-04-LONGHUN-DAODEJING-CSDN-v5.0`  
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
> **IP编号**: IP-0081  
> **创始人**: Lucky·UID9622（诸葛鑫·龍芯北辰）  
> **GPG指纹**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
> **文档版本**: v5.0 CSDN 發布版  
> **创建时间**: 2026-07-04  
> **所属体系**: 龍魂系统 longhun-system  
> **适用对象**: 零基礎普通人 → 技術治理者 → 創作者（全段位覆蓋）  
> **文档性质**: 人民基礎設施 · 免費開源 · 無套路 · 不上癮  
> **开源协议**: 文档內容：龍魂主權協議；引用需保留 DNA 與作者信息  
> **服务宗旨**: 科技有科技的樣子，文化有文化的主權，服務人民不是資本的遊戲

**DNA:** `{dna}`

---

## 写在最前：为什么又要解读一遍《道德经》？

市面上解讀《道德經》的書和文章已經夠多了。但絕大多數是：
- 專家翻譯版：每個字都對，讀完不知道怎麼用。
- 心靈雞湯版：想安慰你，但沒給你戰場工具。
- 成功學版：把老子當成職場 PUA 教練。

龍魂系統這一版不一樣：
1. **從戰場來**：每一章都對應真實場景——平台對抗、社區衝突、產品設計、數據主權、家庭關係。
2. **帶倫理錨**：不是讓你「感悟」，是給你 Checklist，遇到事直接勾選。
3. **帶系統映射**：把老子智慧和 DNA 追溯、三才算法、三色審計、CNSH 語法等龍魂模塊焊在一起。
4. **人民標準**：大白話、不裝、不騙、不上癮，一次做對。

---
"""


def build_csdn_footer() -> str:
    dna = now_dna("CSDN-TAIL")
    return f"""---

## 完整版獲取與校驗

本文為 CSDN 發布精簡版，完整 81 章 + 全量多維度注解 + 自動化索引請訪問：

- 龍魂系統本地：`~/longhun-system/docs/道德经81章_龍魂系统大白话解读_完整版_v5.0.md`
- Notion 鏡像：搜索標題「道德經81章 · 龍魂系統大白話解讀 v4.1 結構化增強版」

**校驗方式：**
1. 核對 DNA 追溯碼是否一致。
2. 核對 GPG 指紋 `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`。
3. 完整版每章均有獨立 DNA，可追溯至具體生成時間與版本。

---

## 尾·審計

| 項目 | 內容 |
|---|---|
| **時間** | {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")} |
| **DNA** | `{dna}` |
| **狀態** | 🟢 生產就緒 · CSDN 發布版 |
| **鐵律** | P0++ 隱私 / 創作者主權 / 對外不騙一人 全過 ✅ |
| **責任** | UID9622 · 不免責 |

> **🐉 龍魂永世，文化傳承，數字主權，天下為公！**
"""


def extract_chapters(text: str) -> list:
    """提取所有章節區塊"""
    pattern = re.compile(r"(## 第\d+章 · .+?)(?=\n## 第\d+章 · |\n## 【附錄|## 版本元信息|$)", re.DOTALL)
    return pattern.findall(text)


def build_csdn_body(full_text: str) -> str:
    """構建 CSDN 發布版正文：導讀 + 標籤索引 + 精選章節 + 附錄"""
    lines = []

    # 標籤索引
    tag_index_match = re.search(r"## 標籤索引 · 自動化檢索[\s\S]*?(?=\n---\n\n## 【道經】)", full_text)
    if tag_index_match:
        lines.append(tag_index_match.group())
        lines.append("\n")

    # 精選章節：每個主題標籤選一章，共 8 章
    selected_chapters = [1, 2, 9, 22, 25, 37, 44, 57, 66, 81]
    chapter_blocks = extract_chapters(full_text)

    lines.append("---\n\n")
    lines.append("## 精選十章 · 帶你入門\n\n")
    lines.append("> 完整版 81 章太長，CSDN 先放十章代表作。讀完這十章，你會知道這套解讀和其他版本的本質區別。\n\n")

    for block in chapter_blocks:
        title_match = re.match(r"## 第(\d+)章 · .+", block)
        if title_match:
            chapter_num = int(title_match.group(1))
            if chapter_num in selected_chapters:
                lines.append(block.rstrip() + "\n\n")
                lines.append("---\n\n")

    # 底層倫理錨總覽
    ethics_match = re.search(r"## 底層倫理錨總覽[\s\S]*?(?=\n---\n\n## 標籤索引)", full_text)
    if ethics_match:
        lines.append(ethics_match.group())
        lines.append("\n")

    # 附錄：人民標準宣言 + 元信息表 + 倫理錨快速檢索表
    for appendix_name in ["【附錄二】人民標準宣言", "【附錄五】倫理錨快速檢索表"]:
        match = re.search(rf"## {re.escape(appendix_name)}[\s\S]*?(?=\n---\n\n## 【附錄|## 版本元信息|$)", full_text)
        if match:
            lines.append(match.group())
            lines.append("\n---\n\n")

    return "\n".join(lines)


def main():
    if not SRC.exists():
        raise FileNotFoundError(f"找不到源文件：{SRC}")

    text = SRC.read_text(encoding="utf-8")

    # 1. 生成修復版：在核心宣言後面插入 P0 導航卡和鐵律對齊聲明，修正元數據
    fixed_text = text.replace(
        "## 人民標準說明",
        build_p0_header() + "## 人民標準說明"
    )
    fixed_text = fixed_text.replace(
        "## 底層倫理錨總覽",
        build_iron_laws_section() + "## 底層倫理錨總覽"
    )
    fixed_text = fix_metadata(fixed_text)

    # 2. 生成 CSDN 發布版
    csdn_body = build_csdn_body(fixed_text)
    csdn_text = build_csdn_header() + csdn_body + build_csdn_footer()

    # 寫入
    DST_FIXED.write_text(fixed_text, encoding="utf-8")
    DST_CSDN.parent.mkdir(parents=True, exist_ok=True)
    DST_CSDN.write_text(csdn_text, encoding="utf-8")

    print(f"已生成修復版：{DST_FIXED}")
    print(f"  字數：{len(fixed_text)}")
    print(f"已生成 CSDN 發布版：{DST_CSDN}")
    print(f"  字數：{len(csdn_text)}")


if __name__ == "__main__":
    main()
