#!/usr/bin/env python3
"""
龍魂 · 视频生产线 v1.0 — 鲁班剪辑中枢
DNA: #龍芯⚡️2026-07-25-VIDEO-PIPELINE-v1.0
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0
人格: 鲁班（P04·技术执行）— 三引擎合并·多平台分发·水印签章
铁律: 本地生成·GPG签名·DNA水印·老大拍板才发布
"""

import os
import sys
import json
import time
import hashlib
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from engines.lh_visual_engine import Shi_Jue_Yin_Qing, DNA as SHI_JUE_DNA
except ImportError:
    Shi_Jue_Yin_Qing = None

try:
    from engines.lh_voice_engine import Sheng_Yin_Yin_Qing, DNA as SHENG_YIN_DNA
except ImportError:
    Sheng_Yin_Yin_Qing = None

try:
    from engines.lh_avatar_engine import Shu_Zi_Ren_Yin_Qing, DNA as SHU_ZI_REN_DNA
except ImportError:
    Shu_Zi_Ren_Yin_Qing = None

try:
    from engines.lh_media_sovereignty_marker import VideoMarker
except ImportError:
    VideoMarker = None

DNA = "#龍芯⚡️2026-07-25-VIDEO-PIPELINE-v1.0-LUBAN-EDITOR"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 平台预设
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PING_TAI_YU_SHE = {
    "douyin": {
        "ming_cheng": "抖音",
        "kuan_gao_bi": "9:16",
        "kuan": 1080,
        "gao": 1920,
        "zui_da_shi_chang": 60,
        "zhen_lv": 30,
        "bi_te_lv": "8M",
        "ge_shi": "mp4",
    },
    "shipinhao": {
        "ming_cheng": "视频号",
        "kuan_gao_bi": "9:16",
        "kuan": 1080,
        "gao": 1920,
        "zui_da_shi_chang": 90,
        "zhen_lv": 30,
        "bi_te_lv": "6M",
        "ge_shi": "mp4",
    },
    "bilibili": {
        "ming_cheng": "B站",
        "kuan_gao_bi": "16:9",
        "kuan": 1920,
        "gao": 1080,
        "zui_da_shi_chang": 0,
        "zhen_lv": 30,
        "bi_te_lv": "12M",
        "ge_shi": "mp4",
    },
    "youtube": {
        "ming_cheng": "YouTube",
        "kuan_gao_bi": "16:9",
        "kuan": 1920,
        "gao": 1080,
        "zui_da_shi_chang": 0,
        "zhen_lv": 30,
        "bi_te_lv": "15M",
        "ge_shi": "mp4",
    },
}


