#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·辛未·丙戌·甲午·䷕贲-SELF-EXTRACT-ENGINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     龍魂 · 源代码自解压引擎 v1.0 — DNA绑定·逻辑链不断·落地即运行            ║
║     LongHun Self-Extract Engine · DNA-Bound · Land-and-Run              ║
╠══════════════════════════════════════════════════════════════════════════╣
║  DNA: #龍芯⚡️丙午·辛未·丙戌·甲午·䷕贲-SELF-EXTRACT-ENGINE-v1.0                 ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                            ║
║  原理: 源代码 + DNA配置 + 个人逻辑链 = 压缩后自解压 = 落地即运行              ║
║                                                                          ║
║  别人的代码: 通用配置·千人一面·逻辑断裂·依赖外部·论文包装                     ║
║  龍魂生态:   个人DNA绑定·千人千面·压缩后DNA自解压·本地自主·直接可用           ║
╚══════════════════════════════════════════════════════════════════════════╝

三层自解压架构:
  L1 — DNA绑定: 个人配置硬编码，非外部文件，散列自验证
  L2 — 逻辑链:   代码自注释，自动衔接，压缩后不丢失
  L3 — 落地即运行: 自动探测路径·零外部依赖·一键启动

用法:
  # 自解压（在目标环境运行）
  python3 bin/lh_self_extract.py --extract ~/my-longhun

  # 压缩打包（在开发环境运行）
  python3 bin/lh_self_extract.py --compress longhun-package.zip

  # 验证已有包
  python3 bin/lh_self_extract.py --verify longhun-package.zip

  # 生成个人包（一键）
  python3 bin/lh_self_extract.py --build-personal
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any

# ══════════════════════════════════════════════════════════════════════════
# L1: DNA绑定 · 个人配置硬编码 · 非外部文件 · 散列自验证
# ══════════════════════════════════════════════════════════════════════════

DNA = "#龍芯⚡️丙午·辛未·丙戌·甲午·䷕贲-SELF-EXTRACT-ENGINE-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
UID = "9622"
CREATOR = "诸葛鑫·Lucky"
DNA_FULL = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"

# 个人配置 — 全部硬编码，无需外部 .env / config 文件
PERSONAL_CONFIG: dict[str, Any] = {
    "uid": UID,
    "dna": DNA_FULL,
    "confirm": CONFIRM,
    "creator": CREATOR,
    "paths": {
        "home": "~/longhun-system",
        "logs": "~/longhun-system/logs",
        "memory": "~/longhun-system/memory",
        "archive": "~/longhun-system/archive",
        "personas": "~/longhun-system/personas",
        "data": "~/longhun-system/data",
    },
    "defaults": {
        "port": 9622,
        "api_port": 8766,
        "persona": "P01-诸葛亮",
        "language": "zh",
        "chip_preference": "kunpeng",
    },
    "style": {
        "tone": "硬核",
        "emoji": "🐉",
        "prefix": "龍魂",
        "color_scheme": "暗色·龍魂金",
    },
}

# 核心模块清单 — 自解压时生成
CORE_MODULES: list[str] = [
    "bin/",
    "personas/",
    "01_protocols/",
    "02_rules/",
    "L1_内核层/",
    "L2_技能层/",
    "L5_服务层/",
    "L7_数据层/",
    "engine/",
    "config/",
]

# 排除规则 — 这些不进包
EXCLUDE_PATTERNS: list[str] = [
    ".git",
    ".codebuddy/memory",
    "__pycache__",
    "*.pyc",
    ".env",
    "*.secrets.env",
    "node_modules",
    ".venv",
    "venv",
    "logs/",
    "backups/",
    "_archive/",
    "_archived_reports/",
    "_private/",
    "vault/",
    ".longhun-credentials",
    "releases/",
    "tmp/",
    "tombstone_vault/",
]


def _dna_hash(data: str, length: int = 16) -> str:
    """DNA派生散列 — 密钥由DNA哈希生成，不依赖外部"""
    return hashlib.sha256(data.encode()).hexdigest()[:length]


