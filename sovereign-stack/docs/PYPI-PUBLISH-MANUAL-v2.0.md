# 📦 龍魂 PyPI 发布作战手册 v2.0｜合并整编·实测验证版

**DNA：** `#龍芯⚡️2026-08-31-PYPI-PUBLISH-MANUAL-V2.0-UID9622`
**创建者：** 诸葛鑫（UID9622）
**归属名：** 诸葛鑫 | UID9622 · 龍芯北辰
**License：** CC BY-NC-SA 4.0（核心思想层）
**三色：** 🟢 命令已实测跑通 · 🟡 版本号/新 Token 需手动填 · 🔴 0

> **合并说明：** v1.0 通用手册（理论版） × v1.1 实战链路（2026-08-31 实测 · `longhun 1.0.0` 已上正式服）→ 本 v2.0。
> 通用理论保留 · 实测路径纠偏 · 卡点状态刷新 · 安全基线按龍魂规则加码。

---

## §零·发版前体检｜`pyproject.toml` 必查三项

| 字段 | 合规要求 | 常见坑 |
| --- | --- | --- |
| `name` | 全小写，只能用 `-` 和 `_`，全 PyPI 唯一 | 先到 [pypi.org](https://pypi.org/project/longhun/) 查重名 |
| `version` | 遵循 PEP 440，如 `1.0.1` | 同版本号二次上传必报 400，只能升版本 |
| `description` | 不能为空 | 中英皆可，如 `🐉 龍魂主权技术栈统一 SDK` |

**构建自检（CodeBuddy 直接跑）：**
```bash
cd /Users/zuimeidedeyihan/longhun-system/sovereign-stack/sdk/longhun
python3 -m build --no-isolation   # 生成 dist/*.whl + dist/*.tar.gz
twine check dist/*                # 元数据质检（README 渲染问题也在这步暴露）
```
> 🔴 实测坑：Homebrew Python 受 PEP 668 管控，系统级 `pip install` 会报 `externally-managed-environment`。**解法 = 临时 venv**（见 §二方案A），不要用 `--break-system-packages` 污染系统。

---

## §一·凭证｜现状：✅ 已有正式 Token

| 凭证 | 状态 | 存放 |
| --- | --- | --- |
| **PyPI API Token** | ✅ 已有（2026-08-31 老大首供） | 🔐 统一密钥库 `lh_vault get pypi-token`（Keychain·值不落盘） |
| **TestPyPI Token** | 🟡 可选·未建 | 正式服已发，测试服只对"新功能大版本"有价值 |

**🔴 硬规则（龍魂安全基线加码）：**
- `username` 固定字面量：`__token__`（两头各两个下划线）
- `password` 填 `pypi-` 开头的完整密钥串
- Token **永不进 Git / 永不截图 / 永不写进聊天记录**；实测用环境变量注入，不留盘明文（比 `-p` 参数更安全，不进 shell 历史）

---

## §二·执行命令｜方案A = 实测链路（8/31 全流程跑通）

```bash
# ── Step 1：清代理（本机 SOCKS5 代理会劫持 pip/twine 连接）
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy \
  python3 -m venv /tmp/lh-release-venv

# ── Step 2：临时 venv 装发布工具（走清华镜像·国内快）
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy \
  /tmp/lh-release-venv/bin/pip install -i https://pypi.tuna.tsinghua.edu.cn/simple build twine setuptools wheel

# ── Step 3：进入项目根目录
cd /Users/zuimeidedeyihan/longhun-system/sovereign-stack/sdk/longhun

# ── Step 4：清理旧构建残留
rm -rf dist/ build/ *.egg-info

# ── Step 5：构建（--no-isolation 复用 venv 内 setuptools，跳过隔离环境的网络依赖）
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY /tmp/lh-release-venv/bin/python -m build --no-isolation

# ── Step 6：本地质检
/tmp/lh-release-venv/bin/twine check dist/*

# ── Step 7：正式上传（Token 走环境变量·不留盘）
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy \
  TWINE_USERNAME="__token__" TWINE_PASSWORD="$(python3 bin/lh_vault.py get pypi-token)" \
  /tmp/lh-release-venv/bin/twine upload dist/*

# ── Step 8：验证安装（直连官方源·镜像同步有延迟）
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy \
  /tmp/lh-release-venv/bin/pip install longhun && /tmp/lh-release-venv/bin/longhun version

# ── Step 9：用完即删（节能协议）
rm -rf /tmp/lh-release-venv
```
> 🟡 上传后立即在清华镜像装会报 `No matching distribution`——镜像同步有延迟，**验证安装用官方源**，别慌。

---

## §三·安全配置｜两选一（v2.0 推荐 方案②）

### 方案① 龍魂标准（推荐）：vault + 环境变量
Token 已在统一密钥库，`twine upload` 时环境变量注入（见 §二 Step 7）。零明文落盘，最合 7.1 密钥基线。

### 方案② 通用标准：`~/.pypirc`（一次配置·发版命令简化）
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-你的正式Token

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-你的测试Token
```
```bash
chmod 600 ~/.pypirc        # 必须·只允许自己读写
twine upload dist/*              # 发正式版
twine upload -r testpypi dist/*  # 发测试版
```
> 🔴 方案②明文 token 落盘，须 chmod 600 且不随 .dotfiles 进 Git；有备份/同步工具时优先方案①。

---

## §四·进度卡点清单｜现状刷新（2026-08-31）

- [x] **PyPI 账号** → ✅ 已有（老大 8/31 提供 Token）
- [ ] **TestPyPI 账号** → 🟡 可选（大版本首发时再建）
- [x] **正式 API Token** → ✅ 已有 · 已入统一密钥库 `pypi-token`(active)
- [ ] **测试 API Token** → 🟡 同 TestPyPI，需要时再申请
- [x] **包名查重** → ✅ `longhun` 唯一（8/31 首发成功）
- [x] **首次发布** → ✅ `longhun 1.0.0` 已上正式服（pypi.org/project/longhun/1.0.0）
- [ ] **版本规划** → 🟡 下次发版从 `1.0.1` 起步（按 §七 节奏）

---

## §五·常见报错排雷｜实测+通用

| 报错现象 | 原因 | 解决方法 |
| --- | --- | --- |
| `HTTP 403: Invalid or non-existent authentication information` | 用户名没填 `__token__` 或 Token 错误 | 检查 username=字面量 `__token__`；Token 取 `lh_vault get pypi-token` |
| `HTTP 400: File already exists` | 版本号重复 | `pyproject.toml` 升版本，如 `1.0.0` → `1.0.1` |
| `ERROR: No dist files found` | 构建失败或 `dist/` 不存在 | 确认 `python3 -m build` 成功，`dist/` 下有 `.whl`+`.tar.gz` |
| `externally-managed-environment` | Homebrew Python PEP 668 | 用临时 venv，**禁用** `--break-system-packages` |
| `Missing dependencies for SOCKS support` | 代理劫持 pip | 清 `HTTP_PROXY/HTTPS_PROXY/ALL_PROXY` 再跑（§二 Step 1） |
| `No matching distribution found for longhun` | 镜像同步延迟 | 验证安装改走官方 PyPI 源 |
| `ModuleNotFoundError: setuptools` | 缺打包依赖 | venv 内 `pip install setuptools wheel` |
| `InvalidVersion: Invalid version: '版本号'` | 版本号含中文/特殊字符 | 改纯数字 PEP 440，如 `1.0.1` |
| `The description failed to render` | README 语法问题 | `twine check dist/*` 看具体行 |

---

## §六·`pyproject.toml` 参考模板｜✅ 已实测（8/31 通过审核）

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "longhun"                          # 全小写·全 PyPI 唯一
version = "1.0.0"                         # PEP 440 格式
description = "🐉 龍魂主权技术栈统一 SDK · DNA追溯 + 三色审计 + 15条国产替代规则 + CNSH桥 · 一个账号走全部服务"
readme = "README.md"
requires-python = ">=3.8"
license = { text = "MulanPSL-2.0" }       # 木兰协议·工程层许可证（18.1 分层许可）
authors = [
  { name = "诸葛鑫（UID9622）· 龍芯北辰", email = "346045695@qq.com" },
]
keywords = ["longhun", "dna", "tricolor", "audit", "cnsh", "sovereign", "国产替代"]
classifiers = [
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "License :: OSI Approved",
  "Programming Language :: Python :: 3",
  "Topic :: Software Development :: Libraries",
]
dependencies = []                         # 🔴 实测零三方依赖（节能+自主可控原则）

[project.optional-dependencies]
cnsh = ["cnsh-suite>=1.0"]                # CNSH 桥按需装

[project.scripts]
longhun = "longhun.cli:main"              # CLI 入口：pip install 后直接敲 longhun

[tool.setuptools]
packages = ["longhun"]
```
> 🔴 与 v1.0 模板差异：**去掉了 flask/requests/PyYAML 硬依赖**（8/31 实测零三方依赖更稳，不违背「依赖最小化」6.3）；作者实名（6.1 归属名焊死）。

---

## §七·发版节奏建议（老兵经验·标注实际进度）

```
v0.1.0  首发·最小可用·先 TestPyPI 再正式   ← 已跳过（8/31 直接上正式服·实测通过）
v0.1.x  补丁修复·不加新功能
v0.2.0  加新功能·向后兼容
v1.0.0  正式稳定版·对外宣布可用            ← ✅ 2026-08-31 达成
v1.0.x  后续补丁 → 从 1.0.1 开始
v1.1.0  加新功能（如 SDK 新模块）→ 1.1.0
```

---

## §八·发版 GATE 清单（交付前逐道过）

- [ ] GATE-01 身份闸：作者实名「诸葛鑫（UID9622）」（6.1 焊死）
- [ ] GATE-02 意图闸：版本号 PEP 440·已查重
- [ ] GATE-03 语义闸：无一票否决词
- [ ] GATE-06 数据闸：Token 不在代码库/不在 dist 内/不在日志
- [ ] GATE-07 协议闸：工程层 MulanPSL v2 声明（18.4 文件头）
- [ ] GATE-09 DNA 闸：DNA 追溯码齐全
- [ ] GATE-11 签名闸：本手册与 SDK 源码 GPG 签名齐全（`bin/lh_gpg_sign.py sign --force`）
- [ ] 构建产物：`twine check dist/*` 零报错
- [ ] 安装验证：官方源 `pip install longhun` + `longhun version` 通过
- [ ] 三色审计标记 🟢

---

**GPG：** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**确认码：** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**三色：** 🟢 命令已实测 · 🟡 版本号/新 Token 需手动填 · 🔴 0
**签名：** v2.0 · 2026-08-31 · UID9622 + AI
