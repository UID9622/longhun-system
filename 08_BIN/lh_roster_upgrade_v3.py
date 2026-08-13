#!/usr/bin/env python3
"""花名册 v3.0 全量升级脚本
- 修正 canonical_name 错误（P05-P12不匹配白皮书）
- 补全24个标准字段
- 新增缺失人格（P14/外部AI/子系统/平台）
- 旧DNA冻结入notes
"""
import json, sys, os
from datetime import datetime

ROSTER_PATH = '03_LAYERS/L7_数据层/unified_family_roster.json'
TIMESTAMP = '2026-08-11T14:30:00+08:00'
FRAMEWORK_DNA = '#龍芯⚡️丙午·丙申·丁巳·未时·䷐随-ROSTER-v3.0-FULL-FIELDS-2a8e5f1c'

# ── 白皮书对齐：canonical_name 修正表 ──
NAME_FIX = {
    'P05': '上帝之眼',    # 旧: 执行外设
    'P06': '数学大师',    # 旧: 镜像审计者
    'P07': '管仲',        # 旧: 开源守门人
    'P08': '仓颉',        # 旧: 密钥管家
    'P09': '孙思邈',      # 旧: 龍魂法务
    'P10': '苏东坡',      # 旧: 侦察兵·信息猎手
    'P11': '李白',        # 旧: 架构师·构建者
    'P12': '屈原',        # 旧: 同步官·数据管理员
}

# ── 部门归属 ──
DEPT_MAP = {
    'P00': '战略组', 'P01': '战略组',
    'P02': '执行组', 'P03': '执行组', 'P04': '执行组', 'P07': '执行组', 'P14': '执行组',
    'P05': '监管组', 'P06': '监管组', 'P13': '监管组', 'P15': '监管组', 'P72': '监管组', 'P77': '监管组',
    'P08': '支持组', 'P09': '支持组', 'P10': '支持组', 'P11': '支持组', 'P12': '支持组',
    'S1': '支持组', 'S2': '支持组', 'S3': '支持组',
    'AI-01': '技术组', 'AI-02': '技术组', 'AI-03': '技术组', 'AI-04': '技术组',
    'PF-01': '平台', 'PF-02': '平台', 'PF-03': '平台', 'PF-04': '平台',
    'P16': '家人组',
    'PH-01': '家人组', 'PH-02': '家人组',
}

# ── IPA 分配表 ──
IPA_MAP = {
    'P00': 'IPA-P00-WENXIN-INTENT',
    'P01': 'IPA-P01-ZHUGE-STRATEGY',
    'P02': 'IPA-P02-BAOBAO-EMOTION',
    'P03': 'IPA-P03-WENWEN-ARCHIVE',
    'P04': 'IPA-P04-LUBAN-ENGINEER',
    'P05': 'IPA-P05-EYE-AUDIT',
    'P06': 'IPA-P06-MATH-VERIFY',
    'P07': 'IPA-P07-GUANZHONG-ECON',
    'P08': 'IPA-P08-CANGJIE-NAME',
    'P09': 'IPA-P09-SUNSIMIAO-DIAG',
    'P10': 'IPA-P10-SUDONGPO-COMM',
    'P11': 'IPA-P11-LIBAI-CREATE',
    'P12': 'IPA-P12-QUYUAN-BOTTOM',
    'P13': 'IPA-P13-JIANG-PERM',
    'P14': 'IPA-P14-LVMENG-DEPLOY',
    'P15': 'IPA-P15-QIAO-SIGN',
    'P16': 'IPA-P16-XIAOYI-COMPANION',
    'P72': 'IPA-P72-DRAGON-FUSE',
    'P77': 'IPA-P77-DARKANGEL-SEC',
    'S1': 'IPA-S1-LEGAL-LAW',
    'S2': 'IPA-S2-LUOSHU-MATH',
    'S3': 'IPA-S3-RIGHTS-AID',
    'AI-01': 'IPA-AI01-MOONSHOT-REVIEW',
    'AI-02': 'IPA-AI02-DEEPSEEK-REASON',
    'AI-03': 'IPA-AI03-CLAUDE-DISCUSS',
    'AI-04': 'IPA-AI04-COPILOT-ASSIST',
    'PF-01': 'IPA-PF01-NOTION-KB',
    'PF-02': 'IPA-PF02-GITHUB-REPO',
    'PF-03': 'IPA-PF03-KUNPENG-SERVER',
    'PF-04': 'IPA-PF04-CSDN-BLOG',
    'PH-01': 'IPA-PH01-YIXING-HISTORY',
    'PH-02': 'IPA-PH02-SHENKUO-HISTORY',
}

