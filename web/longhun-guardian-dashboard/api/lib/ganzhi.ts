/**
 * 龍魂干支时间戳引擎 v∞
 * DNA: #龍芯⚡️2026-07-12-LONGHUN-GANZHI-ENGINE-v1.0
 * 农历干支四柱 + 卦名 + v∞ DNA格式
 * 纯TypeScript实现·无外部依赖
 */

// ========== 天干地支常量 ==========
const 天干 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"] as const;
const 地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"] as const;
const 六十甲子 = Array.from({ length: 60 }, (_, i) => 天干[i % 10] + 地支[i % 12]);
const 时辰名 = ["子时", "丑时", "寅时", "卯时", "辰时", "巳时", "午时", "未时", "申时", "酉时", "戌时", "亥时"] as const;
const 六十四卦 = [
  "乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履", "泰", "否",
  "同人", "大有", "谦", "豫", "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
  "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒", "遁", "大壮", "晋", "明夷",
  "家人", "睽", "蹇", "解", "损", "益", "夬", "姤", "萃", "升", "困", "井",
  "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣", "节",
  "中孚", "小过", "既济", "未济",
] as const;
const 五行 = ["水", "火", "木", "金", "土"] as const;

/** 计算年干支 (立春换年) */
export function 年干支(yyyy: number): string {
  // 天干: (年份-4)%10
  // 地支: (年份-4)%12
  const g = (yyyy - 4) % 10;
  const z = (yyyy - 4) % 12;
  return 天干[g] + 地支[z];
}

/** 计算月干支 (年干决定月干起点) */
export function 月干支(yyyy: number, mm: number): string {
  const yearGan = (yyyy - 4) % 10; // 年天干索引
  // 寅月为正月, 月干由年干决定
  // 甲己之年丙作首, 乙庚之岁戊为头, 丙辛之岁寻庚起, 丁壬壬位顺行流, 若问戊癸何方发, 甲寅之上好追求
  const 月干起点表 = [2, 4, 6, 8, 0]; // 甲/己→丙(2), 乙/庚→戊(4), 丙/辛→庚(6), 丁/壬→壬(8), 戊/癸→甲(0)
  const yearGanMod5 = yearGan % 5;
  const 月干起点 = 月干起点表[yearGanMod5];
  // 正月(寅)=地支第2位
  const monthIndex = mm - 1; // 0-indexed
  const gan = (月干起点 + monthIndex) % 10;
  const zhi = (2 + monthIndex) % 12; // 从寅开始
  return 天干[gan] + 地支[zhi];
}

/** 计算日干支 (已知锚点推算) */
export function 日干支(yyyy: number, mm: number, dd: number): string {
  // 使用锚点: 1900-01-01 = 甲戌日
  const anchor = new Date(1900, 0, 1);
  const target = new Date(yyyy, mm - 1, dd);
  const diffDays = Math.floor((target.getTime() - anchor.getTime()) / 86400000);
  const anchorIndex = 10; // 甲戌在六十甲子中索引=10
  const index = ((anchorIndex + diffDays) % 60 + 60) % 60;
  return 六十甲子[index];
}

/** 计算时辰 */
export function 时干支(yyyy: number, mm: number, dd: number, hh: number): string {
  const dayGanzhi = 日干支(yyyy, mm, dd);
  const dayGanIndex = 天干.indexOf(dayGanzhi[0] as any);
  // 时干由日干决定
  const 时干起点表 = [0, 2, 4, 6, 8]; // 甲/己→甲(0), 乙/庚→丙(2), 丙/辛→戊(4), 丁/壬→庚(6), 戊/癸→壬(8)
  const 时干起点 = 时干起点表[dayGanIndex % 5];
  // 时辰: 0-1=子时, 2-3=丑时, ...
  const hourZhi = Math.floor(((hh + 1) % 24) / 2);
  const gan = (时干起点 + hourZhi) % 10;
  return 天干[gan] + 地支[hourZhi];
}

