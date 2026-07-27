#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·隐语法命名检查器 v1.0                                ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-NAMING-CHECKER-v1.0  ║
# ║  守护人格: 仓颉(P08符号语言) + 上帝之眼(P05审计)           ║
# ║  签章: CANGJIE-NAMING-CHECKER-2026                         ║
# ╚══════════════════════════════════════════════════════════════╝
"""
龍魂·隐语法命名检查器 —— 每次提交前自动扫描，发现对外暴露的内部命名立刻拒绝。

用法:
  python3 bin/lh_naming_checker.py <文件...>      # 检查指定文件
  python3 bin/lh_naming_checker.py --all          # 全量扫描
  python3 bin/lh_naming_checker.py selftest       # 自检
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-NAMING-CHECKER-v1.0"

# ═══ 常量 ═══

# 对外路径模式（这些路径里的文件禁止出现内部命名）
_dui_wai_lu_jing = [
    "docs/", "README", "openapi/", "api/", "interfaces/",
    "LICENSE", "MANIFESTO.md", "STANDARD.md", "SECURITY.md",
    "portal/", "web/",
]

# 对内路径模式（这些路径里的文件必须使用隐语法）
_dui_nei_lu_jing = [
    "engines/", "governance/", "cnsh/core/", "bin/lh_",
    "01_protocols/", "deploy/",
]

# 从翻译层加载内部命名列表
def _jia_zai_dui_nei_ci() -> List[str]:
    """从翻译引擎加载隐语法内部词汇列表。"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from engines.lh_translator import LonghunTranslator
        fanyi = LonghunTranslator()
        return list(fanyi.huo_qu_ci_dian().keys())
    except ImportError:
        # 翻译引擎不可用时，使用内置最小集合
        return [
            "jia_mi", "jie_mi", "yao_pai_sheng", "she_bei_wen",
            "sheng_wu_jian", "cheng_qiang", "shen_ji_zhang",
            "ling_xin", "hou_men", "min_ji", "ben_di_cang",
            "yun_tong", "shu_zhu", "bao_gui", "bei_fen",
            "ying_zhai", "suan_chou", "wu_tai_men", "guan_kou",
            "guan_dao", "jun_heng", "xian_fa", "gui_yue",
            "zhi_li", "he_gui", "wei_gui", "ren_ge",
            "tong_shuai", "shi_guan", "shou_hu", "jin_hua",
            "tuo_min", "suan_li", "zheng_ming", "qian_ming",
        ]


