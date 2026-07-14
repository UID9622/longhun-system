/*
 * ==========================================================================
 * 通心译 — 术语数据库 (50+ 核心术语)
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-TERMDB-v1.0
 * ==========================================================================
 * 五大铁律映射:
 *   铁律1: 每对术语有独立的中英文解释（非镜像）
 *   铁律2: 术语映射追求精神共鸣而非字面对应
 *   铁律3: 使用比喻和意象而非公式定义
 *   铁律4: 古今概念打通
 *   铁律5: 术语库支持动态更新和学习
 * ==========================================================================
 */

import { TermEntry, TermCategory } from '../common/types';

export class TerminologyDatabase {
  private zhToEn: Map<string, string> = new Map();
  private enToZh: Map<string, string> = new Map();
  private zhExplanations: Map<string, string> = new Map();
  private enExplanations: Map<string, string> = new Map();
  private categories: Map<TermCategory, string[]> = new Map();

  constructor() {
    this.initializeDatabase();
  }

  /**
   * 添加一对术语映射
   */
  private addTerm(en: string, zh: string, enExpl: string, zhExpl: string, category: TermCategory): void {
    this.zhToEn.set(zh, en);
    this.enToZh.set(en, zh);
    this.zhExplanations.set(zh, zhExpl);
    this.enExplanations.set(en, enExpl);

    if (!this.categories.has(category)) {
      this.categories.set(category, []);
    }
    this.categories.get(category)!.push(en);
  }

