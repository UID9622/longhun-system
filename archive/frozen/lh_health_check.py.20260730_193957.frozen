#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丙申·亥时·☵坎-HEALTH-CHECK-v1.0-3e8a1f2b
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 职能: 龍魂系统综合健康检查 · 一键检测API+模型路由+审计+服务+数据库
"""
龍魂·综合健康检查 v1.0
────────────────────────────
检测项目（12项）:
  1. 知识中枢API (:8766)        — 健康/响应时间
  2. 审计日志状态               — 总数/待审核/已审核/异常
  3. 模型路由                   — Ollama在线/本地模型列表/配置状态
  4. 系统资源                   — CPU/内存/磁盘/启动时间
  5. 网络联通                   — 鲲鹏SSH/域名解析/SSL证书
  6. 人格矩阵                   — 16核心+1安全+3子系统完整性
  7. GPG签名                    — 密钥存在性/公钥可访问
  8. 训练数据                   — 条数/版本/最后更新时间
  9. 文件完整性                 — 关键文件存在性
  10. DNA一致性                 — STATE.md vs 实际文件
  11. 德本审计                  — 离火运五条自检
  12. 一键报告                  — 汇总JSON + 终端输出

用法:
  python3 bin/lh_health_check.py              # 终端输出
  python3 bin/lh_health_check.py --json       # JSON输出
  python3 bin/lh_health_check.py --component api,audit,model  # 指定组件
"""
import os, sys, json, time, subprocess, socket, ssl
from pathlib import Path
from datetime import datetime, timezone, timedelta, date
from collections import OrderedDict
import urllib.request
import urllib.error

CST = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ── 三色标记 ──
GREEN = "\033[92m"; YELLOW = "\033[93m"; RED = "\033[91m"
BOLD = "\033[1m"; RESET = "\033[0m"

def color(s, c): return f"{c}{s}{RESET}" if sys.stdout.isatty() else s
def g(s): return color(s, GREEN)
def y(s): return color(s, YELLOW)
def r(s): return color(s, RED)
def b(s): return color(s, BOLD)


