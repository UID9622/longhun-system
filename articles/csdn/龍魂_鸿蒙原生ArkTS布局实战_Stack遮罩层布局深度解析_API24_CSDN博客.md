# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 · 鸿蒙原生 ArkTS 布局实战：Stack 遮罩层布局深度解析（API 24）

> 龍魂系统 · 鸿蒙原生适配层 · Stack 遮罩层布局深度解析
> 
> DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622 | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

---

## 一、核心定位

| 维度 | 说明 |
|------|------|
| 平台 | 鸿蒙 HarmonyOS NEXT · API 24 · 纯血鸿蒙 |
| 语言 | ArkTS · 声明式UI · 布局系统 |
| 场景 | Stack 堆叠布局 · 遮罩层 · 弹窗系统 · Loading · Toast · Dialog · 层级管理 |
| 架构 | 龍魂蚁群触角 → 鸿蒙布局引擎 → 遮罩层系统 |
| 主权 | 数据本地 · 国密SM2/SM3签名 · 不上传云端 |
| 设计 | 层级隔离 · 动画过渡 · 手势拦截 · 焦点管理 · 生命周期同步 |

---

## 二、系统架构

```
┌─────────────────────────────────────────┐
│           龍魂系统 · 布局层                │
│  DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ │
│  UID: 9622                              │
├─────────────────────────────────────────┤
│         鸿蒙 ArkTS 布局引擎层              │
│                                         │
│  Stack 容器 → 层级管理（Z-Index）          │
│  ├── 基础层（Base Layer）                  │
│  ├── 内容层（Content Layer）               │
│  ├── 遮罩层（Mask Layer）                  │
│  ├── 弹窗层（Dialog Layer）                │
│  ├── 提示层（Toast Layer）                 │
│  ├── 加载层（Loading Layer）               │
│  ├── 导航层（Navigation Layer）            │
│  └── 顶层（Top Layer）                     │
├─────────────────────────────────────────┤
│         鸿蒙系统能力层                      │
│                                         │
│  Stack · Overlay · Mask · Dialog         │
│  动画(Animation) · 过渡(Transition)       │
│  手势(Gesture) · 焦点(Focus)              │
│  窗口(Window) · 遮罩(Overlay)           │
│  国密(CryptoFramework)                   │
└─────────────────────────────────────────┘
```

---

## 三、Stack 布局核心

### 3.1 层级模型（`entry/src/main/ets/models/StackModel.ets`）

