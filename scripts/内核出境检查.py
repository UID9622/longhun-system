# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 内核出境保护检查器

检查代码/配置中是否存在把龍魂内核通过代理、第三方 API、外部仓库等方式流出的风险。
DNA: #龍芯⚡️2026-06-30-LONGHUN-KERNEL-EGRESS-CHECK-v1.0
"""

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
KERNEL_DIRS = [
    HOME / "longhun-system" / "scripts",
    HOME / ".kimi-code" / "skills",
    HOME / ".longhun" / "config",
]

风险模式 = [
    (r"内核.*(上传|导出|发送|返回).*代理", "内核经代理出境"),
    (r"代理.*返回.*(内核|核心|协议)", "代理返回内核数据"),
    (r"第三方.*(获取|调用).*(内核|核心|DNA)", "第三方获取内核"),
    (r"github\.com.*(内核|核心|longhun|CNSH)", "内核上传 GitHub"),
    (r" gist\.github\.com|pastebin|hastebin", "代码粘贴外网"),
    (r"curl.*-F.*file=@.*(\.py|\.json|\.md)", "curl 外发文件"),
    (r"scp.*\.(py|json|md).*@.*:", "SCP 外发文件"),
    (r"上传.*(\.longhun|longhun-system)", "本地目录外发"),
]


def _检查文件(路径: Path) -> list[Any]:
    风险 = []
    if not 路径.is_file():
        return 风险
    try:
        文本 = 路径.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return 风险
    for pattern, 类型 in 风险模式:
        for match in re.finditer(pattern, 文本, re.IGNORECASE):
            风险.append({
                "file": str(路径),
                "type": 类型,
                "line": 文本[:match.start()].count("\n") + 1,
                "preview": 文本[max(0, match.start()-30):match.end()+30],
            })
    return 风险


def main():
    if len(sys.argv) > 1:
        目标 = Path(sys.argv[1])
    else:
        目标 = HOME / "longhun-system"

    所有风险 = []
    for root, _, files in os.walk(目标):
        for name in files:
            if name.endswith((".py", ".json", ".md", ".sh", ".yaml", ".yml")):
                所有风险.extend(_检查文件(Path(root) / name))

    if 所有风险:
        print(f"🟡 发现 {len(所有风险)} 处内核出境风险（需人工复核）")
        for r in 所有风险[:15]:
            print(f"   [{r['type']}] {r['file']}:{r['line']}")
    else:
        print("🟢 未发现明显内核出境风险")

    print(f"   DNA: #龍芯⚡️2026-06-30-LONGHUN-KERNEL-EGRESS-CHECK-v1.0")


if __name__ == "__main__":
    main()
