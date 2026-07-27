#!/usr/bin/env python3
"""
龍魂 · 数字人引擎 v1.0 — 魔瞳凝视
DNA: #龍芯⚡️2026-07-25-AVATAR-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0
人格: 魔瞳（P01·形象守护）— 眼神不动点守护
铁律: 眼神始终凝视观众·穿透屏幕·让心不干净的人害怕·全部本地生成
"""

import os
import sys
import json
import math
from pathlib import Path

DNA = "#龍芯⚡️2026-07-25-AVATAR-ENGINE-v1.0-MOTONG-GAZE"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# P0 焊死形象常量
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
XING_XIANG_FENG_GE = "暗黑鎏金"
FU_SE = "dark_metallic"
FU_ZHUANG = "dark_military"
BIAN_KUANG = "gold_thin"
MU_BIAO = "viewer"
NING_SHI_QIANG_DU = 0.95

# 表情-情感联动表
BIAO_QING_LIAN_DONG = {
    "愤怒": {"mei_mao": "紧锁", "yan_shen": "瞪大+锐利", "zui_xing_xi_shu": 1.2},
    "悲壮": {"mei_mao": "微皱", "yan_shen": "深邃+微红", "zui_xing_xi_shu": 0.8},
    "坚定": {"mei_mao": "自然", "yan_shen": "直视+不动", "zui_xing_xi_shu": 1.0},
    "嘲讽": {"mei_mao": "微扬", "yan_shen": "锐利+微眯", "zui_jiao": "上扬"},
    "希望": {"mei_mao": "放松", "yan_shen": "明亮", "zui_xing_xi_shu": 1.0},
}

# 基础口型映射（汉语拼音声母韵母 → 口型编号）
KOU_XING_YING_SHE = {
    "a": 1, "o": 2, "e": 3, "i": 4, "u": 5, "v": 6,
    "b": 7, "p": 7, "m": 7,
    "f": 8,
    "d": 9, "t": 9, "n": 9, "l": 9,
    "g": 10, "k": 10, "h": 10,
    "j": 11, "q": 11, "x": 11,
    "zh": 12, "ch": 12, "sh": 12, "r": 12,
    "z": 13, "c": 13, "s": 13,
}


class Mo_Tong_Xing_Xiang:
    """魔瞳形象定义"""
    def __init__(self):
        self.feng_ge = XING_XIANG_FENG_GE
        self.fu_se = FU_SE
        self.fu_zhuang = FU_ZHUANG
        self.bian_kuang = BIAN_KUANG
        self.te_zheng = [
            "深邃凝视·穿透屏幕",
            "非真人感·神秘感",
            "老兵身份·暗色军装",
            "心不干净的人看了害怕",
        ]

    def yan_zheng_xing_xiang(self, shu_ju):
        """验证形象是否偏离焊死标准"""
        wei_gui = []
        if shu_ju.get("肤色") != FU_SE:
            wei_gui.append(f"肤色偏离: {shu_ju.get('肤色')} != {FU_SE}")
        if shu_ju.get("服装风格") != FU_ZHUANG:
            wei_gui.append(f"服装偏离: {shu_ju.get('服装风格')} != {FU_ZHUANG}")
        return len(wei_gui) == 0, wei_gui


class Yan_Shen_Gui_Ji:
    """眼神追踪器"""

    def __init__(self):
        self.mu_biao = MU_BIAO
        self.qiang_du = NING_SHI_QIANG_DU
        self.dang_qian_qing_gan = "坚定"
        self.jie_wei_zha_yan = False

    def suo_ding_ning_shi(self, zhen_bian_hao):
        """锁定凝视观众"""
        return {
            "mu_biao": self.mu_biao,
            "qiang_du": self.qiang_du,
            "pian_yi": (0.0, 0.0),  # 不偏移
            "wei_yi": 0.0,
        }

    def qing_gan_yan_shen(self, qing_gan):
        """根据情感调整眼神参数"""
        if qing_gan == "愤怒":
            return {"yan_da": 1.2, "rui_li": 1.0, "wei_hong": 0.0}
        elif qing_gan == "悲壮":
            return {"yan_da": 1.0, "rui_li": 0.8, "wei_hong": 0.3}
        elif qing_gan == "嘲讽":
            return {"yan_da": 0.9, "rui_li": 1.1, "wei_hong": 0.0, "wei_mi": True}
        elif qing_gan == "希望":
            return {"yan_da": 1.0, "rui_li": 0.7, "wei_hong": 0.0, "ming_liang": True}
        else:  # 坚定
            return {"yan_da": 1.0, "rui_li": 0.9, "wei_hong": 0.0}