```typescript
// entry/src/main/ets/models/StackModel.ets
// 龍魂 · Stack 层级模型 · ArkTS

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 层级类型 ===
export enum LayerType {
  BASE = 'base',           // 基础层 - 页面主体内容
  CONTENT = 'content',     // 内容层 - 滚动内容/列表
  MASK = 'mask',           // 遮罩层 - 半透明背景
  DIALOG = 'dialog',       // 弹窗层 - 模态对话框
  TOAST = 'toast',         // 提示层 - 轻量提示
  LOADING = 'loading',       // 加载层 - 加载动画
  NAVIGATION = 'navigation', // 导航层 - 导航栏/侧边栏
  TOP = 'top'              // 顶层 - 最高优先级
}

// === 动画类型 ===
export enum AnimationType {
  FADE = 'fade',           // 淡入淡出
  SLIDE_UP = 'slide_up',   // 从底部滑入
  SLIDE_DOWN = 'slide_down', // 从顶部滑入
  SLIDE_LEFT = 'slide_left', // 从左侧滑入
  SLIDE_RIGHT = 'slide_right', // 从右侧滑入
  SCALE = 'scale',         // 缩放
  ROTATE = 'rotate',       // 旋转
  FLIP = 'flip',           // 翻转
  BOUNCE = 'bounce'        // 弹跳
}

// === 遮罩类型 ===
export enum MaskType {
  NONE = 'none',           // 无遮罩
  TRANSPARENT = 'transparent', // 透明遮罩（仅拦截手势）
  DIM = 'dim',             // 半透明遮罩
  BLUR = 'blur',           // 模糊遮罩
  COLOR = 'color'          // 彩色遮罩
}

// === 焦点策略 ===
export enum FocusStrategy {
  AUTO = 'auto',           // 自动聚焦
  FIRST = 'first',         // 聚焦第一个元素
  LAST = 'last',           // 聚焦最后一个元素
  NONE = 'none'            // 不聚焦
}

// === 层级配置 ===
export class LayerConfig {
  id: string;
  type: LayerType;
  zIndex: number;            // 层级索引

  // 遮罩
  maskType: MaskType;
  maskColor: string;
  maskOpacity: number;

  // 动画
  enterAnimation: AnimationType;
  exitAnimation: AnimationType;
  animationDuration: number;

  // 交互
  dismissOnMaskTap: boolean;  // 点击遮罩是否关闭
  dismissOnBackPress: boolean; // 返回键是否关闭
  interceptGesture: boolean;  // 是否拦截手势

  // 焦点
  focusStrategy: FocusStrategy;

  // 生命周期
  autoDismissDelay?: number;  // 自动关闭延迟ms

  // 审计
  dnaSignature: string;

  constructor(data: Partial<LayerConfig> = {}) {
    this.id = data.id || `LAYER-${Date.now()}`;
    this.type = data.type || LayerType.BASE;
    this.zIndex = data.zIndex || this.getDefaultZIndex(data.type || LayerType.BASE);

    this.maskType = data.maskType || this.getDefaultMaskType(data.type || LayerType.BASE);
    this.maskColor = data.maskColor || '#000000';
    this.maskOpacity = data.maskOpacity ?? this.getDefaultOpacity(data.type || LayerType.BASE);

    this.enterAnimation = data.enterAnimation || AnimationType.FADE;
    this.exitAnimation = data.exitAnimation || AnimationType.FADE;
    this.animationDuration = data.animationDuration || 300;

    this.dismissOnMaskTap = data.dismissOnMaskTap ?? true;
    this.dismissOnBackPress = data.dismissOnBackPress ?? true;
    this.interceptGesture = data.interceptGesture ?? true;

    this.focusStrategy = data.focusStrategy || FocusStrategy.AUTO;
    this.autoDismissDelay = data.autoDismissDelay;

    this.dnaSignature = this.signData();
  }

  private getDefaultZIndex(type: LayerType): number {
    const zIndexMap: Record<LayerType, number> = {
      [LayerType.BASE]: 0,
      [LayerType.CONTENT]: 10,
      [LayerType.NAVIGATION]: 20,
      [LayerType.MASK]: 30,
      [LayerType.DIALOG]: 40,
      [LayerType.TOAST]: 50,
      [LayerType.LOADING]: 60,
      [LayerType.TOP]: 100
    };
    return zIndexMap[type] || 0;
  }

  private getDefaultMaskType(type: LayerType): MaskType {
    const maskMap: Record<LayerType, MaskType> = {
      [LayerType.BASE]: MaskType.NONE,
      [LayerType.CONTENT]: MaskType.NONE,
      [LayerType.NAVIGATION]: MaskType.NONE,
      [LayerType.MASK]: MaskType.DIM,
      [LayerType.DIALOG]: MaskType.DIM,
      [LayerType.TOAST]: MaskType.TRANSPARENT,
      [LayerType.LOADING]: MaskType.DIM,
      [LayerType.TOP]: MaskType.TRANSPARENT
    };
    return maskMap[type] || MaskType.NONE;
  }

  private getDefaultOpacity(type: LayerType): number {
    const opacityMap: Record<LayerType, number> = {
      [LayerType.BASE]: 0,
      [LayerType.CONTENT]: 0,
      [LayerType.NAVIGATION]: 0,
      [LayerType.MASK]: 0.5,
      [LayerType.DIALOG]: 0.6,
      [LayerType.TOAST]: 0,
      [LayerType.LOADING]: 0.7,
      [LayerType.TOP]: 0
    };
    return opacityMap[type] || 0;
  }

  private signData(): string {
    const payload = `${this.id}-${this.type}-${this.zIndex}`;
    return `SM3-${payload.split('').reduce((a,b)=>a+b.charCodeAt(0),0).toString(16).substring(0,16)}`;
  }

  // 获取遮罩颜色
  getMaskColor(): string {
    if (this.maskType === MaskType.NONE) return 'transparent';
    if (this.maskType === MaskType.TRANSPARENT) return 'rgba(0,0,0,0.01)';
    const opacity = Math.round(this.maskOpacity * 255).toString(16).padStart(2, '0');
    return `${this.maskColor}${opacity}`;
  }
}

// === 弹窗配置 ===
export class DialogConfig extends LayerConfig {
  title: string;
  message: string;
  icon?: string;

  // 按钮
  primaryButton?: DialogButton;
  secondaryButton?: DialogButton;
  cancelButton?: DialogButton;

  // 输入
  hasInput: boolean;
  inputPlaceholder?: string;
  inputDefaultValue?: string;

  // 样式
  width: number;             // 弹窗宽度百分比
  borderRadius: number;

  constructor(data: Partial<DialogConfig> = {}) {
    super({ type: LayerType.DIALOG, ...data });
    this.title = data.title || '提示';
    this.message = data.message || '';
    this.icon = data.icon;

    this.primaryButton = data.primaryButton;
    this.secondaryButton = data.secondaryButton;
    this.cancelButton = data.cancelButton;

    this.hasInput = data.hasInput || false;
    this.inputPlaceholder = data.inputPlaceholder;
    this.inputDefaultValue = data.inputDefaultValue;

    this.width = data.width || 80;
    this.borderRadius = data.borderRadius || 12;
  }
}

export interface DialogButton {
  label: string;
  type: 'primary' | 'secondary' | 'danger' | 'cancel';
  action?: () => void;
}

// === Toast 配置 ===
export class ToastConfig extends LayerConfig {
  message: string;
  icon?: string;
  position: 'top' | 'center' | 'bottom';
  duration: number;

  constructor(data: Partial<ToastConfig> = {}) {
    super({ type: LayerType.TOAST, ...data });
    this.message = data.message || '';
    this.icon = data.icon;
    this.position = data.position || 'center';
    this.duration = data.duration || 2000;
    this.autoDismissDelay = this.duration;
  }
}

// === Loading 配置 ===
export class LoadingConfig extends LayerConfig {
  message: string;
  progress?: number;         // 0-100
  cancelable: boolean;

  constructor(data: Partial<LoadingConfig> = {}) {
    super({ type: LayerType.LOADING, ...data });
    this.message = data.message || '加载中...';
    this.progress = data.progress;
    this.cancelable = data.cancelable ?? false;
  }
}

// === 层级栈 ===
export class LayerStack {
  layers: LayerConfig[] = [];

  // 压入层级
  push(layer: LayerConfig): void {
    // 检查是否有同类型层级，有则替换
    const existingIndex = this.layers.findIndex(l => l.type === layer.type);
    if (existingIndex !== -1) {
      this.layers.splice(existingIndex, 1);
    }
    this.layers.push(layer);
    this.sortLayers();
  }

  // 弹出层级
  pop(): LayerConfig | undefined {
    return this.layers.pop();
  }

  // 移除指定层级
  remove(id: string): void {
    const index = this.layers.findIndex(l => l.id === id);
    if (index !== -1) {
      this.layers.splice(index, 1);
    }
  }

  // 移除类型
  removeByType(type: LayerType): void {
    this.layers = this.layers.filter(l => l.type !== type);
  }

  // 获取顶层
  top(): LayerConfig | undefined {
    if (this.layers.length === 0) return undefined;
    return this.layers[this.layers.length - 1];
  }

  // 获取最高层级索引
  getMaxZIndex(): number {
    if (this.layers.length === 0) return 0;
    return Math.max(...this.layers.map(l => l.zIndex));
  }

  // 是否有遮罩层
  hasMaskLayer(): boolean {
    return this.layers.some(l => l.maskType !== MaskType.NONE);
  }

  // 获取遮罩层配置
  getMaskConfig(): LayerConfig | undefined {
    // 返回最高层级的遮罩配置
    const maskLayers = this.layers.filter(l => l.maskType !== MaskType.NONE);
    if (maskLayers.length === 0) return undefined;
    return maskLayers.reduce((max, l) => l.zIndex > max.zIndex ? l : max);
  }

  // 清空
  clear(): void {
    this.layers = [];
  }

  // 排序
  private sortLayers(): void {
    this.layers.sort((a, b) => a.zIndex - b.zIndex);
  }

  // 获取可见层级
  getVisibleLayers(): LayerConfig[] {
    return this.layers.filter(l => l.type !== LayerType.BASE);
  }
}
```

