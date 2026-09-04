#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·素材搜索与标签引擎 v1.0 — 素材查询 + AI辅助打标 + 场景匹配
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-MATERIAL-SEARCH-V1.0-5b2c8d1e
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

提供:
- 关键词/语义搜索素材
- 按场景需求匹配素材（主题/情感/色调/构图）
- AI辅助自动打标（调用本地 longhun 模型）
- 素材使用统计
"""

import os, sys, json, sqlite3, argparse, time, subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "material_library.db"

# ══════════════════════════════════════════════════════════════════════
# AI 辅助打标（调用本地模型）
# ══════════════════════════════════════════════════════════════════════

TAG_PROMPT_TEMPLATE = """你是龍魂素材标签助手。给一个媒体文件打标签，只输出JSON，不要解释。

文件名: {filename}
文件类型: {media_type}
尺寸: {width}x{height}
文件夹: {dirname}
当前推测: 类型={content_type}, 情感={emotion}, 来源={source_type}

请输出:
{{
  "tags": ["标签1", "标签2", ...],
  "scene_category": "技术教学/文化传承/系统运维/证据记录/创意设计/生活记录/其他",
  "scene_mood": "严肃/温暖/警示/激励/平和/紧张",
  "visual_style": "暗色科技/明亮自然/文档截图/界面展示/人物场景/数据图表",
  "suggested_use": "片头/背景/过渡/字幕背景/证据展示/资料画面",
  "relevance_keywords": ["关键词1", ...],
  "quality_note": "可用/需裁剪/低质量/重复素材",
  "confidence": 0.0-1.0
}}"""


def ai_tag_material(filename: str, media_type: str, width: int, height: int,
                    dirname: str, content_type: str, emotion: str, source_type: str) -> dict:
    """调用 Ollama longhun 模型打标签"""
    prompt = TAG_PROMPT_TEMPLATE.format(
        filename=filename, media_type=media_type,
        width=width, height=height, dirname=dirname,
        content_type=content_type, emotion=emotion, source_type=source_type
    )
    try:
        result = subprocess.run(
            ['ollama', 'run', 'longhun-v4.0', prompt],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            # 提取 JSON
            response = result.stdout.strip()
            # 找第一个 { ... } 块
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
    except Exception as e:
        pass
    return {}


# ══════════════════════════════════════════════════════════════════════
# 搜索/查询
# ══════════════════════════════════════════════════════════════════════

def _is_chinese(text: str) -> bool:
    """检测字符串是否包含中文"""
    return any('\u4e00' <= c <= '\u9fff' for c in text)


def search_materials(query: str, media_type: str = None, content_type: str = None,
                     emotion: str = None, min_quality: float = 0, limit: int = 50) -> list:
    """全文搜索 + 筛选（中英文混合搜索）"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    conditions = []
    params = []

    sql = "SELECT m.* FROM materials m WHERE 1=1"

    if query:
        if _is_chinese(query):
            # 中文用 LIKE 搜索 tags/filename/content_type/notes
            like_clauses = [
                "m.tags LIKE ?", "m.filename LIKE ?",
                "m.content_type LIKE ?", "m.notes LIKE ?",
                "m.emotion LIKE ?",
            ]
            like_val = f"%{query}%"
            conditions.append(f"({' OR '.join(like_clauses)})")
            params.extend([like_val] * 5)
        else:
            # 英文/ASCII 用 FTS
            sql = """SELECT m.* FROM materials m
                     JOIN materials_fts fts ON m.id = fts.rowid
                     WHERE materials_fts MATCH ?"""
            params.insert(0, query)
            # query 条件已直接在 sql 中，不重复加入 conditions

    # 附加筛选条件
    if media_type:
        conditions.append("m.media_type = ?")
        params.append(media_type)
    if content_type:
        conditions.append("m.content_type = ?")
        params.append(content_type)
    if emotion:
        conditions.append("m.emotion = ?")
        params.append(emotion)
    if min_quality > 0:
        conditions.append("m.quality_score >= ?")
        params.append(min_quality)

    if conditions:
        sql += "\n            AND " + "\n            AND ".join(conditions)

    sql += f" ORDER BY m.quality_score DESC, m.usage_count DESC LIMIT {limit}"

    cur = conn.execute(sql, params)
    results = [dict(row) for row in cur.fetchall()]
    conn.close()
    return results


