#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2
"""
🐲 龍魂·文档分块工具
DNA: #龍芯⚡️2026-08-04-CHUNKER-v2.0-UID9622
"""
import re
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Optional


class ChunkMethod(Enum):
    HEADERS = auto()      # 按Markdown标题分块
    SIZE = auto()         # 按字符数分块
    SEMANTIC = auto()     # 按语义段落分块
    HYBRID = auto()       # 混合：标题优先，超限按大小切


@dataclass
class Chunk:
    id: int
    header: str = ""
    content: str = ""
    level: int = 0
    start: int = 0
    end: int = 0
    metadata: Dict = field(default_factory=dict)

    @property
    def length(self) -> int:
        return len(self.content)

    @property
    def preview(self) -> str:
        return self.content[:100].replace('\n', ' ')


class DocumentChunker:
    """文档自适应分块器"""

    def __init__(self, chunk_size: int = 2000, overlap: int = 200, max_chunks: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.max_chunks = max_chunks

    def chunk(self, text: str, method: ChunkMethod = ChunkMethod.HYBRID) -> List[Chunk]:
        """分块主入口"""
        if method == ChunkMethod.HEADERS:
            return self._by_headers(text)
        elif method == ChunkMethod.SIZE:
            return self._by_size(text)
        elif method == ChunkMethod.SEMANTIC:
            return self._by_semantic(text)
        else:
            return self._hybrid(text)

    def _by_headers(self, text: str) -> List[Chunk]:
        """按Markdown标题分块"""
        pattern = r'(^|\n)(#{1,6}\s+.*?)(?=\n#{1,6}\s+|\n*$)'
        matches = list(re.finditer(pattern, text, re.MULTILINE | re.DOTALL))
        if not matches:
            return [Chunk(id=0, header="全文", content=text[:self.chunk_size])]

        chunks = []
        for i, m in enumerate(matches):
            header = m.group(2).strip()
            level = len(re.match(r'#+', header).group())
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            content = text[start:end].strip()
            if content:
                chunks.append(Chunk(id=i, header=header, content=content, level=level, start=start, end=end))
        return chunks[:self.max_chunks]

    def _by_size(self, text: str) -> List[Chunk]:
        """按字符数分块（带重叠+智能断句）"""
        chunks, start, cid = [], 0, 0
        while start < len(text) and cid < self.max_chunks:
            end = min(start + self.chunk_size, len(text))
            if end < len(text):
                for sep in ['\n\n', '。', '！', '？', '.\n', '!\n', '?\n', '\n']:
                    pos = text.rfind(sep, start + self.chunk_size // 2, end)
                    if pos > start:
                        end = pos + len(sep)
                        break
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(Chunk(id=cid, content=chunk_text, start=start, end=end))
            start = end - self.overlap if end < len(text) else end
            cid += 1
        return chunks

    def _by_semantic(self, text: str) -> List[Chunk]:
        """按语义段落分块（空行分隔优先，超长再切）"""
        paragraphs = re.split(r'\n\n+', text)
        chunks, cid, buf = [], 0, ""
        for para in paragraphs:
            if len(buf) + len(para) > self.chunk_size and buf:
                chunks.append(Chunk(id=cid, content=buf.strip()))
                cid += 1
                buf = para
            else:
                buf = buf + "\n\n" + para if buf else para
        if buf.strip():
            chunks.append(Chunk(id=cid, content=buf.strip()))
        return chunks[:self.max_chunks]

    def _hybrid(self, text: str) -> List[Chunk]:
        """混合模式：先按标题分，超限块再按大小切"""
        header_chunks = self._by_headers(text)
        if not header_chunks:
            return self._by_semantic(text)
        result = []
        for hc in header_chunks:
            if len(hc.content) <= self.chunk_size:
                result.append(hc)
            else:
                sub = self._by_size(hc.content)
                for j, s in enumerate(sub):
                    s.header = hc.header + (f" (续{j+1})" if j > 0 else "")
                    s.level = hc.level
                result.extend(sub)
        return result[:self.max_chunks]

    def get_summary(self, chunks: List[Chunk]) -> str:
        lines = [f"📄 共 {len(chunks)} 块，总字符: {sum(c.length for c in chunks):,}"]
        for c in chunks:
            lines.append(f"  [{c.id}] {c.header[:40] or '(无标题)':40s} | {c.length:>6}字 | {c.preview}")
        return "\n".join(lines)
