// core/purifier.js - 从 C++ purifier.cpp 移植
// DNA: #龍芯⚡️2026-03-03-JS净化器-浏览器版

class DragonPurifier {
  constructor() {
    this.uid = "9622";
    this.gpgFingerprint = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F";
    this.dnaPrefix = "#龍芯⚡️";

    // 尺寸限制
    this.MAX_INPUT_BYTES = 10 * 1024 * 1024; // 10 MB

    // DNA前缀迁移表
    this.dnaMigrations = [
      ["#ZHUGEXIN⚡️", "#龍芯⚡️"],
      ["#LUCKY⚡️", "#龍芯⚡️"],
      ["#UID9622⚡️", "#龍芯⚡️"]
    ];

    // 威胁特征库（直接熔断）
    this.threatPatterns = [
      "<script", "javascript:", "vbscript:",
      "eval(", "exec(", "system(", "popen(",
      "../", "..%2F", "%2e%2e",
      "' OR 1=1", "'; DROP TABLE", "UNION SELECT",
      "; rm -rf", "| curl ", "| wget "
    ];

    // 可疑特征库（隔离待审）
    this.suspiciousPatterns = [
      "base64", "0x", "\\x",
      "data:text", "file://", "ldap://"
    ];
  }

  // 统一净化入口
  async purify(rawInput, source = "unknown") {
    const result = {
      status: "PASS",
      content: "",
      originalHash: "",
      purifiedHash: "",
      dnaTrace: "",
      mutations: [],
      threats: [],
      auditColor: "🟢"
    };

    // 生成原始哈希
    result.originalHash = await this.sha256(rawInput);
    result.dnaTrace = `${this.dnaPrefix}PURIFY-${this.uid}-${this.nowISO()}`;

    // 关卡 1: 尺寸炸弹防护
    if (rawInput.length > this.MAX_INPUT_BYTES) {
      result.status = "BLOCKED";
      result.threats.push(`超大输入: ${rawInput.length} bytes`);
      result.auditColor = "🔴";
      await this.writeAudit(result, source);
      throw new Error("[🔴熔断] 输入超限，拒绝处理");
    }

    // 关卡 2: UTF-8编码强制
    if (!this.isValidUTF8(rawInput)) {
      result.status = "BLOCKED";
      result.threats.push("非UTF-8编码");
      result.auditColor = "🔴";
      await this.writeAudit(result, source);
      throw new Error("[🔴熔断] 非法编码，拒绝处理");
    }

    // 关卡 3: 威胁特征扫描
    const lowerInput = rawInput.toLowerCase();
    for (const pattern of this.threatPatterns) {
      if (lowerInput.includes(pattern.toLowerCase())) {
        result.status = "BLOCKED";
        result.threats.push(`威胁特征命中: ${pattern}`);
        result.auditColor = "🔴";
        await this.writeAudit(result, source);
        throw new Error(`[🔴熔断] 威胁内容检测: ${pattern}`);
      }
    }

    // 关卡 4: 可疑特征扫描
    const suspiciousHits = [];
    for (const pattern of this.suspiciousPatterns) {
      if (lowerInput.includes(pattern.toLowerCase())) {
        suspiciousHits.push(pattern);
      }
    }

    if (suspiciousHits.length > 0) {
      result.status = "QUARANTINE";
      result.threats = suspiciousHits;
      result.auditColor = "🟡";
      await this.writeQuarantine(rawInput, source, suspiciousHits);
      await this.writeAudit(result, source);
      return result;
    }

    // 关卡 5: 内容修正
    let content = rawInput;
    content = this.migrateDNAPrefix(content, result.mutations);
    content = this.tagForeignUID(content, result.mutations);

    // 关卡 6: DNA格式校验
    if (!this.validateDNAFormat(content)) {
      result.mutations.push("DNA格式不合规，已标记为🟡BRANCH");
      content += "\n[🟡BRANCH: DNA格式不符合CNSH v3.0规范]";
    }

    result.content = content;
    result.purifiedHash = await this.sha256(content);
    result.status = result.mutations.length === 0 ? "PASS" : "NORMALIZED";
    result.auditColor = "🟢";

    await this.writeAudit(result, source);

    if (result.mutations.length > 0) {
      console.log(`[🟢净化器] 修正 ${result.mutations.length} 处 | 来源: ${source}`);
      result.mutations.forEach(m => console.log(`  · ${m}`));
    }

    return result;
  }

