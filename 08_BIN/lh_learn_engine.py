# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·癸丑·戊午·䷨损-LH-LEARN-ENGINE-V1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂 · 学习协作引擎 v1.0
=========================
老大说「学 XX」不再由 AI 单方面填内容，而是走五步协作流水线：

  ① 缺口审计(P05·三色)  → 系统在主题下已有什么 / 缺什么 / 薄弱在哪
  ② 推荐补什么(P01)     → 按优先级推荐要补的知识卡·文章·组件·文档
  ③ 人格分配写作(P00)   → 按内容类型把产出任务分给对应人格(20人格矩阵)
  ④ 左右互搏(保守者vs探索者) → 对关键产出双人格互审
  ⑤ P15签章 + 图谱注入 + 认知索引刷新 → 产出真正长进系统

用法:
  lh learn "鸿蒙开发"            # 全流程: 缺口审计→推荐→人格分配→学习卡→图谱注入
  lh learn "AI模型" --gaps       # 只审计缺口(三色标注)
  lh learn "AI模型" --assign     # 只出人格分配表
  lh learn "AI模型" --duel       # 对已有学习卡跑左右互搏(保守者vs探索者)
  lh learn "AI模型" --audit      # 对已有学习卡跑三色审计
  lh learn --list                # 列出已生成的学习卡
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KG_PATH = os.path.join(ROOT, "data", "knowledge_graph.json")
INDEX_PATH = os.path.expanduser("~/.longhun/cognitive_index.json")
LEARN_DIR = os.path.join(ROOT, "03_KNOWLEDGE_GRAPH", "learn")
KG_SCRIPT = os.path.join(ROOT, "bin", "lh_knowledge_graph.py")
DUAL_SCRIPT = os.path.join(ROOT, "bin", "lh_dual_audit_engine.py")
COLOR_SCRIPT = os.path.join(ROOT, "bin", "lh_three_color_audit.py")
SIGN_SCRIPT = os.path.join(ROOT, "bin", "lh_gpg_sign.py")

# ============ 人格写作分配矩阵（20人格·按内容类型路由） ============
PERSONA_MATRIX = [
    # (内容类型关键词, 人格ID, 人格名, 产出类型, 写作提示词)
    (["技术", "组件", "实现", "代码", "架构", "开发", "工程", "后端", "前端", "鸿蒙", "Android", "iOS"],
     "P04", "鲁班", "技术实现文档/组件清单",
     "写可执行的技术落地稿: 组件清单·实现要点·关键代码·验收标准，直接能照着做"),
    (["文化", "创作", "文章", "故事", "灵感", "创意", "文案"],
     "P11", "李白", "文化创作/文章",
     "写有温度的文化创作稿: 主题立意·文章框架·金句·可发布到CSDN"),
    (["分析", "推演", "评估", "策略", "方案", "决策", "博弈", "战略"],
     "P01", "诸葛亮", "分析推演报告",
     "写多路径推演稿: 现状→路径→优劣势→推荐决策·附风险提示"),
    (["教学", "白话", "科普", "新手", "入门", "解释", "学习"],
     "P02", "宝宝", "教学讲解稿",
     "写白话教学稿: 术语旁边跟人话注释·由浅入深·带类比"),
    (["命名", "术语", "符号", "翻译", "桥接"],
     "P08", "仓颉", "术语命名规范",
     "写术语桥接稿: CNSH命名规范校验·术语翻译·名词对照表"),
    (["诊断", "健康", "体检", "检查", "治理"],
     "P09", "孙思邈", "诊断检查单",
     "写系统诊断稿: 治未病检查·健康评估·风险清单"),
    (["计算", "权重", "数字", "算法", "数学", "数据"],
     "P06", "数学大师", "计算建模稿",
     "写计算建模稿: 公式·权重·数字根验证·镜像审计"),
    (["经济", "成本", "预算", "价值", "商业", "盈利"],
     "P07", "管仲", "经济分析稿",
     "写经济可行性稿: 成本核算·ROI·资源配置建议"),
    (["部署", "上线", "发布", "运维", "服务器"],
     "P14", "吕蒙", "部署运维稿",
     "写部署执行稿: 步骤·命令·回滚方案·健康检查"),
    (["合规", "底线", "原则", "法律", "伦理", "红线"],
     "P12", "屈原", "合规底线审查稿",
     "写底线审查稿: 六誓验证·红线清单·不可破原则"),
    (["归档", "整理", "结构", "索引", "图谱", "知识"],
     "P03", "雯雯", "结构化归档稿",
     "写结构归档稿: 四签验证·德字闸·知识入库清单"),
    (["安全", "审计", "漏洞", "风险", "渗透", "防御"],
     "P05", "上帝之眼", "安全审计报告",
     "写安全审计稿: 三色审计·十闸口·风险分级"),
]
# 无匹配时默认: 通用写作 → P11李白(创意) + P03雯雯(归档)
DEFAULT_PERSONA = ("P11", "李白")

