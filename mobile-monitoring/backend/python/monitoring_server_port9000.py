#!/usr/bin/env python3
import sys
sys.argv = ['monitoring_server.py', '--port', '9000']

# 修改 monitoring_server.py 以使用端口 9000
code = open('monitoring_server.py').read()
code = code.replace("port=8000", "port=9000")
exec(code)
