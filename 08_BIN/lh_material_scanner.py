#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·素材扫描引擎 v1.0 — 全量媒体文件扫描 + 元数据提取 + 入库
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-MATERIAL-SCANNER-V1.0-3a7f1b2c
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

扫描所有媒体目录，提取元数据，写入素材库 SQLite。
支持增量扫描：已入库文件跳过（除非 --force）。
"""

import os, sys, json, hashlib, sqlite3, argparse, re, time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "material_library.db"
os.makedirs(DB_PATH.parent, exist_ok=True)

# 扫描目录配置
SCAN_DIRS = [
    PROJECT_ROOT / "data" / "training" / "media",
    PROJECT_ROOT / "output" / "videos",
    PROJECT_ROOT / "videos",
    PROJECT_ROOT / "data" / "auto-learned",
]

# 支持的媒体扩展名
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.heic', '.tiff'}
VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.webm', '.mkv', '.flv', '.m4v'}
AUDIO_EXTS = {'.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a', '.opus'}

# 内容类型关键词映射 (从文件名/路径推断)
CONTENT_KEYWORDS = {
    'code': ['code', '代码', '编程', 'python', 'js', 'html', 'css', 'api'],
    'architecture': ['架构', 'arch', '系统', '拓扑', 'flow', '流程', 'diagram'],
    'data': ['数据', 'data', '图表', 'chart', '统计', '仪表盘', 'dashboard'],
    'security': ['安全', 'security', '加密', '密钥', '攻击', '漏洞', 'audit'],
    'culture': ['文化', 'culture', '易经', '道德经', '老子', '五行', '八卦', '哲学'],
    'protocol': ['协议', 'protocol', '宪法', '规则', 'constitution', 'governance'],
    'deploy': ['部署', 'deploy', '服务器', 'server', '鲲鹏', 'docker', 'k8s'],
    'ui': ['界面', 'ui', '截图', '页面', 'portal', '前端', 'frontend', '页面'],
    'persona': ['人格', 'persona', 'AI', '模型', 'model', 'agent', '智能'],
    'evidence': ['证据', 'evidence', '截图', 'screen', '记录', 'proof'],
    'video_frame': ['视频', 'video', '帧', 'frame', '画面', '场景', 'scene'],
    'document': ['文档', 'doc', '论文', 'paper', 'article', '文章'],
    'photo': ['照片', 'photo', 'img_', '拍摄'],
    'log': ['日志', 'log', '记录', '报告', 'report'],
}

# 情感映射 (从文件名/路径推断)
EMOTION_MAP = {
    'angry': ['愤怒', '怒', '抗议', '维权'],
    'solemn': ['庄严', '严肃', '宣誓', '宪法', 'protocol'],
    'hopeful': ['希望', '未来', '计划', 'roadmap', '蓝图'],
    'analytical': ['分析', '数据', '统计', '图表', '审计'],
    'creative': ['创意', '设计', '灵感', '艺术', 'creative'],
    'protective': ['守护', '安全', '保护', '防御', '护'],
}


def file_hash(filepath: Path) -> str:
    """SHA-256 前 16 字符"""
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()[:16]


def get_file_type(ext: str) -> str:
    ext = ext.lower()
    if ext in IMAGE_EXTS:
        return 'image'
    elif ext in VIDEO_EXTS:
        return 'video'
    elif ext in AUDIO_EXTS:
        return 'audio'
    return 'other'


def extract_image_meta(filepath: Path) -> dict:
    """提取图片尺寸/模式等元数据"""
    try:
        from PIL import Image
        img = Image.open(filepath)
        w, h = img.size
        return {
            'width': w,
            'height': h,
            'mode': img.mode,
            'aspect_ratio': round(w / h, 3) if h else 0,
            'is_portrait': h > w,
            'is_screenshot': (w > 800 and h > 800 and (abs(w/h - 9/16) < 0.1 or abs(w/h - 9/19.5) < 0.1 or abs(w/h - 0.461) < 0.1))
        }
    except Exception:
        return {}


def extract_video_meta(filepath: Path) -> dict:
    """提取视频时长/分辨率 (ffprobe)"""
    try:
        import subprocess
        cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format',
               '-show_streams', str(filepath)]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            fmt = data.get('format', {})
            duration = float(fmt.get('duration', 0))
            # 找视频流
            video_stream = None
            for s in data.get('streams', []):
                if s.get('codec_type') == 'video':
                    video_stream = s
                    break
            return {
                'duration': round(duration, 1),
                'duration_fmt': f"{int(duration//60)}:{int(duration%60):02d}",
                'width': video_stream.get('width', 0) if video_stream else 0,
                'height': video_stream.get('height', 0) if video_stream else 0,
                'fps': eval(str(video_stream.get('r_frame_rate', '0/1'))) if video_stream else 0,
                'codec': video_stream.get('codec_name', '') if video_stream else '',
            }
    except Exception:
        pass
    return {}


def infer_content_type(filepath: Path) -> tuple:
    """从文件名和路径推断内容类型"""
    path_lower = str(filepath).lower()
    filename_lower = filepath.name.lower()

    scores = defaultdict(int)
    for ctype, keywords in CONTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in path_lower or kw in filename_lower:
                scores[ctype] += 1

    if scores:
        return max(scores, key=scores.get), list(scores.keys())[:3]
    return 'unknown', []


def infer_emotion(filepath: Path) -> str:
    """推断情感基调"""
    path_lower = str(filepath).lower()
    for emotion, keywords in EMOTION_MAP.items():
        for kw in keywords:
            if kw in path_lower:
                return emotion
    return 'neutral'


def detect_media_source(filepath: Path) -> str:
    """检测来源类型"""
    name = filepath.name
    if name.upper().startswith('IMG_'):
        return 'phone_camera'
    elif re.match(r'^[a-f0-9]{40}', name, re.I):
        return 'hash_screenshot'
    elif 'screenshot' in name.lower() or '截屏' in name.lower() or '截图' in name.lower():
        return 'screenshot'
    elif 'evidence' in str(filepath).lower():
        return 'evidence_screenshot'
    elif 'generated' in str(filepath).lower() or 'output' in str(filepath).lower():
        return 'ai_generated'
    elif 'video' in str(filepath).lower():
        return 'video_frame'
    return 'unknown'


def get_exif_date(filepath: Path) -> str:
    """尝试提取 EXIF 拍摄日期"""
    try:
        from PIL import Image
        img = Image.open(filepath)
        exif = img._getexif()
        if exif:
            for tag_id, value in exif.items():
                # 36867 = DateTimeOriginal, 36868 = DateTimeDigitized, 306 = DateTime
                if tag_id in (36867, 36868, 306):
                    return value
    except Exception:
        pass
    return ''


def dominant_colors_heuristic(filepath: Path) -> list:
    """快速主色调提取（采样法，不依赖重库）"""
    try:
        from PIL import Image
        img = Image.open(filepath)
        img = img.convert('RGB')
        # 缩小到 50x50 加速
        img_small = img.resize((50, 50), Image.LANCZOS)
        pixels = list(img_small.getdata())

        # 简易颜色聚类
        from collections import Counter
        # 量化到 32 级
        quantized = [(r//32*32, g//32*32, b//32*32) for r, g, b in pixels]
        color_counts = Counter(quantized)
        top5 = color_counts.most_common(5)
        total = sum(c for _, c in top5)

        result = []
        for (r, g, b), count in top5:
            pct = round(count / total * 100, 1)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            # 判定色调
            if max(r, g, b) - min(r, g, b) < 30:
                tone = 'gray' if r > 128 else 'dark'
            elif r > g and r > b:
                tone = 'warm' if g > b * 0.8 else 'red'
            elif g > r and g > b:
                tone = 'nature'
            elif b > r and b > g:
                tone = 'cool'
            else:
                tone = 'mixed'
            result.append({'hex': hex_color, 'tone': tone, 'pct': pct})

        # 整体亮度
        avg_brightness = sum(sum(p) for p in pixels) / (3 * len(pixels))
        brightness_level = 'dark' if avg_brightness < 85 else 'mid' if avg_brightness < 170 else 'bright'

        return result, brightness_level
    except Exception:
        return [], 'unknown'


# ══════════════════════════════════════════════════════════════════════
# 数据库初始化
# ══════════════════════════════════════════════════════════════════════

def init_db(db_path: Path):
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id TEXT UNIQUE NOT NULL,
            filepath TEXT NOT NULL,
            filename TEXT NOT NULL,
            ext TEXT NOT NULL,
            media_type TEXT NOT NULL,        -- image/video/audio/other
            file_size INTEGER,               -- bytes
            file_hash TEXT NOT NULL,         -- SHA-256[:16]
            created_at TEXT,                 -- 文件修改时间
            scanned_at TEXT NOT NULL,        -- 扫描时间
            -- 图片专属
            width INTEGER,
            height INTEGER,
            aspect_ratio REAL,
            mode TEXT,                       -- 图片色彩模式
            is_portrait INTEGER DEFAULT 0,
            is_screenshot INTEGER DEFAULT 0,
            dominant_colors TEXT,            -- JSON: [{hex, tone, pct}]
            brightness TEXT,                 -- dark/mid/bright
            -- 视频专属
            duration REAL,                   -- 秒
            duration_fmt TEXT,              -- MM:SS
            fps REAL,
            video_codec TEXT,
            -- 通用标签
            content_type TEXT DEFAULT 'unknown',
            content_subtypes TEXT,            -- JSON array
            emotion TEXT DEFAULT 'neutral',
            source_type TEXT DEFAULT 'unknown',
            exif_date TEXT,
            -- 质量/使用标记
            quality_score REAL DEFAULT 0.5,   -- 0-1 可用度评分
            usage_count INTEGER DEFAULT 0,
            last_used TEXT,
            tags TEXT DEFAULT '[]',            -- JSON array 自定义标签
            notes TEXT                         -- 备注
        );

        CREATE TABLE IF NOT EXISTS material_scenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id TEXT NOT NULL,
            scene_index INTEGER DEFAULT 0,
            scene_label TEXT,                 -- 场景描述标签
            scene_emotion TEXT,
            scene_colors TEXT,                -- JSON
            thumbnail_path TEXT,              -- 缩略图路径
            relevance_score REAL DEFAULT 0.5,
            FOREIGN KEY(material_id) REFERENCES materials(material_id)
        );

        CREATE TABLE IF NOT EXISTS scan_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_start TEXT NOT NULL,
            scan_end TEXT,
            total_files INTEGER DEFAULT 0,
            new_files INTEGER DEFAULT 0,
            updated_files INTEGER DEFAULT 0,
            skipped_files INTEGER DEFAULT 0,
            errors INTEGER DEFAULT 0,
            dna TEXT
        );

        -- 全文搜索索引
        CREATE VIRTUAL TABLE IF NOT EXISTS materials_fts USING fts5(
            filename, content_type, emotion, source_type, tags, notes,
            content='materials', content_rowid='id'
        );

        -- 触发器保持 FTS 同步
        CREATE TRIGGER IF NOT EXISTS materials_ai AFTER INSERT ON materials BEGIN
            INSERT INTO materials_fts(rowid, filename, content_type, emotion, source_type, tags, notes)
            VALUES (new.id, new.filename, new.content_type, new.emotion, new.source_type, new.tags, new.notes);
        END;

        CREATE TRIGGER IF NOT EXISTS materials_ad AFTER DELETE ON materials BEGIN
            INSERT INTO materials_fts(materials_fts, rowid, filename, content_type, emotion, source_type, tags, notes)
            VALUES ('delete', old.id, old.filename, old.content_type, old.emotion, old.source_type, old.tags, old.notes);
        END;

        CREATE TRIGGER IF NOT EXISTS materials_au AFTER UPDATE ON materials BEGIN
            INSERT INTO materials_fts(materials_fts, rowid, filename, content_type, emotion, source_type, tags, notes)
            VALUES ('delete', old.id, old.filename, old.content_type, old.emotion, old.source_type, old.tags, old.notes);
            INSERT INTO materials_fts(rowid, filename, content_type, emotion, source_type, tags, notes)
            VALUES (new.id, new.filename, new.content_type, new.emotion, new.source_type, new.tags, new.notes);
        END;
    """)

    conn.commit()
    return conn


