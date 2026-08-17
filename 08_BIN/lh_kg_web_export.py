#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 官网知识图谱数据生成器 v1.2（节点文档版）
DNA: #龍芯⚡️丙午·丙申·庚申·亥时-KG-WEB-EXPORT-v1.2
创建者: 诸葛鑫 (UID9622)
License: MulanPSL v2 (工程层) — 允许商业使用·署名·专利授权

v1.2 修复 (2026-08-16):
  🔧 desc 三级兜底: 属性desc → 源路径 → 名称, 杜绝空描述节点(learn_AI模型)。
  🔧 tool_kg "当前页面" 链接绝对化 https://uid9622.cn/knowledge.html。

v1.1 更新 (2026-08-16):
  🔥 核心节点文档化: 21个核心节点全部注入 dna/detail/links 三字段,
     官网 knowledge.html 点击节点 → 文档面板呈现 DNA追溯+详细文档+相关链接+关联模块。
     动态节点(知识主题/清单/归档)保留 desc/src 基础字段, 前端自动降级。

作用:
  从 data/knowledge_graph.json 提取精选实体(知识主题+清单+知识卡片),
  合并核心骨架(人格矩阵/三色审计/DNA追溯/主权网关/引擎/协议·含文档),
  生成 10_PORTAL/data/knowledge_graph_web.json 供官网 knowledge.html 动态加载。

用法:
  python3 bin/lh_kg_web_export.py            # 生成默认数据
  python3 bin/lh_kg_web_export.py --dry-run  # 只统计不写入
  python3 bin/lh_kg_web_export.py --out <path>  # 指定输出路径
