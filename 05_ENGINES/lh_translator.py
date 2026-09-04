#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂 · 隐语法翻译层 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-YIN-YU-FA-TRANSLATOR-v1.0
创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0

对外接口与对内核心代码之间的双向翻译桥梁。
对外 → 对内: 英文术语 → 拼音代号
对内 → 对外: 拼音代号 → 英文术语

铁律：翻译层不可绕过。对外暴露内部命名即P0违规。
守护人格: 仓颉(P08符号语言) · 签章: CANGJIE-TRANSLATOR-2026
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-YIN-YU-FA-TRANSLATOR-v1.0"

# ═══ 翻译词典 ═══
_yu_fa_ci_dian = {
    # 安全与加密层
    "jia_mi": "encrypt",
    "jie_mi": "decrypt",
    "yao_pai_sheng": "key_derivation",
    "she_bei_wen": "device_fingerprint",
    "sheng_wu_jian": "biometric_auth",
    "cheng_qiang": "firewall_rules",
    "shen_ji_zhang": "audit_log",
    "ling_xin": "zero_trust",
    "hou_men": "backdoor",
    # 数据与存储层
    "min_ji": "user_data",
    "ben_di_cang": "local_storage",
    "yun_tong": "cloud_sync",
    "shu_zhu": "data_sovereignty",
    "bao_gui": "vault",
    "bei_fen": "backup",
    # 计算与网络层
    "ying_zhai": "server",
    "suan_chou": "compute_task",
    "wu_tai_men": "stateless_api",
    "guan_kou": "gateway",
    "guan_dao": "pipeline",
    "jun_heng": "load_balancer",
    # 治理与协议层
    "xian_fa": "constitution",
    "gui_yue": "protocol",
    "zhi_li": "governance",
    "he_gui": "compliance",
    "wei_gui": "violation",
    # 人格与系统层
    "ren_ge": "persona",
    "tong_shuai": "orchestrator",
    "shi_guan": "chronicler",
    "shou_hu": "guardian",
    "jin_hua": "evolution",
    # 算力分离扩展
    "tuo_min": "desensitize",
    "suan_li": "compute_power",
    "zheng_ming": "proof",
    "qian_ming": "signature",
    "yan_zheng": "verify",
    "wan_zheng_xing": "integrity",
    "chu_li": "process",
    "ji_lu": "record",
    "jie_guo": "result",
    "cuo_wu": "error",
    "jing_gao": "warning",
    "fa_song": "send",
    "jie_shou": "receive",
    "qing_qiu": "request",
    "xiang_ying": "response",
    "lian_jie": "connect",
    "duan_kai": "disconnect",
    "chong_zhi": "reset",
    "shi_bai": "failure",
    "cheng_gong": "success",
}


class LonghunTranslator:
    """隐语法双向翻译器 —— 内外命名隔离的桥接层。"""

    def __init__(self, ci_dian_pi: Optional[str] = None):
        """
        Args:
            ci_dian_pi: 自定义词典JSON文件路径，默认使用内置词典
        """
        self.ci_dian = dict(_yu_fa_ci_dian)
        if ci_dian_pi:
            self._jia_zai_ci_dian(ci_dian_pi)
        # 构建反向词典
        self.fan_xiang_ci_dian: Dict[str, str] = {
            v: k for k, v in self.ci_dian.items()
        }

    def _jia_zai_ci_dian(self, lu_jing: str) -> None:
        """从JSON文件加载额外词典条目。"""
        p = Path(lu_jing)
        if p.exists():
            with open(p, 'r', encoding='utf-8') as f:
                bu_chong = json.load(f)
            self.ci_dian.update(bu_chong)

    def dao_dui_wai(self, dui_nei_ming: str) -> str:
        """对内命名 → 对外命名（隐语法 → 英文）。"""
        return self.ci_dian.get(dui_nei_ming, dui_nei_ming)

    def dao_dui_nei(self, dui_wai_ming: str) -> str:
        """对外命名 → 对内命名（英文 → 隐语法）。"""
        return self.fan_xiang_ci_dian.get(dui_wai_ming, dui_wai_ming)

    def yi_han_shu_ming(self, dui_nei_ming: str) -> str:
        """把内部函数/变量名里的隐语词按最长匹配翻译为英文（用于对外文档生成）。"""
        jie_guo = dui_nei_ming
        # 按词长度降序排列，优先匹配长词
        pai_xu_ci = sorted(self.ci_dian.keys(), key=len, reverse=True)
        for ci in pai_xu_ci:
            ying_wen = self.ci_dian[ci]
            jie_guo = jie_guo.replace(ci, ying_wen)
        return jie_guo

    def yi_wai_wen_wei_nei(self, dui_wai_ming: str) -> str:
        """把外部英文函数/变量名里的英文术语按最长匹配翻译为隐语法（用于对内代码生成）。

        边界策略：把下划线视为分隔符而非单词字符，使用自定义 lookaround
        `(?<![a-zA-Z0-9])...(?![a-zA-Z0-9])`。这样既能匹配 snake_case 中的独立
        术语（如 submit_compute_task 中的 compute_task），又不会误匹配普通英文
        单词的子串（如 serverless 中的 server）。
        """
        import re
        jie_guo = dui_wai_ming
        # 按英文词长度降序，优先匹配长词
        pai_xu_ci = sorted(self.fan_xiang_ci_dian.keys(), key=len, reverse=True)
        for ying_wen in pai_xu_ci:
            yin_yu = self.fan_xiang_ci_dian[ying_wen]
            # 自定义边界：下划线视为分隔符
            jie_guo = re.sub(
                r'(?<![a-zA-Z0-9])' + re.escape(ying_wen) + r'(?![a-zA-Z0-9])',
                yin_yu, jie_guo
            )
        return jie_guo

    def huo_qu_ci_dian(self) -> Dict[str, str]:
        """返回完整词典（只读）。"""
        return dict(self.ci_dian)

    def cha_ci(self, ci: str) -> Optional[str]:
        """查词：输入任一语言，返回对应翻译。"""
        if ci in self.ci_dian:
            return self.ci_dian[ci]
        if ci in self.fan_xiang_ci_dian:
            return self.fan_xiang_ci_dian[ci]
        return None

    def shi_fou_shi_dui_nei(self, ci: str) -> bool:
        """判断一个词是否属于隐语法内部词。"""
        return ci in self.ci_dian

    def shi_fou_shi_dui_wai(self, ci: str) -> bool:
        """判断一个词是否属于对外英文词。"""
        return ci in self.fan_xiang_ci_dian


