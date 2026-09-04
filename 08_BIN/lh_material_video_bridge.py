#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·素材↔视频管线桥接 v1.0 — 视频生产自动调素材
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-MATERIAL-VIDEO-BRIDGE-V1.0-9c1a2b3d
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
- 根据脚本内容自动匹配素材
- 为每个场景分配最适画面
- 导出场景→素材映射 JSON
- 素材使用追踪
"""

import os, sys, json, sqlite3, argparse, re, random
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "material_library.db"


# ══════════════════════════════════════════════════════════════════════
# 场景关键词提取
# ══════════════════════════════════════════════════════════════════════

TOPIC_KEYWORDS = {
    '主权': ['security', 'protocol', 'evidence'],
    '数字': ['code', 'architecture', 'ui'],
    'AI': ['ai', 'code', 'architecture'],
    '安全': ['security', 'protocol'],
    '数据': ['data', 'evidence', 'ui'],
    '技术': ['code', 'architecture', 'ai'],
    '文化': ['culture', 'protocol'],
    '道德经': ['culture'],
    '易经': ['culture'],
    '战争': ['security', 'protocol', 'evidence'],
    '人民': ['evidence', 'photo'],
    '法律': ['protocol', 'evidence'],
    '底层': ['code', 'architecture'],
    '算法': ['code', 'ai', 'data'],
    '部署': ['deploy', 'architecture'],
    '系统': ['architecture', 'code'],
    '隐私': ['security', 'protocol'],
    '未来': ['ai', 'architecture'],
    '孩子': ['photo'],
    '教育': ['photo'],
    '社会': ['evidence', 'photo'],
}

MOOD_KEYWORDS = {
    '愤怒': 'angry',
    '抗议': 'angry',
    '保护': 'protective',
    '守护': 'protective',
    '防御': 'protective',
    '严肃': 'solemn',
    '庄重': 'solemn',
    '宣誓': 'solemn',
    '希望': 'hopeful',
    '未来': 'hopeful',
    '激励': 'hopeful',
    '分析': 'analytical',
    '数据': 'analytical',
    '研究': 'analytical',
    '创意': 'creative',
    '灵感': 'creative',
    '温暖': 'warm',
    '关怀': 'warm',
}

VISUAL_STYLE_MAP = {
    '科技': '暗色科技',
    '代码': '暗色科技',
    '系统': '暗色科技',
    '安全': '暗色科技',
    '界面': '界面展示',
    '截图': '文档截图',
    '文档': '文档截图',
    '自然': '明亮自然',
    '生活': '明亮自然',
    '照片': '明亮自然',
    '人物': '人物场景',
    '数据': '数据图表',
    '图表': '数据图表',
}


# ══════════════════════════════════════════════════════════════════════
# 核心匹配逻辑
# ══════════════════════════════════════════════════════════════════════

def extract_scene_params(script_text: str, scene_index: int = 0) -> dict:
    """
    从脚本文本提取场景匹配参数。
    返回: {topic_keywords, content_types, mood, visual_style}
    """
    text_lower = script_text.lower()
    content_types = set()
    mood = '平和'
    visual_style = '暗色科技'

    # 主题→内容类型
    for topic, types in TOPIC_KEYWORDS.items():
        if topic in script_text or topic in text_lower:
            content_types.update(types)

    # 情绪
    for word, m in MOOD_KEYWORDS.items():
        if word in script_text:
            mood = m
            break

    # 视觉风格
    for word, style in VISUAL_STYLE_MAP.items():
        if word in script_text:
            visual_style = style
            break

    return {
        'content_types': list(content_types) if content_types else ['evidence'],
        'mood': mood,
        'visual_style': visual_style,
        'topic_words': [t for t in TOPIC_KEYWORDS if t in script_text],
    }


def match_materials_for_scene(scene_params: dict, count: int = 3,
                               exclude_ids: set = None) -> List[dict]:
    """
    为单个场景匹配素材。
    优先: 内容类型匹配 → 情绪匹配 → 色调匹配
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    content_types = scene_params.get('content_types', [])
    mood = scene_params.get('mood', '')
    visual_style = scene_params.get('visual_style', '')

    conditions = ["m.media_type = 'image'", "m.quality_score >= 0.4"]
    cond_params = []

    # 排除已使用的
    if exclude_ids:
        e_placeholders = ','.join('?' * len(exclude_ids))
        conditions.append(f"m.id NOT IN ({e_placeholders})")
        cond_params.extend(exclude_ids)

    # 内容类型筛选
    if content_types:
        ct_placeholders = ','.join('?' * len(content_types))
        conditions.append(f"m.content_type IN ({ct_placeholders})")
        cond_params.extend(content_types)

    # 简单查询——评分在 Python 里做
    sql = f"""
        SELECT m.* FROM materials m
        WHERE {' AND '.join(conditions)}
        ORDER BY m.quality_score DESC, m.width DESC
        LIMIT {count * 5}
    """

    cur = conn.execute(sql, cond_params)
    candidates = [dict(row) for row in cur.fetchall()]

    # Python 评分
    for c in candidates:
        score = 0
        if c['content_type'] in content_types:
            score += 3
        notes = json.loads(c.get('notes', '{}')) if isinstance(c.get('notes'), str) else (c.get('notes') or {})
        if mood and mood in notes.get('scene_mood', ''):
            score += 2
        if c.get('brightness') in ('dark', 'mid'):
            score += 1
        c['_score'] = score

    candidates.sort(key=lambda x: -x['_score'])
    candidates = [dict(row) for row in cur.fetchall()]

    # 如果不够，用高分素材补充
    if len(candidates) < count:
        exclude_all = exclude_ids | {c['id'] for c in candidates} if exclude_ids else {c['id'] for c in candidates} if candidates else {-1}
        fill_sql = f"""
            SELECT m.*, 0 as match_score FROM materials m
            WHERE m.media_type = 'image' AND m.quality_score >= 0.5
            AND m.id NOT IN ({','.join('?'*len(exclude_all))})
            ORDER BY m.quality_score DESC LIMIT ?
        """
        fill_cur = conn.execute(fill_sql, list(exclude_all) + [count - len(candidates)])
        candidates.extend([dict(row) for row in fill_cur.fetchall()])

    # 去重，取最优 count 个
    seen = set()
    results = []
    for c in candidates:
        if c['id'] not in seen:
            seen.add(c['id'])
            results.append(c)
            if len(results) >= count:
                break

    conn.close()
    return results


