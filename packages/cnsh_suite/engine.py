#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 引擎模块

DNA: #龍芯⚡️丙午·丙申·庚申·亥时-CNSH-ENGINE-UID9622

本模块作为 core.py 中 CNSHEngine 的显式导出层，
保持与文件清单 `engine.py` 的对应关系。
"""

from .core import CNSHEngine, CNSHSuite, CNSHError, CNSHErrorCode, generate_dna

__all__ = ["CNSHEngine", "CNSHSuite", "CNSHError", "CNSHErrorCode", "generate_dna"]
