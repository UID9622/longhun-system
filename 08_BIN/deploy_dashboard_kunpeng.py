# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂仪表盘 · 鲲鹏服务器部署脚本 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
P5 · 外网仪表盘 · 多节点数据同步
DNA: #龍芯⚡️丙午·甲申·辛丑·甲午·䷁坤-DASHBOARD-DEPLOY-KUNPENG-v1.0-UID9622
"""

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

HOME = Path.home()
PROJECT_DIR = Path(__file__).resolve().parent.parent
WEB_STATIC = PROJECT_DIR / "web" / "static"

DEFAULT_REMOTE = "root@119.13.90.27"
DEFAULT_REMOTE_DIR = "/opt/longhun-dashboard"
DEFAULT_PORT = 9600
SSH_KEY = os.environ.get("SSH_KEY", str(HOME / ".ssh" / "longhun_kunpeng_ed25519"))


def ssh_cmd(remote: str, cmd: str, capture: bool = False) -> subprocess.CompletedProcess:
    base = ["ssh", "-i", SSH_KEY, "-o", "ConnectTimeout=10", "-o", "StrictHostKeyChecking=no", remote]
    full = base + [cmd]
    if capture:
        return subprocess.run(full, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return subprocess.run(full)


def scp_cmd(local: str, remote_spec: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["scp", "-i", SSH_KEY, "-o", "ConnectTimeout=10", "-o", "StrictHostKeyChecking=no",
         "-r", local, remote_spec],
        capture_output=True, text=True, encoding="utf-8", errors="ignore",
    )


def rsync_cmd(local: str, remote_spec: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["rsync", "-avz", "-e", f"ssh -i {SSH_KEY} -o ConnectTimeout=10 -o StrictHostKeyChecking=no",
         local, remote_spec],
        capture_output=True, text=True, encoding="utf-8", errors="ignore",
    )


def ensure_remote_dir(remote: str, rdir: str):
    ssh_cmd(remote, f"mkdir -p {rdir}/08_BIN {rdir}/web/static/fonts {rdir}/data/agent_orchestrator {rdir}/data/workflow_runs {rdir}/data/triggers {rdir}/data/event_bus")


def deploy_code(remote: str, rdir: str) -> bool:
    print("📦 1/5 上传仪表盘代码...")
    files = [
        (PROJECT_DIR / "08_BIN" / "lh_dashboard_web.py", f"{rdir}/08_BIN/lh_dashboard_web.py"),
    ]
    for local, remote_path in files:
        if not local.exists():
            print(f"   ⚠️ 缺失: {local}")
            continue
        r = scp_cmd(str(local), f"{remote}:{remote_path}")
        if r.returncode != 0:
            print(f"   🔴 上传失败 {local}: {r.stderr}")
            return False
        print(f"   ✅ {local.name}")

    # 静态资源：只传必要文件（css + 字体），避免大 icons/layui 拖慢
    print("   📦 上传静态资源...")
    static_items = ["css"]
    font_file = WEB_STATIC / "fonts" / "MiSans-Regular.woff2"
    if font_file.exists():
        r = scp_cmd(str(font_file), f"{remote}:{rdir}/web/static/fonts/MiSans-Regular.woff2")
        if r.returncode != 0:
            print(f"   ⚠️ 字体上传失败（非关键）: {r.stderr}")
        else:
            print(f"   ✅ fonts/MiSans-Regular.woff2")
    for d in static_items:
        src = WEB_STATIC / d
        if src.exists():
            r = scp_cmd(str(src), f"{remote}:{rdir}/web/static/")
            if r.returncode != 0:
                print(f"   🔴 上传 {d} 失败: {r.stderr}")
                return False
            print(f"   ✅ web/static/{d}")
    return True


def sync_data(remote: str, rdir: str) -> bool:
    print("🔄 2/5 同步本地运行数据到鲲鹏...")
    mappings = [
        (HOME / ".longhun" / "agent_orchestrator", f"{rdir}/data/agent_orchestrator"),
        (HOME / ".longhun" / "workflow_runs", f"{rdir}/data/workflow_runs"),
        (HOME / ".longhun" / "triggers", f"{rdir}/data/triggers"),
        (HOME / ".longhun" / "event_bus", f"{rdir}/data/event_bus"),
    ]
    for local, remote_path in mappings:
        if not local.exists():
            print(f"   ⚠️ 本地目录不存在: {local}")
            continue
        # rsync 带尾斜杠同步目录内容，避免嵌套
        r = rsync_cmd(str(local) + "/", f"{remote}:{remote_path}/")
        if r.returncode != 0:
            print(f"   🔴 同步 {local.name} 失败: {r.stderr}")
            return False
        print(f"   ✅ {local.name}")
    return True


def install_service(remote: str, rdir: str, port: int) -> bool:
    print("🔧 3/5 安装 systemd 服务...")
    service_name = "longhun-dashboard"
    service = f"""[Unit]