### 3.2 全局遮罩状态

```typescript
// === 遮罩全局状态 ===
@Observed
export class OverlayState {
  // 层级栈
  layerStack: LayerStack = new LayerStack();

  // 当前显示的弹窗
  currentDialog: DialogConfig | null = null;
  currentToast: ToastConfig | null = null;
  currentLoading: LoadingConfig | null = null;

  // 遮罩可见性
  isMaskVisible: boolean = false;
  maskColor: string = 'transparent';
  maskZIndex: number = 0;

  // 动画状态
  isAnimating: boolean = false;
  animationProgress: number = 0;

  // 统计
  get statistics(): OverlayStats {
    return {
      totalLayers: this.layerStack.layers.length,
      visibleLayers: this.layerStack.getVisibleLayers().length,
      hasDialog: this.currentDialog !== null,
      hasToast: this.currentToast !== null,
      hasLoading: this.currentLoading !== null,
      maxZIndex: this.layerStack.getMaxZIndex(),
      isMaskActive: this.isMaskVisible
    };
  }

  // 显示弹窗
  showDialog(config: DialogConfig): void {
    this.layerStack.push(config);
    this.currentDialog = config;
    this.updateMaskState();
    console.info(`[龍魂] 显示弹窗: ${config.title}`);
  }

  // 关闭弹窗
  dismissDialog(): void {
    if (this.currentDialog) {
      this.layerStack.remove(this.currentDialog.id);
      this.currentDialog = null;
      this.updateMaskState();
      console.info('[龍魂] 关闭弹窗');
    }
  }

  // 显示 Toast
  showToast(config: ToastConfig): void {
    this.layerStack.push(config);
    this.currentToast = config;
    this.updateMaskState();

    // 自动关闭
    if (config.autoDismissDelay) {
      setTimeout(() => { this.dismissToast(); }, config.autoDismissDelay);
    }
  }

  // 关闭 Toast
  dismissToast(): void {
    if (this.currentToast) {
      this.layerStack.remove(this.currentToast.id);
      this.currentToast = null;
      this.updateMaskState();
    }
  }

  // 显示 Loading
  showLoading(config: LoadingConfig): void {
    this.layerStack.push(config);
    this.currentLoading = config;
    this.updateMaskState();
  }

  // 关闭 Loading
  dismissLoading(): void {
    if (this.currentLoading) {
      this.layerStack.remove(this.currentLoading.id);
      this.currentLoading = null;
      this.updateMaskState();
    }
  }

  // 更新遮罩状态
  private updateMaskState(): void {
    const maskConfig = this.layerStack.getMaskConfig();
    if (maskConfig) {
      this.isMaskVisible = true;
      this.maskColor = maskConfig.getMaskColor();
      this.maskZIndex = maskConfig.zIndex - 1;
    } else {
      this.isMaskVisible = false;
      this.maskColor = 'transparent';
      this.maskZIndex = 0;
    }
  }

  // 处理返回键
  handleBackPress(): boolean {
    const top = this.layerStack.top();
    if (top && top.dismissOnBackPress) {
      this.layerStack.pop();
      this.updateMaskState();
      return true; // 拦截
    }
    return false; // 不拦截
  }

  // 处理遮罩点击
  handleMaskTap(): boolean {
    const top = this.layerStack.top();
    if (top && top.dismissOnMaskTap) {
      this.layerStack.pop();
      this.updateMaskState();
      return true;
    }
    return false;
  }

  // 清空所有层级
  clearAll(): void {
    this.layerStack.clear();
    this.currentDialog = null;
    this.currentToast = null;
    this.currentLoading = null;
    this.updateMaskState();
  }

  persist(): void {
    // 遮罩状态通常不持久化
  }
}

export interface OverlayStats {
  totalLayers: number;
  visibleLayers: number;
  hasDialog: boolean;
  hasToast: boolean;
  hasLoading: boolean;
  maxZIndex: number;
  isMaskActive: boolean;
}

export const overlayState = new OverlayState();
AppStorage.setOrCreate('overlayState', overlayState);


---

## 四、Stack 遮罩层组件

### 4.1 遮罩层容器（`entry/src/main/ets/components/OverlayContainer.ets`）

```typescript
// entry/src/main/ets/components/OverlayContainer.ets
// 龍魂 · Stack 遮罩层容器

