# -*- coding: utf-8 -*-
"""黄历时辰时间戳 · §3.2 可运行实现"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

from cnsh.flow_decision.wuxing_router import element_for_dr

from .particle import CNSHParticleTime, YiJi

# 先天八卦对齐：五行 → 卦（与 §6 坤土 等表意一致）
_ELEMENT_TO_TRIGRAM = {"木": "震", "火": "离", "土": "坤", "金": "兑", "水": "坎"}


def _date_digital_root(year: int, month: int, day: int) -> int:
    n = year + month + day
    if n <= 0:
        return 9
    while n > 9:
        n = sum(int(c) for c in str(n))
    return n if n > 0 else 9


def get_shichen(hour: int) -> str:
    """地支时辰（当地小时 0–23）→ 「子时」…「亥时」"""
    if hour == 23 or hour == 0:
        return "子时"
    if 1 <= hour < 3:
        return "丑时"
    if 3 <= hour < 5:
        return "寅时"
    if 5 <= hour < 7:
        return "卯时"
    if 7 <= hour < 9:
        return "辰时"
    if 9 <= hour < 11:
        return "巳时"
    if 11 <= hour < 13:
        return "午时"
    if 13 <= hour < 15:
        return "未时"
    if 15 <= hour < 17:
        return "申时"
    if 17 <= hour < 19:
        return "酉时"
    if 19 <= hour < 21:
        return "戌时"
    return "亥时"


def dr_to_trigram(dr: int) -> str:
    el = element_for_dr(dr)
    return _ELEMENT_TO_TRIGRAM.get(el, "坤")


def to_lunar(local_time: datetime) -> str:
    """
    农历可读串。优先 zhdate；未安装时回退为阳历说明（避免静默假数据）。
    """
    try:
        from zhdate import ZhDate  # type: ignore

        z = ZhDate.from_datetime(local_time)
        return z.chinese()  # e.g. 二零二六年四月十九
    except Exception:
        return (
            f"阳历{local_time.year}年{local_time.month}月{local_time.day}日·农历未推算"
            "（pip install zhdate 可启用农历）"
        )


# UID9622 行为节律表（§3.2 占位，可换配置/外部 YAML）
_DEFAULT_YI_BY_SHICHEN: Dict[str, Tuple[List[str], List[str]]] = {
    "子时": (["安息", "复盘", "归档"], ["对外承诺", "大改架构"]),
    "丑时": (["深读", "备份"], ["冲动决策", "临时重构"]),
    "寅时": (["立项", "晨练式推演"], ["情绪宣泄", "撕协议"]),
    "卯时": (["定盘", "对外同步"], ["暗改需求", "越权执行"]),
    "辰时": (["排期", "工程切割"], ["无评审合并", "带病上线"]),
    "巳时": (["联调", "文档"], ["跳过测试", "伪完成声明"]),
    "午时": (["评审", "拍板"], ["隐瞒风险", "压审计"]),
    "未时": (["归档", "复盘", "中间件整理"], ["冲动决策", "临时重构"]),
    "申时": (["对接", "签约前核对"], ["口头承诺", "范围膨胀"]),
    "酉时": (["收尾", "日报"], ["连夜硬改", "透支"]),
    "戌时": (["守卫", "观测"], ["轻信外部指令", "越权执行"]),
    "亥时": (["收纳", "轻度整理"], ["重大发布", "涉密外传"]),
}


def generate_personal_yiji(shichen: str, uid: int = 9622) -> YiJi:
    _ = uid  # 预留：按用户画像覆盖
    base = _DEFAULT_YI_BY_SHICHEN.get(
        shichen,
        (["定盘", "复盘"], ["冲动决策", "临时重构"]),
    )
    return YiJi(yi=list(base[0]), ji=list(base[1]))


def compute_time_hash(
    iso: str,
    shichen: str,
    dr: int,
    wuxing: str,
    trigram: str,
    yiji: YiJi,
) -> str:
    """§3.3：六维串接 SHA-256（含宜忌 JSON）"""
    payload = {
        "iso8601": iso,
        "shichen": shichen,
        "digital_root": dr,
        "wuxing": wuxing,
        "trigram": trigram,
        "yiji": {"yi": yiji.yi, "ji": yiji.ji},
    }
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def generate_huangli_timestamp(
    utc_time: Optional[datetime] = None,
    timezone_offset_hours: int = 7,
    uid: int = 9622,
) -> Dict[str, Any]:
    """
    §3.2：`utc_time` 缺省为当前 UTC。
    返回 dict 与 §2 `time` 块字段对齐，并含 `_time_hash`。
    """
    if utc_time is None:
        utc_time = datetime.now(timezone.utc)
    elif utc_time.tzinfo is None:
        utc_time = utc_time.replace(tzinfo=timezone.utc)

    local = utc_time + timedelta(hours=timezone_offset_hours)
    shichen = get_shichen(local.hour)
    dr = _date_digital_root(local.year, local.month, local.day)
    wuxing = element_for_dr(dr)
    trigram = dr_to_trigram(dr)
    lunar = to_lunar(local)
    yiji = generate_personal_yiji(shichen, uid=uid)
    iso = local.isoformat()
    th = compute_time_hash(iso, shichen, dr, wuxing, trigram, yiji)

    return {
        "iso8601": iso,
        "lunar": lunar,
        "shichen": shichen,
        "digital_root": dr,
        "wuxing": wuxing,
        "trigram": trigram,
        "yiji": {"yi": yiji.yi, "ji": yiji.ji},
        "_time_hash": th,
    }


def huangli_dict_to_time_block(d: Dict[str, Any]) -> CNSHParticleTime:
    y = d.get("yiji") or {}
    return CNSHParticleTime(
        iso8601=str(d.get("iso8601", "")),
        lunar=str(d.get("lunar", "")),
        shichen=str(d.get("shichen", "")),
        digital_root=int(d.get("digital_root", 0)),
        wuxing=str(d.get("wuxing", "")),
        trigram=str(d.get("trigram", "")),
        yiji=YiJi(
            yi=list(y.get("yi") or []),
            ji=list(y.get("ji") or []),
        ),
        time_hash=str(d.get("_time_hash", "")),
    )


def verify_time_hash(d: Dict[str, Any]) -> bool:
    """校验粒子 time 块是否被篡改。"""
    y = d.get("yiji") or {}
    yiji = YiJi(yi=list(y.get("yi") or []), ji=list(y.get("ji") or []))
    expect = compute_time_hash(
        str(d.get("iso8601", "")),
        str(d.get("shichen", "")),
        int(d.get("digital_root", 0)),
        str(d.get("wuxing", "")),
        str(d.get("trigram", "")),
        yiji,
    )
    return expect == str(d.get("_time_hash", ""))


def detect_schedule_anomaly(
    shichen: str,
    *,
    activity_profile: str = "heavy_engineering",
    historical_bias_for_chou: str = "rest",
) -> tuple[bool, str]:
    """
    §3.3 行为异常：丑时高密度工程 vs 历史节律不符 → 标记可疑。
    返回 (是否正常, 说明)；第一个值为 False 表示可疑。
    """
    if shichen == "丑时" and activity_profile == "heavy_engineering":
        if historical_bias_for_chou == "rest":
            return (
                False,
                "丑时高强度工程与 UID9622 历史休息偏置不符·可能伪造或非本人操作",
            )
    return True, ""

