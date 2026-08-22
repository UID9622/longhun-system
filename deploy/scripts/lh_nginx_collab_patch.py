# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-5f275383
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
LongHun Collab nginx incremental patch (idempotent) v1.0
DNA: #LONGHUN-CONFIG-UNIFY-NGINX-PATCH-v1.0
Usage: python3 lh_nginx_collab_patch.py [--conf /etc/nginx/conf.d/nginx-uid9622.cn.conf]
Adds: /collab/.audit/ deny all, /collab/health check
Modifies: /collab/ block add X-LongHun-Tricolor headers
Idempotent, backups conf, rolls back on nginx -t failure.
"""
import argparse
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

AUDIT_BLOCK = '''
    # --- Collab audit zone (deny all, public 403) ---
    location /collab/.audit/ {
        alias /opt/longhun/shared/.audit/;
        autoindex off;
        deny all;
    }

    # --- Collab health check ---
    location = /collab/health {
        access_log off;
        return 200 "LongHun Collab Hub OK\\nDNA: LONGHUN-COLLAB-NGINX-UID9622\\n";
        add_header Content-Type "text/plain; charset=utf-8";
    }

'''

TRICOLOR_HEADERS = '''        add_header X-LongHun-Tricolor "GREEN" always;
        add_header X-LongHun-DNA "LONGHUN-COLLAB-NGINX-UID9622" always;
'''


def main() -> int:
    ap = argparse.ArgumentParser(description="LongHun collab nginx patch")
    ap.add_argument("--conf", default="/etc/nginx/conf.d/nginx-uid9622.cn.conf")
    ap.add_argument("--no-reload", action="store_true")
    args = ap.parse_args()

    conf = Path(args.conf)
    if not conf.exists():
        print("FAIL: conf not found: %s" % conf)
        return 1
    text = conf.read_text(encoding="utf-8")
    changed = []

    if "/collab/.audit/" in text:
        print("SKIP: audit block already present")
    else:
        anchor = "    location /collab/handoffs/ {"
        if anchor not in text:
            print("FAIL: anchor not found")
            return 1
        text = text.replace(anchor, AUDIT_BLOCK + anchor, 1)
        changed.append("audit+health")

    if "X-LongHun-Tricolor" in text:
        print("SKIP: tricolor headers already present")
    else:
        block = '''    location /collab/ {
        alias /opt/longhun/shared/collab/;
        charset utf-8;
        autoindex on;
        add_header Cache-Control "no-cache";
        add_header X-Data-Sovereignty "China-HuaweiCloud-Kunpeng" always;
    }'''
        if block not in text:
            print("FAIL: collab block anchor not found")
            return 1
        new_block = block.replace(
            '        add_header X-Data-Sovereignty "China-HuaweiCloud-Kunpeng" always;\n    }',
            '        add_header X-Data-Sovereignty "China-HuaweiCloud-Kunpeng" always;\n'
            + TRICOLOR_HEADERS + '    }',
            1,
        )
        text = text.replace(block, new_block, 1)
        changed.append("tricolor-headers")

    if not changed:
        print("OK: nothing to change")
        return 0

    bak = "%s.bak-collab-%s" % (conf, datetime.now().strftime("%Y%m%d-%H%M%S"))
    shutil.copy2(conf, bak)
    print("BACKUP -> %s" % bak)

    conf.write_text(text, encoding="utf-8")
    t = subprocess.run(["nginx", "-t"], capture_output=True, text=True)
    if t.returncode != 0:
        shutil.copy2(bak, conf)
        print("FAIL: nginx -t, rolled back\n" + t.stdout + t.stderr)
        return 1
    print("OK: nginx -t passed")

    if not args.no_reload:
        r = subprocess.run(["systemctl", "reload", "nginx"], capture_output=True, text=True)
        if r.returncode != 0:
            print("WARN: reload failed: " + r.stderr)
        else:
            print("OK: nginx reloaded")

    print("CHANGED: %s" % ", ".join(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
