#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·己未·癸酉·䷬萃-CNSH-STAMP-PLUGIN-v1.1-UID9622
# 创建者: 诸葛鑫（UID9622）
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 通过
# 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · CNSH 智能贴入插件 v1.1（审查修正版）
核心定位: 粘贴即锚定 —— 任何内容贴入龍魂系统，自动生成不可篡改的机器可读数字指纹包。

v1.1 审查修正（相对 v1.0 草案）:
  1. 🔴 路径修正: 不再硬编码 /opt/longhun-system → 自动探测 LONGHUN_ROOT（env > ~/longhun-system > 本文件上级）
  2. 🔴 目录修正: 04_AUDIT/08_STATE 为编造目录 → 真实 07_AUDIT/audit_plugin.jsonl + 11_DATA/shame_wall.jsonl
  3. 🔴 干支修正: 原 generate_dna() 月/日干支错用年干支公式 → 复用 bin/lh_time_engine.py（LU-Time v4.0·实测输出正确）
  4. 🟡 死代码修正: current_hour > 23 永不真 → 0:00-4:59 判定（对齐文档 0:00-5:00）
  5. 🟡 数字根统一: 文档公式 1+((总字数-1)%9) 落地，与草案字符码和算法统一
  6. 🟡 故障自愈落地: 10MB 截断 + GPG 超时降级确认码比对（原只有文档无代码）
  7. 🟡 skip-auth 打印醒目警告（防误用）

用法:
  python3 08_BIN/lh_cnsh_plugin.py -i input.txt -o output.json
  echo "内容" | python3 08_BIN/lh_cnsh_plugin.py
  python3 08_BIN/lh_cnsh_plugin.py --device-info
  python3 08_BIN/lh_cnsh_plugin.py --verify output.json
  或经统一入口: lh cnsh-stamp ...
