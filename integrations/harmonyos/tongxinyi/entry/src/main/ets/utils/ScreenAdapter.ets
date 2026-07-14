/*
 * ==========================================================================
 * 通心译 — 屏幕适配 ✅ 检查项#7
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-SCREEN-v1.0
 * ==========================================================================
 * vp = 虚拟像素 (自动缩放)
 * fp = 字体像素 (跟随系统字号)
 * 鸿蒙底座: 基于 display API 精确适配
 * ==========================================================================
 */

import { display } from '@kit.ArkUI';

export class ScreenAdapter {
  private static density: number = -1;
  private static scaled: number = -1;
  private static screenWidth: number = -1;
  private static screenHeight: number = -1;

  /** 初始化屏幕参数 (首次调用自动初始化) */
  private static ensureInit(): void {
    if (this.density > 0) return;
    try {
      const disp = display.getDefaultDisplaySync();
      this.density = disp.densityPixels;    // 物理像素密度
      this.scaled = disp.scaledDensity;      // 缩放后密度(含系统字号)
      this.screenWidth = disp.width;
      this.screenHeight = disp.height;
    } catch {
      this.density = 160;
      this.scaled = 160;
      this.screenWidth = 1080;
      this.screenHeight = 2340;
    }
  }

  /** vp → px (虚拟像素转物理像素) */
  static vp2px(vp: number): number {
    this.ensureInit();
    return vp * this.density / 160;
  }

  /** fp → px (字体像素转物理像素) */
  static fp2px(fp: number): number {
    this.ensureInit();
    return fp * this.scaled / 160;
  }

  /** px → vp (物理像素转虚拟像素) */
  static px2vp(px: number): number {
    this.ensureInit();
    return px * 160 / this.density;
  }

  /** 获取屏幕宽度 (vp) */
  static getScreenWidth(): number {
    this.ensureInit();
    return this.screenWidth * 160 / this.density;
  }

  /** 获取屏幕高度 (vp) */
  static getScreenHeight(): number {
    this.ensureInit();
    return this.screenHeight * 160 / this.density;
  }

  /** 判断是否为平板/折叠屏 (≥600vp 为平板) */
  static isTablet(): boolean {
    return this.getScreenWidth() >= 600;
  }

  /** 获取屏幕断点: compact(手机) / medium(折叠屏) / expanded(平板) */
  static getBreakpoint(): 'compact' | 'medium' | 'expanded' {
    const width = this.getScreenWidth();
    if (width < 600) return 'compact';
    if (width < 840) return 'medium';
    return 'expanded';
  }
}
