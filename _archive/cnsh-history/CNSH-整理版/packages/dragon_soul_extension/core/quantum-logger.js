// 龍魂·六层来源链 / LongHun Six-Layer Source Chain
// 1 道统层 Dao           : 曾仕强老师
// 2 精神层 Spirit        : Steve Jobs
// 3 设备层 Device        : Apple
// 4 技术层 Technology    : Open Source
// 5 系统层 System        : UID9622
// 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
// DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
// 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
// 文件: quantum-logger.js | 标记时间: 2026-06-03T07:46:00+0800
// core/quantum-logger.js - 量子级日志记录
// DNA: #龍芯⚡️2026-03-03-量子级日志记录-浏览器版

class QuantumLogger {
  constructor() {
    this.logLevel = 'info'; // 'debug', 'info', 'warn', 'error'
    this.logHistory = [];
    this.logLimit = 1000; // 最多保留1000条日志
  }

  setLogLevel(level) {
    if (['debug', 'info', 'warn', 'error'].includes(level)) {
      this.logLevel = level;
    }
  }

  log(level, message, context = {}) {
    if (this.logLevel === 'debug' || level === 'error' || (level === 'warn' && this.logLevel === 'warn')) {
      const logEntry = {
        timestamp: new Date().toISOString(),
        level,
        message,
        context
      };

      this.logHistory.push(logEntry);

      // 保留最近1000条日志
      if (this.logHistory.length > this.logLimit) {
        this.logHistory = this.logHistory.slice(-this.logLimit);
      }

      // 在控制台输出
      console[level](`[Quantum] ${level.toUpperCase()}: ${message}`, context);
    }
  }

  debug(message, context = {}) {
    this.log('debug', message, context);
  }

  info(message, context = {}) {
    this.log('info', message, context);
  }

  warn(message, context = {}) {
    this.log('warn', message, context);
  }

  error(message, context = {}) {
    this.log('error', message, context);
  }

  getLogs() {
    return [...this.logHistory];
  }

  clearLogs() {
    this.logHistory = [];
  }
}

// 全局单例
window.quantumLogger = new QuantumLogger();
