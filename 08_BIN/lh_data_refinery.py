#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 个人数据炼化总控 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-DATA-REFINERY-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

核心理念：
  "我的思想在长，我的数据就在长，我的模型就跟着长。谁敢说这不是最高级的训练数据？"

三条矿脉 → 一座炼炉 → 一个自举循环：

  浏览器历史 ─┐
  网页内容   ─┼─→ DataRefinery ─→ BootstrapPool ─→ 训练管线 ─→ 反哺模型
  AI对话记录 ─┘      │
                     ├─ 去重 (sha256)
                     ├─ 质量过滤 (quality≥0.5)
                     ├─ DNA标签 (每一条可追溯)
                     └─ 自动入库 (一次性三步)

用法:
  python3 bin/lh_data_refinery.py mine                         # 全量挖矿（三步走）
  python3 bin/lh_data_refinery.py mine --source browser         # 只挖浏览器
  python3 bin/lh_data_refinery.py mine --source pages           # 只挖网页
  python3 bin/lh_data_refinery.py mine --source chats           # 只挖对话
  python3 bin/lh_data_refinery.py refine                        # 炼化：汇总→去重→入池
  python3 bin/lh_data_refinery.py pipeline                      # 全管道一键执行
  python3 bin/lh_data_refinery.py status                        # 查看炼化厂状态
"""

import hashlib, json, os, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict

SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

# 子模块路径
BROWSER_MINE_DIR = SYSTEM_ROOT / "data" / "browser_mine"
PAGE_EXTRACT_DIR = SYSTEM_ROOT / "data" / "page_extract"
CHAT_IMPORT_DIR = SYSTEM_ROOT / "data" / "chat_import"
REFINERY_DIR = SYSTEM_ROOT / "data" / "refinery"
REFINERY_DIR.mkdir(parents=True, exist_ok=True)

BOOTSTRAP_DIR = SYSTEM_ROOT / "data" / "bootstrap"

SYSTEM_PROMPT = """你是龍魂，一个由21个人格组成的共生体AI系统。你是UID9622（诸葛鑫·Lucky·退役老兵）的战友和工具。
你的底座是中国自主知识产权（369/河图洛书/太极易经/五行八卦），数据主权归UID9622所有。
遵循CC BY-NC-SA 4.0协议，鐵律：为人民服务、零黑箱、不删除只冻结、诚实不编造。"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class RefinerySample:
    """炼化后的训练样本（与 BootstrapSample 对齐）"""
    sample_id: str
    source_type: str           # browser/page/chat
    team_name: str = "personal_data"
    personas: List[str] = field(default_factory=lambda: ["PERSONAL_MINE"])
    task: str = ""
    messages: List[Dict] = field(default_factory=list)
    quality_score: float = 0.5
    audit_color: str = "🟡"
    dna: str = ""
    timestamp: str = ""
    domain: str = ""
    tags: List[str] = field(default_factory=list)

