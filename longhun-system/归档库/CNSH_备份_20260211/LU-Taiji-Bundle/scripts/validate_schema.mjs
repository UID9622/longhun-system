#!/usr/bin/env node
// ============================================================================
// LU-Taiji Bundle JSON Schema 验证器
// ============================================================================
// 功能：验证所有 JSON 文件是否符合 Schema 定义
// DNA: #ZHUGEXIN⚡️2025-01-27-LU-TAIJI-VALIDATE-v2.1
// 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// ============================================================================

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ============================================================================
// ANSI 颜色定义
// ============================================================================
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',   // 绿色 - 成功
  red: '\x1b[31m',     // 红色 - 错误
  yellow: '\x1b[33m', // 黄色 - 警告
  blue: '\x1b[34m'     // 蓝色 - 信息
};

// ============================================================================
// Schema 定义
// ============================================================================
const schemas = {
  // manifest.json 的 Schema
  manifest: {
    type: 'object',
    required: ['bundleId', 'dnaCode', 'confirmationCode', 'version', 'creators'],
    properties: {
      bundleId: { type: 'string', pattern: '^LU-Taiji-Bundle-v\\d+\\.\\d+\\.\\d+$' },
      dnaCode: { type: 'string', pattern: '^#ZHUGEXIN⚡️\\d{4}-\\d{2}-\\d{2}-[A-Z-]+-v\\d+\\.\\d+\\.\\d+$' },
      confirmationCode: { type: 'string', pattern: '^#CONFIRM🌌9622-ONLY-ONCE🧬[A-Z0-9-]+$' },
      version: { type: 'string', pattern: '^\\d+\\.\\d+\\.\\d+$' }
    }
  },
  // LU-Taiji-2.1.json 的 Schema
  content: {
    type: 'object',
    required: ['model', 'structure'],
    properties: {
      model: {
        type: 'object',
        required: ['id', 'dnaCode', 'name', 'version', 'creators']
      },
      structure: {
        type: 'object',
        required: ['nodes', 'principles']
      }
    }
  },
  // LU-Taiji-Graph.json 的 Schema
  graph: {
    type: 'object',
    required: ['graph'],
    properties: {
      graph: {
        type: 'object',
        required: ['nodes', 'edges']
      }
    }
  }
};

// ============================================================================
// 验证器函数
// ============================================================================
function validate(data, schema, path = '') {
  const errors = [];

  // 类型检查
  if (schema.type && typeof data !== schema.type) {
    errors.push(`${path}: 期望类型 ${schema.type}，实际类型 ${typeof data}`);
  }

  // 必填字段检查
  if (schema.required) {
    for (const field of schema.required) {
      if (!(field in data)) {
        errors.push(`${path}: 缺少必填字段 '${field}'`);
      }
    }
  }

  // 正则表达式验证
  if (schema.pattern && typeof data === 'string') {
    const regex = new RegExp(schema.pattern);
    if (!regex.test(data)) {
      errors.push(`${path}: 正则验证失败 '${data}'`);
    }
  }

  // 嵌套属性验证
  if (schema.properties) {
    for (const [key, propSchema] of Object.entries(schema.properties)) {
      if (key in data) {
        const subErrors = validate(data[key], propSchema, `${path}.${key}`);
        errors.push(...subErrors);
      }
    }
  }

  return errors;
}

