# -*- coding: utf-8 -*-
"""#龍芯⚡️2026-06-29-SECOND-BRAIN-IMPORTER-v1.0
Obsidian Markdown 导入器
"""
import re
import hashlib
import frontmatter
from pathlib import Path
from datetime import datetime
from typing import Iterator, List

from . import config
from .models import Note


class ObsidianImporter:
    """读取 Obsidian vault，解析 frontmatter、标签、wiki-link"""

    def __init__(self, vault_path: Path = None):
        self.vault_path = vault_path or config.VAULT_PATH

    def scan(self) -> Iterator[Path]:
        if not self.vault_path.exists():
            return
        for p in self.vault_path.rglob("*.md"):
            # 跳过模板/隐藏目录
            if any(part.startswith(".") for part in p.relative_to(self.vault_path).parts):
                continue
            yield p

    @staticmethod
    def _make_id(rel_path: str) -> str:
        h = hashlib.sha256(rel_path.encode("utf-8")).hexdigest()[:12]
        return f"note-{h}"

    @staticmethod
    def _make_dna(note_id: str) -> str:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{config.DNA_PREFIX}{ts}-SECOND-BRAIN-NOTE-{note_id}"

    @staticmethod
    def _extract_wiki_links(text: str) -> List[str]:
        # 匹配 [[Note]] 或 [[Note|alias]]
        pattern = r"\[\[(?:([^|\]]+)\|)?([^\]]+)\]\]"
        matches = re.findall(pattern, text)
        return [m[1] if m[1] else m[0] for m in matches]

    @staticmethod
    def _extract_inline_tags(text: str) -> List[str]:
        return sorted(set(re.findall(r"#([\w\u4e00-\u9fa5/_-]+)", text)))

    def parse(self, path: Path) -> Note:
        rel = str(path.relative_to(self.vault_path))
        text = path.read_text(encoding="utf-8", errors="ignore")

        try:
            post = frontmatter.loads(text)
        except Exception:
            post = frontmatter.Post(text)

        title = post.get("title", "")
        if not title:
            # 取第一个 H1，但先剔除代码块，避免把代码注释当标题
            text_no_code = re.sub(r"```[\s\S]*?```", "", text)
            text_no_code = re.sub(r"`[^`]+`", "", text_no_code)
            m = re.search(r"^#\s+(.+)$", text_no_code, re.MULTILINE)
            title = m.group(1).strip() if m else Path(path).stem

        tags = list(post.get("tags", []))
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]
        tags += self._extract_inline_tags(post.content)
        tags = sorted(set(tags))

        links = self._extract_wiki_links(post.content)
        aliases = list(post.get("aliases", []))
        if isinstance(aliases, str):
            aliases = [aliases]

        content_hash = hashlib.sha256(post.content.encode("utf-8")).hexdigest()
        note_id = self._make_id(rel)

        # 三色审计：标题/标签/链接/正文长度
        audit = "🟢"
        score = 0
        if title and title != Path(path).stem:
            score += 1
        if tags:
            score += 1
        if links:
            score += 1
        if len(post.content) > 200:
            score += 1
        if score < 2:
            audit = "🔴"
        elif score < 4:
            audit = "🟡"

        return Note(
            note_id=note_id,
            path=rel,
            title=title,
            content=post.content,
            content_hash=content_hash,
            created=post.get("created", "") or datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
            modified=post.get("modified", "") or datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
            tags=tags,
            links=links,
            aliases=aliases,
            metadata=dict(post.metadata),
            dna=self._make_dna(note_id),
            audit=audit,
        )

    def iter_notes(self) -> Iterator[Note]:
        for path in self.scan():
            try:
                yield self.parse(path)
            except Exception as e:
                print(f"🟡 解析失败 {path}: {e}")
