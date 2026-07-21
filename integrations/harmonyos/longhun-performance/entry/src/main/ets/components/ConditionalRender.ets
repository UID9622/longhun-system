// entry/src/main/ets/components/ConditionalRender.ets
// 龍魂 · 条件渲染组件 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { performanceState } from '../models/PerformanceModel';

@Component
export struct ConditionalRender {
  @Prop condition: boolean = false;
  @BuilderParam trueBuilder: () => void = this.emptyBuilder;
  @BuilderParam falseBuilder?: () => void;
  @BuilderParam placeholderBuilder?: () => void;
  @Prop deferTime: number = 0;
  @Prop pageName: string = 'ConditionalRender';
  @Prop componentName: string = 'ConditionalRender';

  @State private isReady: boolean = false;
  @State private renderStartTime: number = 0;

  aboutToAppear(): void {
    if (this.deferTime > 0) {
      setTimeout(() => {
        this.isReady = true;
        this.renderStartTime = Date.now();
      }, this.deferTime);
    } else {
      this.isReady = true;
      this.renderStartTime = Date.now();
    }
  }

  aboutToDisappear(): void {
    this.isReady = false;
  }

  @Builder
  emptyBuilder(): void {
    Column().width('100%').height(0)
  }

  @Builder
  defaultPlaceholderBuilder(): void {
    Column() {
      Row() {
        LoadingProgress()
          .width(20)
          .height(20)
          .color('#c41e3a')
      }
      .width('100%')
      .height(40)
      .justifyContent(FlexAlign.Center)
    }
    .width('100%')
    .opacity(0.5)
  }

  build() {
    Column() {
      if (!this.isReady) {
        if (this.placeholderBuilder) {
          this.placeholderBuilder()
        } else {
          this.defaultPlaceholderBuilder()
        }
      } else if (this.condition) {
        this.trueBuilder()
      } else if (this.falseBuilder) {
        this.falseBuilder()
      } else {
        this.emptyBuilder()
      }
    }
    .width('100%')
  }

  // 获取渲染耗时
  getRenderTime(): number {
    if (this.renderStartTime === 0) return 0;
    return Date.now() - this.renderStartTime;
  }
}

// === 延迟渲染包装器 ===
@Component
export struct DeferredRender {
  @Prop delayMs: number = 100;
  @Prop priority: 'high' | 'medium' | 'low' = 'medium';
  @BuilderParam contentBuilder: () => void = this.emptyBuilder;

  @State private isReady: boolean = false;
  private timerId: number = -1;

  aboutToAppear(): void {
    const actualDelay = this.priority === 'high' ? 16 : this.priority === 'medium' ? 50 : 100;
    const delay = Math.max(this.delayMs, actualDelay);

    this.timerId = setTimeout(() => {
      this.isReady = true;
    }, delay);
  }

  aboutToDisappear(): void {
    if (this.timerId !== -1) {
      clearTimeout(this.timerId);
      this.timerId = -1;
    }
  }

  @Builder
  emptyBuilder(): void {
    Column().width('100%').height(0)
  }

  build() {
    if (this.isReady) {
      this.contentBuilder()
    } else {
      this.emptyBuilder()
    }
  }
}

// === 分批渲染组件 ===
@Component
export struct BatchedRender {
  @Prop items: string[] = [];
  @Prop batchSize: number = 10;
  @Prop intervalMs: number = 16;
  @BuilderParam itemBuilder: (item: string, index: number) => void = this.defaultItemBuilder;

  @State private renderedCount: number = 0;
  private batchTimerId: number = -1;

  aboutToAppear(): void {
    this.renderNextBatch();
  }

  aboutToDisappear(): void {
    if (this.batchTimerId !== -1) {
      clearTimeout(this.batchTimerId);
      this.batchTimerId = -1;
    }
  }

  private renderNextBatch(): void {
    if (this.renderedCount >= this.items.length) return;

    this.renderedCount = Math.min(this.renderedCount + this.batchSize, this.items.length);

    if (this.renderedCount < this.items.length) {
      this.batchTimerId = setTimeout(() => {
        this.renderNextBatch();
      }, this.intervalMs);
    }
  }

  @Builder
  defaultItemBuilder(item: string, index: number): void {
    Text(item).fontSize(14).fontColor('#fff')
  }

  build() {
    Column() {
      ForEach(this.items.slice(0, this.renderedCount), (item: string, index: number) => {
        this.itemBuilder(item, index)
      }, (item: string, index: number) => `batch-${index}`)
    }
    .width('100%')
  }
}
