// 龍魂 · 印章管理主页面 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️
// UID: 9622

import { Seal, SealType, SealStatus, SealApplication, SealOutRecord, ApprovalLevel, UsageType, SealState, sealState, SealStats, AlertItem } from '../models/SealModel';
import { SealDetailDialog } from '../components/SealDetailDialog';
import { ApplicationDialog } from '../components/ApplicationDialog';
import { ApprovalDialog } from '../components/ApprovalDialog';
import { ExecuteDialog } from '../components/ExecuteDialog';
import { OutRecordDialog } from '../components/OutRecordDialog';
import { AlertBanner } from '../components/SealAlertBanner';
import { SealDatabase } from '../database/SealDatabase';

// === 常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";

@Entry
@Component
struct SealRecordPage {
  @StorageLink('sealState') sealState: SealState = sealState;
  @State private selectedTab: number = 0;
  @State private showSealDialog: boolean = false;
  @State private showAppDialog: boolean = false;
  @State private showApprovalDialog: boolean = false;
  @State private showExecuteDialog: boolean = false;
  @State private showOutDialog: boolean = false;
  @State private editingSeal: Seal | null = null;
  @State private editingApp: SealApplication | null = null;
  @State private showSearch: boolean = false;
  @State private searchText: string = '';
  @State private showAlerts: boolean = false;
  @State private scanMode: boolean = false;

  private sealDetailController: CustomDialogController | null = null;
  private appDialogController: CustomDialogController | null = null;
  private approvalDialogController: CustomDialogController | null = null;
  private executeDialogController: CustomDialogController | null = null;
  private outDialogController: CustomDialogController | null = null;

  aboutToAppear() {
    this.sealState.load();
    SealDatabase.init(getContext(this));
    this.scheduleAlerts();
  }

