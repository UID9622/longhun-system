// core/fuse-engine.js - 熔断引擎
// DNA: #龍芯⚡️2026-03-03-熔断引擎-浏览器版

class FuseEngine {
  constructor() {
    this.fuseThreshold = 0.7; // 0.0-1.0，越低越严格
    this.fuseCooldown = 5 * 60 * 1000; // 5分钟熔断冷却
    this.fuseHistory = [];
    this.fuseActive = false;
  }

  shouldFuse() {
    if (this.fuseActive) return true;

    const now = Date.now();
    const recentFuses = this.fuseHistory.filter(time => now - time < this.fuseCooldown);

    // 如果最近10分钟内有超过5次熔断，触发熔断
    if (recentFuses.length >= 5) {
      this.fuseActive = true;
      return true;
    }

    return false;
  }

  recordFuse() {
    this.fuseHistory.push(Date.now());

    // 保留最近10次熔断记录
    if (this.fuseHistory.length > 10) {
      this.fuseHistory = this.fuseHistory.slice(-10);
    }

    // 如果熔断触发，记录并触发熔断
    if (this.shouldFuse()) {
      this.activateFuse();
      return true;
    }

    return false;
  }

  activateFuse() {
    this.fuseActive = true;
    console.log('[🔥 熔断] 系统熔断已激活，5分钟内禁止操作');

    // 5分钟后自动解除熔断
    setTimeout(() => {
      this.deactivateFuse();
    }, this.fuseCooldown);
  }

  deactivateFuse() {
    this.fuseActive = false;
    console.log('[✅ 熔断] 系统熔断已解除');
  }

  getFuseStatus() {
    return {
      active: this.fuseActive,
      cooldownRemaining: this.fuseActive ? (this.fuseCooldown - (Date.now() - this.fuseHistory[this.fuseHistory.length - 1])) / 1000 : 0
    };
  }
}

// 全局单例
window.fuseEngine = new FuseEngine();
