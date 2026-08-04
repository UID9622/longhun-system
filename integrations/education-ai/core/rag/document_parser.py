#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# core/rag/document_parser.py
# 龍魂 · 文档解析引擎 · 支持多格式教育资料

import os
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import hashlib

# === DNA常量 ===
MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"
MASTER_UID = "9622"
CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

@dataclass
class DocumentChunk:
    """文档分块"""
    id: str
    content: str
    source: str                    # 来源文件
    page: int                      # 页码
    chunk_index: int               # 分块序号
    metadata: Dict                 # 元数据
    embedding: Optional[List[float]] = None
    dna_signature: str = ""
    
    def __post_init__(self):
        if not self.dna_signature:
            self.dna_signature = self._sign_data()
    
    def _sign_data(self) -> str:
        payload = f"{self.id}-{self.source}-{self.chunk_index}-{datetime.now().timestamp()}"
        return f"SM3-{hashlib.sha256(payload.encode()).hexdigest()[:16]}"


class DocumentParser:
    """文档解析器"""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.supported_formats = ['.pdf', '.docx', '.md', '.txt', '.html']
    
    def parse_file(self, file_path: str) -> List[DocumentChunk]:
        """解析文件"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            return self._parse_pdf(file_path)
        elif ext == '.docx':
            return self._parse_docx(file_path)
        elif ext == '.md':
            return self._parse_markdown(file_path)
        elif ext == '.txt':
            return self._parse_text(file_path)
        elif ext == '.html':
            return self._parse_html(file_path)
        else:
            raise ValueError(f"不支持的格式: {ext}")
    
    def _parse_pdf(self, file_path: str) -> List[DocumentChunk]:
        """解析PDF"""
        try:
            import PyPDF2
        except ImportError:
            raise ImportError("请安装PyPDF2: pip install PyPDF2")
        
        chunks = []
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                page_chunks = self._chunk_text(text, file_path, page_num + 1)
                chunks.extend(page_chunks)
        
        return chunks
    
    def _parse_docx(self, file_path: str) -> List[DocumentChunk]:
        """解析Word"""
        try:
            from docx import Document
        except ImportError:
            raise ImportError("请安装python-docx: pip install python-docx")
        
        doc = Document(file_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        return self._chunk_text(full_text, file_path, 1)
    
    def _parse_markdown(self, file_path: str) -> List[DocumentChunk]:
        """解析Markdown"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按标题分块
        sections = self._split_by_headers(content)
        chunks = []
        for i, section in enumerate(sections):
            section_chunks = self._chunk_text(
                section['content'], file_path, 1, 
                metadata={'header': section['header']}
            )
            chunks.extend(section_chunks)
        
        return chunks
    
    def _parse_text(self, file_path: str) -> List[DocumentChunk]:
        """解析纯文本"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self._chunk_text(content, file_path, 1)
    
    def _parse_html(self, file_path: str) -> List[DocumentChunk]:
        """解析HTML"""
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            raise ImportError("请安装beautifulsoup4: pip install beautifulsoup4")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # 提取正文
        text = soup.get_text(separator='\n', strip=True)
        return self._chunk_text(text, file_path, 1)
    
    def _chunk_text(self, text: str, source: str, page: int, 
                   metadata: Optional[Dict] = None) -> List[DocumentChunk]:
        """文本分块"""
        if not text.strip():
            return []
        
        # 清理文本
        text = self._clean_text(text)
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            
            # 智能截断：在句子边界截断
            if end < len(text):
                end = self._find_sentence_boundary(text, end)
            
            chunk_text = text[start:end]
            
            chunk = DocumentChunk(
                id=f"CHUNK-{hashlib.md5(f'{source}-{chunk_index}'.encode()).hexdigest()[:12]}",
                content=chunk_text,
                source=source,
                page=page,
                chunk_index=chunk_index,
                metadata=metadata or {}
            )
            chunks.append(chunk)
            
            start = end - self.chunk_overlap
            chunk_index += 1
        
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text)
        # 保留中英文标点和常见字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,;:!?。；：！？、—""''（）()【】\[\]《》<>]', '', text)
        return text.strip()
    
    def _find_sentence_boundary(self, text: str, pos: int) -> int:
        """查找句子边界"""
        # 向后查找句号、问号、感叹号
        for i in range(pos, max(pos - 100, -1), -1):
            if i < len(text) and text[i] in '。！？.!?':
                return i + 1
        return pos
    
    def _split_by_headers(self, content: str) -> List[Dict]:
        """按Markdown标题分块"""
        sections = []
        current_header = "无标题"
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('#'):
                if current_content:
                    sections.append({
                        'header': current_header,
                        'content': '\n'.join(current_content)
                    })
                current_header = line.strip('# ').strip()
                current_content = []
            else:
                current_content.append(line)
        
        if current_content:
            sections.append({
                'header': current_header,
                'content': '\n'.join(current_content)
            })
        
        return sections


# === 使用示例 ===
if __name__ == "__main__":
    parser = DocumentParser(chunk_size=512, chunk_overlap=50)
    
    # 解析PDF教材
    chunks = parser.parse_file("data/数学教材.pdf")
    print(f"解析完成: {len(chunks)} 个分块")
    
    for chunk in chunks[:3]:
        print(f"\n[{chunk.id}] 页{chunk.page} 块{chunk.chunk_index}")
        print(f"内容: {chunk.content[:100]}...")
        print(f"签名: {chunk.dna_signature}")
