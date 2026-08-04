#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·大有-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""Configuration management for Longhun WeChat Public Account integration."""

import json
import os
from pathlib import Path
from typing import Optional, Any

from dotenv import load_dotenv

# Load .env if exists (project root)
ENV_PATH = Path(__file__).parent.parent / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


def _load_from_vault(key_name: str) -> Optional, Any[str]:
    """Load a credential from Longhun vault plaintext JSON fallback.

    The vault is managed by the 龍魂密钥管家 persona. Plaintext files are
    local-only (permission 600) and should not be committed.
    """
    vault_dir = Path.home() / ".longhun" / "vault" / "keys"
    if not vault_dir.exists():
        return None

    for f in vault_dir.glob("*.plain.json"):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if data.get("key_name") == key_name:
                return data.get("value")
        except Exception:
            continue
    return None


class Settings:
    """Configuration settings loaded from environment variables and vault."""

    # WeChat Official Account (env first, vault fallback)
    WECHAT_APPID: Optional, Any[str] = os.getenv("WECHAT_APPID") or _load_from_vault(
        "WECHAT_APPID"
    )
    WECHAT_APPSECRET: Optional, Any[str] = os.getenv("WECHAT_APPSECRET") or _load_from_vault(
        "WECHAT_APPSECRET"
    )
    WECHAT_TOKEN: Optional, Any[str] = os.getenv("WECHAT_TOKEN")
    WECHAT_ENCODING_AES_KEY: Optional, Any[str] = os.getenv("WECHAT_ENCODING_AES_KEY")

    # AI Services
    KIMI_API_KEY: Optional, Any[str] = os.getenv("KIMI_API_KEY")
    DEEPSEEK_API_KEY: Optional, Any[str] = os.getenv("DEEPSEEK_API_KEY")
    OPENAI_API_KEY: Optional, Any[str] = os.getenv("OPENAI_API_KEY")

    # Paths
    LONGHUN_SYSTEM_ROOT: Path = Path(
        os.getenv("LONGHUN_SYSTEM_ROOT", "~/longhun-system")
    ).expanduser()
    PERSONAS_FILE: Path = Path(__file__).parent.parent / "personas" / "personas.json"
    CACHE_DIR: Path = Path(__file__).parent.parent / ".cache"

    # Web UI
    WEB_HOST: str = os.getenv("WEB_HOST", "0.0.0.0")
    WEB_PORT: int = int(os.getenv("WEB_PORT", "8443"))

    @classmethod
    def validate_wechat(cls) -> dict[str, Any]:
        """Validate WeChat configuration and return status."""
        errors = []
        if not cls.WECHAT_APPID:
            errors.append("WECHAT_APPID not set")
        if not cls.WECHAT_APPSECRET:
            errors.append("WECHAT_APPSECRET not set")
        return {
            "ok": len(errors) == 0,
            "errors": errors,
            "appid": cls.WECHAT_APPID[:6] + "..." if cls.WECHAT_APPID else None,
        }

    @classmethod
    def ensure_dirs(cls):
        """Ensure required directories exist."""
        cls.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cls.LONGHUN_SYSTEM_ROOT.mkdir(parents=True, exist_ok=True)


# Global settings instance
_settings = None


def get_settings() -> Settings:
    """Get or create settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.ensure_dirs()
    return _settings
