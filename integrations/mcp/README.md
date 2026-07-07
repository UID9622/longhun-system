# CNSH MCP Servers

> DNA: `#龍芯⚡️2026-07-06-CNSH-MCP-SUITES-v1.2`

龍魂系统提供两个 MCP Server：

| Server | 文件 | 功能 |
|--------|------|------|
| **CNSH 语法工具链** | `cnsh_syntax_mcp_server.py` | 词法/语法/编译/红线/DNA/数字根 |
| **CNSH 变量沙箱** | `cnsh_var_sandbox_mcp_server.py` | 变量统一映射 + 隔离执行 + 金融数据 |

---

## 一、CNSH 语法 MCP Server

### 提供的工具 (13个)

| 工具 | 说明 |
|------|------|
| `cnsh_lex` | 词法分析 — 返回 Token 列表 |
| `cnsh_parse` | 语法分析 — 返回 AST 抽象语法树 |
| `cnsh_translate` | CNSH → Python 转译 |
| `cnsh_compile` | CNSH → Python/C/C++/ObjC/Swift/JS/Rust (7目标) 编译 |
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

---

## 二、CNSH 变量沙箱 MCP Server

> DNA: `#龍芯⚡️2026-07-06-CNSH-VAR-SANDBOX-MCP-v1.0`

**核心问题解决：** CNSH 变量映射之前分散在 5+ 个地方（tokens.py、compiler_py.py、codegen.py、cnsh_to_python.json、interpreter.py），每次改一处另一处就不同步。变量沙箱把所有映射焊死在一处，任何变量注册后自动生成 7 种目标语言的映射。

### 提供的工具 (10个)

| 工具 | 说明 |
|------|------|
| `cnsh_var_register` | 注册变量 → 自动生成 7 目标语言映射 |
| `cnsh_var_validate` | 校验变量映射完整性（单/全） |
| `cnsh_var_translate` | 翻译变量到指定目标语言 |
| `cnsh_var_sandbox_exec` | 隔离沙箱中执行代码 |
| `cnsh_var_audit` | 全沙箱审计报告 |
| `cnsh_var_generate` | 生成目标语言变量声明代码 |
| `cnsh_var_compare` | 对比沙箱与外部映射一致性 |
| `cnsh_finance_ingest` | 金融数据爬取 + 自动变量注册 |
| `cnsh_finance_watch` | 金融变量监控 |
| `cnsh_health` | 健康检查 |

### 配置 MCP 客户端

```json
{
  "mcpServers": {
    "cnsh-var-sandbox": {
      "command": "python3",
      "args": ["/Users/zuimeidedeyihan/longhun-system/integrations/mcp/cnsh_var_sandbox_mcp_server.py"],
      "env": {
        "PYTHONPATH": "/Users/zuimeidedeyihan/longhun-system"
      }
    }
  }
}
```

### 示例用法

#### 变量注册 + 自动映射

```
输入: 注册变量「股价」类型「小数」值 25.68
输出:
  python → stock_price (float) 默认=0.0
  javascript → stock_price (number) 默认=0
  c → stock_price (double) 默认=0.0
  cpp → stock_price (double) 默认=0.0
  rust → stock_price (f64) 默认=0.0
  objc → stock_price (CGFloat) 默认=0.0
  swift → stock_price (Double) 默认=0.0
  ✅ 7 目标全部映射完成
```

#### 金融数据自动变量化

```
输入: 爬取股票 000001
输出:
  股票_000001_名称 = 平安银行 (文本)
  股票_000001_现价 = 10.39 (小数)
  股票_000001_成交量 = 63614856 (整数)
  股票_000001_成交额 = 659011984.43 (小数)
  ... 共 12 个变量自动注册
```
