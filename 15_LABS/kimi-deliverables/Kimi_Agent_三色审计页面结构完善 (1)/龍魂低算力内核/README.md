# 🐉 龍魂低算力内核 · longhun-core v1.0.0

> 治大国若烹小鲜。——《道德经》第60章
> 大厂告诉你：算力=智能。龍魂告诉你：**你随时可以验证我说的话。**

## 三十秒跑通

```bash
tar -xzf dist/longhun-core-1.0.0.tar.gz
bash install.sh        # 自动自测，看到🟢即成
lh version             # 🐉 longhun-core v1.0.0
lh dna 我的第一行代码    # 打印干支DNA
lh audit --json '{"阻塞率":0.02}'
python3 tools/benchmark_lowpower.py   # 复现实测报告
```

## 实测数据（2026-08-11 沙箱实跑，非估算）

| 指标 | 实测值 |
|:---|:---|
| 内核增量内存 | ≈0–6 MB（纯标准库零依赖） |
| DNA签发吞吐 | 44,875 条/秒 |
| 年轮链落笔 | 11,250 条/秒（篡改即断链🔴） |
| 流式token吞吐 | 327,785 token/秒 |
| 五万条审计记录业务内存 | 32.4 MB |
| 网络依赖 | **零**（断网可跑） |

## 目录

```
core/longhun_core/   五模块内核（dna_trace干支DNA·tricolor_audit三色·historian年轮链·digital_root数字根·flow_control流控）
lh                   命令行
install.sh           一键安装
tools/               实测脚本 + 成本对比器
web/                 可视化看板 + 成本对比页（浏览器直接打开）
docs/                实测报告·节约证明·浪费案例库·5个叙事案例
dist/                发行包 longhun-core-1.0.0.tar.gz（10KB）
```

## 分层许可
思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

🐉 `#龍芯⚡️丙午·丙申·丁巳·丙午·䷟恒-LOW-POWER-BENCH-UID9622`