def plan_scene_materials(script_path: str, materials_per_scene: int = 3) -> dict:
    """
    完整场景→素材规划。
    读取脚本，分场景，为每个场景匹配素材。
    返回: {scenes: [{text, params, materials}], stats}
    """
    with open(script_path, 'r', encoding='utf-8') as f:
        script_text = f.read()

    # 分场景（按 --- 或空行）
    raw_scenes = re.split(r'\n---\n|\n\n\n+', script_text)
    raw_scenes = [s.strip() for s in raw_scenes if s.strip()]

    result = {'script': script_path, 'total_scenes': len(raw_scenes),
              'materials_per_scene': materials_per_scene, 'scenes': []}

    used_ids = set()
    total_matched = 0

    for i, scene_text in enumerate(raw_scenes):
        params = extract_scene_params(scene_text, i)
        materials = match_materials_for_scene(params, materials_per_scene, used_ids)

        for m in materials:
            used_ids.add(m['id'])

        result['scenes'].append({
            'index': i + 1,
            'text_preview': scene_text[:120] + ('...' if len(scene_text) > 120 else ''),
            'params': params,
            'materials': [{
                'material_id': m['material_id'],
                'filepath': m['filepath'],
                'filename': m['filename'],
                'width': m['width'],
                'height': m['height'],
                'tags': json.loads(m.get('tags', '[]')),
                'suggested_use': json.loads(m.get('notes', '{}')).get('suggested_use', '资料画面'),
                'scene_mood': json.loads(m.get('notes', '{}')).get('scene_mood', ''),
            } for m in materials]
        })
        total_matched += len(materials)

    result['stats'] = {
        'total_materials_matched': total_matched,
        'unique_materials': len(used_ids),
        'coverage': round(total_matched / (len(raw_scenes) * materials_per_scene) * 100, 1),
    }

    return result


def mark_materials_used(material_ids: List[str]):
    """标记素材已使用"""
    conn = sqlite3.connect(str(DB_PATH))
    now = datetime.now().isoformat()
    for mid in material_ids:
        conn.execute(
            "UPDATE materials SET usage_count = usage_count + 1, last_used = ? WHERE material_id = ?",
            (now, mid)
        )
    conn.commit()
    conn.close()


# ══════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='龍魂素材↔视频管线桥接')
    sub = parser.add_subparsers(dest='command')

    p_plan = sub.add_parser('plan', help='为脚本规划素材')
    p_plan.add_argument('script', help='解说稿路径')
    p_plan.add_argument('--per-scene', '-n', type=int, default=3, help='每场景素材数')
    p_plan.add_argument('--output', '-o', help='输出JSON路径')
    p_plan.add_argument('--json', action='store_true', help='JSON输出到stdout')

    p_test = sub.add_parser('test', help='测试场景匹配')
    p_test.add_argument('text', help='测试文本')
    p_test.add_argument('--count', '-n', type=int, default=3, help='返回素材数')

    args = parser.parse_args()

    if args.command == 'plan':
        result = plan_scene_materials(args.script, args.per_scene)

        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"✅ 素材规划已导出 → {out_path}")
        else:
            print(f"\n🎬 脚本素材规划: {args.script}")
            print(f"   场景: {result['total_scenes']} | 每场景素材: {args.per_scene}")
            print(f"   匹配素材: {result['stats']['total_materials_matched']} | 覆盖率: {result['stats']['coverage']}%")
            print()
            for scene in result['scenes']:
                print(f"  📍 场景 {scene['index']}: {scene['text_preview'][:80]}")
                print(f"      参数: 类型={scene['params']['content_types'][:3]} 情绪={scene['params']['mood']} 风格={scene['params']['visual_style']}")
                for m in scene['materials']:
                    tags = ','.join(m['tags'][:3])
                    print(f"      🎞 {m['filename'][:50]:50s} → {m['suggested_use']:6s} [{tags}]")
                print()

    elif args.command == 'test':
        params = extract_scene_params(args.text)
        materials = match_materials_for_scene(params, args.count)
        print(f"\n🎬 场景匹配测试: \"{args.text[:60]}...\"")
        print(f"   匹配参数: {params}")
        print(f"   素材 ({len(materials)}):")
        for m in materials:
            tags = json.loads(m.get('tags', '[]'))
            notes = json.loads(m.get('notes', '{}'))
            print(f"   🎞 {m['filename'][:50]:50s} | {notes.get('scene_category','?'):6s} | {notes.get('scene_mood','?'):4s} | {notes.get('suggested_use','?')}")

    else:
        parser.print_help()
