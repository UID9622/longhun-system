# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 🐉 CNSH 套件 · CNSH 脚本执行器
 * DNA: #龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-CNSH-EXECUTOR-UID9622
 */

import { defineTool } from '@deepseek-ai/dsh-tools'
import { readFile } from 'fs/promises'
import { LongHunEngine } from '../longhun-engine'

export const cnshExecutor = (engine: LongHunEngine) => defineTool({
  name: 'run_cnsh',
  description: '执行 CNSH 中文原生脚本。支持变量赋值、函数调用、条件判断等，所有执行结果自动绑定DNA追溯码',
  parameters: {
    type: 'object',
    properties: {
      script: {
        type: 'string',
        description: 'CNSH 脚本源码'
      },
      file: {
        type: 'string',
        description: '.cnsh 文件路径（与 script 二选一）'
      },
      args: {
        type: 'object',
        description: '脚本参数（键值对）',
        additionalProperties: true
      }
    }
  },
  execute: async ({ script, file, args = {} }, _ctx) => {
    let source = script
    if (file && !source) {
      try {
        source = await readFile(file, 'utf-8')
      } catch (e: any) {
        return {
          success: false,
          error: `读取文件失败: ${e.message}`,
          message: `❌ 无法读取 ${file}`
        }
      }
    }

    if (!source) {
      return {
        success: false,
        error: '请提供 script 或 file 参数',
        message: '❌ 缺少CNSH脚本源码'
      }
    }

    const result = await engine.cnsh.execute(source, args)

    return {
      success: true,
      output: result.output,
      dna: result.dna,
      tricolor: result.tricolor,
      message: `✅ CNSH 脚本执行成功，DNA: ${result.dna}`
    }
  }
})