Description=龍魂系统可视化仪表盘
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {rdir}/08_BIN/lh_dashboard_web.py --host 127.0.0.1 --port {port}
Restart=always
RestartSec=5
WorkingDirectory={rdir}
Environment=LONGHUN_DATA_DIR={rdir}/data

[Install]
WantedBy=multi-user.target
"""
    # 写服务文件到 /tmp 再上传
    local_service = Path("/tmp") / f"{service_name}.service"
    local_service.write_text(service, encoding="utf-8")
    r = scp_cmd(str(local_service), f"{remote}:/etc/systemd/system/{service_name}.service")
    if r.returncode != 0:
        print(f"   🔴 服务文件上传失败: {r.stderr}")
        return False

    setup = f"""set -e
systemctl daemon-reload
systemctl enable {service_name}
(systemctl stop {service_name} || true)
systemctl start {service_name}
sleep 1
systemctl status {service_name} --no-pager | head -5
"""
    r = ssh_cmd(remote, setup, capture=True)
    print(r.stdout)
    if r.returncode != 0:
        print(f"   🔴 服务启动失败: {r.stderr}")
        return False
    print(f"   ✅ {service_name} 已启动")
    return True


def install_nginx(remote: str, port: int) -> bool:
    print("🌐 4/5 配置 nginx /dashboard/ 反代...")
    # 定位 8080 入口配置文件（公网访问实际落在此文件）
    target_conf = "/etc/nginx/conf.d/longhun-8080.conf"
    check = ssh_cmd(remote, f"test -f {target_conf} && echo yes || echo no", capture=True)
    if check.stdout.strip() != "yes":
        print(f"   🔴 未找到 8080 入口配置: {target_conf}")
        return False

    location_path = "/system-dashboard/"
    include_file = "/etc/nginx/conf.d/longhun-dashboard-locations.inc"
    include_directive = f"include {include_file};"
    old_include_directive = "include /etc/nginx/conf.d/longhun-dashboard-locations.conf;"

    # 清理旧 .conf include 并去重
    cleanup = f"""python3 << 'PYEOF'
path = "{target_conf}"
with open(path, "r") as f:
    lines = f.readlines()
seen = set()
result = []
for line in lines:
    stripped = line.strip()
    if stripped == "{old_include_directive}" or stripped == "{include_directive}":
        if stripped not in seen:
            result.append(line)
            seen.add(stripped)
        continue
    result.append(line)
with open(path, "w") as f:
    f.writelines(result)
