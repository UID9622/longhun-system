# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-c9617159
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 龍魂NPC对话台 · lh npc"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "personas"))
from npc_engine import NPC
from 二十四人格 import 二十四人格

def main():
    db = os.path.expanduser("~/.longhun/npc.db")
    os.makedirs(os.path.dirname(db), exist_ok=True)
    print("🐉 龍魂·24人格对话台（输入编号选人格，/quit退出）")
    for p in 二十四人格:
        print(f"  {p.代号} {p.名字}｜{p.头衔}")
    sel = input("选人格> ").strip().upper().replace("P","")
    try: p = 二十四人格[int(sel)-1]
    except Exception: print("无效"); return
    npc = NPC(p, db路径=db)
    玩家 = input("你的名字> ").strip() or "老大"
    print(f"\n{p.名字}：{p.口头禅[0]}，{玩家}。 ({p.头衔})")
    while True:
        try: 话 = input(f"\n{玩家}> ").strip()
        except (EOFError, KeyboardInterrupt): break
        if 话 in ("/quit","/exit"): break
        if 话 == "/情感": print(npc.记忆.情感状态(玩家)); continue
        if 话 == "/自主": print(npc.自主一刻()); continue
        r = npc.互动(玩家, 话)
        print(f"{r['npc']}> {r['回应']}")
    print(f"🐉 记忆已存入 {db}，下次接着聊。")

if __name__ == "__main__":
    main()
