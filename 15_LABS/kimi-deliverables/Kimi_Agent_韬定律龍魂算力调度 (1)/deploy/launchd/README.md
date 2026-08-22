# 龍魂·韬定律 macOS launchd 部署示例

DNA：`#龍芯⚡️丙午·乙未·辛酉·甲午·䷫姤-TAO-LAW-INTEGRATED-v2.2`

## 文件清单

| 文件 | 用途 |
|---|---|
| `com.longhun.tao.collector.plist` | 用量采集器守护进程（持续运行） |
| `com.longhun.tao.audit-verifier.plist` | 审计链校验定时任务（每小时一次） |
| `com.longhun.tao.scheduler.plist` | 调度器 API 守护进程（Unix socket，Web UI 入口） |

## 安装步骤

```bash
# 1. 复制 plist 到 LaunchDaemons（需要 root）
sudo cp deploy/launchd/*.plist /Library/LaunchDaemons/

# 2. 修正所有权与权限
sudo chown root:wheel /Library/LaunchDaemons/com.longhun.tao.*.plist
sudo chmod 644 /Library/LaunchDaemons/com.longhun.tao.*.plist

# 3. 创建日志与运行目录
sudo mkdir -p /var/log/longhun /usr/local/longhun/run
sudo chmod 755 /var/log/longhun /usr/local/longhun/run

# 4. 加载服务
sudo launchctl load /Library/LaunchDaemons/com.longhun.tao.collector.plist
sudo launchctl load /Library/LaunchDaemons/com.longhun.tao.audit-verifier.plist
sudo launchctl load /Library/LaunchDaemons/com.longhun.tao.scheduler.plist

# 5. 查看状态
sudo launchctl list | grep com.longhun.tao
```

## Web UI 访问（Unix socket → Nginx 转发示例）

调度器 API 默认监听 Unix socket，浏览器无法直接访问，需通过 Nginx/launchd 转发到 TCP。

```nginx
server {
    listen 8788;
    server_name localhost;

    location / {
        proxy_pass http://unix:/usr/local/longhun/run/tao_scheduler.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

启动 Nginx 后访问：

```
http://127.0.0.1:8788/static/tao-scheduler/index.html
```

如需直接 TCP，修改 `ProgramArguments`：

```xml
<array>
    <string>/usr/local/bin/python3</string>
    <string>/usr/local/longhun/api/tao_scheduler_api.py</string>
    <string>--host</string>
    <string>127.0.0.1</string>
    <string>--port</string>
    <string>8788</string>
</array>
```

## 注意事项

- `tao_usage_collect.py` 在 macOS 上默认使用 `powermetrics`，该命令需要 root 权限，因此采集器必须以 root 运行。
- `powermetrics` 会占用 CPU 约 1-3%，生产环境如需更低开销，可改用 `ioreg` 或电池回路估算，并自行实现 `MacIORegProbe`。
- 审计校验任务若发现断链，会在 `tao_audit_verifier.err` 中输出；建议配合告警脚本转发到龍魂监控体系。
- 调度器 API 的 `HardResourceLimits` 仅作 macOS 近似配额示例；真正的 CPU/cpuset 隔离需配合 cgroups（Linux）或 `taskpolicy`/`ulimit`（macOS）另行实现。
- 路径 `/usr/local/longhun/` 为示例安装根目录，部署时请按实际安装位置修改 plist 中的 `ProgramArguments` 与 `WorkingDirectory`。
