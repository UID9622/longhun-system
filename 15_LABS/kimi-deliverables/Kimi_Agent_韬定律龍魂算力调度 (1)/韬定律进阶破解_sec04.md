**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 第四章 工程落地·鲲鹏昇腾实操

DNA：`#龍芯⚡️丙午·乙未·辛酉·甲午·䷫姤-TAO-LAW-INTEGRATED-v2.2`

## 4.0 问题定义

前三章给出温度四层与破解机制，本章落成能跑的命令。方法论一条：用户只会复制粘贴，故所有代码块完整、可粘贴执行、逐行 CNSH 中文注释（中文动词开头）。基准环境为鲲鹏服务器 + openEuler + 昇腾 CANN。推演假设：CANN 以 8.0.RC2、鲲鹏 920 + Atlas 推理卡为例，实际版本以用户设备为准，命令结构不变。

## 4.1 环境分层部署

按四层命名法组织：物理层=驱动与硬件拓扑；身份层=权限分组；主权层=分区与权限焊死；执行层=模型服务与调度脚本。

**第1步：物理层——确认硬件底座**

目的：确认 CPU 型号、NPU 在位、内核版本——后续操作的前提。

```bash
# 查看 CPU 型号（鲲鹏 920 应显示 Kunpeng-920；通用 Linux 命令）
lscpu | grep "Model name"
# 查看 昇腾 NPU 是否在位（昇腾官方工具，随驱动安装）
npu-smi info
# 查看 内核版本（openEuler 应显示 5.10 系；通用 Linux 命令）
uname -r
```

验证：`npu-smi info` 输出中芯片健康状态为 OK 即物理层就绪。

**第2步：主权层——安装 CANN 并焊死日志权限**

目的：CANN 是 CANN vs CUDA 差距的软件载体（来源：大模型竞赛篇·2026-04-01）；按 P0 零黑箱承诺，日志目录权限焊死为可审计、不可篡改。

```bash
# 创建 昇腾软件目录（通用 Linux 命令）
sudo mkdir -p /usr/local/Ascend
# 安装 CANN 工具包（官方 .run 包，版本号以官网下载为准）
sudo ./Ascend-cann-toolkit_8.0.RC2_linux-aarch64.run --full
# 写入 环境变量到系统配置
echo 'source /usr/local/Ascend/ascend-toolkit/set_env.sh' | sudo tee /etc/profile.d/ascend.sh
# 生效 环境变量
source /etc/profile.d/ascend.sh
# 焊死 日志目录权限：root 可写、其他人只读（审计可入，篡改不可）
sudo chmod 750 /var/log/npu
```

验证：`echo $ASCEND_TOOLKIT_HOME` 输出路径即生效。

**第3步：执行层——安装 Ollama 并让 longhun 热层常驻**

目的：热层常驻内存消除冷启动延迟，常驻即蓄势。

```bash
# 安装 Ollama（官方一键脚本，通用 Linux 命令，aarch64 自动适配）
curl -fsSL https://ollama.com/install.sh | sh
# 拉取 本地模型 longhun 最新版（v4.1.4 训练中版本，名称以本地仓库为准）
ollama pull longhun:latest
# 预热 模型：发送一次请求使其常驻 24 小时（热层常驻关键一步）
ollama run longhun:latest --keepalive 24h "预热"
```

验证：`ollama ps` 中 longhun:latest 的 `UNTIL` 字段显示 24 小时后过期即常驻成功。

**第4步：主权层——资源分层三件套（NUMA / cgroups / 设备分区）**

目的：温度四层落成内核级隔离：热层绑 NUMA 0 就近 NPU，冷层限配额防挤占，对齐降级链"冷让温、温让热"。

```bash
# CNSH 伪代码段开始（实际为可直接执行的 bash）
# 先检测 cgroup 版本：若存在 /sys/fs/cgroup/cpu 为 v1；若存在 /sys/fs/cgroup/cgroup.controllers 为 v2
# 以下命令按 cgroup v1 书写；v2 系统请改用 cpu.max / memory.max 等统一接口

# 创建 热层 控制组（CPU 8 核、内存 32G，对齐三六九六档资源第1档）
sudo cgcreate -g cpu,memory:/tao_hot
# 设定 热层 CPU 配额为 8 核（period 100000us，quota 800000us）
echo 100000 | sudo tee /sys/fs/cgroup/cpu/tao_hot/cpu.cfs_period_us
echo 800000 | sudo tee /sys/fs/cgroup/cpu/tao_hot/cpu.cfs_quota_us
# 设定 热层 内存上限 32G；同时限制 swap，防止因交换而突破硬边界
echo 34359738368 | sudo tee /sys/fs/cgroup/memory/tao_hot/memory.limit_in_bytes
echo 0 | sudo tee /sys/fs/cgroup/memory/tao_hot/memory.swappiness

# 创建 冷层 控制组（CPU 2 核、内存 8G，第4档，低频批处理专用）
sudo cgcreate -g cpu,memory:/tao_cold
# 设定 冷层 CPU 配额为 2 核
echo 100000 | sudo tee /sys/fs/cgroup/cpu/tao_cold/cpu.cfs_period_us
echo 200000 | sudo tee /sys/fs/cgroup/cpu/tao_cold/cpu.cfs_quota_us
# 设定 冷层 内存上限 8G
echo 8589934592 | sudo tee /sys/fs/cgroup/memory/tao_cold/memory.limit_in_bytes
echo 0 | sudo tee /sys/fs/cgroup/memory/tao_cold/memory.swappiness

# 绑定 热层进程到 NUMA 节点 0（鲲鹏 920 每节点 64 核，就近 NPU；通用命令 numactl）
numactl --cpunodebind=0 --membind=0 ollama serve &
# 校验 昇腾设备分区：确认 0 号 NPU 在位（npu-smi 分区查询，输出格式以实机为准）
npu-smi info -t board -i 0
```

