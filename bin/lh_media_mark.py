#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_MEDIA_MARK-v1.0-d12adc2b
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·媒体主权标记 CLI 入口
调用 engines/lh_media_sovereignty_marker.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "engines"))
from lh_media_sovereignty_marker import main  # noqa: E402

if __name__ == "__main__":
    main()
