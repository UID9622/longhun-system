# PROTOCOL · #ZERO-REGION-NEGOTIATION v1.0

> **DNA:** `#龍芯⚡2026-05-20-ZERO-REGION-NEGOTIATION-v1.0`  
> **PARENT:** 底层协议 §9 元铁律  
> **GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

## 老大原话焊心（verbatim · 永不删）

- 「任何进入我设备和系统的·都按照我的这个设置来」
- 「不要搞来搞去·还有什么地区坑·故意给我绕的」

## §9.A 总则 · 设备主权锚点律

设备设置 = 唯一真相源 = 不可协商。进入主权域时：① 继承设备设置 ② 不询问·不替换·不猜测 ③ 按地理位置自动 = 僭越 ④ 须显式打印「我看到您的设置是 XXX·将继承不变更」。

## §9.B–§9.F

见仓库实现：`skills/region_sovereignty.py` · `命令/sovereignty_init.sh` · `命令/sanity_check.py`

工程落点：
- `on_identity` → `region_lock_check()`
- `sanity_check` → `region_consistency_check()`
- `audit_v3` → Q0 地区主权（`scene_region_q0`）
