from setuptools import setup, find_packages

setup(
    name="lh_standard_adapter",
    version="1.0.0",
    description="LongHun Standard Adapter — wrap JSON payloads with DNA traceability and behavioral audit metadata",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="LongHun Core · UID9622",
    author_email="uid9622@petalmail.com",
    url="https://uid9622.cn",
    license="CC BY-NC-SA 4.0",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.9",
    include_package_data=True,
    package_data={
        "lh_standard_adapter": ["schemas/*.json"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Free for non-commercial use",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security :: Cryptography",
    ],
    keywords="longhun, dna, traceability, audit, ai, behavioral-cryptography, seven-factor, hexagram",
)
