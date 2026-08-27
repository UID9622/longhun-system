# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 命令修复引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-CMD-REPAIR-UID9622
自动检测失效命令并修复
"""
import os, sys, json, re, subprocess
from pathlib import Path
from datetime import datetime

HOME = Path.home()
INDEX_FILE = HOME / ".longhun" / "cmd_index" / "commands.json"
REPAIR_LOG = HOME / ".longhun" / "cmd_index" / "repair_log.jsonl"
LH_ENTRY = HOME / "longhun-system" / "bin" / "lh.py"

class CommandRepair:
    def __init__(self):
        self.index = self._load_index()
        self.repaired = []
        self.failed = []

    def _load_index(self):
        if INDEX_FILE.exists():
            try:
                return json.loads(INDEX_FILE.read_text(encoding='utf-8'))
            except Exception:
                pass
        return {"commands": [], "services": [], "skills": []}

    def check_all(self):
        issues = []
        for cmd in self.index.get("commands", []):
            result = self._check_command(cmd["name"], cmd.get("source", "lh"))
            if not result["available"]:
                issues.append({"type": "command", "name": cmd["name"], "issue": result["reason"], "original": cmd})
        for svc in self.index.get("services", []):
            result = self._check_service(svc["port"])
            if not result["available"]:
                issues.append({"type": "service", "name": svc.get("process", "unknown"), "port": svc["port"], "issue": result["reason"]})
        return issues

    def _check_command(self, cmd_name, source="lh"):
        """检查单个命令：静态校验（lh 子命令）+ which（独立命令）"""
        if source == "lh" and LH_ENTRY.exists():
            # 静态确认该命令定义在 lh.py 中（SUB_DISPATCH key 或 subcmd==分支）——无需运行，快且准
            try:
                content = LH_ENTRY.read_text(encoding='utf-8', errors='ignore')
                if re.search(r'subcmd\s*==\s*[\'"]%s[\'"]|[\'"]%s[\'"]\s*:\s*\(' % (re.escape(cmd_name), re.escape(cmd_name)), content):
                    return {"available": True, "path": f"lh {cmd_name}"}
            except Exception:
                pass
        try:
            r = subprocess.run(["which", cmd_name], capture_output=True, text=True, timeout=3)
            if r.returncode == 0 and r.stdout.strip():
                return {"available": True, "path": r.stdout.strip()}
        except Exception:
            pass
        return {"available": False, "reason": "命令不存在或不可执行"}

    def _check_service(self, port):
        try:
            r = subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, text=True, timeout=10)
            if r.stdout.strip():
                return {"available": True, "pid": r.stdout.split()[1] if len(r.stdout.split()) > 1 else "unknown"}
            return {"available": False, "reason": f"端口 {port} 未监听"}
        except Exception:
            return {"available": False, "reason": "检查失败"}

    def repair(self, issue):
        if issue["type"] == "command":
            return self._repair_command(issue)
        elif issue["type"] == "service":
            return self._repair_service(issue)
        return False

    def _repair_command(self, issue):
        name = issue["name"]
        try:
            alias_file = HOME / ".longhun" / "user_aliases.json"
            aliases = {}
            if alias_file.exists():
                try:
                    aliases = json.loads(alias_file.read_text(encoding='utf-8'))
                except Exception:
                    aliases = {}
            if name not in aliases:
                aliases[name] = f"lh {name}"
                alias_file.parent.mkdir(parents=True, exist_ok=True)
                alias_file.write_text(json.dumps(aliases, indent=2, ensure_ascii=False), encoding='utf-8')
                self.repaired.append(f"登记别名: {name} -> lh {name}")
                return True
            return False
        except Exception:
            return False

    def _repair_service(self, issue):
        port = issue["port"]
        try:
            for cmd in self.index.get("commands", []):
                if port in cmd.get("description", ""):
                    subprocess.Popen([sys.executable, str(LH_ENTRY), cmd["name"], "--daemon"], cwd=str(HOME / "longhun-system"))
                    self.repaired.append(f"重启服务: {cmd['name']} (端口 {port})")
                    return True
            return False
        except Exception:
            return False

    def auto_repair_all(self):
        issues = self.check_all()
        results = {"total": len(issues), "repaired": 0, "failed": 0, "details": []}
        for issue in issues:
            if self.repair(issue):
                results["repaired"] += 1
                results["details"].append({"issue": issue, "status": "repaired"})
            else:
                results["failed"] += 1
                results["details"].append({"issue": issue, "status": "failed"})
        self._log_results(results)
        return results

    def _log_results(self, results):
        REPAIR_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(REPAIR_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps({"timestamp": datetime.now().isoformat(), "results": results}, ensure_ascii=False) + "\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐉 命令修复引擎")
    parser.add_argument("--check", action="store_true", help="检查所有命令")
    parser.add_argument("--repair", action="store_true", help="自动修复")
    args = parser.parse_args()
    repair = CommandRepair()
    if args.check:
        issues = repair.check_all()
        print(f"\n🔍 发现 {len(issues)} 个问题")
        for issue in issues[:10]:
            print(f"  ❌ {issue['type']}: {issue.get('name', issue.get('port'))} - {issue['issue']}")
        if len(issues) > 10:
            print(f"  ... 还有 {len(issues)-10} 个")
        return
    if args.repair:
        results = repair.auto_repair_all()
        print(f"\n🔧 修复完成")
        print(f"  ✅ 已修复: {results['repaired']}")
        print(f"  ❌ 失败: {results['failed']}")
        return
    parser.print_help()

if __name__ == "__main__":
    main()
