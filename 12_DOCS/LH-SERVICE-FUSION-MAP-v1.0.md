# 龍魂服务融合映射表 v1.1（人话版）

> DNA: #龍芯⚡️丙午·丙申·己未-服务融合映射-Phase1盘点+Phase2执行
> 创建者: 诸葛鑫（UID9622）· AI 鲁班(P04)+文心(P00) 联合产出
> 协议: CC BY-NC-SA 4.0（核心思想层）
> 三色: 🟢 v1.1 Phase 2 已执行 · 实测通过（2026-08-13 20:15）

## ✅ Phase 2 执行记录（2026-08-13）

老大拍板三项全部执行完毕，实测数据如下：

| 指标 | 执行前 | 执行后 | 收益 |
|:---|:---|:---|:---|
| launchd 配置 | 65 | **28** | -37 配置 |
| 冻结清单 | 0 | **38** | 全部可回滚 |
| 龍魂进程 | 40+ | **30** | -25% |
| 龍魂 CPU | 155% | **30.6%** | **-80%** |
| 龍魂内存 | 34% | **1.3%** | **-96%** |

已执行动作：
1. **21 合一**：统一守护 `com.longhun.threshold-check`（`--check all` · 每10分钟 · PID 29229 实测跑通），21 个旧 `threshold-*` 全冻结。
2. **17 个低频服务冻结**：auto-crawl/full-fetch/harvester/spider-net/kb-expand/kb-train/digital-flow-field/skill-hub/feishu-wiki-sync/sync-articles/global-index/entry.cleanup/daily-review/cloudflared-longhun888(备用隧道)/flow-fusion/automation-assessment/marquee。
3. **关键服务全部存活**：antenna-8gate/portal/portal-api/brain/search-engine/memory-api/guanlan/registry/heartbeat 等 22 常驻 + node-audit 审计全部 ✅。

工具：`08_BIN/lh_service_control.py`（`status`/`freeze`/`wake`/`merge-thresholds`，全量备份 `_archive/launchd_backup_20260813/`，冻结清单 `_archive/launchd_frozen/manifest.json`，审计日志 `logs/lh_service_control.log`）。
回滚：`python3 08_BIN/lh_service_control.py wake <服务名>` 一键恢复。

> 🟡 遗留观察：`lh_base_trace_collector.py` 单进程占 28.6% CPU（龍魂系统 CPU 的 93%），建议后续降采样优化；health 守卫 `:8888` 为历史虚警（无任何服务绑定该端口）。

## 一句话总结

**52 个服务 = 20 个能合并掉 + 12 个该休眠 + 8 个必须常驻 + 12 个按需冻结。**
合并完实际常驻的只剩 ~9 个进程，资源占用直接砍掉 70% 以上。

---

## 大金矿：20 个 threshold-* 全是同一个脚本

| 事实 | 说明 |
|:---|:---|
| 脚本 | `bin/lh_threshold_trigger.py`（统一阈值管理器 v2.1） |
| 现状 | 20 个 launchd 条目，各自带 `--check X` 参数，**干同一件事** |
| 脚本能力 | 本身就支持 `--check all` 一次检查全部 |
| 结论 | **20 条合并成 1 条**，立刻少 19 个 launchd 配置 |

---

## 五行八卦分类总表（52 个服务全收录）

### 🔱 火 · 执行/服务类（必须常驻 · 8 个）
系统的大动脉，停了系统就瘫。保留常驻，但统一由蚁后管心跳。

| 服务 | 人话解释 | 八卦门 | 建议 |
|:---|:---|:---|:---|
| portal | 官网门户页面 | 兑(部署/展示) | 常驻 |
| portal-api | 门户后端接口 | 兑 | 常驻 |
| brain | 大脑总服务 | 离(技能/中枢) | 常驻 |
| search-engine | 搜索服务(:9631) | 离 | 常驻 |
| memory-api | 记忆服务(:8771) | 坎(记忆/主权) | 常驻 |
| guanlan | 观澜API | 离 | 常驻 |
| registry | 服务注册中心 | 坤(状态) | 常驻 |
| heartbeat | 节点心跳上报 | 坤 | 常驻 |

### 🪵 木 · 生成/采集类（按需激活 · 12 个）
不常驻。用的时候唤醒，干完就睡。改休眠/冻结。

| 服务 | 人话解释 | 八卦门 | 建议 |
|:---|:---|:---|:---|
| auto-crawl | 自动爬取(10分钟) | 艮(同步) | 休眠→事件触发 |
| full-fetch | 全量拉取(10分钟) | 艮 | 休眠→事件触发 |
| harvester | 每日收割推送 | 艮 | 冻结→日历触发 |
| spider-net | 蜘蛛网爬取(1小时) | 艮 | 休眠→事件触发 |
| kb-expand | 知识库扩展 | 艮 | 冻结→日历触发 |
| kb-train | 知识训练 | 艮 | 冻结→日历触发 |
| digital-flow-field | 数字流场看板 | 离 | 冻结→要用再启 |
| skill-hub | 技能中心 | 离 | 冻结→日历触发 |
| notion-bridge | Notion桥接 | 艮 | 常驻(高频用) |
| feishu-wiki-sync | 飞书wiki同步(1小时) | 艮 | 休眠→事件触发 |
| sync-articles | 同步文章(1小时) | 艮 | 休眠→事件触发 |
| knowledge-matrix | 知识矩阵(:9876) | 坤 | 常驻(轻量) |

