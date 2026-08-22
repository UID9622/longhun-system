# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 全盘命令扫描引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-CMD-SCANNER-UID9622
扫描所有来源，生成统一命令索引
覆盖: lh命令 / 08_BIN脚本 / 05_ENGINES引擎 / 运行服务 / Skills / 知识图谱 / 别名 / Notion导出
"""
import os, sys, json, re, subprocess
from pathlib import Path
from datetime import datetime

HOME = Path.home()
PROJECT_ROOT = HOME / "longhun-system"
INDEX_FILE = HOME / ".longhun" / "cmd_index" / "commands.json"
LH_ENTRY = PROJECT_ROOT / "bin" / "lh.py"

class CommandScanner:
    def __init__(self):
        self.index = {
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "sources": {}, "commands": [], "services": [],
            "skills": [], "knowledge": [], "aliases": []
        }

    def scan_all(self):
        print("🔍 开始全盘扫描...")
        self._scan_lh_commands()
        print(f"  ✅ lh 命令: {len(self.index['commands'])} 个")
        self._scan_bin_scripts()
        print(f"  ✅ 08_BIN 脚本: {len(self.index['sources'].get('bin', []))} 个")
        self._scan_engines()
        print(f"  ✅ 引擎: {len(self.index['sources'].get('engines', []))} 个")
        self._scan_services()
        print(f"  ✅ 运行服务: {len(self.index['services'])} 个")
        self._scan_skills()
        print(f"  ✅ Skills: {len(self.index['skills'])} 个")
        self._scan_knowledge()
        print(f"  ✅ 知识节点: {len(self.index['knowledge'])} 个")
        self._scan_aliases()
        print(f"  ✅ 别名: {len(self.index['aliases'])} 个")
        self._scan_notion_export()
        print(f"  ✅ Notion 知识: {len(self.index['sources'].get('notion', []))} 条")
        self._save_index()
        return self.index

    def _scan_lh_commands(self):
        """扫描 lh 命令：黄金来源 = SUB_DISPATCH 注册表（280+ 子命令含描述）"""
        lh_file = LH_ENTRY
        if not lh_file.exists():
            lh_file = HOME / "bin" / "lh"
        if not lh_file.exists():
            print("  ⚠️ 未找到 lh 入口"); return
        content = lh_file.read_text(encoding='utf-8', errors='ignore')
        seen = set()
        # 主来源: SUB_DISPATCH dict 的 key + 描述
        m = re.search(r'SUB_DISPATCH\s*=\s*\{(.*?)\n\}', content, re.DOTALL)
        if m:
            body = m.group(1)
            pat = re.compile(r'[\'"]([a-z][a-z0-9_-]*)[\'"]\s*:\s*\(\s*[\'"][^\'"]*[\'"]\s*,\s*[\'"][^\'"]*[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]')
            for km in pat.finditer(body):
                name, desc = km.group(1), km.group(2).strip()
                if name not in seen:
                    seen.add(name)
                    self.index["commands"].append({"name": name, "description": desc, "source": "lh", "type": "command", "path": str(lh_file)})
        # 补充: subcmd == "x" 分支（SUB_DISPATCH 之外的内置子命令）
        for m2 in re.finditer(r'subcmd\s*==\s*[\'"]([a-z][a-z0-9_-]*)[\'"]', content):
            name = m2.group(1)
            if name not in seen:
                seen.add(name)
                self.index["commands"].append({"name": name, "description": "", "source": "lh", "type": "command", "path": str(lh_file)})

    def _scan_bin_scripts(self):
        bin_dir = PROJECT_ROOT / "08_BIN"
        if not bin_dir.exists(): return
        scripts = []
        for f in sorted(bin_dir.rglob("*.py")):
            if f.name.startswith("__"): continue
            scripts.append({"name": f.stem, "path": str(f), "description": self._extract_description(f), "type": "script"})
        self.index["sources"]["bin"] = scripts

    def _scan_engines(self):
        engine_dir = PROJECT_ROOT / "05_ENGINES"
        if not engine_dir.exists(): return
        engines = []
        for f in sorted(engine_dir.rglob("*.py")):
            if f.name.startswith("__"): continue
            engines.append({"name": f.stem, "path": str(f), "description": self._extract_description(f), "type": "engine"})
        self.index["sources"]["engines"] = engines

    def _scan_services(self):
        try:
            result = subprocess.run(["lsof", "-iTCP", "-sTCP:LISTEN", "-P", "-n"], capture_output=True, text=True, timeout=20)
            seen = set()
            for line in result.stdout.split("\n"):
                parts = line.split()
                if len(parts) < 9 or parts[0] == "COMMAND": continue
                proc = parts[0].lower()
                if proc in ("python", "python3", "node"):
                    nf = parts[8]
                    port = nf.split(":")[-1].strip("() ").split(" ")[0] if ":" in nf else nf
                    key = f"{parts[0]}:{port}"
                    if key in seen: continue
                    seen.add(key)
                    self.index["services"].append({"process": parts[0], "pid": parts[1], "port": port, "status": "running"})
        except Exception:
            pass

    def _scan_skills(self):
        skill_dir = PROJECT_ROOT / "skills"
        if not skill_dir.exists(): return
        for skill_path in sorted(skill_dir.rglob("SKILL.md")):
            try:
                content = skill_path.read_text(encoding='utf-8', errors='ignore')
                nm = re.search(r'name:\s*(.+?)(?:\n|$)', content)
                tm = re.search(r'(?:trigger|触发[：:]|when[：:])\s*(.+?)(?:\n|$)', content)
                self.index["skills"].append({
                    "name": nm.group(1).strip() if nm else skill_path.parent.name,
                    "path": str(skill_path),
                    "trigger": tm.group(1).strip()[:200] if tm else "",
                    "status": "active"})
            except Exception:
                pass

    def _scan_knowledge(self):
        kg_dir = HOME / ".longhun" / "knowledge_graph"
        # 主入口: knowledge_index.json
        kg_file = kg_dir / "knowledge_index.json"
        if not kg_file.exists():
            kg_file = kg_dir / "knowledge_export_20260815.json"
        if kg_file.exists():
            try:
                data = json.loads(kg_file.read_text(encoding='utf-8'))
                nodes = data if isinstance(data, list) else data.get("nodes", data.get("entries", []))
                if isinstance(nodes, dict):
                    nodes = list(nodes.values())
                for node in nodes[:500]:
                    if isinstance(node, dict):
                        self.index["knowledge"].append({"id": node.get("id", node.get("key", "")), "title": node.get("title", node.get("name", "")), "content": str(node.get("content", node.get("description", "")))[:100], "type": "knowledge_node"})
            except Exception:
                pass
        # 兜底: nodes/ 目录
        nodes_dir = kg_dir / "nodes"
        if nodes_dir.exists() and not self.index["knowledge"]:
            for f in sorted(nodes_dir.rglob("*.json"))[:500]:
                try:
                    data = json.loads(f.read_text(encoding='utf-8'))
                    title = data.get("title", data.get("name", f.stem))
                    self.index["knowledge"].append({"id": data.get("id", f.stem), "title": title, "content": str(data.get("content", data.get("summary", "")))[:100], "type": "knowledge_node"})
                except Exception:
                    pass

    def _scan_aliases(self):
        alias_file = HOME / ".longhun" / "user_aliases.json"
        if alias_file.exists():
            try:
                aliases = json.loads(alias_file.read_text(encoding='utf-8'))
                for key, value in aliases.items():
                    self.index["aliases"].append({"alias": key, "target": value, "source": "user_aliases.json"})
            except Exception:
                pass

    def _scan_notion_export(self):
        notion_dir = PROJECT_ROOT / "docs" / "notion_full_export"
        if not notion_dir.exists(): return
        items = []
        for f in sorted(notion_dir.rglob("*.json")):
            if f.name.startswith("_index"): continue
            try:
                data = json.loads(f.read_text(encoding='utf-8'))
                title = f.stem
                for key, val in data.get("properties", {}).items():
                    t = val.get("title") or val.get("rich_text")
                    if t:
                        title = t[0].get("text", {}).get("content", f.stem); break
                items.append({"title": title, "path": str(f), "type": "notion_page"})
            except Exception:
                pass
        self.index["sources"]["notion"] = items

    def _extract_description(self, filepath):
        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')[:800]
            ds = re.search(r'"""(.*?)"""', content, re.DOTALL)
            if ds:
                for line in ds.group(1).strip().split("\n"):
                    line = line.strip()
                    if line and not line.startswith("🐉") and "DNA" not in line:
                        return line[:120]
            for line in content.split("\n")[:12]:
                line = line.strip()
                if line.startswith("#") and not line.startswith("#!"):
                    desc = line.lstrip("#").strip()
                    if desc and len(desc) > 5 and "DNA" not in desc and "创建者" not in desc:
                        return desc[:120]
        except Exception:
            pass
        return filepath.stem

    def _save_index(self):
        INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)
        print(f"\n💾 索引已保存: {INDEX_FILE}")

    def _print_summary(self):
        print("\n📊 扫描摘要")
        print("=" * 40)
        print(f"  lh 命令: {len(self.index['commands'])} 个")
        print(f"  08_BIN 脚本: {len(self.index['sources'].get('bin', []))} 个")
        print(f"  引擎: {len(self.index['sources'].get('engines', []))} 个")
        print(f"  运行服务: {len(self.index['services'])} 个")
        print(f"  Skills: {len(self.index['skills'])} 个")
        print(f"  知识节点: {len(self.index['knowledge'])} 个")
        print(f"  别名: {len(self.index['aliases'])} 个")
        print(f"  Notion 导出: {len(self.index['sources'].get('notion', []))} 条")
        print("=" * 40)

if __name__ == "__main__":
    s = CommandScanner()
    s.scan_all()
    s._print_summary()
