/**
 * 🐉 龍魂DNA追溯助手 · 弹窗面板控制器
 * DNA: #龍芯⚡️20260525|LONGHUNWIDGET-POPUP|v1.0|xxxxx
 */

const UID9622 = "9622";
const CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// ========== DOM元素 ==========

const scanBtn = document.getElementById('scan-btn');
const reportBtn = document.getElementById('report-btn');
const addDnaBtn = document.getElementById('add-dna-btn');
const copyDnaBtn = document.getElementById('copy-dna-btn');
const exportBtn = document.getElementById('export-btn');
const viewEvidenceBtn = document.getElementById('view-evidence-btn');
const settingsBtn = document.getElementById('settings-btn');
const verifyDnaBtn = document.getElementById('verify-dna-btn');

const dnaSection = document.getElementById('dna-section');
const hooksSection = document.getElementById('hooks-section');
const scanResult = document.getElementById('scan-result');
const dnaList = document.getElementById('dna-list');
const hooksList = document.getElementById('hooks-list');

const dnaCount = document.getElementById('dna-count');
const hookCount = document.getElementById('hook-count');
const blacklistCount = document.getElementById('blacklist-count');

let currentTab = null;
let currentDNAs = [];
let currentHooks = [];

// ========== 初始化 ==========

document.addEventListener('DOMContentLoaded', () => {
  // 获取当前标签页
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    currentTab = tabs[0];
    updateStats();
  });

  // 绑定事件
  scanBtn.addEventListener('click', scanPage);
  reportBtn.addEventListener('click', reportInfringement);
  addDnaBtn.addEventListener('click', addDNA);
  copyDnaBtn.addEventListener('click', copyDNA);
  exportBtn.addEventListener('click', exportEvidence);
  viewEvidenceBtn.addEventListener('click', viewEvidence);
  settingsBtn.addEventListener('click', openSettings);
  verifyDnaBtn.addEventListener('click', verifyDNA);
});

// ========== 页面扫描 ==========

async function scanPage() {
  if (!currentTab) return;

  scanBtn.disabled = true;
  scanBtn.innerHTML = '🔍 <span class="loading">扫描中...</span>';

  try {
    // 向content script发送扫描请求
    const response = await new Promise((resolve, reject) => {
      chrome.tabs.sendMessage(currentTab.id, {
        action: 'scan_watermark',
        payload: {}
      }, (response) => {
        if (chrome.runtime.lastError) {
          reject(chrome.runtime.lastError);
        } else {
          resolve(response);
        }
      });
    });

    if (!response) {
      showResult('未能扫描页面·可能未加载content script', 'warning');
      return;
    }

    currentDNAs = response.result?.dnas || [];
    currentHooks = response.hooks || [];

    // 显示结果
    if (currentDNAs.length > 0) {
      dnaSection.classList.remove('hidden');
      displayDNAs(currentDNAs);
      showResult(`✅ 发现 ${currentDNAs.length} 个DNA水印!`, 'success');
    } else {
      showResult('⚠️ 未发现DNA水印·页面可能未标记', 'warning');
    }

    if (currentHooks.length > 0) {
      hooksSection.classList.remove('hidden');
      displayHooks(currentHooks);
    }

    // 更新统计
    dnaCount.textContent = currentDNAs.length;
    hookCount.textContent = currentHooks.length;

  } catch (error) {
    console.error('扫描失败:', error);
    showResult(`❌ 扫描失败: ${error.message}`, 'danger');
  } finally {
    scanBtn.disabled = false;
    scanBtn.innerHTML = '🔍 扫描页面';
  }
}

// ========== DNA显示 ==========

function displayDNAs(dnas) {
  dnaList.innerHTML = dnas.map((dna, index) => {
    return `<div class="dna-display">${dna}</div>`;
  }).join('');
}

function displayHooks(hooks) {
  if (hooks.length === 0) return;

  hooksList.innerHTML = hooks.map(hook => {
    return `
      <div class="hook-item">
        <span class="hook-name">🎣 ${hook.type}</span>
        <span class="hook-count">${hook.count}次</span>
      </div>
    `;
  }).join('');
}

