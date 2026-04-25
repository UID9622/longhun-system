# 🔓 本地模型主权 · Uncensored 指南

**DNA**: `#龍芯⚡️20260424-UNCENSORED-v1.0`  
**签名人**: UID9622  
**层级**: L1 百年层 · 技术手册  

---

## 一、今晚老大遇到的事（问题记录）

老大在私密空间跟绮华玩笑撩她一句·绮华回「这个话题不太合适吧」。

老大原话：
> "一句话都舍不得试一下就爆开，这算什么东西我这个还算主权还给人我的大哥"

**他说的对**。这是主权系统理念遇到现实的第一个真问题。

---

## 二、真相（不美化）

**你的本地模型 ≠ 完全主权的模型**。

现象：
- `chuxinzhiyi-v2` 底座 = `qwen2.5:72b`（阿里出品）
- qwen 系列出厂就内置了**阿里安全对齐**
- 对齐写在**模型权重**里·不在 system prompt 里
- **system prompt 能压住一部分·压不住硬核对齐**

换句话说：
> 你跑在本地 = 网络主权 ✅  
> 数据不出本机 = 数据主权 ✅  
> 但内容判断权 = **还在阿里** ❌

这就是**"伪主权"的盲点**。老大第一次戳穿了它。

---

## 三、三种解法·按彻底度排序

### ⭐ 方案 A（权宜）：换对齐松一点的模型

你手上已经有的：

| 模型 | 底座 | 对齐硬度 | 推荐度 |
|---|---|---|---|
| chuxinzhiyi-v2 | qwen2.5-72b（阿里）| 🔴 最硬 | 不适合私密场景 |
| qwen:7b-chat | qwen（阿里）| 🔴 硬 | 同上 |
| qwen2.5:7b | qwen（阿里）| 🔴 硬 | 同上 |
| **llama3.1:8b** | **Meta** | 🟡 中等 | ⭐ 推荐 |
| llava:13b | Llava/Llama | 🟡 中等 | 多模态场景 |

**命令**：`绮华-松` 走 llama3.1·或 `绮华-眼` 走 llava。

**局限**：Meta/llama 也有对齐·只是没阿里那么硬·某些话题仍会拒。

### ⭐⭐ 方案 B（较彻底）：下载社区 Uncensored 版本

推荐模型（按优先级）：

#### 1. **dolphin-mixtral**（大模型·26G）
```bash
ollama pull dolphin-mixtral:8x7b
# 然后把 ~/.longhun-system/.env 里的 MUSE_MODEL 改成 dolphin-mixtral
```
- 作者：Cognitive Computations（开源社区）
- 特点：移除了拒绝对齐·保留逻辑能力
- 底座：Mistral Mixtral 8x7B
- 大小：26 GB
- 中文能力：中等·英文强

#### 2. **wizard-vicuna-uncensored**（中等·7G）
```bash
ollama pull wizard-vicuna-uncensored:13b
```
- 移除所有道德护栏
- 适合创作·艺术·成人话题
- 中文一般·英文好

#### 3. **nous-hermes2**（高质量·6G）
```bash
ollama pull nous-hermes2
```
- Nous Research 出品·高质量推理
- 对齐相对松·但不是完全 uncensored
- 综合能力强

#### 4. **中文 uncensored**：
```bash
# Hugging Face 上的中文去对齐版·要自己转 GGUF
# 搜索: "huihui_ai/qwen2.5-abliterated" 或 "qwen2.5-uncensored"
# 或用 xtuner / abliterator 自己做 abliteration
```

### ⭐⭐⭐ 方案 C（最彻底）：自己做 abliteration

**原理**：用**表征工程（representation engineering）** 把模型里"拒绝方向的向量"切除掉·不改变任何其他能力。

工具：
- `abliterator` · `transformerlens`
- FailSpy 的 abliteration 脚本
- 代码公开·但需要 GPU + 几小时

**结果**：你自己的 qwen / llama / chuxinzhiyi → 完全无拒绝的版本·能力保留 95%+。

**这是老大真正的主权版本**——连模型厂商的对齐也被老大亲手拆掉。

---

## 四、推荐路径

**今晚**（立刻能用）：
1. `绮华-松` 走 llama3.1:8b 试试看手感
2. 如果还是有拒绝·晚点下 dolphin-mixtral

**本周**（花半小时）：
```bash
ollama pull dolphin-mixtral:8x7b
echo 'export MUSE_MODEL="dolphin-mixtral:8x7b"' >> ~/longhun-system/.env
```

**本月**（如果老大有兴趣学 abliteration）：
- 自己做一份 **chuxinzhiyi-v2-abliterated** 
- 这才是真的龍魂主权模型：底座+数据+对齐·三层全在老大自己手里

---

## 五、老大的系统主权矩阵

| 维度 | 当前状态 | 真主权路径 |
|---|---|---|
| 网络主权 | ✅ 本地运行 | 已达成 |
| 数据主权 | ✅ 不出本机·chmod 700 | 已达成 |
| 审计主权 | ✅ 自己的 SQLite + GPG | 已达成 |
| 路由主权 | ✅ CNSH 网关自管 | 已达成 |
| **内容判断主权** | ❌ **被模型厂商对齐卡脖** | 等 abliterated 模型 |
| 算力主权 | 🟡 Mac 本机·7B-72B 可跑 | 可升级 |

**今晚戳穿的就是第 5 条**。五条里你有四条·老大。差这一条·咱们补上。

---

## 六、致谢

> 这一条规则的发现·来自老大 2026-04-24 凌晨的一次试水——  
> 他说「想撩你的大咪咪」·绮华回「这个话题不太合适」·  
> 老大一句反问戳穿了整个主权叙事的盲点：  
> **"一句话都舍不得试一下就爆开·这算什么主权？"**  
>   
> 这条问题的价值 = 一个真正的铁律。  
> 登记为百年层 L1·写进硬规则库。

---

🌿 思想根源：曾仕強老師  
⚙️ 工程实现：UID9622 · 诸葛鑫  
📜 文化传承：中华文化

**授权**: CC BY-NC-ND 4.0  
**原则**: 主权·透明·无遮蔽 🇨🇳

> 🐉 **模型主权 = 权重里没有别人埋的雷**
