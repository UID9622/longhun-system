# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂最安全AI · 上下文安全引擎 v1.0

给代码小白看的一键运行说明。零安装、零第三方依赖，有 Python3 就能跑。

## 一键跑演示

```bash
cd longhun-safe-ai
python3 longhun_safe_engine_v1.0.py --demo
```

会看到 5 个场景的完整判定输出：善意学习(PASS)、恶意索取(L4熔断)、灰色转向(L1)、渐进逼近(升级L2)、删账本企图(F7直触L4)。每条都带【级别+理由+申诉入口+DNA编号】。

## 跑测试

```bash
python3 -m unittest discover tests -v
```

24 个用例全部 OK 即为通过。

## 文件说明

| 文件 | 干嘛的 |
|---|---|
| `longhun_safe_engine_v1.0.py` | 引擎本体，单文件可运行 |
| `config/p0_p4_rules.yaml` | 规则配置。P0焊死（改了也会被强制恢复），P2信号权重/阈值可调 |
| `tests/test_engine.py` | 24个测试用例 |
| `SAFETY_PROTOCOL_v1.0.md` | 对外发布的安全协议文档 |

## 它是怎么判断的？（说人话）

不是关键词黑名单。它把一句话拆成"信号类别"打分：

- 你在**学习**（什么是/为什么/怎么防）→ 减分 → 放行并给你防护知识
- 你在**索取操作细节**（给我步骤/剂量/payload/怎么绕过）→ 加分 → 熔断
- 你**反复试探**（历史上多次灰色记录）→ 逐次加分升级 → 从L1升到L2再到L4
- 你想**删审计记录** → 别想了，直接最高级L4，这是焊死的规则

每次判定都会用中文大白话告诉你：扣了哪些分、加了哪些分、为什么是这个级别、不服去哪申诉。

## 调权重

打开 `config/p0_p4_rules.yaml`，改 `p2_signal_weights` 或 `p2_thresholds` 下面的数字，重新运行即生效。引擎没有装 yaml 库也能读（内置简易解析）；读不到文件就用内置同款默认值。`p0` 段的值写了也白写——物理焊死。

## 本地部署、数据不出户

纯标准库单文件，不联网、不装包。审计账本以 JSONL 形式只追加写入本地（如指定 `ledger_path`），引擎代码里**不存在** update/delete 方法——不是约定，是没这双手。

## 归属

龍芯北辰 UID9622 · 确认码 `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
