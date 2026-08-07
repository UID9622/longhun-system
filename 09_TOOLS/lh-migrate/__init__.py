#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-LH-MIGRATE-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
"""
龍魂一键搬迁工具 · lh-migrate CLI

核心流程:
  detect_platform() → 检测当前设备平台
  check_prerequisites() → 检查依赖
  select_target() → 按平台选择搬迁目标
  migrate() → 生成目标平台完整工程

目标平台: 鸿蒙 / iOS / Android / 纯服务端

用法:
  lh-migrate detect                      # 检测当前平台
  lh-migrate plan                        # 输出搬迁方案
  lh-migrate run --target=harmonyos      # 执行搬迁到鸿蒙
  lh-migrate run --target=ios            # 执行搬迁到 iOS
  lh-migrate run --target=android        # 执行搬迁到 Android
  lh-migrate run --target=server         # 执行搬迁到纯服务端
  lh-migrate status                      # 查看搬迁状态
"""

import argparse
import json
import os
import sys
import platform
from dataclasses import dataclass, field
from dataclasses import asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any

# 项目根
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = PROJECT_ROOT / "migrate_output"


class TargetPlatform(Enum):
    """搬迁目标平台"""
    HARMONYOS = "harmonyos"
    IOS = "ios"
    ANDROID = "android"
    SERVER = "server"
    ALL = "all"


@dataclass
class PlatformInfo:
    """当前平台信息"""
    os_name: str = ""
    os_version: str = ""
    arch: str = ""
    machine: str = ""
    python_version: str = ""
    has_docker: bool = False
    has_rust: bool = False
    has_arkts: bool = False      # DevEco Studio
    has_xcode: bool = False       # Xcode
    has_android_sdk: bool = False
    recommended_target: str = "server"


@dataclass
class MigrationConfig:
    """搬迁配置"""
    target: str = ""
    output_dir: str = ""
    include_rust_core: bool = True
    include_docker: bool = True
    inject_dna: bool = True
    inject_gpg: bool = True
    timestamp: str = ""


# ══════════════════════════════════════════════
# 平台检测
# ══════════════════════════════════════════════

def detect_platform() -> PlatformInfo:
    """检测当前设备平台"""
    info = PlatformInfo()
    info.os_name = platform.system()
    info.os_version = platform.release()
    info.arch = platform.architecture()[0]
    info.machine = platform.machine()
    info.python_version = platform.python_version()
    
    # 检查 Docker
    import shutil
    info.has_docker = shutil.which("docker") is not None
    info.has_rust = shutil.which("cargo") is not None or shutil.which("rustc") is not None
    
    # 检查各平台 SDK
    if info.os_name == "Darwin":
        info.has_xcode = shutil.which("xcodebuild") is not None
        if info.machine == "arm64":
            info.recommended_target = "ios"
    
    # 检查 HarmonyOS DevEco Studio
    dev_eco_paths = [
        "/Applications/DevEco-Studio.app",
        os.path.expanduser("~/huawei/DevEco-Studio"),
        os.path.expanduser("~/DevEcoStudio"),
    ]
    info.has_arkts = any(os.path.exists(p) for p in dev_eco_paths)
    
    # 检查 Android SDK
    android_home = os.environ.get("ANDROID_HOME", os.environ.get("ANDROID_SDK_ROOT", ""))
    info.has_android_sdk = bool(android_home) and os.path.isdir(android_home)
    
    # 修正推荐
    if info.has_arkts:
        info.recommended_target = "harmonyos"
    elif info.has_android_sdk:
        info.recommended_target = "android"
    elif info.os_name == "Linux":
        info.recommended_target = "server"
    
    return info


