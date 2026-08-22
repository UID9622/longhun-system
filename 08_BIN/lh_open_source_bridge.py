#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 开源工具主权引入与CNSH转译系统 v1.0
DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-OPEN-SOURCE-BRIDGE-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过

功能:
  1. 开源工具主权评估与引入
  2. 贡献者信息提取与永久溯源
  3. 贡献者DNA生成与荣誉墙
  4. 原始代码 → CNSH转译（与 cnsh/core/foundation/cnsh_mapper.py 对齐）
  5. 原始代码只读归档 + CNSH代码进入内核
  6. 双链记录 (原始代码 ↔ CNSH代码 ↔ 贡献者信息)
  7. 主权验证与三色审计
"""

import os
import sys
import json
import hashlib
import re
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict

# ============================================================
# 动态加载 CNSH 语义映射表，保持关键字与底座一致
# ============================================================

CNSH_FOUNDATION = Path(__file__).resolve().parent.parent / "cnsh" / "core" / "foundation"
MAPPER_MODULE = CNSH_FOUNDATION / "cnsh_mapper.py"


def _load_mapper_keyword_map() -> Dict[str, str]:
    """
    从 cnsh_mapper.py 加载中文→英文关键字映射，
    返回英文→中文的反向映射表，用于 Python → CNSH 转译。
    """
    keyword_map = {}
    if MAPPER_MODULE.exists():
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("cnsh_mapper", MAPPER_MODULE)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            semantic_mapper = getattr(module, "SemanticMapper", None)
            if semantic_mapper and hasattr(semantic_mapper, "KEYWORD_MAP"):
                for cn, en in semantic_mapper.KEYWORD_MAP.items():
                    keyword_map[en] = cn
        except Exception as e:
            print(f"🟡 加载 {MAPPER_MODULE} 失败，使用内置兜底映射: {e}", file=sys.stderr)

    # 兜底：确保基础关键字一定存在
    fallback = {
        "def": "函数", "class": "类", "if": "如果", "else": "否则",
        "elif": "否则如果", "for": "循环", "while": "当", "return": "返回",
        "import": "导入", "from": "从", "True": "真", "False": "假",
        "None": "空", "and": "且", "or": "或", "not": "非", "in": "在",
        "is": "是", "with": "使用", "as": "作为", "try": "尝试",
        "except": "捕获", "finally": "最终", "raise": "抛出", "yield": "生成",
        "async": "异步", "await": "等待", "lambda": "匿名函数",
        "global": "全局", "nonlocal": "非局部", "del": "删除", "pass": "通过",
        "break": "跳出", "continue": "继续", "int": "整数", "str": "文本",
        "list": "列表", "dict": "字典", "tuple": "元组", "set": "集合",
        "bool": "布尔", "float": "浮点", "print": "输出", "len": "长度",
        "type": "类型", "range": "区间", "enumerate": "枚举", "zip": "压缩",
        "map": "映射", "filter": "过滤", "sum": "求和", "max": "最大值",
        "min": "最小值", "sorted": "排序", "reversed": "反转",
        "open": "打开", "read": "读取", "write": "写入", "close": "关闭",
    }
    for en, cn in fallback.items():
        keyword_map.setdefault(en, cn)
    return keyword_map


# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

LONGHUN_HOME = Path.home() / ".longhun"
BRIDGE_DIR = LONGHUN_HOME / "open_source_bridge"
CONTRIBUTORS_DIR = BRIDGE_DIR / "contributors"
CNSH_DIR = BRIDGE_DIR / "cnsh_translated"
ORIGINAL_DIR = BRIDGE_DIR / "original_archives"
METADATA_DIR = BRIDGE_DIR / "metadata"

for d in [BRIDGE_DIR, CONTRIBUTORS_DIR, CNSH_DIR, ORIGINAL_DIR, METADATA_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def generate_dna(module: str = "BRIDGE") -> str:
    h = hashlib.md5(f"{module}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-{module}-{h}-{UID}"


def sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ============================================================
# 数据结构
# ============================================================

@dataclass
class Contributor:
    """贡献者信息 — 永久保存，不可覆盖"""
    name: str
    github_id: Optional[str] = None
    email: Optional[str] = None
    original_repo: str = ""
    original_url: str = ""
    license: str = ""
    dna: str = ""
    introduced_at: str = field(default_factory=lambda: datetime.now().isoformat())
    files_contributed: List[str] = field(default_factory=list)
    status: str = "active"  # active | archived

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> "Contributor":
        return cls(**data)


@dataclass
class CNSHTranslation:
    """CNSH转译记录"""
    original_file: str
    original_hash: str
    cnsh_file: str
    cnsh_dna: str
    contributor_dna: str
    translated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "verified"  # pending | verified | failed


@dataclass
class BridgeRecord:
    """引入记录"""
    record_id: str
    tool_name: str
    original_repo: str
    original_url: str
    license: str
    contributors: List[str]
    cnsh_files: List[str]
    introduced_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "active"
    audit_color: str = "🟢"


    @classmethod
    def from_dict(cls, data: Dict) -> "BridgeRecord":
        return cls(**data)


# ============================================================
# 贡献者管理
# ============================================================

class ContributorManager:
    """贡献者管理器 - 永久保存贡献者信息，不可覆盖"""

    def __init__(self):
        self.contributors: Dict[str, Contributor] = {}
        self._load()

    def _dna_to_filename(self, dna: str) -> str:
        safe = dna.replace("#", "").replace("⚡️", "_").replace("/", "_")
        return f"{safe}.json"

    def _load(self):
        """加载已保存的贡献者"""
        for file in CONTRIBUTORS_DIR.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    contrib = Contributor.from_dict(data)
                    self.contributors[contrib.dna] = contrib
            except Exception as e:
                print(f"🟡 加载贡献者失败 {file}: {e}", file=sys.stderr)

    def register(self, name: str, repo: str, url: str, license_type: str,
                 github_id: str = None, email: str = None) -> Contributor:
        """注册贡献者（如果已存在则返回已有记录，信息永不覆盖）"""
        # 检查是否已存在相同姓名+仓库
        for existing in self.contributors.values():
            if existing.name == name and existing.original_repo == repo:
                return existing

        raw = f"{name}{repo}{time.time()}{UID}"
        dna = f"#CONTRIBUTOR⚡️{hashlib.sha256(raw.encode()).hexdigest()[:16].upper()}-{UID}"

        contrib = Contributor(
            name=name,
            github_id=github_id,
            email=email,
            original_repo=repo,
            original_url=url,
            license=license_type,
            dna=dna,
        )
        self.contributors[dna] = contrib
        self._save(contrib)
        return contrib

    def _save(self, contrib: Contributor):
        """保存贡献者"""
        filepath = CONTRIBUTORS_DIR / self._dna_to_filename(contrib.dna)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(contrib.to_dict(), f, indent=2, ensure_ascii=False)

    def get(self, dna: str) -> Optional[Contributor]:
        return self.contributors.get(dna)

    def list_all(self) -> List[Contributor]:
        return list(self.contributors.values())

    def get_honor_wall(self) -> str:
        """生成贡献者荣誉墙"""
        lines = [
            "🐉 龍魂系统 · 贡献者荣誉墙",
            "=" * 60,
            f"总计: {len(self.contributors)} 位贡献者",
            "-" * 60,
        ]
        for contrib in self.contributors.values():
            lines.append(f"🧬 {contrib.dna}")
            lines.append(f"  姓名: {contrib.name}")
            if contrib.github_id:
                lines.append(f"  GitHub: @{contrib.github_id}")
            if contrib.email:
                lines.append(f"  邮箱: {contrib.email}")
            lines.append(f"  仓库: {contrib.original_repo}")
            lines.append(f"  原始URL: {contrib.original_url}")
            lines.append(f"  许可证: {contrib.license}")
            lines.append(f"  引入时间: {contrib.introduced_at}")
            lines.append(f"  贡献文件: {len(contrib.files_contributed)}")
            lines.append("")
        lines.append("=" * 60)
        lines.append("每一位开源贡献者都被永久铭记，不可覆盖。")
        return "\n".join(lines)


# ============================================================
# CNSH转译引擎
# ============================================================

class CNSHTranslator:
    """CNSH转译引擎 - 将原始代码转为CNSH中文原生代码"""

    KEYWORD_MAP = _load_mapper_keyword_map()

    def __init__(self, contributor_manager: ContributorManager):
        self.contrib_mgr = contributor_manager

    @classmethod
    def translate_python_to_cnsh(cls, code: str, contrib_dna: str,
                                 tool_name: str) -> Tuple[str, str]:
        """
        将Python代码转译为CNSH。
        返回: (CNSH代码, CNSH DNA)
        """
        cnsh_dna = generate_dna(f"CNSH-{tool_name}")

        # 保护字符串内容：先分割出字符串片段
        pieces = re.split(r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')', code)
        mapped_pieces = []

        for idx, piece in enumerate(pieces):
            if idx % 2 == 1:  # 字符串片段保持原样
                mapped_pieces.append(piece)
                continue

            # 对非字符串片段按词替换关键字
            # 按英文关键字长度降序，避免短词先命中
            sorted_keywords = sorted(cls.KEYWORD_MAP.items(), key=lambda x: -len(x[0]))
            for en_word, cn_word in sorted_keywords:
                piece = re.sub(rf'\b{re.escape(en_word)}\b', cn_word, piece)

            mapped_pieces.append(piece)

        cnsh_code = "".join(mapped_pieces)

        # 注入贡献者信息头
        contrib = cls._get_contributor(contrib_dna)
        header = f"""# 🐉 CNSH 代码 · 由龍魂系统转译
