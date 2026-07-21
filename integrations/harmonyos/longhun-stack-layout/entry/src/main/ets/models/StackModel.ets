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
