// entry/src/main/ets/components/LazyList.ets
// 龍魂 · 懒加载列表组件 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { performanceState, ComponentProfile, MetricType, PerformanceMetric } from '../models/PerformanceModel';

@Component
export struct LazyList<T> {
  @Prop data: T[] = [];
  @Prop itemHeight: number = 56;
  @Prop bufferSize: number = 5;
  @BuilderParam itemBuilder: (item: T, index: number) => void = this.defaultItemBuilder;
  @BuilderParam headerBuilder?: () => void;
  @BuilderParam footerBuilder?: () => void;
  @Prop pageName: string = 'LazyList';

  @State private visibleStart: number = 0;
  @State private visibleEnd: number = 20;
  private componentProfile: ComponentProfile = new ComponentProfile();

  aboutToAppear(): void {
    this.componentProfile = performanceState.getComponentProfile('LazyList', this.pageName);
    const layoutStart = Date.now();
    this.calculateVisibleRange(0, 600);
    this.componentProfile.recordLayout(Date.now() - layoutStart);
  }

  @Builder
  defaultItemBuilder(item: T, index: number): void {
    Text(`Item ${index}`)
  }

  private calculateVisibleRange(scrollOffset: number, containerHeight: number): void {
    const start = Math.max(0, Math.floor(scrollOffset / this.itemHeight) - this.bufferSize);
    const end = Math.min(this.data.length, Math.ceil((scrollOffset + containerHeight) / this.itemHeight) + this.bufferSize);

    if (start !== this.visibleStart || end !== this.visibleEnd) {
      this.visibleStart = start;
      this.visibleEnd = end;
    }
  }

  private getVisibleData(): T[] {
    if (!this.data || this.data.length === 0) return [];
    return this.data.slice(this.visibleStart, this.visibleEnd);
  }

  build() {
    Column() {
      List() {
        if (this.headerBuilder) {
          ListItem() {
            this.headerBuilder()
          }
        }

        LazyForEach(this.getVisibleData(), (item: T, index: number) => {
          ListItem() {
            this.itemBuilder(item, this.visibleStart + index)
          }
          .height(this.itemHeight)
        }, (item: T, index: number) => `lazy-item-${this.visibleStart + index}`)

        if (this.footerBuilder) {
          ListItem() {
            this.footerBuilder()
          }
        }
      }
      .width('100%')
      .layoutWeight(1)
      .scrollBar(BarState.Auto)
      .onScroll((scrollOffset: number) => {
        const containerHeight = 600;
        const layoutStart = Date.now();
        this.calculateVisibleRange(scrollOffset, containerHeight);
        this.componentProfile.recordLayout(Date.now() - layoutStart);
      })
      .onScrollStop(() => {
        const renderStart = Date.now();
        this.componentProfile.recordRender(Date.now() - renderStart);
      })
    }
    .width('100%')
    .height('100%')
  }
}
