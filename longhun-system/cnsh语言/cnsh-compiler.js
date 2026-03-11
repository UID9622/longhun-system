#!/usr/bin/env node

/**
 * CNSH编译器 v1.0
 * DNA追溯码：#ZHUGEXIN⚡️2025-12-31-CNSH编译器-v1.0
 * 
 * 功能：将CNSH代码转译为C代码
 * 创建者：Lucky·UID9622
 */

const fs = require('fs');
const path = require('path');

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

    if (ch === '"' || ch === "'" || ch === '「' || ch === '『') {
      const closeQuote = ch === '「' ? '」' : (ch === '『' ? '』' : ch);
      const value = this.readString(closeQuote);
      return { type: 'STRING', value, line: this.line, column: this.column };
    }

    if (/[0-9]/.test(ch)) {
      const value = this.readNumber();
      return { type: 'NUMBER', value, line: this.line, column: this.column };
    }

    if (/[\u4e00-\u9fa5a-zA-Z_]/.test(ch)) {
      const value = this.readIdentifier();
      const type = this.isKeyword(value) ? 'KEYWORD' : 'IDENTIFIER';
      return { type, value, line: this.line, column: this.column };
    }

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
      '打印', '输入', '真', '假', '空',
      '分配', '释放', '安全检查'
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
      if (token.value === '打印') {
        return this.parsePrintStatement();
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
    this.advance();
    const value = this.parseExpression();
    
    if (this.current().type === 'SEMICOLON') {
      this.advance();
    }
    
    return new ASTNode('PrintStatement', { value });
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
  constructor(ast) {
    this.ast = ast;
    this.indent = 0;
    this.output = [];
  }

  generate() {
    this.output.push('// Generated by CNSH Compiler v1.0');
    this.output.push('// DNA追溯码：#ZHUGEXIN⚡️2025-12-31-CNSH编译输出');
    this.output.push('');
    this.output.push('#include <stdio.h>');
    this.output.push('#include <stdlib.h>');
    this.output.push('#include <string.h>');
    this.output.push('#include <stdbool.h>');
    this.output.push('');
    
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
    const value = this.generateExpression(node.value);
    
    if (node.value.type === 'String') {
      this.emit(`printf("%s\\n", ${value});`);
    } else if (node.value.type === 'Number') {
      this.emit(`printf("%g\\n", (double)${value});`);
    } else {
      this.emit(`printf("%d\\n", ${value});`);
    }
  }

  generateExpression(node) {
    switch (node.type) {
      case 'Number':
        return node.value;
      case 'String':
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
      'char*': 'NULL',
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

// ==================== 编译器 ====================

class CNSHCompiler {
  compile(sourceCode, sourcePath) {
    console.log('🇨🇳 CNSH编译器 v1.0');
    console.log('DNA追溯码：#ZHUGEXIN⚡️2025-12-31-CNSH编译器');
    console.log('━━━━━━━━━━━━━━━━━━\n');
    
    try {
      console.log('📝 阶段1：词法分析...');
      const lexer = new Lexer(sourceCode);
      const tokens = lexer.tokenize();
      console.log(`   找到 ${tokens.length} 个token\n`);
      
      console.log('🌳 阶段2：语法分析...');
      const parser = new Parser(tokens);
      const ast = parser.parse();
      console.log('   生成抽象语法树\n');
      
      console.log('⚙️  阶段3：代码生成...');
      const generator = new CCodeGenerator(ast);
      const cCode = generator.generate();
      console.log('   生成C代码\n');
      
      const outputPath = sourcePath.replace('.cnsh', '.c');
      fs.writeFileSync(outputPath, cCode);
      console.log(`✅ 编译成功！`);
      console.log(`   输出文件：${outputPath}\n`);
      
      console.log('📦 下一步：');
      console.log(`   gcc ${outputPath} -o ${sourcePath.replace('.cnsh', '')}`);
      console.log(`   ./${sourcePath.replace('.cnsh', '')}\n`);
      
      return { success: true, outputPath, cCode };
      
    } catch (error) {
      console.error('❌ 编译失败：', error.message);
      return { success: false, error: error.message };
    }
  }
}

// ==================== Main ====================

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

module.exports = { CNSHCompiler, Lexer, Parser, CCodeGenerator };
