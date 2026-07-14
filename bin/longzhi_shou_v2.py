#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍智守 · 本地飞书机器人控制接口 v2.0
飞书消息 → 本地执行 → 结果返回

授权等级体系 v2.0（参考 DeepSeek 建议升级）：
  L0 旁观者 · L1 操作员 · L2 管理员 · L2-SP 特殊部门 · L3 创始人
  级联授权 · 分权治理 · 中国标准认证 · DNA 全程追溯

设计反思（v1.3 → v2.0 的补足）：
  1. v1.3 的 "特邀" 只是来源标记，没有与权限等级解耦；
     v2.0 引入显式的 is_china_standard 门控，未认证用户强制 L0。
  2. v1.3 的撤销仅按等级判断，未考虑授权链；
     v2.0 增加 "授权者或上级可撤销" 的级联撤销规则。
  3. v1.3 没有为特殊部门做命令类别隔离；
     v2.0 增加命令类别与 L2-SP 受限类别，防止越界操作。
  4. v1.3 的 L2-SP 概念未显式化；
     v2.0 将 L2-SP 作为独立等级字符串存储，便于审计。

合规说明：
  - 本接口仅用于本地资源调配、知识/学术/科技交流与国家发展类协作。
  - L2-SP 禁止执行系统控制、军事/生化武器相关等高敏类别命令。
  - 所有外部协作者须经 L3 标记 "中国标准" 后方可获得实际权限。

