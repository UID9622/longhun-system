#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║     📥 龍魂·四类收纳→六层架构 自动映射引擎 v1.0                  ║
║                                                                  ║
║  协议: LH-PROTOCOL-INBOX-MAPPER-2026-0714-v1.0                  ║
║  来源: 融合架构 §5 · 四类收纳→六层信息流控制                     ║
║                                                                  ║
║  功能:                                                           ║
║    - 从inbox文件导入条目                                         ║
║    - 关键词自动匹配→建议目标层                                   ║
║    - 置信度≥0.85自动映射🟢                                      ║
║    - 置信度0.70-0.84建议复核🟡                                  ║
║    - 置信度<0.70需人工判定🔴                                    ║
║    - 输出未映射清单                                              ║
║                                                                  ║
║  DNA: #龍芯⚡️丙午·辛未·乙酉·亥时·INBOX-MAPPER-v1.0              ║
╚══════════════════════════════════════════════════════════════════╝

用法:
  python3 bin/lh_inbox_mapper.py --scan               # 扫描所有待映射条目
  python3 bin/lh_inbox_mapper.py --map-all             # 自动映射置信度≥0.85的
  python3 bin/lh_inbox_mapper.py --add "内容" --bucket "灵感碎片"  # 手动添加
  python3 bin/lh_inbox_mapper.py --status              # 查看映射状态
  python3 bin/lh_inbox_mapper.py --unmapped            # 列出所有未映射条目
  python3 bin/lh_inbox_mapper.py --report              # 生成映射报告
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / ".longhun" / "inbox"
STATE_DIR.mkdir(parents=True, exist_ok=True)
INBOX_DB = STATE_DIR / "inbox_items.json"
MAP_LOG = STATE_DIR / "mapping_log.jsonl"

DNA = "#龍芯⚡️丙午·辛未·乙酉·亥时·INBOX-MAPPER-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# ══════════════════════════════════════════════════════
# 六层架构定义
# ══════════════════════════════════════════════════════

LAYERS = {
    "L1": {
        "name": "核心架构层",
        "en": "System Core & Governance",
        "desc": "北辰母协议·铁律宪法·蚁群节点·三色审计·IW-ECB·芯片适配",
    },
    "L2": {
        "name": "人格协作层",
        "en": "Personas & Activation",
        "desc": "16/71人格矩阵·LU指令引擎·人格签章·红蓝对抗·融合引擎",
    },
    "L3": {
        "name": "太极进化系统",
        "en": "Evolution / Experiments",
        "desc": "沙盒推演·易经推演·哲学十维·新算法孵化·A/B测试·原型迭代",
    },
    "L4": {
        "name": "知识管理层",
        "en": "Knowledge & Data Governance",
        "desc": "知识图谱·语义注册表·万国算法仓库·论文库·文章库·Notion",
    },
    "L5": {
        "name": "数据管理层",
        "en": "Backups / Sync / APIs",
        "desc": "数据同步·备份策略·API网关·跨平台同步·L5时间轴归档",
    },
    "L6": {
        "name": "安全保护层",
        "en": "Identity / Tokens / Channels",
        "desc": "DNA身份·密钥管理·传送门认证·哨兵·GPG签章·黑名单·防抵赖",
    },
}

# ══════════════════════════════════════════════════════
# 四类收纳入口定义
# ══════════════════════════════════════════════════════

BUCKETS = {
    "系统规则": {"color": "🔵", "desc": "System Rules — 协议·治理·审计·配置"},
    "知识派系": {"color": "🟣", "desc": "Knowledge — 论文·文档·文化·哲学"},
    "操作日志": {"color": "🟠", "desc": "Operational — 执行·部署·故障·健康"},
    "灵感碎片": {"color": "🟢", "desc": "Inspiration — 想法·假设·草图·随手"},
}

# ══════════════════════════════════════════════════════
# 自动映射规则 (bucket, keywords) → (layer, base_confidence)
# ══════════════════════════════════════════════════════

