// entry/src/main/ets/models/InventoryModel.ets
// 龍魂 · 办公物资库存模型 · ArkTS

// === DNA常量 ===
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 物资分类 ===
export enum SupplyCategory {
  OFFICE = '办公用品',
  ELECTRONICS = '电子设备',
  FURNITURE = '家具',
  CONSUMABLES = '耗材',
  STATIONERY = '文具',
  CLEANING = '清洁用品',
  SAFETY = '安全用品',
  OTHER = '其他'
}

// === 物资状态 ===
export enum ItemStatus {
  IN_STOCK = '在库',
  LOW_STOCK = '低库存',
  OUT_OF_STOCK = '缺货',
  RESERVED = '预留',
  DAMAGED = '损坏',
  EXPIRED = '过期',
  DISCARDED = '已报废'
}

// === 审批状态 ===
export enum ApprovalStatus {
  DRAFT = '草稿',
  PENDING = '待审批',
  APPROVED = '已通过',
  REJECTED = '已驳回',
  CANCELLED = '已取消'
}

// === 库存流水记录 ===
export class InventoryRecord {
  id: string;
  itemId: string;
  type: '入库' | '出库' | '盘点' | '调拨' | '报废';
  quantity: number;
  oldQuantity: number;
  newQuantity: number;
  operator: string;
  approver?: string;
  reason: string;
  documentNo?: string;
  photoPath?: string;
  timestamp: Date;
  dnaSignature: string;

