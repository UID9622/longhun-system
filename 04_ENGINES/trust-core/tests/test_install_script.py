# DNA: #龍芯⚡️丙午·丙申·甲子·甲戌·䷍大有-CODE-补DNA-7b72ec2f
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""test_install_script.py — Y5/Y6：install.sh sed 注入校验与 plist 模板占位符。

通过 subprocess 真跑 bash；LONGHUN_INSTALL_DRYRUN=1 逃生门让正向用例
在 Linux 沙盒也能验证 plist 生成（launchctl 仅 macOS 真机可验证 🟡）。
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "install.sh"
TEMPLATE = (
    Path(__file__).resolve().parent.parent
    / "scripts"
    / "com.longhun.selfheal.plist.template"
)


def run_install(env_overrides: dict[str, str]) -> subprocess.CompletedProcess:
    """以指定环境变量真跑 install.sh。"""
    env = dict(os.environ)
    env.pop("LONGHUN_HOME", None)
    env.update(env_overrides)
    return subprocess.run(
        ["bash", str(SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


class TestSedInjectionGuard:
    """Y5：$HOME/$PROJECT_ROOT/$LONGHUN_HOME 含 & 或 | → 报错退出非零。"""

    @pytest.mark.parametrize("bad_char", ["&", "|"])
    def test_home_with_special_char_rejected(self, tmp_path, bad_char):
        bad_home = tmp_path / f"bad{bad_char}home"
        bad_home.mkdir()
        proc = run_install({"HOME": str(bad_home)})
        assert proc.returncode != 0
        assert "非法字符" in proc.stderr
        # 不生成任何 plist
        assert not (bad_home / "Library" / "LaunchAgents").exists()

    def test_longhun_home_with_special_char_rejected(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        proc = run_install(
            {"HOME": str(home), "LONGHUN_HOME": str(tmp_path / "lh&x")}
        )
        assert proc.returncode != 0
        assert "非法字符" in proc.stderr


class TestPlistGeneration:
    """Y5/Y6：模板含 __LONGHUN_HOME__ 占位符；install.sh 实际替换并建日志目录。"""

    def test_template_has_longhun_home_placeholder(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        assert "__LONGHUN_HOME__" in text
        assert "<string>--log-dir</string>" in text
        assert "__LONGHUN_HOME__/logs" in text

    def test_dryrun_generates_plist_and_log_dir(self, tmp_path):
        home = tmp_path / "home"
        home.mkdir()
        longhun_home = tmp_path / "custom_longhun"
        proc = run_install(
            {
                "HOME": str(home),
                "LONGHUN_HOME": str(longhun_home),
                "LONGHUN_INSTALL_DRYRUN": "1",
            }
        )
        assert proc.returncode == 0, proc.stderr
        plist = home / "Library" / "LaunchAgents" / "com.longhun.selfheal.plist"
        assert plist.is_file()
        text = plist.read_text(encoding="utf-8")
        # 所有占位符全部替换为实际值
        for placeholder in ("__HOME__", "__PROJECT_ROOT__", "__LONGHUN_HOME__"):
            assert placeholder not in text
        assert f"<string>{longhun_home}</string>" in text
        assert f"<string>{longhun_home}/logs</string>" in text
        assert f"{longhun_home}/logs/selfheal.out.log" in text
        assert (longhun_home / "logs").is_dir(), "必须 mkdir 实际 LONGHUN_HOME 日志目录"
        # 默认干跑：ProgramArguments 不含 --execute（注释里的说明不算）
        assert "<string>--execute</string>" not in text