MAP_RULES = [
    # 系统规则 → L1核心 / L6安全 / L5数据
    ("系统规则", ["协议", "宪法", "铁律", "治理", "芯片", "架构", "基础", "核心"], "L1", 0.95),
    ("系统规则", ["审计", "熔断", "合规", "访问控制", "权限", "加密"], "L6", 0.90),
    ("系统规则", ["备份", "同步", "API", "数据库", "存储", "恢复"], "L5", 0.85),
    ("系统规则", ["人格", "执行器", "调度", "签章"], "L2", 0.80),

    # 操作日志 → L2人格 / L5数据 / L6安全
    ("操作日志", ["人格", "签章", "红蓝", "对抗", "融合", "切换"], "L2", 0.90),
    ("操作日志", ["部署", "健康检查", "监控", "告警", "修复", "启动"], "L5", 0.85),
    ("操作日志", ["认证", "登录", "密钥", "签名", "GPG", "DNA"], "L6", 0.85),
    ("操作日志", ["同步", "备份", "归档", "导出", "导入"], "L5", 0.80),

    # 灵感碎片 → L3进化 / L4知识
    ("灵感碎片", ["推演", "沙盒", "实验", "假设", "新想法", "试试"], "L3", 0.85),
    ("灵感碎片", ["知识", "文章", "教程", "论文", "文档"], "L4", 0.75),
    ("灵感碎片", ["元世界", "传送门", "产品", "入口", "净土"], "L3", 0.80),
    ("灵感碎片", ["算法", "模型", "引擎", "优化", "新功能"], "L3", 0.78),

    # 知识派系 → L4知识 / L3进化
    ("知识派系", ["论文", "研究", "报告", "技术文档", "教程", "手册"], "L4", 0.95),
    ("知识派系", ["推演", "哲学", "文化", "易经", "道德经", "五行"], "L3", 0.80),
    ("知识派系", ["算法", "代码", "实现", "技术"], "L4", 0.85),
    ("知识派系", ["CNSH", "语义", "注册表", "术语", "命名"], "L4", 0.82),
]


@dataclass
class InboxItem:
    """一条inbox条目"""
    id: str = ""
    bucket: str = ""            # 四类收纳之一
    content: str = ""           # 内容
    source: str = ""            # 来源（公众号/手动/语音/邮件）
    target_layer: str = ""      # 映射目标层（空=未映射）
    confidence: float = 0.0     # 映射置信度
    audit_color: str = ""       # 三色：🟢/🟡/🔴
    status: str = "open"        # open/mapped/archived/rejected
    created_at: str = ""
    mapped_at: str = ""
    owner: str = ""             # 负责人
    next_action: str = ""       # 下一步操作
    tags: List[str] = field(default_factory=list)


