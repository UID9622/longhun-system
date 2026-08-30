// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-28e28bf4
##龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-CNSH-NOTION-API-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

/**
 * Notion API 封装
 * 面向 UID9622 龍魂数字大军的 4 大数据库
 *
 * v0.2.0 · 根据真实 schema 重写字段映射
 *   - Inbox title: 资源名
 *   - DNA   title: 核心概念
 *   - 人心  title: 洞察标题
 *
 * 注意: 该文件是 ES Module, 由 background.js (service worker) import
 */

const NOTION_VERSION = '2022-06-28';
const NOTION_API = 'https://api.notion.com/v1';

/**
 * 生成 DNA 追溯码
 * 格式: #龍芯⚡️{YYYYMMDD}-{TYPE}-{HASH6}
 */
export async function generateDNA(type, content) {
  const d = new Date();
  const ymd = `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`;

  const buf = new TextEncoder().encode(content || String(Date.now()));
  const hashBuf = await crypto.subtle.digest('SHA-256', buf);
  const hex = Array.from(new Uint8Array(hashBuf))
    .map(b => b.toString(16).padStart(2, '0'))
    .join('').toUpperCase().slice(0, 6);

  return `#龍芯⚡️${ymd}-${type}-${hex}`;
}

/**
 * 读取配置
 */
export async function getConfig() {
  const cfg = await chrome.storage.local.get([
    'notion_token',
    'db_inbox', 'db_dna', 'db_tasks', 'db_heart'
  ]);
  return cfg;
}

/**
 * 保存配置
 */
export async function setConfig(cfg) {
  await chrome.storage.local.set(cfg);
}

/**
 * 归一化数据库 ID（去掉 collection:// 前缀和横线）
 */
