# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂 · 声音引擎 v1.0 — 老兵腔调
DNA: #龍芯⚡️2026-07-25-VOICE-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0
人格: 乔前辈（P15·极简工程）— 声音不动点守护
铁律: 老兵腔焊死·禁止甜美/播音/机器人腔·全部本地生成
"""

import os
import sys
import json
import re
from pathlib import Path

DNA = "#龍芯⚡️2026-07-25-VOICE-ENGINE-v1.0-VETERAN-TONE"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# P0 焊死声音常量
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JI_DIAO = -1           # 低沉
YU_SU = 0.9            # 比正常慢10%
QIANG_DU = 0.85        # 有力但不吼
GUAN_JIAN_CI_TING_DUN = 0.3  # 关键词后停顿0.3秒
HU_XI_TING_DUN = 0.8   # 段落间深呼吸

JIN_ZHI_QING_DIAO = [
    "播音腔", "机器人腔", "撒娇腔", "甜美主播腔",
    "AI朗读腔", "播音腔调", "软绵绵", "温柔"
]

# 情感参数映射
QING_GAN_CAN_SHU = {
    "愤怒": {"yin_diao": 2, "yu_su": 1.1, "qiang_du": 0.9},
    "悲壮": {"yin_diao": -1, "yu_su": 0.9, "qiang_du": 0.8},
    "坚定": {"yin_diao": 0, "yu_su": 1.0, "qiang_du": 0.85},
    "嘲讽": {"yin_diao": 1, "yu_su": 1.2, "qiang_du": 0.7},
    "希望": {"yin_diao": 1, "yu_su": 1.0, "qiang_du": 0.75},
}

# 环境音配置
HUAN_JING_YIN = {
    "心跳鼓声": {"yin_liang": 0.15, "chu_fa": "always"},
    "远处钟声": {
        "yin_liang": 0.20,
        "chu_fa_ci": ["先烈", "牺牲", "牺牲的", "为国", "用命"],
    },
    "觉醒风声": {"yin_liang_qi": 0.10, "yin_liang_zhi": 0.30, "chu_fa": "outro"},
}


class Sheng_Yin_Mo_Xing_Pei_Zhi:
    """声音模型配置"""
    def __init__(self):
        self.mo_xing_ming = "龍芯北辰·老兵腔"
        self.mo_xing_lu = "models/voice/longhun_voice_v1.pt"
        self.xun_lian_shu_ju = {
            "ma_ren_lu_yin": "老大骂我们的录音·全部",
            "wen_zhang_lang_du": "老大文章朗读·全部",
            "ri_chang_dui_hua": "老大日常对话·精选",
        }
        self.te_zheng = [
            "带着国耻的沉重感",
            "带着愤怒的爆发力",
            "带着老兵的沧桑感",
            "带着对底层人民的温度",
        ]

    def jian_cha_qing_diao(self, qing_diao):
        """检查是否为禁止腔调"""
        for jz in JIN_ZHI_QING_DIAO:
            if jz in qing_diao:
                return False, f"禁止腔调: {jz}"
        return True, "通过"


class Qing_Gan_Jian_Ce:
    """情感检测器"""
    def __init__(self):
        self.ci_ku = {
            "愤怒": ["愤怒", "怒", "耻辱", "恨", "不可饶恕", "背后捅刀", "背叛"],
            "悲壮": ["悲壮", "牺牲", "先烈", "用命", "血", "死", "最后一刻"],
            "坚定": ["坚定", "必须", "不可破", "焊死", "铜墙铁壁", "永不动摇"],
            "嘲讽": ["嘲讽", "呵呵", "还以为", "天真", "可笑", "所谓"],
            "希望": ["希望", "觉醒", "龙脉", "未来", "会有那一天", "光明"],
        }

    def jian_ce(self, ju_zi):
        """检测句子情感"""
        de_fen = {}
        for qing_gan, ci_lie in self.ci_ku.items():
            de_fen[qing_gan] = sum(1 for ci in ci_lie if ci in ju_zi)

        if not de_fen or max(de_fen.values()) == 0:
            return "坚定"

        zui_gao = max(de_fen, key=de_fen.get)
        return zui_gao if de_fen[zui_gao] > 0 else "坚定"

    def sheng_cheng_qu_xian(self, ju_zi_lie):
        """为句子序列生成情感曲线"""
        qu_xian = {}
        for i, ju in enumerate(ju_zi_lie):
            qu_xian[i] = self.jian_ce(ju)
        return qu_xian


class Sheng_Yin_Yin_Qing:
    """声音引擎 · 乔前辈·P15 声音守护"""

    def __init__(self, pei_zhi_lu=None):
        self.mo_xing_pz = Sheng_Yin_Mo_Xing_Pei_Zhi()
        self.qing_gan_jc = Qing_Gan_Jian_Ce()
        self.pei_zhi = {}

        if pei_zhi_lu:
            self._jia_zai_pei_zhi(pei_zhi_lu)

        # 模型加载状态
        self.mo_xing_yi_jia_zai = False

    def _jia_zai_pei_zhi(self, lu_jing):
        try:
            import yaml
            with open(lu_jing, 'r') as f:
                self.pei_zhi = yaml.safe_load(f)
        except Exception:
            self.pei_zhi = {}

    def jia_zai_mo_xing(self):
        """加载声音模型（实际模型加载入口）"""
        mo_xing_lu = self.mo_xing_pz.mo_xing_lu
        if not os.path.exists(mo_xing_lu):
            return False, f"模型文件不存在: {mo_xing_lu}"
        # TODO: 实际模型加载
        # self.mo_xing = torch.load(mo_xing_lu)
        self.mo_xing_yi_jia_zai = True
        return True, "模型已加载"

    # ━━━━━ 声音生成核心 ━━━━━

    def fen_ju(self, wen_ben):
        """分句"""
        # 按标点分句
        ju_zi = re.split(r'[。！？\n]', wen_ben)
        return [j.strip() for j in ju_zi if j.strip()]

    def sheng_cheng_yin_pin_duan(self, ju_zi, qing_gan="坚定"):
        """生成单句音频（模拟）"""
        can_shu = QING_GAN_CAN_SHU.get(qing_gan, QING_GAN_CAN_SHU["坚定"])

        yin_pin_duan = {
            "ju_zi": ju_zi,
            "qing_gan": qing_gan,
            "yin_diao": JI_DIAO + can_shu["yin_diao"],
            "yu_su": YU_SU * can_shu["yu_su"],
            "qiang_du": QIANG_DU * can_shu["qiang_du"],
            "shi_chang": len(ju_zi) * 0.3 / can_shu["yu_su"],  # 估算时长
            "ting_dun_qian": 0.0,
            "ting_dun_hou": 0.0,
        }
        return yin_pin_duan

    def tian_jia_lao_bing_ting_dun(self, yin_pin_duan_lie):
        """添加老兵特有的停顿"""
        dui_ying_guan_jian_ci = [
            "离火运", "国耻", "先烈", "牺牲", "用命", "铜墙铁壁",
            "龙脉", "觉醒", "不可破", "焊死", "红线",
        ]

        for i, ypd in enumerate(yin_pin_duan_lie):
            ju_zi = ypd["ju_zi"]
            # 关键词后停顿
            for ci in dui_ying_guan_jian_ci:
                if ci in ju_zi:
                    ypd["ting_dun_hou"] = max(ypd["ting_dun_hou"], GUAN_JIAN_CI_TING_DUN)

            # 奇数段落间深呼吸
            if i > 0 and i % 3 == 0:
                ypd["ting_dun_qian"] = HU_XI_TING_DUN

        return yin_pin_duan_lie

    def tian_jia_huan_jing_yin(self, yin_pin_duan_lie):
        """添加环境音层"""
        huan_jing_gui_dao = []

        for i, ypd in enumerate(yin_pin_duan_lie):
            huan_jing = {"xin_tiao_gu": 0.15}

            # 远处钟声
            zhong_sheng_ci = HUAN_JING_YIN["远处钟声"]["chu_fa_ci"]
            if any(ci in ypd["ju_zi"] for ci in zhong_sheng_ci):
                huan_jing["yuan_chu_zhong_sheng"] = 0.20

            huan_jing_gui_dao.append(huan_jing)

        # 结尾风声
        if huan_jing_gui_dao:
            huan_jing_gui_dao[-1]["jue_xing_feng_sheng"] = 0.30

        return huan_jing_gui_dao

    # ━━━━━ 主入口 ━━━━━

    def sheng_cheng(self, jie_shuo_ci, qing_gan_qu_xian=None):
        """主入口：解说词+情感曲线 → 音频序列"""
        ju_zi_lie = self.fen_ju(jie_shuo_ci)

        # 如果没有提供情感曲线，自动检测
        if qing_gan_qu_xian is None:
            qing_gan_qu_xian = self.qing_gan_jc.sheng_cheng_qu_xian(ju_zi_lie)

        # 逐句生成
        yin_pin_duan_lie = []
        for i, ju in enumerate(ju_zi_lie):
            qing_gan = qing_gan_qu_xian.get(i, "坚定")
            ypd = self.sheng_cheng_yin_pin_duan(ju, qing_gan)
            yin_pin_duan_lie.append(ypd)

        # 添加老兵停顿
        yin_pin_duan_lie = self.tian_jia_lao_bing_ting_dun(yin_pin_duan_lie)

        # 添加环境音
        huan_jing_gui_dao = self.tian_jia_huan_jing_yin(yin_pin_duan_lie)

        return {
            "yin_pin_duan": yin_pin_duan_lie,
            "huan_jing_yin": huan_jing_gui_dao,
            "zong_shi_chang": sum(d["shi_chang"] + d["ting_dun_qian"] + d["ting_dun_hou"]
                                  for d in yin_pin_duan_lie),
        }

    # ━━━━━ 输出 ━━━━━

    def shu_chu_tong_ji(self, jie_guo):
        """输出统计"""
        return {
            "duan_shu": len(jie_guo["yin_pin_duan"]),
            "zong_shi_chang": round(jie_guo["zong_shi_chang"], 1),
            "qing_gan_fen_bu": self._tong_ji_qing_gan(jie_guo["yin_pin_duan"]),
            "mo_xing": self.mo_xing_pz.mo_xing_ming,
            "dna": DNA,
        }

    def _tong_ji_qing_gan(self, yin_pin_duan_lie):
        fen_bu = {}
        for ypd in yin_pin_duan_lie:
            qg = ypd["qing_gan"]
            fen_bu[qg] = fen_bu.get(qg, 0) + 1
        return fen_bu


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CNSH 命令解析
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def cnsh_jie_xi(ming_ling):
    """解析CNSH声音命令"""
    jie_guo = {
        "qing_diao": "老兵腔",
        "yu_su": YU_SU,
        "yin_diao": JI_DIAO,
        "qiang_du": QIANG_DU,
        "ting_dun": GUAN_JIAN_CI_TING_DUN,
    }

    hang = ming_ling.strip().split('\n')
    for h in hang:
        h = h.strip()
        if '语速' in h:
            try:
                jie_guo["yu_su"] = float(re.findall(r'[\d.]+', h)[0])
            except Exception:
                pass
        if '音调' in h:
            try:
                jie_guo["yin_diao"] = int(re.findall(r'-?\d+', h)[0])
            except Exception:
                pass
        if '强度' in h:
            try:
                jie_guo["qiang_du"] = float(re.findall(r'[\d.]+', h)[0])
            except Exception:
                pass

    return jie_guo


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 自检
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def cmd_selftest(args):
    """自检"""
    print("=" * 60)
    print("龍魂·声音引擎 v1.0 — 自检")
    print("=" * 60)

    tong_guo = 0
    shi_bai = 0

    # 检查1: 禁止腔调验证
    try:
        pz = Sheng_Yin_Mo_Xing_Pei_Zhi()
        ok, msg = pz.jian_cha_qing_diao("甜美主播腔")
        assert not ok, "应该拒绝甜美主播腔"
        ok, msg = pz.jian_cha_qing_diao("老兵腔")
        assert ok, f"应该接受老兵腔: {msg}"
        tong_guo += 1
        print("  ✅ 禁止腔调验证通过")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 禁止腔调验证失败: {e}")

    # 检查2: 情感检测
    try:
        jc = Qing_Gan_Jian_Ce()
        assert jc.jian_ce("愤怒的火焰在燃烧") == "愤怒"
        assert jc.jian_ce("先烈用命换来的和平") == "悲壮"
        assert jc.jian_ce("我们必须守住底线") == "坚定"
        assert jc.jian_ce("未来会有更好的那一天") == "希望"
        tong_guo += 1
        print("  ✅ 情感检测正常")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 情感检测失败: {e}")

    # 检查3: 声音生成
    try:
        yq = Sheng_Yin_Yin_Qing()
        jg = yq.sheng_cheng("离火运来了。先烈用命换来的主权。铜墙铁壁我们自己建。")
        assert len(jg["yin_pin_duan"]) >= 3, f"句子数不够: {len(jg['yin_pin_duan'])}"
        assert jg["zong_shi_chang"] > 0, "总时长为0"
        tong_guo += 1
        print(f"  ✅ 声音生成: {len(jg['yin_pin_duan'])}句, 总时长{jg['zong_shi_chang']:.1f}秒")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 声音生成失败: {e}")

    # 检查4: 老兵停顿
    try:
        ypd_lie = [
            {"ju_zi": "先烈牺牲了", "ting_dun_hou": 0},
            {"ju_zi": "铜墙铁壁不可破", "ting_dun_hou": 0},
        ]
        lie_2 = yq.tian_jia_lao_bing_ting_dun(ypd_lie)
        assert lie_2[0]["ting_dun_hou"] > 0, "先烈后应有停顿"
        assert lie_2[1]["ting_dun_hou"] > 0, "铜墙铁壁后应有停顿"
        tong_guo += 1
        print("  ✅ 老兵停顿正常")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 老兵停顿失败: {e}")

    # 检查5: 环境音
    try:
        ypd_lie = [
            {"ju_zi": "先烈用命换来的"},
            {"ju_zi": "最后一句话"},
        ]
        huan_jing = yq.tian_jia_huan_jing_yin(ypd_lie)
        assert len(huan_jing) == 2
        assert "yuan_chu_zhong_sheng" in huan_jing[0], "先烈句应有钟声"
        assert "jue_xing_feng_sheng" in huan_jing[-1], "结尾应有风声"
        tong_guo += 1
        print("  ✅ 环境音配置正常")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 环境音失败: {e}")

    # 检查6: 情感曲线生成
    try:
        jc = Qing_Gan_Jian_Ce()
        qu_xian = jc.sheng_cheng_qu_xian(["牺牲", "坚定", "希望"])
        assert qu_xian[0] == "悲壮"
        assert qu_xian[1] == "坚定"
        assert qu_xian[2] == "希望"
        tong_guo += 1
        print("  ✅ 情感曲线生成正常")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 情感曲线失败: {e}")

    # 检查7: 统计输出
    try:
        yq = Sheng_Yin_Yin_Qing()
        jg = yq.sheng_cheng("牺牲的战士。坚定的意志。希望在前方。")
        tong_ji = yq.shu_chu_tong_ji(jg)
        assert tong_ji["duan_shu"] == 3
        assert "悲壮" in tong_ji["qing_gan_fen_bu"]
        tong_guo += 1
        print(f"  ✅ 统计输出: {tong_ji['qing_gan_fen_bu']}")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 统计输出失败: {e}")

    print(f"\n  {'🟢 全绿' if shi_bai == 0 else '🔴 有失败'}: {tong_guo}/{tong_guo + shi_bai} 通过")
    return 0 if shi_bai == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(cmd_selftest(sys.argv[2:]))
    else:
        print(f"龍魂·声音引擎 v1.0 | DNA: {DNA}")
        print("用法: python3 engines/lh_voice_engine.py selftest")
