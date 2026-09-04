#!/bin/bash
# 🐉 龍魂 · 守护狗 v1.0 (端口级自动修复)
# DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-WATCHDOG-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 由 launchd StartInterval=300 每5分钟托管调用,死不了
# 核心逻辑复用 start_all.sh(幂等,端口已监听则跳过)

exec /Users/zuimeidedeyihan/longhun-system/deploy/scripts/start_all.sh >> /Users/zuimeidedeyihan/longhun-system/logs/watchdog.log 2>&1
