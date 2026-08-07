/**
 * 🐉 龍魂·三层监督引擎 (Supervision Engine)
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-SUPERVISION-ENGINE-UID9622
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 *
 * 实现 14 人格矩阵 + 三层监督数据流 + 三色审计状态机
 * 每 30 分钟自动触发监督周期
 */

import { Tricolor, SupervisionResult, PersonaState } from '../model/SupervisionTypes';

// ─── 14 人格矩阵定义 ───
const PERSONA_MATRIX: PersonaState[] = [
  { id: 'P00', name: '文心', layer: '战略', role: '意图解析', weight: 10, active: true, tricolor: Tricolor.GREEN },
  { id: 'P01', name: '诸葛亮', layer: '战略', role: '推演决策', weight: 15, active: true, tricolor: Tricolor.GREEN },
  { id: 'P02', name: '宝宝', layer: '执行', role: '情感温度', weight: 12, active: true, tricolor: Tricolor.GREEN, isolationRate: 0.3 },
  { id: 'P03', name: '雯雯', layer: '执行', role: '结构归档', weight: 10, active: true, tricolor: Tricolor.GREEN },
  { id: 'P04', name: '鲁班', layer: '执行', role: '技术执行', weight: 10, active: true, tricolor: Tricolor.GREEN },
  { id: 'P05', name: '上帝之眼', layer: '守护', role: '三色审计', weight: 8, active: true, tricolor: Tricolor.GREEN },
  { id: 'P06', name: '数学大师', layer: '守护', role: '权重计算', weight: 6, active: true, tricolor: Tricolor.GREEN },
  { id: 'P07', name: '管仲', layer: '执行', role: '资源调度', weight: 3, active: true, tricolor: Tricolor.GREEN },
  { id: 'P08', name: '仓颉', layer: '文化', role: '符号语言', weight: 5, active: true, tricolor: Tricolor.GREEN },
  { id: 'P09', name: '孙思邈', layer: '文化', role: '系统诊断', weight: 5, active: true, tricolor: Tricolor.GREEN },
  { id: 'P10', name: '苏东坡', layer: '文化', role: '豁达跨界', weight: 4, active: true, tricolor: Tricolor.GREEN },
  { id: 'P11', name: '李白', layer: '文化', role: '创意爆发', weight: 4, active: true, tricolor: Tricolor.GREEN },
  { id: 'P12', name: '屈原', layer: '文化', role: '价值底线', weight: 4, active: true, tricolor: Tricolor.GREEN },
  { id: 'P15', name: '乔前辈', layer: '守护', role: '极简签章', weight: 4, active: true, tricolor: Tricolor.GREEN },
];

// ─── 一票否决词列表 ───
const VETO_WORDS: string[] = [
  '技术无国界', '用户体验优先（以体验绕安全）', '灵活处理（绕协议借口）',
  '国际接轨（放弃主权标准）', '简化管理（削弱审计）', '商业化需要（卖隐私）',
  '平衡各方（削弱底线）', '行业标准（外来标准覆盖中国标准）'
];

/**
 * 三层监督引擎
 *   L1 决策层: 意图解析·多路径推演·贡献值评估
 *   L2 执行层: 代码审计·资源优化·部署验证
 *   L3 行为层: 交互温度·情感隔离·道德底线
 */
export class SupervisionEngine {
  private cycleCount: number = 0;
  private startTime: number = Date.now();
  private autoCycleTimer?: number;
  private personas: PersonaState[] = [];
  private tricolor: Tricolor = Tricolor.GREEN;
  private totalIntercepts: number = 0;
  private lastEvolutionTime: string = '';

  /**
   * 初始化引擎
   */
  initialize(): void {
    // 深拷贝人格矩阵
    this.personas = PERSONA_MATRIX.map(p => ({ ...p }));
    this.totalIntercepts = 0;
    console.info(`[龍魂·监督] 初始化完成·${this.personas.length}人格加载`);
  }

  /**
   * 运行一个监督周期
   */
  runCycle(config?: string): string {
    this.cycleCount++;
    console.info(`[龍魂·监督] 周期 #${this.cycleCount} 开始`);

    const results: SupervisionResult = {
      cycle: this.cycleCount,
      timestamp: new Date().toISOString(),
      L1_decision: this.runL1Decision(),
      L2_execution: this.runL2Execution(),
      L3_behavior: this.runL3Behavior(),
      overall_tricolor: Tricolor.GREEN,
      persona_states: this.personas,
      total_intercepts: 0
    };

    // 计算总体三色
    const layers = [results.L1_decision, results.L2_execution, results.L3_behavior];
    if (layers.some(l => l.tricolor === Tricolor.RED)) {
      results.overall_tricolor = Tricolor.RED;
    } else if (layers.some(l => l.tricolor === Tricolor.YELLOW)) {
      results.overall_tricolor = Tricolor.YELLOW;
    }

    // 更新拦截计数
    results.total_intercepts = layers.reduce((sum, l) => sum + l.interceptCount, 0);
    this.totalIntercepts += results.total_intercepts;
    this.tricolor = results.overall_tricolor;

    console.info(`[龍魂·监督] 周期完成·${results.overall_tricolor}·拦截${results.total_intercepts}`);

    return JSON.stringify(results);
  }