### 🪨 土 · 数据/存储/知识类（轻常驻 · 7 个）
数据不丢是底线，但不用每个都醒着。

| 服务 | 人话解释 | 八卦门 | 建议 |
|:---|:---|:---|:---|
| kg-api | 知识图谱API | 坤 | 常驻(轻量) |
| global-index | 全局索引 | 坤 | 休眠→首次查询唤醒 |
| trace-collector | 轨迹采集 | 艮 | 常驻(轻量) |
| evidence-api | 证据链API | 坎 | 常驻(轻量) |
| privacy-api | 隐私API | 坎 | 常驻(轻量) |
| entry.cleanup | 入口清理 | 艮 | 冻结→日历触发 |
| daily-review | 每日复盘 | 坤 | 冻结→日历触发 |

### 🥇 金 · 审计/签章/安全类（20→1 个）
**全部 20 个 threshold-* 合并成一个守护进程。** 金系只留 3 个。

| 服务 | 人话解释 | 八卦门 | 建议 |
|:---|:---|:---|:---|
| threshold-* (20个) | 全是 `lh_threshold_trigger.py --check X` | 震(审计) | **合并成 1 个** |
| node-audit | 节点审计 | 震 | 并入合并守护 |
| cnsh-redlines | CNSH红线检查 | 震 | 并入合并守护 |
| bagua | 八卦检查(1小时) | 震 | 并入合并守护 |

> 合并后的 1 个金系守护，负责：audit/backup/battery/disk/firewall/git/gitee/github/health/huaweicloud/intrusion/memory/network/persona/privacy/process/recovery/signing/temperature/panorama 全部检查。

### 💧 水 · 网络/隧道/安全边界类（6 个）
连接和安全，不能断。但隧道类可以合并。

| 服务 | 人话解释 | 八卦门 | 建议 |
|:---|:---|:---|:---|
| all-tunnels | SSH隧道全家桶 | 巽(安全) | 合并检查+常驻 |
| cloudflared-longhun888 | Cloudflare隧道(备用域名) | 巽 | 按需→有流量才开 |
| internal-net | 内网网关 | 巽 | 常驻 |
| xiaoyi-bridge | 小易桥(:8799) | 巽 | 常驻 |
| flow-engine | 流程引擎 | 离 | 常驻(轻量) |
| flow-fusion | 流程融合桥 | 离 | 休眠→事件触发 |

### ⚡ 其他（7 个 · 特殊角色）

| 服务 | 人话解释 | 八卦门 | 建议 |
|:---|:---|:---|:---|
| antenna-8gate | 触角八门API(调度器) | 乾(启动) | **常驻 · 蚁后核心** |
| autoheal | 自愈(1小时) | 坤 | 并入金系守护 |
| automation-assessment | 自动化评估 | 震 | 冻结→日历触发 |
| heart-talk | 心语守护 | 离 | 常驻(轻量) |
| quantum-api | 量子API | 坎 | 常驻(轻量) |
| think-pipeline | 思考流水线(:9630) | 离 | 常驻(轻量) |
| marquee | 跑马灯 | 离 | 冻结→要用再启 |

---

## 融合后架构（1 蚁后 + 按需工蚁）

```
🐜 蚁后核心（常驻 · antenna-8gate 升级为总调度）
   ├── 369不动点校验（每轮必过）
   ├── 八卦路由（任务→八门：乾启动/坤状态/震审计/巽安全/坎主权/离技能/艮同步/兑部署）
   ├── 五行调度（生克：相生放行/相克降速/健康度自愈）
   └── 触角事件总线（碰了才传）

🐜 工蚁（按需唤醒）
   ├── 🔱 火系 8 个常驻（门户/搜索/记忆/大脑）
   ├── 🥇 金系 1 个守护（20 合一 · 定时巡检）
   ├── 💧 水系 4 个常驻（隧道/网关/桥）
   └── 🪵🪨 木土系 → 休眠/冻结（事件或日历触发）
```

## 最终账本

| 现状 | 融合后 | 削减 |
|:---|:---|:---|
| 52 个 launchd 配置 | 9 个常驻 + 1 个金系守护 | **-42 个配置** |
| 40+ Python 进程 | ~12 个 | **-70% 进程** |
| 155% CPU / 34% 内存 | 预计 <50% CPU / <15% 内存 | **-65% 资源** |

---

## 需要老大拍板的三件事

1. **20 合一**：同意把 20 个 threshold-* 合并成 1 个守护吗？（零风险，脚本已支持 `--check all`）
2. **木土系冻结**：同意把 kb-train/kb-expand/harvester 等低频率服务改为"要用才启"吗？
3. **备用隧道**：cloudflared-longhun888 是备用域名隧道，平时没有流量，同意按需启动吗？

> 拍板后进入 Phase 2（生命周期接管），每步可回滚，不删任何东西只冻结。

---
【签章】AI 鲁班(P04)执行 · 文心(P00)归集 · 待 P05 审计