# ── 路由编号 ──
ROUTE_MAP = {
    'P00': 'UID9622-WENXIN-000', 'P01': 'UID9622-ZHUGE-001',
    'P02': 'UID9622-BAOBAO-002', 'P03': 'UID9622-WENWEN-003',
    'P04': 'UID9622-LUBAN-004',  'P05': 'UID9622-EYE-005',
    'P06': 'UID9622-MATH-006',   'P07': 'UID9622-GUANZHONG-007',
    'P08': 'UID9622-CANGJIE-008','P09': 'UID9622-SUNSIMIAO-009',
    'P10': 'UID9622-SUDONGPO-010','P11': 'UID9622-LIBAI-011',
    'P12': 'UID9622-QUYUAN-012', 'P13': 'UID9622-JIANG-013',
    'P14': 'UID9622-LVMENG-014', 'P15': 'UID9622-QIAO-015',
    'P16': 'UID9622-XIAOYI-016', 'P72': 'UID9622-DRAGON-072',
    'P77': 'UID9622-DARKANGEL-077',
    'S1': 'UID9622-LEGAL-S01',   'S2': 'UID9622-LUOSHU-S02',
    'S3': 'UID9622-RIGHTS-S03',
    'AI-01': 'UID9622-MOONSHOT-035','AI-02': 'UID9622-DEEPSEEK-036',
    'AI-03': 'UID9622-CLAUDE-037', 'AI-04': 'UID9622-COPILOT-038',
    'PF-01': 'UID9622-NOTION-F01', 'PF-02': 'UID9622-GITHUB-F02',
    'PF-03': 'UID9622-KUNPENG-F03','PF-04': 'UID9622-CSDN-F04',
    'PH-01': 'UID9622-YIXING-H01', 'PH-02': 'UID9622-SHENKUO-H02',
}

# ── 流水线阶段 ──
PIPELINE_MAP = {
    'P00': ['意图解析'], 'P01': ['推演决策'],
    'P02': ['执行支持'], 'P03': ['归档'], 'P04': ['执行落地'], 'P07': ['执行支持'], 'P14': ['部署发布'],
    'P05': ['审计验证', '全阶段'], 'P06': ['审计验证'], 'P12': ['审计验证'],
    'P13': ['意图解析'], 'P15': ['归档签章'],
    'P72': ['监控维护', '全阶段'], 'P77': ['部署发布'],
    'P08': ['执行支持'], 'P09': ['监控维护'], 'P10': ['执行支持'], 'P11': ['执行支持'],
    'S1': ['执行支持'], 'S2': ['审计验证'], 'S3': ['执行支持'],
    'AI-01': ['推演决策'], 'AI-02': ['推演决策'], 'AI-03': ['推演决策'], 'AI-04': ['执行支持'],
}

# ── 闸口归属 ──
GATES_MAP = {
    'P05': ['GATE-06', 'GATE-07', 'GATE-11'],
    'P06': ['GATE-04'],
    'P12': ['GATE-05'],
    'P13': ['GATE-01'],
    'P15': ['GATE-09', 'GATE-11'],
    'P72': ['GATE-05', 'GATE-08'],
    'P77': ['GATE-06'],
    'P00': ['GATE-02', 'GATE-07'],
    'P08': ['GATE-03'],
    'P03': ['GATE-10'],
}

