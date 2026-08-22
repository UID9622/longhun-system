#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丙申·申时·䷜坎-GUANLAN-TRAIN-DATA-GEN-V1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
观澜浏览器训练数据生成器
DNA: #龍芯⚡️丙午·乙未·丙申·申时·䷜坎-GUANLAN-TRAIN-DATA-GEN-V1.0
生成观澜浏览器知识域的 JSONL 训练数据
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

SYSTEM_PROMPT = "你是龍魂，UID9622（诸葛鑫·Lucky）的个人主权AI。你精通观澜浏览器架构和AI联动协议。"

# ============================================================
# 知识域1: 观澜浏览器核心架构
# ============================================================
ARCHITECTURE_QA = [
    {
        "q": "观澜浏览器是什么？它的四层架构是什么？",
        "a": """观澜浏览器是龍魂系统的自主浏览器产品，定位为外壳+本地网关+AI联动层，而非自研渲染内核。

四层架构（自上而下）：
- L1 观澜外壳：标签/书签/阅读模式/AI侧栏/看板 — 人直接接触的一层
- L2 龍魂网关：127.0.0.1本地代理 — 主权层，负责流量过滤、守护(J0-J4)、主权守门(TS0-TS4)、记账(人机两本账)、显化
- L3 AI联动层：模型路由+断路器+标注器 — Ollama默认/Kimi增强/CodeBuddy编码/小艺语音/预留槽
- L4 内核层：系统WebView或CEF（可换壳层）

核心理念：主权在网关不在像素。渲染交给系统内核，龍魂管流量过滤、AI路由、账本显化、红线熔断。"""
    },
    {
        "q": "观澜浏览器的命名由来和哲学锚点是什么？",
        "a": """观澜之名取自易经观卦䷓（风地观）：「观国之光，利用宾于王」——看遍天下的光，仍以宾主之礼自持：看得多，拿得少；全网尽收眼底，数据不出我门。

哲学锚点还包含道德经第四十七章：「不出户，知天下；不窥牖，见天道。」本地网关+本地模型——不出户而知天下，不是神话，是把该留在屋里的留在屋里，把该看清的看清。

观卦属于离宫·火明。"""
    },
    {
        "q": "观澜浏览器的五条核心原则是什么？",
        "a": """观澜浏览器五条天条（不可违背）：

第1条：主权在网关，不在像素。渲染交给系统内核；龍魂管流量过滤、AI路由、账本显化、红线熔断。

第2条：本地优先，云是增强。默认Ollama本地推理；Kimi云端仅在用户允许且任务需要时启用；云端内容出域前过隐私闸门。

第3条：AI必须自报家门。每段AI输出带标注：哪个引擎、哪个版本、何时生成；不标注的AI输出视同来源不明，默认降信一级🟡。

第4条：浏览器是人工端。人看的归人，爬的归爬：浏览器每一笔阅览记人工账，侦察蚁每一笔抓取记爬虫账——两本账在观澜看板合显。

第5条：红线随身带。未成年守护引擎(J0-J4)、技术主权守门员(TS0-TS4)、反诈直通全部内嵌网关——换浏览器不等于换底线。"""
    },
    {
        "q": "观澜浏览器的渲染内核用什么？为什么不自己写？",
        "a": """观澜浏览器不自研渲染内核。内核选型按平台：

- macOS/iOS：WKWebView（系统级省电+安全更新跟系统走）
- Windows：WebView2（系统自带，免打包体积），备选CEF
- Linux：WebKitGTK（发行版仓库直装），备选CEF
- 鸿蒙：ArkWeb（原生组件，对接小艺零成本）
- 兜底：CEF（Chromium Embedded，全平台一致行为，但打包体积大）

不自研的理由：自研渲染内核是十年工程；主权不在像素里，在流量与模型路由里。抓住流量过滤、AI路由、账本显化、红线熔断这四样，内核换谁都是龍魂浏览器。"""
    },
]

