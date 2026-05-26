# CNSH Fixed Point Runtime

## Fixed modules
- `fixed_points.py`: 主权不动点常量
- `tongxinyi_core.py`: 通心译（情绪-意图净化）
- `cnsh_core_engine.py`: CNSH主干路由（闸门/三重检测/抽屉/状态）
- `integration_runtime.py`: 通心译 + CNSH + 审计链集成入口

## Run
```bash
python3 longhun-system/longhun-runtime/runtime/cnsh_fixed_point/integration_runtime.py
```

## Event
- `cnsh_fixed_point_pipeline`
