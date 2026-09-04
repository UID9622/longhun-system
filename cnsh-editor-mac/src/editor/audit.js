/**
 * 🐉 三色审计引擎
 * 🟢 通过 / 🟡 警告 / 🔴 失败
 * DNA: #龍芯⚡️丙午·丙申·辛酉·己丑·䷹兑为泽-CNSH-AUDIT-UID9622
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 */

(function () {
  const AUDIT_RULES = [
    { id: 'DNA', pattern: /#龍芯⚡️/, weight: 20, msg: '缺少DNA追溯码' },
    { id: 'CONFIRM', pattern: /#CONFIRM🌌/, weight: 15, msg: '缺少确认码' },
    { id: 'GPG', pattern: /A2D0092CEE2E5BA87035600924C3704A8CC26D5F/, weight: 10, msg: '缺少GPG指纹' },
    { id: 'KEYWORD', pattern: /(函数|类|如果|循环|返回)/, weight: 15, msg: '未检测到CNSH关键字' },
    { id: 'STRUCTURE', pattern: /(函数\s+\w+|类\s+\w+)/, weight: 10, msg: '缺少函数或类定义' },
    { id: 'UID', pattern: /UID9622/, weight: 10, msg: '缺少UID9622主权标识' }
  ];

  class AuditEngine {
    static audit(content) {
      let score = 0;
      const issues = [];
      const passed = [];

      for (const rule of AUDIT_RULES) {
        if (rule.pattern.test(content)) {
          score += rule.weight;
          passed.push(rule.id);
        } else {
          issues.push(rule.msg);
        }
      }

      let color, status;
      if (score >= 70) {
        color = '🟢';
        status = '通过';
      } else if (score >= 40) {
        color = '🟡';
        status = '警告';
      } else {
        color = '🔴';
        status = '失败';
      }

      return {
        color,
        status,
        score: Math.min(100, score),
        issues,
        passed,
        passedCount: passed.length,
        totalRules: AUDIT_RULES.length
      };
    }

    static getStatusIcon(status) {
      return status === '通过' ? '🟢' : status === '警告' ? '🟡' : '🔴';
    }
  }

  if (typeof window !== 'undefined') {
    window.AuditEngine = AuditEngine;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = AuditEngine;
  }
})();