  constructor(data: Partial<InventoryRecord>) {
    this.id = data.id || `REC-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`;
    this.itemId = data.itemId || '';
    this.type = data.type || '入库';
    this.quantity = data.quantity || 0;
    this.oldQuantity = data.oldQuantity || 0;
    this.newQuantity = data.newQuantity || 0;
    this.operator = data.operator || '';
    this.approver = data.approver;
    this.reason = data.reason || '';
    this.documentNo = data.documentNo;
    this.photoPath = data.photoPath;
    this.timestamp = data.timestamp || new Date();
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.itemId}-${this.type}-${this.quantity}`;
    let hash = 0;
    for (let i = 0; i < payload.length; i++) {
      hash = ((hash << 5) - hash) + payload.charCodeAt(i);
      hash |= 0;
    }
    return `SM3-${(hash >>> 0).toString(16).padStart(16, '0')}`;
  }
}

// === 物资档案 ===
export class SupplyItem {
  id: string;
  sku: string;
  name: string;
  category: SupplyCategory;
  specification: string;
  brand: string;
  unit: string;
  location: string;
  status: ItemStatus;
  quantity: number;
  minQuantity: number;
  maxQuantity: number;
  reorderPoint: number;
  batchNo: string;
  supplier: string;
  purchaseDate: Date;
  expiryDate?: Date;
  purchasePrice: number;
  totalValue: number;
  custodian: string;
  department: string;
  lastUsedBy?: string;
  lastUsedDate?: Date;
  barcode: string;
  qrCode: string;
  photoPath?: string;
  rfidTag?: string;
  createdAt: Date;
  updatedAt: Date;
  dnaSignature: string;

  constructor(data: Partial<SupplyItem>) {
    this.id = data.id || this.generateId();
    this.sku = data.sku || this.generateSKU(data.category, data.name);
    this.name = data.name || '';
    this.category = data.category || SupplyCategory.OTHER;
    this.specification = data.specification || '';
    this.brand = data.brand || '';
    this.unit = data.unit || '个';
    this.location = data.location || '未指定';
    this.status = data.status || ItemStatus.IN_STOCK;
    this.quantity = data.quantity || 0;
    this.minQuantity = data.minQuantity || 10;
    this.maxQuantity = data.maxQuantity || 100;
    this.reorderPoint = data.reorderPoint || 20;
    this.batchNo = data.batchNo || this.generateBatchNo();
    this.supplier = data.supplier || '';
    this.purchaseDate = data.purchaseDate || new Date();
    this.expiryDate = data.expiryDate;
    this.purchasePrice = data.purchasePrice || 0;
    this.totalValue = this.quantity * this.purchasePrice;
    this.custodian = data.custodian || '';
    this.department = data.department || '';
    this.lastUsedBy = data.lastUsedBy;
    this.lastUsedDate = data.lastUsedDate;
    this.barcode = data.barcode || this.sku;
    this.qrCode = data.qrCode || this.generateQRCode();
    this.photoPath = data.photoPath;
    this.rfidTag = data.rfidTag;
    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
    this.dnaSignature = this.signData();
  }

  private generateId(): string {
    return `INV-${MASTER_UID}-${Date.now().toString(36).substr(-6)}`;
  }

  private generateSKU(category?: SupplyCategory, name?: string): string {
    const catCode = (category || 'OT').substring(0, 2).toUpperCase();
    const nameCode = (name || 'XX').substring(0, 2).toUpperCase();
    const seq = Math.floor(Math.random() * 9999).toString().padStart(4, '0');
    return `${catCode}-${nameCode}-${seq}`;
  }

  private generateBatchNo(): string {
    const date = new Date();
    return `B${date.getFullYear()}${(date.getMonth() + 1).toString().padStart(2, '0')}${date.getDate().toString().padStart(2, '0')}-${Math.floor(Math.random() * 999).toString().padStart(3, '0')}`;
  }

  private generateQRCode(): string {
    return `LH-INV://${this.id}?dna=${this.dnaSignature.substring(0, 16)}`;
  }

  private signData(): string {
    const payload = `${this.id}-${this.sku}-${this.name}-${this.quantity}`;
    let hash = 0;
    for (let i = 0; i < payload.length; i++) {
      hash = ((hash << 5) - hash) + payload.charCodeAt(i);
      hash |= 0;
    }
    return `SM3-${(hash >>> 0).toString(16).padStart(16, '0')}`;
  }

  // 更新库存
  updateQuantity(delta: number, operator: string, reason: string): InventoryRecord {
    const oldQty = this.quantity;
    this.quantity += delta;
    this.totalValue = this.quantity * this.purchasePrice;
    this.updatedAt = new Date();

    if (this.quantity <= 0) {
      this.status = ItemStatus.OUT_OF_STOCK;
    } else if (this.quantity <= this.minQuantity) {
      this.status = ItemStatus.LOW_STOCK;
    } else {
      this.status = ItemStatus.IN_STOCK;
    }

    this.dnaSignature = this.signData();

    return new InventoryRecord({
      itemId: this.id,
      type: delta > 0 ? '入库' : '出库',
      quantity: Math.abs(delta),
      oldQuantity: oldQty,
      newQuantity: this.quantity,
      operator: operator,
      reason: reason,
      timestamp: new Date()
    });
  }

  checkExpiry(): boolean {
    if (!this.expiryDate) {
      return false;
    }
    return new Date() > this.expiryDate;
  }

  needsReorder(): boolean {
    return this.quantity <= this.reorderPoint;
  }

  getHealthScore(): number {
    if (this.quantity <= 0) {
      return 0;
    }
    if (this.quantity <= this.minQuantity) {
      return 30;
    }
    if (this.quantity <= this.reorderPoint) {
      return 60;
    }
    if (this.quantity >= this.maxQuantity) {
      return 90;
    }
    return 80;
  }
}

// === 采购物项 ===
export class PurchaseItem {
  id: string;
  itemName: string;
  specification: string;
  quantity: number;
  unit: string;
  estimatedPrice: number;
  totalPrice: number;
  supplier?: string;
  remark?: string;

  constructor(data: Partial<PurchaseItem>) {
    this.id = data.id || `PI-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`;
    this.itemName = data.itemName || '';
    this.specification = data.specification || '';
    this.quantity = data.quantity || 1;
    this.unit = data.unit || '个';
    this.estimatedPrice = data.estimatedPrice || 0;
    this.totalPrice = this.quantity * this.estimatedPrice;
    this.supplier = data.supplier;
    this.remark = data.remark;
  }
}