class InboxMapper:
    """四类收纳 → 六层架构 映射引擎"""

    def __init__(self):
        self.items: Dict[str, InboxItem] = {}
        self.stats = {
            "total": 0, "mapped": 0, "unmapped": 0,
            "auto_green": 0, "suggest_yellow": 0, "manual_red": 0,
            "by_bucket": {}, "by_layer": {},
        }
        self._load()

    def _load(self):
        """从磁盘加载"""
        if INBOX_DB.exists():
            data = json.loads(INBOX_DB.read_text())
            for item_data in data.get("items", []):
                item = InboxItem(**item_data)
                self.items[item.id] = item
        self._refresh_stats()

    def _save(self):
        """持久化"""
        data = {
            "version": "1.0",
            "updated": datetime.now().isoformat(),
            "count": len(self.items),
            "items": [vars(item) for item in self.items.values()],
        }
        INBOX_DB.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def _log(self, action: str, item_id: str, detail: dict):
        """操作日志"""
        import time
        entry = {
            "ts": datetime.now().isoformat(),
            "action": action,
            "item_id": item_id,
            "detail": detail,
            "dna": DNA,
        }
        with open(MAP_LOG, "a") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def add(self, bucket: str, content: str, source: str = "manual") -> InboxItem:
        """添加新条目到inbox"""
        if bucket not in BUCKETS:
            raise ValueError(f"未知桶: {bucket}, 可用: {list(BUCKETS.keys())}")

        item = InboxItem(
            id=f"INBOX-{uuid.uuid4().hex[:8].upper()}",
            bucket=bucket,
            content=content,
            source=source,
            created_at=datetime.now().isoformat(),
        )

        # 立即尝试自动映射
        self._suggest_map(item)

        self.items[item.id] = item
        self._save()
        self._log("add", item.id, {"bucket": bucket, "len": len(content)})

        return item

    def _suggest_map(self, item: InboxItem) -> dict:
        """对单个条目建议目标层"""
        best = {"layer": None, "confidence": 0.0}

        for bucket, keywords, layer, base_conf in MAP_RULES:
            if bucket != item.bucket:
                continue
            hit_count = sum(1 for kw in keywords if kw in item.content)
            if hit_count > 0:
                # 命中1个关键词 → 75%基准分，每多1个+15%，上限100%
                adjusted = base_conf * min(0.75 + 0.15 * hit_count, 1.0)
                # 额外加分：命中比例高 → +0.05
                if hit_count >= len(keywords):
                    adjusted = min(adjusted + 0.05, 1.0)
                if adjusted > best["confidence"]:
                    best = {"layer": layer, "confidence": round(adjusted, 2)}

        item.confidence = best["confidence"]
        item.target_layer = best["layer"] or ""

        if best["confidence"] >= 0.85:
            item.audit_color = "🟢"
        elif best["confidence"] >= 0.70:
            item.audit_color = "🟡"
        else:
            item.audit_color = "🔴"

        return best

    def map_all_auto(self) -> Dict[str, int]:
        """自动映射所有置信度≥0.85的条目（🟢）"""
        results = {"mapped": 0, "skipped_yellow": 0, "skipped_red": 0}

        for item in self.items.values():
            if item.status != "open":
                continue

            self._suggest_map(item)

            if item.audit_color == "🟢":
                item.status = "mapped"
                item.mapped_at = datetime.now().isoformat()
                results["mapped"] += 1
                self._log("auto_map", item.id, {
                    "confidence": item.confidence,
                    "target": item.target_layer,
                })
            elif item.audit_color == "🟡":
                results["skipped_yellow"] += 1
            else:
                results["skipped_red"] += 1

        self._save()
        self._refresh_stats()
        return results

    def map_one(self, item_id: str, target_layer: str) -> bool:
        """手动映射单条"""
        if item_id not in self.items:
            return False
        if target_layer not in LAYERS:
            return False

        item = self.items[item_id]
        item.target_layer = target_layer
        item.status = "mapped"
        item.mapped_at = datetime.now().isoformat()
        item.confidence = 1.0  # 人工确认=100%置信
        item.audit_color = "🟢"

        self._save()
        self._log("manual_map", item_id, {"target": target_layer})
        self._refresh_stats()
        return True

    def get_unmapped(self) -> List[InboxItem]:
        """获取所有未映射条目"""
        return [item for item in self.items.values()
                if item.status == "open" or not item.target_layer]

    def get_by_bucket(self, bucket: str) -> List[InboxItem]:
        return [item for item in self.items.values() if item.bucket == bucket]

    def get_by_layer(self, layer: str) -> List[InboxItem]:
        return [item for item in self.items.values() if item.target_layer == layer]

    def _refresh_stats(self):
        """刷新统计"""
        items = list(self.items.values())
        self.stats["total"] = len(items)
        self.stats["mapped"] = sum(1 for i in items if i.status == "mapped")
        self.stats["unmapped"] = sum(1 for i in items if i.status != "mapped")
        self.stats["auto_green"] = sum(1 for i in items if i.audit_color == "🟢" and i.status == "mapped")
        self.stats["suggest_yellow"] = sum(1 for i in items if i.audit_color == "🟡" and not i.target_layer)
        self.stats["manual_red"] = sum(1 for i in items if i.audit_color == "🔴" and not i.target_layer)

        for bk in BUCKETS:
            self.stats["by_bucket"][bk] = sum(1 for i in items if i.bucket == bk)
        for lk in LAYERS:
            self.stats["by_layer"][lk] = sum(1 for i in items if i.target_layer == lk)

    def report(self) -> str:
        """生成映射报告"""
        self._refresh_stats()
        lines = [
            "",
            "╔══════════════════════════════════════════════╗",
            f"║  📊 四类收纳→六层架构 映射报告                    ║",
            "╠══════════════════════════════════════════════╣",
            f"║  总计: {self.stats['total']:>4d} 条  已映射: {self.stats['mapped']:>4d} 条  未映射: {self.stats['unmapped']:>4d} 条   ║",
            f"║  🟢自动: {self.stats['auto_green']:>4d}  🟡待审: {self.stats['suggest_yellow']:>4d}  🔴人工: {self.stats['manual_red']:>4d}        ║",
            "╠══════════════════════════════════════════════╣",
        ]

        lines.append("║  按入口桶:                                      ║")
        for bk, count in self.stats["by_bucket"].items():
            lines.append(f"║    {BUCKETS[bk]['color']} {bk}: {count} 条                                  ║")

        lines.append("╠══════════════════════════════════════════════╣")
        lines.append("║  按目标层:                                      ║")
        for lk, count in self.stats["by_layer"].items():
            lname = LAYERS[lk]["name"]
            lines.append(f"║    {lk} {lname}: {count} 条                         ║")

        lines.append("╠══════════════════════════════════════════════╣")

        # 未映射清单
        unmapped = self.get_unmapped()
        if unmapped:
            lines.append("║  未映射条目:                                    ║")
            for item in unmapped[:10]:
                short = item.content[:30].replace("\n", " ")
                lines.append(f"║    [{item.id}] {item.audit_color} {item.bucket[:2]} {short}...             ║")
            if len(unmapped) > 10:
                lines.append(f"║    ... 还有 {len(unmapped)-10} 条未显示                       ║")

        lines.extend([
            "╚══════════════════════════════════════════════╝",
            f"\nDNA: {DNA}",
        ])
        return "\n".join(lines)

    def export_unmapped_json(self, path: str = None) -> str:
        """导出未映射清单为JSON"""
        unmapped = self.get_unmapped()
        data = {
            "count": len(unmapped),
            "generated": datetime.now().isoformat(),
            "dna": DNA,
            "unmapped": [
                {
                    "id": i.id,
                    "bucket": i.bucket,
                    "content": i.content[:200],
                    "suggested_layer": i.target_layer or "N/A",
                    "confidence": i.confidence,
                    "audit_color": i.audit_color,
                    "created_at": i.created_at,
                }
                for i in unmapped
            ],
        }
        output = path or str(STATE_DIR / "unmapped_report.json")
        Path(output).write_text(json.dumps(data, ensure_ascii=False, indent=2))
        return output

    def seed_defaults(self):
        """播种默认条目（从现有项目文件采样）"""
        defaults = [
            # 系统规则类 — 已存在的协议
            ("系统规则", "北辰母协议v2.0 — 龍魂最高宪法，所有协议必须遵守", "sync"),
            ("系统规则", "三色审计机制自动化 — 绿🟢/黄🟡/红🔴分级执行与回滚", "sync"),
            ("系统规则", "国产芯片适配：鲲鹏920/LoongArch/麒麟9000S/昇腾910", "sync"),
            ("系统规则", "蚁群节点协议：P2P通信·信息素路由·四类蚂蚁角色", "sync"),
            ("系统规则", "数据主权保护：用户数据本地存储·网关不存消息", "sync"),

            # 操作日志类
            ("操作日志", "全人格矩阵P00-P72满编·16人格全部落地", "sync"),
            ("操作日志", "GPG签章登记册更新至109份签章", "sync"),
            ("操作日志", "语义统一注册表v3.1：420条目·自动同步守护", "sync"),
            ("操作日志", "健康检查守护进程已配置Bark推送+服务自愈", "sync"),
            ("操作日志", "红蓝对抗融合引擎v1.0上线·五阶段流程", "sync"),

            # 知识派系类
            ("知识派系", "IEEE论文9篇：CNSH×北辰·權重v2.1·治理v4.0·洛書369", "sync"),
            ("知识派系", "哲学资产：12域28公式·15命题·70+文件", "sync"),
            ("知识派系", "CNSH中文编程语言技术栈：编译器·运行时·编辑器", "sync"),
            ("知识派系", "拔水军体系v1.0：4引擎·5阶段·11条法律引用", "sync"),
            ("知识派系", "对外文章：懶的牢房全五篇·AI市場硬邏輯v2.0", "sync"),

            # 灵感碎片类
            ("灵感碎片", "元世界传送门iOS版：万年历+暗门+哨兵过滤", "manual"),
            ("灵感碎片", "1:1真实产品数字孪生：每件虚拟产品对应现实实物", "manual"),
            ("灵感碎片", "柜台AI跨文化强制说明：说漏算商家责任", "manual"),
            ("灵感碎片", "71人格扩展：元世界运营层24人+自动服务层24人", "manual"),
            ("灵感碎片", "公众号技术专栏启动：CNSH·算法·架构连载", "manual"),
        ]

        for bucket, content, source in defaults:
            if not any(i.content == content for i in self.items.values()):
                self.add(bucket, content, source)

        print(f"✅ 播种 {len(defaults)} 条默认inbox条目")


