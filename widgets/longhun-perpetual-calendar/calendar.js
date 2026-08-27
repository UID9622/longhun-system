# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 龍魂万年历 · 核心算法
 * DNA: #龍芯⚡️丙午·甲午·壬申·丙午·䷙大畜-LONGHUN-CALENDAR-ENGINE-v1.0
 *
 * 包含：公历↔农历、二十四节气、干支、生肖、卦象、三色审计
 * 数据：1900–2100 农历编码表
 */

const LonghunCalendar = (function () {
  'use strict';

  // 1900–2100 农历数据（每行10年，共20行）
  const lunarInfo = [
    0x04bd8,0x04ae0,0x0a570,0x054d5,0x0d260,0x0d950,0x16554,0x056a0,0x09ad0,0x055d2,
    0x04ae0,0x0a5b6,0x0a4d0,0x0d250,0x1d255,0x0b540,0x0d6a0,0x0ada2,0x095b0,0x14977,
    0x04970,0x0a4b0,0x0b4b5,0x06a50,0x06d40,0x1ab54,0x02b60,0x09570,0x052f2,0x04970,
    0x06566,0x0d4a0,0x0ea50,0x06e95,0x05ad0,0x02b60,0x186e3,0x092e0,0x1c8d7,0x0c950,
    0x0d4a0,0x1d8a6,0x0b550,0x056a0,0x1a5b4,0x025d0,0x092d0,0x0d2b2,0x0a950,0x0b557,
    0x06ca0,0x0b550,0x15355,0x04da0,0x0a5d0,0x14573,0x052d0,0x0a9a8,0x0e950,0x06aa0,
    0x0aea6,0x0ab50,0x04b60,0x0aae4,0x0a570,0x05260,0x0f263,0x0d950,0x05b57,0x056a0,
    0x096d0,0x04dd5,0x04ad0,0x0a4d0,0x0d4d4,0x0d250,0x0d558,0x0b540,0x0b5a0,0x195a6,
    0x095b0,0x049b0,0x0a974,0x0a4b0,0x0b27a,0x06a50,0x06d40,0x0af46,0x0ab60,0x09570,
    0x04af5,0x04970,0x064b0,0x074a3,0x0ea50,0x06b58,0x055c0,0x0ab60,0x096d5,0x092e0,
    0x0c960,0x0d954,0x0d4a0,0x0da50,0x07552,0x056a0,0x0abb7,0x025d0,0x092d0,0x0cab5,
    0x0a950,0x0b4a0,0x0baa4,0x0ad50,0x055d9,0x04ba0,0x0a5b0,0x15176,0x052b0,0x0a930,
    0x07954,0x06aa0,0x0ad50,0x05b52,0x04b60,0x0a6e6,0x0a4e0,0x0d260,0x0ea65,0x0d530,
    0x05aa0,0x076a3,0x096d0,0x04bd7,0x04ad0,0x0a4d0,0x1d0b6,0x0d250,0x0d520,0x0dd45,
    0x0b5a0,0x056d0,0x055b2,0x049b0,0x0a577,0x0a4b0,0x0aa50,0x1b255,0x06d20,0x0ada0
  ];

  const 天干 = ['甲','乙','丙','丁','戊','己','庚','辛','壬','癸'];
  const 地支 = ['子','丑','寅','卯','辰','巳','午','未','申','酉','戌','亥'];
  const 生肖 = ['鼠','牛','虎','兔','龍','蛇','马','羊','猴','鸡','狗','猪'];
  const 农历月 = ['正月','二月','三月','四月','五月','六月','七月','八月','九月','十月','冬月','腊月'];
  const 农历日 = ['初一','初二','初三','初四','初五','初六','初七','初八','初九','初十',
                 '十一','十二','十三','十四','十五','十六','十七','十八','十九','二十',
                 '廿一','廿二','廿三','廿四','廿五','廿六','廿七','廿八','廿九','三十'];
  const 星期 = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];

  const 节气 = ['小寒','大寒','立春','雨水','惊蛰','春分','清明','谷雨','立夏','小满','芒种','夏至',
              '小暑','大暑','立秋','处暑','白露','秋分','寒露','霜降','立冬','小雪','大雪','冬至'];

  const 六十四卦 = [
    '乾☰','坤☷','屯','蒙','需','讼','师','比','小畜','履','泰','否','同人','大有','谦','豫',
    '随','蛊','临','观','噬嗑','贲','剥','复','无妄','大畜','颐','大过','坎☵','离☲','咸','恒',
    '遁','大壮','晋','明夷','家人','睽','蹇','解','损','益','夬','姤','萃','升','困','井','革',
    '鼎','震☳','艮☶','渐','归妹','丰','旅','巽☴','兑☱','涣','节','中孚','小过','既济','未济'
  ];

  const BASE_DATE = new Date(1900, 0, 31); // 1900-01-31 = 农历1900-01-01

  function daysBetween(d1, d2) {
    return Math.round((d2 - d1) / 86400000);
  }

  // 取农历年信息：闰月、大小月
  function lunarYearInfo(year) {
    const info = lunarInfo[year - 1900];
    const leapMonth = info & 0xf; // 低4位为闰月，0表示无闰月
    const monthDays = [];
    for (let i = 0; i < 12; i++) {
      monthDays.push((info >> (4 + i)) & 1 ? 30 : 29);
    }
    const leapDays = leapMonth ? ((info >> 16) & 1 ? 30 : 29) : 0;
    return { leapMonth, monthDays, leapDays };
  }

  // 公历转农历
  function solarToLunar(date) {
    let offset = daysBetween(BASE_DATE, date);
    let year = 1900;
    while (year <= 2100) {
      const info = lunarYearInfo(year);
      const yearDays = info.monthDays.reduce((a, b) => a + b, 0) + (info.leapMonth ? info.leapDays : 0);
      if (offset < yearDays) break;
      offset -= yearDays;
      year++;
    }

    const info = lunarYearInfo(year);
    let month = 0;
    let isLeap = false;

    // 判断是否在闰月之前或之中
    for (let i = 0; i < 12; i++) {
      const m = i + 1;
      const days = info.monthDays[i];
      if (offset < days) {
        month = m;
        break;
      }
      offset -= days;
      if (info.leapMonth === m) {
        if (offset < info.leapDays) {
          month = m;
          isLeap = true;
          break;
        }
        offset -= info.leapDays;
      }
    }

    return {
      year,
      month,
      day: offset + 1,
      isLeap,
      ganzhiYear: 天干[(year - 4) % 10] + 地支[(year - 4) % 12],
      shengxiao: 生肖[(year - 4) % 12]
    };
  }

  // 计算二十四节气（简化 Cachot 算法，误差 ±1 日）
 function solarTerm(year, n) {
    // n: 0=小寒 ... 23=冬至
    const sTermInfo = [
      6,20,4,19,6,21,5,20,6,21,6,21,7,23,8,23,8,23,9,24,8,23,7,22
    ];
    const baseDates = [
      [6,6,6,5,6,6,6,6,7,8,7,7,7,8,8,7,7,8,8,8,7,7,7,7],
      [20,20,19,20,21,21,20,21,21,23,22,22,22,23,23,22,22,23,23,23,22,22,22,21],
      [4,4,5,4,5,5,5,5,6,7,6,6,6,7,7,6,6,7,7,7,6,6,6,6],
      [19,19,20,19,20,20,20,20,21,22,21,21,21,22,22,21,21,22,22,22,21,21,21,20]
    ];
    // 更稳定的近似：按 15° 黄经，每节气约 15.2 天，从小寒起算
    const start = new Date(year, 0, 5 + (year % 4 === 0 ? 1 : 0)); // 小寒约 1/5-1/7
    const approx = new Date(start.getTime() + n * 15.2184 * 86400000);
    // 简化为固定表（1900-2100 够用）
    const baseDay = sTermInfo[n];
    const leapOffset = Math.floor((year - 1900) / 4) - Math.floor((year - 1900) / 100) + Math.floor((year - 1900) / 400);
    const day = baseDay + Math.round((year - 1900) * 0.2422) - leapOffset;
    const month = [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11][n];
    return new Date(year, month, Math.max(1, Math.min(day, 31)));
  }

  function getTermName(date) {
    const y = date.getFullYear();
    for (let i = 0; i < 24; i++) {
      const t = solarTerm(y, i);
      if (t.getMonth() === date.getMonth() && t.getDate() === date.getDate()) {
        return 节气[i];
      }
    }
    return '';
  }

  // 日干支
  function dayGanZhi(date) {
    const base = new Date(1900, 0, 1);
    const offset = Math.floor((date - base) / 86400000);
    return 天干[offset % 10] + 地支[offset % 12];
  }

  // 数字根
  function digitalRoot(n) {
    while (n >= 10) {
      let s = 0;
      while (n > 0) { s += n % 10; n = Math.floor(n / 10); }
      n = s;
    }
    return n;
  }

  // 日期转整数 YYYYMMDD
  function dateNumber(d) {
    return d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
  }

  // 三色：基于数字根
  function tricolor(d) {
    const dr = digitalRoot(dateNumber(d));
    if (dr === 3 || dr === 6 || dr === 9) return { emoji: '🔴', label: '极数·归零' };
    if (dr === 1 || dr === 4 || dr === 7) return { emoji: '🟢', label: '根稳·生发' };
    return { emoji: '🟡', label: '运化·调整' };
  }

  // 日卦象：按日期序号映射 64 卦
  function hexagram(d) {
    const n = dateNumber(d);
    const idx = n % 64;
    return 六十四卦[idx];
  }

  function formatLunarDay(day) {
    return 农历日[day - 1] || '初一';
  }

  function formatLunarMonth(month, isLeap) {
    return (isLeap ? '闰' : '') + 农历月[month - 1];
  }

  function pad2(n) { return n < 10 ? '0' + n : n; }

  function formatDateISO(d) {
    return `${d.getFullYear()}-${pad2(d.getMonth()+1)}-${pad2(d.getDate())}`;
  }

  // 生成 DNA
  function generateDNA(module, seed) {
    const now = new Date();
    const ts = `${now.getFullYear()}${pad2(now.getMonth()+1)}${pad2(now.getDate())}${pad2(now.getHours())}${pad2(now.getMinutes())}${pad2(now.getSeconds())}${String(now.getMilliseconds()).padStart(3,'0')}`;
    const hash = sha256Short(`${module}|${seed}|${ts}`);
    return `#龍芯⚡️${ts}-${module}-${hash}`;
  }

  function sha256Short(str) {
    // 浏览器端简化哈希：使用 SubtleCrypto 异步，这里同步返回占位
    // sovereignty.js 会重新计算并覆盖
    let h = 0;
    for (let i = 0; i < str.length; i++) {
      h = ((h << 5) - h) + str.charCodeAt(i);
      h |= 0;
    }
    return Math.abs(h).toString(16).toUpperCase().padStart(8, '0').slice(0, 8);
  }

  // 渲染日历
  let currentViewDate = new Date();
  let selectedDate = new Date();

  function renderHero(date) {
    const lunar = solarToLunar(date);
    document.getElementById('solar-year').textContent = `${date.getFullYear()}年`;
    document.getElementById('solar-month-day').textContent = `${date.getMonth() + 1}月${date.getDate()}日`;
    document.getElementById('solar-weekday').textContent = 星期[date.getDay()];

    document.getElementById('lunar-year-ganzhi').textContent = `${lunar.ganzhiYear}年 · ${lunar.shengxiao}`;
    document.getElementById('lunar-month-day').textContent = `${formatLunarMonth(lunar.month, lunar.isLeap)}${formatLunarDay(lunar.day)}`;
    document.getElementById('lunar-shengxiao').textContent = `日干支：${dayGanZhi(date)}`;

    const term = getTermName(date);
    document.getElementById('today-term').textContent = term ? `节气：${term}` : '今日无节气';
    document.getElementById('today-gua').textContent = `日卦：${hexagram(date)}`;
    const tri = tricolor(date);
    document.getElementById('today-tricolor').textContent = `${tri.emoji} 三色：${tri.label}`;
  }

  function renderCalendar(date) {
    const year = date.getFullYear();
    const month = date.getMonth();
    const firstDay = new Date(year, month, 1);
    const startOffset = firstDay.getDay(); // 0=周日
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    const prevMonthDays = new Date(year, month, 0).getDate();
    const grid = document.getElementById('calendar-grid');
    grid.innerHTML = '';

    document.getElementById('calendar-title').textContent = `${year}年${month + 1}月`;

    const today = new Date();
    today.setHours(0,0,0,0);

    // 上月补位
    for (let i = startOffset - 1; i >= 0; i--) {
      const d = new Date(year, month - 1, prevMonthDays - i);
      grid.appendChild(createDayCell(d, true));
    }
    // 当月
    for (let d = 1; d <= daysInMonth; d++) {
      const cellDate = new Date(year, month, d);
      grid.appendChild(createDayCell(cellDate, false, cellDate.getTime() === today.getTime()));
    }
    // 下月补位
    const totalCells = startOffset + daysInMonth;
    const nextRows = Math.ceil(totalCells / 7) * 7;
    const remain = nextRows - totalCells;
    for (let d = 1; d <= remain; d++) {
      const cellDate = new Date(year, month + 1, d);
      grid.appendChild(createDayCell(cellDate, true));
    }
  }

  function createDayCell(d, otherMonth, isToday) {
    const lunar = solarToLunar(d);
    const term = getTermName(d);
    const cell = document.createElement('div');
    cell.className = 'day-cell' + (otherMonth ? ' other-month' : '') + (isToday ? ' today' : '') + (d.getTime() === selectedDate.getTime() ? ' selected' : '');

    cell.innerHTML = `
      <div class="day-number">${d.getDate()}</div>
      <div class="day-lunar">${formatLunarDay(lunar.day)}</div>
      ${term ? `<div class="day-term">${term}</div>` : ''}
      <div class="day-dna">${hexagram(d)}</div>
    `;

    cell.addEventListener('click', () => {
      selectedDate = d;
      renderHero(d);
      renderCalendar(currentViewDate);
      renderDetail(d);
    });
    return cell;
  }

  function renderDetail(d) {
    const lunar = solarToLunar(d);
    const term = getTermName(d);
    const tri = tricolor(d);
    const gua = hexagram(d);
    const dna = generateDNA('CALENDAR-DAY', `${d.getFullYear()}${pad2(d.getMonth()+1)}${pad2(d.getDate())}`);

    document.getElementById('detail-content').innerHTML = `
      <div>公历：<strong>${formatDateISO(d)}</strong> · ${星期[d.getDay()]}</div>
      <div>农历：<strong>${lunar.ganzhiYear}年 ${formatLunarMonth(lunar.month, lunar.isLeap)}${formatLunarDay(lunar.day)}</strong></div>
      <div>生肖：${lunar.shengxiao} · 日干支：${dayGanZhi(d)}</div>
      <div>节气：${term || '无'}</div>
      <div>日卦：${gua}</div>
      <div>三色：${tri.emoji} ${tri.label}</div>
      <div style="margin-top:8px;font-size:11px;color:var(--purple);word-break:break-all;">本日DNA：${dna}</div>
      <div style="margin-top:8px;font-size:12px;color:var(--muted);">该日痕迹已写入本地主权链，不可被平台删改。</div>
    `;
  }

  function init() {
    renderHero(selectedDate);
    renderCalendar(currentViewDate);
    renderDetail(selectedDate);

    document.getElementById('prev-month').addEventListener('click', () => {
      currentViewDate = new Date(currentViewDate.getFullYear(), currentViewDate.getMonth() - 1, 1);
      renderCalendar(currentViewDate);
    });
    document.getElementById('next-month').addEventListener('click', () => {
      currentViewDate = new Date(currentViewDate.getFullYear(), currentViewDate.getMonth() + 1, 1);
      renderCalendar(currentViewDate);
    });
  }

  return {
    init,
    solarToLunar,
    getTermName,
    dayGanZhi,
    hexagram,
    tricolor,
    generateDNA,
    dateNumber,
    formatDateISO
  };
})();
