#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂 Web 工件构建器 v1.0
Longhun Web Artifacts Builder

DNA: #龍芯⚡️2026-06-07-WEB-ARTIFACTS-BUILDER-v1.0
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class ArtifactMetadata:
    """工件元数据"""
    id: str
    name: str
    type: str  # html, react, svg, component
    version: str
    created_at: str
    updated_at: str
    author: str = "Longhun"
    tags: List[str] = None
    description: str = ""
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class WebArtifact:
    """Web 工件基础类"""
    
    def __init__(
        self,
        artifact_id: str,
        name: str,
        artifact_type: str,
        code: str = "",
        description: str = ""
    ):
        self.metadata = ArtifactMetadata(
            id=artifact_id,
            name=name,
            type=artifact_type,
            version="1.0.0",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            description=description
        )
        self.code = code
        self.dependencies: List[str] = []
        self.assets: Dict[str, str] = {}
    
    def add_dependency(self, dependency: str) -> None:
        """添加依赖"""
        if dependency not in self.dependencies:
            self.dependencies.append(dependency)
    
    def add_asset(self, name: str, content: str) -> None:
        """添加资源"""
        self.assets[name] = content
    
    def export_metadata(self) -> Dict:
        """导出元数据"""
        return {
            "metadata": asdict(self.metadata),
            "dependencies": self.dependencies,
            "assets": list(self.assets.keys()),
            "code_length": len(self.code)
        }
    
    def save(self, output_dir: str = ".") -> Dict:
        """保存工件"""
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存代码
        ext = self._get_file_extension()
        code_file = f"{output_dir}/{self.metadata.id}.{ext}"
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(self.code)
        
        # 保存元数据
        metadata_file = f"{output_dir}/{self.metadata.id}.meta.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.export_metadata(), f, indent=2, ensure_ascii=False)
        
        # 保存资源
        for asset_name, asset_content in self.assets.items():
            asset_file = f"{output_dir}/{asset_name}"
            with open(asset_file, 'w', encoding='utf-8') as f:
                f.write(asset_content)
        
        return {
            "artifact_id": self.metadata.id,
            "code_file": code_file,
            "metadata_file": metadata_file,
            "asset_files": list(self.assets.keys()),
            "status": "saved"
        }
    
    def _get_file_extension(self) -> str:
        """获取文件扩展名"""
        extensions = {
            "html": "html",
            "react": "jsx",
            "svg": "svg",
            "component": "jsx"
        }
        return extensions.get(self.metadata.type, "txt")


class HTMLArtifact(WebArtifact):
    """HTML 工件"""
    
    def __init__(self, artifact_id: str, name: str, code: str = ""):
        super().__init__(artifact_id, name, "html", code)
        self.add_dependency("HTML5")


class ReactArtifact(WebArtifact):
    """React 工件"""
    
    def __init__(self, artifact_id: str, name: str, code: str = ""):
        super().__init__(artifact_id, name, "react", code)
        self.add_dependency("react@18.0.0")
        self.add_dependency("react-dom@18.0.0")


class SVGArtifact(WebArtifact):
    """SVG 工件"""
    
    def __init__(self, artifact_id: str, name: str, code: str = ""):
        super().__init__(artifact_id, name, "svg", code)
        self.add_dependency("SVG 1.1")


