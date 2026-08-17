#!/usr/bin/env python3
# 龍魂 · launchd 服务生命周期接管工具
# DNA: #龍芯⚡️丙午·丙申·己未-服务生命周期接管-Phase2-v1.1
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
# ============================================================
"""
launchd 服务生命周期接管（Phase 2 · 服务融合执行层）

设计原则（焊死）：
  1. 不删除只冻结 —— plist 移入 _archive/launchd_frozen/，随时可回滚
  2. 每步可回滚 —— manifest.json 记录冻结前完整状态，wake 一键恢复
  3. 每步留痕 —— 所有操作 append 写 logs/lh_service_control.log

命令：
  lh-service status            列出全部 com.longhun.* 状态 + 冻结清单
  lh-service freeze <label..>  冻结（unload + plist 归档）
  lh-service wake <label..>    唤醒（从归档恢复 + load）
  lh-service merge-thresholds  21 合一：建统一 threshold-check 守护 + 冻结旧条目
  lh-service rollback <label>  回滚单个（等价 wake）
  lh-service api [--port 8971] 启动本地 API（给 10_PORTAL/service-control.html 点点点）
"""
import sys, os, json, time, shutil, subprocess, glob, plistlib, argparse, threading
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = Path.home() / "longhun-system"
LAUNCHD_DIR = Path.home() / "Library" / "LaunchAgents"
ARCHIVE_DIR = ROOT / "_archive" / "launchd_frozen"
MANIFEST = ARCHIVE_DIR / "manifest.json"
LOG = ROOT / "logs" / "lh_service_control.log"
THRESHOLD_SCRIPT = ROOT / "bin" / "lh_threshold_trigger.py"


def log(msg: str):
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    with open(LOG, "a") as f:
        f.write(line + "\n")
    print(line)


def load_manifest() -> list:
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text())
        except Exception:
            return []
    return []


def save_manifest(data: list):
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2))


def plist_of(label: str) -> Path:
    base = label if label.endswith(".plist") else f"{label}.plist"
    return LAUNCHD_DIR / base


def is_loaded(label: str) -> str:
    """返回 RUNNING / LOADED / NOT-LOADED"""
    try:
        out = subprocess.run(["launchctl", "list"], capture_output=True, text=True).stdout
        for line in out.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 3 and parts[2] == label:
                return "RUNNING" if parts[0] != "-" else "LOADED"
    except Exception:
        pass
    return "NOT-LOADED"


def freeze(label: str, silent: bool = False) -> bool:
    """冻结单个服务：unload + plist 移入归档 + manifest 记录"""
    plist = plist_of(label)
    full_label = label if label.startswith("com.longhun.") else f"com.longhun.{label}"
    if not plist.exists():
        # 可能 plist 用完整 label 命名
        alt = plist_of(full_label)
        if alt.exists():
            plist = alt
        else:
            log(f"  ⚠️ {label}: plist 不存在，跳过")
            return False
    try:
        subprocess.run(["launchctl", "unload", str(plist)], capture_output=True, timeout=15)
        # 进程可能残留，温和清理（只杀该 plist 对应程序）
        subprocess.run(["launchctl", "remove", full_label], capture_output=True, timeout=10)
    except Exception as e:
        log(f"  ⚠️ {label}: unload 异常 {e}")
    # 读程序信息（写进 manifest 便于回滚/审计）
    prog = "?"
    try:
        with open(plist, "rb") as fh:
            p = plistlib.load(fh)
        prog = " ".join(p.get("ProgramArguments", []))[:120]
    except Exception:
        pass
    # 移动归档（保留原名，manifest 记录全路径）
    dest = ARCHIVE_DIR / plist.name
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        shutil.move(str(plist), str(dest))
    except Exception as e:
        log(f"  ❌ {label}: 归档失败 {e}")
        return False
    m = load_manifest()
    m.append({
        "label": full_label, "plist": plist.name, "program": prog,
        "frozen_at": time.strftime("%Y-%m-%d %H:%M:%S"), "restored": False,
    })
    save_manifest(m)
    if not silent:
        log(f"  ✅ 已冻结: {full_label} → {dest.name}")
    return True


