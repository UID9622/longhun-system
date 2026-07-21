/*
 * ==========================================================================
 * 龍魂 · 生日提醒主页面 v2.0 · 人格联动增强版
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-BIRTHDAY-PAGE-v2.0
 * ==========================================================================
 * 增强:
 *   1. 人格路由仪表盘 — 切换10个活跃人格
 *   2. 关系层级分组 — 密友/队友/同事/领导/伙伴
 *   3. 情感协议集成 — 每个成员关联情感参数
 *   4. 祝福编辑器 — 5种人格风格实时切换
 *   5. 生肖干支显示 — 农历引擎驱动
 *   6. 数据审计追踪 — DNA签名链
 *   7. 手势操作 — 删除/快速祝福
 */

import { TeamMember, teamState } from '../models/BirthdayModel';
import { BirthdayDetailDialog } from '../components/BirthdayDetailDialog';
import { MemberEditDialog } from '../components/MemberEditDialog';
import { BlessingComposer } from '../components/BlessingComposer';
import { NotificationManager } from '../managers/NotificationManager';
import { BlessingGenerator } from '../engines/BlessingGenerator';
import { PersonaRouter } from '../engines/PersonaRouter';
import { EmotionProtocol } from '../engines/EmotionProtocol';
import {
  PersonaID,
  PERSONA_ROLES,
  RELATIONSHIP_EMOTION_MAP,
  MASTER_DNA,
  MASTER_UID,
  MASTER_NAME,
  CONFIRM_SEAL
} from '../common/types';

@Entry
@Component
struct BirthdayReminderPage {
  @StorageLink('teamState') teamState = teamState;
  @State showAddDialog: boolean = false;
  @State editingMember: TeamMember | null = null;
  @State showDetailDialog: boolean = false;
  @State detailMember: TeamMember | null = null;
  @State showBlessingComposer: boolean = false;
  @State blessingMember: TeamMember | null = null;
  @State selectedTab: number = 0;
  @State showSearch: boolean = false;
  @State showPersonaPanel: boolean = false;

  // ── 人格路由状态 ──
  @State activePersona: PersonaID = PersonaID.BAOBAO;

  private tabs = [
    { label: '全部', icon: '📋' },
    { label: '7天内', icon: '⏰' },
    { label: '今天', icon: '🎂' },
    { label: '本月', icon: '📅' },
    { label: '仪表盘', icon: '🧚' }
  ];

  aboutToAppear() {
    NotificationManager.requestPermission();
    NotificationManager.scheduleAll(this.teamState.members);
  }