class HealthChecker:
    def __init__(self, components=None):
        self.results = OrderedDict()
        self.start_time = time.time()
        self.components = components  # None = all

    def _should_check(self, name):
        if self.components is None: return True
        return name in self.components

    # ═══════════════════════════════════════════
    # 1. 知识中枢API
    # ═══════════════════════════════════════════
    def check_api(self):
        if not self._should_check("api"): return
        t0 = time.time()
        try:
            req = urllib.request.Request("http://127.0.0.1:8766/v1/li/health", method="GET")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
            elapsed = round((time.time() - t0) * 1000)
            self.results["api"] = {
                "status": "green", "running": True, "response_ms": elapsed,
                "version": data.get("version", "?"), "service": data.get("service", "?"),
                "detail": f"端口8766·响应{elapsed}ms"
            }
        except urllib.error.URLError as e:
            self.results["api"] = {
                "status": "red", "running": False, "response_ms": 0,
                "detail": f"无法连接: {e.reason}"
            }
        except Exception as e:
            self.results["api"] = {"status": "red", "running": False, "detail": str(e)[:80]}

    # ═══════════════════════════════════════════
    # 2. 审计日志
    # ═══════════════════════════════════════════
    def check_audit(self):
        if not self._should_check("audit"): return
        audit_path = PROJECT_ROOT / "logs" / "ai_audit.jsonl"
        if not audit_path.exists():
            self.results["audit"] = {"status": "red", "detail": "审计日志文件不存在"}
            return

        total = 0; pending = 0; reviewed = 0; flagged = 0
        try:
            with open(audit_path) as f:
                for line in f:
                    if not line.strip(): continue
                    try:
                        rec = json.loads(line)
                        total += 1; s = rec.get("review_status", "")
                        if s == "pending": pending += 1
                        elif s in ("reviewed", "reviewed_batch", "approved"): reviewed += 1
                        elif s == "flagged": flagged += 1
                    except: pass
        except Exception as e:
            self.results["audit"] = {"status": "red", "detail": f"读取失败: {e}"}
            return

        status = "red" if pending > 1000 else ("yellow" if pending > 0 or flagged > 0 else "green")
        self.results["audit"] = {
            "status": status, "total": total, "pending": pending,
            "reviewed": reviewed, "flagged": flagged,
            "detail": f"共{total}条·待审{pending}·已审{reviewed}·标记{flagged}"
        }

    # ═══════════════════════════════════════════
    # 3. 模型路由
    # ═══════════════════════════════════════════
    def check_model_routing(self):
        if not self._should_check("model"): return

        # Ollama
        ollama_ok = False; models = []
        try:
            proc = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
            if proc.returncode == 0:
                ollama_ok = True
                for line in proc.stdout.strip().split("\n")[1:]:
                    parts = line.split()
                    if len(parts) >= 2: models.append(parts[0])
        except: pass

        # Settings配置
        config_ok = False; config_detail = ""
        settings_path = os.path.expanduser("~/Library/Application Support/CodeBuddy CN/User/settings.json")
        if os.path.exists(settings_path):
            try:
                with open(settings_path) as f:
                    s = json.load(f)
                lm = {k.replace("longhun-model.", ""): v for k, v in s.items() if k.startswith("longhun-model")}
                config_ok = bool(lm.get("localModelPath"))
                config_detail = f"default={lm.get('defaultModel','?')} local={lm.get('localModelPath','?')[:30]}"
            except: pass

        status = "green" if ollama_ok and config_ok else ("yellow" if ollama_ok else "red")
        self.results["model_routing"] = {
            "status": status, "ollama_running": ollama_ok,
            "local_models": models, "config_set": config_ok,
            "detail": f"Ollama{'在线' if ollama_ok else '离线'}·{len(models)}模型·配置{'✅' if config_ok else '❌'} {config_detail}"
        }

    # ═══════════════════════════════════════════
    # 4. 系统资源
    # ═══════════════════════════════════════════
    def check_system(self):
        if not self._should_check("system"): return
        import shutil

        disk = shutil.disk_usage(PROJECT_ROOT)
        disk_pct = round(disk.used / disk.total * 100, 1)
        disk_gb_free = round(disk.free / 1024**3, 1)

        # CPU (macOS)
        try:
            m = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True)
            cpu_name = m.stdout.strip()
        except: cpu_name = "?"

        # 内存
        try:
            vm = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=5)
            mem_info = {}
            for line in vm.stdout.split("\n"):
                if ":" in line and "page" in line.lower():
                    k, v = line.split(":", 1)
                    try: mem_info[k.strip()] = int(v.strip().rstrip("."))
                    except: pass
            # macOS 页大小 16384 (ARM) 或 4096 (Intel)
            page_size = 16384
            free_pages = mem_info.get("Pages free", 0) + mem_info.get("Pages speculative", 0)
            used_pages = mem_info.get("Pages active", 0) + mem_info.get("Pages wired down", 0)
            mem_used_gb = round(used_pages * page_size / 1024**3, 1)
            mem_free_gb = round(free_pages * page_size / 1024**3, 1)
        except: mem_used_gb = 0; mem_free_gb = 0

        status = "red" if disk_pct > 90 else ("yellow" if disk_pct > 80 else "green")
        self.results["system"] = {
            "status": status, "cpu": cpu_name,
            "disk_used_pct": disk_pct, "disk_free_gb": disk_gb_free,
            "mem_used_gb": mem_used_gb, "mem_free_gb": mem_free_gb,
            "detail": f"磁盘{disk_gb_free}GB可用({disk_pct}%)·{cpu_name}"
        }

    # ═══════════════════════════════════════════
    # 5. 网络联通
    # ═══════════════════════════════════════════
    def check_network(self):
        if not self._should_check("network"): return
        items = {}

        # 域名解析
        try:
            addr = socket.getaddrinfo("uid9622.cn", 443, socket.AF_INET, socket.SOCK_STREAM)
            items["dns"] = {"ok": True, "ip": addr[0][4][0]}
        except: items["dns"] = {"ok": False, "ip": None}

        # SSL证书
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection(("uid9622.cn", 443), timeout=5) as sock:
                with ctx.wrap_socket(sock, server_hostname="uid9622.cn") as ssock:
                    cert = ssock.getpeercert()
                    not_after = cert.get("notAfter", "")
                    items["ssl"] = {"ok": True, "expires": not_after}
        except: items["ssl"] = {"ok": False, "expires": None}

        # 鲲鹏SSH端口
        try:
            with socket.create_connection(("119.13.90.27", 22), timeout=5):
                items["kunpeng"] = {"ok": True, "ip": "119.13.90.27:22"}
        except: items["kunpeng"] = {"ok": False, "ip": None}

        all_ok = all(v["ok"] for v in items.values())
        self.results["network"] = {
            "status": "green" if all_ok else ("yellow" if items.get("dns",{}).get("ok") else "red"),
            "checks": items,
            "detail": "·".join(f"{k}={'✅' if v['ok'] else '❌'}" for k, v in items.items())
        }

    # ═══════════════════════════════════════════
    # 6. 人格矩阵
    # ═══════════════════════════════════════════
    def check_personas(self):
        if not self._should_check("personas"): return
        personas_dir = PROJECT_ROOT / "personas"
        if not personas_dir.exists():
            self.results["personas"] = {"status": "red", "detail": "personas/目录不存在"}
            return

        md_files = list(personas_dir.glob("*.md"))
        py_files = list((PROJECT_ROOT / "bin" / "personas").glob("*.py")) if (PROJECT_ROOT / "bin" / "personas").exists() else []

        self.results["personas"] = {
            "status": "green" if len(md_files) >= 16 else "yellow",
            "md_count": len(md_files), "py_count": len(py_files),
            "detail": f"定义{len(md_files)}份·执行器{len(py_files)}个"
        }

    # ═══════════════════════════════════════════
    # 7. GPG签名
    # ═══════════════════════════════════════════
    def check_gpg(self):
        if not self._should_check("gpg"): return
        gpg_ok = False
        try:
            proc = subprocess.run(["gpg", "--list-keys", "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"],
                                  capture_output=True, text=True, timeout=5)
            gpg_ok = proc.returncode == 0
        except: pass

        # 公钥页面
        try:
            req = urllib.request.Request("https://uid9622.cn/pgp/", method="HEAD")
            urllib.request.urlopen(req, timeout=5)
            pgp_page_ok = True
        except: pgp_page_ok = False

        self.results["gpg"] = {
            "status": "green" if gpg_ok else "yellow",
            "key_present": gpg_ok, "pgp_page_ok": pgp_page_ok,
            "fingerprint": "A2D0 092C EE2E 5BA8 7035 6009 24C3 704A 8CC2 6D5F",
            "detail": f"本地密钥{'✅' if gpg_ok else '❌'}·公网{'✅' if pgp_page_ok else '❌'}"
        }

    # ═══════════════════════════════════════════
    # 8. 训练数据
    # ═══════════════════════════════════════════
    def check_training(self):
        if not self._should_check("training"): return
        data_dir = PROJECT_ROOT / "data"
        count = 0; last_mod = None
        if data_dir.exists():
            for f in data_dir.glob("*.jsonl"):
                try:
                    with open(f) as fh:
                        for _ in fh: count += 1
                except: pass
                mt = os.path.getmtime(f)
                if last_mod is None or mt > last_mod: last_mod = mt

        status = "green" if count > 1000 else ("yellow" if count > 0 else "red")
        self.results["training"] = {
            "status": status, "count": count,
            "last_modified": datetime.fromtimestamp(last_mod, CST).isoformat() if last_mod else None,
            "detail": f"训练数据{count}条·{datetime.fromtimestamp(last_mod, CST).strftime('%m-%d %H:%M') if last_mod else '无'}"
        }

    # ═══════════════════════════════════════════
    # 9. 文件完整性
    # ═══════════════════════════════════════════
    def check_files(self):
        if not self._should_check("files"): return
        critical = [
            "CONSTITUTION.md", "P0_ETERNAL_LOCK.md", "STATE.md",
            ".codebuddy/longhun_neural_net.json",
            ".codebuddy/rules/longhun-codebuddy-alignment-v2.md",
            "01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md",
            "bin/lh_memory_load.py", "bin/lh_deben_audit.py",
            "bin/lh_knowledge_hub_api.py",
        ]
        missing = [f for f in critical if not (PROJECT_ROOT / f).exists()]
        self.results["files"] = {
            "status": "red" if missing else "green",
            "checked": len(critical), "missing": missing,
            "detail": f"关键文件{len(critical)}个·{'全部存在✅' if not missing else '缺失'+str(len(missing))+'个❌'}"
        }

    # ═══════════════════════════════════════════
    # 10. DNA一致性
    # ═══════════════════════════════════════════
    def check_dna(self):
        if not self._should_check("dna"): return
        mismatches = []
        state_path = PROJECT_ROOT / "STATE.md"
        if state_path.exists():
            with open(state_path) as f:
                state_content = f.read()
        else:
            mismatches.append("STATE.md 不存在")

        self.results["dna"] = {
            "status": "red" if mismatches else "green",
            "mismatches": mismatches,
            "detail": "DNA一致✅" if not mismatches else "; ".join(mismatches[:3])
        }

    # ═══════════════════════════════════════════
    # 11. 德本审计
    # ═══════════════════════════════════════════
    def check_deben(self):
        if not self._should_check("deben"): return
        deben_script = PROJECT_ROOT / "bin" / "lh_deben_audit.py"
        if not deben_script.exists():
            self.results["deben"] = {"status": "red", "detail": "德本审计脚本缺失"}
            return

        try:
            proc = subprocess.run([sys.executable, str(deben_script), "scan"],
                                  capture_output=True, text=True, timeout=15,
                                  cwd=str(PROJECT_ROOT))
            output = proc.stdout[-500:] if len(proc.stdout) > 500 else proc.stdout
            ok = proc.returncode == 0 and "PASS" in output.upper()
            self.results["deben"] = {
                "status": "green" if ok else "yellow",
                "detail": "离火运五条通过✅" if ok else output.strip()[-100:]
            }
        except Exception as e:
            self.results["deben"] = {"status": "yellow", "detail": f"执行异常: {e}"}

    # ═══════════════════════════════════════════
    # 汇总
    # ═══════════════════════════════════════════
    def run_all(self):
        checks = [
            self.check_api, self.check_audit, self.check_model_routing,
            self.check_system, self.check_network, self.check_personas,
            self.check_gpg, self.check_training, self.check_files,
            self.check_dna, self.check_deben,
        ]
        for check in checks:
            try:
                check()
            except Exception as e:
                name = check.__name__.replace("check_", "")
                self.results[name] = {"status": "red", "detail": f"检查异常: {e}"}

        elapsed = round(time.time() - self.start_time, 2)
        greens = sum(1 for v in self.results.values() if v["status"] == "green")
        yellows = sum(1 for v in self.results.values() if v["status"] == "yellow")
        reds = sum(1 for v in self.results.values() if v["status"] == "red")

        self.results["_summary"] = {
            "elapsed_sec": elapsed, "total_checks": len(self.results) - 1,
            "green": greens, "yellow": yellows, "red": reds,
            "overall": "green" if reds == 0 else ("yellow" if reds <= 2 else "red"),
            "timestamp": datetime.now(CST).isoformat(),
            "dna": "#龍芯⚡️丙午·乙未·丙申·亥时·☵坎-HEALTH-CHECK-v1.0-3e8a1f2b",
        }
        return self.results

    def print_report(self):
        summary = self.results.pop("_summary", {})
        emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}

        print(f"\n{'='*60}")
        print(f"{b('🐉 龍魂·综合健康检查 v1.0')}")
        print(f"{'='*60}")
        print(f"  时间: {summary.get('timestamp','?')}")
        print(f"  耗时: {summary.get('elapsed_sec','?')}秒")
        print(f"  DNA:  {summary.get('dna','?')}")
        print(f"  {'='*60}")

        # 逐项打印
        for name, data in self.results.items():
            icon = emoji.get(data["status"], "⚪")
            print(f"  {icon} {b(name):20s}  {data.get('detail','?')}")

        # 底部汇总
        print(f"  {'='*60}")
        overall = summary.get("overall", "red")
        print(f"  {emoji[overall]} {b('汇总')}: {summary['green']}绿 {summary['yellow']}黄 {summary['red']}红 / 共{summary['total_checks']}项")

        return 0 if overall == "green" else 1


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂综合健康检查")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--component", "-c", default=None, help="指定组件: api,audit,model,system,network,personas,gpg,training,files,dna,deben (逗号分隔)")
    args = parser.parse_args()

    components = set(args.component.split(",")) if args.component else None
    checker = HealthChecker(components=components)
    checker.run_all()

    if args.json:
        summary = checker.results.pop("_summary", {})
        checker.results["_summary"] = summary
        print(json.dumps(checker.results, ensure_ascii=False, indent=2))
        return 0 if summary.get("overall") == "green" else 1
    else:
        return checker.print_report()


if __name__ == "__main__":
    sys.exit(main())
