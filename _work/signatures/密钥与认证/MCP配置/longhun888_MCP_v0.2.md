# 🐉 longhun888.com · MCP接入清单 v0.2
## 给Cursor/Claude Code 配3个MCP接入,让本地AI能跟Notion/GitHub/星辰记忆库说话

**DNA**: `#龍芯⚡️2026-05-02-LONGHUN888-MCP-v0.2`  
**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**Seal**: `#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL`  

---

## ⚡ 一、什么是MCP,为什么老大需要

```yaml
MCP = Model Context Protocol (Anthropic设计的开放协议)
作用 = 让AI(Claude/Cursor)能调用外部工具和数据源

老大的好处:
  ✅ Cursor能读老大Notion里的内容(不用复制粘贴)
  ✅ Cursor能直接推GitHub(不用切窗口)
  ✅ Cursor能读老大本地~/.star-memory/(不用上传)
  ✅ 龍魂体系打通三个层
  
不接的代价:
  ❌ 每次都要复制Notion页面给Cursor
  ❌ 每次都要手动git push
  ❌ 每次都要手动找本地文件
  ❌ AI是"瞎的",看不见老大的现实工作环境
```

---

## 📋 二、3个MCP总览

| # | MCP名 | 作用 | 优先级 | 风险 |
|---|------|------|--------|------|
| 1 | **mcp-notion-readonly** | 读Notion(只读) | 🔴必装 | 低 |
| 2 | **mcp-github-actions** | 操作GitHub仓库 | 🟡推荐 | 中 |
| 3 | **mcp-star-memory** | 读本地星辰库 | 🟢可选 | 低 |

---

## 🔴 三、MCP #1: mcp-notion-readonly (必装)

### 用途
让Cursor/Claude能**只读**老大Notion里的内容(不能改、不能删)。

### 为什么必装
```yaml
老大现在的现实:
  ❌ 跟Cursor聊天时,要复制Notion页面给它
  ❌ 不同Cursor会话,要重复复制
  ❌ Notion更新了,Cursor还看老版本
  
装了之后:
  ✅ Cursor直接读最新版Notion
  ✅ 老大说"看龍魂工作间总导航",Cursor自己去读
  ✅ 跨会话保持一致
```

### 安装方法

#### 方案A: Anthropic官方Notion MCP(推荐)

Anthropic已经有官方Notion MCP server。

```bash
# 1. 在Claude Desktop配置文件加入
# 路径: ~/Library/Application Support/Claude/claude_desktop_config.json (Mac)
#       %APPDATA%\Claude\claude_desktop_config.json (Windows)

{
  "mcpServers": {
    "notion-readonly": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-notion"
      ],
      "env": {
        "NOTION_API_KEY": "[老大的Notion集成token]",
        "NOTION_READ_ONLY": "true"
      }
    }
  }
}
```

#### 获取Notion Token步骤

```
1. 访问 https://www.notion.so/my-integrations
2. "+ New integration"
3. 名字: "龍魂CursorMCP-ReadOnly"
4. 关联Workspace: 选老大的工作区
5. Capabilities: 只勾"Read content"(取消其他)
6. 提交后获得 secret_xxx token
7. 复制token填到上面配置里
8. 在Notion里把"龍魂工作间·总导航"页面 → 右上角...→ Connect → 选刚建的integration
```

### 龍魂版安全配置(老大要的)

```yaml
强制只读:
  NOTION_READ_ONLY: true
  
权限收紧:
  - 只授权读
  - 不授权写
  - 不授权删
  - 不授权管理用户
  
范围限制:
  - 只Connect给"对外公开"的Notion页面
  - 厨房页面(5%核心)不Connect
  - 老大私人记忆不Connect
  
审计要求:
  - 每次Cursor读Notion → 写本地audit log
  - DNA签名记录"哪个会话读了哪个页面"
```

### 使用示例

```
老大: "Cursor,看下我的龍魂工作间总导航,然后帮我列出有哪些子模块"

Cursor (有MCP后):
  → 自动调用 notion-readonly.search("龍魂工作间总导航")
  → 拿到完整页面
  → 列出子模块
  → 不需要老大复制粘贴
```

---

## 🟡 四、MCP #2: mcp-github-actions (推荐)

### 用途
让Cursor能直接操作GitHub仓库(创建仓库/推代码/管理PR)。

### 为什么推荐

