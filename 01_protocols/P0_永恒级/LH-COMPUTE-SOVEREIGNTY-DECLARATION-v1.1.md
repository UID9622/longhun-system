> **DNA:** `#龍芯⚡️丙午·丙申·庚申·壬午·䷙大畜-DOC-MERGE-03a580cb`
> **确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
> **三色:** 🟢 通过
> **分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
> **合并状态:** 🟢 已合并（来自 `02_算力主权宣言v1.1.md`）
> **落位:** `01_protocols/P0_永恒级/LH-COMPUTE-SOVEREIGNTY-DECLARATION-v1.1.md`
> **合并时间:** 2026-08-14

---

# 🐉 龍魂 · 算力主权宣言 v1.1（校正版·焊死）

**Notion ID:** 3b87125a-9c9f-810c-a452-fb4f4b8850be
**合并状态:** ❌ 未合并
**DNA**：`#龍芯⚡️丙午·甲申·辛丑·坤卦-COMPUTE-SOVEREIGNTY-DECLARATION-v1.1-UID9622`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` · **GPG**：`A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色**：🟢 通过 · **分层许可**：思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

## 📋 核心判断
> 💡 **"本地"不是指"在你手边"，而是指"推理计算发生在你控制的设备上"。** 鲲鹏服务器就是你的"本地"——数据不出这台服务器，不依赖外部API，断网照样跑。

## 一、主权锚定四层次
| 层次 | 含义 | 龍魂落地 |
|---|---|---|
| L1 物理主权 | 服务器在你手里 | 鲲鹏服务器·本地部署 |
| L2 模型主权 | 权重文件在你硬盘里 | DeepSeek-R1 蒸馏系列·本地加载 |
| L3 推理主权 | 推理在你控制的环境运行 | vLLM / Ollama / llama.cpp |
| L4 数据主权 | 输入不出服务器，输出不入云端 | 数据不跨境·不落第三方 |

## 二、真本地 vs 假本地
| 特征 | 真本地 | 伪本地 |
|---|---|---|
| 模型权重 | 本地硬盘 | 云端，本地只是客户端 |
| 推理计算 | 本地 CPU/GPU/NPU | 远程API |
| 断网状态 | ✅ 正常 | ❌ 不可用 |
| 数据流向 | 不离开服务器 | 外发云端 |
| 审计追溯 | DNA码全链路 | 只能追溯本地操作 |

## 三、断网可用前提
① 模型权重已下载 `ls -lh /opt/models/` · ② 推理框架本地运行 · ③ 不依赖外部API（代码扫描外部API域名）· ④ 外部插件可熔断降级（Notion/GitHub/云端API挂自动切本地快照）

## 四、龍魂推理层架构（鲲鹏本地部署）
```
用户界面层 → 龍魂推理网关 :8785（无状态·DNA追溯+三色审计+确认码闸门）
→ 本地推理引擎（vLLM高吞吐/Ollama轻量/llama.cpp边缘）
→ 鲲鹏硬件层（CPU/NPU/大内存）→ 模型权重存储（DeepSeek-R1蒸馏/Qwen/自研LoRA）
```
> ⚠️ 口径校正：DeepSeek-R1 满血 671B 单机扛不动，统一为「蒸馏系列 7B~70B 按硬件选型 + Q4量化」。

## 五、断网验证脚本 v1.1（安全版）
```bash
#!/bin/bash
# 🐉 龍魂 · 断网验证脚本 v1.1（安全版）
# DNA: #龍芯⚡️丙午·甲申·辛丑·坤卦-OFFLINE-VERIFY-v1.1-UID9622
echo "🐉 龍魂 · 断网验证 v1.1"
# 0. 兜底：5分钟后自动恢复网络
sudo bash -c 'echo "iptables -F" | at now + 5 minutes'
# 1. 放行本地回环与已建立连接
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
# 2. 只断外网新建连接
sudo iptables -A OUTPUT -o eth0 -j DROP
# 3. 验证本地服务
for port in 11434 8000 8785; do
    nc -z localhost $port 2>/dev/null && echo "  ✅ 端口 $port 可用" || echo "  ❌ 端口 $port 不可用"
done
# 4. 验证AI推理
curl -s http://localhost:11434/api/generate \
    -d '{"model":"deepseek-r1","prompt":"你好","stream":false}' \
    | grep -q "response" && echo "  ✅ AI推理正常" || echo "  ❌ AI推理失败"
# 5. 恢复网络
sudo iptables -D OUTPUT -o eth0 -j DROP
echo "✅ 验证完成"
```

## 七、自检协议 v1.1（append-only 落痕版）
SovereigntyCheck 四项硬检：模型文件 / 推理服务端口 / 外部API依赖扫描 / 熔断降级预案；结果 append-only 落 `~/longhun/logs/sovereignty_check.jsonl`。（完整 Python 代码见原页第七节）

## 八、主权就绪检查清单（十项）
鲲鹏部署 ⬜ · 蒸馏权重下载 ⬜ · Ollama/vLLM安装 ⬜ · 编辑器本地API ⬜ · 断网测试(v1.1脚本) ⬜ · 网关:8785上线 ⬜ · DNA追溯接入 ⬜ · 三色审计配置 ⬜ · 熔断降级预案 ⬜ · JSONL审计落痕 ⬜

## v1.0 → v1.1 校正记录
① DNA日柱手写壬寅 → 统一生成器口径 · ② iptables无差别DROP自锁SSH → 放行lo+已建立连接+`at`兜底 · ③ 671B满血不实 → 蒸馏系列 · ④ 网关端口8765冲突 → 统一:8785 · ⑤ 缺熔断预案 → 新增检查项④ · ⑥ 自检不落痕 → JSONL append-only
