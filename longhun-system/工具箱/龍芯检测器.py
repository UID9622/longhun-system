#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
# 🛡️ 龍芯·本地异常检测器 v1.0
# DNA: #龍芯⚡️2026-03-31-本地异常检测器-v1.0
# 创建者: 💎 龍芯北辰｜UID9622
# 使用: python3 龍芯检测器.py
# 向善四律: L3_不替代人 — 检测只报告，老大决定删不删
# ═══════════════════════════════════════════════════════════════

import subprocess
import os
import sys
import datetime
import json
from pathlib import Path

# ── 颜色定义（终端彩色输出）──────────────────────────────────
class C:
    RED    = "\033[91m"
    ORANGE = "\033[93m"
    GREEN  = "\033[92m"
    BLUE   = "\033[94m"
    PURPLE = "\033[95m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"

# ── 可疑关键词黑名单 ──────────────────────────────────────────
SUSPICIOUS_KEYWORDS = [
    "huawei", "hicloud", "xiayi", "小艺",
    "mediarouter", "root.home", "router.home",
    "hilink", "hisuite",
    "anyconnect", "checkpoint", "zscaler",
    "charles", "mitmproxy", "fiddler",
    "surveillance", "monitor", "spy",
    "remote", "mdm", "jamf", "kandji",
]

SAFE_KEYWORDS = [
    "apple", "digicert", "comodo", "entrust",
    "globalsign", "letsencrypt", "sectigo",
    "amazon", "google", "microsoft",
    "verisign", "symantec", "thawte",
]

results = {"p0": [], "p1": [], "p2": [], "info": []}
report_lines = []

def log(msg, level="info", color=C.RESET):
    print(f"{color}{msg}{C.RESET}")
    report_lines.append(msg)

def header(title):
    line = "═" * 60
    log(f"\n{C.BOLD}{C.BLUE}{line}{C.RESET}")
    log(f"{C.BOLD}{C.BLUE}  {title}{C.RESET}")
    log(f"{C.BOLD}{C.BLUE}{line}{C.RESET}")

def run_cmd(cmd, timeout=15):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=timeout
        )
        return result.stdout + result.stderr
    except Exception:
        return ""

def is_suspicious(text):
    text_lower = text.lower()
    for safe in SAFE_KEYWORDS:
        if safe in text_lower:
            return False, None
    for kw in SUSPICIOUS_KEYWORDS:
        if kw in text_lower:
            return True, kw
    return False, None

# ════════════════════════════════════════════════════════════════
# M1: 描述文件（Profiles）扫描
# ════════════════════════════════════════════════════════════════
def scan_profiles():
    header("🔍 M1·描述文件（Profiles）扫描")
    log("正在扫描系统描述文件...", color=C.BLUE)

    output = run_cmd("profiles list -all 2>/dev/null")
    if "There are no configuration profiles" in output or output.strip() == "":
        output2 = run_cmd("sudo profiles list -all 2>/dev/null")
        if "There are no" in output2 or output2.strip() == "":
            log("  ✅ 未发现任何描述文件（Profiles）", color=C.GREEN)
            results["info"].append("M1: 无描述文件")
            return
        output = output2

    lines = output.split("\n")
    found_profiles = []
    for line in lines:
        if line.strip() and ("profileIdentifier" in line or "name:" in line.lower() or "attribute" in line.lower()):
            found_profiles.append(line.strip())

    if found_profiles:
        log(f"  🔴 发现 {len(found_profiles)} 条描述文件记录！", color=C.RED)
        for p in found_profiles:
            suspicious, kw = is_suspicious(p)
            if suspicious:
                log(f"  🚨 [可疑·含'{kw}'] {p}", color=C.RED)
                results["p0"].append(f"可疑描述文件: {p}")
            else:
                log(f"  ⚠️  [存在] {p}", color=C.ORANGE)
                results["p1"].append(f"描述文件: {p}")
    else:
        log(f"  ⚠️  发现描述文件，原始内容：", color=C.ORANGE)
        for line in lines[:20]:
            if line.strip():
                log(f"  {line}", color=C.ORANGE)
                results["p1"].append(f"描述文件原始: {line}")

