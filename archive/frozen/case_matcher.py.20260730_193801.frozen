# -*- coding: utf-8 -*-
"""
龍魂民生 · 相似案例匹配

从 data/cases/ 案例库按标签相似度匹配。当前为结构占位+本地库读取；
联网裁判文书网默认不启用(数据主权)。
DNA #龍魂⚡️丙午·辛未·CASE-v1
"""

import json
import glob
from pathlib import Path


def match(hits: list[Any], cases_dir: str | None = None) -> list[Any]:
    """按命中标签匹配案例库。返回相似案例列表。"""
    tags = {h["tag"] for h in hits}
    cases_dir = cases_dir or (Path(__file__).resolve().parent.parent / "data" / "cases")
    results = []
    try:
        for fp in glob.glob(str(Path(cases_dir) / "*.json")):
            try:
                data = json.loads(open(fp, encoding="utf-8").read())
            except Exception:
                continue
            ctags = set(data.get("tags", []))
            inter = tags & ctags
            sim = len(inter) / max(1, len(tags | ctags))
            if inter:
                results.append({
                    "dna": data.get("dna", fp),
                    "type": data.get("type", ""),
                    "similarity": round(sim * 100, 1),
                    "result": data.get("result", ""),
                    "lesson": data.get("lesson", ""),
                    "reuse": data.get("reuse", True),
                })
    except Exception as e:
        results.append({"error": f"案例库读取失败: {e}"})
    if not results:
        results.append({"note": "本地案例库为空·建议补充真实案例(数据主权·不联网裁判文书网)"})
    return results


if __name__ == "__main__":
    print(match([{"tag": "#押金陷阱"}]))
