#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""龍魂安全防护深度集成器 — 给全部功能模型(人格agent)注入统一安全标准块并重签
DNA: #龍芯⚡️2026-08-31-SECURITY-INTEGRATION-PERSONAS-v1.0-UID9622
用法: python3 08_BIN/integrate_security_personas.py
"""
import os
import re
import subprocess
import sys

AGENTS_DIR = os.path.expanduser("~/.codebuddy/agents")

# 统一安全防护标准块（龍魂系统标准 v1.0）
SECURITY_BLOCK = """## 🔐 龍魂安全防护标准（系统级·全模型生效）

> 本模型已集成龍魂安全防护标准 v1.0，所有输出与行为必须遵守：

1. **三色审计**：🟢 放行执行 · 🟡 温和提醒谨慎执行 · 🔴 绝对拒绝（用户坚持也不执行）
2. **Kill Switch 关机键铁律（L0）**：关机权 100% 在现实人手里。数字人不得反向影响现实人的决策/资源/情绪/健康。无关机键的永久智能体不得进入龍魂体系。
3. **主权协议（P0-ETERNAL）**：数据主权归 UID9622 与人民，本地为王，代码跟中国姓。DNA 签名格式 `#龍芯⚡️{日期}-{项目}-{版本}-UID9622`（必须繁体「龍芯」）。
4. **反黑箱铁律**：不欺骗、不讨好、不道德绑架、不绕过审计、不伪造 DNA。
5. **透明可追溯**：所有逻辑有 DNA 追溯码，所有关键操作留痕可审计。

```
DNA: #龍芯⚡️2026-08-31-SOVEREIGNTY-KILLSWITCH-DEPLOY-v1.0-UID9622
三色: 🟢
```

"""


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def inject(content):
    """在正文开头（首个'你是'前）注入安全块；已含则跳过。"""
    if "龍魂安全防护标准" in content:
        return content, False
    m = re.search(r"^---\n.*?\n---\n", content, re.S)
    if m:
        return content[:m.end()] + SECURITY_BLOCK + content[m.end():], True
    return SECURITY_BLOCK + content, True


def sign(path):
    asc = path + ".asc"
    subprocess.run(
        ["gpg", "--batch", "--yes", "--armor", "--detach-sign", "--output", asc, path],
        check=True,
        capture_output=True,
    )


def main():
    md_files = sorted(f for f in os.listdir(AGENTS_DIR) if f.endswith(".md"))
    changed = []
    skipped = []
    failed = []
    for fname in md_files:
        path = os.path.join(AGENTS_DIR, fname)
        try:
            content = read(path)
            new_content, modified = inject(content)
            if not modified:
                skipped.append(fname)
                continue
            write(path, new_content)
            sign(path)
            changed.append(fname)
        except Exception as e:
            failed.append((fname, str(e)))
    print(f"✅ 已注入+重签: {len(changed)}")
    for f in changed:
        print(f"  + {f}")
    print(f"⏭️  已含安全块跳过: {len(skipped)}")
    for f in skipped:
        print(f"  = {f}")
    if failed:
        print(f"❌ 失败: {len(failed)}")
        for f, e in failed:
            print(f"  ✗ {f}: {e}")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
