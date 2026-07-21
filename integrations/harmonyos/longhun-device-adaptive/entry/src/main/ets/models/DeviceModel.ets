// entry/src/main/ets/models/DeviceModel.ets
// 龍魂 · 设备形态模型 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 设备类型 ===
export enum DeviceType {
  PHONE = 'phone',
  FOLDABLE = 'foldable',
  TABLET = 'tablet',
  WATCH = 'watch',
  CAR = 'car',
  TV = 'tv',
  IOT = 'iot'
}

// === 断点枚举 ===
export enum Breakpoint {
  XS = 'xs',
  SM = 'sm',
  MD = 'md',
  LG = 'lg',
  XL = 'xl'
}

// === 交互模式 ===
export enum InteractionMode {
  TOUCH = 'touch',
  VOICE = 'voice',
  KNOB = 'knob',
  GESTURE = 'gesture',
  REMOTE = 'remote',
  STEERING = 'steering'
}

// === 色彩模式 ===
export enum ColorMode {
  LIGHT = 'light',
  DARK = 'dark',
  AUTO = 'auto'
}

// === 方向 ===
export enum Orientation {
  PORTRAIT = 'portrait',
  LANDSCAPE = 'landscape',
  SQUARE = 'square'
}

// === 设备形态 ===
@Observed
export class DeviceProfile {
  id: string;
  deviceType: DeviceType;
  breakpoint: Breakpoint;
  screenWidth: number;
  screenHeight: number;
  screenDensity: number;
  orientation: Orientation;
  interactionMode: InteractionMode;
  colorMode: ColorMode;
  isRound: boolean;
  hasNotch: boolean;
  safeAreaTop: number;
  safeAreaBottom: number;
  safeAreaLeft: number;
  safeAreaRight: number;
  dnaSignature: string;

