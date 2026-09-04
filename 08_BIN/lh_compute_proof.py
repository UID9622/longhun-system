#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-COMPUTE-PROOF-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·算力证明引擎 v1.0                                      ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-COMPUTE-PROOF-v1.0     ║
# ║  守护人格: 乔前辈(P04鲁班)                                   ║
# ║  签章: JOE-PROOF-VERIFIER-2026                              ║
# ╚══════════════════════════════════════════════════════════════╝
"""
龍魂·算力证明引擎 — 验证鲲鹏签名，归档到本地保险柜。

铁律：
  - 每次计算必须有鲲鹏签名的零留存证明
  - 证明验签失败 → 立即告警，拒绝结果
  - 非ZERO留存 → 断开连接
  - 所有证明归档到本地保险柜，含DNA追溯

用法:
  python3 bin/lh_compute_proof.py verify <proof.json>    # 验证单次证明
  python3 bin/lh_compute_proof.py audit                   # 审计链
  python3 bin/lh_compute_proof.py selftest                # 自检
"""

import os
import sys
import json
import hmac
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# ═══ 常量 ═══
DNA = "#龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-COMPUTE-PROOF-v1.0"
创建者 = "诸葛鑫（UID9622）"
协议 = "CC BY-NC-SA 4.0"

PROOF_ARCHIVE = Path.home() / ".longhun" / "proofs"
PROOF_INDEX = PROOF_ARCHIVE / "index.json"
ZERO_RETENTION = "ZERO"

# 鲲鹏节点公钥（通过SSH部署时写入）
KUNPENG_NODE_ID = "kunpeng-119.13.90.27"