class Zui_Xing_Tong_Bu:
    """嘴型同步器"""

    def __init__(self):
        self.tong_bu_jing_du = 0.05  # 50ms精度

    def yin_su_dao_kou_xing(self, pin_yin):
        """拼音→口型编号"""
        # 简单映射
        for yun_mu in ["a", "o", "e", "i", "u", "v"]:
            if yun_mu in pin_yin:
                return KOU_XING_YING_SHE[yun_mu]
        for sheng_mu in ["zh", "ch", "sh", "b", "p", "m", "f", "d", "t", "n", "l",
                          "g", "k", "h", "j", "q", "x", "z", "c", "s", "r"]:
            if pin_yin.startswith(sheng_mu):
                return KOU_XING_YING_SHE.get(sheng_mu, 0)
        return 0  # 闭嘴

    def sheng_cheng_kou_xing_xu_lie(self, yin_pin_duan_lie):
        """为音频段生成口型序列

        每个字绑定所在句子的情感（duan_index/qing_gan），供数字人帧生成时
        正确选择表情，避免按帧号误映射情感。
        """
        kou_xing_xu_lie = []

        for duan_index, ypd in enumerate(yin_pin_duan_lie):
            ju_zi = ypd["ju_zi"]
            qing_gan = ypd["qing_gan"]
            xi_shu = BIAO_QING_LIAN_DONG.get(qing_gan, {}).get("zui_xing_xi_shu", 1.0)

            for zi in ju_zi:
                # 优先用拼音映射口型；无拼音支持时按字符 Unicode 稳定映射
                kou_xing_id = self._kou_xing_id_for_zi(zi)
                kou_xing_xu_lie.append({
                    "zi": zi,
                    "kou_xing_id": kou_xing_id,
                    "xi_shu": xi_shu,
                    "chi_xu": 0.3 / ypd["yu_su"],
                    "qing_gan": qing_gan,
                    "duan_index": duan_index,
                })

        return kou_xing_xu_lie

    def _kou_xing_id_for_zi(self, zi: str) -> int:
        """字 → 口型编号。优先 pypinyin；否则用 Unicode 码点稳定占位。"""
        try:
            import pypinyin
            py = pypinyin.lazy_pinyin(zi)
            if py:
                return self.yin_su_dao_kou_xing(py[0])
        except ImportError:
            pass
        # 无 pypinyin 时：按 Unicode 码点稳定取模，保持同一字口型一致
        return ord(zi) % 14