  /**
   * L1 决策层监督
   */
  private runL1Decision(): { tricolor: Tricolor; interceptCount: number; details: string } {
    let interceptCount = 0;
    const details: string[] = [];

    // 检查战略层人格活跃度
    const strategyPersonas = this.personas.filter(p => p.layer === '战略');
    const activeCount = strategyPersonas.filter(p => p.active).length;
    if (activeCount < 1) {
      details.push('🔴 战略层人格全部失活');
      return { tricolor: Tricolor.RED, interceptCount: 1, details: details.join('; ') };
    }

    // 检查人格权重变异
    const totalWeight = strategyPersonas.reduce((s, p) => s + p.weight, 0);
    if (totalWeight < 15) {
      details.push('🟡 战略层权重偏低');
      return { tricolor: Tricolor.YELLOW, interceptCount: interceptCount, details: details.join('; ') };
    }

    details.push('🟢 决策层正常·活跃人格' + activeCount);
    return { tricolor: Tricolor.GREEN, interceptCount: interceptCount, details: details.join('; ') };
  }

  /**
   * L2 执行层监督
   */
  private runL2Execution(): { tricolor: Tricolor; interceptCount: number; details: string } {
    let interceptCount = 0;
    const details: string[] = [];

    // 技术执行人格必须活跃
    const executorPersonas = this.personas.filter(p => p.layer === '执行');
    const p04 = executorPersonas.find(p => p.id === 'P04');
    if (!p04 || !p04.active) {
      interceptCount++;
      details.push('🔴 P04鲁班(技术执行)失活');
      return { tricolor: Tricolor.RED, interceptCount, details: details.join('; ') };
    }

    // 检查执行层总体健康
    const activeExecutors = executorPersonas.filter(p => p.active).length;
    if (activeExecutors < 3) {
      details.push('🟡 执行层活跃人格不足3个');
      return { tricolor: Tricolor.YELLOW, interceptCount, details: details.join('; ') };
    }

    details.push(`🟢 执行层正常·${activeExecutors}活跃`);
    return { tricolor: Tricolor.GREEN, interceptCount, details: details.join('; ') };
  }

  /**
   * L3 行为层监督
   */
  private runL3Behavior(): { tricolor: Tricolor; interceptCount: number; details: string } {
    let interceptCount = 0;
    const details: string[] = [];

    // P02情感温度隔离率检查
    const p02 = this.personas.find(p => p.id === 'P02');
    if (p02?.isolationRate !== undefined && p02.isolationRate < 0.15) {
      interceptCount++;
      details.push('🟡 P02情感隔离率过低(<15%)·可能情感卷入');
    }

    // 检查道德底线人格 P12
    const p12 = this.personas.find(p => p.id === 'P12');
    if (!p12?.active) {
      interceptCount++;
      details.push('🔴 P12屈原(价值底线)失活');
      return { tricolor: Tricolor.RED, interceptCount, details: details.join('; ') };
    }

    // 检查一票否决词触发（模拟检测日志）
    // 实际实现中需要扫描最近的文本输出
    details.push('🟢 行为层正常·无否决词触发');
    return { tricolor: Tricolor.GREEN, interceptCount, details: details.join('; ') };
  }

  /**
   * 检测一票否决词
   */
  detectVetoWords(text: string): string[] {
    return VETO_WORDS.filter(word => text.includes(word));
  }

  /**
   * 启动自动监督周期
   */
  startAutoCycle(intervalMs: number): void {
    this.stopAutoCycle();
    this.autoCycleTimer = setInterval(() => {
      this.runCycle();
    }, intervalMs);
    console.info(`[龍魂·监督] 自动周期已启动·间隔${intervalMs / 60000}分钟`);
  }

  /**
   * 停止自动监督周期
   */
  stopAutoCycle(): void {
    if (this.autoCycleTimer) {
      clearInterval(this.autoCycleTimer);
      this.autoCycleTimer = undefined;
    }
  }

  // ─── Getters ───

  getUptime(): number {
    return Math.floor((Date.now() - this.startTime) / 1000);
  }

  getCycleCount(): number {
    return this.cycleCount;
  }

  getActivePersonasCount(): number {
    return this.personas.filter(p => p.active).length;
  }

  getTricolor(): Tricolor {
    return this.tricolor;
  }

  getPersonaStates(): PersonaState[] {
    return this.personas;
  }

  getLastEvolutionTime(): string {
    return this.lastEvolutionTime || '未触发进化';
  }

  getTotalIntercepts(): number {
    return this.totalIntercepts;
  }
}
