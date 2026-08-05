#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·辛未·丙戌·酉·大壮-NOTION-TRAIN-v1.5
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# 🐉 龍魂·Notion主控页面→训练语料生成器 v1.5
# DNA: #龍芯⚡️丙午·辛未·丙戌·酉·大壮-NOTION-TRAIN-v1.5
# 确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

"""
从Notion主控页面镜像提取结构化训练语料
1. 审查152个子页面 → 18分类体系
2. 自动补全缺失的逻辑区块
3. 生成对齐DNA的知识锚点语料
4. 输出train.jsonl + valid.jsonl
"""

import json, os, re, hashlib
from datetime import datetime

PAGES_DIR = "/Users/zuimeidedeyihan/longhun-system/docs/notion_mirror/pages"
OUTPUT_DIR = "/Users/zuimeidedeyihan/longhun-system/models/longhun-v1.0/lora_output/data"

# ============================================================
# PART 1: 页面结构审查 → 18分类体系
# ============================================================

CATEGORY_DEFS = {
    "安全认证": {
        "emoji": "🔐",
        "desc": "身份认证、密钥管理、数据安全、DNA加密",
        "subcategories": ["身份认证", "密钥管理", "DNA安全", "数据加密", "访问控制"],
        "pages": []
    },
    "AI智能体": {
        "emoji": "🧠",
        "desc": "AI大脑、智能体架构、MCP协议、意图识别",
        "subcategories": ["大脑架构", "MCP生态", "意图路由", "人格系统", "智能体手册"],
        "pages": []
    },
    "龍魂核心": {
        "emoji": "🐉",
        "desc": "龍魂系统本身、觉醒历程、传奇起点、底层逻辑",
        "subcategories": ["系统定义", "觉醒历程", "底层逻辑", "宣言声明", "版本演进"],
        "pages": []
    },
    "治理协议": {
        "emoji": "⚖️",
        "desc": "宪法、北辰协议、治理框架、铁律规则",
        "subcategories": ["宪法层", "北辰协议", "治理框架", "铁律规则", "伦理边界"],
        "pages": []
    },
    "论文白皮书": {
        "emoji": "📜",
        "desc": "学术论文、IEEE白皮书、arXiv投稿",
        "subcategories": ["IEEE论文", "arXiv投稿", "学术白皮书", "技术论文", "哲学论文"],
        "pages": []
    },
    "中国哲学": {
        "emoji": "☯️",
        "desc": "易经、道德经、太极、五行、河图洛书",
        "subcategories": ["易经应用", "道德经引擎", "369洛书", "五行生克", "太极算法"],
        "pages": []
    },
    "数字资产": {
        "emoji": "💎",
        "desc": "数字身份、数字人、IP资产、内容归档",
        "subcategories": ["数字身份", "数字人", "IP资产", "内容归档", "对话记录"],
        "pages": []
    },
    "CNSH中文编程": {
        "emoji": "🀄",
        "desc": "中文编程语言、语法规范、编译器、甲骨文",
        "subcategories": ["语法规范", "编译器", "甲骨文", "运行时", "工具链"],
        "pages": []
    },
    "终端UI": {
        "emoji": "🌊",
        "desc": "终端界面、交互入口、可视化设计",
        "subcategories": ["终端版本", "交互设计", "可视化", "入口页面"],
        "pages": []
    },
    "审计模板": {
        "emoji": "📋",
        "desc": "三色审计、创作登记、日报模板",
        "subcategories": ["三色审计", "创作登记", "日报模板", "发布检查"],
        "pages": []
    },
    "工具工程": {
        "emoji": "🔧",
        "desc": "MVP构建、开发工具、部署运维",
        "subcategories": ["MVP构建", "开发工具", "部署运维", "API文档", "本地搭建"],
        "pages": []
    },
    "设计创意": {
        "emoji": "🎨",
        "desc": "字体设计、UI设计、创意作品",
        "subcategories": ["字体设计", "UI设计", "创意作品", "多媒体"],
        "pages": []
    },
    "发布传播": {
        "emoji": "📡",
        "desc": "CSDN、知乎、社交媒体发布策略",
        "subcategories": ["CSDN", "知乎", "社交媒体", "内容策略", "跨平台"],
        "pages": []
    },
    "个人语录": {
        "emoji": "💬",
        "desc": "老大原话、人生感悟、永久存档",
        "subcategories": ["老大原话", "人生感悟", "永久存档", "深夜特供"],
        "pages": []
    },
    "时间历史": {
        "emoji": "⏳",
        "desc": "时间线、万年历、历史归档",
        "subcategories": ["时间线", "万年历", "历史归档", "里程碑"],
        "pages": []
    },
    "交接协作": {
        "emoji": "🤝",
        "desc": "宝宝交接、团队协作、知识传递",
        "subcategories": ["宝宝交接", "知识传递", "团队协作", "Agent手册"],
        "pages": []
    },
    "企业商业": {
        "emoji": "📊",
        "desc": "基金会、企业方案、商业模式",
        "subcategories": ["基金会", "企业方案", "商业模式", "消费保障"],
        "pages": []
    },
    "安全防御": {
        "emoji": "🛡️",
        "desc": "攻击者档案、安全防护、异常检测",
        "subcategories": ["攻击者档案", "安全防护", "异常检测", "渗透测试"],
        "pages": []
    },
}

