# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 统一配置加载器 v1.1
DNA: #龍芯⚡️丙午·丙申·己未·乙亥·䷏豫-CONFIG-LOADER-UID9622
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

加载优先级: ① ~/.longhun/lh.env > ② deploy/.kunpeng_config > ③ 内置默认
用法:
    from lh_config import load_config
    cfg = load_config()   # 返回 dict（lh.env 存在时覆盖默认）
"""
import os
from pathlib import Path
from typing import Dict

CONFIG_DIR = Path.home() / ".longhun"
CONFIG_FILE = CONFIG_DIR / "lh.env"          # 🔴 修正: 原方案 config 为目录

DEFAULTS = {
    "KUNPENG_HOST": "root@119.13.90.27",
    "KUNPENG_PORT": "22",
    "KUNPENG_IDENTITY": "~/.ssh/longhun_kunpeng_ed25519",
    "KUNPENG_DEPLOY_PATH": "/opt/longhun",
    "SHARED_ROOT": "/opt/longhun/shared",
    "SHARED_WEB_PATH": "/collab/",
    "LOCAL_SHARED_ROOT": "12_DOCS/collab",
    "NGINX_SERVER_NAME": "uid9622.cn",
    "NGINX_SSL_CERT": "/etc/letsencrypt/live/uid9622.cn/fullchain.pem",
    "NGINX_SSL_KEY": "/etc/letsencrypt/live/uid9622.cn/privkey.pem",
}


def load_config() -> Dict[str, str]:
    """加载配置，返回键值对（lh.env 存在时覆盖默认）"""
    config = DEFAULTS.copy()

    if not CONFIG_FILE.exists():
        return config

    with open(CONFIG_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export "):].strip()
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key:
                    # 展开 ${HOME}/$VAR 与 ~
                    config[key] = os.path.expandvars(os.path.expanduser(value))

    return config


if __name__ == "__main__":
    import json
    cfg = load_config()
    print(json.dumps(cfg, ensure_ascii=False, indent=2))
    print(f"\n✅ 配置源: {CONFIG_FILE}（{'存在' if CONFIG_FILE.exists() else '不存在，使用内置默认'}）")
