#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂跨平台同步专业知识入库脚本
================================
DNA: #龍芯⚡️2026-06-29-ADD-CROSS-PLATFORM-KB-v1.0

1. 向 CS KB SQLite 写入 20+ 张跨平台同步/本地直连/国密加密知识卡片
2. 在 longhun-system/knowledge/cross-platform-sync/ 生成 Markdown 概念文档
3. 调用全局索引服务将新文档编入知识图谱
"""

import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# 路径
HOME = Path.home()
CS_KB_DB = HOME / "longhun-system/backups/cs-kb-enhanced-20260701/cs_kb.db"
KG_DIR = HOME / "longhun-system/knowledge/cross-platform-sync"
GLOBAL_INDEX_SERVICE = HOME / ".longhun/scripts/global_index_service.py"
GLOBAL_INDEX_DB = HOME / ".longhun/global_index/global_index.db"

DNA_PREFIX = "#龍芯⚡️"


def _dna(主题: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    short = hashlib.sha256(f"{主题}:{ts}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-{主题}-{short}"


def _dr(idx: int) -> str:
    # 简单循环赋值，仅作索引用
    drs = [
        "DR=8·木→震宫(东·木)",
        "DR=8·火→离宫(南·火)",
        "DR=8·土→中宫(中·土)",
        "DR=8·金→兑宫(西·金)",
        "DR=8·水→坎宫(北·水)",
    ]
    return drs[idx % len(drs)]


知识卡片清单 = [
    {
        "name": "mDNS/Bonjour 本地服务发现",
        "category": "网络协议",
        "subcategory": "本地直连",
        "description": "零配置网络发现协议。设备在局域网内广播 _longhun-sync._tcp.local. 服务，无需固定 IP、无需外网 DNS，即可被对端自动发现。",
        "context_trigger": "局域网发现、设备自动发现、Bonjour、zeroconf、无需 IP",
        "ipa_abbr": "mDNS",
        "py_example": "from zeroconf import Zeroconf, ServiceBrowser\n# 参见 longhun-cross-platform/scripts/设备发现器.py",
    },
    {
        "name": "WiFi Direct P2P 直连",
        "category": "网络协议",
        "subcategory": "本地直连",
        "description": "设备间直接建立 WiFi P2P 组，无需路由器。理论速率 54Mbps+，适合大文件传输。鸿蒙使用 @ohos.wifiManager.p2p，iOS 使用 NEHotspotConfiguration。",
        "context_trigger": "WiFi Direct、P2P、大文件传输、无路由器",
        "ipa_abbr": "WiFi P2P",
        "py_example": "# 平台原生 API 调用，Python 层通过 TCP over P2P IP 回退\n# 参见 longhun-cross-platform/scripts/传输管理器.py::_连接WiFiDirect",
    },
    {
        "name": "蓝牙 BLE 低功耗传输",
        "category": "网络协议",
        "subcategory": "本地直连",
        "description": "GATT/Notify 机制小数据通道，速率 1-3Mbps，用于密钥交换或备用文本同步。受 MTU 限制需分片重组。",
        "context_trigger": "BLE、蓝牙低功耗、小数据、低功耗、备用通道",
        "ipa_abbr": "BLE",
        "py_example": "# BLE MTU 分片示例\nMTU = 185\nfor i in range(0, len(data), MTU):\n    chunk = data[i:i+MTU]\n    # gatt.write_characteristic(chunk)",
    },
    {
        "name": "局域网 TCP 兜底通道",
        "category": "网络协议",
        "subcategory": "本地直连",
        "description": "当 WiFi Direct / BLE 不可用时，通过同 WiFi 下的标准 socket TCP 直连。数据带 4 字节长度前缀，便于流式解析。",
        "context_trigger": "TCP LAN、局域网、socket、兜底通道",
        "ipa_abbr": "TCP LAN",
        "py_example": "import struct, socket\nsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\nsock.connect(('192.168.1.x', 9622))\nmsg = b'hello'\nsock.sendall(struct.pack('>I', len(msg)) + msg)",
    },
    {
        "name": "RFC1918 本地地址白名单",
        "category": "网络安全",
        "subcategory": "主权网关",
        "description": "龍魂主权网关仅允许目标地址落在 10/8、172.16/12、192.168/16、169.254/16、127/8、fc00::/7、fe80::/10 等本地段，外网传输一律阻断。",
        "context_trigger": "本地地址、RFC1918、Link-local、出境阻断、白名单",
        "ipa_abbr": "RFC1918",
        "py_example": "import ipaddress\ndef is_local(ip):\n    addr = ipaddress.ip_address(ip)\n    return addr.is_private or addr.is_link_local or addr.is_loopback\nprint(is_local('192.168.1.3'), is_local('8.8.8.8'))",
    },
    {
        "name": "ECDH Curve25519 密钥协商",
        "category": "密码学",
        "subcategory": "密钥交换",
        "description": "双方各自生成临时 X25519 密钥对，仅交换公钥即可计算相同共享密钥。私钥永不离设备，每次会话换新密钥对可实现前向安全。",
        "context_trigger": "ECDH、Curve25519、密钥协商、前向安全、公钥交换",
        "ipa_abbr": "ECDH X25519",
        "py_example": "from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey\npriv = X25519PrivateKey.generate()\npub = priv.public_key()\nshared = priv.exchange(peer_pub_key)",
    },
    {
        "name": "HKDF-SHA256 密钥派生",
        "category": "密码学",
        "subcategory": "密钥派生",
        "description": "从 ECDH 共享密钥派生固定长度会话密钥。龍魂默认派生 16 字节 SM4-128 密钥，盐值需两端一致。",
        "context_trigger": "HKDF、SHA256、密钥派生、SM4 会话密钥",
        "ipa_abbr": "HKDF",
        "py_example": "from cryptography.hazmat.primitives.kdf.hkdf import HKDF\nfrom cryptography.hazmat.primitives import hashes\nhkdf = HKDF(algorithm=hashes.SHA256(), length=16, salt=b'longhun-salt', info=b'session')\nsm4_key = hkdf.derive(shared_secret)",
    },
    {
        "name": "国密 SM4-CBC 加密信封",
        "category": "密码学",
        "subcategory": "对称加密",
        "description": "业务数据先 JSON 序列化，再使用 SM4-CBC 加密，附带随机 IV、HMAC-SHA256 完整性校验与 DNA 追溯码，组成加密信封后出应用。",
        "context_trigger": "SM4、国密、CBC、加密信封、HMAC、完整性校验",
        "ipa_abbr": "SM4-CBC",
        "py_example": "from gmssl.sm4 import CryptSM4, SM4_ENCRYPT\ncrypt = CryptSM4()\ncrypt.set_key(key, SM4_ENCRYPT)\ncipher = crypt.crypt_cbc(iv, plaintext)",
    },
    {
        "name": "HMAC-SHA256 完整性校验",
        "category": "密码学",
        "subcategory": "消息认证",
        "description": "在 SM4 密文上计算 HMAC-SHA256，防止中间人篡改。接收方使用 compare_digest 常量时间比较，避免时序攻击。",
        "context_trigger": "HMAC、SHA256、完整性、防篡改、时序攻击",
        "ipa_abbr": "HMAC",
        "py_example": "import hmac, hashlib\nmac = hmac.new(key, iv + ciphertext, hashlib.sha256).digest()\nif not hmac.compare_digest(mac, received_mac): raise ValueError('tampered')",
    },
    {
        "name": "版本向量时钟 (Version Vector)",
        "category": "分布式系统",
        "subcategory": "一致性",
        "description": "每个设备维护一个计数器向量。同步时比较向量可判断数据先后、相等或并发冲突，是本地优先同步的核心数据结构。",
        "context_trigger": "版本向量、Version Vector、并发冲突、因果关系",
        "ipa_abbr": "VV",
        "py_example": "# 向量比较逻辑\nvec_a, vec_b = {'ios':2,'harmonyos':1}, {'ios':1,'harmonyos':2}\n# 互不支配 => concurrent => 冲突",
    },
    {
        "name": "CRDT 无冲突复制数据类型",
        "category": "分布式系统",
        "subcategory": "一致性",
        "description": "本地优先同步的基础抽象。通过设计满足交换律、结合律、幂等律的数据类型，离线编辑后自动合并，无需中央服务器。",
        "context_trigger": "CRDT、本地优先、离线同步、自动合并",
        "ipa_abbr": "CRDT",
        "py_example": "# G-Counter 示例\nmerge = {k: max(a.get(k,0), b.get(k,0)) for k in set(a)|set(b)}",
    },
    {
        "name": "字段级冲突合并策略",
        "category": "分布式系统",
        "subcategory": "冲突解决",
        "description": "当双端同时修改同一对象不同字段时，自动保留各自修改的字段，仅对冲突字段按策略（时间戳/人工确认/双方保留）处理。",
        "context_trigger": "字段合并、冲突解决、并发修改、自动合并",
        "ipa_abbr": "Field Merge",
        "py_example": "# 参见 longhun-cross-platform/scripts/冲突解决器.py 字段级合并实现",
    },
    {
        "name": "QR/NFC 近场公钥交换",
        "category": "安全工程",
        "subcategory": "密钥交换",
        "description": "ECDH 公钥通过二维码（视觉通道）或 NFC（近场电磁通道）交换，避免经过网络，降低中间人攻击面。",
        "context_trigger": "二维码配对、NFC、公钥交换、近场、MITM",
        "ipa_abbr": "QR/NFC",
        "py_example": "import qrcode\nqr = qrcode.QRCode()\nqr.add_data('LONGHUN:ECDH:v1:' + base64.b64encode(pubkey).decode())\nqr.print_ascii()",
    },
    {
        "name": "主权网关出境阻断",
        "category": "网络安全",
        "subcategory": "主权保障",
        "description": "传输前检查目标地址是否本地、数据是否已加密、是否含外网 DNS 查询。任一不通过即阻断并告警，确保数据根留中国。",
        "context_trigger": "主权网关、出境阻断、外网阻断、DNS 泄露、数据主权",
        "ipa_abbr": "Sovereign Gateway",
        "py_example": "# 参见 longhun-cross-platform/scripts/主权网关.py::_是本地地址 与 检查出境许可",
    },
    {
        "name": "本地优先软件 (Local-First Software)",
        "category": "软件架构",
        "subcategory": "设计理念",
        "description": "数据优先存储在端侧，云端仅作可选备份。网络不可用时照常工作，恢复连接后再同步， sovereignty 与可用性兼得。",
        "context_trigger": "本地优先、Local-First、离线可用、端侧主权",
        "ipa_abbr": "Local-First",
        "py_example": "# 架构原则：本地 SQLite + 版本向量 + 加密信封 + 可选云端备份",
    },
    {
        "name": "链路本地地址 (Link-Local)",
        "category": "网络协议",
        "subcategory": "本地直连",
        "description": "169.254.0.0/16 与 fe80::/10 段，设备无 DHCP/路由器时仍可互相通信，适合临时直连场景。",
        "context_trigger": "Link-Local、169.254、fe80、无网直连",
        "ipa_abbr": "Link-Local",
        "py_example": "import ipaddress\naddr = ipaddress.ip_address('169.254.12.34')\nprint(addr.is_link_local)",
    },
    {
        "name": "IPv6 唯一本地地址 (ULA)",
        "category": "网络协议",
        "subcategory": "本地直连",
        "description": "fc00::/7 为本地私有 IPv6 空间，类似于 IPv4 RFC1918，龍魂主权网关将其纳入本地白名单。",
        "context_trigger": "IPv6 ULA、fc00::/7、本地地址",
        "ipa_abbr": "ULA",
        "py_example": "import ipaddress\naddr = ipaddress.ip_address('fd00::1')\nprint(addr.is_private)",
    },
    {
        "name": "传输通道自动降级",
        "category": "网络协议",
        "subcategory": "可靠性",
        "description": "龍魂传输管理器按 WiFi Direct → TCP LAN → BLE 优先级尝试连接，失败自动降级，提高端到端可用性。",
        "context_trigger": "自动降级、故障转移、传输通道、WiFi Direct、BLE",
        "ipa_abbr": "Fallback",
        "py_example": "# 参见 longhun-cross-platform/scripts/传输管理器.py::连接() 优先级列表",
    },
    {
        "name": "端到端加密 (E2EE)",
        "category": "密码学",
        "subcategory": "安全模型",
        "description": "数据在发送端加密、接收端解密，中间任何节点（包括本地路由器、可能的云端）只能看到密文，无法读取明文。",
        "context_trigger": "端到端加密、E2EE、密文传输、中间节点不可读",
        "ipa_abbr": "E2EE",
        "py_example": "# 流程: 明文 -> SM4-CBC -> HMAC -> 信封 -> 网络 -> 验证 -> 解密 -> 明文",
    },
    {
        "name": "龍魂跨平台同步协议 v5.3",
        "category": "龍魂专属",
        "subcategory": "端到端同步",
        "description": "iOS 与 鸿蒙设备间本地网络直连数据同步的完整协议栈：mDNS 发现 → ECDH 协商 → SM4 信封 → 版本向量 → 冲突解决 → 主权网关审计。",
        "context_trigger": "龍魂跨平台、iOS 鸿蒙同步、本地直连、数据主权",
        "ipa_abbr": "LongHun-XSync",
        "py_example": "# 一键演示:\n# python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py demo",
    },
]


def 写入_cs_kb():
    import sqlite3
    conn = sqlite3.connect(str(CS_KB_DB))
    cur = conn.cursor()
    cur.execute('SELECT MAX(CAST(card_id AS INTEGER)) FROM cs_kb')
    start_id = (cur.fetchone()[0] or 0) + 1
    inserted = 0
    for i, card in enumerate(知识卡片清单):
        cid = str(start_id + i)
        name = card["name"]
        row = {
            "card_id": cid,
            "name": name,
            "category": card.get("category", "网络协议"),
            "subcategory": card.get("subcategory", "本地直连"),
            "description": card.get("description", ""),
            "core_formula": card.get("core_formula", ""),
            "misconceptions": card.get("misconceptions", ""),
            "status": card.get("status", "已完成"),
            "difficulty": card.get("difficulty", "L2 进阶"),
            "priority": card.get("priority", "高优先级"),
            "context_trigger": card.get("context_trigger", ""),
            "persona_route": json.dumps({"route": "跨平台同步工程师"}, ensure_ascii=False),
            "architecture_layer": card.get("architecture_layer", "L3 传输层"),
            "is_core": card.get("is_core", "是"),
            "is_in_system": card.get("is_in_system", "是"),
            "dr_wuxing_gong": _dr(i),
            "alpha_san yi": card.get("alpha_san yi", ""),
            "short_dna": _dna(name),
            "ipa_abbr": card.get("ipa_abbr", ""),
            "tri_color_audit": card.get("tri_color_audit", "🟢可用🟡注意🔴阻断"),
            "related_knowledge": card.get("related_knowledge", "龍魂跨平台同步协议 v5.3"),
            "source_ref": _dna("CS-KB-" + name),
            "formula": card.get("formula", ""),
            "routing_params": json.dumps({
                "skill": "longhun-cross-platform",
                "module": "xsync_workflow",
                "action": "search",
            }, ensure_ascii=False),
            "py_example": card.get("py_example", ""),
        }
        cols = ", ".join(f'"{k}"' for k in row.keys())
        placeholders = ", ".join(["?"] * len(row))
        cur.execute(f"INSERT OR REPLACE INTO cs_kb ({cols}) VALUES ({placeholders})", tuple(row.values()))
        inserted += 1
    conn.commit()
    conn.close()
    return inserted, start_id


def 生成_markdown_文档():
    KG_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    # 总览文档
    overview = KG_DIR / "README.md"
    overview.write_text(
        f"""# 龍魂跨平台同步专业知识库

