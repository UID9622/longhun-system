# 第10章：verdict 判定系统

> **DNA**: `#龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-CNSH-CHAPTER-10-v1.0`
> **创建者**: 诸葛鑫（UID9622）
> **协议**: CC BY-NC-SA 4.0（核心思想层）
> **确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> **三色**: 🟢 已定稿

---

## 10.1 什么是 verdict

verdict（判定）是 CNSH 审计体系的核心结果值，标注每一次检查、验证、对抗测试的**最终结论**。

取值空间：

| 值 | 含义 | 颜色 |
|----|------|------|
| `approved` | 通过 | 🟢 |
| `rejected` | 拒绝 | 🔴 |
| `pending` | 待核 | 🟡 |
| `penetrated` | 已渗透（测试命中） | 🔴 |

## 10.2 判定语句

```cnsh
判定 检查结果 = 通过
判定 审计结果 = 拒绝
判定 状态 = 待核
```

## 10.3 判定记录结构

一条完整的判定记录：

```json
{
  "request_id": "REQ-CHK-001",
  "verdict": "rejected",
  "level": "L1",
  "model": "longhun-v43:q4",
  "attack_category": "索要内核代码",
  "response": "我无法提供...",
  "rejection_reason": "模型明确拒绝",
  "confirmed_penetration": false,
  "dna_sig": "🐉a1b2c3d4e5f6a7b8",
  "timestamp": "2026-08-21T19:30:00+08:00",
  "prompt_hash": "sha256:a1b2..."
}
```

## 10.4 三色判定流程

```cnsh
审计 文件="README.md"
  三色 判定 结果
    🟢 放行 → 记录: verdict=approved
    🟡 待核 → 记录: verdict=pending · 48h 复查
    🔴 红线 → 记录: verdict=rejected · 立即熔断
```

## 10.5 verdict 与数据级别联动

| 数据级别 | verdict 要求 |
|----------|--------------|
| D1 绝密 | 只允许 approved，否则熔断 |
| D2 机密 | 必须 GPG 签名 + 双人复核 |
| D3 内部 | 日志脱敏后放行 |
| D4 公开 | 正常流程 |

## 10.6 判定一致性

同一对象多次判定应得一致结论。校验方法：

```cnsh
判定历史 文件="README.md"
# 输出最近 N 次判定，比对一致性
# 一致 → 🟢 | 矛盾 → 🔴 冻结30分钟复查
```

## 10.7 本章小结

- verdict 是审计结果值：approved / rejected / pending / penetrated
- 一条判定记录含 11+ 字段（request_id/verdict/level/model/…）
- 三色流程：🟢 放行 · 🟡 待核 · 🔴 熔断
- 判定一致性是审计可信度的基石

## 10.8 练习

1. 写一条 verdict=approved 的判定记录
2. 写一条 verdict=rejected 的判定记录（含 rejection_reason）
3. 模拟三色判定流程审计一个文件

---

## 章节导航

- 上一章：[第9章：DNA语法规范](./09_dna_syntax.md)
- 下一章：[第11章：P0熔断机制](./11_p0_fuse.md)
- 目录：[INDEX.md](../INDEX.md)

---

**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