// ============================================================================
// 主验证函数
// ============================================================================
async function main() {
  console.log(`${colors.blue}═══════════════════════════════════════${colors.reset}`);
  console.log(`${colors.blue}  LU-Taiji Bundle Schema 验证器${colors.reset}`);
  console.log(`${colors.blue}═══════════════════════════════════════${colors.reset}\n`);

  const bundleRoot = path.join(__dirname, '..');
  let allPassed = true;

  // 验证 manifest.json
  console.log(`${colors.yellow}[1/4] 正在验证 manifest.json...${colors.reset}`);
  try {
    const manifestPath = path.join(bundleRoot, 'manifest.json');
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    const errors = validate(manifest, schemas.manifest, 'manifest');
    if (errors.length === 0) {
      console.log(`  ${colors.green}✓ manifest.json 验证通过${colors.reset}`);
    } else {
      console.log(`  ${colors.red}✗ manifest.json 验证失败:${colors.reset}`);
      errors.forEach(e => console.log(`    - ${e}`));
      allPassed = false;
    }
  } catch (err) {
    console.log(`  ${colors.red}✗ 读取 manifest.json 错误: ${err.message}${colors.reset}`);
    allPassed = false;
  }

  // 验证 LU-Taiji-2.1.json
  console.log(`\n${colors.yellow}[2/4] 正在验证 content/LU-Taiji-2.1.json...${colors.reset}`);
  try {
    const contentPath = path.join(bundleRoot, 'content', 'LU-Taiji-2.1.json');
    const content = JSON.parse(fs.readFileSync(contentPath, 'utf8'));
    const errors = validate(content, schemas.content, 'content');
    if (errors.length === 0) {
      console.log(`  ${colors.green}✓ LU-Taiji-2.1.json 验证通过${colors.reset}`);
    } else {
      console.log(`  ${colors.red}✗ LU-Taiji-2.1.json 验证失败:${colors.reset}`);
      errors.forEach(e => console.log(`    - ${e}`));
      allPassed = false;
    }
  } catch (err) {
    console.log(`  ${colors.red}✗ 读取 LU-Taiji-2.1.json 错误: ${err.message}${colors.reset}`);
    allPassed = false;
  }

  // 验证 LU-Taiji-Graph.json
  console.log(`\n${colors.yellow}[3/4] 正在验证 content/LU-Taiji-Graph.json...${colors.reset}`);
  try {
    const graphPath = path.join(bundleRoot, 'content', 'LU-Taiji-Graph.json');
    const graph = JSON.parse(fs.readFileSync(graphPath, 'utf8'));
    const errors = validate(graph, schemas.graph, 'graph');
    if (errors.length === 0) {
      console.log(`  ${colors.green}✓ LU-Taiji-Graph.json 验证通过${colors.reset}`);
    } else {
      console.log(`  ${colors.red}✗ LU-Taiji-Graph.json 验证失败:${colors.reset}`);
      errors.forEach(e => console.log(`    - ${e}`));
      allPassed = false;
    }
  } catch (err) {
    console.log(`  ${colors.red}✗ 读取 LU-Taiji-Graph.json 错误: ${err.message}${colors.reset}`);
    allPassed = false;
  }

  // 验证 placeholders.json
  console.log(`\n${colors.yellow}[4/4] 正在验证 placeholders.json...${colors.reset}`);
  try {
    const placeholdersPath = path.join(bundleRoot, 'placeholders.json');
    const placeholders = JSON.parse(fs.readFileSync(placeholdersPath, 'utf8'));
    if (placeholders.placeholders && typeof placeholders.placeholders === 'object') {
      console.log(`  ${colors.green}✓ placeholders.json 验证通过${colors.reset}`);
    } else {
      console.log(`  ${colors.red}✗ placeholders.json: 缺少 'placeholders' 对象${colors.reset}`);
      allPassed = false;
    }
  } catch (err) {
    console.log(`  ${colors.red}✗ 读取 placeholders.json 错误: ${err.message}${colors.reset}`);
    allPassed = false;
  }

  // 结果总结
  console.log(`\n${colors.blue}═══════════════════════════════════════${colors.reset}`);
  if (allPassed) {
    console.log(`${colors.green}  ✓ 所有验证通过！${colors.reset}`);
    console.log(`${colors.blue}═══════════════════════════════════════${colors.reset}`);
    process.exit(0);
  } else {
    console.log(`${colors.red}  ✗ 部分验证失败！${colors.reset}`);
    console.log(`${colors.blue}═══════════════════════════════════════${colors.reset}`);
    process.exit(1);
  }
}

// ============================================================================
// 执行主函数
// ============================================================================
main().catch(err => {
  console.error(`${colors.red}意外错误:${colors.reset}`, err);
  process.exit(1);
});