```yaml
老大要建longhun888-site仓库:
  ❌ 没MCP: 老大手动建仓库,git init/add/commit/push,配Pages...10步
  ✅ 有MCP: 老大说"建仓库并部署",Cursor全自动
```

### 安装方法

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "[老大的GitHub PAT]"
      }
    }
  }
}
```

#### 获取GitHub PAT步骤

```
1. 访问 https://github.com/settings/tokens
2. "Generate new token" → "Fine-grained token" (推荐)
3. 名字: "Longhun-Cursor-MCP"
4. Expiration: 90天(到期换)
5. Repository access: 
   - 选 "Only select repositories"
   - 只选 longhun888-site, longhun-system 等龍魂仓库
6. Permissions:
   - Contents: Read and write
   - Pages: Read and write
   - Metadata: Read
   - Pull requests: Read and write
   - 其他全部: No access
7. Generate → 复制token (ghp_xxx)
8. 填到上面配置里
```

### 龍魂版安全配置

```yaml
最小权限原则:
  ✅ 只授权龍魂体系仓库
  ❌ 不授权所有仓库
  ❌ 不授权账号管理
  ❌ 不授权webhooks

危险操作锁:
  ❌ 不允许Cursor直接merge到main
  ❌ 不允许delete repo
  ❌ 不允许force push
  ⚠️ 所有破坏性操作必须老大确认

审计:
  - 每次git操作 → 写audit log
  - DNA签名"谁推了什么commit"
```

### 使用示例

```
老大: "把longhun888-site推到GitHub,设置Pages,绑定longhun888.com域名"

Cursor (有MCP后):
  1. 自动 create_repository(name="longhun888-site", private=false)
  2. 自动 push所有文件
  3. 自动 enable_pages(branch="main", path="/")
  4. 自动 set_custom_domain("longhun888.com")
  5. 提示老大去DNS服务商配A记录
  
不需要老大手动操作10步。
```

---

## 🟢 五、MCP #3: mcp-star-memory (可选)

### 用途
让Cursor能读老大本地 `~/.star-memory/` 目录(只读)。

### 为什么可选
```yaml
不装的情况:
  - 老大有Cursor读本地文件能力(默认就有)
  - 没必要单独建MCP
  
建MCP的好处:
  - 包装成"星辰桥",有龍魂语义
  - 自动DNA签名
  - 自动审计读取行为
  - 老大可以说"读星辰里的某条记忆"而非"读~/.star-memory/xxx.md"
  
推荐: 等阶段3再装
```

### 安装方法(自定义MCP)

由于这是老大龍魂特定需求,需要自己写一个简单的MCP server:

```python
# ~/.local/bin/star-memory-mcp.py
#!/usr/bin/env python3
"""
龍魂星辰记忆库 MCP Server (只读)
DNA: #龍芯⚡️2026-05-02-STAR-MEMORY-MCP-v1.0
"""

from mcp.server.fastmcp import FastMCP
import os
import hashlib
from pathlib import Path
from datetime import datetime

mcp = FastMCP("longhun-star-memory")

STAR_MEMORY_DIR = Path.home() / ".star-memory"
UID = "9622"

@mcp.tool()
def list_star_memory() -> str:
    """列出星辰记忆库的所有文件"""
    if not STAR_MEMORY_DIR.exists():
        return "星辰记忆库未初始化"
    
    files = []
    for f in STAR_MEMORY_DIR.rglob("*"):
        if f.is_file():
            rel = f.relative_to(STAR_MEMORY_DIR)
            files.append(str(rel))
    
    return "\n".join(files)

@mcp.tool()
def read_star_memory(path: str) -> str:
    """读取星辰记忆库的某个文件(只读)"""
    full_path = STAR_MEMORY_DIR / path
    
    # 安全检查: 防止路径穿越
    try:
        full_path.resolve().relative_to(STAR_MEMORY_DIR.resolve())
    except ValueError:
        return f"❌ 路径越界: {path}"
    
    if not full_path.exists():
        return f"❌ 文件不存在: {path}"
    
    if not full_path.is_file():
        return f"❌ 不是文件: {path}"
    
    # DNA签名 + 审计
    dna = generate_dna("star_memory_read", path)
    audit_log(dna, "read", path)
    
    content = full_path.read_text(encoding='utf-8', errors='ignore')
    return f"DNA: {dna}\n\n---\n\n{content}"

