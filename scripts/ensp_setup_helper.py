# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 华为 eNSP + CNSH + 龍魂字体 安装辅助脚本 v1.2
DNA: #龍芯⚡️2026-07-04-LONGHUN-ENSP-SETUP-v1.2

说明：
- 本脚本不下载 eNSP 安装包（官方/社区下载链接时常变动，需用户手动获取）。
- 本脚本检查运行环境、定位本地龍魂资源、输出安装指引。
- 在 Windows 上可一键检查 WinPcap / Wireshark / VirtualBox 是否已安装。
"""
import os
import platform
import shutil
import sys
from pathlib import Path

# 本地龍魂资源路径（相对于用户主目录）
LONGHUN_BASE = Path.home() / "longhun-system"
CNSH_RUNTIME_CANDIDATES = [
    LONGHUN_BASE / "cnsh-core",
    LONGHUN_BASE / "cnsh_terminal_v5.0",
    LONGHUN_BASE / "cnsh_editor",
]
FONT_CANDIDATES = [
    LONGHUN_BASE / "longhun-font" / "assets" / "LonghunFont-Regular-v0004.otf",
    Path.home() / "Library" / "Fonts" / "LonghunFont-Regular-v0004.otf",  # macOS 已安装
    Path.home() / "Library" / "Fonts" / "LonghunFont-Regular.otf",
    Path.home() / ".龍魂" / "万年历" / "assets" / "LonghunFont-Regular.ttf",
    Path.home() / ".龍魂" / "万年历" / "assets" / "LonghunFont-Regular.woff2",
]


def detect_os():
    p = platform.system().lower()
    if "windows" in p:
        return "windows"
    elif "darwin" in p:
        return "macos"
    return "linux"


def check_windows_prereqs():
    """检查 Windows 下 eNSP 依赖是否已安装"""
    results = {}
    results["WinPcap"] = shutil.which("wpcap.dll") is not None or \
        Path("C:/Windows/System32/wpcap.dll").exists()
    results["Wireshark"] = shutil.which("wireshark") is not None or \
        any((Path("C:/Program Files/Wireshark") / f).exists() for f in ["wireshark.exe"])
    results["VirtualBox"] = shutil.which("vboxmanage") is not None or \
        any((Path("C:/Program Files/Oracle/VirtualBox") / f).exists() for f in ["VBoxManage.exe"])
    return results


def find_cnsh_runtime():
    """查找本地 CNSH 运行时目录"""
    for candidate in CNSH_RUNTIME_CANDIDATES:
        if candidate.exists() and any(candidate.iterdir()):
            return candidate
    return None


def find_longhun_font():
    """查找本地龍魂字体文件"""
    for candidate in FONT_CANDIDATES:
        if candidate.exists():
            return candidate
    return None


def print_section(title):
    print(f"\n{'=' * 60}")
    print(title)
    print("=" * 60)


def main():
    os_name = detect_os()
    print_section("龍魂 · 华为 eNSP 安装辅助脚本 v1.1")
    print(f"检测到操作系统: {os_name}")
    print(f"龍魂系统根目录: {LONGHUN_BASE}")

    # 1. 平台说明
    print_section("一、平台支持说明")
    if os_name == "windows":
        print("✅ eNSP 官方原生支持 Windows。")
        print("⚠️  请确保使用 VirtualBox 5.2.x 版本，6.x/7.x 可能不兼容。")
    else:
        print("⚠️  eNSP 官方仅支持 Windows。")
        print("   在 macOS / Linux 上请通过虚拟机运行 Windows，")
        print("   或使用远程桌面连接已安装 eNSP 的 Windows 主机。")

    # 2. 依赖检查（仅 Windows）
    if os_name == "windows":
        print_section("二、依赖检查")
        prereqs = check_windows_prereqs()
        for name, installed in prereqs.items():
            status = "✅ 已安装" if installed else "❌ 未安装"
            print(f"  {name}: {status}")
        if not all(prereqs.values()):
            print("\n请按以下顺序安装缺失项：")
            print("  1. WinPcap 4.1.3")
            print("  2. Wireshark（任意稳定版）")
            print("  3. VirtualBox 5.2.44")
            print("  4. 华为 eNSP V100R003 安装包")

    # 3. 下载指引
    print_section("三、下载指引")
    print("eNSP 官方下载（需登录）：")
    print("  https://support.huawei.com/enterprise/zh/network-management/ensp-pid-9017384")
    print("\n社区镜像（链接可能变动，请自行搜索最新）：")
    print("  关键词：eNSP V100R003 百度网盘 / CSDN 下载")
    print("\n注意：请勿从不可信来源下载，安装前请校验文件哈希。")

    # 4. 本地龍魂资源
    print_section("四、本地龍魂资源定位")
    cnsh = find_cnsh_runtime()
    if cnsh:
        print(f"✅ CNSH 运行时目录: {cnsh}")
    else:
        print("❌ 未找到本地 CNSH 运行时")
        print("   请确认已克隆或解压 longhun-system 到 ~/longhun-system")

    font = find_longhun_font()
    if font:
        print(f"✅ 龍魂字体文件: {font}")
    else:
        print("❌ 未找到龍魂字体文件")
        print("   如需安装，请将字体文件复制到系统字体目录。")

    # 5. 龍魂生态工具链
    print_section("五、龍魂生态工具链（新增）")
    tools = [
        ("哈希校验工具", LONGHUN_BASE / "tools" / "ensp_hash_checker.py"),
        ("官方依赖下载助手", LONGHUN_BASE / "tools" / "ensp_downloader.py"),
        ("eNSP 完全指南", LONGHUN_BASE / "docs" / "华为_eNSP_安装完全指南_人民标准版_v3.0.md"),
        ("字体安装脚本（macOS）", LONGHUN_BASE / "longhun-font" / "install_macos.sh"),
        ("字体安装脚本（Windows）", LONGHUN_BASE / "longhun-font" / "install_windows.bat"),
    ]
    for name, path in tools:
        status = "✅" if path.exists() else "❌"
        print(f"  {status} {name}: {path}")
    print("\n推荐使用顺序：")
    print("  1. 运行 ensp_downloader.py 下载官方依赖")
    print("  2. 运行 ensp_hash_checker.py 校验文件哈希")
    print("  3. 按 docs/华为_eNSP_安装完全指南_人民标准版_v3.0.md 完成安装")

    # 6. 使用提示
    print_section("六、下一步操作")
    if os_name == "windows":
        print("1. 按第二节安装缺失依赖")
        print("2. 从第三节获取 eNSP 安装包并完成安装")
        print("3. 启动 eNSP，新建拓扑测试 AR2220 能否正常运行")
    else:
        print("1. 在虚拟机中安装 Windows 10/11")
        print("2. 在虚拟机内按 Windows 步骤安装 eNSP")
        print("3. 通过本地网络或远程桌面访问 eNSP")
    print("4. CNSH 脚本与龍魂字体可直接引用本地路径（见第四节）")

    print("\n✅ 环境检查完成")
    print("DNA: #龍芯⚡️2026-07-04-LONGHUN-ENSP-SETUP-v1.2")


if __name__ == "__main__":
    main()
