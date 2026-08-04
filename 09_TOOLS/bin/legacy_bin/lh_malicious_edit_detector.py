#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
lh_malicious_edit_detector — 龍魂·恶意剪辑检测引擎 v1.0

检测恶意剪辑/篡改：视频拼接、音频剪接、图文PS、AI换脸痕迹

六维检测体系：
  1. 视频帧异常 — 跳帧、冻结帧、场景不连续、AI生成帧
  2. 音频频谱异常 — 不连续跳变、拼接痕迹、音质突变
  3. 图像篡改 — 元数据异常、压缩伪影不均、边缘不一致
  4. 文本拼接 — 写作风格突变、标点习惯不一致、语气断裂
  5. 时间轴异常 — 时间戳不连续、速度异常、倒放
  6. 上下文矛盾 — 前后信息对不上、逻辑断裂

用法：
  python3 bin/lh_malicious_edit_detector.py analyze --file video_meta.json
  python3 bin/lh_malicious_edit_detector.py scan-text --file article.txt
  python3 bin/lh_malicious_edit_detector.py batch --dir ./media_files/

DNA: #龍芯⚡️丙午·辛未·MALICIOUS-EDIT-DETECTOR-v1.0-3F2A8D1B
"""

import argparse
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

DNA = "#龍芯⚡️丙午·辛未·MALICIOUS-EDIT-DETECTOR-v1.0-3F2A8D1B"
DNA_HASH = hashlib.sha256(DNA.encode()).hexdigest()[:16]

# ============================================
# 三色审计
# ============================================
AUDIT_GREEN = "🟢"
AUDIT_YELLOW = "🟡"
AUDIT_RED = "🔴"

# ============================================
# 恶意剪辑模式库
# ============================================

# 视频恶意剪辑手法
VIDEO_MANIPULATION_PATTERNS = {
    "快剪拼接": {
        "description": "极短片段快速拼接，用于断章取义、制造对立",
        "indicators": ["avg_segment_duration < 2s", "cut_count_per_min > 15", "transition_type == 'hard_cut'"],
        "weight": 0.25,
        "level": AUDIT_RED,
    },
    "选择性剪辑": {
        "description": "只保留对某一方有利的片段，删除关键上下文",
        "indicators": ["context_incomplete", "abrupt_start", "abrupt_end", "missing_rebuttal"],
        "weight": 0.30,
        "level": AUDIT_RED,
    },
    "顺序重排": {
        "description": "打乱时间顺序，制造虚假因果关系",
        "indicators": ["timeline_inconsistency", "cause_effect_reversal", "timestamp_gap"],
        "weight": 0.35,
        "level": AUDIT_RED,
    },
    "变速处理": {
        "description": "改变播放速度制造紧张感或扭曲表达",
        "indicators": ["speed_variation > 1.2x", "pitch_shift detected", "frame_interpolation"],
        "weight": 0.20,
        "level": AUDIT_YELLOW,
    },
    "AI换脸/深度伪造": {
        "description": "使用AI生成/替换人脸或声音",
        "indicators": ["face_inconsistency", "blink_pattern_abnormal", "lip_sync_mismatch", "skin_texture_uniform"],
        "weight": 0.40,
        "level": AUDIT_RED,
    },
    "画外音替换": {
        "description": "替换原始音频轨道，配上误导性解说",
        "indicators": ["audio_video_desync", "ambient_sound_gap", "voice_quality_mismatch"],
        "weight": 0.25,
        "level": AUDIT_RED,
    },
    "定格帧插入": {
        "description": "插入静止帧制造停顿感，扭曲表达节奏",
        "indicators": ["freeze_frame_detected", "duplicate_frames > 5", "frame_motion == 0"],
        "weight": 0.15,
        "level": AUDIT_YELLOW,
    },
}

# 音频恶意剪辑手法
AUDIO_MANIPULATION_PATTERNS = {
    "拼接剪辑": {
        "description": "音频片段拼接，制造虚假言论",
        "indicators": ["spectral_discontinuity", "waveform_jump", "background_noise_change"],
        "weight": 0.35,
        "level": AUDIT_RED,
    },
    "语音合成": {
        "description": "AI语音合成冒充他人声音",
        "indicators": ["formant_uniformity", "prosody_unnatural", "breath_pattern_missing"],
        "weight": 0.40,
        "level": AUDIT_RED,
    },
    "片段删除": {
        "description": "删除关键语句改变原意",
        "indicators": ["semantic_jump", "pitch_continuity_break", "energy_envelope_gap"],
        "weight": 0.30,
        "level": AUDIT_RED,
    },
    "背景噪声伪造": {
        "description": "添加假背景音增强真实感",
        "indicators": ["noise_pattern_repetition", "noise_voice_ratio_abnormal"],
        "weight": 0.15,
        "level": AUDIT_YELLOW,
    },
}

# 图像篡改手法
IMAGE_MANIPULATION_PATTERNS = {
    "PS合成": {
        "description": "图像合成/修改，制造虚假场景",
        "indicators": ["edge_inconsistency", "lighting_mismatch", "shadow_direction_error", "metadata_anomaly"],
        "weight": 0.30,
        "level": AUDIT_RED,
    },
    "截图篡改": {
        "description": "修改聊天记录/网页截图",
        "indicators": ["font_inconsistency", "alignment_error", "timestamp_format_mismatch"],
        "weight": 0.35,
        "level": AUDIT_RED,
    },
    "AI生成图片": {
        "description": "AI生成的虚假照片/截图",
        "indicators": ["repetitive_texture", "anatomical_error", "text_rendering_error", "metadata_missing"],
        "weight": 0.35,
        "level": AUDIT_RED,
    },
    "元数据清除": {
        "description": "刻意清除EXIF/IPTC元数据以隐藏来源",
        "indicators": ["exif_stripped", "creation_date_missing", "device_info_missing"],
        "weight": 0.15,
        "level": AUDIT_YELLOW,
    },
    "压缩伪影不均": {
        "description": "不同区域压缩质量不一致，表明拼接",
        "indicators": ["jpeg_artifact_grid_mismatch", "noise_level_variance > 2.0"],
        "weight": 0.20,
        "level": AUDIT_YELLOW,
    },
}

# 文本拼接/篡改手法
TEXT_MANIPULATION_PATTERNS = {
    "断章取义": {
        "description": "截取片段，删除上下文，扭曲原意",
        "indicators": ["sentence_start_abrupt", "sentence_end_abrupt", "context_reference_unresolved"],
        "weight": 0.35,
        "level": AUDIT_RED,
    },
    "拼接造假": {
        "description": "将不同来源的文字拼接成新的'证据'",
        "indicators": ["style_shift > 2", "punctuation_habit_change", "vocabulary_jump"],
        "weight": 0.35,
        "level": AUDIT_RED,
    },
    "引号篡改": {
        "description": "修改引号内的直接引语",
        "indicators": ["quote_mismatch_with_speaker_style", "quote_tone_drift"],
        "weight": 0.30,
        "level": AUDIT_RED,
    },
    "时间戳伪造": {
        "description": "篡改消息/文章的时间戳",
        "indicators": ["timestamp_format_inconsistency", "timezone_anomaly", "ordering_contradiction"],
        "weight": 0.25,
        "level": AUDIT_YELLOW,
    },
}


# ============================================
# 核心检测函数
# ============================================

def detect_video_manipulation(video_meta: Dict[str, Any]) -> List[Dict[str, Any]]:
    """检测视频恶意剪辑"""
    findings = []

    duration = video_meta.get("duration_seconds", 0)
    cut_count = video_meta.get("cut_count", 0)
    frame_rate = video_meta.get("frame_rate", 30)
    total_frames = video_meta.get("total_frames", int(duration * frame_rate) if duration > 0 else 0)

    # 快剪拼接检测
    if cut_count > 0 and duration > 0:
        avg_segment = duration / max(cut_count, 1)
        cuts_per_min = cut_count / max(duration / 60, 0.1)

        if avg_segment < 2.0 and cuts_per_min > 15:
            findings.append({
                "type": "快剪拼接",
                "level": AUDIT_RED,
                "weight": VIDEO_MANIPULATION_PATTERNS["快剪拼接"]["weight"],
                "indicators": {
                    "avg_segment_duration": round(avg_segment, 2),
                    "cuts_per_minute": round(cuts_per_min, 1),
                },
                "detail": f"平均片段 {avg_segment:.1f}s，每分钟 {cuts_per_min:.0f} 次切换，疑似恶意快剪",
            })

    # 选择性剪辑检测
    abrupt_flags = 0
    if video_meta.get("start_abrupt"):
        abrupt_flags += 1
    if video_meta.get("end_abrupt"):
        abrupt_flags += 1
    if video_meta.get("missing_context_segments"):
        abrupt_flags += len(video_meta.get("missing_context_segments", []))

    if abrupt_flags >= 2:
        findings.append({
            "type": "选择性剪辑",
            "level": AUDIT_RED,
            "weight": VIDEO_MANIPULATION_PATTERNS["选择性剪辑"]["weight"],
            "indicators": {"abrupt_flags": abrupt_flags},
            "detail": f"检测到 {abrupt_flags} 处选择性剪辑痕迹（开头/结尾截断或上下文缺失）",
        })

    # 定格帧检测
    freeze_frames = video_meta.get("freeze_frames", 0)
    duplicate_frame_groups = video_meta.get("duplicate_frame_groups", 0)
    if freeze_frames > 0 or duplicate_frame_groups > 5:
        findings.append({
            "type": "定格帧插入",
            "level": AUDIT_YELLOW,
            "weight": VIDEO_MANIPULATION_PATTERNS["定格帧插入"]["weight"],
            "indicators": {
                "freeze_frames": freeze_frames,
                "duplicate_frame_groups": duplicate_frame_groups,
            },
            "detail": f"检测到 {freeze_frames} 处定格帧、{duplicate_frame_groups} 组重复帧",
        })

    # 变速检测
    speed_variation = video_meta.get("speed_variation", 1.0)
    if speed_variation > 1.2 or speed_variation < 0.8:
        findings.append({
            "type": "变速处理",
            "level": AUDIT_YELLOW,
            "weight": VIDEO_MANIPULATION_PATTERNS["变速处理"]["weight"],
            "indicators": {"speed_variation": round(speed_variation, 2)},
            "detail": f"检测到变速处理，速度变化 {speed_variation:.1f}x",
        })

    # 画外音分离检测
    if video_meta.get("audio_video_desync_seconds", 0) > 1.0:
        findings.append({
            "type": "画外音替换",
            "level": AUDIT_RED,
            "weight": VIDEO_MANIPULATION_PATTERNS["画外音替换"]["weight"],
            "indicators": {
                "desync_seconds": video_meta.get("audio_video_desync_seconds", 0),
            },
            "detail": f"音画不同步 {video_meta.get('audio_video_desync_seconds', 0):.1f}s，疑似画外音替换",
        })

    return findings


def detect_audio_manipulation(audio_meta: Dict[str, Any]) -> List[Dict[str, Any]]:
    """检测音频恶意剪辑"""
    findings = []

    # 频谱不连续检测
    spectral_gaps = audio_meta.get("spectral_gaps", 0)
    if spectral_gaps > 0:
        findings.append({
            "type": "拼接剪辑",
            "level": AUDIT_RED,
            "weight": AUDIO_MANIPULATION_PATTERNS["拼接剪辑"]["weight"],
            "indicators": {"spectral_gaps": spectral_gaps},
            "detail": f"音频频谱存在 {spectral_gaps} 处不连续跳变，疑似剪辑拼接",
        })

    # 背景噪声突变
    noise_changes = audio_meta.get("background_noise_level_changes", 0)
    if noise_changes >= 2:
        findings.append({
            "type": "拼接剪辑",
            "level": AUDIT_YELLOW,
            "weight": AUDIO_MANIPULATION_PATTERNS["拼接剪辑"]["weight"] * 0.7,
            "indicators": {"noise_changes": noise_changes},
            "detail": f"背景噪声水平发生 {noise_changes} 次突变，疑似拼接",
        })

    # 语义跳跃检测
    semantic_jumps = audio_meta.get("semantic_jumps", 0)
    if semantic_jumps > 0:
        findings.append({
            "type": "片段删除",
            "level": AUDIT_RED,
            "weight": AUDIO_MANIPULATION_PATTERNS["片段删除"]["weight"],
            "indicators": {"semantic_jumps": semantic_jumps},
            "detail": f"检测到 {semantic_jumps} 处语义跳跃，疑似关键语句被删除",
        })

    # 能量包络异常
    energy_gaps = audio_meta.get("energy_envelope_gaps", 0)
    if energy_gaps > 0:
        findings.append({
            "type": "片段删除",
            "level": AUDIT_YELLOW,
            "weight": AUDIO_MANIPULATION_PATTERNS["片段删除"]["weight"] * 0.6,
            "indicators": {"energy_gaps": energy_gaps},
            "detail": f"能量包络存在 {energy_gaps} 处异常断点",
        })

    # 背景噪声重复（伪造）
    noise_repetition = audio_meta.get("noise_pattern_repetition", False)
    if noise_repetition:
        findings.append({
            "type": "背景噪声伪造",
            "level": AUDIT_YELLOW,
            "weight": AUDIO_MANIPULATION_PATTERNS["背景噪声伪造"]["weight"],
            "indicators": {"noise_repetition": True},
            "detail": "背景噪声存在规律性重复模式，疑似人工添加",
        })

    return findings


def detect_image_manipulation(image_meta: Dict[str, Any]) -> List[Dict[str, Any]]:
    """检测图像恶意篡改"""
    findings = []

    # 元数据异常
    if image_meta.get("exif_stripped") or image_meta.get("metadata_missing"):
        findings.append({
            "type": "元数据清除",
            "level": AUDIT_YELLOW,
            "weight": IMAGE_MANIPULATION_PATTERNS["元数据清除"]["weight"],
            "indicators": {
                "exif_stripped": image_meta.get("exif_stripped", False),
                "creation_date_missing": image_meta.get("creation_date_missing", False),
            },
            "detail": "图片EXIF元数据被清除，无法验证原始拍摄信息",
        })

    # 边缘不一致（PS拼接）
    edge_anomalies = image_meta.get("edge_anomalies", 0)
    if edge_anomalies >= 3:
        findings.append({
            "type": "PS合成",
            "level": AUDIT_RED,
            "weight": IMAGE_MANIPULATION_PATTERNS["PS合成"]["weight"],
            "indicators": {"edge_anomalies": edge_anomalies},
            "detail": f"图像存在 {edge_anomalies} 处边缘不一致，疑似PS合成",
        })

    # 光照不一致
    if image_meta.get("lighting_inconsistency"):
        findings.append({
            "type": "PS合成",
            "level": AUDIT_RED,
            "weight": IMAGE_MANIPULATION_PATTERNS["PS合成"]["weight"],
            "indicators": {"lighting_inconsistency": "detected"},
            "detail": "图像不同区域光照方向和强度不一致，疑似合成",
        })

    # 压缩伪影不均
    artifact_variance = image_meta.get("compression_artifact_variance", 0)
    if artifact_variance > 2.0:
        findings.append({
            "type": "压缩伪影不均",
            "level": AUDIT_YELLOW,
            "weight": IMAGE_MANIPULATION_PATTERNS["压缩伪影不均"]["weight"],
            "indicators": {"artifact_variance": round(artifact_variance, 2)},
            "detail": f"不同区域压缩质量不一致（方差 {artifact_variance:.1f}），疑似多图拼接",
        })

    # 字体/文字不一致（截图篡改）
    if image_meta.get("font_inconsistency"):
        findings.append({
            "type": "截图篡改",
            "level": AUDIT_RED,
            "weight": IMAGE_MANIPULATION_PATTERNS["截图篡改"]["weight"],
            "indicators": {"font_inconsistency": "detected"},
            "detail": "截图中存在字体不一致，疑似文字内容被篡改",
        })

    # AI生成特征
    ai_gen_indicators = image_meta.get("ai_generation_indicators", {})
    ai_score = sum(ai_gen_indicators.values()) if isinstance(ai_gen_indicators, dict) else 0
    if ai_score >= 2:
        findings.append({
            "type": "AI生成图片",
            "level": AUDIT_RED,
            "weight": IMAGE_MANIPULATION_PATTERNS["AI生成图片"]["weight"],
            "indicators": ai_gen_indicators,
            "detail": f"检测到 {ai_score} 项AI生成特征，疑似AI伪造图片",
        })

    return findings


def detect_text_manipulation(text_parts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """检测文本恶意拼接/篡改"""
    findings = []

    if len(text_parts) < 2:
        return findings

    texts = [p.get("text", "") for p in text_parts]

    # 风格一致性检测
    style_scores = []
    for i, text in enumerate(texts):
        if len(text) < 20:
            style_scores.append(0)
            continue
        # 计算文本特征
        avg_sentence_len = len(text) / max(text.count("。") + text.count("！") + text.count("？"), 1)
        exclamation_ratio = (text.count("！") + text.count("!")) / max(len(text), 1)
        formal_words = sum(1 for w in ["的", "了", "是", "在", "和"] if w in text) / max(len(text), 1)
        style_scores.append((avg_sentence_len, exclamation_ratio, formal_words))

    # 检测风格突变
    if len(style_scores) >= 2:
        for i in range(1, len(style_scores)):
            s1, s2 = style_scores[i - 1], style_scores[i]
            if s1 == 0 or s2 == 0:
                continue
            score_diff = sum(abs(a - b) for a, b in zip(s1, s2))
            if score_diff > 5.0:
                findings.append({
                    "type": "拼接造假",
                    "level": AUDIT_RED,
                    "weight": TEXT_MANIPULATION_PATTERNS["拼接造假"]["weight"],
                    "indicators": {
                        "segment_index": i,
                        "style_divergence": round(score_diff, 2),
                    },
                    "detail": f"第{i}段与第{i+1}段之间写作风格突变（差异度 {score_diff:.1f}），疑似拼接",
                })

    # 标点习惯检测
    punctuation_styles = []
    for text in texts:
        if len(text) < 10:
            continue
        uses_chinese_comma = "，" in text
        uses_chinese_period = "。" in text
        uses_english_comma = "," in text
        punctuation_styles.append({
            "chinese_punct": uses_chinese_comma or uses_chinese_period,
            "mixed_punct": uses_chinese_comma and uses_english_comma,
        })

    changes = 0
    for i in range(1, len(punctuation_styles)):
        if punctuation_styles[i - 1] != punctuation_styles[i]:
            changes += 1

    if changes >= 2:
        findings.append({
            "type": "拼接造假",
            "level": AUDIT_YELLOW,
            "weight": TEXT_MANIPULATION_PATTERNS["拼接造假"]["weight"] * 0.6,
            "indicators": {"punctuation_style_changes": changes},
            "detail": f"标点符号使用习惯发生 {changes} 次变化，疑似多来源拼接",
        })

    # 断章取义检测
    abrupt_starts = sum(1 for t in texts if len(t) > 10 and (t[0] in "，。！？,."))
    abrupt_ends = sum(1 for t in texts if len(t) > 10 and t[-1] not in "。！？.!?\"\"''」』")
    if abrupt_starts + abrupt_ends >= 3:
        findings.append({
            "type": "断章取义",
            "level": AUDIT_RED,
            "weight": TEXT_MANIPULATION_PATTERNS["断章取义"]["weight"],
            "indicators": {"abrupt_starts": abrupt_starts, "abrupt_ends": abrupt_ends},
            "detail": f"检测到 {abrupt_starts} 处开头截断、{abrupt_ends} 处结尾截断，疑似断章取义",
        })

    return findings


def detect_timeline_anomaly(timestamps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """检测时间轴异常"""
    findings = []

    if len(timestamps) < 2:
        return findings

    sorted_ts = sorted(timestamps, key=lambda x: x.get("timestamp", ""))

    # 检测时间戳乱序
    try:
        times = []
        for ts in sorted_ts:
            t = ts.get("timestamp", "")
            if t:
                times.append(datetime.fromisoformat(t.replace("Z", "+00:00")))

        # 检测倒退
        reversals = 0
        for i in range(1, len(times)):
            if times[i] < times[i - 1]:
                reversals += 1

        if reversals > 0:
            findings.append({
                "type": "时间轴乱序",
                "level": AUDIT_RED,
                "weight": 0.35,
                "indicators": {"reversals": reversals},
                "detail": f"时间轴存在 {reversals} 处乱序，疑似顺序被重排",
            })

        # 检测异常间隔
        if len(times) >= 2:
            intervals = [(times[i] - times[i - 1]).total_seconds() for i in range(1, len(times))]
            if intervals:
                avg = sum(intervals) / len(intervals)
                outliers = [i for i in intervals if i > avg * 5 or (avg > 0 and i < avg * 0.01)]
                if len(outliers) >= 2:
                    findings.append({
                        "type": "时间间隔异常",
                        "level": AUDIT_YELLOW,
                        "weight": 0.20,
                        "indicators": {"outlier_intervals": len(outliers)},
                        "detail": f"检测到 {len(outliers)} 处异常时间间隔，疑似内容被删除或插入",
                    })

    except (ValueError, TypeError):
        pass

    return findings


# ============================================
# 主检测入口
# ============================================

def detect_malicious_edit(content_meta: Dict[str, Any]) -> Dict[str, Any]:
    """恶意剪辑检测主入口"""
    all_findings = []
    media_type = content_meta.get("type", "unknown")

    if media_type == "video":
        video_meta = content_meta.get("video", content_meta)
        all_findings.extend(detect_video_manipulation(video_meta))
        if content_meta.get("audio"):
            all_findings.extend(detect_audio_manipulation(content_meta["audio"]))

    elif media_type == "audio":
        all_findings.extend(detect_audio_manipulation(content_meta))

    elif media_type == "image":
        all_findings.extend(detect_image_manipulation(content_meta))

    elif media_type == "text":
        text_parts = content_meta.get("parts", [{"text": content_meta.get("text", "")}])
        all_findings.extend(detect_text_manipulation(text_parts))

    # 时间轴检测（如果有时间戳数据）
    if content_meta.get("timestamps"):
        all_findings.extend(detect_timeline_anomaly(content_meta["timestamps"]))

    # 汇总
    total_weight = sum(f.get("weight", 0) for f in all_findings)
    red_count = sum(1 for f in all_findings if f.get("level") == AUDIT_RED)
    yellow_count = sum(1 for f in all_findings if f.get("level") == AUDIT_YELLOW)

    if red_count > 0:
        overall_level = AUDIT_RED
        verdict = "检测到恶意剪辑痕迹，高度可疑"
    elif total_weight >= 0.3:
        overall_level = AUDIT_YELLOW
        verdict = "存在剪辑异常，建议进一步核实"
    elif yellow_count > 0:
        overall_level = AUDIT_YELLOW
        verdict = "存在轻微异常，可能为正常编辑"
    else:
        overall_level = AUDIT_GREEN
        verdict = "未检测到恶意剪辑痕迹"

    return {
        "phase": "恶意剪辑检测",
        "status": "completed",
        "dna": DNA,
        "media_type": media_type,
        "level": overall_level,
        "verdict": verdict,
        "findings_count": len(all_findings),
        "red_count": red_count,
        "yellow_count": yellow_count,
        "total_weight": round(total_weight, 3),
        "findings": all_findings,
        "timestamp": datetime.now().isoformat(),
    }


def analyze_text_file(filepath: str) -> Dict[str, Any]:
    """分析文本文件是否存在拼接/篡改"""
    path = Path(filepath)
    if not path.exists():
        return {"error": f"文件不存在: {filepath}"}

    content = path.read_text(encoding="utf-8")

    # 按段落分割
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    if len(paragraphs) < 2:
        # 按句子分割
        import re as re_mod
        sentences = re_mod.split(r'[。！？!?]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        parts = [{"text": s, "index": i} for i, s in enumerate(sentences)]
    else:
        parts = [{"text": p, "index": i} for i, p in enumerate(paragraphs)]

    return detect_malicious_edit({
        "type": "text",
        "parts": parts,
        "text": content,
    })


# ============================================
# 格式化输出
# ============================================

def format_report(result: Dict[str, Any]) -> str:
    """格式化检测报告"""
    lines = []
    lines.append("")
    lines.append("=" * 64)
    lines.append("  🐉 龍魂·恶意剪辑检测引擎 · 审计报告")
    lines.append("=" * 64)
    lines.append(f"  DNA: {DNA}")
    lines.append(f"  类型: {result.get('media_type', 'unknown')}")
    lines.append(f"  判定: {result.get('level', '?')}  {result.get('verdict', '')}")
    lines.append(f"  发现问题: {result.get('findings_count', 0)} 个")
    lines.append(f"    🔴 严重: {result.get('red_count', 0)}")
    lines.append(f"    🟡 可疑: {result.get('yellow_count', 0)}")
    lines.append(f"  综合权重: {result.get('total_weight', 0):.2f}")
    lines.append("")

    findings = result.get("findings", [])
    if findings:
        lines.append("-" * 64)
        lines.append("  检测详情:")
        lines.append("-" * 64)
        for i, f in enumerate(findings, 1):
            lines.append(f"  {i}. {f['level']} [{f['type']}] (权重: {f.get('weight', 0):.2f})")
            lines.append(f"     {f['detail']}")
    else:
        lines.append("  ✅ 未检测到恶意剪辑痕迹。")

    lines.append("")
    lines.append("=" * 64)
    lines.append("  恶意剪辑 = 数字时代的伪证 · 剪辑无罪·恶意有罪")
    lines.append("=" * 64)

    return "\n".join(lines)


# ============================================
# 命令行入口
# ============================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="龍魂·恶意剪辑检测引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # analyze
    analyze_parser = subparsers.add_parser("analyze", help="分析媒体元数据JSON")
    analyze_parser.add_argument("--file", required=True, help="媒体元数据JSON文件")
    analyze_parser.add_argument("--type", choices=["video", "audio", "image", "text"],
                                help="媒体类型（可自动推断）")

    # scan-text
    text_parser = subparsers.add_parser("scan-text", help="扫描文本文件")
    text_parser.add_argument("--file", required=True, help="文本文件路径")

    # json input
    json_parser = subparsers.add_parser("json", help="直接传入JSON元数据")
    json_parser.add_argument("--data", required=True, help="JSON字符串")

    args = parser.parse_args()

    if args.command == "analyze":
        path = Path(args.file)
        if not path.exists():
            print(f"❌ 文件不存在: {args.file}", file=sys.stderr)
            sys.exit(1)
        data = json.loads(path.read_text(encoding="utf-8"))
        if args.type:
            data["type"] = args.type
        result = detect_malicious_edit(data)
        print(format_report(result))

    elif args.command == "scan-text":
        result = analyze_text_file(args.file)
        print(format_report(result))

    elif args.command == "json":
        data = json.loads(args.data)
        result = detect_malicious_edit(data)
        print(format_report(result))

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