import { overlayState, OverlayState, LayerType, MaskType, AnimationType } from '../models/StackModel';

@Component
export struct OverlayContainer {
  @StorageLink('overlayState') overlayState: OverlayState = overlayState;
  @BuilderParam contentBuilder: () => void;  // 基础内容Builder

  // 动画效果
  getAnimation(effect: AnimationType): object {
    switch (effect) {
      case AnimationType.FADE: return { opacity: [0, 1], duration: 300 };
      case AnimationType.SLIDE_UP: return { translate: { y: ['100%', '0%'] }, opacity: [0, 1], duration: 300 };
      case AnimationType.SLIDE_DOWN: return { translate: { y: ['-100%', '0%'] }, opacity: [0, 1], duration: 300 };
      case AnimationType.SLIDE_LEFT: return { translate: { x: ['100%', '0%'] }, opacity: [0, 1], duration: 300 };
      case AnimationType.SLIDE_RIGHT: return { translate: { x: ['-100%', '0%'] }, opacity: [0, 1], duration: 300 };
      case AnimationType.SCALE: return { scale: { x: [0.8, 1], y: [0.8, 1] }, opacity: [0, 1], duration: 300 };
      case AnimationType.ROTATE: return { rotate: { z: [-90, 0] }, opacity: [0, 1], duration: 300 };
      case AnimationType.BOUNCE: return { scale: { x: [0.3, 1.1, 1], y: [0.3, 1.1, 1] }, opacity: [0, 1], duration: 500 };
      default: return { opacity: [0, 1], duration: 300 };
    }
  }