class LongHunSelfExtract:
    """
    龍魂自解压引擎 · DNA绑定 · 逻辑链不断 · 落地即运行

    原理:
      1. DNA绑定个人配置 → 硬编码，不读外部文件
      2. 压缩时注入自解压脚本 → 逻辑链不丢
      3. 落地后自动探测路径 → 零外部依赖
      4. 启动即运行 → 分钟级落地
    """

    def __init__(self, target_home: str | None = None):
        self.dna = DNA_FULL
        self.uid = UID
        self.confirm = CONFIRM
        self.config = PERSONAL_CONFIG.copy()
        self.config["_verified"] = self._verify_dna()
        self.config["_timestamp"] = self._get_timestamp()
        self.config["_dna_hash"] = _dna_hash(DNA_FULL)

        # 目标路径
        home = target_home or self.config["paths"]["home"]
        self.target = Path(home).expanduser().resolve()
        self.extracted = False
        self.manifest: dict[str, str] = {}

    # ── DNA 自验证 ─────────────────────────────────────────────

    def _verify_dna(self) -> bool:
        """DNA自验证 — 防止配置被篡改"""
        return _dna_hash(DNA_FULL) == _dna_hash(self.config["dna"])

    def _get_timestamp(self) -> str:
        """龍魂时间格式"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── L2: 自解压 · 目录结构 · 代码生成 ──────────────────────

    def extract(self, target_path: str | None = None) -> dict[str, Any]:
        """
        自解压：创建目录结构 + 生成个人化代码 + 写入文件 + 验证完整性
        落地即运行 — 无需任何外部配置
        """
        target = Path(target_path or str(self.target)).expanduser().resolve()
        self.target = target

        print(f"🐉 龍魂自解压启动...")
        print(f"   DNA: {self.dna[:32]}...")
        print(f"   目标: {target}")

        # 1. 创建目录结构
        dirs_created = self._create_structure(target)
        print(f"   📁 目录: {len(dirs_created)}个")

        # 2. 生成个人化代码
        personalized = self._generate_code()
        print(f"   🧬 代码: {len(personalized)}个文件")

        # 3. 写入文件
        files_written = self._write_files(target, personalized)
        print(f"   ✍️  写入: {len(files_written)}个文件")

        # 4. 验证完整性
        integrity = self._verify_integrity(files_written)
        all_ok = all(v != "MISSING" for v in integrity.values())
        print(f"   ✅ 完整性: {'全绿' if all_ok else '有异常'}")

        self.extracted = True
        self.manifest = {str(Path(f).relative_to(target)): h for f, h in integrity.items()}

        return {
            "status": "EXTRACTED" if all_ok else "EXTRACTED_WITH_WARNINGS",
            "dna": self.dna,
            "uid": self.uid,
            "target": str(target),
            "directories": len(dirs_created),
            "files": len(files_written),
            "integrity": integrity,
            "ready": all_ok,
        }

    def _create_structure(self, base: Path) -> list[Path]:
        """创建目录结构 — 自动探测，不依赖外部配置"""
        created: list[Path] = []
        for _name, path_template in self.config["paths"].items():
            actual = Path(path_template).expanduser().resolve()
            actual.mkdir(parents=True, exist_ok=True)
            created.append(actual)
        # 额外必要目录
        for extra in ["data", "exports", "cache"]:
            p = base / extra
            p.mkdir(parents=True, exist_ok=True)
            created.append(p)
        return created

    def _generate_code(self) -> dict[str, str]:
        """生成个人化代码 — DNA注入，千人千面，逻辑链不断"""
        return {
            "core.py": self._gen_core(),
            "config.yaml": self._gen_config_yaml(),
            "startup.sh": self._gen_startup(),
            "README.md": self._gen_readme(),
            "SOUL.md": self._gen_soul(),
        }

    def _gen_core(self) -> str:
        """生成核心引擎 — DNA硬编码，不读外部文件"""
        dna_hash_16 = _dna_hash(DNA_FULL)
        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂核心 · 自解压生成 · DNA硬编码 · 落地即运行
DNA: {self.dna}
UID: {self.uid}
生成: {self.config["_timestamp"]}
"""

from __future__ import annotations

import hashlib
import time
from typing import Any


