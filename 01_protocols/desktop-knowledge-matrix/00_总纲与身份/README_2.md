# 03_compiler — CNSH 编译器 & 语法库

**路径**：`03_compiler`

## 状态

🟢 活跃开发中

## 功能概述

该模块包含 CNSH 编译器的映射配置和统一语法库：

| 文件 | 说明 |
|------|------|
| `mappings/syntax_library.json` | 🆕 **统一语法库 v1.0** — 25类·350+条目·20种目标语言归一总表 |
| `mappings/SYNTAX_LIBRARY.md` | 🆕 语法库使用文档 |
| `mappings/keywords.json` | 中文关键字→多目标语言映射 (历史·已合并到语法库) |
| `mappings/operators.json` | 中文运算符→多目标语言映射 (历史·已合并到语法库) |
| `mappings/stdlib.json` | 中文标准库→多目标语言映射 (历史·已合并到语法库) |
| `COMPILE-REGISTRY.local.jsonl` | 编译任务注册表 (Append-Only) |

## 入口脚本

- `bin/syntax_lookup.py` — 语法库查询工具

```bash
python3 bin/syntax_lookup.py "打印"              # 查单个中文关键字
python3 bin/syntax_lookup.py "打印" --target py   # 只查Python映射
python3 bin/syntax_lookup.py --list-categories    # 列出所有语法类别
python3 bin/syntax_lookup.py --category 控制流     # 列出某类别所有关键字
python3 bin/syntax_lookup.py --search "merge"     # 模糊搜索
```

## 哲学

**只翻译·不破解·MD格式归一·中文编辑可用·丢啥给啥·原汁原味。**

几百个不同脚本和语法 → 一个 JSON 总表 → 中文关键字 → 20种目标语言。

**DNA**: `#龍芯⚡️丙午·丙申·庚申·亥时-SYNTAX-LIBRARY-v1.0`