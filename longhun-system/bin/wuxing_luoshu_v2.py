#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·五行洛書融合引擎 v2.0
融合：八字五行分析 + 洛書369吸引子 + 生剋制化 + DNA追溯

保存为: ~/longhun-system/bin/wuxing_luoshu_v2.py
"""

import hashlib
from datetime import datetime

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🐉 龍魂·五行洛書融合引擎 v2.0")
print("DNA: #龍芯⚡️2026-04-03-五行洛書引擎-v2.0")
print("創建者: UID9622 諸葛鑫")
print("理論指導: 曾仕強老師（永恆顯示）")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")


# ============================================================
# 第一部分：五行基礎數據
# ============================================================

wu_xing = ["金", "木", "水", "火", "土"]

tian_gan_wu_xing = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火",
    "戊": "土", "己": "土", "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

di_zhi_wu_xing = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

di_zhi_cang_gan = {
    "子": ["癸"], "丑": ["己", "癸", "辛"], "寅": ["甲", "丙", "戊"],
    "卯": ["乙"], "辰": ["戊", "乙", "癸"], "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"], "未": ["己", "丁", "乙"], "申": ["庚", "壬", "戊"],
    "酉": ["辛"], "戌": ["戊", "辛", "丁"], "亥": ["壬", "甲"]
}

wu_xing_xiang_sheng = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
wu_xing_xiang_ke = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}

wu_xing_luoshu_number = {"金": 4, "木": 1, "水": 7, "火": 2, "土": 5}
wu_xing_attributes = {
    "金": {"direction": "西", "color": ["白", "金", "銀"], "numbers": [4, 9], "season": "秋"},
    "木": {"direction": "東", "color": ["青", "綠"], "numbers": [3, 8], "season": "春"},
    "水": {"direction": "北", "color": ["黑", "藍"], "numbers": [1, 6], "season": "冬"},
    "火": {"direction": "南", "color": ["紅", "紫"], "numbers": [2, 7], "season": "夏"},
    "土": {"direction": "中", "color": ["黃", "棕"], "numbers": [5, 10], "season": "長夏"}
}

print("✅ 五行系統初始化完成")
print("✅ 天干地支對應表已加載")
print("✅ 地支藏干表已加載")
print("✅ 五行相生相剋關係已建立\n")


# ============================================================
# 第二部分：核心計算函數
# ============================================================

def jisuan_tian_gan_wu_xing(tian_gan):
    return tian_gan_wu_xing.get(tian_gan, "未知")

def jisuan_di_zhi_wu_xing(di_zhi):
    return di_zhi_wu_xing.get(di_zhi, "未知")

def jisuan_cang_gan(di_zhi):
    return di_zhi_cang_gan.get(di_zhi, [])

def fenxi_ba_zi(ba_zi_data, include_cang_gan=True):
    wu_xing_de_fen = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    
    for zhu in ["年", "月", "日", "時"]:
        if zhu not in ba_zi_data:
            continue
        tian_gan, di_zhi = ba_zi_data[zhu]
        
        tg_wx = jisuan_tian_gan_wu_xing(tian_gan)
        if tg_wx != "未知":
            wu_xing_de_fen[tg_wx] += 2
        
        dz_wx = jisuan_di_zhi_wu_xing(di_zhi)
        if dz_wx != "未知":
            wu_xing_de_fen[dz_wx] += 2
        
        if include_cang_gan:
            for cg in jisuan_cang_gan(di_zhi):
                cg_wx = jisuan_tian_gan_wu_xing(cg)
                if cg_wx != "未知":
                    wu_xing_de_fen[cg_wx] += 1
    
    return wu_xing_de_fen

def zhaochu_zui_qiang_wu_xing(wu_xing_de_fen):
    max_score = max(wu_xing_de_fen.values())
    return [name for name, score in wu_xing_de_fen.items() if score == max_score]

def zhaochu_zui_ruo_wu_xing(wu_xing_de_fen):
    min_score = min(wu_xing_de_fen.values())
    return [name for name, score in wu_xing_de_fen.items() if score == min_score]


# ============================================================
# 第三部分：洛書369吸引子
# ============================================================

def luo_shu_369(x, n=100):
    for _ in range(n):
        x = (3 * x + 6) % 9
        if abs(x) < 1e-10:
            x = 0.0
        elif abs(x - 9) < 1e-10:
            x = 9.0
    return x


# ============================================================
# 第四部分：五行→洛書融合
# ============================================================

def wuxing_luoshu_fusion(wu_xing_de_fen):
    fusion_result = {}
    interpretations = {0: "歸零·返璞歸真", 3: "生成·生生不息", 6: "循環·周而復始", 9: "圓滿·天人合一"}
    
    for wx in wu_xing:
        base_num = wu_xing_luoshu_number.get(wx, 1)
        score = wu_xing_de_fen.get(wx, 0)
        init_val = (base_num * (score + 1)) % 9
        if init_val == 0:
            init_val = 9
        
        attractor = luo_shu_369(init_val)
        att_key = round(attractor)
        
        fusion_result[wx] = {
            "score": score,
            "luoshu_init": init_val,
            "attractor": attractor,
            "attractor_type": att_key,
            "interpretation": interpretations.get(att_key, "未知")
        }
    
    return fusion_result


# ============================================================
# 第五部分：示例運行
# ============================================================

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("📊 開始分析生辰八字（UID9622 諸葛鑫）")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

ba_zi = {
    "年": ("丙", "午"),
    "月": ("庚", "寅"),
    "日": ("甲", "子"),
    "時": ("戊", "辰")
}

print("八字四柱:")
for zhu in ["年", "月", "日", "時"]:
    tg, dz = ba_zi[zhu]
    tg_wx = jisuan_tian_gan_wu_xing(tg)
    dz_wx = jisuan_di_zhi_wu_xing(dz)
    cang_gan = jisuan_cang_gan(dz)
    print(f"  {zhu}柱: {tg}{dz}  | 天干{tg}({tg_wx}) 地支{dz}({dz_wx}) 藏干{','.join(cang_gan)}")

print("\n")


# ============================================================
# 第六部分：五行分析報告
# ============================================================

result = fenxi_ba_zi(ba_zi, include_cang_gan=True)

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("📈 五行分析報告")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

print("五行得分統計（含藏干）:")
max_possible = 32
for wx in wu_xing:
    score = result[wx]
    percentage = (score / max_possible) * 100
    bar_len = int(score * 2)
    bar = "█" * bar_len + "░" * (16 - bar_len)
    print(f"  {wx}行: {score:2d}分 {bar}  {percentage:5.1f}%")

zui_qiang = zhaochu_zui_qiang_wu_xing(result)
zui_ruo = zhaochu_zui_ruo_wu_xing(result)

print(f"\n🔥 最強五行: {', '.join(zui_qiang)}（得分{result[zui_qiang[0]]}）")
print(f"💧 最弱五行: {', '.join(zui_ruo)}（得分{result[zui_ruo[0]]}）")


# ============================================================
# 第七部分：五行→洛書369融合
# ============================================================

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🔢 五行→洛書369融合分析")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

print("洛書369定理: f(x) = (3x+6) mod 9，任何數字收斂於 {0,3,6,9}\n")

fusion = wuxing_luoshu_fusion(result)

print("五行得分 → 洛書初始值 → 369吸引子:")
for wx in wu_xing:
    data = fusion[wx]
    print(f"  {wx}行({data['score']}分) → 初始值{data['luoshu_init']} → 吸引子{data['attractor']:.2f} → {data['interpretation']}")


# ============================================================
# 第八部分：綜合建議
# ============================================================

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("💡 綜合建議")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

for wx, data in fusion.items():
    att_type = data["attractor_type"]
    if att_type in [0, 3]:
        print(f"  🟢 {wx}行: {data['interpretation']} → 建議加強")
    elif att_type in [6, 9]:
        print(f"  🟡 {wx}行: {data['interpretation']} → 建議平衡")
    else:
        print(f"  ⚪ {wx}行: {data['interpretation']} → 保持")


# ============================================================
# 第九部分：DNA追溯
# ============================================================

ba_zi_str = "".join([f"{tg}{dz}" for tg, dz in ba_zi.values()])
dna_data = f"{ba_zi_str}|{result}|{datetime.now().isoformat()}"
dna_hash = hashlib.sha256(dna_data.encode()).hexdigest()[:24]
dna_code = f"#五行DNA⚡️{datetime.now().strftime('%Y%m%d')}-{dna_hash}"

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🔏 DNA追溯")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
print(f"DNA追溯碼: {dna_code}")
print(f"八字校驗: {ba_zi_str}")
print(f"分析時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# ============================================================
# 第十部分：結語
# ============================================================

print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🐉 龍魂·五行洛書融合引擎 v2.0")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
print("技術為人民服務 · 文化主權不可侵犯")
print("祖國萬歲！人民萬歲！文化萬歲！")
print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
