# LH-OPERATIONS v1.0 · 运维规范
DNA: #龍芯⚡️2026-08-31-LH-OPERATIONS-V1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: MulanPSL v2（工程实现层）

## 运维三色原则
🟢 系统健康·正常运行·无告警
🟡 有警告·可降级运行·需关注
🔴 有故障·服务中断·立即处理

## 日常检查（每日·自动化）

```bash
#!/bin/bash
# 健康检查脚本（加入 crontab: */5 * * * *）
services=(
  "http://localhost:9000/health"
  "http://localhost:8890/health"
  "http://localhost:8897/meter/health"
)
for url in "${services[@]}"; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  if [ "$status" = "200" ]; then
    echo "🟢 $url"
  else
    echo "🔴 $url (HTTP $status)"
    # 触发告警（可接钉钉/企业微信 webhook）
  fi
done
```

## 故障处理流程（SOP）
1. **发现**：告警触发（🔴）
2. **隔离**：确定影响范围，切断故障服务
3. **诊断**：查看日志 `docker logs <container>`
4. **修复**：修复或回滚到上一版本
5. **验证**：验证恢复（🟢）
6. **复盘**：写故障报告，记录 DNA，更新 SOP

## 备份策略
| 数据 | 频率 | 保留 | 位置 |
|---|---|---|---|
| SQLite 数据库 | 每日 | 30天 | OBS/本地 |
| Notion 索引 | 每日 | 7天 | 本地 |
| 配置文件 | 每次变更 | 永久 | Git |
| 密钥（加密后） | 每次变更 | 永久 | 离线介质 |

## 成本控制
- 按量付费服务：每月检查用量·超出预期立即告警
- 不用的 ECS/服务：及时停止（停止不删除，不产生计算费用）
- 流量费用：CDN 回源流量配置缓存策略减少回源