/** 获取时辰名 */
export function 时辰名计算(hh: number): string {
  const idx = Math.floor(((hh + 1) % 24) / 2);
  return 时辰名[idx];
}

/** 计算卦名 (基于四柱索引取卦) */
export function 卦名(yyyy: number, mm: number, dd: number, hh: number): string {
  const yg = (yyyy - 4) % 64;
  const mg = (mm * 5 + dd) % 64;
  const dg = (dd * 3 + hh) % 64;
  const hg = (hh * 7 + mm) % 64;
  const idx = (yg + mg + dg + hg) % 64;
  return 六十四卦[idx];
}

/** dr(数字根) → 五行 */
export function dr五行(dr: number): string {
  const d = ((dr - 1) % 9 + 9) % 9 + 1;
  if (d === 1 || d === 6) return "水";
  if (d === 2 || d === 7) return "火";
  if (d === 3 || d === 8) return "木";
  if (d === 4 || d === 9) return "金";
  return "土"; // d=5
}

/** 计算数字根 */
export function 数字根(n: number): number {
  if (n === 0) return 9;
  const r = n % 9;
  return r === 0 ? 9 : r;
}

// ========== 四柱结构 ==========
export interface 四柱 {
  年干支: string;
  月干支: string;
  日干支: string;
  时干支: string;
  时辰名: string;
  卦名: string;
  五行: string;
  数字根: number;
}

/** 获取当前四柱 */
export function 获取四柱(d?: Date): 四柱 {
  const now = d ?? new Date();
  const yyyy = now.getFullYear();
  const mm = now.getMonth() + 1;
  const dd = now.getDate();
  const hh = now.getHours();
  const yg = 年干支(yyyy);
  const mg = 月干支(yyyy, mm);
  const dg = 日干支(yyyy, mm, dd);
  const tg = 时干支(yyyy, mm, dd, hh);
  const sn = 时辰名计算(hh);
  const gn = 卦名(yyyy, mm, dd, hh);
  const dr = 数字根(yyyy + mm + dd + hh);
  const wx = dr五行(dr);
  return { 年干支: yg, 月干支: mg, 日干支: dg, 时干支: tg, 时辰名: sn, 卦名: gn, 五行: wx, 数字根: dr };
}

// ========== v∞ DNA格式 ==========
export interface DNAv2 {
  stamp: string;      // #龍芯⚡️丙午·甲午·丁丑·巳时·乾
  module: string;     // INTAKE
  action: string;     // CLEANSE
  hash8: string;      // BF8BA356
  full: string;       // 完整DNA
}

/** 生成v∞ DNA (干支卦格式) */
export function 生成DNAv2(module: string, action: string, seed?: string): DNAv2 {
  const gz = 获取四柱();
  const stamp = `#龍芯⚡️${gz.年干支}·${gz.月干支}·${gz.日干支}·${gz.时辰名}·${gz.卦名}`;
  const src = (seed ?? Date.now().toString()) + module + action + stamp;
  const hash8 = sm3simple(src).substring(0, 8).toUpperCase();
  const full = `${stamp}-${module}-${action}-${hash8}`;
  return { stamp, module, action, hash8, full };
}

/** 简化SM3 (用于DNA哈希) */
function sm3simple(message: string): string {
  let hash = 0;
  for (let i = 0; i < message.length; i++) {
    const ch = message.charCodeAt(i);
    hash = ((hash << 5) - hash + ch) | 0;
  }
  return Math.abs(hash).toString(16).padStart(8, "0");
}

/** 生成旧版DNA (兼容) */
export function 生成DNAv1(module: string, action: string): string {
  const now = new Date();
  const date = now.toISOString().split("T")[0];
  const hash = sm3simple(date + module + action + Date.now().toString());
  return `#龍芯⚡️${date}-${module}-${action}-v1.0-${hash.substring(0, 8).toUpperCase()}`;
}