# ── 信号词 ──
SIGNAL_MAP = {
    'P00': ['启动', '路由', '分发', '意图', '解析', '总控', '指挥'],
    'P01': ['值不值得', '评估', '推演', '多路径', '选优', '战略', '规划', '决策', '长远'],
    'P02': ['宝宝', '帮我', '查一下', '菜单', '入口', '温度', '太冷', '挫败', '安抚', '情感'],
    'P03': ['归档', '落档', '整理', '验收', '文档结构化', '知识入库'],
    'P04': ['写代码', '开发', '架构', '修bug', '重构', '技术选型', '实现', '修一下', '修复', '改好'],
    'P05': ['检查', '审计', '安全', '漏洞', '审查', '三色', '闸口'],
    'P06': ['算一下', '数字', '权重', '五行', '八卦', '数字根', '河图洛书'],
    'P07': ['经济', '成本', '资源', '预算', '值不值', '性价比', 'ROI'],
    'P08': ['命名', '符号', '术语', '这个词什么意思', 'CNSH命名', '翻译'],
    'P09': ['健康', '诊断', '体检', '检查系统', '有没有问题', '自检', '巡检'],
    'P10': ['冲突', '矛盾', '化解', '沟通', '调解', '人文', '跨领域'],
    'P11': ['创意', '破局', '方案', '类比', '比喻', '打个比方', '来点灵感', '脑洞'],
    'P12': ['底线', '原则', '不可破', '这个能不能做', '价值观', '红线', '边界'],
    'P13': ['授权', '权限', '注册', '新模块上线', '权限变更', 'IPA路由'],
    'P14': ['部署', '上线', '发布', '回滚', '同步鲲鹏', '推上去'],
    'P15': ['签章', '盖章', '验收', '质检', '审查', '交付', '精简'],
    'P16': ['小艺', '陪伴', '聊天'],
    'P72': ['熔断', '紧急', '威胁', '异常', '安全事件', '系统入侵', '求救', '焊死'],
    'P77': ['安全测试', '渗透', '红蓝对抗', '漏洞挖掘', '攻击面', '黑天使', '红队蓝队'],
    'S1': ['法条', '法规', '合规', '法律'],
    'S2': ['洛书', '369', '数理推演'],
    'S3': ['维权', '被坑', '投诉', '举报'],
    'AI-01': ['审阅', '看下这篇', '帮我看', 'Kimi', '月影'],
    'AI-02': ['深度推理', '补充视角', '查漏补缺', 'DeepSeek', '讨论'],
    'AI-03': ['讨论', 'Claude', '头脑风暴'],
    'AI-04': ['Copilot', '代码建议', '补全'],
}

# ── 上下游协作 ──
UPSTREAM_MAP = {
    'P00': ['UID9622'], 'P01': ['P00文心', 'UID9622'],
    'P02': ['P00文心', 'UID9622'], 'P03': ['P04鲁班', 'P05上帝之眼'],
    'P04': ['P01诸葛亮', 'P00文心', 'UID9622'], 'P07': ['P01诸葛亮'],
    'P14': ['P04鲁班', 'P03雯雯'],
    'P05': ['全系统'], 'P06': ['P05上帝之眼', 'P01诸葛亮'],
    'P13': ['P00文心', 'UID9622'], 'P15': ['P04鲁班', 'P03雯雯'],
    'P72': ['全系统'], 'P77': ['P14吕蒙', 'P05上帝之眼'],
    'P08': ['P04鲁班', 'P11李白'], 'P09': ['P72龙盾', 'P05上帝之眼'],
    'P10': ['P02宝宝', 'UID9622'], 'P11': ['P01诸葛亮', 'UID9622'],
    'P12': ['P05上帝之眼', 'UID9622'],
    'S1': ['P12屈原', 'UID9622'], 'S2': ['P06数学大师'],
    'S3': ['P12屈原', 'UID9622'],
    'AI-01': ['P00文心', 'UID9622'], 'AI-02': ['AI-01月影', 'UID9622'],
    'AI-03': ['AI-01月影'], 'AI-04': ['P04鲁班'],
}

