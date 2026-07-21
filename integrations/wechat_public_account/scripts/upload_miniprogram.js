#!/usr/bin/env node
/**
 * Upload WeChat Mini Program using miniprogram-ci.
 *
 * Usage:
 *   node scripts/upload_miniprogram.js --version 1.0.0 --desc "initial upload"
 */

const ci = require('miniprogram-ci');
const path = require('path');
const fs = require('fs');

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {};
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace(/^--/, '');
    result[key] = args[i + 1];
  }
  return result;
}

async function main() {
  const args = parseArgs();
  const appid = process.env.WECHAT_APPID;
  const privateKeyPath = process.env.WECHAT_MINIPROGRAM_PRIVATE_KEY_PATH;

  if (!appid) {
    console.error('Error: WECHAT_APPID not set');
    process.exit(1);
  }
  if (!privateKeyPath) {
    console.error('Error: WECHAT_MINIPROGRAM_PRIVATE_KEY_PATH not set');
    process.exit(1);
  }

  const projectPath = path.resolve(__dirname, '..', 'miniprogram');
  if (!fs.existsSync(projectPath)) {
    console.error(`Error: mini program project not found at ${projectPath}`);
    process.exit(1);
  }

  const project = new ci.Project({
    appid,
    type: 'miniProgram',
    projectPath,
    privateKeyPath: path.resolve(privateKeyPath.replace('~', process.env.HOME)),
    ignores: ['node_modules/**/*'],
  });

  const version = args.version || '1.0.0';
  const desc = args.desc || `Longhun mini program upload at ${new Date().toISOString()}`;

  try {
    const uploadResult = await ci.upload({
      project,
      version,
      desc,
      setting: {
        es6: true,
        es7: true,
        minify: true,
        codeProtect: false,
        autoPrefixWXSS: true,
      },
      onProgressUpdate: (info) => {
        console.log(`[${info._status}] ${info.msg || ''}`);
      },
    });

    console.log('Upload successful:');
    console.log(JSON.stringify(uploadResult, null, 2));
  } catch (err) {
    console.error('Upload failed:', err.message);
    process.exit(1);
  }
}

main();
