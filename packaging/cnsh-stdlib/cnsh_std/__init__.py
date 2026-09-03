#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-STDLIB-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）· License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

CNSH 官方标准库 v1.0 —— 零三方依赖（M77 零中间层）
模块一览:
  基础: cnsh_std.io    文件读写   · cnsh_std.http  网络请求
        cnsh_std.time  时间/干支  · cnsh_std.crypto 哈希/加密
  审计: cnsh_std.dna   DNA追溯    · cnsh_std.audit  三色审计
        cnsh_std.fuse  P0熔断
  龍魂: cnsh_std.topo   系统拓扑    · cnsh_std.memorial 铭碑记录
安装: pip install -e packaging/cnsh-stdlib
"""
VERSION = "1.0.0"
UID = "UID9622"

__all__ = ["VERSION", "UID", "io", "http", "time", "crypto",
           "dna", "audit", "fuse", "topo", "memorial"]
