/**
 * 🐉 龙魂·干支时间戳
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-GANZHI-TIMESTAMP-v1.0
 * License: MulanPSL v2
 * 创建者: 诸葛鑫（UID9622）
 */
import { TianGanDiZhi } from '../yijing/culture/TianGanDiZhi';

/** 64卦Unicode符号表 */
const GUA_SYMBOLS_64: string[] = [
  '', '䷀','䷁','䷂','䷃','䷄','䷅','䷆','䷇',
  '䷈','䷉','䷊','䷋','䷌','䷍','䷎','䷏',
  '䷐','䷑','䷒','䷓','䷔','䷕','䷖','䷗',
  '䷘','䷙','䷚','䷛','䷜','䷝','䷞','䷟',
  '䷠','䷡','䷢','䷣','䷤','䷥','䷦','䷧',
  '䷨','䷩','䷪','䷫','䷬','䷭','䷮','䷯',
  '䷰','䷱','䷲','䷳','䷴','䷵','䷶','䷷',
  '䷸','䷹','䷺','䷻','䷼','䷽','䷾','䷿',
];

export class GanzhiTimestamp {
  /** 获取当前完整时间戳 */
  static getCurrent(): { full: string; compact: string; simple: string; guaId: number } {
    const now = new Date();
    const ganzhi = TianGanDiZhi.getFullGanzhi(now);

    // 用时间起卦获取当前卦
    const upperNum = (now.getFullYear() + now.getMonth() + 1 + now.getDate()) % 8;
    const lowerNum = (now.getFullYear() + now.getMonth() + 1 + now.getDate() + now.getHours()) % 8;
    // 6位二进制: upper×8 + lower → 卦ID (0-63)
    const guaKey = ((upperNum === 0 ? 8 : upperNum) - 1) * 8 + ((lowerNum === 0 ? 8 : lowerNum) - 1);

    const guaId = guaKey + 1;
    const guaSymbol = GUA_SYMBOLS_64[guaId] || '?';

    const iso = now.toISOString();

    return {
      full: `[${ganzhi}·${guaSymbol}] ${iso}`,
      compact: `#龍芯⚡️${ganzhi}·${guaSymbol}`,
      simple: `🐉${ganzhi.split('·')[2] || ganzhi}·${guaSymbol}`,
      guaId,
    };
  }
}
