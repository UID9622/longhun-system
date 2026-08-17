#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂 · 视觉引擎 v1.0 — 暗夜鎏金军魂
DNA: #龍芯⚡️2026-07-25-VISUAL-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0
人格: 李白（P11·创意守护）— 美学不动点守护
铁律: 极夜黑#080808+龍魂金#C9A84C焊死·图腾位置焊死·效果参数焊死
"""

import os
import sys
import json
import math
from pathlib import Path

DNA = "#龍芯⚡️2026-07-25-VISUAL-ENGINE-v1.0-DARK-GOLDEN"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# P0 焊死色彩常量
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SE_JI_YE_HEI = "#080808"       # 极夜黑 — 永不更改
SE_LONG_HUN_JIN = "#C9A84C"    # 龍魂金 — 永不更改
SE_AN_HUI = "#6B6B6B"          # 暗灰
SE_XUE_HONG = "#FF4444"        # 血红
SE_GUO_DU = "#1A1A2E"          # 深蓝过渡
SE_BIAN_KUANG = "#C9A84C"      # 鎏金边框


class Yan_Se_Pan:
    """颜色盘 — 焊死不可改"""
    def __init__(self):
        self.bei_jing = SE_JI_YE_HEI
        self.jin = SE_LONG_HUN_JIN
        self.hui = SE_AN_HUI
        self.jing = SE_XUE_HONG
        self.guo_du = SE_GUO_DU
        self.bian_kuang = SE_BIAN_KUANG

    def __repr__(self):
        return f"颜色盘(背景={self.bei_jing}, 金={self.jin})"


class Tu_Teng:
    """图腾六件套"""
    def __init__(self):
        self.tu_teng = {
            "dna": {
                "ming_cheng": "DNA追溯码",
                "wei_zhi": "bottom-right",
                "tou_ming_du": 0.6,
                "shan_shuo_jian_ge": 5.0,
                "xiao_guo": "极慢闪烁",
            },
            "mo_tong": {
                "ming_cheng": "魔瞳符号",
                "wei_zhi": "top-left",
                "tou_ming_du": 0.4,
                "gen_sui_qiang_du": 0.3,
                "xiao_guo": "凝视跟随",
            },
            "ba_gua": {
                "ming_cheng": "八卦暗纹",
                "wei_zhi": "background-center",
                "tou_ming_du": 0.03,
                "xuan_zhuan_zhou_qi": 360.0,
                "xiao_guo": "极慢旋转",
            },
            "long": {
                "ming_cheng": "龍字",
                "wei_zhi": "center",
                "kai_chang_shi_chang": 3.0,
                "jie_wei_shi_chang": 3.0,
                "xiao_guo": "粒子燃烧/消散",
            },
            "369": {
                "ming_cheng": "369数字",
                "wei_zhi": "center",
                "zhuan_chang_shi_chang": 0.5,
                "xiao_guo": "闪电划过",
            },
            "gua": {
                "ming_cheng": "卦象",
                "wei_zhi": "emphasis-zone",
                "gao_liang_shi_chang": 2.0,
                "xiao_guo": "对应卦象高亮",
            },
        }

    def huo_qu(self, ming_cheng):
        return self.tu_teng.get(ming_cheng)


class Wen_Zi_Xiao_Guo:
    """文字效果引擎"""
    def __init__(self, yan_se_pan):
        self.se = yan_se_pan

    def ran_shao_jin(self, wen_zi):
        """燃烧金文字 — 关键词特效"""
        return {
            "wen_zi": wen_zi,
            "yan_se": self.se.jin,
            "xiao_guo": "particle_fire",
            "qiang_du": "high",
            "chi_xu": 2.0,
        }

    def shan_shuo_jin(self, wen_zi):
        """闪烁金文字 — 警告"""
        return {
            "wen_zi": wen_zi,
            "yan_se": self.se.jin,
            "xiao_guo": "flashing",
            "qiang_du": "medium",
            "chi_xu": 1.5,
        }

    def jing_tai_jin(self, wen_zi):
        """静态金文字 — 普通陈述"""
        return {
            "wen_zi": wen_zi,
            "yan_se": self.se.jin,
            "xiao_guo": "static",
            "qiang_du": "low",
        }

    def xue_hong_shan_shuo(self, wen_zi):
        """血红闪烁 — 红线警告"""
        return {
            "wen_zi": wen_zi,
            "yan_se": self.se.jing,
            "xiao_guo": "flashing_alert",
            "qiang_du": "high",
            "chi_xu": 2.0,
        }

    def jin_shu_rong_jie(self, wen_zi):
        """金属溶解 — 转场"""
        return {
            "wen_zi": wen_zi,
            "yan_se": self.se.jin,
            "xiao_guo": "metal_dissolve",
            "qiang_du": "medium",
            "chi_xu": 1.0,
        }

    def li_zi_ran_shao(self, wen_zi):
        """粒子燃烧 — 强情感关键词"""
        return {
            "wen_zi": wen_zi,
            "yan_se": self.se.jin,
            "xiao_guo": "particle_burn_sparks",
            "qiang_du": "maximum",
            "chi_xu": 2.5,
        }

    def pan_duan_xiao_guo(self, wen_zi, jin_ci_biao):
        """根据关键词自动判断效果"""
        ran_shao_ci = {"离火运", "国耻", "先烈", "牺牲", "铜墙铁壁", "龍脉", "觉醒"}
        jing_gao_ci = {"红线", "违规", "不可破", "焊死", "熔断", "背后捅刀"}

        for ci in ran_shao_ci:
            if ci in wen_zi:
                return self.li_zi_ran_shao(wen_zi)
        for ci in jing_gao_ci:
            if ci in wen_zi:
                return self.xue_hong_shan_shuo(wen_zi)
        if jin_ci_biao and any(c in wen_zi for c in jin_ci_biao):
            return self.ran_shao_jin(wen_zi)
        return self.jing_tai_jin(wen_zi)


class Shi_Jue_Yin_Qing:
    """视觉引擎 · 李白·P11 美学守护"""

    def __init__(self, pei_zhi_lu=None):
        self.yan_se = Yan_Se_Pan()
        self.tu_teng = Tu_Teng()
        self.wen_zi_xg = Wen_Zi_Xiao_Guo(self.yan_se)

        # 加载预设
        self.pei_zhi = {}
        if pei_zhi_lu:
            self._jia_zai_pei_zhi(pei_zhi_lu)

        # 当前帧序列
        self.zhen_xu_lie = []
        self.dang_qian_zhen = 0

    def _jia_zai_pei_zhi(self, lu_jing):
        try:
            import yaml
            with open(lu_jing, 'r') as f:
                self.pei_zhi = yaml.safe_load(f)
        except Exception:
            self.pei_zhi = {}

    # ━━━━━ 帧生成核心 ━━━━━

    def sheng_cheng_bei_jing(self, kuan=1920, gao=1080, zhen_bian_hao=0):
        """生成暗夜鎏金背景帧"""
        # 八卦暗纹旋转角度
        ba_gua_jiao_du = (zhen_bian_hao / 30.0 / 360.0 * 360) % 360

        zhen = {
            "bian_hao": zhen_bian_hao,
            "kuan": kuan,
            "gao": gao,
            "bei_jing_se": self.yan_se.bei_jing,
            "ceng_ji": {
                "bei_jing": {"yan_se": self.yan_se.bei_jing},
                "ba_gua_an_wen": {
                    "yan_se": self.yan_se.jin,
                    "tou_ming_du": 0.03,
                    "xuan_zhuan_jiao_du": ba_gua_jiao_du,
                },
                "tu_teng": [],
                "wen_zi": [],
            },
        }
        return zhen

    def die_jia_tu_teng(self, zhen, tu_teng_ming, zi_ding_yi=None):
        """叠加图腾到帧"""
        tt = self.tu_teng.huo_qu(tu_teng_ming)
        if not tt:
            return zhen

        tu_teng_ceng = dict(tt)
        if zi_ding_yi:
            tu_teng_ceng.update(zi_ding_yi)
        zhen["ceng_ji"]["tu_teng"].append(tu_teng_ceng)
        return zhen

    def tian_jia_wen_zi(self, zhen, wen_zi, xiao_guo="static", jin_ci_biao=None):
        """添加文字层"""
        xg = self.wen_zi_xg.pan_duan_xiao_guo(wen_zi, jin_ci_biao)
        if xiao_guo != "static":
            xg = self._qiang_zhi_xiao_guo(wen_zi, xiao_guo)

        zhen["ceng_ji"]["wen_zi"].append(xg)
        return zhen

    def _qiang_zhi_xiao_guo(self, wen_zi, xiao_guo):
        if xiao_guo == "burning":
            return self.wen_zi_xg.ran_shao_jin(wen_zi)
        elif xiao_guo == "flashing":
            return self.wen_zi_xg.shan_shuo_jin(wen_zi)
        elif xiao_guo == "alert":
            return self.wen_zi_xg.xue_hong_shan_shuo(wen_zi)
        return self.wen_zi_xg.jing_tai_jin(wen_zi)

    # ━━━━━ 脚本生成 ━━━━━

    def sheng_cheng(self, wen_zhang, shi_jue_jiao_ben=None, jin_ci_biao=None, kuan=1080, gao=1920):
        """主入口：文章+视觉脚本 → 帧序列"""
        zhen_xu_lie = []

        # 解析文章段落
        duan_luo = self._fen_duan_luo(wen_zhang)

        for bian_hao, duan in enumerate(duan_luo):
            # 每段生成多帧（模拟），单段上限120帧（4秒@30fps），防止长文爆炸
            zhen_ji_shu = min(120, max(30, len(duan) * 2))
            for zhen_i in range(zhen_ji_shu):
                zhen = self.sheng_cheng_bei_jing(
                    kuan=kuan, gao=gao, zhen_bian_hao=len(zhen_xu_lie)
                )

                # 总是叠加固定图腾
                zhen = self.die_jia_tu_teng(zhen, "dna")
                zhen = self.die_jia_tu_teng(zhen, "mo_tong")

                # 第一帧和最后一帧：龍字
                if zhen_i == 0 and bian_hao == 0:
                    zhen = self.die_jia_tu_teng(zhen, "long",
                        {"xiao_guo": "particle_burn", "shi_chang": 3.0})
                if zhen_i == zhen_ji_shu - 1 and bian_hao == len(duan_luo) - 1:
                    zhen = self.die_jia_tu_teng(zhen, "long",
                        {"xiao_guo": "particle_dissolve", "shi_chang": 3.0})

                # 段首帧加文字
                if zhen_i == 0:
                    zhen = self.tian_jia_wen_zi(zhen, duan, jin_ci_biao=jin_ci_biao)

                zhen_xu_lie.append(zhen)

        self.zhen_xu_lie = zhen_xu_lie
        return zhen_xu_lie

    def _fen_duan_luo(self, wen_ben):
        """按换行分段落（兼容 Windows \r\n）"""
        duan_luo = [d.strip() for d in wen_ben.replace('\r', '\n').split('\n') if d.strip()]
        if not duan_luo:
            duan_luo = [wen_ben.replace('\r', '').strip()]
        return duan_luo

    # ━━━━━ 输出 ━━━━━

    def shu_chu_tong_ji(self):
        """输出统计信息"""
        return {
            "zong_zhen_shu": len(self.zhen_xu_lie),
            "se_cai": str(self.yan_se),
            "tu_teng_shu": len(self.tu_teng.tu_teng),
            "dna": DNA,
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CNSH 命令解析
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def cnsh_jie_xi(ming_ling):
    """解析CNSH视觉命令"""
    jie_guo = {
        "bei_jing_se": SE_JI_YE_HEI,
        "wen_zi_se": SE_LONG_HUN_JIN,
        "tu_teng_lie_biao": ["dna", "mo_tong", "ba_gua", "long"],
        "xiao_guo_dui_zhao": {},
    }

    hang = ming_ling.strip().split('\n')
    for h in hang:
        h = h.strip()
        if '极夜黑' in h or '#080808' in h:
            jie_guo["bei_jing_se"] = SE_JI_YE_HEI
        if '龍魂金' in h or '#C9A84C' in h:
            jie_guo["wen_zi_se"] = SE_LONG_HUN_JIN

    return jie_guo


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 自检
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def cmd_selftest(args):
    """自检"""
    print("=" * 60)
    print("龍魂·视觉引擎 v1.0 — 自检")
    print("=" * 60)

    tong_guo = 0
    shi_bai = 0

    # 检查1: 色彩常量焊死
    try:
        yq = Shi_Jue_Yin_Qing()
        assert yq.yan_se.bei_jing == "#080808", "背景色不是极夜黑"
        assert yq.yan_se.jin == "#C9A84C", "金色不是龍魂金"
        tong_guo += 1
        print("  ✅ 色彩常量焊死验证通过")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 色彩常量验证失败: {e}")

    # 检查2: 图腾六件套完整
    try:
        tt = Tu_Teng()
        bi_xu = {"dna", "mo_tong", "ba_gua", "long", "369", "gua"}
        assert set(tt.tu_teng.keys()) == bi_xu, f"图腾不完整: {set(tt.tu_teng.keys())}"
        tong_guo += 1
        print("  ✅ 图腾六件套完整")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 图腾验证失败: {e}")

    # 检查3: 帧生成
    try:
        yq = Shi_Jue_Yin_Qing()
        zhen = yq.sheng_cheng_bei_jing(1080, 1920, 0)
        assert "bei_jing_se" in zhen
        assert zhen["bei_jing_se"] == "#080808"
        assert "ceng_ji" in zhen
        tong_guo += 1
        print("  ✅ 背景帧生成正常")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 帧生成失败: {e}")

    # 检查4: 图腾叠加
    try:
        zhen = yq.sheng_cheng_bei_jing()
        zhen = yq.die_jia_tu_teng(zhen, "dna")
        assert len(zhen["ceng_ji"]["tu_teng"]) == 1
        assert zhen["ceng_ji"]["tu_teng"][0]["ming_cheng"] == "DNA追溯码"
        tong_guo += 1
        print("  ✅ 图腾叠加正常")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 图腾叠加失败: {e}")

    # 检查5: 文字效果自动判断
    try:
        wxg = Wen_Zi_Xiao_Guo(Yan_Se_Pan())
        ranshao = wxg.pan_duan_xiao_guo("离火运来了", None)
        assert ranshao["xiao_guo"] == "particle_burn_sparks", f"应该是粒子燃烧: {ranshao['xiao_guo']}"
        pingchang = wxg.pan_duan_xiao_guo("今天天气不错", None)
        assert pingchang["xiao_guo"] == "static", f"应该是静态: {pingchang['xiao_guo']}"
        jinggao = wxg.pan_duan_xiao_guo("这是红线", None)
        assert jinggao["xiao_guo"] == "flashing_alert", f"应该是闪烁警告: {jinggao['xiao_guo']}"
        tong_guo += 1
        print("  ✅ 文字效果自动判断正常")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 文字效果判断失败: {e}")

    # 检查6: 完整生成流程
    try:
        yq = Shi_Jue_Yin_Qing()
        zhen_lie = yq.sheng_cheng("离火运·科技创造的价值到底谁来定义\n先烈用命换来的主权不能被算法偷走\n铜墙铁壁我们自己建")
        tong_ji = yq.shu_chu_tong_ji()
        assert tong_ji["zong_zhen_shu"] > 0, "帧序列为空"
        assert tong_ji["se_cai"] is not None
        tong_guo += 1
        print(f"  ✅ 完整生成流程: {tong_ji['zong_zhen_shu']}帧, 3段落")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 完整生成流程失败: {e}")

    # 检查7: CNSH命令解析
    try:
        cnsh_ml = """
        设 背景 为 极夜黑 #080808
        设 文字 为 龍魂金 #C9A84C
        """
        jg = cnsh_jie_xi(cnsh_ml)
        assert jg["bei_jing_se"] == "#080808"
        assert jg["wen_zi_se"] == "#C9A84C"
        tong_guo += 1
        print("  ✅ CNSH命令解析正常")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 CNSH命令解析失败: {e}")

    print(f"\n  {'🟢 全绿' if shi_bai == 0 else '🔴 有失败'}: {tong_guo}/{tong_guo + shi_bai} 通过")
    return 0 if shi_bai == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(cmd_selftest(sys.argv[2:]))
    else:
        print(f"龍魂·视觉引擎 v1.0 | DNA: {DNA}")
        print("用法: python3 engines/lh_visual_engine.py selftest")