  build() {
    Column() {
      // === 顶部标题栏 ===
      this.HeaderBuilder()

      // === 预警横幅 ===
      if (this.getAlertCount() > 0 && !this.showAlerts) {
        this.AlertBannerBuilder()
      }

      // === 预警面板 ===
      if (this.showAlerts) {
        AlertBanner({
          alerts: this.getAllAlerts(),
          onClose: () => { this.showAlerts = false; }
        })
      }

      // === 统计卡片 ===
      this.StatsBuilder()

      // === 标签切换 ===
      this.TabBuilder()

      // === 搜索栏 ===
      if (this.showSearch) {
        this.SearchBuilder()
      }

      // === 内容区 ===
      this.ContentBuilder()

      // === 底部操作栏 ===
      this.FooterBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  // ==================== 标题栏 ====================
  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉')
        .fontSize(28)
        .margin({ right: 8 })

      Column() {
        Text('龍魂印章管理')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor('#c41e3a')

        Text(`UID:${MASTER_UID} · ${this.sealState.seals.length}枚印章`)
          .fontSize(12)
          .fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)

      Blank()

      // 预警按钮
      Badge({
        value: this.getAlertCount().toString(),
        position: BadgePosition.RightTop,
        style: { badgeSize: 18, badgeColor: '#c41e3a' }
      }) {
        Button() {
          Text('🔔')
            .fontSize(20)
        }
        .type(ButtonType.Circle)
        .backgroundColor(this.getAlertCount() > 0 ? 'rgba(196,30,58,0.2)' : '#1a1a1a')
        .width(40)
        .height(40)
        .onClick(() => {
          this.showAlerts = !this.showAlerts;
        })
      }

      // 扫码按钮
      Button() {
        Text('📷')
          .fontSize(20)
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(40)
      .height(40)
      .onClick(() => {
        this.startScan();
      })

      // 搜索按钮
      Button() {
        Text(this.showSearch ? '✕' : '🔍')
          .fontSize(20)
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(40)
      .height(40)
      .onClick(() => {
        this.showSearch = !this.showSearch;
        if (!this.showSearch) {
          this.sealState.searchQuery = '';
        }
      })

      // 添加印章
      Button() {
        Text('+')
          .fontSize(24)
          .fontColor('#fff')
      }
      .type(ButtonType.Circle)
      .backgroundColor('#c41e3a')
      .width(40)
      .height(40)
      .onClick(() => {
        this.editingSeal = null;
        this.showSealDialog = true;
      })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // ==================== 预警横幅 ====================
  @Builder
  AlertBannerBuilder() {
    Row() {
      Text('⚠️')
        .fontSize(24)
        .margin({ right: 8 })

      Column() {
        Text(`${this.getAlertCount()} 条预警待处理`)
          .fontSize(14)
          .fontWeight(FontWeight.Bold)
          .fontColor('#ffcc00')

        Text(this.getAlertPreview())
          .fontSize(12)
          .fontColor('#ffcc00')
          .maxLines(1)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Button('查看')
        .fontSize(12)
        .fontColor('#0a0a0a')
        .backgroundColor('#ffcc00')
        .borderRadius(12)
        .padding({ left: 12, right: 12 })
        .onClick(() => {
          this.showAlerts = true;
        })
    }
    .width('100%')
    .padding(12)
    .backgroundColor('rgba(255,204,0,0.1)')
    .border({ width: { bottom: 1 }, color: 'rgba(255,204,0,0.3)' })
  }

  // ==================== 统计卡片 ====================
  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('印章总数', this.sealState.statistics.totalSeals.toString(), '#fff')
      this.StatCard('在库', this.sealState.statistics.inVault.toString(), '#00ff00')
      this.StatCard('使用中', this.sealState.statistics.inUse.toString(), '#ffcc00')
      this.StatCard('外带', this.sealState.statistics.outside.toString(), '#ff6600')
      this.StatCard('今日用印', this.sealState.statistics.todayExecutions.toString(), '#c41e3a')
    }
    .width('100%')
    .padding({ left: 12, right: 12, top: 12, bottom: 12 })
    .justifyContent(FlexAlign.SpaceAround)
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() {
      Text(value)
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .fontColor(color)

      Text(label)
        .fontSize(11)
        .fontColor('#888')
        .margin({ top: 4 })
    }
    .padding(8)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .width('18%')
  }

  // ==================== 标签切换 ====================
  @Builder
  TabBuilder() {
    Row() {
      ForEach([
        { label: '印章档案', icon: '🔏', count: 0 },
        { label: '用印申请', icon: '📝', count: this.sealState.pendingApprovals.length },
        { label: '执行记录', icon: '✅', count: 0 },
        { label: '外带追踪', icon: '📍', count: this.sealState.activeOutRecords.length }
      ], (item: { label: string; icon: string; count: number }, index: number) => {
        Column() {
          Text(`${item.icon} ${item.label}${item.count > 0 ? `(${item.count})` : ''}`)
            .fontSize(13)
            .fontWeight(this.selectedTab === index ? FontWeight.Bold : FontWeight.Normal)
            .fontColor(this.selectedTab === index ? '#c41e3a' : '#888')

          if (this.selectedTab === index) {
            Divider()
              .strokeWidth(2)
              .color('#c41e3a')
              .width(20)
              .margin({ top: 4 })
          }
        }
        .padding({ top: 12, bottom: 12, left: 16, right: 16 })
        .onClick(() => {
          this.selectedTab = index;
        })
      })
    }
    .width('100%')
    .justifyContent(FlexAlign.SpaceAround)
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // ==================== 搜索栏 ====================
  @Builder
  SearchBuilder() {
    Row() {
      TextInput({ placeholder: '搜索印章/编号/保管人/部门...', text: $$this.searchText })
        .width('100%')
        .height(40)
        .backgroundColor('#2a2a2a')
        .fontColor('#fff')
        .placeholderColor('#666')
        .borderRadius(8)
        .padding({ left: 12, right: 12 })
        .onChange((value: string) => {
          this.sealState.searchQuery = value;
        })
    }
    .width('100%')
    .padding({ left: 16, right: 16, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
  }

  // ==================== 内容区 ====================
  @Builder
  ContentBuilder() {
    if (this.selectedTab === 0) {
      this.SealListBuilder()
    } else if (this.selectedTab === 1) {
      this.ApplicationListBuilder()
    } else if (this.selectedTab === 2) {
      this.RecordListBuilder()
    } else {
      this.OutTrackBuilder()
    }
  }

  // ==================== 印章列表 ====================
  @Builder
  SealListBuilder() {
    List() {
      ForEach(this.sealState.filteredSeals, (seal: Seal) => {
        ListItem() {
          this.SealCardBuilder(seal)
        }
        .swipeAction({ end: this.SealSwipeBuilder(seal) })
        .onClick(() => {
          this.editingSeal = seal;
          this.showSealDialog = true;
        })
      }, (seal: Seal) => seal.id)
    }
    .width('100%')
    .layoutWeight(1)
    .divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto)
    .edgeEffect(EdgeEffect.Spring)
    .padding({ bottom: 16 })
  }

  // ==================== 印章卡片 ====================
  @Builder
  SealCardBuilder(seal: Seal) {
    Row() {
      // 印章图标
      Stack() {
        Column() {
          Text('印')
            .fontSize(20)
            .fontWeight(FontWeight.Bold)
            .fontColor(
              seal.status === SealStatus.IN_VAULT ? '#00ff00' :
              seal.status === SealStatus.IN_USE ? '#ffcc00' :
              seal.status === SealStatus.OUTSIDE ? '#ff6600' :
              seal.status === SealStatus.FROZEN ? '#888' :
              '#ff0000'
            )
        }
        .width(48)
        .height(48)
        .backgroundColor('#2a2a2a')
        .borderRadius(8)
        .justifyContent(FlexAlign.Center)

        // 状态角标
        Text(
          seal.status === SealStatus.IN_VAULT ? '库' :
          seal.status === SealStatus.IN_USE ? '用' :
          seal.status === SealStatus.OUTSIDE ? '外' :
          seal.status === SealStatus.FROZEN ? '冻' : '废'
        )
        .fontSize(9)
        .fontColor('#fff')
        .backgroundColor(
          seal.status === SealStatus.IN_VAULT ? '#00aa00' :
          seal.status === SealStatus.IN_USE ? '#ffaa00' :
          seal.status === SealStatus.OUTSIDE ? '#ff6600' :
          seal.status === SealStatus.FROZEN ? '#666' : '#ff0000'
        )
        .borderRadius(4)
        .padding({ left: 3, right: 3 })
        .position({ x: 32, y: -4 })
      }
      .width(48)
      .height(48)
      .margin({ right: 12 })

      // 信息
      Column() {
        Row() {
          Text(seal.name)
            .fontSize(15)
            .fontWeight(FontWeight.Medium)
            .fontColor('#fff')
            .layoutWeight(1)

          Text(seal.sealNo)
            .fontSize(11)
            .fontColor('#666')
            .fontFamily('monospace')
        }
        .width('100%')

        Row() {
          Text(`${seal.type} · ${seal.material} · ${seal.diameter}mm${seal.shape}`)
            .fontSize(12)
            .fontColor('#888')
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
            .layoutWeight(1)

          Text(`${seal.useCount}次`)
            .fontSize(12)
            .fontColor('#888')
        }
        .width('100%')
        .margin({ top: 4 })

        Row() {
          Text(`👤${seal.custodian}`)
            .fontSize(11)
            .fontColor('#666')

          Text(`📍${seal.vaultLocation}`)
            .fontSize(11)
            .fontColor('#666')
            .margin({ left: 8 })

          Blank()

          // 安全特征
          Row() {
            if (seal.fingerprintLock) {
              Text('🔐')
                .fontSize(12)
                .margin({ right: 4 })
            }
            if (seal.faceLock) {
              Text('👤')
                .fontSize(12)
                .margin({ right: 4 })
            }
            if (seal.gpsTracker) {
              Text('📡')
                .fontSize(12)
            }
          }
        }
        .width('100%')
        .margin({ top: 6 })
      }
      .layoutWeight(1)
      .alignItems(HorizontalAlign.Start)
    }
    .width('100%')
    .padding(16)
    .backgroundColor(
      seal.status === SealStatus.OUTSIDE ? 'rgba(255,102,0,0.05)' :
      seal.status === SealStatus.IN_USE ? 'rgba(255,204,0,0.05)' :
      '#0a0a0a'
    )
    .borderRadius(8)
    .margin({ left: 12, right: 12, top: 8 })
  }

  // ==================== 滑动操作 ====================
  @Builder
  SealSwipeBuilder(seal: Seal) {
    Row() {
      Button() {
        Text('申请')
          .fontColor('#fff')
          .fontSize(12)
      }
      .type(ButtonType.Capsule)
      .backgroundColor('#0066cc')
      .width(60)
      .height('100%')
      .margin({ right: 4 })
      .onClick(() => {
        this.startApplication(seal);
      })

      Button() {
        Text('外带')
          .fontColor('#fff')
          .fontSize(12)
      }
      .type(ButtonType.Capsule)
      .backgroundColor('#ff6600')
      .width(60)
      .height('100%')
      .margin({ right: 4 })
      .onClick(() => {
        this.startOutRecord(seal);
      })

      Button() {
        Text('删除')
          .fontColor('#fff')
          .fontSize(12)
      }
      .type(ButtonType.Capsule)
      .backgroundColor('#ff0000')
      .width(60)
      .height('100%')
      .onClick(() => {
        AlertDialog.show({
          title: '确认删除',
          message: `删除 ${seal.name}？此操作不可恢复`,
          primaryButton: {
            value: '删除',
            action: () => {
              this.sealState.removeSeal(seal.id);
            }
          },
          secondaryButton: {
            value: '取消',
            action: () => { }
          }
        });
      })
    }
    .width(200)
    .height('100%')
    .padding({ left: 4 })
  }

  // ==================== 申请列表 ====================
  @Builder
  ApplicationListBuilder() {
    List() {
      ForEach(this.sealState.applications.sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime()), (app: SealApplication) => {
        ListItem() {
          this.ApplicationCardBuilder(app)
        }
        .onClick(() => {
          this.editingApp = app;
          if (app.result === 'pending') {
            this.showApprovalDialog = true;
          } else {
            this.showExecuteDialog = true;
          }
        })
      }, (app: SealApplication) => app.id)
    }
    .width('100%')
    .layoutWeight(1)
    .divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto)
    .padding({ bottom: 16 })
  }

  // ==================== 申请卡片 ====================
  @Builder
  ApplicationCardBuilder(app: SealApplication) {
    Row() {
      // 状态图标
      Column() {
        Text(
          app.result === 'pending' ? '⏳' :
          app.result === 'approved' ? '✅' :
          app.result === 'rejected' ? '❌' :
          app.result === 'executed' ? '📋' : '✕'
        )
        .fontSize(24)
      }
      .width(40)
      .height(40)
      .margin({ right: 12 })
      .justifyContent(FlexAlign.Center)

      // 信息
      Column() {
        Row() {
          Text(app.documentName)
            .fontSize(15)
            .fontWeight(FontWeight.Medium)
            .fontColor('#fff')
            .layoutWeight(1)
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })

          // 紧急度
          Text(app.urgency)
            .fontSize(11)
            .fontColor(
              app.urgency === '特急' ? '#ff0000' :
              app.urgency === '紧急' ? '#ffcc00' : '#888'
            )
            .backgroundColor(
              app.urgency === '特急' ? 'rgba(255,0,0,0.1)' :
              app.urgency === '紧急' ? 'rgba(255,204,0,0.1)' : '#2a2a2a'
            )
            .borderRadius(4)
            .padding({ left: 6, right: 6 })
        }
        .width('100%')

        Row() {
          Text(`${app.sealName} · ${app.usageType}`)
            .fontSize(12)
            .fontColor('#888')
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
            .layoutWeight(1)

          Text(`${app.documentCount}份${app.documentPages}页`)
            .fontSize(12)
            .fontColor('#888')
        }
        .width('100%')
        .margin({ top: 4 })

        Row() {
          Text(`👤${app.applicant}`)
            .fontSize(11)
            .fontColor('#666')

          Text(`📅${app.applyDate.toLocaleDateString()}`)
            .fontSize(11)
            .fontColor('#666')
            .margin({ left: 8 })

          Blank()

          // 审批进度
          if (app.result === 'pending') {
            const progress = app.getApprovalProgress();
            Stack() {
              Row()
                .width(60)
                .height(4)
                .backgroundColor('#333')
                .borderRadius(2)

              Row()
                .width(`${progress.percentage}%`)
                .height(4)
                .backgroundColor('#c41e3a')
                .borderRadius(2)
            }
            .width(60)
            .height(4)

            Text(`${progress.current}/${progress.total}`)
              .fontSize(10)
              .fontColor('#c41e3a')
              .margin({ left: 4 })
          }
        }
        .width('100%')
        .margin({ top: 6 })
      }
      .layoutWeight(1)
      .alignItems(HorizontalAlign.Start)
    }
    .width('100%')
    .padding(16)
    .backgroundColor(
      app.result === 'pending' ? 'rgba(196,30,58,0.05)' :
      app.result === 'rejected' ? 'rgba(255,0,0,0.05)' :
      '#0a0a0a'
    )
    .borderRadius(8)
    .margin({ left: 12, right: 12, top: 8 })
  }

  // ==================== 执行记录列表 ====================
  @Builder
  RecordListBuilder() {
    List() {
      ForEach(
        this.sealState.applications.filter(a => a.result === 'executed').sort((a, b) =>
          (b.executeTime?.getTime() || 0) - (a.executeTime?.getTime() || 0)
        ),
        (app: SealApplication) => {
          ListItem() {
            this.RecordCardBuilder(app)
          }
        },
        (app: SealApplication) => app.id
      )
    }
    .width('100%')
    .layoutWeight(1)
    .divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto)
    .padding({ bottom: 16 })
  }