class Shu_Zi_Ren_Yin_Qing:
    """数字人引擎 · 魔瞳·P01 形象守护"""

    def __init__(self, pei_zhi_lu=None):
        self.xing_xiang = Mo_Tong_Xing_Xiang()
        self.yan_shen_gj = Yan_Shen_Gui_Ji()
        self.zui_xing_tb = Zui_Xing_Tong_Bu()
        self.pei_zhi = {}

        if pei_zhi_lu:
            self._jia_zai_pei_zhi(pei_zhi_lu)

        self.mo_xing_lu = "models/avatar/motong_v1.pt"
        self.mo_xing_yi_jia_zai = False

    def _jia_zai_pei_zhi(self, lu_jing):
        try:
            import yaml
            with open(lu_jing, 'r') as f:
                self.pei_zhi = yaml.safe_load(f)
        except Exception:
            self.pei_zhi = {}

    def jia_zai_mo_xing(self):
        """加载数字人模型"""
        if not os.path.exists(self.mo_xing_lu):
            return False, f"模型文件不存在: {self.mo_xing_lu}"
        # TODO: 实际模型加载
        self.mo_xing_yi_jia_zai = True
        return True, "模型已加载"

    # ━━━━━ 数字人生成核心 ━━━━━

    def sheng_cheng_yi_zhen(self, zhen_bian_hao, kou_xing_id, qing_gan, zhen_zong_shu):
        """生成单帧数字人"""
        # 眼神
        ning_shi = self.yan_shen_gj.suo_ding_ning_shi(zhen_bian_hao)
        yan_shen_can_shu = self.yan_shen_gj.qing_gan_yan_shen(qing_gan)

        # 表情
        biao_qing = BIAO_QING_LIAN_DONG.get(qing_gan, BIAO_QING_LIAN_DONG["坚定"])

        # 结尾缓慢眨眼
        jie_wei_zha_yan = False
        if zhen_bian_hao >= zhen_zong_shu - 30:  # 最后1秒
            jie_wei_zha_yan = (zhen_bian_hao == zhen_zong_shu - 1)

        zhen = {
            "bian_hao": zhen_bian_hao,
            "ning_shi": ning_shi,
            "yan_shen": yan_shen_can_shu,
            "biao_qing": biao_qing,
            "kou_xing_id": kou_xing_id,
            "jie_wei_zha_yan": jie_wei_zha_yan,
            "xing_xiang": {
                "feng_ge": self.xing_xiang.feng_ge,
                "fu_se": self.xing_xiang.fu_se,
                "fu_zhuang": self.xing_xiang.fu_zhuang,
            },
        }
        return zhen

    def sheng_cheng(self, yin_pin_duan_lie, shi_jue_jiao_ben=None):
        """主入口：音频段 → 数字人帧序列"""
        if not yin_pin_duan_lie:
            return []

        # 生成口型序列（已绑定每字所属句子情感）
        kou_xing_xu_lie = self.zui_xing_tb.sheng_cheng_kou_xing_xu_lie(yin_pin_duan_lie)

        zhen_xu_lie = []
        zhen_zong_shu = len(kou_xing_xu_lie)

        for bian_hao, kx in enumerate(kou_xing_xu_lie):
            # 从口型条目直接读取所在句子情感，避免按帧号误映射
            qing_gan = kx.get("qing_gan", "坚定")

            zhen = self.sheng_cheng_yi_zhen(
                bian_hao, kx["kou_xing_id"], qing_gan, zhen_zong_shu
            )
            zhen_xu_lie.append(zhen)

        return zhen_xu_lie

    # ━━━━━ 输出 ━━━━━

    def shu_chu_tong_ji(self, zhen_xu_lie):
        """输出统计"""
        return {
            "zong_zhen_shu": len(zhen_xu_lie),
            "xing_xiang": self.xing_xiang.feng_ge,
            "ning_shi_qiang_du": self.yan_shen_gj.qiang_du,
            "dna": DNA,
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CNSH 命令解析
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def cnsh_jie_xi(ming_ling):
    """解析CNSH数字人命令"""
    jie_guo = {
        "xing_xiang": XING_XIANG_FENG_GE,
        "ning_shi_qiang_du": NING_SHI_QIANG_DU,
        "zui_xing_tong_bu": 0.05,
    }

    hang = ming_ling.strip().split('\n')
    for h in hang:
        h = h.strip()
        if '同步精度' in h:
            try:
                jie_guo["zui_xing_tong_bu"] = float(re.findall(r'[\d.]+', h)[0])
            except Exception:
                pass
        if '凝视' in h:
            jie_guo["ning_shi_qiang_du"] = NING_SHI_QIANG_DU

    return jie_guo


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 自检
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def cmd_selftest(args):
    """自检"""
    import re as regex_module

    print("=" * 60)
    print("龍魂·数字人引擎 v1.0 — 自检")
    print("=" * 60)

    tong_guo = 0
    shi_bai = 0

    # 检查1: 形象焊死
    try:
        xx = Mo_Tong_Xing_Xiang()
        assert xx.feng_ge == "暗黑鎏金"
        assert xx.fu_se == "dark_metallic"
        ok, wei_gui = xx.yan_zheng_xing_xiang({"肤色": "dark_metallic", "服装风格": "dark_military"})
        assert ok, f"形象验证失败: {wei_gui}"
        ok2, wg2 = xx.yan_zheng_xing_xiang({"肤色": "white", "服装风格": "suit"})
        assert not ok2, "应该拒绝偏离形象"
        tong_guo += 1
        print("  ✅ 形象焊死验证通过")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 形象验证失败: {e}")

    # 检查2: 眼神锁定
    try:
        ysgj = Yan_Shen_Gui_Ji()
        ns = ysgj.suo_ding_ning_shi(0)
        assert ns["mu_biao"] == "viewer"
        assert ns["qiang_du"] == 0.95
        assert ns["pian_yi"] == (0.0, 0.0), "眼神不能偏移"
        tong_guo += 1
        print("  ✅ 眼神锁定正常")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 眼神锁定失败: {e}")

    # 检查3: 情感眼神
    try:
        ysgj = Yan_Shen_Gui_Ji()
        fn_ys = ysgj.qing_gan_yan_shen("愤怒")
        assert fn_ys["yan_da"] == 1.2, "愤怒应瞪大"
        bz_ys = ysgj.qing_gan_yan_shen("悲壮")
        assert bz_ys["wei_hong"] == 0.3, "悲壮应微红"
        tong_guo += 1
        print("  ✅ 情感眼神联动正常")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 情感眼神失败: {e}")

    # 检查4: 表情联动完整
    try:
        bi_xu_qing_gan = {"愤怒", "悲壮", "坚定", "嘲讽", "希望"}
        assert set(BIAO_QING_LIAN_DONG.keys()) == bi_xu_qing_gan
        for qg, bq in BIAO_QING_LIAN_DONG.items():
            assert "mei_mao" in bq, f"{qg}缺少眉毛"
            assert "yan_shen" in bq, f"{qg}缺少眼神"
        tong_guo += 1
        print("  ✅ 表情联动完整")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 表情联动失败: {e}")

    # 检查5: 口型映射
    try:
        zxtb = Zui_Xing_Tong_Bu()
        assert zxtb.yin_su_dao_kou_xing("a") > 0, "a映射失败"
        assert zxtb.yin_su_dao_kou_xing("zh") > 0, "zh映射失败"
        assert zxtb.yin_su_dao_kou_xing("b") > 0, "b映射失败"
        tong_guo += 1
        print("  ✅ 口型映射正常")
    except AssertionError as e:
        shi_bai += 1
        print(f"  🔴 口型映射失败: {e}")

    # 检查6: 数字人帧生成
    try:
        yq = Shu_Zi_Ren_Yin_Qing()
        zhen = yq.sheng_cheng_yi_zhen(0, 5, "坚定", 900)
        assert zhen["bian_hao"] == 0
        assert zhen["ning_shi"]["mu_biao"] == "viewer"
        assert zhen["xing_xiang"]["feng_ge"] == "暗黑鎏金"
        tong_guo += 1
        print("  ✅ 数字人帧生成正常")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 数字人帧生成失败: {e}")

    # 检查7: 完整序列生成 + 情感正确绑定
    try:
        yq = Shu_Zi_Ren_Yin_Qing()
        # 模拟音频段：愤怒2字 + 悲壮2字 + 坚定2字
        yin_pin_duan_lie = [
            {"ju_zi": "愤怒", "qing_gan": "愤怒", "yu_su": 0.9},
            {"ju_zi": "悲壮", "qing_gan": "悲壮", "yu_su": 0.9},
            {"ju_zi": "坚定", "qing_gan": "坚定", "yu_su": 0.9},
        ]
        zhen_lie = yq.sheng_cheng(yin_pin_duan_lie)
        assert len(zhen_lie) == 6, f"应为6帧: {len(zhen_lie)}"
        # 验证每帧情感与所在句子一致
        assert zhen_lie[0]["biao_qing"]["mei_mao"] == BIAO_QING_LIAN_DONG["愤怒"]["mei_mao"]
        assert zhen_lie[2]["biao_qing"]["mei_mao"] == BIAO_QING_LIAN_DONG["悲壮"]["mei_mao"]
        assert zhen_lie[4]["biao_qing"]["mei_mao"] == BIAO_QING_LIAN_DONG["坚定"]["mei_mao"]
        tong_ji = yq.shu_chu_tong_ji(zhen_lie)
        assert tong_ji["ning_shi_qiang_du"] == 0.95
        tong_guo += 1
        print(f"  ✅ 完整序列生成: {len(zhen_lie)}帧·情感绑定正确")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 完整序列生成失败: {e}")

    print(f"\n  {'🟢 全绿' if shi_bai == 0 else '🔴 有失败'}: {tong_guo}/{tong_guo + shi_bai} 通过")
    return 0 if shi_bai == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(cmd_selftest(sys.argv[2:]))
    else:
        print(f"龍魂·数字人引擎 v1.0 | DNA: {DNA}")
        print("用法: python3 engines/lh_avatar_engine.py selftest")