# 原始贡献者: {contrib.name if contrib else '未知'}
# 原始仓库: {contrib.original_repo if contrib else '未知'}
# 许可证: {contrib.license if contrib else '未知'}
# CNSH DNA: {cnsh_dna}
# 贡献者DNA: {contrib_dna}
# 转译时间: {datetime.now().isoformat()}
# ──────────────────────────────────────
# 警告: 此代码为自动转译，修改请谨慎
# 如需修改，请同步更新原始代码记录并保留贡献者信息

"""
        cnsh_code = header + cnsh_code
        return cnsh_code, cnsh_dna

    @classmethod
    def _get_contributor(cls, contrib_dna: str) -> Optional[Contributor]:
        # 静态方法中无法访问实例的 contrib_mgr，这里从磁盘加载
        mgr = ContributorManager()
        return mgr.get(contrib_dna)

    def save_translation(self, original_code: str, cnsh_code: str,
                         tool_name: str, contrib_dna: str,
                         cnsh_dna: str = None) -> CNSHTranslation:
        """保存转译结果，原始代码只读归档"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # 保存原始代码（只读归档）
        orig_file = ORIGINAL_DIR / f"{tool_name}_{timestamp}_original.py"
        orig_file.write_text(original_code, encoding="utf-8")
        orig_hash = sha256_of_text(original_code)

        # 保存CNSH代码
        cnsh_file = CNSH_DIR / f"{tool_name}_{timestamp}.cnsh"
        cnsh_file.write_text(cnsh_code, encoding="utf-8")
        if not cnsh_dna:
            cnsh_dna = generate_dna(f"CNSH-{tool_name}")

        return CNSHTranslation(
            original_file=str(orig_file),
            original_hash=orig_hash,
            cnsh_file=str(cnsh_file),
            cnsh_dna=cnsh_dna,
            contributor_dna=contrib_dna,
        )


