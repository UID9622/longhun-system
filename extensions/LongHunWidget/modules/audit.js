##龍芯⚡️2026-06-21-ENGINE-AUDIT-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

/**
 * 龍魂审核系统 v1.0
 * 三色审计：绿 / 黄 / 红
 */

const AUDIT_RULES = {
  green: ['read_page', 'take_screenshot', 'list_pages', 'copy_text'],
  yellow: ['click', 'type', 'navigate', 'fill_form'],
  red: ['evaluate_script', 'delete_cookies', 'clear_storage', 'modify_page', 'auto_submit']
};

const IRON_LAW = {
  no_decision: '不替人做决定',
  no_shortcut: '不帮人走捷径',
  no_override: '不越自己的权限',
  no_password: '不读取密码输入框',
  no_bank: '不读取银行账号字段',
  no_private: '不读取标记为私密的页面'
};

class AuditEngine {
  constructor() {
    this.log = [];
    this.enabled = true;
  }

  audit(action, context = {}) {
    let level = 'green';
    let reason = '常规只读操作';
    let blocked = false;

    if (AUDIT_RULES.red.includes(action)) {
      level = 'red';
      reason = '🔴 高危操作：可能修改数据或执行代码';
      blocked = true;
    } else if (AUDIT_RULES.yellow.includes(action)) {
      level = 'yellow';
      reason = '🟡 需谨慎：涉及页面交互';
      blocked = false;
    }

    // 铁律检查
    if (context.isPasswordField || context.isBankPage) {
      level = 'red';
      reason = '🔴 铁律熔断：密码/银行页面禁止操作';
      blocked = true;
    }

    const record = {
      id: Date.now().toString(36),
      action,
      level,
      reason,
      blocked,
      url: context.url || '',
      timestamp: Date.now(),
      dna: generateDNA('AUDIT', 'v1.0')
    };

    this.log.unshift(record);
    if (this.log.length > 200) this.log.pop();
    this.save();
    return record;
  }

  async save() {
    if (typeof chrome !== 'undefined' && chrome.storage) {
      await chrome.storage.local.set({ auditLog: this.log });
    }
  }

  async load() {
    if (typeof chrome !== 'undefined' && chrome.storage) {
      const data = await chrome.storage.local.get('auditLog');
      this.log = data.auditLog || [];
    }
  }

  getStats() {
    const total = this.log.length;
    const green = this.log.filter(r => r.level === 'green').length;
    const yellow = this.log.filter(r => r.level === 'yellow').length;
    const red = this.log.filter(r => r.level === 'red').length;
    const blocked = this.log.filter(r => r.blocked).length;
    return { total, green, yellow, red, blocked };
  }

  getRecent(limit = 20) {
    return this.log.slice(0, limit);
  }
}

// 页面内容扫描（简化版）
function scanPage() {
  const data = {
    url: location.href,
    title: document.title,
    hasPassword: !!document.querySelector('input[type="password"]'),
    hasForm: !!document.querySelector('form'),
    images: document.images.length,
    links: document.links.length,
    textLength: document.body.innerText.length,
    dna: generateDNA('PAGE-SCAN', 'v1.0')
  };
  return data;
}

if (typeof window !== 'undefined') {
  window.AuditEngine = AuditEngine;
  window.AUDIT_RULES = AUDIT_RULES;
  window.IRON_LAW = IRON_LAW;
  window.scanPage = scanPage;
}
