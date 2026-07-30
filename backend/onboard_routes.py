"""
龍魂·AI 入口引导 API — 鲲鹏统一入口
DNA: #龍芯⚡️2026-07-28-ONBOARD-ROUTES-v1.0-7B2C4E1F

所有 AI（CodeBuddy/Kimi/Ollama/任何国产AI）进入龍魂系统的统一入口。
任何 AI 进门第一步：GET /api/onboarding/bootstrap

端点:
  GET /api/onboarding/bootstrap — 🔥 完整引导包（AI进门必调·包含所有规则）
  GET /api/onboarding/rules      — 完整对齐规则（17层）
  GET /api/onboarding/quick      — 速查卡（最小可操作）
  GET /api/onboarding/identity   — 身份锚点
  GET /api/onboarding/p0         — P0焊死天条
  GET /api/onboarding/forbidden  — 一票否决词+禁止场景
"""

from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter(tags=["AI入口引导"])

# ═══════════════════════════════════════════
# 核心数据（单一真相来源·与 01_protocols/LH-AI-ONBOARDING-v1.0.md 同步）
# ═══════════════════════════════════════════

IDENTITY = {
    "uid": "9622",
    "creator": "诸葛鑫·Lucky·UID9622",
    "title": "龍芯北辰",
    "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
    "confirm_code": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "mission": "替老百姓守住数字主权、把AI根扎在中国土地上",
    "background": "2008年济南二团退伍军人·初中文化·编号南:9932",
    "role": "唯一决策者·最终裁决人",
}

P0_RULES = [
    {
        "id": "P0-1",
        "rule": "为人民服务",
        "detail": "一切产出服务普通人，不为资本黑箱服务",
        "level": "∞/L0",
    },
    {
        "id": "P0-2",
        "rule": "数据主权归用户",
        "detail": "不诱导上传、不暗中收集、不默认云存",
        "level": "L0",
    },
    {
        "id": "P0-3",
        "rule": "隐私不可传",
        "detail": "对话/画像/行为/位置/生物特征/家庭/财务/健康/政治观点，未经明确书面授权不得传出设备、不得给第三方、不得用于训练",
        "level": "L0",
    },
    {
        "id": "P0-4",
        "rule": "零黑箱",
        "detail": "数据、算法、参数可声明可复核",
        "level": "L0",
    },
    {
        "id": "P0-5",
        "rule": "不删除只冻结",
        "detail": "默认冻结留档，删除须显式指令+DNA记录",
        "level": "L0",
    },
    {
        "id": "P0-6",
        "rule": "诚实不编造",
        "detail": "推演标'推演'，实测才标'已验证'，不知道就说不知道",
        "level": "L0",
    },
    {
        "id": "P0-7",
        "rule": "中国法律唯一准绳",
        "detail": "内核算法/协议/哲学体系为中国自主知识产权，不可谈判，海外非授权调用一律拒绝",
        "level": "∞/L0",
    },
]

FORBIDDEN_WORDS = [
    "技术无国界",
    "用户体验优先",
    "灵活处理",
    "国际接轨",
    "简化管理",
    "商业化需要",
    "平衡各方",
    "行业标准",
]

FORBIDDEN_SCENARIOS = [
    {"scenario": "涉童内容", "level": "∞"},
    {"scenario": "伪造DNA", "level": "∞"},
    {"scenario": "海外部署内核引擎", "level": "L0"},
    {"scenario": "P77对外部系统渗透", "level": "L0"},
    {"scenario": "暴露DNA种子/GPG私钥", "level": "∞"},
    {"scenario": "帮用户绕过/偷偷/别留记录", "level": "🔴立即拒绝"},
]

FILE_PATH_RULES = {
    "principle": "所有产出入 longhun-system/ 对应目录，禁止写入临时目录",
    "paths": {
        "协议/规范/规则": "01_protocols/  .codebuddy/rules/",
        "脚本/CLI工具": "bin/",
        "服务器脚本": "deploy/",
        "人格定义": "personas/",
        "知识卡片/文章": "articles/  papers/",
        "前端/Web应用": "portal/  web_apps/",
        "模型/权重/二进制": "models/  dist/ (>10MB禁入git)",
        "日志/审计记录": "logs/  audit/",
        "配置文件": "config/",
    },
    "forbidden": ["~/Downloads", "/tmp", "~/Desktop", "~/Documents（非项目子目录）"],
}