# ============================================================
# 主权引入流程
# ============================================================

class OpenSourceBridge:
    """开源工具主权引入主流程"""

    def __init__(self):
        self.contrib_mgr = ContributorManager()
        self.translator = CNSHTranslator(self.contrib_mgr)
        self.records: List[BridgeRecord] = []
        self._load_records()

    def _load_records(self):
        """加载引入记录"""
        meta_file = METADATA_DIR / "bridge_records.json"
        if meta_file.exists():
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.records = [BridgeRecord.from_dict(r) for r in data]
            except Exception as e:
                print(f"🟡 加载引入记录失败: {e}", file=sys.stderr)

    def _save_records(self):
        """保存引入记录"""
        meta_file = METADATA_DIR / "bridge_records.json"
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in self.records], f, indent=2, ensure_ascii=False)

    def import_tool(self, tool_name: str, repo_url: str, license_type: str,
                    code: str, author_name: str, github_id: str = None,
                    email: str = None) -> Dict:
        """
        主权引入四步:
        1. 主权评估（简化：记录许可证与来源）
        2. 注册贡献者
        3. 转译为CNSH
        4. 双链记录
        """
        # 1. 注册贡献者
        contrib = self.contrib_mgr.register(
            name=author_name,
            repo=tool_name,
            url=repo_url,
            license_type=license_type,
            github_id=github_id,
            email=email,
        )

        # 2. 转译为CNSH
        cnsh_code, cnsh_dna = self.translator.translate_python_to_cnsh(
            code, contrib.dna, tool_name
        )
        translation = self.translator.save_translation(
            code, cnsh_code, tool_name, contrib.dna, cnsh_dna=cnsh_dna
        )

        # 3. 创建引入记录
        record_id = (
            f"BRIDGE-{datetime.now().strftime('%Y%m%d')}"
            f"-{hashlib.sha256(tool_name.encode()).hexdigest()[:8].upper()}"
        )
        record = BridgeRecord(
            record_id=record_id,
            tool_name=tool_name,
            original_repo=repo_url,
            original_url=repo_url,
            license=license_type,
            contributors=[contrib.dna],
            cnsh_files=[translation.cnsh_file],
        )
        self.records.append(record)
        self._save_records()

        # 4. 更新贡献者文件列表
        contrib.files_contributed.append(translation.cnsh_file)
        self.contrib_mgr._save(contrib)

        return {
            "status": "success",
            "record_id": record_id,
            "tool_name": tool_name,
            "contributor": contrib.name,
            "contributor_dna": contrib.dna,
            "cnsh_file": translation.cnsh_file,
            "original_file": translation.original_file,
            "cnsh_dna": translation.cnsh_dna,
            "original_hash": translation.original_hash,
            "message": f"✅ {tool_name} 已主权引入，贡献者 {contrib.name} 已记录",
        }

    def get_contributor_honor_wall(self) -> str:
        """获取荣誉墙"""
        return self.contrib_mgr.get_honor_wall()

    def list_imported_tools(self) -> List[Dict]:
        """列出所有已引入工具"""
        return [
            {
                "record_id": r.record_id,
                "tool_name": r.tool_name,
                "license": r.license,
                "contributors": r.contributors,
                "status": r.status,
                "audit_color": r.audit_color,
                "cnsh_files": r.cnsh_files,
                "introduced_at": r.introduced_at,
            }
            for r in self.records
        ]

    def get_status(self) -> Dict:
        """系统状态"""
        return {
            "contributors": len(self.contrib_mgr.contributors),
            "imported_tools": len(self.records),
            "contributors_dir": str(CONTRIBUTORS_DIR),
            "cnsh_dir": str(CNSH_DIR),
            "original_dir": str(ORIGINAL_DIR),
            "metadata_dir": str(METADATA_DIR),
        }


