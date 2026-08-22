#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂视频引擎 · 剧本解析器 v1.1
DNA: #龍芯⚡️2026-08-22-SCRIPT-PARSER-v1.1
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
设计原则: 先有解说稿再有画面·每句对应一个镜头·时间戳供音画对齐
修复记录 v1.1: md5→sha256(规则第七层)·_detect_visual 逻辑简化·注释勘误
"""

import re, json, hashlib
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path

# 中文语速：每秒 4.5 个字（标准普通话升调）
CHARS_PER_SECOND_ZH = 4.5

# 镜头识别关键词表
VISUAL_KEYWORDS = {
    "screenshot_terminal": ["终端", "命令行", "执行", "运行", "输出", "报错", "日志", "bash", "shell"],
    "screenshot_ide":      ["代码", "函数", "类", "方法", "IDE", "编辑器", "源码"],
    "screenshot_browser":  ["浏览器", "网页", "URL", "http", "界面", "页面"],
    "character":           ["讲解", "介绍", "北辰", "我来", "我们来", "接下来由", "大家好"],
    "title":               ["欢迎", "本节", "第一章", "第二章", "总结", "结语", "小结"],
}

@dataclass
class Segment:
    id:            str
    text:          str
    duration_hint: float
    visual_type:   str               # screenshot | character | generated | title
    visual_target: Optional[str] = None  # terminal | ide | browser
    character:     Optional[str] = None
    expression:    Optional[str] = None
    camera:        str = "固定"
    lip_sync:      bool = False
    scene_prompt:  Optional[str] = None
    dna:           Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

class ScriptParser:
    """
    将自然语言解说稿解析为严格结构化的镜头序列
    每个 Segment 携带时间锚点供后续音画对齐使用
    """

    @staticmethod
    def _estimate_duration(text: str) -> float:
        zh = len(re.findall(r'[\u4e00-\u9fff]', text))
        en = len(re.findall(r'[a-zA-Z]+', text))
        # 中文按字速，英文按词速，加 0.4s 句间停顿
        return round(zh / CHARS_PER_SECOND_ZH + en * 0.35 + 0.4, 2)

    @staticmethod
    def _detect_visual(text: str) -> tuple:
        low = text.lower()
        for vtype, kws in VISUAL_KEYWORDS.items():
            if any(kw in text or kw in low for kw in kws):
                if vtype.startswith("screenshot_"):
                    target = vtype.split("_", 1)[1]
                    return "screenshot", target
                return vtype, None
        return "generated", None

    @staticmethod
    def _detect_character(text: str, char_map: Dict[str, str]) -> Optional[str]:
        """char_map: {char_id: name}"""
        for cid, name in char_map.items():
            if name in text:
                return cid
        return None

    @staticmethod
    def _make_dna(seg_id: str) -> str:
        # 禁 md5（规则第七层加密下界）→ sha256
        ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        h  = hashlib.sha256(f"{seg_id}{ts}".encode()).hexdigest()[:8].upper()
        return f"#龍芯⚡️{ts}-SEG-{seg_id.upper()}-{h}"

    @classmethod
    def parse(cls, script: str,
              char_registry_path: Optional[str] = None) -> dict:
        """
        参数:
          script:              解说稿文本（多句）
          char_registry_path:  角色注册表 JSON 路径
        返回:
          带 segments 列表的完整 Timeline JSON
        """
        # 加载角色注册表
        char_map: Dict[str, str] = {}
        if char_registry_path and Path(char_registry_path).exists():
            data = json.loads(Path(char_registry_path).read_text("utf-8"))
            for c in data.get("characters", []):
                char_map[c["character_id"]] = c["name"]

        # 按句分割（中英文句尾 + 换行）
        raw = re.split(r'(?<=[\u3002\uff01\uff1f.!?])\s*|\n+', script.strip())
        sentences = [s.strip() for s in raw if s.strip()]

        segments = []
        for i, text in enumerate(sentences):
            seg_id = f"seg_{i+1:03d}"
            vtype, vtarget = cls._detect_visual(text)
            char_id = None
            if vtype == "character":
                char_id = cls._detect_character(text, char_map)

            seg = Segment(
                id            = seg_id,
                text          = text,
                duration_hint = cls._estimate_duration(text),
                visual_type   = vtype,
                visual_target = vtarget,
                character     = char_id,
                expression    = "讲解" if char_id else None,
                camera        = "中景" if char_id else "固定",
                lip_sync      = bool(char_id),
                scene_prompt  = None if vtype != "generated" else f"{text[:30]}... 风格: 中国风, 未来感",
                dna           = cls._make_dna(seg_id),
            )
            segments.append(seg.to_dict())

        total = sum(s["duration_hint"] for s in segments)
        return {
            "schema_version":    "1.0",
            "dna":               cls._make_dna("TIMELINE"),
            "created_at":        datetime.now().isoformat(),
            "total_duration":    round(total, 2),
            "segment_count":     len(segments),
            "segments":          segments,
        }

    @classmethod
    def save(cls, timeline: dict, output_path: str) -> None:
        Path(output_path).write_text(
            json.dumps(timeline, ensure_ascii=False, indent=2), "utf-8")
        print(f"✅ Timeline saved → {output_path}")

# JSON Schema
SCRIPT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "LH-VideoEngine-Timeline",
    "type": "object",
    "required": ["schema_version", "segments"],
    "properties": {
        "schema_version":  {"type": "string"},
        "dna":             {"type": "string"},
        "total_duration":  {"type": "number"},
        "segment_count":   {"type": "integer"},
        "segments": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "text", "duration_hint", "visual_type"],
                "properties": {
                    "id":            {"type": "string"},
                    "text":          {"type": "string"},
                    "duration_hint": {"type": "number"},
                    "visual_type":   {"enum": ["screenshot", "character", "generated", "title"]},
                    "visual_target": {"type": ["string", "null"]},
                    "character":     {"type": ["string", "null"]},
                    "expression":    {"type": ["string", "null"]},
                    "camera":        {"type": "string"},
                    "lip_sync":      {"type": "boolean"},
                    "scene_prompt":  {"type": ["string", "null"]},
                    "dna":           {"type": "string"},
                }
            }
        }
    }
}

if __name__ == "__main__":
    sample = """
    欢迎来到龍魂系统讲解视频。
    我们先看这段代码的执行结果。
    接下来由北辰为大家讲解核心逻辑。
    终端输出显示三色审计日志写入成功。
    本节内容总结完毕，感谢收看。
    """
    result = ScriptParser.parse(sample)
    print(json.dumps(result, ensure_ascii=False, indent=2))
