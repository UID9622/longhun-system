# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 双节点 CLI 控制器 v1.0
DNA: #龍芯⚡️丙午·辛未·DUAL-NODE-CLI-v1.0

Mac 端日常操作入口：
  lh sync              五维全量同步
  lh sync --dry        预览同步
  lh status            双节点状态
  lh ask "问题"         推理（本地优先，离线可用）
  lh train <任务>       提交训练到鲲鹏
  lh train-status <id>  查看训练进度
  lh checkpoint         查看/拉取最新模型
  lh health             健康检查

别名配置（加入 ~/.zshrc）：
  alias lh="python3 $HOME/longhun-system/L6_同步层/dual_node_cli.py"
"""

import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DNA = "#龍芯⚡️丙午·辛未·DUAL-NODE-CLI-v2.0"
CST = timezone(timedelta(hours=8))

# 默认配置
DEFAULT_KUNPENG_IP = "119.13.90.27"
DEFAULT_KUNPENG_API_PORT = 9633
DEFAULT_LOCAL_API_PORT = 9634

# FRP 隧道后：本地 127.0.0.1:9633 = 鲲鹏 API
FRP_LOCAL_API = f"http://127.0.0.1:{DEFAULT_KUNPENG_API_PORT}"

# 颜色
GREEN = '\033[0;32m'; YELLOW = '\033[1;33m'; RED = '\033[0;31m'
CYAN = '\033[0;36m'; BOLD = '\033[1m'; NC = '\033[0m'


def load_config() -> Dict[str, Any]:
    """加载配置"""
    config_file = ROOT / "deploy" / ".kunpeng_config"
    config = {
        "kunpeng_ip": DEFAULT_KUNPENG_IP,
        "kunpeng_user": "root",
        "kunpeng_port": 22,
        "kunpeng_path": "/opt/longhun-system",
        "kunpeng_api_port": DEFAULT_KUNPENG_API_PORT,
    }
    if config_file.exists():
        with open(config_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                v = v.strip().strip('"').strip("'")
                k = k.strip()
                if k == "KUNPENG_MGMT_IP":
                    config["kunpeng_ip"] = v
                elif k == "KUNPENG_USER":
                    config["kunpeng_user"] = v
                elif k == "KUNPENG_SSH_PORT":
                    config["kunpeng_port"] = int(v)
                elif k == "KUNPENG_DEPLOY_PATH":
                    config["kunpeng_path"] = v
    return config


def load_auth() -> Optional[Dict[str, str]]:
    """加载认证信息"""
    key_file = ROOT / "L6_同步层" / ".dual_node_keys"
    if key_file.exists():
        return json.loads(key_file.read_text())
    return None


def _detect_frp() -> bool:
    """检测 frp 隧道是否可用"""
    try:
        req = Request(f"{FRP_LOCAL_API}/health", method="GET")
        resp = urlopen(req, timeout=3)
        data = json.loads(resp.read().decode())
        return data.get("node_role") == "kunpeng"
    except Exception:
        return False


def api_call(endpoint: str, method: str = "GET", data: Dict = None,
             use_auth: bool = True) -> Dict[str, Any]:
    """调用鲲鹏 API（frp隧道优先 → 直连fallback）"""
    config = load_config()

    # 优先 frp 隧道
    if _detect_frp():
        url = f"{FRP_LOCAL_API}{endpoint}"
    else:
        url = f"http://{config['kunpeng_ip']}:{config['kunpeng_api_port']}{endpoint}"

    def _call(_url):
        body = json.dumps(data).encode() if data else None
        req = Request(_url, data=body, method=method)
        req.add_header("Content-Type", "application/json")
        if use_auth:
            auth = load_auth()
            if auth:
                req.add_header("X-Longhun-API-Key", auth.get("api_key", ""))
        try:
            resp = urlopen(req, timeout=30)
            return json.loads(resp.read().decode())
        except HTTPError as e:
            return {"error": f"HTTP {e.code}: {e.reason}", "offline": True}
        except URLError:
            return {"error": "无法连接鲲鹏", "offline": True}

    result = _call(url)
    # frp 失败则尝试直连
    if "error" in result and "127.0.0.1" in url:
        direct_url = f"http://{config['kunpeng_ip']}:{config['kunpeng_api_port']}{endpoint}"
        return _call(direct_url)
    return result


def local_inference(query: str) -> Dict[str, Any]:
    """本地 Ollama 推理（离线降级）"""
    try:
        # 先检测可用模型
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=5
        )
        models = []
        for line in result.stdout.strip().split("\n")[1:]:
            if line.strip():
                models.append(line.split()[0])

        model = None
        for m in models:
            if "longhun" in m.lower():
                model = m
                break
        if not model and models:
            model = models[0]

        if not model:
            return {"error": "无本地模型", "offline": True}

        print(f"{CYAN}🧠 本地推理 ({model})...{NC}")
        result = subprocess.run(
            ["ollama", "run", model, query],
            capture_output=True, text=True, timeout=120
        )
        return {
            "response": result.stdout.strip(),
            "model": model,
            "source": "local-offline",
        }
    except FileNotFoundError:
        return {"error": "Ollama 未安装", "offline": True}
    except subprocess.TimeoutExpired:
        return {"error": "推理超时", "offline": True}


# ─── 命令处理 ───

def cmd_status():
    """双节点状态"""
    print(f"{BOLD}🐉 龍魂双节点状态{NC}\n")

    # 本地
    print(f"{CYAN}[本地 Mac]{NC}")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
        models = [l.split()[0] for l in result.stdout.strip().split("\n")[1:] if l.strip()]
        print(f"   Ollama: {GREEN}✅{NC} | 模型: {', '.join(models) if models else '无'}")
    except Exception:
        print(f"   Ollama: {YELLOW}❌{NC}")

    # FRP 隧道
    print(f"\n{CYAN}[FRP 隧道]{NC}")
    config = load_config()
    try:
        from L6_同步层.frp_manager import FrpManager
        mgr = FrpManager()
        frp_status = mgr.status()
        if frp_status["running"]:
            print(f"   状态: {GREEN}🟢 运行中{NC} (PID: {frp_status['pid']})")
            for name, ok in frp_status["channels"].items():
                print(f"   {name}: {GREEN if ok else RED}{'🟢' if ok else '🔴'}{NC}")
        else:
            print(f"   状态: {YELLOW}🔴 未运行{NC} (安装: {'✅' if frp_status['installed'] else '❌'})")
    except Exception:
        print(f"   状态: {YELLOW}❌ 未检测到 frp{NC}")

    # 鲲鹏 SSH
    print(f"\n{CYAN}[远端鲲鹏 SSH]{NC}")
    try:
        result = subprocess.run(
            ["ssh", "-p", str(config["kunpeng_port"]),
             "-i", os.path.expanduser("~/.ssh/longhun_kunpeng_ed25519"),
             "-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=10",
             f"{config['kunpeng_user']}@{config['kunpeng_ip']}",
             "echo OK && uname -m && free -h | grep Mem && df -h / | tail -1"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")
            print(f"   SSH: {GREEN}✅{NC} | 架构: {lines[1] if len(lines) > 1 else '?'}")
            if len(lines) > 2:
                print(f"   内存: {lines[2].split(':')[1].strip() if ':' in lines[2] else lines[2]}")
            if len(lines) > 3:
                parts = lines[3].split()
                if len(parts) >= 5:
                    print(f"   磁盘: {parts[2]}/{parts[1]} ({parts[4]})")
        else:
            print(f"   SSH: {RED}❌{NC}")
    except Exception as e:
        print(f"   SSH: {RED}❌{NC} ({e})")

    # API
    print(f"\n{CYAN}[双节点 API]{NC}")
    health = api_call("/health", use_auth=False)
    if "error" not in health:
        transport = "frp隧道" if _detect_frp() else "直连"
        print(f"   鲲鹏 API: {GREEN}✅{NC} ({transport}) | 离线降级: {'✅' if health.get('can_fallback') else '❌'}")
    else:
        print(f"   鲲鹏 API: {YELLOW}❌ 离线{NC}")

    print(f"\n{BOLD}DNA: {DNA}{NC}")


def cmd_sync(dry_run: bool = False):
    """五维同步"""
    mode = "预览" if dry_run else "同步"
    print(f"{BOLD}🐉 五维{mode}...{NC}\n")

    # 直接调用本地协议引擎（不用API，减少一层）
    from L6_同步层.dual_node_protocol import DualNodeProtocol, SyncDimension
    config = load_config()
    protocol = DualNodeProtocol(
        kunpeng_ip=config["kunpeng_ip"],
        kunpeng_user=config["kunpeng_user"],
        kunpeng_port=config["kunpeng_port"],
        kunpeng_path=config["kunpeng_path"],
    )

    if dry_run:
        result = protocol.sync_all(dry_run=True)
    else:
        result = protocol.sync_all()

    for dim_name, info in result["dimensions"].items():
        errors = len(info.get("errors", []))
        icon = f"{GREEN}✅{NC}" if errors == 0 else f"{YELLOW}⚠️{NC}"
        print(f"   {icon} {dim_name}: {info['direction']} ({info['path_count']}路径)")

    print(f"\n{BOLD}DNA: {DNA}{NC}")


def cmd_ask(query: str):
    """推理 — 本地优先，离线降级"""
    print(f"{BOLD}🐉 龍魂推理{NC}\n")

    # 1. 尝试本地
    local_result = local_inference(query)
    if "error" not in local_result:
        print(local_result["response"])
        print(f"\n{CYAN}── 本地推理 · {local_result['model']} · 离线可用{NC}")
        return

    # 2. 本地不可用，尝试鲲鹏
    print(f"{YELLOW}本地无模型，请求鲲鹏...{NC}")
    result = api_call("/inference", method="POST", data={"query": query})
    if "error" in result:
        print(f"{RED}❌ 鲲鹏不可达，且本地无模型{NC}")
        print(f"   建议: ollama pull longhun-v1.9:latest")
        return

    print(result.get("response", json.dumps(result, ensure_ascii=False)))
    print(f"\n{CYAN}── 鲲鹏推理 · {result.get('model', 'unknown')}{NC}")


def cmd_train(task_id: str, data_path: str, epochs: int = 1):
    """提交训练任务"""
    print(f"{BOLD}🐉 提交训练任务{NC}\n")
    result = api_call("/train", method="POST", data={
        "task_id": task_id,
        "data_path": data_path,
        "epochs": epochs,
    })
    if "error" in result:
        print(f"{RED}❌ {result['error']}{NC}")
        return
    print(f"   {GREEN}✅{NC} 任务已提交: {task_id}")
    print(f"   状态: {result.get('status', 'unknown')}")
    print(f"\n{BOLD}DNA: {DNA}{NC}")


def cmd_train_status(task_id: str):
    """查询训练进度"""
    result = api_call(f"/train/{task_id}", method="GET")
    if "error" in result:
        print(f"{RED}❌ {result['error']}{NC}")
        return
    print(f"{BOLD}🐉 训练进度: {task_id}{NC}")
    print(f"   状态: {result.get('status', 'unknown')}")
    if result.get("started_at"):
        print(f"   开始: {result['started_at']}")
    print(f"\n{BOLD}DNA: {DNA}{NC}")


def cmd_checkpoint(pull: bool = False):
    """查看/拉取最新 checkpoint"""
    result = api_call("/checkpoint/latest", method="GET")
    if "error" in result:
        print(f"{RED}❌ {result['error']}{NC}")
        return

    print(f"{BOLD}🐉 最新 Checkpoint{NC}")
    print(f"   文件: {result['filename']}")
    print(f"   大小: {result['size_mb']} MB")
    print(f"   修改: {result['modified']}")
    print(f"   哈希: {result['hash_first_mb']}")

    if pull:
        print(f"\n{YELLOW}⬇️  拉取中...{NC}")
        config = load_config()
        remote_path = f"{config['kunpeng_path']}/{result['relative_path']}"
        local_dst = ROOT / "models"
        local_dst.mkdir(parents=True, exist_ok=True)

        subprocess.run([
            "scp", "-P", str(config["kunpeng_port"]),
            "-i", os.path.expanduser("~/.ssh/longhun_kunpeng_ed25519"),
            "-o", "StrictHostKeyChecking=accept-new",
            f"{config['kunpeng_user']}@{config['kunpeng_ip']}:{remote_path}",
            str(local_dst / result["filename"]),
        ])
        print(f"{GREEN}✅ 已拉取到 models/{result['filename']}{NC}")

    print(f"\n{BOLD}DNA: {DNA}{NC}")


def cmd_health():
    """健康检查"""
    health = api_call("/health", use_auth=False)
    print(f"{BOLD}🐉 健康检查{NC}\n")
    for k, v in health.items():
        if k in ("dna", "uid", "timestamp"):
            continue
        icon = f"{GREEN}✅{NC}" if v else f"{RED}❌{NC}" if isinstance(v, bool) else ""
        print(f"   {icon} {k}: {v}")
    print(f"\n{BOLD}DNA: {health.get('dna', DNA)}{NC}")


# ─── FRP 隧道命令 ───

def cmd_tunnel(args_left: list):
    """FRP 隧道管理"""
    sub_cmd = args_left[0] if args_left else "status"

    from L6_同步层.frp_manager import FrpManager, FrpConfig, FRP_VERSION
    cfg = FrpConfig.from_env()
    mgr = FrpManager(cfg)

    if sub_cmd == "install":
        print(f"{BOLD}🐉 安装 frpc v{FRP_VERSION}{NC}")
        mgr.install()

    elif sub_cmd == "start":
        print(f"{BOLD}🐉 启动 FRP 隧道...{NC}")
        ok, msg = mgr.start()
        print(f"   {'✅' if ok else '❌'} {msg}")
        if ok and mgr.is_running():
            print(f"   {CYAN}📡 鲲鹏API: 127.0.0.1:{cfg.local_api_port} → :{cfg.remote_api_port}{NC}")
            print(f"   {CYAN}🔑 鲲鹏SSH: 127.0.0.1:9622 → :{cfg.remote_ssh_port}{NC}")

    elif sub_cmd == "stop":
        ok, msg = mgr.stop()
        print(f"   {'✅' if ok else '❌'} {msg}")

    elif sub_cmd == "restart":
        ok, msg = mgr.restart()
        print(f"   {'✅' if ok else '❌'} {msg}")

    elif sub_cmd == "status":
        st = mgr.status()
        print(f"{BOLD}🐉 FRP 隧道状态{NC}\n")
        print(f"   安装: {'✅ 已安装' if st['installed'] else '❌ 未安装'}")
        print(f"   运行: {'🟢 运行中' if st['running'] else '🔴 已停止'} {'(PID: ' + str(st['pid']) + ')' if st['pid'] else ''}")
        print(f"   服务器: {st['server_addr'] or '未配置'}")
        print(f"   通道:")
        for name, ok in st["channels"].items():
            print(f"     {name}: {'🟢 通畅' if ok else '🔴 断开'}")
        if st.get("last_logs"):
            print(f"\n   最近日志:")
            for line in st["last_logs"][-3:]:
                print(f"     {line[:120]}")
        print(f"\n{BOLD}DNA: {DNA}{NC}")

    elif sub_cmd == "health":
        h = mgr.health_check()
        print(f"{BOLD}🐉 隧道健康{NC}\n")
        color = GREEN if h["status"] == "healthy" else RED if h["status"] == "dead" else YELLOW
        print(f"   状态: {color}{h['status']}{NC}")
        print(f"   隧道: {'🟢' if h['tunnel_running'] else '🔴'}")
        print(f"   API: {'🟢' if h['api_reachable'] else '🔴'}")
        print(f"   SSH降级: {'✅' if h['fallback_available'] else '❌'}")

    elif sub_cmd == "log":
        n = 50
        if len(args_left) > 1:
            try:
                n = int(args_left[1])
            except ValueError:
                pass
        print(mgr.tail_logs(n))

    elif sub_cmd == "config":
        if len(args_left) > 1 and args_left[1] == "--set":
            if len(args_left) >= 3:
                cfg.server_addr = args_left[2]
            if len(args_left) >= 4:
                cfg.auth_token = args_left[3]
            cfg.save_to_config_file()
            print(f"✅ 配置已保存: {cfg.server_addr}")
        else:
            print(f"{BOLD}🐉 FRP 配置{NC}")
            print(f"   服务器: {cfg.server_addr or '未设置'}")
            print(f"   Token: {'***' + cfg.auth_token[-4:] if cfg.auth_token else '未设置'}")
            print(f"\n   {CYAN}配置命令: lh tunnel config --set <服务器IP> [Token]{NC}")

    elif sub_cmd == "dashboard":
        if cfg.server_addr:
            url = f"http://{cfg.server_addr}/longhun/"
            print(f"🐉 面板: {url}")
            try:
                subprocess.run(["open", url])
            except Exception:
                pass
        else:
            print("❌ 未配置服务器地址")

    elif sub_cmd == "daemon":
        interval = 30
        if len(args_left) > 1:
            try:
                interval = int(args_left[1])
            except ValueError:
                pass
        print(f"{BOLD}🐉 FRP 守护模式 (检查间隔: {interval}s){NC}")
        print("Ctrl+C 退出\n")

        fail_count = 0
        last_restart = 0
        while True:
            try:
                h = mgr.health_check()
                ts = datetime.now(CST).strftime("%H:%M:%S")
                if h["status"] != "healthy":
                    fail_count += 1
                    print(f"[{ts}] 🔴 异常 (×{fail_count})")
                    if fail_count >= 3 and time.time() - last_restart > 60:
                        print(f"[{ts}] 🔄 自动重启...")
                        mgr.restart()
                        last_restart = time.time()
                        fail_count = 0
                else:
                    if fail_count > 0:
                        print(f"[{ts}] 🟢 已恢复")
                    fail_count = 0
                time.sleep(interval)
            except KeyboardInterrupt:
                print(f"\n👋 守护退出")
                break
            except Exception as e:
                print(f"[{ts}] ⚠️ {e}")
                time.sleep(interval)

    else:
        print(f"未知子命令: {sub_cmd}")
        print("用法: lh tunnel [install|start|stop|restart|status|health|log|config|dashboard|daemon]")


# ─── 主入口 ───

def main():
    if len(sys.argv) < 2:
        print(f"""
{BOLD}🐉 龍魂双节点 CLI 控制器 v2.0{NC}