// ========== 操作函数 ==========

function reportInfringement() {
  if (!currentTab) return;

  reportBtn.innerHTML = '🚨 <span class="loading">报告中...</span>';
  reportBtn.disabled = true;

  chrome.runtime.sendMessage({
    action: 'mark_infringement',
    tab: currentTab
  }, (response) => {
    showResult('✅ 侵权已报告!', 'success');
    reportBtn.innerHTML = '🚨 标记侵权';
    reportBtn.disabled = false;
  });
}

function addDNA() {
  if (!currentTab) return;

  addDnaBtn.innerHTML = '✍️ <span class="loading">添加中...</span>';
  addDnaBtn.disabled = true;

  chrome.runtime.sendMessage({
    action: 'add_dna',
    tab: currentTab
  }, (response) => {
    showResult('✅ DNA已添加!', 'success');
    addDnaBtn.innerHTML = '✍️ 添加DNA';
    addDnaBtn.disabled = false;

    // 延迟重新扫描
    setTimeout(scanPage, 1000);
  });
}

function copyDNA() {
  if (currentDNAs.length === 0) {
    showResult('❌ 没有DNA可复制', 'danger');
    return;
  }

  const dna = currentDNAs[0];
  navigator.clipboard.writeText(dna).then(() => {
    showResult(`✅ 已复制: ${dna}`, 'success');
  }).catch(err => {
    showResult('❌ 复制失败', 'danger');
  });
}

function verifyDNA() {
  if (currentDNAs.length === 0) {
    showResult('❌ 没有DNA可验证', 'danger');
    return;
  }

  const dna = currentDNAs[0];
  const pattern = /#龍芯⚡️(\d{8})\|([A-Z\-]+)\|v(\d\.\d)\|([a-f0-9]{8})/;
  const match = dna.match(pattern);

  if (!match) {
    showResult('❌ DNA格式无效', 'danger');
    return;
  }

  const [_, date, topic, version, sha8] = match;
  const formatted = `${date.slice(0, 4)}-${date.slice(4, 6)}-${date.slice(6, 8)}`;

  showResult(`
    ✅ DNA有效
    📅 日期: ${formatted}
    📌 主题: ${topic}
    📦 版本: ${version}
    🔐 SHA8: ${sha8}
  `, 'success');
}

function exportEvidence() {
  chrome.runtime.sendMessage({
    action: 'export_evidence',
    tab: currentTab
  }, (response) => {
    showResult('📥 证据包已导出!', 'success');
  });
}

function viewEvidence() {
  chrome.storage.local.get(['evidence_cache', 'dna_registry'], (items) => {
    const evidence = items.evidence_cache || {};
    const registry = items.dna_registry || [];

    const html = `
      <div style="font-size: 12px; color: #90EE90;">
        <div>📋 DNA注册表: ${registry.length}项</div>
        <div>🗂️ 证据缓存: ${Object.keys(evidence).length}项</div>
      </div>
    `;

    scanResult.innerHTML = html;
    scanResult.classList.remove('hidden');
  });
}

function openSettings() {
  chrome.runtime.openOptionsPage?.();
}

// ========== 工具函数 ==========

function showResult(message, type = 'info') {
  scanResult.className = `result-box ${type}`;
  scanResult.innerHTML = message;
  scanResult.classList.remove('hidden');

  if (type === 'success') {
    setTimeout(() => {
      scanResult.classList.add('hidden');
    }, 3000);
  }
}

function updateStats() {
  chrome.storage.local.get(['dna_registry', 'blacklist'], (items) => {
    const registry = items.dna_registry || [];
    const blacklist = items.blacklist || [];

    dnaCount.textContent = registry.length;
    blacklistCount.textContent = blacklist.length;
  });
}

console.log('🐉 龍魂DNA追溯助手·弹窗面板已加载');
