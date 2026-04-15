# 龍魂系统快速参考卡

## 启动命令

```bash
# 一键启动全部
bash start.sh

# 仅启动API服务器
python3 main.py

# 注册所有DNA
python3 register_all_dna.py

# 启动清道夫守护（每小时扫描）
python3 sweeper_daemon.py 3600

# 系统测试
python3 test_system.py
```

## Claude快捷函数

```python
from claude_client import *

# DNA确权
dna_create("概念名", "内容")

# 嵌入水印
dna_embed("内容", "DNA码")

# 追踪查询
dna_trace("DNA码")

# 提取水印
dna_extract("内容")

# 清道夫扫描
sweeper("DNA码")

# 生成证据包
confront("DNA码")

# 获取证据链
evidence("DNA码")
```

## API端点

| 功能 | 端点 | 方法 |
|------|------|------|
| DNA创建 | `/yang/create` | POST |
| DNA嵌入 | `/yang/embed` | POST |
| DNA追踪 | `/yin/trace/{dna}` | GET |
| DNA提取 | `/yin/extract` | POST |
| 清道夫扫描 | `/sweeper/scan` | POST |
| 微信配置 | `/wechat/config` | POST |
| 生成证据包 | `/confront/generate` | POST |
| 下载证据 | `/confront/download/{id}` | GET |
| 证据链 | `/evidence/chain/{dna}` | GET |
| 黑名单 | `/audit/blacklist` | GET |

## DNA码格式

```
#龍芯⚡️{timestamp}-{type}-{hash}

示例:
#龍芯⚡️2026-03-20-150045-system-a1b2c3d4
```

## CNSH预警级别

| 级别 | 代码 | 说明 |
|------|------|------|
| 48小时警告 | CNSH-48H | 整改期 |
| 全网警报 | CNSH-ALERT | 公开通报 |
| 永久黑名单 | CNSH-PERMANENT | 终身封禁 |

## 文件位置

```
/mnt/okcomputer/output/longhun_api/
```

## 关键DNA追溯码

- 系统: `#龍芯⚡️2026-03-20-LONGHUN-API-v1.0`
- 构建指南: `#龍芯⚡️2026-03-05-BUILD-GUIDE-FOR-AI`
- 资源清单: `#龍芯⚡️2026-03-09-RESOURCE-INVENTORY`
- 规则覆盖: `#龍芯⚡️2026-03-09-RULE-COVERAGE-CHECK`
- 规则钩子: `#龍芯⚡️2026-03-09-RULE-HOOKS-DESIGN`

---

**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
