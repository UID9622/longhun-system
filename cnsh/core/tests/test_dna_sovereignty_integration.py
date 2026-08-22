#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂人民主权联动测试

DNA:#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-PEOPLE-SOVEREIGNTY-INTEGRATION-TEST-v2.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dna_sovereignty_kernel import PeopleSovereigntyGuard, Context


def main():
    print("╔═══════════════════════════════════════════════════╗")
    print("║  龍魂人民主权联动测试                             ║")
    print("║  识主 · 随行 · 守望                               ║")
    print("╚═══════════════════════════════════════════════════╝")

    guard = PeopleSovereigntyGuard()
    print(f"\n守护状态: {guard.stats()}")

    founder_home = Context(who="UID9622", network="瑞安老家", ip="192.168.1.5")
    founder_airport = Context(who="UID9622", network="机场 WiFi", ip="10.0.0.1")
    people = Context(who="张三", is_known_person=True)
    platform = Context(who="某支付APP", is_platform=True)

    print("\n【创始人·老家·读宪法】", guard.check(founder_home, "cnsh-core/constitution/longhun_foundation_config.py", "read"))
    print("【创始人·老家·写宪法】", guard.check(founder_home, "cnsh-core/constitution/longhun_foundation_config.py", "write"))
    print("【创始人·机场·写界面】", guard.check(founder_airport, "ops-console/index.html", "write"))
    print("【人民·读宪法】      ", guard.check(people, "cnsh-core/constitution/longhun_foundation_config.py", "read"))
    print("【人民·写宪法】      ", guard.check(people, "cnsh-core/constitution/longhun_foundation_config.py", "write"))
    print("【平台·写核心】      ", guard.check(platform, "cnsh-core/constitution/longhun_foundation_config.py", "write"))

    print("\n" + guard.founder_going_to("北京"))
    founder_bj = Context(who="UID9622", network="北京酒店", ip="172.16.0.1", where="北京", said_where="北京")
    print("【创始人·报备后·写界面】", guard.check(founder_bj, "ops-console/index.html", "write"))

    print("\n✅ 联动测试完成")


if __name__ == "__main__":
    main()