# 一票否决词（缺口审计时发现产出触碰即标 🔴）
VETO_WORDS = ["技术无国界", "用户体验优先", "灵活处理", "国际接轨", "简化管理",
              "商业化需要", "平衡各方", "行业标准"]


# ============ ① 缺口审计（P05·三色） ============
def load_kg_entities():
    try:
        with io.open(KG_PATH, "r", encoding="utf-8") as f:
            d = json.load(f)
        return d.get("entities", {})
    except Exception:
        return {}


def load_index_keys():
    try:
        with io.open(INDEX_PATH, "r", encoding="utf-8") as f:
            d = json.load(f)
        keys = set()
        for cat in ("docs", "tools", "functions", "protocols", "custom"):
            v = d.get(cat)
            if isinstance(v, dict):
                keys.update(v.keys())
            elif isinstance(v, list):
                keys.update(str(x) for x in v)
        return keys
    except Exception:
        return set()


def grams(text):
    """中文 2-gram + 英文单词分词"""
    out = set()
    for w in re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z][a-zA-Z0-9_.]+', text):
        wl = w.lower()
        out.add(wl)
        if re.match(r'^[\u4e00-\u9fff]+$', w) and len(w) >= 2:
            for i in range(len(w) - 1):
                out.add(w[i:i + 2])
    return out


def gap_audit(topic):
    """扫描知识图谱+认知索引+知识域文件 → 返回 (已覆盖, 薄弱, 缺失, 红线)"""
    t_grams = grams(topic)
    covered, weak, missing = [], [], []
    reds = []
    # 红线词预检
    for w in VETO_WORDS:
        if w in topic:
            reds.append(w)
    # 1) 知识图谱
    entities = load_kg_entities()
    for eid, ent in entities.items():
        name = ent.get("name", "")
        name_grams = grams(name)
        hit = t_grams & name_grams
        if hit:
            covered.append(f"图谱·{name}（{ent.get('type', '')}）")
    # 2) 认知索引
    idx_keys = load_index_keys()
    for k in idx_keys:
        if t_grams & grams(k):
            covered.append(f"索引·{k}")
    # 3) 知识域文件（03_KNOWLEDGE_GRAPH/*.md 文件名+首行）
    try:
        for fn in sorted(os.listdir(os.path.join(ROOT, "03_KNOWLEDGE_GRAPH"))):
            if not fn.endswith(".md"):
                continue
            if t_grams & grams(fn):
                covered.append(f"知识域·{fn}")
    except Exception:
        pass
    # 4) 已生成学习卡（learn 目录）→ 命中说明该主题已学过
    learned = []
    try:
        for fn in sorted(os.listdir(LEARN_DIR)):
            if fn.endswith(".md") and (t_grams & grams(fn)):
                learned.append(fn)
    except Exception:
        pass
    # 去重
    covered = sorted(set(covered))
    return covered, weak, missing, reds, learned