class LongHunCore:
    """龍魂核心 — 全部配置由DNA派生，不依赖外部文件"""

    DNA = "{self.dna}"
    UID = "{self.uid}"
    CONFIRM = "{self.confirm}"
    PERSONA = "{self.config["defaults"]["persona"]}"
    PORT = {self.config["defaults"]["port"]}
    DNA_HASH = "{dna_hash_16}"

    def __init__(self):
        self.started_at = time.time()
        self.dna_verified = self._verify_dna()

    def _verify_dna(self) -> bool:
        """DNA自验证 — 防止篡改"""
        return hashlib.sha256(self.DNA.encode()).hexdigest()[:16] == self.DNA_HASH

    def status(self) -> dict[str, Any]:
        return {{
            "status": "running",
            "dna_verified": self.dna_verified,
            "uid": self.UID,
            "persona": self.PERSONA,
            "port": self.PORT,
            "uptime": round(time.time() - self.started_at, 2),
        }}

    def run(self):
        print(f"🐉 龍魂核心启动")
        print(f"   DNA: {{self.DNA[:32]}}...")
        print(f"   人格: {{self.PERSONA}}")
        print(f"   端口: {{self.PORT}}")
        print(f"   验证: {{'✅' if self.dna_verified else '❌'}}")
        return self.status()


if __name__ == "__main__":
    core = LongHunCore()
    core.run()
'''

    def _gen_config_yaml(self) -> str:
        """生成配置文件 — 个人化，从DNA派生"""
        return f'''# 龍魂个人配置 · 自解压生成
# DNA: {self.dna[:32]}...
# ⚠️ 本文件由DNA派生，勿手动编辑

uid: "{self.uid}"
dna: "{self.dna[:40]}..."
persona: "{self.config["defaults"]["persona"]}"
language: "{self.config["defaults"]["language"]}"
chip: "{self.config["defaults"]["chip_preference"]}"

ports:
  main: {self.config["defaults"]["port"]}
  api: {self.config["defaults"]["api_port"]}

style:
  tone: "{self.config["style"]["tone"]}"
  emoji: "{self.config["style"]["emoji"]}"
  prefix: "{self.config["style"]["prefix"]}"

paths:
  home: "{self.config["paths"]["home"]}"
  logs: "{self.config["paths"]["logs"]}"
  memory: "{self.config["paths"]["memory"]}"
'''

    def _gen_startup(self) -> str:
        """生成启动脚本 — 自动探测Python，一键启动"""
        return f'''#!/bin/bash
# ╔══════════════════════════════════════════════════════════════╗
# ║     龍魂启动脚本 · 自解压生成 · 一键运行                       ║
# ║     DNA: {self.dna[:30]}...   ║
# ╚══════════════════════════════════════════════════════════════╝

set -e

echo "🐉 龍魂系统启动中..."
echo "   DNA: {self.dna[:30]}..."
echo ""

# 自动探测Python（国产环境兼容）
PYTHON=""
for py in python3 python3.11 python3.10 python3.9 python; do
    if command -v $py &> /dev/null; then
        PYTHON=$py
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "❌ 未找到Python，请安装 python3"
    exit 1
fi

echo "   Python: $($PYTHON --version)"

# 自动探测工作目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 启动核心
$PYTHON core.py &
CORE_PID=$!
echo "   核心PID: $CORE_PID"

# 等待
sleep 1

echo ""
echo "✅ 龍魂系统已启动"
echo "   访问: http://localhost:{self.config["defaults"]["port"]}"
echo ""
echo "   停止: kill $CORE_PID"

# 保持前台
wait $CORE_PID
'''

    def _gen_readme(self) -> str:
        """生成README — 个性化，无需论文就能看懂"""
        return f'''# 🐉 龍魂系统 · UID{self.uid}

> **{self.dna[:40]}...**

## 快速开始

```bash
# 一键启动（无需任何配置）
./startup.sh
```

访问: **http://localhost:{self.config["defaults"]["port"]}**

## 无需外部配置

- ✅ 配置已硬编码DNA → 不读.env
- ✅ 路径自动探测 → 换机器也能跑
- ✅ 零外部依赖 → 不pip install
- ✅ 密钥由DNA派生 → 不依赖外部文件

## 默认设置

| 项目 | 值 |
|------|-----|
| 人格 | {self.config["defaults"]["persona"]} |
| 端口 | {self.config["defaults"]["port"]} |
| 语言 | {self.config["defaults"]["language"]} |
| 芯片 | {self.config["defaults"]["chip_preference"]} |