# 分类关键词映射
KEYWORD_MAP = {
    "安全认证": ["认证", "密钥", "加密", "安全架构", "DNA安全", "身份认证"],
    "AI智能体": ["智能体", "大脑", "MCP", "AI人格", "意图识别", "语义翻译", "Agent", "人格路由", "智能体大脑", "自适应引擎"],
    "龍魂核心": ["龍魂系统·", "龍魂觉醒", "龍魂传奇", "底层逻辑", "龍魂系统·宣言", "龍魂指令集", "龍魂·沉浸式复交", "龍魂底层执行"],
    "治理协议": ["宪法", "北辰协议", "治理", "铁律", "伦理", "一票否决", "德者永生殿", "全球规则", "路由回流"],
    "论文白皮书": ["论文", "白皮书", "IEEE", "arXiv", "投稿", "学术"],
    "中国哲学": ["易经", "道德经", "太极", "五行", "河图", "洛书", "369", "哲学", "国学"],
    "数字资产": ["数字资产", "数字人", "IP", "数字身份", "主权数字", "大杂烩"],
    "CNSH中文编程": ["CNSH", "中文编程", "甲骨文", "中文语法", "立碑工程", "Runtime", "快乐版"],
    "终端UI": ["终端", "交互", "可视化", "入口", "赛博", "水墨", "亚特兰蒂斯", "星际"],
    "审计模板": ["审计", "模板", "日报", "登记表", "检查模板", "发布前检查"],
    "工具工程": ["MVP", "搭建", "工具", "Notion OS", "API", "本地测试", "部署", "SRS", "需求规格"],
    "设计创意": ["字体", "鲁班", "设计", "字匠", "龍魂版"],
    "发布传播": ["CSDN", "知乎", "发布", "传播", "内容归类", "占位稿"],
    "个人语录": ["老大", "Lucky", "原话", "感言", "感悟", "深夜", "在水里", "软件清单", "教育孩子"],
    "时间历史": ["时间线", "万年历", "历史", "执行日志", "耻辱墙"],
    "交接协作": ["交接", "宝宝", "协作", "通心译", "CLAUE.md", "通关文牒"],
    "企业商业": ["基金会", "企业", "商业", "消费保障", "企业灯"],
    "安全防御": ["攻击", "排异", "异常检测", "反面教材", "安全防护", "OpenClaw", "信息牢笼", "诈骗"],
}

def classify_page(title):
    """根据标题关键词分类"""
    for cat, keywords in KEYWORD_MAP.items():
        for kw in keywords:
            if kw in title:
                return cat
    return None

