#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·Notion素材提取器 v1.0 — 从Notion页面提取视频素材引用
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-NOTION-MATERIAL-EXTRACTOR-V1.0-4d5e6f7a
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

从 Notion 全量同步数据库提取:
- 视频帧占位 (frame_NNNN.png)
- 场景描述 (scene_xxx)
- 素材链接 (any image/video URL)
- Notion页面中的截图/图片引用

支持两种模式:
1. 本地模式: 从 notion_full_sync.db 读取（无需Token）
2. API模式: 直接调 Notion API（需Token）
"""

import os, sys, json, sqlite3, argparse, re, urllib.parse
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTION_DB_PATH = PROJECT_ROOT / "data" / "notion_full_sync.db"
MATERIAL_DB_PATH = PROJECT_ROOT / "data" / "material_library.db"


# ══════════════════════════════════════════════════════════════════════
# 本地模式: 从 notion_full_sync.db 提取
# ══════════════════════════════════════════════════════════════════════

def extract_from_local_db(limit: int = None) -> list:
    """从本地 Notion 全量同步库提取素材引用"""
    if not NOTION_DB_PATH.exists():
        print(f"❌ Notion 同步库不存在: {NOTION_DB_PATH}")
        print(f"   请先运行: python3 bin/lh_notion_full_sync.py")
        return []

    conn = sqlite3.connect(str(NOTION_DB_PATH))
    conn.row_factory = sqlite3.Row

    # 搜索含视频/图片/素材相关内容的页面
    sql = """
        SELECT id, title, url, content, database_name, last_edited
        FROM pages
        WHERE 1=1
    """
    rows = conn.execute(sql).fetchall()

    materials = []
    image_url_pattern = re.compile(
        r'(https?://[^\s<>"]+?\.(?:png|jpg|jpeg|gif|webp|svg|mp4|mov|heic|bmp)(?:\?[^\s<>"]*)?)',
        re.IGNORECASE
    )
    notion_image_pattern = re.compile(
        r'https?://[^\s]+?notion\.so/image/[^\s<>"]+'
    )
    frame_pattern = re.compile(r'frame[_-]?\d+', re.IGNORECASE)
    scene_pattern = re.compile(r'scene[_-]?\w+', re.IGNORECASE)

    for row in rows:
        content = row['content'] or ''
        title = row['title'] or ''
        combined = f"{title} {content}"

        # 提取图片URL
        image_urls = image_url_pattern.findall(content) + image_url_pattern.findall(title)
        notion_urls = notion_image_pattern.findall(content)

        # 提取帧引用
        frames = frame_pattern.findall(combined)
        scenes = scene_pattern.findall(combined)

        if image_urls or notion_urls or frames or scenes:
            material = {
                'source': 'notion',
                'page_id': row['id'],
                'page_title': title,
                'page_url': row['url'],
                'database': row['database_name'],
                'last_edited': row['last_edited'],
                'image_urls': image_urls[:10],
                'notion_image_urls': notion_urls[:10],
                'frame_refs': frames,
                'scene_refs': scenes,
                'content_snippet': content[:500],
                'extracted_at': datetime.now().isoformat(),
            }
            materials.append(material)

            if limit and len(materials) >= limit:
                break

    conn.close()
    return materials


# ══════════════════════════════════════════════════════════════════════
# API模式 (预留: 当Notion Token可用时)
# ══════════════════════════════════════════════════════════════════════

def extract_from_notion_api(token: str, database_id: str = None) -> list:
    """
    通过 Notion API 直接提取素材。
    Token 可以通过环境变量 NOTION_TOKEN 或参数传入。
    """
    try:
        import requests
    except ImportError:
        print("❌ 需要 requests 库: pip install requests")
        return []

    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    materials = []

    # 搜索含媒体内容的页面
    if database_id:
        url = f"https://api.notion.com/v1/databases/{database_id}/query"
        resp = requests.post(url, headers=headers, json={"page_size": 100})
        if resp.status_code == 200:
            data = resp.json()
            for page in data.get('results', []):
                # 解析页面内容
                mat = _parse_notion_page(page)
                if mat:
                    materials.append(mat)
    else:
        # 搜索所有可访问的页面
        search_url = "https://api.notion.com/v1/search"
        # 搜索含图片/视频的block
        resp = requests.post(search_url, headers=headers, json={
            "filter": {"property": "object", "value": "page"},
            "page_size": 100
        })
        if resp.status_code == 200:
            data = resp.json()
            for page in data.get('results', []):
                mat = _parse_notion_page(page)
                if mat:
                    materials.append(mat)

    return materials


def _parse_notion_page(page: dict) -> dict:
    """解析 Notion 页面为素材格式"""
    try:
        props = page.get('properties', {})
        title = ''
        for key, val in props.items():
            if val.get('type') == 'title':
                titles = val.get('title', [])
                if titles:
                    title = titles[0].get('plain_text', '')

        # 检查有无图片block
        page_id = page.get('id', '')
        return {
            'source': 'notion_api',
            'page_id': page_id,
            'page_title': title,
            'page_url': page.get('url', ''),
            'extracted_at': datetime.now().isoformat(),
        }
    except:
        return {}


# ══════════════════════════════════════════════════════════════════════
# 素材合并入库
# ══════════════════════════════════════════════════════════════════════

def import_to_material_library(materials: list, download_images: bool = False):
    """将 Notion 提取的素材导入素材库"""
    conn = sqlite3.connect(str(MATERIAL_DB_PATH))

    imported = 0
    skipped = 0

    for mat in materials:
        # 为每个图片URL创建material条目
        for img_url in mat.get('image_urls', []):
            # 生成 material_id
            not_id = f"n_{mat['page_id'][:8]}_{hash(img_url) % 10000:04d}"

            existing = conn.execute(
                "SELECT id FROM materials WHERE material_id = ?", (not_id,)
            ).fetchone()

            if existing:
                skipped += 1
                continue

            filename = Path(urllib.parse.urlparse(img_url).path).name or f"notion_{mat['page_id'][:8]}"
            tags = json.dumps(mat.get('frame_refs', []) + mat.get('scene_refs', []), ensure_ascii=False)
            notes = json.dumps({
                'source': 'notion',
                'page_title': mat.get('page_title', ''),
                'page_url': mat.get('page_url', ''),
                'database': mat.get('database', ''),
                'original_url': img_url,
            }, ensure_ascii=False)

            conn.execute("""
                INSERT OR IGNORE INTO materials
                (material_id, filepath, filename, ext, media_type, source_type,
                 content_type, emotion, tags, notes, quality_score, scanned_at)
                VALUES (?, ?, ?, ?, 'image', 'notion', 'unknown', 'neutral', ?, ?, 0.6, ?)
            """, (
                not_id, img_url, filename, Path(filename).suffix or '.png',
                tags, notes, datetime.now().isoformat()
            ))
            imported += 1

        # Notion内嵌图片
        for n_url in mat.get('notion_image_urls', []):
            not_id = f"nni_{mat['page_id'][:8]}_{hash(n_url) % 10000:04d}"
            existing = conn.execute(
                "SELECT id FROM materials WHERE material_id = ?", (not_id,)
            ).fetchone()
            if existing:
                skipped += 1
                continue

            notes = json.dumps({
                'source': 'notion_inline',
                'page_title': mat.get('page_title', ''),
                'page_url': mat.get('page_url', ''),
                'notion_image_url': n_url,
            }, ensure_ascii=False)

            conn.execute("""
                INSERT OR IGNORE INTO materials
                (material_id, filepath, filename, ext, media_type, source_type,
                 content_type, emotion, tags, notes, quality_score, scanned_at)
                VALUES (?, ?, ?, ?, 'image', 'notion', 'unknown', 'neutral', ?, ?, 0.5, ?)
            """, (
                not_id, n_url, f"notion_inline_{mat['page_id'][:8]}.png", '.png',
                json.dumps([], ensure_ascii=False), notes, datetime.now().isoformat()
            ))
            imported += 1

    conn.commit()
    conn.close()

    print(f"✅ Notion素材入库: 新增 {imported} | 跳过 {skipped} (已存在)")
    return imported


# ══════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='龍魂·Notion素材提取器')
    parser.add_argument('--mode', choices=['local', 'api'], default='local', help='提取模式')
    parser.add_argument('--token', help='Notion API Token (API模式)')
    parser.add_argument('--database', help='Notion Database ID (API模式)')
    parser.add_argument('--limit', '-n', type=int, help='限制提取数量')
    parser.add_argument('--output', '-o', help='输出JSON路径')
    parser.add_argument('--import', dest='do_import', action='store_true', help='直接导入素材库')
    parser.add_argument('--json', action='store_true', help='JSON输出到stdout')

    args = parser.parse_args()

    materials = []

    if args.mode == 'local':
        materials = extract_from_local_db(limit=args.limit)
        print(f"\n📥 Notion本地提取: {len(materials)} 个页面含素材引用")
    elif args.mode == 'api':
        token = args.token or os.environ.get('NOTION_TOKEN')
        if not token:
            print("❌ 需要 Notion Token (--token 或 NOTION_TOKEN 环境变量)")
            sys.exit(1)
        materials = extract_from_notion_api(token, args.database)
        print(f"\n📥 Notion API提取: {len(materials)} 个素材")

    # 汇总
    total_urls = sum(len(m.get('image_urls', [])) + len(m.get('notion_image_urls', [])) for m in materials)
    total_frames = sum(len(m.get('frame_refs', [])) for m in materials)
    print(f"   图片URL: {total_urls} | 帧引用: {total_frames}")

    # 输出
    if args.json:
        print(json.dumps(materials, ensure_ascii=False, indent=2))

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(materials, f, ensure_ascii=False, indent=2)
        print(f"✅ 导出 → {out_path}")

    if args.do_import:
        import_to_material_library(materials)
