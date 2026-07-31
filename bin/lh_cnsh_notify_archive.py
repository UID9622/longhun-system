# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·乙卯·戌时·䷰革-lh_cnsh_notify_archive-INTEGRATION-SYSTEM
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

"""🐉 龍魂引擎：lh_cnsh_notify_archive
路径：bin/lh_cnsh_notify_archive.py
TODO：请补充详细功能说明（不少于20字）。"""
import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)
"""
CNSH 通知归档模块 v1.0
支持：SMTP 邮件告警、Notion 页面归档
原则：配置存在才发送，不存在则静默跳过；绝不泄露源码。
#龍芯⚡️丙午·乙未·乙卯·戌时·䷰革-lh_cnsh_notify_archive-INTEGRATION-SYSTEM
"""

import json
import smtplib
import urllib.request
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any, Dict, Optional


class CNSH_通知归档:
    def __init__(
        self,
        smtp主机: Optional[str] = None,
        smtp端口: int = 587,
        smtp用户: Optional[str] = None,
        smtp密码: Optional[str] = None,
        收件人列表: Optional[list] = None,
        notion_token: Optional[str] = None,
        notion数据库ID: Optional[str] = None,
    ):
        self.smtp主机 = smtp主机
        self.smtp端口 = smtp端口
        self.smtp用户 = smtp用户
        self.smtp密码 = smtp密码
        self.收件人列表 = 收件人列表 or []
        self.notion_token = notion_token
        self.notion数据库ID = notion数据库ID

    # ---------- SMTP 邮件 ----------
    def smtp可用(self) -> bool:
        return all([self.smtp主机, self.smtp用户, self.smtp密码, self.收件人列表])

    def 发送邮件(self, 主题: str, 摘要: str, 报告路径: Optional[str] = None) -> Dict[str, Any]:
        if not self.smtp可用():
            return {"ok": False, "reason": "SMTP 未配置"}

        结果 = {"ok": True, "sent": 0, "errors": []}
        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp用户
            msg["To"] = ", ".join(self.收件人列表)
            msg["Subject"] = f"[CNSH] {主题}"

            body = f"""
CNSH 三色审计归档通知
========================
{摘要}

时间: {datetime.now(timezone.utc).isoformat()}
DNA: #龍芯⚡️丙午·乙未·乙卯·戌时·䷰革-lh_cnsh_notify_archive-INTEGRATION-SYSTEM

本邮件仅含审计摘要，不含源代码。
"""
            msg.attach(MIMEText(body, "plain", "utf-8"))

            if 报告路径 and Path(报告路径).exists():
                with open(报告路径, "r", encoding="utf-8") as f:
                    附件 = MIMEText(f.read(), "plain", "utf-8")
                    附件.add_header("Content-Disposition", "attachment", filename=Path(报告路径).name)
                    msg.attach(附件)

            with smtplib.SMTP(self.smtp主机, self.smtp端口) as server:
                server.starttls()
                server.login(self.smtp用户, self.smtp密码)
                server.send_message(msg)
                结果["sent"] = len(self.收件人列表)
        except Exception as e:
            结果["ok"] = False
            结果["errors"].append(str(e))

        return 结果

    # ---------- Notion 归档 ----------
    def notion可用(self) -> bool:
        return bool(self.notion_token and self.notion数据库ID)

    def 归档到Notion(self, 标题: str, 摘要: Dict[str, Any], 报告路径: Optional[str] = None) -> Dict[str, Any]:
        if not self.notion可用():
            return {"ok": False, "reason": "Notion 未配置"}

        风险文件数 = 摘要.get("风险文件数", 0)
        文件总数 = 摘要.get("文件总数", 0)
        三色 = 摘要.get("三色摘要", {})

        属性 = {
            "标题": {"title": [{"text": {"content": 标题}}]},
            "风险文件数": {"number": 风险文件数},
            "文件总数": {"number": 文件总数},
            "红灯": {"number": 三色.get("🔴", 0)},
            "黄灯": {"number": 三色.get("🟡", 0)},
            "绿灯": {"number": 三色.get("🟢", 0)},
            "时间": {"date": {"start": datetime.now(timezone.utc).isoformat()}},
            "状态": {"select": {"name": "已归档"}},
        }

        请求体 = {
            "parent": {"database_id": self.notion数据库ID},
            "properties": 属性,
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"CNSH 审计摘要：{json.dumps(摘要, ensure_ascii=False)}"}}]
                    },
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "DNA: #龍芯⚡️丙午·乙未·乙卯·戌时·䷰革-lh_cnsh_notify_archive-INTEGRATION-SYSTEM"}}]
                    },
                },
            ],
        }

        try:
            req = urllib.request.Request(
                "https://api.notion.com/v1/pages",
                data=json.dumps(请求体).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.notion_token}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                return {"ok": True, "status": resp.status, "data": json.loads(resp.read().decode("utf-8"))}
        except Exception as e:
            return {"ok": False, "reason": str(e)}

    # ---------- 统一归档入口 ----------
    def 归档(self, 标题: str, 摘要: Dict[str, Any], 报告路径: Optional[str] = None) -> Dict[str, Any]:
        文本摘要 = json.dumps(摘要, ensure_ascii=False, indent=2)
        return {
            "smtp": self.发送邮件(标题, 文本摘要, 报告路径),
            "notion": self.归档到Notion(标题, 摘要, 报告路径),
        }


# ============== 配置模板 ==============
配置模板 = """
# CNSH 通知归档配置模板
# 复制以下内容到 CNSH_通知配置.json，填入真实值
{
    "smtp_host": "smtp.example.com",
    "smtp_port": 587,
    "smtp_user": "audit@example.com",
    "smtp_password": "YOUR_SMTP_PASSWORD",
    "recipients": ["admin@example.com"],
    "notion_token": "secret_xxx",
    "notion_database_id": "db_xxx"
}
"""


def 从文件加载配置(路径: str = "CNSH_通知配置.json") -> CNSH_通知归档:
    p = Path(路径)
    if not p.exists():
        return CNSH_通知归档()
    with open(p, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    return CNSH_通知归档(
        smtp主机=cfg.get("smtp_host"),
        smtp端口=cfg.get("smtp_port", 587),
        smtp用户=cfg.get("smtp_user"),
        smtp密码=cfg.get("smtp_password"),
        收件人列表=cfg.get("recipients"),
        notion_token=cfg.get("notion_token"),
        notion数据库ID=cfg.get("notion_database_id"),
    )


if __name__ == "__main__":
    通知 = 从文件加载配置()
    摘要 = {
        "文件总数": 10,
        "风险文件数": 3,
        "三色摘要": {"🟢": 20, "🟡": 5, "🔴": 8},
    }
    结果 = 通知.归档("测试审计归档", 摘要)
    print(json.dumps(结果, ensure_ascii=False, indent=2))
    if not 通知.smtp可用() and not 通知.notion可用():
        print("\n提示：未检测到通知配置。请创建 CNSH_通知配置.json：")
        print(配置模板)