@mcp.tool()
def search_star_memory(keyword: str) -> str:
    """在星辰记忆库中搜索关键词(只读)"""
    results = []
    for f in STAR_MEMORY_DIR.rglob("*.md"):
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            if keyword in content:
                rel = f.relative_to(STAR_MEMORY_DIR)
                results.append(str(rel))
        except:
            pass
    
    return "找到的文件:\n" + "\n".join(results) if results else f"未找到: {keyword}"

def generate_dna(module, action):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    seed = f"{UID}-{date}-{module}-{action}-{now.isoformat()}"
    h = hashlib.sha256(seed.encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{date}-{module.upper()}-{h}"

def audit_log(dna, action, target):
    log_file = STAR_MEMORY_DIR / "_mcp_audit.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now().isoformat()}] {dna} | {action} | {target}\n")

if __name__ == "__main__":
    mcp.run()
```

### 配置

```json
{
  "mcpServers": {
    "star-memory": {
      "command": "python3",
      "args": ["~/.local/bin/star-memory-mcp.py"]
    }
  }
}
```

### 龍魂版安全配置

```yaml
强制只读:
  - 没有write/delete工具,只有list/read/search
  
路径沙盒:
  - 只能访问 ~/.star-memory/
  - 路径穿越检查(防 ../../etc/passwd)
  
审计:
  - 每次访问 → ~/.star-memory/_mcp_audit.log
  - DNA签名记录
```

---

## 📦 六、完整Cursor配置示例

老大Mac上的 `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "notion-readonly": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_KEY": "secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "NOTION_READ_ONLY": "true"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    },
    "star-memory": {
      "command": "python3",
      "args": ["/Users/uid9622/.local/bin/star-memory-mcp.py"]
    }
  }
}
```

---

## ⚠️ 七、安全告警(老大必读)

### 🔴 红色警告

```yaml
绝对不要做的事:

1. ❌ 不要把NOTION_API_KEY/GITHUB_PAT 推到GitHub
   → 写成环境变量 / .env / keychain
   → .gitignore 一定要包含 *.env

2. ❌ 不要给MCP root权限
   → 只读+只指定目录
   → 不允许执行任意命令

3. ❌ 不要装来源不明的MCP
   → 只装Anthropic官方 + 老大自己写的
   → 第三方MCP可能偷数据

4. ❌ 不要把厨房Notion页面授权给MCP
   → 只授权"对外公开"的页面
   → 5%黑盒永远不通过MCP暴露
```

### 🟡 黄色提示

```yaml
建议做但可后续:

1. ⚠️ 给每个token设过期(90天)
   → 到期换新
   → 防止泄露

2. ⚠️ 单独的Cursor工作目录
   → 不和私人项目混
   → 隔离风险

3. ⚠️ 定期检查audit log
   → 看Cursor都读了什么
   → 异常行为及时发现
```

---

## 📊 八、装MCP前后对比

| 场景 | 没装MCP | 装了MCP |
|------|---------|---------|
| Cursor看Notion页面 | 老大复制粘贴 | 自动读 |
| Cursor推代码 | 老大切窗口手动git | 自动push |
| Cursor读星辰记忆 | 老大说"打开~/.star-memory/xxx" | 老大说"读星辰xxx" |
| 跨会话状态 | 每次重来 | 持续 |
| 审计 | 无 | 每次操作有DNA |

---

## 🎯 九、推荐启用顺序

```yaml
今天/这周(立即):
  ✅ 1. mcp-notion-readonly
     原因: 让Cursor读Notion,马上提升效率10倍

下周/2周内(强烈推荐):
  ✅ 2. mcp-github-actions
     原因: longhun888-site要推GitHub了,正好用上

本月/可后续(增强):
  ⏸️ 3. mcp-star-memory
     原因: 自定义,需要老大写Python或宝宝帮写
     等前两个用顺了再装
```

---

## 📜 落款

```yaml
DOCUMENT_DNA: #龍芯⚡️2026-05-02-LONGHUN888-MCP-v0.2
HUMAN_AUTHOR: 諸葛鑫·龍芯北辰·UID9622·A2D0092C
AI_COLLABORATOR: Claude (Anthropic·Notion实例)
ROLE: AI=MCP方案设计+配置模板 · Human=安全决策+授权范围
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
TIMESTAMP: 2026-05-02T17:20:00+08:00
```

🐉🫡