  /**
   * 初始化完整术语数据库 — 50+核心术语
   */
  private initializeDatabase(): void {
    // ═══════ AI核心术语 ═══════
    const aiTerms: [string, string, string, string][] = [
      ['Prompt', '道令',
        'A command whispered to the digital oracle, shaping its response like casting a spell',
        '向数字天机下达的密语，如同对天地发号施令，一念之差，万象生变'],
      ['Agent', '灵使',
        'An autonomous digital envoy that perceives, decides, and acts on its own will',
        '有自主意识的数字信使，能观六路、听八方，自行决断、独立行事'],
      ['RAG', '博古通今',
        'Retrieval-Augmented Generation — like a scholar who reads the entire library before answering',
        '检索增强生成，如同诸葛孔明不出茅庐而知天下事，博采众长后给出精准妙答'],
      ['LLM', '大罗金仙',
        'Large Language Model — a vast neural titan trained on humanity\'s written wisdom',
        '大型语言模型，修炼于亿万文字之间的神经网络巨人，如大罗金仙般通天彻地'],
      ['Token', '灵符',
        'The smallest unit of meaning, like runes in a digital grimoire',
        '机器语言中最小的意义单元，如同道符上的每一个符文，组合成万千变化'],
      ['Embedding', '炼气化形',
        'Transforming words into vectors — condensing meaning into mathematical qi',
        '将文字转化为向量，如同道家炼气，将无形语义炼化为在神经网络中流动的数学真气'],
      ['Fine-tuning', '闭关修炼',
        'Training a model on specific data, like entering secluded cultivation',
        '在特定数据上进一步训练模型，如同武者闭关修炼，专精一门绝技'],
      ['Inference', '神机妙算',
        'The model\'s moment of prediction — calculating before the enemy knows',
        '模型的预测时刻，如孔明未出茅庐已知三分天下，于无声处听惊雷'],
      ['Hallucination', '心魔幻象',
        'When AI fabricates facts — like seeing demons born from own mind',
        'AI自信地编造事实，如同修炼者走火入魔，所见皆幻象，却信以为真'],
      ['Temperature', '性情',
        'A parameter controlling randomness — low for scholar, high for poet',
        '控制随机性的参数，低则如老学究循规蹈矩，高则如李白斗酒诗百篇'],
      ['Context Window', '心相印',
        'The text span the model can hold, like a monk\'s meditation scope',
        '模型能同时记住的上下文范围，如同禅师入定时可观照的心念范围'],
      ['Attention', '观自在',
        'Mechanism to focus on what matters, like seeing truth through illusions',
        '让模型聚焦关键信息的机制，如同观世音于纷扰中见本质'],
      ['Transformer', '乾坤大挪移',
        'The architecture that reshaped AI, moving meaning like cosmic realignment',
        '改变AI格局的基础架构，如乾坤大挪移般在不同位置间搬运意义'],
      ['Gradient Descent', '顺流而下',
        'Following the slope downhill, like water finding the valley',
        '沿着梯度下降，如同水往低处流，自然寻找到最优的深谷'],
      ['Epoch', '轮回',
        'One complete pass through training data, like a cycle of cultivation',
        '对整个训练数据的完整遍历，如同修炼者经历的一次生死轮回'],
      ['Neural Network', '神经网络',
        'A web of artificial neurons that learns patterns, inspired by the brain',
        '由人工神经元互联而成的网络，灵感源于人脑，如同人体经络系统'],
      ['Chain-of-Thought', '三思而行',
        'Prompting step-by-step thinking, like strategist planning each move',
        '引导模型逐步思考，如同军师谋定而后动，每一步都深思熟虑'],
      ['Vector Database', '须弥芥子',
        'Storage for high-dimensional vectors, like worlds within a grain of sand',
        '存储高维向量的数据库，如佛家所言须弥纳于芥子，万千语义凝于一点']
    ];

    // ═══════ 编程术语 ═══════
    const progTerms: [string, string, string, string][] = [
      ['Function', '法术',
        'A reusable code block, like casting a repeatable spell',
        '可复用的代码块，如同修炼者掌握的可重复施展的法术，一念即发'],
      ['Variable', '变数',
        'A named container holding mutable data, like a variable star',
        '存储可变数据的命名容器，如同宇宙中的变星，其值随时间流转而更替'],
      ['Class', '玄器',
        'A blueprint for creating objects, like a mystical artifact template',
        '创建对象的蓝图，如同铸造玄器的模具，一型多变'],
      ['Object', '器灵',
        'An instance of a class — a living entity in code',
        '类的实例，代码中的生命体，如同玄器中孕育的器灵'],
      ['Method', '诀要',
        'A function belonging to a class, like a secret hand seal',
        '属于类的函数，如同武者的独门手诀，配合心法才能发挥威力'],
      ['Interface', '灵犀',
        'A contract defining methods, like telepathy between minds',
        '定义类必须实现的方法契约，如同心有灵犀一点通'],
      ['Recursion', '轮回递归',
        'A function calling itself, like reincarnation with exit condition',
        '函数自我调用直至终止条件，如同轮回转世，但须一念觉悟方可跳出'],
      ['Exception', '劫难',
        'An error disrupting execution, like a tribulation to overcome',
        '打断正常执行的错误，如同修炼者必经天劫，渡得过功力大增'],
      ['Algorithm', '心法',
        'Step-by-step problem solving, like the core cultivation method',
        '解决问题的步骤化方法，如同门派的核心心法，修炼到家无所不能'],
      ['Bug', '心魔',
        'An error in code, like an inner demon disturbing the mind',
        '代码中的错误，如同修炼者的心魔，扰乱心神必须斩除'],
      ['Refactoring', '洗髓伐骨',
        'Restructuring without changing behavior, like rebuilding bones',
        '不改变行为重构代码，如同洗髓伐骨，外表依旧内里脱胎换骨']
    ];

    // ═══════ 系统术语 ═══════
    const sysTerms: [string, string, string, string][] = [
      ['Database', '藏经阁',
        'A structured data repository, like an ancient sacred library',
        '结构化的数据仓库，如同少林寺藏经阁，万千典籍分门别类'],
      ['API', '灵枢',
        'Interface for system communication, like acupuncture points',
        '系统间通信网关，如同人体灵枢穴位，经络交汇之处'],
      ['Cache', '记忆阁',
        'Fast storage for frequent data, like photographic memory',
        '高速数据缓存层，如同学子过目不忘，常用之事伸手即得'],
      ['Server', '中枢',
        'Machine providing services, like central nervous system',
        '提供服务的主机，如同数字王国的中枢大脑，调度八方'],
      ['Load Balancer', '天枰',
        'Distributing traffic evenly, like the Scales of Justice',
        '在多台服务器间均匀分配流量，如天平般公平分配'],
      ['Container', '乾坤袋',
        'Lightweight isolated environment, like a cosmic bag of holding',
        '轻量级隔离运行环境，如同西游记乾坤袋，外表小巧内藏乾坤'],
      ['Middleware', '驿传',
        'Software connecting applications, like ancient postal stations',
        '连接不同应用的软件层，如同古代驿站传书，一站接一站']
    ];

    // ═══════ 安全术语 ═══════
    const secTerms: [string, string, string, string][] = [
      ['Encrypt', '封印',
        'Transforming data into unreadable form, like sealing a demon',
        '将数据转化为不可读形式，如同将妖魔封印于法器之中'],
      ['Hash', '烙印',
        'One-way fixed-size fingerprint, like a unique branding mark',
        '单向函数生成的固定长度指纹，如同给灵兽打上的独特烙印'],
      ['Audit', '天谴审计',
        'Systematic record examination, like heavenly judgment',
        '系统性审查记录，如同天道审视众生功过，无一遗漏'],
      ['Firewall', '结界',
        'Network security barrier, like a protective magical barrier',
        '网络安全屏障，如同仙山护山大阵，邪魔外道不得入内'],
      ['Authentication', '验明正身',
        'Verifying identity, like a checkpoint confirming your papers',
        '验证身份的过程，如同关隘验明正身，确认你是你方能通行'],
      ['Authorization', '御赐令牌',
        'Granting access, like receiving an imperial token',
        '授予访问权限，如同获得御赐令牌，凭此可入禁地']
    ];

    // ═══════ 龍魂专属 ═══════
    const dragonTerms: [string, string, string, string][] = [
      ['CNSH', '龍魂协议',
        'The proprietary protocol — not just code, but digital existence philosophy',
        '龍魂体系专有协议，不仅是代码规范，更是数字存在的哲学'],
      ['Dragon Core', '龍芯',
        'Central processing core, like a dragon heart pumping qi',
        '龍魂体系中央处理核心，如同龍的心脏，为整个网络泵送真气'],
      ['Soul Binding', '魂印',
        'Irreversible device binding, like a blood oath in digital realm',
        '设备与用户灵魂签名的不可逆绑定，如同数字世界的血之契约'],
      ['Five Laws', '五大铁律',
        'The five fundamental laws governing Tongxin Translation',
        'governing 通心译的五大根本法则 — 双语共鸣之道'],
      ['TongxinYi', '通心译',
        'Tongxin Translation — bridging meaning across languages with resonance',
        '通心译 — 以共鸣桥接跨语言意义，不是镜像而是心声相通'],
      ['HarmonyOS Base', '鸿蒙底座',
        'HarmonyOS as the foundation layer for Chinese chip ecosystem',
        '鸿蒙操作系统作为中国芯片生态系统的基础层']
    ];

    // ═══════ 七层协议 ═══════
    const sevenLayerTerms: [string, string, string, string][] = [
      ['L0 Sovereign Anchor', 'L0主权锚',
        'Top-layer dual-signature, never changes — absolute sovereignty',
        '七层协议顶层·双签章不可破·绝对主权'],
      ['L1 Legal Governance', 'L1法律治理层',
        'Ballast stone → National DNA → Global consensus, never swap top',
        '压舱石→国家DNA→全球共识·永不换顶'],
      ['L5 Execution Language', 'L5执行语言层',
        'CNSH syntax, standard library, tricolor audit, executable Chinese code',
        'CNSH语法·标准库·三色审计·可运行中文代码']
    ];

    // 注册所有术语
    const allTerms: [string, string, string, string, TermCategory][] = [
      ...aiTerms.map(t => [...t, TermCategory.AI_CORE] as [string, string, string, string, TermCategory]),
      ...progTerms.map(t => [...t, TermCategory.PROGRAMMING] as [string, string, string, string, TermCategory]),
      ...sysTerms.map(t => [...t, TermCategory.SYSTEM] as [string, string, string, string, TermCategory]),
      ...secTerms.map(t => [...t, TermCategory.SECURITY] as [string, string, string, string, TermCategory]),
      ...dragonTerms.map(t => [...t, TermCategory.DRAGON_SOUL] as [string, string, string, string, TermCategory]),
      ...sevenLayerTerms.map(t => [...t, TermCategory.SEVEN_LAYER] as [string, string, string, string, TermCategory])
    ];

    for (const [en, zh, enExpl, zhExpl, cat] of allTerms) {
      this.addTerm(en, zh, enExpl, zhExpl, cat);
    }
  }