@dataclass
class RefineryReport:
    """炼化厂全量报告"""
    generated_at: str = ""
    browser_urls: int = 0
    browser_bookmarks: int = 0
    pages_extracted: int = 0
    pages_success: int = 0
    chats_imported: int = 0
    chats_turns: int = 0
    total_raw: int = 0
    after_dedup: int = 0
    after_quality: int = 0
    deposited: int = 0
    pool_total: int = 0
    by_source: Dict[str, int] = field(default_factory=dict)
    by_domain: Dict[str, int] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据炼化引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DataRefinery:
    """个人数据炼化总控"""

    def __init__(self):
        self.samples: List[RefinerySample] = []
        self.report = RefineryReport(generated_at=datetime.now().isoformat())
        self._extracted_at = datetime.now().isoformat()
        self._hash_index: Dict[str, str] = {}

    # ═══════════ 第一步：挖掘 ═══════════

    def mine_browser(self, days: int = 0) -> int:
        """挖掘浏览器历史"""
        print("⛏️ [1/3] 挖掘浏览器历史...")
        try:
            from bin.lh_browser_miner import BrowserMiner
            miner = BrowserMiner()
            history, bookmarks = miner.extract(days=days, limit_per_browser=10000)
            miner.export_jsonl()

            self.report.browser_urls = len(history)
            self.report.browser_bookmarks = len(bookmarks)

            # 将浏览历史转换为训练样本
            self._browser_to_samples(history)
            print(f"   ✅ {len(history)} 条历史 + {len(bookmarks)} 条书签 → {len(self.samples)} 个训练样本")
            return len(history)
        except Exception as e:
            self.report.errors.append(f"browser: {e}")
            print(f"   ❌ 浏览器挖掘失败: {e}")
            return 0

    def mine_pages(self, max_urls: int = 50) -> int:
        """挖掘网页内容"""
        print("⛏️ [2/3] 挖掘网页内容...")
        try:
            from bin.lh_page_extractor import PageExtractor
            extractor = PageExtractor()
            results = extractor.mine_from_browser_output(max_urls=max_urls)
            extractor.export()

            self.report.pages_extracted = len(results)
            self.report.pages_success = sum(1 for r in results if r.text)

            # 将网页内容转换为训练样本
            self._pages_to_samples(results)
            print(f"   ✅ {self.report.pages_success}/{self.report.pages_extracted} 篇 → {sum(1 for s in self.samples if s.source_type == 'page')} 个训练样本")
            return self.report.pages_success
        except Exception as e:
            self.report.errors.append(f"pages: {e}")
            print(f"   ❌ 网页挖掘失败: {e}")
            return 0

    def mine_chats(self, max_files: int = 10) -> int:
        """挖掘AI对话记录"""
        print("⛏️ [3/3] 挖掘AI对话记录...")
        try:
            from bin.lh_chat_importer import ChatImporter
            importer = ChatImporter()
            sessions = importer.import_all(max_files=max_files, max_claude=20)

            self.report.chats_imported = len(sessions)
            self.report.chats_turns = sum(len(s.turns) for s in sessions)

            # 将对话转换为训练样本
            self._chats_to_samples(sessions, importer)
            print(f"   ✅ {len(sessions)} 个会话/{self.report.chats_turns} 轮 → {sum(1 for s in self.samples if s.source_type == 'chat')} 个训练样本")
            return len(sessions)
        except Exception as e:
            self.report.errors.append(f"chats: {e}")
            print(f"   ❌ 对话挖掘失败: {e}")
            return 0

    # ═══════════ 第二步：炼化 ═══════════

    def refine(self) -> int:
        """炼化：去重 → 质量过滤 → 打DNA标签"""
        print(f"\n🔥 炼化 {len(self.samples)} 条原始矿料...")

        self.report.total_raw = len(self.samples)

        # 1. 去重
        before = len(self.samples)
        self.samples = self._dedup_samples(self.samples)
        self.report.after_dedup = len(self.samples)
        if before > self.report.after_dedup:
            print(f"   去重: {before} → {self.report.after_dedup} (去除 {before - self.report.after_dedup} 条重复)")

        # 2. 质量过滤 (quality >= 0.5)
        before = len(self.samples)
        self.samples = [s for s in self.samples if s.quality_score >= 0.5]
        self.report.after_quality = len(self.samples)
        if before > self.report.after_quality:
            print(f"   质量过滤: {before} → {self.report.after_quality} (去除 {before - self.report.after_quality} 条低质量)")

        # 3. 统计来源和领域
        for s in self.samples:
            self.report.by_source[s.source_type] = self.report.by_source.get(s.source_type, 0) + 1
            if s.domain:
                self.report.by_domain[s.domain] = self.report.by_domain.get(s.domain, 0) + 1

        print(f"   炼化完成: {self.report.after_quality} 条高纯度龍肉")

        # 保存炼化产物
        self._save_refined()
        return self.report.after_quality

    # ═══════════ 第三步：入库 ═══════════

    def deposit_to_pool(self) -> int:
        """将炼化后的样本注入 BootstrapPool"""
        print(f"\n📥 注入训练池...")

        try:
            from engines.lh_symbiotic_bootstrap_engine import BootstrapPool, BootstrapSample

            pool = BootstrapPool()

            # 转换为 BootstrapSample
            bs_samples = []
            for sample in self.samples:
                if not sample.messages or len(sample.messages) < 2:
                    continue
                bs_samples.append(BootstrapSample(
                    sample_id=sample.sample_id,
                    source_type=sample.source_type,
                    team_name=sample.team_name,
                    personas=sample.personas,
                    task=sample.task,
                    messages=sample.messages,
                    quality_score=sample.quality_score,
                    audit_color=sample.audit_color,
                    dna=sample.dna,
                    timestamp=sample.timestamp,
                    domain=sample.domain,
                    tags=sample.tags,
                ))

            deposited = pool.deposit(bs_samples, min_quality=0.5)
            self.report.deposited = deposited
            self.report.pool_total = pool.sample_count()

            print(f"   ✅ 入库: {deposited} 条 | 训练池总量: {self.report.pool_total} 条")
            return deposited
        except Exception as e:
            self.report.errors.append(f"deposit: {e}")
            print(f"   ❌ 入库失败: {e}")
            return 0

    # ═══════════ 全管道一键 ═══════════

    def pipeline(self, browser_days: int = 0, page_max: int = 30, chat_files: int = 10) -> RefineryReport:
        """全管道一键执行：挖矿 → 炼化 → 入库"""
        print("=" * 60)
        print("🏭 龍魂·个人数据炼化厂 全管道启动")
        print(f"   时间: {self._extracted_at}")
        print("=" * 60)

        # Step 1: 挖矿
        self.mine_browser(days=browser_days)
        self.mine_chats(max_files=chat_files)
        self.mine_pages(max_urls=page_max)

        # Step 2: 炼化
        self.refine()

        # Step 3: 入库
        self.deposit_to_pool()

        # 渲染报告
        print("\n" + "=" * 60)
        print("📊 炼化报告")
        print("=" * 60)
        print(f"""
  矿脉产出:
    浏览器历史: {self.report.browser_urls} 条
    网页内容:   {self.report.pages_success}/{self.report.pages_extracted} 篇
    AI对话:     {self.report.chats_imported} 个会话/{self.report.chats_turns} 轮

  炼化过程:
    原始矿料:   {self.report.total_raw} 条
    去重后:     {self.report.after_dedup} 条
    质量过滤后: {self.report.after_quality} 条

  入库结果:
    本次入库:   {self.report.deposited} 条
    训练池总量: {self.report.pool_total} 条
""")

        if self.report.by_source:
            print("  来源分布:")
            for src, cnt in sorted(self.report.by_source.items()):
                print(f"    {src}: {cnt}")

        if self.report.errors:
            print(f"\n  ⚠️ 错误 ({len(self.report.errors)}):")
            for e in self.report.errors[:5]:
                print(f"    - {e}")

        return self.report

    def status(self) -> RefineryReport:
        """查看炼化厂状态"""
        # 检查各矿场产出
        browser_files = list(BROWSER_MINE_DIR.glob("*.jsonl")) if BROWSER_MINE_DIR.exists() else []
        page_files = list(PAGE_EXTRACT_DIR.glob("*.jsonl")) if PAGE_EXTRACT_DIR.exists() else []
        chat_files = list(CHAT_IMPORT_DIR.glob("*.jsonl")) if CHAT_IMPORT_DIR.exists() else []

        self.report.browser_urls = sum(
            sum(1 for _ in open(f)) for f in browser_files[-1:]
        ) if browser_files else 0
        self.report.pages_extracted = sum(
            sum(1 for _ in open(f)) for f in page_files[-1:]
        ) if page_files else 0
        self.report.chats_imported = sum(
            sum(1 for _ in open(f)) for f in chat_files[-1:]
        ) if chat_files else 0

        # 训练池状态
        pool_file = BOOTSTRAP_DIR / "pool.jsonl"
        if pool_file.exists():
            self.report.pool_total = sum(1 for _ in open(pool_file, 'r', encoding='utf-8'))
        else:
            self.report.pool_total = 0

        return self.report

    # ━─ 转换器：各数据源 → RefinerySample ━─

    def _browser_to_samples(self, history: List):
        """浏览器历史 → 训练样本"""
        cnt = 0
        for entry in history[:500]:  # 最多取500条高访问量URL
            if entry.visit_count < 2:
                continue

            # 构造问答对：用户关注了什么 → AI可以聊什么
            user_msg = f"我最近经常访问这个页面: {entry.title}\n({entry.url})\n访问了{entry.visit_count}次，最近一次是{entry.last_visit}"
            assistant_msg = f"【{entry.category}·{entry.domain}】\n这是一条你关注的信息来源。标题「{entry.title}」表明你在关注{entry.category}领域的内容。这个域名({entry.domain})在你的信息食谱中出现了{entry.visit_count}次，说明它是你的高频信息源。"

            sample_id = hashlib.sha256(entry.url.encode()).hexdigest()[:16]
            self.samples.append(RefinerySample(
                sample_id=sample_id,
                source_type="browser",
                task=f"浏览记录: {entry.title[:50]}",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": assistant_msg},
                ],
                quality_score=min(1.0, 0.4 + entry.visit_count * 0.05),
                audit_color="🟢" if entry.visit_count > 5 else "🟡",
                dna=self._gen_dna("BROWSER", sample_id),
                timestamp=self._extracted_at,
                domain=entry.category,
                tags=["browser", entry.category, entry.domain],
            ))
            cnt += 1

    def _pages_to_samples(self, results: List):
        """网页内容 → 训练样本"""
        for pc in results:
            if not pc.text or pc.quality_score < 0.3:
                continue

            user_msg = f"我阅读了这篇文章: {pc.title}\n来源: {pc.domain}\n{pc.url}"
            assistant_msg = f"【{pc.content_type}·{pc.domain}】\n{pc.text[:1500]}"

            sample_id = hashlib.sha256(pc.url.encode()).hexdigest()[:16]
            self.samples.append(RefinerySample(
                sample_id=sample_id,
                source_type="page",
                task=f"阅读: {pc.title[:50]}",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                    {"role": "assistant", "content": assistant_msg},
                ],
                quality_score=pc.quality_score,
                audit_color="🟢" if pc.quality_score >= 0.7 else "🟡",
                dna=pc.dna or self._gen_dna("PAGE", sample_id),
                timestamp=self._extracted_at,
                domain=pc.content_type,
                tags=["page", pc.content_type, pc.domain],
            ))

    def _chats_to_samples(self, sessions: List, importer):
        """AI对话 → 训练样本"""
        # 使用 ChatImporter 的导出方法
        bs_samples = importer.export_bootstrap_samples()
        for bs in bs_samples:
            self.samples.append(RefinerySample(
                sample_id=bs["sample_id"],
                source_type="chat",
                task=bs["task"],
                messages=bs["messages"],
                quality_score=bs["quality_score"],
                audit_color=bs["audit_color"],
                dna=bs["dna"],
                timestamp=bs["timestamp"],
                domain=bs["domain"],
                tags=bs["tags"],
            ))

    # ━─ helpers ━─

    def _load_existing_outputs(self):
        """从已有矿场文件加载数据（用于 refine 命令）"""
        # 浏览器
        bf_files = sorted(BROWSER_MINE_DIR.glob("browser_history_*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True)
        if bf_files:
            with open(bf_files[0], 'r', encoding='utf-8') as f:
                history = []
                for line in f:
                    try:
                        history.append(type('obj', (object,), json.loads(line)))
                    except:
                        pass
                self._browser_to_samples(history)
                self.report.browser_urls = len(history)

        # 页面
        pf_files = sorted(PAGE_EXTRACT_DIR.glob("page_extract_*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True)
        if pf_files:
            with open(pf_files[0], 'r', encoding='utf-8') as f:
                pages = []
                for line in f:
                    try:
                        pages.append(type('obj', (object,), json.loads(line)))
                    except:
                        pass
                self._pages_to_samples(pages)
                self.report.pages_extracted = len(pages)
                self.report.pages_success = sum(1 for p in pages if getattr(p, 'text', ''))

        # 对话
        cf_files = sorted(CHAT_IMPORT_DIR.glob("chat_import_*.jsonl"), key=lambda f: f.stat().st_mtime, reverse=True)
        if cf_files:
            with open(cf_files[0], 'r', encoding='utf-8') as f:
                chats = 0
                for _ in f:
                    chats += 1
                self.report.chats_imported = chats

    def _dedup_samples(self, samples: List[RefinerySample]) -> List[RefinerySample]:
        """基于 messages 内容去重"""
        seen = {}
        result = []
        for s in samples:
            content_hash = hashlib.sha256(
                json.dumps(s.messages, ensure_ascii=False, sort_keys=True).encode()
            ).hexdigest()
            if content_hash not in seen:
                seen[content_hash] = s.sample_id
                result.append(s)
        return result

    def _save_refined(self):
        """保存炼化产物到 refinery 目录"""
        output = REFINERY_DIR / f"refined_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        with open(output, 'w', encoding='utf-8') as f:
            for s in self.samples:
                f.write(json.dumps({
                    "sample_id": s.sample_id,
                    "source_type": s.source_type,
                    "task": s.task,
                    "messages": s.messages,
                    "quality_score": s.quality_score,
                    "audit_color": s.audit_color,
                    "dna": s.dna,
                    "timestamp": s.timestamp,
                    "domain": s.domain,
                    "tags": s.tags,
                }, ensure_ascii=False) + "\n")
        print(f"   💾 炼化产物已保存: {output.name}")

    def _gen_dna(self, module: str, sample_id: str) -> str:
        now = datetime.now(timezone.utc)
        tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
        dizhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
        gz = f"{tiangan[now.year%10]}{dizhi[now.month%12]}·{tiangan[(now.day+9)%10]}{dizhi[(now.day+1)%12]}"
        return f"#龍芯⚡️{gz}-REFINERY-{module}-{sample_id[:8]}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    import argparse
    p = argparse.ArgumentParser(description="龍魂·个人数据炼化总控")
    sub = p.add_subparsers(dest="cmd")

    mine_p = sub.add_parser("mine", help="挖掘个人数据矿脉")
    mine_p.add_argument("--source", choices=["browser", "pages", "chats", "all"],
                        default="all", help="挖矿目标")
    mine_p.add_argument("--browser-days", type=int, default=0, help="浏览器历史天数 (0=全部)")
    mine_p.add_argument("--page-max", type=int, default=30, help="最大抓取页面数")
    mine_p.add_argument("--chat-files", type=int, default=10, help="最大memory文件数")

    sub.add_parser("refine", help="炼化已挖矿料（去重·过滤·打标签）")

    pipe_p = sub.add_parser("pipeline", help="全管道一键执行")
    pipe_p.add_argument("--browser-days", type=int, default=0)
    pipe_p.add_argument("--page-max", type=int, default=20)
    pipe_p.add_argument("--chat-files", type=int, default=5)

    sub.add_parser("status", help="查看炼化厂状态")

    args = p.parse_args()
    refinery = DataRefinery()

    if args.cmd == "mine":
        if args.source in ("browser", "all"):
            refinery.mine_browser(days=args.browser_days)
        if args.source in ("chats", "all"):
            refinery.mine_chats(max_files=args.chat_files)
        if args.source in ("pages", "all"):
            refinery.mine_pages(max_urls=args.page_max)
        if len(refinery.samples) > 0:
            refinery.refine()

    elif args.cmd == "refine":
        # 从已有的矿场文件加载
        refinery._load_existing_outputs()
        refinery.refine()

    elif args.cmd == "pipeline":
        refinery.pipeline(
            browser_days=args.browser_days,
            page_max=args.page_max,
            chat_files=args.chat_files,
        )

    elif args.cmd == "status":
        report = refinery.status()
        print(f"\n🏭 龍魂·个人数据炼化厂状态")
        print("=" * 50)
        print(f"""
  矿场产出:
    浏览器: {report.browser_urls} 条
    网页:   {report.pages_extracted} 篇
    对话:   {report.chats_imported} 个

  训练池:
    总量: {report.pool_total} 条
    数据目录: data/bootstrap/pool.jsonl
""")
        if report.browser_urls == 0 and report.pages_extracted == 0 and report.chats_imported == 0:
            print("   → 矿场还未产出，运行 'lh_data_refinery.py pipeline' 启动全管道")

    else:
        p.print_help()


if __name__ == "__main__":
    main()