class ArtifactBuilder:
    """工件构建器"""
    
    def __init__(self):
        self.artifacts: Dict[str, WebArtifact] = {}
        self.build_log: List[str] = []
    
    def create_html_artifact(
        self,
        artifact_id: str,
        name: str,
        code: str,
        description: str = ""
    ) -> HTMLArtifact:
        """创建 HTML 工件"""
        artifact = HTMLArtifact(artifact_id, name, code)
        artifact.metadata.description = description
        self.artifacts[artifact_id] = artifact
        self._log(f"✅ HTML 工件已创建: {name}")
        return artifact
    
    def create_react_artifact(
        self,
        artifact_id: str,
        name: str,
        code: str,
        description: str = ""
    ) -> ReactArtifact:
        """创建 React 工件"""
        artifact = ReactArtifact(artifact_id, name, code)
        artifact.metadata.description = description
        self.artifacts[artifact_id] = artifact
        self._log(f"✅ React 工件已创建: {name}")
        return artifact
    
    def create_svg_artifact(
        self,
        artifact_id: str,
        name: str,
        code: str,
        description: str = ""
    ) -> SVGArtifact:
        """创建 SVG 工件"""
        artifact = SVGArtifact(artifact_id, name, code)
        artifact.metadata.description = description
        self.artifacts[artifact_id] = artifact
        self._log(f"✅ SVG 工件已创建: {name}")
        return artifact
    
    def get_artifact(self, artifact_id: str) -> Optional[WebArtifact]:
        """获取工件"""
        return self.artifacts.get(artifact_id)
    
    def list_artifacts(self) -> List[Dict]:
        """列出所有工件"""
        return [
            {
                "id": a.metadata.id,
                "name": a.metadata.name,
                "type": a.metadata.type,
                "code_length": len(a.code)
            }
            for a in self.artifacts.values()
        ]
    
    def build_bundle(self, output_dir: str = ".") -> Dict:
        """构建包含所有工件的包"""
        os.makedirs(output_dir, exist_ok=True)
        
        bundle_info = {
            "timestamp": datetime.now().isoformat(),
            "artifact_count": len(self.artifacts),
            "artifacts": [],
            "dna": "#龍芯⚡️2026-06-07-WEB-ARTIFACTS-BUILDER-v1.0"
        }
        
        for artifact in self.artifacts.values():
            save_result = artifact.save(output_dir)
            bundle_info["artifacts"].append(save_result)
        
        # 保存包元数据
        bundle_file = f"{output_dir}/bundle.json"
        with open(bundle_file, 'w', encoding='utf-8') as f:
            json.dump(bundle_info, f, indent=2, ensure_ascii=False)
        
        self._log(f"✅ 工件包已构建: {bundle_file}")
        
        return bundle_info
    
    def generate_index_html(self, output_dir: str = ".") -> str:
        """生成索引 HTML"""
        html = """<!DOCTYPE html>
<html lang="zh-Hans">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐉 龍魂 Web 工件</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #151a3f 100%);
            color: #fff;
            padding: 40px 20px;
        }
        .container { max-width: 1000px; margin: 0 auto; }
        h1 {
            background: linear-gradient(90deg, #00d4ff, #00f5ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .artifact-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }
        .artifact-card {
            background: rgba(21, 26, 63, 0.8);
            border: 2px solid #00d4ff;
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s;
        }
        .artifact-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
        }
        .artifact-type {
            display: inline-block;
            padding: 4px 8px;
            background: rgba(0, 212, 255, 0.2);
            border-radius: 4px;
            font-size: 0.8em;
            color: #00d4ff;
            margin-bottom: 10px;
        }
        .artifact-name {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #00f5ff;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐉 龍魂 Web 工件索引</h1>
        <div class="artifact-list">
            {artifacts}
        </div>
    </div>
</body>
</html>"""
        
        artifacts_html = ""
        for artifact in self.artifacts.values():
            artifacts_html += f"""
            <div class="artifact-card">
                <div class="artifact-type">{artifact.metadata.type.upper()}</div>
                <div class="artifact-name">{artifact.metadata.name}</div>
                <p style="color: #a0aec0; font-size: 0.9em;">{artifact.metadata.description}</p>
                <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #00d4ff; font-size: 0.85em; color: #a0aec0;">
                    代码长度: {len(artifact.code)} 字符<br>
                    依赖: {', '.join(artifact.dependencies)}
                </div>
            </div>
            """
        
        html = html.format(artifacts=artifacts_html)
        
        index_file = f"{output_dir}/index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return index_file
    
    def _log(self, message: str) -> None:
        """记录日志"""
        self.build_log.append(message)
        print(message)
    
    def get_build_log(self) -> List[str]:
        """获取构建日志"""
        return self.build_log


# 示例使用
if __name__ == "__main__":
    print("🐉 龍魂 Web 工件构建器 v1.0")
    print("=" * 50)
    
    builder = ArtifactBuilder()
    
    # 创建 HTML 工件
    print("\n📝 创建 HTML 工件...")
    html_code = """<div style="text-align: center; padding: 50px;">
    <h1 style="color: #00d4ff;">龍魂系统</h1>
    <p style="color: #a0aec0;">Web 工件构建演示</p>
</div>"""
    
    html_artifact = builder.create_html_artifact(
        "artifact-001",
        "HTML 演示",
        html_code,
        "简单的 HTML 演示页面"
    )
    
    # 创建 React 工件
    print("\n⚛️ 创建 React 工件...")
    react_code = """import React from 'react';

export default function App() {
    return (
        <div style={{ textAlign: 'center', padding: '50px' }}>
            <h1 style={{ color: '#00d4ff' }}>龍魂反应式组件</h1>
            <button style={{ padding: '10px 20px', background: '#00d4ff', color: '#0a0e27' }}>
                点击我
            </button>
        </div>
    );
}"""
    
    react_artifact = builder.create_react_artifact(
        "artifact-002",
        "React 组件",
        react_code,
        "交互式 React 组件"
    )
    
    # 创建 SVG 工件
    print("\n🎨 创建 SVG 工件...")
    svg_code = """<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
    <circle cx="100" cy="100" r="80" fill="#00d4ff" opacity="0.2" stroke="#00d4ff" stroke-width="2"/>
    <text x="100" y="110" text-anchor="middle" fill="#00d4ff" font-size="20" font-weight="bold">龍魂</text>
</svg>"""
    
    svg_artifact = builder.create_svg_artifact(
        "artifact-003",
        "SVG 图形",
        svg_code,
        "龍魂 SVG 标志"
    )
    
    # 列出工件
    print("\n📋 工件列表:")
    for artifact in builder.list_artifacts():
        print(f"  - {artifact['name']} ({artifact['type']})")
    
    # 构建包
    print("\n📦 构建工件包...")
    bundle = builder.build_bundle("/mnt/user-data/outputs/longhun-artifacts")
    print(f"✅ 工件数量: {bundle['artifact_count']}")
    
    # 生成索引
    print("\n📑 生成索引页面...")
    index_file = builder.generate_index_html("/mnt/user-data/outputs/longhun-artifacts")
    print(f"✅ 索引已生成: {index_file}")
    
    # 显示构建日志
    print("\n📊 构建日志:")
    for log in builder.get_build_log():
        print(log)
    
    print("\n✅ Web 工件构建完成！")
