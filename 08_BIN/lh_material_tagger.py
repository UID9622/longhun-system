#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·素材自动标签引擎 v2.0 — 启发式打标 + AI辅助
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-MATERIAL-TAGGER-V2.0-7e1f3d4b
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

启发式规则覆盖 80%+ 素材，AI 只补标不确定的。
"""

import os, sys, json, sqlite3, argparse, subprocess, re
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "material_library.db"


# ══════════════════════════════════════════════════════════════════════
# 场景分类规则引擎
# ══════════════════════════════════════════════════════════════════════

def heuristic_tag(row: dict) -> dict:
    """
    基于文件名、路径、尺寸、颜色等启发式规则打标签。
    返回: {tags, scene_category, scene_mood, visual_style, suggested_use, confidence}
    """
    filename = row.get('filename', '')
    filepath = row.get('filepath', '')
    path_lower = filepath.lower()
    name_lower = filename.lower()
    width = row.get('width') or 0
    height = row.get('height') or 0
    is_portrait = row.get('is_portrait', 0)
    is_screenshot = row.get('is_screenshot', 0)
    brightness = row.get('brightness', 'unknown')
    colors_json = row.get('dominant_colors', '[]')

    tags = set()
    scene_category = '其他'
    scene_mood = '平和'
    visual_style = '界面展示'
    suggested_use = '资料画面'
    confidence = 0.5

    # ─── 步骤1: 文件名模式匹配 ───

    # IMG_xxxx = iPhone 拍照
    if re.match(r'^IMG_\d{4}', filename, re.I):
        tags.add('手机拍摄')
        tags.add('照片')
        source_guess = '生活记录'
        confidence += 0.1

        # HEIC = iPhone 原片
        if filename.lower().endswith('.heic'):
            tags.add('iPhone原片')
            tags.add('高质量')
            confidence += 0.05

        # 竖屏照片 → 生活记录
        if is_portrait:
            scene_category = '生活记录'
            scene_mood = '平和'
            visual_style = '明亮自然'
            suggested_use = '背景'

    # hash-based = 截图/下载
    elif re.match(r'^[a-f0-9]{40}', name_lower):
        tags.add('网络截图')
    elif re.match(r'^[a-f0-9]{32}', name_lower):
        tags.add('网络图片')
    elif name_lower.startswith('image_'):
        tags.add('导入图片')

    # ─── 步骤2: 路径推断 ───

    if 'evidence' in path_lower or '截图' in path_lower:
        tags.add('证据截图')
        scene_category = '证据记录'
        scene_mood = '严肃'
        visual_style = '文档截图'
        suggested_use = '证据展示'
        confidence += 0.2

    if 'screenshot' in path_lower:
        tags.add('截图')
        visual_style = '界面展示'
        confidence += 0.1

    if 'z_s_photo' in path_lower or '照片' in path_lower:
        tags.add('个人照片')
        scene_category = '生活记录'
        suggested_use = '背景'
        confidence += 0.1

    if 'training' in path_lower and 'media' in path_lower:
        tags.add('训练素材')
        confidence += 0.05

    # ─── 步骤3: 尺寸/构图推断 ───

    if width and height:
        ratio = width / height if height else 0

        # 横屏 → 更适合视频背景
        if 1.6 <= ratio <= 2.0:
            suggested_use = '背景'
            tags.add('横屏')
            confidence += 0.05

        # 竖屏 → 手机截图
        if 0.4 <= ratio <= 0.65:
            tags.add('竖屏')
            if is_screenshot:
                tags.add('手机截图')
                visual_style = '界面展示'
                scene_category = '证据记录'
                confidence += 0.1

        # 方形
        if 0.9 <= ratio <= 1.1:
            tags.add('方形')
            suggested_use = '字幕背景'

        # 超宽 → 全景/Banner
        if ratio > 2.0:
            tags.add('超宽屏')
            suggested_use = '片头'
            confidence += 0.05

    # 高分 → 好素材
    if width >= 1920:
        tags.add('高清')
        confidence += 0.1
    elif width >= 1280:
        tags.add('标清')
    else:
        tags.add('低分辨率')

    # ─── 步骤4: 色调推断 ───

    if brightness == 'dark':
        scene_mood = '严肃'
        visual_style = '暗色科技'
        suggested_use = '字幕背景' if suggested_use == '资料画面' else suggested_use
        confidence += 0.05
    elif brightness == 'bright':
        if scene_mood == '平和':
            scene_mood = '激励'
        visual_style = '明亮自然'

    # ─── 步骤5: 颜色分析推断内容 ───

    try:
        colors = json.loads(colors_json) if isinstance(colors_json, str) else colors_json
        if colors:
            main_color = colors[0]
            hex_c = main_color.get('hex', '')

            # 大量蓝色 → 可能代码编辑器
            if main_color.get('tone') == 'cool' and brightness == 'dark':
                tags.add('代码风格')
                scene_category = '技术教学'
                visual_style = '暗色科技'
                scene_mood = '分析'
                suggested_use = '字幕背景'
                confidence += 0.1

            # 大量绿色 → 可能自然风景
            if main_color.get('tone') == 'nature':
                tags.add('自然色调')
                visual_style = '明亮自然'
                scene_category = '生活记录'
                confidence += 0.05
    except:
        pass

    # ─── 步骤6: 文件名关键词额外标签 ───

    keyword_map = {
        'code': ['代码', 'code', '编程', 'github'],
        'architecture': ['架构', 'arch', '系统', '拓扑', 'flow', '流程'],
        'security': ['安全', 'security', '加密', '密钥', '漏洞', 'audit'],
        'culture': ['文化', '易经', '道德经', '哲学', '传统', '龍'],
        'deploy': ['部署', 'deploy', '鲲鹏', 'docker', 'k8s', '服务器'],
        'ai': ['AI', '模型', 'model', '智能', 'agent', '网络', 'neural'],
        'video': ['视频', 'video', '帧', '画面', '场景', 'scene'],
    }

    for tag_name, keywords in keyword_map.items():
        for kw in keywords:
            if kw in name_lower or kw in path_lower:
                tags.add(tag_name)
                if tag_name in ('code', 'architecture', 'security', 'ai'):
                    scene_category = '技术教学'
                elif tag_name == 'culture':
                    scene_category = '文化传承'
                elif tag_name == 'deploy':
                    scene_category = '系统运维'
                elif tag_name == 'video':
                    scene_category = '创意设计'
                    suggested_use = '过渡'
                confidence += 0.05
                break

    # ─── 步骤7: 视频文件特殊处理 ───

    if row.get('media_type') == 'video':
        tags.add('视频素材')
        suggested_use = '过渡'
        scene_category = '创意设计'
        confidence += 0.1

    if row.get('media_type') == 'audio':
        tags.add('音频素材')
        suggested_use = '背景'
        scene_category = '创意设计'
        confidence += 0.1

    # ─── 步骤8: 来源类型推断 ───

    source = row.get('source_type', 'unknown')
    if source == 'phone_camera':
        tags.add('手机拍摄')
    elif source in ('screenshot', 'evidence_screenshot', 'hash_screenshot'):
        tags.add('截图')
    elif source == 'ai_generated':
        tags.add('AI生成')

    # ─── 最终清理 ───

    confidence = min(1.0, round(confidence, 2))

    return {
        'tags': sorted(list(tags)),
        'scene_category': scene_category,
        'scene_mood': scene_mood,
        'visual_style': visual_style,
        'suggested_use': suggested_use,
        'confidence': confidence,
    }


def ai_enhance_tag(row: dict, heuristic_result: dict) -> dict:
    """
    对启发式打分低的素材，用 AI 补标。
    只对 confidence < 0.5 或 tags 为空的素材调用。
    """
    if heuristic_result['confidence'] >= 0.7:
        return heuristic_result

    prompt = f"""你是素材标签助手。给这个文件打标签，输出纯JSON:

文件: {row['filename']}
类型: {row['media_type']} (尺寸:{row.get('width')}x{row.get('height')})
路径: {row['filepath'][-80:]}
已知: {json.dumps(heuristic_result, ensure_ascii=False)}

请确认或纠正，只输出JSON:
{{"tags":["tag1","tag2"],"scene_category":"技术教学|文化传承|系统运维|证据记录|创意设计|生活记录|其他","scene_mood":"严肃|温暖|警示|激励|平和|紧张","visual_style":"暗色科技|明亮自然|文档截图|界面展示|人物场景|数据图表","suggested_use":"片头|背景|过渡|字幕背景|证据展示|资料画面","confidence":0.5}}"""

    try:
        result = subprocess.run(
            ['ollama', 'run', 'longhun-v4.0:q4', prompt],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            response = result.stdout.strip()
            # 清理 ANSI 转义码
            clean = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', response)
            # 提取 JSON
            start = clean.find('{')
            end = clean.rfind('}') + 1
            if start >= 0 and end > start:
                ai_result = json.loads(clean[start:end])
                # 清洗结果（AI可能返回完整的选项列表而非单选）
                for field in ['scene_category', 'scene_mood', 'visual_style', 'suggested_use']:
                    val = ai_result.get(field, '')
                    if '|' in val:
                        # 取第一个选项
                        ai_result[field] = val.split('|')[0].strip('/').strip()
                    if '/' in val and '|' not in val:
                        ai_result[field] = val.split('/')[0].strip()
                return ai_result
    except Exception:
        pass

    return heuristic_result


# ══════════════════════════════════════════════════════════════════════
# 批量打标
# ══════════════════════════════════════════════════════════════════════

def tag_all(limit: int = None, ai_fallback: bool = False, verbose: bool = False):
    """全量打标素材库"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    sql = """
        SELECT * FROM materials
        WHERE media_type IN ('image', 'video', 'audio')
          AND (tags = '[]' OR tags IS NULL OR json_array_length(tags) = 0)
        ORDER BY quality_score DESC
    """
    if limit:
        sql += f" LIMIT {limit}"

    rows = conn.execute(sql).fetchall()
    print(f"\n🏷️ 龍魂素材标签引擎 v2.0")
    print(f"   待打标: {len(rows)} 个素材")
    print(f"   模式: {'启发式+AI补标' if ai_fallback else '纯启发式'}\n")

    stats = {
        'tagged': 0, 'ai_enhanced': 0, 'skipped': 0,
        'by_category': {}, 'by_style': {}, 'by_mood': {}
    }

    for i, row in enumerate(rows):
        # 启发式打标
        result = heuristic_tag(dict(row))

        # AI 补标（可选）
        if ai_fallback and result['confidence'] < 0.5:
            result = ai_enhance_tag(dict(row), result)
            stats['ai_enhanced'] += 1

        # 写入数据库
        tags_json = json.dumps(result.get('tags', []), ensure_ascii=False)
        notes = json.dumps({
            'scene_category': result.get('scene_category', '其他'),
            'scene_mood': result.get('scene_mood', '平和'),
            'visual_style': result.get('visual_style', '界面展示'),
            'suggested_use': result.get('suggested_use', '资料画面'),
            'tag_confidence': result.get('confidence', 0.5),
            'tagged_at': datetime.now().isoformat(),
            'tag_method': 'heuristic+ai' if ai_fallback else 'heuristic',
        }, ensure_ascii=False)

        conn.execute(
            "UPDATE materials SET tags = ?, notes = ? WHERE id = ?",
            (tags_json, notes, row['id'])
        )
        stats['tagged'] += 1

        # 统计
        cat = result.get('scene_category', '其他')
        stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1
        style = result.get('visual_style', '未知')
        stats['by_style'][style] = stats['by_style'].get(style, 0) + 1
        mood = result.get('scene_mood', '平和')
        stats['by_mood'][mood] = stats['by_mood'].get(mood, 0) + 1

        if verbose or (i + 1) % 50 == 0:
            tags_str = ','.join(result.get('tags', [])[:5])
            print(f"   [{i+1:3d}/{len(rows)}] {row['filename'][:40]:40s} → {result.get('scene_category','?'):6s} | {result.get('suggested_use','?'):6s} | [{tags_str}]")

    conn.commit()

    # 打印汇总
    print(f"\n{'='*50}")
    print(f"✅ 打标完成: {stats['tagged']} 个 (AI辅助: {stats['ai_enhanced']})")
    print(f"\n📊 场景分类:")
    for cat, cnt in sorted(stats['by_category'].items(), key=lambda x: -x[1]):
        bar = '█' * min(cnt, 30)
        print(f"   {cat:8s} {cnt:4d} {bar}")
    print(f"\n📊 视觉风格:")
    for style, cnt in sorted(stats['by_style'].items(), key=lambda x: -x[1]):
        print(f"   {style:10s} {cnt:4d}")
    print(f"\n📊 情绪分布:")
    for mood, cnt in sorted(stats['by_mood'].items(), key=lambda x: -x[1]):
        print(f"   {mood:8s} {cnt:4d}")

    conn.close()


# ══════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='龍魂素材标签引擎 v2.0')
    parser.add_argument('--limit', '-n', type=int, help='批处理数量')
    parser.add_argument('--ai', action='store_true', help='启用AI补标（低置信度）')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')

    args = parser.parse_args()
    tag_all(limit=args.limit, ai_fallback=args.ai, verbose=args.verbose)
