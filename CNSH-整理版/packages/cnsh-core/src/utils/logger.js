/**
 * 日志工具
 * 提供统一的日志记录功能
 */

const fs = require('fs-extra');
const path = require('path');

class Logger {
  constructor(level = 'info', logFile = null) {
    this.level = level;
    this.logFile = logFile;
    
    // 确保日志目录存在
    if (this.logFile) {
      fs.ensureDir(path.dirname(this.logFile));
    }
    
    // 日志级别
    this.levels = {
      error: 0,
      warn: 1,
      info: 2,
      debug: 3
    };
    
    // 当前日志级别数值
    this.currentLevel = this.levels[level] || this.levels.info;
  }

  /**
   * 格式化日志消息
   */
  formatMessage(level, message) {
    const timestamp = new Date().toISOString();
    return `[${timestamp}] [${level.toUpperCase()}] ${message}`;
  }

  /**
   * 写入日志到文件
   */
  async writeToFile(message) {
    if (!this.logFile) {
      return;
    }
    
    try {
      await fs.appendFile(this.logFile, message + '\n');
    } catch (error) {
      console.error(`Error writing to log file: ${error.message}`);
    }
  }

  /**
   * 记录错误日志
   */
  error(message) {
    const formattedMessage = this.formatMessage('error', message);
    
    if (this.currentLevel >= this.levels.error) {
      console.error(formattedMessage);
    }
    
    this.writeToFile(formattedMessage);
  }

  /**
   * 记录警告日志
   */
  warn(message) {
    const formattedMessage = this.formatMessage('warn', message);
    
    if (this.currentLevel >= this.levels.warn) {
      console.warn(formattedMessage);
    }
    
    this.writeToFile(formattedMessage);
  }

  /**
   * 记录信息日志
   */
  info(message) {
    const formattedMessage = this.formatMessage('info', message);
    
    if (this.currentLevel >= this.levels.info) {
      console.log(formattedMessage);
    }
    
    this.writeToFile(formattedMessage);
  }

  /**
   * 记录调试日志
   */
  debug(message) {
    const formattedMessage = this.formatMessage('debug', message);
    
    if (this.currentLevel >= this.levels.debug) {
      console.log(formattedMessage);
    }
    
    this.writeToFile(formattedMessage);
  }

  /**
   * 创建子日志记录器
   */
  child(suffix) {
    const childLogger = new Logger(this.level, this.logFile);
    
    // 重写日志方法，添加前缀
    const originalMethods = ['error', 'warn', 'info', 'debug'];
    
    originalMethods.forEach(method => {
      childLogger[method] = (message) => {
        const prefixedMessage = `[${suffix}] ${message}`;
        Logger.prototype[method].call(childLogger, prefixedMessage);
      };
    });
    
    return childLogger;
  }
}

module.exports = Logger;