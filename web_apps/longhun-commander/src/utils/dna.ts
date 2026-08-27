# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// DNA追溯生成器 · 龍魂核心
// DNA: #龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-LONGHUN-HEART-TALK-v1.0

import type { AuditColor } from '@/types';

let msgCounter = 0;

export function generateDNA(
  project: string,
  module: string,
  version: string = 'v1.0'
): string {
  const now = new Date();
  const date = now.toISOString().slice(0, 10);
  return `#龍芯⚡️${date}-${project}-${module}-${version}`;
}

export function generateMessageDNA(roomId: string, _index: number): string {
  const date = new Date().toISOString().slice(0, 10);
  msgCounter++;
  return `#龍芯⚡️${date}-HEART-TALK-${roomId}-MSG${String(msgCounter).padStart(4, '0')}`;
}

export function generateRoomDNA(roomType: string, roomName: string): string {
  const date = new Date().toISOString().slice(0, 10);
  const sanitized = roomName.replace(/\s+/g, '-').slice(0, 12).toUpperCase();
  return `#龍芯⚡️${date}-ROOM-${roomType}-${sanitized}-v1.0`;
}

export function sha256Hash(input: string): string {
  // 浏览器可用的简化哈希模拟
  let hash = 0;
  for (let i = 0; i < input.length; i++) {
    const char = input.charCodeAt(i);
    hash = ((hash << 5) - hash + char) | 0;
  }
  return Math.abs(hash).toString(16).padStart(16, '0');
}

export function encryptSimulate(text: string): string {
  // 模拟端侧加密 — 显示为加密摘要
  const hash = sha256Hash(text);
  return `[ENCRYPTED:${hash.slice(0, 8)}...${hash.slice(-8)}]`;
}

export function getTimestamp(): string {
  const now = new Date();
  return now.toISOString().replace('T', ' ').slice(0, 19);
}

export function getLonghunTimestamp(): string {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  const h = String(now.getHours()).padStart(2, '0');
  const min = String(now.getMinutes()).padStart(2, '0');
  const s = String(now.getSeconds()).padStart(2, '0');
  return `${y}年${m}月${d}日 ${h}:${min}:${s}`;
}

export function auditMessage(content: string): AuditColor {
  // 模拟三层监督审计
  const lower = content.toLowerCase();
  // 感知层：检测危险关键词
  const dangerWords = ['攻击', '暴力', '色情', '诈骗', '反动', '颠覆'];
  const warnWords = ['争议', '纠纷', '投诉', '敏感', '政治', '宗教'];
  
  if (dangerWords.some(w => lower.includes(w))) return '🔴';
  if (warnWords.some(w => lower.includes(w))) return '🟡';
  return '🟢';
}

// 六十甲子
const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
const HEXAGRAMS = [
  '乾', '坤', '屯', '蒙', '需', '讼', '师', '比',
  '小畜', '履', '泰', '否', '同人', '大有', '谦', '豫',
  '随', '蛊', '临', '观', '噬嗑', '贲', '剥', '复',
  '无妄', '大畜', '颐', '大过', '坎', '离', '咸', '恒',
  '遁', '大壮', '晋', '明夷', '家人', '睽', '蹇', '解',
  '损', '益', '夬', '姤', '萃', '升', '困', '井',
  '革', '鼎', '震', '艮', '渐', '归妹', '丰', '旅',
  '巽', '兑', '涣', '节', '中孚', '小过', '既济', '未济',
];

export function getGanZhi(offset: number = 0): string {
  const base = 36; // 2026-06-28 = 甲辰年
  const idx = (base + offset) % 60;
  return TIAN_GAN[idx % 10] + DI_ZHI[idx % 12];
}

export function getHexagram(date: Date): string {
  const day = date.getDate();
  const month = date.getMonth() + 1;
  const idx = ((day + month) * 7) % 64;
  return HEXAGRAMS[idx];
}

export function getJieQi(date: Date): string | undefined {
  const m = date.getMonth() + 1;
  const d = date.getDate();
  const jieQiTable: Record<number, { name: string; day: number }[]> = {
    1: [{ name: '小寒', day: 5 }, { name: '大寒', day: 20 }],
    2: [{ name: '立春', day: 3 }, { name: '雨水', day: 18 }],
    3: [{ name: '惊蛰', day: 5 }, { name: '春分', day: 20 }],
    4: [{ name: '清明', day: 4 }, { name: '谷雨', day: 20 }],
    5: [{ name: '立夏', day: 5 }, { name: '小满', day: 21 }],
    6: [{ name: '芒种', day: 5 }, { name: '夏至', day: 21 }],
    7: [{ name: '小暑', day: 7 }, { name: '大暑', day: 22 }],
    8: [{ name: '立秋', day: 7 }, { name: '处暑', day: 23 }],
    9: [{ name: '白露', day: 7 }, { name: '秋分', day: 23 }],
    10: [{ name: '寒露', day: 8 }, { name: '霜降', day: 23 }],
    11: [{ name: '立冬', day: 7 }, { name: '小雪', day: 22 }],
    12: [{ name: '大雪', day: 7 }, { name: '冬至', day: 21 }],
  };
  const entries = jieQiTable[m];
  if (!entries) return undefined;
  for (const e of entries) {
    if (Math.abs(d - e.day) <= 1) return e.name;
  }
  return undefined;
}

export function getLunarDay(date: Date): string {
  const lunarDays = [
    '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
    '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
    '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十',
  ];
  // 简化农历计算 — 基于固定偏移
  const baseDay = 14; // 2026-06-28 = 五月十四
  const dayOfYear = Math.floor((date.getTime() - new Date(date.getFullYear(), 0, 0).getTime()) / 86400000);
  const lunarDayIdx = (baseDay + dayOfYear) % 30;
  return lunarDays[lunarDayIdx];
}