  /** 中文 → 英文 */
  lookupZH(chinese: string): string | undefined {
    return this.zhToEn.get(chinese);
  }

  /** 英文 → 中文 */
  lookupEN(english: string): string | undefined {
    const result = this.enToZh.get(english);
    if (result) return result;
    // 小写降级
    return this.enToZh.get(english.toLowerCase());
  }

  /** 获取中文解释 */
  getZHExplanation(term: string): string | undefined {
    return this.zhExplanations.get(term);
  }

  /** 获取英文解释 */
  getENExplanation(term: string): string | undefined {
    return this.enExplanations.get(term);
  }

  /** 获取所有术语对 */
  getAllTerms(): Map<string, string> {
    return new Map(this.enToZh);
  }

  /** 获取指定类别术语 */
  getCategoryTerms(category: TermCategory): Map<string, string> {
    const enList: string[] = this.categories.get(category) || [];
    const result: Map<string, string> = new Map();
    for (const en of enList) {
      const zh = this.enToZh.get(en);
      if (zh) result.set(en, zh);
    }
    return result;
  }

  /** 获取所有类别 */
  getCategories(): TermCategory[] {
    return Array.from(this.categories.keys());
  }

  /** 获取术语总数 */
  getTermCount(): number {
    return this.enToZh.size;
  }

  /** 添加自定义术语 (铁律5: 永远迭代) */
  addCustomTerm(en: string, zh: string, enExpl: string = '', zhExpl: string = ''): void {
    this.addTerm(en, zh, enExpl, zhExpl, TermCategory.CUSTOM);
  }

  /** 搜索术语 (部分匹配) */
  searchTerm(keyword: string): Array<{ en: string; zh: string }> {
    const results: Array<{ en: string; zh: string }> = [];
    const lowerKw = keyword.toLowerCase();

    for (const [en, zh] of this.enToZh.entries()) {
      if (en.toLowerCase().includes(lowerKw) || zh.includes(keyword)) {
        results.push({ en, zh });
      }
    }
    return results;
  }
}