# ============================================================
# 知识域2: AI联动路由
# ============================================================
AI_ROUTING_QA = [
    {
        "q": "观澜浏览器如何联动Ollama、Kimi、CodeBuddy和小艺？",
        "a": """观澜浏览器AI联动层有四个引擎+预留槽：

1. Ollama = 本地默认引擎：离线问答、隐私内容摘要、本地代码补全、账本分析。数据永不出机，断网可用。模型仓版本化（DNA铸链），换模型走修宪公示。

2. CodeBuddy = 编码专用通道：触发方式有地址栏 cb:// 或AI侧栏选"编码模式"或IDE联动按钮。负责代码生成/解释/重构/审查。CloudBase是算力层，敏感代码段端侧脱敏后才允许出域。

3. Kimi = 云端增强引擎：触发场景为长文档解析/深度研究/用户手动切换。有断路器保护：API异常→自动转移Ollama本地推理。出域前过隐私扫描（身份证/银行卡/地址命中即脱敏或拦截🔴）。

4. 小艺 = 华为语音入口：鸿蒙设备经HMS小艺唤起观澜；语音指令→文字→进模型路由。小艺是"嘴和耳"，推理仍走上面三个引擎——入口与引擎分层。"""
    },
    {
        "q": "观澜浏览器的模型路由表是怎样的？",
        "a": """观澜浏览器任务→引擎默认路由：

| 任务类型 | 首选引擎 | 故障转移链 |
|---------|---------|-----------|
| 代码生成/审查 | CodeBuddy | → Ollama本地代码模型 |
| 长文档/研究 | Kimi | → Ollama（脱敏版任务） |
| 隐私内容/离线 | Ollama | 无转移（本地即终点） |
| 通用问答 | Ollama | — |
| 语音入口 | 小艺(入口) | 推理走上面三选 |
| 摘要 | Ollama | — |

路由规则：
- 隐私和离线任务锁定本地（Ollama），永不转出
- 小艺是入口不是推理引擎，语音→文字后按任务类型重路由
- 用户可手动偏好切换引擎
- 断路器：连续3次失败熔断该引擎10分钟，自动转移并记录审计链"""
    },
    {
        "q": "什么是AI Truth Protocol？观澜浏览器如何标注AI输出？",
        "a": """AI Truth Protocol 是观澜浏览器的AI来源标注协议，核心要求：每段AI输出必须自报家门。

标注格式：[引擎名·版本·位置·信级·时间]
例如：[Kimi·v1.0·云·信🟢·14:30]

标注包含五个字段：
- 引擎名：Ollama/Kimi/CodeBuddy/小艺
- 版本：模型版本号
- 位置：本地/云
- 信级：🟢(置信≥0.85)/🟡(0.60≤置信<0.85)/🔴(置信<0.60)
- 时间：生成时间

铁律：不标注的AI输出视同来源不明，默认降信一级🟡。这是GAP-02补全的关键——不知道是谁说的=新的不信任。"""
    },
    {
        "q": "观澜浏览器的断路器是怎么工作的？",
        "a": """观澜断路器是引擎故障自动转移机制。

参数：
- 熔断阈值：连续3次失败
- 冷却时间：10分钟（600秒）
- 审计链：所有失败/熔断/恢复事件记录

工作流程：
1. 每次引擎调用失败，失败计数+1
2. 连续失败达到3次 → 触发熔断：记录熔断时间，清零失败计数
3. 熔断期间，该引擎的路由自动转移到备用引擎（如 Kimi→Ollama）
4. 10分钟冷却后自动恢复，清零计数器
5. 如果成功调用，计数器重置

不变式：计数器和熔断时间互斥——(熔断时间>0)⇒(计数=0)，(计数>0)⇒(熔断时间=0)

故障转移链：Kimi→Ollama, CodeBuddy→Ollama, 小艺→Ollama"""
    },
]

# ============================================================
# 知识域3: 安全与隐私
# ============================================================
SECURITY_QA = [
    {
        "q": "观澜浏览器如何保护用户隐私？",
        "a": """观澜浏览器隐私保护有三层装甲：

1. 隐私装甲（L2网关层）：
   - 第三方追踪器拦截
   - 浏览器指纹随机化
   - Cookie分罐隔离（不同站点cookie不互通）
   - 只传用量不传内容——浏览记录永不出机

2. 隐私出域闸门（M8模块）：
   - 文本离机前自动扫描敏感信息
   - 命中模式：身份证号、手机号、银行卡号、邮箱、详细地址
   - 两种策略：脱敏（替换为[***类型***]）或拦截（直接拒绝🔴）
   - 脱敏幂等性：已脱敏文本再次扫描不会产生新命中

3. 隐私任务锁定：
   - "隐私"和"离线"类型的任务永不出机
   - 即使Kimi可用，隐私任务也只走Ollama本地推理
   - 强制本地标志可覆盖路由"""
    },
    {
        "q": "观澜浏览器的网关层有什么安全功能？",
        "a": """龍魂网关（L2层，127.0.0.1本地代理）是观澜的主权核心，安全功能包括：

1. 流量过滤：广告拦截、追踪器拦截
2. 未成年守护（J0-J4）：实时内容过滤、分级判定
3. 技术主权守门（TS0-TS4）：境外回源检测、数据出境拦截
4. 反诈直通：钓鱼链接拦截、诈骗模式识别
5. 红线熔断：命中红线词立即熔断+理由码
6. 人机两本账：浏览器阅览记人工账，爬虫抓取记爬虫账

关键安全性质：网关挂 = 浏览器拒绝联网（fail-closed，不裸奔）。
网关进程被杀或异常退出，浏览器立即断开所有网络连接——宁可断网不可无防护。"""
    },
    {
        "q": "观澜浏览器的插件治理机制是什么？",
        "a": """观澜浏览器插件治理（GAP-06补全）：

1. 沙箱运行：所有插件在隔离沙箱中运行，不能直接访问浏览器内核

2. 权限审计：
   - 敏感权限集：读历史、改页面、发网络、读书签、读Cookie、注入脚本
   - 审计规则：敏感权限命中≥2项 → 🔴拒装；命中1项 → 🟡标记；0项 → 🟢通过

3. 签名核验：插件包必须附带GPG/SM2签名，安装前校验

4. 升级管控：插件升级后权限集扩大→触发重新审计，用户确认后方可升级

5. 信誉体系：插件评分复用电商信任引擎（信誉分引擎），未来插件商店可用"""
    },
]

