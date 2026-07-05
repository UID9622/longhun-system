# CNSH 语法 MCP Server

> DNA: `#龍芯⚡️2026-07-05-CNSH-SYNTAX-MCP-v1.0`

CNSH（中文原生语义层级）语言的完整语法工具链 MCP Server。
基于 stdio 传输，可直接配置到 Claude/Cursor/CodeBuddy 等 MCP 客户端。

## 提供的工具 (13个)

| 工具 | 说明 |
|------|------|
| `cnsh_lex` | 词法分析 — 返回 Token 列表 |
| `cnsh_parse` | 语法分析 — 返回 AST 抽象语法树 |
| `cnsh_translate` | CNSH → Python 转译 |
| `cnsh_compile` | CNSH → Python/JS/Rust/C 编译 |
| `cnsh_keywords` | 查询关键字注册表 |
| `cnsh_redline_check` | 红线词组熔断检查 (P0-P3) |
| `cnsh_redline_list` | 列出所有红线词组 |
| `cnsh_dna_generate` | 生成 DNA 追溯码 |
| `cnsh_dna_validate` | 校验 DNA 追溯码 |
| `cnsh_digital_root` | 数字根 + 五行 + 三色闸门 |
| `cnsh_audit` | 三色审计判定 |
| `cnsh_diagnostics` | 四合一完整诊断 |
| `cnsh_health` | 健康检查 |

## 安装

```bash
cd integrations/mcp
pip install -r requirements.txt
```

## 配置 MCP 客户端

### CodeBuddy

在 CodeBuddy 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "cnsh-syntax": {
      "command": "python3",
      "args": ["/Users/zuimeidedeyihan/longhun-system/integrations/mcp/cnsh_syntax_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/Users/zuimeidedeyihan/longhun-system"
      }
    }
  }
}
```

### Claude Desktop

在 `~/Library/Application Support/Claude/claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "cnsh-syntax": {
      "command": "python3",
      "args": [
        "/Users/zuimeidedeyihan/longhun-system/integrations/mcp/cnsh_syntax_mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/zuimeidedeyihan/longhun-system"
      }
    }
  }
}
```

### Cursor

在 Cursor 设置中 `Features > MCP` 添加：

```json
{
  "mcpServers": {
    "cnsh-syntax": {
      "command": "python3",
      "args": [
        "/Users/zuimeidedeyihan/longhun-system/integrations/mcp/cnsh_syntax_mcp_server.py"
      ],
      "env": {
        "PYTHONPATH": "/Users/zuimeidedeyihan/longhun-system"
      }
    }
  }
}
```

## 示例用法

### 词法分析

```
输入: 如果 a 大于 10 { 返回 真 }
输出: Token 列表 (IF, IDENTIFIER(a), GT, NUMBER(10), LBRACE, RETURN, TRUE, RBRACE)
```

### 代码转译

```
输入: 函数 加法(甲, 乙) { 返回 甲 加 乙 }
输出: def 加法(甲, 乙):\n    return 甲 + 乙
```

### 红线检查

```
输入: "这个平台使用生态锁定策略"
输出: 🔴 触发 P0_伦理红线: 生态锁定
```

### 数字根

```
输入: "9622"
输出: digital_root=1, wuxing=水, gate=🟡
```