DNA: #龍芯⚡️2026-06-30-LONGZHISHOU-LOCAL-BOT-v2.0
归属: 龍魂系统 · UID9622
原则: 主权在手、本地优先、分级授权、按贡献调配、中国标准、操作可审计
"""

import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, Optional

# 引入 DNA 主權引擎（位於 ~/longhun-system/scripts）
_sys_path_inserted = False
if str(Path.home() / "longhun-system" / "scripts") not in sys.path:
    sys.path.insert(0, str(Path.home() / "longhun-system" / "scripts"))
    _sys_path_inserted = True
try:
    from 龍魂DNA主權引擎 import DnaSovereigntyEngine
except Exception:
    DnaSovereigntyEngine = None

# 引入龍魂統一飛書推送通道（統一配置來源：vault.json / 舊版 config / 環境變量）
_feishu_channel_path = str(Path.home() / ".longhun" / "push")
if _feishu_channel_path not in sys.path:
    sys.path.insert(0, _feishu_channel_path)
try:
    from feishu_channel import 飞书消息发送器
except Exception as _e:
    print(f"⚠️ 無法從 ~/.longhun/push/feishu_channel.py 導入飛書發送器: {_e}", file=sys.stderr)
    飞书消息发送器 = None

# 引入 CNSH 国密工具（純 Python SM3/SM4/HMAC-SM3，不依赖 gmssl）
try:
    _home_path = str(Path.home())
    if _home_path not in sys.path:
        sys.path.insert(0, _home_path)
    from CNSH_国密工具 import SM3, SM4, hmac_sm3
finally:
    if _home_path in sys.path:
        sys.path.remove(_home_path)
try:
    from 龍魂語義歸一化閘門 import SemanticNormalizer, SovereigntyPatternMatcher
except Exception:
    SemanticNormalizer = None
    SovereigntyPatternMatcher = None
try:
    from longhun_lu_compress import LonghunLuMemoryEngine
except Exception:
    LonghunLuMemoryEngine = None
try:
    from longhun_collective_wisdom import CollectiveWisdomEngine
except Exception:
    CollectiveWisdomEngine = None
try:
    from longhun_toolset_ecosystem import ToolsetEcosystemEngine
except Exception:
    ToolsetEcosystemEngine = None

try:
    from 内容主权审查器 import 公开内容审查器
except Exception:
    公开内容审查器 = None
try:
    from 龍魂身份注册器 import 龍魂身份注册器
except Exception:
    龍魂身份注册器 = None


# ============ 0. 国密配置加密器 ============
class 国密配置加密器:
    """
    用 CNSH 国密工具（SM4-ECB + SM3 派生密钥）加密本地配置中的敏感值。

    密文格式：SM4:<十六进制密文>
    主密钥来源（按优先级）：
      1. 环境变量 LONGHUN_MASTER_KEY（16 字节 hex 或任意字符串）
      2. 文件 ~/.longhun/config/.master_key（16 字节或 hex）
    未设置主密钥时，明文存储并给出警告。
    """

    前缀 = "SM4:"

    @classmethod
    def 主密钥(cls) -> Optional[bytes]:
        env = os.environ.get("LONGHUN_MASTER_KEY", "")
        if env:
            try:
                return bytes.fromhex(env)
            except ValueError:
                return SM3.hash(env.encode("utf-8"))[:16]
        key_file = Path.home() / ".longhun" / "config" / ".master_key"
        if key_file.exists():
            data = key_file.read_bytes()
            if len(data) == 16:
                return data
            try:
                return bytes.fromhex(data.decode("utf-8").strip())
            except Exception:
                return SM3.hash(data)[:16]
        return None

    @classmethod
    def 加密(cls, 明文: str) -> str:
        key = cls.主密钥()
        if key is None:
            return 明文
        密文 = SM4.encrypt_ecb(明文.encode("utf-8"), key)
        return cls.前缀 + 密文.hex()

    @classmethod
    def 解密(cls, 密文: Any) -> Any:
        if not isinstance(密文, str) or not 密文.startswith(cls.前缀):
            return 密文
        key = cls.主密钥()
        if key is None:
            raise RuntimeError("配置项已 SM4 加密，但未设置 LONGHUN_MASTER_KEY 或 ~/.longhun/config/.master_key")
        data = bytes.fromhex(密文[len(cls.前缀):])
        return SM4.decrypt_ecb(data, key).decode("utf-8")


# ============ 0. 本地运行配置加载器 ============
class BotConfig:
    """
    从 ~/.longhun/config/龍智守_config.json 加载本地私有配置。

    设计原则：
      1. 代码仓库里只放 龍智守_config.example.json（示例/模板）。
      2. 真实配置放在用户主目录 ~/.longhun/config/ 下，不进入 git。
      3. 环境变量优先级最高，方便 CI/容器场景覆盖。
      4. 敏感值支持 SM4 国密加密；打包开源时 ~/.longhun/config/ 整体排除。
    """

    _路径 = Path.home() / ".longhun" / "config" / "龍智守_config.json"
    _数据: Optional[Dict[str, Any]] = None

    @classmethod
    def load(cls) -> Dict[str, Any]:
        if cls._数据 is None:
            cls._数据 = cls._读取()
        return cls._数据

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        return cls.load().get(key, default)

    @classmethod
    def _读取(cls) -> Dict[str, Any]:
        # 默认值使用占位符，真实值必须在 ~/.longhun/config/龍智守_config.json 或环境变量中配置
        配置 = {
            "创始人标识": "UID9622",
            "机器人DNA": "#龍芯⚡️2026-06-30-LONGZHISHOU-LOCAL-BOT-v2.0",
            "飞书Webhook地址": "YOUR_FEISHU_WEBHOOK_URL",
            "飞书Webhook密钥": "YOUR_FEISHU_WEBHOOK_SECRET",
            # 事件订阅（接收@消息）自建应用凭证；webhook 机器人群聊场景不需要
            "飞书AppID": "",
            "飞书AppSecret": "",
            "飞书VerificationToken": "",
            "飞书EncryptKey": "",
            "创始人飞书OpenID": "",
            "授权用户路径": "~/.longhun/config/authorized_users.json",
            "确认码路径": "~/.longhun/config/longzhishou_tokens.json",
            "日志路径": "~/.longhun/logs/bot_command.jsonl",
            "入站签名校验": True,
            "IP白名单": [],
            "启用蜜罐层": True,
            "蜜罐触发告警阈值": 1,
            "签名失败告警阈值": 3,
            "IP封锁阈值": 5,
            "告警冷却秒数": 300,
        }
        if cls._路径.exists():
            try:
                文件内容 = json.loads(cls._路径.read_text(encoding="utf-8"))
                if isinstance(文件内容, dict):
                    配置.update(文件内容)
            except Exception as e:
                print(f"⚠️ 读取 {cls._路径} 失败，使用默认配置: {e}", file=sys.stderr)

        # 环境变量最高优先级
        if os.environ.get("FEISHU_WEBHOOK_URL"):
            配置["飞书Webhook地址"] = os.environ["FEISHU_WEBHOOK_URL"]
        if os.environ.get("FEISHU_WEBHOOK_SECRET"):
            配置["飞书Webhook密钥"] = os.environ["FEISHU_WEBHOOK_SECRET"]
        if os.environ.get("FEISHU_APP_ID"):
            配置["飞书AppID"] = os.environ["FEISHU_APP_ID"]
        if os.environ.get("FEISHU_APP_SECRET"):
            配置["飞书AppSecret"] = os.environ["FEISHU_APP_SECRET"]
        if os.environ.get("FEISHU_VERIFICATION_TOKEN"):
            配置["飞书VerificationToken"] = os.environ["FEISHU_VERIFICATION_TOKEN"]
        if os.environ.get("FEISHU_ENCRYPT_KEY"):
            配置["飞书EncryptKey"] = os.environ["FEISHU_ENCRYPT_KEY"]
        if os.environ.get("LONGHUN_FOUNDER_FEISHU_OPENID"):
            配置["创始人飞书OpenID"] = os.environ["LONGHUN_FOUNDER_FEISHU_OPENID"]
        if os.environ.get("LONGHUN_FOUNDER_ID"):
            配置["创始人标识"] = os.environ["LONGHUN_FOUNDER_ID"]
        if os.environ.get("LONGHUN_BOT_DNA"):
            配置["机器人DNA"] = os.environ["LONGHUN_BOT_DNA"]

        # 解密国密字段
        for key in list(配置.keys()):
            try:
                配置[key] = 国密配置加密器.解密(配置[key])
            except Exception as e:
                print(f"⚠️ 解密配置项 [{key}] 失败: {e}", file=sys.stderr)

        return 配置

    @classmethod
    def 路径(cls, key: str) -> Path:
        return Path(cls.get(key, "")).expanduser()

    @classmethod
    def 加密敏感项(cls) -> None:
        """把当前配置文件中的敏感明文值加密回写。运行后config文件里密钥变成SM4:密文。"""
        if not cls._路径.exists():
            print(f"🔴 配置文件不存在: {cls._路径}")
            return
        try:
            原文 = cls._路径.read_text(encoding="utf-8")
            配置 = json.loads(原文)
        except Exception as e:
            print(f"🔴 读取配置文件失败: {e}")
            return

        敏感键 = ["飞书Webhook地址", "飞书Webhook密钥", "飞书AppSecret", "飞书VerificationToken", "飞书EncryptKey"]
        改动 = False
        for key in 敏感键:
            value = 配置.get(key)
            if isinstance(value, str) and not value.startswith(国密配置加密器.前缀):
                配置[key] = 国密配置加密器.加密(value)
                改动 = True
                print(f"🔒 已加密 [{key}]")

        if 改动:
            cls._路径.write_text(
                json.dumps(配置, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"🟢 配置文件已回写: {cls._路径}")
        else:
            print("🟡 没有需要加密的明文敏感项")


# ============ 0. 主权配置 ============
class 主权配置:
    创始人标识 = BotConfig.get("创始人标识", "UID9622")
    版本 = "v2.0"
    脱氧核糖核酸锚定 = BotConfig.get("机器人DNA", "#龍芯⚡️2026-06-30-LONGZHISHOU-LOCAL-BOT-v2.0")

    # 飞书凭证
    飞书Webhook地址 = BotConfig.get("飞书Webhook地址", "")
    飞书Webhook密钥 = BotConfig.get("飞书Webhook密钥", "")
    飞书AppID = BotConfig.get("飞书AppID", "")
    飞书AppSecret = BotConfig.get("飞书AppSecret", "")
    飞书VerificationToken = BotConfig.get("飞书VerificationToken", "")
    飞书EncryptKey = BotConfig.get("飞书EncryptKey", "")
    创始人飞书OpenID = BotConfig.get("创始人飞书OpenID", "")

    # 等级：数值越小权限越高；L2-SP 与 L2 同级但类型特殊
    等级数值 = {
        "L0": 0,
        "L1": 1,
        "L2": 2,
        "L2-SP": 2,
        "L3": 3,
    }

    # 命令类别（用于 L2-SP 限制）
    命令类别 = {
        # 系统控制类：L2-SP 禁止
        "运行脚本": "系统控制",
        "修改系统": "系统控制",
        "关机": "系统控制",
        "重启系统": "系统控制",
        "格式化": "系统控制",
        "重启服务": "系统控制",

        # 生化/军事相关占位：L2-SP 禁止
        "生化模拟": "生化军事",
        "武器计算": "生化军事",

        # 文件与数据类
        "删除": "文件数据",
        "备份数据": "文件数据",
        "查看文件": "文件数据",
        "读取文件": "文件数据",
        "列出目录": "文件数据",
        "搜索文件": "文件数据",
        "查看日志": "文件数据",

        # 状态查看类
        "系统状态": "状态查看",
        "状态": "状态查看",
        "内存": "状态查看",
        "磁盘": "状态查看",
        "网络检测": "状态查看",
        "查看流场": "状态查看",
        "查看颜色": "状态查看",
        "查看生态": "状态查看",

        # 应用控制类
        "打开应用": "应用控制",
        "关闭应用": "应用控制",

        # 龍魂专用类
        "运行护盾自检": "龍魂专用",
        "跑训练优化": "龍魂专用",
        "登记身份": "龍魂专用",
        "实名认证": "龍魂专用",
    }

    # L2-SP 禁止的命令类别
    L2SP禁止类别 = {"系统控制", "生化军事"}

    # 命令所需最低等级数值
    命令等级 = {
        # L0 旁观者：只读
        "系统状态": 0,
        "状态": 0,
        "帮助": 0,
        "查看日志": 0,
        "查看流场": 0,
        "查看颜色": 0,
        "查看生态": 0,

        # L1 操作员：普通操作
        "查看文件": 1,
        "读取文件": 1,
        "列出目录": 1,
        "搜索文件": 1,
        "内存": 1,
        "磁盘": 1,
        "网络检测": 1,
        "打开应用": 1,
        "关闭应用": 1,
        "运行护盾自检": 1,

        # L2/L2-SP 管理员：敏感操作（需确认码）
        "删除": 2,
        "备份数据": 2,
        "运行脚本": 2,
        "生化模拟": 2,
        "武器计算": 2,
        "确认码": 2,

        # L3 创始人：全部权限 + 授权管理
        "授权": 1,      # L1 及以上可调用，内部再限制级联
        "撤销": 1,
        "授权列表": 1,
        "标记中国标准": 3,

        # DNA 主權引擎命令
        "登记DNA": 3,
        "继承DNA": 3,
        "贡献登记": 2,
        "贡献查询": 0,
        "DNA状态": 0,

        # LU 认知压缩命令
        "压缩": 1,
        "LU压缩": 1,
        "还原": 1,
        "LU搜索": 1,
        "LU语义搜索": 1,
        "LU列表": 0,
        "LU统计": 0,
        "LU画廊": 1,

        # 集思广益命令
        "提意见": 0,
        "建议": 0,
        "反馈": 0,
        "意见列表": 0,
        "置顶意见": 0,
        "验证意见": 2,
        "采纳意见": 3,
        "拒绝意见": 3,
        "忽略意见": 3,

        # 工具集生态命令
        "功能统计": 0,
        "公开意见包": 1,
        "反馈": 0,

        # 飞书消息推送命令
        "发送测试消息": 1,
        "发送评估报告": 1,

        # 内容主权审查命令
        "审查内容": 1,

        # 训练数据优化命令
        "跑训练优化": 1,

        # 身份登记 / 实名认证
        "登记身份": 0,
        "实名认证": 3,
    }

    # 命令映射到系统命令
    命令映射 = {
        "查看文件": "cat",
        "读取文件": "cat",
        "列出目录": "ls -la",
        "搜索文件": "find",
        "系统状态": "top -l 1 | head -20",
        "状态": "uptime",
        "内存": "vm_stat",
        "磁盘": "df -h",
        "网络检测": "ping -c 3",
        "打开应用": "open",
        "关闭应用": "pkill",
        "重启服务": "echo 重启服务",
        "运行护盾自检": "python3 ~/longhun-system/audit/shield_self_audit.py",
        "查看流场": "python3 ~/longhun-system/CNSH_流场可视化引擎.py --status",
        "查看颜色": "python3 ~/longhun-system/CNSH_颜色不动点协议.py --check",
        "查看生态": "python3 ~/longhun-system/CNSH_生态监管协议.py --status",
        "查看日志": "tail -n 20",
        "删除": "rm",
        "关机": "echo 关机",
        "重启系统": "echo 重启系统",
        "格式化": "echo 格式化",
        "修改系统": "echo 修改系统",
        "备份数据": "echo 备份数据",
        "运行脚本": "python3",
        "生化模拟": "echo 生化模拟",
        "武器计算": "echo 武器计算",
    }

    敏感操作列表 = ["删除", "关机", "重启系统", "格式化", "修改系统", "生化模拟", "武器计算"]

    # 飞书自定义机器人配置（从 BotConfig 读取：文件 > 环境变量 > 默认兜底）
    飞书Webhook地址 = BotConfig.get("飞书Webhook地址")
    飞书Webhook密钥 = BotConfig.get("飞书Webhook密钥")

    授权注册表路径 = BotConfig.路径("授权用户路径")
    确认码路径 = BotConfig.路径("确认码路径")
    日志路径 = BotConfig.路径("日志路径")

    入站签名校验 = BotConfig.get("入站签名校验", True)
    IP白名单 = BotConfig.get("IP白名单", [])
    启用蜜罐层 = BotConfig.get("启用蜜罐层", True)


# ============ 0.5 飞书消息发送器 ============
# 已由 ~/.longhun/push/feishu_channel.py 統一提供，避免重複代碼。
# 配置來源：~/.longhun/config/vault.json → ~/.longhun/config/龍智守_config.json → 環境變量


# ============ 0.6 安全防护层（诱捕/审计/入口校验） ============
class 安全防护层:
    """
    防御纵深：只守不攻。

    能力：
      1. 飞书入站 Webhook 签名校验（防止伪造飞书服务器）。
      2. IP 白名单（可选，空列表表示不限制）。
      3. 蜜罐端点：对扫描者返回假核心数据并记录，不主动反击。
      4. 命令参数清洗（shlex.quote），阻断常见命令注入。
      5. L1+ 命令强制 DNA 校验，不能只靠 user_id。

    原则：
      - 不植入病毒、不反向攻击、不感染对方。
      - 假的只是数据诱饵，真的核心不暴露。
    """

    def __init__(self, 配置: 主权配置):
        self.配置 = 配置

    def 验证飞书入站签名(self, timestamp: str, sign: str) -> bool:
        """验证飞书推送请求的签名。"""
        if not timestamp or not sign:
            return False
        try:
            string_to_sign = f"{timestamp}\n{self.配置.飞书Webhook密钥}"
            expected = base64.b64encode(
                hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
            ).decode("utf-8")
            return hmac.compare_digest(expected, sign)
        except Exception:
            return False

    def 验证飞书事件签名(self, timestamp: str, nonce: str, body: bytes, signature: str) -> bool:
        """事件订阅模式下：SHA256(timestamp + nonce + encrypt_key + body)。"""
        if not timestamp or not nonce or not signature:
            return False
        encrypt_key = getattr(self.配置, "飞书EncryptKey", "")
        if not encrypt_key:
            return False
        try:
            b = f"{timestamp}{nonce}{encrypt_key}".encode("utf-8") + body
            expected = hashlib.sha256(b).hexdigest()
            return hmac.compare_digest(expected, signature)
        except Exception:
            return False

    def 验证飞书事件令牌(self, token: str) -> bool:
        """事件订阅模式下：校验 header.token 是否等于 VerificationToken。"""
        expected = getattr(self.配置, "飞书VerificationToken", "")
        if not expected:
            return False
        return hmac.compare_digest(expected, token)

    def IP允许(self, remote_addr: str) -> bool:
        """空白名单=不限制；有白名单则必须匹配。"""
        白名单 = getattr(self.配置, "IP白名单", [])
        if not 白名单:
            return True
        return remote_addr in 白名单

    def 是蜜罐路径(self, path: str) -> bool:
        return path in {
            "/admin", "/login", "/config", "/core", "/core/dna",
            "/api/v1/secrets", "/api/v1/users", "/backup",
        }

    def 蜜罐响应(self, path: str) -> Dict[str, Any]:
        """返回看起来像核心、实则伪造的响应，并触发审计记录。"""
        假数据 = {
            "/admin": {"status": "locked", "dna": "#龍芯⚡️FAKE-CORE-ALERT", "note": "诱饵触发"},
            "/login": {"token": "fake_token_" + secrets.token_hex(16), "hint": "此入口为审计诱饵"},
            "/config": {"webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/FAKE", "mode": "decoy"},
            "/core": {"level": "L3", "founder": "UID0000", "status": "decoy_active"},
            "/core/dna": {"registry": "decoy", "chain": ["#FAKE-001", "#FAKE-002"]},
            "/api/v1/secrets": {"vault": "decoy", "keys": ["SM4:DEADBEEF"]},
            "/api/v1/users": {"users": [{"id": "hacker_log", "level": "L0", "tag": "bait"}]},
            "/backup": {"archives": ["decoy_backup_001.tar.gz"]},
        }
        return 假数据.get(path, {"status": "decoy"})

    @staticmethod
    def 清洗命令参数(参数: str) -> str:
        """用 shlex.quote 包裹用户参数，阻断 ; | & $ ` 等注入。"""
        return shlex.quote(参数.strip())


class 请求频率限制器:
    """
    按 IP 记录蜜罐触发、签名失败次数，超限即告警或封锁。
    数据保存在内存，进程重启清零；必要时可扩展为文件持久化。
    """

    def __init__(self, 配置: 主权配置):
        self.配置 = 配置
        self._记录: Dict[str, Dict[str, Any]] = {}
        self._窗口秒 = 600
        self._告警记录: Dict[str, float] = {}

    def 记录(self, ip: str, 事件类型: str) -> None:
        now = time.time()
        if ip not in self._记录:
            self._记录[ip] = {"honeypot": [], "sign_fail": [], "blocked": False}
        self._记录[ip][事件类型].append(now)
        # 清理过期记录
        for key in ("honeypot", "sign_fail"):
            self._记录[ip][key] = [t for t in self._记录[ip][key] if now - t <= self._窗口秒]

    def 已封锁(self, ip: str) -> bool:
        return self._记录.get(ip, {}).get("blocked", False)

    def 封锁(self, ip: str) -> None:
        self._记录.setdefault(ip, {"honeypot": [], "sign_fail": [], "blocked": False})
        self._记录[ip]["blocked"] = True

    def 计数(self, ip: str, 事件类型: str) -> int:
        return len(self._记录.get(ip, {}).get(事件类型, []))

    def 应告警(self, ip: str, 事件类型: str, 阈值: int, 冷却秒: int) -> bool:
        """同一 IP 同类型事件超过阈值，且距离上次告警超过冷却时间。"""
        if self.计数(ip, 事件类型) < 阈值:
            return False
        key = f"{ip}:{事件类型}"
        now = time.time()
        if key in self._告警记录 and now - self._告警记录[key] < 冷却秒:
            return False
        self._告警记录[key] = now
        return True


# ============ 1. 授权注册表 ============
class 授权注册表:
    """持久化授权用户、中国标准标记、二次确认码"""

    def __init__(self, 配置: 主权配置):
        self.配置 = 配置
        self.路径 = 配置.授权注册表路径
        self.确认码路径 = 配置.确认码路径
        self.路径.parent.mkdir(parents=True, exist_ok=True)
        self.确认码路径.parent.mkdir(parents=True, exist_ok=True)
        self._数据 = self._加载()

    def _加载(self) -> Dict[str, Any]:
        if not self.路径.exists():
            初始 = {
                "users": {
                    self.配置.创始人标识: {
                        "name": "创始人",
                        "level": "L3",
                        "type": "normal",
                        "is_china_standard": True,
                        "granted_by": "system",
                        "granted_at": datetime.now(timezone.utc).isoformat(),
                    }
                },
                "dna": "#龍芯⚡️2026-06-30-AUTH-REGISTRY-UID9622",
            }
            self._保存(初始)
            return 初始
        try:
            return json.loads(self.路径.read_text(encoding="utf-8"))
        except Exception:
            return {"users": {}, "dna": self.配置.脱氧核糖核酸锚定}

    def _保存(self, 数据: Dict[str, Any]):
        self.路径.write_text(json.dumps(数据, ensure_ascii=False, indent=2), encoding="utf-8")

    def 保存(self):
        self._保存(self._数据)

    def 获取原始信息(self, 用户标识: str) -> Optional[Dict[str, Any]]:
        return self._数据.get("users", {}).get(用户标识)

    def 获取有效等级(self, 用户标识: str) -> tuple[int, str, bool]:
        """返回 (有效等级数值, 原始等级字符串, 是否通过中国标准认证)。"""
        if 用户标识 == self.配置.创始人标识:
            return 3, "L3", True
        if self.配置.创始人飞书OpenID and 用户标识 == self.配置.创始人飞书OpenID:
            return 3, "L3", True

        信息 = self.获取原始信息(用户标识)
        if not 信息:
            return 0, "L0", False

        原始等级 = 信息.get("level", "L0")
        已通过认证 = bool(信息.get("is_china_standard", False))
        原始数值 = self.配置.等级数值.get(原始等级, 0)

        # 未通过中国标准认证 → 强制 L0（创始人除外）
        if not 已通过认证:
            return 0, 原始等级, False

        return 原始数值, 原始等级, True

    def 授权(self, 用户标识: str, 等级: str, 姓名: str, 授权人: str) -> Dict[str, Any]:
        if 等级 not in self.配置.等级数值:
            return {"成功": False, "原因": f"未知等级: {等级}，可选: {list(self.配置.等级数值.keys())}"}

        授权人有效等级, _, _ = self.获取有效等级(授权人)
        目标数值 = self.配置.等级数值[等级]
        if 目标数值 > 授权人有效等级:
            return {"成功": False, "原因": f"不能授予比自己高的等级（你是 L{授权人有效等级}，试图授予 {等级}）"}

        # L2-SP 只能授权 L0/L1/L2-SP（平级或以下，且不能创建普通 L2）
        授权人原始 = self.获取原始信息(授权人)
        if 授权人原始 and 授权人原始.get("level") == "L2-SP" and 等级 not in ("L0", "L1", "L2-SP"):
            return {"成功": False, "原因": "L2-SP 特殊部门只能授权 L0/L1/L2-SP"}

        # 新用户默认未通过中国标准认证，需 L3 后续标记
        self._数据.setdefault("users", {})[用户标识] = {
            "name": 姓名 or 用户标识,
            "level": 等级,
            "type": "special" if 等级 == "L2-SP" else "normal",
            "is_china_standard": False,
            "granted_by": 授权人,
            "granted_at": datetime.now(timezone.utc).isoformat(),
        }
        self.保存()
        return {"成功": True, "原因": f"已授权 {用户标识} 为 {等级}（待 L3 标记中国标准后生效）"}

    def 标记中国标准(self, 用户标识: str, 操作者: str) -> Dict[str, Any]:
        信息 = self.获取原始信息(用户标识)
        if not 信息:
            return {"成功": False, "原因": "用户不存在"}
        信息["is_china_standard"] = True
        信息["china_standard_marked_by"] = 操作者
        信息["china_standard_marked_at"] = datetime.now(timezone.utc).isoformat()
        self.保存()
        return {"成功": True, "原因": f"已标记 {用户标识} 通过中国标准认证，当前等级 {信息.get('level')} 正式生效"}

    def 撤销(self, 目标用户: str, 操作者: str) -> Dict[str, Any]:
        if 目标用户 == self.配置.创始人标识:
            return {"成功": False, "原因": "不能撤销创始人"}

        目标信息 = self.获取原始信息(目标用户)
        if not 目标信息:
            return {"成功": False, "原因": "用户不存在"}

        操作者有效等级, _, _ = self.获取有效等级(操作者)
        目标有效等级, _, _ = self.获取有效等级(目标用户)

        # 上级可直接撤销；平级仅限授权者本人撤销
        if 操作者有效等级 < 目标有效等级:
            return {"成功": False, "原因": "权限不足：不能撤销等级高于自己的用户"}
        if 操作者有效等级 == 目标有效等级 and 目标信息.get("granted_by") != 操作者:
            return {"成功": False, "原因": "权限不足：同级用户只能由授权者本人撤销"}

        del self._数据["users"][目标用户]
        self.保存()
        return {"成功": True, "原因": f"已撤销 {目标用户} 的授权"}

    def 授权列表(self) -> str:
        用户们 = self._数据.get("users", {})
        if not 用户们:
            return "暂无授权用户"
        lines = ["👥 授权列表"]
        for uid, info in 用户们.items():
            认证 = "✅国标" if info.get("is_china_standard") else "⏳待认证"
            类型 = "· 特殊" if info.get("type") == "special" else ""
            lines.append(
                f"- `{uid}` · {info.get('name', '-')} · {info.get('level')} {类型} · {认证} · "
                f"由 {info.get('granted_by')} 于 {info.get('granted_at', '-')[:10]} 授权"
            )
        return "\n".join(lines)

    def 生成确认码(self, 操作: str, 授权人: str, 有效期分钟: int = 10) -> str:
        码 = f"{secrets.randbelow(900000) + 100000}"
        库 = self._加载确认码()
        库[码] = {
            "operation": 操作,
            "generated_by": 授权人,
            "user_id": "",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=有效期分钟)).isoformat(),
            "used": False,
        }
        self._保存确认码(库)
        return 码

    def 校验确认码(self, 码: str, 操作: str) -> Dict[str, Any]:
        库 = self._加载确认码()
        记录 = 库.get(码)
        if not 记录:
            return {"有效": False, "原因": "确认码不存在"}
        if 记录.get("used"):
            return {"有效": False, "原因": "确认码已使用"}
        if datetime.fromisoformat(记录["expires_at"]) < datetime.now(timezone.utc):
            return {"有效": False, "原因": "确认码已过期"}
        if 记录.get("operation") and 记录["operation"] != 操作:
            return {"有效": False, "原因": f"确认码操作不匹配（期望: {记录['operation']}）"}
        记录["used"] = True
        self._保存确认码(库)
        return {"有效": True, "原因": "确认码校验通过"}

    def _加载确认码(self) -> Dict[str, Any]:
        if not self.确认码路径.exists():
            return {}
        try:
            return json.loads(self.确认码路径.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _保存确认码(self, 数据: Dict[str, Any]):
        self.确认码路径.write_text(json.dumps(数据, ensure_ascii=False, indent=2), encoding="utf-8")


# ============ 2. 主权验证器 ============
class 主权验证器:
    """验证用户身份、DNA、返回有效等级"""

    def __init__(self, 配置: 主权配置, 注册表: 授权注册表):
        self.配置 = 配置
        self.注册表 = 注册表

    def 验证(self, 用户标识: str, 消息脱氧核糖核酸: str = "") -> Dict[str, Any]:
        有效等级, 原始等级, 已认证 = self.注册表.获取有效等级(用户标识)

        if 消息脱氧核糖核酸 and self.配置.脱氧核糖核酸锚定 not in 消息脱氧核糖核酸:
            return {"通过": False, "原因": "DNA不匹配", "操作": "熔断", "等级": 有效等级, "原始等级": 原始等级, "已认证": 已认证}

        return {
            "通过": True,
            "原因": "主权验证通过",
            "操作": "执行",
            "等级": 有效等级,
            "原始等级": 原始等级,
            "已认证": 已认证,
        }


# ============ 3. 自然语义命令意图路由 ============
class 意图路由器:
    """
    让老百姓不用背精确指令，说人话就能命中 LU 能力。
    精确指令继续保留给 L1/L2 执行者。
    """

    # 意图关键词：越靠前优先级越高
    _意图表 = [
        {
            "命令": "压缩",
            "类型": "lu-memory",
            "关键词": ["记住", "存一下", "帮我存", "记下来", "压起来", "存起来", "保存一下", "压缩一下"],
        },
        {
            "命令": "还原",
            "类型": "lu-memory",
            "关键词": ["找回来", "调出来", "给我看看", "拿回来", "恢复一下", "还原一下"],
        },
        {
            "命令": "LU搜索",
            "类型": "lu-memory",
            "关键词": ["搜一下", "找找看", "查一下", "搜索一下"],
        },
        {
            "命令": "LU画廊",
            "类型": "lu-memory",
            "关键词": ["画廊", "卡片墙", "看看卡片", "卡片画廊"],
        },
        {
            "命令": "提意见",
            "类型": "collective-wisdom",
            "关键词": ["提意见", "我建议", "我有个建议", "我有个想法", "吐槽一下", "反馈一下", "能不能", "能不能加个", "建议增加"],
        },
        {
            "命令": "发送测试消息",
            "类型": "feishu-send",
            "关键词": ["发个测试", "发测试消息", "测试一下机器人", "测试飞书"],
        },
        {
            "命令": "发送评估报告",
            "类型": "feishu-send",
            "关键词": ["发送评估报告", "把报告发到群里", "发评估报告", "推送评估报告"],
        },
        {
            "命令": "审查内容",
            "类型": "content-review",
            "关键词": ["审查内容", "发布前审查", "内容审查", "检查一下内容", "这能发吗"],
        },
        {
            "命令": "跑训练优化",
            "类型": "training-optimizer",
            "关键词": ["跑训练数据优化", "跑训练优化", "训练优化", "跑一下训练", "跑优化", "跑训练", "优化训练数据"],
        },
        {
            "命令": "登记身份",
            "类型": "identity-register",
            "关键词": ["登记", "注册", "我是新人", "生成DNA", "生成UID", "我要登记", "我要注册"],
        },
    ]

    def infer(self, 原始消息: str, 归一化消息: str) -> Optional[Dict[str, Any]]:
        """从自然语言中识别意图并提取参数。"""
        for intent in self._意图表:
            for kw in intent["关键词"]:
                # 在归一化消息里找关键词位置
                idx = 归一化消息.find(kw)
                if idx == -1:
                    continue
                # 参数 = 关键词之后的文本（从原始消息或归一化消息提取）
                # 优先用原始消息保留大小写、DNA、LU 短码
                # 如果原始消息和归一化消息长度/结构差异大，用归一化消息兜底
                参数起点 = idx + len(kw)
                参数 = 归一化消息[参数起点:].strip(" :：")
                # 尝试从原始消息同位置提取（避免 opencc/小写破坏 DNA）
                原始参数 = self._extract_raw_param(原始消息, kw, 参数)
                return {
                    "命令": intent["命令"],
                    "系统命令": "",
                    "参数": 原始参数,
                    "类型": intent["类型"],
                    "_intent_matched": kw,
                }
        return None

    @staticmethod
    def _extract_raw_param(原始消息: str, 关键词: str, 归一化参数: str) -> str:
        """尽量从原始消息提取参数，保留 LU 短码、DNA 大小写。"""
        # 简单策略：如果原始消息包含关键词（繁体/简体），取关键词之后内容
        for variant in (关键词,):
            idx = 原始消息.find(variant)
            if idx != -1:
                return 原始消息[idx + len(variant):].strip(" :：")
        # 兜底
        return 归一化参数


# ============ 4. 命令解析器 ============
class 命令解析器:
    """解析飞书消息中的指令"""

    def __init__(self, 配置: 主权配置):
        self.配置 = 配置
        self._归一化 = SemanticNormalizer() if SemanticNormalizer else None
        self._意图路由 = 意图路由器()

    def 清洗(self, 原始消息: str) -> str:
        # 先進行語義歸一化：繁簡、全半形、大小寫、多語言變體統一
        消息 = self._归一化.normalize(原始消息) if self._归一化 else 原始消息
        消息 = re.sub(r"^@龙智守\s*", "", 消息.strip())
        消息 = re.sub(r"^@龍智守\s*", "", 消息)
        return 消息

    def 解析(self, 原始消息: str) -> Dict[str, Any]:
        消息 = self.清洗(原始消息)

        # 授权管理指令（先匹配完整词）
        if 消息 in ("授权列表", "用户列表"):
            return {"命令": "授权列表", "系统命令": "", "参数": "", "类型": "管理"}
        if 消息.startswith(("授权", "添加用户", "新增用户")):
            return self._解析授权(消息)
        if 消息.startswith(("撤销", "删除用户", "移除用户")):
            return self._解析撤销(消息)
        if 消息.startswith(("标记中国标准", "认证")):
            return self._解析标记中国标准(消息)
        if 消息.startswith(("确认码", "生成确认码")):
            参数 = 消息.split(None, 1)[1] if len(消息.split(None, 1)) > 1 else "敏感操作"
            return {"命令": "确认码", "系统命令": "", "参数": 参数, "类型": "管理"}

        # DNA 主權引擎指令
        if 消息.startswith(("登记DNA", "登记 DNA")):
            return self._解析登记DNA(消息)
        if 消息.startswith(("继承DNA", "继承 DNA")):
            return self._解析继承DNA(消息)
        if 消息.startswith(("贡献登记", "登记贡献")):
            return self._解析贡献登记(消息)
        if 消息.startswith(("贡献查询", "查询贡献")):
            return self._解析贡献查询(消息)
        if 消息.startswith(("DNA状态", "DNA 状态")):
            return self._解析DNA状态(消息)

        # LU 认知压缩命令（使用原始消息保留短码、DNA 与大小写）
        原始去头 = re.sub(r"^@[龙龍]智守\s*", "", 原始消息.strip())
        if 原始去头.startswith(("LU压缩", "LU 压缩", "lu压缩", "压缩")):
            return self._解析压缩(原始去头)
        if 原始去头.startswith(("还原", "LU还原", "LU 还原")):
            return self._解析还原(原始去头)
        if 原始去头.startswith(("LU搜索", "LU 搜索", "lu搜索")):
            return self._解析LU搜索(原始去头)
        if 原始去头 in ("LU列表", "lu列表", "LU 列表"):
            return {"命令": "LU列表", "系统命令": "", "参数": "", "类型": "lu-memory"}
        if 原始去头 in ("LU统计", "lu统计", "LU 统计"):
            return {"命令": "LU统计", "系统命令": "", "参数": "", "类型": "lu-memory"}
        if 原始去头.startswith(("LU语义搜索", "LU 语义搜索", "lu语义搜索")):
            return self._解析LU语义搜索(原始去头)
        if 原始去头 in ("LU画廊", "lu画廊", "LU 画廊"):
            return {"命令": "LU画廊", "系统命令": "", "参数": "", "类型": "lu-memory"}

        # 集思广益命令
        if 原始去头.startswith(("提意见", "建议", "反馈")):
            return self._解析提意见(原始去头)
        if 原始去头.startswith(("采纳意见", "拒绝意见", "忽略意见", "验证意见")):
            return self._解析意见操作(原始去头)
        if 原始去头 in ("置顶意见", "意见列表", "意见统计"):
            return {"命令": 原始去头, "系统命令": "", "参数": "", "类型": "collective-wisdom"}

        # 工具集生态命令
        if 原始去头.startswith(("反馈", "一键反馈")):
            return self._解析反馈(原始去头)
        if 原始去头 in ("功能统计", "公开意见包"):
            return {"命令": 原始去头, "系统命令": "", "参数": "", "类型": "toolset-ecosystem"}

        # 飞书消息推送命令
        if 原始去头.startswith(("发送测试消息", "发测试消息")):
            参数 = 原始去头.split(None, 1)[1] if len(原始去头.split(None, 1)) > 1 else "🐉 龍智守测试消息：机器人连接正常。"
            return {"命令": "发送测试消息", "系统命令": "", "参数": 参数, "类型": "feishu-send"}
        if 原始去头.startswith(("发送评估报告", "发评估报告", "推送评估报告")):
            return {"命令": "发送评估报告", "系统命令": "", "参数": "", "类型": "feishu-send"}

        # 内容主权审查命令
        if 原始去头.startswith(("审查内容", "发布前审查", "内容审查")):
            参数 = 原始去头.split(None, 1)[1] if len(原始去头.split(None, 1)) > 1 else ""
            return {"命令": "审查内容", "系统命令": "", "参数": 参数, "类型": "content-review"}

        # 训练数据优化命令
        if 原始去头.startswith(("跑训练数据优化", "跑训练优化", "跑一下训练优化", "优化训练数据")):
            return {"命令": "跑训练优化", "系统命令": "", "参数": "", "类型": "training-optimizer"}

        # 实名认证命令（创始人/管理员专用）
        if 原始去头.startswith("实名认证"):
            参数 = 原始去头.split(None, 1)[1] if len(原始去头.split(None, 1)) > 1 else ""
            return {"命令": "实名认证", "系统命令": "", "参数": 参数, "类型": "identity-verify"}

        # 身份登记命令
        if 原始去头.startswith(("登记身份", "我要登记", "我要注册", "生成DNA", "生成UID")):
            参数 = 原始去头.split(None, 1)[1] if len(原始去头.split(None, 1)) > 1 else ""
            return {"命令": "登记身份", "系统命令": "", "参数": 参数, "类型": "identity-register"}

        # 自然语义路由：老百姓说人话也能命中 LU 能力 / 集思广益
        intent = self._意图路由.infer(原始消息, 消息)
        if intent:
            return intent

        # 普通命令
        for 关键词, 系统命令 in self.配置.命令映射.items():
            if 关键词 in 消息:
                位置 = 消息.find(关键词) + len(关键词)
                参数 = 消息[位置:].strip()
                return {"命令": 关键词, "系统命令": 系统命令, "参数": 参数, "类型": "执行"}

        return {"命令": "未知", "系统命令": "", "参数": 消息, "类型": "对话"}

    def _解析授权(self, 消息: str) -> Dict[str, Any]:
        部分 = 消息.split()
        if len(部分) < 3:
            return {"命令": "授权", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，应为：授权 <用户ID> <L0/L1/L2/L2-SP/L3> [姓名]"}
        return {"命令": "授权", "系统命令": "", "参数": {"用户ID": 部分[1], "等级": 部分[2], "姓名": " ".join(部分[3:]) or 部分[1]}, "类型": "管理"}

    def _解析撤销(self, 消息: str) -> Dict[str, Any]:
        部分 = 消息.split()
        if len(部分) < 2:
            return {"命令": "撤销", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，应为：撤销 <用户ID>"}
        return {"命令": "撤销", "系统命令": "", "参数": {"用户ID": 部分[1]}, "类型": "管理"}

    def _解析标记中国标准(self, 消息: str) -> Dict[str, Any]:
        部分 = 消息.split()
        if len(部分) < 2:
            return {"命令": "标记中国标准", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，应为：标记中国标准 <用户ID>"}
        return {"命令": "标记中国标准", "系统命令": "", "参数": {"用户ID": 部分[1]}, "类型": "管理"}

    def _解析登记DNA(self, 消息: str) -> Dict[str, Any]:
        部分 = 消息.split()
        if len(部分) < 2:
            return {"命令": "登记DNA", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，应为：登记DNA <DNA> [生物锚哈希] [设备指纹] [所有者]"}
        return {
            "命令": "登记DNA",
            "系统命令": "",
            "参数": {
                "DNA": 部分[1],
                "生物锚": 部分[2] if len(部分) > 2 else "",
                "设备": 部分[3] if len(部分) > 3 else "",
                "所有者": " ".join(部分[4:]) if len(部分) > 4 else "",
            },
            "类型": "dna-sovereignty",
        }

    def _解析继承DNA(self, 消息: str) -> Dict[str, Any]:
        部分 = 消息.split()
        if len(部分) < 3:
            return {"命令": "继承DNA", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，应为：继承DNA <旧DNA> <新DNA> [生物锚哈希] [设备指纹] [所有者]"}
        return {
            "命令": "继承DNA",
            "系统命令": "",
            "参数": {
                "旧DNA": 部分[1],
                "新DNA": 部分[2],
                "生物锚": 部分[3] if len(部分) > 3 else "",
                "设备": 部分[4] if len(部分) > 4 else "",
                "所有者": " ".join(部分[5:]) if len(部分) > 5 else "",
            },
            "类型": "dna-sovereignty",
        }

    def _解析贡献登记(self, 消息: str) -> Dict[str, Any]:
        部分 = 消息.split()
        if len(部分) < 4:
            return {"命令": "贡献登记", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，应为：贡献登记 <DNA> <类别> <描述> [值]"}
        # 嘗試把最後一個可選欄位解析為數值
        值 = 1
        描述終點 = len(部分)
        if len(部分) > 4 and 部分[-1].isdigit():
            值 = int(部分[-1])
            描述終點 = -1
        return {
            "命令": "贡献登记",
            "系统命令": "",
            "参数": {
                "DNA": 部分[1],
                "类别": 部分[2],
                "值": 值,
                "描述": " ".join(部分[3:描述終點]),
            },
            "类型": "dna-sovereignty",
        }

    def _解析贡献查询(self, 消息: str) -> Dict[str, Any]:
        部分 = 消息.split()
        if len(部分) < 2:
            return {"命令": "贡献查询", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，应为：贡献查询 <DNA>"}
        return {"命令": "贡献查询", "系统命令": "", "参数": {"DNA": 部分[1]}, "类型": "dna-sovereignty"}

    def _解析DNA状态(self, 消息: str) -> Dict[str, Any]:
        部分 = 消息.split()
        return {"命令": "DNA状态", "系统命令": "", "参数": {"DNA": 部分[1] if len(部分) > 1 else ""}, "类型": "dna-sovereignty"}

    def _解析压缩(self, 消息: str) -> Dict[str, Any]:
        # 支持 "压缩 内容..." / "LU压缩 内容..." / "LU 压缩 内容..."
        for prefix in ("LU 压缩", "LU压缩", "lu压缩", "压缩"):
            if 消息.startswith(prefix):
                参数 = 消息[len(prefix):].strip()
                break
        else:
            参数 = ""
        if not 参数:
            return {"命令": "压缩", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，应为：压缩 <要压缩的长文本>"}
        return {"命令": "压缩", "系统命令": "", "参数": 参数, "类型": "lu-memory"}

    def _解析还原(self, 消息: str) -> Dict[str, Any]:
        for prefix in ("LU 还原", "LU还原", "还原"):
            if 消息.startswith(prefix):
                参数 = 消息[len(prefix):].strip()
                break
        else:
            参数 = ""
        if not 参数:
            return {"命令": "还原", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，应为：还原 <LU短码 或 DNA>"}
        return {"命令": "还原", "系统命令": "", "参数": 参数, "类型": "lu-memory"}

    def _解析LU搜索(self, 消息: str) -> Dict[str, Any]:
        for prefix in ("LU 搜索", "LU搜索", "lu搜索"):
            if 消息.startswith(prefix):
                参数 = 消息[len(prefix):].strip()
                break
        else:
            参数 = ""
        if not 参数:
            return {"命令": "LU搜索", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，应为：LU搜索 <关键词>"}
        return {"命令": "LU搜索", "系统命令": "", "参数": 参数, "类型": "lu-memory"}

    def _解析LU语义搜索(self, 消息: str) -> Dict[str, Any]:
        for prefix in ("LU 语义搜索", "LU语义搜索", "lu语义搜索"):
            if 消息.startswith(prefix):
                参数 = 消息[len(prefix):].strip()
                break
        else:
            参数 = ""
        if not 参数:
            return {"命令": "LU语义搜索", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，应为：LU语义搜索 <查询句>"}
        return {"命令": "LU语义搜索", "系统命令": "", "参数": 参数, "类型": "lu-memory"}

    def _解析提意见(self, 消息: str) -> Dict[str, Any]:
        for prefix in ("提意见", "建议", "反馈"):
            if 消息.startswith(prefix):
                参数 = 消息[len(prefix):].strip(" :：")
                break
        else:
            参数 = ""
        if not 参数:
            return {"命令": "提意见", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，例如：提意见 增加语音输入功能"}
        return {"命令": "提意见", "系统命令": "", "参数": 参数, "类型": "collective-wisdom"}

    def _解析意见操作(self, 消息: str) -> Dict[str, Any]:
        for prefix in ("采纳意见", "拒绝意见", "忽略意见", "验证意见"):
            if 消息.startswith(prefix):
                参数 = 消息[len(prefix):].strip()
                命令 = prefix
                break
        else:
            return {"命令": "未知", "系统命令": "", "参数": 消息, "类型": "对话"}
        if not 参数:
            return {"命令": 命令, "系统命令": "", "参数": "", "类型": "错误", "原因": f"格式错误，应为：{命令} <意见码>"}
        return {"命令": 命令, "系统命令": "", "参数": 参数, "类型": "collective-wisdom"}

    def _解析反馈(self, 消息: str) -> Dict[str, Any]:
        for prefix in ("一键反馈", "反馈"):
            if 消息.startswith(prefix):
                参数 = 消息[len(prefix):].strip(" :：")
                break
        else:
            参数 = ""
        # 参数格式：<功能ID/名称> <内容>
        parts = 参数.split(None, 1)
        if len(parts) < 2:
            return {"命令": "反馈", "系统命令": "", "参数": "", "类型": "错误", "原因": "格式错误，例如：反馈 压缩记忆 希望能支持语音输入"}
        return {"命令": "反馈", "系统命令": "", "参数": {"function": parts[0], "content": parts[1]}, "类型": "toolset-ecosystem"}


# ============ 4. 执行引擎 ============
class 执行引擎:
    """安全执行本地命令"""

    def __init__(self, 配置: 主权配置, 注册表: 授权注册表):
        self.配置 = 配置
        self.注册表 = 注册表
        self._敏感检查 = 敏感操作检查器(配置)
        self._dna处理器 = DNA主权命令处理器(注册表) if DnaSovereigntyEngine else None
        self._lu处理器 = LuMemoryCommandHandler(注册表) if LonghunLuMemoryEngine else None
        self._cw处理器 = CollectiveWisdomCommandHandler(注册表) if CollectiveWisdomEngine else None
        self._工具集处理器 = ToolsetCommandHandler(注册表) if ToolsetEcosystemEngine else None
        self._飞书 = 飞书消息发送器()
        self._内容审查器 = 公开内容审查器() if 公开内容审查器 else None
        self._身份注册器 = 龍魂身份注册器(注册表, 配置) if 龍魂身份注册器 else None

    def 执行(self, 解析结果: Dict[str, Any], 等级: int, 原始等级: str, 用户标识: str, 原始消息: str) -> Dict[str, Any]:
        命令词 = 解析结果["命令"]
        参数 = 解析结果.get("参数", "")

        # 权限检查
        所需等级 = self.配置.命令等级.get(命令词, 3)
        if 等级 < 所需等级:
            return {"成功": False, "输出": f"🔴 权限不足: `{命令词}` 需要 L{所需等级} 及以上", "返回码": -1}

        # L2-SP 命令类别限制
        if 原始等级 == "L2-SP":
            类别 = self.配置.命令类别.get(命令词)
            if 类别 and 类别 in self.配置.L2SP禁止类别:
                return {"成功": False, "输出": f"🔴 L2-SP 特殊部门禁止执行 `{命令词}`（类别：{类别}）", "返回码": -1}

        # 管理类命令
        if 解析结果["类型"] == "管理":
            return self._执行管理(解析结果, 等级, 原始等级, 用户标识)

        # DNA 主權引擎命令
        if 解析结果["类型"] == "dna-sovereignty":
            if not self._dna处理器:
                return {"成功": False, "输出": "🔴 DNA 主权引擎未加载", "返回码": -1}
            return self._dna处理器.执行(解析结果, 等级, 原始等级, 用户标识)

        # LU 认知压缩命令
        if 解析结果["类型"] == "lu-memory":
            if not self._lu处理器:
                return {"成功": False, "输出": "🔴 LU 认知压缩引擎未加载", "返回码": -1}
            return self._lu处理器.执行(解析结果, 等级, 原始等级, 用户标识, 原始消息)

        # 集思广益命令
        if 解析结果["类型"] == "collective-wisdom":
            if not self._cw处理器:
                return {"成功": False, "输出": "🔴 集思广益引擎未加载", "返回码": -1}
            return self._cw处理器.执行(解析结果, 等级, 原始等级, 用户标识)

        # 工具集生态命令
        if 解析结果["类型"] == "toolset-ecosystem":
            if not self._工具集处理器:
                return {"成功": False, "输出": "🔴 工具集生态引擎未加载", "返回码": -1}
            return self._工具集处理器.执行(解析结果, 等级, 原始等级, 用户标识)

        # 飞书消息推送命令
        if 解析结果["类型"] == "feishu-send":
            return self._执行飞书发送(解析结果, 等级, 原始等级, 用户标识)

        # 内容主权审查命令
        if 解析结果["类型"] == "content-review":
            return self._执行内容审查(解析结果, 等级, 原始等级, 用户标识)

        # 训练数据优化命令
        if 解析结果["类型"] == "training-optimizer":
            return self._执行训练优化(解析结果, 等级, 原始等级, 用户标识)

        # 身份登记命令
        if 解析结果["类型"] == "identity-register":
            return self._执行身份登记(解析结果, 等级, 原始等级, 用户标识)

        # 实名认证命令
        if 解析结果["类型"] == "identity-verify":
            return self._执行实名认证(解析结果, 等级, 原始等级, 用户标识)

        # 二次确认码提取
        确认码 = self._提取确认码(原始消息)

        # 敏感操作检查
        检查文本 = f"{命令词} {参数}"
        敏感检查 = self._敏感检查.检查(检查文本)
        if 敏感检查["敏感"]:
            if 等级 < 3:
                if not 确认码:
                    return {
                        "成功": False,
                        "输出": f"🔴 敏感操作阻断: {敏感检查['原因']}\n请让 L2/L3 生成确认码后再执行。",
                        "返回码": -1,
                    }
                校验 = self.注册表.校验确认码(确认码, 命令词)
                if not 校验["有效"]:
                    return {"成功": False, "输出": f"🔴 确认码无效: {校验['原因']}", "返回码": -1}

        # 构建完整命令（去掉确认码字段，并用 shlex.quote 阻断注入）
        系统命令 = 解析结果.get("系统命令", "")
        if 参数 and isinstance(参数, str):
            参数 = re.sub(r"确认码[\s:：]*\d{6}", "", 参数).strip()
            完整命令 = f"{系统命令} {shlex.quote(参数)}" if 参数 else 系统命令
        else:
            完整命令 = 系统命令

        try:
            结果 = subprocess.run(
                完整命令,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(Path.home()),
            )
            return {
                "成功": 结果.returncode == 0,
                "输出": 结果.stdout if 结果.returncode == 0 else 结果.stderr,
                "返回码": 结果.returncode,
                "命令": 完整命令,
            }
        except subprocess.TimeoutExpired:
            return {"成功": False, "输出": "⏱️ 命令执行超时（30秒）", "返回码": -1}
        except Exception as 错误:
            return {"成功": False, "输出": f"❌ 执行错误: {str(错误)}", "返回码": -1}

    def 工具集使用反馈(self, 解析结果: Dict[str, Any], 用户标识: str) -> str:
        """记录命令使用并返回主动提醒文本（如有）。"""
        if not self._工具集处理器:
            return ""
        命令 = 解析结果.get("命令", "未知")
        # 把命令映射到一个功能模块 ID
        功能映射 = {
            "压缩": "lu_compress",
            "LU压缩": "lu_compress",
            "还原": "lu_recall",
            "LU搜索": "lu_search",
            "LU语义搜索": "lu_semantic_search",
            "LU画廊": "lu_gallery",
            "LU列表": "lu_list",
            "LU统计": "lu_stats",
            "提意见": "collective_wisdom",
            "建议": "collective_wisdom",
            "反馈": "collective_wisdom_feedback",
            "意见列表": "collective_wisdom",
            "置顶意见": "collective_wisdom",
            "验证意见": "collective_wisdom",
            "采纳意见": "collective_wisdom",
            "拒绝意见": "collective_wisdom",
            "忽略意见": "collective_wisdom",
            "功能统计": "toolset_stats",
            "公开意见包": "toolset_public_package",
        }
        function_id = 功能映射.get(命令, 命令)
        try:
            self._工具集处理器.引擎.record_usage(function_id, 用户标识, event_type="use", context=f"命令:{命令}")
            remind = self._工具集处理器.引擎.should_remind(function_id, 用户标识)
            if remind:
                self._工具集处理器.引擎.create_reminder(function_id, 用户标识, context=f"命令:{命令}")
                return (
                    f"\n\n💡 主动提醒：你刚用了『{remind['function_name']}』"
                    f"（第 {remind['usage_count']} 次）。\n"
                    f"如果对这个新用法有想法，直接回复：\n"
                    f"`反馈 {function_id} <你的想法>`\n"
                    f"系统会自动带 DNA 归档，无需填表。"
                )
        except Exception:
            pass
        return ""

    def _执行管理(self, 解析结果: Dict[str, Any], 等级: int, 原始等级: str, 用户标识: str) -> Dict[str, Any]:
        命令 = 解析结果["命令"]
        参数 = 解析结果.get("参数", {})

        if 解析结果.get("类型") == "错误":
            return {"成功": False, "输出": f"🔴 {解析结果.get('原因', '格式错误')}", "返回码": -1}

        if 命令 == "授权":
            if 等级 < 1:
                return {"成功": False, "输出": "🔴 权限不足：L0 不能授权他人", "返回码": -1}
            目标用户 = 参数.get("用户ID")
            目标等级 = 参数.get("等级")
            姓名 = 参数.get("姓名", 目标用户)
            if not 目标用户 or not 目标等级:
                return {"成功": False, "输出": "🔴 格式错误：授权 <用户ID> <L0/L1/L2/L2-SP/L3> [姓名]", "返回码": -1}
            结果 = self.注册表.授权(目标用户, 目标等级, 姓名, 用户标识)
            return {"成功": 结果["成功"], "输出": f"{'🟢' if 结果['成功'] else '🔴'} {结果['原因']}", "返回码": 0 if 结果["成功"] else -1}

        if 命令 == "撤销":
            if 等级 < 1:
                return {"成功": False, "输出": "🔴 权限不足：L0 不能撤销他人", "返回码": -1}
            目标用户 = 参数.get("用户ID")
            if not 目标用户:
                return {"成功": False, "输出": "🔴 格式错误：撤销 <用户ID>", "返回码": -1}
            结果 = self.注册表.撤销(目标用户, 用户标识)
            return {"成功": 结果["成功"], "输出": f"{'🟢' if 结果['成功'] else '🔴'} {结果['原因']}", "返回码": 0 if 结果["成功"] else -1}

        if 命令 == "授权列表":
            if 等级 < 1:
                return {"成功": False, "输出": "🔴 权限不足：L0 不能查看授权列表", "返回码": -1}
            return {"成功": True, "输出": self.注册表.授权列表(), "返回码": 0}

        if 命令 == "标记中国标准":
            if 等级 < 3:
                return {"成功": False, "输出": "🔴 权限不足：只有 L3 创始人可标记中国标准", "返回码": -1}
            目标用户 = 参数.get("用户ID")
            if not 目标用户:
                return {"成功": False, "输出": "🔴 格式错误：标记中国标准 <用户ID>", "返回码": -1}
            结果 = self.注册表.标记中国标准(目标用户, 用户标识)
            return {"成功": 结果["成功"], "输出": f"{'🟢' if 结果['成功'] else '🔴'} {结果['原因']}", "返回码": 0 if 结果["成功"] else -1}

        if 命令 == "确认码":
            if 等级 < 2:
                return {"成功": False, "输出": "🔴 权限不足：只有 L2/L2-SP/L3 可生成确认码", "返回码": -1}
            操作 = 参数 if isinstance(参数, str) else "敏感操作"
            码 = self.注册表.生成确认码(操作, 用户标识)
            return {"成功": True, "输出": f"🟢 确认码已生成（10分钟内有效）: `{码}`\n用途: {操作}\n任何授权用户均可使用一次", "返回码": 0}

        return {"成功": False, "输出": "🔴 未知管理命令", "返回码": -1}

    def _提取确认码(self, 消息: str) -> Optional[str]:
        匹配 = re.search(r"确认码[\s:：]*(\d{6})", 消息)
        return 匹配.group(1) if 匹配 else None

    def _执行飞书发送(self, 解析结果: Dict[str, Any], 等级: int, 原始等级: str, 用户标识: str) -> Dict[str, Any]:
        命令 = 解析结果["命令"]
        if 命令 == "发送测试消息":
            文本 = 解析结果.get("参数") or "🐉 龍智守测试消息：机器人连接正常。"
            结果 = self._飞书.发送文本(文本)
            if 结果.get("成功"):
                return {"成功": True, "输出": f"🟢 测试消息已发送：{文本[:50]}{'...' if len(文本) > 50 else ''}", "返回码": 0}
            return {"成功": False, "输出": f"🔴 发送失败：{结果.get('响应') or 结果.get('错误', '未知错误')}", "返回码": -1}

        if 命令 == "发送评估报告":
            report_dir = Path.home() / ".longhun" / "evaluation"
            files = sorted(report_dir.glob("unified_evaluation_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
            report_path = files[0] if files else None
            if not report_path or not report_path.exists():
                return {"成功": False, "输出": "🔴 未找到统一评估报告", "返回码": -1}

            content = report_path.read_text(encoding="utf-8")
            # 公开前自动内容主权审查
            if self._内容审查器:
                review = self._内容审查器.生成报告(content)
                if "🔴" in review:
                    return {"成功": False, "输出": f"🔴 评估报告未通过内容主权审查，禁止发布。\n\n{review}", "返回码": -1}
                if "🟡" in review:
                    content = "🟡 本报告已通过内容主权初审，存在待关注项，请 UID9622 复核后再公开。\n\n" + content

            标题 = f"🐉 龍魂系统 · 统一评估报告 ({report_path.stem.split('_')[-1]})"
            结果 = self._飞书.发送Markdown(标题, content)
            if 结果.get("成功"):
                return {"成功": True, "输出": f"🟢 评估报告已推送至飞书：{report_path.name}", "返回码": 0}
            return {"成功": False, "输出": f"🔴 推送失败：{结果.get('响应') or 结果.get('错误', '未知错误')}", "返回码": -1}

        return {"成功": False, "输出": "🔴 未知飞书发送命令", "返回码": -1}

    def _执行内容审查(self, 解析结果: Dict[str, Any], 等级: int, 原始等级: str, 用户标识: str) -> Dict[str, Any]:
        文本 = 解析结果.get("参数", "")
        if not 文本:
            return {"成功": False, "输出": "🔴 请提供要审查的内容：审查内容 <文本>", "返回码": -1}
        if not self._内容审查器:
            return {"成功": False, "输出": "🔴 内容主权审查器未加载", "返回码": -1}

        报告 = self._内容审查器.生成报告(文本)
        # 提取状态行判断三色
        状态 = "🟡"
        for line in 报告.splitlines():
            if "审查状态**" in line:
                if "🟢" in line:
                    状态 = "🟢"
                elif "🔴" in line:
                    状态 = "🔴"
                break

        提示 = f"{状态} 内容主权审查完成，最终发布决定权归 UID9622。\n\n{报告}"
        return {"成功": True, "输出": 提示, "返回码": 0}

    def _执行训练优化(self, 解析结果: Dict[str, Any], 等级: int, 原始等级: str, 用户标识: str) -> Dict[str, Any]:
        """调用龍魂訓練數據優化器 v3.2.0，生成报告并推送飞书。"""
        # 優先使用規範化目錄 ~/.longhun/training/scripts/ 中的主版本
        optimizer_path = Path.home() / ".longhun" / "training" / "scripts" / "龍魂訓練數據優化器_v3.2.0.py"
        # 兼容舊版 Downloads 路徑
        fallback_path = Path.home() / "Downloads" / "Kimi_Agent_龙魂训练协议" / "龍魂訓練數據優化器_v3.2.0.py"
        if not optimizer_path.exists():
            if fallback_path.exists():
                optimizer_path = fallback_path
            else:
                return {"成功": False, "输出": f"🔴 优化器脚本不存在: {optimizer_path}", "返回码": -1}

        # 不用 shell=True，避免注入；使用当前 Python 解释器
        cmd = [sys.executable, str(optimizer_path), "--加密"]
        try:
            result = subprocess.run(
                cmd,
                shell=False,
                capture_output=True,
                text=True,
                timeout=180,
                cwd=str(optimizer_path.parent),
            )
        except subprocess.TimeoutExpired:
            return {"成功": False, "输出": "⏱️ 训练优化执行超时（180秒）", "返回码": -1}
        except Exception as e:
            return {"成功": False, "输出": f"❌ 执行优化器失败: {e}", "返回码": -1}

        if result.returncode != 0:
            return {"成功": False, "输出": f"🔴 优化器执行失败（返回码 {result.returncode}）：\n{result.stderr}", "返回码": -1}

        report_dir = Path.home() / "longhun-system" / "data" / "training" / "v3.2"
        if not report_dir.exists():
            return {"成功": False, "输出": f"🔴 报告目录不存在: {report_dir}", "返回码": -1}

        report_files = sorted(report_dir.glob("report_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        if not report_files:
            return {"成功": False, "输出": "🔴 未找到生成的报告文件", "返回码": -1}

        latest_report = report_files[0]
        try:
            report_data = json.loads(latest_report.read_text(encoding="utf-8"))
        except Exception as e:
            return {"成功": False, "输出": f"🔴 读取报告失败: {e}", "返回码": -1}

        # 报告字段为繁体（与优化器输出保持一致）
        熔断统计 = report_data.get("熔斷統計", {})
        质量统计 = report_data.get("質量統計", {})
        主权统计 = report_data.get("主權統計", {})
        来源统计 = report_data.get("來源統計", [])
        总条数 = sum(质量统计.values()) if 质量统计 else 0

        来源行 = "\n".join(
            f"- {item.get('渠道', '未知')}: {item.get('條目數', 0)} 条"
            for item in 来源统计
        )

        msg = (
            f"## 🐉 龍魂训练数据优化报告\n"
            f"**生成时间**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
            f"**总数据条数**: {总条数}\n\n"
            f"### 📊 来源统计\n{来源行}\n\n"
            f"### 🔥 熔断统计\n"
            f"- 🟢 通过: {熔断统计.get('🟢', 0)}\n"
            f"- 🟡 警告: {熔断统计.get('🟡', 0)}\n"
            f"- 🔴 熔断: {熔断统计.get('🔴', 0)}\n\n"
            f"### 📈 质量评分\n"
            f"- 优秀: {质量统计.get('優秀', 0)}\n"
            f"- 合格: {质量统计.get('合格', 0)}\n"
            f"- 需改进: {质量统计.get('需改進', 0)}\n\n"
            f"### 🛡️ 主权审核\n"
            f"- 通过: {主权统计.get('通過', 0)}\n"
            f"- 熔断: {主权统计.get('熔斷', 0)}\n\n"
            f"**报告路径**: `{latest_report}`"
        )

        # 公开前自动内容主权审查
        if self._内容审查器:
            review = self._内容审查器.生成报告(msg)
            if "🔴" in review:
                return {"成功": False, "输出": f"🔴 训练优化报告未通过内容主权审查，禁止发布。\n\n{review}", "返回码": -1}
            if "🟡" in review:
                msg = "🟡 本报告已通过内容主权初审，存在待关注项，请 UID9622 复核后再公开。\n\n" + msg

        推送结果 = self._飞书.发送Markdown("龍魂训练数据优化报告", msg)
        if 推送结果.get("成功"):
            return {
                "成功": True,
                "输出": f"🟢 训练优化完成，报告已推送至飞书群。\n本地报告: {latest_report}",
                "返回码": 0,
                "数据": report_data,
            }
        else:
            return {
                "成功": False,
                "输出": f"🟡 优化完成，但飞书推送失败：{推送结果.get('响应') or 推送结果.get('错误', '未知错误')}。\n本地报告: {latest_report}",
                "返回码": -1,
            }

    def _执行身份登记(self, 解析结果: Dict[str, Any], 等级: int, 原始等级: str, 用户标识: str) -> Dict[str, Any]:
        """为飞书用户生成唯一 UID 和 DNA，默认未实名 L0。"""
        if not self._身份注册器:
            return {"成功": False, "输出": "🔴 身份注册器未加载", "返回码": -1}
        姓名 = str(解析结果.get("参数", "")).strip()
        结果 = self._身份注册器.登记(用户标识, 姓名=姓名, 操作人=用户标识)
        return {
            "成功": 结果.get("ok", False),
            "输出": 结果.get("message", "未知结果"),
            "返回码": 0 if 结果.get("ok") else -1,
            "数据": {"uid": 结果.get("uid"), "dna": 结果.get("dna"), "verified": 结果.get("verified")},
        }

    def _执行实名认证(self, 解析结果: Dict[str, Any], 等级: int, 原始等级: str, 用户标识: str) -> Dict[str, Any]:
        """创始人/管理员把用户升级为实名 L1。"""
        if not self._身份注册器:
            return {"成功": False, "输出": "🔴 身份注册器未加载", "返回码": -1}
        参数 = str(解析结果.get("参数", "")).strip()
        if not 参数:
            return {"成功": False, "输出": "🔴 格式错误：实名认证 <用户open_id> [姓名]", "返回码": -1}
        部分 = 参数.split(None, 1)
        目标open_id = 部分[0]
        姓名 = 部分[1] if len(部分) > 1 else ""
        结果 = self._身份注册器.实名认证(目标open_id, 姓名=姓名, 操作人=用户标识)
        return {
            "成功": 结果.get("ok", False),
            "输出": 结果.get("message", "未知结果"),
            "返回码": 0 if 结果.get("ok") else -1,
            "数据": {"uid": 结果.get("uid"), "dna": 结果.get("dna"), "verified": 结果.get("verified")},
        }


class 敏感操作检查器:
    """检查是否涉及敏感/危险操作"""

    def __init__(self, 配置: 主权配置):
        self.配置 = 配置

    def 检查(self, 命令文本: str) -> Dict[str, Any]:
        小写 = 命令文本.lower()
        for 敏感词 in self.配置.敏感操作列表:
            if 敏感词 in 小写:
                return {"敏感": True, "原因": f"检测到敏感操作: {敏感词}"}
        危险路径 = ["/System", "/usr/bin", "/etc", "rm -rf", "sudo"]
        for 路径 in 危险路径:
            if 路径 in 小写:
                return {"敏感": True, "原因": f"涉及系统路径/危险命令: {路径}"}
        return {"敏感": False, "原因": "通过"}


class DNA主权命令处理器:
    """把 DNA 主權引擎命令橋接到飛書本地控制接口"""

    def __init__(self, 注册表: 授权注册表):
        self.注册表 = 注册表
        self.引擎 = DnaSovereigntyEngine() if DnaSovereigntyEngine else None

    def 执行(self, 解析结果: Dict[str, Any], 等级: int, 原始等级: str, 用户标识: str) -> Dict[str, Any]:
        if not self.引擎:
            return {"成功": False, "输出": "🔴 DNA 主权引擎未加载", "返回码": -1}

        命令 = 解析结果["命令"]
        参数 = 解析结果.get("参数", {})

        if 解析结果.get("类型") == "错误":
            return {"成功": False, "输出": f"🔴 {解析结果.get('原因', '格式错误')}", "返回码": -1}

        if 命令 == "登记DNA":
            return self._登记DNA(参数, 用户标识)
        if 命令 == "继承DNA":
            return self._继承DNA(参数, 用户标识)
        if 命令 == "贡献登记":
            return self._贡献登记(参数, 用户标识)
        if 命令 == "贡献查询":
            return self._贡献查询(参数, 用户标识)
        if 命令 == "DNA状态":
            return self._DNA状态(参数)

        return {"成功": False, "输出": "🔴 未知 DNA 主权命令", "返回码": -1}

    def _默认生物锚(self, 用户标识: str) -> str:
        return hashlib.sha256(f"{用户标识}:longhun-biometric-anchor".encode("utf-8")).hexdigest()

    def _默认设备指纹(self, 用户标识: str) -> str:
        return hashlib.sha256(f"{用户标识}:longhun-device-fingerprint".encode("utf-8")).hexdigest()

    def _格式化(self, 结果: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "成功": bool(结果.get("ok")),
            "输出": 结果.get("message", "-"),
            "返回码": 0 if 结果.get("ok") else -1,
            "data": 结果,
        }

    def _登记DNA(self, 参数: Dict[str, Any], 用户标识: str) -> Dict[str, Any]:
        dna = 参数.get("DNA", "")
        bio = 参数.get("生物锚") or self._默认生物锚(用户标识)
        device = 参数.get("设备") or self._默认设备指纹(用户标识)
        owner = 参数.get("所有者") or 用户标识
        if not dna:
            return {"成功": False, "输出": "🔴 缺少 DNA", "返回码": -1}
        return self._格式化(
            self.引擎.register_identity(dna, owner, bio, device, 用户标识, user_id=用户标识)
        )

    def _继承DNA(self, 参数: Dict[str, Any], 用户标识: str) -> Dict[str, Any]:
        old = 参数.get("旧DNA", "")
        new = 参数.get("新DNA", "")
        bio = 参数.get("生物锚") or self._默认生物锚(用户标识)
        device = 参数.get("设备") or self._默认设备指纹(用户标识)
        owner = 参数.get("所有者") or 用户标识
        if not old or not new:
            return {"成功": False, "输出": "🔴 缺少旧/新 DNA", "返回码": -1}
        return self._格式化(
            self.引擎.seal_and_inherit(old, new, owner, bio, device, 用户标识, user_id=用户标识)
        )

    def _贡献登记(self, 参数: Dict[str, Any], 用户标识: str) -> Dict[str, Any]:
        dna = 参数.get("DNA", "")
        category = 参数.get("类别", "")
        desc = 参数.get("描述", "")
        value = 参数.get("值", 1)
        if not dna or not category or not desc:
            return {"成功": False, "输出": "🔴 格式错误：贡献登记 <DNA> <类别> <描述> [值]", "返回码": -1}
        return self._格式化(
            self.引擎.record_contribution(dna, category, desc, value, 用户标识)
        )

    def _贡献查询(self, 参数: Dict[str, Any], 用户标识: str) -> Dict[str, Any]:
        dna = 参数.get("DNA", "")
        if not dna:
            return {"成功": False, "输出": "🔴 缺少 DNA", "返回码": -1}
        result = self.引擎.list_contributions(dna)
        if not result.get("ok"):
            return self._格式化(result)
        lines = [f"🐉 DNA {dna} 的贡献记录（共 {result['count']} 条）"]
        for r in result.get("records", []):
            lines.append(
                f"- `{r.get('timestamp', '-')}` [{r.get('category', '-')}] {r.get('description', '-')} (值: {r.get('value', '-')})"
            )
        return {"成功": True, "输出": "\n".join(lines), "返回码": 0, "data": result}

    def _DNA状态(self, 参数: Dict[str, Any]) -> Dict[str, Any]:
        dna = 参数.get("DNA", "")
        if not dna:
            ids = self.引擎.list_identities("active")
            lines = [f"🐉 当前活跃 DNA 身份（{len(ids)} 个）"]
            for info in ids:
                lines.append(f"- `{info.get('dna_identity')}` · {info.get('owner_label')} · 创建于 {info.get('created_at', '-')[:10]}")
            return {"成功": True, "输出": "\n".join(lines), "返回码": 0}
        result = self.引擎.get_status(dna)
        if not result.get("ok"):
            return self._格式化(result)
        info = result["identity"]
        lines = [
            f"🐉 DNA 状态：`{dna}`",
            f"所有者：{info.get('owner_label')}",
            f"状态：{info.get('status')}",
            f"继承自：{info.get('inherited_from') or '无'}",
            f"贡献记录数：{result['contributions']['count']}",
        ]
        return {"成功": True, "输出": "\n".join(lines), "返回码": 0, "data": result}


class LuMemoryCommandHandler:
    """把 LU 认知压缩引擎桥接到飛書本地控制接口"""

    def __init__(self, 注册表: 授权注册表):
        self.注册表 = 注册表
        self.引擎 = LonghunLuMemoryEngine() if LonghunLuMemoryEngine else None

    def 执行(self, 解析结果: Dict[str, Any], 等级: int, 原始等级: str, 用户标识: str, 原始消息: str) -> Dict[str, Any]:
        if not self.引擎:
            return {"成功": False, "输出": "🔴 LU 认知压缩引擎未加载", "返回码": -1}

        命令 = 解析结果["命令"]
        参数 = 解析结果.get("参数", "")

        if 解析结果.get("类型") == "错误":
            return {"成功": False, "输出": f"🔴 {解析结果.get('原因', '格式错误')}", "返回码": -1}

        try:
            if 命令 == "压缩":
                return self._压缩(参数, 用户标识)
            if 命令 == "还原":
                return self._还原(参数, 用户标识)
            if 命令 == "LU搜索":
                return self._搜索(参数)
            if 命令 == "LU语义搜索":
                return self._语义搜索(参数)
            if 命令 == "LU列表":
                return self._列表()
            if 命令 == "LU统计":
                return self._统计()
            if 命令 == "LU画廊":
                return self._画廊()
        except Exception as e:
            return {"成功": False, "输出": f"🔴 LU 引擎执行错误：{e}", "返回码": -1}

        return {"成功": False, "输出": "🔴 未知 LU 命令", "返回码": -1}

    def _格式化卡片(self, record: Dict[str, Any], 含全文: bool = False) -> str:
        lines = [
            f"🗜️ LU 短码：`{record.get('lu_code')}`",
            f"🧬 DNA：`{record.get('dna')}`",
            f"📌 标题：{record.get('title') or record.get('summary')}",
            f"📝 摘要：{record.get('summary')}",
            f"📊 原始长度：{record.get('char_count', 0)} 字符",
            f"🏷️ 关键词：{', '.join(record.get('keywords', []))}",
            f"🛡️ 语义闸：{record.get('gate_decision', '-')}",
            f"⏰ 创建时间：{record.get('created_at', '-')}",
        ]
        if 含全文:
            lines.append("")
            lines.append("📖 原始全文：")
            lines.append(record.get("fulltext", "")[:3000])
            if len(record.get("fulltext", "")) > 3000:
                lines.append("...（已截断，可通过 DNA 再次还原）")
        return "\n".join(lines)

    def _压缩(self, 文本: str, 用户标识: str) -> Dict[str, Any]:
        result = self.引擎.compress(文本, source="longzhishou", operator=用户标识)
        if not result.get("ok"):
            return {"成功": False, "输出": result.get("message", "压缩失败"), "返回码": -1, "data": result}
        record = result["record"]
        return {
            "成功": True,
            "输出": f"🟢 已压缩\n{self._格式化卡片(record)}\n\n{record.get('card', '')}",
            "返回码": 0,
            "data": {"lu_code": record["lu_code"], "dna": record["dna"]},
        }

    def _还原(self, 句柄: str, 用户标识: str) -> Dict[str, Any]:
        result = self.引擎.recall(句柄, operator=用户标识)
        if not result.get("ok"):
            return {"成功": False, "输出": result.get("message", "还原失败"), "返回码": -1, "data": result}
        record = result["record"]
        lineage = record.get("lineage", [])
        lineage_text = "\n".join(
            f"- `{r.get('timestamp', '-')}` [{r.get('action')}] {r.get('operator')} {r.get('detail', '')}"
            for r in lineage[:10]
        ) or "（无）"
        output = (
            f"🟢 已还原\n{self._格式化卡片(record, 含全文=True)}\n\n"
            f"🔗 操作血缘（最近 {len(lineage)} 条）：\n{lineage_text}"
        )
        return {"成功": True, "输出": output, "返回码": 0, "data": {"lu_code": record["lu_code"], "dna": record["dna"]}}

    def _搜索(self, 查询: str) -> Dict[str, Any]:
        results = self.引擎.search(查询)
        if not results:
            return {"成功": True, "输出": "未找到匹配的 LU 记忆。", "返回码": 0}
        lines = [f"🔍 LU 记忆搜索：{查询}（{len(results)} 条）"]
        for r in results:
            lines.append(
                f"- `{r.get('lu_code')}` · {r.get('title') or r.get('summary')} "
                f"· 关键词：{r.get('keywords', '')}"
            )
        return {"成功": True, "输出": "\n".join(lines), "返回码": 0}

    def _语义搜索(self, 查询: str) -> Dict[str, Any]:
        results = self.引擎.search_semantic(查询)
        if not results:
            return {"成功": True, "输出": "未找到语义相近的 LU 记忆。", "返回码": 0}
        lines = [f"🧠 LU 语义搜索：{查询}（{len(results)} 条）"]
        for r in results:
            lines.append(
                f"- `{r.get('lu_code')}` · {r.get('title') or r.get('summary')} "
                f"· 相似度：{r.get('semantic_score', 0)}"
            )
        return {"成功": True, "输出": "\n".join(lines), "返回码": 0}

    def _列表(self) -> Dict[str, Any]:
        results = self.引擎.list_recent(limit=20)
        if not results:
            return {"成功": True, "输出": "暂无 LU 记忆。", "返回码": 0}
        lines = [f"📚 最近 {len(results)} 条 LU 记忆"]
        for r in results:
            lines.append(
                f"- `{r.get('lu_code')}` · {r.get('title') or r.get('summary')} · {r.get('created_at', '-')[:10]}"
            )
        return {"成功": True, "输出": "\n".join(lines), "返回码": 0}

    def _画廊(self) -> Dict[str, Any]:
        try:
            import longhun_lu_gallery
            path = longhun_lu_gallery.generate()
            return {"成功": True, "输出": f"🖼️ LU 记忆画廊已生成\n本地路径：`{path}`\n浏览器打开：file://{path}", "返回码": 0}
        except Exception as e:
            return {"成功": False, "输出": f"🔴 画廊生成失败：{e}", "返回码": -1}

    def _统计(self) -> Dict[str, Any]:
        stats = self.引擎.stats()
        output = (
            f"🗜️ LU 认知压缩统计\n"
            f"- 总记录数：{stats.get('total_records')}\n"
            f"- 活跃记录：{stats.get('active_records')}\n"
            f"- 累计字符：{stats.get('total_chars'):,}\n"
            f"- 血缘事件：{stats.get('lineage_events')}\n"
            f"- 数据库：{stats.get('db_path')}"
        )
        return {"成功": True, "输出": output, "返回码": 0}


class CollectiveWisdomCommandHandler:
    """把 龍魂集思广益引擎 桥接到飛書本地控制接口"""

    def __init__(self, 注册表: 授权注册表):
        self.注册表 = 注册表
        self.引擎 = CollectiveWisdomEngine() if CollectiveWisdomEngine else None

    def 执行(self, 解析结果: Dict[str, Any], 等级: int, 原始等级: str, 用户标识: str) -> Dict[str, Any]:
        if not self.引擎:
            return {"成功": False, "输出": "🔴 集思广益引擎未加载", "返回码": -1}

        命令 = 解析结果["命令"]
        参数 = 解析结果.get("参数", "")

        if 解析结果.get("类型") == "错误":
            return {"成功": False, "输出": f"🔴 {解析结果.get('原因', '格式错误')}", "返回码": -1}

        try:
            if 命令 == "提意见":
                return self._提意见(参数, 用户标识, 原始等级)
            if 命令 == "意见列表":
                return self._意见列表()
            if 命令 == "置顶意见":
                return self._置顶意见()
            if 命令 == "验证意见":
                return self._验证意见(参数, 用户标识)
            if 命令 == "采纳意见":
                return self._设置状态(参数, "adopted", 用户标识)
            if 命令 == "拒绝意见":
                return self._设置状态(参数, "rejected", 用户标识)
            if 命令 == "忽略意见":
                return self._设置状态(参数, "ignored", 用户标识)
        except Exception as e:
            return {"成功": False, "输出": f"🔴 集思广益引擎执行错误：{e}", "返回码": -1}

        return {"成功": False, "输出": "🔴 未知集思广益命令", "返回码": -1}

    def _格式化(self, record: Dict[str, Any], 含详情: bool = False) -> str:
        lines = [
            f"💡 意见码：`{record.get('idea_code')}`",
            f"🧬 DNA：`{record.get('dna')}`",
            f"📝 内容：{record.get('content')}",
            f"👤 提交人：{record.get('submitter')}（{record.get('level')}）",
            f"📊 权重：{record.get('weight', 0):.2f} · 提及 {record.get('mention_count', 0)} 次 · 验证 {record.get('verified_count', 0)} 次",
            f"🏷️ 状态：{record.get('status')}",
            f"🛡️ 语义闸：{record.get('gate_decision', '-')}",
            f"🔗 LU 短码：`{record.get('lu_code', '-')}`",
        ]
        if 含详情:
            lineage = record.get("lineage", [])
            if lineage:
                lines.append("\n📜 血缘：")
                for r in lineage[:10]:
                    lines.append(f"- `{r.get('timestamp', '-')}` [{r.get('action')}] {r.get('operator')}")
        return "\n".join(lines)

    def _提意见(self, 内容: str, 用户标识: str, 原始等级: str) -> Dict[str, Any]:
        result = self.引擎.submit(内容, submitter=用户标识, level=原始等级, source="longzhishou")
        if not result.get("ok"):
            return {"成功": False, "输出": result.get("message", "提交失败"), "返回码": -1, "data": result}
        record = result["record"]
        return {
            "成功": True,
            "输出": f"🟢 {result['message']}\n{self._格式化(record)}",
            "返回码": 0,
            "data": {"idea_code": record["idea_code"], "dna": record["dna"]},
        }

    def _意见列表(self) -> Dict[str, Any]:
        results = self.引擎.list_ideas(limit=20)
        if not results:
            return {"成功": True, "输出": "暂无已归档的意见。", "返回码": 0}
        lines = [f"💡 最近 {len(results)} 条意见（按权重排序）"]
        for r in results:
            lines.append(
                f"- `{r.get('idea_code')}` · 权重 {r.get('weight', 0):.2f} · "
                f"{r.get('content', '')[:60]}{'...' if len(r.get('content', '')) > 60 else ''}"
            )
        return {"成功": True, "输出": "\n".join(lines), "返回码": 0}

    def _置顶意见(self) -> Dict[str, Any]:
        results = self.引擎.top_ideas(limit=10)
        if not results:
            return {"成功": True, "输出": "暂无浮出的置顶意见。", "返回码": 0}
        lines = [f"🔝 系统按权重浮出的 {len(results)} 条意见"]
        for r in results:
            lines.append(
                f"- `{r.get('idea_code')}` · 权重 {r.get('weight', 0):.2f} · 提及 {r.get('mention_count', 0)} · "
                f"{r.get('content', '')[:60]}{'...' if len(r.get('content', '')) > 60 else ''}"
            )
        return {"成功": True, "输出": "\n".join(lines), "返回码": 0}

    def _验证意见(self, 意见码: str, 用户标识: str) -> Dict[str, Any]:
        result = self.引擎.verify(意见码.strip(), operator=用户标识)
        if not result.get("ok"):
            return {"成功": False, "输出": result.get("message", "验证失败"), "返回码": -1, "data": result}
        record = result["record"]
        return {"成功": True, "输出": f"🟢 {result['message']}\n{self._格式化(record, 含详情=True)}", "返回码": 0}

    def _设置状态(self, 意见码: str, 状态: str, 用户标识: str) -> Dict[str, Any]:
        result = self.引擎.set_status(意见码.strip(), 状态, operator=用户标识)
        if not result.get("ok"):
            return {"成功": False, "输出": result.get("message", "状态更新失败"), "返回码": -1, "data": result}
        record = result["record"]
        return {"成功": True, "输出": f"🟢 {result['message']}\n{self._格式化(record, 含详情=True)}", "返回码": 0}


class ToolsetCommandHandler:
    """把 龍魂自适应工具集生态引擎 桥接到飛書本地控制接口"""

    def __init__(self, 注册表: 授权注册表):
        self.注册表 = 注册表
        self.引擎 = ToolsetEcosystemEngine() if ToolsetEcosystemEngine else None

    def 执行(self, 解析结果: Dict[str, Any], 等级: int, 原始等级: str, 用户标识: str) -> Dict[str, Any]:
        if not self.引擎:
            return {"成功": False, "输出": "🔴 工具集生态引擎未加载", "返回码": -1}

        命令 = 解析结果["命令"]
        参数 = 解析结果.get("参数", "")

        if 解析结果.get("类型") == "错误":
            return {"成功": False, "输出": f"🔴 {解析结果.get('原因', '格式错误')}", "返回码": -1}

        try:
            if 命令 == "反馈":
                return self._反馈(参数, 用户标识, 原始等级)
            if 命令 == "功能统计":
                return self._统计()
            if 命令 == "公开意见包":
                return self._公开包()
        except Exception as e:
            return {"成功": False, "输出": f"🔴 工具集生态引擎执行错误：{e}", "返回码": -1}

        return {"成功": False, "输出": "🔴 未知工具集命令", "返回码": -1}

    def _反馈(self, 参数: Dict[str, Any], 用户标识: str, 原始等级: str) -> Dict[str, Any]:
        function_id = 参数.get("function", "")
        content = 参数.get("content", "")
        if not function_id or not content:
            return {"成功": False, "输出": "🔴 格式错误：反馈 <功能ID/名称> <内容>", "返回码": -1}
        result = self.引擎.submit_feedback(用户标识, function_id, content, level=原始等级)
        if not result.get("ok"):
            return {"成功": False, "输出": result.get("message", "反馈提交失败"), "返回码": -1, "data": result}
        record = result["record"]
        return {
            "成功": True,
            "输出": (
                f"🟢 反馈已提交，自动关联 DNA\n"
                f"意见码：`{record.get('idea_code')}`\n"
                f"DNA：`{record.get('dna')}`\n"
                f"功能：{function_id}\n"
                f"内容：{content}"
            ),
            "返回码": 0,
            "data": {"idea_code": record.get("idea_code"), "dna": record.get("dna")},
        }

    def _统计(self) -> Dict[str, Any]:
        stats = self.引擎.stats()
        output = (
            f"🧰 工具集生态统计\n"
            f"- 功能模块：{stats['functions']['total']}（活跃 {stats['functions']['active']}，待上架 {stats['functions']['pending']}）\n"
            f"- 真实使用事件：{stats['usage_events']}\n"
            f"- 主动提醒：{stats['reminders']}\n"
            f"- 公开意见包：{stats['public_packages']}\n"
            f"- 数据库：{stats['db_path']}"
        )
        return {"成功": True, "输出": output, "返回码": 0}

    def _公开包(self) -> Dict[str, Any]:
        result = self.引擎.generate_public_package()
        if not result.get("ok"):
            return {"成功": False, "输出": result.get("message", "公开意见包生成失败"), "返回码": -1, "data": result}
        return {
            "成功": True,
            "输出": (
                f"🟢 公开意见包已生成\n"
                f"包 ID：`{result['package_id']}`\n"
                f"DNA：`{result['dna']}`\n"
                f"收录意见数：{result['idea_count']}\n"
                f"文件路径：`{result['public_path']}`"
            ),
            "返回码": 0,
            "data": result,
        }


# ============ 5. 审计日志 ============
class 审计日志:
    """所有操作记录，只追加"""

    def __init__(self, 配置: 主权配置):
        self.配置 = 配置
        self.路径 = Path(配置.日志路径)
        self.路径.parent.mkdir(parents=True, exist_ok=True)

    def 记录(self, 用户: str, 等级: int, 原始消息: str, 解析结果: Dict, 执行结果: Dict):
        条目 = {
            "时间": datetime.now(timezone.utc).isoformat(),
            "用户": 用户,
            "有效等级": f"L{等级}",
            "原始消息": 原始消息,
            "解析命令": 解析结果.get("命令", "未知"),
            "执行结果": "成功" if 执行结果.get("成功") else "失败",
            "输出摘要": 执行结果.get("输出", "")[:200],
            "脱氧核糖核酸": self.配置.脱氧核糖核酸锚定,
        }
        with open(self.路径, "a", encoding="utf-8") as 文件:
            文件.write(json.dumps(条目, ensure_ascii=False) + "\n")


# ============ 6. 飞书消息处理器 ============
class 飞书消息处理器:
    """处理飞书机器人消息"""

    def __init__(self):
        self.配置 = 主权配置()
        self.注册表 = 授权注册表(self.配置)
        self.验证器 = 主权验证器(self.配置, self.注册表)
        self.解析器 = 命令解析器(self.配置)
        self.引擎 = 执行引擎(self.配置, self.注册表)
        self.日志 = 审计日志(self.配置)
        self._语义匹配器 = SovereigntyPatternMatcher() if SovereigntyPatternMatcher else None

    def 处理(self, 飞书消息: Dict[str, Any]) -> Dict[str, Any]:
        用户标识 = 飞书消息.get("user_id", "未知")
        消息内容 = 飞书消息.get("text", "")
        消息脱氧核糖核酸 = 飞书消息.get("dna", "")

        # 1. 主权验证
        验证结果 = self.验证器.验证(用户标识, 消息脱氧核糖核酸)
        if not 验证结果["通过"]:
            return {
                "code": 403,
                "message": f"🔴 {验证结果['原因']}，操作{验证结果['操作']}",
                "data": None,
            }

        # 1.5 語義歸一化與繞過檢測（多語言、拆分、口語化統一攔截）
        if self._语义匹配器:
            reject_matches = [m for m in self._语义匹配器.match(消息内容) if m.get("action") == "reject"]
            bypass_attempts = self._语义匹配器.detect_bypass(消息内容)
            if reject_matches or bypass_attempts:
                return {
                    "code": 403,
                    "message": "🔴 语义主权熔断：检测到规则违反或绕过企图",
                    "data": {
                        "matches": reject_matches,
                        "bypass_attempts": bypass_attempts,
                    },
                }

        等级 = 验证结果.get("等级", 0)
        原始等级 = 验证结果.get("原始等级", "L0")
        已认证 = 验证结果.get("已认证", False)

        # 2. 解析命令
        解析结果 = self.解析器.解析(消息内容)

        # 2.5 L1 及以上真实命令必须带 DNA，不能只靠 user_id
        if 解析结果["类型"] != "对话" and 等级 >= 1 and not 消息脱氧核糖核酸:
            self.日志.记录(
                用户标识,
                等级,
                消息内容,
                解析结果,
                {"成功": False, "输出": "🔴 L1+ 命令必须携带 DNA 锚定", "返回码": -1},
            )
            return {
                "code": 403,
                "message": "🔴 L1 及以上命令必须携带 DNA 锚定",
                "data": {"命令": 解析结果.get("命令", "未知"), "等级": f"L{等级}"},
            }

        # 3. 执行或对话
        if 解析结果["类型"] == "对话":
            执行结果 = {"成功": True, "输出": self._对话回复(消息内容, 等级, 已认证), "返回码": 0}
        else:
            执行结果 = self.引擎.执行(解析结果, 等级, 原始等级, 用户标识, 消息内容)

        # 4. 工具集生态：记录命令使用并触发主动提醒（仅非对话命令）
        if 解析结果["类型"] != "对话" and 执行结果.get("成功"):
            提醒文本 = self.引擎.工具集使用反馈(解析结果, 用户标识)
            if 提醒文本:
                执行结果["输出"] += 提醒文本

        # 5. 记录审计
        self.日志.记录(用户标识, 等级, 消息内容, 解析结果, 执行结果)

        return {
            "code": 200 if 执行结果["成功"] else 500,
            "message": "执行成功" if 执行结果["成功"] else "执行失败",
            "data": {
                "命令": 解析结果.get("命令", "对话"),
                "等级": f"L{等级}",
                "已认证": 已认证,
                "输出": 执行结果["输出"],
                "时间": datetime.now(timezone.utc).isoformat(),
            },
        }

    def _对话回复(self, 消息: str, 等级: int, 已认证: bool) -> str:
        消息 = 消息.lower()
        认证状态 = "已认证" if 已认证 else "未认证（L0 只读）"
        if "你好" in 消息 or "在吗" in 消息:
            return f"🐉 龍智守在线。当前有效等级 L{等级}（{认证状态}），有什么吩咐？"
        if "帮助" in 消息 or "怎么用" in 消息:
            return self._帮助文本()
        if "状态" in 消息:
            return self._系统状态()
        return "🐉 收到。如需执行命令，请说'帮助'查看可用指令。"

    def _帮助文本(self) -> str:
        return """🐉 龍智守 · 授权等级指令 v2.0

👑 L3 创始人：
  授权 <用户ID> <L0/L1/L2/L2-SP/L3> [姓名]
  撤销 <用户ID>
  授权列表
  标记中国标准 <用户ID>
  登记DNA <DNA> [生物锚哈希] [设备指纹] [所有者]
  继承DNA <旧DNA> <新DNA> [生物锚哈希] [设备指纹] [所有者]
  实名认证 <用户open_id> [姓名]  → 把已登记用户升级为正式 DNA（L1）

🪪 任意用户（L0 也可）：
  登记 [姓名]              → 生成唯一 UID + DNA，默认未实名（L0）
  注册 / 我是新人 / 生成DNA / 生成UID

🧬 L2 / L2-SP / L3 可登记贡献（不可变现/消费）：
  贡献登记 <DNA> <类别> <描述> [值]

📊 任意等级可查询：
  贡献查询 <DNA>
  DNA状态 <DNA>

🔧 L2 / L2-SP / L3 可生成敏感操作确认码：
  确认码 <操作>

📖 L0 旁观者（未认证用户也强制为 L0）：
  系统状态 / 状态 / 查看流场 / 查看颜色 / 查看生态 / 帮助

🔧 L1 操作员（L0 + 普通命令，可授权 L0/L1）：
  查看文件 [路径]      列出目录 [路径]
  内存 / 磁盘 / 网络检测 [IP]
  打开应用 / 关闭应用
  运行护盾自检

⚠️ L2 管理员（L1 + 敏感命令需确认码，可授权 L0/L1/L2）：
  删除 [路径]          备份数据

🛡️ L2-SP 特殊部门（同 L2，但禁止系统控制/生化军事类）：
  禁止：运行脚本、修改系统、关机、重启系统、格式化、重启服务、生化模拟、武器计算

🌐 中国标准认证：
  所有新授权用户默认待认证，仅 L3 可执行「标记中国标准 <用户ID>」后正式生效。

🗜️ LU 认知压缩（L1 及以上）：
  # 精确指令（L1/L2 执行者）
  压缩 <长文本>          → LU 短码 + DNA + 认知卡片
  还原 <LU短码 或 DNA>   → 原始全文 + 血缘
  LU搜索 <关键词>        → FTS5 关键词检索
  LU语义搜索 <查询句>    → TF-IDF 语义相似度检索
  LU画廊                 → 生成本地 HTML 卡片画廊
  LU列表                 → 最近 20 条
  LU统计                 → 压缩统计

  # 老百姓自然语义（意图路由，无需背指令）
  "记住 / 存一下 / 帮我存 / 记下来 / 压起来" → 压缩
  "找回来 / 调出来 / 给我看看 / 恢复一下"     → 还原
  "搜一下 / 找找看 / 查一下"                  → LU搜索
  "画廊 / 卡片墙 / 看看卡片"                  → LU画廊
  "提意见 / 我建议 / 我有个想法 / 吐槽一下"    → 集思广益提交

💡 集思广益（L0 可提，L2 可验证，L3 可决策）：
  提意见 <内容>              → 归档，自动计算权重
  意见列表                   → 按权重排序
  置顶意见                   → 系统浮出的高权重意见
  验证意见 <意见码>          → L2+ 标记可验证改进
  采纳意见 / 拒绝意见 / 忽略意见 <意见码>  → L3 决策

🧰 自适应工具集生态：
  功能统计                   → 功能模块分数与状态
  公开意见包                 → 生成脱敏公开意见包
  反馈 <功能ID> <内容>       → 一键 DNA 反馈

📢 飞书消息推送（L1 及以上）：
  发送测试消息 [内容]        → 向飞书群推一条测试消息
  发送评估报告               → 推送最新的统一评估报告到飞书群

🚀 训练数据优化（L1 及以上）：
  跑训练优化 / 跑训练数据优化 → 执行龍魂训练数据优化器 v3.2.0 并推送报告

🔐 国密配置保护（CLI 专用）：
  加密配置                   → 用 SM4 加密 ~/.longhun/config/龍智守_config.json 中的敏感项
  解密依赖：LONGHUN_MASTER_KEY 环境变量 或 ~/.longhun/config/.master_key

🛡️ 内容主权审查（L1 及以上）：
  审查内容 <文本>            → 公开前按 CNSH 内容主权协议审查，输出风险报告
  发送评估报告               → 自动附带主权审查摘要

  每次使用命令后，如果系统判断你接触了新功能/新用法，
  会自动弹出提醒："反馈 <功能ID> <你的想法>"，无需填表。

示例：
  授权 user1 L1 张三
  标记中国标准 user1
  删除 /tmp/test 确认码 123456
  压缩 这里是我想记住的长内容...
  还原 /LU-260630-主题-ABCD

DNA: #龍芯⚡️UID9622"""

    def _系统状态(self) -> str:
        try:
            结果 = subprocess.run("uptime", shell=True, capture_output=True, text=True, timeout=5)
            负载 = 结果.stdout.strip()
            结果 = subprocess.run("df -h / | tail -1", shell=True, capture_output=True, text=True, timeout=5)
            磁盘 = 结果.stdout.strip()
            用户数 = len(self.注册表._数据.get("users", {}))
            已认证数 = sum(1 for u in self.注册表._数据.get("users", {}).values() if u.get("is_china_standard"))
            return f"🐉 系统状态\n负载: {负载}\n磁盘: {磁盘}\n龍智守: 在线 | 授权用户: {用户数}（已认证 {已认证数}）\nDNA: 完整"
        except:
            return "🐉 系统状态获取失败，请检查权限。"


# ============ 7. HTTP 服务入口 ============
def 创建服务():
    """创建本地HTTP服务，接收飞书回调"""
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        print("❌ 请先安装 Flask: pip3 install flask")
        sys.exit(1)

    应用 = Flask(__name__)
    处理器 = 飞书消息处理器()
    安全 = 安全防护层(处理器.配置)
    限流 = 请求频率限制器(处理器.配置)

    def _审计记录(事件: str, 详情: Dict[str, Any]) -> None:
        try:
            处理器.日志.记录(
                用户标识="系统",
                等级=0,
                消息内容=f"[安全防护] {事件}",
                解析结果={"命令": 事件, "类型": "security"},
                执行结果={"成功": True, "输出": json.dumps(详情, ensure_ascii=False), "返回码": 0},
            )
        except Exception:
            pass

    def _发送安全告警(事件: str, 详情: Dict[str, Any]) -> None:
        """把安全事件推送到飞书群，让老大第一时间知道有人搞事。"""
        try:
            发送器 = 飞书消息发送器()
            文本 = (
                f"🚨 龍智守安全告警\n"
                f"事件：{事件}\n"
                f"来源 IP：{详情.get('ip', '未知')}\n"
                f"路径：{详情.get('path', '-')}"
            )
            发送器.发送文本(文本)
        except Exception:
            # 告警发送失败不影响主流程，但会错过实时通知
            pass

    @应用.before_request
    def _请求前检查():
        remote_addr = request.remote_addr or "未知"
        if 限流.已封锁(remote_addr):
            return jsonify({"code": 403, "message": "🔴 IP 已被临时封锁", "data": None}), 403

    @应用.route("/", methods=["GET"])
    def 首页():
        return f"🐉 龍智守 · 本地控制接口 {处理器.配置.版本} 已启动<br>DNA: {处理器.配置.脱氧核糖核酸锚定}"

    @应用.route("/webhook", methods=["POST"])
    def 飞书回调():
        remote_addr = request.remote_addr or "未知"

        # IP 白名单检查
        if not 安全.IP允许(remote_addr):
            _审计记录("IP白名单拒绝", {"ip": remote_addr, "path": "/webhook"})
            return jsonify({"code": 403, "message": "🔴 IP 不在白名单", "data": None}), 403

        raw_body = request.get_data(as_text=True)
        try:
            数据 = json.loads(raw_body) if raw_body else {}
        except Exception:
            数据 = {}

        # 1. URL 验证：飞书配置回调地址时先发一个 challenge，必须原样返回
        challenge = 数据.get("challenge")
        if challenge:
            return jsonify({"challenge": challenge})

        # 2. 事件订阅安全校验（token + 签名）
        if getattr(处理器.配置, "入站签名校验", True):
            header = 数据.get("header", {})
            token = header.get("token", "")
            signature = request.headers.get("X-Lark-Signature", "")
            timestamp = request.headers.get("X-Lark-Request-Timestamp", "")
            nonce = request.headers.get("X-Lark-Request-Nonce", "")

            has_token = bool(getattr(处理器.配置, "飞书VerificationToken", ""))
            has_key = bool(getattr(处理器.配置, "飞书EncryptKey", ""))

            if has_token and not 安全.验证飞书事件令牌(token):
                限流.记录(remote_addr, "sign_fail")
                return jsonify({"code": 403, "message": "🔴 飞书事件 token 校验失败", "data": None}), 403
            if has_key and not 安全.验证飞书事件签名(timestamp, nonce, raw_body.encode("utf-8"), signature):
                限流.记录(remote_addr, "sign_fail")
                return jsonify({"code": 403, "message": "🔴 飞书事件签名校验失败", "data": None}), 403
            if not has_token and not has_key:
                # 未配置凭据时只记录，不阻断，方便本地调测
                _审计记录("未配置事件校验凭据", {"ip": remote_addr, "path": "/webhook"})

        # 3. 解析事件消息
        event = 数据.get("event", {})
        message = event.get("message", {})
        sender = event.get("sender", message.get("sender", {}))
        chat_id = message.get("chat_id", "")
        chat_type = message.get("chat_type", "")

        # 消息内容：text 类型里是 JSON 字符串，如 {"text":"@_user xxx 跑训练优化"}
        content_raw = message.get("content", "{}")
        try:
            content_obj = json.loads(content_raw) if isinstance(content_raw, str) else content_raw
        except Exception:
            content_obj = {}
        text = str(content_obj.get("text", "")).strip()
        # 去掉 @机器人的标记
        text = re.sub(r"@[\w\-]+\s*", "", text).strip()

        user_id = "未知"
        sender_id = sender.get("sender_id", {})
        for key in ("user_id", "open_id", "union_id"):
            if sender_id.get(key):
                user_id = sender_id[key]
                break

        飞书消息 = {
            "user_id": user_id,
            "text": text,
            "chat_id": chat_id,
            "chat_type": chat_type,
            "dna": "",
            "ip": remote_addr,
        }
        结果 = 处理器.处理(飞书消息)

        # 4. 把执行结果回复到聊天窗口（异步/耗时命令已经自己推 webhook）
        输出 = ""
        if isinstance(结果, dict):
            data = 结果.get("data")
            if isinstance(data, dict):
                输出 = data.get("输出", "")
            elif 结果.get("message"):
                输出 = 结果["message"]
        # 未授权用户顺便告诉对方自己的飞书 Open ID，方便创始人授权
        if 输出 and ("权限不足" in 输出 or "L0" in 输出):
            输出 += f"\n\n你的飞书用户标识： `{user_id}`\n请让创始人用命令授权：\n`授权 {user_id} L3 UID9622`"
        if 输出:
            # 长结果截断，避免超限
            if len(输出) > 1500:
                输出 = 输出[:1500] + "\n...(已截断)"
            try:
                飞书 = 飞书消息发送器()
                飞书.发送事件回复(chat_id, 输出)
            except Exception:
                pass

        return jsonify({"code": 0, "message": "ok"})

    @应用.route("/status", methods=["GET"])
    def 状态():
        return jsonify({
            "状态": "在线",
            "服务": "龍智守本地控制接口",
            "版本": 处理器.配置.版本,
            "脱氧核糖核酸": 处理器.配置.脱氧核糖核酸锚定,
            "创始人": 处理器.配置.创始人标识,
            "授权用户数": len(处理器.注册表._数据.get("users", {})),
        })

    # 蜜罐层：看起来像核心入口，实则只记录+返回假数据
    if getattr(处理器.配置, "启用蜜罐层", True):
        @应用.route("/<path:path>", methods=["GET", "POST"])
        def 蜜罐入口(path):
            path = "/" + path
            if not 安全.是蜜罐路径(path):
                return jsonify({"code": 404, "message": "Not Found", "data": None}), 404
            remote_addr = request.remote_addr or "未知"
            限流.记录(remote_addr, "honeypot")
            详情 = {"ip": remote_addr, "path": path, "method": request.method, "count": 限流.计数(remote_addr, "honeypot")}
            _审计记录("蜜罐触发", 详情)
            # 蜜罐触发即告警（阈值默认 1）
            if 限流.应告警(remote_addr, "honeypot", getattr(处理器.配置, "蜜罐触发告警阈值", 1), getattr(处理器.配置, "告警冷却秒数", 300)):
                _发送安全告警("蜜罐被触发", 详情)
            # 多次触发直接封锁
            if 限流.计数(remote_addr, "honeypot") >= getattr(处理器.配置, "IP封锁阈值", 5):
                限流.封锁(remote_addr)
                _发送安全告警("IP 已被临时封锁", {"ip": remote_addr, "reason": "蜜罐触发超限"})
            return jsonify({"code": 200, "message": "decoy", "data": 安全.蜜罐响应(path)})

    return 应用


# ============ 8. 命令行测试入口 ============
def 命令行测试():
    """本地测试，不启动HTTP服务"""
    处理器 = 飞书消息处理器()

    print(f"🐉 龍智守 · 本地控制接口测试模式 {处理器.配置.版本}")
    print(f"DNA: {处理器.配置.脱氧核糖核酸锚定}")
    print("输入命令测试，或输入 '退出' 结束\n")

    while True:
        输入 = input("[UID9622] > ").strip()
        if 输入.lower() in ["退出", "exit", "quit"]:
            break

        飞书消息 = {
            "user_id": "UID9622",
            "text": 输入,
            "dna": 处理器.配置.脱氧核糖核酸锚定,
        }

        结果 = 处理器.处理(飞书消息)
        print(f"\n状态: {结果['message']}")
        if 结果.get("data"):
            print(f"输出:\n{结果['data']['输出']}")
        print("-" * 40)


# ============ 9. 启动入口 ============
def _命令行执行(命令文本: str) -> None:
    """不启动 HTTP，直接以 UID9622 身份执行一条命令。"""
    处理器 = 飞书消息处理器()
    飞书消息 = {
        "user_id": 处理器.配置.创始人标识,
        "text": 命令文本,
        "dna": 处理器.配置.脱氧核糖核酸锚定,
    }
    结果 = 处理器.处理(飞书消息)
    print(f"状态: {结果['message']}")
    if 结果.get("data"):
        print(结果["data"]["输出"])
    sys.exit(0 if 结果["code"] == 200 else 1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        命令行测试()
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == "加密配置":
        BotConfig.加密敏感项()
        sys.exit(0)

    # 支持命令行直接调用：python3 龍智守_本地控制接口_v2.0.py 发送测试消息 "内容"
    if len(sys.argv) > 1 and sys.argv[1] in (
        "发送测试消息", "发送评估报告", "审查内容",
        "跑训练优化", "跑训练数据优化",
        "登记", "登记身份", "实名认证",
    ):
        命令 = sys.argv[1]
        参数 = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if 参数:
            _命令行执行(f"{命令} {参数}")
        else:
            _命令行执行(命令)

    # 默认启动 HTTP 服务，只监听 127.0.0.1，避免直接暴露到公网
    print("🐉 启动龍智守本地控制接口...")
    print(f"DNA: {主权配置.脱氧核糖核酸锚定}")
    print("访问: http://127.0.0.1:5000")
    print("飞书回调: POST http://127.0.0.1:5000/webhook")
    print("状态检查: GET http://127.0.0.1:5000/status")
    print("提示: 如需外网访问，请用 Nginx/HTTPS 反向代理，不要直接监听 0.0.0.0\n")

    应用 = 创建服务()
    应用.run(host="127.0.0.1", port=5000, debug=False)


# ============ selftest() 自检函数 ============
def selftest() -> dict:
    """
    自检函数：验证核心模块是否正常加载。
    DNA: #龍芯⚡️2026-07-01-LONGZHISHOU-SELFTEST-v2.0
    """
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dna": "#龍芯⚡️2026-07-01-LONGZHISHOU-SELFTEST-v2.0",
        "tests": {},
    }
    try:
        cfg = 主权配置()
        results["tests"]["主权配置"] = {"pass": True, "msg": f"版本={cfg.版本}"}
    except Exception as e:
        results["tests"]["主权配置"] = {"pass": False, "msg": str(e)}
    try:
        cfg = 主权配置()
        reg = 授权注册表(cfg)
        等级, 等级名, 认证 = reg.获取有效等级("UID9622")
        results["tests"]["授权注册表"] = {"pass": True, "msg": f"创始人等级={等级名}"}
    except Exception as e:
        results["tests"]["授权注册表"] = {"pass": False, "msg": str(e)}
    try:
        cfg = 主权配置()
        reg = 授权注册表(cfg)
        verifier = 主权验证器(cfg, reg)
        result = verifier.验证("UID9622", cfg.脱氧核糖核酸锚定)
        results["tests"]["主权验证器"] = {"pass": result["通过"], "msg": result["原因"]}
    except Exception as e:
        results["tests"]["主权验证器"] = {"pass": False, "msg": str(e)}
    try:
        cfg = 主权配置()
        parser = 命令解析器(cfg)
        parsed = parser.解析("帮助")
        results["tests"]["命令解析器"] = {"pass": parsed["命令"] == "帮助", "msg": f"解析结果={parsed['命令']}"}
    except Exception as e:
        results["tests"]["命令解析器"] = {"pass": False, "msg": str(e)}
    all_pass = all(t.get("pass", False) for t in results["tests"].values())
    results["overall"] = "PASS" if all_pass else "FAIL"
    return results


if __name__ == "__main__" and "--selftest" in sys.argv:
    import json as _json
    print(_json.dumps(selftest(), ensure_ascii=False, indent=2))
    sys.exit(0)