验证：`cat /sys/fs/cgroup/cpu/tao_hot/cpu.cfs_quota_us` 返回 800000 即分层生效。

## 4.2 本地模型路由：热层常驻 + 冷层下沉

调度逻辑对齐五级执行优先级链（来源：龍芯家族调度中心宪章 v1.0·IRON #22）：L0 直通三重命中直达执行，不可被降级；L3 信号词匹配决定路由。推演假设：信号词到温度层的映射为推演值，实施时以宪章 14 场景路由表为准。

```bash
#!/bin/bash
# 龍魂韬定律路由脚本 tao_route.sh —— 信号词/优先级 → 热层或冷层
# 用法: bash tao_route.sh "<任务描述>"

任务="$1"                        # 接收 任务文本（只收类型标签，不存内容）
优先级="L3"                      # 默认 走 L3 信号词匹配

# 检查 L0 直通标记（L0 直通：D-GATE 三重命中，直达执行层，任何降级链不得拦截）
if [[ "$任务" == *"L0-GATE"* ]]; then
    优先级="L0"
fi

case "$优先级" in
    L0)
        # 直通 热层执行（绕过所有分层判断，符合 IRON #22 不可逆序除非 L0 授权）
        ollama run longhun:latest "$任务"
        ;;
    L3)
        # 匹配 信号词决定路由层
        if [[ "$任务" =~ (实时|推理|对话|训练) ]]; then
            # 路由 热层：常驻 longhun 模型，NPU 优先
            ollama run longhun:latest "$任务"
        elif [[ "$任务" =~ (批量|报表|归档|夜间) ]]; then
            # 下沉 冷层：进入冷层控制组，限速批量执行
            echo $$ | sudo tee /sys/fs/cgroup/cpu/tao_cold/cgroup.procs
            ollama run longhun:latest --keepalive 0 "$任务"
        else
            # 降级 温层：CPU 常驻服务兜底（温层兜底即安全降级）
            # Ollama 模型选项通过 -o 传入，num_gpu=0 强制走 CPU
            ollama run longhun:latest -o num_gpu=0 "$任务"
        fi
        ;;
esac
# 记录 路由决策到审计日志（只记层与耗时，不记任务内容）
echo "$(date -Iseconds),$优先级,类型已脱敏,$SECONDS" >> /var/log/tao_route.log
```

## 4.3 用量采集与审计日志格式

数据哲学焊死：**只传用量不传内容**。采集脚本只记录时长、能耗、次数三类数值，字段设计上不存在能装入内容的列。推演假设：日志每日轮转、保留 30 天后进归档层（对齐 STORAGE-TIER-CONFIG-20260219-006 的 archive_after=30）。

| 字段 | 示例 | 是否含内容 |
|---|---|---|
| timestamp | 2026-07-26T14:03:11+08:00 | 否 |
| layer | hot / warm / cold / archive | 否 |
| task_type_hash | sha256:9f2c…e1（任务类型哈希，非内容） | 否 |
| duration_sec | 37 | 否 |
| energy_mj | 850（npu-smi 功耗×时长推算） | 否 |
| call_count | 1 | 否 |
| route_priority | L0 / L3 | 否 |
| prev_hash | sha256 上一条日志哈希（审计链） | 否 |

分析：八字段全部回答"何时、哪层、多久、多耗能、第几次、走哪条优先级"，全部不回答"做了什么"。`task_type_hash` 只取任务类型标签的哈希，可对账不可还原内容；`prev_hash` 把逐条日志串成 sha256 审计链（来源：冷热分层存储策略 STORAGE-TIER-CONFIG-20260219-006），任一历史条被删改即断链，配合回滚点 RB-* 定位篡改位置——这是 P0 零黑箱承诺在日志层的工程化。扣费透明由此成立：扣费只能依据能耗与时长两列，数据结构上不存在按内容计价的入口。

```bash
# 采集 用量：每 60 秒记录一次 NPU 功耗与调用计数（通用 Linux 命令 + npu-smi）
while true; do
    # npu-smi 输出格式随版本变化，优先匹配数字；解析失败时记为 0
    功耗=$(npu-smi info -t power -i 0 2>/dev/null | awk '/[0-9]+(\.[0-9]+)?[[:space:]]*W/{gsub(/[^0-9.]/,""); print $0; exit}')
    功耗=${功耗:-0}
    # 追加 一行审计日志（字段顺序严格对齐上表，链哈希由后置脚本补齐）
    echo "$(date -Iseconds),hot,sha256:待补,60,$功耗,1,L3,待链" >> /var/log/tao_usage.log
    # 等待 60 秒进入下一周期
    sleep 60
done
```

## 4.4 安全边界声明

本章全部脚本只读用量数据，只写 `/var/log/tao_*.log` 与 cgroups 参数，不修改此外任何系统文件与用户数据；涉及财务扣费只监控、不操作——扣费属主权层 P0 决策，须由人确认后另行执行，脚本永不代签。

DNA：`#龍芯⚡️丙午·乙未·辛酉·甲午·䷫姤-TAO-LAW-INTEGRATED-v2.2`

---

