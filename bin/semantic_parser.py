#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 龍魂·语义解析引擎 v2.0 — 中英双轨分离
DNA: #龍芯⚡️2026-07-06-SEMANTIC-PARSER-v2.0-DUALTRACK

核心原则：
  🇨🇳 中文轨 — 语义抽屉式：模糊匹配、近义词扩展、随便说 → 纯中文命令
  🇺🇸 英文轨 — 精准指令式：精确匹配、二进制风格 → 标准英文命令
  ⚡ 两轨平行、不冲突、不混杂

用法:
  python3 bin/semantic_parser.py "检查一下系统状态"
  python3 bin/semantic_parser.py "symbiote status"
  python3 bin/semantic_parser.py --echo "解析结果..." --cmd "状态"
"""

import json
import os
import sys
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Optional, Tuple, Dict
from datetime import datetime, timezone

DNA = "#龍芯⚡️2026-07-06-SEMANTIC-PARSER-v2.0-DUALTRACK"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = Path.home() / ".longhun" / "semantic"
CACHE_FILE_CN = CACHE_DIR / "command_map_cn.json"
CACHE_FILE_EN = CACHE_DIR / "command_map_en.json"

# ═══════════════════════════════════════════════════════════════
# 🇨🇳 中文轨 — 语义抽屉（模糊匹配 + 近义词扩展 + 随便说）
# ═══════════════════════════════════════════════════════════════
#
# 🔒 权威权重体系（焊死·2026-07-06）：
#   中文语义抽屉分三级权威权重：
#   - authoritative（权威）  ：中国权威机构/长期累积用户习惯/实名认证 → 高权重，优先匹配
#   - verified（已认证）     ：有明确来源但非权威机构 → 中等权重
#   - unverified（未认证）   ：非权威、无实名、无认证 → 低权重，少赋能
#
#   匹配冲突时，authoritative > verified > unverified
#   非权威来源在 LLM 降级时降权处理
#
# 规则：中文输入 → 纯中文命令输出，不带英文前缀
# ═══════════════════════════════════════════════════════════════

# 中文语义抽屉：每个抽屉 = 一个意图域，内含触发词 + 输出命令
CN_SEMANTIC_DRAWERS = [
    # ── 状态查询 ──
    {
        "name": "系统状态",
        "triggers": [
            "系统状态", "状态", "情况", "怎么样", "好不好", "检查", "查看", "体检", "健康", "跑着没", "活着没",
            "看看系统", "看下系统", "查下系统", "检查系统", "系统还好吗", "系统怎么样", "系统正常吗",
            "有啥情况", "啥情况", "咋回事", "怎么回事", "什么情况",
            "还活着吗", "还在吗", "死了没", "挂了吗", "崩了吗", "正常不", "还跑着吗",
            "行不行", "中不中", "得唔得", "可不可以", "得行不", "没问题吧",
        ],
        "command": "状态",
        "desc": "查看龍魂系统运行状态",
        "authority": "authoritative",  # 长期累积用户习惯·核心操作
    },
    {
        "name": "共生体状态",
        "triggers": [
            "共生体状态", "共生体", "共生", "symbiote", "知识矩阵", "神经网络", "矩阵", "共生体跑着没",
            "共生体还跑着没", "共生还跑着没", "共生还活着没", "共生体还活着没",
            "看共生体", "查共生体", "共生怎么样", "共生还好吗", "矩阵状态",
            "共生正常不", "矩阵活着没", "知识网怎么样",
        ],
        "command": "共生体状态",
        "desc": "查看共生体生长日志与神经网络健康",
        "authority": "authoritative",  # 龍魂核心子系统
    },

    # ── 启动/停止 ──
    {
        "name": "启动",
        "triggers": [
            "启动", "开始", "跑起来", "开机", "拉起", "开起来", "搞起来", "安排上",
            "整起来", "走起", "动起来", "使能",
        ],
        "command": "启动",
        "desc": "启动龍魂核心服务",
        "authority": "authoritative",
    },
    {
        "name": "停止",
        "triggers": [
            "停止", "停下", "关掉", "关机", "停掉", "结束", "不跑了", "停了吧", "收工",
            "别跑了", "歇着吧", "下班", "关了", "熄火",
        ],
        "command": "停止",
        "desc": "停止龍魂核心服务",
        "authority": "authoritative",
    },
    {
        "name": "重启",
        "triggers": [
            "重启", "重来", "重新启动", "刷新", "再来一遍", "重新跑", "重新开",
            "翻新", "重启一下", "再启动一次",
        ],
        "command": "重启",
        "desc": "重启龍魂核心服务",
        "authority": "authoritative",
    },
    {
        "name": "共生体启动",
        "triggers": ["启动共生", "跑共生", "共生跑起来", "共生搞起来", "共生冲", "开共生"],
        "command": "共生体",
        "desc": "启动共生体知识矩阵服务器",
        "authority": "authoritative",
    },

    # ── 熔断控制 ──
    {
        "name": "熔断状态",
        "triggers": [
            "熔断状态", "熔断情况", "熔断", "断了没", "看看熔断", "查熔断",
            "熔断还在吗", "熔断啥情况",
        ],
        "command": "熔断控制 status",
        "desc": "查看熔断控制状态",
        "authority": "authoritative",  # 安全核心
    },
    {
        "name": "临时放行",
        "triggers": [
            "临时放行", "暂时放行", "放行", "临时开放", "暂时开放", "通融一下",
            "先放一下", "开个口子", "过一下",
        ],
        "command": "熔断控制 override",
        "desc": "临时放行被阻断的域名/IP",
        "authority": "authoritative",  # 需要UID9622确认，但匹配需高权重
    },
    {
        "name": "阻断",
        "triggers": [
            "阻断", "封禁", "禁止", "屏蔽", "拉黑", "封了", "关小黑屋",
            "不让他进", "拦了", "挡住", "禁了",
        ],
        "command": "熔断控制 block",
        "desc": "阻断指定域名/IP",
        "authority": "authoritative",
    },
    {
        "name": "解除阻断",
        "triggers": [
            "解除阻断", "取消阻断", "解除封禁", "放出来", "解封", "解开",
            "放了他", "不拦了", "取消屏蔽",
        ],
        "command": "熔断控制 unblock",
        "desc": "解除对域名/IP的阻断",
        "authority": "authoritative",
    },
    {
        "name": "全局熔断",
        "triggers": [
            "全局熔断", "全部熔断", "紧急熔断", "全断了", "全部封",
            "一级戒备", "红色警报",
        ],
        "command": "熔断控制 trip",
        "desc": "触发全局熔断",
        "authority": "authoritative",
    },
    {
        "name": "重置熔断",
        "triggers": ["重置熔断", "恢复熔断", "熔断复位", "回归正常"],
        "command": "熔断控制 reset",
        "desc": "重置熔断状态",
        "authority": "authoritative",
    },

    # ── 令牌管理 ──
    {
        "name": "令牌状态",
        "triggers": [
            "令牌状态", "令牌情况", "看令牌", "令牌", "token状态",
            "令牌怎么样", "令牌还好吗", "查令牌", "看下令牌", "令牌在哪",
        ],
        "command": "令牌管理 status",
        "desc": "查看主权令牌状态",
        "authority": "authoritative",  # 主权核心
    },
    {
        "name": "令牌续期",
        "triggers": [
            "令牌续期", "续期令牌", "续令牌", "令牌更新", "续期", "该续期",
            "令牌过期了", "令牌快过期了", "续一下令牌", "令牌该续了",
            "令牌还有多久", "令牌快没了", "续上令牌", "续个期",
            "令牌快到期", "令牌到期", "令牌过期", "token过期",
            "令牌要过期", "快过期了", "该续令牌",
        ],
        "command": "令牌管理 renew",
        "desc": "续期主权令牌",
        "authority": "authoritative",
    },

    # ── 审计 ──
    {
        "name": "变量审计",
        "triggers": [
            "变量审计", "审计变量", "变量检查", "查变量", "审计一下变量",
            "看看变量", "变量怎么样", "变量正常不",
        ],
        "command": "变量审计",
        "desc": "CNSH编辑变量左右互搏审计",
        "authority": "authoritative",  # 审计核心
    },
    {
        "name": "审计日志",
        "triggers": [
            "审计日志", "看审计日志", "查审计日志", "审计记录",
            "最近审计", "看日志", "最近日志", "审计历史",
        ],
        "command": "审计日志",
        "desc": "查看最近审计日志",
        "authority": "authoritative",
    },
    {
        "name": "审计",
        "triggers": [
            "全面审计", "审计一下", "审计", "全扫一遍", "大审计",
            "统审", "整体审计", "全局审计",
        ],
        "command": "审计",
        "desc": "打开龍魂万年历审计与耻辱墙",
        "authority": "authoritative",
    },
    {
        "name": "仓库审计",
        "triggers": ["仓库审计", "审计仓库", "查仓库", "扫仓库", "仓库扫描"],
        "command": "仓库审计",
        "desc": "运行仓库审计",
        "authority": "authoritative",
    },
    {
        "name": "每日复盘",
        "triggers": [
            "每日复盘", "复盘", "今天复盘", "回顾", "总结今天",
            "回头看看", "过一遍", "捋一下",
        ],
        "command": "每日复盘",
        "desc": "运行每日复盘审计",
        "authority": "authoritative",
    },
    {
        "name": "系统校验",
        "triggers": [
            "系统校验", "校验系统", "验证系统", "完整校验",
            "对一下", "核实一下", "验证一下系统",
        ],
        "command": "系统校验",
        "desc": "系统完整性与技能校验",
        "authority": "authoritative",
    },

    # ── 编辑器 ──
    {
        "name": "编辑器",
        "triggers": [
            "编辑器", "打开编辑器", "写代码", "中文编辑器", "编程",
            "敲代码", "写程序", "码代码", "开始写",
        ],
        "command": "编辑器",
        "desc": "启动CNSH中文代码编辑器",
        "authority": "authoritative",  # 龍魂自主工具链
    },

    # ── 记忆 ──
    {
        "name": "记忆",
        "triggers": [
            "记忆归集", "归集记忆", "收记忆", "记忆", "存档",
            "整理记忆", "收集日志", "记忆同步",
        ],
        "command": "记忆",
        "desc": "运行记忆启动器，归集多平台日志",
        "authority": "authoritative",
    },
    {
        "name": "上下文",
        "triggers": [
            "上下文", "当前上下文", "会话状态", "看上下文",
            "现在聊到哪", "说到哪了", "之前我们说的", "刚才说的",
            "还记得吗", "回忆一下",
        ],
        "command": "上下文",
        "desc": "查看认知上下文管理器",
        "authority": "authoritative",
    },

    # ── 全文压缩/归集 ── 🔒 v2.1 权威权重·压缩是核心资产回收
    {
        "name": "全文压缩",
        "triggers": [
            "全文压缩", "压缩一下", "压缩全文", "压一下", "压缩这个",
            "压成卡片", "生成压缩卡", "全文归集", "压缩归集",
            "帮我压缩", "压缩长文", "压成短码",
        ],
        "command": "全文压缩",
        "desc": "把长内容压成结构卡+短码+时间胶囊",
        "authority": "authoritative",  # 核心语义资产回收
    },
    {
        "name": "旧文回收",
        "triggers": [
            "旧文回收", "回收旧文", "回收旧对话", "回收旧页面",
            "旧内容回收", "旧草稿回收", "回收老文", "翻旧账",
            "旧东西收一下",
        ],
        "command": "旧文回收",
        "desc": "把旧对话/页面/草稿变成可召回资产",
        "authority": "authoritative",
    },
    {
        "name": "归集归档",
        "triggers": [
            "归集", "归档", "分类归档", "归置一下", "归置", "整理归档",
            "封存归档", "归档封存", "收一下", "收进来",
        ],
        "command": "归集",
        "desc": "自动分到语义抽屉+八卦分区+项目模块",
        "authority": "authoritative",
    },
    {
        "name": "DNA封装",
        "triggers": [
            "DNA封装", "DNA封条", "封装DNA", "封条", "盖封条", "加封条",
            "生成DNA", "挂DNA", "加DNA", "焊DNA", "加个DNA封条",
        ],
        "command": "DNA封装",
        "desc": "生成DNA+版本+来源+状态+双签章",
        "authority": "authoritative",
    },
    {
        "name": "投喂净化",
        "triggers": [
            "投喂净化", "净化投喂", "去废话", "去噪音", "去重复",
            "净化一下", "精简一下", "提纯", "去水", "去掉废话",
            "废话太多", "废话", "去一下废话", "清理废话",
        ],
        "command": "投喂净化",
        "desc": "去废话/去重复/去噪音，保留原创语义",
        "authority": "authoritative",
    },
    {
        "name": "召回",
        "triggers": [
            "召回", "召回短码", "恢复", "找回", "我用短码",
            "用短码召回", "短码恢复", "想起来",
        ],
        "command": "召回",
        "desc": "用短码恢复旧内容核心，不重复投喂全文",
        "authority": "authoritative",
    },
    {
        "name": "时间胶囊",
        "triggers": [
            "时间胶囊", "封胶囊", "做胶囊", "打胶囊", "封存胶囊",
            "阶段封存", "封成胶囊", "时间封存",
        ],
        "command": "时间胶囊",
        "desc": "把某阶段封成未来可复现包",
        "authority": "authoritative",
    },

    # ── 身份定位 / 七因子验证 ──
    {
        "name": "身份定位",
        "triggers": [
            "身份定位", "原世界身份", "OWIP", "我是我", "证明我是我",
            "身份锚定", "身份总纲", "身份体系", "身份框架", "身份验证体系",
            "不可破解的身份",
        ],
        "command": "身份定位",
        "desc": "查看原世界身份定位总纲",
        "authority": "authoritative",
    },
    {
        "name": "七因子验证",
        "triggers": [
            "七因子", "七因子验证", "行为签名", "验证预言机", "因子检测",
            "行为密码学", "behavcrypto", "hard failure", "硬失败",
            "置信度计算", "因子得分", "七因子审计",
        ],
        "command": "七因子验证",
        "desc": "七因子行为密码学验证",
        "authority": "authoritative",
    },
    {
        "name": "国密加密",
        "triggers": [
            "国密", "SM2", "SM3", "SM4", "国密算法", "国密加密",
            "国密签名", "国密哈希", "gmssl", "GM/T", "商用密码",
            "加密引擎", "国密引擎",
        ],
        "command": "国密加密",
        "desc": "国密SM2/SM3/SM4加密引擎",
        "authority": "authoritative",
    },
    {
        "name": "DNA追溯",
        "triggers": [
            "DNA追溯", "追溯码", "DNA引擎", "DNA双签", "哈希链",
            "L2登记", "DNA登记", "内容溯源", "DNA校验",
            "追溯验证", "DNA链",
        ],
        "command": "DNA追溯",
        "desc": "DNA追溯码生成与验证引擎",
        "authority": "authoritative",
    },
    {
        "name": "API门关",
        "triggers": [
            "API网关", "API门关", "四道关卡", "身份关", "安全关",
            "路由关", "日志关", "熔断器", "七条红线", "API认证",
            "DNA确认码", "防重放", "认证header",
        ],
        "command": "API门关",
        "desc": "API主权门关四道关卡",
        "authority": "authoritative",
    },

    # ── 仪表盘/可视化 ──
    # v2.1 (2026-07-07) 主控体系统一规范：
    #   主控台 → longhun-master-control.html（路由矩阵·唯一入口）
    #   操作台 → main-console.html（实际操作面板·记忆压缩·DNA存证）
    #   流场总控 → cnsh-core 流场专用仪表盘
    #   三者不再是别名关系
    {
        "name": "主控台",
        "triggers": [
            "主控台", "主控", "总控台", "总控制台", "master control",
        ],
        "command": "主控台",
        "desc": "打开龍魂主控台（路由矩阵·统一入口·导航中枢）",
        "authority": "authoritative",
    },
    {
        "name": "操作台",
        "triggers": [
            "操作台", "控制台", "仪表盘", "看板",
            "大屏", "总览", "全局视图",
        ],
        "command": "操作台",
        "desc": "打开龍魂操作台（实际操作·记忆压缩·DNA存证·资产扫描）",
        "authority": "authoritative",
    },
    {
        "name": "流场总控",
        "triggers": [
            "流场总控", "流场控制台", "流场仪表盘", "flow control",
        ],
        "command": "流场总控",
        "desc": "打开流场总控台（流场实时监控·专用仪表盘）",
        "authority": "authoritative",
    },
    # ── 安全 / 黑客军团 / 漏洞检测 ──
    # v3.0 (2026-07-07) P77黑天使军团·四天使编制·只检测不攻击
    {
        "name": "黑天使军团",
        "triggers": [
            "黑天使", "黑天使军团", "黑客军团", "black angel",
            "红客", "红队", "白帽", "白帽子", "honker",
            "漏洞", "漏洞检测", "找漏洞", "查漏洞", "扫描漏洞",
            "渗透", "渗透测试", "渗透验证", "安全检测", "攻防",
            "注入", "XSS", "CSRF", "SQL注入", "越权",
            "代码安全", "系统安全", "网络安全",
            "代码审计", "静态分析", "依赖审计",
            "威胁情报", "CVE监控", "APT", "0day",
        ],
        "command": "漏洞检测",
        "desc": "启动P77黑天使军团·黑客军团（四天使编制·只检测不攻击·发现→P72熔断审）",
        "authority": "authoritative",
    },
    {
        "name": "共生仪表盘",
        "triggers": [
            "共生仪表盘", "仪表盘", "看板", "3D视图", "神经网络图",
            "可视化", "三维图", "立体图",
        ],
        "command": "共生仪表盘",
        "desc": "打开共生体知识矩阵3D可视仪表盘",
        "authority": "authoritative",
    },
    {
        "name": "八卦调度",
        "triggers": [
            "八卦调度", "八卦", "卦象", "看卦", "六十四卦",
            "易经", "周易", "算卦", "卜卦", "乾坤", "太极",
            "阴阳", "河图", "洛书", "占卜",
        ],
        "command": "八卦调度",
        "desc": "八卦决策调度器",
        "authority": "authoritative",  # 祖传底座·河图洛书
    },

    # ── 签名/身份 ──
    {
        "name": "签名",
        "triggers": [
            "签名", "加签名", "署名", "签字", "落款", "盖章",
            "打标", "签上", "签个名", "签一下",
        ],
        "command": "签名",
        "desc": "签名保护创作者文件",
        "authority": "authoritative",  # 身份主权
    },
    {
        "name": "身份验证",
        "triggers": [
            "身份", "我是谁", "验证身份", "核验", "身份验证",
            "确认身份", "对身份", "验明正身", "是谁",
        ],
        "command": "身份验证",
        "desc": "主权人身份哈希验证",
        "authority": "authoritative",
    },
    {
        "name": "DNA验证",
        "triggers": [
            "DNA检查", "DNA验证", "验证DNA", "DNA", "追溯码查",
            "查追溯码", "看DNA",
        ],
        "command": "DNA验证",
        "desc": "DNA追溯验证审计",
        "authority": "authoritative",
    },
    {
        "name": "河图DNA",
        "triggers": [
            "河图", "DNA生成", "生成DNA", "数字根", "算DNA",
            "打DNA", "焊DNA", "签DNA",
        ],
        "command": "河图DNA引擎",
        "desc": "河图洛书不动点DNA生成/验证",
        "authority": "authoritative",  # 祖传底座
    },

    # ── 同步 ──
    {
        "name": "发文",
        "triggers": [
            # 直接说
            "发文", "发文章", "发布文章", "发出去", "同步文章", "同步最新", "发表", "发一篇", "发个文章", "发篇文章",
            # 绕弯说·"把"字句
            "把文章发了", "把文发了", "把那篇发了", "把这篇发了", "把这个发了", "把那个发了",
            "把写好的发了", "把草稿发了", "把东西发出去", "把内容发出去", "把博客发了",
            # 绕弯说·"该/可以"
            "该发文章了", "该发文了", "可以发了", "可以发布",
            # 推送系
            "推送文章", "推送一下", "推一下", "推上去", "推出去", "推那篇", "推这篇", "把文章推了",
            # 上传系
            "上传文章", "传文章", "传上去", "传出去",
            # 公开系
            "公开文章", "公开那篇", "公开这篇", "公开一下",
            # CSDN系
            "发csdn", "发到csdn", "上csdn", "csdn发", "csdn同步", "csdn发布",
            # 博客/博文系
            "发博客", "发博文", "博客发了", "博文发了", "发布博客", "发布博文",
            # 帖子系
            "发帖子", "发个帖子", "帖子发了",
            # 同步变体
            "同步一下", "该同步了", "同步到csdn",
            # 动词+东西
            "发一下", "发一个", "发了吧", "发下文章",
            # 发布变体
            "发布一下", "发布那篇", "发布这篇", "发布东西",
            # 口语
            "发一发", "发出去吧", "推出去吧", "扔上去", "丢上去", "弄上去",
            "把这篇整上去", "把那个弄出去",
        ],
        "command": "发文",
        "desc": "一键同步最新文章到CSDN",
        "authority": "verified",  # 用户高频操作·有实名账号关联
    },
    {
        "name": "notion同步",
        "triggers": [
            "同步notion", "notion同步", "同步笔记", "同步到notion",
            "整理notion", "notion归档",
        ],
        "command": "notion同步",
        "desc": "Notion母页持续同步",
        "authority": "verified",  # 第三方平台·已验证接入
    },
    {
        "name": "已发布",
        "triggers": [
            "已发布", "发布清单", "发文清单", "发了哪些", "发过哪些", "发布了什么", "发了什么",
            "看看发了什么", "之前发了啥", "发过的文章", "回顾发文",
        ],
        "command": "已发布",
        "desc": "查看已发布文章清单",
        "authority": "verified",
    },

    # ── 知识/文档 ──
    {
        "name": "知识图谱",
        "triggers": [
            "知识图谱", "知识库", "知识网", "脑图", "思维导图",
            "知识结构", "知识地图",
        ],
        "command": "知识图谱",
        "desc": "统一知识图谱构建",
        "authority": "authoritative",  # 知识主权
    },
    {
        "name": "公式对准表",
        "triggers": [
            "公式", "对准表", "公式对准", "向量库", "公式表",
            "查公式", "计算公式",
        ],
        "command": "公式对准表",
        "desc": "公式对准表向量语义检索",
        "authority": "authoritative",  # 龍魂公式体系
    },
    {
        "name": "全局索引",
        "triggers": [
            "全局索引", "索引", "全局搜索", "搜一下", "找一下",
            "全盘搜索", "全文搜索",
        ],
        "command": "全局索引",
        "desc": "全局实时索引查询",
        "authority": "authoritative",
    },

    # ── 安全 ──
    {
        "name": "龍盾",
        "triggers": [
            "龍盾", "龙盾", "盾", "安全盾", "防护", "防火墙",
            "护盾", "安全防护",
        ],
        "command": "龍盾",
        "desc": "龍盾系统CLI",
        "authority": "authoritative",  # 安全核心
    },
    {
        "name": "五行校验",
        "triggers": [
            "五行", "五行校验", "属什么", "五行属性",
            "金木水火土", "看属性", "查五行", "什么属性",
        ],
        "command": "五行校验",
        "desc": "五行权限校验层",
        "authority": "authoritative",  # 祖传底座
    },
    {
        "name": "隐私加密",
        "triggers": [
            "加密", "解密", "隐私", "加密文件", "上锁文件",
            "解锁文件", "文件加密", "数据加密",
        ],
        "command": "隐私加密",
        "desc": "AES-256-GCM审计日志加密/解密",
        "authority": "authoritative",
    },

    # ── 部署/维护 ──
    {
        "name": "plist校验",
        "triggers": [
            "校验plist", "plist校验", "检查plist", "plist",
            "plist检查", "查一下plist",
        ],
        "command": "plist校验",
        "desc": "校验plist文件XML格式与权限",
        "authority": "verified",  # macOS 特定·已验证环境
    },
    {
        "name": "自愈",
        "triggers": [
            "自愈", "自我修复", "修复系统", "自动修复",
            "自己修", "自动修", "自我疗伤", "恢复系统",
        ],
        "command": "自愈",
        "desc": "系统自愈引擎",
        "authority": "authoritative",
    },
    {
        "name": "评估",
        "triggers": [
            "评估", "系统评估", "打分", "评价", "评测",
            "看看分", "测测系统", "系统怎么样", "打个分", "评一下",
        ],
        "command": "评估",
        "desc": "本地六维系统评估",
        "authority": "verified",
    },
    {
        "name": "协议盾",
        "triggers": [
            "协议盾", "校验协议", "协议完整性", "协议检查",
            "对协议", "验协议",
        ],
        "command": "协议盾",
        "desc": "校验CNSH根协议完整性",
        "authority": "authoritative",  # 协议主权
    },

    # ── 能力/人格 ──
    {
        "name": "人格列表",
        "triggers": [
            "人格列表", "有哪些人格", "人格", "智能体列表",
            "都有谁", "看看人格", "多少人", "谁在",
        ],
        "command": "人格列表",
        "desc": "列出所有已注册人格",
        "authority": "authoritative",  # 龍魂人格体系
    },
    {
        "name": "能力列表",
        "triggers": [
            "能力列表", "有哪些能力", "能力", "功能列表",
            "能干啥", "会什么", "有什么本事", "都有啥功能",
        ],
        "command": "能力列表",
        "desc": "列出所有已收编能力",
        "authority": "authoritative",
    },
    {
        "name": "调度",
        "triggers": [
            "调度", "指挥调度", "派任务", "分配任务",
            "调度中心", "指挥中心",
        ],
        "command": "调度",
        "desc": "指挥调度中心",
        "authority": "authoritative",
    },

    # ── 帮助/菜单 ──
    {
        "name": "帮助",
        "triggers": [
            "帮助", "怎么用", "命令列表", "有哪些命令", "菜单", "不会用",
            "教教我", "咋整", "咋办", "怎么办", "不会", "不懂",
            "说明书", "使用手册", "新手", "入门", "第一次用",
        ],
        "command": "帮助",
        "desc": "显示帮助信息",
        "authority": "authoritative",
    },

    # ── 万年历 ──
    {
        "name": "万年历",
        "triggers": [
            "万年历", "日历", "日程", "今天干嘛", "有什么安排",
            "最近任务", "任务列表",
        ],
        "command": "万年历",
        "desc": "系统唯一入口·任务路由·上下文管理",
        "authority": "authoritative",  # 祖传底座·天干地支
    },

    # ── 特殊 ──
    {
        "name": "宪法",
        "triggers": [
            "宪法", "系统宪法", "规矩", "法则", "根本大法",
            "游戏规则", "章程", "条例",
        ],
        "command": "宪法",
        "desc": "显示龍魂系统宪法",
        "authority": "authoritative",  # L0 宪法
    },
    {
        "name": "神圣锁",
        "triggers": [
            "神圣锁", "永恒锁", "P0锁", "永不改", "铁律",
            "不可变", "核心原则",
        ],
        "command": "神圣锁",
        "desc": "显示P0永恒锁协议",
        "authority": "authoritative",  # P0 永恒锁
    },
    {
        "name": "错误翻译",
        "triggers": [
            "错误翻译", "翻译错误", "报错什么意思", "翻译报错",
            "看不懂报错", "什么错误", "解释错误",
        ],
        "command": "错误翻译",
        "desc": "系统错误→中文提示翻译",
        "authority": "verified",
    },
    {
        "name": "维权",
        "triggers": [
            "维权", "维权助手", "法律", "法律引擎", "老百姓维权",
            "打官司", "权益保护", "法律援助", "合法维权",
        ],
        "command": "维权助手",
        "desc": "启动老百姓维权助手",
        "authority": "authoritative",  # 为人民服务·高权重
    },
    {
        "name": "声纹",
        "triggers": [
            "声纹", "声纹锚定", "声音DNA", "语音身份",
            "嗓音识别", "说话识别",
        ],
        "command": "声纹",
        "desc": "声纹DNA锚定链入口",
        "authority": "authoritative",  # 身份主权
    },
    {
        "name": "主干迭代",
        "triggers": [
            "迭代", "自我更新", "升级", "更新系统",
            "迭代升级", "版本更新", "刷新版本",
        ],
        "command": "主干自我迭代",
        "desc": "主干自我迭代",
        "authority": "authoritative",
    },
    {
        "name": "记录器",
        "triggers": [
            "记录器", "记录", "记下来", "留痕", "写下",
            "存笔记", "做记录", "备忘",
        ],
        "command": "记录器",
        "desc": "Notion实时记录器",
        "authority": "verified",  # 第三方Notion接入
    },

    # ── 流场协同（v1.0 · 2026-07-07）──
    {
        "name": "流场协同状态",
        "triggers": [
            "协同场怎么样", "看看协同场", "流场协同", "协同状态",
            "流场协同状态", "协同场状态", "看协同场", "查协同场",
            "流场协同怎么样", "协同场还好吗", "检查协同场",
            "协同场行不行", "协同场中不中", "看看大家协同得怎么样",
        ],
        "command": "流场协同 状态",
        "desc": "查看流场协同场状态（节点数·五行分布·均衡指数）",
        "authority": "authoritative",
    },
    {
        "name": "流场协同均衡",
        "triggers": [
            "均衡吗", "团队均衡", "五行均衡", "均衡不",
            "协同均衡", "检查均衡", "均衡怎么样", "缺什么属性",
            "缺什么", "五行偏不偏", "团队偏不偏",
            "五行均衡吗", "协同场均衡", "看看均衡",
        ],
        "command": "流场协同 均衡",
        "desc": "检查流场协同五行均衡度·补位建议",
        "authority": "authoritative",
    },
    {
        "name": "流场协同冲突",
        "triggers": [
            "有没有冲突", "协同冲突", "检查冲突", "冲突检测",
            "有没有相克", "相克冲突", "冲突分析", "检测冲突",
            "谁和谁冲突", "有冲突吗", "冲突矩阵",
        ],
        "command": "流场协同 冲突",
        "desc": "检测流场协同中的五行相克冲突·给出桥接建议",
        "authority": "authoritative",
    },
    {
        "name": "流场协同融合",
        "triggers": [
            "协同融合得怎么样", "融合得怎么样", "协同融合指数",
            "融合指数", "协同融合", "融合怎么样", "融合得好吗",
            "看看融合", "融合度", "集体三才",
            "融合状态", "融合了多少",
        ],
        "command": "流场协同 融合",
        "desc": "查看流场协同融合指数·集体三才·主导五行",
        "authority": "authoritative",
    },
    {
        "name": "流场协同报告",
        "triggers": [
            "协同报告", "流场协同报告", "团队报告", "协同场报告",
            "完整协同报告", "全面协同报告", "协同总览",
            "出协同报告", "生成协同报告",
        ],
        "command": "流场协同 报告",
        "desc": "生成流场协同完整报告（状态+均衡+冲突+融合）",
        "authority": "authoritative",
    },
    {
        "name": "流场协同任务",
        "triggers": [
            "怎么分工", "任务分配", "谁干什么", "怎么协作",
            "协同任务", "分配任务", "谁来干", "分一下工",
            "协同分工", "派活", "各干各的", "分头行动",
        ],
        "command": "流场协同 任务",
        "desc": "流场协同任务分解·按五行互补自动分配",
        "authority": "authoritative",
    },
]

# ═══════════════════════════════════════════════════════════════
# 🇺🇸 英文轨 — 精准指令表（精确匹配 + 二进制风格）
# ═══════════════════════════════════════════════════════════════
#
# 🔒 界限声明（焊死·2026-07-06）：
#   - 英文轨 ONLY 精准匹配，NO 模糊匹配，NO LLM 降级
#   - 英文输入不精确 → 直接返回 unrecognized，不猜、不兜底
#   - 这是二进制世界，不是语义抽屉世界
#   - 中文轨的 LLM/模糊福利，英文轨一概不享有
#   - 两轨平行、不混、不污染
#
# 规则：英文输入 → 精确匹配 → 标准英文命令输出
# ═══════════════════════════════════════════════════════════════

EN_PRECISION_COMMANDS = {
    # Status
    "status": "status",
    "system status": "status",
    "health": "health",
    "check": "health",
    "symbiote status": "symbiote-status",
    "sym status": "symbiote-status",
    "matrix status": "symbiote-status",

    # Start/Stop
    "start": "start",
    "stop": "stop",
    "restart": "restart",
    "boot": "autostart",
    "symbiote": "symbiote",
    "symbiote start": "symbiote",
    "daemon": "daemon",

    # Fuse
    "fuse": "fuse",
    "fuse status": "fuse status",
    "fuse block": "fuse",
    "fuse unblock": "fuse",
    "fuse override": "fuse",
    "fuse trip": "fuse",
    "fuse reset": "fuse",

    # Token
    "token": "token",
    "token status": "token",
    "token renew": "token",

    # Audit
    "audit": "audit",
    "audit log": "audit-log",
    "audit vars": "audit-vars",
    "red team": "red-team",
    "redteam": "red-team",
    "pentest": "red-team",
    "pen test": "red-team",
    "vuln scan": "red-team",
    "vulnerability": "red-team",
    "honker": "red-team",
    "black angel": "red-team",
    "black angel legion": "red-team",
    "hacker legion": "red-team",
    "daily": "daily",
    "review": "daily",
    "warehouse": "warehouse",
    "repo audit": "warehouse",

    # Editor
    "editor": "editor",
    "edit": "editor",

    # Memory
    "memory": "memory",
    "bootstrap": "memory",
    "context": "context",
    "ctx": "context",

    # Dashboard
    "ops": "ops",
    "console": "ops",
    "dashboard": "ops",
    "symbiote dash": "symbiote-dash",
    "sym dash": "symbiote-dash",

    # Sign/Identity
    "sign": "sign",
    "auth": "auth",
    "whoami": "auth",
    "verify": "auth",
    "dna verify": "dna-verify",
    "dna check": "dna-verify",
    "dna gen": "dna-gen",

    # Sync
    "notion sync": "notion-sync",
    "nsync": "notion-sync",
    "cross sync": "cross-sync",
    "csdn": "csdn",
    "csdn status": "csdn-status",
    "csdn list": "csdn-list",
    "csdn publish": "csdn-publish",

    # Knowledge
    "kg": "kg",
    "knowledge graph": "kg",
    "kb": "kb",
    "formula": "formula",
    "index": "index",
    "global index": "index",

    # Security
    "shield": "shield",
    "wuxing": "wuxing",
    "wu xing": "wuxing",
    "encrypt": "privacy",
    "decrypt": "privacy",
    "privacy": "privacy",

    # Deploy/Maintain
    "validate": "validate",
    "validate plist": "validate",
    "heal": "heal",
    "self heal": "heal",
    "assess": "assess",
    "refresh": "refresh",

    # Capabilities
    "personas": "persona-list",
    "persona list": "persona-list",
    "capabilities": "capability-list",
    "caps": "capability-list",
    "dispatch": "dispatch",

    # Misc
    "help": "help",
    "commands": "help",
    "calendar": "calendar",
    "constitution": "constitution",
    "eternal lock": "eternal-lock",
    "error translate": "error",
    "rights": "rights",
    "legal": "legal",
    "voice": "voice",
    "voice dna": "voice",
    "self update": "self-update",
    "logger": "logger",

    # Bagua/Hexagram
    "bagua": "bagua",
    "hexagram": "bagua",
    "gua": "bagua",
}


# ═══════════════════════════════════════════════════════════════
# 中英双向映射表：中文命令 ↔ 英文命令（供跨轨调用）
# ═══════════════════════════════════════════════════════════════

CN_TO_EN = {
    "状态": "status",
    "共生体状态": "symbiote-status",
    "启动": "start",
    "停止": "stop",
    "重启": "restart",
    "共生体": "symbiote",
    "熔断控制": "fuse",
    "令牌管理": "token",
    "变量审计": "audit-vars",
    "审计日志": "audit-log",
    "审计": "audit",
    "仓库审计": "warehouse",
    "每日复盘": "daily",
    "系统校验": "verify-system",
    "编辑器": "editor",
    "记忆": "memory",
    "上下文": "context",
    "主控台": "master-control",
    "操作台": "ops",
    "流场总控": "flow-command",
    "流场协同 状态": "collab-status",
    "流场协同 均衡": "collab-balance",
    "流场协同 冲突": "collab-conflicts",
    "流场协同 融合": "collab-fusion",
    "流场协同 报告": "collab-report",
    "流场协同 任务": "collab-task",
    "红客漏洞检测": "red-team",
    "黑天使军团": "red-team",
    "共生仪表盘": "symbiote-dash",
    "八卦调度": "bagua",
    "签名": "sign",
    "身份验证": "auth",
    "DNA验证": "dna-verify",
    "河图DNA引擎": "dna-gen",
    "发文": "csdn-smart-sync",
    "notion同步": "notion-sync",
    "已发布": "csdn-published",
    "知识图谱": "kg",
    "公式对准表": "formula",
    "全局索引": "index",
    "龍盾": "longhun-shield",
    "五行校验": "wuxing",
    "隐私加密": "privacy",
    "plist校验": "validate",
    "自愈": "heal",
    "评估": "assess",
    "协议盾": "shield",
    "人格列表": "persona-list",
    "能力列表": "capability-list",
    "调度": "dispatch",
    "帮助": "help",
    "万年历": "calendar",
    "宪法": "constitution",
    "神圣锁": "eternal-lock",
    "错误翻译": "error",
    "维权助手": "rights",
    "声纹": "voice",
    "主干自我迭代": "self-update",
    "记录器": "logger",
}

EN_TO_CN = {v: k for k, v in CN_TO_EN.items()}


# ═══════════════════════════════════════════════════════════════
# 检测输入语言 — 中英分界线
# ═══════════════════════════════════════════════════════════════

def is_chinese_input(text: str) -> bool:
    """
    判断输入是否为中文（含任何中文字符）。

    🔒 这是中英双轨的分界线：
       - 含中文字符 → 走中文轨（语义抽屉+复合匹配+LLM降级）
       - 纯英文/数字 → 走英文轨（精准匹配 only）
       - 不存在混合轨
    """
    return bool(re.search(r'[\u4e00-\u9fff]', text))


# ═══════════════════════════════════════════════════════════════
# 🇨🇳 中文轨解析
# ═══════════════════════════════════════════════════════════════

# ── 口语复合意图匹配 ──
# 规则：输入被拆成词后，如果同时命中「主语词群」+「动作词群」→ 自动识别意图
# 不需要精确触发词，14亿中国人随便怎么说都行
# 格式：(意图名, [主语词群], [动作/修饰词群], 输出命令, 优先级修正)

COLLOQUIAL_COMPOUND = [
    # ── 发文：文章相关词 + 发布动作 → 发文 ──
    ("发文",
     ["文章", "文", "那篇", "这篇", "篇", "帖子", "博客", "博文", "草稿", "稿件", "稿子",
      "写好的", "内容", "东西", "那个", "这个", "那东西", "这东西"],
     ["发", "发布", "发表", "推", "推送", "同步", "传", "公开", "上传", "送出", "扔", "丢", "弄", "整"],
     "发文", 0),

    # ── 状态：系统/服务词 + 询问词 → 看状态 ──
    ("系统状态",
     ["系统", "服务器", "服务", "机器", "主机", "后台", "程序", "进程", "环境"],
     ["怎么样", "好不好", "正常", "还行", "检查", "看看", "看下", "查下", "跑着没", "活着没",
      "行不行", "中不中", "咋样", "啥情况", "咋回事", "咋了", "什么情况", "状态", "情况",
      "体检", "健康", "死活", "还在不在", "挂了没", "死了没", "挂了", "崩了", "坏了没",
      "完蛋没", "完蛋", "出问题", "不行了"],
     "状态", 5),

    # ── 共生体：共生/矩阵词 + 询问词 → 共生体状态 ──
    ("共生体状态",
     ["共生体", "共生", "知识矩阵", "神经网络", "矩阵", "网络"],
     ["怎么样", "好不好", "正常", "跑着没", "活着没", "看看", "看下", "查下", "状态", "啥情况", "咋样"],
     "共生体状态", 0),

    # ── 令牌续期：令牌词 + 到期/续期词 → 续令牌 ──
    ("令牌续期",
     ["令牌", "token", "密钥", "key", "口令", "凭证", "票"],
     ["过期", "到期", "快到了", "没了", "该续", "续期", "续上", "续一下", "更新", "刷新", "延期", "该续了"],
     "令牌管理 renew", 0),

    # ── 令牌查看：令牌词 + 查看词 → 看令牌 ──
    ("令牌状态",
     ["令牌", "token", "密钥", "key", "口令", "凭证"],
     ["看看", "看下", "查下", "怎么样", "还有多久", "状态", "情况", "在哪", "是啥"],
     "令牌管理 status", 0),

    # ── 启动：启动词 + 无否定 → 启动 ──
    ("启动",
     ["启动", "开始", "跑起来", "开机", "拉起", "打开", "开起来", "搞起来", "安排上", "整起来"],
     [],  # 不需要第二组
     "启动", 0),

    # ── 停止：停止词 → 停止 ──
    ("停止",
     ["停止", "停下", "关掉", "关机", "停掉", "结束", "不跑了", "别跑了", "停了吧", "收工"],
     [],
     "停止", 0),

    # ── 重启：重启词 → 重启 ──
    ("重启",
     ["重启", "重来", "重新启动", "刷新", "再来一遍", "重新跑"],
     [],
     "重启", 0),

    # ── 熔断相关 ──
    ("熔断状态",
     ["熔断", "断"],
     ["状态", "情况", "看看", "查下", "什么情况", "断了没", "还在断吗"],
     "熔断控制 status", 0),
    ("阻断",
     ["封", "禁", "屏蔽", "拉黑", "不让", "拦住", "挡"],
     ["域名", "IP", "地址", "网站", "那个", "这个"],
     "熔断控制 block", 0),
    ("解除阻断",
     ["解除", "取消", "放", "解封", "放开", "解锁"],
     ["阻断", "封禁", "屏蔽", "拉黑", "拦住", "禁了"],
     "熔断控制 unblock", 0),

    # ── 审计相关 ──
    ("审计",
     ["审计", "扫", "检查"],
     ["全面", "全体", "整个", "系统", "一遍", "一下", "一轮"],
     "审计", 0),
    ("审计日志",
     ["审计", "日志", "记录"],
     ["看看", "看下", "查下", "最近", "今天", "昨天", "这几天"],
     "审计日志", 0),

    # ── 黑天使军团漏洞检测 ──
    ("黑天使军团",
     ["黑天使", "黑客军团", "Black Angel"],
     [],
     "漏洞检测", 0),
    ("黑天使军团",
     ["红客", "红队", "白帽", "白帽子", "honker", "黑客"],
     [],
     "漏洞检测", 0),
    ("漏洞检测",
     ["漏洞", "找漏洞", "查漏洞", "扫描漏洞", "安全漏洞"],
     ["检测", "扫描", "找", "查", "看看", "扫"],
     "漏洞检测", 0),
    ("渗透测试",
     ["渗透", "渗透测试", "渗透验证", "安全检测", "攻防"],
     [],
     "漏洞检测", 0),
    ("注入检测",
     ["注入", "XSS", "CSRF", "SQL注入", "越权", "提权"],
     ["检测", "检查", "有没有", "是否存在"],
     "漏洞检测", 0),
    ("代码审计",
     ["代码审计", "静态分析", "依赖审计", "代码安全"],
     [],
     "漏洞检测", 0),
    ("威胁情报",
     ["威胁情报", "CVE", "0day", "APT", "暗网"],
     ["监控", "预警", "跟踪", "扫描"],
     "漏洞检测", 0),
    ("每日复盘",
     ["复盘", "回顾", "总结", "回头看看"],
     ["今天", "昨天", "每日", "一天", "一下"],
     "每日复盘", 0),

    # ── 编辑器 ──
    ("编辑器",
     ["编辑器", "写代码", "编程", "敲代码", "写程序"],
     [],
     "编辑器", 0),
    ("编辑器",
     ["打开", "开"],
     ["编辑器", "中文编辑器", "CNSH编辑器"],
     "编辑器", 0),

    # ── 记忆/上下文 ──
    ("记忆",
     ["记忆", "归集", "收", "存", "归档"],
     ["日志", "记忆", "聊天", "记录", "多平台", "各平台"],
     "记忆", 0),
    ("上下文",
     ["上下文", "会话", "聊天记录", "刚才说了什么", "现在聊到哪", "说到哪了", "之前说的"],
     [],
     "上下文", 0),

    # ── 仪表盘 ──
    ("主控台",
     ["主控台", "主控", "总控台", "总控制台", "master control"],
     [],
     "主控台", 0),
    ("操作台",
     ["操作台", "控制台", "仪表盘", "看板", "大屏"],
     [],
     "操作台", 0),
    ("流场总控",
     ["流场总控", "流场控制台", "流场仪表盘", "flow control"],
     [],
     "流场总控", 0),

    # ── 流场协同 ──
    ("流场协同 状态",
     ["协同场", "流场协同", "协同"],
     ["看看", "状态", "怎么样", "还好吗", "如何", "检查", "查", "看"],
     "流场协同 状态", 0),
    ("流场协同 均衡",
     ["均衡", "五行", "团队", "协同"],
     ["吗", "不", "检查", "看看", "缺什么", "偏不偏", "偏吗"],
     "流场协同 均衡", 0),
    ("流场协同 冲突",
     ["冲突", "相克", "协同"],
     ["有没有", "检查", "检测", "谁和谁", "分析"],
     "流场协同 冲突", 0),
    ("流场协同 融合",
     ["融合", "协同", "集体", "融合指数"],
     ["怎么样", "看看", "得怎么样", "多少", "程度"],
     "流场协同 融合", 0),
    ("流场协同 报告",
     ["协同", "报告", "总览", "全貌"],
     ["出", "生成", "完整", "全面", "看看"],
     "流场协同 报告", 0),
    ("流场协同 任务",
     ["分工", "任务", "分配", "协作", "协同"],
     ["怎么", "谁", "谁来", "分一下", "派", "干什么"],
     "流场协同 任务", 0),

    # ── 八卦/玄学 ──
    ("八卦调度",
     ["八卦", "卦", "易经", "周易", "六十四卦", "乾坤", "太极", "阴阳"],
     ["看看", "算", "卜", "占", "测", "问", "查"],
     "八卦调度", 0),

    # ── 五行 ──
    ("五行校验",
     ["五行", "金木水火土", "属性"],
     ["看看", "查", "算", "属什么", "什么属性", "校验"],
     "五行校验", 0),

    # ── 签名/DNA ──
    ("签名",
     ["签名", "署名", "签字", "盖章", "落款"],
     [],
     "签名", 0),
    ("身份验证",
     ["身份", "我是谁", "验证", "核验", "确认身份"],
     [],
     "身份验证", 0),
    ("DNA验证",
     ["DNA", "追溯码", "签名码"],
     ["验证", "检查", "看看", "对一下"],
     "DNA验证", 0),

    # ── 帮助 ──
    ("帮助",
     ["帮助", "怎么用", "不会用", "咋整", "咋办", "怎么办", "搞不懂", "不会", "教", "帮我"],
     [],
     "帮助", 0),
    ("帮助",
     ["有哪些", "都有什么", "能干什么", "你会什么", "你都会啥", "有啥功能"],
     ["命令", "功能", "能力", "本事"],
     "帮助", 0),

    # ── 维权 ──
    ("维权",
     ["维权", "法律", "打官司", "纠纷", "权益", "老百姓"],
     ["帮助", "助手", "引擎", "工具", "帮忙", "怎么办"],
     "维权助手", 0),

    # ── 知识图谱 ──
    ("知识图谱",
     ["知识", "图谱", "知识库", "知识网", "脑图"],
     ["打开", "看看", "构建", "建"],
     "知识图谱", 0),

    # ── 自愈/修复 ──
    ("自愈",
     ["自愈", "自我修复", "自动修复", "自己修"],
     [],
     "自愈", 0),
    ("自愈",
     ["修复", "修", "治", "搞"],
     ["系统", "自动", "自己"],
     "自愈", 0),

    # ── 评估 ──
    ("评估",
     ["评估", "打分", "评价", "看看水平", "测测"],
     ["系统", "整体", "全局"],
     "评估", 0),

    # ── 已发布查看 ──
    ("已发布",
     ["发了", "发过", "发布过", "已发布"],
     ["哪些", "什么", "多少", "清单", "列表", "看看", "查"],
     "已发布", 0),

    # ── 隐私加密 ──
    ("隐私加密",
     ["加密", "解密", "上锁", "解锁"],
     ["文件", "日志", "数据", "内容"],
     "隐私加密", 0),

    # ── 声纹 ──
    ("声纹",
     ["声纹", "声音", "语音", "嗓音"],
     ["DNA", "身份", "锚定", "识别", "验证"],
     "声纹", 0),

    # ── 万年历 ──
    ("万年历",
     ["万年历", "日历", "日程", "安排", "今天干嘛", "有什么任务"],
     [],
     "万年历", 0),

    # ── 宪法 ──
    ("宪法",
     ["宪法", "规矩", "规则", "法则", "王法"],
     ["系统", "咱们", "龍魂"],
     "宪法", 0),

    # ── 记录器 ──
    ("记录器",
     ["记下来", "记录", "留痕", "存一下", "备忘"],
     [],
     "记录器", 0),
]


def _match_group(text: str, word_group: list) -> bool:  # type: ignore[type-arg]
    """一组词中至少一个命中（大小写不敏感，中英文混输兼容）"""
    if not word_group:
        return True
    text_lower = text.lower()
    return any(w.lower() in text_lower for w in word_group)


def _compound_intent_match(text: str) -> Optional[Dict[str, str]]:
    """
    口语复合意图匹配。
    输入不需要精确触发词，只要同时命中主语词群+动作词群就认。
    多个命中时取优先级更高的。
    """
    candidates = []
    for name, group_a, group_b, cmd, priority in COLLOQUIAL_COMPOUND:
        a_ok = _match_group(text, group_a)
        b_ok = _match_group(text, group_b)
        if a_ok and b_ok:
            candidates.append((name, cmd, priority))

    if not candidates:
        return None

    # 优先级降序（priority 小时优先 → 数值越大越优先）
    candidates.sort(key=lambda x: -x[2] if x[2] > 0 else x[2])
    best = candidates[0]
    # 找抽屉
    for d in CN_SEMANTIC_DRAWERS:
        if d["name"] == best[0]:
            return d
    return None


# 权威权重映射：authoritative=3, verified=2, unverified=1
_AUTHORITY_WEIGHT = {
    "authoritative": 3,
    "verified": 2,
    "unverified": 1,
}


def cn_semantic_match(text: str) -> Optional[Dict[str, str]]:
    """
    中文语义抽屉匹配。

    策略：
    1. 先找最长精确命中词（精准意图优先）
    2. 精确没命中 → 口语复合意图匹配（词+词组合推断）
    3. 复合也没命中 → 不匹配
    4. 多个命中时：先按触发词长度，再按权威权重分级
       - 同等长度下，authoritative > verified > unverified
       - 非权威来源自动降权，权威来源优先
    """
    # 第一层：精确触发词匹配（大小写不敏感）
    hits = []
    text_lower = text.lower()
    for drawer in CN_SEMANTIC_DRAWERS:
        for trigger in drawer["triggers"]:
            if trigger.lower() in text_lower:
                auth_w = _AUTHORITY_WEIGHT.get(drawer.get("authority", "unverified"), 1)
                hits.append((drawer, trigger, len(trigger), auth_w))

    if hits:
        # 按 (触发词长度, 权威权重) 降序排列
        hits.sort(key=lambda x: (-x[2], -x[3]))
        best = hits[0]
        # 如果最优触发词长度 ≤ 2 且有更长的，用更长的
        if best[2] <= 2 and len(hits) > 1:
            for drawer, trigger, tlen, auth_w in hits[1:]:
                if tlen > 2:
                    return drawer
        return best[0]

    # 第二层：口语复合意图匹配
    compound = _compound_intent_match(text)
    if compound:
        return compound

    return None


def cn_cache_match(text: str) -> Optional[str]:
    """中文缓存匹配"""
    if CACHE_FILE_CN.exists():
        try:
            cache = json.loads(CACHE_FILE_CN.read_text())
            for key, cmd in cache.get("mappings", {}).items():
                if key in text:
                    return cmd
        except Exception:
            pass
    return None


# ═══════════════════════════════════════════════════════════════
# 🤖 LLM 意图理解 — 口语/脏话/错别字/混乱输入的最后防线
# ═══════════════════════════════════════════════════════════════

# 可用的命令列表（给 LLM 做分类用）
CN_COMMAND_CATALOG = [
    {"name": "系统状态", "command": "状态", "desc": "查看系统运行状态、健康检查"},
    {"name": "共生体状态", "command": "共生体状态", "desc": "查看共生体/知识矩阵/神经网络"},
    {"name": "启动", "command": "启动", "desc": "启动核心服务"},
    {"name": "停止", "command": "停止", "desc": "停止核心服务"},
    {"name": "重启", "command": "重启", "desc": "重启核心服务"},
    {"name": "共生体启动", "command": "共生体", "desc": "启动共生体知识矩阵"},
    {"name": "熔断状态", "command": "熔断控制 status", "desc": "查看熔断状态"},
    {"name": "临时放行", "command": "熔断控制 override", "desc": "临时放行被阻断的域名/IP"},
    {"name": "阻断", "command": "熔断控制 block", "desc": "封禁/拉黑域名或IP"},
    {"name": "解除阻断", "command": "熔断控制 unblock", "desc": "解除封禁"},
    {"name": "全局熔断", "command": "熔断控制 trip", "desc": "紧急全部熔断"},
    {"name": "重置熔断", "command": "熔断控制 reset", "desc": "重置熔断状态"},
    {"name": "令牌状态", "command": "令牌管理 status", "desc": "查看令牌状态"},
    {"name": "令牌续期", "command": "令牌管理 renew", "desc": "续期/更新令牌"},
    {"name": "变量审计", "command": "变量审计", "desc": "审计CNSH变量"},
    {"name": "审计日志", "command": "审计日志", "desc": "查看审计日志"},
    {"name": "审计", "command": "审计", "desc": "全面审计"},
    {"name": "仓库审计", "command": "仓库审计", "desc": "仓库扫描审计"},
    {"name": "每日复盘", "command": "每日复盘", "desc": "每日回顾总结"},
    {"name": "系统校验", "command": "系统校验", "desc": "系统完整性校验"},
    {"name": "编辑器", "command": "编辑器", "desc": "打开中文代码编辑器"},
    {"name": "记忆", "command": "记忆", "desc": "归集整理记忆"},
    {"name": "上下文", "command": "上下文", "desc": "查看当前会话上下文"},
    {"name": "主控台", "command": "主控台", "desc": "打开龍魂主控台（路由矩阵·统一入口）"},
    {"name": "操作台", "command": "操作台", "desc": "打开龍魂操作台（记忆压缩·DNA存证·资产扫描）"},
    {"name": "流场总控", "command": "流场总控", "desc": "打开流场总控台（流场实时监控）"},
    {"name": "共生仪表盘", "command": "共生仪表盘", "desc": "3D可视化仪表盘"},
    {"name": "八卦调度", "command": "八卦调度", "desc": "易经八卦占卜调度"},
    {"name": "签名", "command": "签名", "desc": "给文件加署名"},
    {"name": "身份验证", "command": "身份验证", "desc": "验证身份"},
    {"name": "DNA验证", "command": "DNA验证", "desc": "DNA追溯码验证"},
    {"name": "河图DNA", "command": "河图DNA引擎", "desc": "生成DNA追溯码"},
    {"name": "发文", "command": "发文", "desc": "发布/同步文章到CSDN"},
    {"name": "notion同步", "command": "notion同步", "desc": "同步到Notion"},
    {"name": "已发布", "command": "已发布", "desc": "查看已发布文章清单"},
    {"name": "知识图谱", "command": "知识图谱", "desc": "知识图谱构建"},
    {"name": "公式对准表", "command": "公式对准表", "desc": "公式向量检索"},
    {"name": "全局索引", "command": "全局索引", "desc": "全局搜索"},
    {"name": "龍盾", "command": "龍盾", "desc": "安全防护"},
    {"name": "五行校验", "command": "五行校验", "desc": "五行属性校验"},
    {"name": "隐私加密", "command": "隐私加密", "desc": "文件加密/解密"},
    {"name": "plist校验", "command": "plist校验", "desc": "校验plist文件"},
    {"name": "自愈", "command": "自愈", "desc": "系统自我修复"},
    {"name": "评估", "command": "评估", "desc": "系统评估打分"},
    {"name": "协议盾", "command": "协议盾", "desc": "校验CNSH协议完整性"},
    {"name": "人格列表", "command": "人格列表", "desc": "列出所有AI人格"},
    {"name": "能力列表", "command": "能力列表", "desc": "列出所有能力"},
    {"name": "调度", "command": "调度", "desc": "指挥调度中心"},
    {"name": "帮助", "command": "帮助", "desc": "帮助信息"},
    {"name": "万年历", "command": "万年历", "desc": "日程任务管理"},
    {"name": "宪法", "command": "宪法", "desc": "显示系统宪法"},
    {"name": "神圣锁", "command": "神圣锁", "desc": "显示P0永恒锁"},
    {"name": "错误翻译", "command": "错误翻译", "desc": "翻译系统报错"},
    {"name": "维权", "command": "维权助手", "desc": "法律维权助手"},
    {"name": "声纹", "command": "声纹", "desc": "声纹DNA锚定"},
    {"name": "主干迭代", "command": "主干自我迭代", "desc": "系统自我更新"},
    {"name": "记录器", "command": "记录器", "desc": "实时记录留痕"},
    {"name": "身份定位", "command": "身份定位", "desc": "查看原世界身份定位总纲"},
    {"name": "七因子验证", "command": "七因子验证", "desc": "七因子行为密码学验证"},
    {"name": "国密加密", "command": "国密加密", "desc": "国密SM2/SM3/SM4加密引擎"},
    {"name": "DNA追溯", "command": "DNA追溯", "desc": "DNA追溯码生成与验证"},
    {"name": "API门关", "command": "API门关", "desc": "API主权门关四道关卡"},
    {"name": "未知", "command": "", "desc": "无法识别意图"},
]


# 模块级导入 model_router（避免每次 _llm_intent_parse 调用时重复导入）
_model_router: Any = None
try:
    from sovereignty.portal import model_router as _mr  # type: ignore[no-redef]
    _model_router = _mr
except ImportError:
    pass

# LLM 降级用的精简命令列表（只给名字，不给描述，让 LLM 凭名字选）
_LLM_COMMAND_NAMES = [
    "系统状态", "共生体状态", "启动", "停止", "重启", "共生体启动",
    "熔断状态", "临时放行", "阻断", "解除阻断", "全局熔断", "重置熔断",
    "令牌状态", "令牌续期",
    "审计", "审计日志", "变量审计", "仓库审计", "每日复盘", "系统校验",
    "编辑器", "记忆", "上下文",
    "全文压缩", "旧文回收", "归集归档", "DNA封装", "投喂净化", "召回", "时间胶囊",
    "主控台", "操作台", "流场总控", "共生仪表盘", "八卦调度",
    "红客漏洞检测", "黑天使军团",
    "签名", "身份验证", "DNA验证", "河图DNA",
    "发文", "notion同步", "已发布",
    "知识图谱", "公式对准表", "全局索引",
    "龍盾", "五行校验", "隐私加密", "协议盾",
    "plist校验", "自愈", "评估",
    "人格列表", "能力列表", "调度",
    "帮助", "万年历", "宪法", "神圣锁", "错误翻译",
    "维权", "声纹", "主干迭代", "记录器",
    "身份定位", "七因子验证", "国密加密", "DNA追溯", "API门关",
]
_LLM_COMMAND_NAMES_STR = "，".join(_LLM_COMMAND_NAMES)


def _llm_intent_parse(text: str) -> Optional[Dict[str, str]]:
    """
    把用户的原始口语/脏话/错别字输入丢给 LLM，让它判断意图。
    返回匹配到的抽屉 dict，或 None。

    设计哲学：不需要 LLM 理解每个命令的含义，只需要它从混乱输入中
    找出最接近的意图名。命令名本身就是中文，LLM 能理解。

    🔒 权威降权：LLM 结果如果是 unverified 来源，降低置信度，
       只有 authoritative/verified 的结果才直接采用。
    """
    if _model_router is None:
        return None

    system_prompt = (
        "判断用户意图。忽略脏话、语气词、错别字、语音识别错误。\n"
        "必须从以下选一个最接近的，只输出名字，不要解释：\n"
        + _LLM_COMMAND_NAMES_STR
    )

    try:
        req = _model_router.ChatRequest(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            provider="auto",
            temperature=0.0,
            max_tokens=16,
        )
        result = _model_router.chat(req)
        intent_name = (result.get("reply") or result.get("content") or "").strip()
    except Exception:
        return None

    if not intent_name:
        return None

    # 精确匹配
    for d in CN_SEMANTIC_DRAWERS:
        if d["name"] == intent_name:
            # 🔒 权威降权：unverified 来源在 LLM 层直接拒绝
            #    只有 authoritative / verified 的才走 LLM 兜底
            authority = d.get("authority", "unverified")
            if authority == "unverified":
                return None  # 非权威来源，LLM 不兜底
            return d

    # 模糊匹配（LLM 可能返回略有差异的名字）
    for d in CN_SEMANTIC_DRAWERS:
        if d["name"] in intent_name or intent_name in d["name"]:
            authority = d.get("authority", "unverified")
            if authority == "unverified":
                return None
            return d

    return None


def cn_parse(text: str) -> Tuple[Optional[str], Optional[str], str]:
    """
    中文轨解析：返回 (中文命令, 英文命令, 来源标记)

    三层降级：
    1. 语义抽屉精确匹配 → 快、准、不用调 LLM
    2. 口语复合意图匹配 → 词+词组合推断
    3. LLM 意图理解 → 口语/脏话/错别字/语音转文字的最后防线
    """
    # 1. 语义抽屉匹配
    match = cn_semantic_match(text)
    if match:
        cn_cmd = match["command"]
        en_cmd = CN_TO_EN.get(cn_cmd, cn_cmd)
        return cn_cmd, en_cmd, f"语义抽屉·{match['name']}"

    # 2. 缓存匹配
    cached = cn_cache_match(text)
    if cached:
        en_cmd = CN_TO_EN.get(cached, cached)
        return cached, en_cmd, "中文缓存"

    # 3. LLM 意图理解 — 口语/脏话/错别字/语音转文字的最后防线
    llm_match = _llm_intent_parse(text)
    if llm_match:
        cn_cmd = llm_match["command"]
        en_cmd = CN_TO_EN.get(cn_cmd, cn_cmd)
        return cn_cmd, en_cmd, f"LLM意图理解·{llm_match['name']}"

    return None, None, "无法识别"


# ═══════════════════════════════════════════════════════════════
# 🇺🇸 英文轨解析
# ═══════════════════════════════════════════════════════════════

def en_precision_match(text: str) -> Optional[str]:
    """英文精准匹配。多词输入时尝试最长匹配。"""
    text_lower = text.strip().lower()
    if text_lower in EN_PRECISION_COMMANDS:
        return EN_PRECISION_COMMANDS[text_lower]
    return None


def en_cache_match(text: str) -> Optional[str]:
    """英文缓存匹配"""
    if CACHE_FILE_EN.exists():
        try:
            cache = json.loads(CACHE_FILE_EN.read_text())
            text_lower = text.strip().lower()
            for key, cmd in cache.get("mappings", {}).items():
                if key == text_lower:
                    return cmd
        except Exception:
            pass
    return None


def en_parse(text: str) -> Tuple[Optional[str], Optional[str], str]:
    """
    英文轨解析：返回 (英文命令, 中文命令, 来源标记)

    🔒 界限：英文轨 ONLY 精准匹配。
    不精确 → 直接 unrecognized，不猜、不兜底、不降级。
    中文轨的 LLM/模糊福利，英文轨不享有。
    """
    # 1. 精准匹配
    cmd = en_precision_match(text)
    if cmd:
        cn_cmd = EN_TO_CN.get(cmd, cmd)
        return cmd, cn_cmd, "英文精准匹配"

    # 2. 缓存匹配
    cached = en_cache_match(text)
    if cached:
        cn_cmd = EN_TO_CN.get(cached, cached)
        return cached, cn_cmd, "英文缓存"

    # 🔒 英文轨到此为止。不降级、不猜、不调 LLM。
    return None, None, "unrecognized"


# ═══════════════════════════════════════════════════════════════
# 统一解析入口
# ═══════════════════════════════════════════════════════════════

def parse_command(text: str) -> Dict[str, Any]:
    """
    统一解析入口。自动检测语言，走对应轨道。

    🔒 中英分界（焊死·2026-07-06）：
       - 含任意中文字符 → 🇨🇳 中文轨（语义抽屉+复合匹配+LLM降级）
       - 纯英文/数字       → 🇺🇸 英文轨（精准匹配 only，不降级）
       - 两轨平行、不混、不污染
       - 英文轨不享受中文轨的模糊/LLM福利

    返回:
    {
        "input": 原始输入,
        "lang": "cn" | "en",
        "cn_command": 中文命令（纯中文）,
        "en_command": 英文命令（标准英文）,
        "source": 来源标记,
        "success": True/False,
    }
    """
    text = text.strip()

    if is_chinese_input(text):
        # 🇨🇳 中文轨
        cn_cmd, en_cmd, source = cn_parse(text)
        return {
            "input": text,
            "lang": "cn",
            "cn_command": cn_cmd,
            "en_command": en_cmd,
            "source": source,
            "success": cn_cmd is not None,
        }
    else:
        # 🇺🇸 英文轨
        en_cmd, cn_cmd, source = en_parse(text)
        return {
            "input": text,
            "lang": "en",
            "cn_command": cn_cmd,
            "en_command": en_cmd,
            "source": source,
            "success": en_cmd is not None,
        }


# ═══════════════════════════════════════════════════════════════
# 回显确认
# ═══════════════════════════════════════════════════════════════

def echo_confirm(result: Dict[str, Any]) -> bool:
    """语义回显确认"""
    lang_label = "🇨🇳 中文轨" if result["lang"] == "cn" else "🇺🇸 English Track"
    cn_cmd = result.get("cn_command") or "—"
    en_cmd = result.get("en_command") or "—"

    print(f"""