// === 采购申请 ===
export class PurchaseRequest {
  id: string;
  requestNo: string;
  items: PurchaseItem[];
  requester: string;
  department: string;
  requestDate: Date;
  requiredDate: Date;
  totalAmount: number;
  status: ApprovalStatus;
  level1Approver?: string;
  level1Approved?: Date;
  level1Comment?: string;
  level2Approver?: string;
  level2Approved?: Date;
  level2Comment?: string;
  level3Approver?: string;
  level3Approved?: Date;
  level3Comment?: string;
  purchaseOrderNo?: string;
  supplier?: string;
  actualAmount?: number;
  receivedDate?: Date;
  createdAt: Date;
  dnaSignature: string;

  constructor(data: Partial<PurchaseRequest>) {
    this.id = data.id || `PR-${Date.now()}-${Math.random().toString(36).substr(2, 6)}`;
    this.requestNo = data.requestNo || this.generateRequestNo();
    this.items = data.items || [];
    this.requester = data.requester || '';
    this.department = data.department || '';
    this.requestDate = data.requestDate || new Date();
    this.requiredDate = data.requiredDate || new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
    this.totalAmount = data.totalAmount || this.calculateTotal();
    this.status = data.status || ApprovalStatus.DRAFT;
    this.level1Approver = data.level1Approver;
    this.level1Approved = data.level1Approved;
    this.level1Comment = data.level1Comment;
    this.level2Approver = data.level2Approver;
    this.level2Approved = data.level2Approved;
    this.level2Comment = data.level2Comment;
    this.level3Approver = data.level3Approver;
    this.level3Approved = data.level3Approved;
    this.level3Comment = data.level3Comment;
    this.purchaseOrderNo = data.purchaseOrderNo;
    this.supplier = data.supplier;
    this.actualAmount = data.actualAmount;
    this.receivedDate = data.receivedDate;
    this.createdAt = data.createdAt || new Date();
    this.dnaSignature = this.signData();
  }

  private generateRequestNo(): string {
    const date = new Date();
    return `CG${date.getFullYear()}${(date.getMonth() + 1).toString().padStart(2, '0')}${date.getDate().toString().padStart(2, '0')}-${Math.floor(Math.random() * 999).toString().padStart(3, '0')}`;
  }

  private calculateTotal(): number {
    return this.items.reduce((sum, item) => sum + item.totalPrice, 0);
  }

  private signData(): string {
    const payload = `${this.id}-${this.requestNo}-${this.totalAmount}`;
    let hash = 0;
    for (let i = 0; i < payload.length; i++) {
      hash = ((hash << 5) - hash) + payload.charCodeAt(i);
      hash |= 0;
    }
    return `SM3-${(hash >>> 0).toString(16).padStart(16, '0')}`;
  }

  submit(): void {
    this.status = ApprovalStatus.PENDING;
  }

  approve(level: 1 | 2 | 3, approver: string, comment: string): void {
    const now = new Date();
    switch (level) {
      case 1:
        this.level1Approver = approver;
        this.level1Approved = now;
        this.level1Comment = comment;
        if (this.totalAmount < 5000) {
          this.status = ApprovalStatus.APPROVED;
        }
        break;
      case 2:
        this.level2Approver = approver;
        this.level2Approved = now;
        this.level2Comment = comment;
        if (this.totalAmount < 50000) {
          this.status = ApprovalStatus.APPROVED;
        }
        break;
      case 3:
        this.level3Approver = approver;
        this.level3Approved = now;
        this.level3Comment = comment;
        this.status = ApprovalStatus.APPROVED;
        break;
    }
  }

  reject(level: 1 | 2 | 3, approver: string, comment: string): void {
    this.status = ApprovalStatus.REJECTED;
    switch (level) {
      case 1:
        this.level1Approver = approver;
        this.level1Approved = new Date();
        this.level1Comment = comment;
        break;
      case 2:
        this.level2Approver = approver;
        this.level2Approved = new Date();
        this.level2Comment = comment;
        break;
      case 3:
        this.level3Approver = approver;
        this.level3Approved = new Date();
        this.level3Comment = comment;
        break;
    }
  }
}

// === 预警项 ===
export interface AlertItem {
  type: 'low_stock' | 'out_of_stock' | 'expired' | 'reorder' | 'pending_approval';
  level: 'critical' | 'warning' | 'info';
  itemId: string;
  title: string;
  message: string;
  timestamp: Date;
}