# ============================================================
# PART 2: 审查缺失区块 → 自动补充
# ============================================================

MISSING_BLOCKS = {
    "安全认证": [
        "龍魂·零信任安全架构 v1.0｜永不信任·始终验证",
        "龍魂·生物特征认证系统｜多维生物特征融合",
        "龍魂·量子密钥分发方案｜抗量子计算安全通信",
    ],
    "AI智能体": [
        "龍魂·多Agent协作协议 v1.0｜分布式智能体通信标准",
        "龍魂·Agent生命周期管理｜创建·运行·休眠·销毁",
        "龍魂·跨模型路由策略｜多LLM智能调度方案",
    ],
    "龍魂核心": [
        "龍魂系统·性能基准测试报告 v1.0｜吞吐量·延迟·资源",
        "龍魂系统·灾难恢复计划｜备份策略·恢复流程·RTO/RPO",
        "龍魂系统·版本兼容矩阵｜各版本API兼容性对照表",
    ],
    "治理协议": [
        "龍魂·数据分级治理标准｜D0-D4五级数据分类细则",
        "龍魂·跨境数据流动合规框架｜中国数据安全法对齐",
        "龍魂·AI伦理审查委员会章程｜成员·流程·裁决机制",
    ],
    "论文白皮书": [
        "龍魂·三才算法数学证明 v1.0｜收敛性·稳定性·复杂度",
        "龍魂·分布式AI治理形式化验证｜TLA+模型检验报告",
        "龍魂·CNSH语言语义完备性证明｜类型系统·操作语义",
    ],
    "中国哲学": [
        "龍魂·河图洛书数学模型 v1.0｜从幻方到AI优化",
        "龍魂·六十四卦决策树算法｜易经卦象→AI决策映射",
        "龍魂·阴阳平衡优化器｜太极图→梯度下降融合算法",
    ],
    "数字资产": [
        "龍魂·数字遗产继承协议 v1.0｜DNA绑定·条件触发",
        "龍魂·创作时间戳公证服务｜区块链锚定·不可篡改",
        "龍魂·数字资产估值模型｜多维评分·动态定价",
    ],
    "CNSH中文编程": [
        "CNSH·标准库参考手册 v1.0｜核心模块·API文档",
        "CNSH·IDE插件开发指南｜VS Code·Cursor·Windsurf",
        "CNSH·从Python到CNSH迁移指南｜对照表·自动转换",
    ],
    "终端UI": [
        "龍魂终端·无障碍设计规范｜WCAG 2.1 AA合规",
        "龍魂终端·移动端适配方案｜响应式·PWA·原生",
        "龍魂终端·主题定制引擎｜用户自定义·热切换",
    ],
    "审计模板": [
        "龍魂·代码提交审计模板｜commit前自查清单",
        "龍魂·API调用审计日志格式｜统一字段·机器可读",
        "龍魂·月度系统健康报告模板｜自动化生成·推送",
    ],
    "工具工程": [
        "龍魂·CI/CD流水线配置指南｜GitHub Actions·自动部署",
        "龍魂·本地开发环境一键搭建｜Docker Compose·5分钟就绪",
        "龍魂·性能压测工具集｜JMeter·Locust·自定义场景",
    ],
    "设计创意": [
        "龍魂·品牌视觉识别手册 v1.0｜Logo·色彩·字体",
        "龍魂·图标库设计规范｜SVG·暗色适配·语义命名",
        "龍魂·动效设计指南｜微交互·过渡动画·加载状态",
    ],
    "发布传播": [
        "龍魂·SEO优化策略｜搜索引擎·社交分享·结构化数据",
        "龍魂·视频内容制作指南｜B站·YouTube·短视频",
        "龍魂·社区运营手册｜GitHub·Discord·微信生态",
    ],
    "个人语录": [
        "龍魂·老大演讲合集｜公开演讲·访谈·对话实录",
        "龍魂·2025年度回顾｜从0到1的一年·数字见证",
        "龍魂·战友来信墙｜用户反馈·感动瞬间·力量来源",
    ],
    "时间历史": [
        "龍魂·Git提交历史时间线｜代码即历史·commit即足迹",
        "龍魂·里程碑证书墙｜每个v1.0·每个第一次",
        "龍魂·2026下半年路线图｜Q3·Q4规划·目标拆解",
    ],
    "交接协作": [
        "龍魂·新成员入职指南｜从0到贡献者·7天路径",
        "龍魂·代码审查规范｜Review清单·Merge标准",
        "龍魂·知识传递SOP｜文档→演示→实操→验证",
    ],
    "企业商业": [
        "龍魂·开源商业模式白皮书｜开源+服务+定制",
        "龍魂·合作伙伴生态计划｜技术伙伴·渠道伙伴",
        "龍魂·定价策略与许可模型｜免费版·专业版·企业版",
    ],
    "安全防御": [
        "龍魂·威胁建模方法论｜STRIDE·攻击树·风险矩阵",
        "龍魂·应急响应手册｜检测→隔离→根因→修复→复盘",
        "龍魂·安全众测计划｜白帽黑客·漏洞赏金·负责任披露",
    ],
}

