-- 龍魂控制中心啟動器
-- DNA:#龍芯⚡️2026-06-18-LONGHUN-CONTROL-CENTER-LAUNCHER-v1.0

property rootPath : "/Users/zuimeidedeyihan/longhun-system"

do shell script "cd " & quoted form of rootPath & " && python3 desktop/龍魂控制中心.py >/dev/null 2>&1 &"
