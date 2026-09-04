# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂·自动对齐闭环流水线 v2.0 工程文档

**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**DNA**: 由 `bin/lh_dna_generator.py` 生成（干支四柱+卦名，禁止手写）
**运行环境**: 鲲鹏本地，不调用云端

---

## 一、v1.0 → v2.0 修了哪些坑

| # | 问题 | 严重级 | v2.0 处理 |
|:--|:--|:--|:--|
| 1 | `lh_fix_missing_dna.py` 用了 `datetime` 但没 import，一跑就崩 | 🔴 致命 | 已修复，补 import 并重构 |
| 2 | DNA 手写时间戳格式，违反 2026-07-19 新规 | 🔴 合规 | 一律调用 `bin/lh_dna_generator.py`，生成器挂了则跳过告警，绝不写违规DNA |
| 3 | 修复脚本直接覆盖原文件，违反 P0「不删除只冻结」 | 🔴 违宪 | 写入前先备份到 `archive/frozen/*.frozen` |
| 4 | 路由表里有 large_files/unused_imports，但检测分类永不产生 → 死代码 | 🟡 | `classify_issues` 补全六类问题 |
| 5 | subprocess 无超时，检查器卡死拖死整个闭环 | 🟡 | 检查器 600s / 修复 300s 超时兜底 |
| 6 | 缺 `lh_fix_missing_confirm.py`，路由引用了不存在的脚本 | 🟡 | 已补齐 |
| 7 | crontab 无锁，可能并发重入；日志无限膨胀 | 🟡 | flock 防重入 + 日志按周切割 |
| 8 | 修复→验证只跑一轮，修不干净就结束 | 🟡 | 最多迭代 3 轮，仍不干净则退出码 2 告警 |
| 9 | 报告字段 dict/list 类型不一致导致统计错误 | 🟡 | `_as_list()` 统一兼容 |
| 10 | 没有干跑模式，上线即改文件风险高 | 🟡 | 新增 `--dry-run`：只检测给建议，不动文件 |

## 二、闭环流水线

```
检测(align_checker) → 分类+人格路由 → 自动修复 → 验证(重扫) → 归档 → 终端通知
       ↑____________________ 最多迭代3轮 ____________________↓
```

| 阶段 | 做什么 | 谁做 |
|:--|:--|:--|
| ① 检测 | 扫描代码，产出报告 | `lh_align_checker.py` |
| ② 路由 | 六类问题分配人格 | 调度器内置路由表 |
| ③ 修复 | 补DNA/补确认码/合并/拆分/清理 | 鲁班·司马迁·诸葛亮·通心译 |
| ④ 验证 | 重新扫描确认 | `lh_align_checker.py` |
| ⑤ 归档 | 写 `archive/archive_<run_id>.json` | 自动 |
| ⑥ 通知 | 终端彩色输出 + 日志 | 自动 |

## 三、文件清单

```
~/longhun-system/
├── bin/
│   ├── lh_auto_align_daemon.py    # 闭环调度器 v2.0
│   ├── lh_fix_missing_dna.py      # 补DNA v2.0（接生成器+冻结备份）
│   ├── lh_fix_missing_confirm.py  # 补确认码 v1.0（新）
│   ├── lh_align_checker.py        # 检查器（已有）
│   └── lh_dna_generator.py        # DNA生成器（已有，干支+卦名）
├── reports/                       # 检查器报告
├── logs/fixes/                    # 通知日志（按天）
├── logs/auto_align_YYYYWW.log     # cron 日志（按周）
└── archive/
    ├── archive_*.json             # 每次闭环运行归档
    └── frozen/                    # 被修改文件的原版冻结（P0）
```

## 四、部署（复制粘贴执行）

```bash
cd ~/longhun-system
bash deploy_align_loop.sh
```

脚本会：建目录 → 赋权 → 语法自检 → **干跑验证** → 装 crontab（每小时一次，flock 防重入）。

## 五、日常命令

```bash
python3 ~/longhun-system/bin/lh_auto_align_daemon.py            # 手动跑一轮
python3 ~/longhun-system/bin/lh_auto_align_daemon.py --dry-run  # 只看不动手
cat ~/longhun-system/logs/fixes/notifications_$(date +%Y%m%d).log
ls ~/longhun-system/archive/archive_*.json
```

## 六、退出码（给 cron/监控用）

| 码 | 含义 |
|:--|:--|
| 0 | 全部对齐 / 干跑完成 |
| 1 | 检测器或系统错误 |
| 2 | 3轮迭代后仍有未修复项 → 需要人工介入 |

## 七、铁律提醒

- **P0 不删除只冻结**：任何自动修复必须先冻结原版，本流水线已焊死在代码里。
- **DNA 禁止手写**：格式以 `bin/lh_dna_generator.py` 输出为准。
- **先干跑后上线**：新环境第一次部署，务必 `--dry-run` 看一遍再放行。
