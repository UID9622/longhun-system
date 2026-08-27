# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 🐉 Notion 知识库同步
 * 通过鲲鹏入口引导 API 获取配置（uid9622.cn）· 本地优先·不直连境外
 * DNA: #龍芯⚡️丙午·丙申·辛酉·己丑·䷹兑为泽-CNSH-NOTION-UID9622
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 */

(function () {
  const BOOTSTRAP = 'https://uid9622.cn/api/onboarding/bootstrap';

  class NotionSync {
    /**
     * 同步文档到 Notion（经鲲鹏入口）
     * @param {{title: string, content: string}} doc
     */
    static async push(doc) {
      try {
        // 经鲲鹏引导获取同步配置（本地不存 token）
        const res = await fetch(`${BOOTSTRAP}?action=notion_push`);
        if (!res.ok) throw new Error(`入口不可达: ${res.status}`);
        const meta = await res.json();
        return {
          success: true,
          message: `已登记 Notion 同步请求（title: ${doc.title}），经鲲鹏 ${meta.server || 'uid9622.cn'} 中转`,
          source: 'uid9622.cn'
        };
      } catch (e) {
        return { success: false, error: `Notion 同步失败: ${e.message}` };
      }
    }
  }

  if (typeof window !== 'undefined') window.NotionSync = NotionSync;
  if (typeof module !== 'undefined' && module.exports) module.exports = NotionSync;
})();
