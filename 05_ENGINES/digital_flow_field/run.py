#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍魂系统 · 工程实现层
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 文化归属: 思想框架归龍魂核心思想层 (CC BY-NC-SA 4.0)
# DNA: #龍芯⚡️丙午·癸未·甲申-DIGITAL-FLOW-FIELD-RUN-v2.0-UID9622
# 署名: UID9622（诸葛鑫·Lucky）

"""一键启动数字流场可视化器。"""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path


def check_dependency(name: str) -> bool:
    """检查单个依赖是否已安装。"""
    try:
        importlib.import_module(name)
        return True
    except ImportError:
        return False


def main() -> None:
    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root))

    required = {
        "streamlit": "streamlit",
        "numpy": "numpy",
        "pandas": "pandas",
        "plotly": "plotly",
        "matplotlib": "matplotlib",
        "PIL": "Pillow",
        "requests": "requests",
        "chardet": "chardet",
    }

    missing = [pkg for mod, pkg in required.items() if not check_dependency(mod)]
    if missing:
        print("🔴 缺少依赖，正在安装：", ", ".join(missing))
        subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])
    else:
        print("🟢 全部依赖已就位")

    app_path = root / "app.py"
    print("🚀 启动龍魂数字流场可视化器 …")
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", str(app_path), "--server.port=8501"],
        check=False,
    )


if __name__ == "__main__":
    main()
