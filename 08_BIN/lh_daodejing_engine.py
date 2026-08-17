#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·丙申·戊申·䷗复-DAODEJING-ENGINE-v2.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# CREATOR: 诸葛鑫 (UID9622)
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂·道德经知识引擎 v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
可编程、可查询、可分析的81章道德经龍魂解读引擎。
底座焊死：蚁群定锚 + 五行生克 + 三六九不动点 + DNA全链路追溯。
向上兼容 lh_daodejing_anchor.py（场景定锚器）提供语义搜索。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

功能：
  ✅ 解析 v5.0 Markdown 完整81章数据
  ✅ 多维度查询：章号/关键词/标签/卦象/生肖/三六九
  ✅ 蚁群定锚：场景→最相关章节（联动 anchor 引擎）
  ✅ 统计分析：标签分布/卦象覆盖/标签共现
  ✅ 导出：JSON / CSV / 快速参考卡
  ✅ 底座焊死：DNA/GPG/五行/卦象/时间戳

用法:
    python3 bin/lh_daodejing_engine.py --chapter 1
    python3 bin/lh_daodejing_engine.py --search "资本"
    python3 bin/lh_daodejing_engine.py --tag "数据主权"
    python3 bin/lh_daodejing_engine.py --anchor "数据最小化做减法"
    python3 bin/lh_daodejing_engine.py --stats
    python3 bin/lh_daodejing_engine.py --export-json daodejing.json
