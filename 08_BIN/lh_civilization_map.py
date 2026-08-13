#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""🐉 龍魂·文明基因图谱引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·戊午·午时·谦-LH-CIVILIZATION-MAP-v1.0
创建者: 诸葛鑫（UID9622） · 协议: CC BY-NC-SA 4.0

三向进化：
  深 → 历史DNA扫描器升级为【文明基因图谱】：事件编码为DNA特征向量（甲子序/卦象/五行/类型），
       滑动窗口序列比对 → 自动识别【历史重演】模式（历史周期律）。
  宽 → 领域参数化：同一套引擎，切数据即用。内置 龍魂史 / 希腊神话谱系 / 工业革命时间线。
  活 → 装上嘴巴：重演识别 → 预言生成 → 日历事件+Bark推送；H武器16维推演联动输出战略投影。

输出（静态JSON，前端/订阅源直接消费）：
  gene-map.json   文明基因图谱 + 重演模式
  prophecy.json   预言（重演→预测下一步）
  h-weapon.json   H武器推演投影（太极易经收敛解）

用法：
  python3 bin/lh_civilization_map.py scan  [--data-dir DIR] [--out DIR] [--domain all]
  python3 bin/lh_civilization_map.py domains
  python3 bin/lh_civilization_map.py status
"""
from __future__ import annotations
import hashlib, json, sys, time, math
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─────────────────────────────────────────────
# 底座锚点：太极易经核心
# ─────────────────────────────────────────────
十天干 = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
十二地支 = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
河图五行 = {1: '水', 2: '火', 3: '木', 4: '金', 5: '土', 6: '水', 7: '火', 8: '木', 9: '金'}

# 64卦（序号1-64，简表：序号→卦名）
六十四卦 = [
    '', '乾', '坤', '屯', '蒙', '需', '讼', '师', '比', '小畜', '履',
    '泰', '否', '同人', '大有', '谦', '豫', '随', '蛊', '临', '观',
    '噬嗑', '贲', '剥', '复', '无妄', '大畜', '颐', '大过', '坎', '离',
    '咸', '恒', '遁', '大壮', '晋', '明夷', '家人', '睽', '蹇', '解',
    '损', '益', '夬', '姤', '萃', '升', '困', '井', '革', '鼎',
    '震', '艮', '渐', '归妹', '丰', '旅', '巽', '兑', '涣', '节',
    '中孚', '小过', '既济', '未济',
]


def 数字根(n: int) -> int:
    """洛书数字根 1-9"""
    if n == 0:
        return 0
    r = n % 9
    return 9 if r == 0 else r


def 甲子索引(year: int) -> int:
    """六十甲子索引：1984=甲子年=0，六十年一周期（历史周期律的时间轴）"""
    return (year - 1984) % 60


def 梅花易数卦(year: int, month: int, day: int, hour: int = 0) -> int:
    """梅花易数时间起卦 → 卦序号(1-64)
    上卦 = (年+月+日) % 8 · 下卦 = (年+月+日+时) % 8 · 动爻 = (年+月+日+时) % 6"""
    base = year + month + day
    upper = base % 8 or 8
    lower = (base + hour) % 8 or 8
    # 先天卦序: 乾1兑2离3震4巽5坎6艮7坤8
    先天 = {1: 1, 2: 58, 3: 30, 4: 51, 5: 57, 6: 29, 7: 52, 8: 2}
    upper_gua = 先天[upper]
    lower_gua = 先天[lower]
    return ((upper_gua - 1) * 8 + lower_gua) % 64 + 1


def 五行(数字根_val: int) -> str:
    return 河图五行.get(数字根_val, '土')


def _sha8(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:8]


# ─────────────────────────────────────────────
# 领域配置（宽：一套引擎 · 多领域通用）
# ─────────────────────────────────────────────
# 事件模板: (年, 月, 日, 类型, 标题, 描述)
# 类型统一枚举: 诞生/革命/变革/危机/扩张/发明/复兴/征服/联盟/战争
DOMAINS: Dict[str, Dict[str, Any]] = {
    'longhun': {
        'name': '龍魂史',
        'desc': '龍魂体系自身关键里程碑 · 事件源：日历事件 + 扫描差异',
        'seed_events': [
            (2026, 6, 27, '诞生', '龍魂万年历上线', '自主渲染·自主字体·自主主权，不按苹果/谷歌/华为标准走'),
            (2026, 7, 20, '变革', '对齐规则v2.1全量补全', '三层对齐·审计体系·降级处理'),
            (2026, 7, 28, '变革', 'GPG签名焊死', '1574个.asc分离签名·GATE-11签名闸·自动补签'),
            (2026, 8, 2, '变革', 'LU-Time Engine v4.0时间戳焊死', '天干地支四柱·64卦·每句输出附卦'),
            (2026, 8, 4, '变革', '分层许可治理', '思想层CC BY-NC-SA + 工程层MulanPSL v2'),
            (2026, 8, 12, '扩张', '预警日历上线', '历史DNA扫描器+万年历通知闭环·鲲鹏每小时自动巡检'),
        ],
    },
    'greek': {
        'name': '希腊神话谱系',
        'desc': '赫西俄德《神谱》主线 · 神权更迭与宇宙秩序',
        'seed_events': [
            (0, 1, 1, '诞生', '卡俄斯诞生', '混沌初开·万物之源'),
            (100, 1, 1, '诞生', '盖亚诞生', '大地母神·根基确立'),
            (200, 1, 1, '诞生', '乌拉诺斯崛起', '天空神权·第一代统治'),
            (300, 1, 1, '征服', '克洛诺斯阉父夺权', '权力更迭·第二代神权'),
            (400, 1, 1, '危机', '提坦之战爆发', '新旧神权全面对抗'),
            (500, 1, 1, '革命', '宙斯推翻克洛诺斯', '第三代神权确立'),
            (600, 1, 1, '复兴', '奥林匹斯秩序建立', '十二主神分治·宇宙新秩序'),
        ],
    },
    'industrial': {
        'name': '工业革命时间线',
        'desc': '1760-1840 英国工业革命关键节点 · 技术变革周期律',
        'seed_events': [
            (1764, 1, 1, '发明', '珍妮纺纱机', '哈格里夫斯·纺织业革命起点'),
            (1769, 1, 1, '发明', '瓦特改良蒸汽机', '动力革命·工业心脏'),
            (1779, 1, 1, '扩张', '铁桥建成', '铸铁工程·工业建材'),
            (1785, 1, 1, '扩张', '蒸汽织布机投产', '纺织全面机械化'),
            (1814, 1, 1, '发明', '史蒂芬森造出火车', '运输革命·时空压缩'),
            (1825, 1, 1, '变革', '斯托克顿-达灵顿铁路开通', '世界首条商用铁路'),
            (1830, 1, 1, '扩张', '利物浦-曼彻斯特铁路', '铁路网络化·工业帝国成型'),
        ],
    },
}


def _encode_raw(evt: Tuple[int, int, int, str, str, str], seq: int) -> Dict[str, Any]:
    """原始事件 → DNA特征向量（甲子序/卦象/五行/类型）"""
    year, month, day, etype, title, desc = evt
    gz_idx = 甲子索引(max(year, 1984))
    gua_id = 梅花易数卦(year, month, day)
    gua_name = 六十四卦[gua_id] if 0 < gua_id <= 64 else '未济'
    wuxing = 五行(数字根(sum(ord(c) for c in title)))
    return {
        'seq': seq,
        'year': year,
        'month': month,
        'day': day,
        'gz': f"{十天干[gz_idx % 10]}{十二地支[gz_idx % 12]}",
        'gz_idx': gz_idx,
        'gua_id': gua_id,
        'gua': gua_name,
        'wuxing': wuxing,
        'type': etype,
        'title': title,
        'desc': desc,
    }


# ─────────────────────────────────────────────
# 相似度 & 重演识别（深：历史周期律）
# ─────────────────────────────────────────────
def _event_sim(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    """两事件特征相似度 0-1（太极易理加权）"""
    s, w = 0.0, 0.0
    # 类型同构 +0.4
    if a['type'] == b['type']:
        s += 0.4
    w += 0.4
    # 甲子同序（六十年周期共振）+0.3，邻位（相邻周期）+0.15
    diff = abs(a['gz_idx'] - b['gz_idx']) % 60
    if diff == 0:
        s += 0.3
    elif diff in (1, 59):
        s += 0.15
    w += 0.3
    # 卦同 +0.2
    if a['gua_id'] == b['gua_id']:
        s += 0.2
    w += 0.2
    # 五行同 +0.1
    if a['wuxing'] == b['wuxing']:
        s += 0.1
    w += 0.1
    return s / w if w else 0.0


def _seq_sim(tail: List[Dict], hist: List[Dict]) -> float:
    """序列相似度：位置加权（越近越重）"""
    if not tail or len(hist) != len(tail):
        return 0.0
    total, wsum = 0.0, 0.0
    for i, (ta, hb) in enumerate(zip(tail, hist)):
        wgt = (i + 1) / len(tail)  # 尾部事件权重最高
        total += _event_sim(ta, hb) * wgt
        wsum += wgt
    return total / wsum if wsum else 0.0


def detect_repeats(events: List[Dict[str, Any]], window: int = 4,
                   high: float = 0.80, mid: float = 0.62) -> List[Dict[str, Any]]:
    """滑动窗口历史重演识别
    把事件序列末尾 window 个（当前尾）与每个历史窗口比对，
    相似度≥high → 🔴确定性重演；≥mid → 🟡疑似重演。"""
    if len(events) < window + 1:
        return []
    tail = events[-window:]
    hits = []
    for start in range(0, len(events) - window):
        hist = events[start:start + window]
        score = _seq_sim(tail, hist)
        if score >= mid:
            hits.append({
                'score': round(score, 3),
                'level': '🔴' if score >= high else '🟡',
                'matched_window': hist,
                'window_idx': start,
                'era_label': f"{hist[0]['year']} → {hist[-1]['year']}" if hist[0]['year'] else f"第{hist[0]['seq']+1}段",
                'tail_label': f"{tail[0]['year']} → {tail[-1]['year']}" if tail[0]['year'] else f"第{tail[0]['seq']+1}段",
            })
    hits.sort(key=lambda h: -h['score'])
    return hits[:5]


def generate_prophecies(events: List[Dict[str, Any]], repeats: List[Dict[str, Any]],
                        window: int = 4) -> List[Dict[str, Any]]:
    """活：预言——被匹配历史段"接下来发生的事件"即为预言
    当前尾尚未演进到的那一步 → 预判下一步（历史重演的下一步）"""
    prophecies = []
    if len(events) < window + 1:
        return prophecies
    for r in repeats:
        hit_end = r['window_idx'] + window
        if hit_end < len(events):
            nxt = events[hit_end]
            prophecies.append({
                'level': r['level'],
                'confidence': r['score'],
                'matched_era': r['era_label'],
                'title': f"预言：{nxt['type']}·{nxt['title']}",
                'desc': nxt['desc'],
                'gua': nxt['gua'],
                'gz': nxt['gz'],
                'wuxing': nxt['wuxing'],
                'eta_hint': f"历史对应事件于 {nxt['year']} 年（{nxt['gz']}）发生",
            })
    return prophecies


# ─────────────────────────────────────────────
# H武器联动（太极易经推演投影）
# ─────────────────────────────────────────────
_推演维度 = [
    '证据链完整度', '执行可行性', '时机成熟度', '舆论环境',
    '对方反扑能力', '自我保护措施', '历史行为模式', '天时五行',
    '因果链完整度', '盟友支持度', '风险敞口', '资源冗余',
]


def _locate_h_weapon() -> Optional[Path]:
    """动态定位 h_weapon_simulator.py（本地 03_LAYERS / 鲲鹏缺省）"""
    here = Path(__file__).resolve().parent
    candidates = [
        here.parent / '03_LAYERS' / 'L7_数据层' / 'persona_knowledge' / 'P01_诸葛亮' / 'h_weapon_simulator.py',
        Path('/opt/longhun-system/03_LAYERS/L7_数据层/persona_knowledge/P01_诸葛亮/h_weapon_simulator.py'),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def _load_h_weapon():
    """加载 H武器引擎（原路径直载，不复制文件）：
    不复制 → __file__ 保持原路径，顶层 parents[4] 的 ROOT 定位正确；
    预注入 sys.modules['lh_hw_sim.yijing_divination'] → 延迟相对导入可解析。
    失败返回 None（走内置降级）。不越权修改人格知识文件。"""
    import importlib.util
    src = _locate_h_weapon()
    if src is None:
        return None
    try:
        mod_name = 'lh_hw_sim'
        # ① 预加载 yijing_divination（父目录），并注册为 lh_hw_sim 的子模块，
        #    使 h_weapon_simulator 内部的 `from .yijing_divination import 河图五行` 能找到
        spec_y = importlib.util.spec_from_file_location(
            mod_name + '.yijing_divination', src.parent / 'yijing_divination.py')
        mod_y = importlib.util.module_from_spec(spec_y)
        mod_y.__package__ = mod_name           # 相对导入需要父包名
        sys.modules[mod_y.__name__] = mod_y
        spec_y.loader.exec_module(mod_y)
        # ② 原路径直载 h_weapon_simulator（__file__ 保持原位 → ROOT 正确）
        spec = importlib.util.spec_from_file_location(mod_name, src)
        mod = importlib.util.module_from_spec(spec)
        mod.__package__ = mod_name             # simulate 内延迟相对导入可解析
        sys.modules[mod_name] = mod
        spec.loader.exec_module(mod)
        return mod
    except Exception:
        return None


def h_weapon_projection(trigger: str) -> Dict[str, Any]:
    """一句话触发推演 → 收敛解。优先复用 H武器引擎，缺省内置轻量16维收敛。"""
    try:
        mod = _load_h_weapon()
        if mod:
            hw = mod.HWeaponSimulator(mod.WeaponConfig(max_dimensions=16, entropy_factor=0.2))
            res = hw.simulate(trigger, _推演维度[:8])
            opt = res.optimal_strategy
            return {
                'engine': 'HWeaponSimulator',
                'trigger': trigger,
                'final_score': opt.final_score,
                'convergence_speed': opt.convergence_speed,
                'dimensions_used': opt.dimensions_used[:8],
                'optimal_strategy': {
                    'path_id': opt.path_id,
                    'final_score': opt.final_score,
                    'is_optimal': opt.is_optimal,
                },
                'wuxing_diagnosis': res.wuxing_diagnosis,
                'execution_timeline': res.execution_timeline[:3],
                'dna': res.dna,
            }
    except Exception:
        pass
    # 内置轻量推演（纯标准库·太极易理收敛）
    seed = int(_sha8(trigger), 16) % 100000
    scores = {}
    for d in _推演维度:
        base = hashlib.sha256(f"{trigger}{d}".encode()).digest()[0] / 255.0 * 10
        scores[d] = max(0.0, min(10.0, base + ((seed + len(d)) % 7 - 3)))
    best_d = max(scores, key=scores.get)
    avg = sum(scores.values()) / len(scores)
    dr = 数字根(sum(ord(c) for c in trigger))
    return {
        'engine': 'builtin-太极收敛',
        'trigger': trigger,
        'final_score': round(avg, 2),
        'convergence_speed': round(1 - (len(scores) - 1) / len(scores), 2),
        'dimensions_used': sorted(scores, key=scores.get, reverse=True)[:8],
        'optimal_strategy': {'path_id': best_d, 'final_score': round(scores[best_d], 2), 'is_optimal': True},
        'wuxing_diagnosis': {'trigger_wuxing': 五行(dr), 'dr': dr},
        'execution_timeline': [f"阶段1·锁定{best_d}", '阶段2·验证', '阶段3·签章'],
        'dna': f"#龍芯⚡️丙午·丙申·戊午·午时·谦-HW-{_sha8(trigger)}",
    }


# ─────────────────────────────────────────────
# 领域数据装载（龍魂史从日历事件实时合并）
# ─────────────────────────────────────────────
def _load_domain_events(domain: str, data_dir: Optional[Path]) -> List[Dict[str, Any]]:
    """装载领域事件：种子 + （龍魂史）日历事件合并"""
    cfg = DOMAINS[domain]
    raw = list(cfg['seed_events'])
    if domain == 'longhun' and data_dir:
        events_file = data_dir / 'events.json'
        if events_file.exists():
            try:
                d = json.loads(events_file.read_text(encoding='utf-8'))
                for e in d.get('events', []):
                    try:
                        ts = datetime.fromisoformat(e.get('created_at', '').replace('Z', '+00:00'))
                        raw.append((ts.year, ts.month, ts.day, e.get('level') or '变革',
                                    e.get('title') or '事件', (e.get('desc') or '')[:60]))
                    except Exception:
                        continue
            except Exception:
                pass
    raw.sort(key=lambda x: (x[0], x[1], x[2]))
    return [_encode_raw(e, i) for i, e in enumerate(raw)]


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────
def cmd_scan(data_dir: Optional[Path], out_dir: Optional[Path], domain_sel: str, quiet: bool = False) -> None:
    out_dir = out_dir or Path('www')
    out_dir.mkdir(parents=True, exist_ok=True)
    domains = list(DOMAINS) if domain_sel in ('all', '') else [d.strip() for d in domain_sel.split(',') if d.strip() in DOMAINS]
    gene_all = {'generated_at': datetime.now().isoformat(timespec='seconds'),
                'engine': 'lh_civilization_map v1.0', 'domains': {}}
    prophecies_all = {'generated_at': gene_all['generated_at'], 'prophecies': []}
    for dom in domains:
        events = _load_domain_events(dom, data_dir)
        repeats = detect_repeats(events)
        props = generate_prophecies(events, repeats)
        gene_all['domains'][dom] = {
            'name': DOMAINS[dom]['name'],
            'desc': DOMAINS[dom]['desc'],
            'total_events': len(events),
            'windows_checked': max(0, len(events) - 4),
            'repeats': repeats,
            'event_chain': [
                {'seq': e['seq'], 'gz': e['gz'], 'gua': e['gua'], 'wuxing': e['wuxing'],
                 'type': e['type'], 'title': e['title']}
                for e in events[-12:]  # 最近12个事件链
            ],
        }
        for p in props:
            p['domain'] = dom
            p['domain_name'] = DOMAINS[dom]['name']
            prophecies_all['prophecies'].append(p)
    (out_dir / 'gene-map.json').write_text(
        json.dumps(gene_all, ensure_ascii=False, indent=2), encoding='utf-8')
    (out_dir / 'prophecy.json').write_text(
        json.dumps(prophecies_all, ensure_ascii=False, indent=2), encoding='utf-8')
    if not quiet:
        print(f"✅ 图谱已生成 → {out_dir}/gene-map.json · prophecy.json")
        print(f"   领域 {len(domains)} 个 · 重演 {sum(len(g['repeats']) for g in gene_all['domains'].values())} 处 · 预言 {len(prophecies_all['prophecies'])} 条")
    # H武器推演投影（取龍魂史最新事件为触发词）
    if 'longhun' in gene_all['domains'] and gene_all['domains']['longhun']['event_chain']:
        last = gene_all['domains']['longhun']['event_chain'][-1]
        trigger = f"{last['title']}（{last['gz']}·{last['gua']}卦·{last['wuxing']}）"
        hw = h_weapon_projection(trigger)
        hw['generated_at'] = gene_all['generated_at']
        (out_dir / 'h-weapon.json').write_text(
            json.dumps(hw, ensure_ascii=False, indent=2), encoding='utf-8')
        if not quiet:
            print(f"✅ H武器投影 → {out_dir}/h-weapon.json · 收敛分 {hw['final_score']}")


def cmd_domains() -> None:
    for k, v in DOMAINS.items():
        print(f"  {k:12s} {v['name']:<10s} {v['desc']}")


def main() -> int:
    import argparse
    p = argparse.ArgumentParser(description='🐉 龍魂·文明基因图谱引擎 v1.0')
    sub = p.add_subparsers(dest='cmd')
    s = sub.add_parser('scan', help='重建图谱+预言+H武器投影')
    s.add_argument('--data-dir', default=None, help='日历事件目录（龍魂史领域合并用）')
    s.add_argument('--out', default='www', help='输出目录')
    s.add_argument('--domain', default='all', help='领域: all 或逗号分隔')
    s.add_argument('--quiet', action='store_true', help='抑制输出（cron 环境）')
    sub.add_parser('domains', help='列出领域')
    args = p.parse_args()
    if args.cmd == 'scan':
        data_dir = Path(args.data_dir) if args.data_dir else None
        if data_dir and not data_dir.exists():
            print(f"⚠️ data-dir 不存在: {data_dir}，仅用种子事件")
            data_dir = None
        cmd_scan(data_dir, Path(args.out), args.domain, args.quiet)
    elif args.cmd == 'domains':
        cmd_domains()
    else:
        p.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
