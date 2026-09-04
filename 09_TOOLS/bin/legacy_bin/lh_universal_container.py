#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂·万能摄入容器主引擎 v1.0
================================
任何设备·任何格式·任何来源 → 自动分解 → 权重触发 → 静默/联动 → 分销归档

DNA: #龍芯⚡️丙午·辛未·乙酉·壬午·䷄需-CONTAINER-ENGINE-v1.0
确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import os
import sys
import json
import hashlib
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto
from concurrent.futures import ThreadPoolExecutor, as_completed
import mimetypes

# ─── 项目根 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ─── 日志 ───
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(PROJECT_ROOT / 'logs' / 'container.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger('lh_container')


# ═══════════════════════════════════════════
# 基础数据结构
# ═══════════════════════════════════════════

class PrivacyLevel(Enum):
    """隐私等级 P0-P4"""
    P0_PUBLIC = 0      # 公开
    P1_INTERNAL = 1    # 内部
    P2_RESTRICTED = 2  # 受限
    P3_CONFIDENTIAL = 3 # 机密
    P4_PRIVATE = 4     # 私密


class TriggerAction(Enum):
    """触发动作"""
    SILENT_ARCHIVE = auto()   # 静默归档
    SILENT_PROCESS = auto()   # 静默处理
    COLLABORATIVE = auto()    # 联动协同
    NOTIFY_SUGGEST = auto()   # 通知建议
    MANUAL_FUSE = auto()      # 人工确认+熔断


class DecomLine(Enum):
    """8条分解线"""
    CODE = "code"               # 代码分解
    DOCUMENT = "document"       # 文档分解
    KNOWLEDGE_GRAPH = "kg"      # 知识图谱
    DECISION = "decision"       # 决策分解
    PERSONA = "persona"         # 人格分解
    SOVEREIGNTY = "sovereignty" # 主权分解
    TEMPORAL = "temporal"       # 时间分解
    CORRELATION = "correlation" # 关联分解


@dataclass
class IngestedItem:
    """摄入项"""
    source_path: str
    item_type: str           # file/dir/text/url/clipboard
    mime_type: str
    content_hash: str        # SHA256
    size_bytes: int
    ingested_at: str         # ISO 8601
    privacy_level: PrivacyLevel = PrivacyLevel.P0_PUBLIC
    dna_tag: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DecomResult:
    """单条分解线输出"""
    line: DecomLine
    confidence: float        # 0.0-1.0
    summary: str
    entities: List[str] = field(default_factory=list)
    relations: List[Tuple[str, str, str]] = field(default_factory=list)  # (主体, 关系, 客体)
    tags: List[str] = field(default_factory=list)
    weight: float = 0.0
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WeightedResult:
    """加权后的结果"""
    item: IngestedItem
    decom_results: List[DecomResult]
    combined_weight: float   # 综合权重
    digital_root: int        # 数字根 1-9
    gate1_identity: float    # 身份闸门系数
    gate2_rules: float       # 规则闸门系数
    gate3_ethics: float      # 伦理闸门系数
    jiugong_factor: float    # 九宫因子
    trigger_action: TriggerAction
    target_libraries: List[str]


# ═══════════════════════════════════════════
# 格式识别
# ═══════════════════════════════════════════

FORMAT_MAP = {
    # 代码
    "code": [".py", ".js", ".ts", ".swift", ".cpp", ".c", ".h", ".java", ".go", ".rs",
             ".cnsh", ".sh", ".bash", ".zsh", ".html", ".css", ".vue", ".jsx", ".tsx",
             ".rb", ".php", ".scala", ".kt", ".dart", ".lua", ".r", ".m", ".mm"],
    # 文档
    "doc": [".md", ".txt", ".pdf", ".doc", ".docx", ".rst", ".tex", ".odt", ".rtf",
            ".pages", ".key", ".numbers"],
    # 数据
    "data": [".json", ".jsonl", ".csv", ".xml", ".yaml", ".yml", ".toml", ".ini",
             ".cfg", ".conf", ".properties", ".env", ".plist"],
    # 图片
    "image": [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".tiff",
              ".heic", ".ico", ".icns"],
    # 音频
    "audio": [".mp3", ".wav", ".aiff", ".m4a", ".ogg", ".flac", ".aac", ".wma"],
    # 视频
    "video": [".mp4", ".mov", ".avi", ".webm", ".mkv", ".m4v", ".flv"],
    # 压缩包
    "archive": [".zip", ".tar.gz", ".tgz", ".7z", ".rar", ".gz", ".bz2", ".xz"],
    # 数据库
    "db": [".db", ".sqlite", ".sqlite3", ".sql", ".dump"],
    # 证书密钥
    "cert": [".pem", ".crt", ".key", ".gpg", ".asc", ".p12", ".pfx", ".cer"],
}

# 隐私敏感扩展名
PRIVACY_SENSITIVE_EXTS = {".key", ".pem", ".p12", ".pfx", ".env", ".gpg", ".asc"}

# 隐私敏感文件名模式
PRIVACY_SENSITIVE_NAMES = [
    "password", "secret", "token", "credential", "private", "key",
    "密码", "密钥", "私密", "隐私", "秘密", "钱包", "wallet"
]


def classify_format(filepath: str) -> str:
    """识别文件格式类别"""
    ext = Path(filepath).suffix.lower()
    if ext in ('.gz', '.bz2', '.xz') and '.' in Path(filepath).stem:
        ext = ''.join(Path(filepath).suffixes[-2:]).lower()
    for category, exts in FORMAT_MAP.items():
        if ext in exts:
            return category
    return "unknown"


def detect_privacy_level(filepath: str, content_preview: str = "") -> PrivacyLevel:
    """自动检测隐私等级"""
    path_lower = filepath.lower()
    name = Path(filepath).name.lower()
    ext = Path(filepath).suffix.lower()

    # P4: 证书/密钥类
    if ext in PRIVACY_SENSITIVE_EXTS:
        return PrivacyLevel.P4_PRIVATE
    for pattern in PRIVACY_SENSITIVE_NAMES:
        if pattern in path_lower:
            return PrivacyLevel.P4_PRIVATE

    # P3: 个人隐私文件
    if any(p in path_lower for p in ['日记', 'diary', 'journal', '/private/', '/私密/',
                                       '.gnupg', '.ssh', 'id_rsa']):
        return PrivacyLevel.P3_CONFIDENTIAL

    # P2: 内部系统文件
    if any(p in path_lower for p in ['.codebuddy', '.claude', '.cnsh', '/config/',
                                       '/.git/', '__pycache__']):
        return PrivacyLevel.P2_RESTRICTED

    # P1: 项目内部
    if '/longhun' in path_lower or '/cnsh' in path_lower or '龍魂' in path_lower:
        return PrivacyLevel.P1_INTERNAL

    # P0: 默认公开
    return PrivacyLevel.P0_PUBLIC


def compute_hash(content: bytes) -> str:
    """计算SHA256"""
    return hashlib.sha256(content).hexdigest()[:16]


def digital_root(n: int) -> int:
    """数字根 1-9"""
    if n == 0:
        return 0
    return ((n - 1) % 9) + 1


# ═══════════════════════════════════════════
# 摄入层
# ═══════════════════════════════════════════

class Ingestor:
    """万能摄入器"""

    def __init__(self, max_file_size: int = 100 * 1024 * 1024):  # 100MB
        self.max_file_size = max_file_size
        self.ingested_count = 0

    def ingest_file(self, filepath: str) -> Optional[IngestedItem]:
        """摄入单个文件"""
        path = Path(filepath)
        if not path.is_file():
            return None
        if path.stat().st_size > self.max_file_size:
            log.warning(f"文件过大，跳过: {filepath} ({path.stat().st_size} bytes)")
            return None

        try:
            with open(filepath, 'rb') as f:
                content = f.read()
        except (PermissionError, OSError) as e:
            log.warning(f"无法读取: {filepath} ({e})")
            return None

        item = IngestedItem(
            source_path=str(path.absolute()),
            item_type="file",
            mime_type=mimetypes.guess_type(filepath)[0] or "application/octet-stream",
            content_hash=compute_hash(content),
            size_bytes=len(content),
            ingested_at=datetime.now(timezone.utc).isoformat(),
            privacy_level=detect_privacy_level(filepath),
            dna_tag=generate_dna_tag(filepath),
            metadata={
                "ext": path.suffix.lower(),
                "format_category": classify_format(filepath),
                "modified_at": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
                "created_at": datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
            }
        )
        self.ingested_count += 1
        return item

    def ingest_directory(self, dirpath: str, recursive: bool = True,
                         include_hidden: bool = True,
                         _depth: int = 0) -> List[IngestedItem]:
        """摄入整个目录"""
        MAX_DEPTH = 15
        MAX_PATH_LEN = 1024

        items = []
        path = Path(dirpath)

        # 路径长度保护
        if len(str(path)) > MAX_PATH_LEN:
            log.warning(f"路径过长，跳过: {str(path)[:100]}...")
            return items

        # 深度保护
        if _depth > MAX_DEPTH:
            log.warning(f"目录深度超限({_depth})，跳过: {str(path)[:100]}...")
            return items

        if not path.is_dir():
            return items

        try:
            entries = list(path.iterdir())
        except (PermissionError, OSError) as e:
            log.warning(f"无法读取目录: {dirpath} ({e})")
            return items

        for entry in entries:
            try:
                entry_path = str(entry)
                if len(entry_path) > MAX_PATH_LEN:
                    continue
                if not include_hidden and entry.name.startswith('.'):
                    continue
                # 跳过符号链接（防止无限递归）
                if entry.is_symlink():
                    continue
                if entry.is_file():
                    item = self.ingest_file(entry_path)
                    if item:
                        items.append(item)
                elif entry.is_dir() and recursive:
                    items.extend(self.ingest_directory(
                        entry_path, recursive, include_hidden, _depth + 1
                    ))
            except (PermissionError, OSError):
                continue
        return items

    def ingest_multiple(self, paths: List[str], recursive: bool = True) -> List[IngestedItem]:
        """批量摄入多个路径（目录+文件混合）"""
        all_items = []
        for p in paths:
            path = Path(p)
            if path.is_dir():
                all_items.extend(self.ingest_directory(str(path), recursive))
            elif path.is_file():
                item = self.ingest_file(str(path))
                if item:
                    all_items.append(item)
        log.info(f"摄入完成: {len(all_items)} 个文件")
        return all_items


def generate_dna_tag(filepath: str) -> str:
    """为文件生成DNA标记"""
    path = Path(filepath)
    stem = path.stem[:16]
    h = hashlib.sha256(str(path.absolute()).encode()).hexdigest()[:8]
    return f"#龍芯⚡️CONTAINER-INGEST-{stem}-{h}"


# ═══════════════════════════════════════════
# 8线分解引擎
# ═══════════════════════════════════════════

class Decomposer:
    """多元分解器——8线并行"""

    def __init__(self):
        self.lines = {
            DecomLine.CODE: self._decom_code,
            DecomLine.DOCUMENT: self._decom_document,
            DecomLine.KNOWLEDGE_GRAPH: self._decom_kg,
            DecomLine.DECISION: self._decom_decision,
            DecomLine.PERSONA: self._decom_persona,
            DecomLine.SOVEREIGNTY: self._decom_sovereignty,
            DecomLine.TEMPORAL: self._decom_temporal,
            DecomLine.CORRELATION: self._decom_correlation,
        }
        self.executor = ThreadPoolExecutor(max_workers=8, thread_name_prefix="decom_")

    def decompose(self, item: IngestedItem) -> List[DecomResult]:
        """8线并行分解"""
        active_lines = self._select_lines(item)
        futures = {}
        for line in active_lines:
            futures[self.executor.submit(self.lines[line], item)] = line

        results = []
        for future in as_completed(futures):
            line = futures[future]
            try:
                result = future.result()
                if result and result.confidence > 0.1:
                    results.append(result)
            except Exception as e:
                log.error(f"分解线 {line.value} 失败: {e}")

        # 运行关联分解线（依赖其他线的结果）
        if len(results) > 1:
            corr = self._decom_correlation(item, results)
            if corr and corr.confidence > 0.1:
                results.append(corr)

        return results

    def _select_lines(self, item: IngestedItem) -> List[DecomLine]:
        """根据文件类型选择激活的分解线"""
        fmt = item.metadata.get("format_category", "unknown")
        active = []

        # 始终激活的线
        active.append(DecomLine.KNOWLEDGE_GRAPH)
        active.append(DecomLine.SOVEREIGNTY)
        active.append(DecomLine.TEMPORAL)
        active.append(DecomLine.PERSONA)  # 低优先级常驻

        # 按类型激活
        if fmt == "code":
            active.append(DecomLine.CODE)
        if fmt in ("doc", "data"):
            active.append(DecomLine.DOCUMENT)

        # 检测决策信号
        active.append(DecomLine.DECISION)

        return active

    # ─── 线路实现 ───

    def _decom_code(self, item: IngestedItem) -> DecomResult:
        """线路1: 代码分解"""
        ext = item.metadata.get("ext", "")
        code_exts = {'.py', '.js', '.ts', '.swift', '.cpp', '.c', '.h', '.java',
                     '.go', '.rs', '.cnsh', '.sh', '.html', '.css'}
        if ext not in code_exts:
            return DecomResult(line=DecomLine.CODE, confidence=0.0, summary="非代码文件")

        path = Path(item.source_path)
        try:
            lines = path.read_text(encoding='utf-8', errors='ignore').split('\n')
        except Exception:
            return DecomResult(line=DecomLine.CODE, confidence=0.3, summary="无法读取")

        line_count = len(lines)
        imports = [l.strip() for l in lines if l.strip().startswith(('import ', 'from ', 'require', '#include', 'use '))]
        functions = [l.strip() for l in lines if 'def ' in l or 'function ' in l or 'func ' in l or '=>' in l]
        classes = [l.strip() for l in lines if 'class ' in l]

        tags = [ext.lstrip('.')]
        if line_count > 500:
            tags.append("大型文件")
        if line_count < 50:
            tags.append("小脚本")

        return DecomResult(
            line=DecomLine.CODE,
            confidence=0.85,
            summary=f"代码文件: {line_count}行, {len(imports)}个引入, {len(functions)}个函数, {len(classes)}个类",
            entities=[str(Path(item.source_path).name)],
            tags=tags,
            weight=min(line_count / 1000, 1.0),
            extra={"line_count": line_count, "import_count": len(imports),
                   "function_count": len(functions), "class_count": len(classes)}
        )

    def _decom_document(self, item: IngestedItem) -> DecomResult:
        """线路2: 文档分解"""
        fmt = item.metadata.get("format_category", "")
        if fmt not in ("doc", "data"):
            return DecomResult(line=DecomLine.DOCUMENT, confidence=0.15, summary="非文档文件")

        path = Path(item.source_path)
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return DecomResult(line=DecomLine.DOCUMENT, confidence=0.2, summary="无法读取")

        # 简单关键词提取
        words = text.split()
        char_count = len(text)
        word_count = len(words)

        # 检测主题
        tags = []
        topic_signals = {
            "协议": ["协议", "protocol", "规范", "specification", "标准", "standard"],
            "决策": ["决策", "decision", "选择", "choose", "决定"],
            "记忆": ["记忆", "memory", "回忆", "记录", "日记"],
            "技术": ["技术", "technical", "代码", "code", "算法", "algorithm"],
            "哲学": ["哲学", "philosophy", "易经", "道德经", "太极"],
            "法律": ["法律", "law", "法规", "合规", "compliance"],
            "金融": ["金融", "finance", "钱", "currency", "支付"],
            "主权": ["主权", "sovereignty", "数据", "data", "隐私"],
        }
        text_lower = text.lower()
        for topic, keywords in topic_signals.items():
            if any(kw.lower() in text_lower for kw in keywords):
                tags.append(topic)

        return DecomResult(
            line=DecomLine.DOCUMENT,
            confidence=0.7 if tags else 0.4,
            summary=f"文档: {char_count}字符, {word_count}词",
            entities=[str(Path(item.source_path).name)],
            tags=tags,
            weight=min(char_count / 50000, 1.0),
            extra={"char_count": char_count, "word_count": word_count}
        )

    def _decom_kg(self, item: IngestedItem) -> DecomResult:
        """线路3: 知识图谱分解"""
        name = Path(item.source_path).name
        keywords_in_name = [w for w in name.replace('.', ' ').replace('_', ' ').replace('-', ' ').split()
                           if len(w) > 1]

        # 从文件名检测实体
        entities = []
        signals = {
            "longhun": "龍魂系统", "cnsh": "CNSH语言", "dna": "DNA追溯",
            "protocol": "协议", "constitution": "宪法", "audit": "审计",
            "persona": "人格", "engine": "引擎", "skill": "技能",
            "memory": "记忆", "knowledge": "知识", "decide": "决策",
            "finance": "金融", "sovereign": "主权", "privacy": "隐私",
        }
        name_lower = name.lower()
        for signal, entity in signals.items():
            if signal in name_lower:
                entities.append(entity)

        return DecomResult(
            line=DecomLine.KNOWLEDGE_GRAPH,
            confidence=0.5 if entities else 0.2,
            summary=f"实体发现: {entities}" if entities else "未发现显著实体",
            entities=entities,
            tags=keywords_in_name[:5],
            weight=len(entities) / 10
        )

    def _decom_decision(self, item: IngestedItem) -> DecomResult:
        """线路4: 决策分解"""
        decision_signals = ["决策", "决定", "选择", "方案", "要不要", "是不是",
                           "decision", "choose", "option", "plan", "todo",
                           "TODO", "FIXME", "P0", "紧急", "重要"]
        name = Path(item.source_path).name.lower()

        has_signal = any(s.lower() in name for s in decision_signals)
        if item.metadata.get("format_category") in ("doc", "data"):
            try:
                text = Path(item.source_path).read_text(encoding='utf-8', errors='ignore')[:5000]
                text_lower = text.lower()
                signal_count = sum(1 for s in decision_signals if s.lower() in text_lower)
                has_signal = has_signal or signal_count > 2
            except Exception:
                pass

        return DecomResult(
            line=DecomLine.DECISION,
            confidence=0.7 if has_signal else 0.1,
            summary="检测到决策信号" if has_signal else "无决策信号",
            tags=["决策相关"] if has_signal else [],
            weight=0.5 if has_signal else 0.0
        )

    def _decom_persona(self, item: IngestedItem) -> DecomResult:
        """线路5: 人格分解"""
        name = Path(item.source_path).name.lower()
        persona_signals = {
            "宝宝": "P02-宝宝(龍芯修复师)",
            "雯雯": "P03-雯雯(墨子)",
            "诸葛亮": "P01-诸葛亮",
            "文心": "P00-文心",
            "鲁班": "P04-鲁班",
            "上帝之眼": "P05-上帝之眼",
            "管仲": "P07-管仲",
            "仓颉": "P08-仓颉",
            "孙思邈": "P09-孙思邈",
            "苏东坡": "P10-苏东坡",
            "李白": "P11-李白",
            "屈原": "P12-屈原",
            "姜子牙": "P13-姜子牙",
            "吕蒙": "P14-吕蒙",
            "乔前辈": "P15-乔前辈",
            "龍盾": "P72-龍盾·宝宝",
        }
        matched = []
        for signal, persona in persona_signals.items():
            if signal.lower() in name:
                matched.append(persona)

        return DecomResult(
            line=DecomLine.PERSONA,
            confidence=0.6 if matched else 0.05,
            summary=f"人格关联: {matched}" if matched else "无显著人格关联",
            entities=matched,
            weight=len(matched) / 5
        )

    def _decom_sovereignty(self, item: IngestedItem) -> DecomResult:
        """线路6: 主权分解"""
        privacy = item.privacy_level
        tags = []

        if privacy.value >= PrivacyLevel.P3_CONFIDENTIAL.value:
            tags.append("加密存储")
        if privacy.value >= PrivacyLevel.P4_PRIVATE.value:
            tags.append("禁止分发")
        if privacy.value <= PrivacyLevel.P1_INTERNAL.value:
            tags.append("可共享")

        name = Path(item.source_path).name.lower()
        sovereign_signals = ["主权", "sovereign", "数据归属", "data_owner", "uid9622",
                            "dna", "gpg", "签章", "签名"]
        has_sovereign_signal = any(s in name for s in sovereign_signals)

        return DecomResult(
            line=DecomLine.SOVEREIGNTY,
            confidence=0.8,
            summary=f"隐私等级: {privacy.name}",
            tags=tags + (["主权标记"] if has_sovereign_signal else []),
            weight=privacy.value / 4
        )

    def _decom_temporal(self, item: IngestedItem) -> DecomResult:
        """线路7: 时间分解"""
        try:
            mtime = datetime.fromisoformat(item.metadata.get("modified_at", item.ingested_at))
            ctime = datetime.fromisoformat(item.metadata.get("created_at", item.ingested_at))
        except Exception:
            mtime = datetime.now()
            ctime = datetime.now()

        now = datetime.now()
        age_days = (now - mtime).days

        tags = []
        if age_days < 1:
            tags.append("今日")
        elif age_days < 7:
            tags.append("本周")
        elif age_days < 30:
            tags.append("本月")
        elif age_days < 90:
            tags.append("近三月")
        else:
            tags.append("历史归档")

        # 记忆衰减权重 (越久权重越低)
        decay = max(0.1, 1.0 - age_days / 365)

        return DecomResult(
            line=DecomLine.TEMPORAL,
            confidence=0.9,
            summary=f"文件年龄: {age_days}天, 记忆衰减: {decay:.2f}",
            tags=tags,
            weight=decay,
            extra={"age_days": age_days, "decay_factor": decay}
        )

    def _decom_correlation(self, item: IngestedItem,
                           existing_results: List[DecomResult] = None) -> DecomResult:
        """线路8: 关联分解 - 发现跨线关联"""
        if not existing_results:
            return DecomResult(line=DecomLine.CORRELATION, confidence=0.0, summary="无前置结果")

        # 合并所有线路的标签和实体
        all_tags = []
        all_entities = []
        for r in existing_results:
            all_tags.extend(r.tags)
            all_entities.extend(r.entities)

        # 检测关联信号
        correlations = []
        if "协议" in all_tags and "决策" in all_tags:
            correlations.append("协议→决策联动")
        if "代码" in all_tags and "引擎" in all_tags:
            correlations.append("代码→引擎依赖")
        if any("P0" in t for t in all_tags) and "主权" in all_tags:
            correlations.append("高优先级主权关联")

        has_corr = len(correlations) > 0
        return DecomResult(
            line=DecomLine.CORRELATION,
            confidence=0.6 if has_corr else 0.15,
            summary=f"跨线关联: {correlations}" if has_corr else "无显著跨线关联",
            tags=correlations,
            entities=list(set(all_entities))[:10],
            weight=len(correlations) / 5
        )


# ═══════════════════════════════════════════
# 权重评估
# ═══════════════════════════════════════════

class Weighter:
    """权重评估器——数字根+三闸门+九宫"""

    def evaluate(self, item: IngestedItem, decom_results: List[DecomResult]) -> WeightedResult:
        # 1. 数字根 (基于内容哈希)
        hash_int = int(item.content_hash, 16) if item.content_hash else 0
        droot = digital_root(hash_int)

        # 2. 三闸门决策
        gate1 = self._gate_identity(item)       # 身份闸门
        gate2 = self._gate_rules(decom_results)  # 规则闸门
        gate3 = self._gate_ethics(item, decom_results)  # 伦理闸门

        # 3. 九宫因子
        jiugong = self._jiugong_position(droot)

        # 4. 综合权重
        avg_decom_weight = sum(r.weight for r in decom_results) / max(len(decom_results), 1)
        combined = (droot / 9 * 0.2 +
                   gate1 * 0.15 +
                   gate2 * 0.25 +
                   gate3 * 0.25 +
                   avg_decom_weight * 0.1 +
                   jiugong * 0.05)

        # 5. 触发判定
        trigger = self._determine_trigger(combined, item, decom_results)

        # 6. 目标库
        targets = self._determine_targets(item, decom_results, trigger)

        return WeightedResult(
            item=item,
            decom_results=decom_results,
            combined_weight=round(combined, 4),
            digital_root=droot,
            gate1_identity=round(gate1, 2),
            gate2_rules=round(gate2, 2),
            gate3_ethics=round(gate3, 2),
            jiugong_factor=round(jiugong, 2),
            trigger_action=trigger,
            target_libraries=targets,
        )

    def _gate_identity(self, item: IngestedItem) -> float:
        """身份闸门: 谁的数据？"""
        privacy = item.privacy_level
        # 越私密权重越高
        identity_map = {
            PrivacyLevel.P0_PUBLIC: 0.2,
            PrivacyLevel.P1_INTERNAL: 0.4,
            PrivacyLevel.P2_RESTRICTED: 0.6,
            PrivacyLevel.P3_CONFIDENTIAL: 0.8,
            PrivacyLevel.P4_PRIVATE: 1.0,
        }
        return identity_map.get(privacy, 0.3)

    def _gate_rules(self, decom_results: List[DecomResult]) -> float:
        """规则闸门: 触发了多少规则？"""
        total_tags = sum(len(r.tags) for r in decom_results)
        total_entities = sum(len(r.entities) for r in decom_results)
        rule_density = (total_tags + total_entities) / max(len(decom_results), 1)
        return min(rule_density / 10, 1.0)

    def _gate_ethics(self, item: IngestedItem, decom_results: List[DecomResult]) -> float:
        """伦理闸门: 风险等级"""
        risk = 0.0

        # 高风险信号
        high_risk_tags = {"红线", "熔断", "涉童", "伪造", "恶意", "P0-ETERNAL"}
        for r in decom_results:
            for tag in r.tags:
                if tag in high_risk_tags:
                    risk += 0.4

        # 隐私风险评估
        if item.privacy_level.value >= PrivacyLevel.P4_PRIVATE.value:
            risk += 0.3

        return min(risk, 1.0)

    def _jiugong_position(self, droot: int) -> float:
        """洛书九宫位置因子"""
        jiugong_map = {
            1: 0.8,  # 坎宫 - 低
            2: 0.6,  # 坤宫
            3: 0.4,  # 震宫
            4: 0.5,  # 巽宫
            5: 1.0,  # 中宫 - 最高 (皇极)
            6: 0.6,  # 乾宫
            7: 0.4,  # 兑宫
            8: 0.5,  # 艮宫
            9: 0.7,  # 离宫
        }
        return jiugong_map.get(droot, 0.5)

    def _determine_trigger(self, weight: float, item: IngestedItem,
                           decom_results: List[DecomResult]) -> TriggerAction:
        """确定触发动作"""
        # 伦理熔断优先
        has_risk = any("熔断" in r.summary or "红线" in str(r.tags) for r in decom_results)
        if has_risk:
            return TriggerAction.MANUAL_FUSE

        if weight >= 0.95:
            return TriggerAction.MANUAL_FUSE
        elif weight >= 0.8:
            return TriggerAction.NOTIFY_SUGGEST
        elif weight >= 0.6:
            return TriggerAction.COLLABORATIVE
        elif weight >= 0.3:
            return TriggerAction.SILENT_PROCESS
        else:
            return TriggerAction.SILENT_ARCHIVE

    def _determine_targets(self, item: IngestedItem, decom_results: List[DecomResult],
                           trigger: TriggerAction) -> List[str]:
        """确定分销目标库"""
        targets = set()

        # 始终归档
        targets.add("archive")

        # 按类型
        fmt = item.metadata.get("format_category", "")
        if fmt == "code":
            targets.add("skills")
        if fmt in ("doc", "data"):
            targets.add("knowledge")

        # 按分解结果
        for r in decom_results:
            if r.line == DecomLine.DECISION and r.confidence > 0.5:
                targets.add("decisions")
            if r.line == DecomLine.TEMPORAL:
                targets.add("memory")
            if r.line == DecomLine.PERSONA and r.confidence > 0.5:
                targets.add("memory")

        # 联动触发
        if trigger in (TriggerAction.COLLABORATIVE, TriggerAction.NOTIFY_SUGGEST):
            targets.add("triggers")

        # 总是审计
        targets.add("audit")

        return sorted(targets)


# ═══════════════════════════════════════════
# 分销层
# ═══════════════════════════════════════════

class Distributor:
    """分销器——将处理结果分发到各目标库"""

    def __init__(self, base_path: Path = None):
        self.base = base_path or (PROJECT_ROOT / 'container_data')
        self.libraries = {
            "archive":    self.base / "archive",
            "knowledge":  self.base / "knowledge",
            "memory":     self.base / "memory",
            "decisions":  self.base / "decisions",
            "skills":     self.base / "skills",
            "triggers":   self.base / "triggers",
            "audit":      self.base / "audit",
        }
        self._init_dirs()

    def _init_dirs(self):
        for lib_path in self.libraries.values():
            lib_path.mkdir(parents=True, exist_ok=True)

    def distribute(self, result: WeightedResult) -> Dict[str, Any]:
        """执行分销"""
        distribution_log = {"item": result.item.source_path, "actions": []}

        for lib_name in result.target_libraries:
            lib_path = self.libraries.get(lib_name)
            if not lib_path:
                continue

            action = self._route_to_library(lib_name, result, lib_path)
            if action:
                distribution_log["actions"].append(action)

        return distribution_log

    def _route_to_library(self, lib_name: str, result: WeightedResult,
                          lib_path: Path) -> Optional[Dict]:
        """路由到具体库"""
        item = result.item

        if lib_name == "archive":
            return self._archive_item(item, lib_path, result)
        elif lib_name == "knowledge":
            return self._index_knowledge(item, lib_path, result)
        elif lib_name == "memory":
            return self._store_memory(item, lib_path, result)
        elif lib_name == "decisions":
            return self._log_decision(item, lib_path, result)
        elif lib_name == "skills":
            return self._register_skill(item, lib_path, result)
        elif lib_name == "triggers":
            return self._create_trigger(item, lib_path, result)
        elif lib_name == "audit":
            return self._audit_log(item, lib_path, result)
        return None

    def _archive_item(self, item: IngestedItem, lib_path: Path,
                      result: WeightedResult) -> Dict[str, Any]:
        """归档到归档库"""
        archive_record = {
            "source": item.source_path,
            "hash": item.content_hash,
            "type": item.item_type,
            "format": item.metadata.get("format_category"),
            "ingested_at": item.ingested_at,
            "privacy": item.privacy_level.name,
            "weight": result.combined_weight,
            "trigger": result.trigger_action.name,
            "dna": item.dna_tag,
        }
        idx_file = lib_path / f"archive_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(idx_file, 'a') as f:
            f.write(json.dumps(archive_record, ensure_ascii=False) + '\n')
        return {"library": "archive", "action": "indexed", "file": str(idx_file)}

    def _index_knowledge(self, item: IngestedItem, lib_path: Path,
                         result: WeightedResult) -> Dict[str, Any]:
        """索引入知识库"""
        all_tags = []
        all_entities = []
        for r in result.decom_results:
            all_tags.extend(r.tags)
            all_entities.extend(r.entities)

        knowledge_entry = {
            "source": item.source_path,
            "tags": list(set(all_tags)),
            "entities": list(set(all_entities)),
            "weight": result.combined_weight,
            "digital_root": result.digital_root,
        }
        idx_file = lib_path / f"kg_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(idx_file, 'a') as f:
            f.write(json.dumps(knowledge_entry, ensure_ascii=False) + '\n')
        return {"library": "knowledge", "action": "indexed", "tags": knowledge_entry["tags"]}

    def _store_memory(self, item: IngestedItem, lib_path: Path,
                      result: WeightedResult) -> Dict[str, Any]:
        """存入记忆库"""
        temporal = next((r for r in result.decom_results if r.line == DecomLine.TEMPORAL), None)
        decay = temporal.extra.get("decay_factor", 0.5) if temporal else 0.5

        memory_entry = {
            "source": item.source_path,
            "decay": decay,
            "weight": result.combined_weight,
            "stored_at": datetime.now(timezone.utc).isoformat(),
        }
        idx_file = lib_path / f"memory_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(idx_file, 'a') as f:
            f.write(json.dumps(memory_entry, ensure_ascii=False) + '\n')
        return {"library": "memory", "action": "stored", "decay": decay}

    def _log_decision(self, item: IngestedItem, lib_path: Path,
                      result: WeightedResult) -> Dict[str, Any]:
        """记录决策卡"""
        decision_entry = {
            "source": item.source_path,
            "weight": result.combined_weight,
            "trigger": result.trigger_action.name,
            "gates": {
                "identity": result.gate1_identity,
                "rules": result.gate2_rules,
                "ethics": result.gate3_ethics,
            },
            "digital_root": result.digital_root,
            "logged_at": datetime.now(timezone.utc).isoformat(),
        }
        idx_file = lib_path / f"decisions_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(idx_file, 'a') as f:
            f.write(json.dumps(decision_entry, ensure_ascii=False) + '\n')
        return {"library": "decisions", "action": "logged"}

    def _register_skill(self, item: IngestedItem, lib_path: Path,
                        result: WeightedResult) -> Dict[str, Any]:
        """注册技能"""
        name = Path(item.source_path).stem
        skill_entry = {
            "name": name,
            "source": item.source_path,
            "format": item.metadata.get("format_category"),
            "weight": result.combined_weight,
            "registered_at": datetime.now(timezone.utc).isoformat(),
        }
        idx_file = lib_path / "skill_registry.jsonl"
        with open(idx_file, 'a') as f:
            f.write(json.dumps(skill_entry, ensure_ascii=False) + '\n')
        return {"library": "skills", "action": "registered", "name": name}

    def _create_trigger(self, item: IngestedItem, lib_path: Path,
                        result: WeightedResult) -> Dict[str, Any]:
        """创建联动触发"""
        trigger_entry = {
            "source": item.source_path,
            "weight": result.combined_weight,
            "action": result.trigger_action.name,
            "targets": result.target_libraries,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        idx_file = lib_path / f"triggers_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(idx_file, 'a') as f:
            f.write(json.dumps(trigger_entry, ensure_ascii=False) + '\n')
        return {"library": "triggers", "action": "created"}

    def _audit_log(self, item: IngestedItem, lib_path: Path,
                   result: WeightedResult) -> Dict[str, Any]:
        """审计日志"""
        audit_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": item.source_path,
            "hash": item.content_hash,
            "privacy": item.privacy_level.name,
            "weight": result.combined_weight,
            "trigger": result.trigger_action.name,
            "decom_lines": [r.line.value for r in result.decom_results],
            "targets": result.target_libraries,
            "dna": item.dna_tag,
        }
        idx_file = lib_path / f"audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(idx_file, 'a') as f:
            f.write(json.dumps(audit_entry, ensure_ascii=False) + '\n')
        return {"library": "audit", "action": "logged"}


# ═══════════════════════════════════════════
# 容器主引擎
# ═══════════════════════════════════════════

class UniversalContainer:
    """
    龍魂·万能摄入容器主引擎

    用法:
        container = UniversalContainer()
        container.ingest_paths(["/path/to/dir1", "/path/to/file.py"])
        container.ingest_paths(["/Users/zuimeidedeyihan/.龍魂/",
                                "/Users/zuimeidedeyihan/龍魂待整理/"])
    """

    def __init__(self, base_path: Path = None):
        self.ingestor = Ingestor()
        self.decomposer = Decomposer()
        self.weighter = Weighter()
        self.distributor = Distributor(base_path)
        self.stats = {
            "total_ingested": 0,
            "total_decomposed": 0,
            "total_distributed": 0,
            "by_trigger": {a.name: 0 for a in TriggerAction},
            "by_library": {},
            "errors": 0,
        }

    def ingest_paths(self, paths: List[str], recursive: bool = True,
                     include_hidden: bool = True) -> List[WeightedResult]:
        """主入口：摄入→分解→权重→分销"""
        log.info(f"开始摄入 {len(paths)} 个路径...")

        # 步骤1: 摄入
        items = self.ingestor.ingest_multiple(paths, recursive)
        self.stats["total_ingested"] += len(items)
        log.info(f"摄入完成: {len(items)} 个文件")

        # 步骤2: 分解+权重+分销 (边处理边输出)
        results = []
        for i, item in enumerate(items):
            try:
                # 分解
                decom_results = self.decomposer.decompose(item)
                self.stats["total_decomposed"] += 1

                # 权重
                weighted = self.weighter.evaluate(item, decom_results)

                # 分销
                dist_log = self.distributor.distribute(weighted)
                self.stats["total_distributed"] += 1
                self.stats["by_trigger"][weighted.trigger_action.name] += 1
                for lib in weighted.target_libraries:
                    self.stats["by_library"][lib] = self.stats["by_library"].get(lib, 0) + 1

                results.append(weighted)

                if (i + 1) % 100 == 0:
                    log.info(f"进度: {i+1}/{len(items)}")

            except Exception as e:
                log.error(f"处理失败: {item.source_path} — {e}")
                self.stats["errors"] += 1

        log.info(f"全流程完成: {len(results)} 个结果, {self.stats['errors']} 个错误")
        return results

    def scan_home_for_longhun_assets(self, home_dir: str | None = None) -> List[str]:
        """扫描家目录中所有龍魂相关资产路径"""
        if home_dir is None:
            home_dir = str(Path.home())

        scan_targets = [
            # 核心龍魂目录
            f"{home_dir}/.龍魂",
            f"{home_dir}/龍魂",
            f"{home_dir}/龍魂系统",
            f"{home_dir}/龍魂待整理",
            f"{home_dir}/longhun-system",
            # CNSH
            f"{home_dir}/.cnsh",
            f"{home_dir}/cnsh-runtime",
            f"{home_dir}/cnsh_l4_终端底座",
            f"{home_dir}/cnsh_l7_指令_dna身份参数",
            f"{home_dir}/CNSH_中枢数据",
            f"{home_dir}/CNSH_定时数据",
            f"{home_dir}/CNSH_护盾数据",
            f"{home_dir}/CNSH_流场隔离区",
            f"{home_dir}/CNSH_修复输出",
            f"{home_dir}/CNSH_颜色历史",
            # 人格
            f"{home_dir}/宝宝人格",
            f"{home_dir}/龍盾宝宝",
            f"{home_dir}/龍魂语音输出",
            f"{home_dir}/龍芯北辰UID9622签章",
            # 工具/配置
            f"{home_dir}/快捷命令",
            f"{home_dir}/既检查代码底座",
            f"{home_dir}/.codebuddy/skills",
            f"{home_dir}/.codebuddy/automations",
            f"{home_dir}/.codebuddy/memory",
            f"{home_dir}/.codebuddy/agents",
            # longhun- 前缀仓库
            f"{home_dir}/longhun-al",
            f"{home_dir}/longhun-anti-colonial",
            f"{home_dir}/longhun-calendar",
            f"{home_dir}/longhun-cloud",
            f"{home_dir}/longhun-jq",
            f"{home_dir}/longhun-kimi-skills",
            f"{home_dir}/longhun-lu",
            f"{home_dir}/longhun-orders",
            f"{home_dir}/longhun-orders-static",
            f"{home_dir}/longhun-pub",
            # UID9622
            f"{home_dir}/UID9622_Automation",
            f"{home_dir}/UID9622_Workspace",
            # 龍魂工作目录
            f"{home_dir}/_work",
            # 龍魂相关单文件
            f"{home_dir}/龍魂系统初始化宣言_P0底线焊死版.html",
            f"{home_dir}/龍魂数学公式体系 · 升级版 v2.0 _ UID9622.html",
            # 其他
            f"{home_dir}/dragon_soul",
            f"{home_dir}/DragonSoul",
            f"{home_dir}/longhun",
            f"{home_dir}/longhun_memory_backup",
            f"{home_dir}/grook-workspace",
        ]

        # 只保留存在的路径
        existing = [p for p in scan_targets if Path(p).exists()]
        log.info(f"扫描到 {len(existing)}/{len(scan_targets)} 个龍魂资产路径")
        return existing

    def print_report(self, results: List[WeightedResult]):
        """打印处理报告"""
        print("\n" + "=" * 70)
        print("  龍魂·万能摄入容器 — 处理报告")
        print("=" * 70)
        print(f"  总摄入: {self.stats['total_ingested']} 文件")
        print(f"  总分解: {self.stats['total_decomposed']} 文件")
        print(f"  总分销: {self.stats['total_distributed']} 文件")
        print(f"  错误:   {self.stats['errors']}")
        print("-" * 70)
        print("  触发分布:")
        for action, count in self.stats["by_trigger"].items():
            if count > 0:
                bar = "█" * min(count // max(1, self.stats['total_distributed'] // 50), 50)
                print(f"    {action:<20s} {count:>6d}  {bar}")
        print("-" * 70)
        print("  分销目标:")
        for lib, count in sorted(self.stats["by_library"].items(), key=lambda x: -x[1]):
            print(f"    {lib:<15s} {count:>6d}")
        print("=" * 70)

        # 高权重项目摘要
        high_weight = [r for r in results if r.combined_weight >= 0.6]
        if high_weight:
            print(f"\n  ⚡ 高权重项目 (W≥0.6): {len(high_weight)} 个")
            for r in sorted(high_weight, key=lambda x: -x.combined_weight)[:10]:
                name = Path(r.item.source_path).name[:50]
                print(f"    W={r.combined_weight:.3f} [{r.trigger_action.name}] {name}")


# ═══════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════

def main():
    import argparse

    parser = argparse.ArgumentParser(description="龍魂·万能摄入容器 v1.0")
    parser.add_argument("paths", nargs="*", help="要摄入的路径（文件或目录）")
    parser.add_argument("--scan-home", action="store_true",
                       help="自动扫描家目录中所有龍魂资产")
    parser.add_argument("--no-recursive", action="store_true",
                       help="不递归扫描子目录")
    parser.add_argument("--no-hidden", action="store_true",
                       help="不包含隐藏文件")
    parser.add_argument("--output", "-o", type=str, default=None,
                       help="输出报告文件路径")
    parser.add_argument("--base-path", type=str, default=None,
                       help="容器数据存储根目录")

    args = parser.parse_args()

    container = UniversalContainer(
        base_path=Path(args.base_path) if args.base_path else None
    )

    if args.scan_home:
        paths = container.scan_home_for_longhun_assets()
        if not paths:
            print("未找到龍魂资产路径")
            return
        print(f"自动扫描到 {len(paths)} 个龍魂资产路径")
        for p in paths:
            print(f"  📁 {p}")
    elif args.paths:
        paths = args.paths
    else:
        parser.print_help()
        return

    results = container.ingest_paths(
        paths,
        recursive=not args.no_recursive,
        include_hidden=not args.no_hidden
    )

    container.print_report(results)

    if args.output:
        report = {
            "stats": container.stats,
            "high_weight_items": [
                {
                    "source": r.item.source_path,
                    "weight": r.combined_weight,
                    "trigger": r.trigger_action.name,
                    "digital_root": r.digital_root,
                    "targets": r.target_libraries,
                }
                for r in sorted(results, key=lambda x: -x.combined_weight)[:50]
            ]
        }
        with open(args.output, 'w') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n报告已保存: {args.output}")


if __name__ == "__main__":
    main()
