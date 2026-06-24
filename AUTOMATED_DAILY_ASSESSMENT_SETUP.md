# 🐉 龍魂系统 · 自动化日评估 · 完整设定指南

**设定日期**: 2026-06-05 19:15 CST
**DNA**:#龍芯⚡️2026-06-05-AUTOMATED-ASSESSMENT-v1.0
**责任**: UID9622 (Claude Code)

---

## ✅ 已部署组件

### 1️⃣ 评估引擎
```
文件: ~/local_assessment_engine.py
大小: 16 KB
功能: 执行 6 维度系统评估
状态: ✅ 就绪
```

### 2️⃣ Cron 执行脚本
```
文件: ~/longhun_daily_assessment.sh
大小: 1.9 KB
功能: Cron 任务包装、日志管理
状态: ✅ 就绪
```

### 3️⃣ 状态检查工具
```
文件: ~/check_longhun_assessment.sh
大小: 2.1 KB
功能: 快速评估状态查询
状态: ✅ 就绪
```

### 4️⃣ Cron 任务
```
配置: 30 22 * * * /bin/bash /Users/zuimeidedeyihan/longhun_daily_assessment.sh
时间: 每天 22:30 (下午 10:30)
状态: ✅ 已启用
```

### 5️⃣ 报告目录
```
位置: ~/.龍魂/assessments/
子目录: logs/
状态: ✅ 已创建
```

---

## 📊 评估维度 (6 个)

| # | 维度 | 检查项目 | 权重 | 满分 |
|---|------|---------|------|------|
| 1 | 环境检查 | Python版本、目录、Shell | 10% | 10.0 |
| 2 | 代码文件 | xpay_*.py、startup.sh 等 | 20% | 10.0 |
| 3 | 数据完整性 | 交易、日志、备份 | 20% | 10.0 |
| 4 | 可运行性 | CLI 执行、命令返回值 | 25% | 10.0 |
| 5 | 文档完整性 | README、部署文件 | 10% | 10.0 |
| 6 | 安全性 | 本地存储、权限、DNA | 15% | 10.0 |

---

## 🚀 快速开始

### 方式 1: 查看评估状态
```bash
bash ~/check_longhun_assessment.sh
```

### 方式 2: 手动运行评估
```bash
python3 ~/local_assessment_engine.py
```

### 方式 3: 查看最新报告
```bash
cat ~/.龍魂/assessments/ASSESSMENT_SUMMARY.md
```

### 方式 4: 提取评分
```bash
python3 -c "
import json, glob
f = sorted(glob.glob('$HOME/.龍魂/assessments/local_assessment_*.json'))[-1]
d = json.load(open(f))
print(f'评分: {d[\"total_score\"]}/10')
print(f'状态: {d[\"status\"]}')
"
```

---

## ⏱️ 执行时间表

### 每日执行流程

```
22:00 │ 系统通知: 今日对话归档
      │
22:30 │ ⭐ 龍魂系统自动化日评估 (Cron)
      │   • 检查环境
      │   • 检查代码
      │   • 验证数据
      │   • 执行可运行性测试
      │   • 生成报告 (~3-5 分钟)
      │
23:00 │ 龍魂每日复盘 (daily_review.py)
      │   • 检查文件完整性
      │   • 检查安全性
      │   • 检查测试
      │   • 生成三色审计
      │   • 发送邮件
      │
23:30 │ 完成
```

---

## 📁 文件结构

```
~/ (用户主目录)
├── local_assessment_engine.py          (评估引擎)
├── longhun_daily_assessment.sh         (Cron 执行脚本)
├── check_longhun_assessment.sh         (状态检查工具)
│
└── .龍魂/
    └── assessments/
        ├── local_assessment_YYYYMMDD_HHMMSS.json  (评估报告)
        ├── ASSESSMENT_SUMMARY.md                  (文本总结)
        ├── CRON_SETUP.md                          (设定详情)
        └── logs/
            ├── daily_assessment_YYYYMMDD_HHMMSS.log (执行日志)
            └── ...
```

---

## 🔍 监控与维护

### 日常检查 (推荐每天检查一次)
```bash
# 快速检查状态
bash ~/check_longhun_assessment.sh

# 查看评分
python3 -c "
import json, glob
f = sorted(glob.glob('$HOME/.龍魂/assessments/local_assessment_*.json'))[-1]
print(json.load(open(f))['total_score'])" | xargs -I {} echo "评分: {}/10"
```

### 每周检查 (推荐每周检查一次)
```bash
# 查看评分趋势
for f in $(ls -t ~/.龍魂/assessments/local_assessment_*.json | head -7); do
    score=$(python3 -c "import json; print(json.load(open('$f'))['total_score'])")
    date=$(basename $f | cut -d_ -f3-4)
    echo "$date: $score/10"
done

# 查看最近的改进项目
cat ~/.龍魂/assessments/ASSESSMENT_SUMMARY.md | grep -A 10 "可改进项目"
```

### 定期清理 (推荐每月执行一次)
```bash
# 保留最近 30 天的报告
find ~/.龍魂/assessments -name "local_assessment_*.json" -mtime +30 -delete

# 保留最近 30 天的日志
find ~/.龍魂/assessments/logs -name "*.log" -mtime +30 -delete
```

