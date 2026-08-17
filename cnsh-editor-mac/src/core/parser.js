/**
 * 🐉 CNSH 语法解析器
 * 中文关键字 → 词法单元 → 结构提取（函数/类/变量/流程）
 * DNA: #龍芯⚡️丙午·丙申·辛酉·丑时-CNSH-PARSER-UID9622
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 */

(function () {
  const KEYWORDS = [
    '函数', '类', '如果', '否则如果', '否则', '循环', '当', '返回', '从', '导入',
    '整数', '文本', '列表', '字典', '布尔', '浮点', '真', '假', '空', '新建'
  ];

  class CNSHParser {
    /**
     * 解析 CNSH 源码，提取结构信息
     * @param {string} code
     * @returns {{functions: Array, classes: Array, keywords: Array, errors: Array, lineCount: number}}
     */
    static parse(code) {
      const lines = code.split('\n');
      const functions = [];
      const classes = [];
      const keywordHits = new Set();
      const errors = [];

      lines.forEach((line, i) => {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith('#')) return;

        // 函数定义（支持中文名）
        let m = trimmed.match(/^函数\s+([\w\u4e00-\u9fa5]+)\s*\(/);
        if (m) {
          functions.push({ name: m[1], line: i + 1 });
          keywordHits.add('函数');
          return;
        }

        // 类定义（支持中文名）
        m = trimmed.match(/^类\s+([\w\u4e00-\u9fa5]+)/);
        if (m) {
          classes.push({ name: m[1], line: i + 1 });
          keywordHits.add('类');
          return;
        }

        // 统计其它关键字
        for (const kw of KEYWORDS) {
          if (trimmed.includes(kw)) keywordHits.add(kw);
        }

        // 常见错误检查
        if (trimmed.includes('：') && !trimmed.includes(':')) {
          // 全角冒号提示
          errors.push({ line: i + 1, msg: '使用全角冒号「：」，建议改为半角「:」' });
        }
        if ((trimmed.match(/\(/g) || []).length !== (trimmed.match(/\)/g) || []).length) {
          errors.push({ line: i + 1, msg: '括号不配对' });
        }
      });

      return {
        functions,
        classes,
        keywords: [...keywordHits],
        errors,
        lineCount: lines.length
      };
    }

    /**
     * 词法单元（供高亮/补全使用）
     * @param {string} code
     */
    static tokenize(code) {
      const tokens = [];
      const re = /#龍芯⚡️[^\s]+|#[^\n]*|"[^"]*"|[\w\u4e00-\u9fa5]+|[(){}:,\s]|./g;
      let m;
      while ((m = re.exec(code)) !== null) {
        tokens.push(m[0]);
      }
      return tokens;
    }
  }

  if (typeof window !== 'undefined') window.CNSHParser = CNSHParser;
  if (typeof module !== 'undefined' && module.exports) module.exports = CNSHParser;
})();