# ============ ③ 人格分配（P00 路由） ============
def assign_personas(topic):
    """按内容类型关键词匹配人格 → 返回分配任务列表"""
    t = topic.lower()
    matched = []
    for keywords, pid, pname, ptype, prompt in PERSONA_MATRIX:
        if any(k.lower() in t for k in keywords):
            matched.append((pid, pname, ptype, prompt))
    # 去重(同一人格只领一个任务)
    seen, tasks = set(), []
    for pid, pname, ptype, prompt in matched:
        if pid not in seen:
            seen.add(pid)
            tasks.append({"persona": pid, "name": pname, "type": ptype, "prompt": prompt})
    if not tasks:
        # 词义兜底: 按主题特征智能选默认人格
        if re.search(r'模型|算法|AI|数据|算力|智能', t):
            pid, pname, ptype, prompt = ("P06", "数学大师", "计算建模稿",
                                         "写计算建模稿: 公式·权重·数字根验证·架构推演·可落地路径")
        elif re.search(r'文|章|记|故事|诗', t):
            pid, pname, ptype, prompt = ("P11", "李白", "文化创作稿",
                                         "写有温度的文化创作稿: 立意·框架·金句·可发布")
        elif re.search(r'系统|服务|平台|架构', t):
            pid, pname, ptype, prompt = ("P04", "鲁班", "技术实现稿",
                                         "写可执行的技术落地稿: 组件清单·实现要点·验收标准")
        else:
            pid, pname = DEFAULT_PERSONA
            ptype, prompt = "通用创作稿", f"围绕「{topic}」写可落地的创作稿，附知识卡+行动项"
        tasks.append({"persona": pid, "name": pname, "type": ptype, "prompt": prompt})
    # 补充审计/归档/签章人格（协作链固定班底）
    tasks.append({"persona": "P05", "name": "上帝之眼", "type": "三色审计",
                  "prompt": "对全部产出跑三色审计+十闸口，标🟢🟡🔴"})
    tasks.append({"persona": "P03", "name": "雯雯", "type": "结构化归档",
                  "prompt": "四签验证·知识入库·图谱注入"})
    tasks.append({"persona": "P15", "name": "乔前辈", "type": "签章验收",
                  "prompt": "DNA盖章·GPG签名·交付验收"})
    return tasks


# ============ ④ 左右互搏（保守者 vs 探索者） ============
def run_duel(topic, solution_path=None):
    """对学习主题/产出跑左右互搏，返回裁决文本"""
    problem = {"topic": topic,
               "context": "系统学习缺口审计后，需要补充该主题内容",
               "conservative": "保守者视角: 是否真的缺? 现有体系是否已覆盖? 补了会不会冗余/冲突?",
               "explorer": "探索者视角: 缺口在哪? 最优补法是什么? 该主题能否联动其他引擎?"}
    solution = {"proposal": f"按人格分配矩阵协作产出「{topic}」知识卡并注入图谱",
                "fallback": "若互搏判冗余则降级为仅索引标注"}
    p = os.path.join(LEARN_DIR, f"_duel_problem_{datetime.now().strftime('%H%M%S')}.json")
    s = os.path.join(LEARN_DIR, f"_duel_solution_{datetime.now().strftime('%H%M%S')}.json")
    report = os.path.join(LEARN_DIR, f"左右互搏_{topic[:8]}_{datetime.now().strftime('%Y%m%d')}.md")
    try:
        os.makedirs(LEARN_DIR, exist_ok=True)
        with io.open(p, "w", encoding="utf-8") as f:
            json.dump(problem, f, ensure_ascii=False)
        with io.open(s, "w", encoding="utf-8") as f:
            json.dump(solution, f, ensure_ascii=False)
        r = subprocess.run([sys.executable, DUAL_SCRIPT, "duel", "-p", p, "-s", s, "-o", report],
                           capture_output=True, text=True, cwd=ROOT, timeout=60)
        verdict = "🟡 左右互搏已执行（详见报告）"
        for line in (r.stdout or "").splitlines():
            if "🟢" in line or "🔴" in line or "通过" in line or "驳回" in line:
                verdict = line.strip()
                break
        return verdict, report, r.returncode
    except Exception as e:
        return f"🟡 左右互搏调用失败({e})", "", 1
    finally:
        for tmp in (p, s):
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass


# ============ ⑤ 图谱注入 ============
def inject_kg(topic, card_path, tasks):
    """注入学习主题实体 + 学习卡实体 + 人格分工关系"""
    try:
        with io.open(KG_PATH, "r", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return "🟡 图谱数据读取失败"
    entities = d.setdefault("entities", {})
    eid = "learn_" + re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]', '_', topic)[:40]
    if eid in entities:
        return f"🟡 学习主题「{topic}」已存在图谱（{eid}），跳过重复注入"
    entities[eid] = {"type": "knowledge_topic", "name": f"学习·{topic}",
                     "properties": {"learn_card": card_path, "date": datetime.now().strftime("%Y-%m-%d"),
                                    "personas": ",".join(t["name"] for t in tasks)}}
    with io.open(KG_PATH, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    return f"✅ 图谱注入: {eid}（学习·{topic}）"


# ============ 学习卡生成 ============
def build_card(topic, covered, reds, learned, tasks, duel_verdict):
    now = datetime.now()
    date_s = now.strftime("%Y-%m-%d")
    fname = f"学习协作卡_{topic}_{date_s}.md"
    fpath = os.path.join(LEARN_DIR, fname)
    os.makedirs(LEARN_DIR, exist_ok=True)
    color = "🔴" if reds else ("🟢" if covered else "🟡")
    cover_lines = "\n".join(f"  - {c}" for c in covered[:25]) or "  - （无）"
    red_lines = "\n".join(f"  - 🔴 {w}" for w in reds) or "  - 无"
    learn_lines = "\n".join(f"  - 📚 {f}" for f in learned) or "  - 无"
    task_lines = "\n".join(
        f"  | {t['persona']} {t['name']} | {t['type']} | {t['prompt']} |" for t in tasks)
    md = f"""# 学习协作卡 · {topic} · {date_s}

> DNA: #龍芯⚡️丙午·丙申·{date_s.replace('-','')[-4:]}-LEARN-{re.sub(r'[^\u4e00-\u9fffA-Za-z0-9]', '', topic)[:12]}-V1.0
> 创建者: 诸葛鑫（UID9622）· 学习协作引擎 v1.0
> 协议: CC BY-NC-SA 4.0（思想层）· License: MulanPSL v2（工程层）
> 三色: {color}

---

## ① 缺口审计（P05·三色）{color}
- **已有覆盖**: {len(covered)} 项
{cover_lines}
- **一票否决词预检**:
{red_lines}
- **已学过的卡**:
{learn_lines}
- **审计结论**: {'🔴 触碰红线词，暂停学习，先过 P05 复核' if reds else ('🟢 系统已具备基础，重点做「补强+联动」' if covered else '🟡 系统缺口明显，重点做「从零补全」')}

## ② 推荐补什么（P01）
| 优先级 | 推荐产出 | 理由 |
|:---:|:---|:---|
| {'🔴 停' if reds else 'P0'} | {'红线复核/协议审计' if reds else '知识卡（从零搭建）' if not covered else '补强卡（缺啥补啥）'} | {'触碰P0天条·先审后学' if reds else '系统该主题无覆盖·需建地基' if not covered else '系统已覆盖·按缺口补强+跨域联动'} |
| P1 | 行动清单 | 每张卡带可执行步骤，学完能直接用 |
| P2 | 图谱注入+索引挂载 | 让产出长进系统，说人话就能搜到 |

## ③ 人格分配写作（P00 路由 · 20人格矩阵）
| 人格 | 职能 | 领的任务 |
|:---|:---|:---|
{task_lines}

## ④ 左右互搏（保守者 vs 探索者）
- **裁决**: {duel_verdict}
- 保守者: 是否冗余/冲突；探索者: 最优补法/跨引擎联动 → 双人格互审后再签章

## ⑤ 落地动作（写完后自动执行）
- [ ] 各人格产出落盘（按路径铁律: 知识卡→`03_KNOWLEDGE_GRAPH/learn/`·协议→`01_protocols/`·脚本→`bin/`）
- [ ] P05 三色审计全部产出（`lh three_color`）
- [ ] P15 GPG 签章（`lh_gpg_sign.py sign`）
- [ ] 知识图谱注入 + 认知索引刷新（说「学 {topic}」直接命中）

---
*生成: 龍魂学习协作引擎 v1.0 · {date_s} · 学=审计缺口→人格分工→互搏验收*
"""
    with io.open(fpath, "w", encoding="utf-8") as f:
        f.write(md)
    return fpath


# ============ 主流程 ============
def main():
    parser = argparse.ArgumentParser(description="龍魂·学习协作引擎 v1.0")
    parser.add_argument("topic", nargs="?", default="", help="学习主题")
    parser.add_argument("--gaps", action="store_true", help="只审计缺口(三色)")
    parser.add_argument("--assign", action="store_true", help="只出人格分配表")
    parser.add_argument("--duel", action="store_true", help="只跑左右互搏")
    parser.add_argument("--audit", action="store_true", help="只跑三色审计")
    parser.add_argument("--list", action="store_true", help="列出已生成学习卡")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    if args.list:
        try:
            cards = sorted(f for f in os.listdir(LEARN_DIR) if f.endswith(".md") and not f.startswith("_"))
        except Exception:
            cards = []
        print(f"📚 已生成学习卡 {len(cards)} 张:")
        for c in cards:
            print(f"  - {c}")
        return

    if not args.topic:
        parser.print_help()
        return

    topic = args.topic
    covered, weak, missing, reds, learned = gap_audit(topic)
    tasks = assign_personas(topic)

    if args.json:
        print(json.dumps({"topic": topic, "covered": covered, "reds": reds,
                          "learned": learned, "tasks": tasks}, ensure_ascii=False, indent=1))
        return

    if args.gaps:
        print(f"🔍 缺口审计（P05·三色）: 「{topic}」")
        print(f"  🟢 已有覆盖 {len(covered)} 项:")
        for c in covered[:25]:
            print(f"     - {c}")
        print(f"  🔴 红线词: {reds if reds else '无'}")
        print(f"  📚 已学过: {learned if learned else '无'}")
        print(f"  结论: {'🔴 触碰红线·停' if reds else '🟢 补强' if covered else '🟡 从零补全'}")
        return

    if args.assign:
        print(f"👥 人格分配写作（P00 路由）: 「{topic}」→ {len(tasks)} 个人格")
        for t in tasks:
            print(f"  [{t['persona']} {t['name']}] {t['type']}")
            print(f"     任务: {t['prompt']}")
        return

    if args.duel:
        verdict, report, rc = run_duel(topic)
        print(f"⚔️ 左右互搏: {verdict}")
        if report and os.path.exists(report):
            print(f"   📄 报告: {os.path.relpath(report, ROOT)}")
        return

    if args.audit:
        r = subprocess.run([sys.executable, COLOR_SCRIPT, "audit",
                            "--object", f"学习主题「{topic}」缺口审计",
                            "--type", "学习审计", "--json"],
                           capture_output=True, text=True, cwd=ROOT, timeout=60)
        out = (r.stdout or "") + (r.stderr or "")
        print(out[-800:] if out else "🟡 三色审计执行完毕")
        return

    # ===== 全流程 =====
    print(f"🎓 学习协作引擎 v1.0 · 主题「{topic}」\n")
    # ① 缺口审计
    color = "🔴" if reds else ("🟢" if covered else "🟡")
    print(f"① 缺口审计（P05）{color}: 已有覆盖 {len(covered)} 项"
          + (f" · 红线 {reds}" if reds else ""))
    # ② 推荐
    print(f"② 推荐补什么（P01）: "
          + ("红线复核优先" if reds else "从零补全知识卡" if not covered else "按缺口补强+跨域联动"))
    # ③ 人格分配
    print(f"③ 人格分配（P00）: {len(tasks)} 个人格协作 → "
          + ", ".join(f"[{t['persona']}{t['name']}]" for t in tasks))
    # ④ 左右互搏
    if reds:
        verdict = "🔴 触碰红线词，学习暂停，先过 P05 复核"
        report = ""
    else:
        verdict, report, _ = run_duel(topic)
    print(f"④ 左右互搏: {verdict}")
    # ⑤ 生成学习卡 + 图谱注入
    fpath = build_card(topic, covered, reds, learned, tasks, verdict)
    print(f"⑤ 学习卡生成: {os.path.relpath(fpath, ROOT)}")
    if not reds:
        msg = inject_kg(topic, os.path.relpath(fpath, ROOT), tasks)
        print(f"   {msg}")
    print(f"\n✅ 学「{topic}」流程完成。下一步: 各人格按任务写作 → P05审计 → P15签章 → 说「学 {topic}」即命中")
    # 打开学习卡
    try:
        subprocess.Popen(["open", fpath])
    except Exception:
        pass


if __name__ == "__main__":
    main()
