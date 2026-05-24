# UID9622 健康检查系统 V3.6

## 版本信息
- **版本代号**: UID9622-HEALTHCHECK-V3.6
- **生效时间**: 2025-12-24 (GMT+8)
- **等级**: P0
- **确认码**: #P0-HEALTHCHECK-INSTANCE-FORCE-UPDATE-V3.6

## 核心功能

### 1. 健康度四问（P0 自检法）
1. **新手可走通**: 公开中心 → 总入口 → 分支母本
2. **不确定能降级**: 存在拒绝/降级规则（P0+++）
3. **可追溯**: 母本唯一、版本代号、生效时间
4. **本地可 ingest**: 导出后能净化为 dist，并通过验收

### 2. 检测项目
- **PLACEHOLDER_REMAINS**: 占位符残留检测
- **NOTION_TAG**: Notion 标签残留检测  
- **ZERO_WIDTH**: 零宽度字符检测
- **INSTANCE_AGE**: 实例年龄检查（24小时窗口）

## 文件说明

### 核心脚本
1. **uid9622_healthcheck_optimized.py**: 优化后的健康检查器
2. **instance_meta.json**: 实例元数据管理
3. **integrated_health_workflow.sh**: 一键集成工作流

### 运行方式

#### 单独运行健康检查
```bash
# macOS / Linux
python3 uid9622_healthcheck_optimized.py --dist ./dist --meta ./instance_meta.json

# Windows PowerShell
python uid9622_healthcheck_optimized.py --dist .\dist --meta .\instance_meta.json
```

#### 一键完整工作流
```bash
# macOS / Linux
./integrated_health_workflow.sh
```

#### 手动两步骤
```bash
# 步骤1: 净化
python3 uid9622_notion_sanitize.py --in ./notion_export --out ./dist

# 步骤2: 健康检查
python3 uid9622_healthcheck_optimized.py --dist ./dist --meta ./instance_meta.json
```

## 输出说明

### 成功输出
```
[2025-12-24 08:00:00] Scanning 15 markdown files...
Instance age: 12.5 hours
Health report saved to: ./dist/health_report.json
Summary: 15/15 files passed

OK: HEALTHCHECK PASSED
```

### 失败输出
```
FAIL: filename.md
  - PLACEHOLDER_REMAINS
  - ZERO_WIDTH

FAIL: HEALTHCHECK FAILED
Issues found:
  - PLACEHOLDERS: FAIL
  - ZERO_WIDTH: FAIL
```

## 实例治理规则

### 统一原则（最硬规则）
- **PULL ONLY**: 外部实例只允许从母本拉取更新
- **24小时窗口**: 落后超过 24 小时触发强制更新
- **无人理照样执行**: 超时不处理 = 自动/远程强制更新

### 安全机制
- 更新包必须签名或哈希验证
- 失败更新必须回滚
- 强制更新只触及规则/配置/提示，绝不碰用户私人数据

## 故障处理

### PLACEHOLDER 问题
- **原因**: Notion 占位符未完全净化
- **解决**: 重新运行 sanitize 脚本
- **影响**: 不建议喂给 CodeBuddy

### NOTION_TAG 问题  
- **原因**: Notion 结构化标签残留
- **解决**: 增强 sanitize 规则
- **影响**: 可能导致 AI 读取断片

### ZERO_WIDTH 问题
- **原因**: 隐藏字符污染
- **解决**: 字符级净化处理
- **影响**: 容易导致检索错乱

## 集成配置

### 定时任务设置
```bash
# 每小时检查一次
0 * * * * /path/to/integrated_health_workflow.sh

# 或使用 crontab -e 添加
```

### CI/CD 集成
```yaml
# GitHub Actions 示例
- name: Run Health Check
  run: |
    python3 uid9622_healthcheck_optimized.py --dist ./dist
```

## 最佳实践

1. **每次导出后**: 立即运行完整工作流
2. **发布前**: 确认健康检查 PASSED
3. **定期检查**: 设置定时任务自动执行
4. **版本管理**: 保留健康检查报告用于审计

## 紧急联系

如果遇到无法解决的健康检查问题，请检查：
1. instance_meta.json 格式是否正确
2. dist 目录是否完整
3. Python 依赖是否满足要求
4. 文件权限是否正确设置

---

**P0+++ 安全标准**: 绝不容忍任何形式的内容污染，确保本地 AI 处理环境的纯净性。