DNA: {_dna('cross-platform-sync-overview')}

本目录汇总 iOS / 鸿蒙 / macOS / Linux 本地网络直连、端到端加密、冲突解决等专业知识，
对应可执行实现位于 `~/.kimi-code/skills/longhun-cross-platform/scripts/`。

## 核心原则

1. 数据根留中国，不经过外网。
2. 先加密再出应用：SM4-CBC + HMAC-SHA256。
3. 密钥不离设备：ECDH Curve25519 + HKDF-SHA256。
4. 本地网络直连：mDNS / WiFi Direct / BLE / TCP LAN。

## 关键命令

```bash
# 单机端到端演示
python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py demo

# mDNS 发现
python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py discover

# 生成/扫描二维码配对
python3 .../xsync_workflow.py pair-qr --text-out /tmp/server_pub.txt
python3 .../xsync_workflow.py pair-scan --input /tmp/server_pub.txt
```
""",
        encoding="utf-8",
    )
    paths.append(overview)

    for card in 知识卡片清单:
        safe = card["name"].replace("/", "-")
        md_path = KG_DIR / f"{safe}.md"
        md_path.write_text(
            f"""# {card['name']}

**DNA**: {_dna(card['name'])}
**分类**: {card['category']} / {card['subcategory']}
**英文缩写**: {card.get('ipa_abbr', '')}

