"""龍魂 Python SDK

DNA: #龍芯⚡️丙午·丙申·丙辰·戊子·坎-SDK-SETUP-v2.1
"""
from setuptools import setup, find_packages

setup(
    name="longhun",
    version="2.1.0",
    description="中国自主可控 AI 人格路由器（v2.1 · 内联引擎·零依赖可用）",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="UID9622 · 诸葛鑫",
    url="https://gitee.com/longhun/longhun-system",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "httpx>=0.27.0,<1.0.0",
        "pydantic>=2.0.0,<3.0.0",
    ],
    package_data={
        "longhun": ["py.typed"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: OS Independent",
    ],
)