# ═══ 算力证明 ═══
class ComputeProofEngine:
    """验签、归档、审计。"""

    def __init__(self):
        PROOF_ARCHIVE.mkdir(parents=True, exist_ok=True)
        PROOF_ARCHIVE.chmod(0o700)
        if not PROOF_INDEX.exists():
            PROOF_INDEX.write_text(json.dumps({
                "version": "1.0",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "proofs": {},
                "count": 0,
                "verified_count": 0,
                "rejected_count": 0,
            }, indent=2))
            PROOF_INDEX.chmod(0o600)

    def verify(self, proof: Dict[str, Any], local_request_hash: str) -> bool:
        """
        三步验证：
        1. 签名有效性
        2. 请求哈希一致性
        3. 零留存声明
        """
        errors = []

        # 1. 验证签名
        signature = proof.pop("signature", None)
        if not signature:
            errors.append("缺少签名")
        else:
            message = json.dumps(proof, sort_keys=True, ensure_ascii=False)
            if not self._verify_signature(message, signature):
                errors.append("签名无效 — 鲲鹏可能被篡改")

        proof["signature"] = signature

        # 2. 请求哈希一致性
        proof_hash = proof.get("request_hash", "")
        if proof_hash != local_request_hash:
            errors.append(f"请求哈希不匹配: {proof_hash[:16]} vs {local_request_hash[:16]}")

        # 3. 零留存声明
        if proof.get("data_retention") != ZERO_RETENTION:
            errors.append(f"非零留存: {proof.get('data_retention')}")

        # 归档
        self._archive(proof, errors == [])

        if errors:
            print(f"🔴 证明验证失败:")
            for e in errors:
                print(f"   - {e}")
            return False

        return True

    def _verify_signature(self, message: str, signature: str) -> bool:
        """验证鲲鹏签名。"""
        # 简化版：HMAC验证（生产用ECDSA公钥验签）
        key = hashlib.sha256(f"kunpeng:{KUNPENG_NODE_ID}".encode()).digest()
        expected = hashlib.sha256(key + message.encode()).hexdigest()
        return hmac.compare_digest(expected, signature)

    def _archive(self, proof: Dict[str, Any], verified: bool):
        """归档证明到本地保险柜。"""
        import hmac as _hmac  # 避免命名冲突

        proof_dna = self._generate_dna(proof)
        entry = {
            "dna": proof_dna,
            "proof": proof,
            "verified": verified,
            "archived_at": datetime.now(timezone.utc).isoformat(),
        }

        # 写入文件
        filepath = PROOF_ARCHIVE / f"{proof_dna}.proof"
        filepath.write_text(json.dumps(entry, indent=2, ensure_ascii=False))
        filepath.chmod(0o600)

        # 更新索引
        index = json.loads(PROOF_INDEX.read_text())
        index["proofs"][proof_dna] = {
            "session_id": proof.get("session_id", ""),
            "verified": verified,
            "archived_at": entry["archived_at"],
            "model": proof.get("model_used", ""),
        }
        index["count"] = len(index["proofs"])
        if verified:
            index["verified_count"] += 1
        else:
            index["rejected_count"] += 1
        PROOF_INDEX.write_text(json.dumps(index, indent=2, ensure_ascii=False))

    def audit_trail(self) -> Dict[str, Any]:
        """审计链：所有算力证明的完整记录。"""
        index = json.loads(PROOF_INDEX.read_text()) if PROOF_INDEX.exists() else {}
        entries = []

        for dna, info in index.get("proofs", {}).items():
            entries.append({
                "dna": dna,
                "session_id": info["session_id"],
                "verified": info["verified"],
                "archived_at": info["archived_at"],
            })

        # Merkle根
        sorted_entries = sorted(entries, key=lambda x: x["archived_at"])
        hashes = [hashlib.sha256(json.dumps(e, sort_keys=True).encode()).digest() for e in sorted_entries]
        merkle_root = self._merkle_root(hashes) if hashes else "0" * 64

        return {
            "total_computations": index.get("count", 0),
            "verified": index.get("verified_count", 0),
            "rejected": index.get("rejected_count", 0),
            "merkle_root": merkle_root,
            "entries": entries[-20:],  # 最近20条
        }

    def _generate_dna(self, proof: Dict[str, Any]) -> str:
        """生成证明DNA追溯码。"""
        sid = proof.get("session_id", "unknown")[:8]
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        h = hashlib.sha256(json.dumps(proof, sort_keys=True).encode()).hexdigest()[:8]
        return f"PROOF-{sid}-{ts}-{h}"

    def _merkle_root(self, hashes: List[bytes]) -> str:
        """Merkle树根哈希。"""
        if not hashes:
            return "0" * 64
        while len(hashes) > 1:
            if len(hashes) % 2 == 1:
                hashes.append(hashes[-1])
            hashes = [
                hashlib.sha256(hashes[i] + hashes[i+1]).digest()
                for i in range(0, len(hashes), 2)
            ]
        return hashes[0].hex() if hashes else "0" * 64


# ═══ CLI ═══
def cmd_verify(args):
    engine = ComputeProofEngine()
    proof = json.loads(Path(args.proof_file).read_text()) if args.proof_file else json.loads(sys.stdin.read())
    request_hash = args.hash or proof.get("request_hash", "")
    ok = engine.verify(proof, request_hash)
    if ok:
        print("✅ 证明验证通过 — 零留存确认")
    else:
        sys.exit(1)


def cmd_audit(args):
    engine = ComputeProofEngine()
    trail = engine.audit_trail()
    print("=" * 60)
    print("龍魂·算力证明审计链")
    print("=" * 60)
    print(f"总算力调用: {trail['total_computations']}")
    print(f"已验证:     {trail['verified']}")
    print(f"已拒绝:     {trail['rejected']}")
    print(f"Merkle根:   {trail['merkle_root'][:32]}...")
    print()
    if trail['entries']:
        print(f"{'DNA':<45} {'会话ID':<20} {'状态':>6}")
        print("-" * 75)
        for e in trail['entries']:
            status = "🟢" if e['verified'] else "🔴"
            print(f"{e['dna']:<45} {e['session_id']:<20} {status:>6}")


