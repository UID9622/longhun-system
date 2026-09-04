# 龍魂项目 `.gitignore` 模板 v1.0

> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 用途: 新项目复制本文件为 `.gitignore`，自动继承「生成物不入库」规则（与 `lh publish pr` 生成物白名单联动）。
> DNA: #龍芯⚡️2026-09-04-GITIGNORE-TEMPLATE-v1.0

复制以下整段即可：

```gitignore
# ── 龍魂生成物白名单（与 lh publish pr 的 GENERATED_SEGMENTS 联动·自动排除不入 PR）──
# 生成物目录（可再生成·不入库·--include-generated 可强制纳入）
site/
html_assets/
dist/
dist_ide/
build/
build_ide/
models/
weights/
_work/
backups/
backup/
__pycache__/
.venv/
node_modules/

# 生成物后缀
*.pyc
*.pyo
*.pid
*.tmp
.DS_Store
*.log

# ── 龍魂约定 ──
# 操作日志等动态文件不入 git（07_AUDIT/*.log）
# 守护状态心跳等运行时文件
```

设计原则:
1. **同名段与 `lh_publish.py` `GENERATED_SEGMENTS` / `GENERATED_SUFFIXES` 保持同步**——
   改生成物白名单时两处一起改（单点真源: `lh_publish.py` 常量）。
2. `--include-generated` 场景（首次发版需打包产物）用 `git add -f` + `lh publish pr --include-generated`。
3. `.asc`（GPG 签名）**永远不入 gitignore**——签名随源文件入库。
4. 所有新项目初始化时: 复制本模板 → `.gitignore`，即自动继承「site/dist/pyc 不入库」铁律。