# ═══ CLI ═══
def _ming_ling_cha_ci(ci: str) -> None:
    """查词命令。"""
    fanyi = LonghunTranslator()
    jie_guo = fanyi.cha_ci(ci)
    if jie_guo:
        if fanyi.shi_fou_shi_dui_nei(ci):
            print(f"  {ci} → {jie_guo}  [隐语法 → 英文]")
        else:
            print(f"  {ci} → {jie_guo}  [英文 → 隐语法]")
    else:
        print(f"  '{ci}' 不在词典中")


def _ming_ling_lie_biao() -> None:
    """列出全部词典。"""
    fanyi = LonghunTranslator()
    ci_dian = fanyi.huo_qu_ci_dian()
    fen_lei = {
        "安全与加密": ["jia_mi", "jie_mi", "yao_pai_sheng", "she_bei_wen", "sheng_wu_jian", "cheng_qiang", "shen_ji_zhang", "ling_xin", "hou_men"],
        "数据与存储": ["min_ji", "ben_di_cang", "yun_tong", "shu_zhu", "bao_gui", "bei_fen"],
        "计算与网络": ["ying_zhai", "suan_chou", "wu_tai_men", "guan_kou", "guan_dao", "jun_heng"],
        "治理与协议": ["xian_fa", "gui_yue", "zhi_li", "he_gui", "wei_gui"],
        "人格与系统": ["ren_ge", "tong_shuai", "shi_guan", "shou_hu", "jin_hua"],
        "通用操作": ["tuo_min", "suan_li", "zheng_ming", "qian_ming", "yan_zheng", "chu_li", "jie_guo", "fa_song", "jie_shou"],
    }
    for fen_lei_ming, ci_lie in fen_lei.items():
        print(f"\n  [{fen_lei_ming}]")
        for ci in ci_lie:
            if ci in ci_dian:
                print(f"    {ci} = {ci_dian[ci]}")


def _ming_ling_fan_yi(wen_ben: str, fang_xiang: str = "dui_wai") -> None:
    """翻译文本中所有可识别术语。"""
    fanyi = LonghunTranslator()
    if fang_xiang == "dui_wai":
        jie_guo = fanyi.yi_han_shu_ming(wen_ben)
    else:
        jie_guo = fanyi.yi_wai_wen_wei_nei(wen_ben)
    print(f"  输入: {wen_ben}")
    print(f"  输出: {jie_guo}")


