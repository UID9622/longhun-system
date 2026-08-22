# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-b5be892d
#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
龍魂视频工坊 · 索引生成器 v1.0
================================================================================
扫描 videos/ 目录下所有 JSON 元数据，生成统一的视频索引文件
供前端画廊页面 + API 使用

DNA: #龍芯⚡️丙午·乙未·癸亥·戊午·䷖剥-VIDEO-INDEX-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

用法:
    python3 bin/lh_video_index.py                 # 生成 index.json
    python3 bin/lh_video_index.py --watch         # 持续监听（开发用）
    python3 bin/lh_video_index.py --serve :8788   # 启动画廊API

输出:
    videos/index.json         # 视频索引
    portal/video-studio/      # 画廊页面（静态引用index.json）

依赖:
    - Python 3.9+
    - http.server (标准库)
================================================================================
"""

import os
import sys
import json
import time
import hashlib
import urllib.parse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIDEO_DIR = PROJECT_ROOT / "videos"
INDEX_PATH = VIDEO_DIR / "index.json"
PORTAL_DIR = PROJECT_ROOT / "portal" / "video-studio"


def scan_videos() -> List[Dict]:
    """扫描 videos/ 目录，读取所有 JSON 元数据"""
    videos = []

    if not VIDEO_DIR.exists():
        return videos

    for json_file in sorted(VIDEO_DIR.glob("*.json"), reverse=True):
        if json_file.name == "index.json":
            continue

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                meta = json.load(f)
        except (json.JSONDecodeError, IOError):
            continue

        # 检查对应的 mp4 文件是否存在
        mp4_path = json_file.with_suffix('.mp4')
        if not mp4_path.exists():
            continue

        # 获取文件信息
        stat = mp4_path.stat()
        file_md5 = hashlib.md5(mp4_path.read_bytes()[:8192]).hexdigest()[:12]

        video_info = {
            "id": json_file.stem,
            "title": extract_title(json_file.stem, meta.get("style", "")),
            "style": meta.get("style", "默认"),
            "dna": meta.get("dna", ""),
            "scenes": meta.get("scenes", []),
            "total_scenes": meta.get("total_scenes", len(meta.get("scenes", []))),
            "total_duration": round(meta.get("total_duration", 0), 1),
            "duration_str": format_duration(meta.get("total_duration", 0)),
            "resolution": meta.get("resolution", "1920x1080"),
            "voice": meta.get("voice", ""),
            "generated_at": meta.get("generated_at", ""),
            "generator": meta.get("generator", "龍魂视频工坊"),
            "uid": meta.get("uid", "UID9622"),
            # 文件信息
            "file_name": mp4_path.name,
            "file_size": stat.st_size,
            "file_size_mb": round(stat.st_size / (1024 * 1024), 2),
            "file_md5": file_md5,
            "video_path": f"/videos/{mp4_path.name}",
            "json_path": f"/videos/{json_file.name}",
        }
        # 叠加互动指标
        metrics = _load_metrics()
        video_info["metrics"] = _video_metrics_summary(metrics, video_info["id"])
        videos.append(video_info)

    return videos


def extract_title(filename: str, style: str) -> str:
    """从文件名提取标题"""
    # 格式: {名称}_{风格}_{时间戳}
    parts = filename.rsplit('_', 2)
    if len(parts) >= 3:
        return parts[0]
    return filename


def format_duration(seconds: float) -> str:
    """格式化时长"""
    if seconds < 60:
        return f"{seconds:.0f}秒"
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}分{secs}秒"


def generate_index() -> Dict:
    """生成视频索引"""
    videos = scan_videos()

    # 统计
    styles = {}
    total_duration = 0
    for v in videos:
        s = v["style"]
        styles[s] = styles.get(s, 0) + 1
        total_duration += v["total_duration"]

    index = {
        "generated_at": datetime.now().isoformat(),
        "generator": "龍魂视频工坊 · 索引引擎 v1.0",
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-VIDEO-INDEX-v1.0",
        "total_videos": len(videos),
        "total_duration": round(total_duration, 1),
        "total_duration_str": format_duration(total_duration),
        "styles": styles,
        "videos": videos,
    }

    # 写入索引文件
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    return index


# =============================================================================
# Metrics & Comments
# =============================================================================

METRICS_PATH = VIDEO_DIR / "metrics.json"


def _load_metrics() -> Dict:
    """加载视频互动数据（浏览/下载/转发/评论）。"""
    if not METRICS_PATH.exists():
        return {
            "videos": {},
            "totals": {"views": 0, "downloads": 0, "shares": 0, "comments": 0, "videos": 0},
            "daily": {},
            "updated_at": datetime.now().isoformat(),
        }
    try:
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "videos": {},
            "totals": {"views": 0, "downloads": 0, "shares": 0, "comments": 0, "videos": 0},
            "daily": {},
            "updated_at": datetime.now().isoformat(),
        }


def _save_metrics(metrics: Dict):
    """保存互动数据。"""
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    metrics["updated_at"] = datetime.now().isoformat()
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)


def _ensure_video_metrics(metrics: Dict, video_id: str) -> Dict:
    """确保单个视频有指标容器。"""
    if video_id not in metrics["videos"]:
        metrics["videos"][video_id] = {
            "views": 0,
            "downloads": 0,
            "shares": 0,
            "comments": [],
            "comments_count": 0,
            "generated_count": 0,
        }
    return metrics["videos"][video_id]


def _bump(metrics: Dict, video_id: str, field: str):
    """增加一次互动计数（views/downloads/shares/comments）。"""
    vm = _ensure_video_metrics(metrics, video_id)
    if field == "comments":
        vm["comments_count"] = vm.get("comments_count", 0) + 1
    else:
        vm[field] = vm.get(field, 0) + 1
    now = datetime.now()
    vm[f"last_{field}_at"] = now.isoformat()
    metrics["totals"][field] = metrics["totals"].get(field, 0) + 1
    day = now.strftime("%Y-%m-%d")
    metrics["daily"].setdefault(day, {"views": 0, "downloads": 0, "shares": 0, "comments": 0, "videos": 0})
    metrics["daily"][day][field] = metrics["daily"][day].get(field, 0) + 1


def _record_generation(metrics: Dict, video_id: str):
    """记录一次视频生成。"""
    vm = _ensure_video_metrics(metrics, video_id)
    vm["generated_count"] = vm.get("generated_count", 0) + 1
    now = datetime.now()
    vm["generated_at"] = now.isoformat()
    metrics["totals"]["videos"] = metrics["totals"].get("videos", 0) + 1
    day = now.strftime("%Y-%m-%d")
    metrics["daily"].setdefault(day, {"views": 0, "downloads": 0, "shares": 0, "comments": 0, "videos": 0})
    metrics["daily"][day]["videos"] = metrics["daily"][day].get("videos", 0) + 1


def _classify_comment(content: str, client_id: str, metrics: Dict) -> str:
    """简单水军识别：重复内容 / 过短 / 同一客户端高频。"""
    content = content.strip()
    if len(content) < 3:
        return "疑似水军（无意义）"
    normalized = content.lower()
    repeats = 0
    for vid, vm in metrics.get("videos", {}).items():
        for c in vm.get("comments", []):
            if c.get("content", "").strip().lower() == normalized:
                repeats += 1
    if repeats >= 2:
        return "疑似水军（重复内容）"
    # 同一客户端 1 小时内超过 3 条
    try:
        hour_ago = datetime.now().timestamp() - 3600
        recent = 0
        for vid, vm in metrics.get("videos", {}).items():
            for c in vm.get("comments", []):
                if c.get("client_id") == client_id:
                    t = datetime.fromisoformat(c.get("created_at", "2000-01-01T00:00:00")).timestamp()
                    if t > hour_ago:
                        recent += 1
        if recent > 3:
            return "疑似水军（高频）"
    except Exception:
        pass
    return "真实用户"


def _add_comment(metrics: Dict, video_id: str, payload: Dict, client_id: str) -> Dict:
    """添加一条评论并返回。"""
    vm = _ensure_video_metrics(metrics, video_id)
    content = payload.get("content", "").strip()
    if not content:
        raise ValueError("评论内容不能为空")
    nickname = payload.get("nickname", "").strip() or "匿名"
    source = payload.get("source", "").strip()
    allowed = ("真实用户", "匿名游客", "系统", "测试")
    if not source or source not in allowed:
        source = _classify_comment(content, client_id, metrics)
    comment = {
        "id": hashlib.md5(f"{client_id}{time.time()}{content}".encode()).hexdigest()[:12],
        "nickname": nickname,
        "content": content,
        "source": source,
        "client_id": client_id,
        "created_at": datetime.now().isoformat(),
    }
    vm["comments"].append(comment)
    _bump(metrics, video_id, "comments")
    return comment


def _video_metrics_summary(metrics: Dict, video_id: str) -> Dict:
    """单个视频的指标摘要。"""
    vm = _ensure_video_metrics(metrics, video_id)
    return {
        "views": vm.get("views", 0),
        "downloads": vm.get("downloads", 0),
        "shares": vm.get("shares", 0),
        "comments_count": vm.get("comments_count", len(vm.get("comments", []))),
        "generated_count": vm.get("generated_count", 0),
        "last_viewed_at": vm.get("last_viewed_at", ""),
        "last_downloaded_at": vm.get("last_downloaded_at", ""),
        "last_shared_at": vm.get("last_shared_at", ""),
    }


def _recent_comments(metrics: Dict, limit: int = 20) -> List[Dict]:
    """聚合最近的评论。"""
    all_comments = []
    for vid, vm in metrics.get("videos", {}).items():
        for c in vm.get("comments", []):
            all_comments.append({**c, "video_id": vid})
    all_comments.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return all_comments[:limit]


def get_system_metrics() -> Dict:
    """供图表使用的系统级指标。"""
    index = generate_index()
    metrics = _load_metrics()

    by_date = {}
    for v in index["videos"]:
        d = v.get("generated_at", "")[:10]
        if d:
            by_date[d] = by_date.get(d, 0) + 1

    daily_sorted = sorted(metrics.get("daily", {}).items())

    top = []
    for v in index["videos"]:
        vm = metrics["videos"].get(v["id"], {})
        top.append({
            "id": v["id"],
            "title": v["title"],
            "views": vm.get("views", 0),
            "downloads": vm.get("downloads", 0),
            "shares": vm.get("shares", 0),
            "comments_count": len(vm.get("comments", [])),
        })
    top.sort(key=lambda x: -x["views"])

    return {
        "videos": {
            "total": index["total_videos"],
            "total_duration": index["total_duration_str"],
            "by_style": index.get("styles", {}),
            "by_date": by_date,
        },
        "engagement": metrics.get("totals", {}),
        "daily": [
            {"date": d, "views": v.get("views", 0), "downloads": v.get("downloads", 0),
             "shares": v.get("shares", 0), "comments": v.get("comments", 0),
             "videos": v.get("videos", 0)}
            for d, v in daily_sorted
        ],
        "top_videos": top[:10],
        "recent_comments": _recent_comments(metrics, 20),
        "updated_at": metrics.get("updated_at", ""),
    }


def print_summary(index: Dict):
    """打印摘要"""
    print(f"""
