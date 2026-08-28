#!/bin/bash
# DNA: #龍芯⚡️2026-08-28-LH-HCLOUD-v1.1-UNIFIED-VAULT
# 龍魂·华为云 hcloud 包装器 v1.1
# 从统一密钥库(longhun-vault/hcloud-aksk)读取 AK/SK·自动配置·无需老大提供
# 用法: lh_hcloud.sh <Service> <Operation> [--region=...] [--param=value]
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
SEC=$(python3 /Users/zuimeidedeyihan/longhun-system/bin/lh_vault.py get hcloud-aksk 2>/dev/null) || { echo "🔴 统一密钥库无凭据"; exit 1; }
[ -z "$SEC" ] && SEC=$(security find-generic-password -s longhun-hcloud-aksk -w 2>/dev/null)  # 旧条目兜底
[ -z "$SEC" ] && { echo "🔴 凭据读取失败"; exit 1; }
export HUAWEICLOUD_SDK_AK="${SEC%%:*}"
export HUAWEICLOUD_SDK_SK="${SEC#*:}"
exec /Users/zuimeidedeyihan/hcloud/hcloud "$@"