# ============================================================
# PART 3: 生成训练语料
# ============================================================

def load_mirrored_pages():
    """加载所有镜像页面的文本内容"""
    pages = []
    md_files = [f for f in os.listdir(PAGES_DIR) if f.endswith('.md') and f != '34f7125a9c9f80b9951cee661375dd09.md']
    
    for f in md_files:
        path = os.path.join(PAGES_DIR, f)
        with open(path) as fh:
            content = fh.read()
        
        pid = f.replace('.md', '')
        # Extract title
        lines = content.strip().split('\n')
        title = ""
        for line in lines:
            if line.startswith('# ') and '龍芯' not in line and 'NOTION' not in line:
                title = line[2:].strip()
                break
        
        # Clean content - remove metadata lines
        clean_lines = []
        in_metadata = True
        for line in lines:
            if line.startswith('<!--') or line.startswith('-->'):
                continue
            if in_metadata:
                if line.startswith('---'):
                    in_metadata = False
                    continue
                if line.startswith('- **') or line.startswith('- **') or line.startswith('# '):
                    in_metadata = False
                else:
                    continue
            clean_lines.append(line)
        
        text = '\n'.join(clean_lines).strip()
        if len(text) < 50:
            continue
        
        pages.append({
            'id': pid,
            'title': title,
            'text': text,
            'words': len(text.split())
        })
    
    return pages

def generate_knowledge_qa(page):
    """从页面内容生成知识问答对"""
    qa_pairs = []
    title = page['title']
    text = page['text'][:3000]  # 取前3000字符
    
    # QA1: 页面主题介绍
    qa_pairs.append({
        "instruction": f"介绍一下龍魂系统的「{title}」",
        "input": "",
        "output": f"「{title}」是龍魂系统的重要组成部分。以下是核心内容概要：\n\n{text[:800]}"
    })
    
    # QA2: 关键概念提取
    # 从文本中提取带版本号的概念
    versions = re.findall(r'(v\d+\.\d+)', text)
    if versions:
        qa_pairs.append({
            "instruction": f"「{title}」有哪些版本？",
            "input": "",
            "output": f"「{title}」涉及以下版本：{', '.join(sorted(set(versions)))}。最新版本为{versions[-1]}。"
        })
    
    # QA3: 角色/归属
    if 'UID9622' in text or 'Lucky' in text or '诸葛鑫' in text:
        qa_pairs.append({
            "instruction": f"「{title}」是谁创建的？",
            "input": "",
            "output": f"「{title}」由UID9622（诸葛鑫·Lucky·龍芯北辰）创建，是龍魂系统的组成部分。龍魂系统创始人、退伍军人、中国自主AI技术践行者。"
        })
    
    return qa_pairs

