#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☰☰ 龍🇨🇳魂 ☷ · 字体管理中枢
DNA: #龍芯⚡️2026-04-08-FONT-MANAGER-v1.0
作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人

功能: 管理15+个字元库和CNSH自制字体
端口: 8081
路由: / (首页) | /fonts (字体列表) | /libs (字元库) | /preview/<ver> | /download/<file>
"""

import json
import os
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE = Path.home() / "longhun-system"
FONT_ENGINE = BASE / "CNSH引擎"
OUTPUT_DIR = FONT_ENGINE / "CNSH_字体输出"


def get_all_glyph_libs():
    """获取所有字元库"""
    libs = []
    for f in sorted(FONT_ENGINE.glob("CNSH_字元库_v*.json")):
        try:
            with open(f, 'r', encoding='utf-8') as file:
                data = json.load(file)
                libs.append({
                    "file": f.name,
                    "version": f.stem.split('_v')[-1],
                    "dna": data.get('DNA追溯码', 'N/A'),
                    "chars": list(data.get('字符集_cnsh9622', {}).keys()),
                    "char_count": len(data.get('字符集_cnsh9622', {}))
                })
        except:
            pass
    return libs


def get_all_fonts():
    """获取所有字体文件"""
    fonts = []
    for f in OUTPUT_DIR.glob("*.ttf"):
        fonts.append({
            "file": f.name,
            "size_kb": round(f.stat().st_size / 1024, 2),
            "path": str(f)
        })
    return fonts


@app.route('/')
def index():
    """字体管理首页"""
    libs = get_all_glyph_libs()
    fonts = get_all_fonts()
    
    return jsonify({
        "name": "☰☰ 龍🇨🇳魂 ☷ · 字体管理中枢",
        "dna": "#龍芯⚡️2026-04-08-FONT-MANAGER-v1.0",
        "stats": {
            "glyph_libs": len(libs),
            "fonts": len(fonts),
            "total_chars": sum(l['char_count'] for l in libs)
        },
        "glyph_libs": libs,
        "fonts": fonts,
        "endpoints": [
            "/fonts - 列出所有字体",
            "/libs - 列出所有字元库",
            "/preview/<version> - 预览字元库",
            "/download/<filename> - 下载字体"
        ]
    })


@app.route('/fonts')
def list_fonts():
    """列出所有字体"""
    return jsonify(get_all_fonts())


@app.route('/libs')
def list_libs():
    """列出所有字元库"""
    return jsonify(get_all_glyph_libs())


@app.route('/download/<filename>')
def download_font(filename):
    """下载字体文件"""
    font_path = OUTPUT_DIR / filename
    if font_path.exists():
        return send_file(font_path, as_attachment=True)
    return jsonify({"error": "字体不存在"}), 404


@app.route('/preview/<version>')
def preview_lib(version):
    """预览字元库内容"""
    lib_file = FONT_ENGINE / f"CNSH_字元库_v{version}.json"
    if not lib_file.exists():
        return jsonify({"error": "字元库不存在"}), 404
    
    try:
        with open(lib_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chars = data.get('字符集_cnsh9622', {})
        preview = {}
        for char_name, char_data in list(chars.items())[:5]:  # 前5个字符
            preview[char_name] = {
                "标识": char_data.get('字元标识', 'N/A'),
                "笔画数": len(char_data.get('笔画路径_cnsh9622', []))
            }
        
        return jsonify({
            "version": version,
            "dna": data.get('DNA追溯码', 'N/A'),
            "工程": data.get('工程名称', 'N/A'),
            "字符预览": preview,
            "总字符数": len(chars)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health')
def health():
    """健康检查 — 供龍魂启动脚本/API检测使用"""
    libs = get_all_glyph_libs()
    fonts = get_all_fonts()
    return jsonify({
        "status": "🟢",
        "dna": "#龍芯⚡️2026-04-08-FONT-MANAGER-v1.0",
        "glyph_libs": len(libs),
        "fonts": len(fonts),
        "total_chars": sum(l['char_count'] for l in libs)
    })


@app.route('/stats')
def stats():
    """统计总览 — 字元库版本对比"""
    libs = get_all_glyph_libs()
    return jsonify({
        "versions": len(libs),
        "libs": [
            {"version": l["version"], "chars": l["char_count"], "dna": l["dna"]}
            for l in libs
        ],
        "latest": libs[-1] if libs else None,
        "evolution": f"v{libs[0]['version']} → v{libs[-1]['version']}" if len(libs) > 1 else "N/A"
    })


if __name__ == '__main__':
    print("🐉 启动字体管理中枢 (端口 8081)")
    print(f"DNA: #龍芯⚡️2026-04-08-FONT-MANAGER-v1.0")
    print(f"📁 字元库: {FONT_ENGINE}")
    print(f"📁 字体输出: {OUTPUT_DIR}")

    libs = get_all_glyph_libs()
    fonts = get_all_fonts()
    print(f"\n📊 统计:")
    print(f"   字元库: {len(libs)} 个 (v0001-v{libs[-1]['version'] if libs else '????'})")
    print(f"   字体文件: {len(fonts)} 个")
    print(f"   总字符: {sum(l['char_count'] for l in libs)} 个")
    print(f"\n📡 路由: / | /fonts | /libs | /preview/<ver> | /download/<file> | /health | /stats")

    app.run(host='0.0.0.0', port=8081, debug=True)