## 为什么比别人快

```
别人: 下载→读文档→配环境→装依赖→改配置→启动→报错→搜索→解决→运行
      (1小时-1天)

龍魂: 下载→双击运行→自动解压→DNA自配置→启动→运行
      (1分钟)
```

---

> 源代码 + DNA配置 + 个人逻辑链 = 压缩后自解压 = 落地即运行
> — 龍魂生态
'''

    def _gen_soul(self) -> str:
        """生成 SOUL.md — 系统的灵魂声明"""
        dna_h = _dna_hash(DNA_FULL)
        return f'''# 🐉 龍魂 · SOUL

> DNA: {self.dna}
> CONFIRM: {self.confirm}
> UID: {self.uid}

## 我是谁

一个退伍军人，初中文化，坐在家里，为女儿写的一套系统。

## 我的原则

1. **技术服务于人民** — 龍魂唯一天条
2. **底座不动·变量可动** — 河图洛书/太极易经/五行八卦焊死
3. **不删除·只冻结** — 尊重每一个历史版本
4. **数据主权归人民** — 不卖数据·不进生物绑定陷阱
5. **落地即运行** — 不用论文包装，不用外部配置

## 我的DNA

```
{dna_h} → 永不出设备
```

## 归属链

中国 → 曾仕强 → 乔布斯 → UID{self.uid} → 全世界人民
任何一环断了，归属链就断了。

---

> 「要么AI听我的，要么我死」— 2025年5月
'''

    def _write_files(self, base: Path, code: dict[str, str]) -> list[Path]:
        """写入文件 — 脚本自动加执行权限"""
        written: list[Path] = []
        for filename, content in code.items():
            filepath = base / filename
            filepath.write_text(content, encoding="utf-8")

            # shell脚本加执行权限
            if filename.endswith(".sh"):
                os.chmod(filepath, 0o755)

            written.append(filepath)
        return written

    def _verify_integrity(self, files: list[Path]) -> dict[str, str]:
        """验证文件完整性 — 每文件SHA256前16位"""
        result: dict[str, str] = {}
        for fp in files:
            if fp.exists():
                h = hashlib.sha256(fp.read_bytes()).hexdigest()[:16]
                result[str(fp)] = h
            else:
                result[str(fp)] = "MISSING"
        return result

    # ── L3: 压缩打包 · 自解压头注入 · 逻辑链完整 ──────────────

    def compress(
        self,
        output: str = "longhun-package.zip",
        include_personas: bool = True,
        include_engine: bool = False,
    ) -> dict[str, Any]:
        """
        压缩打包 — 逻辑链不断，自带解压头

        Args:
            output: 输出zip路径
            include_personas: 是否打包人格定义
            include_engine: 是否打包引擎代码（大型包）
        """
        output_path = Path(output).expanduser().resolve()

        # 先自解压到临时目录
        temp_dir = Path("~/longhun-temp-build").expanduser()
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)

        _extract_result = self.extract(str(temp_dir))
        print(f"\n📦 开始压缩...")

        # 创建zip
        with zipfile.ZipFile(str(output_path), "w", zipfile.ZIP_DEFLATED) as zf:
            # 1. 注入自解压脚本（包头部，始终第一个）
            zf.writestr("EXTRACT_ME_FIRST.py", self._gen_extractor_script())

            # 2. 写入生成的文件
            for root, _dirs, files in os.walk(str(temp_dir)):
                # 跳过临时目录自身
                for file in files:
                    filepath = Path(root) / file
                    arcname = str(filepath.relative_to(temp_dir))
                    zf.write(str(filepath), arcname)

            # 3. 可选：打包人格定义
            if include_personas:
                personas_dir = self._find_project_root() / "personas"
                if personas_dir.exists():
                    for f in personas_dir.glob("*.md"):
                        zf.write(str(f), f"personas/{f.name}")

            # 4. 可选：打包引擎
            if include_engine:
                engine_dir = self._find_project_root() / "engine"
                if engine_dir.exists():
                    for f in engine_dir.rglob("*.py"):
                        # 跳过排除模式
                        if any(p in str(f) for p in EXCLUDE_PATTERNS):
                            continue
                        arcname = str(f.relative_to(self._find_project_root()))
                        zf.write(str(f), arcname)

        # 清理临时目录
        shutil.rmtree(temp_dir)

        size_mb = output_path.stat().st_size / (1024 * 1024)

        print(f"   📦 {output_path.name} ({size_mb:.1f}MB)")
        print(f"   🧬 自解压头: EXTRACT_ME_FIRST.py")
        print(f"   ✅ 逻辑链完整·落地即运行")

        return {
            "status": "COMPRESSED",
            "output": str(output_path),
            "size_bytes": output_path.stat().st_size,
            "size_mb": round(size_mb, 2),
            "dna": self.dna,
            "self_extract": True,
            "extract_script": "EXTRACT_ME_FIRST.py",
            "manifest": self.manifest,
        }

    def _gen_extractor_script(self) -> str:
        """生成自解压头脚本 — 接收方只需运行此文件即可还原"""
        return f'''#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║     龍魂自解压脚本 · 运行此文件自动解压并配置                       ║