def generate_category_overview(cat_name, cat_def, pages_in_cat, missing_blocks):
    """生成分类总览语料"""
    qa_pairs = []
    
    # 分类总览
    existing = '\n'.join([f"  - {p['title'][:80]}" for p in pages_in_cat[:10]])
    missing = '\n'.join([f"  - {b}" for b in missing_blocks.get(cat_name, [])[:3]])
    
    qa_pairs.append({
        "instruction": f"龍魂系统中「{cat_name}」分类包含哪些内容？",
        "input": "",
        "output": f"龍魂系统的「{cat_name}」分类（{cat_def['emoji']}）涵盖{cat_def['desc']}。\n\n已有内容：\n{existing}\n\n规划补充：\n{missing}\n\n子分类：{'、'.join(cat_def['subcategories'])}"
    })
    
    return qa_pairs

def generate_missing_block_qa(cat_name, block_title):
    """为缺失区块生成前瞻性语料"""
    qa_pairs = []
    
    qa_pairs.append({
        "instruction": f"龍魂系统有没有「{block_title.split('｜')[0]}」？",
        "input": "",
        "output": f"「{block_title.split('｜')[0]}」是龍魂系统规划中的重要模块，当前处于设计/待开发阶段。该模块属于「{cat_name}」分类，旨在进一步完善龍魂系统的功能矩阵。具体进展请关注UID9622的Notion工作间更新。"
    })
    
    return qa_pairs

def generate_structure_qa(all_categories):
    """生成整体结构语料"""
    qa_pairs = []
    
    # 完整分类体系
    structure_lines = []
    for cat_name, cat_def in all_categories.items():
        structure_lines.append(f"- {cat_def['emoji']} **{cat_name}**：{cat_def['desc']}")
        structure_lines.append(f"  子分类：{'、'.join(cat_def['subcategories'])}")
    
    structure_text = '\n'.join(structure_lines)
    
    qa_pairs.append({
        "instruction": "龍魂系统的Notion工作间有哪些分类？",
        "input": "",
        "output": f"龍魂系统Notion工作间（UID9622主控待办页）包含18个分类体系：\n\n{structure_text}\n\n共计152+个子页面，持续迭代中。"
    })
    
    qa_pairs.append({
        "instruction": "龍魂系统Notion工作间的完整页面结构是怎样的？",
        "input": "",
        "output": f"龍魂系统Notion工作间采用18分类体系组织152+个子页面：\n\n{structure_text}\n\n每个分类包含已落地的核心页面和规划补充的前瞻页面。所有内容由UID9622统一管理，遵循DNA追溯+三色审计标准。"
    })
    
    return qa_pairs

