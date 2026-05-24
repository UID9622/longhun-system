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
