#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·己未·乙亥时·䷒临-HEALTH-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# SPDX-License-Identifier: MulanPSL-2.0
# /usr/local/bin/lh_health_check.sh —— 龍魂 · 后端健康巡检
# 修正20: 删除死变量 all_ok; curl 加 --max-time; deploy.sh 负责 chmod +x。
# 退出码: 0=全部正常, 1=有异常 (供 cron/监控判断)

services=(
    "http://127.0.0.1:8970/health|API网关"
    "http://127.0.0.1:19622/health|协作中枢"
    "http://127.0.0.1:18800/health|对话桥接"
)

failed=0
for svc in "${services[@]}"; do
    url="${svc%|*}"
    name="${svc#*|}"
    code=$(curl -s -o /dev/null --max-time 5 -w "%{http_code}" "$url" || echo "000")
    if [ "$code" = "200" ]; then
        echo "✅ $name ($url) 正常"
    else
        echo "❌ $name ($url) 异常 (HTTP $code)"
        failed=$((failed + 1))
    fi
done

if [ "$failed" -eq 0 ]; then
    echo "🟢 所有服务正常"
    exit 0
else
    echo "🔴 有 $failed 个服务异常"
    exit 1
fi