## 定义

{card['description']}

## 触发场景

{card.get('context_trigger', '')}

## Python 示例

```python
{card.get('py_example', '# 见对应实现脚本')}
```

## 相关链接

- 龍魂跨平台同步工作流: `~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py`
- 龍魂技能 SKILL.md: `~/.kimi-code/skills/longhun-cross-platform/SKILL.md`
""",
            encoding="utf-8",
        )
        paths.append(md_path)
    return paths


def 编入全局索引(文档路径列表):
    # 动态导入全局索引服务中的类
    sys.path.insert(0, str(GLOBAL_INDEX_SERVICE.parent))
    import importlib.util
    spec = importlib.util.spec_from_file_location("global_index_service", GLOBAL_INDEX_SERVICE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    cfg = mod.Config(mod.CONFIG_PATH)
    db = mod.Database(GLOBAL_INDEX_DB)
    rules = mod.ExclusionRules(cfg)
    extractor = mod.MediaExtractor(cfg)
    indexer = mod.Indexer(cfg, db, rules, extractor)

    root = str(HOME / "longhun-system")
    for p in 文档路径列表:
        indexer.index_file(Path(p), root, event_type="created")
    indexer.flush()
    return len(文档路径列表)


def main():
    print(f"\n{'='*60}")
    print("  龍魂跨平台同步专业知识入库")
    print(f"  DNA: {_dna('add-cross-platform-kb')}")
    print(f"{'='*60}\n")

    inserted, start_id = 写入_cs_kb()
    print(f"🟢 CS KB 写入 {inserted} 张知识卡片，起始 ID: {start_id}")

    paths = 生成_markdown_文档()
    print(f"🟢 生成 {len(paths)} 篇 Markdown 知识文档: {KG_DIR}")

    indexed = 编入全局索引(paths)
    print(f"🟢 编入全局索引 {indexed} 个文件")

    print(f"\n{'='*60}")
    print("  完成。可执行验证：")
    print("  python3 ~/.kimi-code/skills/longhun-cross-platform/scripts/xsync_workflow.py demo")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