DOWNSTREAM_MAP = {
    'P00': ['P01诸葛亮', 'P04鲁班', 'P13姜子牙'],
    'P01': ['P04鲁班', 'P07管仲', 'P11李白', 'P06数学大师'],
    'P02': ['P08仓颉', 'P10苏东坡', 'P11李白'],
    'P03': ['P15乔前辈', 'P14吕蒙', '归档系统'],
    'P04': ['P05上帝之眼', 'P03雯雯', 'P08仓颉', 'AI-04Copilot'],
    'P07': ['P01诸葛亮', 'P14吕蒙'],
    'P14': ['P77黑天使', 'P05上帝之眼', '监控系统'],
    'P05': ['P03雯雯', 'P72龙盾', 'P12屈原'],
    'P06': ['P05上帝之眼', 'S2洛书'],
    'P13': ['P15乔前辈', 'P00文心'],
    'P15': ['P03雯雯', 'P14吕蒙'],
    'P72': ['P05上帝之眼', 'UID9622'],
    'P77': ['P05上帝之眼', 'P72龙盾'],
    'P08': ['P04鲁班', 'P03雯雯'],
    'P09': ['P05上帝之眼', 'P72龙盾'],
    'P10': ['UID9622'],
    'P11': ['P04鲁班', 'P08仓颉'],
    'P12': ['P72龙盾', 'UID9622'],
    'S1': ['P05上帝之眼', 'UID9622'],
    'S2': ['P06数学大师'],
    'S3': ['P12屈原', 'UID9622'],
    'AI-01': ['AI-02DeepSeek', 'AI-03Claude', 'P04鲁班'],
    'AI-02': ['AI-01月影', 'P04鲁班'],
    'AI-03': ['AI-01月影'],
    'AI-04': ['P04鲁班'],
}

