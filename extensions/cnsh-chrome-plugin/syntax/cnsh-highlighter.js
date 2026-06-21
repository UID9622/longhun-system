##龍芯⚡️2026-06-21-CNSH-CNSH-HIGHLIGHTER-v1.0
# 君子協議: 本文件受龍魂DNA追溯保護

/**
 * CNSH 语法高亮引擎
 * Chinese Natural Syntax Hybrid · 中文自然语法
 *
 * DNA追溯: #龍芯⚡️20260417-SKILL-CNSHHILITE
 *
 * 三才架构:
 *   天层 (输入) -- 关键字捕获
 *   地层 (处理) -- token 归类染色
 *   人层 (决策) -- DOM 标记注入
 */

(function () {
  'use strict';
  if (window.__CNSH_HILITE_INITED__) return;
  window.__CNSH_HILITE_INITED__ = true;

  // ─────────────────────────────────────────
  // 关键字表：CNSH 的核心中文语法
  // ─────────────────────────────────────────
  const KEYWORDS = {
    // 控制流（天）
    control: [
      '若', '则', '否则', '否則', '当', '否则若',
      '循环', '遍', '每次', '迭代', '重复',
      '跳出', '继续', '返回', '抛出',
      '尝试', '捕获', '最终', '匹配', '分支', '默认'
    ],
    // 定义（地）
    define: [
      '定义', '声明', '设', '令', '赋值',
      '函数', '方法', '过程', '模块', '类',
      '接口', '协议', '抽象', '实现', '继承',
      '常量', '变量', '参数', '返回值', '类型'
    ],
    // 动作（人）
    action: [
      '调用', '执行', '运行', '启动', '停止',
      '读取', '写入', '保存', '加载', '删除',
      '发送', '接收', '推送', '拉取', '查询',
      '打印', '输出', '提示', '警告', '报错'
    ],
    // 龍魂专属
    dragonsoul: [
      '净化', '拆解', '布军', '组军', '武装',
      '三才', 'DNA', '追溯', '三色审计', '数字大军',
      '天层', '地层', '人层', '龍魂', '龍芯',
      'Inbox', '入库', '沙盒', '流场', '洛书'
    ],
    // 布尔/常量
    literal: [
      '真', '假', '是', '否', '有', '无', '空', '未定义',
      '通过', '待审', '危险'
    ],
    // 运算与连接词
    operator: [
      '加', '减', '乘', '除', '取余', '幂',
      '等于', '不等于', '大于', '小于', '大于等于', '小于等于',
      '并且', '或者', '不是', '属于', '不属于',
      '的', '之', '之中', '之上', '之下', '由', '向', '至'
    ]
  };

  // 三色审计：🟢🟡🔴
  const AUDIT_COLORS = {
    '🟢': 'cnsh-audit-green',
    '🟡': 'cnsh-audit-yellow',
    '🔴': 'cnsh-audit-red'
  };

  // 构建正则
  const buildRegex = (words) =>
    new RegExp(`(${words.map(w => w.replace(/([.*+?^${}()|[\]\\])/g, '\\$1')).join('|')})`, 'g');

  const REGEX_MAP = {
    'cnsh-kw-control': buildRegex(KEYWORDS.control),
    'cnsh-kw-define': buildRegex(KEYWORDS.define),
    'cnsh-kw-action': buildRegex(KEYWORDS.action),
    'cnsh-kw-dragonsoul': buildRegex(KEYWORDS.dragonsoul),
    'cnsh-kw-literal': buildRegex(KEYWORDS.literal),
    'cnsh-kw-operator': buildRegex(KEYWORDS.operator)
  };

  // DNA 追溯码正则
  const DNA_REGEX = /#龍芯⚡️\d{8}-[A-Z]+-[A-F0-9]{6,8}/g;
  // 字符串字面量
  const STRING_REGEX = /([「『])([^」』]*)([」』])/g;
  // 注释
  const COMMENT_REGEX = /(\/\/[^\n]*|#[^\n]*)/g;

  /**
   * 给一段纯文本上色，返回 HTML
   */
  function highlightText(text) {
    if (!text || typeof text !== 'string') return text;

    let html = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // 先打 DNA 追溯码（最高优先级）
    html = html.replace(DNA_REGEX, m => `<span class="cnsh-dna">${m}</span>`);

    // 三色审计标记
    Object.entries(AUDIT_COLORS).forEach(([emoji, cls]) => {
      html = html.replace(new RegExp(emoji, 'g'), `<span class="${cls}">${emoji}</span>`);
    });

    // 字符串（中文引号）
    html = html.replace(STRING_REGEX,
      (_, l, mid, r) => `<span class="cnsh-string">${l}${mid}${r}</span>`);

    // 注释
    html = html.replace(COMMENT_REGEX, m => `<span class="cnsh-comment">${m}</span>`);

    // 关键字高亮（按类别）
    for (const [cls, regex] of Object.entries(REGEX_MAP)) {
      html = html.replace(regex, (m) => `<span class="${cls}">${m}</span>`);
    }

    return html;
  }

  /**
   * 检测是否 "看起来像 CNSH"
   */
  function looksLikeCNSH(text) {
    if (!text || text.length < 10) return false;
    let hits = 0;
    for (const list of Object.values(KEYWORDS)) {
      for (const kw of list) {
        if (text.includes(kw)) {
          hits++;
          if (hits >= 3) return true;
        }
      }
    }
    return false;
  }

  /**
   * 扫描页面 <pre><code> 块，若像 CNSH 就上色
   */
  function scanAndHighlight() {
    const blocks = document.querySelectorAll('pre > code, pre.cnsh, code.cnsh');
    blocks.forEach(el => {
      if (el.dataset.cnshDone === '1') return;
      const txt = el.textContent;
      const forced = el.classList.contains('cnsh') ||
        (el.parentElement && el.parentElement.classList.contains('cnsh'));
      if (forced || looksLikeCNSH(txt)) {
        el.innerHTML = highlightText(txt);
        el.classList.add('cnsh-highlighted');
        el.dataset.cnshDone = '1';
      }
    });
  }

  // 暴露给外部调用
  window.CNSH = {
    highlightText,
    looksLikeCNSH,
    scanAndHighlight,
    KEYWORDS
  };

  // 初次扫描
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', scanAndHighlight);
  } else {
    scanAndHighlight();
  }

  // 动态页面：5s 节流再扫一次
  let scanTimer = null;
  const observer = new MutationObserver(() => {
    clearTimeout(scanTimer);
    scanTimer = setTimeout(scanAndHighlight, 1500);
  });
  observer.observe(document.body || document.documentElement, {
    childList: true,
    subtree: true
  });
})();
