#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️2026-08-30-ASI-DIAG-v1.0-UID9622
"""龍魂系统·本地ASI全栈诊断工具 v1.0"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
import hashlib
import json
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE = Path.home() / "longhun-system"
CNSH = Path.home() / "cnsh_model"
DIAG_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sep(title): print(f"\n{'='*60}\n【{title}】\n{'='*60}")
def ok(msg):  print(f"  🟢 {msg}")
def warn(msg):print(f"  🟡 {msg}")
def err(msg): print(f"  🔴 {msg}")
def info(msg):print(f"  ℹ️  {msg}")

def check_port(port, name):
    try:
        s = socket.create_connection(("127.0.0.1", port), timeout=1)
        s.close()
        ok(f"{name} :{port} 在线")
        return True
    except Exception:
        err(f"{name} :{port} 未启动")
        return False

def check_file(path, label):
    p = Path(path).expanduser()
    if p.exists():
        size = p.stat().st_size
        ok(f"{label} — {size:,} bytes — {p}")
        return True
    else:
        err(f"{label} 不存在 — {p}")
        return False

def check_dir(path, label):
    p = Path(path).expanduser()
    if p.exists():
        files = list(p.iterdir())
        ok(f"{label} — {len(files)} 个文件/目录")
        return True
    else:
        warn(f"{label} 目录不存在")
        return False

def run_cmd(cmd, label):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        out = (r.stdout + r.stderr).strip()[:200]
        if r.returncode == 0:
            ok(f"{label}: {out[:100]}")
        else:
            warn(f"{label} (rc={r.returncode}): {out[:100]}")
        return r.returncode == 0, out
    except Exception as e:
        warn(f"{label} 超时/错误: {e}")
        return False, str(e)

print("\n🐉 龍魂·本地ASI全栈诊断 v1.0")
print(f"⏰ 诊断时间: {DIAG_TIME}")
print(f"🖥️  主机: {socket.gethostname()} | Python {sys.version.split()[0]}")

# ══════════════════════════════════════
sep("1. 龍魂系统目录结构")
# ══════════════════════════════════════
core_dirs = [
    ("~/longhun-system",             "主目录"),
    ("~/longhun-system/bin",         "bin/ 工具目录"),
    ("~/longhun-system/08_BIN",      "08_BIN/ 引擎目录"),
    ("~/longhun-system/10_PORTAL",   "10_PORTAL/ 门户"),
    ("~/longhun-system/12_DOCS",     "12_DOCS/ 文档库"),
    ("~/longhun-system/sandbox_runtime", "插件沙箱"),
    ("~/longhun-system/lh_video_engine",  "视频引擎"),
    ("~/longhun-system/integrity",   "integrity/ harness"),
    ("~/longhun-system/skills",      "skills/ 技能目录"),
    ("~/longhun-system/weights",     "weights/ 权重目录"),
]
for path, label in core_dirs:
    check_dir(path, label)

# ══════════════════════════════════════
sep("2. 关键脚本版本检查")
# ══════════════════════════════════════
key_scripts = [
    ("~/longhun-system/bin/lh_logs_sync.py",    "lh_logs_sync.py"),
    ("~/longhun-system/bin/lh_vault.py",        "lh_vault.py"),
    ("~/longhun-system/bin/lh_gpg_sign.py",     "lh_gpg_sign.py"),
    ("~/longhun-system/08_BIN/hash_engine.py",  "hash_engine.py (M73)"),
    ("~/longhun-system/08_BIN/hash_api.py",     "hash_api.py (M73)"),
    ("~/longhun-system/bin/plugin_metadata.py", "plugin_metadata.py"),
    ("~/longhun-system/bin/plugin_compat_check.py", "plugin_compat_check.py"),
]
for path, label in key_scripts:
    p = Path(path).expanduser()
    if p.exists():
        content = p.read_text(encoding="utf-8", errors="ignore")[:500]
        # 提取DNA行
        dna = next((line.strip() for line in content.splitlines() if "龍芯⚡️" in line), "无DNA标记")
        # 提取版本
        ver = next((line.strip() for line in content.splitlines() if "v1." in line.lower() or "version" in line.lower()), "")
        ok(f"{label} ✅ | DNA: {dna[:80]}")
    else:
        err(f"{label} 不存在")

# ══════════════════════════════════════
sep("3. lh_logs_sync.py 版本详查")
# ══════════════════════════════════════
sync_path = Path("~/longhun-system/bin/lh_logs_sync.py").expanduser()
if sync_path.exists():
    content = sync_path.read_text(encoding="utf-8", errors="ignore")
    if 'idx["logs"]' in content or 'idx.get("logs")' in content:
        ok('lh_logs_sync.py = v1.1 (索引结构正确: idx["logs"])')
    elif 'idx.get(date)' in content and 'idx["logs"]' not in content:
        err('lh_logs_sync.py = v1.0 (BUG: 索引读写位置错误，需升级到v1.1)')
    else:
        warn('lh_logs_sync.py 版本未知，请检查')
    if 'dry_run' in content or 'dry-run' in content:
        ok('  ✅ dry-run 模式已实现')
    else:
        warn('  🟡 dry-run 模式未实现')
    if 'time.sleep' in content:
        ok('  ✅ rate-limit 保护已实现')
    else:
        warn('  🟡 rate-limit 保护未实现')
else:
    err('lh_logs_sync.py 不存在')

# ══════════════════════════════════════
sep("4. CNSH 模型训练结果")
# ══════════════════════════════════════
cnsh_items = [
    ("~/cnsh_model",                                     "cnsh_model 主目录"),
    ("~/cnsh_model/base/Qwen2.5-0.5B-Instruct",         "底座模型 Qwen2.5-0.5B"),
    ("~/cnsh_model/weights/sd-0-adapter",                "sd-0 adapter 目录"),
    ("~/cnsh_model/weights/sd-0-adapter/adapter_model.safetensors", "sd-0 权重文件"),
    ("~/cnsh_model/weights/sd-1-adapter",                "sd-1 adapter 目录"),
    ("~/cnsh_model/weights/sd-2-adapter",                "sd-2 adapter 目录"),
    ("~/cnsh_model/config/cnsh-full_weights_v1.json",    "CNSH 主配置"),
]
for path, label in cnsh_items:
    check_dir(path, label) if not path.endswith(('.json','.safetensors','.bin')) else check_file(path, label)

# sd-0 哈希
sd0 = Path("~/cnsh_model/weights/sd-0-adapter/adapter_model.safetensors").expanduser()
if sd0.exists():
    h = hashlib.sha256(sd0.read_bytes()).hexdigest()[:16]
    info(f"sd-0 SHA256前16位: {h} (预期: 64885844...)")
    if h.startswith("64885844"):
        ok("sd-0 哈希验证通过")
    else:
        warn(f"sd-0 哈希不匹配: {h}")

# ══════════════════════════════════════
sep("5. v4.1.9 LoRA 训练结果")
# ══════════════════════════════════════
v419_dirs = [
    "~/longhun-system/weights/v419",
    "~/longhun-system/weights/v4.1.9",
    "~/cnsh_model/weights/v419",
]
found_v419 = False
for d in v419_dirs:
    p = Path(d).expanduser()
    if p.exists():
        files = list(p.glob("**/*"))
        ok(f"v4.1.9 权重目录: {p} ({len(files)} 个文件)")
        for f in files[:5]:
            info(f"  {f.name}")
        found_v419 = True
if not found_v419:
    warn("v4.1.9 权重目录未找到（可能训练中或路径不同）")
    run_cmd("ps aux | grep train_lora | grep -v grep", "训练进程状态")
    run_cmd("ps aux | grep PID | grep 72422", "v4.1.9 PID 72422")

# ══════════════════════════════════════
sep("6. 服务端口状态")
# ══════════════════════════════════════
ports = [
    (9622,  "M73 哈希引擎"),
    (11434, "Ollama"),
    (8792,  "通心译API"),
    (9658,  "Web登录鉴权"),
    (8788,  "render服务"),
    (19862, "龍魂浏览器守护"),
    (3000,  "Langfuse本地"),
    (8899,  "数字人民币桥"),
]
for port, name in ports:
    check_port(port, name)

# ══════════════════════════════════════
sep("7. Ollama 模型列表")
# ══════════════════════════════════════
run_cmd("ollama list 2>/dev/null", "Ollama 已有模型")
run_cmd("ollama ps 2>/dev/null",   "Ollama 运行中")

# ══════════════════════════════════════
sep("8. Python 依赖检查")
# ══════════════════════════════════════
pkg_list = [
    "fastapi", "uvicorn", "pydantic", "torch",
    "transformers", "peft", "jieba",
    "qwen_agent", "chromadb", "guardrails",
    "langfuse", "mlflow", "trulens",
]
for pkg in pkg_list:
    r = subprocess.run(f"python3 -c 'import {pkg.replace('-','_')}; print({pkg.replace('-','_')}.__version__)'",
                       shell=True, capture_output=True, text=True)
    if r.returncode == 0:
        ok(f"{pkg}: {r.stdout.strip()}")
    else:
        warn(f"{pkg}: 未安装")

# ══════════════════════════════════════
sep("9. MEMORY.md 状态")
# ══════════════════════════════════════
mem = Path("~/longhun-system/MEMORY.md").expanduser()
if mem.exists():
    lines = mem.read_text(encoding="utf-8",errors="ignore").splitlines()
    ok(f"MEMORY.md 存在 ({len(lines)} 行)")
    for line in lines[:5]:
        info(f"  {line}")
else:
    warn("MEMORY.md 不存在")
run_cmd("find ~/longhun-system -name 'MEMORY.md' 2>/dev/null | head -3", "MEMORY.md 搜索")

# ══════════════════════════════════════
sep("10. 玻璃墙 & 门户")
# ══════════════════════════════════════
check_file("~/longhun-system/10_PORTAL/apps/console/glass.html", "玻璃墙 glass.html")
check_dir("~/longhun-system/10_PORTAL", "10_PORTAL 目录")

# ══════════════════════════════════════
sep("11. GPG 签名状态")
# ══════════════════════════════════════
run_cmd("gpg --list-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F 2>&1 | head -5", "GPG主密钥")
run_cmd("gpg --list-keys 2>&1 | grep -c uid", "GPG密钥数量")

# ══════════════════════════════════════
sep("12. 日志索引状态")
# ══════════════════════════════════════
idx_path = Path("~/longhun-system/12_DOCS/dragon-soul-open-hub/logs-notion-index.json").expanduser()
if idx_path.exists():
    try:
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        if "logs" in idx:
            ok(f"索引结构 v1.1 正确 | 已入库: {len(idx['logs'])} 条")
            keys = sorted(idx['logs'].keys())
            if keys:
                info(f"  最新: {keys[-1]} | 最早: {keys[0]}")
        else:
            err(f"索引结构 v1.0 (顶层日期键，需迁移) | {len(idx)} 条")
    except Exception:
        warn("索引文件解析失败")
else:
    warn("日志索引文件不存在（首次运行正常）")

# ══════════════════════════════════════
sep("13. CodeBuddy MCP 配置")
# ══════════════════════════════════════
mcp_path = Path("~/.codebuddy/mcp.json").expanduser()
if mcp_path.exists():
    try:
        mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
        servers = mcp.get("mcpServers", {})
        ok(f"mcp.json 存在 | 配置了 {len(servers)} 个 MCP 服务器")
        for name in servers:
            info(f"  - {name}")
    except Exception:
        warn("mcp.json 解析失败")
else:
    warn("~/.codebuddy/mcp.json 不存在")

# ══════════════════════════════════════
sep("14. 本地日志文件统计")
# ══════════════════════════════════════
log_dir = Path("~/longhun-system/.codebuddy/memory").expanduser()
if log_dir.exists():
    logs = sorted(log_dir.glob("*.md"))
    ok(f"操作日志: {len(logs)} 份")
    if logs:
        info(f"  最新: {logs[-1].name} | 最早: {logs[0].name}")
else:
    warn("日志目录不存在: ~/longhun-system/.codebuddy/memory/")
    run_cmd("find ~/.codebuddy/memory -name '*.md' 2>/dev/null | wc -l", "日志文件数 (备选路径)")

# ══════════════════════════════════════
sep("15. 鲲鹏服务器连通性")
# ══════════════════════════════════════
try:
    s = socket.create_connection(("119.13.90.27", 22), timeout=3)
    s.close()
    ok("鲲鹏 119.13.90.27:22 SSH 可达")
except Exception:
    warn("鲲鹏 119.13.90.27:22 不可达（可能需要VPN或网络限制）")

# ══════════════════════════════════════
sep("16. 磁盘 & 内存")
# ══════════════════════════════════════
run_cmd("df -h ~/ | tail -1", "家目录磁盘")
run_cmd("df -h ~/longhun-system 2>/dev/null | tail -1", "longhun-system磁盘")
run_cmd("free -h 2>/dev/null || vm_stat 2>/dev/null | head -5", "内存状态")
run_cmd("nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader 2>/dev/null || echo 'no GPU'" , "GPU状态")

# ══════════════════════════════════════
print(f"\n{'='*60}")
print(f"✅ 诊断完成 | {DIAG_TIME}")
print("DNA: #龍芯⚡️2026-08-30-ASI-DIAG-v1.0-UID9622")
print(f"{'='*60}\n")