# ════════════════════════════════════════════════════════════════
# M2: 证书扫描
# ════════════════════════════════════════════════════════════════
def scan_certificates():
    header("🔐 M2·系统证书扫描")
    log("正在扫描可疑根证书...", color=C.BLUE)

    keychains = [
        "/System/Library/Keychains/SystemRootCertificates.keychain",
        "/Library/Keychains/System.keychain",
        f"{Path.home()}/Library/Keychains/login.keychain-db",
    ]

    suspicious_certs = []

    for kc in keychains:
        if not os.path.exists(kc) and "login" not in kc:
            continue
        kc_name = os.path.basename(kc)
        output = run_cmd(f'security find-certificate -a "{kc}" 2>/dev/null | grep -E "labl|subj|issu" | head -200')
        lines = output.split("\n")
        for line in lines:
            suspicious, kw = is_suspicious(line)
            if suspicious:
                suspicious_certs.append((kc_name, line.strip(), kw))

    danger_keywords = ["huawei", "mediarouter", "root.home", "hicloud"]
    for kw in danger_keywords:
        output = run_cmd(f'security find-certificate -a -c "{kw}" 2>/dev/null')
        if output.strip() and "No matching" not in output:
            log(f"  🚨 发现含'{kw}'的证书！", color=C.RED)
            log(f"  {output[:300]}", color=C.RED)
            results["p0"].append(f"危险证书·含'{kw}': {output[:200]}")

    if suspicious_certs:
        log(f"  🔴 发现 {len(suspicious_certs)} 个可疑证书！", color=C.RED)
        for kc_name, cert, kw in suspicious_certs:
            log(f"  🚨 [{kc_name}] 含'{kw}': {cert}", color=C.RED)
            results["p0"].append(f"可疑证书[{kc_name}]: {cert}")
    else:
        log("  ✅ 未发现明显可疑证书", color=C.GREEN)
        results["info"].append("M2: 未发现可疑证书")

# ════════════════════════════════════════════════════════════════
# M3: 网络异常扫描
# ════════════════════════════════════════════════════════════════
def scan_network():
    header("🌐 M3·网络异常扫描")

    log("[3.1] 检查 DNS 服务器...", color=C.BLUE)
    dns_output = run_cmd("scutil --dns | grep 'nameserver' | sort -u")
    if dns_output.strip():
        dns_servers = [line.strip() for line in dns_output.split("\n") if line.strip()]
        safe_dns = ["8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1", "114.114.114.114",
                    "223.5.5.5", "119.29.29.29", "180.76.76.76"]
        for dns in dns_servers:
            ip = dns.split(":")[-1].strip() if ":" in dns else dns
            if any(s in ip for s in safe_dns) or ip.startswith("192.168") or ip.startswith("10."):
                log(f"  ✅ DNS: {ip} (正常)", color=C.GREEN)
            else:
                log(f"  ⚠️  DNS: {ip} (未知DNS服务器，需关注)", color=C.ORANGE)
                results["p1"].append(f"未知DNS服务器: {ip}")
    else:
        log("  ✅ DNS配置正常（使用系统默认）", color=C.GREEN)

    log("[3.2] 检查系统代理设置...", color=C.BLUE)
    proxy_output = run_cmd("scutil --proxy")
    proxy_issues = []
    for line in proxy_output.split("\n"):
        if "Enable : 1" in line:
            proxy_issues.append(line.strip())
    if proxy_issues:
        log(f"  ⚠️  发现已启用的代理！", color=C.ORANGE)
        for p in proxy_issues:
            log(f"  ⚠️  {p}", color=C.ORANGE)
            results["p1"].append(f"代理已启用: {p}")
    else:
        log("  ✅ 未发现异常代理设置", color=C.GREEN)

    log("[3.3] 检查 /etc/hosts 文件...", color=C.BLUE)
    hosts_output = run_cmd("cat /etc/hosts")
    suspicious_hosts = []
    for line in hosts_output.split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            suspicious, kw = is_suspicious(line)
            if suspicious:
                suspicious_hosts.append((line, kw))
            elif not any(x in line for x in ["127.0.0.1", "::1", "255.255.255", "broadcast",
                                               "localhost", "0.0.0.0", "fe80", "ff00", "ff02"]):
                log(f"  ⚠️  非标准hosts条目: {line}", color=C.ORANGE)
                results["p1"].append(f"非标准hosts: {line}")

    if suspicious_hosts:
        for h, kw in suspicious_hosts:
            log(f"  🚨 可疑hosts条目·含'{kw}': {h}", color=C.RED)
            results["p0"].append(f"可疑hosts: {h}")
    else:
        log("  ✅ /etc/hosts 未发现明显异常", color=C.GREEN)

    log("[3.4] 检查活跃网络连接...", color=C.BLUE)
    conn_output = run_cmd("netstat -an | grep ESTABLISHED | head -40")
    suspicious_conns = []
    for line in conn_output.split("\n"):
        suspicious, kw = is_suspicious(line)
        if suspicious:
            suspicious_conns.append((line.strip(), kw))

    if suspicious_conns:
        for conn, kw in suspicious_conns:
            log(f"  🚨 可疑连接·含'{kw}': {conn}", color=C.RED)
            results["p1"].append(f"可疑连接: {conn}")
    else:
        log("  ✅ 未发现明显可疑网络连接", color=C.GREEN)