# ============================================================
# 知识域4: 多端与同步
# ============================================================
MULTI_DEVICE_QA = [
    {
        "q": "观澜浏览器支持哪些平台？",
        "a": """观澜浏览器多端落点：

- macOS：WKWebView内核（先行）
- Windows：WebView2内核（先行）
- Linux：WebKitGTK内核（先行）
- 鸿蒙：ArkWeb内核+小艺语音入口（随后）
- iOS：WKWebView+对接longhun-ios（随后）

全部"一核多壳"架构：内核换壳不换魂。桌面版先行，移动端随后。

同步机制：
- 书签/历史/摘要库跨端同步走 longhun-cross-platform
- 本地直连+SM4加密信封+ECDH协商+版本向量一致性
- 同步不过外网，数据根留中国

账号体系：
- 登录走注册协议（双轨邮箱+三锚）
- 浏览器配置文件绑定用户DNA
- 公共设备启用访客模式（GUEST_前缀，关窗即焚）"""
    },
    {
        "q": "观澜浏览器断网时还能用吗？",
        "a": """观澜浏览器支持断网可用（GAP-05补全）：

断网时仍可用的功能：
- 本地书签浏览和管理
- 浏览历史查看和搜索
- 本地摘要库（之前生成的摘要缓存）
- Ollama本地AI问答（模型已下载到本地）
- 离线阅读模式（已缓存的页面）

断网时不可用的功能：
- 云端引擎（Kimi等）灰显并标注"断网"
- 新网页加载（除非有本地缓存）
- 跨端同步

设计原则：浏览器不能因为没网就变白板。核心能力本地化，云是增强不是命脉。"""
    },
]

# ============================================================
# 知识域5: 预留接口与扩展
# ============================================================
EXTENSIBILITY_QA = [
    {
        "q": "观澜浏览器预留了哪些接口？",
        "a": """观澜浏览器预留接口体系（K6核心——今天的空白，明天的座位）：

| 接口槽 | 路径 | 用途 | 状态 |
|--------|------|------|------|
| AI引擎槽 | /api/v1/li/browser/engines/{name} | 新AI助手注册（小易/DeepSeek/通义…） | 🟡预留 |
| 插件槽 | /api/v1/li/browser/plugins/{name} | 第三方功能扩展（沙箱） | 🟡预留 |
| MCP客户端槽 | 对接 longhun-cloud-mcp | 14技能工具浏览器内调用 | 🟢可用 |
| 脚本槽 | 用户脚本（类油猴） | 页面自动化，签名后运行 | 🟡预留 |
| 主题槽 | 主题工厂（对接既有技能） | 界面皮肤 | 🟢可用 |
| 协议槽 | longhun:// 自定义协议 | 内部资源寻址（如 longhun://dna/…） | 🟢可用 |

AI引擎槽注册规范：
- 新引擎须实现统一接口 ask(任务) → {回答, 引擎, 版本, 置信}
- 必须过三锚（DNA/闸口/签章）
- 必须过出域闸门
- 缺一不注册——接口槽开放不等于防线开放"""
    },
    {
        "q": "观澜浏览器的人机两本账是什么？怎么看？",
        "a": """人机两本账是观澜浏览器的核心数据分流机制（对接爬虫协议）：

- 人工账：用户在浏览器中手动浏览的页面数量
- 爬虫账：侦察蚁自动抓取的页面数量

两本账在观澜看板合显，格式：
"人工账:42(65%) ｜ 爬虫账:23(35%) ｜ 总计:65"

数学性质：
- 账本值永不负数（不变式）
- 每日明细可追溯（记录时间、URL、侧）
- 支持清零重置

设计目的：人看的归人，爬的归爬——浏览器不是爬虫，爬虫不是浏览器。两本账分列才能看清信息获取的真实来源。"""
    },
    {
        "q": "观澜浏览器的多模型对比功能怎么用？",
        "a": """多模型对比是观澜浏览器的GAP-04补全功能：

使用方式：同一问题可以并排调用两个AI引擎，结果左右对照显示。

对比输出：
- 问题原文
- 引擎A的回答 + 标注
- 引擎B的回答 + 标注
- 分歧点高亮（自动检测关键差异）
- 共识度评分（0-1，1=完全一致）

共识度计算：
共识度 = max(0, min(1, 1.0 - |分歧点|×0.1 - 长度差比例×0.2))

设计哲学：兼听则明，偏信则暗。两个引擎说一样的话→可信度高；说法不同→分歧点高亮提醒用户注意。"""
    },
]

