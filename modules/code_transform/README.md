# 龍魂·AST 代码变换引擎 v1.0

**DNA**: `#龍芯⚡️2026-05-28-LONGHUN-AST-TRANSFORM-v1.0`

## 功能

将英文代码（变量名、函数名、类名）转换为中文，保持 100% 逻辑不变。

## 使用

```bash
# 单文件变换
python3 longhun_ast_transform_v1.0.py --input app.py --output app_中文.py

# 目录变换
python3 longhun_ast_transform_v1.0.py --input ./project --output ./project_中文版

# 导出词典
python3 longhun_ast_transform_v1.0.py --dump-vocab
```

## 核心模块

- `中文变换器`: AST 节点访问器
- `transform_file()`: 单文件处理
- `transform_project()`: 目录级处理
- `DEFAULT_VOCAB`: 默认词典（250+ 词条）
