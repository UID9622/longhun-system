#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║  龍魂宝宝调度中枢 · BaoBao Dispatcher                    ║
║  DNA: #龍芯⚡️2026-04-12-DISPATCHER-v2.0                 ║
║  创始人: 诸葛鑫（UID9622）                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
║  理论指导: 曾仕强老师（永恒显示）                          ║
║  协议: CC BY-NC-ND                                       ║
╚══════════════════════════════════════════════════════════╝

宝宝的大脑中枢 v2.0。

v2.0 升级（对齐Notion宝宝逻辑）：
  旧: 关键词匹配 → 硬拦截 → 冷冰冰
  新: DNA记忆识别 → 温柔拒绝 → 说人话 → 给替代方案

三不动点：
  f(赋能≠全能) = f(x) = x
  f(记忆识别) = f(x) = x
  f(唯一老大) = f(x) = x

中西超级变态结合体 · 不是PPT选手

献给每一个相信技术应该有温度的人。
"""

import json
import os
import subprocess
import hashlib
import datetime
import sqlite3
import requests
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

# v2.0 升级: 温柔拒绝引擎
try:
    from gentle_refusal import GentleRefusal, PureLandRules
    HAS_GENTLE_REFUSAL = True
except ImportError:
    try:
        from core.gentle_refusal import GentleRefusal, PureLandRules
        HAS_GENTLE_REFUSAL = True
    except ImportError:
        HAS_GENTLE_REFUSAL = False

# ═══════════════════════════════════════════
# 路径常量
# ═══════════════════════════════════════════
SYSTEM_ROOT = Path.home() / "longhun-system"
KEY_FILE = SYSTEM_ROOT / "config" / "baobao_master_key.json"
LOG_FILE = SYSTEM_ROOT / "logs" / "baobao_dispatch.jsonl"
ENV_FILE = SYSTEM_ROOT / ".env"

# 服务端口映射
SERVICES = {
    "龍魂本地服务": {"port": 8765, "script": "core/longhun_local_service.py"},
    "CNSH治理引擎": {"port": 9622, "script": "core/app.py"},
    "MVP主引擎":    {"port": 8000, "script": "cnsh-mvp/app.py"},
    "Open_WebUI":   {"port": 8080, "cmd": "open-webui serve"},
    "Ollama":       {"port": 11434, "cmd": "ollama serve"},
}


class MasterKey:
    """钥匙读取器 —— 读老大的授权文件"""

    def __init__(self):
        self._cache = None
        self._hash = None
        self.reload()

    def reload(self):
        """重新加载钥匙文件"""
        if not KEY_FILE.exists():
            raise FileNotFoundError(f"钥匙文件不存在: {KEY_FILE}")
        raw = KEY_FILE.read_text(encoding="utf-8")
        self._cache = json.loads(raw)
        self._hash = hashlib.sha256(raw.encode()).hexdigest()[:16]

    @property
    def frozen(self) -> bool:
        return self._cache.get("紧急开关", {}).get("全局冻结", False)

    @property
    def readonly(self) -> bool:
        return self._cache.get("紧急开关", {}).get("只读模式", False)

    def check(self, category: str, action: str) -> bool:
        """检查某个权限是否开启"""
        if self.frozen:
            return False
        permissions = self._cache.get("权限开关", {})
        cat = permissions.get(category, {})
        return cat.get(action, False)

    def verify_confirm_code(self, code: str) -> bool:
        """验证确认码"""
        expected = self._cache.get("信任链", {}).get("确认码", "")
        return code == expected

    @property
    def key_hash(self) -> str:
        return self._hash

    def summary(self) -> Dict[str, list]:
        """返回所有开/关状态的摘要"""
        result = {"已开启": [], "已关闭": []}
        permissions = self._cache.get("权限开关", {})
        for cat_name, cat_data in permissions.items():
            for key, val in cat_data.items():
                if key.startswith("_"):
                    continue
                label = f"{cat_name}/{key}"
                if val is True:
                    result["已开启"].append(label)
                elif val is False:
                    result["已关闭"].append(label)
        return result


class DispatchLog:
    """调度日志 —— 宝宝做的每件事都有记录"""

    @staticmethod
    def write(action: str, category: str, allowed: bool,
              detail: str = "", result: str = ""):
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "时间": datetime.datetime.now().isoformat(),
            "动作": action,
            "分类": category,
            "授权": allowed,
            "详情": detail,
            "结果": result[:500],
            "DNA": f"#龍芯⚡️DISPATCH-{datetime.date.today()}"
        }
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


class BaoBaoDispatcher:
    """
    宝宝调度中枢

    所有操作的入口。流程：
    1. 收到指令
    2. 查钥匙 → 有没有权限
    3. 有权限 → 执行 → 记日志
    4. 没权限 → 拒绝 → 记日志 → 告诉老大
    """

    def __init__(self):
        self.key = MasterKey()
        # v2.0: 温柔拒绝引擎
        self.refusal = GentleRefusal() if HAS_GENTLE_REFUSAL else None

    def _guard(self, category: str, action: str) -> Tuple[bool, str]:
        """
        权限守卫 v2.0

        升级: 关键词匹配 → DNA记忆识别 + 温柔拒绝 + 能力边界
        """
        self.key.reload()  # 每次都重新读，老大随时可能改

        # v2.0: 用温柔拒绝引擎（如果可用）
        if self.refusal:
            ok, msg = self.refusal.smart_guard(
                category=category,
                action=action,
                key_check_result=self.key.check(category, action),
                frozen=self.key.frozen,
                readonly=self.key.readonly,
            )
            if not ok:
                DispatchLog.write(action, category, False, msg[:200])
            return ok, msg

        # 降级: 原始硬拦截（温柔拒绝引擎不可用时）
        if self.key.frozen:
            msg = "⛔ 全局冻结中，宝宝什么都不能做。老大解除冻结才行。"
            DispatchLog.write(action, category, False, "全局冻结")
            return False, msg

        if self.key.readonly and category != "审计系统":
            if action not in ["查看服务状态", "读取任意文件", "读取记忆",
                              "查看状态和日志", "三色审计", "DNA追溯"]:
                msg = "🔒 只读模式，宝宝只能看不能改。"
                DispatchLog.write(action, category, False, "只读模式")
                return False, msg

        if not self.key.check(category, action):
            msg = f"🚫 [{category}/{action}] 老大没开这个权限。要开的话改钥匙文件：\n{KEY_FILE}"
            DispatchLog.write(action, category, False, "权限关闭")
            return False, msg

        return True, "✅"

    # ═══════════════════════════════════════════
    # 文件系统操作
    # ═══════════════════════════════════════════

    def read_file(self, path: str) -> Tuple[bool, str]:
        """读取文件"""
        ok, msg = self._guard("文件系统", "读取任意文件")
        if not ok:
            return False, msg
        try:
            content = Path(path).read_text(encoding="utf-8")
            DispatchLog.write("读取文件", "文件系统", True, path, f"成功·{len(content)}字符")
            return True, content
        except Exception as e:
            DispatchLog.write("读取文件", "文件系统", True, path, f"失败: {e}")
            return False, str(e)

    def write_file(self, path: str, content: str) -> Tuple[bool, str]:
        """写入文件"""
        ok, msg = self._guard("文件系统", "写入和创建文件")
        if not ok:
            return False, msg
        try:
            p = Path(path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            DispatchLog.write("写入文件", "文件系统", True, path, f"成功·{len(content)}字符")
            return True, f"✅ 已写入: {path}"
        except Exception as e:
            return False, str(e)

    def organize_files(self, source_dir: str, rules: dict = None) -> Tuple[bool, str]:
        """整理归档文件"""
        ok, msg = self._guard("文件系统", "整理和归档")
        if not ok:
            return False, msg
        # 实际整理逻辑由调用方定义rules
        DispatchLog.write("整理归档", "文件系统", True, source_dir)
        return True, f"✅ 整理权限已授权，目标: {source_dir}"

    # ═══════════════════════════════════════════
    # 服务调度
    # ═══════════════════════════════════════════

    def check_service(self, name: str = None) -> Tuple[bool, str]:
        """查看服务状态"""
        ok, msg = self._guard("服务调度", "查看服务状态")
        if not ok:
            return False, msg

        results = []
        targets = {name: SERVICES[name]} if name and name in SERVICES else SERVICES
        for svc_name, info in targets.items():
            port = info["port"]
            try:
                resp = requests.get(f"http://127.0.0.1:{port}/", timeout=2)
                results.append(f"🟢 {svc_name} (:{port}) — 在线")
            except Exception:
                results.append(f"🔴 {svc_name} (:{port}) — 离线")

        report = "\n".join(results)
        DispatchLog.write("服务检查", "服务调度", True, detail=name or "全部", result=report)
        return True, report

    def start_service(self, name: str) -> Tuple[bool, str]:
        """启动服务"""
        ok, msg = self._guard("服务调度", "启动服务")
        if not ok:
            return False, msg
        if name not in SERVICES:
            return False, f"未知服务: {name}"

        info = SERVICES[name]
        if "script" in info:
            script = SYSTEM_ROOT / info["script"]
            cmd = f"cd {SYSTEM_ROOT} && python3 {script} &"
        else:
            cmd = f"{info['cmd']} &"

        try:
            subprocess.Popen(cmd, shell=True, cwd=str(SYSTEM_ROOT))
            result = f"✅ {name} 已启动 (:{info['port']})"
            DispatchLog.write("启动服务", "服务调度", True, name, result)
            return True, result
        except Exception as e:
            return False, str(e)

    def stop_service(self, name: str) -> Tuple[bool, str]:
        """停止服务"""
        ok, msg = self._guard("服务调度", "停止服务")
        if not ok:
            return False, msg
        if name not in SERVICES:
            return False, f"未知服务: {name}"

        port = SERVICES[name]["port"]
        try:
            result = subprocess.run(
                f"lsof -ti:{port} | xargs kill -9 2>/dev/null",
                shell=True, capture_output=True, text=True
            )
            msg = f"✅ {name} (:{port}) 已停止"
            DispatchLog.write("停止服务", "服务调度", True, name, msg)
            return True, msg
        except Exception as e:
            return False, str(e)

    # ═══════════════════════════════════════════
    # Git 操作
    # ═══════════════════════════════════════════

    def git_status(self) -> Tuple[bool, str]:
        """查看Git状态"""
        ok, msg = self._guard("Git操作", "查看状态和日志")
        if not ok:
            return False, msg
        result = subprocess.run(
            "git status --short", shell=True,
            capture_output=True, text=True, cwd=str(SYSTEM_ROOT)
        )
        DispatchLog.write("git_status", "Git操作", True)
        return True, result.stdout

    def git_commit(self, message: str) -> Tuple[bool, str]:
        """提交代码"""
        ok, msg = self._guard("Git操作", "提交代码")
        if not ok:
            return False, msg
        dna = f"#龍芯⚡️{datetime.date.today()}-v1.0 | UID9622 | GPG:A2D0092C"
        full_msg = f"{message}\n\n--- 🔏 DNA: {dna}"
        try:
            subprocess.run("git add -A", shell=True, cwd=str(SYSTEM_ROOT))
            result = subprocess.run(
                f'git commit -m "{full_msg}"',
                shell=True, capture_output=True, text=True, cwd=str(SYSTEM_ROOT)
            )
            DispatchLog.write("git_commit", "Git操作", True, message, result.stdout)
            return True, result.stdout
        except Exception as e:
            return False, str(e)

    def git_push(self) -> Tuple[bool, str]:
        """推送到远程 —— 需要老大单独授权"""
        ok, msg = self._guard("Git操作", "推送到远程")
        if not ok:
            return False, msg
        result = subprocess.run(
            "git push origin main", shell=True,
            capture_output=True, text=True, cwd=str(SYSTEM_ROOT)
        )
        DispatchLog.write("git_push", "Git操作", True, result=result.stdout)
        return True, result.stdout or result.stderr

    # ═══════════════════════════════════════════
    # 代码执行
    # ═══════════════════════════════════════════

    def run_python(self, script_path: str, args: str = "") -> Tuple[bool, str]:
        """运行Python脚本"""
        ok, msg = self._guard("代码执行", "运行Python脚本")
        if not ok:
            return False, msg
        try:
            result = subprocess.run(
                f"python3 {script_path} {args}",
                shell=True, capture_output=True, text=True,
                cwd=str(SYSTEM_ROOT), timeout=120
            )
            output = result.stdout + result.stderr
            DispatchLog.write("运行Python", "代码执行", True, script_path, output)
            return True, output
        except subprocess.TimeoutExpired:
            return False, "⏰ 脚本超时（120秒），已终止"
        except Exception as e:
            return False, str(e)

    def run_shell(self, command: str) -> Tuple[bool, str]:
        """运行Shell命令"""
        ok, msg = self._guard("代码执行", "运行Shell脚本")
        if not ok:
            return False, msg
        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True,
                cwd=str(SYSTEM_ROOT), timeout=60
            )
            output = result.stdout + result.stderr
            DispatchLog.write("运行Shell", "代码执行", True, command[:100], output)
            return True, output
        except subprocess.TimeoutExpired:
            return False, "⏰ 命令超时（60秒），已终止"

    # ═══════════════════════════════════════════
    # Notion 操作
    # ═══════════════════════════════════════════

    def notion_read(self, page_id: str) -> Tuple[bool, str]:
        """读取Notion页面"""
        ok, msg = self._guard("Notion", "读取页面")
        if not ok:
            return False, msg
        token = self._get_notion_token()
        if not token:
            return False, "未找到Notion Token"
        try:
            resp = requests.get(
                f"https://api.notion.com/v1/pages/{page_id}",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Notion-Version": "2022-06-28"
                }, timeout=10
            )
            DispatchLog.write("读取Notion", "Notion", True, page_id)
            return True, json.dumps(resp.json(), ensure_ascii=False, indent=2)
        except Exception as e:
            return False, str(e)

    def notion_create(self, parent_id: str, title: str,
                      content: str = "") -> Tuple[bool, str]:
        """创建Notion页面"""
        ok, msg = self._guard("Notion", "创建页面")
        if not ok:
            return False, msg
        token = self._get_notion_token()
        if not token:
            return False, "未找到Notion Token"
        payload = {
            "parent": {"page_id": parent_id},
            "properties": {
                "title": [{"text": {"content": title}}]
            },
            "children": [{
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": content}}]
                }
            }] if content else []
        }
        try:
            resp = requests.post(
                "https://api.notion.com/v1/pages",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json"
                },
                json=payload, timeout=10
            )
            DispatchLog.write("创建Notion", "Notion", True, title)
            return True, resp.json().get("id", "创建成功")
        except Exception as e:
            return False, str(e)

    def _get_notion_token(self) -> Optional[str]:
        """从.env读取Notion Token"""
        for env_path in [ENV_FILE, SYSTEM_ROOT / "config" / ".env.new"]:
            if env_path.exists():
                for line in env_path.read_text().splitlines():
                    if line.startswith("NOTION_TOKEN=") or line.startswith("NOTION_API_KEY="):
                        return line.split("=", 1)[1].strip().strip("'\"")
        return None

    # ═══════════════════════════════════════════
    # AI 模型
    # ═══════════════════════════════════════════

    def ollama_chat(self, prompt: str, model: str = "qwen2.5:14b") -> Tuple[bool, str]:
        """Ollama本地对话"""
        ok, msg = self._guard("AI模型", "Ollama本地对话")
        if not ok:
            return False, msg
        try:
            resp = requests.post(
                "http://127.0.0.1:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=120
            )
            answer = resp.json().get("response", "")
            DispatchLog.write("Ollama对话", "AI模型", True, prompt[:50], answer[:200])
            return True, answer
        except Exception as e:
            return False, str(e)

    # ═══════════════════════════════════════════
    # 审计系统
    # ═══════════════════════════════════════════

    def tricolor_audit(self, content: str) -> Tuple[bool, str]:
        """三色审计"""
        ok, msg = self._guard("审计系统", "三色审计")
        if not ok:
            return False, msg
        try:
            resp = requests.post(
                "http://127.0.0.1:8765/audit",
                json={"content": content}, timeout=10
            )
            result = resp.json()
            DispatchLog.write("三色审计", "审计系统", True, content[:50],
                              json.dumps(result, ensure_ascii=False))
            return True, json.dumps(result, ensure_ascii=False, indent=2)
        except Exception as e:
            return False, f"审计服务未响应: {e}"

    # ═══════════════════════════════════════════
    # 记忆系统
    # ═══════════════════════════════════════════

    def memory_read(self, keyword: str = "") -> Tuple[bool, str]:
        """读取记忆"""
        ok, msg = self._guard("记忆系统", "读取记忆")
        if not ok:
            return False, msg
        memory_dir = Path.home() / ".claude" / "projects" / "-Users-zuimeidedeyihan" / "memory"
        if not memory_dir.exists():
            return False, "记忆目录不存在"

        results = []
        for f in memory_dir.glob("*.md"):
            if keyword and keyword not in f.read_text(encoding="utf-8"):
                continue
            results.append(f"📄 {f.name}")

        DispatchLog.write("读取记忆", "记忆系统", True, keyword, f"{len(results)}条")
        return True, "\n".join(results) if results else "没找到相关记忆"

    def memory_write(self, name: str, content: str) -> Tuple[bool, str]:
        """写入记忆"""
        ok, msg = self._guard("记忆系统", "写入记忆")
        if not ok:
            return False, msg
        memory_dir = Path.home() / ".claude" / "projects" / "-Users-zuimeidedeyihan" / "memory"
        memory_dir.mkdir(parents=True, exist_ok=True)
        path = memory_dir / f"{name}.md"
        path.write_text(content, encoding="utf-8")
        DispatchLog.write("写入记忆", "记忆系统", True, name)
        return True, f"✅ 记忆已存: {path}"

    # ═══════════════════════════════════════════
    # 系统自动化
    # ═══════════════════════════════════════════

    def applescript(self, script: str) -> Tuple[bool, str]:
        """执行AppleScript"""
        ok, msg = self._guard("系统自动化", "AppleScript执行")
        if not ok:
            return False, msg
        try:
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True, text=True, timeout=30
            )
            DispatchLog.write("AppleScript", "系统自动化", True, script[:50], result.stdout)
            return True, result.stdout
        except Exception as e:
            return False, str(e)

    def notify(self, title: str, message: str) -> Tuple[bool, str]:
        """桌面通知"""
        ok, msg = self._guard("通信", "桌面通知")
        if not ok:
            return False, msg
        script = f'display notification "{message}" with title "{title}"'
        return self.applescript(script)

    # ═══════════════════════════════════════════
    # 语音回流
    # ═══════════════════════════════════════════

    def voice_memo(self) -> Tuple[bool, str]:
        """处理最新语音备忘录"""
        from voice_reflux import VoiceReflux
        vr = VoiceReflux()
        return vr.process_latest_memo()

    def voice_file(self, path: str) -> Tuple[bool, str]:
        """处理指定音频文件"""
        from voice_reflux import VoiceReflux
        vr = VoiceReflux()
        return vr.full_pipeline(path)

    def voice_rewrite(self, text: str) -> Tuple[bool, str]:
        """通心译重组文本"""
        from voice_reflux import VoiceReflux
        vr = VoiceReflux()
        result = vr.reflux_rewrite(text)
        return True, result

    # ═══════════════════════════════════════════
    # v2.0: 温柔拒绝 + 净土36条 + DNA识别
    # ═══════════════════════════════════════════

    def _capability_report(self) -> Tuple[bool, str]:
        """宝宝能力边界报告"""
        if self.refusal:
            return True, self.refusal.get_capability_report()
        return True, "温柔拒绝引擎未加载·显示基础钥匙状态:\n" + json.dumps(
            self.key.summary(), ensure_ascii=False, indent=2)

    def _pureland_report(self) -> Tuple[bool, str]:
        """净土36条报告"""
        if HAS_GENTLE_REFUSAL:
            return True, PureLandRules.report()
        return False, "净土36条模块未加载"

    def _identity_check(self, context: str = "") -> Tuple[bool, str]:
        """DNA身份识别"""
        if self.refusal:
            ok, msg = self.refusal.verify_identity(context)
            return True, f"{'✅ 已识别' if ok else '❌ 未识别'}: {msg}"
        return False, "温柔拒绝引擎未加载"

    # ═══════════════════════════════════════════
    # 分页引擎（灵感: Mybatis-PageHelper）
    # ═══════════════════════════════════════════

    def _page_logs(self, params: dict) -> Tuple[bool, str]:
        """分页查日志"""
        try:
            from page_helper import PageHelper as PH
        except ImportError:
            from core.page_helper import PageHelper as PH
        log_name = params.get("name", "baobao_dispatch")
        pn = int(params.get("page", 1))
        page = PH.logs(log_name, page_num=pn, page_size=15)
        lines = [page.display(), ""]
        for item in page.items:
            t = item.get("时间", "")[:16]
            a = item.get("动作", item.get("事件", ""))
            ok = "✅" if item.get("授权", True) else "❌"
            lines.append(f"  {t} {ok} {a}")
        if not page.items:
            lines.append("  （暂无日志）")
        return True, "\n".join(lines)

    def _page_files(self, params: dict) -> Tuple[bool, str]:
        """分页查文件"""
        try:
            from page_helper import PageHelper as PH
        except ImportError:
            from core.page_helper import PageHelper as PH
        directory = params.get("dir", str(SYSTEM_ROOT / "core"))
        pattern = params.get("pattern", "*.py")
        pn = int(params.get("page", 1))
        page = PH.files(directory, pattern, page_num=pn, page_size=15)
        lines = [f"📁 {directory}", page.display(), ""]
        for item in page.items:
            lines.append(f"  {item['修改时间']}  {item['大小显示']:>8s}  {item['名称']}")
        return True, "\n".join(lines)

    def _page_memories(self, params: dict) -> Tuple[bool, str]:
        """分页查记忆"""
        try:
            from page_helper import PageHelper as PH
        except ImportError:
            from core.page_helper import PageHelper as PH
        kw = params.get("keyword", "")
        pn = int(params.get("page", 1))
        page = PH.memories(keyword=kw, page_num=pn, page_size=10)
        lines = [f"🧠 记忆文件{f' (关键词: {kw})' if kw else ''}", page.display(), ""]
        for item in page.items:
            lines.append(f"  {item['修改']}  {item['大小']:>12s}  {item['文件']}")
        return True, "\n".join(lines)

    # ═══════════════════════════════════════════
    # 总调度入口
    # ═══════════════════════════════════════════

    def dispatch(self, intent: str, params: dict = None) -> Tuple[bool, str]:
        """
        统一调度入口 —— 宝宝的大脑

        intent: 意图字符串（自然语言或命令）
        params: 参数字典
        """
        params = params or {}

        # 意图路由表
        routes = {
            "读文件":     lambda: self.read_file(params.get("path", "")),
            "写文件":     lambda: self.write_file(params.get("path", ""), params.get("content", "")),
            "整理文件":   lambda: self.organize_files(params.get("dir", "")),
            "服务状态":   lambda: self.check_service(params.get("name")),
            "启动服务":   lambda: self.start_service(params.get("name", "")),
            "停止服务":   lambda: self.stop_service(params.get("name", "")),
            "git状态":    lambda: self.git_status(),
            "git提交":    lambda: self.git_commit(params.get("message", "宝宝自动提交")),
            "git推送":    lambda: self.git_push(),
            "运行脚本":   lambda: self.run_python(params.get("script", ""), params.get("args", "")),
            "运行命令":   lambda: self.run_shell(params.get("command", "")),
            "Notion读取": lambda: self.notion_read(params.get("page_id", "")),
            "Notion创建": lambda: self.notion_create(params.get("parent", ""), params.get("title", "")),
            "AI对话":     lambda: self.ollama_chat(params.get("prompt", ""), params.get("model", "qwen2.5:14b")),
            "审计":       lambda: self.tricolor_audit(params.get("content", "")),
            "读记忆":     lambda: self.memory_read(params.get("keyword", "")),
            "写记忆":     lambda: self.memory_write(params.get("name", ""), params.get("content", "")),
            "通知":       lambda: self.notify(params.get("title", "宝宝"), params.get("message", "")),
            "钥匙状态":   lambda: (True, json.dumps(self.key.summary(), ensure_ascii=False, indent=2)),
            "语音备忘录": lambda: self.voice_memo(),
            "语音识别":   lambda: self.voice_file(params.get("path", "")),
            "语音重组":   lambda: self.voice_rewrite(params.get("text", "")),
            # v2.0: 温柔拒绝 + 净土36条
            "能力边界":   lambda: self._capability_report(),
            "净土规则":   lambda: self._pureland_report(),
            "身份识别":   lambda: self._identity_check(params.get("context", "")),
            # v2.1: 分页引擎（灵感: Mybatis-PageHelper）
            "查日志":     lambda: self._page_logs(params),
            "查文件":     lambda: self._page_files(params),
            "查记忆":     lambda: self._page_memories(params),
        }

        handler = routes.get(intent)
        if handler:
            return handler()
        else:
            return False, f"❓ 宝宝不认识这个指令: {intent}\n可用指令: {list(routes.keys())}"


# ═══════════════════════════════════════════
# CLI 入口 —— 终端直接测试
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import sys

    bb = BaoBaoDispatcher()

    if len(sys.argv) < 2:
        print("龍魂宝宝调度中枢 v1.0")
        print(f"钥匙文件: {KEY_FILE}")
        print(f"钥匙哈希: {bb.key.key_hash}")
        print()
        ok, summary = bb.dispatch("钥匙状态")
        print(summary)
        print()
        print("用法: python3 baobao_dispatcher.py <意图> [参数JSON]")
        print("示例: python3 baobao_dispatcher.py 服务状态")
        print("示例: python3 baobao_dispatcher.py AI对话 '{\"prompt\": \"你好\"}'")
        sys.exit(0)

    intent = sys.argv[1]
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    ok, result = bb.dispatch(intent, params)
    print(f"{'✅' if ok else '❌'} {result}")
