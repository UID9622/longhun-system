
from pathlib import Path

class Settings:
    CACHE_DIR = Path.home() / ".longhun" / "wechat_cache"
    WECHAT_APPID = ""
    WECHAT_APPSECRET = ""
    OPENAI_API_KEY = ""
    KIMI_API_KEY = ""
    PERSONAS_FILE = Path.home() / ".longhun" / "personas.json"

def get_settings():
    return Settings()