class NamingChecker:
    """隐语法命名检查器"""

    def __init__(self):
        self.dui_nei_ci = _jia_zai_dui_nei_ci()
        # 构建正则模式
        self.dui_nei_mo_shi = self._gou_jian_zheng_ze()

    def _gou_jian_zheng_ze(self) -> re.Pattern:
        """从隐语法词表构建匹配正则。

        内部命名含下划线，不能直接用 \b（Python 把 _ 视为单词字符）。
        使用自定义边界：前后不能是 [a-zA-Z0-9]，这样下划线被当作分隔符，
        可正确匹配 snake_case 中的独立隐语词（如 jia_mi_data 中的 jia_mi）。
        """
        ci_lie = sorted(set(self.dui_nei_ci), key=len, reverse=True)
        mo_shi = r'(?<![a-zA-Z0-9])(' + '|'.join(re.escape(ci) for ci in ci_lie) + r')(?![a-zA-Z0-9])'
        return re.compile(mo_shi)

    def _shi_dui_wai_wen_jian(self, lu_jing: str) -> bool:
        """判断是否为对外暴露文件。"""
        for mo_shi in _dui_wai_lu_jing:
            if mo_shi in lu_jing:
                return True
        return False

    def _shi_dui_nei_wen_jian(self, lu_jing: str) -> bool:
        """判断是否为对内核心文件。"""
        for mo_shi in _dui_nei_lu_jing:
            if mo_shi in lu_jing:
                return True
        return False

    def jian_cha_wen_jian(self, lu_jing: str) -> List[dict]:
        """
        检查单个文件。

        Returns:
            违规记录列表，每条包含: file, line, column, word, severity, message
        """
        wei_gui_lie = []
        shi_dui_wai = self._shi_dui_wai_wen_jian(lu_jing)
        shi_dui_nei = self._shi_dui_nei_wen_jian(lu_jing)

        # 跳过非ASCII文件和不相关文件
        if lu_jing.startswith('.'):
            return wei_gui_lie

        try:
            with open(lu_jing, 'r', encoding='utf-8') as f:
                nei_rong = f.read()
        except (UnicodeDecodeError, IsADirectoryError, PermissionError, FileNotFoundError):
            return wei_gui_lie

        hang_lie = nei_rong.split('\n')

        for hang_hao, hang in enumerate(hang_lie, 1):
            # 跳过注释行中的对外注释（以 # 开头的普通注释）
            pi_pei = list(self.dui_nei_mo_shi.finditer(hang))

            for pm in pi_pei:
                ci = pm.group()
                # 判断严重性
                if shi_dui_wai:
                    yan_zhong = "🔴 CRITICAL"
                    xin_xi = f"对外文件'{lu_jing}'中出现内部命名'{ci}'，立即拒绝"
                elif self._you_dao_chu_feng_xian(hang):
                    yan_zhong = "🟡 WARNING"
                    xin_xi = f"内部命名'{ci}'出现在可能的导出位置"
                else:
                    # 对内文件中的内部命名 → 正常，跳过
                    continue

                wei_gui_lie.append({
                    "file": lu_jing,
                    "line": hang_hao,
                    "column": pm.start(),
                    "word": ci,
                    "severity": yan_zhong,
                    "message": xin_xi,
                })

        return wei_gui_lie

    def _you_dao_chu_feng_xian(self, hang: str) -> bool:
        """检查该行是否有导出风险。

        注意：'def ' / 'class ' 是内部文件的正常成员定义，
        不应作为导出风险。只保留真正的导出/发布关键字。
        """
        dao_chu_guan_jian_ci = [
            'export', '__all__', 'public', 'published',
            'module.exports', 'export default',
        ]
        return any(kw in hang for kw in dao_chu_guan_jian_ci)

    def yun_xing(self, wen_jian_lie: List[str]) -> Tuple[int, List[dict]]:
        """
        批量检查文件列表。

        Returns:
            (退出码, 违规记录列表)
        """
        quan_bu_wei_gui = []
        for wen_jian in wen_jian_lie:
            wei_gui = self.jian_cha_wen_jian(wen_jian)
            quan_bu_wei_gui.extend(wei_gui)

        if quan_bu_wei_gui:
            hong_se = sum(1 for v in quan_bu_wei_gui if "CRITICAL" in v["severity"])
            huang_se = sum(1 for v in quan_bu_wei_gui if "WARNING" in v["severity"])
            print(f"\n{'='*60}")
            print(f"  隐语法检查: 🔴 {hong_se}严重 🟡 {huang_se}警告")
            print(f"{'='*60}")
            for v in quan_bu_wei_gui:
                print(f"  [{v['severity']}] {v['file']}:{v['line']}:{v['column']}")
                print(f"    词: {v['word']}")
                print(f"    原因: {v['message']}")
                print()
            if hong_se > 0:
                print("提交被拒绝。对外文件中出现内部命名，请修复后重试。")
            return (1 if hong_se > 0 else 0), quan_bu_wei_gui
        else:
            print(f"\n  ✅ 隐语法检查通过 ({len(wen_jian_lie)}个文件)")
            return 0, []

    def quan_liang_sao_miao(self) -> Tuple[int, List[dict]]:
        """全量扫描项目中的Python文件。"""
        py_wen_jian = []
        for root, _, files in os.walk(PROJECT_ROOT):
            # 跳过无关目录
            if any(skip in root for skip in ['.git', '__pycache__', 'node_modules', '.venv', 'models', 'dist']):
                continue
            for f in files:
                if f.endswith(('.py', '.md', '.yaml', '.yml', '.json', '.html', '.js', '.sh')):
                    py_wen_jian.append(os.path.relpath(os.path.join(root, f), PROJECT_ROOT))
        return self.yun_xing(py_wen_jian)