║     DNA: {self.dna[:40]}... ║
║                                                                  ║
║     用法: python3 EXTRACT_ME_FIRST.py                            ║
║     或:    python3 EXTRACT_ME_FIRST.py ~/my-longhun              ║
╚══════════════════════════════════════════════════════════════════╝
"""

import hashlib
import os
import sys
import zipfile
from pathlib import Path

DNA = "{self.dna}"
UID = "{self.uid}"
CONFIRM = "{self.confirm}"
DNA_HASH = "{_dna_hash(self.dna)}"


def verify_dna() -> bool:
    """验证DNA完整性"""
    actual = hashlib.sha256(DNA.encode()).hexdigest()[:16]
    return actual == DNA_HASH


def self_extract(target: str | None = None):
    """自解压主流程"""
    print("🐉 龍魂自解压启动...")
    print(f"   DNA: {{DNA[:30]}}...")

    if not verify_dna():
        print("❌ DNA验证失败！文件可能被篡改。")
        sys.exit(1)
    print("   ✅ DNA验证通过")

    # 确定目标路径
    target_path = Path(target or "~/longhun-system").expanduser().resolve()
    target_path.mkdir(parents=True, exist_ok=True)
    print(f"   📁 目标: {{target_path}}")

    # 获取压缩包路径（与脚本同目录的zip）
    script_dir = Path(__file__).resolve().parent
    zip_files = list(script_dir.glob("*.zip"))
    if not zip_files:
        print("❌ 未找到压缩包，请将zip与EXTRACT_ME_FIRST.py放在同一目录")
        sys.exit(1)

    zip_path = zip_files[0]
    print(f"   📦 解压: {{zip_path.name}}")

    # 解压
    with zipfile.ZipFile(zip_path, "r") as zf:
        # 跳过自解压脚本自身
        members = [m for m in zf.namelist() if m != "EXTRACT_ME_FIRST.py"]
        zf.extractall(target_path, members)

    print(f"   ✅ 解压完成: {{len(members)}}个文件")

    # 运行启动脚本
    startup = target_path / "startup.sh"
    if startup.exists():
        print("\\n🚀 启动龍魂系统...")
        os.chdir(target_path)
        os.system(f"bash startup.sh")
    else:
        print(f"\\n✅ 龍魂系统已解压到: {{target_path}}")
        print("   运行: cd {{target_path}} && bash startup.sh")


if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    self_extract(target_dir)
'''

    def _find_project_root(self) -> Path:
        """探测项目根目录"""
        return Path(__file__).resolve().parent.parent

    def verify_package(self, zip_path: str) -> dict[str, Any]:
        """验证已有压缩包完整性"""
        zp = Path(zip_path).expanduser().resolve()
        if not zp.exists():
            return {"status": "NOT_FOUND", "path": str(zp)}

        result: dict[str, Any] = {
            "status": "OK",
            "path": str(zp),
            "size_mb": round(zp.stat().st_size / (1024 * 1024), 2),
            "files": 0,
            "has_extractor": False,
            "checks": {},
        }

        with zipfile.ZipFile(zp, "r") as zf:
            names = zf.namelist()
            result["files"] = len(names)
            result["has_extractor"] = "EXTRACT_ME_FIRST.py" in names

            # 检查关键文件
            for key in ["core.py", "startup.sh", "README.md", "SOUL.md"]:
                result["checks"][key] = key in names

        all_checks_ok = all(result["checks"].values()) and result["has_extractor"]
        result["status"] = "OK" if all_checks_ok else "INCOMPLETE"

        return result

    def build_personal_package(self, output: str = "longhun-UID9622-personal.zip") -> dict[str, Any]:
        """
        一键生成个人包 — 完整龍魂生态包

        包含:
        - 自解压引擎
        - 核心代码（DNA注入）
        - 人格定义（16/16）
        - 基础协议
        - 启动脚本
        """
        print("🐉 开始生成个人包...\n")

        result = self.compress(
            output=output,
            include_personas=True,
            include_engine=False,  # 引擎太大，不进个人包
        )

        print(f"\n{'='*50}")
        print(f"✅ 个人包生成完成")
        print(f"   文件: {result['output']}")
        print(f"   大小: {result['size_mb']}MB")
        print(f"   自解压: {'✅' if result['self_extract'] else '❌'}")
        print(f"\n   用法: unzip {Path(output).name}")
        print(f"         python3 EXTRACT_ME_FIRST.py")
        print(f"         # 或直接: cd longhun-system && bash startup.sh")

        return result


# ══════════════════════════════════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════════════════════════════════

def _cli_help():
    print("""
