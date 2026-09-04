/**
 * 🐉 龍魂·MemoryDetail + MemorySearch 页面
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-MEMORY-DETAIL-SEARCH-UID9622
 */

import { router } from '@kit.ArkUI';

// ─── 记忆详情页 ───
@Entry
@Component
struct MemoryDetail {
  @State memory: Record<string, Object> = {};

  aboutToAppear(): void {
    const params = router.getParams() as Record<string, Object>;
    if (params && params['memory']) {
      try {
        this.memory = JSON.parse(params['memory'] as string) as Record<string, Object>;
      } catch (e) {
        this.memory = {};
      }
    }
  }

  build() {
    Column() {
      Row() {
        Text('← 返回')
          .fontSize(14)
          .fontColor('#C9A84C')
          .onClick(() => { router.back(); })
        Blank()
        Text('记忆详情')
          .fontSize(18)
          .fontColor('#C9A84C')
          .fontWeight(FontWeight.Bold)
      }
      .width('100%')
      .padding(16)

      if (Object.keys(this.memory).length > 0) {
        Scroll() {
          Column({ space: 12 }) {
            // 优先级
            DetailRow('优先级', `P${this.memory['priority']}`)
            // 分类
            DetailRow('分类', (this.memory['category'] as string) || '')
            // 三色
            DetailRow('三色状态', (this.memory['tricolor'] as string) || '')
            // 时间
            DetailRow('时间', (this.memory['timestamp'] as string) || '')
            // DNA (全量)
            Text('DNA 追溯码')
              .fontSize(11)
              .fontColor('#6B7280')
            Text((this.memory['dna'] as string) || '')
              .fontSize(11)
              .fontColor('#C9A84C')
              .fontFamily('monospace')
              .width('100%')
              .padding(12)
              .backgroundColor('#1E293B')
              .borderRadius(8)
            // 完整内容
            Text('内容')
              .fontSize(11)
              .fontColor('#6B7280')
            Text((this.memory['content'] as string) || '')
              .fontSize(14)
              .fontColor('#E5E7EB')
              .width('100%')
              .padding(16)
              .backgroundColor('#1E293B')
              .borderRadius(8)
              .lineHeight(22)
            // 关键词
            if (this.memory['keywords']) {
              Text('关键词')
                .fontSize(11)
                .fontColor('#6B7280')
              Wrap({ space: 6 }) {
                ForEach((this.memory['keywords'] as string[]) || [], (kw: string) => {
                  Text(kw)
                    .fontSize(10)
                    .fontColor('#C9A84C')
                    .padding({ left: 8, right: 8, top: 2, bottom: 2 })
                    .backgroundColor('#1E293B')
                    .border({ width: 0.5, color: '#334155', style: BorderStyle.Solid })
                    .borderRadius(10)
                })
              }
            }
          }
          .width('100%')
          .padding({ left: 16, right: 16 })
        }
        .layoutWeight(1)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0F172A')
  }
}

@Component
struct DetailRow {
  @Prop label: string = '';
  @Prop value: string = '';

  build() {
    Row() {
      Text(this.label)
        .fontSize(11)
        .fontColor('#6B7280')
        .width(80)
      Text(this.value)
        .fontSize(13)
        .fontColor('#E5E7EB')
        .layoutWeight(1)
    }
    .width('100%')
    .padding({ top: 4, bottom: 4 })
    .border({ width: { bottom: 0.5 }, color: '#1E293B', style: BorderStyle.Solid })
  }
}

// ─── 记忆搜索页 ───
@Entry
@Component
struct MemorySearch {
  @State query: string = '';
  @State results: Record<string, Object>[] = [];
  @State searching: boolean = false;
  private viewModel: MemoryViewModel = new MemoryViewModel();

  build() {
    Column() {
      Row() {
        Button('←')
          .fontSize(14)
          .backgroundColor('#0F172A')
          .fontColor('#C9A84C')
          .onClick(() => { router.back(); })

        TextInput({ placeholder: '输入搜索关键词...' })
          .fontSize(14)
          .backgroundColor('#1E293B')
          .borderRadius(20)
          .height(40)
          .layoutWeight(1)
          .placeholderColor('#6B7280')
          .onChange((value: string) => { this.query = value; })
          .onSubmit(() => { this.performSearch(); })

        Button('搜索')
          .fontSize(12)
          .height(36)
          .backgroundColor('#1E293B')
          .fontColor('#C9A84C')
          .border({ width: 1, color: '#C9A84C', style: BorderStyle.Solid })
          .borderRadius(20)
          .margin({ left: 8 })
          .onClick(() => { this.performSearch(); })
      }
      .width('100%')
      .padding(16)

      if (this.searching) {
        LoadingProgress()
          .width(40)
          .height(40)
          .color('#C9A84C')
          .margin({ top: 40 })
      } else if (this.results.length > 0) {
        List() {
          ForEach(this.results, (item: Record<string, Object>) => {
            ListItem() {
              MemoryCard({
                id: (item['id'] as string) || '',
                priority: (item['priority'] as number) || 2,
                category: (item['category'] as string) || '',
                content: (item['content'] as string) || '',
                timestamp: (item['timestamp'] as string) || '',
                tricolor: (item['tricolor'] as string) || '🟢',
                dna: (item['dna'] as string) || '',
                keywords: (item['keywords'] as string[]) || [],
              })
            }
          })
        }
        .layoutWeight(1)
      } else {
        Column() {
          Text('🔍')
            .fontSize(40)
            .margin({ bottom: 12 })
          Text('输入关键词搜索记忆')
            .fontSize(14)
            .fontColor('#6B7280')
        }
        .width('100%')
        .layoutWeight(1)
        .justifyContent(FlexAlign.Center)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0F172A')
  }

  private performSearch(): void {
    if (!this.query.trim()) return;
    this.searching = true;
    this.viewModel.search(this.query).then(() => {
      this.results = this.viewModel.memories.map(m => {
        const obj: Record<string, Object> = {};
        obj['id'] = m.id;
        obj['priority'] = m.priority;
        obj['category'] = m.category;
        obj['content'] = m.content;
        obj['timestamp'] = m.timestamp;
        obj['tricolor'] = m.tricolor;
        obj['dna'] = m.dna;
        obj['keywords'] = m.keywords;
        return obj;
      });
      this.searching = false;
    });
  }
}
