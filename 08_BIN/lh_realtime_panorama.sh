#!/bin/bash
# 龍魂·实时采集+全景报告联动 (com.longhun.realtime-panorama)
# DNA: #龍芯⚡️丙午·丙申·REALTIME-PANORAMA-CRON-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
cd /Users/zuimeidedeyihan/longhun-system || exit 1
export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/homebrew/bin:$PATH

/usr/bin/python3 bin/lh_realtime_collector.py capture >> /Users/zuimeidedeyihan/.longhun/logs/realtime-panorama.out.log 2>&1
/usr/bin/python3 bin/lh_panorama_report.py generate >> /Users/zuimeidedeyihan/.longhun/logs/realtime-panorama.out.log 2>&1

echo "✅ [$()] 实时采集+全景报告完成" >> /Users/zuimeidedeyihan/.longhun/logs/realtime-panorama.out.log
