/**
 * 🐉 龍魂 Notion 目录查询 Demo
 * 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · License: MulanPSL v2
 * 只读: 连鲲鹏 8768 镜像端点 → 秒搜目录 → 正文主权留主控层
 */
import { QueryClient, NativeQuery, LhConfig } from 'notion-mcp-sdk';
import { MirrorStatus, CatalogEntry } from 'notion-mcp-sdk';

@Entry
@Component
struct Index {
  private client: QueryClient = new QueryClient();
  private native: NativeQuery = new NativeQuery();
  @State statusLine: string = '未连接';
  @State pages: number = 0;
  @State syncedAt: string = '-';
  @State endpoint: string = LhConfig.ENDPOINT;
  @State keyword: string = '';
  @State results: CatalogEntry[] = [];
  @State searching: boolean = false;

  async aboutToAppear(): Promise<void> {
    await this.loadStatus();
  }

  async loadStatus(): Promise<void> {
    this.statusLine = '连接中…';
    try {
      const st: MirrorStatus = await this.client.getMirrorStatus();
      if (st.ok) {
        this.pages = st.pages;
        this.syncedAt = st.synced_at;
        this.statusLine = '已连接 · 快照 ' + st.pages + ' 页';
      } else {
        this.statusLine = '端点无响应: ' + st.note;
      }
    } catch (e) {
      this.statusLine = '异常: ' + JSON.stringify(e);
    }
  }

  async onSearch(): Promise<void> {
    const q: string = this.keyword.trim();
    if (q.length === 0) {
      this.statusLine = '请输入关键词';
      return;
    }
    this.searching = true;
    try {
      const r = await this.client.searchCatalog(q, 30);
      this.results = r.items;
      this.statusLine = '命中 ' + r.count + ' 条（本地零 API）';
    } catch (e) {
      this.statusLine = '搜索异常: ' + JSON.stringify(e);
    } finally {
      this.searching = false;
    }
  }

  async onRawDemo(): Promise<void> {
    const q: string = this.keyword.trim() || '龍';
    const raw = await this.native.searchRaw(q);
    this.statusLine = raw.length > 160 ? raw.slice(0, 160) + '…' : raw;
  }

  build() {
    Column({ space: 10 }) {
      Text('🐉 龍魂 · Notion 目录')
        .fontSize(22)
        .fontWeight(FontWeight.Bold)
        .fontColor('#E8C46A')
        .margin({ top: 24 })
      Text(this.endpoint)
        .fontSize(11)
        .fontColor('#8A8FA3')
      Text(this.statusLine)
        .fontSize(14)
        .fontColor(this.statusLine.startsWith('已连接') ? '#5BD1A3' : '#E8A06A')
        .margin({ top: 4 })

      Row({ space: 12 }) {
        Column() {
          Text('📄 页')
            .fontSize(12)
            .fontColor('#8A8FA3')
          Text(this.pages.toString())
            .fontSize(24)
            .fontWeight(FontWeight.Bold)
        }
        .layoutWeight(1)
        .alignItems(HorizontalAlign.Center)

        Column() {
          Text('🕒 快照')
            .fontSize(12)
            .fontColor('#8A8FA3')
          Text(this.syncedAt.slice(0, 16))
            .fontSize(13)
        }
        .layoutWeight(1)
        .alignItems(HorizontalAlign.Center)
      }
      .padding(16)
      .backgroundColor('#24263C')
      .borderRadius(14)

      Row({ space: 8 }) {
        TextInput({ placeholder: '搜目录标题/URL', text: this.keyword })
          .layoutWeight(1)
          .height(44)
          .onChange((v: string) => {
            this.keyword = v;
          })
        Button('秒搜')
          .height(44)
          .enabled(!this.searching)
          .onClick(() => {
            this.onSearch();
          })
        Button('裸调')
          .height(44)
          .backgroundColor('#3A3D5C')
          .onClick(() => {
            this.onRawDemo();
          })
      }
      .width('100%')

      Button('重新连接')
        .width('100%')
        .backgroundColor('#4A4D73')
        .onClick(() => {
          this.loadStatus();
        })

      if (this.results.length > 0) {
        List({ space: 8 }) {
          ForEach(this.results, (item: CatalogEntry) => {
            ListItem() {
              Column({ space: 4 }) {
                Text(item.icon.length > 0 ? item.icon + ' ' + item.title : item.title)
                  .fontSize(15)
                  .fontColor('#F0F2FA')
                  .maxLines(2)
                Text(item.updated_at.slice(0, 10) + ' · ' + item.id.slice(0, 8))
                  .fontSize(11)
                  .fontColor('#8A8FA3')
              }
              .width('100%')
              .alignItems(HorizontalAlign.Start)
              .padding(12)
              .backgroundColor('#2A2C45')
              .borderRadius(10)
            }
          }, (item: CatalogEntry) => item.id)
        }
        .width('100%')
        .layoutWeight(1)
      } else {
        Blank()
          .layoutWeight(1)
      }

      Text('正文主权留主控层 · 本端只读目录')
        .fontSize(10)
        .fontColor('#6A6E85')
        .margin({ bottom: 12 })
    }
    .width('100%')
    .height('100%')
    .padding({ left: 16, right: 16 })
    .backgroundColor('#17182A')
  }
}
