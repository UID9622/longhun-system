# DNA: #龍芯⚡️丙午·丙申·甲戌·卯时·䷐随-QUAD-SYNC-v1.0-ATTRIBUTION-8c26d5f
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
Page({
  data: {
    articles: [],
    loading: true,
    error: '',
  },

  onLoad() {
    this.loadArticles();
  },

  async loadArticles() {
    try {
      const res = await wx.request({
        url: `${getApp().globalData.apiBase}/articles`,
        method: 'GET',
      });

      if (res.statusCode === 200 && res.data.ok) {
        this.setData({
          articles: res.data.articles || [],
          loading: false,
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

  onArticleTap(e) {
    const { id } = e.currentTarget.dataset;
    wx.navigateTo({
      url: `/pages/article/article?id=${id}`,
    });
  },

  onPullDownRefresh() {
    this.loadArticles().finally(() => {
      wx.stopPullDownRefresh();
    });
  },
});
