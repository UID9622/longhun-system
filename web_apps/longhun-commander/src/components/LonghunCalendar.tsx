// 龍魂万年历组件 · 农历/节气/卦象/主权审计
// DNA: #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v1.0

import { CalendarDays, Sparkles } from 'lucide-react';
import { getLonghunTimestamp, getTimestamp } from '@/utils/dna';

interface CalendarDay {
  date: Date;
  lunar: string;
  ganZhi: string;
  hexagram: string;
  jieQi: string | null;
  isToday: boolean;
}

function generateCalendarDays(): CalendarDay[] {
  const today = new Date();
  const hexagrams = ['乾','坤','屯','蒙','需','讼','师','比','小畜','履','泰','否','同人','大有','谦','豫','随','蛊','临','观','噬嗑','贲','剥','复','无妄','大畜','颐','大过','坎','离','咸','恒','遁','大壮','晋','明夷','家人','睽','蹇','解','损','益','夬','姤','萃','升','困','井','革','鼎','震','艮','渐','归妹','丰','旅','巽','兑','涣','节','中孚','小过','既济','未济'];
  const ganZhi = ['甲子','乙丑','丙寅','丁卯','戊辰','己巳','庚午','辛未','壬申','癸酉','甲戌','乙亥','丙子','丁丑','戊寅','己卯','庚辰','辛巳','壬午','癸未','甲申','乙酉','丙戌','丁亥','戊子','己丑','庚寅','辛卯','壬辰','癸巳','甲午','乙未','丙申','丁酉','戊戌','己亥','庚子','辛丑','壬寅','癸卯','甲辰','乙巳','丙午','丁未','戊申','己酉','庚戌','辛亥','壬子','癸丑','甲寅','乙卯','丙辰','丁巳','戊午','己未','庚申','辛酉','壬戌','癸亥'];
  const lunarDays = ['初一','初二','初三','初四','初五','初六','初七','初八','初九','初十','十一','十二','十三','十四','十五','十六','十七','十八','十九','二十','廿一','廿二','廿三','廿四','廿五','廿六','廿七','廿八','廿九','三十'];

  const result: CalendarDay[] = [];
  const start = new Date(today);
  start.setDate(today.getDate() - today.getDay());

  for (let i = 0; i < 35; i++) {
    const date = new Date(start);
    date.setDate(start.getDate() + i);
    const isToday = date.toDateString() === today.toDateString();
    const dayIndex = (date.getDate() + date.getMonth() * 30) % 30;
    const gzIndex = (date.getDate() + date.getMonth() * 2) % 60;
    const hxIndex = (date.getDate() + date.getMonth() * 5) % 64;
    result.push({
      date,
      lunar: lunarDays[dayIndex] || '初一',
      ganZhi: ganZhi[gzIndex] || '甲子',
      hexagram: hexagrams[hxIndex] || '乾',
      jieQi: null,
      isToday,
    });
  }
  return result;
}

export default function LonghunCalendar() {
  const days = generateCalendarDays();
  const today = days.find((d: CalendarDay) => d.isToday);

  return (
    <div className="space-y-3">
      {/* 今日主面板 */}
      {today && (
        <div className="p-3 rounded-lg border border-amber-500/20 bg-gradient-to-br from-amber-500/5 to-zinc-900/50">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-lg font-bold text-amber-400">{getLonghunTimestamp()}</p>
              <p className="text-xs text-zinc-500 font-mono mt-0.5">{getTimestamp()}</p>
            </div>
            <Sparkles className="w-5 h-5 text-amber-500/50" />
          </div>
          <div className="flex items-center gap-3 mt-2">
            <span className="text-sm text-zinc-300">{today.lunar}</span>
            <span className="text-xs px-2 py-0.5 rounded bg-zinc-800 text-zinc-400 font-mono">{today.ganZhi}日</span>
            <span className="text-xs px-2 py-0.5 rounded bg-purple-500/10 text-purple-400 border border-purple-500/20">
              {today.hexagram}卦
            </span>
            {today.jieQi && (
              <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                {today.jieQi}
              </span>
            )}
          </div>
        </div>
      )}

      {/* 十五天视图 */}
      <div className="grid grid-cols-7 gap-1">
        {['日', '一', '二', '三', '四', '五', '六'].map(d => (
          <div key={d} className="text-center text-[10px] text-zinc-600 py-1">{d}</div>
        ))}
        {days.map((day: CalendarDay, i: number) => (
          <div
            key={i}
            className={`aspect-square rounded border flex flex-col items-center justify-center text-center transition-all ${
              day.isToday
                ? 'border-amber-500/40 bg-amber-500/10'
                : 'border-zinc-800/30 bg-zinc-900/30 hover:border-zinc-700/50'
            }`}
          >
            <span className={`text-[10px] font-mono ${day.isToday ? 'text-amber-400 font-bold' : 'text-zinc-400'}`}>
              {day.date.getDate()}
            </span>
            <span className="text-[8px] text-zinc-600 mt-0.5">{day.lunar}</span>
            {day.jieQi && (
              <span className="text-[6px] text-emerald-500/70 mt-0.5">{day.jieQi}</span>
            )}
            {day.isToday && (
              <div className="w-1 h-1 rounded-full bg-amber-500 mt-0.5" />
            )}
          </div>
        ))}
      </div>

      {/* DNA时间戳 */}
      <div className="p-2 rounded border border-zinc-800/30 bg-zinc-900/30">
        <div className="flex items-center gap-2">
          <CalendarDays className="w-3 h-3 text-amber-500/50" />
          <code className="text-[10px] text-amber-500/70 font-mono truncate">
            #龍芯⚡️2026-06-28-CALENDAR-ACTIVE-v1.0
          </code>
        </div>
      </div>
    </div>
  );
}
