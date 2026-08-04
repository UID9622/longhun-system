#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-22-LONGHUN-GOVERNANCE-CLI-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
🐉 龍魂分层治理自愈引擎 · CLI 入口

统一命令：
  python3 bin/lh_governance.py status          巡检并显示状态
  python3 bin/lh_governance.py heal            自动修复可修复项
  python3 bin/lh_governance.py heal --dry-run  演练模式
  python3 bin/lh_governance.py watch           值守模式（定时巡检）
  python3 bin/lh_governance.py freeze --component <id> --reason <原因>
  python3 bin/lh_governance.py activate --component <id>

DNA: #龍芯⚡️2026-06-22-LONGHUN-GOVERNANCE-CLI-v1.0
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cnsh" / "core"))

from governance.layered_governance_engine import main

if __name__ == "__main__":
    main()