# ════════════════════════════════════════════════════════════════
# M4: 启动项扫描
# ════════════════════════════════════════════════════════════════
def scan_launch_items():
    header("⚙️  M4·启动项扫描（LaunchAgents/Daemons）")

    scan_dirs = [
        "/Library/LaunchAgents",
        "/Library/LaunchDaemons",
        "/System/Library/LaunchAgents",
        "/System/Library/LaunchDaemons",
        f"{Path.home()}/Library/LaunchAgents",
    ]

    all_plist_files = []
    suspicious_items = []

    for d in scan_dirs:
        if not os.path.exists(d):
            continue
        try:
            files = os.listdir(d)
            for f in files:
                if f.endswith(".plist"):
                    full_path = os.path.join(d, f)
                    all_plist_files.append(full_path)
                    suspicious, kw = is_suspicious(f)
                    if suspicious:
                        suspicious_items.append((full_path, kw))
        except PermissionError:
            pass

    log(f"  扫描到 {len(all_plist_files)} 个启动项 plist 文件", color=C.BLUE)

    for plist_path in all_plist_files:
        try:
            content = open(plist_path, "r", errors="ignore").read()
            suspicious, kw = is_suspicious(content)
            if suspicious:
                suspicious_items.append((plist_path, kw))
        except Exception:
            pass

    seen = set()
    unique_suspicious = []
    for item in suspicious_items:
        if item[0] not in seen:
            seen.add(item[0])
            unique_suspicious.append(item)

    if unique_suspicious:
        log(f"  🔴 发现 {len(unique_suspicious)} 个可疑启动项！", color=C.RED)
        for path, kw in unique_suspicious:
            log(f"  🚨 含'{kw}': {path}", color=C.RED)
            results["p1"].append(f"可疑启动项: {path}")
    else:
        log("  ✅ 未发现可疑启动项", color=C.GREEN)
        results["info"].append("M4: 启动项正常")

# ════════════════════════════════════════════════════════════════
# M5: 进程监控
# ════════════════════════════════════════════════════════════════
def scan_processes():
    header("📡 M5·可疑进程扫描")

    process_output = run_cmd("ps aux")
    suspicious_procs = []

    for line in process_output.split("\n"):
        if any(x in line for x in ["grep", "python3", "bash", "sh ", "/usr/sbin",
                                    "kernel", "launchd", "Finder", "Dock",
                                    "WindowServer", "loginwindow"]):
            continue
        suspicious, kw = is_suspicious(line)
        if suspicious:
            suspicious_procs.append((line.strip()[:120], kw))

    if suspicious_procs:
        log(f"  🔴 发现 {len(suspicious_procs)} 个可疑进程！", color=C.RED)
        for proc, kw in suspicious_procs:
            log(f"  🚨 含'{kw}': {proc}", color=C.RED)
            results["p1"].append(f"可疑进程: {proc[:100]}")
    else:
        log("  ✅ 未发现明显可疑进程", color=C.GREEN)
        results["info"].append("M5: 进程正常")

    log("[5.2] 检查监听端口...", color=C.BLUE)
    listen_output = run_cmd("lsof -i -n -P | grep LISTEN | head -30")
    if listen_output.strip():
        for line in listen_output.split("\n"):
            if line.strip():
                suspicious, kw = is_suspicious(line)
                if suspicious:
                    log(f"  🚨 可疑监听端口·含'{kw}': {line.strip()[:100]}", color=C.RED)
                    results["p1"].append(f"可疑监听: {line.strip()[:100]}")