export function normalizeId(id) {
  if (!id) return '';
  let s = String(id).trim();
  s = s.replace(/^collection:\/\//, '');
  s = s.replace(/-/g, '');
  return s;
}

/**
 * 通用 Notion API 调用
 */
async function notionFetch(path, { method = 'GET', body = null, token } = {}) {
  const resp = await fetch(`${NOTION_API}${path}`, {
    method,
    headers: {
      'Authorization': `Bearer ${token}`,
      'Notion-Version': NOTION_VERSION,
      'Content-Type': 'application/json'
    },
    body: body ? JSON.stringify(body) : undefined
  });
  const text = await resp.text();
  let data = null;
  try { data = JSON.parse(text); } catch (_) { data = { raw: text }; }
  if (!resp.ok) {
    const err = new Error(`Notion API ${resp.status}: ${data?.message || text}`);
    err.status = resp.status;
    err.body = data;
    throw err;
  }
  return data;
}

/**
 * 向指定数据库创建一个 page
 */
export async function createPage({ token, dbId, properties, children = [] }) {
  return notionFetch('/pages', {
    method: 'POST',
    token,
    body: {
      parent: { database_id: normalizeId(dbId) },
      properties,
      children
    }
  });
}

/**
 * 查询数据库的 schema
 */
export async function getDatabase({ token, dbId }) {
  return notionFetch(`/databases/${normalizeId(dbId)}`, { token });
}

// ──────────────────────────────────────────────────────
// 辅助: 构造各类 property 值
// ──────────────────────────────────────────────────────
const titleProp = (text) => ({ title: [{ text: { content: String(text).slice(0, 180) } }] });
const textProp  = (text) => ({ rich_text: [{ text: { content: String(text).slice(0, 1900) } }] });
const urlProp   = (u)    => ({ url: u && /^https?:\/\//.test(u) ? u : null });
const selectProp = (name) => name ? ({ select: { name } }) : undefined;
const statusProp = (name) => name ? ({ status: { name } }) : undefined;

/**
 * 纯度数字映射到 Notion select 选项
 * >=80 → 高-核心知识; >=50 → 中-需验证; else → 低-待确认
 */
function purityToSelect(purity) {
  const p = Number(purity) || 0;
  if (p >= 80) return '高-核心知识';
  if (p >= 50) return '中-需验证';
  return '低-待确认';
}

/**
 * ═════════════════════════════════════════════════════
 * 送入 Learning Inbox｜学习入口池
 * title 字段: 资源名
 * 其他字段: 链接 / 原始内容 / 污染指数 / 类型 / 来源标记 / 状态
 * ═════════════════════════════════════════════════════
 */
export async function sendToInbox({ title, url, sourceText, pollution, type, source }) {
  const cfg = await getConfig();
  if (!cfg.notion_token) throw new Error('未配置 Notion Token');
  if (!cfg.db_inbox) throw new Error('未配置 Inbox 数据库 ID');

  const dna = await generateDNA('INBOX', (title || '') + (sourceText || ''));
  const finalTitle = title || '未命名资源';

  const properties = {
    '资源名': titleProp(finalTitle),
    '链接': urlProp(url),
    '原始内容': textProp(sourceText || ''),
    '状态': statusProp('未开始')
  };
  // 可选字段
  const pollSel = selectProp(pollution);
  if (pollSel) properties['污染指数'] = pollSel;
  const typeSel = selectProp(type);
  if (typeSel) properties['类型'] = typeSel;
  const srcSel = selectProp(source);
  if (srcSel) properties['来源标记'] = srcSel;

  // 清掉 undefined
  Object.keys(properties).forEach(k => properties[k] === undefined && delete properties[k]);

  const children = [
    {
      object: 'block', type: 'callout',
      callout: {
        icon: { emoji: '⚡' },
        color: 'purple_background',
        rich_text: [{ text: { content: `龍魂DNA追溯码: ${dna}` } }]
      }
    }
  ];

  return createPage({
    token: cfg.notion_token,
    dbId: cfg.db_inbox,
    properties,
    children
  });
}

/**
 * ═════════════════════════════════════════════════════
 * 送入 Knowledge DNA｜知识基因库
 * title 字段: 核心概念
 * 其他字段: 技术点 / 方向 / 纯度 / 难度等级 / 可复制性 / 示例/伪代码 / 状态
 * ═════════════════════════════════════════════════════
 */
export async function sendToDNA({
  concept, techPoint, direction, purity = 70,
  difficulty, reusability, example
}) {
  const cfg = await getConfig();
  if (!cfg.notion_token) throw new Error('未配置 Notion Token');
  if (!cfg.db_dna) throw new Error('未配置 DNA 数据库 ID');

  const dna = await generateDNA('DNA', concept + (techPoint || ''));
  const finalTitle = concept || '未命名DNA';

  const properties = {
    '核心概念': titleProp(finalTitle),
    '技术点': textProp(techPoint || ''),
    '纯度': selectProp(purityToSelect(purity)),
    '状态': statusProp('未开始')
  };
  // 方向: 只接受预定义的 select 值
  const VALID_DIRECTIONS = ['AI', 'Web', '元宇宙', '系统', '哲学', 'CNSH', '未知'];
  if (direction && VALID_DIRECTIONS.includes(direction)) {
    properties['方向'] = selectProp(direction);
  } else if (direction) {
    properties['方向'] = selectProp('未知');  // fallback
  }
  const diffSel = selectProp(difficulty);
  if (diffSel) properties['难度等级'] = diffSel;
  const reuseSel = selectProp(reusability);
  if (reuseSel) properties['可复制性'] = reuseSel;
  if (example) properties['示例/伪代码'] = textProp(example);

  Object.keys(properties).forEach(k => properties[k] === undefined && delete properties[k]);

  const children = [
    {
      object: 'block', type: 'callout',
      callout: {
        icon: { emoji: '🧬' },
        color: 'yellow_background',
        rich_text: [{ text: { content: `DNA-ID: ${dna}` } }]
      }
    }
  ];

  return createPage({
    token: cfg.notion_token,
    dbId: cfg.db_dna,
    properties,
    children
  });
}

/**
 * ═════════════════════════════════════════════════════
 * 送入 人心算法知识库
 * title 字段: 洞察标题
 * 其他字段: DNA追溯码 / 核心金句 / 人心算法 / 情感标记 / 人生场景 / 来源对话 / 原始对话 / 状态
 * ═════════════════════════════════════════════════════
 */
export async function sendToHeart({
  title, insight, scene, quote, algorithm, emotion, sourceChat, originalUrl
}) {
  const cfg = await getConfig();
  if (!cfg.notion_token) throw new Error('未配置 Notion Token');
  if (!cfg.db_heart) throw new Error('未配置 人心算法 数据库 ID');

  const dnaCode = await generateDNA('HEART', title + (insight || ''));
  const finalTitle = title || '未命名洞察';

  const properties = {
    '洞察标题': titleProp(finalTitle),
    'DNA追溯码': textProp(dnaCode),
    '核心金句': textProp(quote || insight || ''),
    '人生场景': textProp(scene || ''),
    '状态': statusProp('草稿')
  };
  // 可选 select
  const VALID_ALGO = ['不进场', '认知隔离', '运道积累', '自攒', '无意识合道', '日子>代码'];
  if (algorithm && VALID_ALGO.includes(algorithm)) {
    properties['人心算法'] = selectProp(algorithm);
  }
  const VALID_EMO = ['❤️ 温暖', '⚡ 突破', '🛡️ 守护', '🌟 觉醒'];
  if (emotion && VALID_EMO.includes(emotion)) {
    properties['情感标记'] = selectProp(emotion);
  }
  if (sourceChat) properties['来源对话'] = textProp(sourceChat);
  if (originalUrl) properties['原始对话'] = urlProp(originalUrl);

  Object.keys(properties).forEach(k => properties[k] === undefined && delete properties[k]);

  const children = [];
  if (insight) {
    children.push({
      object: 'block', type: 'callout',
      callout: {
        icon: { emoji: '💖' },
        color: 'pink_background',
        rich_text: [{ text: { content: insight.slice(0, 1900) } }]
      }
    });
  }
  children.push({
    object: 'block', type: 'paragraph',
    paragraph: { rich_text: [{ text: { content: `DNA: ${dnaCode}` } }] }
  });

  return createPage({
    token: cfg.notion_token,
    dbId: cfg.db_heart,
    properties,
    children
  });
}

/**
 * 连接性测试
 */
export async function testConnection(token) {
  try {
    const data = await notionFetch('/users/me', { token });
    return { ok: true, bot: data };
  } catch (e) {
    return { ok: false, error: e.message, status: e.status };
  }
}