  // DNA前缀迁移
  migrateDNAPrefix(input, mutations) {
    let result = input;
    for (const [oldPrefix, newPrefix] of this.dnaMigrations) {
      const regex = new RegExp(oldPrefix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
      const matches = result.match(regex);
      if (matches) {
        result = result.replace(regex, newPrefix);
        mutations.push(`DNA前缀迁移: ${oldPrefix} → ${newPrefix}`);
      }
    }
    return result;
  }

  // 外来UID标记
  tagForeignUID(input, mutations) {
    const uidRegex = /UID(\d{4,})/g;
    let result = input;
    let match;

    while ((match = uidRegex.exec(input)) !== null) {
      const foundUID = match[1];
      if (foundUID !== this.uid) {
        const tagged = `UID${foundUID}[🟡BRANCH]`;
        result = result.replace(match[0], tagged);
        mutations.push(`外来UID标记: UID${foundUID}`);
      }
    }

    return result;
  }

  // DNA格式校验
  validateDNAFormat(content) {
    if (!content.includes(this.dnaPrefix)) return true;
    const dnaRegex = /#龍芯⚡️\d{4}-\d{2}-\d{2}-[\w\u4e00-\u9fff\-]+/;
    return dnaRegex.test(content);
  }

  // UTF-8校验
  isValidUTF8(str) {
    try {
      const encoder = new TextEncoder();
      const decoder = new TextDecoder('utf-8', { fatal: true });
      decoder.decode(encoder.encode(str));
      return true;
    } catch {
      return false;
    }
  }

  // SHA256哈希
  async sha256(message) {
    const msgBuffer = new TextEncoder().encode(message);
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  // 当前ISO时间
  nowISO() {
    return new Date().toISOString().substring(0, 10);
  }

  // 写入审计日志
  async writeAudit(result, source) {
    const entry = {
      timestamp: new Date().toISOString(),
      action: `PURIFY_${result.auditColor}`,
      source: source,
      status: result.status,
      originalHash: result.originalHash,
      purifiedHash: result.purifiedHash,
      mutations: result.mutations,
      threats: result.threats,
      dnaTrace: result.dnaTrace,
      uid: this.uid
    };

    // 存储到chrome.storage.local
    const logs = await chrome.storage.local.get(['auditLogs']) || { auditLogs: [] };
    logs.auditLogs = logs.auditLogs || [];
    logs.auditLogs.push(entry);

    // 保留最近1000条
    if (logs.auditLogs.length > 1000) {
      logs.auditLogs = logs.auditLogs.slice(-1000);
    }

    await chrome.storage.local.set({ auditLogs: logs.auditLogs });
  }

  // 写入隔离区
  async writeQuarantine(raw, source, reasons) {
    const quarantineEntry = {
      timestamp: new Date().toISOString(),
      source: source,
      reasons: reasons,
      rawHash: (await this.sha256(raw)).substring(0, 32),
      uid: this.uid
    };

    const quarantine = await chrome.storage.local.get(['quarantine']) || { quarantine: [] };
    quarantine.quarantine = quarantine.quarantine || [];
    quarantine.quarantine.push(quarantineEntry);

    await chrome.storage.local.set({ quarantine: quarantine.quarantine });
    console.warn(`[🟡隔离] 内容已送隔离区`);
  }
}

// 全局单例
window.dragonPurifier = new DragonPurifier();
