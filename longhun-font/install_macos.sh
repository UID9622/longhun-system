#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷇比-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# #龍芯⚡️丙午·甲午·己巳·乙丑·䷮困-AUTO-DNA-668A0266 自动注入·分层治理自愈引擎 · 来源可查
#!/bin/bash
# DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-INSTALL-MACOS-v1.0
#
# LonghunFont macOS installer
# Copies LonghunFont-Regular.otf into the user's Fonts folder.

set -e

FONT_SOURCE="output/LonghunFont-Regular.otf"
FONT_TARGET="${HOME}/Library/Fonts/LonghunFont-Regular.otf"

# 1. OS check
if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "Error: This installer is for macOS only." >&2
    exit 1
fi

# 2. Font file check
if [[ ! -f "${FONT_SOURCE}" ]]; then
    echo "Error: Font file not found at ${FONT_SOURCE}" >&2
    exit 1
fi

# 3. Install font
cp "${FONT_SOURCE}" "${FONT_TARGET}"
echo "Installed LonghunFont-Regular.otf to ${FONT_TARGET}"

# 4. Clear font cache (optional; may require a reboot/logout to take full effect)
echo "Clearing font cache (atsutil) — optional step..."
atsutil databases -remove 2>/dev/null || echo "Note: atsutil cache clear skipped (non-fatal)."

# 5. Success + DNA
echo ""
echo "✅ LonghunFont installed successfully."
echo "DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-INSTALL-MACOS-v1.0"