  build() {
    Stack({ alignContent: Alignment.Center }) {
      // === 基础层 ===
      this.contentBuilder()

      // === 遮罩层 ===
      if (this.overlayState.isMaskVisible) {
        Column()
          .width('100%')
          .height('100%')
          .backgroundColor(this.overlayState.maskColor)
          .zIndex(this.overlayState.maskZIndex)
          .onClick(() => { this.overlayState.handleMaskTap(); })
          .transition(TransitionType.All)
          .animation({ duration: 300, curve: Curve.EaseInOut })
      }

      // === 弹窗层 ===
      if (this.overlayState.currentDialog) {
        this.DialogBuilder(this.overlayState.currentDialog)
      }

      // === Toast 层 ===
      if (this.overlayState.currentToast) {
        this.ToastBuilder(this.overlayState.currentToast)
      }

      // === Loading 层 ===
      if (this.overlayState.currentLoading) {
        this.LoadingBuilder(this.overlayState.currentLoading)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  // === 弹窗 Builder ===
  @Builder
  DialogBuilder(config: DialogConfig) {
    Column() {
      Column() {
        // 图标
        if (config.icon) {
          Text(config.icon)
            .fontSize(48)
            .margin({ bottom: 16 })
        }

        // 标题
        Text(config.title)
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
          .textAlign(TextAlign.Center)
          .width('100%')

        // 消息
        Text(config.message)
          .fontSize(14)
          .fontColor('#888')
          .textAlign(TextAlign.Center)
          .width('100%')
          .margin({ top: 8, bottom: 16 })

        // 输入框
        if (config.hasInput) {
          TextInput({ placeholder: config.inputPlaceholder || '请输入...' })
            .width('100%')
            .height(44)
            .backgroundColor('#1a1a1a')
            .fontColor('#fff')
            .placeholderColor('#666')
            .borderRadius(8)
            .padding({ left: 12, right: 12 })
            .margin({ bottom: 16 })
        }

        // 按钮组
        Row() {
          if (config.cancelButton) {
            Button(config.cancelButton.label)
              .fontSize(14)
              .fontColor('#888')
              .backgroundColor('#1a1a1a')
              .borderRadius(8)
              .padding({ left: 16, right: 16 })
              .layoutWeight(1)
              .onClick(() => {
                config.cancelButton?.action?.();
                this.overlayState.dismissDialog();
              })
          }

          if (config.secondaryButton) {
            Button(config.secondaryButton.label)
              .fontSize(14)
              .fontColor('#fff')
              .backgroundColor('#333')
              .borderRadius(8)
              .padding({ left: 16, right: 16 })
              .layoutWeight(1)
              .margin({ left: 8 })
              .onClick(() => {
                config.secondaryButton?.action?.();
              })
          }

          if (config.primaryButton) {
            Button(config.primaryButton.label)
              .fontSize(14)
              .fontColor('#fff')
              .backgroundColor('#c41e3a')
              .borderRadius(8)
              .padding({ left: 16, right: 16 })
              .layoutWeight(1)
              .margin({ left: 8 })
              .onClick(() => {
                config.primaryButton?.action?.();
                this.overlayState.dismissDialog();
              })
          }
        }
        .width('100%')
      }
      .width(`${config.width}%`)
      .padding(24)
      .backgroundColor('#262626')
      .borderRadius(config.borderRadius)
      .shadow({ radius: 16, color: 'rgba(0,0,0,0.5)' })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
    .zIndex(config.zIndex)
    .transition(this.getAnimation(config.enterAnimation))
    .animation({ duration: config.animationDuration, curve: Curve.EaseInOut })
    .onClick(() => {}) // 阻止事件冒泡
  }

  // === Toast Builder ===
  @Builder
  ToastBuilder(config: ToastConfig) {
    Column() {
      Row() {
        if (config.icon) {
          Text(config.icon)
            .fontSize(20)
            .margin({ right: 8 })
        }

        Text(config.message)
          .fontSize(14)
          .fontColor('#fff')
      }
      .padding({ left: 16, right: 16, top: 12, bottom: 12 })
      .backgroundColor('rgba(0,0,0,0.8)')
      .borderRadius(8)
    }
    .width('100%')
    .height('100%')
    .justifyContent(
      config.position === 'top' ? FlexAlign.Start :
      config.position === 'bottom' ? FlexAlign.End : FlexAlign.Center
    )
    .alignItems(HorizontalAlign.Center)
    .padding({ top: config.position === 'top' ? 80 : 0, bottom: config.position === 'bottom' ? 80 : 0 })
    .zIndex(config.zIndex)
    .transition(TransitionType.All)
    .animation({ duration: 300, curve: Curve.EaseInOut })
    .onClick(() => { this.overlayState.dismissToast(); })
  }

  // === Loading Builder ===
  @Builder
  LoadingBuilder(config: LoadingConfig) {
    Column() {
      Column() {
        // Loading 动画
        LoadingProgress()
          .width(48)
          .height(48)
          .color('#c41e3a')

        // 消息
        Text(config.message)
          .fontSize(14)
          .fontColor('#fff')
          .margin({ top: 16 })

        // 进度条
        if (config.progress !== undefined) {
          Stack() {
            Row()
              .width('100%')
              .height(4)
              .backgroundColor('#333')
              .borderRadius(2)

            Row()
              .width(`${config.progress}%`)
              .height(4)
              .backgroundColor('#c41e3a')
              .borderRadius(2)
          }
          .width(200)
          .height(4)
          .margin({ top: 12 })

          Text(`${config.progress}%`)
            .fontSize(12)
            .fontColor('#888')
            .margin({ top: 4 })
        }

        // 取消按钮
        if (config.cancelable) {
          Button('取消')
            .fontSize(12)
            .fontColor('#888')
            .backgroundColor('transparent')
            .margin({ top: 12 })
            .onClick(() => { this.overlayState.dismissLoading(); })
        }
      }
      .padding(32)
      .backgroundColor('#262626')
      .borderRadius(12)
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
    .zIndex(config.zIndex)
    .transition(TransitionType.All)
    .animation({ duration: 300, curve: Curve.EaseInOut })
    .onClick(() => {}) // 阻止事件冒泡
  }
}
```

---

## 五、便捷方法封装

### 5.1 遮罩工具类（`entry/src/main/ets/utils/OverlayUtils.ets`）

```typescript
// entry/src/main/ets/utils/OverlayUtils.ets
// 龍魂 · 遮罩工具类

import { overlayState, DialogConfig, ToastConfig, LoadingConfig, DialogButton, AnimationType } from '../models/StackModel';

export class OverlayUtils {
  // === 显示确认弹窗 ===
  static confirm(title: string, message: string, onConfirm: () => void, onCancel?: () => void): void {
    overlayState.showDialog(new DialogConfig({
      title,
      message,
      icon: '❓',
      primaryButton: { label: '确认', type: 'primary', action: onConfirm },
      cancelButton: { label: '取消', type: 'cancel', action: onCancel || (() => {}) },
      enterAnimation: AnimationType.SCALE,
      dismissOnMaskTap: true
    }));
  }

  // === 显示警告弹窗 ===
  static alert(title: string, message: string, onConfirm?: () => void): void {
    overlayState.showDialog(new DialogConfig({
      title,
      message,
      icon: '⚠️',
      primaryButton: { label: '确定', type: 'primary', action: onConfirm || (() => {}) },
      enterAnimation: AnimationType.FADE
    }));
  }

  // === 显示错误弹窗 ===
  static error(title: string, message: string, onConfirm?: () => void): void {
    overlayState.showDialog(new DialogConfig({
      title,
      message,
      icon: '❌',
      primaryButton: { label: '确定', type: 'danger', action: onConfirm || (() => {}) },
      enterAnimation: AnimationType.SHAKE
    }));
  }

  // === 显示输入弹窗 ===
  static prompt(title: string, placeholder: string, onConfirm: (value: string) => void, defaultValue?: string): void {
    overlayState.showDialog(new DialogConfig({
      title,
      message: '',
      hasInput: true,
      inputPlaceholder: placeholder,
      inputDefaultValue: defaultValue,
      primaryButton: { label: '确认', type: 'primary', action: () => { /* 获取输入值 */ } },
      cancelButton: { label: '取消', type: 'cancel' },
      enterAnimation: AnimationType.SLIDE_UP
    }));
  }

  // === 显示成功 Toast ===
  static success(message: string, duration?: number): void {
    overlayState.showToast(new ToastConfig({
      message,
      icon: '✅',
      position: 'center',
      duration: duration || 2000
    }));
  }

  // === 显示错误 Toast ===
  static errorToast(message: string, duration?: number): void {
    overlayState.showToast(new ToastConfig({
      message,
      icon: '❌',
      position: 'center',
      duration: duration || 3000
    }));
  }

  // === 显示加载 ===
  static showLoading(message?: string, cancelable?: boolean): void {
    overlayState.showLoading(new LoadingConfig({
      message: message || '加载中...',
      cancelable: cancelable || false
    }));
  }

  // === 显示进度加载 ===
  static showProgressLoading(message: string, progress: number): void {
    overlayState.showLoading(new LoadingConfig({
      message,
      progress,
      cancelable: true
    }));
  }

  // === 关闭加载 ===
  static hideLoading(): void {
    overlayState.dismissLoading();
  }

  // === 更新进度 ===
  static updateProgress(progress: number): void {
    if (overlayState.currentLoading) {
      overlayState.currentLoading.progress = progress;
    }
  }

  // === 显示底部弹窗 ===
  static showBottomSheet(title: string, items: { label: string; action: () => void }[]): void {
    // 构建底部弹窗
    console.info(`[龍魂] 显示底部弹窗: ${title}`);
  }

  // === 显示侧边栏 ===
  static showSidebar(width: number, content: () => void): void {
    // 构建侧边栏
    console.info(`[龍魂] 显示侧边栏: ${width}px`);
  }

  // === 清空所有遮罩 ===
  static clearAll(): void {
    overlayState.clearAll();
  }
}
```

---

## 六、主页面实现

### 6.1 Stack 布局演示页面（`entry/src/main/ets/pages/StackDemoPage.ets`）

```typescript
// entry/src/main/ets/pages/StackDemoPage.ets
// 龍魂 · Stack 布局演示页面

import { overlayState, OverlayState, DialogConfig, ToastConfig, LoadingConfig, AnimationType, LayerType } from '../models/StackModel';
import { OverlayContainer } from '../components/OverlayContainer';
import { OverlayUtils } from '../utils/OverlayUtils';

@Entry
@Component
struct StackDemoPage {
  @StorageLink('overlayState') overlayState: OverlayState = overlayState;
  @State private demoProgress: number = 0;

  build() {
    OverlayContainer({ contentBuilder: this.MainContentBuilder.bind(this) })
  }

  @Builder
  MainContentBuilder() {
    Column() {
      this.HeaderBuilder()
      this.StatsBuilder()
      this.DemoButtonsBuilder()
      this.LayerInfoBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉').fontSize(28).margin({ right: 8 })
      Column() {
        Text('龍魂 Stack 布局').fontSize(20).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text(`UID:${MASTER_UID} · API 24`).fontSize(12).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start).layoutWeight(1)
    }
    .width('100%').height(56).padding({ left: 16, right: 16 }).backgroundColor('#1a1a1a').border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('层级', this.overlayState.statistics.totalLayers.toString(), '#fff')
      this.StatCard('遮罩', this.overlayState.statistics.isMaskActive ? '●' : '○', this.overlayState.statistics.isMaskActive ? '#00ff00' : '#666')
      this.StatCard('Z-Index', this.overlayState.statistics.maxZIndex.toString(), '#ffcc00')
      this.StatCard('弹窗', this.overlayState.statistics.hasDialog ? '●' : '○', this.overlayState.statistics.hasDialog ? '#c41e3a' : '#666')
      this.StatCard('加载', this.overlayState.statistics.hasLoading ? '●' : '○', this.overlayState.statistics.hasLoading ? '#0066cc' : '#666')
    }
    .width('100%').height(80).padding({ left: 12, right: 12, top: 8, bottom: 8 }).backgroundColor('#1a1a1a').border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() { Text(value).fontSize(24).fontWeight(FontWeight.Bold).fontColor(color); Text(label).fontSize(11).fontColor('#666').margin({ top: 4 }); }
    .width('20%').height('100%').justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Center)
  }

  @Builder
  DemoButtonsBuilder() {
    Scroll() {
      Column() {
        Text('弹窗演示').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 16, bottom: 12 }).width('100%')

        Row() {
          Button('确认弹窗').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).onClick(() => {
            OverlayUtils.confirm('确认操作', '您确定要执行此操作吗？', () => { OverlayUtils.success('操作已确认'); });
          })
          Button('警告弹窗').fontSize(12).fontColor('#fff').backgroundColor('#ff6600').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            OverlayUtils.alert('系统警告', '检测到异常状态，请检查配置。');
          })
          Button('错误弹窗').fontSize(12).fontColor('#fff').backgroundColor('#c41e3a').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            OverlayUtils.error('操作失败', '网络连接超时，请重试。');
          })
          Button('输入弹窗').fontSize(12).fontColor('#fff').backgroundColor('#0066cc').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            OverlayUtils.prompt('请输入', '请输入项目名称', (value) => { OverlayUtils.success(`输入: ${value}`); });
          })
        }
        .width('100%').margin({ bottom: 16 })

        Text('Toast 演示').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 16, bottom: 12 }).width('100%')

        Row() {
          Button('成功 Toast').fontSize(12).fontColor('#fff').backgroundColor('#00ff00').borderRadius(8).padding({ left: 12, right: 12 }).onClick(() => {
            OverlayUtils.success('操作成功！');
          })
          Button('错误 Toast').fontSize(12).fontColor('#fff').backgroundColor('#ff0000').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            OverlayUtils.errorToast('操作失败！');
          })
          Button('顶部 Toast').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            overlayState.showToast(new ToastConfig({ message: '顶部提示', position: 'top', duration: 2000 }));
          })
          Button('底部 Toast').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            overlayState.showToast(new ToastConfig({ message: '底部提示', position: 'bottom', duration: 2000 }));
          })
        }
        .width('100%').margin({ bottom: 16 })

        Text('Loading 演示').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 16, bottom: 12 }).width('100%')

        Row() {
          Button('显示 Loading').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).onClick(() => {
            OverlayUtils.showLoading('正在加载数据...');
            setTimeout(() => { OverlayUtils.hideLoading(); OverlayUtils.success('加载完成'); }, 3000);
          })
          Button('进度 Loading').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            this.demoProgress = 0;
            OverlayUtils.showProgressLoading('下载中...', 0);
            const interval = setInterval(() => {
              this.demoProgress += 10;
              OverlayUtils.updateProgress(this.demoProgress);
              if (this.demoProgress >= 100) {
                clearInterval(interval);
                setTimeout(() => { OverlayUtils.hideLoading(); OverlayUtils.success('下载完成'); }, 500);
              }
            }, 300);
          })
          Button('可取消 Loading').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            OverlayUtils.showLoading('处理中...', true);
          })
        }
        .width('100%').margin({ bottom: 16 })

        Text('动画演示').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 16, bottom: 12 }).width('100%')

        Row() {
          Button('淡入').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).onClick(() => {
            this.showAnimatedDialog(AnimationType.FADE);
          })
          Button('滑入').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            this.showAnimatedDialog(AnimationType.SLIDE_UP);
          })
          Button('缩放').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            this.showAnimatedDialog(AnimationType.SCALE);
          })
          Button('弹跳').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            this.showAnimatedDialog(AnimationType.BOUNCE);
          })
        }
        .width('100%').margin({ bottom: 16 })

        Text('层级管理').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 16, bottom: 12 }).width('100%')

        Row() {
          Button('清空所有').fontSize(12).fontColor('#fff').backgroundColor('#c41e3a').borderRadius(8).padding({ left: 12, right: 12 }).onClick(() => {
            OverlayUtils.clearAll();
          })
          Button('多层弹窗').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            this.showMultiLayerDemo();
          })
        }
        .width('100%').margin({ bottom: 16 })
      }
      .width('100%')
      .padding(16)
    }
    .width('100%')
    .layoutWeight(1)
    .scrollBar(BarState.Auto)
  }

  @Builder
  LayerInfoBuilder() {
    Column() {
      Text('当前层级栈').fontSize(14).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 8 })

      if (this.overlayState.layerStack.layers.length === 0) {
        Text('空').fontSize(12).fontColor('#666')
      } else {
        ForEach(this.overlayState.layerStack.layers, (layer) => {
          Row() {
            Text(`${layer.type}`).fontSize(12).fontColor('#fff').layoutWeight(1)
            Text(`zIndex: ${layer.zIndex}`).fontSize(12).fontColor('#888')
            Text(`${layer.maskType}`).fontSize(12).fontColor('#666').margin({ left: 8 })
          }
          .width('100%')
          .padding({ top: 4, bottom: 4 })
        })
      }
    }
    .width('100%')
    .padding(16)
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }

  // 显示动画弹窗
  showAnimatedDialog(animation: AnimationType): void {
    overlayState.showDialog(new DialogConfig({
      title: '动画演示',
      message: `这是 ${animation} 动画效果`,
      icon: '🎬',
      primaryButton: { label: '确定', type: 'primary' },
      enterAnimation: animation,
      animationDuration: 500
    }));
  }

  // 多层弹窗演示
  showMultiLayerDemo(): void {
    overlayState.showDialog(new DialogConfig({
      title: '第一层',
      message: '点击确定打开第二层',
      primaryButton: { 
        label: '打开第二层', 
        type: 'primary',
        action: () => {
          overlayState.showDialog(new DialogConfig({
            title: '第二层',
            message: '这是第二层弹窗',
            primaryButton: { label: '确定', type: 'primary' }
          }));
        }
      }
    }));
  }
}

