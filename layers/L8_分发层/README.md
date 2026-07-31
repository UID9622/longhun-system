# L8_分发层

> 分发层 · 部署、发布、镜像、安装包

## 职责

系统部署、版本发布、安装包分发。

## 关联模块

- `deploy/`
- `releases/`
- `gitee-export/`

## 本层入口

- `deploy/` → 符号链接到 `../deploy/`
- `releases/` → 符号链接到 `../releases/`
- `gitee-export/` → 符号链接到 `../gitee-export/`

---

> 本文件为 L 层结构索引，由 Kimi 整理生成。
> 符号链接仅作为视图入口，不移动原始文件。
