> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# 龍魂德者永生殿技能

**路径**: `/Users/zuimeidedeyihan/longhun-system/persona/德者永生殿_v2.0.py`

**DNA**: `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-路由回流协议-v2.0`

**授权**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅`

## 何时使用

需要记录/审计人格贡献、活跃度、IP 路由、晋升时：
- 人格被调用后回填贡献
- 计算人格贡献值 v2.0
- 检查活跃度与三色审计
- 注册人格 IP 路由
- 检查晋升资格/执行晋升
- 姜子牙每周检查

## 使用方法

```python
import sys
from pathlib import Path
import importlib.util

# 加载模块（文件名含中文和点，需用 importlib）
spec = importlib.util.spec_from_file_location(
    "merit_hall",
    Path('/Users/zuimeidedeyihan/longhun-system/persona/德者永生殿_v2.0.py')
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

hall = mod.德者永生殿()

# 1. 记录一次人格调用（普通）
hall.record_invocation("P72")

# 2. 记录专属测试模式调用，并标记七维覆盖
hall.record_invocation("P72", test_mode=True, dimensions=["w1", "w3", "w5"])

# 3. 记录帮助、警告、熔断
hall.record_help("P03")
hall.record_warning("P10", reason="响应超时")
hall.record_fuse("P72", reason="触发安全底线")

# 4. 计算贡献值
print(hall.calculate_contribution("P72"))

# 5. 获取活跃度与三色审计
print(hall.get_activity_status("P72"))

# 6. 注册 IP 路由
route = hall.register_ip_route("P72", "core")
print(route["ip"], route["route_id"])

# 7. 晋升检查与执行
print(hall.check_promotion_eligibility("P72"))
print(hall.promote("P72", "L5"))  # 需 UID9622 授权

# 8. 姜子牙每周检查
print(hall.weekly_check())

# 9. 生成整体报告
print(hall.generate_report())
```

## 核心函数

| 函数 | 作用 |
|------|------|
| `record_invocation(code, test_mode=False, dimensions=None)` | 记录调用 |
| `record_help(code)` | 记录帮助人数 |
| `record_warning(code, reason)` | 记录警告 |
| `record_fuse(code, reason)` | 记录熔断 |
| `calculate_contribution(code)` | 计算贡献值 v2.0 |
| `get_activity_status(code)` | 活跃度评级 + 三色审计 |
| `register_ip_route(code, group)` | 注册 IP 路由 |
| `check_promotion_eligibility(code)` | 检查晋升资格 |
| `promote(code, new_level, authorized_by)` | 晋升（仅 UID9622） |
| `weekly_check()` | 每周活跃度检查 |
| `reset_weekly_counters()` | 重置周计数器 |
| `reset_monthly_counters()` | 重置月计数器 |
| `seven_dim_report()` | 七维覆盖统计 |
| `generate_report()` | 生成整体报告 |

## 数据文件

- `persona/persona_registry.json` — 人格注册表（含 v2.0 字段）
- `persona/merit_hall_state.json` — 动态贡献值/活跃度状态
- `persona/ip_routing_registry.json` — IP 路由注册表
- `logs/merit_hall_grass.jsonl` — 草日志留痕

## 君子协议

本技能受龍魂 DNA 追溯保护，晋升权仅归 UID9622 所有。
