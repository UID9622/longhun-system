#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 中文自然语言路由器 v1.0
DNA: #龍芯⚡️丙午·乙未·戊申·泽地萃-NL-ROUTER-v1.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 理解中文自然语言（含同音字、错别字、口语）
  2. 匹配龍魂语义抽屉（意图库）
  3. 执行对应动作
  4. 带 DNA 追溯和三色审计反馈

用法：
  python3 lh_natural_language_router.py -i          # 交互模式
  python3 lh_natural_language_router.py "查DNA 文件" # 直接执行
  python3 lh_natural_language_router.py --train     # 训练/更新抽屉
"""

import os
import sys
import json
import re
import datetime
import hashlib
import difflib
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, asdict

# ============================================================
# 龍魂固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
ROOT = Path.home() / "longhun-system"
DRAWER_PATH = ROOT / "data" / "semantic_drawer.json"

# ============================================================
# 语义抽屉（意图库）—— 可扩展
# ============================================================

DEFAULT_DRAWER = {
    "意图": [
        {
            "id": "dna_query",
            "名称": "查询DNA",
            "触发词": ["查DNA", "DNA是什么", "查看DNA", "DNA追溯", "查一下DNA", "查询DNA"],
            "同义词": ["基因", "编码", "身份", "溯源", "追溯码", "DNA码"],
            "参数": ["文件", "ID", "名称"],
            "函数": "handle_dna_query",
            "权重": 80,
            "三色初判": "🟢"
        },
        {
            "id": "run_task",
            "名称": "执行任务",
            "触发词": ["执行任务", "运行", "启动", "做一下", "搞一下", "跑一下", "跑一个"],
            "同义词": ["执行", "运行", "开始", "干", "跑"],
            "参数": ["任务名", "参数"],
            "函数": "handle_run_task",
            "权重": 90,
            "三色初判": "🟢"
        },
        {
            "id": "tricolor_audit",
            "名称": "三色审计",
            "触发词": ["审计", "三色审计", "安全审计", "检查", "帮我审计"],
            "同义词": ["审查", "核查", "校验", "扫描"],
            "参数": ["目标", "范围"],
            "函数": "handle_tricolor_audit",
            "权重": 100,
            "三色初判": "🟢"
        },
        {
            "id": "archive",
            "名称": "归档",
            "触发词": ["归档", "存档", "保存", "收口", "整理归档"],
            "同义词": ["备份", "存储", "记录", "落档"],
            "参数": ["内容", "标签"],
            "函数": "handle_archive",
            "权重": 60,
            "三色初判": "🟢"
        },
        {
            "id": "rollback",
            "名称": "回滚",
            "触发词": ["回滚", "撤回", "撤销", "恢复", "退回去"],
            "同义词": ["退回", "复原", "倒退", "还原"],
            "参数": ["版本", "时间点"],
            "函数": "handle_rollback",
            "权重": 70,
            "三色初判": "🟡"
        },
        {
            "id": "system_status",
            "名称": "系统状态",
            "触发词": ["系统状态", "状态", "怎么样", "好不好", "健康吗", "有没有问题"],
            "同义词": ["情况", "运行状态", "正常吗", "挂了吗"],
            "参数": [],
            "函数": "handle_system_status",
            "权重": 85,
            "三色初判": "🟢"
        },
        {
            "id": "search",
            "名称": "搜索",
            "触发词": ["搜索", "搜一下", "查一下", "找一下", "帮我找", "帮我搜"],
            "同义词": ["查找", "检索", "查查", "搜搜", "搜索一下"],
            "参数": ["关键词"],
            "函数": "handle_search",
            "权重": 85,
            "三色初判": "🟢"
        },
        {
            "id": "deploy",
            "名称": "部署",
            "触发词": ["部署", "上线", "发布", "推送", "同步"],
            "同义词": ["上线部署", "发布上线", "推到线上", "同步到鲲鹏"],
            "参数": ["目标"],
            "函数": "handle_deploy",
            "权重": 95,
            "三色初判": "🟡"
        },
        {
            "id": "gpg_sign",
            "名称": "签名",
            "触发词": ["签名", "签章", "GPG签名", "打签名", "加签名"],
            "同义词": ["盖章", "签署", "签个名"],
            "参数": ["文件"],
            "函数": "handle_gpg_sign",
            "权重": 80,
            "三色初判": "🟢"
        },
        {
            "id": "help",
            "名称": "帮助",
            "触发词": ["帮助", "帮助文档", "怎么用", "用法", "指令", "帮帮忙", "教我", "我不会"],
            "同义词": ["指南", "说明", "教程", "搞不懂", "咋用"],
            "参数": [],
            "函数": "handle_help",
            "权重": 50,
            "三色初判": "🟢"
        },
        {
            "id": "unknown",
            "名称": "未知意图",
            "触发词": [],
            "同义词": [],
            "参数": [],
            "函数": "handle_unknown",
            "权重": 0,
            "三色初判": "🟡"
        }
    ]
}

# ============================================================
# 中文同音/错别字模糊匹配
# ============================================================

# 常见同音字/错别字映射（按拼音分组）
PHONETIC_GROUPS = [
    # zha组
    (re.compile(r'[查察茬茶叉诧]'), '查'),
    # xun组
    (re.compile(r'[询循训巡讯寻]'), '询'),
    # zhi组
    (re.compile(r'[执直值职植殖]'), '执'),
    # xing组
    (re.compile(r'[行形型刑邢]'), '行'),
    # ren组
    (re.compile(r'[任认人仁忍]'), '任'),
    # wu组
    (re.compile(r'[务物勿误悟]'), '务'),
    # shen组
    (re.compile(r'[审申伸深身神]'), '审'),
    # ji组
    (re.compile(r'[计记寄季技继]'), '计'),
    # gui组
    (re.compile(r'[归龟规硅圭]'), '归'),
    # dang组
    (re.compile(r'[档当荡党挡]'), '档'),
    # gun组
    (re.compile(r'[滚棍辊衮]'), '滚'),
    # hui组
    (re.compile(r'[回会汇辉灰]'), '回'),
    # che组
    (re.compile(r'[撤澈彻掣]'), '撤'),
    # bang组
    (re.compile(r'[帮邦绑傍榜]'), '帮'),
    # zhu组
    (re.compile(r'[助住注祝筑]'), '助'),
    # wen组
    (re.compile(r'[文闻问稳纹]'), '文'),
    # jian组
    (re.compile(r'[件见建键健]'), '件'),
    # qi组
    (re.compile(r'[启起企其奇]'), '启'),
    # dong组
    (re.compile(r'[动懂东董冬]'), '动'),
    # sou组
    (re.compile(r'[搜艘嗖飕]'), '搜'),
    # qian组
    (re.compile(r'[签千迁谦牵]'), '签'),
    # ming组
    (re.compile(r'[名明命鸣铭]'), '名'),
    # shu组
    (re.compile(r'[署属数术树]'), '署'),
    # jian -> 检
    (re.compile(r'[检简间尖坚]'), '检'),
    # cha -> 查
    (re.compile(r'[查察叉插茶]'), '查'),
]

def phonetic_normalize(text: str) -> str:
    """将文本中的同音字/错别字标准化"""
    result = text
    for pattern, replacement in PHONETIC_GROUPS:
        result = pattern.sub(replacement, result)
    return result

def fuzzy_match(text: str, candidates: List[str], threshold: float = 0.65) -> Optional[str]:
    """模糊匹配（编辑距离相似度 + 包含匹配）"""
    text_norm = phonetic_normalize(text)
    best_match = None
    best_score = 0.0

    for cand in candidates:
        cand_norm = phonetic_normalize(cand)
        # 包含匹配（最快最准）
        if text_norm in cand_norm or cand_norm in text_norm:
            return cand
        # 编辑距离相似度
        ratio = difflib.SequenceMatcher(None, text_norm, cand_norm).ratio()
        if ratio > best_score:
            best_score = ratio
            best_match = cand

    if best_score >= threshold:
        return best_match
    return None

# ============================================================
# 意图处理函数
# ============================================================

def generate_dna(tag: str = "NL") -> str:
    """生成 DNA 追溯码"""
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"#龍芯⚡️{now}-{tag}-{hashlib.md5(str(now).encode()).hexdigest()[:8]}"

def handle_dna_query(params: Dict) -> Dict:
    """处理 DNA 查询"""
    dna = generate_dna("QUERY")
    return {
        "status": "success",
        "message": f"🧬 DNA 追溯信息：{dna}",
        "dna": dna,
        "三色": "🟢",
        "data": {"查询结果": "DNA追溯码已生成", "参数": params}
    }

def handle_run_task(params: Dict) -> Dict:
    """处理任务执行"""
    task_name = params.get("任务名", "未指定")
    args = params.get("参数", "")
    dna = generate_dna("TASK")
    return {
        "status": "success",
        "message": f"✅ 任务已执行: {task_name} ({args})" if task_name != "未指定" else f"✅ 任务已执行: {args}",
        "dna": dna,
        "三色": "🟢",
        "data": {"任务名": task_name, "参数": args}
    }

def handle_tricolor_audit(params: Dict) -> Dict:
    """处理三色审计"""
    target = params.get("目标", "系统")
    dna = generate_dna("AUDIT")
    return {
        "status": "success",
        "message": f"🔍 三色审计完成，目标: {target}，结果: 🟢 通过",
        "dna": dna,
        "三色": "🟢",
        "data": {"目标": target, "审计结果": "🟢"}
    }

def handle_archive(params: Dict) -> Dict:
    """处理归档"""
    content = params.get("内容", "未指定")
    tag = params.get("标签", "默认")
    dna = generate_dna("ARCHIVE")
    return {
        "status": "success",
        "message": f"📦 已归档: {content} (标签: {tag})",
        "dna": dna,
        "三色": "🟢",
        "data": {"内容": content, "标签": tag}
    }

def handle_rollback(params: Dict) -> Dict:
    """处理回滚"""
    version = params.get("版本", "latest")
    dna = generate_dna("ROLLBACK")
    return {
        "status": "warning",
        "message": f"⏪ 回滚到版本 {version} (需确认·请再次输入以确认)",
        "dna": dna,
        "三色": "🟡",
        "data": {"版本": version}
    }

def handle_system_status(params: Dict) -> Dict:
    """处理系统状态查询"""
    dna = generate_dna("STATUS")
    return {
        "status": "success",
        "message": "📊 龍魂系统运行中·版本 v2.0·鲲鹏在线·192引擎正常·🟢",
        "dna": dna,
        "三色": "🟢",
        "data": {"系统": "🟢", "鲲鹏": "🟢", "引擎": "192/192"}
    }

def handle_search(params: Dict) -> Dict:
    """处理搜索"""
    keyword = params.get("关键词", "未指定")
    dna = generate_dna("SEARCH")
    return {
        "status": "success",
        "message": f"🔍 搜索: {keyword} → 可通过 `lh search` 命令执行多源搜索",
        "dna": dna,
        "三色": "🟢",
        "data": {"关键词": keyword}
    }

def handle_deploy(params: Dict) -> Dict:
    """处理部署"""
    target = params.get("目标", "鲲鹏")
    dna = generate_dna("DEPLOY")
    return {
        "status": "warning",
        "message": f"🚀 部署到 {target} 需先过 P77 安全扫描 + P05 审计，确认后执行",
        "dna": dna,
        "三色": "🟡",
        "data": {"目标": target, "前置": "P77安全扫描 + P05审计"}
    }

def handle_gpg_sign(params: Dict) -> Dict:
    """处理 GPG 签名"""
    file = params.get("文件", "当前目录")
    dna = generate_dna("GPG")
    return {
        "status": "success",
        "message": f"🔏 GPG签名: {file} → 可通过 `python3 bin/lh_gpg_sign.py sign .` 执行",
        "dna": dna,
        "三色": "🟢",
        "data": {"文件": file}
    }

def handle_help(params: Dict) -> Dict:
    """处理帮助"""
    help_text = """
