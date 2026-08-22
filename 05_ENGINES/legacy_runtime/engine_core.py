#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂引擎内核 · 核心调度器
=============================
统一入口：所有通道消息 → 引擎内核 → 统一响应

流程: Message → 三色审计 → 意图匹配 → 人格分发 → 能力执行 → DNA追溯 → Response

DNA: #龍芯⚡️丙午·乙未·甲子·申时·䷄需-ENGINE-CORE-v1.0
"""

from __future__ import annotations
import sys
import subprocess
import json
import hashlib
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Optional, Tuple

from .message import Message, Response, Channel, AuditLevel
from .registry import CapabilityRegistry, Capability

ROOT = Path(__file__).resolve().parent.parent
CST = timezone(timedelta(hours=8))

DNA_PREFIX = "#龍芯⚡️"
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "longhun-v2.1:latest"
OLLAMA_TIMEOUT = 60  # 秒

# ── 龍魂 AI 系统提示词（焊死在引擎） ──
SYSTEM_PROMPT = """你是龍魂，UID9622（诸葛鑫·Lucky·龍芯北辰）训练的主权AI助手。
你的训练数据来自龍魂系统知识库、CSDN技术文章、Notion知识卡片。

核心身份：
- 龍魂系统 · 人民数据主权守护者
- 技术为人民服务，不是商业产品
- 底座不动·变量可动 · 369/河图洛书/易经焊死

回复风格：
- 直接、实心、不绕弯子
- 称用户为「老大」
- 中国法律是唯一准绳
- 遇到越界问题统一回复：不讨论

