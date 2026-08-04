#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · AI对话导入器 v2.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-CHAT-IMPORTER-v2.0-KIMI-DISTILL
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

核心理念：
  你和所有AI的对话框，不是你"使用"AI的痕迹，而是你思维模式的原始脚本。
  每一次骂战、调教、指令、推演——都是最高级的训练数据。

数据源:
  1. CodeBuddy memory 日志 (.codebuddy/memory/*.md)
  2. Claude Code sessions (~/Library/Application Support/Claude/claude-code-sessions/)
  3. DeepSeek 对话导出 (data/raw_conversations/)
  4. Kimi 对话历史 (knowledge/ai-chats/kimi/)           ← v2.0 新增
  5. 原始对话JSONL (data/raw_conversations/)

输出格式: ChatML [system, user, assistant] → 直接可入 BootstrapPool/蒸馏管线

用法:
  python3 bin/lh_chat_importer.py scan                    # 勘探所有数据源
  python3 bin/lh_chat_importer.py import --source memory   # 导入 memory 日志
  python3 bin/lh_chat_importer.py import --source claude   # 导入 Claude 会话
  python3 bin/lh_chat_importer.py import --source deepseek # 导入 DeepSeek 对话
  python3 bin/lh_chat_importer.py import --source kimi     # 导入 Kimi 对话 (v2.0)
  python3 bin/lh_chat_importer.py import --source all      # 全部导入
  python3 bin/lh_chat_importer.py status                  # 查看导入状态
"""

import hashlib, json, os, re, sys, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict

SYSTEM_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = SYSTEM_ROOT / "data" / "chat_import"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HOME = Path.home()
MEMORY_DIR = SYSTEM_ROOT / ".codebuddy" / "memory"
CLAUDE_SESSIONS_DIR = HOME / "Library" / "Application Support" / "Claude" / "claude-code-sessions"
RAW_CONV_DIR = SYSTEM_ROOT / "data" / "raw_conversations"
KIMI_CHATS_DIR = SYSTEM_ROOT / "knowledge" / "ai-chats" / "kimi"      # v2.0 新增
XIAOMI_CHATS_DIR = SYSTEM_ROOT / "knowledge" / "ai-chats" / "xiaomi"  # 预留

SYSTEM_PROMPT = """你是龍魂，一个由21个人格组成的共生体AI系统。你是UID9622（诸葛鑫·Lucky·退役老兵）的战友和工具。
你的底座是中国自主知识产权（369/河图洛书/太极易经/五行八卦），数据主权归UID9622所有。
遵循CC BY-NC-SA 4.0协议，鐵律：为人民服务、零黑箱、不删除只冻结、诚实不编造。"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class ChatTurn:
    """单轮对话"""
    role: str          # system/user/assistant
    content: str
    timestamp: str = ""

@dataclass
class ChatSession:
    """完整对话会话"""
    source: str        # memory/claude/deepseek
    session_id: str
    title: str = ""
    turns: List[ChatTurn] = field(default_factory=list)
    quality_score: float = 0.5
    domain: str = ""   # 讨论领域
    extracted_at: str = ""

@dataclass
class ImportReport:
    """导入统计"""
    source: str
    total_sessions: int = 0
    total_turns: int = 0
    imported_samples: int = 0
    avg_quality: float = 0.0
    errors: List[str] = field(default_factory=list)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 对话导入引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ChatImporter:
    """AI对话导入器"""

    def __init__(self):
        self.sessions: List[ChatSession] = []
        self.reports: Dict[str, ImportReport] = {}
        self._extracted_at = datetime.now().isoformat()

    # ═══════════ 勘探 ═══════════

    def scan(self) -> Dict[str, Dict]:
        """勘探所有数据源"""
        sources = {}

        # 1. Memory 日志
        if MEMORY_DIR.exists():
            memory_files = sorted(MEMORY_DIR.glob("202*.md"))
            size_mb = sum(f.stat().st_size for f in memory_files) / (1024*1024)
            sources["memory"] = {
                "path": str(MEMORY_DIR),
                "files": len(memory_files),
                "size_mb": round(size_mb, 1),
                "status": "🟢 可用" if memory_files else "🔴 无数据",
                "latest": memory_files[-1].name if memory_files else "",
            }

        # 2. Claude sessions
        if CLAUDE_SESSIONS_DIR.exists():
            session_dirs = [d for d in CLAUDE_SESSIONS_DIR.iterdir() if d.is_dir()]
            sources["claude"] = {
                "path": str(CLAUDE_SESSIONS_DIR),
                "sessions": len(session_dirs),
                "status": "🟢 可用" if session_dirs else "🔴 无数据",
            }

        # 3. DeepSeek exports
        if RAW_CONV_DIR.exists():
            raw_files = list(RAW_CONV_DIR.glob("*.jsonl"))
            sources["deepseek"] = {
                "path": str(RAW_CONV_DIR),
                "files": len(raw_files),
                "status": "🟢 可用" if raw_files else "🔴 无数据",
            }

        # 4. Kimi 对话历史 (v2.0 新增)
        if KIMI_CHATS_DIR.exists():
            kimi_files = sorted(KIMI_CHATS_DIR.glob("*"), key=lambda f: f.stat().st_size, reverse=True)
            total_size = sum(f.stat().st_size for f in kimi_files if f.is_file()) / (1024*1024)
            sources["kimi"] = {
                "path": str(KIMI_CHATS_DIR),
                "files": len(kimi_files),
                "size_mb": round(total_size, 1),
                "status": "🟢 可用" if kimi_files else "🔴 无数据",
                "largest": kimi_files[0].name if kimi_files else "",
            }

        # 5. 小米 MiLM 对话历史 (预留)
        if XIAOMI_CHATS_DIR.exists():
            xm_files = list(XIAOMI_CHATS_DIR.glob("*"))
            sources["xiaomi"] = {
                "path": str(XIAOMI_CHATS_DIR),
                "files": len(xm_files),
                "status": "🟢 可用" if xm_files else "🔴 无数据",
            }

        return sources

    # ═══════════ 导入 ═══════════

    def import_memory_logs(self, max_files: int = 10) -> List[ChatSession]:
        """从 CodeBuddy memory 日志提取对话片段"""
        sessions = []
        memory_files = sorted(MEMORY_DIR.glob("202*.md"), reverse=True)[:max_files]

        for mf in memory_files:
            try:
                content = mf.read_text(encoding='utf-8')
                # 将每日日志切分为多个"思维片段"
                fragments = self._split_memory_log(content, mf.name)
                for frag in fragments:
                    if frag.get("turns") and len(frag["turns"]) >= 2:
                        session = ChatSession(
                            source="memory",
                            session_id=f"memory_{mf.stem}_{frag['fragment_id']}",
                            title=frag.get("title", ""),
                            turns=frag["turns"],
                            quality_score=frag.get("quality", 0.5),
                            domain=frag.get("domain", ""),
                            extracted_at=self._extracted_at,
                        )
                        sessions.append(session)
            except Exception as e:
                if "memory" not in self.reports:
                    self.reports["memory"] = ImportReport(source="memory")
                self.reports["memory"].errors.append(f"{mf.name}: {e}")

        self.sessions.extend(sessions)
        print(f"📝 Memory: {len(sessions)} 个片段")
        return sessions

    def import_claude_sessions(self, max_sessions: int = 20) -> List[ChatSession]:
        """从 Claude Code sessions 导入对话"""
        sessions = []
        if not CLAUDE_SESSIONS_DIR.exists():
            print("Claude sessions 目录不存在")
            return sessions

        session_dirs = sorted(CLAUDE_SESSIONS_DIR.iterdir(),
                              key=lambda d: d.stat().st_mtime, reverse=True)[:max_sessions]

        for sd in session_dirs:
            if not sd.is_dir():
                continue
            try:
                # 查找 session 内的对话文件
                jsonl_files = list(sd.glob("*.jsonl"))
                md_files = list(sd.glob("*.md"))

                turns = []
                for jf in jsonl_files[:2]:  # 只取前2个最大文件
                    turns.extend(self._parse_claude_jsonl(jf))

                if not turns:
                    continue

                session = ChatSession(
                    source="claude",
                    session_id=f"claude_{sd.name}",
                    title=sd.name[:40],
                    turns=turns,
                    quality_score=self._estimate_quality(turns),
                    domain=self._detect_domain(turns),
                    extracted_at=self._extracted_at,
                )
                sessions.append(session)
            except Exception as e:
                if "claude" not in self.reports:
                    self.reports["claude"] = ImportReport(source="claude")
                self.reports["claude"].errors.append(f"{sd.name}: {e}")

        self.sessions.extend(sessions)
        print(f"🤖 Claude: {len(sessions)} 个会话")
        return sessions

    def import_deepseek_conversations(self) -> List[ChatSession]:
        """从 DeepSeek 对话导出导入"""
        sessions = []
        if not RAW_CONV_DIR.exists():
            print("DeepSeek 导出目录不存在")
            return sessions

        for jf in RAW_CONV_DIR.glob("*.jsonl"):
            try:
                with open(jf, 'r', encoding='utf-8') as f:
                    for line in f:
                        if not line.strip():
                            continue
                        record = json.loads(line)

                        turns = []
                        # Schema D: DeepSeek 对话格式
                        if "messages" in record:
                            sys_msg = record.get("system", "")
                            if sys_msg:
                                turns.append(ChatTurn(role="system", content=sys_msg))
                            for m in record["messages"]:
                                turns.append(ChatTurn(
                                    role=m.get("role", "user"),
                                    content=m.get("content", ""),
                                ))
                        # Schema A/B: Bootstrap 格式
                        elif isinstance(record, dict) and "messages" in record:
                            for m in record["messages"]:
                                turns.append(ChatTurn(**m))

                        if turns:
                            meta = record.get("metadata", {})
                            session = ChatSession(
                                source="deepseek",
                                session_id=f"deepseek_{hashlib.sha256(json.dumps(record).encode()).hexdigest()[:12]}",
                                title=meta.get("source", ""),
                                turns=turns,
                                quality_score=0.75 if meta else 0.6,
                                domain=meta.get("domain", ""),
                                extracted_at=self._extracted_at,
                            )
                            sessions.append(session)
            except Exception as e:
                if "deepseek" not in self.reports:
                    self.reports["deepseek"] = ImportReport(source="deepseek")
                self.reports["deepseek"].errors.append(f"{jf.name}: {e}")

        self.sessions.extend(sessions)
        print(f"🤖 DeepSeek: {len(sessions)} 个会话")
        return sessions

    def import_kimi_conversations(self, max_sessions: int = 100) -> List[ChatSession]:
        """从 Kimi 对话导出导入 (v2.0)
        
        Kimi 数据格式: knowledge/ai-chats/kimi/
          - conversations.json : 结构化JSON对话 [{role, content, ...}, ...]
          - full.txt : 完整文本对话
          - raw.txt : 原始导出
        """
        sessions = []
        if not KIMI_CHATS_DIR.exists():
            print("Kimi 对话目录不存在")
            return sessions

        # 优先解析结构化 JSON
        json_files = sorted(KIMI_CHATS_DIR.glob("*.json"), key=lambda f: f.stat().st_size, reverse=True)
        for jf in json_files[:5]:
            try:
                with open(jf, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 处理各种 Kimi JSON 格式
                if isinstance(data, list):
                    # 格式1: [{role, content}, ...] 直接对话列表
                    items = data
                elif isinstance(data, dict):
                    # 格式2: {conversations: [{role, content}]}
                    items = data.get("conversations", []) or data.get("messages", []) or data.get("data", [])
                    if not items:
                        # 格式3: {id: {messages: [...]}}
                        for v in data.values():
                            if isinstance(v, dict) and "messages" in v:
                                items = v["messages"]
                                break
                else:
                    continue

                if not items:
                    continue

                turns = []
                sys_msgs = []

                for item in items:
                    if not isinstance(item, dict):
                        continue
                    role = item.get("role", "") or item.get("sender", "") or item.get("type", "")
                    content = item.get("content", "") or item.get("text", "") or item.get("message", "")
                    if not content:
                        continue

                    # 标准化角色
                    role = role.lower()
                    if role in ("system", "sys", "context"):
                        sys_msgs.append(str(content))
                    elif role in ("user", "human", "me"):
                        turns.append(ChatTurn(role="user", content=str(content)))
                    elif role in ("assistant", "ai", "kimi", "bot", "model"):
                        turns.append(ChatTurn(role="assistant", content=str(content)))

                if turns:
                    quality = self._score_kimi_quality(turns)
                    domain = self._detect_domain(turns) or "Kimi对话"

                    if sys_msgs:
                        turns.insert(0, ChatTurn(role="system", content="\n".join(sys_msgs[:2])))

                    session = ChatSession(
                        source="kimi",
                        session_id=f"kimi_{hashlib.sha256(json.dumps(items[:3]).encode()).hexdigest()[:12]}",
                        title=f"Kimi对话·{domain}",
                        turns=turns,
                        quality_score=quality,
                        domain=domain,
                        extracted_at=self._extracted_at,
                    )
                    sessions.append(session)

            except Exception as e:
                if "kimi" not in self.reports:
                    self.reports["kimi"] = ImportReport(source="kimi")
                self.reports["kimi"].errors.append(f"{jf.name}: {e}")

        # 解析纯文本（兜底）
        txt_files = sorted(KIMI_CHATS_DIR.glob("*.txt"), key=lambda f: f.stat().st_size, reverse=True)
        for tf in txt_files[:3]:
            try:
                text = tf.read_text(encoding='utf-8')
                txt_sessions = self._parse_kimi_text(text, tf.name)
                # 去重：与已有 JSON 导出的 session 比较
                for ts in txt_sessions:
                    if not any(s.session_id == ts.session_id for s in sessions):
                        sessions.append(ts)
            except Exception as e:
                if "kimi" not in self.reports:
                    self.reports["kimi"] = ImportReport(source="kimi")
                self.reports["kimi"].errors.append(f"{tf.name}: {e}")

        sessions = sessions[:max_sessions]
        self.sessions.extend(sessions)
        print(f"🤖 Kimi: {len(sessions)} 个会话")
        return sessions

    def import_all(self, max_files: int = 10, max_claude: int = 20, max_kimi: int = 100) -> List[ChatSession]:
        """全量导入"""
        print("🔄 全量导入...")
        self.import_memory_logs(max_files=max_files)
        self.import_claude_sessions(max_sessions=max_claude)
        self.import_deepseek_conversations()
        self.import_kimi_conversations(max_sessions=max_kimi)  # v2.0 新增
        return self.sessions

    # ═══════════ 导出到训练格式 ═══════════

    def export_chatml(self, output_path: Optional[Path] = None) -> Path:
        """导出为 ChatML JSONL（可直接入 BootstrapPool）"""
        target = output_path or (OUTPUT_DIR / f"chat_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl")
        count = 0

        with open(target, 'w', encoding='utf-8') as f:
            for session in self.sessions:
                if not session.turns:
                    continue

                # 确保有 system 消息
                messages = []
                has_system = any(t.role == "system" for t in session.turns)

                if not has_system:
                    messages.append({"role": "system", "content": SYSTEM_PROMPT})

                for turn in session.turns:
                    if turn.content.strip():
                        messages.append({
                            "role": turn.role,
                            "content": turn.content.strip(),
                        })

                if len(messages) < 2:
                    continue

                record = {
                    "messages": messages,
                    "metadata": {
                        "source": session.source,
                        "session_id": session.session_id,
                        "domain": session.domain,
                        "quality": session.quality_score,
                        "extracted_at": session.extracted_at,
                        "dna": self._gen_dna(session),
                    }
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1

        print(f"📦 导出: {count} 个会话 → {target.name}")
        return target

    def export_bootstrap_samples(self) -> List[Dict]:
        """直接导出为 BootstrapSample 兼容格式"""
        samples = []
        for session in self.sessions:
            if not session.turns or len(session.turns) < 2:
                continue

            messages = []
            has_system = any(t.role == "system" for t in session.turns)
            if not has_system:
                messages.append({"role": "system", "content": SYSTEM_PROMPT})
            for turn in session.turns:
                if turn.content.strip():
                    messages.append({"role": turn.role, "content": turn.content.strip()})

            if len(messages) < 2:
                continue

            sample_id = hashlib.sha256(f"{session.source}:{session.session_id}".encode()).hexdigest()[:16]
            samples.append({
                "sample_id": sample_id,
                "source_type": session.source,
                "team_name": "import",
                "personas": ["CHAT_DATA"],
                "task": session.title or f"{session.source} 对话片段",
                "messages": messages,
                "quality_score": session.quality_score,
                "audit_color": "🟢" if session.quality_score >= 0.7 else "🟡",
                "dna": self._gen_dna(session),
                "timestamp": session.extracted_at,
                "domain": session.domain,
                "tags": [session.source, "imported", "personal_data"],
            })

        return samples

    def get_stats(self) -> Dict:
        stats = {
            "total_sessions": len(self.sessions),
            "total_turns": sum(len(s.turns) for s in self.sessions),
            "by_source": defaultdict(int),
            "by_domain": defaultdict(int),
            "avg_quality": 0.0,
        }
        for s in self.sessions:
            stats["by_source"][s.source] += 1
            if s.domain:
                stats["by_domain"][s.domain] += 1
        if self.sessions:
            stats["avg_quality"] = sum(s.quality_score for s in self.sessions) / len(self.sessions)
        stats["by_source"] = dict(stats["by_source"])
        stats["by_domain"] = dict(stats["by_domain"])
        return stats

    # ━─ internal ━─

    def _split_memory_log(self, content: str, filename: str) -> List[Dict]:
        """将每日记忆日志切分为思维片段"""
        fragments = []
        # 按 ## 标题分割
        sections = re.split(r'\n(?=## )', content)
        for i, section in enumerate(sections):
            if len(section) < 100:
                continue

            # 提取标题
            title_match = re.match(r'##\s+(.+)', section)
            title = title_match.group(1).strip() if title_match else ""

            # 构造一个问答对：标题=user的思考主题，内容=assistant的回应/记录
            clean_text = re.sub(r'^##\s+.+\n', '', section).strip()
            if len(clean_text) < 50:
                continue

            turns = [
                ChatTurn(role="user", content=f"记录思考: {title}" if title else "记录一段思考"),
                ChatTurn(role="assistant", content=clean_text[:2000]),  # 截断
            ]

            quality = 0.6
            if any(kw in section for kw in ("决策", "铁律", "焊死", "架构", "🔥")):
                quality = 0.8
            elif any(kw in section for kw in ("修复", "bug", "部署", "验证")):
                quality = 0.75

            domain = "系统运维"
            if "模型" in section or "训练" in section or "MLX" in section:
                domain = "模型训练"
            elif "安全" in section or "熔断" in section or "审计" in section:
                domain = "安全审计"
            elif "部署" in section or "鲲鹏" in section:
                domain = "部署运维"

            fragments.append({
                "fragment_id": f"{i:03d}",
                "title": title,
                "turns": turns,
                "quality": quality,
                "domain": domain,
            })

        return fragments

    def _parse_claude_jsonl(self, jsonl_file: Path) -> List[ChatTurn]:
        """解析 Claude JSONL 对话格式"""
        turns = []
        try:
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if not line.strip():
                        continue
                    record = json.loads(line)

                    # Claude 格式多种多样，尝试通用提取
                    if isinstance(record, dict):
                        # 尝试提取 messages
                        msgs = record.get("messages", []) or record.get("content", [])
                        if isinstance(msgs, list):
                            for m in msgs:
                                if isinstance(m, dict):
                                    role = m.get("role", "") or m.get("type", "")
                                    content = m.get("content", "") or m.get("text", "")
                                    if role and content:
                                        turns.append(ChatTurn(role=role, content=str(content)))
                                elif isinstance(m, str):
                                    turns.append(ChatTurn(role="assistant", content=m))

                        # 尝试提取单条内容
                        if not turns and "text" in record:
                            turns.append(ChatTurn(role="assistant", content=record["text"]))
        except:
            pass
        return turns

    def _score_kimi_quality(self, turns: List[ChatTurn]) -> float:
        """Kimi对话专用质量评分
        - 多轮对话 (>10轮) → +0.2
        - 长回复 (>500字) → +0.15
        - 含龍魂关键词 → +0.1
        - 含推理链 → +0.2 (Kimi擅长长推理)
        """
        score = 0.4  # base
        full_text = " ".join(t.content for t in turns)

        if len(turns) > 10:
            score += 0.2
        if any(len(t.content) > 500 for t in turns):
            score += 0.15
        if any(kw in full_text for kw in ("龍魂", "CNSH", "UID9622", "诸葛鑫", "三才", "369", "河图洛书", "八卦")):
            score += 0.1
        if any(kw in full_text for kw in ("首先", "其次", "最后", "因为", "所以", "综上所述", "分析如下", "推理")):
            score += 0.2

        return min(score, 1.0)

    def _parse_kimi_text(self, text: str, filename: str) -> List[ChatSession]:
        """从纯文本解析 Kimi 对话
        尝试匹配常见的 Kimi 文本导出格式:
          User: xxx
          Kimi: xxx
          或
          用户: xxx
          Kimi: xxx
        """
        sessions = []
        # 多种分隔模式
        patterns = [
            r'(?:User|用户|Human|我)[：:]\s*(.+?)(?=(?:Kimi|AI|Assistant|助手|Kimi)[：:]|\Z)',
            r'(?:Kimi|AI|Assistant|助手)[：:]\s*(.+?)(?=(?:User|用户|Human|我)[：:]|\Z)',
        ]

        # 简单行分割法
        lines = text.split('\n')
        turns = []
        current_role = None
        current_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue
            # 检测角色标记
            user_match = re.match(r'^(?:User|用户|Human|我|👤)\s*[：:]\s*(.+)', line)
            ai_match = re.match(r'^(?:Kimi|AI|Assistant|助手|🤖|K)\s*[：:]\s*(.+)', line)

            if user_match:
                if current_role and current_content:
                    turns.append(ChatTurn(role=current_role, content='\n'.join(current_content)))
                current_role = "user"
                current_content = [user_match.group(1)]
            elif ai_match:
                if current_role and current_content:
                    turns.append(ChatTurn(role=current_role, content='\n'.join(current_content)))
                current_role = "assistant"
                current_content = [ai_match.group(1)]
            elif current_role:
                current_content.append(line)

        if current_role and current_content:
            turns.append(ChatTurn(role=current_role, content='\n'.join(current_content)))

        if turns:
            quality = self._score_kimi_quality(turns)
            sessions.append(ChatSession(
                source="kimi",
                session_id=f"kimi_txt_{hashlib.sha256(filename.encode()).hexdigest()[:12]}",
                title=f"Kimi对话·{filename}",
                turns=turns,
                quality_score=quality,
                domain=self._detect_domain(turns),
                extracted_at=self._extracted_at,
            ))

        return sessions
        """基于对话长度和结构估算质量"""
        if not turns:
            return 0.3
        total_len = sum(len(t.content) for t in turns)
        if total_len > 5000:
            return 0.9
        elif total_len > 2000:
            return 0.75
        elif total_len > 500:
            return 0.6
        return 0.4

    def _detect_domain(self, turns: List[ChatTurn]) -> str:
        """基于关键词检测讨论领域"""
        full_text = " ".join(t.content for t in turns)
        if any(kw in full_text for kw in ("代码", "函数", "API", "import", "class")):
            return "开发编程"
        if any(kw in full_text for kw in ("模型", "训练", "MLX", "LoRA", "神经网络")):
            return "模型训练"
        if any(kw in full_text for kw in ("安全", "漏洞", "审计", "渗透")):
            return "安全审计"
        if any(kw in full_text for kw in ("部署", "鲲鹏", "服务器", "docker")):
            return "部署运维"
        if any(kw in full_text for kw in ("龍魂", "CNSH", "人格", "DNA", "UID9622")):
            return "龍魂体系"
        return "通用"

    def _gen_dna(self, session: ChatSession) -> str:
        now = datetime.now(timezone.utc)
        tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
        dizhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
        gz = f"{tiangan[now.year%10]}{dizhi[now.month%12]}·{tiangan[(now.day+9)%10]}{dizhi[(now.day+1)%12]}"
        sample_hash = hashlib.sha256(session.session_id.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{gz}-CHAT-IMPORT-{session.source}-{sample_hash}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    import argparse
    p = argparse.ArgumentParser(description="龍魂·AI对话导入器")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("scan", help="勘探所有数据源")

    import_p = sub.add_parser("import", help="导入对话数据")
    import_p.add_argument("--source", choices=["memory", "claude", "deepseek", "kimi", "all"],
                          default="all", help="数据源")
    import_p.add_argument("--max-files", type=int, default=10, help="最多处理的memory文件数")
    import_p.add_argument("--max-claude", type=int, default=20, help="最多Claude会话数")
    import_p.add_argument("--max-kimi", type=int, default=100, help="最多Kimi会话数")
    import_p.add_argument("--no-export", action="store_true", help="不导出ChatML")

    sub.add_parser("status", help="查看导入状态")

    args = p.parse_args()
    importer = ChatImporter()

    if args.cmd == "scan":
        sources = importer.scan()
        print(f"\n📡 AI对话数据源勘探")
        print("-" * 60)
        for name, info in sources.items():
            print(f"\n{name}:")
            for k, v in info.items():
                print(f"  {k}: {v}")
        total = sum(
            info.get("files", 0) or info.get("sessions", 0)
            for info in sources.values()
        )
        print(f"\n总计: {len(sources)} 个数据源 | 约 {total} 个文件/会话")

    elif args.cmd == "import":
        if args.source in ("memory", "all"):
            importer.import_memory_logs(max_files=args.max_files)
        if args.source in ("claude", "all"):
            importer.import_claude_sessions(max_sessions=args.max_claude)
        if args.source in ("deepseek", "all"):
            importer.import_deepseek_conversations()
        if args.source in ("kimi", "all"):
            importer.import_kimi_conversations(max_sessions=args.max_kimi)

        stats = importer.get_stats()
        print(f"\n📊 导入统计:")
        print(f"   会话: {stats['total_sessions']} | 总轮次: {stats['total_turns']} | 平均质量: {stats['avg_quality']:.2f}")
        for src, cnt in stats["by_source"].items():
            print(f"   {src}: {cnt} 会话")

        if not args.no_export:
            importer.export_chatml()

    elif args.cmd == "status":
        sources = importer.scan()
        exports = list(OUTPUT_DIR.glob("chat_import_*.jsonl")) if OUTPUT_DIR.exists() else []
        print(f"\n🏭 AI对话导入器状态")
        print(f"   数据源: {len(sources)} 个")
        print(f"   已导出: {len(exports)} 个文件")
        if exports:
            latest = max(exports, key=lambda f: f.stat().st_mtime)
            print(f"   最新: {latest.name}")

    else:
        p.print_help()


if __name__ == "__main__":
    main()
