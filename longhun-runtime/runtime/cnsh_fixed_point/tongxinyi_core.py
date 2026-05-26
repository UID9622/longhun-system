from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from datetime import datetime, timezone
from typing import Any


OWNER_VENT = {"我操", "妈的", "艹", "草", "卧槽", "尼玛", "烦死了", "搞死我了", "麻了", "哈哈哈", "嘿嘿"}


@dataclass
class TongxinyiOutput:
    raw_input: str
    input_hash: str
    emotion_intensity: int
    cleaned_text: str
    understanding: str
    prediction: list[str]
    tricolor: str


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12].upper()


def detect_emotion(text: str) -> int:
    if any(w in text for w in ["我操", "妈的", "卧槽", "尼玛"]):
        return 7
    if any(w in text for w in ["烦死了", "麻了", "搞死我了"]):
        return 6
    if any(w in text for w in ["烦", "累", "卡住"]):
        return 4
    if any(w in text for w in ["哈哈哈", "嘿嘿"]):
        return 3
    return 0


def clean_emotion(text: str) -> str:
    out = text
    for w in OWNER_VENT:
        out = out.replace(w, "")
    return re.sub(r"\s+", " ", out).strip()


def predict(text: str) -> list[str]:
    rules = {
        r"bug|报错|错误": "需要定位还是直接修复?",
        r"DNA|追溯|签名": "要确认DNA格式还是落库路径?",
        r"自动|hook|触发": "要先定触发条件和失败回滚吗?",
        r"不说了|算了": "你是想简化流程还是跳过当前块?",
    }
    result: list[str] = []
    for pattern, q in rules.items():
        if re.search(pattern, text, re.IGNORECASE):
            result.append(q)
    return result[:3]


def tongxinyi(raw_input: str) -> TongxinyiOutput:
    emotion = detect_emotion(raw_input)
    cleaned = clean_emotion(raw_input)

    if emotion >= 9:
        tricolor = "🟢"
        understanding = "[VENT] 情绪放行，不执行指令"
    else:
        tricolor = "🟢" if emotion < 8 else "🟡"
        understanding = cleaned if cleaned else raw_input

    return TongxinyiOutput(
        raw_input=raw_input,
        input_hash=_hash(raw_input),
        emotion_intensity=emotion,
        cleaned_text=cleaned,
        understanding=understanding,
        prediction=predict(raw_input),
        tricolor=tricolor,
    )


def to_dict(output: TongxinyiOutput) -> dict[str, Any]:
    return {
        "raw_input": output.raw_input,
        "input_hash": output.input_hash,
        "emotion_intensity": output.emotion_intensity,
        "cleaned_text": output.cleaned_text,
        "understanding": output.understanding,
        "prediction": output.prediction,
        "tricolor": output.tricolor,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