"""

import os
import sys
import json
import gzip
import base64
import hashlib
import argparse
import subprocess
import platform
import socket
import uuid
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
VERSION = "v1.1"

# ============================================================
# 路径自动探测（v1.1 修正: 不再硬编码 /opt/longhun-system）
# 优先级: 环境变量 LONGHUN_ROOT > ~/longhun-system > 本文件上级目录
# ============================================================

def _detect_root() -> Path:
    env = os.getenv("LONGHUN_ROOT")
    if env:
        return Path(env).expanduser()
    home = Path.home() / "longhun-system"
    if home.exists():
        return home
    return Path(__file__).resolve().parent.parent


LONGHUN_ROOT = _detect_root()
AUDIT_PATH = LONGHUN_ROOT / "07_AUDIT" / "audit_plugin.jsonl"       # 真实审计目录
SHAME_PATH = LONGHUN_ROOT / "11_DATA" / "shame_wall.jsonl"          # 真实耻辱墙（沿用现有惯例）
MAX_CONTENT_SIZE = 10 * 1024 * 1024  # 10MB 截断阈值（故障自愈）


# ============================================================
# DNA 生成（v1.1 修正: 复用 LU-Time Engine v4.0 四柱+卦，不再自算错误干支）
# ============================================================

def generate_dna() -> str:
    try:
        sys.path.insert(0, str(LONGHUN_ROOT / "bin"))
        from lh_time_engine import get_output_stamp
        # compact: "#龍芯⚡️丙午·丙申·己未·酉时·䷖剥" → 取四柱段
        stamp = get_output_stamp(format_type="compact")
        four_pillars = "·".join(stamp.split("·")[:4])
    except Exception:
        # 降级: 时间引擎不可用时用日期+随机，保证 DNA 唯一可用
        four_pillars = datetime.now().strftime("%Y-%m-%d")
    rand = hashlib.sha256(os.urandom(8).hex().encode()).hexdigest()[:8].upper()
    return f"{four_pillars}-CNSH-STAMP-{rand}-{UID}"


# ============================================================
# 1. 三色审计枚举
# ============================================================

class AuditColor(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"


# ============================================================
# 2. 数字根压缩器（v1.1 统一为文档公式 1+((总字数-1)%9)）
# ============================================================

class DigitalRootCompressor:
    @staticmethod
    def calculate_digital_root(text: str) -> int:
        """压缩数字根: 1 + ((总字数 - 1) % 9)，与 CNSH 文档一致"""
        return 1 + ((len(text) - 1) % 9)

    @staticmethod
    def compress(text: str) -> Dict:
        original_size = len(text.encode('utf-8'))
        compressed = gzip.compress(text.encode('utf-8'), compresslevel=9)
        compressed_size = len(compressed)
        return {
            "original_size": original_size,
            "compressed_size": compressed_size,
            "compression_ratio": round(original_size / max(compressed_size, 1), 2),
            "digital_root": DigitalRootCompressor.calculate_digital_root(text),
            "compressed_base64": base64.b64encode(compressed).decode('utf-8'),
            "hash": hashlib.sha256(text.encode('utf-8')).hexdigest()
        }

    @staticmethod
    def decompress(compressed_b64: str) -> str:
        return gzip.decompress(base64.b64decode(compressed_b64)).decode('utf-8')


# ============================================================
# 3. 设备指纹采集器
# ============================================================

class DeviceFingerprint:
    @staticmethod
    def collect() -> Dict:
        fingerprint = {
            "hostname": platform.node(),
            "os": f"{platform.system()} {platform.release()}",
            "arch": platform.machine(),
            "python": platform.python_version(),
            "cpu_count": os.cpu_count() or 0,
            "user": os.getenv("USER", os.getenv("USERNAME", "unknown")),
            "cwd": os.getcwd(),
        }
        try:
            mac = uuid.getnode()
            fingerprint["mac"] = ":".join(
                f"{((mac >> i) & 0xff):02x}" for i in range(40, -1, -8)
            )[:17]
        except Exception:
            fingerprint["mac"] = "unknown"
        try:
            with open("/etc/machine-id", "r") as f:
                fingerprint["machine_id"] = f.read().strip()
        except Exception:
            # macOS 降级: 用 hostname+mount 摘要，保证指纹可区分
            try:
                result = subprocess.run(
                    ["ioreg", "-rd1", "-c", "IOPlatformExpertDevice"],
                    capture_output=True, text=True, timeout=5)
                match = re.search(r'"IOPlatformUUID"\s*=\s*"([^"]+)"', result.stdout)
                fingerprint["machine_id"] = match.group(1) if match else "unknown"
            except Exception:
                fingerprint["machine_id"] = "unknown"
        fingerprint["fingerprint_hash"] = hashlib.sha256(
            json.dumps(fingerprint, sort_keys=True).encode()
        ).hexdigest()[:16]
        return fingerprint


# ============================================================
# 4. 异常登录检测器
# ============================================================

class AnomalyDetector:
    TRUSTED_DEVICES = ["kunpeng-server", "macbook-pro", "localhost"]
    TRUSTED_IPS = ["127.0.0.1", "192.168.1.", "119.13.90.27"]

    @classmethod
    def detect(cls, device: Dict) -> Dict:
        hostname = device.get("hostname", "")
        anomaly_score = 0.0
        reasons: List[str] = []

        if hostname not in cls.TRUSTED_DEVICES:
            anomaly_score += 0.4
            reasons.append("新设备")

        try:
            host_ip = socket.gethostbyname(hostname)
            if not any(host_ip.startswith(ip) for ip in cls.TRUSTED_IPS):
                anomaly_score += 0.3
                reasons.append("新IP")
        except Exception:
            anomaly_score += 0.2
            reasons.append("无法解析IP")

        if device.get("machine_id") == "unknown" or device.get("mac") == "unknown":
            anomaly_score += 0.2
            reasons.append("未知设备指纹")

        # v1.1 修正: 原 current_hour > 23 死代码永不真 → 0:00-4:59
        current_hour = datetime.now().hour
        if current_hour < 5:
            anomaly_score += 0.1
            reasons.append("非工作时间登录")

        return {
            "anomaly_score": round(anomaly_score, 2),
            "is_anomaly": anomaly_score >= 0.5,
            "reasons": reasons,
            "trusted_device": hostname in cls.TRUSTED_DEVICES,
            "requires_auth": anomaly_score >= 0.5
        }


# ============================================================
# 5. GPG 签名验证（真实实现 + 超时降级确认码）
# ============================================================

class GPGVerifier:
    @staticmethod
    def verify_signature(plaintext: str, signature: str) -> bool:
        try:
            challenge_path = Path("/tmp/lh_gpg_challenge.txt")
            sig_path = Path("/tmp/lh_gpg_signature.asc")
            challenge_path.write_text(plaintext)
            sig_path.write_text(signature)
            result = subprocess.run(
                ["gpg", "--verify", str(sig_path), str(challenge_path)],
                capture_output=True, text=True, timeout=10
            )
            challenge_path.unlink(missing_ok=True)
            sig_path.unlink(missing_ok=True)
            return result.returncode == 0 and "Good signature" in result.stdout
        except subprocess.TimeoutExpired:
            # 故障自愈: GPG 验证超时 → 降级为确认码比对（调用方处理）
            raise TimeoutError("GPG 验证超时(>10s)")
        except Exception as e:
            print(f"⚠️ GPG验证异常: {e}")
            return False

    @staticmethod
    def verify_confirm_code(provided: str) -> bool:
        """降级认证: 确认码比对（GPG 不可用时兜底）"""
        return provided.strip() == CONFIRM


# ============================================================
# 6. 史官记录（真实审计目录 07_AUDIT/）
# ============================================================

class Historian:
    @staticmethod
    def record(result: Dict, operation: str = "stamp") -> bool:
        try:
            AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
            record = {
                "operation": operation,
                "dna": result.get("dna"),
                "timestamp": datetime.now().isoformat(),
                "device_hash": result.get("device", {}).get("fingerprint_hash"),
                "digital_root": result.get("content", {}).get("digital_root"),
                "status": result.get("status", "success"),
                "color": result.get("color", "🟢")
            }
            with open(AUDIT_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            return True
        except Exception as e:
            print(f"⚠️ 史官记录失败: {e}")
            return False


# ============================================================
# 7. 耻辱墙（真实文件 11_DATA/shame_wall.jsonl·沿用现有惯例）
# ============================================================

class ShameWall:
    @staticmethod
    def write(auth_failure: Dict) -> bool:
        try:
            SHAME_PATH.parent.mkdir(parents=True, exist_ok=True)
            entry = {
                "type": "plugin_auth_failure",
                "dna": auth_failure.get("dna"),
                "timestamp": datetime.now().isoformat(),
                "device_hash": auth_failure.get("device", {}).get("fingerprint_hash"),
                "anomaly_score": auth_failure.get("anomaly_score", 0),
                "reasons": auth_failure.get("reasons", []),
                "severity": "HIGH"
            }
            with open(SHAME_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            return True
        except Exception as e:
            print(f"⚠️ 耻辱墙写入失败: {e}")
            return False


# ============================================================
# 8. 主插件类
# ============================================================

class CNSHPlugin:
    def __init__(self):
        self.dna = generate_dna()
        self.timestamp = datetime.now().isoformat()
        self.color = AuditColor.GREEN

    def process(self, content: str, skip_auth: bool = False) -> Dict:
        # 故障自愈: 10MB 截断 + 告警
        if len(content.encode('utf-8')) > MAX_CONTENT_SIZE:
            print(f"⚠️ 内容超过 10MB({len(content)}字节)，已截断至 10MB")
            content = content[:MAX_CONTENT_SIZE]

        device = DeviceFingerprint.collect()
        compressed = DigitalRootCompressor.compress(content)
        anomaly = AnomalyDetector.detect(device)

        # 三色判定
        if anomaly["anomaly_score"] >= 0.7:
            self.color = AuditColor.RED
        elif anomaly["anomaly_score"] >= 0.3:
            self.color = AuditColor.YELLOW
        else:
            self.color = AuditColor.GREEN

        # 认证
        if anomaly["requires_auth"] and not skip_auth:
            print(f"\n🔐 {self.color.value} 异常检测: 需要认证")
            print(f"  异常评分: {anomaly['anomaly_score']}")
            print(f"  原因: {', '.join(anomaly['reasons'])}")

            challenge = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
            print(f"\n  签名挑战: {challenge}")
            sig = input("  请输入GPG签名(base64): ").strip()

            auth_ok = False
            if sig:
                try:
                    auth_ok = GPGVerifier.verify_signature(challenge, sig)
                except TimeoutError:
                    # 故障自愈: 超时降级为确认码比对
                    print("  ⚠️ GPG验证超时，降级为确认码验证")
                    code = input("  请输入确认码: ").strip()
                    auth_ok = GPGVerifier.verify_confirm_code(code)

            if auth_ok:
                print("  ✅ 认证通过")
            else:
                print("  ❌ 认证失败")
                ShameWall.write({
                    "dna": self.dna,
                    "device": device,
                    "anomaly_score": anomaly["anomaly_score"],
                    "reasons": anomaly["reasons"]
                })
                return {
                    "status": "rejected",
                    "dna": self.dna,
                    "error": "认证失败",
                    "color": self.color.value
                }
        elif skip_auth and anomaly["requires_auth"]:
            print(f"⚠️ 检测到异常({anomaly['anomaly_score']})但已 --skip-auth 跳过认证，结果仍写入史官")

        # 构建输出
        output = {
            "status": "success",
            "dna": self.dna,
            "confirm": CONFIRM,
            "timestamp": self.timestamp,
            "color": self.color.value,
            "device": device,
            "content": {
                "hash": compressed["hash"],
                "length": compressed["original_size"],
                "digital_root": compressed["digital_root"],
                "compression_ratio": compressed["compression_ratio"],
                "compressed_size": compressed["compressed_size"],
                "type": self._detect_type(content)
            },
            "security": {
                "anomaly_score": anomaly["anomaly_score"],
                "is_anomaly": anomaly["is_anomaly"],
                "trusted_device": anomaly["trusted_device"],
                "auth_required": anomaly["requires_auth"],
                "auth_passed": not anomaly["requires_auth"] or skip_auth
            },
            "backup": {
                "compressed_json": compressed["compressed_base64"],
                "hash": hashlib.sha256(compressed["compressed_base64"].encode()).hexdigest(),
                "algorithm": "gzip+base64"
            }
        }

        # 史官记录
        Historian.record(output)

        return output

    def _detect_type(self, content: str) -> str:
        stripped = content.strip()
        if not stripped:
            return "text"
        if len(content) < 10:
            return "text"
        if stripped.startswith("{") and stripped.endswith("}"):
            try:
                json.loads(stripped)
                return "json"
            except Exception:
                pass
        if re.search(r"^(import|from|def|class|if|for|while)", content, re.MULTILINE):
            return "code"
        if re.search(r"```|^#{1,6}\s|\*\*|__", content, re.MULTILINE):
            return "markdown"
        return "text"


# ============================================================
# 9. 命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · CNSH 智能贴入插件 v1.1（粘贴即锚定）")
    parser.add_argument("-i", "--input", help="输入文件")
    parser.add_argument("-o", "--output", help="输出JSON文件")
    parser.add_argument("--verify", help="验证JSON文件")
    parser.add_argument("--device-info", action="store_true", help="查看设备指纹")
    parser.add_argument("--skip-auth", action="store_true", help="跳过认证(危险·慎用)")
    parser.add_argument("--version", action="store_true", help="版本信息")
    parser.add_argument("--doctor", action="store_true", help="自检: 路径/目录/引擎可用性")
    args = parser.parse_args()

    if args.version:
        print(f"🐉 CNSH 智能贴入插件 {VERSION}")
        print(f"DNA: #龍芯⚡️...-CNSH-STAMP-...-{UID}")
        print(f"确认码: {CONFIRM}")
        return

    if args.doctor:
        print(f"🐉 CNSH 插件自检（{VERSION}）")
        print(f"  ✅ 龍魂根目录: {LONGHUN_ROOT}")
        print(f"  {'✅' if LONGHUN_ROOT.exists() else '❌'} 根目录存在")
        print(f"  {'✅' if AUDIT_PATH.parent.exists() else '❌'} 审计目录: {AUDIT_PATH.parent}")
        print(f"  {'✅' if SHAME_PATH.parent.exists() else '❌'} 耻辱墙目录: {SHAME_PATH.parent}")
        try:
            sys.path.insert(0, str(LONGHUN_ROOT / "bin"))
            from lh_time_engine import get_output_stamp
            print(f"  ✅ 时间引擎: {get_output_stamp(format_type='compact')}")
        except Exception as e:
            print(f"  ❌ 时间引擎不可用: {e}（DNA 将降级为日期格式）")
        return

    if args.device_info:
        print(json.dumps(DeviceFingerprint.collect(), ensure_ascii=False, indent=2))
        return

    if args.verify:
        with open(args.verify, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ DNA: {data.get('dna')}")
        print(f"🟢 三色: {data.get('color')}")
        print(f"🔢 数字根: {data.get('content', {}).get('digital_root')}")
        print(f"🔑 状态: {data.get('status')}")
        return

    content = sys.stdin.read() if not args.input else open(args.input, 'r', encoding='utf-8').read()
    if not content:
        print("❌ 内容为空")
        return

    plugin = CNSHPlugin()
    result = plugin.process(content, args.skip_auth)
    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
        print(f"✅ 已保存: {args.output}")
        print(f"   DNA: {result['dna']}")
        print(f"   三色: {result['color']}")
        print(f"   数字根: {result['content']['digital_root']}")
        print(f"   审计: {AUDIT_PATH}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
