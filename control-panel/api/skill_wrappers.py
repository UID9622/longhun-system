# DNA: #龍芯⚡️丙午·乙未·乙丑·泰-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-SKILL_WRAPPERS-FILE1-v1.0-2
# 君子協議: 本文件受龍魂DNA追溯保護

"""
龍魂技能 API 封裝層
將 skills/py-skills/ 下的腳本封裝為可調用函數，供 FastAPI 使用。
"""
import base64
import inspect
import io
import json
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Any, Dict

# 確保 skills/py-skills 在路徑中
SKILLS_DIR = Path(__file__).resolve().parents[2] / "skills" / "py-skills"
sys.path.insert(0, str(SKILLS_DIR))

import importlib.util


def _load_module(name: str, file_name: str):
    spec = importlib.util.spec_from_file_location(name, str(SKILLS_DIR / file_name))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mcp_mod = _load_module("mcp_builder", "skill-6-mcp-builder.py")
skill_creator_mod = _load_module("skill_creator", "skill-7-skill-creator.py")
gif_mod = _load_module("slack_gif_creator", "skill-8-slack-gif-creator.py")
theme_mod = _load_module("theme_factory", "skill-9-theme-factory.py")
web_mod = _load_module("web_artifacts_builder", "skill-10-web-artifacts-builder.py")


