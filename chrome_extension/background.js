const PANEL_URL = 'http://127.0.0.1:8788/api/download-event';

chrome.downloads.onChanged.addListener((delta) => {
  if (delta.state && delta.state.current === 'complete') {
    chrome.downloads.search({ id: delta.id }, (items) => {
      if (!items || !items.length) return;
      const item = items[0];
      const payload = {
        filename: item.filename,
        local_path: item.filename,
        url: item.url,
        referrer: item.referrer || '',
        mime: item.mime
      };
      fetch(PANEL_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      .then(r => r.json())
      .then(data => {
        if (!data.通过) {
          console.warn('[龍魂] 下载被隔离：', data);
          chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icon48.png',
            title: '龍魂护盾：危险下载已隔离',
            message: `${item.filename.split('/').pop()} 已被移入隔离区`
          });
        } else {
          console.log('[龍魂] 下载干净：', data);
        }
      })
      .catch(err => console.error('[龍魂] 通知面板失败：', err));
    });
  }
});
