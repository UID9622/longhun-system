# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
Page({
  data: {
    article: null,
    content: '',
    loading: true,
    error: '',
  },

  onLoad(options) {
    const { id } = options;
    if (!id) {
      this.setData({ error: '文章 ID 缺失', loading: false });
      return;
    }
    this.loadArticle(id);
  },

  async loadArticle(id) {
    try {
      const res = await wx.request({
        url: `${getApp().globalData.apiBase}/articles/${encodeURIComponent(id)}`,
        method: 'GET',
      });

      if (res.statusCode === 200 && res.data.ok) {
        this.setData({
          article: res.data.article,
          content: res.data.content || '',
          loading: false,
        });
        wx.setNavigationBarTitle({
          title: res.data.article.title || '文章详情',
        });
      } else {
        throw new Error(res.data.detail || '加载失败');
      }
    } catch (err) {
      this.setData({
        error: err.message || '网络错误',
        loading: false,
      });
    }
  },
});
