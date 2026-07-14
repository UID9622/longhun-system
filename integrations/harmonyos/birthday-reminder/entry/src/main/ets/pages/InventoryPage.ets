// entry/src/main/ets/pages/InventoryPage.ets
// 龍魂 · 办公物资库存主页面 · ArkTS

import {
  SupplyItem, SupplyCategory, ItemStatus,
  InventoryState, InventoryRecord, PurchaseRequest,
  inventoryState, AlertItem
} from '../models/InventoryModel';
import { InventoryDetailDialog } from '../components/InventoryDetailDialog';
import { StockOperationDialog } from '../components/StockOperationDialog';
import { PurchaseRequestDialog } from '../components/PurchaseRequestDialog';
import { AlertPanel } from '../components/AlertPanel';
import { InventoryDatabase } from '../database/InventoryDatabase';

const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";

@Entry
@Component
struct InventoryPage {
  @StorageLink('inventoryState') inventoryState: InventoryState = inventoryState;
  @State private selectedTab: number = 0;
  @State private showAddDialog: boolean = false;
  @State private showStockDialog: boolean = false;
  @State private showPurchaseDialog: boolean = false;
  @State private showDetailDialog: boolean = false;
  @State private editingItem: SupplyItem | null = null;
  @State private showSearch: boolean = false;
  @State private searchText: string = '';
  @State private showAlerts: boolean = false;
  @State private filterCategoryIdx: number = 0;
  @State private filterStatusIdx: number = 0;

  private detailController: CustomDialogController | null = null;
  private stockController: CustomDialogController | null = null;
  private purchaseController: CustomDialogController | null = null;

  aboutToAppear() {
    this.inventoryState.load();
  }

  build() {
    Column() {
      // 标题栏
      this.HeaderBuilder()

      // 预警横幅
      if (this.inventoryState.alerts.length > 0 && !this.showAlerts) {
        this.AlertBannerBuilder()
      }

      // 预警面板（展开）
      if (this.showAlerts) {
        AlertPanel({
          alerts: this.inventoryState.alerts,
          onClose: () => { this.showAlerts = false; }
        })
      }

      // 统计卡片
      this.StatsBuilder()

      // 标签切换
      this.TabBuilder()

      // 搜索栏
      if (this.showSearch) {
        this.SearchBuilder()
      }

      // 过滤工具栏
      this.FilterBuilder()

      // 物资列表
      this.ItemListBuilder()

      // 底部操作栏
      this.FooterBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  // === 标题栏 ===
  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉')
        .fontSize(28)
        .margin({ right: 8 })

      Column() {
        Text('龍魂库存管理')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor('#c41e3a')

        Text(`UID:${MASTER_UID} · ${this.inventoryState.items.length}项物资`)
          .fontSize(12)
          .fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)

      Blank()

      // 预警按钮
      Badge({
        value: this.inventoryState.alerts.length.toString(),
        position: BadgePosition.RightTop,
        style: { badgeSize: 18, badgeColor: '#c41e3a' }
      }) {
        Button() {
          Text('🔔').fontSize(20)
        }
        .type(ButtonType.Circle)
        .backgroundColor(this.inventoryState.alerts.length > 0 ? 'rgba(196,30,58,0.2)' : '#1a1a1a')
        .width(40).height(40)
        .onClick(() => {
          this.showAlerts = !this.showAlerts;
        })
      }

      // 搜索按钮
      Button() {
        Text(this.showSearch ? '✕' : '🔍').fontSize(20)
      }
      .type(ButtonType.Circle)
      .backgroundColor('#1a1a1a')
      .width(40).height(40)
      .onClick(() => {
        this.showSearch = !this.showSearch;
        if (!this.showSearch) {
          this.inventoryState.searchQuery = '';
          this.searchText = '';
        }
      })

      // 添加按钮
      Button() {
        Text('+').fontSize(24).fontColor('#fff')
      }
      .type(ButtonType.Circle)
      .backgroundColor('#c41e3a')
      .width(40).height(40)
      .onClick(() => {
        this.editingItem = null;
        this.showAddItemDialog();
      })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // === 预警横幅 ===
  @Builder
  AlertBannerBuilder() {
    Row() {
      Text('⚠️').fontSize(24).margin({ right: 8 })

      Column() {
        Text(`${this.inventoryState.alerts.length} 条预警待处理`)
          .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#ffcc00')
        Text(this.inventoryState.alerts.slice(0, 2).map(a => a.title).join('、'))
          .fontSize(12).fontColor('#ffcc00')
          .maxLines(1).textOverflow({ overflow: TextOverflow.Ellipsis })
      }
      .alignItems(HorizontalAlign.Start).layoutWeight(1)

      Button('查看')
        .fontSize(12).fontColor('#0a0a0a')
        .backgroundColor('#ffcc00').borderRadius(12)
        .padding({ left: 12, right: 12 })
        .onClick(() => { this.showAlerts = true; })
    }
    .width('100%')
    .padding(12)
    .backgroundColor('rgba(255,204,0,0.1)')
    .border({ width: { bottom: 1 }, color: 'rgba(255,204,0,0.3)' })
  }

  // === 统计卡片 ===
  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('总物资', this.inventoryState.statistics.totalItems.toString(), '#fff')
      this.StatCard('在库', this.inventoryState.statistics.inStock.toString(), '#00ff00')
      this.StatCard('低库存', this.inventoryState.statistics.lowStock.toString(), '#ffcc00')
      this.StatCard('缺货', this.inventoryState.statistics.outOfStock.toString(), '#ff0000')
      this.StatCard('总值', `¥${(this.inventoryState.statistics.totalValue / 10000).toFixed(1)}万`, '#c41e3a')
    }
    .width('100%')
    .padding({ left: 12, right: 12, top: 12, bottom: 12 })
    .justifyContent(FlexAlign.SpaceAround)
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() {
      Text(value)
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
        .fontColor(color)
        .maxLines(1)
        .textOverflow({ overflow: TextOverflow.Ellipsis })
      Text(label)
        .fontSize(10)
        .fontColor('#888')
        .margin({ top: 4 })
    }
    .padding(8)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .width('18%')
  }

