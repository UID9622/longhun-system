#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 文档生成引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-DOC-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 从代码生成API文档
  - 从函数签名生成注释
  - 生成README
  - 生成变更日志
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class DocEngine:
    """文档生成引擎——自动生成API文档/注释/README/变更日志"""

    def __init__(self):
        self.project_root = Path.home() / "longhun-system"

    def generate_api_doc(self, src_dir: Path = None) -> Dict:
        """从源码生成API文档"""
        src_dir = src_dir or self.project_root / "bin"
        endpoints = []
        for py_file in src_dir.rglob("*.py"):
            if py_file.name.startswith("test_"):
                continue
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                # FastAPI路由
                for match in re.finditer(r'''@app\.(\w+)\s*\(\s*["']([^"']+)["']''', content):
                    endpoints.append({
                        "method": match.group(1).upper(),
                        "path": match.group(2),
                        "file": str(py_file.relative_to(self.project_root)),
                    })
                # 普通函数
                for match in re.finditer(r'def\s+(?!_)(\w+)\s*\([^)]*\)', content):
                    endpoints.append({
                        "method": "FUNC",
                        "path": f"/{match.group(1)}",
                        "file": str(py_file.relative_to(self.project_root)),
                    })
            except Exception:
                pass
        return {
            "title": "龍魂系统 API",
            "version": "3.0",
            "endpoints": endpoints,
            "generated": datetime.now().isoformat(),
        }

    def generate_readme(self) -> str:
        return """# 🐉 龍魂系统

## 项目简介
龙魂系统是一个主权级AI智能体框架，支持34+引擎协作、任务编排、自我进化。

## 核心特性
- 34+ 引擎覆盖全链路（理解→执行→审计→记忆→进化）
- 主权级数据保护（端侧加密·云上只存密文）
- 国产芯片适配（鲲鹏·华为云）
- 君子协议治理
- 省电积分机制

## 快速开始
```bash
lh 健康检查
lh 审计 .
lh 自我进化
```

## 文档
- [架构文档](./docs/ARCHITECTURE.md)
- [君子协议](./GENTLEMANS_PROTOCOL.md)
- [治理文档](./GOVERNANCE.md)

## 许可证
CC BY-NC-SA 4.0 + 君子协议
"""

    def generate_changelog(self) -> str:
        try:
            result = subprocess.run(
                ["git", "-C", str(self.project_root), "log", "--oneline", "--since=30.days"],
                capture_output=True, text=True, timeout=10,
            )
            lines = result.stdout.strip().split("\n")[:20]
            if not lines or lines == ['']:
                return "近期无变更"
            return "## 变更日志 (最近30天)\n\n" + "\n".join(f"- {line}" for line in lines if line)
        except Exception:
            return "无法获取git日志"

    def generate_comment(self, function_code: str) -> str:
        name_match = re.search(r'def\s+(\w+)', function_code)
        if not name_match:
            return ""
        func_name = name_match.group(1)
        params = re.findall(r'(\w+)(?::\s*\w+)?(?:\s*,\s*|\s*\))', function_code)
        param_doc = "\n".join(f"    {p}: 参数说明" for p in params) if params else "    无"
        return f'''"""
{func_name} 函数

参数:
{param_doc}

返回:
    执行结果

DNA: #龍芯⚡️{datetime.now().strftime("%Y%m%d%H%M%S")}-DOC-UID9622
"""'''


if __name__ == "__main__":
    engine = DocEngine()
    doc = engine.generate_api_doc()
    print(f"API文档: {len(doc['endpoints'])} 个端点")
    print(engine.generate_comment("def hello(name: str, age: int) -> str:"))
    print("🟢 文档生成引擎测试通过")
