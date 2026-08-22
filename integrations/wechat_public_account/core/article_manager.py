#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷍大有-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""WeChat article draft and publish management."""

import html
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from .media_manager import MediaManager
from .wechat_client import WeChatClient


class ArticleManager:
    """Manage WeChat articles: drafts, publish, list."""

    def __init__(self, client: Optional[WeChatClient] = None):
        self.client = client or WeChatClient()
        self.media = MediaManager(self.client)

    def markdown_to_html(self, markdown_text: str) -> str:
        """Convert simple Markdown to HTML suitable for WeChat."""
        # Very basic markdown conversion
        text = markdown_text

        # Escape HTML
        text = html.escape(text)

        # Headers
        for level in range(6, 0, -1):
            pattern = re.compile(rf"^{{'#' * {level}}} \\s*(.+)$", re.MULTILINE)
            text = pattern.sub(rf"<h{level}>\\1</h{level}>", text)

        # Bold and italic
        text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

        # Line breaks to paragraphs
        paragraphs = text.split("\n\n")
        processed = []
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            if p.startswith("<"):
                processed.append(p)
            else:
                # Replace single newlines with <br>
                p = p.replace("\n", "<br>")
                processed.append(f"<p>{p}</p>")

        return "\n".join(processed)

    def build_article(
        self,
        title: str,
        content: str,
        author: Optional[str] = None,
        digest: Optional[str] = None,
        cover_media_id: Optional[str] = None,
        source_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Build a single article dict for draft/add or draft/update."""
        html_content = self.markdown_to_html(content)

        article = {
            "title": title,
            "content": html_content,
            "content_source_url": source_url or "",
            "need_open_comment": 1,
            "only_fans_can_comment": 0,
        }

        if author:
            article["author"] = author
        if digest:
            article["digest"] = digest[:120]
        if cover_media_id:
            article["thumb_media_id"] = cover_media_id

        return article

    def create_draft(
        self,
        title: str,
        content: str,
        author: Optional[str] = None,
        digest: Optional[str] = None,
        cover_image_path: Optional[str] = None,
        source_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new draft article."""
        token = self.client.get_access_token()

        thumb_media_id = None
        if cover_image_path:
            cover_result = self.media.upload_material(
                cover_image_path,
                material_type="thumb",
            )
            thumb_media_id = cover_result.get("media_id")

        article = self.build_article(
            title=title,
            content=content,
            author=author,
            digest=digest,
            cover_media_id=thumb_media_id,
            source_url=source_url,
        )

        result = self.client._request(
            "POST",
            "/draft/add",
            params={"access_token": token},
            data={"articles": [article]},
        )

        return {
            "media_id": result.get("media_id"),
            "title": title,
            "thumb_media_id": thumb_media_id,
        }

    def update_draft(
        self,
        media_id: str,
        index: int,
        title: str,
        content: str,
        author: Optional[str] = None,
        digest: Optional[str] = None,
        cover_image_path: Optional[str] = None,
        source_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update an existing draft article."""
        token = self.client.get_access_token()

        thumb_media_id = None
        if cover_image_path:
            cover_result = self.media.upload_material(
                cover_image_path,
                material_type="thumb",
            )
            thumb_media_id = cover_result.get("media_id")

        article = self.build_article(
            title=title,
            content=content,
            author=author,
            digest=digest,
            cover_media_id=thumb_media_id,
            source_url=source_url,
        )

        result = self.client._request(
            "POST",
            "/draft/update",
            params={"access_token": token},
            data={
                "media_id": media_id,
                "index": index,
                "articles": article,
            },
        )

        return result

    def publish(self, media_id: str) -> Dict[str, Any]:
        """Publish a draft to all subscribers."""
        token = self.client.get_access_token()
        return self.client._request(
            "POST",
            "/freepublish/submit",
            params={"access_token": token},
            data={"media_id": media_id},
        )

    def get_publish_status(self, publish_id: str) -> Dict[str, Any]:
        """Get publish task status."""
        token = self.client.get_access_token()
        return self.client._request(
            "POST",
            "/freepublish/get",
            params={"access_token": token},
            data={"publish_id": publish_id},
        )

    def list_drafts(self, offset: int = 0, count: int = 20, no_content: int = 0) -> Dict[str, Any]:
        """List draft articles."""
        token = self.client.get_access_token()
        return self.client._request(
            "POST",
            "/draft/batchget",
            params={"access_token": token},
            data={"offset": offset, "count": count, "no_content": no_content},
        )

    def delete_draft(self, media_id: str) -> Dict[str, Any]:
        """Delete a draft."""
        token = self.client.get_access_token()
        return self.client._request(
            "POST",
            "/draft/delete",
            params={"access_token": token},
            data={"media_id": media_id},
        )

    def read_file_content(self, file_path: str) -> str:
        """Read content from a file."""
        path = Path(file_path).expanduser()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        return path.read_text(encoding="utf-8")

    def generate_dna(self, action: str = "PUBLISH") -> str:
        """Generate a LongHun DNA trace code."""
        now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        import hashlib
        import random

        rand = random.randint(1000, 9999)
        raw = f"{now}-{action}-{rand}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:12].upper()
        return f"#龍芯⚡️{now}-WECHAT-{action}-{h}"