ALL_QA = ARCHITECTURE_QA + AI_ROUTING_QA + SECURITY_QA + MULTI_DEVICE_QA + EXTENSIBILITY_QA

def generate_train_data(output_path: str = None):
    """生成观澜浏览器训练JSONL"""
    if output_path is None:
        output_path = PROJECT / "data" / "guanlan_browser_train.jsonl"
    
    entries = []
    ts = datetime.now().isoformat()
    
    for qa in ALL_QA:
        entry = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": qa["q"]},
                {"role": "assistant", "content": qa["a"]}
            ],
            "metadata": {
                "source": "guanlan_browser",
                "domain": "观澜浏览器与AI联动",
                "protocol": "LH-GUANLAN-BROWSER-AI-INTEGRATION-v1.0",
                "dna": "#龍芯⚡️丙午·乙未·丙申·申时·䷜坎-GUANLAN-BROWSER-ARCHITECTURE-PROTOCOL-V1.0-P0-61d854ad",
                "generated": ts
            }
        }
        entries.append(entry)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"✅ 生成 {len(entries)} 条观澜浏览器训练数据")
    print(f"   路径: {output_path}")
    return output_path


def merge_with_existing(train_jsonl: str, existing_dir: str = None, output_dir: str = None):
    """合并观澜数据到现有训练集"""
    if existing_dir is None:
        existing_dir = PROJECT / "models" / "longhun-v1.0" / "lora_output_v411" / "data_v411_ready"
    if output_dir is None:
        output_dir = PROJECT / "models" / "longhun-v1.0" / "lora_output_v411" / "data_v412_guanlan_ready"
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 读现有训练数据
    existing_train = Path(existing_dir) / "train.jsonl"
    existing_valid = Path(existing_dir) / "valid.jsonl"
    
    with open(existing_train, 'r', encoding='utf-8') as f:
        train_lines = f.readlines()
    
    with open(existing_valid, 'r', encoding='utf-8') as f:
        valid_lines = f.readlines()
    
    # 读新数据
    with open(train_jsonl, 'r', encoding='utf-8') as f:
        new_lines = f.readlines()
    
    # 按 90/10 拆分新数据
    split_idx = max(1, int(len(new_lines) * 0.9))
    new_train = new_lines[:split_idx]
    new_valid = new_lines[split_idx:]
    
    # 合并
    merged_train = train_lines + new_train
    merged_valid = valid_lines + new_valid
    
    # 写入
    with open(Path(output_dir) / "train.jsonl", 'w', encoding='utf-8') as f:
        f.writelines(merged_train)
    
    with open(Path(output_dir) / "valid.jsonl", 'w', encoding='utf-8') as f:
        f.writelines(merged_valid)
    
    # dataset_info.json
    info = {
        "train_size": len(merged_train),
        "valid_size": len(merged_valid),
        "original_train": len(train_lines),
        "original_valid": len(valid_lines),
        "guanlan_added_train": len(new_train),
        "guanlan_added_valid": len(new_valid),
        "guanlan_total": len(new_lines),
        "merged_at": datetime.now().isoformat()
    }
    with open(Path(output_dir) / "dataset_info.json", 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 合并完成:")
    print(f"   训练集: {len(train_lines)} → {len(merged_train)} (+{len(new_train)} 观澜)")
    print(f"   验证集: {len(valid_lines)} → {len(merged_valid)} (+{len(new_valid)} 观澜)")
    print(f"   总计: {len(merged_train) + len(merged_valid)} 条")
    print(f"   输出: {output_dir}")
    
    return output_dir


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="观澜浏览器训练数据生成器")
    p.add_argument("action", choices=["gen", "merge", "all"], default="all", nargs="?")
    p.add_argument("--output", help="输出路径")
    args = p.parse_args()
    
    if args.action in ("gen", "all"):
        train_file = generate_train_data(args.output)
    
    if args.action in ("merge", "all"):
        merge_with_existing(train_file)