"""

import hashlib
import json
import csv
import re
import os
import sys
import time as _time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict

# ── 龍魂底座常量 ──────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DNA = "#龍芯⚡️丙午·丙申·戊申·䷗复-DAODEJING-ENGINE-v2.0-UID9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
VERSION = "v2.0"

# 底座焊死数据 — 五行 + 三六九 + 六十四卦
WUXING_SX = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}   # 相生
WUXING_XK = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}   # 相克
DR_WUXING = {1: "水", 6: "水",  2: "火", 7: "火",  3: "木", 8: "木",  4: "金", 9: "金",  5: "土"}  # 数字根→五行

# 默认数据文件
DEFAULT_DATA = str(ROOT / "12_DOCS" / "道德经81章_龍魂系统大白话解读_完整版_v5.0.md")

# ── 数据结构 ──────────────────────────────────────
@dataclass
class ChapterData:
    """单章全量数据结构"""
    chapter: int
    title: str
    dna: str = ""
    judge_dna: str = ""
    annotate_dna: str = ""
    original_text: str = ""
    expert_translation: str = ""
    actual_meaning: str = ""
    yijing_hexagram: str = ""
    sanliujiu: str = ""
    zodiac: str = ""
    when_to_use: str = ""
    plain_text: str = ""
    judgments: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    modern_guideline: str = ""
    # 多维度注解
    anchor_human: str = ""          # 人性锚点
    anchor_experience: str = ""     # UID9622经历映射
    anchor_system: str = ""         # 龍魂系统映射
    anchor_checklist: str = ""      # 伦理应用场景
    # 数字根预计算
    chapter_dr: int = 0             # 章号数字根
    chapter_wuxing: str = ""        # 章号五行


# ── 核心引擎 ──────────────────────────────────────
class DaodejingEngine:
    """道德经·龍魂知识引擎 v2.0"""

    DNA = DNA
    CONFIRM = CONFIRM
    GPG = GPG_FINGERPRINT

    def __init__(self):
        self.chapters: Dict[int, ChapterData] = {}
        self.tags_index: Dict[str, List[int]] = defaultdict(list)        # 标签→章号
        self.zodiac_index: Dict[str, List[int]] = defaultdict(list)      # 生肖→章号
        self.hexagram_index: Dict[str, List[int]] = defaultdict(list)    # 卦象→章号
        self.sanliujiu_index: Dict[str, List[int]] = defaultdict(list)   # 三六九→章号
        self.wuxing_index: Dict[str, List[int]] = defaultdict(list)      # 五行→章号
        self.tag_chapter_map: Dict[str, List[int]] = {}                  # v5.0标签索引(从md解析)
        self._loaded = False
        self._anchor_engine = None
        self._anchor_available = False

    # ═══════════════════════════════════════════════
    # 底座工具
    # ═══════════════════════════════════════════════
    @staticmethod
    def digital_root(n: int) -> int:
        """洛书九宫数字根: 1-9循环。369不动点焊死。"""
        return 1 + ((n - 1) % 9)

    @staticmethod
    def sanliujiu_phase(dr: int) -> str:
        """三六九相位判定"""
        return {1: "稳点", 2: "变点", 0: "极点"}.get(dr % 3, "稳点")

    @staticmethod
    def wuxing_of_dr(dr: int) -> str:
        """数字根→五行映射"""
        return DR_WUXING.get(dr, "土")

    @staticmethod
    def text_dr(text: str) -> int:
        """文本→数字根（Unicode码点和取模）"""
        return DaodejingEngine.digital_root(sum(ord(c) for c in text))

    def _get_anchor_engine(self):
        """延迟加载场景定锚器"""
        if self._anchor_engine is None:
            try:
                sys.path.insert(0, str(ROOT / "08_BIN"))
                from lh_daodejing_anchor import CNSH_道德经定锚器
                self._anchor_engine = CNSH_道德经定锚器()
                self._anchor_available = True
            except Exception:
                self._anchor_available = False
        return self._anchor_engine

    # ═══════════════════════════════════════════════
    # 数据加载
    # ═══════════════════════════════════════════════
    def load(self, filepath: str = DEFAULT_DATA) -> int:
        """加载v5.0 Markdown数据文件"""
        content = Path(filepath).read_text(encoding='utf-8')
        return self.load_text(content)

    def load_text(self, content: str) -> int:
        """从文本加载81章数据"""
        # 1. 先解析标签索引
        self._parse_tag_index(content)
        # 2. 解析所有章节
        chapters = self._parse_all_chapters(content)
        # 3. 补全标签（优先用v5.0索引，其次用内容推断兜底）
        self._assign_tags(chapters)
        # 4. 构建索引
        self._build_indices(chapters)
        self._loaded = True
        return len(chapters)

    def _parse_tag_index(self, content: str):
        """从v5.0标签索引表解析标签→章号映射"""
        self.tag_chapter_map.clear()
        idx_match = re.search(
            r'## 標籤索引[^\n]*\n+.*?\n(.*?)(?=\n\n>|\n\n---)',
            content, re.DOTALL
        )
        if not idx_match:
            return
        table = idx_match.group(1)
        for line in table.split('\n'):
            m = re.match(r'\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|', line)
            if not m:
                continue
            tag, ch_list = m.group(1), m.group(2)
            nums = [int(n) for n in re.findall(r'第(\d+)章', ch_list)]
            self.tag_chapter_map[tag] = nums

    def _parse_all_chapters(self, content: str) -> Dict[int, ChapterData]:
        """解析所有81章"""
        chapters: Dict[int, ChapterData] = {}

        # 按 ## 第N章 分割
        blocks = re.split(r'\n(?=## 第\d+章 ·)', content)
        for block in blocks:
            m = re.match(r'## 第(\d+)章 · (.+)', block)
            if not m:
                continue
            ch_num = int(m.group(1))
            ch_title = m.group(2).strip()
            data = self._parse_chapter(ch_num, ch_title, block)
            if data:
                chapters[ch_num] = data
        return chapters

    def _parse_chapter(self, num: int, title: str, block: str) -> Optional[ChapterData]:
        """解析单章"""
        try:
            # DNA
            dna_m = re.search(r'\*\*DNA:\*\*\s*`([^`]+)`', block)
            dna = dna_m.group(1) if dna_m else ""

            # 大白話翻譯表格 — 按 | 項目 | 內容 | 结构解析
            table = {}
            in_table = False
            for line in block.split('\n'):
                line = line.strip()
                if re.match(r'\|\s*項目\s*\|\s*內容\s*\|', line):
                    in_table = True
                    continue
                if in_table and re.match(r'\|[-:]+\|[-:]+\|', line):
                    continue
                if in_table:
                    m = re.match(r'\|\s*\**(.+?)\**\s*\|\s*(.+?)\s*\|', line)
                    if m:
                        key = re.sub(r'\*|<[^>]+>', '', m.group(1)).strip()
                        val = m.group(2).strip()
                        table[key] = val
                    else:
                        in_table = False

            # 核心判斷
            judgments = []
            judge_section = re.search(
                r'### 核心判斷[^\n]*\n+(.*?)(?=\n\*\*DNA追溯.*?:|$)', block, re.DOTALL
            )
            if judge_section:
                for line in judge_section.group(1).split('\n'):
                    line = line.strip()
                    if line and re.match(r'^\d+\.', line):
                        judgments.append(re.sub(r'^\d+\.\s*', '', line))

            judge_dna = ""
            jdna_m = re.search(r'\*\*DNA追溯:\*\*\s*`([^`]+)`', block)
            if jdna_m:
                judge_dna = jdna_m.group(1)

            # 一句话指南
            guideline = ""
            gl_m = re.search(
                r'现代战场一句话指南\*\*\n*>\s*(.+?)(?:\n|$)', block
            )
            if gl_m:
                guideline = gl_m.group(1).strip()

            # 多维度注解子段
            anchors = {}
            anchor_patterns = [
                ("人性锚点", r'#### 人性锚点\n+(.*?)(?=\n####|\n\*\*DNA追溯|\n---|$)'),
                ("UID9622经历映射", r'#### UID9622 经历映射\n+(.*?)(?=\n####|\n\*\*DNA追溯|\n---|$)'),
                ("龍魂系统映射", r'#### 龍魂系统映射\n+(.*?)(?=\n####|\n\*\*DNA追溯|\n---|$)'),
                ("伦理应用场景", r'#### 伦理应用场景 Checklist\n+(.*?)(?=\n####|\n\*\*DNA追溯|\n---|$)'),
            ]
            for akey, apat in anchor_patterns:
                am = re.search(apat, block, re.DOTALL)
                if am:
                    anchors[akey] = am.group(1).strip()

            annotate_dna = ""
            adna_m = list(re.finditer(r'\*\*DNA追溯:\*\*\s*`([^`]+)`', block))
            if len(adna_m) >= 2:
                annotate_dna = adna_m[1].group(1)

            # 数字根预计算
            ch_dr = self.digital_root(num)
            ch_wx = self.wuxing_of_dr(ch_dr)

            return ChapterData(
                chapter=num,
                title=title,
                dna=dna,
                judge_dna=judge_dna,
                annotate_dna=annotate_dna,
                original_text=table.get("原文", ""),
                expert_translation=table.get("專家怎麼翻譯的錯的", ""),
                actual_meaning=table.get("老子實際想說什麼對的", ""),
                yijing_hexagram=table.get("易經卦象", ""),
                sanliujiu=table.get("三六九", ""),
                zodiac=table.get("生肖", ""),
                when_to_use=table.get("什麼時候用", ""),
                plain_text=table.get("大白話", ""),
                judgments=judgments,
                modern_guideline=guideline,
                anchor_human=anchors.get("人性锚点", ""),
                anchor_experience=anchors.get("UID9622经历映射", ""),
                anchor_system=anchors.get("龍魂系统映射", ""),
                anchor_checklist=anchors.get("伦理应用场景", ""),
                chapter_dr=ch_dr,
                chapter_wuxing=ch_wx,
            )
        except Exception as e:
            print(f"⚠️ 解析第{num}章失败: {e}", file=sys.stderr)
            return None

    def _assign_tags(self, chapters: Dict[int, ChapterData]):
        """标签分配：优先v5.0索引，其次内容推断"""
        for num, data in chapters.items():
            # 从v5.0索引获取
            tags = []
            for tag, ch_list in self.tag_chapter_map.items():
                if num in ch_list:
                    tags.append(tag)
            if tags:
                data.tags = sorted(tags)
                continue
            # 兜底：关键词推断
            data.tags = self._infer_tags(data)

    def _infer_tags(self, data: ChapterData) -> List[str]:
        """关键词兜底标签推断"""
        text = f"{data.title} {data.plain_text} {data.actual_meaning}"
        tag_kw = {
            "资本与平台": ["资本", "平台", "垄断", "剥削", "韭菜"],
            "流量与AI": ["流量", "AI", "算法", "推荐", "模型"],
            "数据主权": ["数据", "主权", "隐私", "安全", "合规"],
            "社区与家庭": ["社区", "家庭", "关系", "亲人", "朋友", "邻里"],
            "创业与产品": ["创业", "产品", "市场", "用户", "需求", "迭代"],
            "维权与取证": ["维权", "取证", "证据", "纠纷", "诉讼"],
            "技术与开源": ["技术", "开源", "代码", "框架", "生态"],
            "个人修养": ["修养", "修行", "内心", "自知", "情绪", "心态"],
        }
        return sorted([t for t, kws in tag_kw.items() if any(kw in text for kw in kws)] or ["个人修养"])

    def _build_indices(self, chapters: Dict[int, ChapterData]):
        """构建多维索引"""
        self.chapters = chapters
        self.tags_index.clear()
        self.zodiac_index.clear()
        self.hexagram_index.clear()
        self.sanliujiu_index.clear()
        self.wuxing_index.clear()

        for num, data in chapters.items():
            for tag in data.tags:
                self.tags_index[tag].append(num)
            if data.zodiac:
                self.zodiac_index[data.zodiac].append(num)
            if data.yijing_hexagram:
                h = data.yijing_hexagram.split("·")[0].strip()  # "乾卦·天行健"→"乾卦"
                self.hexagram_index[h].append(num)
                self.hexagram_index[data.yijing_hexagram].append(num)
            if data.sanliujiu:
                self.sanliujiu_index[data.sanliujiu].append(num)
            if data.chapter_wuxing:
                self.wuxing_index[data.chapter_wuxing].append(num)

    # ═══════════════════════════════════════════════
    # 查询 API
    # ═══════════════════════════════════════════════
    def get(self, num: int) -> Optional[ChapterData]:
        """按章号获取"""
        return self.chapters.get(num)

    def search_keyword(self, kw: str) -> List[Tuple[int, str, float]]:
        """关键词搜索（返回章号+标题+相关性分数）"""
        results = []
        kw_lo = kw.lower()
        for num, d in self.chapters.items():
            search_text = f"{d.title} {d.plain_text} {d.actual_meaning} {' '.join(d.judgments)} {d.modern_guideline}"
            count = search_text.lower().count(kw_lo)
            if count > 0:
                # 标题命中加权
                title_hit = 2.0 if kw_lo in d.title.lower() else 1.0
                results.append((num, d.title, count * title_hit))
        results.sort(key=lambda x: -x[2])
        return results

    def search_tag(self, tag: str) -> List[int]:
        """按标签搜索"""
        return sorted(self.tags_index.get(tag, []))

    def search_zodiac(self, z: str) -> List[int]:
        """按生肖搜索"""
        return sorted(self.zodiac_index.get(z, []))

    def search_hexagram(self, h: str) -> List[int]:
        """按卦象搜索"""
        return sorted(self.hexagram_index.get(h, []))

    def search_sanliujiu(self, phase: str) -> List[int]:
        """按三六九搜索"""
        return sorted(self.sanliujiu_index.get(phase, []))

    def search_wuxing(self, wx: str) -> List[int]:
        """按五行搜索"""
        return sorted(self.wuxing_index.get(wx, []))

    def anchor(self, scene: str) -> Optional[Dict]:
        """蚁群定锚：场景→最相关章节（联动 anchor 引擎）"""
        engine = self._get_anchor_engine()
        if not engine or not self._anchor_available:
            # 兜底：关键词搜索结果第一条
            results = self.search_keyword(scene)
            if results:
                num = results[0][0]
                ch = self.get(num)
                return {"chapter": num, "title": ch.title if ch else "", "method": "keyword_fallback"}
            return None
        result = engine.定锚(scene)
        if "error" in result:
            return None
        return {
            "chapter": result["章"],
            "anchor_sentence": result["锚句"],
            "dr": result["dr"],
            "wuxing": result["五行"],
            "sanliujiu": result["三六九"],
            "method": "ant_colony",
        }

    def match_by_wuxing(self, target_wx: str) -> List[Tuple[int, str, str]]:
        """五行匹配：相生>相同>其他（返回排序后的章节列表）"""
        scored = []
        for num, d in self.chapters.items():
            ch_wx = d.chapter_wuxing
            if ch_wx == target_wx:
                scored.append((num, d.title, "同", 3))
            elif WUXING_SX.get(target_wx) == ch_wx:
                scored.append((num, d.title, "我生", 2))
            elif WUXING_SX.get(ch_wx) == target_wx:
                scored.append((num, d.title, "生我", 2))
            elif WUXING_XK.get(target_wx) == ch_wx:
                scored.append((num, d.title, "我克", 1))
            elif WUXING_XK.get(ch_wx) == target_wx:
                scored.append((num, d.title, "克我", 0))
            else:
                scored.append((num, d.title, "无关", 1))
        scored.sort(key=lambda x: -x[3])
        return [(n, t, r) for n, t, r, _ in scored]

    def get_all_tags(self) -> List[str]:
        """所有标签"""
        return sorted(self.tags_index.keys())

    def get_statistics(self) -> Dict:
        """统计信息"""
        return {
            "total_chapters": len(self.chapters),
            "unique_tags": len(self.tags_index),
            "tag_counts": dict(sorted({t: len(v) for t, v in self.tags_index.items()}.items(), key=lambda x: -x[1])),
            "zodiac_counts": dict(sorted({z: len(v) for z, v in self.zodiac_index.items()}.items(), key=lambda x: -x[1])),
            "hexagram_counts": dict(sorted({h: len(v) for h, v in self.hexagram_index.items() if "·" not in h}.items(), key=lambda x: -x[1])),
            "sanliujiu_dist": {p: len(v) for p, v in self.sanliujiu_index.items()},
            "wuxing_dist": {wx: len(v) for wx, v in self.wuxing_index.items()},
        }

    def tag_cooccurrence(self, top_n: int = 20) -> List[Tuple[str, str, int]]:
        """标签共现分析"""
        cooc = defaultdict(int)
        for d in self.chapters.values():
            tags = d.tags
            for i in range(len(tags)):
                for j in range(i + 1, len(tags)):
                    key = tuple(sorted([tags[i], tags[j]]))
                    cooc[key] += 1
        return [(t1, t2, c) for (t1, t2), c in sorted(cooc.items(), key=lambda x: -x[1])[:top_n]]

    # ═══════════════════════════════════════════════
    # 导出
    # ═══════════════════════════════════════════════
    def export_json(self, filepath: str, include_full: bool = True):
        """导出JSON"""
        data = []
        for num in sorted(self.chapters.keys()):
            ch = self.chapters[num]
            entry = {
                "chapter": ch.chapter,
                "title": ch.title,
                "dna": ch.dna,
                "plain_text": ch.plain_text,
                "actual_meaning": ch.actual_meaning,
                "yijing_hexagram": ch.yijing_hexagram,
                "sanliujiu": ch.sanliujiu,
                "zodiac": ch.zodiac,
                "chapter_dr": ch.chapter_dr,
                "chapter_wuxing": ch.chapter_wuxing,
                "tags": ch.tags,
                "modern_guideline": ch.modern_guideline,
                "judgments": ch.judgments,
            }
            if include_full:
                entry.update({
                    "original_text": ch.original_text,
                    "expert_translation": ch.expert_translation,
                    "when_to_use": ch.when_to_use,
                    "anchor_human": ch.anchor_human,
                    "anchor_experience": ch.anchor_experience,
                    "anchor_system": ch.anchor_system,
                    "anchor_checklist": ch.anchor_checklist,
                })
            data.append(entry)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({
                "meta": {
                    "dna": DNA, "confirm": CONFIRM, "gpg": GPG_FINGERPRINT,
                    "version": VERSION,
                    "generated_at": datetime.now().isoformat(),
                    "total_chapters": len(data),
                    "source": "道德经81章_龍魂系统大白话解读_完整版_v5.0.md",
                },
                "chapters": data,
            }, f, ensure_ascii=False, indent=2)

    def export_csv(self, filepath: str):
        """导出CSV"""
        fields = ['chapter', 'title', 'dna', 'plain_text', 'yijing_hexagram',
                   'sanliujiu', 'zodiac', 'chapter_wx', 'tags', 'modern_guideline', 'judgments_count']
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for num in sorted(self.chapters.keys()):
                ch = self.chapters[num]
                w.writerow({
                    'chapter': ch.chapter, 'title': ch.title, 'dna': ch.dna,
                    'plain_text': ch.plain_text[:120] + "...",
                    'yijing_hexagram': ch.yijing_hexagram,
                    'sanliujiu': ch.sanliujiu, 'zodiac': ch.zodiac,
                    'chapter_wx': ch.chapter_wuxing,
                    'tags': ','.join(ch.tags),
                    'modern_guideline': ch.modern_guideline[:80] if ch.modern_guideline else "",
                    'judgments_count': len(ch.judgments),
                })

    def export_refcard(self, filepath: str):
        """导出快速参考卡"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# 🐉 龍魂·道德经快速参考卡\n\n")
            f.write(f"DNA: {DNA}\n\n")
            f.write("| 章 | 标题 | 一句话指南 | 卦象 | 五行 | 生肖 | 三六九 | 标签 |\n")
            f.write("|:---:|:---|:---|:---|:---:|:---:|:---:|:---|\n")
            for num in sorted(self.chapters.keys()):
                ch = self.chapters[num]
                gl = ch.modern_guideline[:40] + "..." if len(ch.modern_guideline) > 40 else ch.modern_guideline
                f.write(f"| {num} | {ch.title} | {gl} | {ch.yijing_hexagram} | "
                        f"{ch.chapter_wuxing} | {ch.zodiac} | {ch.sanliujiu} | {','.join(ch.tags[:2])} |\n")
            f.write(f"\n---\nDNA: {DNA}\n")

    # ═══════════════════════════════════════════════
    # 打印
    # ═══════════════════════════════════════════════
    def print_chapter(self, num: int):
        """打印单章摘要"""
        ch = self.get(num)
        if not ch:
            print(f"❌ 第{num}章不存在", file=sys.stderr)
            return
        print(f"\n{'═'*64}")
        print(f" 第{ch.chapter}章 · {ch.title}")
        print(f"{'═'*64}")
        print(f"  DNA: {ch.dna}")
        print(f"  📖 大白话: {ch.plain_text[:200]}{'...' if len(ch.plain_text) > 200 else ''}")
        print(f"  🔮 {ch.yijing_hexagram} │ 🐉 {ch.zodiac} │ {ch.sanliujiu} │ 五行:{ch.chapter_wuxing} │ DR:{ch.chapter_dr}")
        print(f"  🏷️  {', '.join(ch.tags)}")
        if ch.modern_guideline:
            print(f"  💡 {ch.modern_guideline}")
        if ch.judgments:
            print(f"  📋 核心判断:")
            for j in ch.judgments[:5]:
                print(f"     • {j}")
        if ch.anchor_system:
            print(f"  🔗 龍魂映射: {ch.anchor_system[:120]}...")
        print(f"{'═'*64}")

    def print_anchor_result(self, scene: str, result: Dict):
        """打印定锚结果"""
        print(f"\n🐉 场景定锚: {scene}")
        print(f"  → 第{result['chapter']}章「{result.get('anchor_sentence', '')}」")
        print(f"  方法: {result['method']} │ DR:{result.get('dr','')} │ 五行:{result.get('wuxing','')} │ {result.get('sanliujiu','')}")
        if 'chapter' in result:
            self.print_chapter(result['chapter'])

    def print_stats(self):
        """打印统计信息"""
        s = self.get_statistics()
        print(f"\n{'═'*48}")
        print(f" 🐉 道德经知识引擎 {VERSION} 统计")
        print(f"{'═'*48}")
        print(f"  总章数: {s['total_chapters']}/81")
        print(f"  标签数: {s['unique_tags']}")
        print(f"\n  📊 标签分布:")
        for tag, cnt in s['tag_counts'].items():
            bar = '█' * (cnt // 2)
            print(f"    {tag:　<12s} {bar} {cnt}")
        print(f"\n  🐉 生肖分布: {', '.join(f'{z}({c})' for z,c in sorted(s['zodiac_counts'].items()))}")
        print(f"  三六九: {s['sanliujiu_dist']}")
        print(f"  五行: {s['wuxing_dist']}")
        print(f"{'═'*48}")


# ═════════════════════════════════════════════════════
# 命令行
# ═════════════════════════════════════════════════════
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description=f"🐉 龍魂·道德经知识引擎 v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
DNA: {DNA}
底座: 蚁群定锚 · 五行生克 · 三六九不动点 · DNA全链路追溯

══════════════════════════════════════
示例：
  lh ddj -c 1                     查看第1章
  lh ddj -s "资本"                搜索关键词
  lh ddj -t "数据主权"            按标签搜索
  lh ddj -a "数据最小化"          场景定锚
  lh ddj --stats                  统计信息
  lh ddj --export-json out.json   导出JSON
  lh ddj -W 水                    按五行搜索
  lh ddj --cooccur                标签共现
══════════════════════════════════════
        """
    )
    parser.add_argument("--load", "-l", default=DEFAULT_DATA, help="数据文件路径")
    parser.add_argument("--chapter", "-c", type=int, help="查看指定章节")
    parser.add_argument("--search", "-s", help="关键词搜索")
    parser.add_argument("--tag", "-t", help="按标签搜索")
    parser.add_argument("--zodiac", "-z", help="按生肖搜索")
    parser.add_argument("--hexagram", "-H", help="按卦象搜索")
    parser.add_argument("--sanliujiu", "-S", help="按三六九搜索（稳点/变点/极点）")
    parser.add_argument("--wuxing", "-W", help="按五行搜索（金水木火土）")
    parser.add_argument("--anchor", "-a", help="场景定锚→最相关章节")
    parser.add_argument("--stats", action="store_true", help="统计信息")
    parser.add_argument("--list-tags", action="store_true", help="列出所有标签")
    parser.add_argument("--cooccur", action="store_true", help="标签共现分析")
    parser.add_argument("--export-json", help="导出JSON")
    parser.add_argument("--export-csv", help="导出CSV")
    parser.add_argument("--export-ref", help="导出快速参考卡")
    parser.add_argument("--all-tags", nargs="+", help="多标签AND搜索")
    parser.add_argument("--guideline", "-g", help="按一句话指南搜索")

    args = parser.parse_args()

    # 加载数据
    engine = DaodejingEngine()
    data_path = args.load
    if not os.path.exists(data_path):
        print(f"❌ 数据文件不存在: {data_path}", file=sys.stderr)
        sys.exit(1)
    print(f"📖 加载: {data_path}")
    count = engine.load(data_path)
    print(f"✅ 加载完成: {count}/81 章")

    if count == 0:
        print("❌ 未解析到章节，请检查数据文件格式", file=sys.stderr)
        sys.exit(1)

    # 执行操作
    did_something = False

    if args.chapter:
        engine.print_chapter(args.chapter)
        did_something = True

    if args.search:
        results = engine.search_keyword(args.search)
        print(f"\n🔍 关键词「{args.search}」命中 {len(results)} 条:")
        for num, title, score in results[:20]:
            ch = engine.get(num)
            gl = f" — {ch.modern_guideline[:50]}..." if ch and ch.modern_guideline else ""
            print(f"  {num:>2}. {title} (相关度:{score:.1f}){gl}")
        did_something = True

    if args.tag:
        chs = engine.search_tag(args.tag)
        print(f"\n🏷️  标签「{args.tag}」→ {len(chs)} 章:")
        for n in chs:
            ch = engine.get(n)
            print(f"  {n:>2}. {ch.title}" if ch else f"  {n}")
        did_something = True

    if args.all_tags:
        # 多标签AND：取交集
        sets = [set(engine.search_tag(t)) for t in args.all_tags]
        inter = sets[0].intersection(*sets[1:]) if sets else set()
        tags_str = ' + '.join(args.all_tags)
        print(f"\n🏷️  标签「{tags_str}」(AND) → {len(inter)} 章:")
        for n in sorted(inter):
            ch = engine.get(n)
            print(f"  {n:>2}. {ch.title}" if ch else f"  {n}")
        did_something = True

    if args.zodiac:
        chs = engine.search_zodiac(args.zodiac)
        print(f"\n🐉 生肖「{args.zodiac}」→ {len(chs)} 章:")
        for n in chs:
            ch = engine.get(n)
            print(f"  {n:>2}. {ch.title}" if ch else f"  {n}")
        did_something = True

    if args.hexagram:
        chs = engine.search_hexagram(args.hexagram)
        print(f"\n🔮 卦象「{args.hexagram}」→ {len(chs)} 章:")
        for n in chs:
            ch = engine.get(n)
            print(f"  {n:>2}. {ch.title}" if ch else f"  {n}")
        did_something = True

    if args.sanliujiu:
        chs = engine.search_sanliujiu(args.sanliujiu)
        print(f"\n☯️  三六九「{args.sanliujiu}」→ {len(chs)} 章:")
        for n in chs:
            ch = engine.get(n)
            print(f"  {n:>2}. {ch.title}" if ch else f"  {n}")
        did_something = True

    if args.wuxing:
        chs = engine.search_wuxing(args.wuxing)
        print(f"\n🔥 五行「{args.wuxing}」→ {len(chs)} 章:")
        for n in chs:
            ch = engine.get(n)
            print(f"  {n:>2}. {ch.title}" if ch else f"  {n}")
        did_something = True

    if args.guideline:
        kw = args.guideline
        print(f"\n💡 一句话指南搜索「{kw}」:")
        for n in sorted(engine.chapters.keys()):
            ch = engine.get(n)
            if ch and kw in ch.modern_guideline:
                print(f"  {n:>2}. {ch.title} → {ch.modern_guideline}")
        did_something = True

    if args.anchor:
        result = engine.anchor(args.anchor)
        if result:
            engine.print_anchor_result(args.anchor, result)
        else:
            print(f"❌ 场景「{args.anchor}」定锚失败", file=sys.stderr)
        did_something = True

    if args.stats:
        engine.print_stats()
        did_something = True

    if args.list_tags:
        tags = engine.get_all_tags()
        print(f"\n🏷️  全部标签 ({len(tags)}):")
        for t in tags:
            print(f"  {t} ({len(engine.tags_index[t])}章)")
        did_something = True

    if args.cooccur:
        cooc = engine.tag_cooccurrence()
        print(f"\n🔗 标签共现 TOP 20:")
        for t1, t2, cnt in cooc:
            print(f"  {t1} ⟷ {t2}: {cnt}")
        did_something = True

    if args.export_json:
        engine.export_json(args.export_json)
        print(f"✅ JSON → {args.export_json}")
        did_something = True

    if args.export_csv:
        engine.export_csv(args.export_csv)
        print(f"✅ CSV → {args.export_csv}")
        did_something = True

    if args.export_ref:
        engine.export_refcard(args.export_ref)
        print(f"✅ 快速参考卡 → {args.export_ref}")
        did_something = True

    if not did_something:
        engine.print_chapter(1)
        print(f"\n💡 试试: lh ddj -s \"无为\" | lh ddj -t \"数据主权\" | lh ddj --stats")

    # ── 时间戳 ──
    print(f"\n🐉丙午·{_get_shichen()}·䷗复·🟢 {DNA}")


def _get_shichen() -> str:
    """简单时辰推算（完整版用 lh_time_engine）"""
    h = datetime.now().hour
    dz = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    return dz[((h + 1) // 2) % 12] + "时"


if __name__ == "__main__":
    main()
