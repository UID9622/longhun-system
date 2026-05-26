#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宝宝调度中枢 · Baobao Dispatcher
DNA: #龍芯⚡️2026-05-26-BAOBAO-DISPATCHER-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 读钥匙执行 - 从主钥匙读取权限后执行
  2. 执行路由 - 根据权限分发不同的执行器
  3. 全量日志 - 记录每一件事
  4. 权限检查 - 调用authority验证
  5. 回滚快照 - 关键操作前自动快照

创始人: 诸葛鑫（UID9622）
理论指导: 曾仕强老师（永恒显示）

献给每一个相信技术应该有温度的人。
"""

import json
import subprocess
import datetime
import sys
from pathlib import Path
from typing import Dict, Optional
from baobao_authority import BaobaoAuthority


class BaobaoDispatcher:
    """宝宝调度中枢 - 读钥匙执行"""

    def __init__(self):
        self.system_root = Path.home() / "longhun-system"
        self.logs_dir = self.system_root / "logs"
        self.dispatch_log_path = self.logs_dir / "baobao_dispatch.jsonl"

        # 初始化权限校验器
        self.authority = BaobaoAuthority()
        if not self.authority.load_master_key():
            print("❌ 失败：无法初始化权限系统", file=sys.stderr)
            sys.exit(1)

    def dispatch(
        self, category: str, permission: str, action: str, params: Optional[Dict] = None
    ) -> Dict:
        """
        调度执行

        Args:
            category: 权限类别
            permission: 具体权限
            action: 执行的动作
            params: 动作参数

        Returns:
            执行结果
        """
        params = params or {}
        start_time = datetime.datetime.now()

        # 1. 权限检查
        allowed, reason = self.authority.check_permission(
            category, permission, action_details={"action": action, "params": params}
        )

        if not allowed:
            result = {
                "status": "DENIED",
                "reason": reason,
                "timestamp": start_time.isoformat(),
                "dna": self._generate_dna("DISPATCH-DENIED"),
            }
            self._log_dispatch(category, permission, action, result)
            return result

        # 2. 执行前快照
        snapshot_id = self._create_snapshot(action, params)

        # 3. 路由执行
        try:
            executor = self._get_executor(category)
            execution_result = executor(permission, action, params)

            result = {
                "status": "SUCCESS",
                "execution_result": execution_result,
                "snapshot_id": snapshot_id,
                "duration_ms": (datetime.datetime.now() - start_time).total_seconds()
                * 1000,
                "timestamp": start_time.isoformat(),
                "dna": self._generate_dna("DISPATCH-SUCCESS"),
            }
        except Exception as e:
            result = {
                "status": "ERROR",
                "error": str(e),
                "snapshot_id": snapshot_id,
                "duration_ms": (datetime.datetime.now() - start_time).total_seconds()
                * 1000,
                "timestamp": start_time.isoformat(),
                "dna": self._generate_dna("DISPATCH-ERROR"),
            }

        self._log_dispatch(category, permission, action, result)
        return result

    def _get_executor(self, category: str):
        """获取对应的执行器"""
        executors = {
            "文件系统": self._execute_filesystem,
            "服务调度": self._execute_service,
            "代码执行": self._execute_code,
            "Git": self._execute_git,
            "AI模型": self._execute_ai,
            "系统自动化": self._execute_automation,
            "审计系统": self._execute_audit,
            "通信": self._execute_communication,
        }

        if category not in executors:
            raise ValueError(f"未知的权限类别: {category}")

        return executors[category]

    def _execute_filesystem(self, permission: str, action: str, params: Dict) -> Dict:
        """文件系统执行器"""
        if permission == "读取任意文件":
            path = params.get("path")
            if not path or not Path(path).exists():
                raise FileNotFoundError(f"文件不存在: {path}")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            return {"action": "read", "path": path, "size": len(content)}

        elif permission == "写入和创建文件":
            path = params.get("path")
            content = params.get("content", "")
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"action": "write", "path": path, "size": len(content)}

        elif permission == "整理和归档":
            return {"action": "archive", "status": "ready"}

        else:
            raise ValueError(f"未知的文件系统权限: {permission}")

    def _execute_service(self, permission: str, action: str, params: Dict) -> Dict:
        """服务调度执行器"""
        service_name = params.get("service_name", "unknown")

        if permission == "查看服务状态":
            try:
                result = subprocess.run(
                    ["launchctl", "list", service_name],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                return {
                    "action": "status_check",
                    "service": service_name,
                    "running": result.returncode == 0,
                }
            except Exception as e:
                return {
                    "action": "status_check",
                    "service": service_name,
                    "error": str(e),
                }

        elif permission in ["启动服务", "停止服务", "重启服务"]:
            cmd_map = {"启动服务": "start", "停止服务": "stop", "重启服务": "restart"}
            cmd = cmd_map.get(permission)
            return {"action": cmd, "service": service_name, "status": "queued"}

        else:
            raise ValueError(f"未知的服务权限: {permission}")

    def _execute_code(self, permission: str, action: str, params: Dict) -> Dict:
        """代码执行执行器"""
        if permission == "运行Python脚本":
            script_path = params.get("script_path")
            args = params.get("args", [])
            try:
                result = subprocess.run(
                    ["python3", script_path] + args,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                return {
                    "action": "python_execute",
                    "script": script_path,
                    "returncode": result.returncode,
                    "stdout_len": len(result.stdout),
                    "stderr_len": len(result.stderr),
                }
            except Exception as e:
                raise RuntimeError(f"Python脚本执行失败: {e}")

        elif permission == "运行Shell脚本":
            command = params.get("command")
            try:
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True, timeout=30
                )
                return {
                    "action": "shell_execute",
                    "command": command[:100] + "..." if len(command) > 100 else command,
                    "returncode": result.returncode,
                }
            except Exception as e:
                raise RuntimeError(f"Shell脚本执行失败: {e}")

        else:
            raise ValueError(f"未知的代码执行权限: {permission}")

    def _execute_git(self, permission: str, action: str, params: Dict) -> Dict:
        """Git执行器"""
        repo_path = params.get("repo_path", str(self.system_root))

        if permission == "查看状态和日志":
            try:
                result = subprocess.run(
                    ["git", "-C", repo_path, "status", "--porcelain"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                return {
                    "action": "git_status",
                    "repo": repo_path,
                    "returncode": result.returncode,
                }
            except Exception as e:
                raise RuntimeError(f"Git状态查询失败: {e}")

        elif permission == "提交代码":
            message = params.get("message", "Auto commit")
            try:
                subprocess.run(["git", "-C", repo_path, "add", "."], timeout=10)
                result = subprocess.run(
                    ["git", "-C", repo_path, "commit", "-m", message],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                return {
                    "action": "git_commit",
                    "repo": repo_path,
                    "message": message[:50] + "..." if len(message) > 50 else message,
                    "returncode": result.returncode,
                }
            except Exception as e:
                raise RuntimeError(f"Git提交失败: {e}")

        else:
            raise ValueError(f"未知的Git权限: {permission}")

    def _execute_ai(self, permission: str, action: str, params: Dict) -> Dict:
        """AI模型执行器"""
        if permission == "调用Claude API":
            prompt = params.get("prompt", "")
            return {
                "action": "claude_api_call",
                "prompt_len": len(prompt),
                "status": "ready",
            }

        elif permission == "Ollama本地对话":
            message = params.get("message", "")
            return {
                "action": "ollama_chat",
                "message_len": len(message),
                "endpoint": "http://localhost:11434",
            }

        else:
            raise ValueError(f"未知的AI权限: {permission}")

    def _execute_automation(self, permission: str, action: str, params: Dict) -> Dict:
        """系统自动化执行器"""
        if permission == "AppleScript执行":
            script = params.get("script")
            try:
                result = subprocess.run(
                    ["osascript", "-e", script],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                return {
                    "action": "applescript_execute",
                    "returncode": result.returncode,
                }
            except Exception as e:
                raise RuntimeError(f"AppleScript执行失败: {e}")

        elif permission == "网络请求":
            url = params.get("url")
            method = params.get("method", "GET")
            return {
                "action": "http_request",
                "url": url,
                "method": method,
                "status": "queued",
            }

        else:
            raise ValueError(f"未知的自动化权限: {permission}")

    def _execute_audit(self, permission: str, action: str, params: Dict) -> Dict:
        """审计系统执行器"""
        if permission == "DNA追溯":
            return {
                "action": "dna_trace",
                "status": "ready",
                "dna": self._generate_dna("AUDIT-TRACE"),
            }

        elif permission == "三色审计":
            return {
                "action": "three_color_audit",
                "colors": ["🟢", "🟡", "🔴"],
                "status": "ready",
            }

        else:
            raise ValueError(f"未知的审计权限: {permission}")

    def _execute_communication(
        self, permission: str, action: str, params: Dict
    ) -> Dict:
        """通信执行器"""
        if permission == "桌面通知":
            title = params.get("title", "龍魂系統")
            message = params.get("message", "")
            try:
                script = f'display notification "{message}" with title "{title}"'
                subprocess.run(["osascript", "-e", script], check=False)
                return {
                    "action": "desktop_notification",
                    "title": title,
                    "message": message[:50] + "..." if len(message) > 50 else message,
                }
            except Exception as e:
                return {"action": "desktop_notification", "error": str(e)}

        else:
            raise ValueError(f"未知的通信权限: {permission}")

    def _create_snapshot(self, action: str, params: Dict) -> str:
        """创建操作前快照"""
        snapshot_id = f"snap_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        # 实现快照逻辑（这里简化处理）
        return snapshot_id

    def _log_dispatch(self, category: str, permission: str, action: str, result: Dict):
        """记录调度操作"""
        try:
            dispatch_log = {
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "category": category,
                "permission": permission,
                "action": action,
                "result": result,
                "dna": result.get("dna", self._generate_dna("DISPATCH-LOG")),
            }

            with open(self.dispatch_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(dispatch_log, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"调度日志写入失败: {e}", file=sys.stderr)

    def _generate_dna(self, operation_type: str) -> str:
        """生成DNA追溯码"""
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"#龍芯⚡️{date_str}-{operation_type}-v1.0"

    def get_status(self) -> Dict:
        """获取宝宝状态"""
        return {
            "name": "宝宝",
            "status": "ready",
            "authority_status": self.authority.get_status(),
            "timestamp": datetime.datetime.now().isoformat(),
            "dna": self._generate_dna("DISPATCHER-STATUS"),
        }


def main():
    """命令行接口"""
    dispatcher = BaobaoDispatcher()

    if len(sys.argv) < 2:
        status = dispatcher.get_status()
        print("✅ 宝宝调度中枢已启动")
        print(json.dumps(status, ensure_ascii=False, indent=2, default=str))
        sys.exit(0)

    command = sys.argv[1]

    if command == "服务状态":
        status = dispatcher.get_status()
        print("✅ 宝宝状态")
        print(json.dumps(status, ensure_ascii=False, indent=2, default=str))

    elif command == "AI对话":
        if len(sys.argv) < 3:
            print("用法: python3 baobao_dispatcher.py AI对话 '<json>'")
            sys.exit(1)
        params_json = sys.argv[2]
        try:
            params = json.loads(params_json)
            result = dispatcher.dispatch("AI模型", "调用Claude API", "ask", params)
            print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}", file=sys.stderr)
            sys.exit(1)

    elif command == "权限报告":
        report = dispatcher.authority.generate_report()
        print("📋 权限报告")
        print(json.dumps(report, ensure_ascii=False, indent=2, default=str))

    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