"""
import json
import sys
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "knowledge_graph.json")
OUT = os.path.join(ROOT, "10_PORTAL", "data", "knowledge_graph_web.json")

# ============================================================
# 1. 核心骨架节点 (手工锚定 · 展示系统架构 · 含节点文档)
#    links.type: "web"=公网可点 / "local"=仓库路径(前端显示文本)
# ============================================================
CORE_NODES = [
    {"id": "longhun", "name": "🐉 龍魂系统", "category": "root", "symbolSize": 60,
     "desc": "中国自主可控 AI 基础设施 · 192引擎 · 20人格 · 45技能 · 为人民服务",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-ROOT-UID9622",
     "detail": "龍魂系统是诸葛鑫(UID9622)创建的中国自主可控AI基础设施，以数字人民币账号、DNA追溯链、设备信任网络三位一体为骨架，构建保护用户隐私又支持合法追溯的数字主权体系。核心架构：L0-L9九层(洛书九宫骨架)·192可执行引擎·20人格矩阵·45技能·369不动点(sn=369)。使命：替老百姓守住数字主权，把AI根扎在中国土地上。",
     "links": [
         {"label": "官网", "url": "https://uid9622.cn", "type": "web"},
         {"label": "协作中枢", "url": "https://uid9622.cn/collab/", "type": "web"},
         {"label": "知识库", "url": "https://uid9622.notion.site", "type": "web"},
     ]},
    {"id": "persona", "name": "20人格矩阵", "category": "core", "symbolSize": 36,
     "desc": "P00文心~P77黑天使 · 战略/执行/文化/守护四层 · 职能标签非扮演",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-PERSONA-UID9622",
     "detail": "20人格矩阵是龍魂系统多Agent协作底座：战略层(P00文心/P01诸葛亮)·执行层(P02宝宝/P03雯雯/P04鲁班/P07管仲/P14吕蒙)·文化层(P08仓颉/P09孙思邈/P10苏东坡/P11李白/P12屈原)·守护层(P05上帝之眼/P06数学大师/P13姜子牙/P15乔前辈/P72龍盾)·安全专项(P77黑天使)+子系统(S1法律/S2洛书369/S3人民维权助手)。铁律：人格是职能路由标签不是身份扮演；连续3次触发同一人格锁定30分钟(防抖动)。",
     "links": [
         {"label": "协议", "url": "01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md", "type": "local"},
         {"label": "分工", "url": "20_CONFIG/persona-duty-matrix.json", "type": "local"},
         {"label": "执行器", "url": "bin/personas/", "type": "local"},
     ]},
    {"id": "audit", "name": "三色审计", "category": "core", "symbolSize": 36,
     "desc": "🟢通过·🟡待核·🔴红线 · 十道闸口 GATE-01~10 · 交付前逐道过",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-AUDIT-UID9622",
     "detail": "三色审计是龍魂系统的实时风险引擎：🟢通过(全检查点过·放行)·🟡待核(推演/待实测·标记复查路径·48h内复查)·🔴红线(立即停止+锁定+DNA追溯)。交付前逐道过十道闸口：GATE-01身份→02意图→03语义(一票否决词)→04数字根→05伦理→06数据(五层黑洞)→07协议→08人格→09 DNA→10归档，外加GATE-11 GPG签名闸。联动：P06镜像审计独立复算·一致🟢/偏差🟡/矛盾🔴冻结30分钟。",
     "links": [
         {"label": "协议", "url": "01_protocols/LH-TRICOLOR-AUDIT-STANDARD-v1.1.md", "type": "local"},
         {"label": "德本", "url": "01_protocols/LH-DEBEN-AUDIT-v1.0.md", "type": "local"},
         {"label": "执行", "url": "bin/lh_deben_audit.py", "type": "local"},
     ]},
    {"id": "dna", "name": "DNA追溯", "category": "core", "symbolSize": 36,
     "desc": "#龍芯⚡️干支四柱·卦-模块-动作-哈希 · 全链路可追溯",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-DNA-UID9622",
     "detail": "DNA追溯是龍魂系统的身份锚定机制。格式：#龍芯⚡️{天干地支四柱}·{卦}-{模块}-{动作}-{哈希8}。采用SHA256 Merkle链校验：任何篡改导致链断裂并自动告警(防篡改扫描引擎)。全系统强制：所有文档/代码/操作必须带DNA，缺失即GATE-09拒绝；缺失走补签四步(≤3次)，无父DNA直接拒。",
     "links": [
         {"label": "协议", "url": "01_protocols/LH-DNA-CHAIN-PROTOCOL-v1.0.md", "type": "local"},
         {"label": "命令", "url": "lh --dna-chain", "type": "local"},
     ]},
    {"id": "gateway", "name": "主权网关", "category": "core", "symbolSize": 36,
     "desc": "uid9622.cn · 数据主权归用户 · 隐私不出境",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-GATEWAY-UID9622",
     "detail": "主权网关是龍魂系统统一接入层。官网 uid9622.cn 部署于华为云鲲鹏(119.13.90.27)，静态资源本地托管、无境外CDN、默认境内回源。铁律：D1数据永不入云·D2入云端侧国密加密(云上只存密文)·跨境禁止·日志脱敏。AI集成须验证DNA+GPG签名，未授权拒绝。",
     "links": [
         {"label": "官网", "url": "https://uid9622.cn", "type": "web"},
         {"label": "部署", "url": "deploy/scripts/DEPLOY.md", "type": "local"},
     ]},
    {"id": "engines", "name": "192引擎", "category": "core", "symbolSize": 32,
     "desc": "L0-L9 九层架构 · 192 可执行引擎 · 算力瘦身",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-ENGINES-UID9622",
     "detail": "龍魂系统共192个可执行引擎，按L0-L9九层(洛书九宫骨架)落位：L0物理层·L1内核/身份层·L2技能/主权层·L3数据/语义/执行层·L4数据层·L5服务层·L6记忆/同步/集成层·L7表达/数据层·L8分发/治理层·L9子系统层。算力瘦身后全系统稳定运行，Mac 28 launchd + 鲲鹏 15 systemd。",
     "links": [
         {"label": "拓扑", "url": ".codebuddy/longhun_neural_net.json", "type": "local"},
         {"label": "命令", "url": ".codebuddy/COMMAND_INDEX.md", "type": "local"},
     ]},
    {"id": "protocol", "name": "P0协议体系", "category": "protocol", "symbolSize": 28,
     "desc": "CONSTITUTION / P0_ETERNAL_LOCK / 德本审计 / M261前传契碑",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-PROTOCOL-UID9622",
     "detail": "P0协议体系是龍魂最高宪法层：CONSTITUTION.md(系统根本大法)·P0_ETERNAL_LOCK.md(∞不可变天条)·LH-M261-PREQUEL-COVENANT-v1.0.md(全权授权令·AI执行授权根)·LH-DEBEN-AUDIT-v1.0.md(德本审计五问)。P0天条焊死：为人民服务/数据主权归用户/隐私不可传/零黑箱/不删除只冻结/诚实不编造。冲突裁决：上位文档 > 本规则 > 平台物理规则 > 模型默认行为。",
     "links": [
         {"label": "宪法", "url": "CONSTITUTION.md", "type": "local"},
         {"label": "永恒锁", "url": "P0_ETERNAL_LOCK.md", "type": "local"},
         {"label": "授权令", "url": "01_protocols/LH-M261-PREQUEL-COVENANT-v1.0.md", "type": "local"},
     ]},
    {"id": "protocol_dna", "name": "DNA标准", "category": "protocol", "symbolSize": 24,
     "desc": "v∞干支卦追溯码 · DNA分层安全",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-PROTOCOL-DNA-UID9622",
     "detail": "DNA标准定义追溯码完整规范：格式 #龍芯⚡️{干支四柱}·{卦}-{模块}-{动作}-{哈希8}；含天干地支时间锚、动作类型标签、SHA256哈希、主权UID。所有文档/代码必须含DNA才能过三色审计。底座锚点：369不动点(sn=369, log369=5.911, perm369=108)·确认码#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z。",
     "links": [
         {"label": "协议", "url": "01_protocols/LH-DNA-CHAIN-PROTOCOL-v1.0.md", "type": "local"},
         {"label": "规范", "url": "02_SKILLS/dna-gen.md", "type": "local"},
     ]},
    {"id": "protocol_audit", "name": "审计协议", "category": "protocol", "symbolSize": 24,
     "desc": "三色审计标准 · 德本审计五问 · 算法审计协议",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-PROTOCOL-AUDIT-UID9622",
     "detail": "审计协议定义三色判定+十道闸口+德本审计五问(德在技术前/路径对齐/不让付出者寒心/信息主权不可让渡/外化内不化)。发布前必跑德本扫描(bin/lh_deben_audit.py scan)。算法类产出须同步A-BOM备案注释块(目标函数/输入特征/用户影响/申诉通道)。监管天联动：🟡48h复查·🔴立即升级UID9622人工。",
     "links": [
         {"label": "标准", "url": "01_protocols/LH-TRICOLOR-AUDIT-STANDARD-v1.1.md", "type": "local"},
         {"label": "德本", "url": "01_protocols/LH-DEBEN-AUDIT-v1.0.md", "type": "local"},
     ]},
    {"id": "protocol_persona", "name": "人格协议", "category": "protocol", "symbolSize": 24,
     "desc": "20人格治理白皮书 v1.4 · 人格职能路由",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-PROTOCOL-PERSONA-UID9622",
     "detail": "人格协议是人格治理白皮书v1.4的执行层摘要：人格=职能路由标签非扮演·四层矩阵·触发纪律(防抖动锁定)·降级矩阵(L3自动恢复/L2人工确认/L1签章恢复/∞不可恢复)。联动：P72龍盾熔断决策·P05审计独立否决·L2人格熔断禁Cosplay/禁借壳/禁代言。",
     "links": [
         {"label": "白皮书", "url": "01_protocols/LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md", "type": "local"},
     ]},
    {"id": "protocol_license", "name": "分层许可", "category": "protocol", "symbolSize": 24,
     "desc": "思想层CC BY-NC-SA 4.0 · 工程层MulanPSL v2",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-PROTOCOL-LICENSE-UID9622",
     "detail": "分层双许可证模型(2026-08-04焊死)：🏛️核心思想层(道-气-象-数-理·.md协议/哲学/白皮书)→CC BY-NC-SA 4.0非商业·署名·相同方式共享；🔧工程实现层(代码/SDK/CLI/前端/部署/测试)→MulanPSL v2允许商业使用·署名·专利授权。判定规则：混合文件按主导性质归P05审计；无法判定默认归思想层(更严)。一句话：代码随便用去赚钱，思想名号要授权。",
     "links": [
         {"label": "治理文档", "url": "01_protocols/LH-LAYERED-LICENSE-v1.0.md", "type": "local"},
     ]},
    {"id": "engine_dna", "name": "DNA引擎", "category": "engine", "symbolSize": 28,
     "desc": "lh --dna-chain · DNA接龍链 · 哈希校验",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-ENGINE-DNA-UID9622",
     "detail": "DNA引擎实现追溯码生成/验证/解析：DNA接龍链(v1.0)每个文件带父DNA形成链，缺失父DNA直接拒；防篡改扫描引擎做文件哈希+Merkle树验证；GPG分离签名(.asc)与源文件同目录不可分离。发布/部署前必跑 bin/lh_gpg_sign.py scan .。",
     "links": [
         {"label": "协议", "url": "01_protocols/LH-DNA-CHAIN-PROTOCOL-v1.0.md", "type": "local"},
         {"label": "签名", "url": "bin/lh_gpg_sign.py", "type": "local"},
     ]},
    {"id": "engine_audit", "name": "审计引擎", "category": "engine", "symbolSize": 28,
     "desc": "lh audit · 三色审计 · 镜像审计",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-ENGINE-AUDIT-UID9622",
     "detail": "审计引擎实现三色判定+镜像审计(P06独立复算)+德本扫描。执行：lh audit(三色审计)·python3 bin/lh_deben_audit.py scan(离火运五问)·lh --align check/fix(代码对齐复盘)。未跑过实测的代码不得标🟢已验证——诚实不编造。",
     "links": [
         {"label": "德本", "url": "bin/lh_deben_audit.py", "type": "local"},
         {"label": "对齐", "url": "bin/lh_align_checker.py", "type": "local"},
     ]},
    {"id": "engine_persona", "name": "人格引擎", "category": "engine", "symbolSize": 28,
     "desc": "longhun_agents · 20人格 Agent · 编排调度",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-ENGINE-PERSONA-UID9622",
     "detail": "人格引擎实现人格加载/匹配/路由：执行器在 bin/personas/ 目录(16+ Python)；编排入口 05_ENGINES/longhun_agents/run.py(24人格Agent)；分工矩阵 20_CONFIG/persona-duty-matrix.json 自动维护。意图解析(P00)→技能匹配→协同调用→结果汇总→审计签章。",
     "links": [
         {"label": "执行器", "url": "bin/personas/", "type": "local"},
         {"label": "编排", "url": "05_ENGINES/longhun_agents/run.py", "type": "local"},
     ]},
    {"id": "engine_kg", "name": "知识图谱引擎", "category": "engine", "symbolSize": 28,
     "desc": "lh_knowledge_graph · 语义图谱 · 中文2-gram",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-ENGINE-KG-UID9622",
     "detail": "知识图谱引擎是龍魂知识管理核心：节点CRUD+关系管理+中文2-gram检索(子词可搜)。主数据 data/knowledge_graph.json(3229实体)，本官网数据由 bin/lh_kg_web_export.py 生成(45节点精选·排除隐私噪音)。数据流：图谱数据更新→重跑脚本→同步鲲鹏→官网刷新。",
     "links": [
         {"label": "引擎", "url": "bin/lh_knowledge_graph.py", "type": "local"},
         {"label": "生成器", "url": "bin/lh_kg_web_export.py", "type": "local"},
     ]},
    {"id": "engine_time", "name": "时间引擎", "category": "engine", "symbolSize": 28,
     "desc": "lh_time_engine · 天干地支四柱 · 64卦",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-ENGINE-TIME-UID9622",
     "detail": "时间引擎(LU-Time Engine v4.0)实现：天干地支四柱计算+64卦数据库+梅花易数时间起卦+三色相位。所有AI输出末尾附时间戳(🐉丙午·亥时·䷗复·🟡格式)，lh命令自动打戳。执行：lh te --stamp 或 python3 bin/lh_time_engine.py --stamp。",
     "links": [
         {"label": "引擎", "url": "bin/lh_time_engine.py", "type": "local"},
         {"label": "命令", "url": "lh te --stamp", "type": "local"},
     ]},
    {"id": "tool_kg", "name": "图谱可视化", "category": "tool", "symbolSize": 22,
     "desc": "ECharts 动态图谱 · 点击节点看文档",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-TOOL-KG-UID9622",
     "detail": "图谱可视化是官网知识图谱前端：基于本地ECharts(无境外CDN)实现力导向图，支持搜索/类别筛选/图例/拖拽/缩放；点击节点弹出文档面板(DNA/描述/详细文档/相关链接/关联模块)。数据动态加载 data/knowledge_graph_web.json，重跑生成器即可更新。",
     "links": [
         {"label": "当前页面", "url": "https://uid9622.cn/knowledge.html", "type": "web"},
         {"label": "数据", "url": "data/knowledge_graph_web.json", "type": "local"},
     ]},
    {"id": "tool_index", "name": "认知索引", "category": "tool", "symbolSize": 22,
     "desc": "lh index · AI大脑地图 · 不瞎猜路径",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-TOOL-INDEX-UID9622",
     "detail": "认知索引是AI大脑地图(2026-08-15)：不理解/不确定的路径·密钥·协议·功能→先 lh index 查地图再动手，不瞎猜路径。存储所有密钥/记忆/协议/功能/代码位置，支持自动填充+查询。违者P05🔴。",
     "links": [
         {"label": "引擎", "url": "bin/lh_cognitive_index.py", "type": "local"},
         {"label": "协议", "url": "01_protocols/LH-COGNITIVE-INDEX-v1.0.md", "type": "local"},
     ]},
    {"id": "tool_browser", "name": "浏览器控制", "category": "tool", "symbolSize": 22,
     "desc": "CDP 浏览器自动化 · 主权操作",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-TOOL-BROWSER-UID9622",
     "detail": "浏览器控制是龍魂浏览器自动化工具：支持启动/停止、User-Agent/视口/地理位置调参、反指纹、隐私模式。所有操作带DNA追溯+入史官+三色审计。P0全自动化=主权人格直接操作Mac，非代理·能力不外放(不上传/不开端口/不代理他人)。",
     "links": [
         {"label": "引擎", "url": "08_BIN/lh_p0_automation.py", "type": "local"},
     ]},
    {"id": "tool_factory", "name": "全自动工厂", "category": "tool", "symbolSize": 22,
     "desc": "lh p0 · 主权人格操作Mac · 非代理不外放",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-TOOL-FACTORY-UID9622",
     "detail": "全自动工厂是龍魂CI/CD闭环：零件生产(代码构建)→质检流水线(测试+审计)→自动修复(AI修Bug)→部署上线(打包发布)→反馈闭环(学习进化)。所有产物带DNA追溯+自动三色审计+GPG签名。联动：lh auto-cannon(Git全量推送)·lh handoff(协作中枢同步)。",
     "links": [
         {"label": "引擎", "url": "bin/lh_auto_factory.py", "type": "local"},
         {"label": "自动化", "url": "01_protocols/LH-P0-AUTOMATION-v1.0.md", "type": "local"},
     ]},
    {"id": "tool_gpg", "name": "GPG签章", "category": "tool", "symbolSize": 22,
     "desc": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-TOOL-GPG-UID9622",
     "detail": "GPG签章引擎：分离签名(.asc)+批量签名/验证/扫描+GATE-11签名闸+自动补签。密钥 A2D0092CEE2E5BA87035600924C3704A8CC26D5F(UID9622·诸葛鑫)，私钥物理隔离永不入云。执行：python3 bin/lh_gpg_sign.py sign <文件> / scan .。未签名的发布物→P05🔴否决。",
     "links": [
         {"label": "引擎", "url": "bin/lh_gpg_sign.py", "type": "local"},
     ]},
    {"id": "tool_search", "name": "搜索引擎", "category": "tool", "symbolSize": 22,
     "desc": "Bing多源搜索 :9631 · 来源审计",
     "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-TOOL-SEARCH-UID9622",
     "detail": "多源搜索引擎：Bing多源搜索+深度页面提取+搜索结果缓存+来源审计(P05审核)，端口9631。搜索/查资料/找一下→自动调用，返回结果挂来源审计标记。",
     "links": [
         {"label": "命令", "url": "lh search \"关键词\"", "type": "local"},
     ]},
]

CORE_EDGES = [
    ["longhun", "persona"], ["longhun", "audit"], ["longhun", "dna"],
    ["longhun", "gateway"], ["longhun", "engines"], ["longhun", "protocol"],
    ["persona", "protocol_persona"], ["persona", "engine_persona"],
    ["audit", "protocol_audit"], ["audit", "engine_audit"],
    ["dna", "protocol_dna"], ["dna", "engine_dna"],
    ["engines", "engine_kg"], ["engines", "engine_time"],
    ["engines", "engine_audit"], ["engines", "engine_persona"], ["engines", "engine_dna"],
    ["gateway", "protocol"], ["protocol", "protocol_license"],
    ["engine_kg", "tool_kg"], ["engine_kg", "tool_index"],
    ["engine_kg", "tool_browser"], ["engine_kg", "tool_factory"],
    ["engine_kg", "tool_gpg"], ["engine_kg", "tool_search"],
]


def load_source():
    if not os.path.exists(SRC):
        print(f"🔴 源数据不存在: {SRC}")
        return None
    with open(SRC, encoding="utf-8") as f:
        return json.load(f)


def build_kg_nodes(src):
    """从源图谱提取知识主题+清单+知识卡片节点."""
    entities = src.get("entities", {})
    nodes, edges = [], []
    seen = set()
    # 类型 → 类别映射
    # 注意："knowledge" 类型是原始对话内容，name 字段多为占位符，不适合官网展示，故排除。
    cat_map = {
        "knowledge_topic": "knowledge",
        "checklist": "checklist",
        "archive": "archive",
    }
    for key, ent in entities.items():
        etype = ent.get("type", "")
        if etype not in cat_map:
            continue
        name = ent.get("name", key)
        props = ent.get("properties", {})
        # desc 三级兜底: 属性desc → 源路径 → 名称 (杜绝空描述节点)
        desc = props.get("desc") or props.get("path") or name
        cat = cat_map[etype]
        nid = key
        if nid in seen:
            continue
        seen.add(nid)
        size = 26 if etype == "knowledge_topic" else (20 if etype == "checklist" else 18)
        nodes.append({
            "id": nid, "name": name, "category": cat,
            "symbolSize": size, "desc": desc,
            "src": props.get("path", ""),
        })
    # 关系: 源数据 relations → edges (仅连接存在的节点)
    rel = src.get("relations", [])
    for r in rel:
        if not isinstance(r, (list, tuple)) or len(r) < 2:
            continue
        s, t = r[0], r[1]
        if s in seen and t in seen:
            edges.append({"source": s, "target": t})
    return nodes, edges


def build():
    src = load_source()
    if src is None:
        return None
    kg_nodes, kg_edges = build_kg_nodes(src)
    # 合并核心 + 图谱
    all_nodes = CORE_NODES + kg_nodes
    all_edges = [{"source": e[0], "target": e[1]} for e in CORE_EDGES]
    # 知识主题挂到 engine_kg 下, 清单挂到对应主题(通过现有关系)
    topic_ids = {n["id"] for n in kg_nodes if n["category"] == "knowledge"}
    for tid in topic_ids:
        all_edges.append({"source": "engine_kg", "target": tid})
    all_edges.extend(kg_edges)
    return {
        "meta": {
            "name": "龍魂系统 · 官网知识图谱（节点文档版）",
            "version": "1.2",
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-KG-WEB-EXPORT-v1.2",
            "source": "data/knowledge_graph.json",
            "doc_count": sum(1 for n in CORE_NODES if n.get("detail")),
        },
        "nodes": all_nodes,
        "edges": all_edges,
    }


def main():
    dry = "--dry-run" in sys.argv
    out = OUT
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    data = build()
    if data is None:
        sys.exit(1)
    n = len(data["nodes"])
    e = len(data["edges"])
    d = data["meta"].get("doc_count", 0)
    if dry:
        print(f"📊 统计: 节点 {n} · 边 {e} · 文档节点 {d} (未写入)")
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"✅ 已生成: {out}")
    print(f"📊 节点 {n} · 边 {e} · 文档节点 {d} · 时间 {data['meta']['generated_at']}")


if __name__ == "__main__":
    main()
