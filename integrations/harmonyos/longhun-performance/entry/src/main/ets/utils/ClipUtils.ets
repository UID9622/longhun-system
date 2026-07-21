// entry/src/main/ets/utils/ClipUtils.ets
// 龍魂 · 裁剪工具类

import { clipState, ClipConfig, ClipType, ClipEffect } from '../models/ClipModel';

export class ClipUtils {
  private static instance: ClipUtils;

  static getInstance(): ClipUtils {
    if (!ClipUtils.instance) ClipUtils.instance = new ClipUtils();
    return ClipUtils.instance;
  }

  // 创建圆形裁剪
  createCircleClip(radius: number): Circle {
    return new Circle({ width: radius * 2, height: radius * 2 });
  }

  // 创建圆角矩形裁剪
  createRoundedClip(width: number, height: number, radius: number): RoundedRect {
    return new RoundedRect({
      width: width,
      height: height,
      topLeft: radius,
      topRight: radius,
      bottomLeft: radius,
      bottomRight: radius
    });
  }

  // 创建椭圆裁剪
  createEllipseClip(width: number, height: number): Ellipse {
    return new Ellipse({ width: width, height: height });
  }

  // 创建矩形裁剪
  createRectClip(width: number, height: number): Rect {
    return new Rect({ width: width, height: height });
  }

  // 计算裁剪后的实际显示区域
  calculateClipArea(
    containerWidth: number,
    containerHeight: number,
    clipType: ClipType,
    params: object
  ): { x: number, y: number, width: number, height: number } {
    switch (clipType) {
      case ClipType.CIRCLE:
        const r = params['circleRadius'] || Math.min(containerWidth, containerHeight) / 2;
        return {
          x: (containerWidth - r * 2) / 2,
          y: (containerHeight - r * 2) / 2,
          width: r * 2,
          height: r * 2
        };
      case ClipType.ROUNDED_RECT:
        return {
          x: 0,
          y: 0,
          width: params['width'] || containerWidth,
          height: params['height'] || containerHeight
        };
      default:
        return { x: 0, y: 0, width: containerWidth, height: containerHeight };
    }
  }

  // 性能优化：预计算裁剪路径
  precomputeClipPath(config: ClipConfig): object {
    const cacheKey = `clip_${config.id}`;
    const cached = clipState.getCache(cacheKey);
    if (cached) return cached;

    let path: object;
    switch (config.type) {
      case ClipType.CIRCLE:
        path = this.createCircleClip(config.params.circleRadius || 50);
        break;
      case ClipType.ROUNDED_RECT:
        const [tl, tr, bl, br] = config.getCornerRadius();
        path = new RoundedRect({
          width: config.params.width || 100,
          height: config.params.height || 100,
          topLeft: tl,
          topRight: tr,
          bottomLeft: bl,
          bottomRight: br
        });
        break;
      default:
        path = this.createRectClip(100, 100);
    }

    clipState.setCache(cacheKey, path);
    return path;
  }

  // 记录裁剪效果
  recordClipEffect(
    config: ClipConfig,
    componentName: string,
    pageName: string,
    renderTime: number
  ): void {
    const effect = new ClipEffect({
      config,
      componentName,
      pageName,
      renderTime,
      pixelCount: this.estimatePixelCount(config)
    });
    clipState.recordEffect(effect);
  }

  // 估算裁剪像素数
  private estimatePixelCount(config: ClipConfig): number {
    switch (config.type) {
      case ClipType.CIRCLE:
        const r = config.params.circleRadius || 50;
        return Math.PI * r * r;
      case ClipType.RECT:
        return (config.params.width || 100) * (config.params.height || 100);
      default:
        return 10000;
    }
  }
}

export const clipUtils = ClipUtils.getInstance();