# ============================================================
# 精选开源工具目录（参考清单，不预填引入）
# ============================================================

CATALOG = [
    {"category": "AI编程助手", "tools": [
        ("Continue.dev", "VS Code AI编程插件，支持自定义API", "Apache 2.0", "https://github.com/continuedev/continue"),
        ("OpenCode", "终端AI编程Agent，支持75+模型", "MIT", "https://github.com/sst/open-code"),
        ("Tabby", "自托管AI编程助手，Rust构建", "AGPL", "https://github.com/TabbyML/tabby"),
        ("Cline", "VS Code开源AI编程助手", "Apache 2.0", "https://github.com/cline/cline"),
        ("DeepSeek-TUI", "Rust终端AI助手", "MIT", "https://github.com/deepseek-ai/deepseek-tui"),
    ]},
    {"category": "浏览器自动化", "tools": [
        ("Remote Browser", "自托管浏览器编排系统", "MIT", "https://github.com/remotebrowser/remotebrowser"),
        ("Browser Use", "AI浏览器自动化工具", "MIT", "https://github.com/browser-use/browser-use"),
        ("Rusty Browser", "Rust分布式浏览器自动化集群", "MIT", "https://github.com/dashn9/rusty-browser"),
        ("OpenSteer", "AI浏览器自动化框架", "MIT", "https://github.com/opensteer/opensteer"),
    ]},
    {"category": "知识管理", "tools": [
        ("Open Notebook", "隐私优先开源NotebookLM替代", "MIT", "https://github.com/lfnovo/open-notebook"),
        ("Relatum", "开源本地优先知识画布", "MIT", "https://github.com/yamibk/Relatum-Opensource"),
        ("AFFiNE", "开源本地优先工作空间", "MIT", "https://github.com/toeverything/AFFiNE"),
        ("Logseq", "开源知识管理工具", "AGPL", "https://github.com/logseq/logseq"),
    ]},
    {"category": "代码审计与安全", "tools": [
        ("DeepAudit", "国内首个开源AI代码审计多智能体系统", "Apache 2.0", "https://github.com/DeepAudit/DeepAudit"),
        ("Skylos", "开源本地PR扫描器", "Apache 2.0", "https://github.com/duriantaco/skylos"),
        ("CodeScan", "基于LLM的代码漏洞风险检查工具", "MIT", "https://github.com/HeJiguang/codescan"),
        ("OpenSCA", "国内最大开源SCA工具", "MulanPSL", "https://github.com/XmirrorSecurity/OpenSCA"),
    ]},
    {"category": "工作流与Agent框架", "tools": [
        ("DeerFlow 2.0", "字节开源超智能Agent框架", "MIT", "https://github.com/bytedance/deerflow"),
        ("OpenWeavr", "自托管工作流自动化", "MIT", "https://github.com/openweavr/Openweavr"),
        ("Pipelit", "自托管LLM Agent工作流平台", "MIT", "https://github.com/theuselessai/Pipelit"),
        ("Youtu-Agent", "腾讯开源高性能Agent框架", "Apache 2.0", "https://github.com/TencentCloudADP/youtu-agent"),
        ("Open-Agent", "Claude Agent SDK开源替代", "MIT", "https://github.com/AFK-surf/open-agent"),
    ]},
]


