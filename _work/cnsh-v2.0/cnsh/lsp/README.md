# CNSH Language Server / 编辑器补全（路线图）

**协议真源**: `01_protocols/cnsh/PROTOCOL__CNSH-TOOLCHAIN-FUSION-v1.0.local.md`  
**源流 DNA**: `#ZHUGEXIN⚡️2026-01-02-CNSH-LSP-001`

## 建议目录（后续增量）

```text
cnsh/lsp/
├── README.md                 # 本文件
├── package.json              # [待] Node LSP 包
├── server/                   # [待] createConnection / completion / hover
├── syntaxes/                 # [待] cnsh.tmLanguage.json
└── vscode-extension/         # [待] contributes.languages + client
```

## 实现顺序（推荐）

1. **`.cnsh` TextMate 语法**（关键词：`函数`、`如果`、`类型`、`枚举` …）  
2. **补全字典**（CNSH 关键字 + 从类型库 JSON 加载域扩展）  
3. **LSP**：`textDocument/completion`、`hover`  
4. **转译**：独立模块（AST 或受控模板），避免「全局字符串替换类型名」  

## 注意

示例草稿里用中文函数名仅为说明；**可运行实现**须使用英文标识符 + 中文**关键字/类型别名**表，否则工具链与鲁班审计难以挂接。
