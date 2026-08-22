#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·视频素材自动化清洗引擎 v1.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-VIDEO-CLEANER-V1.0-9a1b2c3d
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

一体化管线: Notion拉取 → 下载 → 帧提取(ffmpeg) → 感知哈希去重 → 
            模糊/亮度过滤 → 自动打标 → 入库 → Notion状态回写

依赖: ffmpeg, Pillow, imagehash, numpy (可选 requests, notion-client)
无OpenCV依赖 — ffmpeg提取帧 + PIL分析图像
"""

import os, sys, json, re, time, hashlib, argparse, subprocess, shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
from PIL import Image, ImageStat
import imagehash

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MATERIAL_DB_PATH = PROJECT_ROOT / "data" / "material_library.db"
VIDEO_CACHE_DIR = PROJECT_ROOT / "data" / "video_cache"
FRAME_OUTPUT_DIR = PROJECT_ROOT / "data" / "scene_library"
LOG_DIR = PROJECT_ROOT / "logs"

# ══════════════════════════════════════════════════════════════════════
# 配置
# ══════════════════════════════════════════════════════════════════════

EXTRACT_INTERVAL_SEC = 1.0        # 帧提取间隔（秒）
SCENE_DETECT_THRESHOLD = 0.35     # 场景切换阈值（感知哈希差异）
SIMILARITY_THRESHOLD = 0.93       # 去重阈值（>此值视为重复）
BLUR_THRESHOLD = 80.0             # 拉普拉斯方差阈值（<此值视为模糊）
MIN_BRIGHTNESS = 15               # 最低平均亮度
MAX_BRIGHTNESS = 245              # 最高平均亮度
MIN_FRAME_DIM = 100               # 最小帧尺寸
JPEG_QUALITY = 85                 # 输出JPEG质量

# Notion 字段映射（按实际列名修改）
NOTION_FIELD_VIDEO_URL = "视频链接"
NOTION_FIELD_NAME = "名称"
NOTION_FIELD_TAGS = "标签"
NOTION_FIELD_STATUS = "状态"
NOTION_FIELD_FRAMES = "提取帧数"

VIDEO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
FRAME_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# ══════════════════════════════════════════════════════════════════════
# 帧提取 (ffmpeg)
# ══════════════════════════════════════════════════════════════════════

def get_video_info(video_path: Path) -> dict:
    """ffprobe 获取视频信息"""
    try:
        result = subprocess.run([
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_format', '-show_streams', str(video_path)
        ], capture_output=True, text=True, timeout=15)
        if result.returncode != 0:
            return {}
        data = json.loads(result.stdout)
        
        video_stream = None
        for s in data.get('streams', []):
            if s.get('codec_type') == 'video':
                video_stream = s
                break
        
        if not video_stream:
            return {}
        
        duration = float(data.get('format', {}).get('duration', 0))
        return {
            'duration': duration,
            'width': int(video_stream.get('width', 0)),
            'height': int(video_stream.get('height', 0)),
            'fps': eval(video_stream.get('r_frame_rate', '0/1')),
            'codec': video_stream.get('codec_name', 'unknown'),
            'bitrate': int(data.get('format', {}).get('bit_rate', 0)) // 1000,
        }
    except Exception as e:
        print(f"  ⚠️ ffprobe失败: {e}")
        return {}


def extract_frames_ffmpeg(video_path: Path, output_dir: Path, 
                           interval: float = EXTRACT_INTERVAL_SEC,
                           scene_threshold: float = SCENE_DETECT_THRESHOLD) -> List[Path]:
    """
    ffmpeg 帧提取: 均匀采样 + 场景切换过滤
    两步:
    1. 按间隔提取关键帧 (fps=1/interval)
    2. 可选: 用 select='gt(scene,threshold)' 补关键帧
    """
    video_name = video_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    frames = []
    
    # Step 1: 均匀采样
    output_pattern = str(output_dir / f"{video_name}_%06d.jpg")
    
    cmd = [
        'ffmpeg', '-y', '-loglevel', 'error',
        '-i', str(video_path),
        '-vf', f'fps=1/{interval}',
        '-q:v', str(max(2, min(31, 31 - JPEG_QUALITY // 4))),
        '-frames:v', str(10**6),
        output_pattern
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0 and result.stderr:
        print(f"  ⚠️ ffmpeg均匀采样: {result.stderr[:200]}")
    
    # 收集均匀采样帧
    uniform_frames = sorted(output_dir.glob(f"{video_name}_*.jpg"))
    frames.extend(uniform_frames)
    
    if not frames:
        # 回退: 只取第一帧
        thumb_path = output_dir / f"{video_name}_thumb.jpg"
        cmd2 = [
            'ffmpeg', '-y', '-loglevel', 'error',
            '-i', str(video_path),
            '-vframes', '1', '-q:v', '2',
            str(thumb_path)
        ]
        subprocess.run(cmd2, capture_output=True, timeout=15)
        if thumb_path.exists():
            frames.append(thumb_path)
    
    # Step 2: 场景切换检测补帧 (如果帧数太少)
    if len(frames) < 5:
        scene_pattern = str(output_dir / f"{video_name}_scene_%06d.jpg")
        cmd3 = [
            'ffmpeg', '-y', '-loglevel', 'error',
            '-i', str(video_path),
            '-vf', f"select='gt(scene\\,{scene_threshold})'",
            '-vsync', 'vfr', '-q:v', '2',
            scene_pattern
        ]
        subprocess.run(cmd3, capture_output=True, timeout=60)
        scene_frames = sorted(output_dir.glob(f"{video_name}_scene_*.jpg"))
        frames.extend(scene_frames)
    
    return sorted(set(frames))


# ══════════════════════════════════════════════════════════════════════
# 清洗: 感知哈希去重 + 模糊检测 + 亮度过滤
# ══════════════════════════════════════════════════════════════════════

def laplacian_variance_pil(img: Image.Image) -> float:
    """PIL 近似拉普拉斯方差 (无OpenCV)"""
    gray = img.convert('L')
    arr = np.array(gray, dtype=np.float64)
    
    # 简单拉普拉斯核卷积: [0,1,0][1,-4,1][0,1,0]
    h, w = arr.shape
    if h < 3 or w < 3:
        return 0.0
    
    lap = np.zeros_like(arr)
    lap[1:-1, 1:-1] = (
        arr[0:-2, 1:-1] + arr[2:, 1:-1] + 
        arr[1:-1, 0:-2] + arr[1:-1, 2:] - 
        4 * arr[1:-1, 1:-1]
    )
    return float(np.var(lap))


def compute_frame_metrics(img: Image.Image) -> dict:
    """计算帧的多维度指标"""
    w, h = img.size
    gray = img.convert('L')
    arr = np.array(gray, dtype=np.float64)
    
    metrics = {
        'width': w, 'height': h,
        'brightness': float(np.mean(arr)),
        'std': float(np.std(arr)),
        'sharpness': laplacian_variance_pil(img),
        'phash': str(imagehash.phash(img)),
        'dhash': str(imagehash.dhash(img)),
        'ahash': str(imagehash.average_hash(img)),
    }
    return metrics


def clean_frames(frame_paths: List[Path], existing_hashes: List[str] = None
                 ) -> Tuple[List[Dict], List[Path]]:
    """
    多级清洗管道:
    1. 感知哈希去重 (vs 已入库 + vs 同批次)
    2. 模糊检测 (拉普拉斯方差)
    3. 亮度异常过滤
    4. 尺寸过滤
    
    返回: (保留的帧元信息, 被删除的路径)
    """
    if existing_hashes is None:
        existing_hashes = []
    
    kept_meta = []
    removed = []
    seen_hashes = set(existing_hashes)
    
    for fp in frame_paths:
        if not fp.exists():
            continue
        
        try:
            img = Image.open(fp)
            
            # 尺寸检查
            if img.width < MIN_FRAME_DIM or img.height < MIN_FRAME_DIM:
                fp.unlink()
                removed.append(fp)
                continue
            
            # 转为 RGB (处理 RGBA/P 模式)
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # 指标计算
            m = compute_frame_metrics(img)
            
            # 去重检查
            ph = m['phash']
            is_duplicate = False
            for sh in seen_hashes:
                if _hash_similar(ph, sh, SIMILARITY_THRESHOLD):
                    is_duplicate = True
                    break
            
            if is_duplicate:
                fp.unlink()
                removed.append(fp)
                continue
            
            # 模糊检测
            if m['sharpness'] < BLUR_THRESHOLD:
                fp.unlink()
                removed.append(fp)
                continue
            
            # 亮度过滤
            b = m['brightness']
            if b < MIN_BRIGHTNESS or b > MAX_BRIGHTNESS:
                fp.unlink()
                removed.append(fp)
                continue
            
            # 通过! 保留
            seen_hashes.add(ph)
            m['path'] = str(fp)
            m['filename'] = fp.name
            kept_meta.append(m)
            
        except Exception as e:
            print(f"    ⚠️ 帧处理异常 {fp.name}: {e}")
            removed.append(fp)
    
    return kept_meta, removed


def _hash_similar(h1: str, h2: str, threshold: float) -> bool:
    """比较两个十六进制哈希字符串的相似度"""
    if len(h1) != len(h2):
        return False
    # Hamming距离
    try:
        n1 = int(h1, 16)
        n2 = int(h2, 16)
        diff = bin(n1 ^ n2).count('1')
        max_bits = len(h1) * 4
        return (1 - diff / max_bits) >= threshold
    except:
        return False


# ══════════════════════════════════════════════════════════════════════
# 启发式自动打标 (帧级)
# ══════════════════════════════════════════════════════════════════════

def infer_frame_tags(metrics: dict, video_name: str = '', 
                     notion_tags: str = '') -> dict:
    """
    从帧属性推断场景标签
    8步规则 (复用 material_tagger 逻辑, 帧级适配)
    """
    tags = []
    content_type = 'video_frame'
    emotion = 'neutral'
    style = 'medium'
    suggested_use = '过渡画面'
    
    w, h = metrics.get('width', 0), metrics.get('height', 0)
    b = metrics.get('brightness', 128)
    s = metrics.get('sharpness', 0)
    std = metrics.get('std', 0)
    
    # 1. 宽高比判断
    if w > 0 and h > 0:
        ratio = w / h
        if ratio > 1.6:
            suggested_use = '背景画面'
            tags.append('横屏')
        elif ratio < 0.7:
            tags.append('竖屏')
        elif 1.2 < ratio < 1.5:
            tags.append('标准画幅')
    
    # 2. 亮度推断
    if b < 60:
        style = '暗色'
        tags.append('暗色调')
        emotion = '严肃'
    elif b > 200:
        style = '明亮'
        tags.append('明亮')
        emotion = '平和'
    elif 60 <= b <= 120:
        style = '暗色'
        tags.append('中低调')
    else:
        style = '中等'
    
    # 3. 锐度推断
    if s > 500:
        tags.append('高锐度')
        quality_note = '可用'
    elif s < BLUR_THRESHOLD:
        quality_note = '低质量'
    else:
        quality_note = '可用'
    
    # 4. 纹理复杂度 (std)
    if std < 30:
        tags.append('低纹理')
        content_type = 'simple_bg'
    elif std > 80:
        tags.append('高纹理')
        content_type = 'detail_scene'
    
    # 5. 视频名关键词
    name_lower = video_name.lower()
    kw_map = {
        'code': (['代码', '技术'], '技术教学', '分析'),
        '编程': (['代码', '编程'], '技术教学', '分析'),
        'tech': (['技术'], '技术教学', '分析'),
        'culture': (['文化', '传统'], '文化传承', '庄严'),
        '易经': (['易经', '哲学'], '文化传承', '庄严'),
        'history': (['历史'], '文化传承', '庄严'),
        'tutorial': (['教学'], '技术教学', '平和'),
        'nature': (['自然', '风景'], '创意设计', '温暖'),
        'music': (['音乐'], '创意设计', '激励'),
        'data': (['数据', '图表'], '数据图表', '分析'),
        'news': (['新闻', '时事'], '证据记录', '严肃'),
        '龍': (['龍魂', '中国'], '文化传承', '庄严'),
        '龍魂': (['龍魂', '数字主权'], '文化传承', '庄严'),
    }
    for kw, (kwtags, ct, em) in kw_map.items():
        if kw in name_lower:
            tags.extend(kwtags)
            content_type = ct
            emotion = em
            break
    
    # 6. Notion标签附加
    if notion_tags:
        for t in notion_tags.split(','):
            t = t.strip()
            if t and t not in tags:
                tags.append(t)
    
    # 7. 质量评分 (0-1)
    quality = 0.7
    if s > 500:
        quality += 0.15
    if 80 < b < 200:
        quality += 0.1
    if std > 50:
        quality += 0.05
    if quality > 1.0:
        quality = 1.0
    
    return {
        'tags': list(set(tags)),
        'content_type': content_type,
        'emotion': emotion,
        'visual_style': f"{style}{'科技' if 'tech' in name_lower or 'code' in name_lower else ''}",
        'suggested_use': suggested_use,
        'quality_score': round(quality, 2),
        'quality_note': quality_note,
    }


# ══════════════════════════════════════════════════════════════════════
# 入库 + 场景组织
# ══════════════════════════════════════════════════════════════════════

def _compute_file_hash(filepath: Path) -> str:
    """SHA-256 前 16 字符 (与 scanner 一致)"""
    h = hashlib.sha256()
    with open(filepath, 'rb') as fh:
        for chunk in iter(lambda: fh.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()[:16]


def _guess_content_type(filename: str, tags: list, video_name: str) -> str:
    """从文件名/视频名/tag 推断内容类型"""
    combined = f"{filename} {video_name} {' '.join(tags)}".lower()
    type_map = [
        (['code', '编程', '代码', '技术', 'tech', '架构', 'architecture', 'topology'], 'code'),
        (['culture', '文化', '易经', '道德经', '哲学', '传统', 'history', '龍魂', '龍'], 'culture'),
        (['security', '安全', '漏洞', '防护', '审计', 'attack', 'defense'], 'security'),
        (['deploy', '部署', '上线', 'server', '服务器', 'docker', 'k8s'], 'deploy'),
        (['evidence', '证据', '记录', 'screenshot', '截图', 'capture'], 'evidence'),
        (['data', '数据', '统计', '图表', 'chart', 'graph'], 'data'),
        (['ai', '人格', '模型', '智能', 'persona', 'brain', 'neural'], 'persona'),
        (['creative', '创意', '设计', 'art', 'drawing', 'paint'], 'creative'),
        (['life', '生活', 'daily', '日常', 'photo', 'img_'], 'life'),
    ]
    for keywords, ct in type_map:
        if any(kw in combined for kw in keywords):
            return ct
    return 'video_frame'


def import_frames_to_library(frames: List[Dict], video_name: str, 
                              source_type: str = 'video_frame') -> int:
    """将清洗后的帧导入素材库 SQLite (对齐 scanner 的 schema)"""
    import sqlite3
    
    conn = sqlite3.connect(str(MATERIAL_DB_PATH))
    conn.row_factory = sqlite3.Row
    imported = 0
    skipped = 0
    
    for f in frames:
        fp = Path(f['path'])
        if not fp.exists():
            continue
        
        w, h = f.get('width', 0), f.get('height', 0)
        tag_info = f.get('tag_info', {})
        tags_list = tag_info.get('tags', [])
        content_type = _guess_content_type(f.get('filename', ''), tags_list, video_name)
        emotion = tag_info.get('emotion', 'neutral')
        
        # 计算 file_hash (scanner 的 NOT NULL 列)
        fhash = _compute_file_hash(fp)
        
        # 检查重复 (同 hash 同 material)
        existing = conn.execute(
            "SELECT id FROM materials WHERE file_hash = ? AND filename = ?",
            (fhash, fp.name)
        ).fetchone()
        
        if existing:
            skipped += 1
            continue
        
        material_id = f"vf_{fhash}_{imported:04d}"
        
        tags_json = json.dumps(tags_list, ensure_ascii=False)
        colors_json = json.dumps([], ensure_ascii=False)
        subtypes_json = json.dumps([], ensure_ascii=False)
        notes_json = json.dumps({
            'source': 'video_frame_extraction',
            'video_name': video_name,
            'sharpness': f.get('sharpness', 0),
            'phash': f.get('phash', ''),
            'dhash': f.get('dhash', ''),
            'std': f.get('std', 0),
            'suggested_use': tag_info.get('suggested_use', ''),
            'quality_note': tag_info.get('quality_note', ''),
            'extracted_at': datetime.now().isoformat(),
        }, ensure_ascii=False)
        
        brightness_level = 'dark' if f.get('brightness', 128) < 80 else (
            'bright' if f.get('brightness', 128) > 180 else 'mid'
        )
        
        aspect = round(w / h, 3) if h else 0
        is_portrait = 1 if h > w else 0
        
        # 完全对齐 scanner 的 INSERT 列
        conn.execute("""
            INSERT OR IGNORE INTO materials 
            (material_id, filepath, filename, ext, media_type, file_hash,
             created_at, scanned_at, width, height, aspect_ratio, mode,
             is_portrait, is_screenshot, dominant_colors, brightness,
             content_type, content_subtypes, emotion, source_type,
             quality_score, tags, notes)
            VALUES (?, ?, ?, ?, 'image', ?, ?, ?, ?, ?, ?, 'RGB', ?, 0, ?, ?,
                    ?, ?, ?, ?, ?, ?, ?)
        """, (
            material_id, str(fp.absolute()), fp.name, fp.suffix,
            fhash, datetime.now().isoformat(), datetime.now().isoformat(),
            w, h, aspect,
            is_portrait, colors_json, brightness_level,
            content_type, subtypes_json, emotion, source_type,
            tag_info.get('quality_score', 0.6), tags_json, notes_json
        ))
        imported += 1
    
    conn.commit()
    conn.close()
    
    if skipped:
        print(f"  🔄 跳过 {skipped} 帧 (已存在)")
    return imported


def organize_scenes(frames: List[Dict], video_name: str) -> Path:
    """组织场景库目录"""
    safe_name = re.sub(r'[^\w\-_]', '_', video_name)
    scene_dir = FRAME_OUTPUT_DIR / safe_name
    scene_dir.mkdir(parents=True, exist_ok=True)
    
    # 移动帧文件到场景目录
    moved = 0
    for f in frames:
        src = Path(f['path'])
        if src.parent != scene_dir:
            dst = scene_dir / src.name
            shutil.move(str(src), str(dst))
            f['path'] = str(dst)
            moved += 1
    
    # 生成索引 JSON
    index = {
        'video_name': video_name,
        'processed_at': datetime.now().isoformat(),
        'total_frames': len(frames),
        'frames': [
            {k: v for k, v in f.items() if k != 'tag_info'} 
            for f in frames
        ],
    }
    
    index_path = scene_dir / f"{safe_name}_scenes.json"
    with open(index_path, 'w', encoding='utf-8') as f_out:
        json.dump(index, f_out, ensure_ascii=False, indent=2)
    
    if moved:
        print(f"  📂 帧文件已组织到: {scene_dir}")
    print(f"  📋 场景索引: {index_path}")
    
    return scene_dir


def load_existing_hashes() -> List[str]:
    """从素材库加载所有视频帧的 phash 列表 (按 source_type='video_frame' 查)"""
    if not MATERIAL_DB_PATH.exists():
        return []
    
    import sqlite3
    conn = sqlite3.connect(str(MATERIAL_DB_PATH))
    rows = conn.execute("""
        SELECT notes FROM materials 
        WHERE source_type = 'video_frame'
    """).fetchall()
    conn.close()
    
    hashes = []
    for (notes_str,) in rows:
        try:
            note = json.loads(notes_str) if notes_str else {}
            if note.get('phash'):
                hashes.append(note['phash'])
        except:
            pass
    
    return hashes


# ══════════════════════════════════════════════════════════════════════
# 主流程: 处理单个视频
# ══════════════════════════════════════════════════════════════════════

def process_video(video_path: Path, video_name: str = '', 
                  tags: str = '', interval: float = EXTRACT_INTERVAL_SEC,
                  skip_existing: bool = True) -> dict:
    """
    处理单个视频的完整管线
    
    返回: {
        'status': 'ok'/'error',
        'video_name': str,
        'total_extracted': int,
        'kept_frames': int,
        'removed_frames': int,
        'imported_to_library': int,
        'scene_dir': str,
        'duration': float,
    }
    """
    name = video_name or video_path.stem
    start_time = time.time()
    
    print(f"\n🎬 处理: {name}")
    print(f"   路径: {video_path}")
    
    # 1. 获取视频信息
    info = get_video_info(video_path)
    if info:
        print(f"   时长: {info['duration']:.1f}s | 分辨率: {info['width']}x{info['height']} "
              f"| 帧率: {info['fps']:.1f} | 编码: {info['codec']}")
    
    # 2. 提取帧
    safe_name = re.sub(r'[^\w\-_]', '_', name)
    frame_dir = VIDEO_CACHE_DIR / f"frames_{safe_name}_{int(time.time())}"
    print(f"   提取帧... (间隔 {interval}s)")
    
    frame_paths = extract_frames_ffmpeg(video_path, frame_dir, interval)
    print(f"   提取: {len(frame_paths)} 帧")
    
    if not frame_paths:
        print("   ❌ 无法提取帧")
        return {'status': 'error', 'error': 'no_frames_extracted', 'video_name': name}
    
    # 3. 清洗
    existing_hashes = load_existing_hashes() if skip_existing else []
    print(f"   清洗中... (已有 {len(existing_hashes)} 个已入库哈希)")
    
    kept_meta, removed = clean_frames(frame_paths, existing_hashes)
    print(f"   保留: {len(kept_meta)} 帧 | 删除: {len(removed)} 帧 "
          f"({len(frame_paths) - len(kept_meta) - len(removed)} 处理失败)")
    
    if not kept_meta:
        print("   ❌ 清洗后无有效帧")
        shutil.rmtree(frame_dir, ignore_errors=True)
        return {'status': 'error', 'error': 'no_valid_frames', 'video_name': name}
    
    # 4. 打标
    print(f"   自动打标: {len(kept_meta)} 帧...")
    for f in kept_meta:
        f['tag_info'] = infer_frame_tags(f, name, tags)
    
    # 统计标签分布
    tag_counts = {}
    for f in kept_meta:
        ct = f['tag_info'].get('content_type', 'unknown')
        tag_counts[ct] = tag_counts.get(ct, 0) + 1
    print(f"   场景分布: {tag_counts}")
    
    # 5. 入库
    imported = import_frames_to_library(kept_meta, name)
    print(f"   入库: {imported} 帧 → material_library.db")
    
    # 6. 组织场景
    scene_dir = organize_scenes(kept_meta, name)
    
    # 7. 清理临时目录
    shutil.rmtree(frame_dir, ignore_errors=True)
    
    elapsed = time.time() - start_time
    print(f"\n✅ {name} 完成 | 耗时 {elapsed:.1f}s | "
          f"保留 {len(kept_meta)} 帧 | 入库 {imported} 条 | 场景库: {scene_dir}")
    
    return {
        'status': 'ok',
        'video_name': name,
        'total_extracted': len(frame_paths),
        'kept_frames': len(kept_meta),
        'removed_frames': len(removed),
        'imported_to_library': imported,
        'filter_summary': {
            'duplicate': sum(1 for r in removed if str(r).startswith(str(frame_dir))),
            'blur': 0,  # 粗略统计
            'brightness': 0,
        },
        'scene_dir': str(scene_dir),
        'duration': info.get('duration', 0) if info else 0,
        'elapsed': round(elapsed, 1),
    }


# ══════════════════════════════════════════════════════════════════════
# 批量处理
# ══════════════════════════════════════════════════════════════════════

def process_batch(video_paths: List[Path], interval: float = EXTRACT_INTERVAL_SEC,
                  parallel: int = 1) -> List[dict]:
    """批量处理多个视频"""
    results = []
    
    if parallel <= 1:
        for vp in video_paths:
            if vp.exists():
                results.append(process_video(vp, interval=interval))
            else:
                print(f"⚠️ 跳过不存在的文件: {vp}")
    else:
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {}
            for vp in video_paths:
                if vp.exists():
                    f = executor.submit(process_video, vp, '', '', interval)
                    futures[f] = vp
            
            for f in as_completed(futures):
                try:
                    results.append(f.result())
                except Exception as e:
                    print(f"❌ 处理 {futures[f]} 异常: {e}")
                    results.append({'status': 'error', 'error': str(e)})
    
    return results


# ══════════════════════════════════════════════════════════════════════
# Notion 集成
# ══════════════════════════════════════════════════════════════════════

def update_notion_status(page_id: str, status: str, frames_count: int = 0,
                          token: str = None, database_id: str = None):
    """更新 Notion 条目处理状态"""
    token = token or os.environ.get('NOTION_TOKEN')
    if not token:
        print("  ⚠️ 无 Notion Token，跳过状态更新")
        return False
    
    try:
        import requests
        headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }
        
        props = {NOTION_FIELD_STATUS: {"select": {"name": status}}}
        if frames_count > 0:
            props[NOTION_FIELD_FRAMES] = {"number": frames_count}
        
        resp = requests.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=headers,
            json={"properties": props},
            timeout=10
        )
        if resp.status_code == 200:
            print(f"  ✅ Notion状态更新: {status} ({frames_count}帧)")
            return True
        else:
            print(f"  ⚠️ Notion更新失败: {resp.status_code}")
            return False
    except Exception as e:
        print(f"  ⚠️ Notion异常: {e}")
        return False


# ══════════════════════════════════════════════════════════════════════
# 下载辅助
# ══════════════════════════════════════════════════════════════════════

def download_video(url: str, dest_dir: Path = None) -> Optional[Path]:
    """下载视频到本地缓存"""
    if dest_dir is None:
        dest_dir = VIDEO_CACHE_DIR
    
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # 本地文件直接返回
    if not url.startswith(('http://', 'https://')):
        local_path = Path(url)
        if local_path.exists():
            return local_path
        return None
    
    # HTTP 下载
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    ext = '.mp4'
    for e in ['.mp4', '.mov', '.webm', '.avi', '.mkv']:
        if e in url.lower():
            ext = e
            break
    
    dest = dest_dir / f"dl_{url_hash}{ext}"
    if dest.exists() and dest.stat().st_size > 1024:
        print(f"  📥 已缓存: {dest}")
        return dest
    
    try:
        import requests
        print(f"  📥 下载: {url[:80]}...")
        resp = requests.get(url, stream=True, timeout=120)
        resp.raise_for_status()
        
        with open(dest, 'wb') as f:
            for chunk in resp.iter_content(8192):
                f.write(chunk)
        
        print(f"  ✅ 下载完成: {dest} ({dest.stat().st_size//1024}KB)")
        return dest
    except Exception as e:
        print(f"  ❌ 下载失败: {e}")
        return None


# ══════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='龍魂·视频素材自动化清洗引擎 v1.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh video-clean test                           # 用本地测试视频跑全管线
  lh video-clean process video.mp4              # 处理单个视频
  lh video-clean process "https://..." --name "教程01" --tags "技术,编程"
  lh video-clean batch videos/                  # 批量处理目录下所有视频
  lh video-clean stats                          # 素材库统计
  lh video-clean notion --token xxx --db xxx    # Notion拉取+处理
        """
    )
    
    sub = parser.add_subparsers(dest='command')
    
    # test — 用本地测试视频跑全管线
    p_test = sub.add_parser('test', help='用本地测试视频跑全管线')
    p_test.add_argument('--interval', '-i', type=float, default=1.0,
                        help='帧提取间隔(秒)')
    
    # process — 处理单个视频
    p_proc = sub.add_parser('process', help='处理单个视频')
    p_proc.add_argument('video', help='视频路径或URL')
    p_proc.add_argument('--name', '-n', help='视频名称')
    p_proc.add_argument('--tags', '-t', default='', help='逗号分隔的标签')
    p_proc.add_argument('--interval', '-i', type=float, default=1.0,
                         help='帧提取间隔(秒)')
    
    # batch — 批量处理
    p_batch = sub.add_parser('batch', help='批量处理目录下所有视频')
    p_batch.add_argument('directory', help='视频目录')
    p_batch.add_argument('--interval', '-i', type=float, default=1.0,
                          help='帧提取间隔(秒)')
    p_batch.add_argument('--parallel', '-p', type=int, default=1,
                          help='并行处理数')
    
    # stats — 素材库统计
    p_stats = sub.add_parser('stats', help='素材库统计')
    
    # notion — Notion模式
    p_notion = sub.add_parser('notion', help='从Notion拉取并处理')
    p_notion.add_argument('--token', help='Notion API Token')
    p_notion.add_argument('--database', '--db', help='Notion Database ID')
    p_notion.add_argument('--interval', '-i', type=float, default=1.0,
                           help='帧提取间隔(秒)')
    
    args = parser.parse_args()
    
    if args.command == 'test':
        # 找本地测试视频
        test_video = PROJECT_ROOT / "data" / "training" / "media" / "videos" / "video_300849978796695.mp4"
        if not test_video.exists():
            # 搜索任意视频
            videos = list(PROJECT_ROOT.glob("data/**/*.mp4")) + list(PROJECT_ROOT.glob("data/**/*.mov"))
            if videos:
                test_video = videos[0]
        
        if not test_video or not test_video.exists():
            print("❌ 没找到测试视频，请用 'lh video-clean process <视频路径>' 指定")
            sys.exit(1)
        
        result = process_video(test_video, interval=args.interval)
        if result['status'] == 'ok':
            print(f"\n📊 总结: {result['video_name']}")
            print(f"   提取帧: {result['total_extracted']}")
            print(f"   保留: {result['kept_frames']} | 删除: {result['removed_frames']}")
            print(f"   入库: {result['imported_to_library']}")
            print(f"   清理率: {(1 - result['kept_frames']/max(1,result['total_extracted']))*100:.0f}%")
    
    elif args.command == 'process':
        video_input = args.video
        video_path = Path(video_input)
        
        # 尝试下载URL
        if video_input.startswith(('http://', 'https://')):
            video_path = download_video(video_input)
        
        if not video_path or not video_path.exists():
            print(f"❌ 视频不可访问: {video_input}")
            sys.exit(1)
        
        result = process_video(
            video_path, 
            video_name=args.name or '',
            tags=args.tags,
            interval=args.interval
        )
    
    elif args.command == 'batch':
        batch_dir = Path(args.directory)
        if not batch_dir.is_dir():
            print(f"❌ 目录不存在: {args.directory}")
            sys.exit(1)
        
        videos = (list(batch_dir.glob("*.mp4")) + list(batch_dir.glob("*.mov")) +
                  list(batch_dir.glob("*.avi")) + list(batch_dir.glob("*.webm")) +
                  list(batch_dir.glob("*.mkv")))
        
        if not videos:
            print(f"❌ 目录中无视频: {args.directory}")
            sys.exit(1)
        
        print(f"🎬 批量处理: {len(videos)} 个视频")
        results = process_batch(videos, args.interval, args.parallel)
        
        ok = sum(1 for r in results if r['status'] == 'ok')
        total_frames = sum(r.get('kept_frames', 0) for r in results)
        print(f"\n📊 批量总结: {ok}/{len(videos)} 成功 | 共入 {total_frames} 帧")
    
    elif args.command == 'stats':
        # 重用 material_search 的统计
        try:
            sys.path.insert(0, str(PROJECT_ROOT / 'bin'))
            from lh_material_search import get_stats
            stats = get_stats()
            
            vf_count = sum(1 for k, v in stats.get('by_source', {}).items() 
                          if 'video' in k.lower())
            
            print(f"\n📊 龍魂素材库统计\n")
            print(f"   总量: {stats['total']} 条")
            print(f"   品类: {stats.get('by_type', {})}")
            print(f"   视频帧素材: ~{vf_count} 条")
            print(f"   平均质量: {stats.get('avg_quality', 0):.2f}")
            print(f"   总使用: {stats.get('total_used', 0)} 次")
            print(f"   最后扫描: {stats.get('last_scan', 'N/A')}")
            print(f"\n   场景库: {FRAME_OUTPUT_DIR}")
            scenes = list(FRAME_OUTPUT_DIR.glob("*_scenes.json")) if FRAME_OUTPUT_DIR.exists() else []
            print(f"   场景索引: {len(scenes)} 个JSON")
        except Exception as e:
            print(f"❌ 统计失败: {e}")
    
    elif args.command == 'notion':
        token = args.token or os.environ.get('NOTION_TOKEN')
        if not token:
            print("❌ 需要 Notion Token (--token 或 NOTION_TOKEN 环境变量)")
            print("   前往 https://www.notion.so/my-integrations 创建集成")
            sys.exit(1)
        
        # 尝试引入 notion_client
        try:
            from notion_client import Client
        except ImportError:
            print("❌ 请安装: pip install notion-client")
            sys.exit(1)
        
        database_id = args.database or os.environ.get('NOTION_DATABASE_ID')
        if not database_id:
            print("❌ 需要 Database ID (--database 或 NOTION_DATABASE_ID)")
            sys.exit(1)
        
        notion = Client(auth=token)
        
        # 查询待处理视频
        print(f"🔍 查询 Notion 数据库中 '待处理' 条目...")
        try:
            resp = notion.databases.query(
                database_id=database_id,
                filter={
                    "property": NOTION_FIELD_STATUS,
                    "select": {"equals": "待处理"}
                }
            )
        except Exception as e:
            print(f"❌ Notion查询失败: {e}")
            sys.exit(1)
        
        items = resp.get('results', [])
        print(f"   找到 {len(items)} 个待处理条目")
        
        if not items:
            print("   没有待处理视频")
            sys.exit(0)
        
        for item in items:
            props = item.get('properties', {})
            page_id = item['id']
            
            name = ''
            title_prop = props.get(NOTION_FIELD_NAME, {})
            titles = title_prop.get('title', [])
            if titles:
                name = titles[0].get('plain_text', '未命名')
            
            url = props.get(NOTION_FIELD_VIDEO_URL, {}).get('url', '')
            tags_prop = props.get(NOTION_FIELD_TAGS, {})
            tags = ''
            for rt in tags_prop.get('rich_text', []):
                tags += rt.get('plain_text', '')
            
            if not url:
                print(f"  ⚠️ 跳过 '{name}': 无视频链接")
                update_notion_status(page_id, '链接缺失', 0, token)
                continue
            
            print(f"\n--- {name} ---")
            video_path = download_video(url)
            if not video_path:
                update_notion_status(page_id, '下载失败', 0, token)
                continue
            
            result = process_video(video_path, name, tags, args.interval)
            
            if result['status'] == 'ok':
                update_notion_status(page_id, '已清洗', result['kept_frames'], token)
            else:
                update_notion_status(page_id, '处理异常', 0, token)
    
    else:
        parser.print_help()
