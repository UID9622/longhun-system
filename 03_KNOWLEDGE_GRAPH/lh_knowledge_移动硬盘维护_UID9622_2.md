# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统·移动硬盘维护 SOP（UID9622-2）

> 作者：龍芯北辰·UID9622
> 发布时间：2026-08-15
> 来源：longhun-system 桌面外置硬盘维护实践
> 入库DNA：#龍芯⚡️丙午·丁酉·辛卯·甲午·䷚颐-丙申-EXTERNAL-DRIVE-UID9622-2

---

> 备份盘也要体检。
> 不是等坏了再修，是常规维护保持干净。

---

## P0 核心原则

1. 先检查再动手
2. 不删用户数据
3. 文件系统检查优先
4. 减少系统后台对备份盘的写入
5. 重命名需符合文件系统限制

---

## P1 设备信息

| 项目 | 值 |
|---|---|
| 设备 | `/dev/disk9s1` |
| 卷标 | `UID9622-2` |
| 文件系统 | ExFAT |
| 容量 | 500.1 GB |
| 用途 | 龍魂系统备份盘 |

---

## P2 维护步骤

### 1. 检查文件系统

```bash
diskutil verifyVolume disk9s1
```

### 2. 清空回收站

```bash
rm -rf /Volumes/UID9622-2/.Trashes/*
```

### 3. 关闭 Spotlight 索引

```bash
mdutil -i off /Volumes/UID9622-2
mdutil -E /Volumes/UID9622-2
```

### 4. 禁用 fseventsd 日志

```bash
mkdir -p /Volumes/UID9622-2/.fseventsd
touch /Volumes/UID9622-2/.fseventsd/no_log
```

### 5. 安全弹出

```bash
diskutil eject disk9
```

---

## P3 注意事项

- ExFAT 卷标最多 11 个字符，不能含空格
- `UID9622 backup 2` 太长，改为 `UID9622-2`
- 清理 `.Spotlight-V100`、`.TemporaryItems` 需先关闭 Spotlight
- 备份盘不建议启用 Spotlight 索引

---

## 签章

```
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#龍芯⚡️丙午·丁酉·辛卯·甲午·䷚颐-丙申-EXTERNAL-DRIVE-UID9622-2
```

---

> 不是用完就拔，是维护后再收。
> 不是存完就忘，是定期体检。
> 不是备份盘，是数字保险箱。
