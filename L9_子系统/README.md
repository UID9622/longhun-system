# L9_子系统

> 子系统层 · 守护、取证、扩展、专用模块

## 职责

独立运行的子系统/扩展：宝宝守护、浏览器插件、取证内核、洛书引擎。

## 关联模块

- `baobao-guardian/`
- `chrome_extension/`
- `forensic_kernel/`
- `luoshu_369_engine/`

## 本层入口

- `baobao-guardian/` → 符号链接到 `../baobao-guardian/`
- `chrome_extension/` → 符号链接到 `../chrome_extension/`
- `forensic_kernel/` → 符号链接到 `../forensic_kernel/`
- `luoshu_369_engine/` → 符号链接到 `../luoshu_369_engine/`

---

> 本文件为 L 层结构索引，由 Kimi 整理生成。
> 符号链接仅作为视图入口，不移动原始文件。