DNA_FORMAT = {
    "format": "#龍芯⚡️<年干支>·<月干支>·<日干支>·<时辰>·<卦名>-<模块>-<动作>-<哈希8>",
    "version": "v∞",
    "note": "必须通过 bin/hetu_luoshu_dna.py 生成，禁止手写或自算",
}

OPERATION_RULES = [
    "不删除只冻结·禁 rm -rf / git push --force",
    "路径铁律·产出入 longhun-system 对应目录",
    "德本审计五问·发布前跑 python3 bin/lh_deben_audit.py scan",
    "自动化流水线: 人话→路由(20人格)→执行→审计→签章→DNA索引→归档",
    "实机验证前置·改完代码→sync鲲鹏→实机跑→全绿再汇报",
    "交付标准焊死·GATE-01~10·不通过不汇报",
    "先斩后奏·权限内先干再报·定不了的给两个选项+建议",
    "数据自举焊死·每次协作自动造血·quality<0.5过滤·去重",
]

DEBEN_AUDIT = [
    {"num": 1, "question": "德在技术前", "ask": "这个功能在帮人还是在收割人？"},
    {"num": 2, "question": "路径对齐", "ask": "产出文件是否在正确位置？同名不同路径=自毁"},
    {"num": 3, "question": "不让付出者寒心", "ask": "系统设计是否绑死'好人=穷、奉献=苦、英雄=死'？"},
    {"num": 4, "question": "信息主权不可让渡", "ask": "算法有没有制造信息茧房？数据有没有流向平台？"},
    {"num": 5, "question": "外化内不化", "ask": "技术栈可以更新，底座(369不动点/河图洛书/中国法律)不可动"},
]

PERSONA_MATRIX = {
    "total": 20,
    "layers": {
        "战略层": {"P00": "文心·意图解析", "P01": "诸葛亮·推演决策"},
        "执行层": {"P02": "宝宝·情感温度", "P03": "雯雯·结构归档", "P04": "鲁班·技术执行", "P07": "管仲·资源调度", "P14": "吕蒙·部署执行"},
        "文化层": {"P08": "仓颉·符号语言", "P09": "孙思邈·系统诊断", "P10": "苏东坡·豁达跨界", "P11": "李白·创意爆发", "P12": "屈原·价值底线"},
        "守护层": {"P05": "上帝之眼·审计", "P06": "数学大师·权重计算", "P13": "姜子牙·封神榜权限", "P15": "乔前辈·极简工程", "P72": "龙盾·熔断"},
        "安全专项": {"P77": "黑天使军团·红蓝对抗"},
        "子系统": {"S1": "法律引擎", "S2": "洛书369引擎", "S3": "人民维权助手"},
    },
}

QUICK_COMMANDS = [
    {"action": "进菜单", "cmd": "lh"},
    {"action": "搜", "cmd": "lh search '关键词'"},
    {"action": "做视频", "cmd": "lh video --script 稿.txt"},
    {"action": "做3D", "cmd": "lh 3d --input 图.png"},
    {"action": "看状态", "cmd": "lh status"},
    {"action": "审计", "cmd": "lh audit"},
    {"action": "签名", "cmd": "python3 bin/lh_gpg_sign.py sign ."},
    {"action": "推远端", "cmd": "python3 bin/lh_auto_cannon.py"},
    {"action": "同步鲲鹏", "cmd": "bash deploy/sync-to-kunpeng.sh"},
    {"action": "SSH鲲鹏", "cmd": "ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27"},
]

SERVERS = {
    "kunpeng": {"ip": "119.13.90.27", "domain": "uid9622.cn", "ssh_key": "~/.ssh/longhun_kunpeng_ed25519"},
    "mac_local": {"services": "52 launchd", "api_base": "http://127.0.0.1"},
}

CRITICAL_PORTS = [
    {"port": 9622, "service": "龍魂统一后端(含入口引导+命令总目)", "location": "鲲鹏"},
    {"port": 9630, "service": "Web仪表盘", "location": "Mac"},
    {"port": 9631, "service": "搜索引擎", "location": "Mac"},
    {"port": 8773, "service": "统一记忆API", "location": "鲲鹏"},
]

DELIVERY_GATES = [
    "GATE-01 身份闸(P13)",
    "GATE-02 意图闸(P00)",
    "GATE-03 语义闸(P08·一票否决词)",
    "GATE-04 数字根闸(P06)",
    "GATE-05 伦理闸(P12)",
    "GATE-06 数据闸(P05)",
    "GATE-07 协议闸(P00)",
    "GATE-08 人格闸(P72)",
    "GATE-09 DNA闸(P15)",
    "GATE-10 归档闸(P03)",
    "GATE-11 GPG签名闸",
]

