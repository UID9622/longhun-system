/**
 * 🐉 龍魂宝宝·DNA追溯助手 · 钩子检测器
 * DNA: #龍芯⚡️20260525|HOOK-DETECTOR|v1.0|xxxxx
 *
 * 職責：
 * ① 檢測18種寫作釣鉤
 * ② 檢測11類論證手法（S2待補全）
 * ③ 計算侵權傾向評分
 *
 * 備註：此檔已在 dna-detector.js 中實現基礎版本
 * S2 階段需要補全所有 11 類論證手法
 */

class HookDetector {
  constructor() {
    // 18 種寫作釣鉤
    this.writingHooks = [
      { name: '標題黨化', pattern: /[【】！！？？]/g, weight: 1.0 },
      { name: '誇大其詞', pattern: /(驚人|震撼|絕密|獨家)/g, weight: 0.8 },
      { name: '煽情論證', pattern: /(讓人|感到|想到|意識到)/g, weight: 0.6 },
      { name: '權威引用', pattern: /(專家|權威|官方|證實)/g, weight: 0.7 },
      { name: '數據偽造', pattern: /(\d+%|\d+倍|提升\d+)/g, weight: 0.9 },
      { name: '推薦話術', pattern: /(強烈推薦|必讀|必看|牆裂推薦)/g, weight: 0.7 },
      { name: '限時優惠', pattern: /(限時|只需|僅售|倒計時)/g, weight: 0.8 },
      { name: '恐吓話術', pattern: /(必須|一定|否則|後悔)/g, weight: 0.6 },
      { name: '隱性廣告', pattern: /(@|鏈接|點擊|關注)/g, weight: 0.5 },
      { name: '虛假證據', pattern: /(聲稱|據說|據傳|有人說)/g, weight: 0.8 },
      { name: '攻擊對手', pattern: /(競爭對手|山寨|仿冒|抄襲)/g, weight: 0.7 },
      { name: '道德綁架', pattern: /(不支持就是|堅決反對|徹底否定)/g, weight: 0.6 },
      { name: '製造焦慮', pattern: /(再不就|趕快|馬上|不然會)/g, weight: 0.7 },
      { name: '隱瞞信息', pattern: /(不能說|祕密|內幕|隱瞞)/g, weight: 0.8 },
      { name: '偷換概念', pattern: /(有點像|基本上|某種程度上)/g, weight: 0.6 },
      { name: '濫用科學', pattern: /(經科學研究|科學證明|醫學驗證)/g, weight: 0.8 },
      { name: '情感訴求', pattern: /(心酸|催淚|感動|溫暖)/g, weight: 0.5 },
      { name: '明星效應', pattern: /(明星|名人|大V|影響力)/g, weight: 0.6 }
    ];

    // 11 類論證手法（待實現）
    this.argumentHooks = [
      { name: '虛假二分法', pattern: /非此即彼|要麼...要麼/g, weight: 0.7 },
      { name: '因果謬誤', pattern: /導致了|因此|所以|結果|造成/g, weight: 0.6 },
      { name: '訴諸權威', pattern: /專家說|官方表示|領導指示/g, weight: 0.7 },
      { name: '訴諸民眾', pattern: /大多數人|人人都說|普遍認為/g, weight: 0.6 },
      { name: '訴諸傳統', pattern: /一直以來|傳統上|從古至今/g, weight: 0.5 },
      { name: '人身攻擊', pattern: /你這種人|某某就是|典型的/g, weight: 0.9 },
      { name: '循環論證', pattern: /因為...所以..., 因為/g, weight: 0.7 },
      { name: '舉例失當', pattern: /比如說|例如|就像/g, weight: 0.5 },
      { name: '類比不當', pattern: /好比|如同|相當於|相似/g, weight: 0.6 },
      { name: '訴諸後果', pattern: /會導致|將造成|必然結果/g, weight: 0.7 },
      { name: '妄下結論', pattern: /顯然|當然|無疑|絕對/g, weight: 0.6 }
    ];
  }

  /**
   * 完整檢測 - 掃描所有釣鉤
   */
  detectAllHooks(text) {
    const hooks = [];

    // 檢測寫作釣鉤
    this.writingHooks.forEach(hook => {
      const matches = text.match(hook.pattern);
      if (matches && matches.length > 0) {
        hooks.push({
          type: hook.name,
          category: 'writing',
          count: matches.length,
          weight: hook.weight,
          score: matches.length * hook.weight
        });
      }
    });

    // 檢測論證手法
    this.argumentHooks.forEach(hook => {
      const matches = text.match(hook.pattern);
      if (matches && matches.length > 0) {
        hooks.push({
          type: hook.name,
          category: 'argument',
          count: matches.length,
          weight: hook.weight,
          score: matches.length * hook.weight
        });
      }
    });

    // 按權重排序
    hooks.sort((a, b) => b.score - a.score);

    return hooks;
  }

  /**
   * 計算總體侵權傾向分數
   */
  calculateInfringementScore(hooks) {
    if (hooks.length === 0) return 0;

    // 加權平均
    const totalScore = hooks.reduce((sum, hook) => sum + hook.score, 0);
    const avgWeight = hooks.reduce((sum, hook) => sum + hook.weight, 0) / hooks.length;

    // 正規化到 0-1
    return Math.min(1, totalScore / (hooks.length * 10));
  }

  /**
   * 獲取風險評級
   */
  getRiskLevel(score) {
    if (score < 0.3) return { level: '綠', desc: '正常' };
    if (score < 0.6) return { level: '黃', desc: '可疑' };
    if (score < 0.8) return { level: '橙', desc: '高風險' };
    return { level: '紅', desc: '極高風險' };
  }
}

// ========== 導出供其他模組使用 ==========

window.HookDetector = HookDetector;

console.log('🐉 釣鉤檢測器已加載');