def cmd_selftest(args):
    """自检：完整证明→验证→归档链路。"""
    import hmac as _hmac
    print("=" * 60)
    print("龍魂·算力证明引擎 v1.0 — 自检")
    print("=" * 60)

    passed = 0
    failed = 0
    engine = ComputeProofEngine()

    # 1. 有效证明验证
    try:
        test_hash = hashlib.sha256(b"test_request").hexdigest()
        message = json.dumps({
            "session_id": "test_session_001",
            "request_hash": test_hash,
            "result_hash": hashlib.sha256(b"test_result").hexdigest(),
            "model_used": "test_model",
            "compute_duration": 0.123,
            "node_id": KUNPENG_NODE_ID,
            "data_retention": ZERO_RETENTION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }, sort_keys=True, ensure_ascii=False)

        key = hashlib.sha256(f"kunpeng:{KUNPENG_NODE_ID}".encode()).digest()
        signature = hashlib.sha256(key + message.encode()).hexdigest()

        proof = json.loads(message)
        proof["signature"] = signature

        ok = engine.verify(proof, test_hash)
        assert ok, "验证失败"
        print("  [1/5] 有效证明     ✅")
        passed += 1
    except Exception as e:
        print(f"  [1/5] 有效证明     ❌ {e}")
        failed += 1

    # 2. 无效签名拒绝
    try:
        bad_proof = json.loads(message)
        bad_proof["session_id"] = "bad_session"
        bad_proof["signature"] = "invalid_signature_ffff"
        ok = engine.verify(bad_proof, test_hash)
        assert not ok, "应该拒绝"
        print("  [2/5] 无效签名     ✅ 正确拒绝")
        passed += 1
    except Exception as e:
        print(f"  [2/5] 无效签名     ❌ {e}")
        failed += 1

    # 3. 哈希不匹配拒绝
    try:
        bad_proof2 = json.loads(message)
        bad_proof2["session_id"] = "hash_mismatch"
        bad_proof2["signature"] = signature
        ok = engine.verify(bad_proof2, "different_hash_value")
        assert not ok, "应该拒绝"
        print("  [3/5] 哈希不匹配   ✅ 正确拒绝")
        passed += 1
    except Exception as e:
        print(f"  [3/5] 哈希不匹配   ❌ {e}")
        failed += 1

    # 4. 非ZERO留存拒绝
    try:
        bad_proof3 = json.loads(message)
        bad_proof3["session_id"] = "non_zero_retention"
        bad_proof3["data_retention"] = "24H"
        bad_proof3["signature"] = signature
        ok = engine.verify(bad_proof3, test_hash)
        assert not ok, "应该拒绝"
        print("  [4/5] 非零留存     ✅ 正确拒绝")
        passed += 1
    except Exception as e:
        print(f"  [4/5] 非零留存     ❌ {e}")
        failed += 1

    # 5. 审计链
    try:
        trail = engine.audit_trail()
        assert trail['total_computations'] >= 1, "无记录"
        assert len(trail['merkle_root']) == 64, "Merkle根不正确"
        print(f"  [5/5] 审计链       ✅ {trail['total_computations']}条记录")
        passed += 1
    except Exception as e:
        print(f"  [5/5] 审计链       ❌ {e}")
        failed += 1

    print(f"\n{'='*60}")
    print(f"结果: {passed}/{passed+failed} 通过")
    if failed == 0:
        print("🟢 证明引擎正常")
    else:
        print(f"🔴 {failed}项失败")


def main():
    parser = argparse.ArgumentParser(description="龍魂·算力证明引擎 v1.0")
    sub = parser.add_subparsers(dest="command")

    p_verify = sub.add_parser("verify", help="验证证明")
    p_verify.add_argument("proof_file", nargs="?", help="证明JSON文件（默认stdin）")
    p_verify.add_argument("--hash", help="本地请求哈希")
    p_verify.set_defaults(func=cmd_verify)

    p_audit = sub.add_parser("audit", help="审计链")
    p_audit.set_defaults(func=cmd_audit)

    p_test = sub.add_parser("selftest", help="自检")
    p_test.set_defaults(func=cmd_selftest)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
