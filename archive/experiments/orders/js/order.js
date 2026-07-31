// 龍魂令前端交互
(function () {
  'use strict';

  // 首页查询跳转
  const queryForm = document.getElementById('query-form');
  if (queryForm) {
    queryForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const id = document.getElementById('anchor-input').value.trim();
      if (id) {
        window.location.href = '/orders/status.html?id=' + encodeURIComponent(id);
      }
    });
  }

  // status.html 读取锚定ID并展示
  const params = new URLSearchParams(window.location.search);
  const anchorId = params.get('id') || 'ORD-DEMO-9622';
  const anchorEl = document.getElementById('anchor-id');
  if (anchorEl) {
    anchorEl.textContent = anchorId;
  }

  // initiate.html 表单占位
  const initiateForm = document.getElementById('initiate-form');
  if (initiateForm) {
    initiateForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const result = document.getElementById('initiate-result');
      const key = document.getElementById('initiate-key').value.trim();
      if (!key) {
        result.textContent = '请输入授权密钥。';
        result.style.color = '#c0392b';
        return;
      }
      result.style.color = '#27ae60';
      result.textContent = '密钥已接收，系统进入锚定流程（静态演示：未实际签发）。';
    });
  }
})();
