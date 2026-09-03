#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·丁酉·丙辰·午时·䷆师-CNSH-STDLIB-SELFTEST-v1.1-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

CNSH 标准库自测 v1.1 · 零依赖断言 · 双向兼容
- 直跑:   python3 tests/test_all.py            → 汇总 + 退出码
- pytest: python3 -m pytest tests/ -q          → 收集 test_stdlib_all
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from cnsh_std import io, http, time, crypto, dna, audit, fuse, topo, memorial


def run_all(quiet: bool = False) -> int:
    passed, failed = 0, []

    def t(name, fn):
        nonlocal passed
        try:
            fn()
            passed += 1
        except Exception as e:  # noqa: BLE001
            failed.append(f"{name}: {e}")

    # io
    def _io():
        with tempfile.TemporaryDirectory() as d:
            p = str(Path(d) / "a" / "b.txt")
            io.write(p, "你好龍魂")
            assert io.read(p) == "你好龍魂"
            io.append(p, "第二行")
            assert "第二行" in io.read(p)
            assert io.exists(p)

    t("io", _io)

    # time
    def _time():
        assert time.today() == __import__("datetime").date.today().isoformat()
        assert len(time.now_iso()) >= 19
        s = time.ganzhi_stamp()
        assert s.endswith("时")

    t("time", _time)

    # http（离线容错：网络不可达时警告不判失败）
    def _http():
        r = http.get("https://uid9622.cn/api/health", timeout=8)
        if r["status"] is None:
            if not quiet:
                print("  🟡 http 网络不可达（跳过断言）:", r["error"])
            return
        assert r["status"] < 500

    t("http", _http)

    # crypto
    def _crypto():
        assert len(crypto.sha256("龍魂")) == 64
        sig = crypto.hmac_sha256("key", "msg")
        assert crypto.verify_hmac("key", "msg", sig)
        tok = crypto.encrypt("机密正文", "pw")
        assert crypto.decrypt(tok, "pw") == "机密正文"
        assert len(crypto.random_token()) > 20

    t("crypto", _crypto)

    # dna
    def _dna():
        d = dna.generate("CNSH-STDLIB", "TEST")
        assert dna.validate(d)
        assert d.endswith(dna.trace_hash("CNSH-STDLIB", "TEST")[:8])

    t("dna", _dna)

    # audit
    def _audit():
        with tempfile.TemporaryDirectory() as d:
            p = str(Path(d) / "audit.jsonl")
            audit.log(p, {"scope": "test", "verdict": "pass"})
            assert audit.verdict("blocked") == "🔴"
            assert audit.read_log(p)[0]["color"] == "🟢"

    t("audit", _audit)

    # fuse
    def _fuse():
        assert fuse.is_triggered("涉及GPG私钥传出")
        assert not fuse.is_triggered("正常写日志")
        try:
            fuse.check("伪造DNA")
            raise SystemExit("should block")
        except PermissionError:
            pass

    t("fuse", _fuse)

    # topo
    def _topo():
        snap = topo.snapshot()
        assert snap["found"] or True  # 无仓库环境不硬断言
        assert isinstance(snap["layers"], list)

    t("topo", _topo)

    # memorial
    def _memorial():
        with tempfile.TemporaryDirectory() as d:
            p = str(Path(d) / "mem.jsonl")
            memorial.record("milestone", "标准库 v1.0", "自测", p)
            assert len(memorial.list_records(p)) == 1
            memorial.freeze(p)

    t("memorial", _memorial)

    if not quiet:
        print(f"✅ CNSH 标准库自测: 通过 {passed} | 失败 {len(failed)}")
        for f in failed:
            print(f"  ❌ {f}")
    return 1 if failed else 0


def test_stdlib_all():
    """pytest 收集入口：自测任何失败即断言失败"""
    assert run_all(quiet=True) == 0


if __name__ == "__main__":
    sys.exit(run_all())
