# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""插入 dashboard/api/webhook location 到 Nginx 配置"""
marker = "include /etc/nginx/longhun-executor.conf;"
with open("/tmp/nginx-dashboard.conf") as f:
    new_block = f.read()
with open("/etc/nginx/sites-enabled/longhun888.com") as f:
    lines = f.readlines()
out = []
for line in lines:
    if marker in line:
        out.append(new_block + "\n")
    out.append(line)
with open("/etc/nginx/sites-enabled/longhun888.com", "w") as f:
    f.writelines(out)
print("DONE")