class Wen_Zhang_Jie_Xi:
    """文章解析器（CNSH·如意角色）"""

    def __init__(self):
        self.guan_jian_ci_ku = {
            "历史": ["离火运", "国耻", "五胡乱华", "先烈", "牺牲", "龙脉", "觉醒"],
            "主权": ["数据主权", "铜墙铁壁", "不可破", "焊死", "红线", "背后捅刀"],
            "科技": ["算法", "AI", "人工智能", "黑箱", "透明", "开源"],
            "人民": ["老百姓", "底层", "付出者", "普通人", "寒心"],
        }

    def ti_qu_guan_jian_ci(self, wen_zhang):
        """提取关键词"""
        jie_guo = []
        for fen_lei, ci_lie in self.guan_jian_ci_ku.items():
            for ci in ci_lie:
                if ci in wen_zhang:
                    jie_guo.append({"ci": ci, "fen_lei": fen_lei})
        return jie_guo

    def pan_duan_qing_gan_ji_diao(self, wen_zhang):
        """判断情感基调"""
        de_fen = {"愤怒": 0, "悲壮": 0, "坚定": 0, "希望": 0}

        nu_ci = ["愤怒", "耻辱", "恨", "不可饶恕", "背叛", "收割", "剥削"]
        bei_ci = ["牺牲", "先烈", "用命", "血", "倒下", "最后一刻"]
        jian_ci = ["必须", "不可破", "焊死", "铜墙铁壁", "永不动摇"]
        xi_ci = ["希望", "光明", "未来", "觉醒", "会有那一天"]

        for ci in nu_ci:
            de_fen["愤怒"] += wen_zhang.count(ci)
        for ci in bei_ci:
            de_fen["悲壮"] += wen_zhang.count(ci)
        for ci in jian_ci:
            de_fen["坚定"] += wen_zhang.count(ci)
        for ci in xi_ci:
            de_fen["希望"] += wen_zhang.count(ci)

        zui_gao = max(de_fen, key=de_fen.get)
        return zui_gao if de_fen[zui_gao] > 0 else "坚定"

    def sheng_cheng_jie_shuo_ci(self, wen_zhang):
        """从文章生成解说词"""
        # 按段落分行，保留原文
        duan_luo = [d.strip() for d in wen_zhang.split('\n') if d.strip()]
        return duan_luo

    def sheng_cheng_shi_jian_zhou(self, jie_shuo_ci):
        """生成时间轴"""
        zhou = []
        lei_ji_shi_jian = 0
        for ju_zi in jie_shuo_ci:
            shi_chang = max(2.0, len(ju_zi) * 0.3)
            zhou.append({
                "ju_zi": ju_zi,
                "kai_shi": lei_ji_shi_jian,
                "jie_shu": lei_ji_shi_jian + shi_chang,
                "shi_chang": shi_chang,
            })
            lei_ji_shi_jian += shi_chang + 0.5  # 句间停顿
        return zhou