  // ==================== 执行记录卡片 ====================
  @Builder
  RecordCardBuilder(app: SealApplication) {
    Row() {
      Column() {
        Text('📋')
          .fontSize(24)
      }
      .width(40)
      .height(40)
      .margin({ right: 12 })
      .justifyContent(FlexAlign.Center)

      Column() {
        Row() {
          Text(app.documentName)
            .fontSize(15)
            .fontWeight(FontWeight.Medium)
            .fontColor('#fff')
            .layoutWeight(1)

          Text('✅已执行')
            .fontSize(11)
            .fontColor('#00ff00')
            .backgroundColor('rgba(0,255,0,0.1)')
            .borderRadius(4)
            .padding({ left: 6, right: 6 })
        }
        .width('100%')

        Row() {
          Text(`${app.sealName} · ${app.executor}`)
            .fontSize(12)
            .fontColor('#888')
            .layoutWeight(1)

          Text(`${app.actualCount || app.documentCount}份`)
            .fontSize(12)
            .fontColor('#888')
        }
        .width('100%')
        .margin({ top: 4 })

        Row() {
          Text(`📅${app.executeTime?.toLocaleString() || ''}`)
            .fontSize(11)
            .fontColor('#666')

          if (app.gpsLocation) {
            Text(`📍${app.gpsLocation.lat.toFixed(4)},${app.gpsLocation.lng.toFixed(4)}`)
              .fontSize(11)
              .fontColor('#666')
              .margin({ left: 8 })
          }

          Blank()

          Text(`👁️${app.witness}`)
            .fontSize(11)
            .fontColor('#666')
        }
        .width('100%')
        .margin({ top: 6 })

        // 现场照片缩略图
        if (app.photos.length > 0) {
          Row() {
            ForEach(app.photos.slice(0, 3), (photo: string) => {
              Image(photo)
                .width(40)
                .height(40)
                .borderRadius(4)
                .objectFit(ImageFit.Cover)
                .margin({ right: 4 })
            })

            if (app.photos.length > 3) {
              Text(`+${app.photos.length - 3}`)
                .fontSize(12)
                .fontColor('#888')
                .width(40)
                .height(40)
                .backgroundColor('#2a2a2a')
                .borderRadius(4)
                .textAlign(TextAlign.Center)
            }
          }
          .width('100%')
          .margin({ top: 8 })
        }
      }
      .layoutWeight(1)
      .alignItems(HorizontalAlign.Start)
    }
    .width('100%')
    .padding(16)
    .backgroundColor('#0a0a0a')
    .borderRadius(8)
    .margin({ left: 12, right: 12, top: 8 })
  }