// === 统计 ===
export interface InventoryStats {
  totalItems: number;
  inStock: number;
  lowStock: number;
  outOfStock: number;
  totalValue: number;
  categories: Record<string, number>;
  locations: Record<string, number>;
}

// === 库存全局状态 ===
@Observed
export class InventoryState {
  items: SupplyItem[] = [];
  records: InventoryRecord[] = [];
  purchaseRequests: PurchaseRequest[] = [];
  filterCategory: SupplyCategory | '全部' = '全部';
  filterStatus: ItemStatus | '全部' = '全部';
  filterLocation: string = '全部';
  searchQuery: string = '';
  lowStockAlert: boolean = true;
  expiryAlert: boolean = true;
  reorderAuto: boolean = false;

  get filteredItems(): SupplyItem[] {
    let result = this.items;

    if (this.filterCategory !== '全部') {
      result = result.filter(i => i.category === this.filterCategory);
    }

    if (this.filterStatus !== '全部') {
      result = result.filter(i => i.status === this.filterStatus);
    }

    if (this.filterLocation !== '全部') {
      result = result.filter(i => i.location === this.filterLocation);
    }

    if (this.searchQuery) {
      const q = this.searchQuery.toLowerCase();
      result = result.filter(i =>
        i.name.toLowerCase().includes(q) ||
        i.sku.toLowerCase().includes(q) ||
        i.barcode.includes(q) ||
        i.location.toLowerCase().includes(q)
      );
    }

    return result.sort((a, b) => b.getHealthScore() - a.getHealthScore());
  }

  get alerts(): AlertItem[] {
    const alerts: AlertItem[] = [];

    if (this.lowStockAlert) {
      this.items.filter(i => i.status === ItemStatus.LOW_STOCK).forEach(i => {
        alerts.push({
          type: 'low_stock',
          level: 'warning',
          itemId: i.id,
          title: `${i.name} 库存不足`,
          message: `当前 ${i.quantity}${i.unit}，低于安全线 ${i.minQuantity}${i.unit}`,
          timestamp: new Date()
        });
      });
    }

    this.items.filter(i => i.status === ItemStatus.OUT_OF_STOCK).forEach(i => {
      alerts.push({
        type: 'out_of_stock',
        level: 'critical',
        itemId: i.id,
        title: `${i.name} 已缺货`,
        message: '库存为零，需立即补货',
        timestamp: new Date()
      });
    });

    if (this.expiryAlert) {
      this.items.filter(i => i.checkExpiry()).forEach(i => {
        alerts.push({
          type: 'expired',
          level: 'critical',
          itemId: i.id,
          title: `${i.name} 已过期`,
          message: `保质期至 ${i.expiryDate?.toLocaleDateString() || '未知'}`,
          timestamp: new Date()
        });
      });
    }

    // 待审批采购单
    this.purchaseRequests.filter(r => r.status === ApprovalStatus.PENDING).forEach(r => {
      alerts.push({
        type: 'pending_approval',
        level: 'info',
        itemId: r.id,
        title: `采购审批: ${r.requestNo}`,
        message: `${r.requester} 申请 ¥${r.totalAmount.toFixed(2)}，${r.items.length}项物资`,
        timestamp: new Date()
      });
    });

    return alerts.sort((a, b) => {
      const levelOrder: Record<string, number> = { critical: 0, warning: 1, info: 2 };
      return levelOrder[a.level] - levelOrder[b.level];
    });
  }

  get statistics(): InventoryStats {
    const total = this.items.length;
    const inStock = this.items.filter(i => i.status === ItemStatus.IN_STOCK).length;
    const lowStock = this.items.filter(i => i.status === ItemStatus.LOW_STOCK).length;
    const outOfStock = this.items.filter(i => i.status === ItemStatus.OUT_OF_STOCK).length;
    const totalValue = this.items.reduce((sum, i) => sum + i.totalValue, 0);

    return {
      totalItems: total,
      inStock,
      lowStock,
      outOfStock,
      totalValue,
      categories: this.getCategoryDistribution(),
      locations: this.getLocationDistribution()
    };
  }

