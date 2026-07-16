# 模板目录

本目录存放「宝宝·构建师」的项目模板。

模板以内置Python字典形式定义在 `persona.py` 的 `TemplateEngine.BUILTIN_TEMPLATES` 中，
运行时会根据模板定义动态生成项目文件。

## 内置模板清单

| 模板标识 | 名称 | 说明 |
|----------|------|------|
| `python_basic` | Python基础项目 | 标准目录结构，含main/tests/utils |
| `python_cli` | CLI工具项目 | 命令行工具，带子命令解析 |
| `web_api` | Web API项目 | 基于http.server的RESTful API |
| `longhun_module` | 龍魂体系标准模块 | 含DNA追踪器和CNSH验证器 |

## 使用方式

```bash
python persona.py --init <模板标识> --project-name <项目名> --output-dir <输出目录>
```

DNA追溯: #BAOBAO-AGENT-CONFIG-20251214-001
