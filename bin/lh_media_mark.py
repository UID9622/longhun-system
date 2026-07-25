#!/usr/bin/env python3
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