  private getCategoryDistribution(): Record<string, number> {
    const dist: Record<string, number> = {};
    this.items.forEach(i => {
      dist[i.category] = (dist[i.category] || 0) + 1;
    });
    return dist;
  }

  private getLocationDistribution(): Record<string, number> {
    const dist: Record<string, number> = {};
    this.items.forEach(i => {
      dist[i.location] = (dist[i.location] || 0) + 1;
    });
    return dist;
  }

  addItem(item: SupplyItem): void {
    this.items.push(item);
    this.persist();
  }

  removeItem(id: string): void {
    const idx = this.items.findIndex(i => i.id === id);
    if (idx >= 0) {
      this.items.splice(idx, 1);
      this.persist();
    }
  }

  updateItem(id: string, data: Partial<SupplyItem>): void {
    const idx = this.items.findIndex(i => i.id === id);
    if (idx >= 0) {
      const old = this.items[idx];
      this.items[idx] = new SupplyItem({ ...old, ...data, id: old.id });
      this.persist();
    }
  }

  getItem(id: string): SupplyItem | undefined {
    return this.items.find(i => i.id === id);
  }

  stockIn(id: string, qty: number, operator: string, reason: string): InventoryRecord {
    const item = this.items.find(i => i.id === id);
    if (!item) {
      throw new Error('物资不存在');
    }
    const record = item.updateQuantity(qty, operator, reason);
    this.records.push(record);
    this.persist();
    return record;
  }

  stockOut(id: string, qty: number, operator: string, reason: string): InventoryRecord {
    const item = this.items.find(i => i.id === id);
    if (!item) {
      throw new Error('物资不存在');
    }
    if (item.quantity < qty) {
      throw new Error('库存不足');
    }
    const record = item.updateQuantity(-qty, operator, reason);
    this.records.push(record);
    this.persist();
    return record;
  }

  addPurchaseRequest(req: PurchaseRequest): void {
    this.purchaseRequests.push(req);
    this.persist();
  }

  getRecordsForItem(itemId: string): InventoryRecord[] {
    return this.records.filter(r => r.itemId === itemId).sort((a, b) =>
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
  }

  private persist(): void {
    try {
      AppStorage.setOrCreate('inventory_items', JSON.stringify(this.items));
      AppStorage.setOrCreate('inventory_records', JSON.stringify(this.records));
      AppStorage.setOrCreate('inventory_requests', JSON.stringify(this.purchaseRequests));
    } catch (e) {
      console.error('库存数据持久化失败', e);
    }
  }

  load(): void {
    try {
      const itemsData = AppStorage.get<string>('inventory_items');
      if (itemsData) {
        const parsed = JSON.parse(itemsData);
        this.items = parsed.map((i: Record<string, Object>) => new SupplyItem(i as Partial<SupplyItem>));
      }
    } catch (e) {
      console.error('加载库存数据失败', e);
    }

    try {
      const recordsData = AppStorage.get<string>('inventory_records');
      if (recordsData) {
        const parsed = JSON.parse(recordsData);
        this.records = parsed.map((r: Record<string, Object>) => new InventoryRecord(r as Partial<InventoryRecord>));
      }
    } catch (e) {
      console.error('加载流水数据失败', e);
    }

    try {
      const requestsData = AppStorage.get<string>('inventory_requests');
      if (requestsData) {
        const parsed = JSON.parse(requestsData);
        this.purchaseRequests = parsed.map((r: Record<string, Object>) => {
          const req = new PurchaseRequest(r as Partial<PurchaseRequest>);
          if (r['items']) {
            req.items = (r['items'] as Record<string, Object>[]).map(
              (pi: Record<string, Object>) => new PurchaseItem(pi as Partial<PurchaseItem>)
            );
          }
          return req;
        });
      }
    } catch (e) {
      console.error('加载采购数据失败', e);
    }
  }
}

// 全局状态单例
export const inventoryState = new InventoryState();
AppStorage.setOrCreate('inventoryState', inventoryState);
