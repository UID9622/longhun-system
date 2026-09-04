#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 CNSH 套件 · 安装配置

DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CNSH-SETUP-UID9622
"""

from setuptools import setup, find_packages

setup(
    name="cnsh-suite",
    version="1.0.0",
    author="诸葛鑫 · UID9622",
    description="🐉 CNSH 套件 · DeepSeek Harness 插件集（龍魂主权底座）",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "pytest>=7.0",
    ],
    entry_points={
        "console_scripts": [
            "cnsh=cnsh_suite.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)",
        "Operating System :: OS Independent",
    ],
)
