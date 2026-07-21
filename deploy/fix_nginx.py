#!/usr/bin/env python3
"""只插入 dashboard location"""
marker = 'include /etc/nginx/longhun-executor.conf;'
block = '''    # ═══ 龍魂Dashboard静态文件 ═══
    location ^~ /dashboard/ {
        alias /opt/longhun-system/L5_服务层/services/dashboard/web/;
        index CNSH_龍魂操作台v4.0.html;
    }

'''
with open('/etc/nginx/sites-enabled/longhun888.com') as f:
    content = f.read()
content = content.replace(marker, block + marker, 1)
with open('/etc/nginx/sites-enabled/longhun888.com', 'w') as f:
    f.write(content)
print('OK')