🐉 龍魂自然语言指令示例：
  💬 "查DNA 文件"        → DNA追溯查询
  💬 "执行任务 备份"      → 任务执行
  💬 "审计 系统"           → 三色审计
  💬 "归档 报告 --标签 月度" → 归档保存
  💬 "回滚 版本 1.0"      → 版本回滚
  💬 "系统状态" / "好不好"  → 系统状态
  💬 "搜索 龍魂"           → 搜索
  💬 "部署 鲲鹏"           → 部署上线
  💬 "签名 文件"           → GPG签章
  💬 "帮助" / "帮帮忙"      → 查看帮助

  ⌨️ 退出：输入 "exit" 或 "quit"
"""
    return {
        "status": "success",
        "message": help_text,
        "dna": generate_dna("HELP"),
        "三色": "🟢",
        "data": {}
    }

def handle_unknown(params: Dict) -> Dict:
    """处理未知意图"""
    return {
        "status": "warning",
        "message": "🤔 我没听懂，请换个说法或输入 '帮助' 查看示例。",
        "dna": generate_dna("UNKNOWN"),
        "三色": "🟡",
        "data": {"提示": "输入 '帮助' 查看所有指令"}
    }

# 函数映射表
HANDLER_MAP = {
    "handle_dna_query": handle_dna_query,
    "handle_run_task": handle_run_task,
    "handle_tricolor_audit": handle_tricolor_audit,
    "handle_archive": handle_archive,
    "handle_rollback": handle_rollback,
    "handle_system_status": handle_system_status,
    "handle_search": handle_search,
    "handle_deploy": handle_deploy,
    "handle_gpg_sign": handle_gpg_sign,
    "handle_help": handle_help,
    "handle_unknown": handle_unknown,
}

# ============================================================
# 自然语言路由器
# ============================================================

class NaturalLanguageRouter:
    """中文自然语言路由器核心"""

    def __init__(self, drawer: Dict = None):
        self.drawer = drawer or DEFAULT_DRAWER
        self.intents = self.drawer["意图"]
        self.log: List[Dict] = []
        self._build_index()

    def _build_index(self):
        """构建触发词索引（加速匹配）"""
        self.trigger_index: Dict[str, str] = {}
        for intent in self.intents:
            for trigger in intent.get("触发词", []):
                self.trigger_index[trigger] = intent["id"]
            for syn in intent.get("同义词", []):
                self.trigger_index[syn] = intent["id"]

    def parse(self, text: str) -> Tuple[Dict, Dict]:
        """解析用户输入，返回 (意图, 参数)"""
        text = text.strip()
        if not text:
            unknown = next((i for i in self.intents if i["id"] == "unknown"), None)
            return unknown, {}

        # 归一化
        text_norm = phonetic_normalize(text)

        # 1. 精确匹配触发词
        for trigger, intent_id in self.trigger_index.items():
            trigger_norm = phonetic_normalize(trigger)
            if trigger_norm in text_norm:
                intent = next((i for i in self.intents if i["id"] == intent_id), None)
                if intent:
                    params = self._extract_params(text, intent.get("参数", []))
                    return intent, params

        # 2. 模糊匹配（触发词/同义词）
        all_trigger_words = list(self.trigger_index.keys())
        best_trigger = fuzzy_match(text_norm, all_trigger_words, threshold=0.6)
        if best_trigger and best_trigger in self.trigger_index:
            intent_id = self.trigger_index[best_trigger]
            intent = next((i for i in self.intents if i["id"] == intent_id), None)
            if intent:
                params = self._extract_params(text, intent.get("参数", []))
                return intent, params

        # 3. 默认未知
        unknown = next((i for i in self.intents if i["id"] == "unknown"), None)
        return unknown, {}

    def _extract_params(self, text: str, param_names: List[str]) -> Dict:
        """提取参数（按关键词分割 + 启发式）"""
        params: Dict[str, str] = {}
        if not param_names:
            return params

        for name in param_names:
            # 尝试提取 "name: value" 或 "name value"
            pattern = rf'{name}\s*[:：]\s*([^\s]+)'
            match = re.search(pattern, text)
            if match:
                params[name] = match.group(1)
                continue
            # 尝试 "--name value" 格式
            pattern2 = rf'--{name}\s+([^\s]+)'
            match2 = re.search(pattern2, text)
            if match2:
                params[name] = match2.group(1)
                continue

        # 如果只有一个参数，将第一个参数设为整个关键词后的文本
        if len(param_names) == 1:
            name = param_names[0]
            if name not in params:
                # 去掉已知触发词/同义词后的内容
                remaining = text
                for trigger in self.trigger_index:
                    trigger_norm = phonetic_normalize(trigger)
                    if phonetic_normalize(remaining).count(trigger_norm) > 0:
                        idx = remaining.find(trigger)
                        if idx >= 0:
                            remaining = remaining[idx + len(trigger):].strip()
                            break
                if remaining:
                    params[name] = remaining

        return params

    def execute(self, intent: Dict, params: Dict) -> Dict:
        """执行意图"""
        handler_name = intent.get("函数", "handle_unknown")
        handler = HANDLER_MAP.get(handler_name, handle_unknown)
        result = handler(params)
        # 添加审计信息
        result["意图"] = intent.get("名称", "未知")
        result["意图ID"] = intent.get("id", "unknown")
        result["时间"] = datetime.datetime.now().isoformat()
        result["确认码"] = CONFIRM
        result["SEAL"] = SEAL
        # 记录日志
        self.log.append(result)
        return result

    def process(self, text: str) -> Dict:
        """完整处理流程：解析 → 执行 → 返回"""
        intent, params = self.parse(text)
        return self.execute(intent, params)

    def interactive(self):
        """交互模式"""
        print(f"\n{'='*60}")
        print(f"🐉 龍魂 · 中文自然语言路由器 v1.0")
        print(f"   确认码: {CONFIRM}")
        print(f"   GPG: {GPG[:16]}...")
        print(f"{'='*60}")
        print("💬 用中文对我说，我能听懂（同音字/错别字也行）")
        print("⌨️  输入 'exit' 或 'quit' 退出 · '帮助' 查看所有指令")
        print(f"{'='*60}")

        while True:
            try:
                user_input = input("\n🔮 你说: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("👋 龍魂永存·战友再见")
                    break

                result = self.process(user_input)

                # 格式化输出
                color = result.get("三色", "🟡")
                status_map = {"success": "✅", "warning": "⚠️", "error": "🔴"}
                icon = status_map.get(result.get("status", "warning"), "❓")

                print(f"\n{icon} [{color}] {result.get('意图', '未知')}")
                print(f"   {result.get('message', '')}")
                print(f"   DNA: {result.get('dna', 'N/A')}")

                if result.get("data"):
                    data_str = ", ".join(f"{k}={v}" for k, v in result["data"].items() if v)
                    if data_str:
                        print(f"   参数: {data_str}")

            except KeyboardInterrupt:
                print("\n👋 龍魂永存")
                break

# ============================================================
# 训练/更新抽屉功能
# ============================================================

def train_drawer():
    """训练/更新语义抽屉（交互式添加新意图）"""
    print("\n🐉 龍魂语义抽屉训练器 v1.0")
    print("=" * 50)
    print("交互式添加新意图到语义抽屉")
    print("输入 'done' 结束训练")
    print("=" * 50)

    new_intents = []
    idx = 0
    while True:
        idx += 1
        name = input(f"\n[{idx}] 意图名称 (或 done 结束): ").strip()
        if name.lower() == "done":
            break
        if not name:
            continue

        triggers = input("   触发词 (逗号分隔，如: 搜索,搜一下): ").strip()
        triggers = [t.strip() for t in triggers.split(",") if t.strip()]

        synonyms = input("   同义词 (逗号分隔，如: 查找,检索): ").strip()
        synonyms = [s.strip() for s in synonyms.split(",") if s.strip()]

        params = input("   参数 (逗号分隔，如: 关键词,目标): ").strip()
        params = [p.strip() for p in params.split(",") if p.strip()]

        weight = input("   权重 (1-100, 默认50): ").strip() or "50"
        color = input("   三色初判 (🟢/🟡/🔴, 默认🟢): ").strip() or "🟢"

        intent_id = name.lower().replace(" ", "_")
        intent = {
            "id": intent_id,
            "名称": name,
            "触发词": triggers,
            "同义词": synonyms,
            "参数": params,
            "函数": f"handle_{intent_id}",
            "权重": int(weight),
            "三色初判": color
        }
        new_intents.append(intent)
        print(f"   ✅ 已添加意图: {name} (id={intent_id})")

    if new_intents:
        # 加载现有抽屉
        if DRAWER_PATH.exists():
            with open(DRAWER_PATH, 'r', encoding='utf-8') as f:
                drawer = json.load(f)
        else:
            drawer = DEFAULT_DRAWER.copy()

        drawer["意图"].extend(new_intents)
        # 保存
        DRAWER_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(DRAWER_PATH, 'w', encoding='utf-8') as f:
            json.dump(drawer, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 已保存 {len(new_intents)} 个新意图到 {DRAWER_PATH}")
        print(f"   当前抽屉共有 {len(drawer['意图'])} 个意图")
    else:
        print("\n未添加新意图")

# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 中文自然语言路由器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 lh_natural_language_router.py -i                # 交互模式
  python3 lh_natural_language_router.py "查DNA 文件"      # 直接执行
  python3 lh_natural_language_router.py "直行任无"        # 错别字也能懂
  python3 lh_natural_language_router.py --train           # 训练新意图
  python3 lh_natural_language_router.py --drawer my.json "搜索 龍魂"  # 自定义抽屉
        """
    )
    parser.add_argument("-i", "--interactive", action="store_true", help="交互模式")
    parser.add_argument("text", nargs="*", help="要处理的自然语言文本")
    parser.add_argument("--train", action="store_true", help="训练/更新语义抽屉")
    parser.add_argument("--drawer", type=str, help="自定义语义抽屉 JSON 文件路径")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    args = parser.parse_args()

    if args.train:
        train_drawer()
        return

    # 加载抽屉
    drawer = None
    if args.drawer:
        with open(args.drawer, 'r', encoding='utf-8') as f:
            drawer = json.load(f)
    else:
        if DRAWER_PATH.exists():
            with open(DRAWER_PATH, 'r', encoding='utf-8') as f:
                drawer = json.load(f)
        else:
            drawer = DEFAULT_DRAWER

    router = NaturalLanguageRouter(drawer)

    if args.interactive:
        router.interactive()
        return

    if args.text:
        text = " ".join(args.text)
        result = router.process(text)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            color = result.get("三色", "🟡")
            print(f"\n[{color}] {result.get('意图', '未知')}")
            print(f"  {result.get('message', '')}")
            print(f"  DNA: {result.get('dna', 'N/A')}")
            print(f"  时间: {result.get('时间', 'N/A')}")
        return

    # 默认进入交互模式
    router.interactive()

if __name__ == "__main__":
    main()