  build() {
    Column() {
      // ── 标题栏 ──
      this.HeaderBuilder()

      // ── 今日生日横幅 ──
      if (this.teamState.todayBirthdays.length > 0) {
        this.TodayBanner()
      }

      // ── 人格面板（条件） ──
      if (this.showPersonaPanel) {
        this.PersonaPanel()
      }

      // ── 标签切换 ──
      this.TabBar()

      // ── 搜索 ──
      if (this.showSearch) {
        this.SearchBar()
      }

      // ── 过滤栏 ──
      this.FilterBar()

      // ── 主内容 ──
      if (this.selectedTab === 4) {
        this.DashboardView()
      } else {
        this.MemberListView()
      }

      // ── 底部操作 ──
      this.FooterBar()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  // ═══════════════════════════════════════════════
  // 标题栏
  // ═══════════════════════════════════════════════
  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉')
        .fontSize(24)
        .margin({ right: 6 })

      Column() {
        Text('龍魂生日提醒')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#c41e3a')
        Text(`UID${MASTER_UID} · ${this.teamState.stats.total}人`)
          .fontSize(11)
          .fontColor('#555')
      }
      .alignItems(HorizontalAlign.Start)

      Blank()

      // 人格切换按钮
      Button() {
        Text(PERSONA_ROLES[this.activePersona]?.icon || '🧚')
          .fontSize(18)
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(36).height(36)
      .onClick(() => {
        this.showPersonaPanel = !this.showPersonaPanel;
      })

      // 搜索
      Button() {
        Text(this.showSearch ? '✕' : '🔍')
          .fontSize(16)
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(36).height(36)
      .margin({ left: 6 })
      .onClick(() => {
        this.showSearch = !this.showSearch;
        if (!this.showSearch) this.teamState.searchQuery = '';
      })

      // 添加
      Button() {
        Text('+')
          .fontSize(20)
          .fontColor('#fff')
      }
      .type(ButtonType.Circle)
      .backgroundColor('#c41e3a')
      .width(36).height(36)
      .margin({ left: 6 })
      .onClick(() => {
        this.editingMember = null;
        this.showAddDialog = true;
      })
    }
    .width('100%')
    .height(52)
    .padding({ left: 12, right: 12 })
    .backgroundColor('#1a1a1a')
  }

  // ═══════════════════════════════════════════════
  // 今日生日横幅
  // ═══════════════════════════════════════════════
  @Builder
  TodayBanner() {
    Column() {
      Row() {
        Text('🎂')
          .fontSize(32)
          .margin({ right: 10 })

        Column() {
          Text(`今天 ${this.teamState.todayBirthdays.length} 位同学生日`)
            .fontSize(15).fontWeight(FontWeight.Bold).fontColor('#fff')
          Text(this.teamState.todayBirthdays.map(m => m.name).join('、'))
            .fontSize(12).fontColor('#ffcc00')
            .maxLines(1).textOverflow({ overflow: TextOverflow.Ellipsis })
        }
        .alignItems(HorizontalAlign.Start).layoutWeight(1)

        Button('祝福')
          .fontSize(13).fontColor('#fff')
          .backgroundColor('#c41e3a').borderRadius(14)
          .padding({ left: 14, right: 14 })
          .onClick(() => {
            // 群发送祝福
            const group = BlessingGenerator.generateGroup(this.teamState.todayBirthdays);
            console.info('Group blessing:', group.slice(0, 50));
          })
      }
      .width('100%')
      .padding(14)
    }
    .width('100%')
    .linearGradient({ direction: GradientDirection.Right, colors: [['#2a1010', 0], ['#1a0505', 1]] })
    .border({ width: { bottom: 1 }, color: '#c41e3a' })
  }

  // ═══════════════════════════════════════════════
  // 人格面板
  // ═══════════════════════════════════════════════
  @Builder
  PersonaPanel() {
    Column() {
      Row() {
        Text('当前人格')
          .fontSize(12).fontColor('#888')
        Blank()
        Text(`${PERSONA_ROLES[this.activePersona]?.icon || ''} ${PERSONA_ROLES[this.activePersona]?.name || this.activePersona}`)
          .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
      }
      .width('100%')
      .padding({ left: 12, right: 12, top: 8, bottom: 4 })

      Scroll() {
        Row() {
          ForEach(PersonaRouter.getPersonaDashboard().filter(p => p.active), (p) => {
            Column() {
              Text(p.icon)
                .fontSize(22)
              Text(p.name)
                .fontSize(10)
                .fontColor(this.activePersona === p.persona ? '#c41e3a' : '#888')
                .maxLines(1)
            }
            .width(60)
            .padding(6)
            .backgroundColor(this.activePersona === p.persona ? 'rgba(196,30,58,0.15)' : 'transparent')
            .borderRadius(8)
            .border({ width: this.activePersona === p.persona ? 1 : 0, color: '#c41e3a' })
            .onClick(() => {
              this.activePersona = p.persona;
              this.teamState.switchPersona(p.persona, '用户手动切换');
            })
          })
        }
        .padding({ left: 8, right: 8 })
      }
      .scrollable(ScrollDirection.Horizontal)
      .scrollBar(BarState.Off)

      Divider().color('#333').margin({ top: 8 })
    }
    .width('100%')
    .backgroundColor('#1a1a1a')
  }

  // ═══════════════════════════════════════════════
  // 标签切换
  // ═══════════════════════════════════════════════
  @Builder
  TabBar() {
    Row() {
      ForEach(this.tabs, (tab: {label: string, icon: string}, index: number) => {
        Column() {
          Text(tab.icon)
            .fontSize(16)
          Text(tab.label)
            .fontSize(11)
            .fontWeight(this.selectedTab === index ? FontWeight.Bold : FontWeight.Normal)
            .fontColor(this.selectedTab === index ? '#c41e3a' : '#666')
            .margin({ top: 2 })

          if (this.selectedTab === index) {
            Divider().strokeWidth(2).color('#c41e3a').width(16).margin({ top: 4 })
          }
        }
        .padding({ top: 10, bottom: 8 })
        .layoutWeight(1)
        .onClick(() => { this.selectedTab = index })
      })
    }
    .width('100%')
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // ═══════════════════════════════════════════════
  // 搜索栏
  // ═══════════════════════════════════════════════
  @Builder
  SearchBar() {
    Row() {
      TextInput({ placeholder: '搜索姓名、部门、标签...', text: this.teamState.searchQuery })
        .width('100%').height(38)
        .backgroundColor('#2a2a2a').fontColor('#fff').placeholderColor('#555')
        .borderRadius(8).padding({ left: 12, right: 12 })
        .onChange((v: string) => { this.teamState.searchQuery = v })
    }
    .width('100%')
    .padding({ left: 12, right: 12, top: 6, bottom: 6 })
    .backgroundColor('#1a1a1a')
  }

  // ═══════════════════════════════════════════════
  // 过滤栏
  // ═══════════════════════════════════════════════
  @Builder
  FilterBar() {
    Row() {
      Select(this.teamState.departments.map(d => ({ value: d })))
        .selected(this.teamState.departments.indexOf(this.teamState.filterDepartment))
        .fontColor('#ccc').backgroundColor('#2a2a2a').borderRadius(6)
        .padding({ left: 6, right: 6 })
        .onSelect((index: number) => {
          this.teamState.filterDepartment = this.teamState.departments[index];
        })

      Select([{ value: '按日期' }, { value: '按姓名' }, { value: '按部门' }, { value: '按关系' }])
        .selected(['date', 'name', 'department', 'relationship'].indexOf(this.teamState.sortBy))
        .fontColor('#ccc').backgroundColor('#2a2a2a').borderRadius(6)
        .padding({ left: 6, right: 6 }).margin({ left: 4 })
        .onSelect((index: number) => {
          const sorts: ('date' | 'name' | 'department' | 'relationship')[] = ['date', 'name', 'department', 'relationship'];
          this.teamState.sortBy = sorts[index];
        })
    }
    .width('100%')
    .height(42)
    .padding({ left: 12, right: 12 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // ═══════════════════════════════════════════════
  // 成员列表
  // ═══════════════════════════════════════════════
  @Builder
  MemberListView() {
    let members = this.getFilteredMembers();

    if (members.length === 0) {
      Column() {
        Text('📭')
          .fontSize(48).margin({ bottom: 12 })
        Text('没有找到成员')
          .fontSize(16).fontColor('#666')
        Text('点击右下角 + 添加第一位成员')
          .fontSize(13).fontColor('#444')
      }
      .width('100%').layoutWeight(1)
      .justifyContent(FlexAlign.Center)
    } else {
      List() {
        ForEach(members, (member: TeamMember) => {
          ListItem() {
            this.MemberCard(member)
          }
          .swipeAction({ end: this.DeleteAction(member) })
          .onClick(() => {
            this.detailMember = member;
            this.showDetailDialog = true;
          })
        }, (member: TeamMember) => member.id)
      }
      .width('100%').layoutWeight(1)
      .divider({ strokeWidth: 1, color: '#1a1a1a' })
      .scrollBar(BarState.Auto)
      .edgeEffect(EdgeEffect.Spring)
    }
  }

  // ═══════════════════════════════════════════════
  // 成员卡片
  // ═══════════════════════════════════════════════
  @Builder
  MemberCard(member: TeamMember) {
    Row() {
      // 头像 + 生日标识
      Stack() {
        Column() {
          Text('🎂')
            .fontSize(36)
        }
        .width(44).height(44)
        .borderRadius(22)
        .backgroundColor('#2a2a2a')
        .justifyContent(FlexAlign.Center)

        if (member.isBirthdayToday()) {
          Text('🎉')
            .fontSize(12)
            .position({ x: 30, y: -2 })
        }
      }
      .width(44).height(44)
      .margin({ right: 10 })

      // 信息
      Column() {
        Row() {
          Text(member.name)
            .fontSize(15).fontWeight(FontWeight.Medium).fontColor('#fff')

          if (member.getAge() > 0) {
            Text(`${member.getAge()}岁`)
              .fontSize(11).fontColor('#888')
              .backgroundColor('#2a2a2a').borderRadius(4)
              .padding({ left: 5, right: 5 }).margin({ left: 6 })
          }

          // 关系标签
          Text(member.getRelationshipLabel())
            .fontSize(10).fontColor('#fff')
            .backgroundColor(this.getRelationColor(member.relationship)).borderRadius(3)
            .padding({ left: 4, right: 4 }).margin({ left: 4 })

          Blank()

          const days = member.getDaysUntilBirthday();
          Text(days === 0 ? '今天!' : `${days}天后`)
            .fontSize(12)
            .fontColor(days <= 7 ? '#c41e3a' : '#666')
            .fontWeight(days <= 7 ? FontWeight.Bold : FontWeight.Normal)
        }
        .width('100%')

        Row() {
          Text(`${member.department} · ${member.role}`)
            .fontSize(12).fontColor('#777')
            .maxLines(1).textOverflow({ overflow: TextOverflow.Ellipsis })
            .layoutWeight(1)

          if (member.birthdayType === 'lunar') {
            Text('农历')
              .fontSize(10).fontColor('#ffcc00')
              .backgroundColor('rgba(255,204,0,0.1)').borderRadius(3)
              .padding({ left: 4, right: 4 })
          }

          if (member.zodiacSign && member.zodiacSign !== '未知') {
            Text(member.zodiacSign)
              .fontSize(10).fontColor('#888')
              .margin({ left: 4 })
          }
        }
        .width('100%').margin({ top: 3 })

        // 标签
        if (member.tags.length > 0) {
          Row() {
            ForEach(member.tags.slice(0, 3), (tag: string) => {
              Text(tag)
                .fontSize(10).fontColor('#888')
                .backgroundColor('#1a1a1a').borderRadius(3)
                .padding({ left: 4, right: 4 }).margin({ right: 3 })
            })
          }
          .width('100%').margin({ top: 4 })
        }
      }
      .layoutWeight(1).alignItems(HorizontalAlign.Start)

      // 快速祝福按钮
      Button() {
        Text('💬')
          .fontSize(14)
      }
      .type(ButtonType.Circle)
      .backgroundColor('rgba(196,30,58,0.2)')
      .width(32).height(32)
      .margin({ left: 6 })
      .onClick(() => {
        this.blessingMember = member;
        this.showBlessingComposer = true;
      })
    }
    .width('100%')
    .padding(12)
    .backgroundColor(member.isBirthdayToday() ? 'rgba(196,30,58,0.08)' : '#0a0a0a')
    .borderRadius(6)
    .margin({ left: 8, right: 8, top: 6 })
  }

  // ═══════════════════════════════════════════════
  // 删除操作
  // ═══════════════════════════════════════════════
  @Builder
  DeleteAction(member: TeamMember) {
    Row() {
      Button() {
        Text('删除').fontColor('#fff').fontSize(13)
      }
      .type(ButtonType.Capsule)
      .backgroundColor('#cc0000')
      .width(70).height('100%')
      .onClick(() => {
        AlertDialog.show({
          title: '确认删除',
          message: `确定删除 ${member.name} 吗？此操作不可撤销。`,
          primaryButton: { value: '删除', action: () => { this.teamState.removeMember(member.id) } },
          secondaryButton: { value: '取消', action: () => {} }
        });
      })
    }
    .width(70).height('100%')
  }

  // ═══════════════════════════════════════════════
  // 仪表盘视图
  // ═══════════════════════════════════════════════
  @Builder
  DashboardView() {
    Scroll() {
      Column() {
        // 统计卡片
        this.DashStatCard()

        // 关系分布
        this.DashRelationCard()

        // 人格活跃度
        this.DashPersonaCard()

        // 协议摘要
        this.DashProtocolCard()

        // 审计追踪
        this.DashAuditCard()
      }
      .padding({ left: 12, right: 12, top: 8, bottom: 16 })
    }
    .layoutWeight(1).scrollBar(BarState.Auto)
  }

  @Builder
  DashStatCard() {
    const s = this.teamState.stats;
    Column() {
      Text('📊 团队概览')
        .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        .width('100%').margin({ bottom: 10 })

      Row() {
        this.DashStatItem('总人数', s.total.toString(), '#c41e3a')
        this.DashStatItem('今天生日', s.today.toString(), '#ffcc00')
        this.DashStatItem('7天内', s.week.toString(), '#ff8c42')
        this.DashStatItem('部门数', s.departments.toString(), '#4a90d9')
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceAround)
    }
    .width('100%').padding(12)
    .backgroundColor('#1a1a1a').borderRadius(10)
    .margin({ bottom: 10 })
  }

  @Builder
  DashStatItem(label: string, value: string, color: string) {
    Column() {
      Text(value)
        .fontSize(24).fontWeight(FontWeight.Bold).fontColor(color)
      Text(label)
        .fontSize(11).fontColor('#888').margin({ top: 4 })
    }
    .alignItems(HorizontalAlign.Center)
  }

  @Builder
  DashRelationCard() {
    Column() {
      Text('🔗 关系分布')
        .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        .width('100%').margin({ bottom: 8 })

      const relations = [
        { label: '密友', value: 'close', color: '#ff8c42' },
        { label: '队友', value: 'mate', color: '#ff6b9d' },
        { label: '同事', value: 'regular', color: '#4a90d9' },
        { label: '领导', value: 'leader', color: '#9b59b6' },
        { label: '伙伴', value: 'external', color: '#7f8c8d' }
      ];

      ForEach(relations, (rel) => {
        const count = this.teamState.members.filter(m => m.relationship === rel.value).length;
        const pct = this.teamState.members.length > 0
          ? ((count / this.teamState.members.length) * 100).toFixed(0)
          : '0';
        Row() {
          Text(rel.label).fontSize(12).fontColor('#ccc').width(40)
          Progress({ value: count, total: this.teamState.members.length || 1, type: ProgressType.Linear })
            .layoutWeight(1).color(rel.color).style({ strokeWidth: 6, strokeRadius: 3 })
          Text(`${count}人 (${pct}%)`).fontSize(11).fontColor('#888').margin({ left: 8 }).width(60)
        }
        .width('100%').padding({ top: 3, bottom: 3 })
      })
    }
    .width('100%').padding(12)
    .backgroundColor('#1a1a1a').borderRadius(10)
    .margin({ bottom: 10 })
  }

  @Builder
  DashPersonaCard() {
    Column() {
      Text('🧚 人格活跃度')
        .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        .width('100%').margin({ bottom: 8 })

      Text(`当前人格: ${PERSONA_ROLES[this.activePersona]?.icon || ''} ${PERSONA_ROLES[this.activePersona]?.name || this.activePersona}`)
        .fontSize(13).fontColor('#ccc').width('100%').margin({ bottom: 6 })

      Text(`职责: ${PERSONA_ROLES[this.activePersona]?.responsibilities?.join(' · ') || ''}`)
        .fontSize(11).fontColor('#888').width('100%').margin({ bottom: 6 })

      Row() {
        ForEach(PersonaRouter.getAllActivePersonaIds(), (p: PersonaID) => {
          Column() {
            Text(PERSONA_ROLES[p]?.icon || '🤖').fontSize(20)
            Text(PERSONA_ROLES[p]?.name || p)
              .fontSize(9).fontColor(p === this.activePersona ? '#c41e3a' : '#666')
              .maxLines(1)
          }
          .padding(4)
          .onClick(() => { this.activePersona = p; })
        })
      }
      .width('100%')
    }
    .width('100%').padding(12)
    .backgroundColor('#1a1a1a').borderRadius(10)
    .margin({ bottom: 10 })
  }

  @Builder
  DashProtocolCard() {
    Column() {
      Text('⚖️ 情感协议状态')
        .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        .width('100%').margin({ bottom: 6 })

      Text(EmotionProtocol.getProtocolSummary())
        .fontSize(11).fontColor('#666').lineHeight(18)
    }
    .width('100%').padding(12)
    .backgroundColor('#1a1a1a').borderRadius(10)
    .margin({ bottom: 10 })
  }

  @Builder
  DashAuditCard() {
    Column() {
      Text('🔒 操作追踪')
        .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        .width('100%').margin({ bottom: 6 })

      if (this.teamState.dnaChain.length === 0) {
        Text('暂无操作记录')
          .fontSize(12).fontColor('#555')
      } else {
        ForEach(this.teamState.dnaChain.slice(-10).reverse(), (dna: string) => {
          Text(dna)
            .fontSize(10).fontColor('#444').fontFamily('monospace')
            .width('100%').padding({ top: 2, bottom: 2 })
        })
      }
    }
    .width('100%').padding(12)
    .backgroundColor('#1a1a1a').borderRadius(10)
  }

  // ═══════════════════════════════════════════════
  // 底部操作栏
  // ═══════════════════════════════════════════════
  @Builder
  FooterBar() {
    Row() {
      Button('导入')
        .fontSize(13).fontColor('#ccc')
        .backgroundColor('#1a1a1a').border({ width: 1, color: '#444' })
        .borderRadius(6).padding({ left: 14, right: 14 })

      Button('导出')
        .fontSize(13).fontColor('#ccc')
        .backgroundColor('#1a1a1a').border({ width: 1, color: '#444' })
        .borderRadius(6).padding({ left: 14, right: 14 })

      Button('通知测试')
        .fontSize(13).fontColor('#fff')
        .backgroundColor('#2a2a2a').borderRadius(6).padding({ left: 14, right: 14 })
        .onClick(() => { NotificationManager.sendTestNotification() })

      Button('刷新提醒')
        .fontSize(13).fontColor('#fff')
        .backgroundColor('#c41e3a').borderRadius(6).padding({ left: 14, right: 14 })
        .onClick(() => {
          NotificationManager.cancelAll();
          NotificationManager.scheduleAll(this.teamState.members);
        })
    }
    .width('100%')
    .height(48)
    .padding({ left: 8, right: 8 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
    .justifyContent(FlexAlign.SpaceAround)
  }

  // ── 辅助 ──
  private getFilteredMembers(): TeamMember[] {
    switch (this.selectedTab) {
      case 0: return this.teamState.filteredMembers;
      case 1: return this.teamState.upcomingBirthdays;
      case 2: return this.teamState.todayBirthdays;
      case 3: return this.teamState.thisMonthBirthdays;
      default: return this.teamState.filteredMembers;
    }
  }

  private getRelationColor(rel: string): string {
    const colors: Record<string, string> = {
      'close': '#ff8c42', 'mate': '#ff6b9d', 'regular': '#4a90d9',
      'leader': '#9b59b6', 'external': '#7f8c8d'
    };
    return colors[rel] || '#666';
  }
}
