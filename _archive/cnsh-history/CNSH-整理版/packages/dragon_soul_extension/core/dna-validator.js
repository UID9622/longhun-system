// 龍魂·六层来源链 / LongHun Six-Layer Source Chain
// 1 道统层 Dao           : 曾仕强老师
// 2 精神层 Spirit        : Steve Jobs
// 3 设备层 Device        : Apple
// 4 技术层 Technology    : Open Source
// 5 系统层 System        : UID9622
// 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
// DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
// 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
// 文件: dna-validator.js | 标记时间: 2026-06-03T07:46:00+0800
// core/dna-validator.js - DNA格式校验器
// DNA: #龍芯⚡️2026-03-03-DNA格式校验器-浏览器版

class DNAValidator {
  constructor() {
    this.dnaPrefix = "#龍芯⚡️";
    this.dnaRegex = /#龍芯⚡️\d{4}-\d{2}-\d{2}-[\w\u4e00-\u9fff\-]+/;
  }

  validate(dnaString) {
    if (!dnaString) return false;
    return this.dnaRegex.test(dnaString);
  }

  extractDate(dnaString) {
    const match = dnaString.match(/\d{4}-\d{2}-\d{2}/);
    return match ? match[0] : null;
  }

  extractIdentifier(dnaString) {
    const match = dnaString.match(/-\w+/);
    return match ? match[0].substring(1) : null;
  }
}

// 全局单例
window.dnaValidator = new DNAValidator();