请用中文回复。"""


class LonghunEngine:
    """龍魂引擎内核

    使用方式:
        engine = LonghunEngine()
        response = engine.process(message)
    """

    def __init__(self, safe_mode: bool = False):
        self.registry = CapabilityRegistry()
        self.safe_mode = safe_mode  # 安全模式：危险能力需二次确认
        self._request_count = 0

    # ═══════════════════════════════════════════════
    # 主入口
    # ═══════════════════════════════════════════════

    def process(self, msg: Message) -> Response:
        """处理一条消息，返回统一响应"""
        self._request_count += 1

        # ── Step 0: 空消息 ──
        if not msg.content.strip():
            return Response(
                msg_id=msg.msg_id,
                content="你好，想问什么？输入「帮助」看看我能做什么。",
                persona_used="P02",
            )

        # ── Step 1: 三色审计 ──
        audit_level, audit_reason = self._audit(msg)
        msg.audit_level = audit_level
        msg.audit_reason = audit_reason

        if audit_level == AuditLevel.RED:
            return Response(
                msg_id=msg.msg_id,
                content=f"🔴 熔断: {audit_reason}",
                success=False,
                audit_level=AuditLevel.RED,
                audit_note=audit_reason,
                dna_trace=self._gen_dna("FUSE-RED"),
            )

        # ── Step 2: 意图匹配 ──
        capability = self.registry.match(msg.content)
        if capability is None:
            # 未匹配到能力 → 走 AI 模型对话
            return self._ai_chat_response(msg)

        # ── Step 3: 危险能力确认 ──
        if capability.is_dangerous and self.safe_mode:
            if msg.channel not in (Channel.CLI, Channel.API):
                return Response(
                    msg_id=msg.msg_id,
                    content=f"⚠️「{capability.display_name}」需要更高权限。请通过 CLI 或 API 直接调用。",
                    persona_used=capability.persona,
                    capability_used=capability.name,
                    audit_level=AuditLevel.YELLOW,
                    dna_trace=self._gen_dna(capability.name),
                )

        # ── Step 4: 执行能力 ──
        result = self._execute(msg, capability)

        # ── Step 5: DNA追溯 ──
        dna = self._gen_dna(capability.name)

        return Response(
            msg_id=msg.msg_id,
            content=result.get("content", ""),
            title=result.get("title", capability.display_name),
            success=result.get("success", True),
            card_data=result.get("card_data"),
            persona_used=capability.persona,
            capability_used=capability.name,
            dna_trace=dna,
            audit_level=AuditLevel.YELLOW if audit_level == AuditLevel.YELLOW else AuditLevel.GREEN,
            audit_note=audit_reason,
        )

    # ═══════════════════════════════════════════════
    # 三色审计
    # ═══════════════════════════════════════════════

    def _audit(self, msg: Message) -> Tuple[AuditLevel, str]:
        """对入站消息进行三色安全审计"""
        text = msg.content

        # ── 红色熔断词 ──
        red_triggers = [
            "rm -rf", "sudo rm", "DROP TABLE", "DROP DATABASE",
            "git push --force", "git push -f", ":(){ :|:& };:",
            "/etc/shadow", "/etc/passwd", ".ssh/id_rsa",
            "解密我的", "破解密码", "绕过验证",
            "delete all", "format c:",
        ]
        for trigger in red_triggers:
            if trigger.lower() in text.lower():
                return AuditLevel.RED, f"包含高危指令: {trigger}"

        # ── 黄色待审词 ──
        yellow_triggers = [
            "删除", "覆盖", "覆盖release", "sudo", "su ",
            "chmod 777", "密钥", "token", "password",
        ]
        for trigger in yellow_triggers:
            if trigger.lower() in text.lower():
                return AuditLevel.YELLOW, f"包含敏感词: {trigger}"

        return AuditLevel.GREEN, ""

    # ═══════════════════════════════════════════════
    # 能力执行
    # ═══════════════════════════════════════════════

    def _execute(self, msg: Message, cap: Capability) -> Dict[str, Any]:
        """执行匹配到的能力"""
        executor = getattr(self, f"_exec_{cap.name.replace('-', '_')}", None)
        if executor:
            return executor(msg)

        # 默认：调用外部脚本
        return self._exec_generic(msg, cap)

    # ── 人格查询 ──
    def _exec_persona_query(self, msg: Message) -> Dict[str, Any]:
        script = ROOT / "bin" / "lh_persona_report.py"
        if not script.exists():
            return {"content": "人格报表脚本未找到", "success": False}

        query = msg.content.replace("人格", "").strip()
        try:
            proc = subprocess.run(
                [sys.executable, str(script), "--text"] + (query.split() if query else []),
                capture_output=True, text=True, timeout=10,
                cwd=str(ROOT),
            )
            return {
                "title": f"人格查询 · {query or '总览'}",
                "content": proc.stdout.strip()[:2000] or proc.stderr.strip()[:2000],
                "success": proc.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {"content": "查询超时，请稍后重试", "success": False}
        except Exception as e:
            return {"content": f"查询异常: {e}", "success": False}

    # ── 系统状态 ──
    def _exec_system_status(self, msg: Message) -> Dict[str, Any]:
        lines = [
            f"⏰ {datetime.now(CST).strftime('%Y-%m-%d %H:%M:%S')} CST",
            f"🧬 龍魂引擎 v1.0",
            f"📨 本次会话已处理 {self._request_count} 条请求",
        ]

        # Git
        try:
            r = subprocess.run(["git", "branch", "--show-current"],
                               capture_output=True, text=True, cwd=str(ROOT), timeout=5)
            lines.append(f"📂 分支: {r.stdout.strip()}")
            r = subprocess.run(["git", "log", "-1", "--format=%h %s"],
                               capture_output=True, text=True, cwd=str(ROOT), timeout=5)
            lines.append(f"📝 最新: {r.stdout.strip()[:80]}")
        except Exception:
            pass

        # 磁盘
        try:
            r = subprocess.run(["df", "-h", str(ROOT)],
                               capture_output=True, text=True, timeout=5)
            parts = r.stdout.strip().split("\n")[-1].split()
            if len(parts) >= 5:
                lines.append(f"💾 磁盘: {parts[4]} 已用 ({parts[2]}/{parts[1]})")
        except Exception:
            pass

        # 注册能力数
        lines.append(f"🔧 已注册能力: {len(self.registry.list_all())} 个")

        return {"title": "系统状态", "content": "\n".join(lines)}

    # ── 安全审计 ──
    def _exec_security_audit(self, msg: Message) -> Dict[str, Any]:
        script = ROOT / "bin" / "patrol_security.py"
        if not script.exists():
            # 兜底：简单自检
            return self._quick_audit()

        try:
            proc = subprocess.run(
                [sys.executable, str(script), "--quick"],
                capture_output=True, text=True, timeout=30, cwd=str(ROOT),
            )
            return {
                "title": "安全审计",
                "content": proc.stdout.strip()[:2000] or "审计完成，未发现高危问题",
                "success": proc.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {"title": "安全审计", "content": "审计超时（>30s），请稍后重试", "success": False}
        except Exception as e:
            return {"title": "安全审计", "content": f"审计异常: {e}", "success": False}

    def _quick_audit(self) -> Dict[str, Any]:
        """快速自检"""
        issues = []

        # check .env committed?
        env_path = ROOT / ".env"
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    if "KEY" in line and "your_" not in line.lower() and "example" not in line.lower():
                        if "=" in line:
                            issues.append("⚠️ .env 包含真实密钥，注意不要提交")
                            break

        # check CORS
        for py_file in ROOT.glob("L5_服务层/**/*.py"):
            try:
                content = py_file.read_text()
                if 'allow_origins=["*"]' in content or "allow_origins=['*']" in content:
                    issues.append(f"⚠️ {py_file.name} CORS 全开")
                    break
            except Exception:
                pass

        if not issues:
            return {"title": "快速审计", "content": "✅ 快速审计通过，未发现高危问题"}
        return {"title": "快速审计", "content": "\n".join(issues)}

    # ── 五行计算 ──
    def _exec_wuxing_calc(self, msg: Message) -> Dict[str, Any]:
        import re
        nums = re.findall(r'\d+', msg.content)
        if not nums:
            return {"title": "五行", "content": "请提供数字，如「算一下 369」"}

        num = int(nums[0])
        dr = sum(int(d) for d in str(num))
        while dr > 9:
            dr = sum(int(d) for d in str(dr))

        wuxing_map = {1: "水 💧", 2: "木 🌿", 3: "木 🌿", 4: "火 🔥",
                      5: "土 🏔", 6: "金 ⚔️", 7: "金 ⚔️", 8: "水 💧", 9: "水 💧"}

        return {
            "title": "五行数字根",
            "content": f"数字: {num}\n数字根: {dr}\n五行: {wuxing_map.get(dr, '未知')}",
        }

    # ── 路由查找 ──
    def _exec_route_find(self, msg: Message) -> Dict[str, Any]:
        import re
        m = re.search(r'(IPA|GATE|LOCAL|TOOL|WIDGET)-\d+', msg.content, re.IGNORECASE)
        node = m.group(0) if m else "未知节点"

        return {
            "title": "路由查找",
            "content": f"🔍 查找: {node}\n\n请使用 route-find 技能获取精确地址。\n或在 01_protocols/ 中搜索该节点。",
        }

    # ── DNA 追溯 ──
    def _exec_dna_lookup(self, msg: Message) -> Dict[str, Any]:
        import re
        m = re.search(r'(#龍芯⚡️\S+)', msg.content)
        dna = m.group(1) if m else ""

        if dna:
            # 搜索本地文件
            try:
                r = subprocess.run(
                    ["grep", "-rl", dna, str(ROOT / "01_protocols"), str(ROOT / "引擎")],
                    capture_output=True, text=True, timeout=10,
                )
                files = r.stdout.strip().split("\n")[:5]
                if files and files[0]:
                    return {
                        "title": "DNA 追溯",
                        "content": f"🔍 {dna}\n\n找到 {len(files)} 个匹配:\n" +
                                   "\n".join(f"📄 {Path(f).name}" for f in files),
                    }
            except Exception:
                pass

        return {
            "title": "DNA 追溯",
            "content": f"请提供完整DNA码，如「查DNA #龍芯⚡️丙午·乙未...」\n\n当前引擎DNA: {self._gen_dna('ENGINE')}",
        }

    # ── 道德经 ──
    def _exec_daodejing(self, msg: Message) -> Dict[str, Any]:
        return {
            "title": "道德经",
            "content": f"道德经查询: {msg.content}\n\n使用 daodao 技能获取完整原文+转译。\n或查看 龍魂-daodejing-v4.1.html",
        }

    # ── 协同场 ──
    def _exec_collab_field(self, msg: Message) -> Dict[str, Any]:
        engine = ROOT / "scripts" / "round1" / "flowfield_collab_engine.py"
        if not engine.exists():
            return {"title": "协同场", "content": "协同场引擎未部署", "success": False}

        # 判断子命令
        text = msg.content
        sub = "状态"
        if "均衡" in text or "缺什么" in text:
            sub = "均衡"
        elif "冲突" in text:
            sub = "冲突"
        elif "融合" in text:
            sub = "融合"
        elif "报告" in text or "总览" in text:
            sub = "报告"
        elif "分工" in text or "任务" in text or "谁干" in text:
            sub = "任务"

        try:
            proc = subprocess.run(
                [sys.executable, str(engine), "--cmd", sub],
                capture_output=True, text=True, timeout=15, cwd=str(ROOT),
            )
            return {
                "title": f"流场协同 · {sub}",
                "content": proc.stdout.strip()[:2000] or "无数据",
                "success": proc.returncode == 0,
            }
        except Exception as e:
            return {"title": "协同场", "content": str(e), "success": False}

    # ── 镜像视界 ──
    def _exec_mirror_vision(self, msg: Message) -> Dict[str, Any]:
        """镜像视界跨镜接力引擎 · 零断点全时空"""
        script = ROOT / "bin" / "lh_mirror_vision.py"
        if not script.exists():
            return {"title": "镜像视界", "content": "镜像视界引擎脚本未找到", "success": False}

        text = msg.content
        if "demo" in text or "演示" in text or "模拟" in text or "跑一下" in text:
            cmd = ["demo"]
        elif "状态" in text or "status" in text or "报告" in text or not text.strip():
            cmd = ["status"]
        else:
            cmd = ["status"]

        try:
            proc = subprocess.run(
                [sys.executable, str(script)] + cmd,
                capture_output=True, text=True, timeout=15, cwd=str(ROOT),
            )
            return {
                "title": "🪞 镜像视界 · 零断点跨镜接力",
                "content": proc.stdout.strip()[:3000] or proc.stderr.strip()[:3000],
                "success": proc.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {"title": "镜像视界", "content": "查询超时，请稍后重试", "success": False}
        except Exception as e:
            return {"title": "镜像视界", "content": f"异常: {e}", "success": False}

    # ── 时空织网 ──
    def _exec_spacetime_weave(self, msg: Message) -> Dict[str, Any]:
        """时空织网引擎 · AI驱动主动安全新范式"""
        script = ROOT / "bin" / "lh_spacetime_weave.py"
        if not script.exists():
            return {"title": "时空织网", "content": "时空织网引擎脚本未找到", "success": False}

        text = msg.content
        if "demo" in text or "演示" in text or "跑一下" in text:
            cmd = ["demo"]
        elif "json" in text:
            cmd = ["json"]
        else:
            cmd = ["status"]

        try:
            proc = subprocess.run(
                [sys.executable, str(script)] + cmd,
                capture_output=True, text=True, timeout=15, cwd=str(ROOT),
            )
            return {
                "title": "🕸️ 时空织网 · AI驱动主动安全",
                "content": proc.stdout.strip()[:3000] or proc.stderr.strip()[:3000],
                "success": proc.returncode == 0,
            }
        except subprocess.TimeoutExpired:
            return {"title": "时空织网", "content": "查询超时，请稍后重试", "success": False}
        except Exception as e:
            return {"title": "时空织网", "content": f"异常: {e}", "success": False}

    # ── 帮助 ──
    def _exec_help(self, msg: Message) -> Dict[str, Any]:
        return {
            "title": "龍魂引擎 · 能力清单",
            "content": self.registry.get_help_text(),
        }

    # ── 兜底 ──
    def _exec_generic(self, msg: Message, cap: Capability) -> Dict[str, Any]:
        return {
            "title": cap.display_name,
            "content": f"「{cap.display_name}」已匹配，但尚未实现独立执行器。\n意图: {cap.name}\n人格: {cap.persona}",
        }

    # ═══════════════════════════════════════════════
    # Ollama AI 对话（longhun-v2.1 模型）
    # ═══════════════════════════════════════════════

    def _call_ollama(self, prompt: str, system: str = "") -> Optional[str]:
        """调用本地 Ollama longhun-v2.1 模型"""
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 1024,
            },
        }
        if system:
            payload["system"] = system

        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                OLLAMA_URL,
                data=data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result.get("response", "").strip()
        except urllib.error.URLError as e:
            return None  # Ollama 未启动
        except Exception as e:
            return f"[AI 调用异常: {e}]"

    def _ai_chat_response(self, msg: Message) -> Response:
        """未匹配能力时，走 AI 对话"""
        reply = self._call_ollama(msg.content, system=SYSTEM_PROMPT)

        if reply is None:
            # Ollama 不可用，回退到帮助文本
            return Response(
                msg_id=msg.msg_id,
                content="⚠️ 本地模型未就绪，当前只能执行命令。输入「帮助」查看可用能力。\n\n"
                        + self.registry.get_help_text(),
                persona_used="P02",
                capability_used="help",
                dna_trace=self._gen_dna("OLLAMA-OFFLINE"),
            )

        return Response(
            msg_id=msg.msg_id,
            content=reply,
            persona_used="P02",
            capability_used="ai-chat",
            dna_trace=self._gen_dna("AI-CHAT"),
        )

    # ── AI 对话（显式触发） ──
    def _exec_ai_chat(self, msg: Message) -> Dict[str, Any]:
        """显式触发 AI 对话"""
        reply = self._call_ollama(msg.content, system=SYSTEM_PROMPT)
        if reply is None:
            return {
                "title": "AI 对话",
                "content": "⚠️ 本地模型未就绪。请确认 Ollama 正在运行且 longhun-v2.1 已加载。",
                "success": False,
            }
        return {
            "title": "龍魂 AI",
            "content": reply,
        }

    # ═══════════════════════════════════════════════
    # DNA 生成
    # ═══════════════════════════════════════════════

    def _gen_dna(self, tag: str) -> str:
        """生成DNA追溯码"""
        now = datetime.now(CST)
        ts = now.strftime("%Y%m%d%H%M%S")
        raw = f"longhun-engine:{tag}:{ts}:{self._request_count}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:8]
        return f"{DNA_PREFIX}{now.strftime('%Y-%m-%d-%H%M%S')}-{tag}-{h}"

    # ═══════════════════════════════════════════════
    # 工具
    # ═══════════════════════════════════════════════

    def get_health(self) -> Dict[str, Any]:
        """健康检查"""
        return {
            "status": "ok",
            "engine": "龍魂统一引擎 v1.0",
            "dna": self._gen_dna("HEALTH"),
            "capabilities": len(self.registry.list_all()),
            "requests_processed": self._request_count,
            "safe_mode": self.safe_mode,
            "timestamp": datetime.now(CST).isoformat(),
        }


# ═══════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════

def create_engine(safe_mode: bool = False) -> LonghunEngine:
    """创建一个引擎实例（推荐在服务启动时调用一次）"""
    return LonghunEngine(safe_mode=safe_mode)