def run_mcp_builder(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Skill-6: MCP 服務器構建工具"""
    name = payload.get("name", "longhun-mcp-service")
    version = payload.get("version", "1.0.0")
    tools = payload.get("tools", [])
    resources = payload.get("resources", [])

    builder = mcp_mod.MCPBuilder(name, version)
    for tool in tools:
        builder.add_tool(tool.get("name", "tool"), tool.get("description", ""), tool.get("parameters", {}))
    for res in resources:
        builder.add_resource(res.get("uri", "/"), res.get("name", ""), res.get("mime_type", "text/plain"))

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        # 手動保存項目文件（規避原 skill 中 generate_server_code 的 f-string 嵌套 bug）
        config = builder.generate_config()
        (tmp_path / "mcp_config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
        (tmp_path / "requirements.txt").write_text(builder.generate_requirements(), encoding="utf-8")
        (tmp_path / "Dockerfile").write_text(builder.generate_dockerfile(), encoding="utf-8")
        (tmp_path / "README.md").write_text(
            f"# {name}\n\nAuto-generated MCP server.\n\n## Tools\n" +
            "".join(f"- **{t['name']}**: {t['description']}\n" for t in builder.tools) +
            "\n## Resources\n" +
            "".join(f"- **{r['uri']}**: {r['name']}\n" for r in builder.resources),
            encoding="utf-8"
        )
        # 構建可執行的 server.py，避免在 Python 字符串中再嵌套 f-string
        tool_code = "\n".join(
            f'''@server.call_tool("{t['name']}")
async def tool_{t['name'].replace('-', '_')}(request):
    """{t['description']}"""
    return {{"status": "success", "result": "Tool {t['name']} executed"}}
''' for t in builder.tools
        )
        resource_code = "\n".join(
            f'''@server.read_resource("{r['uri']}")
async def res_{r['name'].replace('-', '_')}():
    """{r['name']}"""
    return "{r['name']} content"
''' for r in builder.resources
        )
        server_code = f'''#!/usr/bin/env python3
"""{name} MCP Server v{version}"""
from fastmcp import Server
server = Server("{name}")

{tool_code}

{resource_code}

if __name__ == "__main__":
    print("🚀 {name} MCP Server started")
    server.run()
'''
        (tmp_path / "server.py").write_text(server_code, encoding="utf-8")
        files = sorted(tmp_path.rglob("*"))
        file_list = [str(f.relative_to(tmp_path)) for f in files if f.is_file()]

    return {
        "server_code": server_code,
        "generated_files": file_list,
        "metadata": {"name": name, "version": version, "tools": len(tools), "resources": len(resources)},
    }


async def run_skill_creator(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Skill-7: 技能創建框架"""
    skill_id = payload.get("skill_id", "demo-skill")
    name = payload.get("name", "Demo Skill")
    description = payload.get("description", "Auto-created skill")
    category = payload.get("category", "general")

    skill = skill_creator_mod.Skill(skill_id, name, description, author="Longhun", category=category)

    def executor(**kwargs: Any) -> Dict[str, Any]:
        return {"status": "ok", "echo": kwargs}

    skill.set_executor(executor)
    skill.add_test({"msg": "hello"}, {"status": "ok", "echo": {"msg": "hello"}})
    result = await skill.execute(msg="hello")

    return {
        "metadata": skill_creator_mod.asdict(skill.metadata),
        "execution_result": result,
        "config": skill.export_config(),
    }


def run_slack_gif_creator(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Skill-8: Slack GIF 創建工具"""
    width = payload.get("width", 512)
    height = payload.get("height", 512)
    gif_type = payload.get("type", "loading_spinner")

    creator = gif_mod.SlackGIFCreator(width=width, height=height)

    if gif_type == "loading_spinner":
        creator.create_loading_spinner()
    elif gif_type == "success_check":
        creator.create_success_check()
    elif gif_type == "error_x":
        creator.create_error_x()
    elif gif_type == "pulse":
        creator.create_pulse()
    elif gif_type == "wave":
        creator.create_wave()
    else:
        creator.create_loading_spinner()

    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp:
        tmp_path = tmp.name
    creator.save(tmp_path, optimize=True)
    b64 = base64.b64encode(Path(tmp_path).read_bytes()).decode("utf-8")
    Path(tmp_path).unlink(missing_ok=True)

    return {
        "type": gif_type,
        "dimensions": {"width": width, "height": height},
        "frame_count": len(creator.frames),
        "gif_base64": f"data:image/gif;base64,{b64}",
    }


def run_theme_factory(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Skill-9: 主題工廠"""
    base = payload.get("base", "longhun-cyber")
    name = payload.get("name", base)

    factory = theme_mod.ThemeFactory()
    presets = factory.list_presets()
    if base not in presets:
        base = presets[0] if presets else "longhun-cyber"
    theme = factory.get_preset(base)

    return {
        "available_presets": presets,
        "selected_preset": base,
        "theme_name": name or theme.name,
        "description": theme.description,
        "css_variables": theme.generate_css_variables(),
        "css_classes": theme.generate_css_classes(),
        "config": theme.export_config(),
    }


def run_web_artifacts_builder(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Skill-10: Web 工件構建器"""
    artifact_id = payload.get("artifact_id", "demo-page")
    name = payload.get("name", "Demo Page")
    artifact_type = payload.get("type", "html")
    code = payload.get("code", "<h1>Hello Longhun</h1>")

    artifact = web_mod.WebArtifact(artifact_id, name, artifact_type, code=code)

    with tempfile.TemporaryDirectory() as tmp:
        result = artifact.save(tmp)
        saved_path = result.get("code_file")
        saved_code = Path(saved_path).read_text(encoding="utf-8") if saved_path and Path(saved_path).exists() else ""

    return {
        "metadata": artifact.export_metadata(),
        "saved_files": {"code_file": result.get("code_file"), "metadata_file": result.get("metadata_file")},
        "code_preview": saved_code[:2000],
    }


SKILL_RUNNERS = {
    "skill-6-mcp-builder": run_mcp_builder,
    "skill-7-skill-creator": run_skill_creator,
    "skill-8-slack-gif-creator": run_slack_gif_creator,
    "skill-9-theme-factory": run_theme_factory,
    "skill-10-web-artifacts-builder": run_web_artifacts_builder,
}


async def run_skill(skill_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    if skill_id not in SKILL_RUNNERS:
        raise ValueError(f"Unknown Python skill: {skill_id}")
    try:
        runner = SKILL_RUNNERS[skill_id]
        if inspect.iscoroutinefunction(runner):
            result = await runner(payload)
        else:
            result = runner(payload)
        return {"status": "success", "skill_id": skill_id, "result": result}
    except Exception as e:
        return {"status": "error", "skill_id": skill_id, "error": str(e), "trace": traceback.format_exc()}
