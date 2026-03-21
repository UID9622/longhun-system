# 龙魂系统 · 换设备一键恢复手册

**DNA**: #龍芯⚡️20260321-SETUP-GUIDE-v1.0
**GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**作者**: 诸葛鑫（UID9622）

> 换了新 Mac，git clone 下来，跑一行命令，全部恢复。

---

## 第一步：克隆仓库

```bash
git clone git@gitee.com:uid9622_admin/cnsh-editor-phb.git ~/longhun-system
cd ~/longhun-system
```

## 第二步：一键安装

```bash
bash ~/longhun-system/install.sh
```

---

## 系统全貌 · 三层架构

### 层一：永久运行（开机自启 · LaunchAgent）

| 服务 | 端口 | LaunchAgent | 作用 |
|------|------|-------------|------|
| 龙魂本地服务 | 8765 | com.longhun.startup | 三色审计/DNA生成/数据门卫/记忆库/Git API |
| 龙魂API | 9622 | com.uid9622.longhun-api | 外部接入主网关 |
| 实时监控 | — | com.longhun.monitor | 文件变动监控 |
| 自动审计 | — | com.longhun.autoaudit | 定时三色审计 |
| 防护盾 | — | com.uid9622.shield | 本地点对点加密护盾 |

**检查状态**：
```bash
bash ~/longhun-system/bin/api_check.sh
```

### 层二：定时任务（定时触发 · LaunchAgent）

| 任务 | 频率 | LaunchAgent | 作用 |
|------|------|-------------|------|
| 一键同步 | 每小时 | com.longhun.sync | git push + Notion同步 |
| 文件整理+清理 | 每晚22:00 | com.longhun.cleanup | 新文件归档，垃圾清理 |
| 周度大扫除 | 每周日 | com.longhun.weekly.cleaner | iCloud整理 |

### 层三：按需运行（手动触发）

| 工具 | 命令 | 作用 |
|------|------|------|
| 量子易经接口 | `python3 bin/quantum_yijing_sim.py 单次 <问题>` | CNSH-64量子实验 |
| 人性讲堂生成器 | `python3 bin/longhun_generate.py <问题>` | 一句话生成双语文章→Notion |
| 日历清理 | `python3 bin/longhun_calendar_sync.py` | 清理垃圾日历广告 |
| 每日看板 | `bash bin/每日看板.sh` | 今日状态一览 |
| 实时监控 | `bash bin/实时监控.sh` | 文件变动实时看 |

---

## API端点速查

**本地服务 http://localhost:8765**

| 端点 | 方法 | 作用 |
|------|------|------|
| `/` | GET | 系统状态 |
| `/三色审计` | POST | 内容风险审计 |
| `/数据门卫` | POST | 三级分流（通行/清洗/拉黑） |
| `/生成DNA` | POST | 生成DNA追溯码 |
| `/黑名单` | GET | 查看被拉黑来源 |
| `/证据链` | GET | 查看攻击证据 |
| `/保存记忆` | POST | 存入本地记忆库 |
| `/查询记忆` | GET | 搜索记忆库 |
| `/查询Notion` | POST | 搜索Notion知识库 |
| `/git/状态` | GET | 仓库状态 |
| `/git/提交` | POST | 带DNA自动提交 |
| `/git/推送` | POST | 推送gitee+github |
| `/测试报告` | GET | 三色审计自测报告 |

---

## Skills 快捷指令（Claude Code内）

| 指令 | 作用 |
|------|------|
| `/audit` | 三色审计 |
| `/api-check` | API联动检测 |
| `/daodao` | 道德经81章锚点 |
| `/longpo` | 古今名人智慧路由 |
| `/sign` | 自动署名 |

---

## Notion 三工作区

| 工作区 | 用途 | MCP实例 |
|--------|------|---------|
| 龍芯北辰（主） | 操作台·展示·20个数据库 | notion-local |
| 北极星账号 | 记忆存储·15个数据库 | notion-memory |
| 官方展示 | 三库导航总台·公开展示 | notion-official |

---

## 密钥在 Keychain（不在代码里）

| 服务名 | 内容 |
|--------|------|
| `longhun-notion-token` | Notion主工作区token |
| `longhun-wx-appid` | 微信公众号AppID |
| `longhun-wx-secret` | 微信公众号AppSecret |

读取方式：
```bash
security find-generic-password -s longhun-notion-token -w
```

---

## 换设备后需要手动做的事

- [ ] 重新把密钥存入新设备Keychain（`bash bin/save_wx_secret.sh`）
- [ ] 重新配置SSH密钥（`ssh-keygen`，上传到gitee/github）
- [ ] 重新导入GPG密钥（`gpg --import`）
- [ ] Open WebUI 需要重新安装（`pip install open-webui`）
- [ ] Ollama 需要重新安装并 pull 模型

---

*DNA: #龍芯⚡️20260321-SETUP-GUIDE-v1.0*