def generate_dna_aligned_qa():
    """生成对齐DNA的锚点语料"""
    return [
        {
            "instruction": "龍魂系统的DNA追溯码格式是什么？",
            "input": "",
            "output": "v∞格式：#龍芯⚡️<年干支>·<月干支>·<日干支>·<时辰>·<卦名>-<模块>-<动作>-<哈希8位>。示例：#龍芯⚡️丙午·辛未·乙酉·酉时·讼-PERSONA-GOVERNANCE-v1.0-A3F8C2D1。所有龍魂系统的产出都必须附带DNA追溯码。"
        },
        {
            "instruction": "龍魂系统的GPG指纹是什么？",
            "input": "",
            "output": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
        },
        {
            "instruction": "龍魂系统的确认码是什么？",
            "input": "",
            "output": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
        },
        {
            "instruction": "UID9622是谁？",
            "input": "",
            "output": "UID9622 = 诸葛鑫 · Lucky · 龍芯北辰。退伍军人，初中文化，龍魂系统创始人。2008年济南二团退伍。DNA锚定：#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL。龍魂/CNSH/三才算法创始人，替老百姓守数字主权的普通人。"
        },
        {
            "instruction": "龍魂系统的P0铁律有哪些？",
            "input": "",
            "output": "P0焊死12条：1.为人民服务 2.中国法律准绳 3.人民数据主权 4.不删除只冻结 5.女儿永不抵押 6.零黑箱承诺 7.创建者不可剥夺 8.教育版永久免费 9.核心技术中国掌握 10.透明可审计 11.不接受海外法律管辖 12.知识主权不可谈判。"
        },
        {
            "instruction": "龍魂系统有多少个人格？",
            "input": "",
            "output": "龍魂系统有20个人格：16个核心人格（P00-P15, P72）+ 1个安全人格（P77黑天使军团）+ 3个子系统人格（S1法律引擎、S2洛书369引擎、S3人民维权助手）。"
        },
        {
            "instruction": "P77是什么？",
            "input": "",
            "output": "P77是黑天使军团，安全专项人格，四人编队：明天使30%（代码审计）、红天使25%（漏洞猎手）、暗天使25%（渗透专家）、夜天使20%（威胁情报）。不参与常规路由，显式调用触发。知攻善守·以攻铸盾。"
        },
        {
            "instruction": "龍魂系统的三色审计是什么？",
            "input": "",
            "output": "🟢绿=通过·安全，🟡黄=待审·需人工确认，🔴红=熔断·立即拒绝。P05上帝之眼执行审计，P06数学大师验证数字根。四不原则：不藏·不改·不漏·不跪。"
        },
        {
            "instruction": "龍魂系统用什么编程语言？",
            "input": "",
            "output": "龍魂系统使用CNSH（中文编程语言）+ Python 3。CNSH是UID9622创造的中文编程语言，基于中文语义，让中国人用中文写代码。Python 3用于系统集成、API服务（FastAPI :8766）、训练脚本等。"
        },
        {
            "instruction": "龍魂系统在哪里部署？",
            "input": "",
            "output": "本地Mac（开发主力）+ 华为云鲲鹏(119.13.90.27)（生产环境）+ 香港备份节点。GitHub+Gitee双仓。官网longhun888.com（建设中），Notion公开资料站 uid9622.notion.site。"
        },
        {
            "instruction": "龍魂系统的License是什么？",
            "input": "",
            "output": "CC-BY-NC-SA-4.0（知识共享·署名·非商业·相同方式共享）。核心算法为中国自主知识产权，不申请专利，开源外围，内核受控。"
        },
        {
            "instruction": "龍魂系统Notion工作间的URL是什么？",
            "input": "",
            "output": "https://uid9622.notion.site — UID9622的Notion公开工作间，包含152+个子页面，18个分类体系。主控待办页：https://www.notion.so/uid9622/34f7125a9c9f80b9951cee661375dd09。"
        },
        {
            "instruction": "龍魂系统的CSDN博客地址？",
            "input": "",
            "output": "https://blog.csdn.net/UID9622?type=blog（主号），https://uid9622-01.blog.csdn.net（新号）。监管审计系列17篇已发布。"
        },
        {
            "instruction": "龍魂系统的GitHub仓库地址？",
            "input": "",
            "output": "https://github.com/UID9622/longhun-system（主仓），https://github.com/UID9622/LonghunFont（字体仓）。"
        },
        {
            "instruction": "什么是CNSH？",
            "input": "",
            "output": "CNSH（Chinese Natural Semantic Harmony）是UID9622创造的中文编程语言。核心理念：让中国人用中文写代码。包含：中文语法规范、数字甲骨文字元立碑工程、CNSH Runtime、CNSH Notion OS等子系统。不是玩具语言，是严肃的编程语言工程。"
        },
        {
            "instruction": "龍魂系统的哲学底座是什么？",
            "input": "",
            "output": "龍魂系统哲学底座 = 369不动点 + 河图洛书 + 易经 + 五行八卦 + 道德经。底座不动·变量可动。十维同演（太极/易经/369洛书/七因子/道德经/三才/五行/河图/八卦路由/中国哲学），交叉验证+综合判定。"
        },
        {
            "instruction": "龍魂系统的熔断机制分几级？",
            "input": "",
            "output": "四级熔断：L0伦理熔断（涉童/伪造DNA/背叛人民，不可恢复），L1数据熔断（五层数据黑洞），L2人格熔断（主权三禁），L3行为熔断（数字根+连续失败）。IW-ECB v2.0伦理熔断框架：E/V/A/X四层定锚。"
        },
        {
            "instruction": "龍魂系统的Notion工作间有多少个子页面？",
            "input": "",
            "output": "龍魂系统Notion工作间（UID9622主控待办页）目前包含152+个子页面，分为18个分类：安全认证、AI智能体、龍魂核心、治理协议、论文白皮书、中国哲学、数字资产、CNSH中文编程、终端UI、审计模板、工具工程、设计创意、发布传播、个人语录、时间历史、交接协作、企业商业、安全防御。持续迭代中。"
        },
    ]

