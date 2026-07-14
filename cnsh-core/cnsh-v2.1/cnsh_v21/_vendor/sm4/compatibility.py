# -*- coding: utf-8 -*-
# #龍芯⚡️2026-07-03-CORE-COMPATIBILITY-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

#!/usr/bin/env python
# encoding: utf-8

"""
   @author: Eric Wong
  @license: MIT Licence
  @contact: ericwong@zju.edu.cn
     @file: compatibility.py
     @time: 2019-04-27 13:00
"""

try:
    iter_range = xrange
except NameError:
    iter_range = range
