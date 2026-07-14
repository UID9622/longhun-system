// entry/src/main/ets/components/AsyncImage.ets
// 龍魂 · 异步图片组件 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { performanceState } from '../models/PerformanceModel';

@Component
export struct AsyncImage {
  @Prop src: string = '';
  @Prop width: number = 100;
  @Prop height: number = 100;
  @Prop placeholder: Resource = $r('app.media.placeholder');
  @Prop borderRadius: number = 8;
  @Prop objectFit: ImageFit = ImageFit.Cover;
  @Prop showLoadingIndicator: boolean = true;
  @Prop cacheEnabled: boolean = true;
  @Prop animationDuration: number = 300;

  @State private isLoaded: boolean = false;
  @State private isLoading: boolean = false;
  @State private loadError: boolean = false;

  private static imageCache: Map<string, boolean> = new Map();
  private static readonly MAX_CACHE_SIZE: number = 200;

  aboutToAppear(): void {
    this.loadImage();
  }

  aboutToDisappear(): void {
    // 组件销毁时清理
  }

  async loadImage(): Promise<void> {
    if (!this.src) {
      this.loadError = true;
      return;
    }

    this.isLoading = true;
    this.loadError = false;

    // 检查内存缓存
    if (this.cacheEnabled) {
      const cached = AsyncImage.getFromCache(this.src);
      if (cached) {
        this.isLoaded = true;
        this.isLoading = false;
        return;
      }
    }

    // 异步加载图片
    try {
      // 鸿蒙原生：使用 image.createImageSource 异步加载
      // const imageSource = image.createImageSource(this.src);
      // const pixelMap = await imageSource.createPixelMap();

      // 模拟异步加载
      await this.delay(50 + Math.random() * 150);
      this.isLoaded = true;
      this.isLoading = false;

      if (this.cacheEnabled) {
        AsyncImage.saveToCache(this.src);
      }
    } catch (error) {
      console.error(`[龍魂] 图片加载失败: ${this.src}`, error);
      this.isLoading = false;
      this.loadError = true;
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise<void>((resolve) => {
      setTimeout(() => resolve(), ms);
    });
  }

  static getFromCache(src: string): boolean {
    return AsyncImage.imageCache.has(src);
  }

  static saveToCache(src: string): void {
    if (AsyncImage.imageCache.size >= AsyncImage.MAX_CACHE_SIZE) {
      // LRU策略：删除第一个缓存项
      const firstKey = AsyncImage.imageCache.keys().next().value;
      if (firstKey) {
        AsyncImage.imageCache.delete(firstKey);
      }
    }
    AsyncImage.imageCache.set(src, true);
  }

  static clearCache(): void {
    AsyncImage.imageCache.clear();
  }

  static getCacheSize(): number {
    return AsyncImage.imageCache.size;
  }

  build() {
    Stack() {
      // 占位图 - 未加载或加载失败时显示
      if (!this.isLoaded || this.loadError) {
        Column() {
          if (this.isLoading && this.showLoadingIndicator) {
            Image(this.placeholder)
              .width(this.width)
              .height(this.height)
              .objectFit(ImageFit.Cover)
              .borderRadius(this.borderRadius)
              .opacity(0.3)

            LoadingProgress()
              .width(24)
              .height(24)
              .color('#c41e3a')
          } else if (this.loadError) {
            Image(this.placeholder)
              .width(this.width)
              .height(this.height)
              .objectFit(ImageFit.Cover)
              .borderRadius(this.borderRadius)
              .opacity(0.5)

            Text('加载失败')
              .fontSize(10)
              .fontColor('#ff4444')
          } else {
            Image(this.placeholder)
              .width(this.width)
              .height(this.height)
              .objectFit(ImageFit.Cover)
              .borderRadius(this.borderRadius)
              .opacity(0.3)
          }
        }
        .width(this.width)
        .height(this.height)
        .justifyContent(FlexAlign.Center)
        .alignItems(HorizontalAlign.Center)
        .backgroundColor('rgba(255,255,255,0.05)')
        .borderRadius(this.borderRadius)
      }

      // 实际图片 - 加载完成后显示
      Image(this.src)
        .width(this.width)
        .height(this.height)
        .objectFit(this.objectFit)
        .borderRadius(this.borderRadius)
        .opacity(this.isLoaded && !this.loadError ? 1 : 0)
        .animation({
          duration: this.animationDuration,
          curve: Curve.EaseInOut
        })
    }
    .width(this.width)
    .height(this.height)
  }
}