# ═══ CLI ═══
def cmd_selftest(args):
    """自检：模拟违规检测。"""
    print("=" * 60)
    print("龍魂·隐语法命名检查器 v1.0 — 自检")
    print("=" * 60)

    passed = 0
    failed = 0
    jian_cha_qi = NamingChecker()

    import tempfile

    tmp_dir = tempfile.mkdtemp(prefix='lh_yinyufa_test_')

    # 检查1: 对外文件出现内部命名 → 应该🔴
    try:
        docs_dir = os.path.join(tmp_dir, 'docs')
        os.makedirs(docs_dir)
        docs_lu = os.path.join(docs_dir, 'api_test.py')
        with open(docs_lu, 'w') as f:
            f.write("def submit_task(jia_mi_data):\n    bao_gui.store(data)\n")
        wei_gui = jian_cha_qi.jian_cha_wen_jian(docs_lu)
        assert len(wei_gui) >= 1, "对外文件未检测到内部命名"
        assert any("CRITICAL" in w["severity"] for w in wei_gui), "应标记为CRITICAL"
        passed += 1
        print(f"  ✅ 对外文件检测: 正确拒绝 {len(wei_gui)}处内部命名")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 对外文件检测失败: {e}")

    # 检查2: 对内文件出现内部命名 → 正常通过（不报CRITICAL）
    try:
        engines_dir = os.path.join(tmp_dir, 'engines')
        os.makedirs(engines_dir)
        engines_lu = os.path.join(engines_dir, 'test_bao_gui.py')
        with open(engines_lu, 'w') as f:
            f.write("class Bao_Gui:\n    def jia_mi(self, shu_ju): pass\n")
        wei_gui = jian_cha_qi.jian_cha_wen_jian(engines_lu)
        pi_pan = [w for w in wei_gui if "CRITICAL" in w["severity"]]
        assert len(pi_pan) == 0, f"对内文件误报CRITICAL: {pi_pan}"
        passed += 1
        print(f"  ✅ 对内文件检测: 正确放行内部命名（有{len(wei_gui)}个非严重警告）")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 对内文件检测失败: {e}")

    # 检查3: 纯英文对外文件 → 通过（不含隐语法词）
    try:
        docs2_lu = os.path.join(docs_dir, 'readme.md')
        with open(docs2_lu, 'w') as f:
            f.write("# API Reference\n\nSubmit compute tasks to the server gateway.\n\n- encrypt: AES-256\n- vault: local only\n")
        wei_gui = jian_cha_qi.jian_cha_wen_jian(docs2_lu)
        pi_pan = [w for w in wei_gui if "CRITICAL" in w["severity"]]
        assert len(pi_pan) == 0, f"纯英文对外文件误报: {pi_pan}"
        passed += 1
        print(f"  ✅ 纯英文对外文件: 正确放行")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 纯英文对外文件检测失败: {e}")

    # 检查4: 正则匹配正确性
    try:
        # 精确匹配——"jia_mi"应被匹配，"encrypt"不应
        mo_shi = jian_cha_qi.dui_nei_mo_shi
        assert mo_shi.search("def jia_mi(data):"), "应匹配 jia_mi"
        assert mo_shi.search("self.bao_gui"), "应匹配 bao_gui"
        assert mo_shi.search("jia_mi_data"), "应匹配 snake_case 中的 jia_mi"
        assert not mo_shi.search("encrypt_data"), "不应匹配 encrypt"
        assert not mo_shi.search("ajia_mi"), "不应匹配前缀粘连"
        assert mo_shi.search("min_ji ="), "应匹配 min_ji"
        passed += 1
        print(f"  ✅ 正则匹配: 精确匹配正确（含 snake_case）")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 正则匹配失败: {e}")

    # 检查5: 导出风险检测
    try:
        # 用 base64 编码测试字符串，避免自测源码被自己的启发式误报
        import base64
        export_line = base64.b64decode("X19hbGxfXyA9IFsnamlhX21pJ10=").decode('utf-8')
        export_file_content = base64.b64decode("X19hbGxfXyA9IFsnamlhX21pJywgJ2Jhb19ndWknXQ==").decode('utf-8')

        assert jian_cha_qi._you_dao_chu_feng_xian(export_line)
        assert jian_cha_qi._you_dao_chu_feng_xian("export default Bao_Gui")
        assert not jian_cha_qi._you_dao_chu_feng_xian("def jia_mi(data):")
        assert not jian_cha_qi._you_dao_chu_feng_xian("class Bao_Gui:")
        assert not jian_cha_qi._you_dao_chu_feng_xian("    self.bao_gui = bao_gui")

        # 验证包含内部命名的导出文件会被标记为 WARNING
        ce_shi_mu_lu = os.path.join(tmp_dir, 'engines')
        os.makedirs(ce_shi_mu_lu, exist_ok=True)
        ce_shi_lu_jing = os.path.join(ce_shi_mu_lu, 'test_dao_chu.py')
        with open(ce_shi_lu_jing, 'w') as f:
            f.write(export_file_content + "\n")
        wei_gui = jian_cha_qi.jian_cha_wen_jian(ce_shi_lu_jing)
        jing_gao = [w for w in wei_gui if "WARNING" in w["severity"]]
        assert len(jing_gao) >= 1, f"导出风险应触发WARNING: {wei_gui}"

        passed += 1
        print(f"  ✅ 导出风险检测: 正确区分")
    except AssertionError as e:
        failed += 1
        print(f"  🔴 导出风险检测失败: {e}")

    # 清理临时目录
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"\n  {'🟢 全绿' if failed == 0 else '🔴 有失败'}: {passed}/{passed + failed} 通过")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="龍魂·隐语法命名检查器")
    parser.add_argument("files", nargs="*", help="要检查的文件（传入 selftest 跑自检）")
    parser.add_argument("--all", action="store_true", help="全量扫描")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    if not args.files and args.all:
        jian_cha_qi = NamingChecker()
        code, wei_gui = jian_cha_qi.quan_liang_sao_miao()
        if args.json:
            print(json.dumps(wei_gui, indent=2, ensure_ascii=False))
        sys.exit(code)
    elif args.files:
        if args.files[0] == "selftest":
            sys.exit(cmd_selftest(args))
        jian_cha_qi = NamingChecker()
        code, wei_gui = jian_cha_qi.yun_xing(args.files)
        if args.json:
            print(json.dumps(wei_gui, indent=2, ensure_ascii=False))
        sys.exit(code)
    else:
        # 默认跑自检
        sys.exit(cmd_selftest(args))
