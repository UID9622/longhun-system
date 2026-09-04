#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂技能统一注册表
LongHun Unified Skill Registry

负责把项目内部 skills/ 与 ~/.kimi-code/skills/longhun-* 同级技能
统一扫描、去重、生成元数据，供 control-panel 调用。

DNA: #龍芯⚡️丙午·甲午·戊辰·戊午·䷑蛊-LONGHUN-SKILL-REGISTRY-v2.0
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()
EXTERNAL_SKILL_ROOT = HOME / ".kimi-code" / "skills"
INSTALLED_JSON = Path("/tmp/all_installed_skills.json")

# 已知的云端技能，调度时需要特殊端口配置
CLOUD_SKILL_IDS = {
    "longhun-cloud-panel",
    "longhun-cloud-deploy",
    "longhun-cloud-mcp",
    "longhun-cloud-notion",
    "longhun-cloud-kimi",
}

# 默认云端端口（可通过环境变量覆盖）
CLOUD_DEFAULT_PORTS = {
    "longhun-cloud-panel": int(os.getenv("LONGHUN_CLOUD_PANEL_PORT", "8443")),
    "longhun-cloud-deploy": int(os.getenv("LONGHUN_CLOUD_DEPLOY_PORT", "8444")),
    "longhun-cloud-mcp": int(os.getenv("LONGHUN_CLOUD_MCP_PORT", "8445")),
    "longhun-cloud-notion": int(os.getenv("LONGHUN_CLOUD_NOTION_PORT", "8446")),
    "longhun-cloud-kimi": int(os.getenv("LONGHUN_CLOUD_KIMI_PORT", "8447")),
}


def _extract_first_line(text: Any) -> str:
    if not text:
        return ""
    s = str(text).strip()
    # 取第一段，去掉换行
    return s.split("\n")[0].strip()[:200]


def _extract_version(text: Any) -> str:
    """从文本中抓取 vX.Y.Z 版本号。"""
    if not text:
        return ""
    m = re.search(r"v\d+(?:\.\d+){0,2}", str(text))
    return m.group(0) if m else ""


def _parse_skill_md(skill_dir: Path) -> Optional[Dict[str, Any]]:
    """解析 SKILL.md 的 YAML frontmatter。"""
    md_path = skill_dir / "SKILL.md"
    if not md_path.exists():
        return None
    content = md_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        # 没有 frontmatter，退化到目录名
        return None
    # 分离 frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except Exception:
        return None
    return meta


def _scan_scripts(skill_dir: Path) -> List[str]:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return []
    result = []
    for f in sorted(scripts_dir.iterdir()):
        if f.is_file() and f.suffix in (".py", ".sh"):
            result.append(f.name)
    return result


def _detect_skill_type(scripts: List[str], internal_type: Optional[str] = None) -> str:
    if internal_type:
        return internal_type
    has_py = any(s.endswith(".py") for s in scripts)
    has_sh = any(s.endswith(".sh") for s in scripts)
    if has_py and has_sh:
        return "mixed"
    if has_py:
        return "python"
    if has_sh:
        return "shell"
    return "doc"


def _build_metadata(skill_dir: Path, source: str, internal_type: Optional[str] = None) -> Optional[Dict[str, Any]]:
    meta = _parse_skill_md(skill_dir) or {}
    skill_id = meta.get("name") or skill_dir.name
    # 避免空 ID
    if not skill_id:
        return None

    scripts = _scan_scripts(skill_dir)
    # 对内部 py-skills/html-skills 可能没有 SKILL.md，也没有 scripts/，需要特殊处理
    if internal_type in ("html", "python") and not scripts:
        # 内部 skill 文件直接位于 html-skills/ 或 py-skills/ 下
        if skill_dir.is_file():
            scripts = [skill_dir.name]

    version = meta.get("metadata", {}).get("version") if isinstance(meta.get("metadata"), dict) else None
    if not version:
        version = _extract_version(meta.get("description")) or _extract_version(skill_dir.name)
    version = str(version).lstrip("v")  # 统一存成 x.y.z 形式
    dna = None
    if isinstance(meta.get("metadata"), dict):
        dna = meta["metadata"].get("dna")
    if not dna:
        # 从正文抓取 #龍芯⚡️...
        md_path = skill_dir / "SKILL.md"
        if md_path.exists():
            text = md_path.read_text(encoding="utf-8")
            m = re.search(r"#龍芯⚡️[^\s\n]+", text)
            if m:
                dna = m.group(0)

    description = _extract_first_line(meta.get("description")) or skill_id

    return {
        "id": skill_id,
        "name": meta.get("name") or skill_dir.name,
        "version": version or "unknown",
        "description": description,
        "scope": "project",
        "type": _detect_skill_type(scripts, internal_type),
        "scripts": scripts,
        "path": str(skill_dir),
        "source": source,
        "dna": dna,
        "cloud_port": CLOUD_DEFAULT_PORTS.get(skill_id),
    }


