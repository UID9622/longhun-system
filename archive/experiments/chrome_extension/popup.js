document.getElementById('ping').addEventListener('click', async () => {
  try {
    const r = await fetch('http://127.0.0.1:8788/api/status');
    const s = await r.json();
    document.getElementById('status').textContent = s.熔断器 === '完整'
      ? '✅ 面板在线，主权完整'
      : '❌ 面板异常';
  } catch (e) {
    document.getElementById('status').textContent = '❌ 无法连接面板：' + e.message;
  }
});
