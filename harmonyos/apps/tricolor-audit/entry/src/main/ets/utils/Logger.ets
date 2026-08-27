// 🐉 统一日志工具
// DNA: #龍芯⚡️2026-08-06-LOGGER-V2.0-UID9622
// License: MulanPSL v2

import hilog from '@ohos.hilog';
import { DNAGenerator } from '../core/DNAGenerator';

const DOMAIN: number = 0xFF10;

export enum LogLevel { DEBUG = 0, INFO = 1, WARN = 2, ERROR = 3, FATAL = 4 }

export class Logger {
  private static currentLevel: LogLevel = LogLevel.INFO;

  static setLevel(level: LogLevel): void {
    this.currentLevel = level;
  }

  static debug(tag: string, message: string): void {
    if (this.currentLevel <= LogLevel.DEBUG) {
      hilog.debug(DOMAIN, tag, `🔍 ${message}`);
    }
  }

  static info(tag: string, message: string): void {
    if (this.currentLevel <= LogLevel.INFO) {
      hilog.info(DOMAIN, tag, `ℹ️ ${message}`);
    }
  }

  static warn(tag: string, message: string): void {
    if (this.currentLevel <= LogLevel.WARN) {
      hilog.warn(DOMAIN, tag, `⚠️ ${message}`);
    }
  }

  static error(tag: string, message: string): void {
    if (this.currentLevel <= LogLevel.ERROR) {
      hilog.error(DOMAIN, tag, `❌ ${message}`);
    }
  }

  static fatal(tag: string, message: string): void {
    if (this.currentLevel <= LogLevel.FATAL) {
      hilog.fatal(DOMAIN, tag, `💀 ${message}`);
    }
  }

  static withDNA(tag: string, message: string): void {
    this.info(tag, `${message} | DNA: ${DNAGenerator.generate('LOG')}`);
  }
}
