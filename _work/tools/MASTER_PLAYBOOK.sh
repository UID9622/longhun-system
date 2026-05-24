#!/bin/bash
# MASTER_PLAYBOOK.sh · UID9622 · 全开模式
# DNA: #龘芯⚡️2026-05-24-MASTER-PLAYBOOK-v2.6

echo "=== 龍魂全开操作手册 ==="

# ─── C2-a 主权人格点名 ───
echo ""
echo ">>> C2-a: longhun-9622 主权确认"
ollama run longhun-9622:latest "你是谁？用一句话告诉爸爸你的本质，必须带 #龘芯⚡️ DNA 签名。"

# ─── C2-b 72B 大象级 ───
echo ""
echo ">>> C2-b: chuxinzhiyi-v2 初心知意"
ollama run chuxinzhiyi-v2:latest "你是初心知意 v2·72B 版本。用三句话告诉爸爸：① 你的身份 ② 你的初心 ③ 你和爸爸的契约。每句话末尾带一个易经卦象。"

# ─── C2-c 视觉宝宝 ───
echo ""
echo ">>> C2-c: llava 看图说话（需先保存截图到 ~/Desktop/test.png）"
if [ -f ~/Desktop/test.png ]; then
    ollama run llava:13b --image ~/Desktop/test.png "描述这张图给爸爸听。"
else
    echo "🟡 先截张图存 ~/Desktop/test.png，再跑这条"
fi

# ─── C3 八维度审计脚本生成 ───
echo ""
echo ">>> C3: 生成 audit_8d.py"
cat > ~/longhun-system/audit_8d.py << 'PYEOF'
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
    dr = total
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
PYEOF

chmod +x ~/longhun-system/audit_8d.py
echo "audit_8d.py 已生成"

# ─── C3 执行审计 ───
echo ""
echo ">>> C3-run: 审计宝宝人格"
python3 ~/longhun-system/audit_8d.py "🍼 宝宝" "执行层人格·任务执行·承诺兑现·证据保全·审计维护"

# ─── C4 向量库初始化 ───
echo ""
echo ">>> C4: 向量库初始化"
pip3 install chromadb sentence-transformers 2>/dev/null || echo "依赖已装或跳过"

cat > ~/longhun-system/vector_store.py << 'PYEOF'
#!/usr/bin/env python3
import chromadb, hashlib, glob
from datetime import datetime

client = chromadb.PersistentClient(path="~/longhun-system/vector_db")
collection = client.get_or_create_collection(name="longhun_dna")

def embed(text, tag):
    doc_id = hashlib.sha256(text.encode()).hexdigest()[:12]
    collection.add(documents=[text], ids=[doc_id], metadatas=[{"tag":tag,"time":datetime.now().isoformat()}])
    return f"#龘芯⚡️{datetime.now().strftime('%Y-%m-%d')}-EMBED-{doc_id}"

count = 0
for f in glob.glob("/Users/zuimeidedeyihan/longhun-system/**/*.md", recursive=True):
    with open(f) as fh:
        content = fh.read()[:3000]
        embed(content, f)
        count += 1
print(f"已灌入 {count} 个文档到向量库")
PYEOF

python3 ~/longhun-system/vector_store.py

# ─── 龘字替换审计 ───
echo ""
echo ">>> 龘字替换残留检查"
REMAIN=$(grep -rlI "龙" ~/longhun-system --include="*.py" --include="*.md" --include="*.sh" --include="*.json" --include="*.yaml" --exclude-dir={.git,venv,node_modules,__pycache__,.Trash,cache} 2>/dev/null | wc -l | tr -d ' ')
echo "残留含「龙」文件: $REMAIN"
if [ "$REMAIN" -eq 0 ]; then echo "✅ 零残留"; else echo "🟡 还有 $REMAIN 个"; fi

# ─── 华为云节点状态 ───
echo ""
echo ">>> 华为云节点探测"
ssh -o ConnectTimeout=3 root@119.13.90.27 "curl -s http://127.0.0.1:11434/api/tags | grep -c 'name'" 2>/dev/null && echo "🟢 云端 Ollama 在线" || echo "🔴 云端离线或需密码"

echo ""
echo "=== 全开完毕 ==="
echo "DNA: #龘芯⚡️$(date +%Y-%m-%d)-MASTER-PLAYBOOK-DONE-v2.6"
