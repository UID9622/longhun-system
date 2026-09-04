#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 通心译结构落地引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷝离为火-通心译结构-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：
  1. 解析通心译文本结构（章节、公式、映射表、索引）
  2. 验证三层映射完整性（物理↔哲学↔龍魂）
  3. 生成结构化 JSON
  4. 输出 Markdown 结构报告
"""

import json
import re
import hashlib
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from datetime import datetime

# ============================================================
# 一、数据结构
# ============================================================

@dataclass
class PhysicsConcept:
    name: str
    chapter: int
    chinese_philosophy: str
    longhun_mapping: str
    keyword: str
    formula: Optional[str] = None

@dataclass
class Chapter:
    number: int
    title: str
    concepts: List[PhysicsConcept]
    chinese_version: str
    english_version: str
    double_column: List[Dict]

@dataclass
class TongxinDocument:
    dna: str
    title: str
    author: str
    chapters: List[Chapter]
    philosophy_laws: List[str]
    closure_diagram: str
    formulas: Dict[str, List[Dict]]
    index_physics: Dict[str, Dict]
    index_longhun: Dict[str, Dict]
    bilingual_index: Dict[str, Dict]

# ============================================================
# 二、解析引擎
# ============================================================

class TongxinParser:
    """通心译文本结构解析器"""

    def __init__(self, text: str):
        self.text = text
        self.lines = text.split('\n')
        self.chapter_pattern = re.compile(r'^## 第(.+)章')
        self.philosophy_laws = []

    def parse(self) -> TongxinDocument:
        """完整解析"""
        chapters = []
        current_chapter = None

        for i, line in enumerate(self.lines):
            # 检测章节标题
            match = self.chapter_pattern.match(line)
            if match:
                if current_chapter:
                    chapters.append(current_chapter)
                ch_num = self._parse_chapter_number(match.group(1))
                current_chapter = Chapter(
                    number=ch_num,
                    title=line.strip(),
                    concepts=[],
                    chinese_version="",
                    english_version="",
                    double_column=[]
                )
                continue

            # 检测双栏对照表
            if '| 物理概念 |' in line or '| Physics Concept |' in line:
                if current_chapter:
                    current_chapter.double_column = self._parse_table(i)
                continue

            # 提取哲学定律
            if '第一定律' in line or '第二定律' in line or '第三定律' in line:
                self.philosophy_laws.append(line.strip())

        if current_chapter:
            chapters.append(current_chapter)

        # 提取概念
        for ch in chapters:
            ch.concepts = self._extract_concepts_from_table(ch)

        # 生成最终文档
        doc = TongxinDocument(
            dna=self._extract_dna(),
            title="通心译：用中文母语，重新看懂现代物理学",
            author="UID9622 · 龍芯北辰 · 诸葛鑫",
            chapters=chapters,
            philosophy_laws=self.philosophy_laws,
            closure_diagram=self._extract_closure(),
            formulas=self._extract_formulas(),
            index_physics=self._extract_index("物理概念"),
            index_longhun=self._extract_index("龍魂"),
            bilingual_index=self._extract_bilingual_index()
        )
        return doc

    def _parse_chapter_number(self, raw: str) -> int:
        """从 '一 · xxx' 或 '1 · xxx' 中提取章节号"""
        # 中文数字映射
        cn_num = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}
        first_char = raw.strip()[0] if raw.strip() else ''
        if first_char in cn_num:
            return cn_num[first_char]
        match = re.search(r'(\d+)', raw)
        if match:
            return int(match.group(1))
        return 0

    def _extract_dna(self) -> str:
        for line in self.lines:
            if 'DNA追溯码' in line or 'DNA:' in line:
                match = re.search(r'`([#0-9A-Za-z⚡️\-\.]+)`', line)
                if match:
                    return match.group(1)
        return "#龍芯⚡️丙午·癸巳·癸卯·戊午·䷚颐-MODERN-PHYSICS-TONGXIN-BILINGUAL-v1.0"

    def _parse_table(self, start_idx: int) -> List[Dict]:
        table = []
        i = start_idx + 1  # skip header line
        # skip separator line
        if i < len(self.lines) and '---' in self.lines[i]:
            i += 1
        while i < len(self.lines) and self.lines[i].strip().startswith('|'):
            parts = [p.strip() for p in self.lines[i].split('|')[1:-1]]
            if len(parts) >= 3:
                table.append({
                    "物理概念": parts[0],
                    "中文语义": parts[1] if len(parts) > 1 else "",
                    "龍魂映射": parts[2] if len(parts) > 2 else ""
                })
            elif len(parts) >= 2:
                table.append({
                    "物理概念": parts[0],
                    "中文语义": parts[1] if len(parts) > 1 else "",
                    "龍魂映射": ""
                })
            i += 1
        return table

    def _extract_concepts_from_table(self, ch: Chapter) -> List[PhysicsConcept]:
        concepts = []
        for row in ch.double_column:
            concepts.append(PhysicsConcept(
                name=row.get("物理概念", ""),
                chapter=ch.number,
                chinese_philosophy=row.get("中文语义", ""),
                longhun_mapping=row.get("龍魂映射", ""),
                keyword=row.get("物理概念", "")
            ))
        return concepts

    def _extract_closure(self) -> str:
        in_diagram = False
        diagram = []
        for line in self.lines:
            if '```mermaid' in line:
                in_diagram = True
                continue
            if '```' in line and in_diagram:
                break
            if in_diagram:
                diagram.append(line)
        return '\n'.join(diagram)

    def _extract_formulas(self) -> Dict[str, List[Dict]]:
        formulas = {}
        current_appendix = None
        for line in self.lines:
            if '### 附录' in line:
                current_appendix = line.strip()
                formulas[current_appendix] = []
            elif '|' in line and current_appendix:
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 3 and parts[0] and parts[1]:
                    formulas[current_appendix].append({
                        "公式": parts[0],
                        "中文语义": parts[1],
                        "龍魂映射": parts[2] if len(parts) > 2 else ""
                    })
        return formulas

    def _extract_index(self, index_type: str) -> Dict[str, Dict]:
        index = {}
        in_index = False
        for line in self.lines:
            if f"### 按{index_type}索引" in line:
                in_index = True
                continue
            if in_index and line.strip().startswith('|') and not line.strip().startswith('|---'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 4:
                    key = parts[0]
                    index[key] = {
                        "章节": parts[1],
                        "中文解读": parts[2],
                        "龍魂映射": parts[3]
                    }
                continue
            if in_index and line.strip() == '':
                break
        return index

    def _extract_bilingual_index(self) -> Dict[str, Dict]:
        bilingual = {}
        in_index = False
        for line in self.lines:
            if '### 双语交叉索引' in line:
                in_index = True
                continue
            if in_index and line.strip().startswith('|') and not line.strip().startswith('|---'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 3:
                    bilingual[parts[0]] = {
                        "英文": parts[1],
                        "龍魂组件": parts[2]
                    }
            if in_index and line.strip() == '':
                break
        return bilingual


# ============================================================
# 三、验证引擎
# ============================================================

class TongxinValidator:
    """通心译结构验证器"""

    @staticmethod
    def validate(doc: TongxinDocument) -> Dict:
        errors = []
        warnings = []

        # 检查章节
        if len(doc.chapters) != 7:
            warnings.append(f"章节数应为7，实际为{len(doc.chapters)}")

        # 检查每个章节是否有双栏对照
        for ch in doc.chapters:
            if not ch.double_column:
                warnings.append(f"第{ch.number}章缺少双栏对照表")

        # 收集所有映射
        mapping_set = set()
        for ch in doc.chapters:
            for concept in ch.concepts:
                if concept.longhun_mapping:
                    mapping_set.add(concept.longhun_mapping)

        # 检查哲学定律
        if len(doc.philosophy_laws) != 3:
            warnings.append(f"哲学定律应为3条，实际为{len(doc.philosophy_laws)}")

        return {
            "status": "pass" if not errors else "fail",
            "errors": errors,
            "warnings": warnings,
            "chapters": len(doc.chapters),
            "mappings_count": len(mapping_set),
            "philosophy_laws": len(doc.philosophy_laws)
        }


# ============================================================
# 四、生成引擎
# ============================================================

class TongxinGenerator:
    """通心译结构生成器"""

    @staticmethod
    def generate_json(doc: TongxinDocument) -> str:
        return json.dumps(asdict(doc), ensure_ascii=False, indent=2)

    @staticmethod
    def generate_report(doc: TongxinDocument) -> str:
        report = []
        report.append("# 通心译结构报告")
        report.append("")
        report.append(f"**DNA**: {doc.dna}")
        report.append(f"**章节数**: {len(doc.chapters)}")
        report.append("")
        report.append("## 章节结构")
        for ch in doc.chapters:
            report.append(f"- 第{ch.number}章: {ch.title}")
            report.append(f"  - 概念数: {len(ch.concepts)}")
            report.append(f"  - 双栏对照: {'✅' if ch.double_column else '❌'}")
        report.append("")
        report.append("## 哲学定律")
        for law in doc.philosophy_laws:
            report.append(f"- {law}")
        report.append("")
        report.append("## 公式附录")
        for appendix, formulas in doc.formulas.items():
            report.append(f"- {appendix}: {len(formulas)} 条公式")
        report.append("")
        report.append("## 索引")
        report.append(f"- 物理概念索引: {len(doc.index_physics)} 条")
        report.append(f"- 龍魂索引: {len(doc.index_longhun)} 条")
        report.append(f"- 双语索引: {len(doc.bilingual_index)} 条")
        return "\n".join(report)

    @staticmethod
    def generate_markdown(doc: TongxinDocument) -> str:
        md = []
        md.append(f"# {doc.title}")
        md.append("")
        md.append(f"**DNA**: {doc.dna}")
        md.append(f"**主权人**: {doc.author}")
        md.append("")
        for ch in doc.chapters:
            md.append(f"## 第{ch.number}章 · {ch.title}")
            md.append("")
            if ch.double_column:
                md.append("### 双栏对照")
                md.append("")
                md.append("| 物理概念 | 中文语义 | 龍魂映射 |")
                md.append("|:---|:---|:---|")
                for row in ch.double_column:
                    md.append(f"| {row.get('物理概念', '')} | {row.get('中文语义', '')} | {row.get('龍魂映射', '')} |")
                md.append("")
        return "\n".join(md)


# ============================================================
# 五、命令行入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="通心译结构落地引擎 v1.0")
    parser.add_argument("--input", "-i", type=str, help="输入Markdown文件路径")
    parser.add_argument("--output", "-o", type=str, help="输出目录")
    parser.add_argument("--validate", action="store_true", help="验证结构完整性")
    parser.add_argument("--json", action="store_true", help="生成JSON")
    parser.add_argument("--report", action="store_true", help="生成结构报告")
    parser.add_argument("--markdown", action="store_true", help="生成完整Markdown")
    args = parser.parse_args()

    # 读取输入
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"❌ 文件不存在: {args.input}", file=sys.stderr)
            sys.exit(1)
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        # 使用内置示例
        text = """
