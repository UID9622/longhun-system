# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# L4_数据层

> 数据归档层 · 运行时状态、备份、二级数据

## 职责

运行时状态、临时数据、备份归档（与 L3 数据层区分：L3 是活跃数据，L4 是归档/状态）。

## 关联模块

- `state/`
- `backups/`
- `tmp/`

## 本层入口

- `state/` → 符号链接到 `../state/`
- `backups/` → 符号链接到 `../backups/`
- `tmp/` → 符号链接到 `../tmp/`

---

> 本文件为 L 层结构索引，由 Kimi 整理生成。
> 符号链接仅作为视图入口，不移动原始文件。
