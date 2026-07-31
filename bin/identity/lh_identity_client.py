# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-IDENTITY-CLIENT-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·主权人格广播客户端
生成本地主权的身份广播信号，可发送到鲲鹏服务端验证。

DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-IDENTITY-CLIENT-v1.0
"""
import os
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lh_identity_keygen import load_private_key, PRIVATE_DIR
from lh_identity_core import (
    collect_device_fingerprint,
    generate_broadcast,
    BehaviorProfile,
    CONFIRM_CODE,
)


STATE_DIR = Path(__file__).resolve().parent.parent.parent / "state"


def load_behavior_profile() -> BehaviorProfile | None:
    path = STATE_DIR / "identity_behavior.json"
    if path.exists():
        return BehaviorProfile.from_dict(json.loads(path.read_text(encoding="utf-8")))
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂·主权人格广播客户端")
    parser.add_argument("--passphrase", "-p", help="私钥加密口令")
    parser.add_argument("--send", "-s", help="发送到服务端验证，如 http://119.13.90.27:8771/identify")
    parser.add_argument("--out", "-o", help="输出广播信号到文件")
    parser.add_argument("--no-behavior", action="store_true", help="不附带行为密码学")
    args = parser.parse_args()

    private_path = PRIVATE_DIR / "uid9622_private.enc"
    if not private_path.exists():
        print(f"[❌] 私钥不存在: {private_path}")
        print("    请先运行: python3 bin/identity/lh_identity_keygen.py")
        return 1

    print("[🔥] 正在加载 UID9622 身份密钥...")
    private_key = load_private_key(args.passphrase)

    print("[📱] 正在采集设备指纹...")
    device_fp = collect_device_fingerprint()

    behavior = None
    if not args.no_behavior:
        behavior = load_behavior_profile()
        if behavior:
            print(f"[🧠] 已加载行为密码学轮廓（样本数: {behavior.sample_count}）")
        else:
            print("[⚠️] 未找到行为轮廓，将生成不含行为特征的广播信号。")
            print("    如需训练，请运行: python3 bin/identity/lh_behavior_trainer.py")

    print("[🌌] 正在生成主权人格广播信号...")
    bc = generate_broadcast(private_key, device_fp, behavior)

    compact = bc.to_compact_string()
    print("\n" + "=" * 64)
    print(compact)
    print("=" * 64 + "\n")

    if args.out:
        out_path = Path(args.out)
        out_path.write_text(json.dumps(bc.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[✅] 广播信号已保存: {out_path}")

    if args.send:
        import urllib.request
        payload = json.dumps(bc.to_dict(), ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            args.send,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                print("[🛰️] 服务端回应:")
                print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"[❌] 发送到服务端失败: {e}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