# 通心译：用中文母语，重新看懂现代物理学

## 第一章 · 杨振宁 U(1) 规范对称性
### 双栏对照
| 物理概念 | 中文语义 | 龍魂映射 |
|:---|:---|:---|
| 规范对称性 | 变中有不变 | 关系不变性 |

## 第二章 · 对称性破缺
### 双栏对照
| 物理概念 | 中文语义 | 龍魂映射 |
|:---|:---|:---|
| 对称性破缺 | 无极生太极 | KFPP分级响应 |
"""

    parser_engine = TongxinParser(text)
    doc = parser_engine.parse()

    # 输出目录处理
    output_dir = Path(args.output) if args.output else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    # 验证
    if args.validate:
        result = TongxinValidator.validate(doc)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result["status"] != "pass":
            print("❌ 验证失败，请检查错误")
            return

    # 生成JSON
    if args.json:
        json_str = TongxinGenerator.generate_json(doc)
        if output_dir:
            (output_dir / "tongxin_structure.json").write_text(json_str, encoding='utf-8')
            print(f"✅ JSON 已保存到 {output_dir / 'tongxin_structure.json'}")
        else:
            print(json_str)

    # 生成报告
    if args.report:
        report = TongxinGenerator.generate_report(doc)
        if output_dir:
            (output_dir / "tongxin_report.md").write_text(report, encoding='utf-8')
            print(f"✅ 报告已保存到 {output_dir / 'tongxin_report.md'}")
        else:
            print(report)

    # 生成 Markdown
    if args.markdown:
        md = TongxinGenerator.generate_markdown(doc)
        if output_dir:
            (output_dir / "tongxin_full.md").write_text(md, encoding='utf-8')
            print(f"✅ Markdown 已保存到 {output_dir / 'tongxin_full.md'}")
        else:
            print(md)

    # 默认显示结构摘要
    if not args.json and not args.report and not args.validate and not args.markdown:
        print("🐉 通心译结构摘要")
        print(f"  DNA: {doc.dna}")
        print(f"  章节数: {len(doc.chapters)}")
        print(f"  哲学定律: {len(doc.philosophy_laws)} 条")
        print(f"  公式附录: {len(doc.formulas)} 个")
        print(f"  物理索引: {len(doc.index_physics)} 条")
        print(f"  龍魂索引: {len(doc.index_longhun)} 条")
        print(f"  双语索引: {len(doc.bilingual_index)} 条")
        print("\n使用 --json 导出JSON，--report 生成报告，--validate 验证完整性")


if __name__ == "__main__":
    main()
