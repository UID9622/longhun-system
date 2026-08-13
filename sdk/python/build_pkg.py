#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙酉·壬戌·戌时·䷬萃-SDK-PYTHON-BUILD_PKG-UID9622-3F79D790
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""Build longhun-tricolor Python package"""
import shutil
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
SRC = ROOT / "longhun_tricolor"
README = ROOT / "README.md"

DIST.mkdir(exist_ok=True)

# Version
version = "1.1.0"
pkg_name = f"longhun_tricolor-{version}"

# Clean
for f in DIST.glob("*"):
    f.unlink()

# Gather source files
files = list(SRC.rglob("*.py"))
print(f"Packing {len(files)} Python files:")

# Create sdist (tar.gz)
sdist_path = DIST / f"{pkg_name}.tar.gz"
with tarfile.open(sdist_path, "w:gz") as tar:
    for f in files:
        rel = str(f.relative_to(ROOT))
        tar.add(f, arcname=f"{pkg_name}/{rel}")
        print(f"  + {rel}")
    # Add README and setup files
    for extra in ["README.md", "setup.py", "pyproject.toml"]:
        p = ROOT / extra
        if p.exists():
            tar.add(p, arcname=f"{pkg_name}/{extra}")
            print(f"  + {extra}")

print(f"\n✅ sdist: {sdist_path} ({sdist_path.stat().st_size} bytes)")

# Create wheel (.whl)
# Simple approach: just zip the package
wheel_name = f"longhun_tricolor-{version}-py3-none-any.whl"
wheel_path = DIST / wheel_name
with zipfile.ZipFile(wheel_path, "w", zipfile.ZIP_DEFLATED) as zf:
    # Add package files
    for f in files:
        rel = str(f.relative_to(ROOT))
        zf.write(f, arcname=rel)
        print(f"  + wheel:{rel}")
    # Add dist-info
    info_dir = f"longhun_tricolor-{version}.dist-info"
    meta_lines = [
        "Metadata-Version: 2.1",
        f"Name: longhun-tricolor",
        f"Version: {version}",
        "Author: 诸葛鑫 (UID9622)",
        "Author-email: uid9622@dragon-soul.io",
        "License: MulanPSL-2.0",
        "Requires-Dist: httpx>=0.24.0",
        "Requires-Python: >=3.8",
        "Summary: 🐉 龙魂·三色审计 Python SDK — 中国AI合规参考标准",
        "Classifier: Programming Language :: Python :: 3",
        "Classifier: License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
    ]
    zf.writestr(f"{info_dir}/METADATA", "\n".join(meta_lines))
    zf.writestr(f"{info_dir}/WHEEL",
        f"Wheel-Version: 1.0\nGenerator: longhun-build\nRoot-Is-Purelib: true\n"
        f"Tag: py3-none-any\n")
    zf.writestr(f"{info_dir}/top_level.txt", "longhun_tricolor\n")
    zf.writestr(f"{info_dir}/RECORD", "")

print(f"\n✅ wheel: {wheel_path} ({wheel_path.stat().st_size} bytes)")
print("\n🟢 Build complete!")