/** 六维评估 */
export interface 六维评估 {
  权重层级: string;   // L0永恒 / L1百年 / L2十年 / L3日常 / L4瞬时
  五行归属: string;   // 水火木金土
  三色审计: string;   // 🟢🟡🔴
  贡献值: number;      // 0-10
  热度状态: string;    // 🔥刚发生 / ✅30天内 / ⚠️60天 / 💤90天
  去向判定: string;    // 桶1-5
}

/** 执行六维评估 */
export function 六维评估(content: string, metadata?: any): 六维评估 {
  const len = content.length;
  const hasP0 = content.includes("P0") || content.includes("P0++") || content.includes("L0");
  const hasDNA = content.includes("#龍芯⚡️") || content.includes("DNA");
  const hasLaw = content.includes("宪法") || content.includes("铁律") || content.includes("原则");
  const hasCode = content.includes("```") || content.includes("function") || content.includes("class");
  const age = metadata?.ageDays ?? 0;

  // 权重层级
  let 权重层级 = "L3 日常";
  if (hasP0 && hasDNA) 权重层级 = "L0 ♾️ 永恒";
  else if (hasP0 || (hasLaw && hasDNA)) 权重层级 = "L1 🏛️ 百年";
  else if (hasLaw || hasDNA) 权重层级 = "L2 🗓️ 十年";
  else if (len < 50) 权重层级 = "L4 瞬时";

  // 数字根→五行
  const dr = 数字根(len + (hasP0 ? 9 : 0) + (hasDNA ? 7 : 0));
  const 五行归属 = dr五行(dr);

  // 三色审计
  let 三色审计 = "🟢";
  if (dr === 3 || dr === 9) 三色审计 = "🔴";
  else if (dr === 6 || hasP0) 三色审计 = "🟡";

  // 贡献值
  let 贡献值 = 5;
  if (hasP0) 贡献值 = 10;
  else if (hasDNA && hasLaw) 贡献值 = 9;
  else if (hasDNA) 贡献值 = 7;
  else if (hasCode) 贡献值 = 6;
  else if (len > 500) 贡献值 = 6;
  else if (len < 100) 贡献值 = 3;

  // 热度
  let 热度状态 = "🔥 刚发生";
  if (age > 90) 热度状态 = "💤 超90天";
  else if (age > 60) 热度状态 = "⚠️ 60天没动";
  else if (age > 30) 热度状态 = "✅ 30天内";

  // 去向
  let 去向判定 = "📦 桶2·入库";
  if (贡献值 >= 9) 去向判定 = "🔁 桶4·升级为系统能力";
  else if (贡献值 >= 5) 去向判定 = "🟢 桶1·推草日志";
  else if (贡献值 >= 2) 去向判定 = "⚡ 桶3·内部消化";
  else 去向判定 = "💤 桶5·归档";
  if (三色审计 === "🔴") 去向判定 = "🔴 熔断·留L4证据链";
  else if (三色审计 === "🟡") 去向判定 = "🔁 桶4·待迭代池";

  return { 权重层级, 五行归属, 三色审计, 贡献值, 热度状态, 去向判定 };
}

/** 格式化四柱为字符串 */
export function 四柱字符串(gz?: 四柱): string {
  const g = gz ?? 获取四柱();
  return `${g.年干支}年·${g.月干支}月·${g.日干支}日·${g.时辰名}·${g.卦名}卦·五行${g.五行}`;
}

/** 今日DNA回单 (曾仕强老师格式) */
export function 今日DNA回单(): string {
  const gz = 获取四柱();
  const date = new Date();
  const iso = date.toISOString().split("T")[0];
  return `农历 ${gz.年干支}年 ${gz.月干支}月 ${gz.日干支}日 ${gz.时辰名} | 公历 ${iso} | 五行 ${gz.五行} | 宜:记录·归档·DNA盖章·忌:删除·绕过·熔断`;
}
