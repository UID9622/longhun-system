# DNA: #龍芯⚡️2026-08-31-QUANTUM-TEMPLATE-05-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# 来源: Notion「🧬 量子模板引擎」库


## 🎯 模板定位

面向开发者的PyPI包正规发布流程清单——从代码到 pip install 的完整10步，确保每次发布都专业、可追溯、零失误。

> 适用：lh-standard-adapter、longhun-calendar、cnsh-runtime 等龍魂生态包

---


## 📐 标准 pyproject.toml 模板


```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "your-package-name"
version = "1.0.0"  # 遵循 SemVer
description = "一句话描述 | One-line description"
readme = "README.md"
license = {text = "MulanPSL-2.0"}
requires-python = ">=3.8"
authors = [
    {name = "UID9622", email = "uid9622@petalmail.com"}
]
keywords = ["longhun", "dna-traceability", "ai-governance", "cnsh"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

[project.urls]
Homepage = "https://github.com/UID9622/your-repo"
Documentation = "https://uid9622.notion.site"
Repository = "https://github.com/UID9622/your-repo"
Changelog = "https://github.com/UID9622/your-repo/blob/main/CHANGELOG.md"
Issues = "https://github.com/UID9622/your-repo/issues"

[tool.setuptools.packages.find]
where = ["src"]
```


---


## ✅ 发布前10步检查清单


```markdown
## 📦 发布检查清单 v[VERSION] - [DATE]
DNA: #龍芯⚡️[DATE]-[PACKAGE]-v[VERSION]-发布-UID9622

### Step 1 · 版本号确认
- [ ] 版本号遵循 SemVer（MAJOR.MINOR.PATCH）
- [ ] `pyproject.toml` 版本已更新
- [ ] `__version__` 变量已同步
- [ ] Breaking Change → MAJOR+1；新功能 → MINOR+1；Bug修复 → PATCH+1

### Step 2 · 代码质量
- [ ] `pytest tests/ -v` 全部通过（0 failures）
- [ ] `python -m py_compile your_package/*.py` 无语法错误
- [ ] 代码已通过 Black/flake8 格式检查（可选）

### Step 3 · 文档更新
- [ ] `README.md` 版本号/功能描述已更新
- [ ] `CHANGELOG.md` 已添加本次版本条目
- [ ] API 文档已更新（如有）

### Step 4 · Git 操作
- [ ] 所有变更已 commit（`git status` 无未提交文件）
- [ ] commit message 遵循 Conventional Commits
- [ ] 代码已 push 到 main/orphan_main 分支
- [ ] 创建版本标签：`git tag -a v[VERSION] -m "Release v[VERSION]"  `
- [ ] 推送标签：`git push origin v[VERSION]`

### Step 5 · 构建
```

python -m build


# 生成：dist/your_package-1.0.0.tar.gz


# dist/your_package-1.0.0-py3-none-any.whl


```javascript
- [ ] `dist/` 目录下有 `.tar.gz` 和 `.whl` 文件
- [ ] 包大小合理（无意外包含的大文件）

### Step 6 · TestPyPI 验证（推荐）
```

pip install twine

twine upload --repository testpypi dist/*

pip install --index-url https://test.pypi.org/simple/ your-package-name

python -c "import your_package; print(your_package.version)"


```javascript
- [ ] TestPyPI 上传成功
- [ ] 从 TestPyPI 安装验证功能正常

### Step 7 · 正式发布到 PyPI
```

twine upload dist/*


# 输入 PyPI API Token（不是密码！）


# Username: token


# Password: pypi-xxxxxxxxxxxx


```javascript
- [ ] PyPI 上传成功
- [ ] 访问 https://pypi.org/project/your-package/ 确认版本

### Step 8 · 安装验证
```

pip install your-package-name==1.0.0

python -c "from your_package import main; print('OK')"


```javascript
- [ ] `pip install` 成功
- [ ] 基础功能运行正常

### Step 9 · GitHub Release
- [ ] 在 GitHub 创建 Release（从已推送的 tag）
- [ ] Release Notes 填写（使用 Release Notes 模板）
- [ ] 上传 `.tar.gz` 和 `.whl` 作为 Assets

### Step 10 · 发布通知
- [ ] 更新 CSDN 博客（如有）
- [ ] 更新 Notion 知识库相关页面
- [ ] 社区通知（Discussions / README badge 更新）
- [ ] DNA 追溯码记录本次发布
```


---


## 🔧 一键发布脚本


```bash
#!/bin/bash
# 龍魂 PyPI 发布助手 v1.0
# DNA: #龍芯⚡️2026-08-31-PyPI发布助手-v1.0

set -e  # 任何步骤失败立即停止

VERSION=${1:-"patch"}  # patch / minor / major
PACKAGE=$(python -c "import tomllib; f=open('pyproject.toml','rb'); d=tomllib.load(f); print(d['project']['name'])")

echo "🐉 龍魂 PyPI 发布助手"
echo "📦 包名: $PACKAGE"
echo "🔢 版本: $VERSION"

# 1. 运行测试
echo "\n✅ Step 1: 运行测试..."
pytest tests/ -v --tb=short

# 2. 构建
echo "\n🔨 Step 2: 构建..."
rm -rf dist/ build/ *.egg-info
python -m build

# 3. 检查
echo "\n🔍 Step 3: 检查包..."
twine check dist/*

# 4. 上传
echo "\n🚀 Step 4: 上传到 PyPI..."
twine upload dist/*

echo "\n🎉 发布完成！"
echo "📦 pip install $PACKAGE"
echo "🔗 https://pypi.org/project/$PACKAGE/"
echo "🐉 DNA: #龍芯⚡️$(date +%Y-%m-%d)-$PACKAGE-发布"
```


---


## 📊 龍魂生态包发布状态


---

> 💬 DNA： #龍芯⚡️2026-08-31-PyPI发布清单模板-v1.0-UID9622