╔══════════════════════════════════════════╗
║     龍魂视频工坊 · 索引报告            ║
╠══════════════════════════════════════════╣
║  视频总数:  {index['total_videos']:<3}                        ║
║  总时长:    {index['total_duration_str']:<12}              ║
║  风格分布:                              ║""")
    for style, count in index.get("styles", {}).items():
        print(f"║    {style}: {count} 部{'':<20}║")
    print(f"""║  索引文件:  videos/index.json            ║
╚══════════════════════════════════════════╝""")

    for v in index.get("videos", []):
        print(f"  🎬 {v['title']} [{v['style']}] {v['duration_str']} | DNA: {v['dna'][:50]}...")


def serve_gallery(host: str = "0.0.0.0", port: int = 8788):
    """启动视频画廊 HTTP 服务"""
    import http.server
    import socketserver
    import subprocess as sp
    import threading

    class GalleryHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(PROJECT_ROOT), **kwargs)

        def log_message(self, format, *args):
            print(f"  {args[0]}")

        def _json_response(self, data, status=200):
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

        def _read_body(self) -> bytes:
            content_length = int(self.headers.get('Content-Length', 0))
            return self.rfile.read(content_length)

        def do_GET(self):
            # API: /api/videos (list all)
            if self.path == "/api/videos":
                index = generate_index()
                return self._json_response(index)

            # API: /api/metrics (system-wide metrics for charts)
            if self.path == "/api/metrics":
                return self._json_response(get_system_metrics())

            # API: /api/videos/... (detail / comments)
            if self.path.startswith("/api/videos/"):
                rest = self.path[len("/api/videos/"):]
                if "/" in rest:
                    video_id, action = urllib.parse.unquote(rest).split("/", 1)
                    if action == "comments":
                        metrics = _load_metrics()
                        vm = _ensure_video_metrics(metrics, video_id)
                        return self._json_response({
                            "comments": vm.get("comments", []),
                            "comments_count": vm.get("comments_count", len(vm.get("comments", []))),
                        })
                    return self._json_response({"error": "unknown action"}, 404)
                else:
                    video_id = urllib.parse.unquote(rest)
                    index = generate_index()
                    for v in index["videos"]:
                        if v["id"] == video_id:
                            return self._json_response(v)
                    return self._json_response({"error": "not found"}, 404)

            # 静态文件服务（videos/, portal/）
            return super().do_GET()

        def do_POST(self):
            # API: POST /api/videos/generate
            if self.path == "/api/videos/generate":
                body = self._read_body()
                try:
                    params = json.loads(body)
                except json.JSONDecodeError:
                    return self._json_response({"success": False, "error": "JSON解析失败"}, 400)

                script = params.get("script", "").strip()
                name = params.get("name", "龍魂视频").strip()
                style = params.get("style", "龍魂").strip()

                if len(script) < 10:
                    return self._json_response({"success": False, "error": "文本至少10个字"}, 400)

                # 调用 video studio CLI（后台执行）
                bin_dir = PROJECT_ROOT / "bin"
                cmd = [
                    sys.executable,
                    str(bin_dir / "lh_video_studio.py"),
                    "--script", script,
                    "--name", name,
                    "--style", style,
                ]

                try:
                    result = sp.run(cmd, capture_output=True, text=True, timeout=300, cwd=str(PROJECT_ROOT))
                    if result.returncode == 0:
                        # 刷新索引并记录生成
                        index = generate_index()
                        new_video = index["videos"][0] if index["videos"] else None
                        if new_video:
                            metrics = _load_metrics()
                            _record_generation(metrics, new_video["id"])
                            _save_metrics(metrics)
                        return self._json_response({
                            "success": True,
                            "title": name,
                            "id": new_video["id"] if new_video else "",
                            "output": result.stdout.strip().split('\n')[-5:]
                        })
                    else:
                        return self._json_response({
                            "success": False,
                            "error": result.stderr.strip()[-500:] or "生成失败"
                        }, 500)
                except sp.TimeoutExpired:
                    return self._json_response({"success": False, "error": "生成超时（5分钟）"}, 504)
                except Exception as e:
                    return self._json_response({"success": False, "error": str(e)}, 500)

            # API: /api/videos/:id/{view,download,share,comments}
            if self.path.startswith("/api/videos/"):
                rest = self.path[len("/api/videos/"):]
                if "/" in rest:
                    video_id, action = urllib.parse.unquote(rest).split("/", 1)
                    metrics = _load_metrics()

                    if action == "view":
                        _bump(metrics, video_id, "views")
                        _save_metrics(metrics)
                        return self._json_response({"ok": True, "views": metrics["videos"][video_id]["views"]})

                    if action == "download":
                        _bump(metrics, video_id, "downloads")
                        _save_metrics(metrics)
                        return self._json_response({"ok": True, "downloads": metrics["videos"][video_id]["downloads"]})

                    if action == "share":
                        _bump(metrics, video_id, "shares")
                        _save_metrics(metrics)
                        return self._json_response({"ok": True, "shares": metrics["videos"][video_id]["shares"]})

                    if action == "comments":
                        body = self._read_body()
                        try:
                            payload = json.loads(body)
                        except json.JSONDecodeError:
                            return self._json_response({"error": "JSON解析失败"}, 400)
                        client_id = self.headers.get('X-Client-Id', '') or payload.get('client_id', '')
                        if not client_id:
                            import uuid
                            client_id = "anon-" + uuid.uuid4().hex[:8]
                        try:
                            comment = _add_comment(metrics, video_id, payload, client_id)
                            _save_metrics(metrics)
                            return self._json_response({"ok": True, "comment": comment})
                        except ValueError as e:
                            return self._json_response({"error": str(e)}, 400)

                    return self._json_response({"error": "unknown action"}, 404)

            # 未知 POST 端点
            return self._json_response({"error": "not found"}, 404)

        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

    with socketserver.TCPServer((host, port), GalleryHandler) as httpd:
        gallery_url = f"http://localhost:{port}/portal/video-studio/"
        print(f"""
