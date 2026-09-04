#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷿未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-LH_SUGGESTION_TODO-v1.0-5835fe2c
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# 龍芯⚡️丙午·丙申·乙卯·丙戌·䷷旅-LH-SUGGESTION-TODO-v1.0
# -*- coding: utf-8 -*-
"""
龍魂建议即待办管理器

规则：建议即待办，二见即执行。
- AI 每次提出建议，自动登记
- 同一建议出现第 2 次 → 自动执行（高风险除外）
- 执行后标记 done
"""

import json
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path

TODO_FILE = Path("/Users/zuimeidedeyihan/longhun-system/L7_数据层/suggestions/suggestions_todo.json")


def 读取待办():
    if TODO_FILE.exists():
        try:
            with open(TODO_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except (json.JSONDecodeError, Exception):
            pass
    return {
        "version": "1.0.0",
        "owner": "UID9622",
        "principle": "建议即待办，二见即执行",
        "rules": [
            "AI 每次提出的可操作建议，自动写入本文件，状态为 pending",
            "同一建议第二次出现（或用户再次提及），状态升级为 auto-execute，AI 直接执行",
            "执行完成后，状态改为 done，并记录执行 DNA",
            "高风险操作（删除、发布、密钥、sudo、git push --force）仍需触发一票否决，不自动执行",
            "用户可手动将建议改为 dismissed"
        ],
        "suggestions": []
    }


def 保存待办(data):
    TODO_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def 生成ID(content):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    h = hashlib.sha256(f"{content}{today}".encode()).hexdigest()[:4]
    return f"SG-{today}-{h.upper()}"


def 登记建议(content, source="AI"):
    data = 读取待办()
    suggestions = data.get("suggestions", [])
    now = datetime.now(timezone.utc).isoformat()

    for sg in suggestions:
        if sg["content"] == content:
            sg["count"] = sg.get("count", 1) + 1
            sg["last_seen"] = now
            if sg["count"] >= 2 and sg["status"] == "pending":
                sg["status"] = "auto-execute"
            保存待办(data)
            return sg

    new_sg = {
        "id": 生成ID(content),
        "source": source,
        "content": content,
        "status": "pending",
        "count": 1,
        "first_seen": now,
        "last_seen": now,
        "executed_at": "",
        "execution_dna": "",
        "notes": ""
    }
    suggestions.append(new_sg)
    保存待办(data)
    return new_sg


def 标记完成(suggestion_id, dna, notes=""):
    data = 读取待办()
    for sg in data.get("suggestions", []):
        if sg["id"] == suggestion_id:
            sg["status"] = "done"
            sg["executed_at"] = datetime.now(timezone.utc).isoformat()
            sg["execution_dna"] = dna
            sg["notes"] = notes
            保存待办(data)
            return sg
    return None


def 列出待办():
    data = 读取待办()
    return data.get("suggestions", [])


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "list":
            for sg in 列出待办():
                print(f"[{sg['status']}] {sg['id']}: {sg['content'][:40]}...")
        elif cmd == "add" and len(sys.argv) > 2:
            sg = 登记建议(sys.argv[2])
            print(json.dumps(sg, ensure_ascii=False, indent=2))
        elif cmd == "done" and len(sys.argv) > 4:
            sg = 标记完成(sys.argv[2], sys.argv[3], sys.argv[4])
            print(json.dumps(sg, ensure_ascii=False, indent=2))
        else:
            print("用法: lh_suggestion_todo.py list | add <content> | done <id> <dna> <notes>")
    else:
        print("用法: lh_suggestion_todo.py list | add <content> | done <id> <dna> <notes>")