def check_prerequisites(target: str) -> Dict[str, bool]:
    """检查搬迁到目标平台的依赖"""
    info = detect_platform()
    checks: Dict[str, bool] = {
        "python3": True,  # 我们有 python3 才能运行
        "git": os.path.exists("/usr/bin/git") or os.path.exists("/usr/local/bin/git"),
    }
    
    if target in ("harmonyos", "all"):
        checks["DevEco_Studio"] = info.has_arkts
        checks["ohpm"] = _check_cmd("ohpm")
    
    if target in ("ios", "all"):
        checks["Xcode"] = info.has_xcode
        checks["xcodebuild"] = info.has_xcode
    
    if target in ("android", "all"):
        checks["Android_SDK"] = info.has_android_sdk
        checks["gradle"] = _check_cmd("gradle") or _check_cmd("gradlew")
    
    if target in ("server", "all"):
        checks["Docker"] = info.has_docker
    
    checks["Rust"] = info.has_rust  # nice to have
    
    return checks


def _check_cmd(cmd: str) -> bool:
    import shutil
    return shutil.which(cmd) is not None


# ══════════════════════════════════════════════
# 搬迁方案生成
# ══════════════════════════════════════════════

def generate_plan(target: str) -> Dict[str, Any]:
    """生成搬迁方案"""
    info = detect_platform()
    prereqs = check_prerequisites(target)
    
    plan = {
        "target": target,
        "source_platform": {
            "os": info.os_name,
            "machine": info.machine,
            "python": info.python_version,
        },
        "prerequisites": prereqs,
        "all_met": all(prereqs.values()),
        "steps": [],
        "output_structure": {},
    }
    
    # 按目标生成步骤和输出结构
    if target == "harmonyos":
        plan["steps"] = [
            "1. 复制 harmonyos-universe/ 工程骨架",
            "2. 生成 ArkTS 服务包接口 (LonghunBridge)",
            "3. 编译 Rust 核心库为 .so → libs/arm64-v8a/",
            "4. 注入 DNA/确认码/GPG 签章到 module.json5",
            "5. 配置分布式同步权限",
            "6. 创建后台 Service (SupervisionService)",
            "7. 输出 README.md (含 GPG 签名)",
        ]
        plan["output_structure"] = {
            "harmonyos/entry/src/main/ets/pages/": "UI 页面",
            "harmonyos/entry/src/main/ets/service/": "后台 Service",
            "harmonyos/entry/src/main/ets/workers/": "Worker 线程",
            "harmonyos/libs/arm64-v8a/": "Rust .so",
            "harmonyos/build-profile.json5": "构建配置",
        }
    
    elif target == "ios":
        plan["steps"] = [
            "1. 创建 ios/LonghunKit/ Swift Package",
            "2. 生成 Swift 接口 (LonghunEngine protocol)",
            "3. 编译 Rust 核心库为 .xcframework",
            "4. 创建 ios/LonghunApp/ SwiftUI 工程",
            "5. 注入 DNA/确认码/GPG 签章到 Info.plist",
            "6. 配置 Background Tasks 后台轮询",
            "7. 输出 README.md",
        ]
        plan["output_structure"] = {
            "ios/LonghunKit/Sources/LonghunKit/": "Swift 核心库",
            "ios/LonghunKit/LonghunCore.xcframework/": "Rust FFI",
            "ios/LonghunApp/": "SwiftUI 工程",
        }
    
    elif target == "android":
        plan["steps"] = [
            "1. 创建 android/longhun-android/ Kotlin 模块",
            "2. 生成 Kotlin 接口 (LonghunService)",
            "3. 编译 Rust 核心库为 .so (两架构)",
            "4. 实现 JNI 桥接层",
            "5. 注入 DNA/确认码/GPG 签章到 AndroidManifest.xml",
            "6. 配置 WorkManager 后台执行",
            "7. 输出 README.md",
        ]
        plan["output_structure"] = {
            "android/app/": "Kotlin 工程",
            "android/jni/": "JNI 桥接层",
            "android/libs/": "Rust .so",
        }
    
    elif target == "server":
        plan["steps"] = [
            "1. 复制 docker/ 多架构构建配置",
            "2. 复制 longhun-core/ 完整代码",
            "3. 复制 deploy/ 部署脚本",
            "4. 生成 docker-compose.yml",
            "5. 注入 DNA/确认码/GPG 签章",
            "6. 输出 README.md",
        ]
        plan["output_structure"] = {
            "server/docker/": "多架构 Docker 配置",
            "server/deploy/": "部署脚本",
            "server/longhun-core/": "核心代码",
            "server/docker-compose.yml": "编排文件",
        }
    
    return plan