# ════════════════════════════════════════════════════════════════
# M6: 生成清理命令
# ════════════════════════════════════════════════════════════════
def generate_cleanup():
    header("🧹 M6·自动生成清理建议")

    cleanup_cmds = []

    if results["p0"] or results["p1"]:
        has_profile = any("描述文件" in r or "Profile" in r for r in results["p0"] + results["p1"])
        if has_profile:
            cleanup_cmds.append("# 清理描述文件（需要密码）")
            cleanup_cmds.append("sudo profiles remove -all")
            cleanup_cmds.append("")

        has_cert = any("证书" in r for r in results["p0"])
        if has_cert:
            cleanup_cmds.append("# 查找并删除可疑证书（以 huawei 为例）")
            cleanup_cmds.append('security find-certificate -a -c "huawei" -Z | grep SHA-1')
            cleanup_cmds.append('# 拿到 hash 后执行:  security delete-certificate -Z <SHA1_HASH>')
            cleanup_cmds.append("")

        suspicious_launch = [r for r in results["p1"] if "启动项" in r]
        if suspicious_launch:
            cleanup_cmds.append("# 禁用可疑启动项")
            for item in suspicious_launch:
                path = item.replace("可疑启动项: ", "")
                cleanup_cmds.append(f'sudo launchctl unload "{path}" 2>/dev/null')
                cleanup_cmds.append(f'sudo mv "{path}" "{path}.disabled"')
            cleanup_cmds.append("")

        if cleanup_cmds:
            log("  以下清理命令已生成，请确认后在终端逐条执行：", color=C.ORANGE)
            log("  （⚠️ 向善四律L3：老大确认后再执行，不自动运行）", color=C.ORANGE)
            for cmd in cleanup_cmds:
                log(f"  {cmd}", color=C.PURPLE)
    else:
        log("  ✅ 未发现需要清理的项目！你的 Mac 当前状态良好。", color=C.GREEN)

# ════════════════════════════════════════════════════════════════
# 主函数：汇总报告
# ════════════════════════════════════════════════════════════════
def main():
    start_time = datetime.datetime.now()

    print(f"{C.BOLD}{C.PURPLE}")
    print("╔═══════════════════════════════════════════════════════╗")
    print("║  🛡️  龍芯·本地异常检测器 v1.0                         ║")
    print("║  DNA: #龍芯⚡️2026-03-31-本地异常检测器-v1.0          ║")
    print("║  创建者: 💎 龍芯北辰｜UID9622                         ║")
    print("║  向善四律: L3_不替代人·检测只报告·老大拍板            ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print(f"{C.RESET}")
    print(f"  扫描开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  扫描范围: 描述文件 / 证书 / 网络 / 启动项 / 进程")
    print()

    scan_profiles()
    scan_certificates()
    scan_network()
    scan_launch_items()
    scan_processes()
    generate_cleanup()

    header("📊 扫描结果汇总")

    total_issues = len(results["p0"]) + len(results["p1"]) + len(results["p2"])

    if results["p0"]:
        log(f"\n  🔴 P0 级问题（立即处理）：{len(results['p0'])} 项", color=C.RED)
        for i, item in enumerate(results["p0"], 1):
            log(f"    {i}. {item}", color=C.RED)

    if results["p1"]:
        log(f"\n  🟠 P1 级问题（建议处理）：{len(results['p1'])} 项", color=C.ORANGE)
        for i, item in enumerate(results["p1"], 1):
            log(f"    {i}. {item}", color=C.ORANGE)

    if results["p2"]:
        log(f"\n  🟡 P2 级问题（关注）：{len(results['p2'])} 项", color="\033[93m")
        for i, item in enumerate(results["p2"], 1):
            log(f"    {i}. {item}")

    if total_issues == 0:
        log("\n  ✅ 全部通过！未发现异常。Mac 当前状态：干净。", color=C.GREEN)
    else:
        log(f"\n  共发现 {total_issues} 个需关注的问题。", color=C.ORANGE)

    end_time = datetime.datetime.now()
    elapsed = (end_time - start_time).seconds

    log(f"\n  扫描耗时: {elapsed} 秒", color=C.BLUE)
    log(f"  完成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}", color=C.BLUE)

    timestamp = start_time.strftime("%Y%m%d_%H%M%S")
    report_path = Path.home() / f"龍芯_异常报告_{timestamp}.txt"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("龍芯·本地异常检测报告\n")
        f.write(f"DNA: #龍芯⚡️2026-03-31-本地异常检测器-v1.0\n")
        f.write(f"扫描时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n")
        f.write("\n".join(report_lines))
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"P0问题: {len(results['p0'])} 项\n")
        f.write(f"P1问题: {len(results['p1'])} 项\n")
        f.write("P0详情:\n")
        for item in results["p0"]:
            f.write(f"  - {item}\n")
        f.write("P1详情:\n")
        for item in results["p1"]:
            f.write(f"  - {item}\n")

    print(f"\n{C.GREEN}  📄 报告已保存到: {report_path}{C.RESET}")
    print(f"{C.PURPLE}  DNA: #龍芯⚡️2026-03-31-本地异常检测器-v1.0{C.RESET}")
    print(f"{C.PURPLE}  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅{C.RESET}")
    print()

if __name__ == "__main__":
    main()