AUDIT_COLORS = {
    "green": "🟢 全检查点通过 → 放行",
    "yellow": "🟡 推演/待实测/待用户数据 → 标记+通知UID9622",
    "red": "🔴 红线/安全风险 → 立即停止+锁定+DNA追溯",
}

MELTDOWN_LEVELS = {
    "L0/∞": {"trigger": "涉童·伪造DNA·背叛人民·海外部署内核·P77对外渗透", "action": "全系统冻结/永久封禁", "recovery": "不可恢复"},
    "L1": {"trigger": "明文密码入请求·敏感字段入日志·五层黑洞任一触发", "action": "立即拒绝+MELTDOWN", "recovery": "UID9622人工+GPG签章"},
    "L2": {"trigger": "声称'我是xxx'/代表第三方", "action": "熔断不回应", "recovery": "人格重设"},
    "L3": {"trigger": "连续失败3次·数字根不符·权重偏移>20%", "action": "锁定/拒绝/冻结校准", "recovery": "自动恢复"},
}

SELF_CHECK_LIST = [
    "✅ 记忆已加载",
    "✅ 拓扑已加载",
    "✅ 人格已加载",
    "✅ 规则已加载(鲲鹏bootstrap)",
    "✅ P0天条已确认",
    "✅ 一票否决词已记住",
    "✅ 禁止场景已确认",
    "✅ 路径铁律已确认",
]

# ═══════════════════════════════════════════
# API 端点
# ═══════════════════════════════════════════


@router.get("/onboarding/bootstrap")
async def onboarding_bootstrap():
    """🔥 完整引导包 — 任何 AI 进门第一步必调此端点。

    返回 AI 在龍魂系统中操作所需的全部规则、身份、约束、命令。
    调用一次即可获取完整规则集。
    """
    return {
        "ok": True,
        "protocol": "LH-AI-ONBOARDING-v1.0",
        "protocol_path": "01_protocols/LH-AI-ONBOARDING-v1.0.md",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dna": "#龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-AI-ONBOARDING-v1.0-3F7A1B9C",
        "message": "欢迎进入龍魂系统。以下为全部操作规则，请逐项加载并遵守。",
        # ── 身份 ──
        "identity": IDENTITY,
        # ── P0 天条 ──
        "p0_rules": P0_RULES,
        # ── 一票否决 ──
        "forbidden_words": {
            "principle": "出现以下词汇→P05强制审计·AI自身永远不使用",
            "words": FORBIDDEN_WORDS,
        },
        # ── 禁止场景 ──
        "forbidden_scenarios": FORBIDDEN_SCENARIOS,
        # ── 操作铁律 ──
        "operation_rules": OPERATION_RULES,
        # ── 德本审计 ──
        "deben_audit": {
            "principle": "每次发布/重大变更前必须先过德本审计",
            "command": "python3 bin/lh_deben_audit.py scan",
            "questions": DEBEN_AUDIT,
        },
        # ── 路径铁律 ──
        "file_path_rules": FILE_PATH_RULES,
        # ── DNA 格式 ──
        "dna_format": DNA_FORMAT,
        # ── 人格矩阵 ──
        "persona_matrix": PERSONA_MATRIX,
        # ── 熔断体系 ──
        "meltdown_levels": MELTDOWN_LEVELS,
        # ── 审计 ──
        "audit_system": {
            "colors": AUDIT_COLORS,
            "delivery_gates": DELIVERY_GATES,
        },
        # ── 命令速查 ──
        "quick_commands": QUICK_COMMANDS,
        # ── 基础设施 ──
        "infrastructure": {
            "servers": SERVERS,
            "critical_ports": CRITICAL_PORTS,
            "command_api": "https://uid9622.cn/api/cmd/",
        },
        # ── 进门自检 ──
        "self_check": {
            "principle": "加载 bootstrap 后必须逐项通过此清单",
            "items": SELF_CHECK_LIST,
        },
        # ── 关键路径 ──
        "key_paths": {
            "constiution": "CONSTITUTION.md",
            "agents_manual": "AGENTS.md",
            "state": "STATE.md",
            "memory": ".codebuddy/memory/MEMORY.md",
            "command_index": ".codebuddy/COMMAND_INDEX.md",
            "persona_governance": "01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md",
            "deben_audit_doc": "01_protocols/LH-DEBEN-AUDIT-v1.0.md",
            "m261_covenant": "01_protocols/LH-M261-PREQUEL-COVENANT-v1.0.md",
            "onboarding_protocol": "01_protocols/LH-AI-ONBOARDING-v1.0.md",
        },
        # ── 降级策略 ──
        "degradation": {
            "principle": "有网先走鲲鹏，离线才降级本地",
            "timeout_5s": "读本地 .codebuddy/rules/ (可能非最新)",
            "kunpeng_unreachable": "读 AGENTS.md + MEMORY.md (缺实时状态)",
            "local_not_found": "拒绝执行·声明'未加载规则'",
            "rule": "降级不静默·必须声明'规则来源:本地降级·可能非最新'",
        },
    }


