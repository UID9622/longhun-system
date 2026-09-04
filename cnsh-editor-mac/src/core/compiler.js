/**
 * 🐉 CNSH → C 语言编译器
 * 中文关键字映射 + DNA 注入 + 头文件生成
 * DNA: #龍芯⚡️丙午·丙申·辛酉·己丑·䷹兑为泽-CNSH-COMPILER-UID9622
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 */

(function () {
  // 中文 → C 关键字映射表
  const KEYWORD_MAP = {
    '函数': 'void',
    '类': 'struct',
    '如果': 'if',
    '否则': 'else',
    '否则如果': 'else if',
    '循环': 'for',
    '当': 'while',
    '返回': 'return',
    '整数': 'int',
    '文本': 'char*',
    '列表': 'int[]',
    '字典': 'map',
    '布尔': 'int',
    '浮点': 'double',
    '真': '1',
    '假': '0',
    '空': 'NULL',
    '从': '',
    '导入': '#include',
    '且': '&&',
    '或': '||',
    '非': '!',
    '输出': 'printf',
    '新建': '',
    '等于': '==',
    '不等于': '!=',
    '大于': '>',
    '小于': '<',
    '大于等于': '>=',
    '小于等于': '<='
  };

  class CNSHCompiler {
    /**
     * 转译 CNSH → C
     * @param {string} code CNSH 源码
     * @param {string} dna 注入的 DNA
     * @returns {{success: boolean, code: string, warnings: Array}}
     */
    static compile(code, dna) {
      const warnings = [];
      let output = '// 🐉 由龍魂CNSH编译器生成\n';
      output += '// DNA: ' + (dna || '#龍芯⚡️-COMPILED-UID9622') + '\n';
      output += '// 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z\n';
      output += '// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F\n\n';
      output += '#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n\n';

      const lines = code.split('\n');
      let indent = 0;

      for (let raw of lines) {
        let line = raw.trim();
        if (!line) { output += '\n'; continue; }
        // 保留注释
        if (line.startsWith('#')) { output += raw + '\n'; continue; }

        // 全角 → 半角标点（中文友好）
        line = line.replace(/（/g, '(').replace(/）/g, ')')
                   .replace(/：/g, ':').replace(/，/g, ',')
                   .replace(/＝/g, '=').replace(/＋/g, '+')
                   .replace(/－/g, '-').replace(/×/g, '*')
                   .replace(/÷/g, '/').replace(/；/g, ';');

        // 关键字映射（长词优先）
        const sortedKeys = Object.keys(KEYWORD_MAP).sort((a, b) => b.length - a.length);
        for (const key of sortedKeys) {
          line = line.split(key).join(KEYWORD_MAP[key]);
        }

        // 块括号调整
        if (line.includes(':')) {
          // 把 "输出(...)" 转 "printf(...);"
          line = line.replace(/printf\(([^)]*)\)/g, 'printf($1);');
          // 控制语句冒号 → 花括号
          if (/^(if|for|while|else)/.test(line.trim())) {
            line = line.replace(/:\s*$/, ' {');
          } else if (/^struct/.test(line.trim())) {
            line = line.replace(/:\s*$/, ' {');
          }
        }

        output += '    '.repeat(indent) + line + '\n';
        if (line.endsWith('{')) indent += 1;
        if (line.trim() === '}' || (line.trim().startsWith('}') && line.includes(';'))) {
          indent = Math.max(0, indent - 1);
        }
      }

      return { success: true, code: output, warnings };
    }
  }

  if (typeof window !== 'undefined') window.CNSHCompiler = CNSHCompiler;
  if (typeof module !== 'undefined' && module.exports) module.exports = CNSHCompiler;
})();