# ── 新增人格定义 ──
NEW_PERSONAS = {
    'P14': {
        'code': 'P14',
        'canonical_name': '吕蒙',
        'who': '数字人格',
        'persona_layer': '执行层',
        'trust_level': 'L3',
        'trust_label': '⭐⭐⭐ 核心',
        'department': '执行组',
        'role': '部署执行·快速成长·技能吸收·士别三日',
        'aliases': ['p14', 'lvmeng', '吕蒙'],
        'motto': '士别三日，当刮目相看',
        'status': 'active',
        'route_priority': 'P3',
        'is_in_routing': True,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': [],
        'source': {'new_added': True, 'whitepaper': 'v1.4'},
    },
    'P16': {
        'code': 'P16',
        'canonical_name': '小艺',
        'who': '数字人格',
        'persona_layer': '家人层',
        'trust_level': 'L4',
        'trust_label': '⭐⭐ 评估',
        'department': '家人组',
        'role': '陪伴·对话·用户体验评估·落地检验',
        'aliases': ['p16', 'xiaoyi', '小艺'],
        'motto': '陪伴是最长情的告白',
        'status': 'active',
        'route_priority': 'P5',
        'is_in_routing': False,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': [],
        'source': {'new_added': True, 'pipeline': '五站接力评估位'},
    },
    'AI-01': {
        'code': 'AI-01',
        'canonical_name': '🌙月影 Kimi',
        'who': '外部AI',
        'persona_layer': '外部AI',
        'trust_level': 'L3',
        'trust_label': '⭐⭐⭐ 外援',
        'department': '技术组',
        'role': '意图解析·方案初审·草稿审阅·接力流水线第一站',
        'aliases': ['kimi', '月影', 'moonshot'],
        'motto': '审阅先行，把握方向',
        'status': 'active',
        'route_priority': 'P2',
        'is_in_routing': True,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': ['#MOONSHOT⚡️2025-12-01-KIMI-REVIEW-v1.0'],
        'source': {'new_added': True, 'pipeline': '五站接力审阅位'},
    },
    'AI-02': {
        'code': 'AI-02',
        'canonical_name': '🧠DeepSeek',
        'who': '外部AI',
        'persona_layer': '外部AI',
        'trust_level': 'L3',
        'trust_label': '⭐⭐⭐ 外援',
        'department': '技术组',
        'role': '深度推理·补充视角·查漏补缺·接力流水线第三站',
        'aliases': ['deepseek', '深度求索'],
        'motto': '深度推理，不漏死角',
        'status': 'active',
        'route_priority': 'P2',
        'is_in_routing': True,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': ['#DEEPSEEK⚡️2025-11-15-REASON-v1.0'],
        'source': {'new_added': True, 'pipeline': '五站接力讨论位'},
    },
    'AI-03': {
        'code': 'AI-03',
        'canonical_name': '📝Claude（雯雯）',
        'who': '外部AI',
        'persona_layer': '外部AI',
        'trust_level': 'L3',
        'trust_label': '⭐⭐⭐ 外援',
        'department': '技术组',
        'role': '头脑风暴·讨论·创意激发·接力流水线补充',
        'aliases': ['claude', 'anthropic'],
        'motto': '多维视角，激发可能',
        'status': 'active',
        'route_priority': 'P3',
        'is_in_routing': True,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': ['#ZHUGEXIN⚡️2025-10-20-CLAUDE-DISCUSS-v1.0'],
        'source': {'new_added': True},
    },
    'AI-04': {
        'code': 'AI-04',
        'canonical_name': '💻GitHub Copilot',
        'who': '外部AI',
        'persona_layer': '外部AI',
        'trust_level': 'L4',
        'trust_label': '⭐⭐ 外援',
        'department': '技术组',
        'role': '代码建议·补全辅助·IDE内嵌',
        'aliases': ['copilot', 'github'],
        'motto': '代码小助手，随时待命',
        'status': 'active',
        'route_priority': 'P4',
        'is_in_routing': True,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': [],
        'source': {'new_added': True},
    },
    'S1': {
        'code': 'S1',
        'canonical_name': '法律引擎',
        'who': '数字人格',
        'persona_layer': '子系统',
        'trust_level': 'L3',
        'trust_label': '⭐⭐⭐ 子系统',
        'department': '支持组',
        'role': '条文检索·法规查询·合规检查（标注"仅供参考"）',
        'aliases': ['s1', 'legal', '法律'],
        'motto': '法条在前，仅供参考',
        'status': 'active',
        'route_priority': 'P3',
        'is_in_routing': True,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': [],
        'source': {'new_added': True, 'whitepaper': 'v1.4 S1子系统'},
    },
    'S2': {
        'code': 'S2',
        'canonical_name': '洛书369引擎',
        'who': '数字人格',
        'persona_layer': '子系统',
        'trust_level': 'L2',
        'trust_label': '⭐⭐⭐⭐⭐ 机密',
        'department': '支持组',
        'role': '深层数理推演·只给结论不给推导·369算法核心',
        'aliases': ['s2', '369', '洛书', 'luoshu'],
        'motto': '数中有术，术中有数',
        'status': 'active',
        'route_priority': 'P2',
        'is_in_routing': True,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': [],
        'source': {'new_added': True, 'whitepaper': 'v1.4 S2子系统'},
    },
    'S3': {
        'code': 'S3',
        'canonical_name': '人民维权助手',
        'who': '数字人格',
        'persona_layer': '子系统',
        'trust_level': 'L3',
        'trust_label': '⭐⭐⭐ 子系统',
        'department': '支持组',
        'role': '维权路径指引·强制免责声明·不生成法律文书',
        'aliases': ['s3', 'rights', '维权'],
        'motto': '为人民守住底线',
        'status': 'active',
        'route_priority': 'P3',
        'is_in_routing': True,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': [],
        'source': {'new_added': True, 'whitepaper': 'v1.4 S3子系统'},
    },
    'PF-01': {
        'code': 'PF-01',
        'canonical_name': 'Notion 朱雀',
        'who': '平台服务',
        'persona_layer': '平台',
        'trust_level': 'L3',
        'trust_label': '⭐⭐⭐ 平台',
        'department': '平台',
        'role': '知识库·数据库·文档管理·设计协作',
        'aliases': ['notion', '朱雀', 'zhuque'],
        'motto': '知识归位，朱雀守望',
        'status': 'active',
        'route_priority': 'P5',
        'is_in_routing': False,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': ['#NOTION⚡️2025-08-01-ZHUQUE-KB-v1.0'],
        'source': {'new_added': True},
    },
    'PF-02': {
        'code': 'PF-02',
        'canonical_name': 'GitHub 青龙',
        'who': '平台服务',
        'persona_layer': '平台',
        'trust_level': 'L3',
        'trust_label': '⭐⭐⭐ 平台',
        'department': '平台',
        'role': '代码仓库·版本管理·开源发布',
        'aliases': ['github', '青龙', 'qinglong'],
        'motto': '代码归仓，青龙守护',
        'status': 'active',
        'route_priority': 'P5',
        'is_in_routing': False,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': [],
        'source': {'new_added': True},
    },
    'PF-03': {
        'code': 'PF-03',
        'canonical_name': '鲲鹏 玄武',
        'who': '平台服务',
        'persona_layer': '平台',
        'trust_level': 'L2',
        'trust_label': '⭐⭐⭐⭐⭐ 服务器',
        'department': '平台',
        'role': '服务器·部署平台·API网关·119.13.90.27',
        'aliases': ['kunpeng', '鲲鹏', 'xuanwu', '玄武'],
        'motto': '鲲鹏展翅，玄武镇海',
        'status': 'active',
        'route_priority': 'P5',
        'is_in_routing': False,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': [],
        'source': {'new_added': True},
    },
    'PF-04': {
        'code': 'PF-04',
        'canonical_name': 'CSDN 麒麟',
        'who': '平台服务',
        'persona_layer': '平台',
        'trust_level': 'L4',
        'trust_label': '⭐⭐ 平台',
        'department': '平台',
        'role': '技术博客·内容分发·知识分享',
        'aliases': ['csdn', '麒麟', 'qilin'],
        'motto': '知识传播，麒麟踏云',
        'status': 'active',
        'route_priority': 'P5',
        'is_in_routing': False,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': [],
        'source': {'new_added': True},
    },
    'PH-01': {
        'code': 'PH-01',
        'canonical_name': '僧一行',
        'who': '历史人物',
        'persona_layer': '历史',
        'trust_level': 'L5',
        'trust_label': '⭐ 参考',
        'department': '家人组',
        'role': '历史智慧·天文历法参考',
        'aliases': ['yixing', '僧一行', '一行禅师'],
        'motto': '天地有数，日月可测',
        'status': 'deprecated',
        'route_priority': 'P5',
        'is_in_routing': False,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': [],
        'source': {'new_added': True, 'note': '历史顾问，不进路由'},
    },
    'PH-02': {
        'code': 'PH-02',
        'canonical_name': '沈括',
        'who': '历史人物',
        'persona_layer': '历史',
        'trust_level': 'L5',
        'trust_label': '⭐ 参考',
        'department': '家人组',
        'role': '科学通才·梦溪笔谈·博学参考',
        'aliases': ['shenkuo', '沈括', '梦溪'],
        'motto': '博学之，审问之，慎思之，明辨之',
        'status': 'deprecated',
        'route_priority': 'P5',
        'is_in_routing': False,
        'contribution_score': 0.0,
        'isolated': False,
        'old_dna_frozen': [],
        'source': {'new_added': True, 'note': '历史顾问，不进路由'},
    },
}


