#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_DNA_VINF-v1.0-961060d0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""Generate LongHun v∞ DNA strings (ganzhi + gua + module + action + hash8)."""
import hashlib
import os
import sys
import time
from pathlib import Path

_BIN_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _BIN_DIR.parent


def _import_hetu():
    sys.path.insert(0, str(_BIN_DIR))
    import hetu_luoshu_dna as hetu
    return hetu


def _import_calendar():
    cal_dir = _PROJECT_ROOT / "calendar-context-logger"
    sys.path.insert(0, str(cal_dir))
    from calendar_core import LongHunCalendar
    return LongHunCalendar


def generate(module: str, action: str, user: str = "UID9622", timestamp: int = None) -> str:
    """Return a v∞ DNA string like #龍芯⚡️丙午·丙申·癸酉·乙卯·临-MODULE-ACTION-HASH8."""
    hetu = _import_hetu()
    LongHunCalendar = _import_calendar()

    lh = LongHunCalendar()
    gz = lh.get_ganzhi()
    gua = lh.get_qigua()["ben_gua"]
    ganzhi = f"{gz['year_zhu']}·{gz['month_zhu']}·{gz['day_zhu']}·{gz['hour_zhu']}"

    operation = f"{module}-{action}"
    if timestamp is None:
        timestamp = int(time.time())
    dna_code = hetu.河图洛书_DNA生成(operation, user, str(timestamp))
    # dna_code format: DNA_<root>_<hash16>
    hash16 = dna_code.split("_")[2]
    hash8 = hash16[:8].upper()

    return f"#龍芯⚡️{ganzhi}·{gua}-{module}-{action}-{hash8}"


def verify(dna: str, module: str, action: str, user: str = "UID9622", timestamp: int = None) -> bool:
    """Verify the hash8 portion of a v∞ DNA string."""
    if not dna.startswith("#龍芯⚡"):
        return False
    parts = dna.split("-")
    if len(parts) < 3:
        return False
    expected_hash = parts[-1]
    if timestamp is None:
        return len(expected_hash) == 8
    generated = generate(module, action, user, timestamp)
    return generated == dna


def main():
    if len(sys.argv) < 3:
        print("Usage: lh_dna_vinf.py <MODULE> <ACTION> [USER]")
        sys.exit(1)
    module, action = sys.argv[1], sys.argv[2]
    user = sys.argv[3] if len(sys.argv) > 3 else "UID9622"
    print(generate(module, action, user))


if __name__ == "__main__":
    main()