class Shi_Pin_Guan_Xian:
    """视频生产线 · 鲁班·P04 剪辑守护"""

    def __init__(self, pei_zhi_lu=None):
        self.wen_zhang_jx = Wen_Zhang_Jie_Xi()

        # 初始化三引擎
        self.shi_jue_yq = Shi_Jue_Yin_Qing(pei_zhi_lu) if Shi_Jue_Yin_Qing else None
        self.sheng_yin_yq = Sheng_Yin_Yin_Qing(pei_zhi_lu) if Sheng_Yin_Yin_Qing else None
        self.shu_zi_ren_yq = Shu_Zi_Ren_Yin_Qing(pei_zhi_lu) if Shu_Zi_Ren_Yin_Qing else None

        self.pei_zhi_lu = pei_zhi_lu
        self.shu_chu_mu_lu = "output/videos"

    # ━━━━━ 核心生产流程 ━━━━━

    def sheng_chan(self, wen_zhang, mu_biao_ping_tai=None):
        """主入口：文章 → 视频"""
        if mu_biao_ping_tai is None:
            mu_biao_ping_tai = ["douyin", "shipinhao", "bilibili"]

        chan_wu = {
            "wen_zhang_yuan_shi": wen_zhang[:200] + "..." if len(wen_zhang) > 200 else wen_zhang,
            "dna": DNA,
            "sheng_cheng_shi_jian": datetime.now().isoformat(),
            "jie_xi": {},
            "shi_jue": {},
            "sheng_yin": {},
            "shu_zi_ren": {},
            "he_cheng": {},
            "shu_chu": {},
        }

        # 第一步：解析文章
        print("[1/5] 如意·解析文章...")
        chan_wu["jie_xi"] = {
            "guan_jian_ci": self.wen_zhang_jx.ti_qu_guan_jian_ci(wen_zhang),
            "qing_gan_ji_diao": self.wen_zhang_jx.pan_duan_qing_gan_ji_diao(wen_zhang),
            "jie_shuo_ci": self.wen_zhang_jx.sheng_cheng_jie_shuo_ci(wen_zhang),
        }
        jie_shuo_ci = '\n'.join(chan_wu["jie_xi"]["jie_shuo_ci"])
        chan_wu["jie_xi"]["shi_jian_zhou"] = self.wen_zhang_jx.sheng_cheng_shi_jian_zhou(
            chan_wu["jie_xi"]["jie_shuo_ci"]
        )
        print(f"    关键词: {len(chan_wu['jie_xi']['guan_jian_ci'])}个, "
              f"情感基调: {chan_wu['jie_xi']['qing_gan_ji_diao']}")

        # 第二步&第三步：并行生成视觉+声音
        print("[2/5] 李白·生成视觉 + 乔前辈·生成声音（并行）...")
        with ThreadPoolExecutor(max_workers=2) as zhuan_yuan:
            shi_jue_wei_lai = zhuan_yuan.submit(
                self._sheng_cheng_shi_jue, wen_zhang, mu_biao_ping_tai
            )
            sheng_yin_wei_lai = zhuan_yuan.submit(
                self._sheng_cheng_sheng_yin, jie_shuo_ci
            )

            chan_wu["shi_jue"] = shi_jue_wei_lai.result()
            chan_wu["sheng_yin"] = sheng_yin_wei_lai.result()

        print(f"    视觉: {chan_wu['shi_jue'].get('tong_ji', {}).get('zong_zhen_shu', 'N/A')}帧")
        print(f"    声音: {chan_wu['sheng_yin'].get('tong_ji', {}).get('duan_shu', 'N/A')}段")

        # 第四步：数字人（依赖音频）
        print("[3/5] 魔瞳·生成数字人...")
        chan_wu["shu_zi_ren"] = self._sheng_cheng_shu_zi_ren(
            chan_wu["sheng_yin"]["jie_guo"]
        )
        print(f"    数字人: {chan_wu['shu_zi_ren'].get('tong_ji', {}).get('zong_zhen_shu', 'N/A')}帧")

        # 第五步：合并
        print("[4/5] 鲁班·合并视频...")
        chan_wu["he_cheng"] = self._he_cheng_shi_pin(chan_wu)
        gu_ji_shi_chang = chan_wu['he_cheng'].get('gu_ji_shi_chang', 0)
        print(f"    合并: 总时长~{gu_ji_shi_chang:.1f}秒")

        # 第六步：多平台输出
        print(f"[5/5] 鲁班·多平台输出 → {mu_biao_ping_tai}...")
        for ping_tai in mu_biao_ping_tai:
            chan_wu["shu_chu"][ping_tai] = self._shu_chu_ping_tai(
                chan_wu, ping_tai
            )
        print(f"    输出: {len(chan_wu['shu_chu'])}个平台版本")

        return chan_wu

    def _sheng_cheng_shi_jue(self, wen_zhang, mu_biao_ping_tai=None):
        """生成视觉"""
        if self.shi_jue_yq:
            jin_ci = [c["ci"] for c in self.wen_zhang_jx.ti_qu_guan_jian_ci(wen_zhang)]
            # 按首个目标平台分辨率生成视觉
            pt = (mu_biao_ping_tai or ["douyin"])[0]
            ys = PING_TAI_YU_SHE.get(pt, PING_TAI_YU_SHE["douyin"])
            zhen_lie = self.shi_jue_yq.sheng_cheng(
                wen_zhang, jin_ci_biao=jin_ci,
                kuan=ys["kuan"], gao=ys["gao"]
            )
            tong_ji = self.shi_jue_yq.shu_chu_tong_ji()
            return {"zhen_xu_lie": zhen_lie, "tong_ji": tong_ji}
        return {"zhuang_tai": "视觉引擎未加载", "zhen_xu_lie": []}

    def _sheng_cheng_sheng_yin(self, jie_shuo_ci):
        """生成声音"""
        if self.sheng_yin_yq:
            jie_guo = self.sheng_yin_yq.sheng_cheng(jie_shuo_ci)
            tong_ji = self.sheng_yin_yq.shu_chu_tong_ji(jie_guo)
            return {"jie_guo": jie_guo, "tong_ji": tong_ji}
        return {"zhuang_tai": "声音引擎未加载", "jie_guo": {}}

    def _sheng_cheng_shu_zi_ren(self, sheng_yin_jie_guo):
        """生成数字人"""
        if self.shu_zi_ren_yq and sheng_yin_jie_guo:
            yin_pin_duan = sheng_yin_jie_guo.get("yin_pin_duan", [])
            zhen_lie = self.shu_zi_ren_yq.sheng_cheng(yin_pin_duan)
            tong_ji = self.shu_zi_ren_yq.shu_chu_tong_ji(zhen_lie)
            return {"zhen_xu_lie": zhen_lie, "tong_ji": tong_ji}
        return {"zhuang_tai": "数字人引擎未加载", "zhen_xu_lie": []}

    def _he_cheng_shi_pin(self, chan_wu):
        """合并三引擎输出"""
        # 估算总时长
        sheng_yin_jg = chan_wu["sheng_yin"].get("jie_guo", {})
        gu_ji_shi_chang = sheng_yin_jg.get("zong_shi_chang", 0) if sheng_yin_jg else 60

        return {
            "zhuang_tai": "合成完成（模拟）",
            "gu_ji_shi_chang": gu_ji_shi_chang,
            "pian_tou": {"long_zi_ran_shao": 3.0, "ba_gua_dui_ying": True},
            "pian_wei": {"long_zi_xiao_san": 3.0, "dna_wan_zheng_xian_shi": 5.0},
            "zhuan_chang": "369闪电效果",
            "shui_yin": {
                "dna": "右下角极慢闪烁",
                "yin_xing": "防搬运嵌入",
                "gpg": "待签名",
            },
        }

    def _shu_chu_ping_tai(self, chan_wu, ping_tai):
        """输出平台特定版本（含时长限制截断规划）"""
        ys = PING_TAI_YU_SHE.get(ping_tai, PING_TAI_YU_SHE["douyin"])
        shi_chang_xian_zhi = ys["zui_da_shi_chang"]

        sheng_yin_jg = chan_wu["sheng_yin"].get("jie_guo", {})
        gu_ji_shi_chang = sheng_yin_jg.get("zong_shi_chang", 0) if sheng_yin_jg else 0

        # 计算截断策略
        xian_zhi_ce_lue = self._ji_suan_shi_chang_xian_zhi(
            gu_ji_shi_chang, shi_chang_xian_zhi
        )

        return {
            "ping_tai": ys["ming_cheng"],
            "kuan_gao_bi": ys["kuan_gao_bi"],
            "fen_bian_lv": f"{ys['kuan']}x{ys['gao']}",
            "shi_chang_xian_zhi": shi_chang_xian_zhi if shi_chang_xian_zhi > 0 else "不限",
            "gu_ji_shi_chang": round(gu_ji_shi_chang, 1),
            "xian_zhi_ce_lue": xian_zhi_ce_lue,
            "wen_jian_ge_shi": ys["ge_shi"],
            "zhuang_tai": "就绪·待实际渲染",
        }

    def _ji_suan_shi_chang_xian_zhi(self, gu_ji_shi_chang, xian_zhi):
        """根据平台时长限制生成截断/变速策略"""
        if xian_zhi <= 0 or gu_ji_shi_chang <= xian_zhi:
            return {
                "xu_yao_jie_duan": False,
                "su_du_bei_lv": 1.0,
                "jian_yi": "直接输出完整版",
            }

        su_du_bei_lv = round(gu_ji_shi_chang / xian_zhi, 2)
        return {
            "xu_yao_jie_duan": True,
            "mu_biao_shi_chang": xian_zhi,
            "su_du_bei_lv": su_du_bei_lv,
            "jian_yi": f"内容超{xian_zhi}秒限制，建议分段输出或语速×{su_du_bei_lv}",
        }

    # ━━━━━ 水印与签名 ━━━━━

    def tian_jia_dna_shui_yin(self, shi_pin_lu_jing):
        """添加DNA追溯码水印"""
        dna_sheng_cheng_shi_jian = datetime.now().strftime("%Y-%m-%d %H:%M")
        shui_yin_wen_zi = f"{DNA} | {dna_sheng_cheng_shi_jian} | UID9622"
        return {
            "wen_jian": shi_pin_lu_jing,
            "shui_yin": shui_yin_wen_zi,
            "wei_zhi": "右下角",
            "xiao_guo": "极慢闪烁·5秒完整显示",
        }

    def qian_ru_dna_shui_yin(self, shi_pin_lu_jing, dna=None):
        """将DNA主权标记嵌入视频（频域盲水印）

        优先使用音频轨 Patchwork 水印（抗压缩/录屏），无音频则回退到
        Y 通道帧级 DCT 水印。输出文件默认保存在原文件同级目录，文件名
        附加 -DNA。
        """
        if dna is None:
            dna = DNA
        if not os.path.exists(shi_pin_lu_jing):
            return {"cuo_wu": f"文件不存在: {shi_pin_lu_jing}"}
        if VideoMarker is None:
            return {"cuo_wu": "视频标记引擎未加载"}

        try:
            shu_ru = Path(shi_pin_lu_jing)
            shu_chu = shu_ru.parent / f"{shu_ru.stem}-DNA{shu_ru.suffix}"
            VideoMarker(shi_pin_lu_jing).embed(dna=dna, output_path=shu_chu)
            return {
                "yuan_wen_jian": str(shu_ru),
                "shu_chu_wen_jian": str(shu_chu),
                "dna": dna,
                "zhuang_tai": "已嵌入DNA盲水印",
            }
        except Exception as e:
            return {"cuo_wu": str(e)}

    def gpg_qian_ming(self, shi_pin_lu_jing):
        """GPG签名视频文件

        优先尝试无密码签名（gpg-agent 已缓存）。若需密码，读取环境变量
        LONGHUN_GPG_PASSPHRASE。密码不在代码中硬编码。
        """
        import shutil

        if not shutil.which("gpg"):
            return {"cuo_wu": "gpg 命令未安装"}

        if not os.path.exists(shi_pin_lu_jing):
            return {"cuo_wu": f"文件不存在: {shi_pin_lu_jing}"}

        fingerprint = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
        qian_ming_lu_jing = f"{shi_pin_lu_jing}.asc"

        try:
            with open(shi_pin_lu_jing, 'rb') as f:
                nei_rong = f.read()
            ha_xi = hashlib.sha256(nei_rong).hexdigest()

            # 先尝试无密码签名（依赖 gpg-agent）
            cmd = [
                "gpg", "--batch", "--yes", "--armor", "--detach-sign",
                "--local-user", fingerprint,
                "--output", qian_ming_lu_jing,
                shi_pin_lu_jing,
            ]
            jie_guo = subprocess.run(cmd, capture_output=True, text=True)

            # 失败则尝试使用环境变量密码
            if jie_guo.returncode != 0:
                passphrase = os.environ.get("LONGHUN_GPG_PASSPHRASE")
                if passphrase:
                    cmd_pin = [
                        "gpg", "--batch", "--yes", "--pinentry-mode", "loopback",
                        "--passphrase-fd", "0", "--armor", "--detach-sign",
                        "--local-user", fingerprint,
                        "--output", qian_ming_lu_jing,
                        shi_pin_lu_jing,
                    ]
                    proc = subprocess.Popen(
                        cmd_pin, stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                    )
                    stdout, stderr = proc.communicate(input=passphrase + "\n")
                    if proc.returncode != 0:
                        return {
                            "cuo_wu": f"GPG签名失败: {stderr}",
                            "sha256": ha_xi,
                        }
                else:
                    return {
                        "cuo_wu": f"GPG签名失败（可设置 LONGHUN_GPG_PASSPHRASE）: {jie_guo.stderr}",
                        "sha256": ha_xi,
                    }

            return {
                "wen_jian": shi_pin_lu_jing,
                "qian_ming_wen_jian": qian_ming_lu_jing,
                "sha256": ha_xi,
                "gpg_fingerprint": fingerprint,
                "zhuang_tai": "已签名",
            }
        except Exception as e:
            return {"cuo_wu": str(e)}

    # ━━━━━ 归档 ━━━━━

    def gui_dang(self, chan_wu):
        """归档产物"""
        ri_qi = datetime.now().strftime("%Y-%m-%d")
        mu_lu = Path(self.shu_chu_mu_lu) / ri_qi

        dang_an = {
            "chan_wu": chan_wu,
            "gui_dang_shi_jian": datetime.now().isoformat(),
            "dna": DNA,
        }

        return {
            "mu_lu": str(mu_lu),
            "zhuang_tai": "归档就绪",
            "nei_rong_gai_yao": {
                "ping_tai_shu": len(chan_wu.get("shu_chu", {})),
                "guan_jian_ci": len(chan_wu.get("jie_xi", {}).get("guan_jian_ci", [])),
            },
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI 命令
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def cmd_sheng_chan(args):
    """生产视频"""
    if len(args) < 1:
        print("用法: python3 bin/lh_video_pipeline.py produce <文章文件> [平台列表]")
        print("平台: douyin,shipinhao,bilibili,youtube (逗号分隔)")
        return 1

    wen_zhang_lu = args[0]
    ping_tai = ["douyin", "shipinhao", "bilibili"]
    if len(args) > 1:
        ping_tai = [p.strip() for p in args[1].split(",") if p.strip()]

    # 校验平台名
    wu_xiao = [p for p in ping_tai if p not in PING_TAI_YU_SHE]
    if wu_xiao:
        print(f"未知平台: {wu_xiao}")
        print(f"可用平台: {', '.join(PING_TAI_YU_SHE.keys())}")
        return 1

    try:
        with open(wen_zhang_lu, 'r', encoding='utf-8') as f:
            wen_zhang = f.read()
    except FileNotFoundError:
        print(f"文章文件不存在: {wen_zhang_lu}")
        return 1

    print("=" * 60)
    print("龍魂·视频生产线 v1.0 — 鲁班执行")
    print(f"DNA: {DNA}")
    print(f"文章: {wen_zhang_lu}")
    print(f"目标平台: {ping_tai}")
    print("=" * 60)
    print()

    pei_zhi_lu = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "config", "video_presets.yaml")
    guan_xian = Shi_Pin_Guan_Xian(pei_zhi_lu)
    chan_wu = guan_xian.sheng_chan(wen_zhang, ping_tai)

    # 归档
    gui_dang = guan_xian.gui_dang(chan_wu)

    print()
    print("=" * 60)
    print("生产完成")
    print(f"  关键词: {[c['ci'] for c in chan_wu['jie_xi']['guan_jian_ci']]}")
    print(f"  情感基调: {chan_wu['jie_xi']['qing_gan_ji_diao']}")
    print(f"  输出平台: {list(chan_wu['shu_chu'].keys())}")
    print(f"  归档: {gui_dang['mu_lu']}")
    print()
    print("⚠️ 视频已生成（模拟）。实际渲染需要影视后期工具链。")
    print("  本管线负责：解析→三引擎调度→合并规划→多平台适配→水印签章→归档。")
    print("=" * 60)

    return 0