# ══════════════════════════════════════════════════════════════════════
# 扫描逻辑
# ══════════════════════════════════════════════════════════════════════

def scan_file(filepath: Path, conn: sqlite3.Connection, force: bool = False) -> str:
    """扫描单个文件，返回状态: new/updated/skipped/error"""
    if not filepath.is_file():
        return 'skipped'

    ext = filepath.suffix.lower()
    media_type = get_file_type(ext)
    if media_type == 'other':
        return 'skipped'

    # 检查是否已存在
    fhash = file_hash(filepath)
    material_id = f"{media_type[0]}_{fhash}"  # i_xxx / v_xxx / a_xxx

    cur = conn.execute("SELECT id, file_hash FROM materials WHERE material_id = ?", (material_id,))
    existing = cur.fetchone()
    if existing and not force:
        if existing[1] == fhash:
            return 'skipped'

    # 提取元数据
    stat = filepath.stat()
    file_size = stat.st_size
    file_mtime = datetime.fromtimestamp(stat.st_mtime).isoformat()

    meta = {}
    if media_type == 'image':
        meta = extract_image_meta(filepath)
    elif media_type == 'video':
        meta = extract_video_meta(filepath)

    content_type, subtypes = infer_content_type(filepath)
    emotion = infer_emotion(filepath)
    source_type = detect_media_source(filepath)
    exif_date = get_exif_date(filepath) if media_type == 'image' else ''

    # 主色调
    colors, brightness = [], 'unknown'
    if media_type == 'image':
        colors, brightness = dominant_colors_heuristic(filepath)

    # 质量评分启发式
    quality = 0.5
    if meta.get('width', 0) >= 1920:
        quality += 0.15
    if media_type == 'image' and meta.get('is_screenshot'):
        quality += 0.1  # 截图有记录价值
    if source_type in ('phone_camera', 'evidence_screenshot'):
        quality += 0.1
    if content_type != 'unknown':
        quality += 0.05
    quality = min(1.0, quality)

    # 构建数据
    data = {
        'material_id': material_id,
        'filepath': str(filepath),
        'filename': filepath.name,
        'ext': ext,
        'media_type': media_type,
        'file_size': file_size,
        'file_hash': fhash,
        'created_at': file_mtime,
        'scanned_at': datetime.now().isoformat(),
        'width': meta.get('width'),
        'height': meta.get('height'),
        'aspect_ratio': meta.get('aspect_ratio'),
        'mode': meta.get('mode'),
        'is_portrait': 1 if meta.get('is_portrait') else 0,
        'is_screenshot': 1 if meta.get('is_screenshot') else 0,
        'dominant_colors': json.dumps(colors, ensure_ascii=False),
        'brightness': brightness,
        'duration': meta.get('duration'),
        'duration_fmt': meta.get('duration_fmt'),
        'fps': meta.get('fps'),
        'video_codec': meta.get('codec'),
        'content_type': content_type,
        'content_subtypes': json.dumps(subtypes, ensure_ascii=False),
        'emotion': emotion,
        'source_type': source_type,
        'exif_date': exif_date,
        'quality_score': quality,
        'tags': json.dumps([], ensure_ascii=False),
    }

    if existing:
        # 更新
        cols = ', '.join(f'{k}=:{k}' for k in data)
        conn.execute(f"UPDATE materials SET {cols} WHERE material_id = :material_id", data)
        return 'updated'
    else:
        # 插入
        cols = ', '.join(data.keys())
        placeholders = ', '.join(f':{k}' for k in data)
        conn.execute(f"INSERT INTO materials ({cols}) VALUES ({placeholders})", data)
        return 'new'