  // ==================== 外带追踪 ====================
  @Builder
  OutTrackBuilder() {
    List() {
      ForEach(this.sealState.activeOutRecords, (record: SealOutRecord) => {
        ListItem() {
          this.OutRecordCardBuilder(record)
        }
      }, (record: SealOutRecord) => record.id)
    }
    .width('100%')
    .layoutWeight(1)
    .divider({ strokeWidth: 1, color: '#222' })
    .scrollBar(BarState.Auto)
    .padding({ bottom: 16 })
  }

  // ==================== 外带记录卡片 ====================
  @Builder
  OutRecordCardBuilder(record: SealOutRecord) {
    Row() {
      Column() {
        Text('📍')
          .fontSize(24)
      }
      .width(40)
      .height(40)
      .margin({ right: 12 })
      .justifyContent(FlexAlign.Center)

      Column() {
        Row() {
          Text(record.sealName)
            .fontSize(15)
            .fontWeight(FontWeight.Medium)
            .fontColor('#fff')
            .layoutWeight(1)

          if (record.isOverdue()) {
            Text('超期')
              .fontSize(11)
              .fontColor('#ff0000')
              .backgroundColor('rgba(255,0,0,0.1)')
              .borderRadius(4)
              .padding({ left: 6, right: 6 })
          } else {
            Text('外带中')
              .fontSize(11)
              .fontColor('#ff6600')
              .backgroundColor('rgba(255,102,0,0.1)')
              .borderRadius(4)
              .padding({ left: 6, right: 6 })
          }
        }
        .width('100%')

        Row() {
          Text(`借出: ${record.borrower} · ${record.borrowDate.toLocaleDateString()}`)
            .fontSize(12)
            .fontColor('#888')
            .layoutWeight(1)

          Text(`预计归还: ${record.expectedReturn.toLocaleDateString()}`)
            .fontSize(12)
            .fontColor(record.isOverdue() ? '#ff0000' : '#888')
        }
        .width('100%')
        .margin({ top: 4 })

        Row() {
          Text(`📍${record.destination}`)
            .fontSize(11)
            .fontColor('#666')
            .layoutWeight(1)

          Text(`👤陪同: ${record.escort}`)
            .fontSize(11)
            .fontColor('#666')
        }
        .width('100%')
        .margin({ top: 6 })

        // GPS轨迹点
        if (record.gpsTrack.length > 0) {
          Row() {
            Text(`📡 GPS轨迹: ${record.gpsTrack.length}个点`)
              .fontSize(11)
              .fontColor('#666')

            Text(`最新: ${record.gpsTrack[record.gpsTrack.length - 1].lat.toFixed(4)},${record.gpsTrack[record.gpsTrack.length - 1].lng.toFixed(4)}`)
              .fontSize(11)
              .fontColor('#666')
              .margin({ left: 8 })
          }
          .width('100%')
          .margin({ top: 4 })
        }

        // 回传记录
        if (record.checkInRecords.length > 0) {
          Row() {
            Text(`📝 回传: ${record.checkInRecords.length}次`)
              .fontSize(11)
              .fontColor('#666')

            Text(`最新: ${record.checkInRecords[record.checkInRecords.length - 1].timestamp.toLocaleString()}`)
              .fontSize(11)
              .fontColor('#666')
              .margin({ left: 8 })
          }
          .width('100%')
          .margin({ top: 4 })
        }
      }
      .layoutWeight(1)
      .alignItems(HorizontalAlign.Start)
    }
    .width('100%')
    .padding(16)
    .backgroundColor(
      record.isOverdue() ? 'rgba(255,0,0,0.05)' : 'rgba(255,102,0,0.05)'
    )
    .borderRadius(8)
    .margin({ left: 12, right: 12, top: 8 })
  }

