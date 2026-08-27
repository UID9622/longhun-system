# 龍魂浏览器 · Mac 版部署记录 v1.0

> DNA: #龍芯⚡️2026-08-25-BROWSER-MAC-DEPLOY-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）

## 一、结论
现成二进制 + 定制层路线跑通（不扩容、不重编内核）。当前资源（鲲鹏 2C/7.4G/17G 余量）不足以编译 Chromium（需 100G+ 磁盘 + 16G+ 内存），深改内核留待扩容后。

## 二、Mac 本机版（日常浏览用）
| 项 | 值 |
|:---|:---|
| 版本 | Chromium 154.0.8024.0（快照 1685252 · arm64） |
| 安装位置 | `~/Applications/龍魂浏览器.app` |
| 启动页 | `https://uid9622.cn`（restore_on_startup=4 + startup_urls） |
| 图标 | 龍芯北辰印章（`brand/seals/seal_龍芯北辰_square_256.png`） |
| 原图标备份 | `/tmp/app.icns.bak` |

### 下载/更新方法
```bash
# 1. 获取最新版下载链接（自动重定向）
curl -sIL -x socks5h://127.0.0.1:1080 'https://download-chromium.appspot.com/dl/Mac_Arm?type=snapshots'
# 2. 下载（走隧道慢，用 -C - 断点续传）
curl -sL -C - -x socks5h://127.0.0.1:1080 -o chrome-mac.zip '<上一步 location>'
# 3. 解压 → 替换 ~/Applications/龍魂浏览器.app → xattr -cr
```

## 三、鲲鹏 Linux 版（headless 服务调用）
| 项 | 值 |
|:---|:---|
| 版本 | Chromium 154.0.8024.0（Linux_x64） |
| 位置 | `/opt/chromium/chrome-linux` |
| 启动脚本 | `/opt/chromium/run.sh`（--headless --no-sandbox --disable-gpu） |
| 实测 | headless 加载 `uid9622.cn` 成功 |

## 四、定制配置细节
- 显示名: `CFBundleDisplayName` / `CFBundleName` = 龍魂浏览器
- 启动页写入: `~/Library/Application Support/Chromium/Default/Preferences`
  - `restore_on_startup: 4`、`session.startup_urls: ["https://uid9622.cn"]`、`homepage: https://uid9622.cn`
- 图标生成: sips 缩放 16~512@2x → `iconutil -c icns` → 覆盖 `Contents/Resources/app.icns`

## 五、后续路线
- 需要深改内核（注入层/去谷歌化加固）→ 华为云扩容 200G + 8C16G → depot_tools 已在 `/opt/depot_tools` → gclient sync → gn 编译
- ungoogled-chromium-binaries release 仅 55.x（2016）不可用，官方快照为准