def match_scene(topic: str, mood: str = None, style: str = None, limit: int = 10) -> list:
    """
    场景匹配：根据视频主题和情绪匹配最佳素材。
    两步策略：
    1. 关键词匹配（内容类型/情感/来源）
    2. 质量+使用频率排序
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    # 从 topic 提取关键词
    topic_lower = topic.lower()

    # 内容类型映射
    content_map = {
        '技术': 'code', '代码': 'code', '编程': 'code', '开发': 'code',
        '安全': 'security', '漏洞': 'security', '防护': 'security', '审计': 'security',
        '文化': 'culture', '易经': 'culture', '道德经': 'culture', '哲学': 'culture', '传统': 'culture',
        '系统': 'architecture', '架构': 'architecture', '拓扑': 'architecture',
        '部署': 'deploy', '上线': 'deploy', '服务器': 'deploy',
        '证据': 'evidence', '记录': 'evidence', '截图': 'evidence',
        '数据': 'data', '统计': 'data', '图表': 'data',
        'AI': 'persona', '模型': 'persona', '智能': 'persona', '人格': 'persona',
    }

    matched_types = []
    for key, val in content_map.items():
        if key in topic_lower:
            matched_types.append(val)

    # 情感映射
    mood_map = {
        '愤怒': 'angry', '庄严': 'solemn', '希望': 'hopeful',
        '分析': 'analytical', '创意': 'creative', '守护': 'protective',
    }

    matched_moods = []
    if mood:
        matched_moods.append(mood_map.get(mood, mood))
    for key, val in mood_map.items():
        if key in topic_lower:
            matched_moods.append(val)

    # 构建查询
    conditions = ["m.media_type = 'image'"]  # 优先图片素材
    params = []

    if matched_types:
        placeholders = ','.join('?' * len(matched_types))
        conditions.append(f"m.content_type IN ({placeholders})")
        params.extend(matched_types)
    if matched_moods:
        placeholders = ','.join('?' * len(matched_moods))
        conditions.append(f"m.emotion IN ({placeholders})")
        params.extend(matched_moods)
    if style:
        # 按视觉风格筛选（从 tags/dominant_colors 推断）
        if '暗色' in style or 'dark' in style.lower():
            conditions.append("m.brightness = 'dark'")
        elif '明亮' in style or 'bright' in style.lower():
            conditions.append("m.brightness = 'bright'")
        elif '科技' in style or 'tech' in style.lower():
            conditions.append("(m.brightness = 'dark' OR m.content_type IN ('code','architecture','ui'))")

    where = " AND ".join(conditions)
    sql = f"""
        SELECT m.* FROM materials m
        WHERE {where}
        ORDER BY m.quality_score DESC, m.width DESC
        LIMIT {limit}
    """

    cur = conn.execute(sql, params)
    results = [dict(row) for row in cur.fetchall()]

    # 如果匹配不够，用通用优质素材补充
    if len(results) < limit:
        exclude_ids = tuple(r['id'] for r in results) if results else (-1,)
        fill_sql = f"""
            SELECT m.* FROM materials m
            WHERE m.media_type = 'image' AND m.id NOT IN ({','.join('?'*len(exclude_ids))})
            ORDER BY m.quality_score DESC LIMIT ?
        """
        fill_cur = conn.execute(fill_sql, list(exclude_ids) + [limit - len(results)])
        results.extend([dict(row) for row in fill_cur.fetchall()])

    conn.close()
    return results


def get_stats() -> dict:
    """获取素材库统计"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    stats = {}
    stats['total'] = conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
    stats['by_type'] = {}
    for row in conn.execute("SELECT media_type, COUNT(*) as cnt FROM materials GROUP BY media_type").fetchall():
        stats['by_type'][row['media_type']] = row['cnt']

    stats['by_content'] = {}
    for row in conn.execute(
        "SELECT content_type, COUNT(*) as cnt FROM materials WHERE content_type != 'unknown' GROUP BY content_type ORDER BY cnt DESC LIMIT 15"
    ).fetchall():
        stats['by_content'][row['content_type']] = row['cnt']

    stats['by_emotion'] = {}
    for row in conn.execute(
        "SELECT emotion, COUNT(*) as cnt FROM materials WHERE emotion != 'neutral' GROUP BY emotion ORDER BY cnt DESC"
    ).fetchall():
        stats['by_emotion'][row['emotion']] = row['cnt']

    stats['by_source'] = {}
    for row in conn.execute(
        "SELECT source_type, COUNT(*) as cnt FROM materials GROUP BY source_type ORDER BY cnt DESC"
    ).fetchall():
        stats['by_source'][row['source_type']] = row['cnt']

    stats['avg_quality'] = conn.execute("SELECT AVG(quality_score) FROM materials").fetchone()[0] or 0
    stats['total_used'] = conn.execute("SELECT SUM(usage_count) FROM materials").fetchone()[0] or 0
    stats['last_scan'] = conn.execute("SELECT MAX(scan_end) FROM scan_log").fetchone()[0] or 'N/A'

    conn.close()
    return stats