╔══════════════════════════════════════════╗
║  龍魂视频工坊 · 画廊服务已启动          ║
╠══════════════════════════════════════════╣
║  🎬 画廊:  {gallery_url:<30}║
║  📡 API:   http://localhost:{port}/api/videos{'':<21}║
║  📁 视频:  http://localhost:{port}/videos/{'':<22}║
║  🛑 退出:  Ctrl+C                         ║
╚══════════════════════════════════════════╝
""")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 画廊服务已停止")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="龍魂视频工坊 · 索引生成器")
    parser.add_argument("--serve", default=None, help="启动画廊服务，如 :8788")
    parser.add_argument("--watch", action="store_true", help="持续监听（开发用）")
    parser.add_argument("--summary", action="store_true", help="只打印摘要")
    args = parser.parse_args()

    if args.serve:
        port = int(args.serve.replace(":", "")) if args.serve.startswith(":") else 8788
        serve_gallery(port=port)
    elif args.watch:
        print("👁️  监听 videos/ 目录变化... (Ctrl+C 退出)")
        last_count = 0
        while True:
            index = generate_index()
            if index["total_videos"] != last_count:
                last_count = index["total_videos"]
                print_summary(index)
            time.sleep(5)
    else:
        index = generate_index()
        print_summary(index)