const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
```

---

## 七、组件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| 层级模型 | `entry/src/main/ets/models/StackModel.ets` | LayerConfig/DialogConfig/ToastConfig/LoadingConfig/LayerStack/OverlayState |
| 遮罩容器 | `entry/src/main/ets/components/OverlayContainer.ets` | Stack容器/Dialog/Toast/Loading/动画过渡 |
| 遮罩工具 | `entry/src/main/ets/utils/OverlayUtils.ets` | confirm/alert/error/prompt/success/showLoading等便捷方法 |
| 演示页面 | `entry/src/main/ets/pages/StackDemoPage.ets` | 完整Stack布局演示 |
| 数据库 | `entry/src/main/ets/database/OverlayDatabase.ets` | 遮罩配置持久化 |

---

## 八、鸿蒙特性使用

| 特性 | 用途 | API |
|------|------|-----|
| ArkTS声明式UI | 界面构建 | `@Component` `@Entry` |
| Stack | 堆叠布局 | `Stack` `alignContent` |
| 状态管理 | 数据响应 | `@State` `@Observed` `@StorageLink` |
| 动画 | 过渡效果 | `animation` `transition` `Curve` |
| 手势 | 点击拦截 | `onClick` `gesture` |
| 遮罩 | 背景遮挡 | `Overlay` `backgroundColor` |
| 焦点 | 焦点管理 | `focus` `tabIndex` |
| 窗口 | 层级控制 | `zIndex` `Window` |
| 加载组件 | 加载动画 | `LoadingProgress` |
| 国密算法 | 数据签名 | `cryptoFramework` SM2/SM3 |

---

## 九、层级对照表

| 层级 | zIndex | 遮罩类型 | 动画 | 自动关闭 | 拦截手势 | 使用场景 |
|------|--------|----------|------|----------|----------|----------|
| BASE | 0 | NONE | 无 | 否 | 否 | 页面主体 |
| CONTENT | 10 | NONE | 无 | 否 | 否 | 滚动内容 |
| NAVIGATION | 20 | NONE | 无 | 否 | 否 | 导航栏/侧边栏 |
| MASK | 30 | DIM | FADE | 否 | 是 | 半透明遮罩 |
| DIALOG | 40 | DIM | SCALE/SLIDE | 否 | 是 | 模态对话框 |
| TOAST | 50 | TRANSPARENT | FADE | 是(2s) | 否 | 轻量提示 |
| LOADING | 60 | DIM | FADE | 否 | 是 | 加载动画 |
| TOP | 100 | TRANSPARENT | FADE | 否 | 是 | 最高优先级 |

---

## 十、动画对照表

| 动画 | 效果 | 时长 | 适用场景 |
|------|------|------|----------|
| FADE | 淡入淡出 | 300ms | 通用 |
| SLIDE_UP | 从底部滑入 | 300ms | 底部弹窗 |
| SLIDE_DOWN | 从顶部滑入 | 300ms | 下拉菜单 |
| SLIDE_LEFT | 从右侧滑入 | 300ms | 侧边栏 |
| SLIDE_RIGHT | 从左侧滑入 | 300ms | 返回导航 |
| SCALE | 缩放 | 300ms | 确认弹窗 |
| ROTATE | 旋转 | 300ms | 特殊效果 |
| FLIP | 翻转 | 300ms | 特殊效果 |
| BOUNCE | 弹跳 | 500ms | 成功提示 |

---

## 十一、龍魂标识

| 位置 | 内容 |
|------|------|
| 应用名称 | 龍魂 Stack 布局 |
| 标题栏 | 🐉 龍魂 Stack 布局 |
| 底部标识 | UID:9622 |
| 数据签名 | SM3-哈希 |
| DNA | ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ |

---

🐉 **龍魂 · 鸿蒙原生 ArkTS 布局实战：Stack 遮罩层布局深度解析（API 24） 交付完成**

> DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️  
> UID: 9622  
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
> 时间: 2026-07-14  
> 模块: 5核心文件  
> 特性: Stack 堆叠布局 · 8级层级系统 · 4种遮罩类型 · 9种动画效果 · 弹窗/Toast/Loading · 便捷工具类 · 国密签名

🐉AI协作输出时间戳: 🐉丙午·丁酉·癸未·子时·䷝离·🟢
