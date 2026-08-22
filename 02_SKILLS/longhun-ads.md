# 🐉 龍魂·自描述子系统 ADS v4.0

**DNA:** `#龍芯⚡️丙午·丙申·丙寅·乙未·䷣明夷-SELF-DESCRIBING-SYSTEM-v4.0-UID9622`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**License:** MulanPSL v2（工程实现层）· 思想层 CC BY-NC-SA 4.0

## 触发词
`ads` · `自描述` · `自指` · `四层认知` · `self-describing` · `自省` · `系统自述` · `我是谁` · `你现在什么状态`

## 是什么
自描述子系统（ADS, Self-Describing Subsystem）——让系统"说清楚自己是谁、在做什么、状态如何"的递归认知层。
四层递归自指认知：L1感知 → L2认知 → L3元认知 → L4自指。
六角色：自省者/历史学家/解释者/诊断者/边界守卫/进化者。

## 快速使用
```bash
# 四层自描述（需确认码闸门）
python3 bin/lh_self_describing.py --describe --confirm "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 健康检查
python3 bin/lh_self_describing.py --health --json

# 六角色
python3 bin/lh_self_describing.py --roles

# 内置自检（6组锚点断言）
python3 bin/lh_self_describing.py --test

# REST API（常驻服务，端口 9626）
python3 bin/lh_self_describing.py --api --port 9626
# 路由: GET /api/v1/health · /api/v1/describe · /api/v1/roles · 需 ?confirm=<确认码>
```

## 端口
**9626**（9622 被 backend 统一 API 占用，ADS 已改 9626）

## 部署
- **Mac launchd**: `deploy/launchd/com.longhun.ads.plist` → `launchctl bootstrap gui/$(id -u)`
- **鲲鹏 systemd**: `deploy/systemd/longhun-ads.service`
- **Docker**: `deploy/docker/Dockerfile.ads`
- 数据主权本地: `~/.longhun/ads/`（SQLite + JSON 双轨，绝不出境）

## 协议 & 测试
- 协议: `01_protocols/LH-ADS-SELF-DESCRIBING-v4.0.md`
- 测试: `python3 tests/test_lh_self_describing.py`（6组锚点断言）
- 命令总目: `.codebuddy/COMMAND_INDEX.md`

## 诚实局限
- 分布式协调/多实例事件总线未测（🟡）
- i18n 多语言钩子预留，翻译未提供（🔴）
- 插件系统动态加载未实现（🔴）
