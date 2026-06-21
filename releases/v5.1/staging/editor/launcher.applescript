-- 龍碼中文編輯器啟動器
-- DNA:#龍芯⚡️2026-06-18-LONGHUN-CHINESE-EDITOR-LAUNCHER-v1.0

property rootPath : "/Users/zuimeidedeyihan/longhun-system"

do shell script "cd " & quoted form of rootPath & " && python3 editor/龍碼編輯器.py >/dev/null 2>&1 &"
