#!/usr/bin/env python3
import json, requests, sys, hashlib
from datetime import datetime

OLLAMA = "http://localhost:11434/api/generate"
MODEL = "longhun-9622:latest"
WEIGHTS = {"创新":0.30,"支持":0.20,"响应":0.10,"优化":0.10,"风控":0.10,"沟通":0.05,"防御":0.10,"协作":0.05}
GUA = ["乾☰","兑☱","离☲","震☳","巽☴","坎☵","艮☶","坤☷"]

def audit(name, desc):
    prompt = f"""你是64卦审计算法引擎。给以下人格8维度打分(0-10)，只输出JSON，不要任何其他文字：

人格名：{name}
描述：{desc}

输出：{{"创新":X,"支持":X,"响应":X,"优化":X,"风控":X,"沟通":X,"防御":X,"协作":X}}"""

    r = requests.post(OLLAMA, json={"model":MODEL,"prompt":prompt,"stream":False,"format":"json"})
    scores = json.loads(r.json()["response"])

    total = sum(scores[k]*WEIGHTS[k] for k in WEIGHTS)
    dr = int(total * 10)
    while dr >= 10: dr = sum(int(d) for d in str(int(dr*10)))
    dr = dr % 9 or 9

    color = "🟢" if dr in {1,2,4,5,7,8} else ("🟡" if dr==6 else "🔴")

    up = min(round(scores["创新"]*0.3 + scores["沟通"]*0.3 + scores["协作"]*0.4), 7)
    dn = min(round(scores["支持"]*0.3 + scores["风控"]*0.4 + scores["防御"]*0.3), 7)
    gua = f"{GUA[up]}{GUA[dn]}"

    return {
        "人格": name, "8维得分": scores, "加权总分": round(total,2),
        "数字根": dr, "三色": color, "卦象": gua,
        "DNA": f"#龘芯⚡️{datetime.now().strftime('%Y-%m-%d')}-AUDIT-8D-v2.6"
    }

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "🍼 宝宝"
    desc = sys.argv[2] if len(sys.argv) > 2 else "执行层人格·任务执行·承诺兑现·证据保全·审计维护"
    result = audit(target, desc)
    print(json.dumps(result, ensure_ascii=False, indent=2))
