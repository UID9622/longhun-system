#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🧬 龍魂操作日记引擎 · setup.py
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

DNA: #龍芯⚡️丙午·癸巳·甲辰·庚午·䷑蛊-SETUP-CONFIG-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
责任: UID9622·不免责

安装配置文件，使龍魂系统可通过 pip install 安装。
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取 README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")
else:
    long_description = "龍魂操作日记引擎 - 完整的本地去中心化身份系统"

# 读取 requirements
requirements_file = Path(__file__).parent / "requirements.txt"
install_requires = []
if requirements_file.exists():
    install_requires = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").split("\n")
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="longhun-operation-log-engine",
    version="1.0.0",
    author="UID9622",
    author_email="uid9622@longhun.dev",
    description="龍魂系统：本地去中心化身份系统 - DNA认人·习惯识别·本地主权",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UID9622/longhun-system",
    project_urls={
        "Bug Tracker": "https://github.com/UID9622/longhun-system/issues",
        "Documentation": "https://github.com/UID9622/longhun-system/blob/main/cnsh-core/ai-tools/operation_log_engine/README.md",
    },
    packages=find_packages(where="."),
    package_data={
        "operation_log_engine": [
            "*.md",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Security :: Cryptography",
        "Topic :: System :: Archiving :: Backup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: Chinese (Traditional)",
    ],
    python_requires=">=3.10",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "operation-log-engine=operation_log_engine.cli:main",
            "longhun-log=operation_log_engine.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "longhun",
        "龍魂",
        "identity",
        "dna",
        "habits",
        "security",
        "cryptography",
        "local",
        "decentralized",
    ],
    license="MIT",
)
