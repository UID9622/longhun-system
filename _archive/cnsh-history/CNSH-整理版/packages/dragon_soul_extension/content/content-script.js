// content/content-script.js - 监听所有输入框
// DNA: #龍芯⚡️2026-03-03-内容脚本-输入拦截

(async function() {
  console.log('🐉 龍魂守护者已激活');

  // 确保核心模块加载完成
  if (typeof window.dragonPurifier === 'undefined') {
    console.error('❌ 龍魂净化器未加载！');
    return;
  }

  // 监听所有输入事件
  document.addEventListener('input', async (e) => {
    const target = e.target;

    // 只处理文本输入
    if (!['INPUT', 'TEXTAREA'].includes(target.tagName)) return;
    if (target.type === 'password') return; // 跳过密码字段

    const originalValue = target.value;

    try {
      // 调用净化器
      const result = await window.dragonPurifier.purify(
        originalValue,
        `${location.hostname}:${target.name || target.id || 'anonymous'}`
      );

      // 根据状态处理
      if (result.status === 'BLOCKED') {
        // 被拦截：清空输入并显示警告
        target.value = '';
        target.style.border = '2px solid red';
        showNotification('🔴 危险内容已拦截', result.threats[0]);

      } else if (result.status === 'QUARANTINE') {
        // 隔离：标记但不阻止
        target.style.border = '2px solid orange';
        showNotification('🟡 可疑内容已隔离', '请人工审核');

      } else if (result.status === 'NORMALIZED') {
        // 已修正：自动替换
        target.value = result.content;
        target.style.border = '2px solid green';
        showNotification('🟢 内容已自动修正', `修正 ${result.mutations.length} 处`);

      } else {
        // 放行
        target.style.border = '';
      }

    } catch (error) {
      // 熔断触发
      target.value = '';
      target.style.border = '3px solid red';
      target.disabled = true;
      showNotification('🔥 系统熔断', error.message);

      // 5秒后恢复
      setTimeout(() => {
        target.disabled = false;
        target.style.border = '';
      }, 5000);
    }
  }, true);

  // 监听粘贴事件
  document.addEventListener('paste', async (e) => {
    const target = e.target;
    if (!['INPUT', 'TEXTAREA'].includes(target.tagName)) return;

    e.preventDefault();
    const pastedText = e.clipboardData.getData('text');

    try {
      const result = await window.dragonPurifier.purify(pastedText, 'paste');

      if (result.status !== 'BLOCKED') {
        document.execCommand('insertText', false, result.content);
      } else {
        showNotification('🔴 粘贴内容被拦截', result.threats[0]);
      }

    } catch (error) {
      showNotification('🔥 粘贴熔断', error.message);
    }
  }, true);

  // 通知函数
  function showNotification(title, message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 15px 20px;
      border-radius: 10px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      z-index: 999999;
      font-family: -apple-system, sans-serif;
      max-width: 300px;
    `;

    notification.innerHTML = `
      <div style="font-weight: bold; margin-bottom: 5px;">${title}</div>
      <div style="font-size: 0.9em; opacity: 0.9;">${message}</div>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.transition = 'opacity 0.5s';
      notification.style.opacity = '0';
      setTimeout(() => notification.remove(), 500);
    }, 3000);
  }
})();