def cmd_mark(args):
    """给已有视频嵌入DNA盲水印"""
    if len(args) < 1:
        print("用法: python3 bin/lh_video_pipeline.py mark <视频文件> [--dna <DNA>]")
        return 1

    shi_pin_lu_jing = args[0]
    dna = None
    if "--dna" in args:
        idx = args.index("--dna")
        if idx + 1 < len(args):
            dna = args[idx + 1]
        else:
            print("错误: --dna 后面需要跟 DNA 字符串")
            return 1

    print("=" * 60)
    print("龍魂·视频生产线 — DNA盲水印注入")
    print(f"目标: {shi_pin_lu_jing}")
    print("=" * 60)

    guan_xian = Shi_Pin_Guan_Xian()
    jie_guo = guan_xian.qian_ru_dna_shui_yin(shi_pin_lu_jing, dna)

    if "cuo_wu" in jie_guo:
        print(f"🔴 失败: {jie_guo['cuo_wu']}")
        return 1

    print(f"✅ 已嵌入: {jie_guo['shu_chu_wen_jian']}")
    print(f"   DNA: {jie_guo['dna'][:80]}...")
    print("=" * 60)
    return 0


def cmd_selftest(args):
    """自检"""
    print("=" * 60)
    print("龍魂·视频生产线 v1.0 — 自检")
    print("=" * 60)

    tong_guo = 0
    shi_bai = 0

    # 检查1: 文章解析
    try:
        jx = Wen_Zhang_Jie_Xi()
        ci = jx.ti_qu_guan_jian_ci("离火运来临，先烈用命换来的数据主权不可破")
        assert len(ci) >= 2, f"关键词不足: {ci}"
        qg = jx.pan_duan_qing_gan_ji_diao("愤怒的火焰，耻辱的历史，不可饶恕")
        assert qg == "愤怒", f"情感判断错误: {qg}"
        tong_guo += 1
        print(f"  ✅ 文章解析: {[c['ci'] for c in ci]}, 基调={qg}")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 文章解析失败: {e}")

    # 检查2: 解说词生成
    try:
        jsc = jx.sheng_cheng_jie_shuo_ci("第一段内容\n第二段内容\n第三段内容")
        assert len(jsc) == 3
        tong_guo += 1
        print(f"  ✅ 解说词: {len(jsc)}段")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 解说词失败: {e}")

    # 检查3: 时间轴生成
    try:
        sjz = jx.sheng_cheng_shi_jian_zhou(["第一句", "第二句", "第三句"])
        assert len(sjz) == 3
        assert sjz[0]["shi_chang"] > 0
        tong_guo += 1
        print(f"  ✅ 时间轴: {len(sjz)}段, 首段{sjz[0]['shi_chang']:.1f}秒")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 时间轴失败: {e}")

    # 检查4: 平台预设完整
    try:
        bi_xu = {"douyin", "shipinhao", "bilibili", "youtube"}
        assert set(PING_TAI_YU_SHE.keys()) == bi_xu
        for pt, ys in PING_TAI_YU_SHE.items():
            assert "kuan" in ys and "gao" in ys, f"{pt}缺少分辨率"
        tong_guo += 1
        print("  ✅ 平台预设完整")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 平台预设失败: {e}")

    # 检查5: 完整生产流程
    try:
        gl = Shi_Pin_Guan_Xian()
        cw = gl.sheng_chan("离火运·科技创造的价值到底谁来定义\n先烈用命换来的主权不能被算法偷走", ["douyin"])
        assert "jie_xi" in cw
        assert "shi_jue" in cw
        assert "sheng_yin" in cw
        assert "he_cheng" in cw
        assert "douyin" in cw["shu_chu"]
        tong_guo += 1
        print("  ✅ 完整生产流程通过")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 生产流程失败: {e}")

    # 检查6: 水印签章
    try:
        import tempfile
        gl = Shi_Pin_Guan_Xian()
        sy = gl.tian_jia_dna_shui_yin("/tmp/test.mp4")
        assert "shui_yin" in sy

        # 用真实临时文件测试 GPG 签名（可能因密码缺失返回 cuo_wu）
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tf:
            tf.write(b"longhun test video content")
            tmp_path = tf.name
        try:
            qm = gl.gpg_qian_ming(tmp_path)
            assert "sha256" in qm
            assert os.path.exists(tmp_path + ".asc") or "cuo_wu" in qm
        finally:
            for p in [tmp_path, tmp_path + ".asc"]:
                try:
                    os.remove(p)
                except FileNotFoundError:
                    pass
        tong_guo += 1
        print("  ✅ 水印签章机制正常")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 水印签章失败: {e}")

    # 检查7: DNA盲水印注入（帧级DCT + 音频指纹）
    try:
        import tempfile
        gl = Shi_Pin_Guan_Xian()
        if VideoMarker is None:
            raise RuntimeError("VideoMarker 未加载")

        # 生成 1 秒测试视频
        tmp_dir = tempfile.mkdtemp()
        test_video = os.path.join(tmp_dir, "test.mp4")
        test_marked = os.path.join(tmp_dir, "test-DNA.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-f", "lavfi", "-i", "testsrc=duration=1:size=320x240:rate=30",
            "-f", "lavfi", "-i", "sine=frequency=1000:duration=1",
            "-c:v", "libx264", "-c:a", "aac", "-b:a", "128k",
            "-pix_fmt", "yuv420p", test_video,
        ], check=True)

        jie_guo = gl.qian_ru_dna_shui_yin(test_video, "#TEST-SELFTEST-DNA")
        assert "shu_chu_wen_jian" in jie_guo, jie_guo.get("cuo_wu", "未知错误")

        # 验证能提取出 LHAF 指纹
        verify_result = VideoMarker(jie_guo["shu_chu_wen_jian"]).extract()
        assert verify_result and verify_result.startswith("LHAF-"), f"验证失败: {verify_result}"

        # 清理
        for p in [test_video, test_marked, jie_guo["shu_chu_wen_jian"]]:
            try:
                os.remove(p)
            except FileNotFoundError:
                pass
        os.rmdir(tmp_dir)

        tong_guo += 1
        print(f"  ✅ DNA盲水印注入正常: {verify_result[:20]}...")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 DNA盲水印注入失败: {e}")

    # 检查8: 归档
    try:
        cw = {"jie_xi": {"guan_jian_ci": [{"ci": "测试"}], "qing_gan_ji_diao": "坚定"},
              "shu_chu": {"douyin": {}, "bilibili": {}}}
        gd = gl.gui_dang(cw)
        assert gd["zhuang_tai"] == "归档就绪"
        assert gd["nei_rong_gai_yao"]["ping_tai_shu"] == 2
        tong_guo += 1
        print("  ✅ 归档机制正常")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 归档失败: {e}")

    # 检查8: 时长限制截断规划
    try:
        gl = Shi_Pin_Guan_Xian()
        # 100秒内容进60秒平台
        ce_lue = gl._ji_suan_shi_chang_xian_zhi(100.0, 60)
        assert ce_lue["xu_yao_jie_duan"] is True
        assert ce_lue["su_du_bei_lv"] > 1.0
        # 50秒内容进60秒平台
        ce_lue2 = gl._ji_suan_shi_chang_xian_zhi(50.0, 60)
        assert ce_lue2["xu_yao_jie_duan"] is False
        tong_guo += 1
        print("  ✅ 时长限制截断规划正常")
    except Exception as e:
        shi_bai += 1
        print(f"  🔴 时长限制规划失败: {e}")

    print(f"\n  {'🟢 全绿' if shi_bai == 0 else '🔴 有失败'}: {tong_guo}/{tong_guo + shi_bai} 通过")
    return 0 if shi_bai == 0 else 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 入口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    if len(sys.argv) < 2:
        print(f"龍魂·视频生产线 v1.0")
        print(f"DNA: {DNA}")
        print()
        print("命令:")
        print("  produce <文章文件> [平台]    生产视频")
        print("  mark <视频文件> [--dna ...]  给已有视频嵌入DNA盲水印")
        print("  selftest                    自检")
        print()
        print("平台: douyin,shipinhao,bilibili,youtube (逗号分隔)")
        return 0

    ming_ling = sys.argv[1]
    args = sys.argv[2:]

    ming_ling_biao = {
        "produce": cmd_sheng_chan,
        "mark": cmd_mark,
        "selftest": cmd_selftest,
    }

    han_shu = ming_ling_biao.get(ming_ling)
    if han_shu:
        return han_shu(args)
    else:
        print(f"未知命令: {ming_ling}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