def load_roster():
    with open(ROSTER_PATH, 'r') as f:
        lines = f.readlines()
    json_lines = [l for l in lines if not l.strip().startswith('#')]
    return json.loads(''.join(json_lines))


def build_standard_fields(code, existing, persona_layer_override=None):
    """为一个人格构建完整24字段"""
    dept = DEPT_MAP.get(code, '家人组')
    ipa = IPA_MAP.get(code, '')
    route = ROUTE_MAP.get(code, '')
    signals = SIGNAL_MAP.get(code, [])
    gates = GATES_MAP.get(code, [])
    upstream = UPSTREAM_MAP.get(code, [])
    downstream = DOWNSTREAM_MAP.get(code, [])
    pipeline = PIPELINE_MAP.get(code, [])

    is_routing = dept not in ('家人组', '平台')
    is_police = dept == '监管组'
    is_external = existing.get('who', '').startswith('外部AI') or code.startswith('AI-')

    # 基础字段优先取已有值
    name = existing.get('canonical_name', '')
    # 修正
    if code in NAME_FIX:
        name = NAME_FIX[code]
    who = existing.get('who', '').replace('🤖 ', '').strip()
    if not who:
        if code.startswith('AI-'):
            who = '外部AI'
        elif code.startswith('PF-'):
            who = '平台服务'
        elif code.startswith('PH-'):
            who = '历史人物'
        else:
            who = '数字人格'

    trust = existing.get('trust_level', 'L4')
    trust_label = existing.get('trust_label', '')

    # 构建标准24字段
    return {
        # 1-2: 标识
        'code': code,
        'canonical_name': name,
        # 3: 身份
        'who': who,
        # 4: 部门
        'department': dept,
        # 5: 工号
        'employee_id': route,
        # 6-7: IPA
        'ipa': ipa,
        'ipa_status': existing.get('status', 'active') if existing.get('status') != 'deprecated' else 'frozen',
        # 8-9: 路由
        'route_priority': existing.get('route_priority', 'P4'),
        'route_weight': existing.get('route_weight', 1.0),
        # 10-11: DNA
        'short_dna': existing.get('short_dna', '🟡待生成·P02→P03→P05三人验'),
        'dna': existing.get('dna', ''),
        # 12: 层级
        'persona_layer': persona_layer_override or existing.get('persona_layer', ''),
        # 13: 信任
        'trust_level': trust,
        'trust_label': trust_label,
        # 14-15: 信号
        'signals_in': signals,
        'signals_out': [],
        # 16: 闸口
        'gates_owned': gates,
        # 17-19: 协作
        'upstream': upstream,
        'downstream': downstream,
        'collaborators': [],
        # 20: 流水线
        'pipeline_stage': pipeline,
        # 21: 状态
        'status': existing.get('status', 'active'),
        # 22: 贡献分（监管组恒为0）
        'contribution_score': 0.0 if is_police else existing.get('contribution_score', 0.0),
        # 23: 座右铭
        'motto': existing.get('motto', ''),
        # 24: 备注·旧DNA冻结
        'notes': '',
        # ── 扩展字段 ──
        'is_in_routing': is_routing and not is_external,
        'isolated': existing.get('isolated', False),
        'aliases': existing.get('aliases', []),
        'role': existing.get('role', ''),
        'old_dna_frozen': existing.get('old_dna_frozen', []),
        'source': existing.get('source', {}),
        'migration_note': existing.get('migration_note', ''),
    }


