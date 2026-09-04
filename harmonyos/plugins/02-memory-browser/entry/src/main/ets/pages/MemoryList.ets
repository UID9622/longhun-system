/**
 * 🐉 龍魂·MemoryList — 记忆列表主页面
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-MEMORY-LIST-UID9622
 *
 * LazyForEach 虚拟列表 · 下拉刷新 · 上拉加载 · 暗金主题
 */

import { MemoryViewModel } from '../viewmodel/MemoryViewModel';
import { MemoryCard } from '../components/MemoryCard';
import { CoreServiceClient } from '../service/CoreServiceClient';
import { router } from '@kit.ArkUI';
import { promptAction } from '@kit.ArkUI';

@Entry
@Component
struct MemoryList {
  @State viewModel: MemoryViewModel = new MemoryViewModel();
  @State connectedToCore: boolean = false;
  @State statsText: string = '加载中...';
  private scroller: Scroller = new Scroller();

  aboutToAppear(): void {
    this.connectAndLoad();
  }

  async connectAndLoad(): Promise<void> {
    // 尝试连接核心服务
    try {
      this.connectedToCore = await CoreServiceClient.connect(getContext(this) as common.UIAbilityContext);
      console.info(`[龍魂·记忆] 核心服务连接: ${this.connectedToCore}`);
    } catch (e) {
      this.connectedToCore = false;
    }

    // 加载记忆
    await this.viewModel.loadMemories();

    // 更新统计
    if (this.viewModel.memories.length > 0) {
      const stats = this.viewModel.getStats();
      this.statsText = `P0:${stats['P0·永恒']} P1:${stats['P1·重要']} P2:${stats['P2·普通']} P3:${stats['P3·临时']}`;
    }
  }

  build() {
    Column() {
      // 顶栏
      Row() {
        Text('🐉 龍魂记忆')
          .fontSize(20)
          .fontColor('#C9A84C')
          .fontWeight(FontWeight.Bold)

        Blank()

        // 核心服务连接状态
        Text(this.connectedToCore ? '🟢 已连接' : '🟡 离线')
          .fontSize(10)
          .fontColor(this.connectedToCore ? '#4ADE80' : '#F4A261')
          .margin({ right: 8 })

        // 图谱入口
        Button('📊 图谱')
          .fontSize(11)
          .height(28)
          .backgroundColor('#1E293B')
          .fontColor('#C9A84C')
          .border({ width: 1, color: '#C9A84C', style: BorderStyle.Solid })
          .borderRadius(14)
          .onClick(() => {
            router.pushUrl({ url: 'pages/MemoryGraph' });
          })
      }
      .width('100%')
      .padding({ left: 16, right: 16, top: 12, bottom: 8 })

      // 统计条
      Row() {
        Text(this.statsText)
          .fontSize(10)
          .fontColor('#6B7280')
          .margin({ left: 16 })

        Blank()

        Text(`共 ${this.viewModel.memories.length} 条`)
          .fontSize(10)
          .fontColor('#6B7280')
          .margin({ right: 16 })
      }
      .width('100%')
      .padding({ bottom: 4 })

      // 搜索栏
      Row() {
        TextInput({ placeholder: '搜索记忆...' })
          .fontSize(13)
          .backgroundColor('#1E293B')
          .borderRadius(20)
          .height(36)
          .layoutWeight(1)
          .placeholderColor('#6B7280')
          .onChange((value: string) => {
            this.viewModel.search(value);
          })

        Button('搜索')
          .fontSize(12)
          .height(36)
          .backgroundColor('#1E293B')
          .fontColor('#C9A84C')
          .border({ width: 1, color: '#C9A84C', style: BorderStyle.Solid })
          .borderRadius(20)
          .margin({ left: 8 })
          .onClick(() => {
            this.viewModel.loadMemories();
          })
      }
      .width('100%')
      .padding({ left: 16, right: 16, bottom: 8 })

      // 记忆列表
      if (this.viewModel.loading) {
        Column() {
          LoadingProgress()
            .width(40)
            .height(40)
            .color('#C9A84C')
          Text('加载记忆中...')
            .fontSize(13)
            .fontColor('#6B7280')
            .margin({ top: 8 })
        }
        .width('100%')
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else if (this.viewModel.memories.length === 0) {
        Column() {
          Text('📭')
            .fontSize(40)
            .margin({ bottom: 12 })
          Text('暂无记忆')
            .fontSize(16)
            .fontColor('#6B7280')
          Text(this.viewModel.error)
            .fontSize(12)
            .fontColor('#4B5563')
            .margin({ top: 4 })
        }
        .width('100%')
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      } else {
        List({ scroller: this.scroller }) {
          LazyForEach(
            new SimpleDataSource(this.viewModel.memories),
            (item: Record<string, Object>, index: number): void => {
              ListItem() {
                MemoryCard({
                  id: item['id'] as string,
                  priority: (item['priority'] as number) ?? 2,
                  category: (item['category'] as string) ?? '',
                  content: (item['content'] as string) ?? '',
                  timestamp: (item['timestamp'] as string) ?? '',
                  tricolor: (item['tricolor'] as string) ?? '🟢',
                  dna: (item['dna'] as string) ?? '',
                  keywords: (item['keywords'] as string[]) ?? [],
                  onCardClick: () => {
                    router.pushUrl({
                      url: 'pages/MemoryDetail',
                      params: { memory: JSON.stringify(item) }
                    });
                  },
                  onCardLongPress: () => {
                    promptAction.showActionMenu({
                      title: '操作',
                      buttons: [
                        { text: '查看详情', color: '#C9A84C' },
                        { text: '复制内容', color: '#E5E7EB' },
                        { text: '导出', color: '#E5E7EB' },
                      ]
                    });
                  }
                })
              }
            },
            (item: Record<string, Object>): string => (item['id'] as string) || ''
          )
        }
        .layoutWeight(1)
        .scrollBar(BarState.Auto)
        .onReachStart(() => {
          // 下拉刷新
          this.viewModel.loadMemories();
        })
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0F172A') // 深色背景
  }
}

// LAZY DATA SOURCE FOR LAZYFOREACH
class SimpleDataSource implements IDataSource {
  private dataArray: Record<string, Object>[] = [];
  private listeners: DataChangeListener[] = [];

  constructor(data: Record<string, Object>[]) {
    this.dataArray = data;
  }

  totalCount(): number { return this.dataArray.length; }
  getData(index: number): Record<string, Object> { return this.dataArray[index]; }

  registerDataChangeListener(listener: DataChangeListener): void {
    this.listeners.push(listener);
  }

  unregisterDataChangeListener(): void {
    this.listeners = [];
  }
}
