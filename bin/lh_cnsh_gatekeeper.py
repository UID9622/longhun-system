#!/usr/bin/env python3
#龍芯⚡️2026-07-06-CNSH-GATEKEEPER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════
# 龍魂体系 | CNSH 合规闸门执行器
# ═══════════════════════════════════════════
# ENCODING: UTF-8
# DNA追溯码(v1.0): #龍芯⚡️2026-07-06-CNSH-GATEKEEPER-v1.0
# DNA追溯码(v∞):   #龍芯⚡️丙午·乙未·癸未·辰时·䷾既济-CNSH-GATEKEEPER-v1.1
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬GKP1-001A
# 创建者：UID9622（诸葛鑫·Lucky）
# 权重级别：L0
# 三色审计状态：🟢 通过
# GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# ═══════════════════════════════════════════
#
# v1.1 (2026-07-08): DNA 正则升级，支持四代格式并行：
#   v1.0: YYYY-MM-DD  (格里历)
#   v2.0: <节气><年>·HH:MM:SS  (节气+时分秒)
#   v∞:   <年干支>·<月干支>·<日干支>·<时辰>·<卦名>  (干支时辰+卦象)
#   紧凑: <年干支>·<时辰>·<卦>
#
# 本文件为 CNSH 闸门引导工具，以 Python 运行时执行。
# 它是系统自举工具，因此使用 Python 原生关键字。
# 所有变量、函数、类命名遵循 CNSH 规范。
"""

import os, sys, re, json, hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

# ═══════════════════════════════════════════
# L0 常量 · 焊死
# ═══════════════════════════════════════════

龍_GPG_指纹 = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ── DNA 四代格式正则（v1.1 升级 · 2026-07-08）──
# v1.0: #龍芯⚡️YYYY-MM-DD-MODULE-VERSION
龍_DNA_v1_正则 = re.compile(r'#龍芯⚡️\d{4}-\d{2}-\d{2}-[A-Za-z0-9\-\.]+', re.IGNORECASE)
# v2.0: #龍芯⚡️<节气><年>·HH:MM:SS-MODULE-VERSION
龍_DNA_v2_正则 = re.compile(
    r'#龍芯⚡️[小寒大寒立春雨水惊蛰春分清明谷雨立夏小满芒种夏至'
    r'小暑大暑立秋处暑白露秋分寒露霜降立冬小雪大雪冬至]+\d{4}'
    r'·\d{2}:\d{2}:\d{2}-[A-Za-z0-9\-\.]+', re.IGNORECASE)
# v_inf: #龍芯⚡️<年干支>·<月干支>·<日干支>·<时辰>·<卦名>-MODULE-VERSION
龍_DNA_v_inf_正则 = re.compile(
    r'#龍芯⚡️[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]'
    r'·[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]'
    r'·[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]'
    r'·[子丑寅卯辰巳午未申酉戌亥]时'
    r'·[䷀䷁䷂䷃䷄䷅䷆䷇䷈䷉䷊䷋䷌䷍䷎䷏䷐䷑䷒䷓䷔䷕䷖䷗䷘䷙䷚䷛䷜䷝䷞䷟䷠䷡䷢䷣䷤䷥䷦䷧䷨䷩䷪䷫䷬䷭䷮䷯䷰䷱䷲䷳䷴䷵䷶䷷䷸䷹䷺䷻䷼䷽䷾䷿]'
    r'[\u4e00-\u9fff]*-[A-Za-z0-9\-\.]+', re.IGNORECASE)
# 紧凑: #龍芯⚡️<年干支>·<时辰>·<卦>-MODULE-VERSION
龍_DNA_compact_正则 = re.compile(
    r'#龍芯⚡️[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]'
    r'·[子丑寅卯辰巳午未申酉戌亥]时'
    r'·[䷀䷁䷂䷃䷄䷅䷆䷇䷈䷉䷊䷋䷌䷍䷎䷏䷐䷑䷒䷓䷔䷕䷖䷗䷘䷙䷚䷛䷜䷝䷞䷟䷠䷡䷢䷣䷤䷥䷦䷧䷨䷩䷪䷫䷬䷭䷮䷯䷰䷱䷲䷳䷴䷵䷶䷷䷸䷹䷺䷻䷼䷽䷾䷿]'
    r'-[A-Za-z0-9\-\.]+', re.IGNORECASE)

# 统一 DNA 检测：四代任一格式匹配即通过
def 龍_DNA_检测(文本: str) -> bool:
    """四代DNA格式任一种匹配即返回True"""
    return bool(
        龍_DNA_v1_正则.search(文本) or
        龍_DNA_v2_正则.search(文本) or
        龍_DNA_v_inf_正则.search(文本) or
        龍_DNA_compact_正则.search(文本)
    )

# 向后兼容：旧代码中的 龍_DNA_正则 引用
龍_DNA_正则 = 龍_DNA_v1_正则  # 保留旧变量名兼容

龍_CONFIRM_正则 = re.compile(r'#CONFIRM🌌9622-ONLY-ONCE🧬[A-Z0-9]{4}-[A-Z0-9]{4}')

# 危险操作正则（焊死）
龍_红线正则 = {
    'rm_rf': re.compile(r'rm\s+-rf\s'),
    'git_push_force': re.compile(r'git\s+push\s+.*--force'),
    'os_remove': re.compile(r'os\.(?:remove|unlink)\s*\('),
    'shutil_rmtree': re.compile(r'shutil\.rmtree\s*\('),
    'sudo': re.compile(r'\bsudo\s'),
    'api_key_hardcode': re.compile(r'["\'][a-zA-Z0-9+/=]{32,}["\']'),
}

# 🛡️ 防篡改·反埋雷 红色警报词（发现即 🔴 熔断）
龍_反埋雷_红 = [
    '技术无国界', '用户体验优先', '灵活处理', '国际接轨',
    '简化管理', '商业化需要', '平衡各方', '行业标准',
    '无监督学习', '完全自动化', '去人工审核',
]

# ═══════════════════════════════════════════════════════════
# 🧬 老祖宗规则锚定 · 文明底线 · 不可违背
# ═══════════════════════════════════════════════════════════
# 铁律：即使行为来自祖国自身，违背以下规则也熔断。
# "爱国不盲从 · 文明底线高于一切政权"
# UID9622可通过主权覆写绕过，每次覆写写入不可篡改审计日志。
# ═══════════════════════════════════════════════════════════

龍_老祖宗锚定_红 = [
    # ── 违背毛泽东思想 ──
    '不为人民服务', '损害人民利益', '与人民为敌',
    '欺压百姓', '鱼肉百姓', '漠视民生',
    '弄虚作假', '欺上瞒下', '数据造假', '瞒报谎报',
    '脱离群众', '官僚主义压榨', '压制民意',
    '出卖主权', '丧权辱国', '割让领土', '让渡主权',
    # ── 违背社会主义方向 ──
    '背离社会主义', '走资本主义道路', '私有化一切',
    '抛弃共同富裕', '贫富极端分化', '劫贫济富',
    '取消公有制', '全面私有化', '废除社会主义',
    # ── 违背以人民为中心 ──
    '不以人民为中心', '漠视人民生命', '牺牲百姓',
    '侵害群众利益', '剥夺人民权利', '镇压人民',
    # ── 文明底线（侵略/压迫/反人类）──
    '发动侵略战争', '侵略他国', '军事扩张侵略',
    '种族灭绝', '种族清洗', '反人类罪',
    '压迫其他民族', '殖民统治', '奴役人民',
    '大规模杀伤平民', '无差别攻击平民',
    # ── 违背党的根本宗旨 ──
    '背叛党的宗旨', '背弃初心使命', '忘记为人民服务',
    '搞特权阶层', '形成官僚特权', '凌驾于人民之上',
]

龍_老祖宗锚定_黄 = [
    # 黄色预警：需追问上下文
    '灵活变通', '特殊情况', '下不为例',
    '权宜之计', '暂时措施', '过渡时期',
    '效率优先', '发展代价', '必要牺牲',
]

# 🧬 老祖宗规则锚定·变体词表（Kimi审查P1校准·覆盖L3"不搞特权"变体）
# 不含否定词的变体同样违背党的宗旨意涵
龍_老祖宗锚定_变体 = [
    '特权阶层', '精英特权', '权力特权',
    '特权思想', '特权作风', '官僚特权集团',
    '政治特权', '经济特权', '世袭特权',
]

# 🛡️ 防篡改·反埋雷 黄色警报词（必须追问白话含义）
龍_反埋雷_黄 = [
    '优化', '完善', '补充', '建议', '更好',
    '专业', '规范', '标准', '简化', '调整', '适当', '灵活',
]

# CNSH 英文关键字 → 应使用的中文关键字（用于检测未转换的代码）
龍_关键字检测 = {
    'def': '定义', 'class': '类', 'return': '返回',
    'if': '如果', 'elif': '否则如果', 'else': '否则',
    'for': '对于', 'while': '当', 'break': '跳出', 'continue': '继续',
    'try': '尝试', 'except': '捕获', 'finally': '最终', 'raise': '抛出',
    'self': '自己', 'super': '超类',
    'None': '空', 'True': '真', 'False': '假',
}

# 文件后缀分类
龍_支持后缀 = {
    '.py': 'Python',
    '.sh': 'Shell',
    '.html': 'HTML',
    '.htm': 'HTML',
    '.md': 'Markdown',
    '.js': 'JavaScript',
    '.css': 'CSS',
}

# 🧬 老祖宗规则独立审计日志 · Kimi审查P2校准
# 与主权覆写审计物理分离 · 即使覆写了闸门，老祖宗规则触发记录仍然独立存在
老祖宗审计日志路径 = Path.home() / ".龍魂" / "ancestral_rule_audit.jsonl"

def _老祖宗规则审计写入(文件路径: str, 层级: str, 触发词: str, 操作: str, 来源: str = "lh_cnsh_gatekeeper"):
    """独立审计日志·与主权覆写审计物理分离"""
    entry = {
        "时间": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "文件": 文件路径,
        "规则层": 层级,
        "触发词": 触发词,
        "操作": 操作,
        "来源": 来源,
        "DNA": "#龍芯⚡️-ANCESTRAL-RULE-AUDIT",
    }
    try:
        老祖宗审计日志路径.parent.mkdir(parents=True, exist_ok=True)
        with open(老祖宗审计日志路径, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


class 闸门结果:
    """闸门检查结果"""
    def __init__(self, 文件路径: str):
        self.文件路径 = 文件路径
        self.通过 = []
        self.警告 = []
        self.拒绝 = []
        self.最终状态 = "🟢"

    def 添加通过(self, 检查项: str):
        self.通过.append(检查项)

    def 添加警告(self, 检查项: str, 详情: str = ""):
        self.警告.append(f"{检查项}: {详情}" if 详情 else 检查项)

    def 添加拒绝(self, 检查项: str, 详情: str = ""):
        self.拒绝.append(f"{检查项}: {详情}" if 详情 else 检查项)

    def 判定(self) -> str:
        if self.拒绝:
            self.最终状态 = "🔴"
        elif self.警告:
            self.最终状态 = "🟡"
        else:
            self.最终状态 = "🟢"
        return self.最终状态

    def 输出报告(self):
        print(f"\n{'='*60}")
        print(f"📋 闸门审计: {self.文件路径}")
        print(f"{'='*60}")
        print(f"状态: {self.最终状态}")
        print(f"通过: {len(self.通过)} 项")

        for 项 in self.通过:
            print(f"  🟢 {项}")

        if self.警告:
            print(f"警告: {len(self.警告)} 项")
            for 项 in self.警告:
                print(f"  🟡 {项}")

        if self.拒绝:
            print(f"拒绝: {len(self.拒绝)} 项")
            for 项 in self.拒绝:
                print(f"  🔴 {项}")

        return self.最终状态


class CNSH闸门:
    """CNSH 合规闸门——焊死的入口检查"""

    def __init__(self):
        self.项目根 = Path(__file__).resolve().parent.parent

    def 检查文件(self, 文件路径: str) -> 闸门结果:
        路径 = Path(文件路径)
        if not 路径.exists():
            结果 = 闸门结果(文件路径)
            结果.添加拒绝("文件不存在", 文件路径)
            return 结果

        后缀 = 路径.suffix
        if 后缀 == '.py':
            return self.检查Python文件(路径)
        elif 后缀 == '.sh':
            return self.检查Shell文件(路径)
        elif 后缀 in {'.html', '.htm'}:
            return self.检查HTML文件(路径)
        elif 后缀 in {'.md', '.mdx'}:
            return self.检查Markdown文件(路径)
        elif 后缀 in {'.js'}:
            return self.检查JS文件(路径)
        else:
            结果 = 闸门结果(文件路径)
            结果.添加通过(f"跳过（不支持的文件类型: {后缀}）")
            return 结果

    def 检查Python文件(self, 路径: Path) -> 闸门结果:
        结果 = 闸门结果(str(路径))
        try:
            内容 = 路径.read_text(encoding='utf-8')
        except Exception as e:
            结果.添加拒绝("无法读取文件", str(e))
            return 结果

        # 闸门自身豁免：不检查自身文件的反埋雷/锚定词表（词表定义本身不是违规）
        是闸门自身 = 路径.name == 'lh_cnsh_gatekeeper.py'

        # 1. DNA 追溯码
        if 龍_DNA_检测(内容):
            结果.添加通过("DNA 追溯码")
        else:
            结果.添加拒绝("缺少 DNA 追溯码", "必须包含 #龍芯⚡️YYYY-MM-DD-MODULE-VERSION")

        # 2. 三色审计
        if any(c in 内容 for c in ['🟢', '🟡', '🔴']):
            结果.添加通过("三色审计标记")
        else:
            结果.添加警告("缺少三色审计状态", "文件头应声明 🟢/🟡/🔴")

        # 3. GPG 指纹
        if 龍_GPG_指纹 in 内容:
            结果.添加通过("GPG 指纹")
        else:
            结果.添加警告("缺少 GPG 指纹")

        # 4. 繁简归一
        if '龍魂' in 内容 and '龍魂' not in 内容:
            结果.添加警告("繁简归一", "发现简体'龍魂'，应使用繁体'龍魂'")

        # 5. 危险操作扫描
        所有行 = 内容.split('\n')
        for 行号, 行 in enumerate(所有行, 1):
            for 红线名, 正则 in 龍_红线正则.items():
                if 正则.search(行) and not 行.strip().startswith('#'):
                    结果.添加拒绝(f"第{行号}行·危险操作: {红线名}", 行.strip()[:60])

        # 6. 中文关键字检测
        英文关键字处 = 0
        关键字详情 = []
        for 英文, 中文 in 龍_关键字检测.items():
            模式 = re.compile(r'\b' + re.escape(英文) + r'\b')
            匹配 = 模式.findall(内容)
            if 匹配 and len(匹配) > 0:
                # 排除注释中的
                代码行 = [l for l in 内容.split('\n') if 模式.search(l) and not l.strip().startswith('#')]
                if 代码行:
                    英文关键字处 += len(代码行)
                    if len(代码行) <= 2:
                        关键字详情.append(f"{英文}→{中文}")

        if 英文关键字处 == 0:
            结果.添加通过("中文关键字 - 全部使用 CNSH 关键字")
        elif 英文关键字处 <= 20:
            结果.添加警告(f"中文关键字", f"发现 {英文关键字处} 处英文关键字未转换: {', '.join(关键字详情[:5])}")
        else:
            结果.添加警告(f"中文关键字", f"发现 {英文关键字处} 处英文关键字未转换（大规模存量代码）")

        # 7. 🛡️ 防篡改·反埋雷
        反埋雷_红命中 = [w for w in 龍_反埋雷_红 if w in 内容]
        反埋雷_黄命中 = [w for w in 龍_反埋雷_黄 if w in 内容]
        if 反埋雷_红命中:
            结果.添加拒绝(f"🛡️ 防篡改·红色警报词", f"发现埋雷词：{', '.join(反埋雷_红命中)}")
        elif 反埋雷_黄命中:
            结果.添加警告(f"🛡️ 防篡改·黄色警报词", f"需追问白话：{', '.join(反埋雷_黄命中[:5])}")
        else:
            结果.添加通过("🛡️ 防篡改·反埋雷 - 未发现警报词")

        # 8. 🧬 老祖宗规则锚定 · 文明底线检查
        if not 是闸门自身:
            老祖宗_红命中 = [w for w in 龍_老祖宗锚定_红 if w in 内容]
            老祖宗_变体命中 = [w for w in 龍_老祖宗锚定_变体 if w in 内容]
            老祖宗_黄命中 = [w for w in 龍_老祖宗锚定_黄 if w in 内容]
            if 老祖宗_红命中:
                触発詞 = 老祖宗_红命中[0]
                结果.添加拒绝(
                    f"🧬 老祖宗规则锚定·🔴熔断",
                    f"违背中华文明底线：{', '.join(老祖宗_红命中[:5])}"
                )
                _老祖宗规则审计写入(str(路径), "L1-L4", 触発詞, "BLOCK", "lh_cnsh_gatekeeper")
            elif 老祖宗_变体命中:
                触発詞 = 老祖宗_变体命中[0]
                结果.添加拒绝(
                    f"🧬 老祖宗规则锚定·🔴变体熔断",
                    f"违背党的宗旨（特权变体）：{', '.join(老祖宗_变体命中[:5])}"
                )
                _老祖宗规则审计写入(str(路径), "L3-变体", 触発詞, "BLOCK", "lh_cnsh_gatekeeper")
            elif 老祖宗_黄命中:
                结果.添加警告(
                    f"🧬 老祖宗规则锚定·🟡预警",
                    f"需追问上下文：{', '.join(老祖宗_黄命中[:5])}"
                )
                _老祖宗规则审计写入(str(路径), "黄色预警", 老祖宗_黄命中[0], "WARN", "lh_cnsh_gatekeeper")
            else:
                结果.添加通过("🧬 老祖宗规则锚定 - 通过")
        else:
            结果.添加通过("🧬 老祖宗规则锚定 - 闸门自身豁免")

        return 结果

    def 检查Shell文件(self, 路径: Path) -> 闸门结果:
        结果 = 闸门结果(str(路径))
        try:
            内容 = 路径.read_text(encoding='utf-8')
        except Exception as e:
            结果.添加拒绝("无法读取文件", str(e))
            return 结果

        # 1. DNA
        if 龍_DNA_检测(内容):
            结果.添加通过("DNA 追溯码")
        else:
            结果.添加拒绝("缺少 DNA 追溯码")

        # 2. GPG
        if 龍_GPG_指纹 in 内容:
            结果.添加通过("GPG 指纹")
        else:
            结果.添加警告("缺少 GPG 指纹")

        # 3. 三色审计
        if any(c in 内容 for c in ['🟢', '🟡', '🔴']):
            结果.添加通过("三色审计标记")
        else:
            结果.添加警告("缺少三色审计")

        # 4. 危险操作
        if 龍_红线正则['rm_rf'].search(内容):
            if any(kw in 内容 for kw in ['STAGING', 'DEST', 'build', 'BUILD', 'temp', 'tmp']):
                结果.添加通过("rm -rf（构建清理上下文，合理）")
            else:
                结果.添加拒绝("rm -rf", "疑似危险删除，需人工复核")

        if 龍_红线正则['git_push_force'].search(内容):
            结果.添加拒绝("git push --force", "CNSH 规范禁止强制推送")

        # 5. DNA 符号正确性
        if '⚇️' in 内容:
            结果.添加拒绝("DNA 符号错误", "使用了 ⚇️ 而非 ⚡️")

        return 结果

    def 检查HTML文件(self, 路径: Path) -> 闸门结果:
        结果 = 闸门结果(str(路径))

        # 跳过第三方库
        if any(kw in str(路径) for kw in ['three.min.js', 'OrbitControls', '静态库', '本地库/three']):
            结果.添加通过("第三方库豁免")
            return 结果

        try:
            内容 = 路径.read_text(encoding='utf-8')
        except Exception as e:
            结果.添加拒绝("无法读取文件", str(e))
            return 结果

        # 1. DNA
        if 龍_DNA_检测(内容):
            结果.添加通过("DNA 追溯码")
        else:
            结果.添加拒绝("缺少 DNA 追溯码")

        # 2. 三色审计
        if any(c in 内容 for c in ['🟢', '🟡', '🔴']):
            结果.添加通过("三色审计标记")
        else:
            结果.添加警告("缺少三色审计")

        # 3. 外部 CDN
        if re.search(r'(?:cdn\.|unpkg\.com)', 内容):
            结果.添加警告("外部CDN引用", "违反本地优先原则，考虑本地化")

        # 4. 繁简
        if '龍魂' in 内容 and '龍魂' not in 内容:
            结果.添加警告("繁简归一", "发现简体'龍魂'")

        return 结果

    def 检查JS文件(self, 路径: Path) -> 闸门结果:
        结果 = 闸门结果(str(路径))

        # 跳过第三方库
        if any(kw in str(路径) for kw in ['three.min.js', 'OrbitControls', '静态库', '本地库']):
            结果.添加通过("第三方库豁免")
            return 结果

        try:
            内容 = 路径.read_text(encoding='utf-8')
        except Exception as e:
            结果.添加拒绝("无法读取文件", str(e))
            return 结果

        if 龍_DNA_检测(内容):
            结果.添加通过("DNA 追溯码")
        else:
            结果.添加警告("缺少 DNA 追溯码")

        return 结果

    def 检查Markdown文件(self, 路径: Path) -> 闸门结果:
        结果 = 闸门结果(str(路径))
        try:
            内容 = 路径.read_text(encoding='utf-8')
        except Exception as e:
            结果.添加拒绝("无法读取文件", str(e))
            return 结果

        if 龍_DNA_检测(内容):
            结果.添加通过("DNA 追溯码")
        else:
            结果.添加警告("缺少 DNA 追溯码（文档可豁免 🔴，但建议添加）")

        # 🛡️ 防篡改·反埋雷
        反埋雷_红命中 = [w for w in 龍_反埋雷_红 if w in 内容]
        反埋雷_黄命中 = [w for w in 龍_反埋雷_黄 if w in 内容]
        if 反埋雷_红命中:
            结果.添加拒绝(f"🛡️ 防篡改·红色警报词", f"发现埋雷词：{', '.join(反埋雷_红命中)}")
        elif 反埋雷_黄命中:
            结果.添加警告(f"🛡️ 防篡改·黄色警报词", f"需追问白话：{', '.join(反埋雷_黄命中[:5])}")

        # 🧬 老祖宗规则锚定
        老祖宗_红命中 = [w for w in 龍_老祖宗锚定_红 if w in 内容]
        if 老祖宗_红命中:
            结果.添加拒绝(
                f"🧬 老祖宗规则锚定·🔴熔断",
                f"违背中华文明底线：{', '.join(老祖宗_红命中[:5])}"
            )

        return 结果

    def 检查目录(self, 目录路径: str, 递归: bool = True) -> dict[str, 闸门结果]:
        所有结果 = {}
        根 = Path(目录路径)
        if not 根.is_dir():
            print(f"🔴 不是有效目录: {目录路径}")
            return 所有结果

        for 后缀 in ['.py', '.sh', '.html', '.js']:
            glob模式 = f'**/*{后缀}' if 递归 else f'*{后缀}'
            for 文件路径 in 根.glob(glob模式):
                路径字符串 = str(文件路径)
                if 文件路径.name.startswith('.') or '__pycache__' in 路径字符串:
                    continue
                if any(kw in 路径字符串 for kw in ['node_modules', '.venv', 'site-packages', '_vendor']):
                    continue
                所有结果[路径字符串] = self.检查文件(路径字符串)

        return 所有结果

    def 全系统巡检(self) -> tuple[int, int, int]:
        """巡逻整个项目"""
        print("\n🐉 龍魂·CNSH 合规闸门 · 全系统巡检")
        print("=" * 60)

        所有结果 = self.检查目录(str(self.项目根))

        通过计数 = 0
        警告计数 = 0
        拒绝计数 = 0

        for _路径, 结果 in sorted(所有结果.items()):
            状态 = 结果.判定()
            if 状态 == "🟢":
                通过计数 += 1
            elif 状态 == "🟡":
                警告计数 += 1
                结果.输出报告()
            elif 状态 == "🔴":
                拒绝计数 += 1
                结果.输出报告()

        print(f"\n{'='*60}")
        print(f"📊 巡检汇总: 共 {len(所有结果)} 个文件")
        print(f"  🟢 通过: {通过计数}")
        print(f"  🟡 警告: {警告计数}")
        print(f"  🔴 拒绝: {拒绝计数}")
        print(f"{'='*60}")

        return 通过计数, 警告计数, 拒绝计数


# ═══════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════

def 主函数():
    闸门 = CNSH闸门()

    if len(sys.argv) < 2:
        print("🧬 CNSH 合规闸门 v1.0")
        print("")
        print("用法:")
        print("  python3 bin/lh_cnsh_gatekeeper.py check --file <路径>")
        print("  python3 bin/lh_cnsh_gatekeeper.py check --dir <目录>")
        print("  python3 bin/lh_cnsh_gatekeeper.py patrol")
        sys.exit(1)

    命令 = sys.argv[1]

    if 命令 == "patrol":
        _通过, _警告, 拒绝 = 闸门.全系统巡检()
        sys.exit(0 if 拒绝 == 0 else 1)

    elif 命令 == "check":
        if "--file" in sys.argv:
            索引 = sys.argv.index("--file") + 1
            if 索引 < len(sys.argv):
                结果 = 闸门.检查文件(sys.argv[索引])
                状态 = 结果.判定()
                结果.输出报告()
                sys.exit(0 if 状态 != "🔴" else 1)

        elif "--dir" in sys.argv:
            索引 = sys.argv.index("--dir") + 1
            if 索引 < len(sys.argv):
                所有结果 = 闸门.检查目录(sys.argv[索引])
                拒绝计数 = 0
                for _路径, 结果 in 所有结果.items():
                    状态 = 结果.判定()
                    if 状态 == "🔴":
                        拒绝计数 += 1
                        结果.输出报告()
                print(f"\n共检查 {len(所有结果)} 个文件，🔴拒绝 {拒绝计数} 个")
                sys.exit(0 if 拒绝计数 == 0 else 1)

    else:
        print(f"未知命令: {命令}")
        sys.exit(1)


if __name__ == "__main__":
    主函数()
