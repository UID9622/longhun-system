# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-MOBILE-MONITORING_SERVER_PORT9000-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python3
import sys
sys.argv = ['monitoring_server.py', '--port', '9000']

# 修改 monitoring_server.py 以使用端口 9000
code = open('monitoring_server.py').read()
code = code.replace("port=8000", "port=9000")
exec(code)
