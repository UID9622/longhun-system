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
