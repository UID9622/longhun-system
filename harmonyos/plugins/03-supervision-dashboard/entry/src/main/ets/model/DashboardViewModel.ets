/**
 * 🐉 龍魂·DashboardViewModel — 仪表盘状态管理
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-DASHBOARD-VIEWMODEL-UID9622
 */

@Observed
export class DashboardViewModel {
  // 系统状态
  systemStatus: string = '🟢 正常运行';
  uptime: string = '0h 0m';
  supervisionCycle: number = 0;

  // 三层监督
  L1: LayerData = { name: '决策监督', value: 92, color: '#4ADE80', interceptRate: 2.3 };
  L2: LayerData = { name: '执行监督', value: 85, color: '#F4A261', interceptRate: 5.1 };
  L3: LayerData = { name: '行为监督', value: 96, color: '#4ADE80', interceptRate: 1.2 };

  // 人格矩阵
  personas: PersonaData[] = [
    { id: 'P00', name: '文心', role: '意图解析', weight: 10, active: true, health: 98 },
    { id: 'P01', name: '诸葛亮', role: '推演决策', weight: 15, active: true, health: 95 },
    { id: 'P02', name: '宝宝', role: '情感温度', weight: 12, active: true, health: 88 },
    { id: 'P03', name: '雯雯', role: '结构归档', weight: 10, active: true, health: 92 },
    { id: 'P04', name: '鲁班', role: '技术执行', weight: 10, active: true, health: 90 },
    { id: 'P05', name: '上帝之眼', role: '三色审计', weight: 8, active: true, health: 97 },
    { id: 'P06', name: '数学大师', role: '权重计算', weight: 6, active: true, health: 94 },
    { id: 'P07', name: '管仲', role: '资源调度', weight: 3, active: true, health: 85 },
    { id: 'P08', name: '仓颉', role: '符号语言', weight: 5, active: true, health: 91 },
    { id: 'P09', name: '孙思邈', role: '系统诊断', weight: 5, active: true, health: 88 },
    { id: 'P10', name: '苏东坡', role: '豁达跨界', weight: 4, active: true, health: 93 },
    { id: 'P11', name: '李白', role: '创意爆发', weight: 4, active: true, health: 90 },
    { id: 'P12', name: '屈原', role: '价值底线', weight: 4, active: true, health: 99 },
    { id: 'P15', name: '乔前辈', role: '极简签章', weight: 4, active: true, health: 96 },
  ];

  // 审计时间线
  auditEvents: AuditEvent[] = [
    { time: '01:15', event: '监督周期 #42 完成', tricolor: '🟢' },
    { time: '00:45', event: '记忆管理器持久化', tricolor: '🟢' },
    { time: '00:30', event: 'P05上帝之眼触发审计', tricolor: '🟡' },
    { time: '00:15', event: '主权验证全通过', tricolor: '🟢' },
    { time: '00:00', event: '系统启动完成', tricolor: '🟢' },
  ];

  /**
   * 刷新仪表盘数据
   */
  async refresh(): Promise<void> {
    // 模拟刷新
    this.supervisionCycle++;
    this.uptime = `${Math.floor(this.supervisionCycle / 2)}h ${(this.supervisionCycle * 3) % 60}m`;
    this.L1.value = Math.min(100, this.L1.value + (Math.random() - 0.5) * 4);
    this.L2.value = Math.min(100, this.L2.value + (Math.random() - 0.5) * 6);
    this.L3.value = Math.min(100, this.L3.value + (Math.random() - 0.5) * 3);

    // 更新系统状态
    const avg = (this.L1.value + this.L2.value + this.L3.value) / 3;
    if (avg > 80) this.systemStatus = '🟢 正常运行';
    else if (avg > 60) this.systemStatus = '🟡 注意';
    else this.systemStatus = '🔴 危险';
  }
}

export interface LayerData {
  name: string;
  value: number;
  color: string;
  interceptRate: number;
}

export interface PersonaData {
  id: string;
  name: string;
  role: string;
  weight: number;
  active: boolean;
  health: number;
}

export interface AuditEvent {
  time: string;
  event: string;
  tricolor: string;
}