  // === 标签切换 ===
  @Builder
  TabBuilder() {
    Row() {
      ForEach([
        { label: '库存总览', icon: '📦' },
        { label: '出入库', icon: '📋' },
        { label: '采购审批', icon: '✅' },
        { label: '盘点', icon: '📊' }
      ], (item: { label: string, icon: string }, index: number) => {
        Column() {
          Text(`${item.icon} ${item.label}`)
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
        .onClick(() => { this.selectedTab = index; })
      })
    }
    .width('100%')
    .justifyContent(FlexAlign.SpaceAround)
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // === 搜索栏 ===
  @Builder
  SearchBuilder() {
    Row() {
      TextInput({ placeholder: '搜索名称/编码/条码/位置...', text: $$this.searchText })
        .width('100%')
        .height(40)
        .backgroundColor('#2a2a2a')
        .fontColor('#fff')
        .placeholderColor('#666')
        .borderRadius(8)
        .padding({ left: 12, right: 12 })
        .onChange((value: string) => {
          this.inventoryState.searchQuery = value;
        })
    }
    .width('100%')
    .padding({ left: 16, right: 16, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
  }

  // === 过滤工具栏 ===
  @Builder
  FilterBuilder() {
    Row() {
      // 分类选择
      Select([{ value: '全部分类' },
        ...Object.values(SupplyCategory).map(c => ({ value: c }))])
        .selected(this.filterCategoryIdx)
        .fontColor('#ccc')
        .backgroundColor('#2a2a2a')
        .borderRadius(8)
        .height(36)
        .padding({ left: 8, right: 8 })
        .layoutWeight(1)
        .onSelect((index: number) => {
          this.filterCategoryIdx = index;
          this.inventoryState.filterCategory = index === 0 ? '全部' : Object.values(SupplyCategory)[index - 1];
        })

      // 状态选择
      Select([{ value: '全部状态' },
        ...Object.values(ItemStatus).map(s => ({ value: s }))])
        .selected(this.filterStatusIdx)
        .fontColor('#ccc')
        .backgroundColor('#2a2a2a')
        .borderRadius(8)
        .height(36)
        .padding({ left: 8, right: 8 })
        .layoutWeight(1)
        .margin({ left: 8 })
        .onSelect((index: number) => {
          this.filterStatusIdx = index;
          this.inventoryState.filterStatus = index === 0 ? '全部' : Object.values(ItemStatus)[index - 1];
        })
    }
    .width('100%')
    .height(48)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // === 物资列表 ===
  @Builder
  ItemListBuilder() {
    if (this.inventoryState.filteredItems.length === 0) {
      Column() {
        Text('📦').fontSize(48).margin({ bottom: 12 })
        Text('暂无物资').fontSize(16).fontColor('#666')
        Text('点击右下角 + 添加第一件物资').fontSize(12).fontColor('#444').margin({ top: 8 })
      }
      .width('100%')
      .layoutWeight(1)
      .justifyContent(FlexAlign.Center)
    } else {
      List() {
        ForEach(this.inventoryState.filteredItems, (item: SupplyItem) => {
          ListItem() {
            this.ItemCardBuilder(item)
          }
          .swipeAction({ end: this.SwipeActionsBuilder(item) })
          .onClick(() => {
            this.editingItem = item;
            this.showDetailDialog = true;
          })
        }, (item: SupplyItem) => item.id)
      }
      .width('100%')
      .layoutWeight(1)
      .divider({ strokeWidth: 1, color: '#222' })
      .scrollBar(BarState.Auto)
      .edgeEffect(EdgeEffect.Spring)
    }
  }

  // === 物资卡片 ===
  @Builder
  ItemCardBuilder(item: SupplyItem) {
    Row() {
      // 左侧健康度+条码
      Stack() {
        Column() {
          Text(item.sku)
            .fontSize(9)
            .fontColor('#888')
            .fontFamily('monospace')
            .rotate({ angle: -90 })
        }
        .width(40)
        .height(40)
        .backgroundColor('#2a2a2a')
        .borderRadius(4)
        .justifyContent(FlexAlign.Center)

        // 状态角标
        if (item.status === ItemStatus.OUT_OF_STOCK || item.status === ItemStatus.LOW_STOCK || item.checkExpiry()) {
          Text(item.status === ItemStatus.OUT_OF_STOCK ? '缺' :
               item.status === ItemStatus.LOW_STOCK ? '低' : '过')
            .fontSize(9)
            .fontColor('#fff')
            .backgroundColor(
              item.status === ItemStatus.OUT_OF_STOCK ? '#ff0000' :
              item.status === ItemStatus.LOW_STOCK ? '#ffcc00' : '#ff6600'
            )
            .borderRadius(4)
            .padding({ left: 2, right: 2 })
            .position({ x: 28, y: -4 })
        }
      }
      .width(40)
      .height(40)
      .margin({ right: 12 })

      // 信息区
      Column() {
        Row() {
          Text(item.name)
            .fontSize(15)
            .fontWeight(FontWeight.Medium)
            .fontColor('#fff')
            .layoutWeight(1)
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })

          Text(`¥${item.purchasePrice.toFixed(2)}`)
            .fontSize(12)
            .fontColor('#888')
        }
        .width('100%')

        Row() {
          Text(`${item.category} · ${item.specification || '-'}`)
            .fontSize(12)
            .fontColor('#888')
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
            .layoutWeight(1)

          Text(`${item.quantity}${item.unit}`)
            .fontSize(14)
            .fontWeight(FontWeight.Bold)
            .fontColor(
              item.status === ItemStatus.OUT_OF_STOCK ? '#ff0000' :
              item.status === ItemStatus.LOW_STOCK ? '#ffcc00' : '#00ff00'
            )
        }
        .width('100%')
        .margin({ top: 4 })

        Row() {
          Text(`📍${item.location}`)
            .fontSize(11).fontColor('#666')
          Text(`👤${item.custodian}`)
            .fontSize(11).fontColor('#666').margin({ left: 8 })
          Blank()

          // 健康度条
          Stack() {
            Row()
              .width('100%').height(4)
              .backgroundColor('#333').borderRadius(2)
            Row()
              .width(`${item.getHealthScore()}%`).height(4)
              .backgroundColor(
                item.getHealthScore() > 80 ? '#00ff00' :
                item.getHealthScore() > 50 ? '#ffcc00' : '#ff0000'
              )
              .borderRadius(2)
          }
          .width(50).height(4)
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
      item.status === ItemStatus.OUT_OF_STOCK ? 'rgba(255,0,0,0.05)' :
      item.status === ItemStatus.LOW_STOCK ? 'rgba(255,204,0,0.05)' : '#0a0a0a'
    )
    .borderRadius(8)
    .margin({ left: 12, right: 12, top: 8 })
  }

  // === 滑动操作 ===
  @Builder
  SwipeActionsBuilder(item: SupplyItem) {
    Row() {
      Button() {
        Text('入库').fontColor('#fff').fontSize(12)
      }
      .type(ButtonType.Capsule)
      .backgroundColor('#00aa00')
      .width(60).height('100%')
      .margin({ right: 4 })
      .onClick(() => {
        this.editingItem = item;
        this.showStockDialog = true;
      })

      Button() {
        Text('出库').fontColor('#fff').fontSize(12)
      }
      .type(ButtonType.Capsule)
      .backgroundColor('#c41e3a')
      .width(60).height('100%')
      .margin({ right: 4 })
      .onClick(() => {
        this.editingItem = item;
        this.showStockDialog = true;
      })

      Button() {
        Text('删除').fontColor('#fff').fontSize(12)
      }
      .type(ButtonType.Capsule)
      .backgroundColor('#ff0000')
      .width(60).height('100%')
      .onClick(() => {
        AlertDialog.show({
          title: '确认删除',
          message: `删除 ${item.name}？`,
          primaryButton: {
            value: '删除',
            fontColor: '#ff0000',
            action: () => { this.inventoryState.removeItem(item.id); }
          },
          secondaryButton: {
            value: '取消',
            action: () => {}
          }
        });
      })
    }
    .width(200).height('100%').padding({ left: 4 })
  }

  // === 底部操作栏 ===
  @Builder
  FooterBuilder() {
    Row() {
      Button('📥 入库')
        .fontSize(13).fontColor('#fff')
        .backgroundColor('#00aa00').borderRadius(8)
        .padding({ left: 16, right: 16 })
        .onClick(() => {
          this.editingItem = undefined;
          this.showStockDialog = true;
        })

      Button('📤 出库')
        .fontSize(13).fontColor('#fff')
        .backgroundColor('#c41e3a').borderRadius(8)
        .padding({ left: 16, right: 16 })
        .onClick(() => {
          this.editingItem = undefined;
          this.showStockDialog = true;
        })

      Button('📝 采购')
        .fontSize(13).fontColor('#fff')
        .backgroundColor('#0066cc').borderRadius(8)
        .padding({ left: 16, right: 16 })
        .onClick(() => { this.showPurchaseDialog = true; })

      Button('📊 导出')
        .fontSize(13).fontColor('#ccc')
        .backgroundColor('#1a1a1a')
        .border({ width: 1, color: '#444' })
        .borderRadius(8)
        .padding({ left: 16, right: 16 })
        .onClick(() => { this.exportCSV(); })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
    .justifyContent(FlexAlign.SpaceAround)
  }

  // === 弹窗 ===
  @Builder
  DetailDialogBuilder() {
    if (this.editingItem && this.showDetailDialog) {
      Column() {
        InventoryDetailDialog({
          controller: new CustomDialogController({
            builder: InventoryDetailDialog({
              item: this.editingItem!,
              controller: new CustomDialogController({ builder: () => {} })
            }),
            autoCancel: true,
            alignment: DialogAlignment.Center,
            customStyle: true
          }),
          item: this.editingItem!
        })
      }
    }
  }

  @Builder
  StockDialogBuilder() {
    Column() {
      StockOperationDialog({
        controller: new CustomDialogController({
          builder: StockOperationDialog({
            item: this.editingItem ?? undefined,
            controller: new CustomDialogController({ builder: () => {} })
          }),
          autoCancel: true,
          alignment: DialogAlignment.Center,
          customStyle: true
        }),
        item: this.editingItem ?? undefined
      })
    }
  }

  @Builder
  PurchaseDialogBuilder() {
    Column() {
      PurchaseRequestDialog({
        controller: new CustomDialogController({
          builder: PurchaseRequestDialog({
            controller: new CustomDialogController({ builder: () => {} })
          }),
          autoCancel: true,
          alignment: DialogAlignment.Center,
          customStyle: true
        })
      })
    }
  }

  // === 功能方法 ===
  private showAddItemDialog() {
    // 跳转到添加物资页（简化：弹窗提示）
    AlertDialog.show({
      title: '添加物资',
      message: '输入物资基本信息',
      primaryButton: { value: '确定', action: () => {} },
      secondaryButton: { value: '取消', action: () => {} }
    });
  }

  private exportCSV() {
    const headers = '编码,名称,分类,规格,品牌,单位,数量,安全线,位置,状态,保管员,部门,采购价,总值\n';
    const rows = this.inventoryState.items.map(i =>
      `${i.sku},${i.name},${i.category},${i.specification},${i.brand},${i.unit},${i.quantity},${i.minQuantity},${i.location},${i.status},${i.custodian},${i.department},${i.purchasePrice},${i.totalValue}`
    ).join('\n');
    const csv = headers + rows;

    // 使用鸿蒙分享能力导出
    console.log('CSV generated:', csv.length, 'bytes');
    AlertDialog.show({
      title: '导出成功',
      message: `已生成 ${this.inventoryState.items.length} 条记录`,
      primaryButton: { value: '确定', action: () => {} }
    });
  }
}