def cmd_selftest(args=None):
    """自检：词典完整性 + 双向翻译一致性。"""
    print("=" * 60)
    print("龍魂·隐语法翻译层 v1.0 — 自检")
    print("=" * 60)

    passed = 0
    failed = 0
    fanyi = LonghunTranslator()

    # 检查1: 词典非空
    try:
        assert len(fanyi.ci_dian) > 0, "词典为空"
        assert len(fanyi.fan_xiang_ci_dian) > 0, "反向词典为空"
        passed += 1
        print(f"  ✅ 词典完整性: {len(fanyi.ci_dian)}条目 / 反向{len(fanyi.fan_xiang_ci_dian)}条目")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 词典完整性失败: {e}")

    # 检查2: 双向无丢失
    try:
        for ci, ying in fanyi.ci_dian.items():
            assert fanyi.dao_dui_nei(ying) == ci, f"反向查找失败: {ying} → {fanyi.dao_dui_nei(ying)} != {ci}"
        passed += 1
        print(f"  ✅ 双向翻译一致性: {len(fanyi.ci_dian)}对全部通过")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 双向翻译一致性失败: {e}")

    # 检查3: 自定义词典加载
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tf:
            json.dump({"ce_shi_ci": "test_word"}, tf)
            lu_jing = tf.name
        f2 = LonghunTranslator(ci_dian_pi=lu_jing)
        assert f2.dao_dui_wai("ce_shi_ci") == "test_word"
        os.unlink(lu_jing)
        passed += 1
        print(f"  ✅ 自定义词典加载: 正常")
    except Exception as e:
        failed += 1
        print(f"  🔴 自定义词典加载失败: {e}")

    # 检查4: 查词功能
    try:
        assert fanyi.cha_ci("jia_mi") == "encrypt"
        assert fanyi.cha_ci("encrypt") == "jia_mi"
        assert fanyi.cha_ci("nonexistent") is None
        assert fanyi.shi_fou_shi_dui_nei("bao_gui") is True
        assert fanyi.shi_fou_shi_dui_nei("vault") is False
        assert fanyi.shi_fou_shi_dui_wai("vault") is True
        passed += 1
        print(f"  ✅ 查词与判断: 全部正确")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 查词功能失败: {e}")

    # 检查5: 函数名翻译（对内→对外）
    try:
        jie_guo = fanyi.yi_han_shu_ming("ti_jiao_suan_chou_tuo_min_min_ji")
        assert "compute_task" in jie_guo or "suan_chou" not in jie_guo, f"翻译后仍含隐语: {jie_guo}"
        passed += 1
        print(f"  ✅ 函数名翻译(内→外): 'ti_jiao_suan_chou_tuo_min_min_ji' → '{jie_guo}'")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 函数名翻译失败: {e}")

    # 检查5b: 函数名翻译（对外→对内）
    try:
        jie_guo = fanyi.yi_wai_wen_wei_nei("submit_compute_task(desensitize_user_data)")
        assert "suan_chou" in jie_guo, f"未翻译 compute_task: {jie_guo}"
        assert "tuo_min" in jie_guo, f"未翻译 desensitize: {jie_guo}"
        assert "min_ji" in jie_guo, f"未翻译 user_data: {jie_guo}"
        passed += 1
        print(f"  ✅ 函数名翻译(外→内): 'submit_compute_task(...)' → '{jie_guo}'")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 反向函数名翻译失败: {e}")

    # 检查5c: 子串误译防御
    try:
        jie_guo = fanyi.yi_wai_wen_wei_nei("serverless_mode")
        assert "ying_zhai" not in jie_guo, f"server 不应在 serverless 中被误译: {jie_guo}"
        passed += 1
        print(f"  ✅ 子串误译防御: 'serverless_mode' 保持原样")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 子串误译防御失败: {e}")

    # 检查6: P0核心词覆盖
    try:
        he_xin_ci = ["jia_mi", "min_ji", "bao_gui", "xian_fa", "shen_ji_zhang"]
        for ci in he_xin_ci:
            assert ci in fanyi.ci_dian, f"P0核心词缺失: {ci}"
            assert fanyi.dao_dui_wai(ci) != ci, f"核心词'{ci}'无翻译"
        passed += 1
        print(f"  ✅ P0核心词覆盖: {len(he_xin_ci)}词全部到位")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 P0核心词缺失: {e}")

    print(f"\n  {'🟢 全绿' if failed == 0 else '🔴 有失败'}: {passed}/{passed + failed} 通过")
    return 0 if failed == 0 else 1



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="龍魂·隐语法翻译层")
    parser.add_argument("command", nargs="?", default="selftest",
                        choices=["selftest", "lookup", "list", "translate"],
                        help="命令")
    parser.add_argument("word", nargs="?", help="要查询/翻译的词")
    parser.add_argument("--direction", choices=["internal", "external"],
                        default="external", help="翻译方向")

    args = parser.parse_args()

    if args.command == "selftest":
        sys.exit(cmd_selftest(args))
    elif args.command == "lookup" and args.word:
        _ming_ling_cha_ci(args.word)
    elif args.command == "list":
        _ming_ling_lie_biao()
    elif args.command == "translate" and args.word:
        fang_xiang = "dui_wai" if args.direction == "external" else "dui_nei"
        _ming_ling_fan_yi(args.word, fang_xiang)
    else:
        parser.print_help()
