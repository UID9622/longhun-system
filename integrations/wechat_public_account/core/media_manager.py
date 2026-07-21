"""WeChat media material management: images, voice, video."""

import json
from pathlib import Path
from typing import Dict, Optional, Any

from .wechat_client import WeChatClient


class MediaManager:
    """Manage media materials for WeChat Official Account."""

    def __init__(self, client: Optional[WeChatClient] = None):
        self.client = client or WeChatClient()

    def upload_image_for_article(self, image_path: str) -> str:
        """Upload an image for use inside article content.

        Returns the URL of the uploaded image.
        """
        token = self.client.get_access_token()
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        with open(path, "rb") as f:
            files = {"media": (path.name, f, f"image/{path.suffix.lstrip('.')}")}
            result = self.client._request(
                "POST",
                "/media/uploadimg",
                params={"access_token": token},
                files=files,
            )

        return result["url"]

    def upload_material(
        self,
        file_path: str,
        material_type: str,
        title: Optional[str] = None,
        introduction: Optional[str] = None,
    ) -> Dict[str, str]:
        """Upload permanent material.

        material_type: image, voice, video, thumb
        """
        token = self.client.get_access_token()
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        description = None
        if material_type == "video" and title and introduction:
            description = json.dumps(
                {"title": title, "introduction": introduction},
                ensure_ascii=False,
            )

        with open(path, "rb") as f:
            files = {"media": (path.name, f)}
            if description:
                files["description"] = (None, description)

            result = self.client._request(
                "POST",
                "/material/add_material",
                params={"access_token": token, "type": material_type},
                files=files,
            )

        return result

    def upload_news_image(self, image_path: str) -> str:
        """Alias for upload_image_for_article."""
        return self.upload_image_for_article(image_path)

    def batch_get_materials(
        self,
        material_type: str,
        offset: int = 0,
        count: int = 20,
    ) -> Dict[str, Any]:
        """List permanent materials."""
        token = self.client.get_access_token()
        return self.client._request(
            "POST",
            "/material/batchget_material",
            params={"access_token": token},
            data={"type": material_type, "offset": offset, "count": count},
        )

    def get_material_count(self) -> Dict[str, Any]:
        """Get count of permanent materials."""
        token = self.client.get_access_token()
        return self.client._request(
            "GET",
            "/material/get_materialcount",
            params={"access_token": token},
        )