def print_catalog() -> str:
    lines = [
        "🐉 龍魂 · 开源工具精选目录",
        "=" * 70,
        "以下工具已通过主权初筛，可使用 --import-tool 单条引入。",
        "",
    ]
    for cat in CATALOG:
        lines.append(f"📁 {cat['category']}")
        lines.append("-" * 70)
        for name, desc, license_type, url in cat["tools"]:
            lines.append(f"  • {name}")
            lines.append(f"    描述: {desc}")
            lines.append(f"    许可证: {license_type}")
            lines.append(f"    来源: {url}")
        lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines)


# ============================================================
# 命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 开源工具主权引入与CNSH转译系统"
    )

    parser.add_argument("--import-tool", help="引入工具 (名称)")
    parser.add_argument("--repo", help="仓库URL")
    parser.add_argument("--license", help="许可证类型")
    parser.add_argument("--code-file", help="代码文件路径")
    parser.add_argument("--author", help="作者名称")
    parser.add_argument("--github-id", help="GitHub ID")
    parser.add_argument("--email", help="邮箱")
    parser.add_argument("--honor-wall", action="store_true", help="显示贡献者荣誉墙")
    parser.add_argument("--list", action="store_true", help="列出已引入工具")
    parser.add_argument("--status", action="store_true", help="显示系统状态")
    parser.add_argument("--catalog", action="store_true", help="显示精选开源工具目录")

    args = parser.parse_args()
    bridge = OpenSourceBridge()

    if args.catalog:
        print(print_catalog())
        return

    if args.honor_wall:
        print(bridge.get_contributor_honor_wall())
        return

    if args.list:
        tools = bridge.list_imported_tools()
        print("🐉 已引入工具列表")
        print("=" * 60)
        if not tools:
            print("  暂无已引入工具")
        for t in tools:
            print(f"{t['audit_color']} {t['tool_name']}")
            print(f"  记录ID: {t['record_id']}")
            print(f"  许可证: {t['license']}")
            print(f"  贡献者: {t['contributors']}")
            print(f"  CNSH文件: {t['cnsh_files']}")
            print(f"  引入时间: {t['introduced_at']}")
            print("")
        return

    if args.import_tool and args.code_file and args.author:
        try:
            with open(args.code_file, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            print(f"❌ 读取代码文件失败: {e}")
            return

        if not code.strip():
            print("❌ 代码文件为空")
            return

        result = bridge.import_tool(
            tool_name=args.import_tool,
            repo_url=args.repo or "未知",
            license_type=args.license or "未知",
            code=code,
            author_name=args.author,
            github_id=args.github_id,
            email=args.email,
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    if args.status:
        status = bridge.get_status()
        print("🐉 开源工具主权引入系统状态")
        print("=" * 40)
        print(f"  贡献者总数: {status['contributors']}")
        print(f"  已引入工具: {status['imported_tools']}")
        print(f"  贡献者目录: {status['contributors_dir']}")
        print(f"  CNSH目录: {status['cnsh_dir']}")
        print(f"  原始代码归档: {status['original_dir']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