╔═══════════════════════════════════════════════════════════╗
║  🧠 龍魂语义解析 · 命令回显确认                           ║
╠═══════════════════════════════════════════════════════════╣
║  输入: {result['input'][:45]}
║  轨道: {lang_label: <44}║
║  来源: {result['source'][:45]}
║  中文命令: {cn_cmd[:43]}
║  英文命令: {en_cmd[:43]}
╠═══════════════════════════════════════════════════════════╣
║  输入 y 确认执行 / n 取消                                 ║
╚═══════════════════════════════════════════════════════════╝
""")
    try:
        ans = input("  → ").strip().lower()
        return ans in ("y", "yes", "是", "确认", "执行")
    except (EOFError, KeyboardInterrupt):
        return False


# ═══════════════════════════════════════════════════════════════
# 列出中文抽屉 / 英文命令
# ═══════════════════════════════════════════════════════════════

def list_drawers():
    """列出所有中文语义抽屉"""
    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║  🇨🇳 中文语义抽屉 — 随便说·模糊匹配·纯中文命令            ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    for d in CN_SEMANTIC_DRAWERS:
        triggers = "、".join(d["triggers"][:5])
        print(f"║  {d['name']:<12} → {d['command']:<16} 触发: {triggers}")
    print("╚═══════════════════════════════════════════════════════════╝")

    print("\n╔═══════════════════════════════════════════════════════════╗")
    print("║  🇺🇸 English Precision — exact match·standard commands     ║")
    print("╠═══════════════════════════════════════════════════════════╣")
    seen = set()
    for k, v in sorted(EN_PRECISION_COMMANDS.items()):
        if v not in seen:
            print(f"║  {k:<25} → {v}")
            seen.add(v)
    print("╚═══════════════════════════════════════════════════════════╝")


# ═══════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n用法:")
        print("  python3 bin/semantic_parser.py \"自然语言命令\"        # 解析并回显")
        print("  python3 bin/semantic_parser.py --auto \"命令\"         # 解析后直接返回结果")
        print("  python3 bin/semantic_parser.py --list                 # 列出所有抽屉与命令")
        print("  python3 bin/semantic_parser.py --echo \"结果\" --cmd \"命令\"  # 仅回显")
        sys.exit(0)

    # --list 列出所有抽屉
    if sys.argv[1] == "--list":
        list_drawers()
        return

    # --echo --cmd 模式
    if sys.argv[1] == "--echo":
        echo_text = sys.argv[2] if len(sys.argv) > 2 else ""
        cmd = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--cmd" else ""
        result = parse_command(echo_text)
        if result["success"]:
            echo_confirm(result)
        else:
            print(f"\n⚠️ 无法识别: {echo_text}")
        return

    # --auto 模式
    auto_exec = False
    text_idx = 1
    if sys.argv[1] == "--auto":
        auto_exec = True
        text_idx = 2

    text = " ".join(sys.argv[text_idx:])
    if not text.strip():
        print("❌ 请输入命令")
        sys.exit(1)

    result = parse_command(text)

    if not result["success"]:
        lang = "中文" if is_chinese_input(text) else "English"
        print(f"""
╔═══════════════════════════════════════════════════════════╗
║  ⚠️  语义解析失败 ({lang})                                    ║
║  输入: {text[:47]}
║  请使用 --list 查看所有可用抽屉与命令                      ║
╚═══════════════════════════════════════════════════════════╝
""")
        sys.exit(1)

    if auto_exec:
        # 输出 JSON 供脚本消费
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if echo_confirm(result):
            print(f"\n▶️ 中文命令: {result['cn_command']}")
            print(f"▶️ 英文命令: {result['en_command']}")
        else:
            print("❌ 已取消")
            sys.exit(1)


if __name__ == "__main__":
    main()