def auto_tag_batch(limit: int = 50, dry_run: bool = False):
    """批量AI自动打标未标记素材"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    # 优先打标 quality > 0.5 且未标记的
    rows = conn.execute("""
        SELECT * FROM materials
        WHERE media_type = 'image' AND quality_score >= 0.5
        AND (tags = '[]' OR tags IS NULL)
        ORDER BY quality_score DESC LIMIT ?
    """, (limit,)).fetchall()

    print(f"🏷️ AI自动打标: {len(rows)} 个素材待处理")
    if dry_run:
        for r in rows:
            print(f"   [DRY] {r['filename'][:50]}")
        conn.close()
        return

    tagged = 0
    for r in rows:
        dirname = str(Path(r['filepath']).parent.name)
        result = ai_tag_material(
            filename=r['filename'], media_type=r['media_type'],
            width=r['width'] or 0, height=r['height'] or 0,
            dirname=dirname, content_type=r['content_type'],
            emotion=r['emotion'], source_type=r['source_type']
        )
        if result:
            tags = json.dumps(result.get('tags', []), ensure_ascii=False)
            notes = json.dumps({
                'scene_category': result.get('scene_category', ''),
                'scene_mood': result.get('scene_mood', ''),
                'visual_style': result.get('visual_style', ''),
                'suggested_use': result.get('suggested_use', ''),
                'confidence': result.get('confidence', 0),
                'auto_tagged_at': datetime.now().isoformat()
            }, ensure_ascii=False)

            conn.execute(
                "UPDATE materials SET tags = ?, notes = ? WHERE id = ?",
                (tags, notes, r['id'])
            )
            tagged += 1
            print(f"   ✅ [{r['filename'][:45]}] {result.get('scene_category','?')} | {result.get('suggested_use','?')}")

    conn.commit()
    conn.close()
    print(f"\n🏷️ 完成: {tagged}/{len(rows)} 个素材已打标")


def export_material_json(output_path: str = None):
    """导出素材库为 JSON（供视频管线使用）"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT material_id, filepath, filename, media_type, width, height,
               content_type, emotion, tags, quality_score, dominant_colors,
               brightness, source_type, notes
        FROM materials
        WHERE quality_score >= 0.3
        ORDER BY quality_score DESC
    """).fetchall()

    data = []
    for r in rows:
        item = dict(r)
        item['tags'] = json.loads(item.get('tags', '[]'))
        item['dominant_colors'] = json.loads(item.get('dominant_colors', '[]'))
        item['notes'] = json.loads(item.get('notes', '{}')) if item.get('notes') else {}
        data.append(item)

    if output_path:
        path = Path(output_path)
    else:
        path = PROJECT_ROOT / "data" / "material_export.json"
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    conn.close()
    print(f"✅ 导出 {len(data)} 条素材 → {path}")
    return str(path)


def mark_used(material_id: str):
    """标记素材已使用"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        UPDATE materials SET usage_count = usage_count + 1, last_used = ?
        WHERE material_id = ?
    """, (datetime.now().isoformat(), material_id))
    conn.commit()
    conn.close()


# ══════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='龍魂素材搜索与标签引擎')
    sub = parser.add_subparsers(dest='command')

    # search
    p_search = sub.add_parser('search', help='搜索素材')
    p_search.add_argument('query', nargs='?', default='', help='搜索关键词')
    p_search.add_argument('--type', '-t', choices=['image', 'video', 'audio'], help='媒体类型')
    p_search.add_argument('--content', '-c', help='内容类型')
    p_search.add_argument('--emotion', '-e', help='情感')
    p_search.add_argument('--quality', '-q', type=float, default=0, help='最低质量分')
    p_search.add_argument('--limit', '-n', type=int, default=30, help='结果数量')
    p_search.add_argument('--json', action='store_true', help='JSON输出')

    # match
    p_match = sub.add_parser('match', help='场景匹配')
    p_match.add_argument('topic', help='视频主题')
    p_match.add_argument('--mood', '-m', help='情感基调')
    p_match.add_argument('--style', '-s', help='视觉风格')
    p_match.add_argument('--limit', '-n', type=int, default=10, help='素材数量')
    p_match.add_argument('--json', action='store_true', help='JSON输出')

    # tag
    p_tag = sub.add_parser('tag', help='AI自动打标')
    p_tag.add_argument('--limit', '-n', type=int, default=30, help='批处理数量')
    p_tag.add_argument('--dry-run', action='store_true', help='预演模式')

    # stats
    p_stats = sub.add_parser('stats', help='素材库统计')

    # export
    p_export = sub.add_parser('export', help='导出素材库JSON')
    p_export.add_argument('--output', '-o', help='输出路径')

    args = parser.parse_args()

    if args.command == 'search':
        results = search_materials(
            query=args.query, media_type=args.type,
            content_type=args.content, emotion=args.emotion,
            min_quality=args.quality, limit=args.limit
        )
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔍 搜索: '{args.query}' → {len(results)} 个结果\n")
            for r in results:
                tags = json.loads(r.get('tags', '[]'))
                print(f"  [{r['media_type'][0].upper()}] {r['filename'][:45]:45s} | {r['content_type']:12s} | {r['emotion']:10s} | Q={r['quality_score']:.1f} | {' '.join(tags[:3])}")

    elif args.command == 'match':
        results = match_scene(topic=args.topic, mood=args.mood, style=args.style, limit=args.limit)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"\n🎬 场景匹配: '{args.topic}' → {len(results)} 个素材\n")
            for r in results:
                colors = json.loads(r.get('dominant_colors', '[]'))
                color_str = ' '.join(c['hex'] for c in colors[:2]) if colors else 'N/A'
                print(f"  [{r['media_type'][0].upper()}] {r['filename'][:40]:40s} | {r['content_type']:12s} | {r['emotion']:10s} | 色调: {r['brightness']} | {color_str}")

    elif args.command == 'tag':
        auto_tag_batch(limit=args.limit, dry_run=args.dry_run)

    elif args.command == 'stats':
        stats = get_stats()
        print(f"\n📊 龍魂素材库统计")
        print(f"   总量: {stats['total']} 条")
        print(f"   品类: {stats['by_type']}")
        print(f"   平均质量: {stats['avg_quality']:.2f}")
        print(f"   总使用次数: {stats['total_used']}")
        print(f"   最后扫描: {stats['last_scan']}")
        print(f"\n   内容类型 Top10:")
        for k, v in sorted(stats['by_content'].items(), key=lambda x: -x[1])[:10]:
            print(f"     {k}: {v}")
        print(f"\n   来源分布:")
        for k, v in stats['by_source'].items():
            print(f"     {k}: {v}")

    elif args.command == 'export':
        export_material_json(args.output)

    else:
        parser.print_help()