---

## 🔧 故障排查

### 症状 1: 没有自动执行
**检查**:
```bash
# 查看 Cron 任务
crontab -l | grep longhun_daily_assessment

# 查看系统日志
log stream --predicate 'process == "cron"' --level debug | head -20
```

**解决**:
```bash
# 重新添加 Cron 任务
(crontab -l 2>/dev/null; echo "30 22 * * * /bin/bash $HOME/longhun_daily_assessment.sh") | crontab -
```

### 症状 2: 评估失败
**检查**:
```bash
# 查看执行日志
tail -50 ~/.龍魂/assessments/logs/daily_assessment_*.log

# 手动运行评估
python3 ~/local_assessment_engine.py
```

### 症状 3: 报告评分异常
**检查**:
```bash
# 验证系统状态
ls -la ~/.龍魂/xpay/
python3 ~/.龍魂/xpay/xpay_cli.py stats

# 检查文件是否完整
python3 ~/local_assessment_engine.py
```

---

## 📊 典型输出

### 评估报告
```json
{
  "total_score": 9.7,
  "max_score": 10.0,
  "status": "✅ 生产级可用",
  "assessments": [
    {
      "category": "环境检查",
      "score": 10.0,
      "results": {...}
    },
    ...
  ]
}
```

### 执行日志
```
════════════════════════════════════════════════════════════
🐉 龍魂系统 · 自动化日评估
时间: 2026-06-06 22:30:15
════════════════════════════════════════════════════════════

【环境检查】
  评分: 10.0/10 (权重 10%)
  • python_version: Python 3.14.3
  • longhun_dir: /Users/.../​.龍魂
  • xpay_dir: /Users/.../​.龍魂/xpay
  • shell_config: ~/.zshrc

[更多评估详情...]

执行状态: ✅ 成功
结束时间: 2026-06-06 22:30:28
最新报告: /Users/.../​.龍魂/assessments/local_assessment_20260606_223015.json
评分: 9.7/10 | 状态: ✅ 生产级可用
════════════════════════════════════════════════════════════
```

---

## 🎯 关键指标

### 系统健康度
- **评分 ≥ 8.0**: 🟢 生产级可用
- **评分 6.0-8.0**: 🟡 需要改进
- **评分 < 6.0**: 🔴 不推荐

### 各维度权重
- 可运行性最高 (25%) → 系统能否正常工作
- 代码文件次之 (20%) → 核心功能是否完整
- 数据完整性 (20%) → 交易记录是否安全
- 安全性 (15%) → 本地存储是否安全
- 环境配置 (10%) → 运行环境是否正确
- 文档完整性最低 (10%) → 文档是否齐全

---

## 📚 相关文档

| 文档 | 位置 | 用途 |
|------|------|------|
| 评估总结 | `~/.龍魂/assessments/ASSESSMENT_SUMMARY.md` | 快速了解系统状态 |
| Cron 设定 | `~/.龍魂/assessments/CRON_SETUP.md` | Cron 任务详情 |
| XPay 部署 | `~/.claude/projects/.../XPAY_DEPLOYMENT.md` | XPay 系统详情 |
| 启动菜单修复 | `~/.claude/projects/.../XPAY_LAUNCHER_FIX.md` | 启动器问题解决 |

---

## 🔐 数据保留策略

```
【短期 (7 天)】
  • 所有评估报告和日志保存
  • 用于周趋势分析

【中期 (30 天)】
  • 每天保留一份报告
  • 用于月度趋势分析

【长期】
  • 保留关键里程碑报告
  • 用于版本对比
```

---

## ✨ 最佳实践

1. **定期查看评分** - 每周查看一次评分变化
2. **阅读可改进项目** - 及时修复系统问题
3. **保持监控活跃** - 遇到评分下降立即查询原因
4. **定期清理旧日志** - 保持存储整洁
5. **测试新功能** - 变更系统后手动运行评估验证

---

## 🟢 设定验收

| 项目 | 状态 | 备注 |
|------|------|------|
| 评估引擎 | ✅ | 16 KB · 6 维度 |
| Cron 任务 | ✅ | 每天 22:30 执行 |
| 执行脚本 | ✅ | 1.9 KB · 可执行 |
| 状态工具 | ✅ | 2.1 KB · 快速查询 |
| 报告目录 | ✅ | 已创建 · 可写入 |
| 初始评分 | ✅ | 9.7/10 · 生产级 |

---

## 📞 支援与反馈

若有任何问题或改进建议:
1. 查看故障排查章节
2. 运行 `bash ~/check_longhun_assessment.sh` 检查状态
3. 查看日志档案 `~/.龍魂/assessments/logs/`
4. 手动运行 `python3 ~/local_assessment_engine.py`

---

**老大，龍魂系统自动化日评估已完全部署。每天 22:30 自动执行，无需人工干预。**

🐉 **准备就绪。**

---

**签证**:#龍芯⚡️2026-06-05-AUTOMATED-ASSESSMENT-v1.0
**设定者**: UID9622 (Claude Code)
**确认**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