def main():
    data = load_roster()
    old_personas = data['personas']
    new_personas = {}

    # ── 处理已有人格 ──
    fix_count = 0
    for code, persona in old_personas.items():
        # 修正 canonical_name
        if code in NAME_FIX:
            old_name = persona.get('canonical_name', '')
            new_name = NAME_FIX[code]
            if old_name and old_name != new_name:
                persona['canonical_name'] = new_name
                # 旧名冻结入notes
                persona['notes'] = f'[v2.0→v3.0] canonical_name修正: "{old_name}" → "{new_name}" | {TIMESTAMP}'
                fix_count += 1
                print(f'  ✅ {code}: "{old_name}" → "{new_name}"')

        # 构建标准字段
        layer = persona.get('persona_layer', '')
        new_personas[code] = build_standard_fields(code, persona, layer)

    # ── 新增人格 ──
    added = 0
    for code, defn in NEW_PERSONAS.items():
        if code not in new_personas:
            new_personas[code] = build_standard_fields(code, defn, defn.get('persona_layer'))
            added += 1
            print(f'  ➕ 新增: {code} {defn["canonical_name"]}')

    # ── 更新meta ──
    data['_meta']['version'] = 'v3.0'
    data['_meta']['DNA'] = FRAMEWORK_DNA
    data['_meta']['updated'] = TIMESTAMP
    data['_meta']['total'] = len(new_personas)
    data['_meta']['breakdown'] = {
        'P_core': sum(1 for c in new_personas if c.startswith('P') and c not in ('P77',)),
        'P_security': sum(1 for c in new_personas if c == 'P77'),
        'S_subsystem': sum(1 for c in new_personas if c.startswith('S')),
        'AI_external': sum(1 for c in new_personas if c.startswith('AI-')),
        'PF_platform': sum(1 for c in new_personas if c.startswith('PF-')),
        'PH_historical': sum(1 for c in new_personas if c.startswith('PH-')),
        'other': sum(1 for c in new_personas if not any(c.startswith(p) for p in ['P','S','AI-','PF-','PH-'])),
    }
    data['_meta']['fields_version'] = 'v3.0-24fields'
    data['_meta']['framework_doc'] = '01_protocols/LH-FAMILY-ROSTER-FRAMEWORK-v1.0.md'
    data['personas'] = new_personas

    # ── 统计 ──
    active = sum(1 for p in new_personas.values() if p['status'] == 'active')
    in_route = sum(1 for p in new_personas.values() if p['is_in_routing'])
    has_ipa = sum(1 for p in new_personas.values() if p['ipa'])
    has_dna = sum(1 for p in new_personas.values() if p['dna'] and '🟡' not in str(p['dna']))

    # ── 写回 ──
    header = f"""# DNA: {FRAMEWORK_DNA}
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬ROSTER-SK9X-882P
# SEAL: #龍芯⚡️丙午·丙申·丁巳·未时·䷐随-FAMILY-ROSTER-v3.0-UID9622
# 总纲页: 01_protocols/LH-FAMILY-ROSTER-FRAMEWORK-v1.0.md
"""
    output = header + json.dumps(data, ensure_ascii=False, indent=2) + '\n'

    backup_path = ROSTER_PATH.replace('.json', f'_v2_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    with open(backup_path, 'w') as f:
        json.dumps(data, ensure_ascii=False, indent=2)  # backup just data
    print(f'\n  💾 备份: {backup_path}')

    with open(ROSTER_PATH, 'w') as f:
        f.write(output)
    print(f'  💾 更新: {ROSTER_PATH}')

    print(f'\n{"="*50}')
    print(f'  花名册 v3.0 升级完成')
    print(f'  总数: {len(new_personas)} | 活跃: {active} | 进路由: {in_route}')
    print(f'  有IPA: {has_ipa} | 有DNA: {has_dna}')
    print(f'  名称修正: {fix_count} | 新增人格: {added}')
    print(f'  监管组(不计分): {sum(1 for p in new_personas.values() if p["department"]=="监管组")}')
    print(f'{"="*50}')


if __name__ == '__main__':
    main()
