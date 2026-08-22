#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
CNSH v2.1 工具链测试
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-CNSH-TOOLCHAIN-TESTS-v2.1
"""
import sys
import unittest
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from cnsh_v21 import toolchain
from cnsh_v21.project import CNSHProject


class TestToolchain(unittest.TestCase):
    def test_version(self):
        out = StringIO()
        err = StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = out, err
        try:
            with self.assertRaises(SystemExit) as cm:
                toolchain.main(["--version"])
            self.assertEqual(cm.exception.code, 0)
        finally:
            sys.stdout, sys.stderr = old_out, old_err
        self.assertIn("2.1.0", out.getvalue() + err.getvalue())

    def test_run_command(self):
        out = StringIO()
        old = sys.stdout
        sys.stdout = out
        try:
            toolchain.main(["run", "examples/types.cnsh"])
        finally:
            sys.stdout = old
        self.assertIn("龍魂", out.getvalue())

    def test_init_command(self):
        with TemporaryDirectory() as tmp:
            name = "hello_cnsh"
            root = Path(tmp) / name
            toolchain.main(["init", str(root), "--description", "测试"])
            self.assertTrue((root / "cnsh.json").exists())
            self.assertTrue((root / "main.cnsh").exists())
            project = CNSHProject(root)
            self.assertEqual(project.name, name)
            self.assertEqual(project.config["description"], "测试")


if __name__ == "__main__":
    unittest.main()