  // ==================== 底部操作栏 ====================
  @Builder
  FooterBuilder() {
    Row() {
      Button('📝 用印申请')
        .fontSize(13)
        .fontColor('#fff')
        .backgroundColor('#0066cc')
        .borderRadius(8)
        .padding({ left: 16, right: 16 })
        .onClick(() => {
          this.showAppDialog = true;
        })

      Button('📋 执行登记')
        .fontSize(13)
        .fontColor('#fff')
        .backgroundColor('#c41e3a')
        .borderRadius(8)
        .padding({ left: 16, right: 16 })
        .onClick(() => {
          this.showExecuteDialog = true;
        })

      Button('📍 外带登记')
        .fontSize(13)
        .fontColor('#fff')
        .backgroundColor('#ff6600')
        .borderRadius(8)
        .padding({ left: 16, right: 16 })
        .onClick(() => {
          this.showOutDialog = true;
        })

      Button('📊 导出台账')
        .fontSize(13)
        .fontColor('#ccc')
        .backgroundColor('#1a1a1a')
        .border({ width: 1, color: '#444' })
        .borderRadius(8)
        .padding({ left: 16, right: 16 })
        .onClick(() => {
          this.exportLedger();
        })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
    .justifyContent(FlexAlign.SpaceAround)
  }

  // ==================== 辅助方法 ====================
  private getAlertCount(): number {
    return this.getAllAlerts().length;
  }

  private getAllAlerts(): AlertItem[] {
    const alerts: AlertItem[] = [];

    // 超期外带
    this.sealState.overdueRecords.forEach(r => {
      alerts.push({
        type: 'overdue',
        level: 'critical',
        title: `${r.sealName} 外带超期`,
        message: `借出人: ${r.borrower}，预计归还: ${r.expectedReturn.toLocaleDateString()}`,
        timestamp: new Date()
      });
    });

    // 待审批
    if (this.sealState.pendingApprovals.length > 0) {
      alerts.push({
        type: 'pending',
        level: 'warning',
        title: `${this.sealState.pendingApprovals.length} 条用印申请待审批`,
        message: '请尽快处理',
        timestamp: new Date()
      });
    }

    return alerts;
  }

  private getAlertPreview(): string {
    const alerts = this.getAllAlerts();
    return alerts.slice(0, 2).map(a => a.title).join('、');
  }

  private startScan() {
    // 调用鸿蒙扫码 / 解析印章条码RFID
    console.info('启动扫码');
  }

  private startApplication(seal: Seal) {
    this.editingSeal = seal;
    this.showAppDialog = true;
  }

  private startOutRecord(seal: Seal) {
    this.editingSeal = seal;
    this.showOutDialog = true;
  }

  private exportLedger() {
    // 导出台账Excel/CSV
    console.info('导出台账');
  }

  private scheduleAlerts() {
    // 设置定时检查：超期提醒、待审批提醒
    console.info('启动预警调度');
  }
}
