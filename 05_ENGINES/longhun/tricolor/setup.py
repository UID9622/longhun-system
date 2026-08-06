# 🐉 龙魂·三色审计 SDK setup
# DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-TRICOLOR-SETUP-v1.1-UID9622
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

from setuptools import setup, find_packages

setup(
    name="longhun-tricolor",
    version="1.1.0",
    author="诸葛鑫（UID9622）",
    author_email="uid9622@longhun-system",
    description="龍魂·三色审计 SDK — 中文原生AI合规治理操作层标准",
    long_description=open("README.md", encoding="utf-8").read() if False else "",
    long_description_content_type="text/markdown",
    url="https://github.com/UID9622/longhun-system",
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MulanPSL v2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
    ],
)