# ══════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="龍魂·四类收纳→六层架构 映射引擎")
    parser.add_argument("--init", action="store_true", help="初始化并播种默认条目")
    parser.add_argument("--scan", action="store_true", help="扫描所有条目并刷新映射建议")
    parser.add_argument("--map-all", action="store_true", help="自动映射所有🟢置信度条目")
    parser.add_argument("--add", type=str, help="添加新条目内容")
    parser.add_argument("--bucket", type=str, default="灵感碎片", help="条目分类（默认:灵感碎片）")
    parser.add_argument("--map-one", type=str, help="手动映射指定ID条目到指定层（格式: ID=层）")
    parser.add_argument("--status", action="store_true", help="查看映射状态")
    parser.add_argument("--unmapped", action="store_true", help="列出未映射条目")
    parser.add_argument("--report", action="store_true", help="生成完整映射报告")
    parser.add_argument("--export", type=str, help="导出未映射清单为JSON（可选路径）")

    args = parser.parse_args()
    mapper = InboxMapper()

    if args.init:
        mapper.seed_defaults()

    elif args.scan:
        for item in mapper.items.values():
            if item.status == "open":
                mapper._suggest_map(item)
        mapper._save()
        mapper._refresh_stats()
        print(f"✅ 扫描完成 — 总计{mapper.stats['total']}条, 🟢{mapper.stats['auto_green']}, 🟡{mapper.stats['suggest_yellow']}, 🔴{mapper.stats['manual_red']}")

    elif args.map_all:
        results = mapper.map_all_auto()
        print(f"✅ 自动映射完成 — 映射{results['mapped']}条, 跳过🟡{results['skipped_yellow']}条, 跳过🔴{results['skipped_red']}条")

    elif args.add:
        mapper.add(args.bucket, args.add)
        print(f"✅ 已添加 — bucket={args.bucket}")

    elif args.map_one:
        try:
            item_id, layer = args.map_one.split("=")
            if mapper.map_one(item_id.strip(), layer.strip()):
                print(f"✅ 已映射 {item_id} → {layer}")
            else:
                print(f"❌ 映射失败 — 检查ID和层名")
        except ValueError:
            print("❌ 格式错误，应使用: --map-one INBOX-ID=L1")

    elif args.unmapped:
        unmapped = mapper.get_unmapped()
        if unmapped:
            print(f"\n🔴 未映射条目 ({len(unmapped)} 条):\n")
            for item in unmapped:
                print(f"  [{item.id}] {item.audit_color} {BUCKETS[item.bucket]['color']} {item.content[:60]}")
                if item.target_layer:
                    print(f"       建议: {item.target_layer} (置信度: {item.confidence:.0%})")
        else:
            print("✅ 所有条目已映射！")

    elif args.status:
        mapper._refresh_stats()
        print(f"总计: {mapper.stats['total']} | 已映射: {mapper.stats['mapped']} | 未映射: {mapper.stats['unmapped']}")
        print(f"按桶: {mapper.stats['by_bucket']}")
        print(f"按层: {mapper.stats['by_layer']}")

    elif args.export:
        path = mapper.export_unmapped_json(args.export if args.export != "auto" else None)
        print(f"✅ 已导出到: {path}")

    elif args.report:
        print(mapper.report())

    else:
        # 默认：显示报告
        mapper._refresh_stats()
        if mapper.stats["total"] == 0:
            print("📭 Inbox为空。运行 --init 播种默认条目。")
        else:
            print(mapper.report())


if __name__ == "__main__":
    main()