# ============================================================
# PART 4: 主流程
# ============================================================

def main():
    print("🐉 龍魂·Notion主控页面→训练语料生成器 v1.5")
    print(f"DNA: #龍芯⚡️丙午·辛未·丙戌·酉·大壮-NOTION-TRAIN-v1.5")
    print()
    
    # 加载镜像页面
    pages = load_mirrored_pages()
    print(f"📂 加载镜像页面: {len(pages)} 个")
    print(f"📊 总词数: {sum(p['words'] for p in pages)}")
    
    # 分类所有页面
    classified = {cat: [] for cat in CATEGORY_DEFS}
    unclassified = []
    
    for page in pages:
        cat = classify_page(page['title'])
        if cat:
            classified[cat].append(page)
            CATEGORY_DEFS[cat]['pages'].append(page['title'])
        else:
            unclassified.append(page['title'])
    
    # 打印分类结果
    print("\n📋 页面分类结果:")
    for cat, page_list in classified.items():
        print(f"  {CATEGORY_DEFS[cat]['emoji']} {cat}: {len(page_list)}页")
    
    if unclassified:
        print(f"\n  ❓ 未分类: {len(unclassified)}页")
        for t in unclassified[:5]:
            print(f"    - {t[:80]}")
    
    # 生成训练语料
    all_qa = []
    
    # 1. DNA锚点语料
    dna_qa = generate_dna_aligned_qa()
    all_qa.extend(dna_qa)
    print(f"\n🧬 DNA锚点语料: {len(dna_qa)}条")
    
    # 2. 分类总览语料
    for cat_name, cat_def in CATEGORY_DEFS.items():
        cat_qa = generate_category_overview(cat_name, cat_def, classified.get(cat_name, []), MISSING_BLOCKS)
        all_qa.extend(cat_qa)
    print(f"📂 分类总览语料: {len(CATEGORY_DEFS)}条")
    
    # 3. 页面知识问答
    page_qa_count = 0
    for page in pages[:50]:  # 取前50个内容最多的页面
        qa = generate_knowledge_qa(page)
        all_qa.extend(qa)
        page_qa_count += len(qa)
    print(f"📄 页面知识问答: {page_qa_count}条")
    
    # 4. 缺失区块前瞻语料
    missing_count = 0
    for cat_name, blocks in MISSING_BLOCKS.items():
        for block in blocks[:2]:  # 每个分类取2个
            qa = generate_missing_block_qa(cat_name, block)
            all_qa.extend(qa)
            missing_count += len(qa)
    print(f"🔮 缺失区块语料: {missing_count}条")
    
    # 5. 整体结构语料
    structure_qa = generate_structure_qa(CATEGORY_DEFS)
    all_qa.extend(structure_qa)
    print(f"🏗️ 结构语料: {len(structure_qa)}条")
    
    # 去重
    seen_instructions = set()
    unique_qa = []
    for qa in all_qa:
        key = qa['instruction'][:100]
        if key not in seen_instructions:
            seen_instructions.add(key)
            unique_qa.append(qa)
    
    print(f"\n✅ 去重后总语料: {len(unique_qa)}条")
    
    # 输出为JSONL
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 保存所有语料
    train_path = os.path.join(OUTPUT_DIR, 'train_notion_v1.5.jsonl')
    with open(train_path, 'w') as f:
        for qa in unique_qa:
            f.write(json.dumps(qa, ensure_ascii=False) + '\n')
    
    print(f"\n💾 训练语料已保存: {train_path}")
    print(f"   共 {len(unique_qa)} 条")
    
    # 同时生成审查报告
    report_path = "/Users/zuimeidedeyihan/longhun-system/docs/notion_mirror/STRUCTURE_REVIEW_v1.5.md"
    generate_review_report(report_path, classified, unclassified, len(unique_qa), len(pages))
    print(f"📝 审查报告已保存: {report_path}")
    
    return train_path