class LonghunSkillRegistry:
    """龍魂统一技能注册表。"""

    def __init__(self):
        self.skills: Dict[str, Dict[str, Any]] = {}
        self._scan_internal()
        self._scan_external()
        self._merge_installed_json()

    def _scan_internal(self):
        """扫描项目内部 skills/。"""
        skills_dir = ROOT / "skills"
        if not skills_dir.is_dir():
            return

        # 1. html-skills / py-skills
        for sub_name, sk_type in [("html-skills", "html"), ("py-skills", "python")]:
            sub_dir = skills_dir / sub_name
            if not sub_dir.is_dir():
                continue
            for filepath in sorted(sub_dir.iterdir()):
                if filepath.is_dir():
                    continue
                ext = filepath.suffix.lower()
                if ext not in (".html", ".py"):
                    continue
                skill_id = filepath.stem
                # 对 skill-1-algorithmic-art 提取显示名
                parts = skill_id.split("-", 2)
                name = parts[2] if len(parts) > 2 else skill_id
                self.skills[skill_id] = {
                    "id": skill_id,
                    "name": name,
                    "version": "1.0",
                    "description": f"内置 {sk_type} 技能: {name}",
                    "scope": "project",
                    "type": sk_type,
                    "scripts": [filepath.name],
                    "path": str(filepath),
                    "source": "internal",
                    "dna": "#龍芯⚡️丙午·甲午·辛酉·甲午·䷨损-SKILL-REGISTRY-v2.0",
                    "cloud_port": None,
                }

        # 2. 内部 longhun 能力目录（含 SKILL.md）
        for sub_dir in sorted(skills_dir.iterdir()):
            if not sub_dir.is_dir():
                continue
            if sub_dir.name in ("html-skills", "py-skills"):
                continue
            if not (sub_dir / "SKILL.md").exists():
                continue
            meta = _build_metadata(sub_dir, source="internal")
            if meta and meta["id"] not in self.skills:
                self.skills[meta["id"]] = meta

    def _scan_external(self):
        """扫描 ~/.kimi-code/skills/ 下的 longhun-* 同级技能。"""
        if not EXTERNAL_SKILL_ROOT.is_dir():
            return
        for sub_dir in sorted(EXTERNAL_SKILL_ROOT.iterdir()):
            if not sub_dir.is_dir():
                continue
            # 只合并 longhun-*、CNSH-*、china-digital-identity、dragon-soul-agent 等项目级技能
            if not (
                sub_dir.name.startswith("longhun-")
                or sub_dir.name.startswith("CNSH-")
                or sub_dir.name in ("china-digital-identity", "dragon-soul-agent")
            ):
                continue
            if not (sub_dir / "SKILL.md").exists():
                continue
            meta = _build_metadata(sub_dir, source="external")
            if not meta:
                continue
            # 命名对齐：外部 longhun-audit 与内部 longhun-audit-integrated 区分开
            if meta["id"] in self.skills and self.skills[meta["id"]]["source"] == "internal":
                # 内部已占用 id，给外部加后缀
                meta["id"] = meta["id"] + "-external"
            self.skills[meta["id"]] = meta

    def _merge_installed_json(self):
        """补充 /tmp/all_installed_skills.json 中没有 SKILL.md 的技能信息。"""
        if not INSTALLED_JSON.exists():
            return
        try:
            installed = json.loads(INSTALLED_JSON.read_text(encoding="utf-8"))
        except Exception:
            return
        for sk in installed:
            sk_id = sk.get("id")
            if not sk_id or sk_id in self.skills:
                continue
            # 跳过非项目级技能（例如 azure-*）
            path = sk.get("path", "")
            if ".agents/skills/" in path:
                continue
            scripts = [s for s in sk.get("scripts", []) if s.endswith(".py") or s.endswith(".sh")]
            self.skills[sk_id] = {
                "id": sk_id,
                "name": sk.get("name") or sk_id,
                "version": _extract_version(sk.get("description", "")),
                "description": _extract_first_line(sk.get("description", "")),
                "scope": sk.get("scope", "project"),
                "type": _detect_skill_type(scripts),
                "scripts": scripts,
                "path": path,
                "source": "external-json",
                "dna": None,
                "cloud_port": CLOUD_DEFAULT_PORTS.get(sk_id),
            }

    def list_skills(self) -> List[Dict[str, Any]]:
        return list(self.skills.values())

    def get_skill(self, skill_id: str) -> Optional[Dict[str, Any]]:
        return self.skills.get(skill_id)

    def export_json(self, path: Optional[Path] = None) -> str:
        data = {
            "total": len(self.skills),
            "skills": self.list_skills(),
            "dna": "#龍芯⚡️丙午·甲午·戊辰·戊午·䷑蛊-LONGHUN-SKILL-REGISTRY-v2.0",
        }
        text = json.dumps(data, ensure_ascii=False, indent=2)
        if path:
            path.write_text(text, encoding="utf-8")
        return text

    def print_overview(self):
        print("=" * 70)
        print("  🐉 龍魂技能全景图 | LongHun Skill Registry v2.0")
        print("=" * 70)
        for source in ("internal", "external", "external-json"):
            group = [s for s in self.skills.values() if s["source"] == source]
            if not group:
                continue
            label = {"internal": "项目内部", "external": "外部 longhun-*", "external-json": "JSON 补充"}[source]
            print(f"\n  📦 {label}（{len(group)} 个）")
            print("  " + "-" * 60)
            for sk in group:
                port = f" :{sk['cloud_port']}" if sk.get("cloud_port") else ""
                ver = f"v{sk['version']}" if sk['version'] != "unknown" else "unknown"
                print(f"    {sk['id']:<35} | {sk['type']:<8} | {ver}{port}")
                print(f"       └─ {sk['description'][:55]}")
        print("\n" + "=" * 70)
        print(f"  总计: {len(self.skills)} 个技能")
        print("=" * 70)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂技能统一注册表")
    parser.add_argument("--list", action="store_true", help="打印技能全景图")
    parser.add_argument("--json", type=str, help="导出 JSON 到指定路径")
    args = parser.parse_args()

    registry = LonghunSkillRegistry()
    if args.json:
        out = Path(args.json)
        registry.export_json(out)
        print(f"[注册表] 💾 已导出: {out}")
    if args.list or not args.json:
        registry.print_overview()


if __name__ == "__main__":
    main()
