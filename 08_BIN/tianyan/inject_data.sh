# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丙辰·䷸巽为风-CODE-补DNA-636f7115
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 将天眼数据注入到 HTML 看板（优先 window.TIANYAN_DATA JS 格式）
TIANYAN_DIR="${HOME}/longhun-system/08_BIN/tianyan"
WWW_DIR="${HOME}/longhun-system/www"
python3 "${TIANYAN_DIR}/tianyan_engine.py" --snapshot --export-html "${WWW_DIR}/tianyan_data.js" 2>/dev/null \
  || python3 "${TIANYAN_DIR}/tianyan_engine.py" --snapshot --json > "${WWW_DIR}/tianyan_data.json"
echo "🟢 数据已注入到 ${WWW_DIR}/tianyan_data.js (JSON 兜底: tianyan_data.json)"