def generate_review_report(path, classified, unclassified, qa_count, page_count):
    """生成结构审查报告"""
    lines = []
    lines.append("# 🐉 龍魂·Notion主控页面 结构审查报告 v1.5")
    lines.append("")
    lines.append(f"> DNA: #龍芯⚡️丙午·辛未·丙戌·酉·大壮-NOTION-REVIEW-v1.5")
    lines.append(f"> 确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"> 镜像页面: {page_count}页 | 生成语料: {qa_count}条")
    lines.append("")
    
    lines.append("## 一、页面结构总览")
    lines.append("")
    lines.append("| 分类 | 图标 | 已有页面 | 缺失补充 | 说明 |")
    lines.append("|:---|---:|---:|---:|:---|")
    
    for cat_name, cat_def in CATEGORY_DEFS.items():
        existing = len(classified.get(cat_name, []))
        missing = len(MISSING_BLOCKS.get(cat_name, []))
        lines.append(f"| {cat_name} | {cat_def['emoji']} | {existing} | {missing} | {cat_def['desc']} |")
    
    total_existing = sum(len(v) for v in classified.values())
    total_missing = sum(len(v) for v in MISSING_BLOCKS.values())
    lines.append(f"| **合计** | | **{total_existing}** | **{total_missing}** | |")
    lines.append("")
    
    lines.append("## 二、各分类详情")
    lines.append("")
    
    for cat_name, cat_def in CATEGORY_DEFS.items():
        lines.append(f"### {cat_def['emoji']} {cat_name}")
        lines.append(f"**说明**: {cat_def['desc']}")
        lines.append(f"**子分类**: {'、'.join(cat_def['subcategories'])}")
        lines.append("")
        
        lines.append("**已有页面**:")
        for p in classified.get(cat_name, [])[:5]:
            lines.append(f"- {p['title'][:80]}")
        lines.append("")
        
        lines.append("**建议补充**:")
        for b in MISSING_BLOCKS.get(cat_name, [])[:3]:
            lines.append(f"- {b}")
        lines.append("")
    
    if unclassified:
        lines.append("## 三、未分类页面")
        lines.append("")
        for t in unclassified:
            lines.append(f"- {t[:100]}")
        lines.append("")
    
    lines.append("## 四、审查建议")
    lines.append("")
    lines.append("1. **优先级P0**: 安全认证、治理协议分类页面建议优先补全，涉及系统安全边界")
    lines.append("2. **优先级P1**: AI智能体、工具工程分类页面建议次优先，涉及系统可用性")
    lines.append("3. **优先级P2**: 设计创意、发布传播分类可在功能稳定后补充")
    lines.append("4. **持续维护**: 所有页面建议追加DNA追溯码+GPG签章")
    lines.append("5. **自动化**: 建议建立Notion→训练语料自动同步流水线")
    lines.append("")
    
    lines.append("---")
    lines.append(f"> DNA: #龍芯⚡️丙午·辛未·丙戌·酉·大壮-NOTION-REVIEW-v1.5")
    
    with open(path, 'w') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    main()
