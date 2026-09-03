#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·数字人岗位注册引擎 v1.0
DNA: #龍芯⚡️2026-09-02-DH-STUDIO-REGISTRY-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
功能: 设计生态岗位数字人批量注册（DH-010~016）· 目录+imprint+registry+neural_net 四端同步
用法: python3 08_BIN/lh_dh_studio_registry.py
"""
import json, os, datetime, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DH_DIR = os.path.join(ROOT, "digital_humans")
REGISTRY = os.path.join(DH_DIR, "registry.json")
NEURAL = os.path.join(ROOT, ".codebuddy", "longhun_neural_net.json")
NOW = "2026-09-02T13:00:00.000000"

# 设计生态岗位全景：视觉(已有DH-009) + 7 岗位补齐
STUDIO_POSTS = [
    {
        "ipa": "DH-010", "dir_name": "DH-010_字靈_字体设计",
        "name": "字靈·字体设计官", "persona": "P08 仓颉",
        "type": "字体设计·符号命名", "principle": "字体审美 · 符号语言 · 命名规范",
        "functions": "龍魂字体维护 · 繁龍焊死 · 命名/符号/CNSH规范 · 字体资产取材(longhun-font)",
    },
    {
        "ipa": "DH-011", "dir_name": "DH-011_匠心_代码实现",
        "name": "匠心·代码工匠官", "persona": "P04 鲁班",
        "type": "代码实现·工程落地", "principle": "工程实现 · 最小闭环 · 可运行优先",
        "functions": "设计稿→代码 · 页面/组件实现 · 修bug · 技术选型 · 可import+自测",
    },
    {
        "ipa": "DH-012", "dir_name": "DH-012_明鉴_审计验收",
        "name": "明鉴·审计验收官", "persona": "P19 极简审计官",
        "type": "UI审计·八项验收", "principle": "极简审计 · 三色判定 · 交付放行",
        "functions": "UI/UX八项验收 · 布局/色彩/字体/间距/无障碍/响应式/表单/一致性 · 防AI味",
    },
    {
        "ipa": "DH-013", "dir_name": "DH-013_诗仙_灵感创意",
        "name": "诗仙·灵感创意官", "persona": "P11 李白",
        "type": "创意灵感·类比破局", "principle": "创意爆发 · 破局方案 · 故事化表达",
        "functions": "灵感供给 · 类比教学 · 概念破局 · 故事化表达 · 创意素材库",
    },
    {
        "ipa": "DH-014", "dir_name": "DH-014_蔡侯_排版印刷",
        "name": "蔡侯·排版印刷官", "persona": "P21 蔡伦",
        "type": "排版润色·知识印刷", "principle": "知识印刷 · 文档排版 · 文章模板",
        "functions": "页面排版 · 文档结构 · 知识卡片 · 抬头模板(六套) · 印刷质感",
    },
    {
        "ipa": "DH-015", "dir_name": "DH-015_墨香_归档整理",
        "name": "墨香·归档整理官", "persona": "P03 雯雯",
        "type": "四签归档·验收整理", "principle": "结构归档 · 四签验证 · 德字闸",
        "functions": "成果归档 · 索引更新 · 四签(GPG/DNA/归属/协议) · 验收放行",
    },
    {
        "ipa": "DH-016", "dir_name": "DH-016_知行_部署上线",
        "name": "知行·部署上线官", "persona": "P14 吕蒙",
        "type": "部署上线·快速成长", "principle": "部署执行 · 士别三日 · 上线回滚",
        "functions": "发布上线 · 静态托管 · 回滚 · 学习新技能 · 部署前安全扫描联动",
    },
]

def make_imprint(post):
    return {
        "dna": f"#龍芯⚡️2026-09-02-{post['ipa']}-STUDIO-v1.0-UID9622",
        "name": post["name"],
        "ipa": post["ipa"],
        "face_hash": f"FACE-{post['ipa']}-C26D5F",
        "voiceprint": f"VOICE-{post['ipa']}-9622",
        "model_path": os.path.join(DH_DIR, post["dir_name"]),
        "created_at": NOW,
        "updated_at": NOW,
        "version": 1,
        "status": "active",
        "metadata": {
            "type": "DH",
            "source": "2026-09-02 老大指令·数字人创作启动·设计生态岗位全补全",
            "persona": post["persona"],
            "principle": post["principle"],
            "functions": post["functions"],
            "team": "设计团流水线: 诗仙灵感→雲錦视觉→字靈字体→匠心代码→蔡侯排版→明鉴验收→墨香归档→知行上线",
        },
    }

def main():
    created = []
    for post in STUDIO_POSTS:
        d = os.path.join(DH_DIR, post["dir_name"])
        os.makedirs(d, exist_ok=True)
        imprint = make_imprint(post)
        p = os.path.join(d, "imprint.json")
        with open(p, "w", encoding="utf-8") as f:
            json.dump(imprint, f, ensure_ascii=False, indent=2)
            f.write("\n")
        created.append((post["ipa"], post["name"], p))

    # registry.json 追加（含历史 DH-001~008 同步对齐）
    reg = json.load(open(REGISTRY, encoding="utf-8"))
    nn_hist = json.load(open(NEURAL, encoding="utf-8"))["digital_humans"]["humans"]
    for h in nn_hist:
        ipa = h["id"]
        if ipa in reg["digital_humans"]:
            continue
        reg["digital_humans"][ipa] = {
            "dna": f"#龍芯⚡️2026-09-02-{ipa}-REGISTRY-ALIGN-v1.0-UID9622",
            "name": h["name"], "ipa": ipa,
            "face_hash": f"FACE-{ipa}-C26D5F", "voiceprint": f"VOICE-{ipa}-9622",
            "model_path": os.path.join(DH_DIR, f"{ipa}_" + h["name"].split("·")[0]),
            "created_at": NOW, "updated_at": NOW,
            "version": 1, "status": "active",
            "metadata": {"type": "DH", "source": "2026-09-02 registry历史对齐", "persona": h["persona"], "principle": h["type"]},
        }
    for post, (ipa, name, _) in zip(STUDIO_POSTS, created):
        reg["digital_humans"][ipa] = make_imprint(post)
    reg["meta"]["version"] = 7
    reg["meta"]["last_updated"] = NOW
    with open(REGISTRY, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # neural_net.json humans 追加 + total
    nn = json.load(open(NEURAL, encoding="utf-8"))
    dh = nn["digital_humans"]
    for post in STUDIO_POSTS:
        dh["humans"].append({
            "id": post["ipa"],
            "name": post["name"],
            "persona": post["persona"],
            "type": post["type"],
            "status": "🟢",
        })
    dh["total"] = len(dh["humans"])
    dh["description"] = f"{dh['total']}个数字人 · 全联动 · 四层桥接 · 设计生态岗位全补全"
    with open(NEURAL, "w", encoding="utf-8") as f:
        json.dump(nn, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # 校验
    reg2 = json.load(open(REGISTRY, encoding="utf-8"))
    nn2 = json.load(open(NEURAL, encoding="utf-8"))
    ok = all(i["ipa"] in reg2["digital_humans"] for i in STUDIO_POSTS)
    ok = ok and nn2["digital_humans"]["total"] == len(nn2["digital_humans"]["humans"])
    print(f"新注册 {len(created)} 个岗位数字人: " + ", ".join(f"{a}({b})" for a, b, _ in created))
    print(f"registry 数字人总数: {len(reg2['digital_humans'])} · neural_net total: {nn2['digital_humans']['total']}")
    print(f"校验: {'🟢 通过' if ok else '🔴 失败'}")

if __name__ == "__main__":
    main()