print("cleanup-ok")
PYEOF
"""
    ssh_cmd(remote, cleanup, capture=True)

    block = f"""    # ─── 龍魂系统仪表盘 {location_path} ───
    location {location_path} {{
        proxy_pass http://127.0.0.1:{port}/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
"""
    # 写 location 块到独立文件
    r = ssh_cmd(remote, f"cat > {include_file} <<'EOF'\n{block}\nEOF\necho 'location-file-ok'", capture=True)
    if r.returncode != 0:
        print(f"   🔴 location 文件写入失败: {r.stderr}")
        return False

    # 检查是否已 include
    check = ssh_cmd(remote, f"grep -q '{include_directive}' {target_conf} && echo yes || echo no", capture=True)
    if check.stdout.strip() != "yes":
        # 在 target_conf 的每个 server 块结束 }} 前插入 include
        insert = f"""python3 << 'PYEOF'
path = "{target_conf}"
include_line = "    {include_directive}\\n"
with open(path, "r") as f:
    lines = f.readlines()
result = []
brace_depth = 0
for line in lines:
    stripped = line.strip()
    if stripped.startswith("server") and "{{" in stripped:
        brace_depth = stripped.count("{{") - stripped.count("}}")
        result.append(line)
        continue
    if brace_depth > 0:
        brace_depth += stripped.count("{{")
        brace_depth -= stripped.count("}}")
        if brace_depth == 0 and "}}" in stripped:
            # 检查这行之前是否已有 include
            if not (result and result[-1].strip() == "{include_directive}"):
                result.append(include_line)
    result.append(line)
with open(path, "w") as f:
    f.writelines(result)
print("include-inserted")
PYEOF
"""
        r = ssh_cmd(remote, insert, capture=True)
        print(r.stdout.strip())
        if r.returncode != 0:
            print(f"   🔴 nginx include 插入失败: {r.stderr}")
            return False
    else:
        print("   🟡 dashboard include 已存在，仅更新 location 文件")

    # 测试并重载
    r = ssh_cmd(remote, "nginx -t && systemctl reload nginx", capture=True)
    print(r.stdout)
    if r.returncode != 0:
        print(f"   🔴 nginx 测试/重载失败: {r.stderr}")
        return False
    print(f"   ✅ nginx {location_path} 反代已配置")
    return True


def verify_dashboard(remote_host: str) -> bool:
    print("🧪 5/5 验证外网仪表盘...")
    url = f"http://{remote_host}:8080/system-dashboard/api/health"
    for i in range(10):
        r = subprocess.run(["curl", "-s", "--max-time", "5", url], capture_output=True, text=True, encoding="utf-8", errors="ignore")
        if r.returncode == 0 and '"status":"ok"' in r.stdout:
            print(f"   ✅ 外网仪表盘可访问: {url}")
            return True
        time.sleep(1)
    print(f"   🔴 外网仪表盘不可达: {url}")
    return False


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂仪表盘 · 鲲鹏部署脚本 v1.0")
    parser.add_argument("--remote", default=DEFAULT_REMOTE, help="远程服务器 user@ip")
    parser.add_argument("--remote-dir", default=DEFAULT_REMOTE_DIR, help="远程部署目录")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="仪表盘本地端口")
    parser.add_argument("--no-sync", action="store_true", help="不同步本地数据")
    parser.add_argument("--sync-only", action="store_true", help="仅同步数据并重启服务（不重新部署代码/nginx）")
    parser.add_argument("--dry-run", action="store_true", help="只打印步骤不执行")
    args = parser.parse_args()

    remote_host = args.remote.split("@")[-1]

    if args.dry_run:
        mode = "sync-only" if args.sync_only else "deploy"
        print(f"🐉 [dry-run] 龍魂仪表盘鲲鹏部署（模式: {mode}）")
        print(f"   remote: {args.remote}")
        print(f"   dir: {args.remote_dir}")
        print(f"   port: {args.port}")
        print(f"   sync: {not args.no_sync}")
        return 0

    if not Path(SSH_KEY).exists():
        print(f"🔴 SSH 密钥不存在: {SSH_KEY}")
        return 1

    if args.sync_only:
        print(f"🐉 仅同步数据到鲲鹏仪表盘: {args.remote}")
        print(f"   远程目录: {args.remote_dir}")
        if not sync_data(args.remote, args.remote_dir):
            return 1
        print("🔄 重启服务以加载新数据...")
        r = ssh_cmd(args.remote, f"systemctl restart longhun-dashboard && systemctl is-active longhun-dashboard")
        if r.returncode != 0:
            print(f"   🔴 服务重启失败: {r.stderr}")
            return 1
        print("   ✅ 服务已重启")
        if not verify_dashboard(remote_host):
            return 1
        print("\n✅ 数据同步完成")
        print(f"   外网访问: http://{remote_host}:8080/system-dashboard/")
        return 0

    print(f"🐉 开始部署龍魂仪表盘到鲲鹏: {args.remote}")
    print(f"   远程目录: {args.remote_dir}")
    print(f"   本地端口: {args.port}")

    ensure_remote_dir(args.remote, args.remote_dir)

    if not deploy_code(args.remote, args.remote_dir):
        return 1

    if not args.no_sync:
        if not sync_data(args.remote, args.remote_dir):
            return 1

    if not install_service(args.remote, args.remote_dir, args.port):
        return 1

    if not install_nginx(args.remote, args.port):
        return 1

    if not verify_dashboard(remote_host):
        return 1

    print("\n✅ 龍魂仪表盘鲲鹏部署完成")
    print(f"   外网访问: http://{remote_host}:8080/system-dashboard/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