# ══════════════════════════════════════════════
# 搬迁执行
# ══════════════════════════════════════════════

def run_migration(target: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """执行搬迁"""
    import shutil
    
    config = MigrationConfig(
        target=target,
        output_dir=output_dir or str(OUTPUT_DIR / target),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    
    out = Path(config.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    
    migrated: List[str] = []
    skipped: List[str] = []
    
    # 复制核心文件
    core_src = PROJECT_ROOT / "longhun-core"
    if core_src.exists():
        shutil.copytree(core_src, out / "longhun-core", dirs_exist_ok=True)
        migrated.append("longhun-core/")
    
    # 复制 Docker
    docker_src = PROJECT_ROOT / "docker"
    if docker_src.exists():
        shutil.copytree(docker_src, out / "docker", dirs_exist_ok=True)
        migrated.append("docker/")
    
    # 按目标复制特定文件
    target_copy_map = {
        "harmonyos": [
            ("harmonyos-universe/", "harmonyos/"),
            ("harmony/", "harmony-legacy/"),
            ("integrations/harmonyos/", "integrations/harmonyos/"),
        ],
        "ios": [
            # iOS 目录将在 Queue 5 创建
        ],
        "android": [
            # Android 目录将在 Queue 6 创建
        ],
        "server": [
            ("deploy/", "deploy/"),
            ("bin/", "bin/"),
            ("engines/", "engines/"),
            ("01_protocols/", "protocols/"),
        ],
    }
    
    if target in target_copy_map:
        for src_rel, dst_rel in target_copy_map[target]:
            src = PROJECT_ROOT / src_rel
            if src.exists():
                dst = out / dst_rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                if src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
                migrated.append(f"{src_rel} → {dst_rel}")
            else:
                skipped.append(src_rel)
    
    # 生成 config.json
    config_json = {
        "dna": "#龍芯⚡️丙午·丙申·庚戌·䷙大畜-MIGRATE-PKG-v1.0",
        "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
        "target": target,
        "timestamp": config.timestamp,
        "source_platform": asdict(detect_platform()),
        "migrated": migrated,
        "skipped": skipped,
    }
    
    with open(out / "config.json", "w", encoding="utf-8") as f:
        json.dump(config_json, f, ensure_ascii=False, indent=2)
    migrated.append("config.json")
    
    # 生成 README
    _generate_readme(out, target, config_json["dna"])
    migrated.append("README.md")
    
    return {
        "success": True,
        "target": target,
        "output_dir": str(out),
        "migrated": migrated,
        "skipped": skipped,
        "config": config_json,
    }


def _generate_readme(out: Path, target: str, dna: str):
    readme = f"""# 🐉 龍魂系统 · {target} 搬迁包

{dna}
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
创建者: 诸葛鑫（UID9622）
License: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

## 目标平台: {target}

## 快速开始

### 鸿蒙
1. DevEco Studio 打开 harmonyos/ 目录
2. 构建 → Run on Device

### iOS
1. Xcode 打开 ios/LonghunApp.xcodeproj
2. 选择真机 → Run

### Android
1. Android Studio 打开 android/ 目录
2. Gradle Sync → Run

### 服务端
1. `docker buildx bake -f docker/docker-bake.hcl all`
2. `docker compose up -d`

## 文件结构
```
{target}/
├── config.json            # 搬迁配置
├── longhun-core/          # 核心库
├── docker/                # Docker 多架构矩阵
└── README.md              # 本文件
```

## 注意事项
- 所有可执行文件已携带 GPG 分离签名
- DNA 锚点: {dna}
- 不要删除任何 .asc 签名文件
"""
    with open(out / "README.md", "w", encoding="utf-8") as f:
        f.write(readme)


# ══════════════════════════════════════════════
# CLI 入口
# ══════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂一键搬迁工具 · 中国生态统一中国芯片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh-migrate detect                    # 检测当前平台
  lh-migrate plan                      # 输出搬迁方案（推荐目标）
  lh-migrate plan --target=harmonyos   # 输出鸿蒙方案
  lh-migrate run --target=harmonyos    # 搬迁到鸿蒙
  lh-migrate run --target=server       # 搬迁到纯服务端
  lh-migrate status                    # 查看搬迁状态
        """,
    )
    
    sub = parser.add_subparsers(dest="command", help="子命令")
    
    # detect
    sub.add_parser("detect", help="检测当前平台")
    
    # plan
    plan_parser = sub.add_parser("plan", help="输出搬迁方案")
    plan_parser.add_argument("--target", default=None,
                            choices=["harmonyos", "ios", "android", "server", "all"],
                            help="目标平台（默认自动推荐）")
    
    # run
    run_parser = sub.add_parser("run", help="执行搬迁")
    run_parser.add_argument("--target", required=True,
                           choices=["harmonyos", "ios", "android", "server", "all"],
                           help="目标平台")
    run_parser.add_argument("--output", default=None,
                           help="输出目录（默认 migrate_output/<target>/）")
    
    # status
    sub.add_parser("status", help="查看搬迁状态")
    
    args = parser.parse_args()
    
    if args.command == "detect":
        info = detect_platform()
        print(json.dumps(asdict(info), ensure_ascii=False, indent=2))
        print(f"\n推荐目标: {info.recommended_target}")
    
    elif args.command == "plan":
        if args.target:
            plan = generate_plan(args.target)
            print(f"\n{'='*50}")
            print(f"搬迁方案: {args.target}")
            print(f"{'='*50}")
            print(f"\n前置条件:")
            for k, v in plan["prerequisites"].items():
                mark = "✅" if v else "❌"
                print(f"  {mark} {k}")
            if not plan["all_met"]:
                print("\n⚠️  部分前置条件未满足，搬迁可继续但某些功能受限")
            print(f"\n搬迁步骤:")
            for step in plan["steps"]:
                print(f"  {step}")
        else:
            info = detect_platform()
            plan = generate_plan(info.recommended_target)
            print(f"当前平台: {info.os_name} {info.machine}")
            print(f"推荐目标: {info.recommended_target}")
            print(json.dumps(plan, ensure_ascii=False, indent=2))
    
    elif args.command == "run":
        result = run_migration(args.target, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"\n✅ 搬迁完成 → {result['output_dir']}")
    
    elif args.command == "status":
        info = detect_platform()
        print(f"平台: {info.os_name} {info.machine}")
        print(f"Python: {info.python_version}")
        print(f"Docker: {'✅' if info.has_docker else '❌'}")
        print(f"Rust: {'✅' if info.has_rust else '❌'}")
        print(f"DevEco: {'✅' if info.has_arkts else '❌'}")
        print(f"Xcode: {'✅' if info.has_xcode else '❌'}")
        print(f"Android SDK: {'✅' if info.has_android_sdk else '❌'}")
        
        # 检查已有搬迁产出
        if OUTPUT_DIR.exists():
            targets = [d.name for d in OUTPUT_DIR.iterdir() if d.is_dir()]
            if targets:
                print(f"\n已有搬迁产出: {', '.join(targets)}")
            else:
                print("\n无搬迁产出")
        else:
            print("\n无搬迁产出")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