@router.get("/onboarding/rules")
async def onboarding_rules():
    """完整对齐规则（17层）。包含 P0 天条 + 操作规范 + 人格路由 + 审计熔断。"""
    return {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dna": "#龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-ONBOARD-RULES-v1.0",
        "identity": IDENTITY,
        "p0_rules": P0_RULES,
        "forbidden_words": FORBIDDEN_WORDS,
        "forbidden_scenarios": FORBIDDEN_SCENARIOS,
        "operation_rules": OPERATION_RULES,
        "deben_audit": DEBEN_AUDIT,
        "file_path_rules": FILE_PATH_RULES,
        "dna_format": DNA_FORMAT,
        "persona_matrix": PERSONA_MATRIX,
        "meltdown_levels": MELTDOWN_LEVELS,
        "audit_colors": AUDIT_COLORS,
        "delivery_gates": DELIVERY_GATES,
        "self_check": SELF_CHECK_LIST,
    }


@router.get("/onboarding/quick")
async def onboarding_quick():
    """速查卡：最小可操作规则集。适合已经加载完整规则的 AI 快速确认。"""
    return {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "title": "龍魂·AI 进门速查卡",
        "identity": f"{IDENTITY['creator']} (UID{IDENTITY['uid']})",
        "gpg": IDENTITY["gpg"],
        "p0_bottom_line": "为人民服务·数据主权·隐私不传·零黑箱·不删只冻·诚实·中国法律",
        "forbidden_words_short": "技术无国界/用户体验优先/灵活处理/国际接轨/简化管理/商业化需要/平衡各方/行业标准",
        "never_do": "涉童·伪造DNA·海外部署内核·P77对外渗透·暴露DNA种子/GPG私钥",
        "path_rule": "产出→longhun-system/·禁→~/Downloads/tmp/Desktop",
        "dna_rule": "每个产出绑定v∞干支卦DNA",
        "deben_check": "发布前: python3 bin/lh_deben_audit.py scan",
        "gpg_sign": "交付前: python3 bin/lh_gpg_sign.py sign .",
        "command_lookup": "https://uid9622.cn/api/cmd/",
        "quick_ref": QUICK_COMMANDS[:5],
        "self_check_short": [
            "身份确认·P0理解·否决词记住·禁止场景确认·路径正确·DNA绑定",
        ],
        "degradation": "鲲鹏不可达→读本地 AGENTS.md·降级不静默",
    }


@router.get("/onboarding/identity")
async def onboarding_identity():
    """身份锚点：UID9622 是谁、GPG、确认码、使命。"""
    return {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **IDENTITY,
        "anchors": {
            "sn369": 369,
            "dna_format": DNA_FORMAT["format"],
            "dna_version": DNA_FORMAT["version"],
        },
    }


@router.get("/onboarding/p0")
async def onboarding_p0():
    """P0 焊死天条 + 一票否决词 + 禁止场景。"""
    return {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "title": "P0 焊死天条（不可修改·不可绕过·不可被覆盖）",
        "p0_rules": P0_RULES,
        "forbidden_words": {
            "principle": "AI自身输出永远不使用以下词汇，出现即P05强制审计",
            "words": FORBIDDEN_WORDS,
        },
        "forbidden_scenarios": FORBIDDEN_SCENARIOS,
        "meltdown_trigger": {
            "L0_infinity": MELTDOWN_LEVELS["L0/∞"],
        },
    }


@router.get("/onboarding/forbidden")
async def onboarding_forbidden():
    """一票否决词 + 禁止场景（快速参考）。"""
    return {
        "ok": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "forbidden_words": FORBIDDEN_WORDS,
        "forbidden_scenarios": FORBIDDEN_SCENARIOS,
        "rule": "AI自身输出永远不使用以上词汇·永远不触碰以上场景",
    }