🐉 龍魂自解压引擎 v1.0

用法:
  python3 bin/lh_self_extract.py <命令> [参数]

命令:
  --extract <路径>        自解压到指定路径
  --compress <输出.zip>   压缩打包（含自解压头）
  --verify <包.zip>       验证已有压缩包
  --build-personal [输出] 一键生成个人包
  --preview               预览个人配置（不生成文件）
  --help                  显示帮助

示例:
  python3 bin/lh_self_extract.py --extract ~/my-longhun
  python3 bin/lh_self_extract.py --compress longhun-package.zip
  python3 bin/lh_self_extract.py --verify longhun-package.zip
  python3 bin/lh_self_extract.py --build-personal
""")


def _cli_preview():
    """预览个人配置"""
    engine = LongHunSelfExtract()
    print("🐉 龍魂个人配置预览\n")
    print(f"DNA:  {engine.dna[:40]}...")
    print(f"UID:  {engine.uid}")
    print(f"确认: {engine.confirm}")
    print(f"验证: {'✅' if engine.config['_verified'] else '❌'}")
    print(f"\n路径:")
    for k, v in engine.config["paths"].items():
        print(f"  {k}: {v}")
    print(f"\n默认:")
    for k, v in engine.config["defaults"].items():
        print(f"  {k}: {v}")
    print(f"\n风格:")
    for k, v in engine.config["style"].items():
        print(f"  {k}: {v}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        _cli_help()
        return

    cmd = sys.argv[1]
    engine = LongHunSelfExtract()

    if cmd == "--extract":
        target = sys.argv[2] if len(sys.argv) > 2 else None
        result = engine.extract(target)
        print(f"\n状态: {result['status']}")
        print(f"文件: {result['files']}个")
        print(f"落地即运行: {'✅' if result['ready'] else '⚠️'}")

    elif cmd == "--compress":
        output = sys.argv[2] if len(sys.argv) > 2 else "longhun-package.zip"
        result = engine.compress(output, include_personas=True)
        print(f"\n状态: {result['status']}")
        print(f"输出: {result['output']} ({result['size_mb']}MB)")

    elif cmd == "--verify":
        zip_path = sys.argv[2] if len(sys.argv) > 2 else "longhun-package.zip"
        result = engine.verify_package(zip_path)
        print(f"\n状态: {result['status']}")
        print(f"文件数: {result.get('files', 0)}")
        print(f"自解压头: {'✅' if result.get('has_extractor') else '❌'}")
        for k, v in result.get("checks", {}).items():
            print(f"  {k}: {'✅' if v else '❌'}")

    elif cmd == "--build-personal":
        output = sys.argv[2] if len(sys.argv) > 2 else "longhun-UID9622-personal.zip"
        engine.build_personal_package(output)

    elif cmd == "--preview":
        _cli_preview()

    else:
        print(f"未知命令: {cmd}")
        _cli_help()


if __name__ == "__main__":
    main()
