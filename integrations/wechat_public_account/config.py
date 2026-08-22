#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷍大有-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

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