def freeze_many(labels: list) -> dict:
    """批量冻结，返回 {ok:[], failed:[]}（供 API 调用）"""
    ok, failed = [], []
    for l in labels:
        if freeze(l, silent=True):
            ok.append(l)
        else:
            failed.append(l)
    if ok:
        log(f"  ✅ 已冻结 {len(ok)} 个: {', '.join(ok)}")
    if failed:
        log(f"  ⚠️ 失败 {len(failed)} 个: {', '.join(failed)}")
    return {"ok": ok, "failed": failed}


def wake(label: str) -> bool:
    """唤醒单个服务：从 manifest 恢复 plist + load"""
    full_label = label if label.startswith("com.longhun.") else f"com.longhun.{label}"
    m = load_manifest()
    rec = next((x for x in m if x["label"] == full_label and not x.get("restored")), None)
    if not rec:
        log(f"  ⚠️ {label}: 不在冻结清单，跳过")
        return False
    src = ARCHIVE_DIR / rec["plist"]
    dest = plist_of(full_label)
    if not src.exists():
        log(f"  ❌ {label}: 归档文件丢失 {src}")
        return False
    shutil.move(str(src), str(dest))
    r = subprocess.run(["launchctl", "load", "-w", str(dest)], capture_output=True, timeout=15)
    if r.returncode != 0:
        log(f"  ⚠️ {label}: load 返回非零 {r.stderr.decode()[:100]}")
    rec["restored"] = True
    rec["restored_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_manifest(m)
    log(f"  ✅ 已唤醒: {full_label}")
    return True


def wake_many(labels: list) -> dict:
    """批量唤醒，返回 {ok:[], failed:[]}（供 API 调用）"""
    ok, failed = [], []
    for l in labels:
        if wake(l):
            ok.append(l)
        else:
            failed.append(l)
    return {"ok": ok, "failed": failed}


def merge_thresholds():
    """21 合一：生成统一 threshold-check 守护，冻结全部旧 threshold-*"""
    log("===== 开始 21 合一（threshold-* → threshold-check）=====")
    if not THRESHOLD_SCRIPT.exists():
        log(f"  ❌ 找不到 {THRESHOLD_SCRIPT}")
        return
    new_plist = plist_of("com.longhun.threshold-check")
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.threshold-check</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{THRESHOLD_SCRIPT}</string>
        <string>--check</string>
        <string>all</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{ROOT}</string>
    <key>StartInterval</key>
    <integer>600</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{ROOT}/logs/threshold_check.out.log</string>
    <key>StandardErrorPath</key>
    <string>{ROOT}/logs/threshold_check.err.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONUNBUFFERED</key>
        <string>1</string>
        <key>LONGHUN_ROOT</key>
        <string>{ROOT}</string>
    </dict>
</dict>
</plist>"""
    new_plist.write_text(content)
    r = subprocess.run(["launchctl", "load", "-w", str(new_plist)], capture_output=True, timeout=15)
    if r.returncode != 0:
        log(f"  ⚠️ 加载统一守护返回非零 {r.stderr.decode()[:100]}")
    log("  ✅ 统一守护 com.longhun.threshold-check 已加载（--check all · 每10分钟）")
    # 冻结全部旧 threshold-*
    old = sorted(glob.glob(str(LAUNCHD_DIR / "com.longhun.threshold-*.plist")))
    n = 0
    for f in old:
        base = Path(f).stem
        if base == "com.longhun.threshold-check":
            continue
        if freeze(base):
            n += 1
    log(f"  ✅ 已冻结旧 threshold-* 条目: {n} 个")
    log("===== 21 合一完成 =====")


def pid_of(label: str) -> str:
    """从 launchctl list 提取 PID，'-' 表示无进程但已加载"""
    try:
        out = subprocess.run(["launchctl", "list"], capture_output=True, text=True).stdout
        for line in out.splitlines()[1:]:
            parts = line.split()
            if len(parts) >= 3 and parts[2] == label:
                return parts[0]
    except Exception:
        pass
    return "-"


def status_data() -> dict:
    """返回结构化状态（供 API / CLI 共用）"""
    frozen = [x for x in load_manifest() if not x.get("restored")]
    files = sorted(glob.glob(str(LAUNCHD_DIR / "com.longhun.*.plist")))
    services = []
    for f in files:
        try:
            with open(f, "rb") as fh:
                p = plistlib.load(fh)
            label = p.get("Label", Path(f).stem)
        except Exception:
            continue
        st = is_loaded(label)
        pid = pid_of(label)
        services.append({
            "label": label,
            "short": label.replace("com.longhun.", ""),
            "status": st,
            "pid": pid,
        })
    return {"services": services, "frozen": frozen}


def status():
    """CLI：列出所有 com.longhun.* 状态 + 冻结清单"""
    data = status_data()
    services = data["services"]
    frozen = data["frozen"]
    print(f"\n🐉 launchd 服务状态 · 活跃配置 {len(services)} 个 · 已冻结 {len(frozen)} 个\n")
    print(f"{'状态':<10} {'服务名':<34} PID")
    print("-" * 60)
    for s in services:
        print(f"{s['status']:<10} {s['short']:<34} {s['pid']}")
    if frozen:
        print("\n📦 已冻结清单（可回滚）:")
        for rec in frozen:
            print(f"  {rec['label']}  (冻结于 {rec['frozen_at']})")
    print()


def read_log(n: int = 100) -> list:
    """读取最近 n 行操作日志"""
    if not LOG.exists():
        return []
    try:
        lines = LOG.read_text().splitlines()
        return lines[-n:]
    except Exception:
        return []


class _APIHandler(BaseHTTPRequestHandler):
    """服务控制 REST API（仅本地 127.0.0.1，CORS 放行本地门户）"""
    API_LOG_LOCK = threading.Lock()

    def _cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")

    def _json(self, code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length:
                return json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            pass
        return {}

    def log_message(self, fmt, *args):
        # 覆写为写审计日志，不在 stdout 刷屏
        with self.API_LOG_LOCK:
            log(f"[API] {self.client_address[0]} - {fmt % args}")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)
        if path == "/status":
            data = status_data()
            data["log_tail"] = read_log(20)
            self._json(200, {"ok": True, **data})
        elif path == "/log":
            n = int(qs.get("n", ["100"])[0])
            self._json(200, {"ok": True, "lines": read_log(n)})
        elif path == "/health":
            self._json(200, {"ok": True, "port": self.server.server_port})
        else:
            self._json(404, {"ok": False, "error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        body = self._read_body()
        labels = body.get("labels", [])
        if not isinstance(labels, list) or not labels:
            self._json(400, {"ok": False, "error": "缺少 labels 数组"})
            return
        if parsed.path == "/freeze":
            res = freeze_many(labels)
            self._json(200, {"ok": True, **res, "lines": read_log(20)})
        elif parsed.path == "/wake":
            res = wake_many(labels)
            self._json(200, {"ok": True, **res, "lines": read_log(20)})
        else:
            self._json(404, {"ok": False, "error": "not found"})


def run_api(port: int = 8971):
    """启动本地 API，仅监听 127.0.0.1"""
    server = HTTPServer(("127.0.0.1", port), _APIHandler)
    log(f"🌐 服务控制 API 已启动: http://127.0.0.1:{port}")
    log(f"   可用端点: /status /log /health /freeze /wake")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("👋 API 已停止")


def main():
    ap = argparse.ArgumentParser(prog="lh-service", description="龍魂 launchd 服务生命周期接管")
    ap.add_argument("action", choices=["status", "freeze", "wake", "merge-thresholds", "rollback", "api"])
    ap.add_argument("labels", nargs="*")
    ap.add_argument("--port", type=int, default=8971, help="API 端口（默认 8971）")
    args = ap.parse_args()

    if args.action == "status":
        status()
    elif args.action == "merge-thresholds":
        merge_thresholds()
    elif args.action == "freeze":
        for l in args.labels:
            freeze(l)
    elif args.action == "wake":
        for l in args.labels:
            wake(l)
    elif args.action == "rollback":
        for l in args.labels:
            wake(l)
    elif args.action == "api":
        run_api(args.port)


if __name__ == "__main__":
    main()
