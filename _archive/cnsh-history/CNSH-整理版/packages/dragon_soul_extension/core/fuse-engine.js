// 龍魂·六层来源链 / LongHun Six-Layer Source Chain
// 1 道统层 Dao           : 曾仕强老师
// 2 精神层 Spirit        : Steve Jobs
// 3 设备层 Device        : Apple
// 4 技术层 Technology    : Open Source
// 5 系统层 System        : UID9622
// 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
// DNA追溯码: #龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-v2.0
// 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
// 文件: fuse-engine.js | 标记时间: 2026-06-03T07:46:00+0800
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
