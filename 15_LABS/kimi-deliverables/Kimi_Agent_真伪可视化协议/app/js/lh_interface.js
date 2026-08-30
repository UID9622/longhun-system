/* ============================================================
 * 龍魂 · 真实性标识协议 · 接口适配层 lh_interface.js
 * DNA: #龍芯⚡️丙午·乙未·丁未·丙午·䷫姤-接口适配-V1.0
 * 归属: 龍魂系统 UID9622 · 免费开源 · 零黑箱
 *
 * 【云码接入说明】
 * 本文件是所有外部引擎的唯一对接口。前端模块（打标器/流水线/嵌入页）
 * 只调用 window.LH_API，不直连任何后端。
 * 本地部署到鲲鹏后，只需修改下方 ENDPOINTS.MODE = 'LOCAL'，
 * 各 stub 分支已预留真实 fetch 调用，前端页面零改动。
 * 缺口标记：===【缺口·云码接管】===
 * ============================================================ */

window.LH_API = (function () {

  /* ---- 端点配置（云码改这里） ---- */
  var ENDPOINTS = {
    MODE: 'STUB',                 // STUB=演示桩 | LOCAL=鲲鹏本地引擎
    LOCAL_ENGINE: 'http://127.0.0.1:9527',  // 龍魂 FastAPI 操作台（鲲鹏）
    AI_JUDGE:   '/api/v1/truth/judge',      // AI 打标判定
    VIDEO_GEN:  '/api/v1/truth/video',      // 视频生成（数字人/成片）
    GRAPH_SYNC: '/api/v1/truth/graph',      // 知识图谱同步入库
    DNA_SIGN:   '/api/v1/dna/sign'          // DNA 追溯码签发（接 bin/lh_dna_generator.py）
  };

  /* ---- 协议常量（焊死，勿改） ---- */
  var TAGS = { SHI: '实', YAN: '演', YI: '疑' };
  var RULES = {
    autoDowngrade: true,   // 声称「实」但无来源 → 自动降级「疑」（P3-3）
    defaultTag: '疑'       // 无标签内容 → 默认「疑」（P0）
  };

  /* ---- 规则引擎初判（本地零算力，永远可用） ---- */
  var KW = {
    shi: ['公告', '统计局', '官方', '新华社', '央视', '白皮书', '国家标准', '财报', '裁判文书', '来源:'],
    yan: ['情景', '剧场', '演绎', '剧情', '改编', '模拟', '虚构', '短剧', '摆拍', '剧本'],
    yi:  ['网传', '听说', '据说', '内部消息', '震惊', '速看', '删前', '曝光', '百分百', '稳赚', '必涨', '包你']
  };
  function ruleJudge(text) {
    var s = { shi: 0, yan: 0, yi: 0 };
    KW.shi.forEach(function (k) { if (text.indexOf(k) >= 0) s.shi++; });
    KW.yan.forEach(function (k) { if (text.indexOf(k) >= 0) s.yan++; });
    KW.yi.forEach(function (k)  { if (text.indexOf(k) >= 0) s.yi += 2; });
    if (s.yi > 0 && s.yi >= s.shi) return { tag: '疑', score: s, by: 'rule' };
    if (s.yan > 0 && s.yan >= s.shi) return { tag: '演', score: s, by: 'rule' };
    if (s.shi > 0) return { tag: '实', score: s, by: 'rule' };
    return { tag: '疑', score: s, by: 'rule-default' };
  }

  /* ---- 解析标注脚本（P2 语法） ---- */
  function parseScript(text) {
    return text.split('\n').map(function (l, i) {
      l = l.trim(); if (!l) return null;
      var m = l.match(/^\[(实|演|疑|混)(\|来源:([^\]]+))?\]\s*(.*)$/);
      if (!m) return { line: i, tag: RULES.defaultTag, src: null, text: l, note: '无标签·默认为疑' };
      var tag = m[1], src = m[3] || null, body = m[4];
      var note = null;
      if (tag === '混') { tag = '演'; note = '真实事件改编'; }
      if (tag === '实' && !src && RULES.autoDowngrade) { tag = '疑'; note = '声称真实但无来源·自动降级'; }
      return { line: i, tag: tag, src: src, text: body, note: note };
    }).filter(Boolean);
  }

  function post(url, payload) {
    return fetch(url, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (r) { return r.json(); });
  }

  return {
    ENDPOINTS: ENDPOINTS,
    TAGS: TAGS,
    parseScript: parseScript,
    ruleJudge: ruleJudge,

    /* AI 精判 ===【缺口·云码接管】=== 接鲲鹏推理引擎复核 */
    aiJudge: function (text) {
      if (ENDPOINTS.MODE === 'LOCAL') {
        return post(ENDPOINTS.LOCAL_ENGINE + ENDPOINTS.AI_JUDGE, { text: text, dna_required: true });
      }
      return Promise.resolve(ruleJudge(text));
    },

    /* 视频生成 ===【缺口·云码接管】=== 接鲲鹏视频引擎/数字人（龍音ASR+数字人渲染） */
    videoGenerate: function (storyboard) {
      if (ENDPOINTS.MODE === 'LOCAL') {
        return post(ENDPOINTS.LOCAL_ENGINE + ENDPOINTS.VIDEO_GEN, storyboard);
      }
      return Promise.resolve({
        status: 'STUB', job_id: null,
        message: '【缺口】视频引擎未接入。本地部署后由云码接管此接口。',
        received_shots: storyboard.shots.length
      });
    },

    /* 知识图谱同步入库 ===【缺口·云码接管】=== 接龍魂知识图谱模块 */
    graphSync: function (graphData) {
      if (ENDPOINTS.MODE === 'LOCAL') {
        return post(ENDPOINTS.LOCAL_ENGINE + ENDPOINTS.GRAPH_SYNC, graphData);
      }
      return Promise.resolve({ status: 'STUB', message: '【缺口】图谱库未接入。' });
    },

    /* DNA 追溯码签发 ===【缺口·云码接管】=== 接 bin/lh_dna_generator.py，以生成器输出为准 */
    dnaSign: function (moduleName, action) {
      if (ENDPOINTS.MODE === 'LOCAL') {
        return post(ENDPOINTS.LOCAL_ENGINE + ENDPOINTS.DNA_SIGN, { module: moduleName, action: action });
      }
      return Promise.resolve({
        status: 'STUB',
        dna: '#龍芯⚡️丙午·乙未·丁未·丙午·䷫姤-' + moduleName + '-' + action + '-STUB',
        message: '【缺口】DNA 生成器未接入，当前为占位码，部署后以生成器输出为准。'
      });
    }
  };
})();