  constructor(data: Partial<DeviceProfile>) {
    this.id = data.id || `DEV-${Date.now()}`;
    this.deviceType = data.deviceType || DeviceType.PHONE;
    this.breakpoint = data.breakpoint || Breakpoint.SM;
    this.screenWidth = data.screenWidth || 360;
    this.screenHeight = data.screenHeight || 780;
    this.screenDensity = data.screenDensity || 3;
    this.orientation = data.orientation || Orientation.PORTRAIT;
    this.interactionMode = data.interactionMode || InteractionMode.TOUCH;
    this.colorMode = data.colorMode || ColorMode.AUTO;
    this.isRound = data.isRound || false;
    this.hasNotch = data.hasNotch || false;
    this.safeAreaTop = data.safeAreaTop || 0;
    this.safeAreaBottom = data.safeAreaBottom || 0;
    this.safeAreaLeft = data.safeAreaLeft || 0;
    this.safeAreaRight = data.safeAreaRight || 0;
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.deviceType}-${this.breakpoint}`;
    const hash = payload.split('').reduce((a, b) => a + b.charCodeAt(0), 0).toString(16).substring(0, 16);
    return `SM3-${hash}`;
  }

  getGridColumns(): number {
    switch (this.breakpoint) {
      case Breakpoint.XS: return 2;
      case Breakpoint.SM: return 4;
      case Breakpoint.MD: return 8;
      case Breakpoint.LG: return 12;
      case Breakpoint.XL: return 24;
      default: return 4;
    }
  }

  getSpacing(): number {
    switch (this.breakpoint) {
      case Breakpoint.XS: return 4;
      case Breakpoint.SM: return 8;
      case Breakpoint.MD: return 12;
      case Breakpoint.LG: return 16;
      case Breakpoint.XL: return 24;
      default: return 8;
    }
  }

  getFontScale(): number {
    switch (this.deviceType) {
      case DeviceType.WATCH: return 0.8;
      case DeviceType.CAR: return 1.5;
      case DeviceType.TV: return 1.8;
      default: return 1.0;
    }
  }

  getBorderRadius(): number {
    switch (this.deviceType) {
      case DeviceType.WATCH: return this.isRound ? 999 : 8;
      case DeviceType.CAR: return 12;
      case DeviceType.TV: return 8;
      default: return 8;
    }
  }

  isMultiColumn(): boolean {
    return this.breakpoint >= Breakpoint.MD;
  }

  isSidebarSupported(): boolean {
    return this.breakpoint >= Breakpoint.MD && this.deviceType !== DeviceType.WATCH;
  }

  getMinTouchTarget(): number {
    switch (this.deviceType) {
      case DeviceType.WATCH: return 36;
      case DeviceType.CAR: return 64;
      case DeviceType.TV: return 48;
      default: return 44;
    }
  }
}

// === 布局策略 ===
@Observed
export class LayoutStrategy {
  id: string;
  name: string;
  deviceType: DeviceType;
  breakpoint: Breakpoint;
  contentPadding: number;
  cardColumns: number;
  listItemHeight: number;
  headerHeight: number;
  footerHeight: number;
  sidebarWidth: number;
  tabBarHeight: number;
  buttonHeight: number;
  buttonMinWidth: number;
  inputHeight: number;
  avatarSize: number;
  iconSize: number;
  animationDuration: number;
  pageTransition: string;
  dnaSignature: string;

  constructor(data: Partial<LayoutStrategy>) {
    this.id = data.id || `LS-${Date.now()}`;
    this.name = data.name || '默认策略';
    this.deviceType = data.deviceType || DeviceType.PHONE;
    this.breakpoint = data.breakpoint || Breakpoint.SM;
    this.contentPadding = data.contentPadding || 16;
    this.cardColumns = data.cardColumns || 1;
    this.listItemHeight = data.listItemHeight || 56;
    this.headerHeight = data.headerHeight || 56;
    this.footerHeight = data.footerHeight || 56;
    this.sidebarWidth = data.sidebarWidth || 0;
    this.tabBarHeight = data.tabBarHeight || 56;
    this.buttonHeight = data.buttonHeight || 44;
    this.buttonMinWidth = data.buttonMinWidth || 80;
    this.inputHeight = data.inputHeight || 44;
    this.avatarSize = data.avatarSize || 40;
    this.iconSize = data.iconSize || 24;
    this.animationDuration = data.animationDuration || 300;
    this.pageTransition = data.pageTransition || 'slide';
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const hash = `${this.id}-${this.deviceType}-${Date.now()}`.split('')
      .reduce((a, b) => a + b.charCodeAt(0), 0).toString(16).substring(0, 16);
    return `SM3-${hash}`;
  }

  static createDefault(deviceType: DeviceType, breakpoint: Breakpoint): LayoutStrategy {
    const strategies: Record<string, Partial<LayoutStrategy>> = {
      'watch-xs': {
        contentPadding: 4, cardColumns: 1, listItemHeight: 36,
        headerHeight: 0, footerHeight: 0, sidebarWidth: 0, tabBarHeight: 0,
        buttonHeight: 36, buttonMinWidth: 60, inputHeight: 36,
        avatarSize: 28, iconSize: 20, animationDuration: 200, pageTransition: 'fade'
      },
      'phone-sm': {
        contentPadding: 16, cardColumns: 1, listItemHeight: 56,
        headerHeight: 56, footerHeight: 56, sidebarWidth: 0, tabBarHeight: 56,
        buttonHeight: 44, buttonMinWidth: 80, inputHeight: 44,
        avatarSize: 40, iconSize: 24, animationDuration: 300, pageTransition: 'slide'
      },
      'phone-md': {
        contentPadding: 16, cardColumns: 2, listItemHeight: 56,
        headerHeight: 56, footerHeight: 56, sidebarWidth: 0, tabBarHeight: 56,
        buttonHeight: 44, buttonMinWidth: 80, inputHeight: 44,
        avatarSize: 40, iconSize: 24, animationDuration: 300, pageTransition: 'slide'
      },
      'tablet-lg': {
        contentPadding: 24, cardColumns: 3, listItemHeight: 64,
        headerHeight: 64, footerHeight: 64, sidebarWidth: 240, tabBarHeight: 0,
        buttonHeight: 48, buttonMinWidth: 96, inputHeight: 48,
        avatarSize: 48, iconSize: 28, animationDuration: 300, pageTransition: 'slide'
      },
      'car-xl': {
        contentPadding: 32, cardColumns: 4, listItemHeight: 80,
        headerHeight: 80, footerHeight: 0, sidebarWidth: 320, tabBarHeight: 0,
        buttonHeight: 64, buttonMinWidth: 120, inputHeight: 56,
        avatarSize: 56, iconSize: 32, animationDuration: 400, pageTransition: 'scale'
      },
      'tv-xl': {
        contentPadding: 48, cardColumns: 6, listItemHeight: 96,
        headerHeight: 96, footerHeight: 0, sidebarWidth: 400, tabBarHeight: 0,
        buttonHeight: 72, buttonMinWidth: 160, inputHeight: 64,
        avatarSize: 64, iconSize: 40, animationDuration: 500, pageTransition: 'fade'
      }
    };

    const key = `${deviceType}-${breakpoint}`;
    const defaults = strategies[key] || strategies['phone-sm'];
    return new LayoutStrategy({ ...defaults, deviceType, breakpoint });
  }
}

// === 设备状态管理 ===
@Observed
export class DeviceState {
  currentProfile: DeviceProfile = new DeviceProfile({});
  currentStrategy: LayoutStrategy = LayoutStrategy.createDefault(DeviceType.PHONE, Breakpoint.SM);
  availableDevices: DeviceProfile[] = [];
  windowWidth: number = 360;
  windowHeight: number = 780;
  private listeners: ((profile: DeviceProfile) => void)[] = [];

  init(): void {
    this.detectDevice();
    this.updateStrategy();
  }

  detectDevice(): void {
    const width = this.windowWidth;
    const height = this.windowHeight;
    const minSide = Math.min(width, height);

    let breakpoint: Breakpoint;
    if (minSide < 320) breakpoint = Breakpoint.XS;
    else if (minSide < 600) breakpoint = Breakpoint.SM;
    else if (minSide < 840) breakpoint = Breakpoint.MD;
    else if (minSide < 1200) breakpoint = Breakpoint.LG;
    else breakpoint = Breakpoint.XL;

    let deviceType = DeviceType.PHONE;
    if (minSide < 200) deviceType = DeviceType.WATCH;
    else if (width > 1200 && height > 600) deviceType = DeviceType.CAR;
    else if (width > 1920) deviceType = DeviceType.TV;
    else if (minSide > 600 && minSide < 840) deviceType = DeviceType.TABLET;

    this.currentProfile = new DeviceProfile({
      deviceType,
      breakpoint,
      screenWidth: width,
      screenHeight: height,
      orientation: width > height ? Orientation.LANDSCAPE : Orientation.PORTRAIT
    });
  }

  updateStrategy(): void {
    this.currentStrategy = LayoutStrategy.createDefault(
      this.currentProfile.deviceType,
      this.currentProfile.breakpoint
    );
  }

  onWindowChange(width: number, height: number): void {
    this.windowWidth = width;
    this.windowHeight = height;
    this.detectDevice();
    this.updateStrategy();
    this.notifyListeners();
  }

  addListener(callback: (profile: DeviceProfile) => void): void {
    this.listeners.push(callback);
  }

  private notifyListeners(): void {
    this.listeners.forEach(cb => cb(this.currentProfile));
  }

  getResponsiveValue<T>(values: Record<Breakpoint, T>): T {
    return values[this.currentProfile.breakpoint] || values[Breakpoint.SM];
  }

  getDeviceValue<T>(values: Record<DeviceType, T>): T {
    return values[this.currentProfile.deviceType] || values[DeviceType.PHONE];
  }
}

// 全局状态
export const deviceState = new DeviceState();
AppStorage.setOrCreate('deviceState', deviceState);
