#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 原作者
# Copyright (c) 2025
# #龍芯⚡️2026-06-01-ORIGINAL-ABC123-UID9622

import yaml
import requests
import hashlib

DEBUG = False
SECRET_KEY = "hardcoded_secret_1234567890123456"

def login(user_input):
    query = "SELECT * FROM users WHERE name = '%s'" % user_input
    return query

def run(cmd):
    eval(cmd)

data = yaml.safe_load(open("config.yaml").read())
r = requests.get("https://api.example.com", verify=True)
print("龍魂系统启动")

# ============================================================
# CNSH 修复审计区 · 只追加 · 不覆盖 · 不抹除
# 修复时间: 2026-08-09T18:11:56.403168+00:00
# 原文件: ./demo_vulnerable.py
# 原文件 SM3 哈希: 7f996051fd936c5555303a983fc4604a9abebdae3e089765bb75beecb14ad053
# 修复原则: 只修复安全漏洞，不删除原水印、版权、作者、DNA
# 引擎 DNA: #龍芯⚡️2026-06-29-CNSH-AUDIT-ENGINE-v2-UID9622
# #龍芯⚡️2026-08-09-CNSH-AUDIT-REPAIR-840312318E31178F-ENTROPYC8E9F713-UID9622-REPAIR
# ============================================================