def scan_all(force: bool = False, verbose: bool = False):
    """全量扫描"""
    conn = init_db(DB_PATH)

    scan_id = datetime.now().isoformat()
    stats = {'new': 0, 'updated': 0, 'skipped': 0, 'errors': 0, 'total': 0}

    print(f"\n🐉 龍魂素材扫描引擎 v1.0")
    print(f"   数据库: {DB_PATH}")
    print(f"   模式: {'强制全扫' if force else '增量扫描'}\n")

    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        print(f"📂 扫描: {scan_dir}")
        count = 0
        for filepath in scan_dir.rglob('*'):
            if filepath.is_file() and filepath.suffix.lower() in (IMAGE_EXTS | VIDEO_EXTS | AUDIO_EXTS):
                try:
                    status = scan_file(filepath, conn, force)
                    stats[status] += 1
                    stats['total'] += 1
                    count += 1
                    if verbose or status in ('new', 'updated'):
                        icon = {'new': '🆕', 'updated': '🔄', 'skipped': '⏭️', 'error': '❌'}.get(status, '❓')
                        print(f"   {icon} [{status:7s}] {filepath.name[:60]}")
                except Exception as e:
                    stats['errors'] += 1
                    if verbose:
                        print(f"   ❌ ERROR: {filepath.name} - {e}")
        if count:
            print(f"   ✅ {count} 个文件处理完成\n")

    conn.commit()

    # 记录扫描日志
    conn.execute("""
        INSERT INTO scan_log (scan_start, scan_end, total_files, new_files, updated_files, skipped_files, errors, dna)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        scan_id, datetime.now().isoformat(), stats['total'],
        stats['new'], stats['updated'], stats['skipped'], stats['errors'],
        '#龍芯⚡️MATERIAL-SCAN-v1.0'
    ))
    conn.commit()

    # 汇总
    total_in_db = conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
    print(f"{'='*50}")
    print(f"📊 扫描完成")
    print(f"   本次处理: {stats['total']} 个文件")
    print(f"   新增: {stats['new']}  更新: {stats['updated']}  跳过: {stats['skipped']}  错误: {stats['errors']}")
    print(f"   素材库总量: {total_in_db} 条")
    print(f"{'='*50}")

    # 分类统计
    print(f"\n📊 素材库分类:")
    for mtype in ['image', 'video', 'audio']:
        count = conn.execute("SELECT COUNT(*) FROM materials WHERE media_type = ?", (mtype,)).fetchone()[0]
        if count:
            print(f"   {mtype}: {count} 条")

    # 内容类型分布
    print(f"\n📊 内容类型:")
    rows = conn.execute("""
        SELECT content_type, COUNT(*) as cnt FROM materials
        WHERE content_type != 'unknown'
        GROUP BY content_type ORDER BY cnt DESC
    """).fetchall()
    for ctype, cnt in rows:
        print(f"   {ctype}: {cnt} 条")
    unknown = conn.execute("SELECT COUNT(*) FROM materials WHERE content_type = 'unknown'").fetchone()[0]
    if unknown:
        print(f"   unknown: {unknown} 条")

    conn.close()
    return stats


# ══════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='龍魂素材扫描引擎')
    parser.add_argument('--force', '-f', action='store_true', help='强制重新扫描所有文件')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细输出')
    parser.add_argument('--stats', '-s', action='store_true', help='仅显示统计')
    parser.add_argument('--path', type=str, help='扫描指定目录')

    args = parser.parse_args()

    if args.path:
        SCAN_DIRS.insert(0, Path(args.path))

    if args.stats:
        conn = init_db(DB_PATH)
        total = conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
        print(f"素材库总量: {total} 条")
        # 按类型
        for mtype in ['image', 'video', 'audio']:
            cnt = conn.execute("SELECT COUNT(*) FROM materials WHERE media_type = ?", (mtype,)).fetchone()[0]
            print(f"  {mtype}: {cnt}")
        # 按内容类型
        for row in conn.execute("SELECT content_type, COUNT(*) FROM materials WHERE content_type != 'unknown' GROUP BY content_type ORDER BY COUNT(*) DESC LIMIT 10").fetchall():
            print(f"  {row[0]}: {row[1]}")
        conn.close()
    else:
        scan_all(force=args.force, verbose=args.verbose)
