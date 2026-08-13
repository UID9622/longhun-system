# 💻 cnsh-compiler.js - 完整编译器代码

> Notion URL: https://app.notion.com/p/cnsh-compiler-js-ef89b2a262404844ba72f2ed4aa42cdb
> Created: 2025-12-30T23:42:00.000Z
> Last edited: 2026-07-01T15:39:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
DNA追溯码： #ZHUGEXIN⚡️2025-12-31-CNSH语言-V1.0
---
## ✅ 关键修复
---
## 📦 完整代码
由于代码超过1000行，请直接从以下位置获取：
### 方式1：从修复页面复制
回到上级页面 → 查看"修复2"部分 → 完整代码
### 方式2：核心结构预览
```javascript
#!/usr/bin/env node

/**
 * CNSH编译器 v1.0
 * DNA追溯码：#ZHUGEXIN⚡️2025-12-31-CNSH语言-V1.0
 */

const fs = require('fs');
const path = require('path');

// ==================== 三色审计系统 ====================
class ThreeColorAudit {
  constructor() {
    this.rules = {
      红色: [...],
      黄色: [...]
    };
  }
  
  检查(sourceCode) {
    // 红色/黄色/绿色审计逻辑
  }
}

// ==================== 词法分析器 ====================
class Lexer {
  constructor(source) {...}
  tokenize() {...}
}

// ==================== 语法分析器 ====================
class Parser {
  constructor(tokens) {...}
  parse() {...}
  
  // 🔧 关键修复点
  parseFunctionDeclaration() {
    // ...
    while (this.current().type !== 'RBRACE') {  // ✅ 修复后
      const stmt = this.parseStatement();
      if (stmt) {
        body.push(stmt);
      }
    }
    // ...
  }
}

// ==================== C代码生成器 ====================
class CCodeGenerator {
  constructor(ast) {...}
  generate() {...}
}

// ==================== 编译器主程序 ====================
class CNSHCompiler {
  constructor() {
    this.auditSystem = new ThreeColorAudit();
  }
  
  compile(sourceCode, sourcePath) {
    // 三色审计 → 词法分析 → 语法分析 → 代码生成
  }
}

function main() {...}

if (require.main === module) {
  main();
}

module.exports = { CNSHCompiler, Lexer, Parser, CCodeGenerator, ThreeColorAudit };
```
---
## 🎯 核心特性
### 1. 三色审计系统
```javascript
// 红色：暴力、违法、仇恨
// 黄色：敏感话题
// 绿色：安全内容
```
### 2. 完整编译流程
```javascript
CNSH源码 → 三色审计 → 词法分析 → 语法分析 → AST → C代码
```
### 3. DNA追溯
```javascript
// 每个生成的C文件都带DNA追溯码
```
---
完整代码请查看上级页面！ 💪
