#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/Users/zuimeidedeyihan/longhun-system/.venv_longhun_math/bin/python
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
三层同步引擎单元测试
DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-LONGHUN-TRIPLE-SYNC-TEST-UID9622
"""

import os
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from triple_sync import TripleSync, _解析_markdown, _扫描本地档案


class MockNotionDashboard:
    def __init__(self):
        self.calls = []

    def init_dashboard(self):
        return {"ok": True}

    def add_or_update_page(self, **kwargs):
        self.calls.append(kwargs)
        return {"ok": True}


class TestTripleSync(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="longhun_triple_sync_test_")
        self.tmp_path = Path(self.tmpdir)
        self.卡片目录 = self.tmp_path / "brain" / "cnsh_cards"
        self.卡片目录.mkdir(parents=True)
        self.报告目录 = self.tmp_path / "audit" / "reports"
        self.报告目录.mkdir(parents=True)
        self.github_root = self.tmp_path / "github-public"

        # 写测试卡片
        (self.卡片目录 / "test_card.md").write_text(
            "---\ntitle: 测试卡片\ntags: [test, cnsh]\ndna: \"#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-TEST-CARD-UID9622\"\n---\n\n# 测试卡片\n内容。\n",
            encoding="utf-8",
        )
        # 写测试报告
        (self.报告目录 / "test_report.md").write_text(
            "# 测试报告\n\n报告内容。\n",
            encoding="utf-8",
        )

        # 修改脚本中的 PROJECT_ROOT 为临时目录（通过 monkey patch）
        import triple_sync as ts
        self.原始根目录 = ts.PROJECT_ROOT
        ts.PROJECT_ROOT = self.tmp_path

        self.mock_dash = MockNotionDashboard()
        self.引擎 = TripleSync(github_root=self.github_root, notion_dashboard=self.mock_dash)

    def tearDown(self):
        import triple_sync as ts
        ts.PROJECT_ROOT = self.原始根目录
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_解析_markdown_frontmatter(self):
        文件 = self.卡片目录 / "test_card.md"
        档案 = _解析_markdown(文件)
        self.assertEqual(档案["title"], "测试卡片")
        self.assertEqual(档案["dna"], "#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-TEST-CARD-UID9622")
        self.assertIn("test", 档案["tags"])
        self.assertEqual(档案["source"], "CNSH卡片")

    def test_解析_markdown无frontmatter(self):
        文件 = self.报告目录 / "test_report.md"
        档案 = _解析_markdown(文件)
        self.assertEqual(档案["title"], "测试报告")
        self.assertTrue(档案["dna"].startswith("#龍芯⚡️"))
        self.assertIn("UID9622", 档案["dna"])
        self.assertEqual(档案["source"], "审计报告")

    def test_扫描本地档案(self):
        档案列表 = list(_扫描本地档案())
        self.assertEqual(len(档案列表), 2)
        标题集 = {a["title"] for a in 档案列表}
        self.assertEqual(标题集, {"测试卡片", "测试报告"})

    def test_sync_to_notion(self):
        结果 = self.引擎.sync_to_notion()
        self.assertTrue(结果["ok"])
        self.assertEqual(结果["synced"], 2)
        self.assertEqual(结果["failed"], 0)
        self.assertEqual(len(self.mock_dash.calls), 2)
        self.assertEqual(self.mock_dash.calls[0]["title"], "测试卡片")

    def test_freeze_to_github(self):
        结果 = self.引擎.freeze_to_github(month="2026-06")
        self.assertTrue(结果["ok"])
        self.assertEqual(结果["month"], "2026-06")
        self.assertEqual(结果["copied"], 2)
        月度目录 = self.github_root / "monthly" / "2026-06"
        self.assertTrue(月度目录.exists())
        self.assertTrue((月度目录 / "README.md").exists())
        readme = (月度目录 / "README.md").read_text(encoding="utf-8")
        self.assertIn("LU 公开档案月度冻结", readme)
        self.assertIn("测试卡片", readme)
        self.assertIn("测试报告", readme)
        # 未配置 remote，不应推送成功
        self.assertFalse(结果["git_pushed"])


if __name__ == "__main__":
    unittest.main()