用法:
  {CYAN}lh status{NC}              双节点状态总览
  {CYAN}lh sync{NC}                五维全量同步
  {CYAN}lh sync --dry{NC}          预览同步内容
  {CYAN}lh ask "问题"{NC}           推理（本地优先→鲲鹏fallback）
  {CYAN}lh train 任务名 数据路径{NC}  提交训练到鲲鹏
  {CYAN}lh train-status 任务名{NC}   查询训练进度
  {CYAN}lh checkpoint{NC}          查看最新模型
  {CYAN}lh checkpoint --pull{NC}   拉取最新模型到本地
  {CYAN}lh health{NC}              健康检查

 {BOLD}FRP 隧道:{NC}
  {CYAN}lh tunnel install{NC}      安装 frpc
  {CYAN}lh tunnel start{NC}        启动隧道
  {CYAN}lh tunnel stop{NC}         停止隧道
  {CYAN}lh tunnel status{NC}       隧道状态
  {CYAN}lh tunnel health{NC}       隧道健康检查
  {CYAN}lh tunnel config{NC}       查看/设置配置
  {CYAN}lh tunnel dashboard{NC}    打开Web面板
  {CYAN}lh tunnel log [N]{NC}      查看日志
  {CYAN}lh tunnel daemon{NC}       守护模式（自动重连）

DNA: {DNA}
UID: UID9622
        """)
        return

    cmd = sys.argv[1]

    if cmd == "status":
        cmd_status()
    elif cmd == "sync":
        dry = "--dry" in sys.argv
        cmd_sync(dry_run=dry)
    elif cmd == "ask":
        if len(sys.argv) < 3:
            print("用法: lh ask \"你的问题\"")
            return
        cmd_ask(sys.argv[2])
    elif cmd == "train":
        if len(sys.argv) < 4:
            print("用法: lh train 任务名 数据路径 [轮数]")
            return
        epochs = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        cmd_train(sys.argv[2], sys.argv[3], epochs)
    elif cmd == "train-status":
        if len(sys.argv) < 3:
            print("用法: lh train-status 任务名")
            return
        cmd_train_status(sys.argv[2])
    elif cmd == "checkpoint":
        pull = "--pull" in sys.argv
        cmd_checkpoint(pull=pull)
    elif cmd == "health":
        cmd_health()
    elif cmd == "tunnel":
        cmd_tunnel(sys.argv[2:])
    else:
        print(f"未知命令: {cmd}\n试试 lh (无参数) 查看帮助")


if __name__ == "__main__":
    main()
