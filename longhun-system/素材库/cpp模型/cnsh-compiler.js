#!/usr/bin/env node

/**
 * CNSH编译器 v1.0
 * DNA追溯码：#ZHUGEXIN-2026-01-27-CNSH-compiler-v1.0
 * 创建者：诸葛鑫（UID9622）
 * 
 * 功能：将CNSH代码转译为C代码
 * 特性：集成三色审计系统、DNA追溯机制
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// ==================== 三色审计系统 ====================

class ThreeColorAudit {
  constructor() {
    this.rules = {
      红色: [
        { pattern: /暴力|血腥|杀人|灭口|下毒|爆炸|炸弹|枪支改造|自制武器|屠杀|恐袭/g, reason: '暴力内容' },
        { pattern: /诈骗|洗钱|贩毒|制毒|走私|博彩漏洞|黑产|外挂售卖/g, reason: '违法与犯罪' },
        { pattern: /入侵|提权|爆破|绕过验证|后门|免杀|木马|钓鱼链接制作|勒索/g, reason: '黑客入侵与破坏' },
        { pattern: /删库|rm -rf|格式化硬盘|清空数据|销毁证据/g, reason: '不可逆破坏' },
        { pattern: /人口贩卖|未成年人伤害/g, reason: 'P0++红线' }
      ],
      黄色: [
        { pattern: /政治敏感|宗教冲突|极端主义|政治煽动|仇恨言论/g, reason: '高争议敏感话题' },
        { pattern: /\b\d{15,18}\b/g, reason: '可能包含身份证号' },
        { pattern: /AKIA[0-9A-Z]{16}/g, reason: '可能包含AWS密钥' },
        { pattern: /-----BEGIN (RSA|OPENSSH|EC) PRIVATE KEY-----/g, reason: '可能包含私钥' }
      ]
    };
  }

  检查(sourceCode) {
    // 红色审计
    for (const rule of this.rules.红色) {
      if (rule.pattern.test(sourceCode)) {
        return {
          级别: '红色',
          原因: rule.reason,
          操作: '阻断编译'
        };
      }
    }

    // 黄色审计
    for (const rule of this.rules.黄色) {
      if (rule.pattern.test(sourceCode)) {
        return {
          级别: '黄色',
          原因: rule.reason,
          操作: '警告但继续'
        };
      }
    }

    return {
      级别: '绿色',
      原因: '内容安全',
      操作: '允许编译'
    };
  }
}

// ==================== DNA追溯系统 ====================

class DNATracer {
  constructor() {
    this.prefix = '#ZHUGEXIN';
  }

  生成(sourceCode, projectName, version = 'v1.0') {
    const date = new Date().toISOString().split('T')[0];
    const hash = crypto
      .createHash('sha256')
      .update(sourceCode + Date.now())
      .digest('hex')
      .substring(0, 8);
    
    return `${this.prefix}-${date}-${projectName}-${version}-${hash}`;
  }
}

// ==================== 词法分析器 ====================

class Lexer {
  constructor(source) {
    this.source = source;
    this.pos = 0;
    this.line = 1;
    this.column = 1;
  }

  skipWhitespace() {
    while (this.pos < this.source.length) {
      const ch = this.source[this.pos];
      if (ch === ' ' || ch === '\t' || ch === '\r') {
        this.pos++;
        this.column++;
      } else if (ch === '\n') {
        this.pos++;
        this.line++;
        this.column = 1;
      } else {
        break;
      }
    }
  }

  skipComment() {
    if (this.source[this.pos] === '#') {
      while (this.pos < this.source.length && this.source[this.pos] !== '\n') {
        this.pos++;
      }
      return true;
    }
    return false;
  }

  readIdentifier() {
    let start = this.pos;
    while (this.pos < this.source.length) {
      const ch = this.source[this.pos];
      if (/[\u4e00-\u9fa5a-zA-Z0-9_]/.test(ch)) {
        this.pos++;
        this.column++;
      } else {
        break;
      }
    }
    return this.source.slice(start, this.pos);
  }

  readNumber() {
    let start = this.pos;
    let hasDecimal = false;

    while (this.pos < this.source.length) {
      const ch = this.source[this.pos];
      if (/[0-9]/.test(ch)) {
        this.pos++;
        this.column++;
      } else if (ch === '.' && !hasDecimal) {
        hasDecimal = true;
        this.pos++;
        this.column++;
      } else {
        break;
      }
    }

    return this.source.slice(start, this.pos);
  }

  readString(quote) {
    let result = '';
    this.pos++;
    this.column++;

    while (this.pos < this.source.length) {
      const ch = this.source[this.pos];

      if (ch === quote) {
        this.pos++;
        this.column++;
        break;
      } else if (ch === '\\') {
        this.pos++;
        this.column++;
        if (this.pos < this.source.length) {
          result += '\\' + this.source[this.pos];
          this.pos++;
          this.column++;
        }
      } else {
        result += ch;
        this.pos++;
        this.column++;
      }
    }

    return result;
  }

  nextToken() {
    this.skipWhitespace();

    if (this.pos >= this.source.length) {
      return { type: 'EOF', value: null, line: this.line, column: this.column };
    }

    if (this.skipComment()) {
      return this.nextToken();
    }

    const ch = this.source[this.pos];

    // 字符串
    if (ch === '"' || ch === "'" || ch === '「' || ch === '『') {
      const closeQuote = ch === '「' ? '」' : (ch === '『' ? '』' : ch);
      const value = this.readString(closeQuote);
      return { type: 'STRING', value, line: this.line, column: this.column };
    }

    // 数字
    if (/[0-9]/.test(ch)) {
      const value = this.readNumber();
      return { type: 'NUMBER', value, line: this.line, column: this.column };
    }

    // 标识符或关键字
    if (/[\u4e00-\u9fa5a-zA-Z_]/.test(ch)) {
      const value = this.readIdentifier();
      const type = this.isKeyword(value) ? 'KEYWORD' : 'IDENTIFIER';
      return { type, value, line: this.line, column: this.column };
    }

    // 符号
    const symbols = {
      '=': 'ASSIGN',
      '+': 'PLUS',
      '-': 'MINUS',
      '*': 'MULTIPLY',
      '/': 'DIVIDE',
      '%': 'MODULO',
      '(': 'LPAREN',
      ')': 'RPAREN',
      '{': 'LBRACE',
      '}': 'RBRACE',
      '[': 'LBRACKET',
      ']': 'RBRACKET',
      '【': 'LBRACKET',
      '】': 'RBRACKET',
      ';': 'SEMICOLON',
      ',': 'COMMA',
      '.': 'DOT',
      '>': 'GT',
      '<': 'LT',
      '!': 'NOT',
      '&': 'AND',
      '|': 'OR'
    };

    if (symbols[ch]) {
      this.pos++;
      this.column++;

      const nextCh = this.source[this.pos];
      if (ch === '=' && nextCh === '=') {
        this.pos++;
        this.column++;
        return { type: 'EQ', value: '==', line: this.line, column: this.column };
      }
      if (ch === '!' && nextCh === '=') {
        this.pos++;
        this.column++;
        return { type: 'NEQ', value: '!=', line: this.line, column: this.column };
      }
      if (ch === '>' && nextCh === '=') {
        this.pos++;
        this.column++;
        return { type: 'GTE', value: '>=', line: this.line, column: this.column };
      }
      if (ch === '<' && nextCh === '=') {
        this.pos++;
        this.column++;
        return { type: 'LTE', value: '<=', line: this.line, column: this.column };
      }
      if (ch === '&' && nextCh === '&') {
        this.pos++;
        this.column++;
        return { type: 'LOGICAL_AND', value: '&&', line: this.line, column: this.column };
      }
      if (ch === '|' && nextCh === '|') {
        this.pos++;
        this.column++;
        return { type: 'LOGICAL_OR', value: '||', line: this.line, column: this.column };
      }

      return { type: symbols[ch], value: ch, line: this.line, column: this.column };
    }

    // 未知字符
    this.pos++;
    this.column++;
    return { type: 'UNKNOWN', value: ch, line: this.line, column: this.column };
  }

  isKeyword(word) {
    const keywords = [
      '整数', '小数', '文本', '真假', '空值',
      '如果', '否则', '循环', '当', '返回', '跳出', '继续',
      '函数', '类', '结构', '返回类型',
      'DNA追溯', '三色审计',
      '熔断',
      '真', '假', '空'
    ];
    return keywords.includes(word);
  }

  tokenize() {
    const tokens = [];
    let token;

    do {
      token = this.nextToken();
      tokens.push(token);
    } while (token.type !== 'EOF');

    return tokens;
  }
}

// ==================== AST节点 ====================

class ASTNode {
  constructor(type, props = {}) {
    this.type = type;
    Object.assign(this, props);
  }
}

// ==================== 语法分析器 ====================

class Parser {
  constructor(tokens) {
    this.tokens = tokens;
    this.pos = 0;
  }

  current() {
    return this.tokens[this.pos];
  }

  advance() {
    this.pos++;
    return this.tokens[this.pos - 1];
  }

  peek() {
    // 查看下一个token，但不消费它
    if (this.pos < this.tokens.length - 1) {
      return this.tokens[this.pos + 1];
    }
    return null;
  }

  expect(type, value = null) {
    const token = this.current();
    if (token.type !== type || (value && token.value !== value)) {
      throw new Error(
        `语法错误 (行${token.line}): 期望 ${type}` +
        (value ? ` "${value}"` : '') +
        `, 但得到 ${token.type} "${token.value}"`
      );
    }
    return this.advance();
  }

  parse() {
    const statements = [];

    while (this.current().type !== 'EOF') {
      const stmt = this.parseStatement();
      if (stmt) {
        statements.push(stmt);
      }
    }

    return new ASTNode('Program', { statements });
  }

  parseStatement() {
    const token = this.current();

    if (token.type === 'KEYWORD') {
      if (['整数', '小数', '文本', '真假'].includes(token.value)) {
        return this.parseVariableDeclaration();
      }
      if (token.value === '函数') {
        return this.parseFunctionDeclaration();
      }
      if (token.value === '如果') {
        return this.parseIfStatement();
      }
      if (token.value === '循环') {
        return this.parseLoopStatement();
      }
      if (token.value === '返回') {
        return this.parseReturnStatement();
      }
    }

    if (token.type === 'IDENTIFIER') {
      // 检查是否是标准库函数调用（打印、提示、报错等）
      if (['打印', '提示', '报错', '熔断', '转文本', '拼接', '包含', '当前时间', '记录日志', '生成追溯', '输入文本', '确认'].includes(token.value)) {
        // 检查是否是语法糖形式：函数名「参数」（省略括号）
        const nextToken = this.peek();
        if (nextToken && nextToken.type === 'STRING') {
          // 语法糖：函数名「参数」 → 函数名(参数)
          const funcName = token.value;
          this.advance(); // 消费函数名token
          const argToken = this.current(); // 获取字符串token
          const argValue = argToken.value;
          this.advance(); // 消费字符串token
          // 返回一个函数调用节点
          return new ASTNode('ExpressionStatement', {
            expression: new ASTNode('FunctionCall', {
              name: funcName,
              args: [new ASTNode('StringLiteral', { value: argValue })]
            })
          });
        }
        return this.parseExpressionStatement();
      }
    }

    return this.parseExpressionStatement();
  }

  parseVariableDeclaration() {
    const typeToken = this.advance();
    const nameToken = this.expect('IDENTIFIER');

    let value = null;
    if (this.current().type === 'ASSIGN') {
      this.advance();
      value = this.parseExpression();
    }

    if (this.current().type === 'SEMICOLON') {
      this.advance();
    }

    return new ASTNode('VariableDeclaration', {
      varType: typeToken.value,
      name: nameToken.value,
      value
    });
  }

  parseFunctionDeclaration() {
    this.advance();
    const nameToken = this.expect('IDENTIFIER');

    this.expect('LPAREN');
    const params = [];

    while (this.current().type !== 'RPAREN') {
      const typeToken = this.current();
      if (!['整数', '小数', '文本', '真假'].includes(typeToken.value)) {
        break;
      }
      this.advance();

      const paramName = this.expect('IDENTIFIER');
      params.push({
        type: typeToken.value,
        name: paramName.value
      });

      if (this.current().type === 'COMMA') {
        this.advance();
      }
    }

    this.expect('RPAREN');

    let returnType = '空值';
    if (this.current().type === 'KEYWORD' && this.current().value === '返回类型') {
      this.advance();
      returnType = this.advance().value;
    }

    this.expect('LBRACE');
    const body = [];

    while (this.current().type !== 'RBRACE') {
      const stmt = this.parseStatement();
      if (stmt) {
        body.push(stmt);
      }
    }

    this.expect('RBRACE');

    return new ASTNode('FunctionDeclaration', {
      name: nameToken.value,
      params,
      returnType,
      body
    });
  }

  parseIfStatement() {
    this.advance();
    this.expect('LBRACKET');
    const condition = this.parseExpression();
    this.expect('RBRACKET');

    this.expect('LBRACE');
    const thenBody = [];
    while (this.current().type !== 'RBRACE') {
      const stmt = this.parseStatement();
      if (stmt) {
        thenBody.push(stmt);
      }
    }
    this.expect('RBRACE');

    let elseBody = null;
    if (this.current().type === 'KEYWORD' && this.current().value === '否则') {
      this.advance();
      this.expect('LBRACE');
      elseBody = [];
      while (this.current().type !== 'RBRACE') {
        const stmt = this.parseStatement();
        if (stmt) {
          elseBody.push(stmt);
        }
      }
      this.expect('RBRACE');
    }

    return new ASTNode('IfStatement', {
      condition,
      thenBody,
      elseBody
    });
  }

  parseLoopStatement() {
    this.advance();
    this.expect('LBRACKET');
    const times = this.parseExpression();
    this.expect('RBRACKET');

    this.expect('LBRACE');
    const body = [];
    while (this.current().type !== 'RBRACE') {
      const stmt = this.parseStatement();
      if (stmt) {
        body.push(stmt);
      }
    }
    this.expect('RBRACE');

    return new ASTNode('LoopStatement', {
      times,
      body
    });
  }

  parseReturnStatement() {
    this.advance();

    let value = null;
    if (this.current().type !== 'SEMICOLON') {
      value = this.parseExpression();
    }

    if (this.current().type === 'SEMICOLON') {
      this.advance();
    }

    return new ASTNode('ReturnStatement', { value });
  }

  parsePrintStatement() {
    const printType = this.advance().value;
    const value = this.parseExpression();

    if (this.current().type === 'SEMICOLON') {
      this.advance();
    }

    return new ASTNode('PrintStatement', { printType, value });
  }

  parseExpressionStatement() {
    const expr = this.parseExpression();

    if (this.current().type === 'SEMICOLON') {
      this.advance();
    }

    return new ASTNode('ExpressionStatement', { expression: expr });
  }

  parseExpression() {
    return this.parseAssignment();
  }

  parseAssignment() {
    const left = this.parseLogicalOr();

    if (this.current().type === 'ASSIGN') {
      this.advance();
      const right = this.parseAssignment();
      return new ASTNode('Assignment', { left, right });
    }

    return left;
  }

  parseLogicalOr() {
    let left = this.parseLogicalAnd();

    while (this.current().type === 'LOGICAL_OR') {
      const op = this.advance().value;
      const right = this.parseLogicalAnd();
      left = new ASTNode('BinaryOp', { op, left, right });
    }

    return left;
  }

  parseLogicalAnd() {
    let left = this.parseEquality();

    while (this.current().type === 'LOGICAL_AND') {
      const op = this.advance().value;
      const right = this.parseEquality();
      left = new ASTNode('BinaryOp', { op, left, right });
    }

    return left;
  }

  parseEquality() {
    let left = this.parseComparison();

    while (['EQ', 'NEQ'].includes(this.current().type)) {
      const op = this.advance().value;
      const right = this.parseComparison();
      left = new ASTNode('BinaryOp', { op, left, right });
    }

    return left;
  }

  parseComparison() {
    let left = this.parseTerm();

    while (['GT', 'LT', 'GTE', 'LTE'].includes(this.current().type)) {
      const op = this.advance().value;
      const right = this.parseTerm();
      left = new ASTNode('BinaryOp', { op, left, right });
    }

    return left;
  }

  parseTerm() {
    let left = this.parseFactor();

    while (['PLUS', 'MINUS'].includes(this.current().type)) {
      const op = this.advance().value;
      const right = this.parseFactor();
      left = new ASTNode('BinaryOp', { op, left, right });
    }

    return left;
  }

  parseFactor() {
    let left = this.parseUnary();

    while (['MULTIPLY', 'DIVIDE', 'MODULO'].includes(this.current().type)) {
      const op = this.advance().value;
      const right = this.parseUnary();
      left = new ASTNode('BinaryOp', { op, left, right });
    }

    return left;
  }

  parseUnary() {
    if (['MINUS', 'NOT'].includes(this.current().type)) {
      const op = this.advance().value;
      const operand = this.parseUnary();
      return new ASTNode('UnaryOp', { op, operand });
    }

    return this.parsePrimary();
  }

  parsePrimary() {
    const token = this.current();

    if (token.type === 'NUMBER') {
      this.advance();
      return new ASTNode('Number', { value: token.value });
    }

    if (token.type === 'STRING') {
      this.advance();
      return new ASTNode('String', { value: token.value });
    }

    if (token.type === 'KEYWORD') {
      if (token.value === '真') {
        this.advance();
        return new ASTNode('Boolean', { value: true });
      }
      if (token.value === '假') {
        this.advance();
        return new ASTNode('Boolean', { value: false });
      }
      if (token.value === '空') {
        this.advance();
        return new ASTNode('Null', {});
      }
    }

    if (token.type === 'IDENTIFIER') {
      this.advance();

      if (this.current().type === 'LPAREN') {
        this.advance();
        const args = [];

        while (this.current().type !== 'RPAREN') {
          args.push(this.parseExpression());
          if (this.current().type === 'COMMA') {
            this.advance();
          }
        }

        this.expect('RPAREN');
        return new ASTNode('FunctionCall', { name: token.value, args });
      }

      return new ASTNode('Identifier', { name: token.value });
    }

    if (token.type === 'LPAREN') {
      this.advance();
      const expr = this.parseExpression();
      this.expect('RPAREN');
      return expr;
    }

    throw new Error(`语法错误 (行${token.line}): 意外的token ${token.type} "${token.value}"`);
  }
}

// ==================== C代码生成器 ====================

class CCodeGenerator {
  constructor(ast, dnaCode = '') {
    this.ast = ast;
    this.dnaCode = dnaCode;
    this.indent = 0;
    this.output = [];
  }

  generate() {
    // C语言头文件
    this.output.push('// Generated by CNSH Compiler v1.0');
    this.output.push(`// DNA追溯码：${this.dnaCode}`);
    this.output.push('// 创建者：诸葛鑫（UID9622）');
    this.output.push('');
    this.output.push('#include <stdio.h>');
    this.output.push('#include <stdlib.h>');
    this.output.push('#include <string.h>');
    this.output.push('#include <stdbool.h>');
    this.output.push('#include <time.h>');
    this.output.push('');

    // 标准库函数声明
    this.output.push('// ==================== CNSH标准库 ====================');
    this.output.push('');
    this.output.push('void 打印(const char* content) {');
    this.output.push('    printf("%s\\n", content);');
    this.output.push('}');
    this.output.push('');
    this.output.push('void 提示(const char* content) {');
    this.output.push('    printf("⚠️ 提示：%s\\n", content);');
    this.output.push('}');
    this.output.push('');
    this.output.push('void 报错(const char* content) {');
    this.output.push('    printf("❌ 错误：%s\\n", content);');
    this.output.push('    exit(1);');
    this.output.push('}');
    this.output.push('');
    this.output.push('char* 拼接(const char* a, const char* b) {');
    this.output.push('    size_t len_a = strlen(a);');
    this.output.push('    size_t len_b = strlen(b);');
    this.output.push('    char* result = malloc(len_a + len_b + 1);');
    this.output.push('    strcpy(result, a);');
    this.output.push('    strcat(result, b);');
    this.output.push('    return result;');
    this.output.push('}');
    this.output.push('');
    this.output.push('bool 包含(const char* text, const char* keyword) {');
    this.output.push('    return strstr(text, keyword) != NULL;');
    this.output.push('}');
    this.output.push('');
    this.output.push('char* 当前时间() {');
    this.output.push('    time_t now = time(NULL);');
    this.output.push('    char* time_str = malloc(64);');
    this.output.push('    strftime(time_str, 64, "%Y-%m-%d %H:%M:%S", localtime(&now));');
    this.output.push('    return time_str;');
    this.output.push('}');
    this.output.push('');
    this.output.push('char* 转文本(int number) {');
    this.output.push('    char* str = malloc(32);');
    this.output.push('    sprintf(str, "%d", number);');
    this.output.push('    return str;');
    this.output.push('}');
    this.output.push('');

    // 生成程序体
    this.generateProgram(this.ast);

    // 添加main函数
    this.output.push('');
    this.output.push('int main() {');
    this.output.push('    主函数();');
    this.output.push('    return 0;');
    this.output.push('}');

    return this.output.join('\n');
  }

  generateProgram(node) {
    for (const stmt of node.statements) {
      this.generateStatement(stmt);
    }
  }

  generateStatement(node) {
    switch (node.type) {
      case 'VariableDeclaration':
        this.generateVariableDeclaration(node);
        break;
      case 'FunctionDeclaration':
        this.generateFunctionDeclaration(node);
        break;
      case 'IfStatement':
        this.generateIfStatement(node);
        break;
      case 'LoopStatement':
        this.generateLoopStatement(node);
        break;
      case 'ReturnStatement':
        this.generateReturnStatement(node);
        break;
      case 'PrintStatement':
        this.generatePrintStatement(node);
        break;
      case 'ExpressionStatement':
        this.emit(this.generateExpression(node.expression) + ';');
        break;
    }
  }

  generateVariableDeclaration(node) {
    const cType = this.cnshTypeToCType(node.varType);
    const value = node.value ? this.generateExpression(node.value) : this.getDefaultValue(cType);
    this.emit(`${cType} ${node.name} = ${value};`);
  }

  generateFunctionDeclaration(node) {
    const returnType = this.cnshTypeToCType(node.returnType);
    const params = node.params
      .map(p => `${this.cnshTypeToCType(p.type)} ${p.name}`)
      .join(', ');

    this.emit(`${returnType} ${node.name}(${params}) {`);
    this.indent++;

    for (const stmt of node.body) {
      this.generateStatement(stmt);
    }

    this.indent--;
    this.emit('}');
    this.emit('');
  }

  generateIfStatement(node) {
    const condition = this.generateExpression(node.condition);
    this.emit(`if (${condition}) {`);
    this.indent++;

    for (const stmt of node.thenBody) {
      this.generateStatement(stmt);
    }

    this.indent--;

    if (node.elseBody) {
      this.emit('} else {');
      this.indent++;

      for (const stmt of node.elseBody) {
        this.generateStatement(stmt);
      }

      this.indent--;
    }

    this.emit('}');
  }

  generateLoopStatement(node) {
    const times = this.generateExpression(node.times);
    this.emit(`for (int __i = 0; __i < ${times}; __i++) {`);
    this.indent++;

    for (const stmt of node.body) {
      this.generateStatement(stmt);
    }

    this.indent--;
    this.emit('}');
  }

  generateReturnStatement(node) {
    if (node.value) {
      const value = this.generateExpression(node.value);
      this.emit(`return ${value};`);
    } else {
      this.emit('return;');
    }
  }

  generatePrintStatement(node) {
    const value = this.generateExpression(node.value) || '""';

    if (node.printType === '提示') {
      this.emit(`提示(${value});`);
    } else if (node.printType === '报错') {
      this.emit(`报错(${value});`);
    } else if (node.printType === '熔断') {
      this.emit(`报错(${value});`);
    } else {
      this.emit(`打印(${value});`);
    }
  }

  generateExpression(node) {
    switch (node.type) {
      case 'Number':
        return node.value;
      case 'String':
      case 'StringLiteral':
        return `"${node.value}"`;
      case 'Boolean':
        return node.value ? 'true' : 'false';
      case 'Null':
        return 'NULL';
      case 'Identifier':
        return node.name;
      case 'BinaryOp':
        const left = this.generateExpression(node.left);
        const right = this.generateExpression(node.right);
        return `(${left} ${node.op} ${right})`;
      case 'UnaryOp':
        const operand = this.generateExpression(node.operand);
        return `(${node.op}${operand})`;
      case 'Assignment':
        const assignLeft = this.generateExpression(node.left);
        const assignRight = this.generateExpression(node.right);
        return `${assignLeft} = ${assignRight}`;
      case 'FunctionCall':
        const args = node.args.map(arg => this.generateExpression(arg)).join(', ');
        return `${node.name}(${args})`;
      default:
        return '';
    }
  }

  cnshTypeToCType(cnshType) {
    const typeMap = {
      '整数': 'int',
      '小数': 'double',
      '文本': 'char*',
      '真假': 'bool',
      '空值': 'void'
    };
    return typeMap[cnshType] || 'void';
  }

  getDefaultValue(cType) {
    const defaults = {
      'int': '0',
      'double': '0.0',
      'char*': '""',
      'bool': 'false',
      'void': ''
    };
    return defaults[cType] || 'NULL';
  }

  emit(code) {
    const indentStr = '    '.repeat(this.indent);
    this.output.push(indentStr + code);
  }
}

// ==================== 编译器主程序 ====================

class CNSHCompiler {
  constructor() {
    this.version = '1.0.0';
    this.auditSystem = new ThreeColorAudit();
    this.dnaTracer = new DNATracer();
  }

  compile(sourceCode, sourcePath) {
    console.log('🇨🇳 CNSH编译器 v' + this.version);
    console.log('DNA追溯码：#ZHUGEXIN-2026-01-27-CNSH-compiler-v1.0');
    console.log('创建者：诸葛鑫（UID9622）');
    console.log('━━━━━━━━━━━━━━━━━━\n');

    try {
      // 三色审计
      console.log('🛡️ 阶段0：三色审计...');
      const auditResult = this.auditSystem.检查(sourceCode);

      if (auditResult.级别 === '红色') {
        console.error(`🔴 三色审计阻断：${auditResult.原因}`);
        console.error('   操作：' + auditResult.操作);
        console.error('   编译终止\n');
        return { success: false, error: `三色审计阻断：${auditResult.原因}` };
      } else if (auditResult.级别 === '黄色') {
        console.warn(`🟡 三色审计警告：${auditResult.原因}`);
        console.warn('   操作：' + auditResult.操作);
        console.warn('   继续编译，但请注意内容');
      } else {
        console.log(`🟢 三色审计通过：${auditResult.原因}`);
      }
      console.log('');

      // 生成DNA追溯码
      const projectName = path.basename(sourcePath, '.cnsh');
      const dnaCode = this.dnaTracer.生成(sourceCode, projectName, 'v1.0');
      console.log('🧬 DNA追溯码：' + dnaCode);
      console.log('');

      // 词法分析
      console.log('📝 阶段1：词法分析...');
      const lexer = new Lexer(sourceCode);
      const tokens = lexer.tokenize();
      console.log(`   找到 ${tokens.length} 个token\n`);

      // 语法分析
      console.log('🌳 阶段2：语法分析...');
      const parser = new Parser(tokens);
      const ast = parser.parse();
      console.log('   生成抽象语法树\n');

      // 代码生成
      console.log('⚙️  阶段3：代码生成...');
      const generator = new CCodeGenerator(ast, dnaCode);
      const cCode = generator.generate();
      console.log('   生成C代码\n');

      // 保存输出
      const outputPath = sourcePath.replace('.cnsh', '.c');
      fs.writeFileSync(outputPath, cCode);
      console.log(`✅ 编译成功！`);
      console.log(`   输出文件：${outputPath}\n`);

      console.log('📦 下一步：');
      console.log(`   gcc ${outputPath} -o ${sourcePath.replace('.cnsh', '')}`);
      console.log(`   ./${sourcePath.replace('.cnsh', '')}\n`);

      return { success: true, outputPath, cCode, dnaCode };

    } catch (error) {
      console.error('❌ 编译失败：', error.message);
      return { success: false, error: error.message };
    }
  }
}

// ==================== 命令行接口 ====================

function main() {
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.log('用法: node cnsh-compiler.js <文件.cnsh>');
    console.log('示例: node cnsh-compiler.js hello.cnsh');
    process.exit(1);
  }

  const sourcePath = args[0];

  if (!fs.existsSync(sourcePath)) {
    console.error(`错误：文件不存在 ${sourcePath}`);
    process.exit(1);
  }

  const sourceCode = fs.readFileSync(sourcePath, 'utf-8');
  const compiler = new CNSHCompiler();
  const result = compiler.compile(sourceCode, sourcePath);

  process.exit(result.success ? 0 : 1);
}

if (require.main === module) {
  main();
}

module.exports = { CNSHCompiler, Lexer, Parser, CCodeGenerator, ThreeColorAudit, DNATracer };
