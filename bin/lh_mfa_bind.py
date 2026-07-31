# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-MFA-BIND-v2.0-8A2C4E1F
# CREATOR: 诸葛鑫（UID9622）
# PROTOCOL: CC BY-NC-SA 4.0
# 功能: 龍魂系统 · MFA/TOTP 绑定快捷入口 v2.0
# 说明: 等同于 python bin/lh_mfa_activate.py --generate
"""
龍魂系统 · MFA/TOTP 绑定快捷入口 v2.0

用法:
  python bin/lh_mfa_bind.py --generate

DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-MFA-BIND-v2.0-8A2C4E1F
"""

import sys
import os

# 确保能导入同目录的 lh_mfa_activate
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lh_mfa_activate import LonghunMFA

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    mfa = LonghunMFA()
    mfa.generate_binding_qr()
