import {
  mysqlTable,
  mysqlEnum,
  serial,
  varchar,
  text,
  timestamp,
  bigint,
  json,
  boolean,
  int,
} from "drizzle-orm/mysql-core";

// ========== 用户表 ==========
export const users = mysqlTable("users", {
  id: serial("id").primaryKey(),
  unionId: varchar("unionId", { length: 255 }).notNull().unique(),
  name: varchar("name", { length: 255 }),
  email: varchar("email", { length: 320 }),
  avatar: text("avatar"),
  role: mysqlEnum("role", ["user", "admin", "superadmin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().notNull().$onUpdate(() => new Date()),
  lastSignInAt: timestamp("lastSignInAt").defaultNow().notNull(),
});

// ========== 国密密钥表 ==========
export const smKeys = mysqlTable("sm_keys", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }).notNull(),
  keyName: varchar("keyName", { length: 255 }).notNull(),
  sm2PublicKey: text("sm2PublicKey"),
  sm2PrivateKey: text("sm2PrivateKey"),
  sm3Hash: text("sm3Hash"),
  sm4Key: text("sm4Key"),
  dnaSignature: varchar("dnaSignature", { length: 255 }),
  status: mysqlEnum("status", ["active", "revoked", "expired"]).default("active").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().notNull().$onUpdate(() => new Date()),
});

// ========== 设备证书表 ==========
export const deviceCerts = mysqlTable("device_certs", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }).notNull(),
  deviceType: mysqlEnum("deviceType", ["huawei", "apple", "other"]).notNull(),
  deviceName: varchar("deviceName", { length: 255 }),
  deviceModel: varchar("deviceModel", { length: 255 }),
  certificatePem: text("certificatePem"),
  fingerprint: varchar("fingerprint", { length: 128 }),
  isTrusted: boolean("isTrusted").default(false).notNull(),
  lastUsedAt: timestamp("lastUsedAt").defaultNow(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

// ========== 二次验证表 ==========
export const twoFactorAuth = mysqlTable("two_factor_auth", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }).notNull(),
  method: mysqlEnum("method", ["sms", "email", "totp", "huawei"]).notNull(),
  secret: text("secret"),
  backupCodes: text("backupCodes"),
  isEnabled: boolean("isEnabled").default(false).notNull(),
  verifiedAt: timestamp("verifiedAt"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

// ========== 内容管理表 ==========
export const contentItems = mysqlTable("content_items", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }).notNull(),
  type: mysqlEnum("type", ["skill", "persona", "document", "config", "audit"]).notNull(),
  title: varchar("title", { length: 255 }).notNull(),
  slug: varchar("slug", { length: 255 }).notNull(),
  content: text("content"),
  metadata: json("metadata"),
  status: mysqlEnum("status", ["draft", "published", "archived"]).default("draft").notNull(),
  tags: text("tags"),
  dnaMarker: varchar("dnaMarker", { length: 255 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().notNull().$onUpdate(() => new Date()),
});

// ========== 人格助手配置表 ==========
export const personaConfigs = mysqlTable("persona_configs", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }).notNull(),
  personaName: varchar("personaName", { length: 255 }).notNull(),
  systemPrompt: text("systemPrompt"),
  triggerKeywords: text("triggerKeywords"),
  responseStyle: mysqlEnum("responseStyle", ["formal", "casual", "military", "friendly"]).default("formal").notNull(),
  enabledSkills: json("enabledSkills"),
  isActive: boolean("isActive").default(true).notNull(),
  priority: int("priority").default(0).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().notNull().$onUpdate(() => new Date()),
});

// ========== 审计日志表 ==========
export const auditLogs = mysqlTable("audit_logs", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }),
  action: varchar("action", { length: 255 }).notNull(),
  resource: varchar("resource", { length: 255 }),
  method: varchar("method", { length: 50 }),
  ipAddress: varchar("ipAddress", { length: 45 }),
  userAgent: text("userAgent"),
  details: json("details"),
  dnaMarker: varchar("dnaMarker", { length: 255 }),
  severity: mysqlEnum("severity", ["info", "warning", "critical"]).default("info").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

// ========== 会话表 ==========
export const sessions = mysqlTable("sessions", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }).notNull(),
  token: varchar("token", { length: 512 }).notNull(),
  deviceType: varchar("deviceType", { length: 50 }),
  ipAddress: varchar("ipAddress", { length: 45 }),
  isRevoked: boolean("isRevoked").default(false).notNull(),
  expiresAt: timestamp("expiresAt").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

// ========== 技能注册表 ==========
export const skillRegistry = mysqlTable("skill_registry", {
  id: serial("id").primaryKey(),
  skillName: varchar("skillName", { length: 255 }).notNull(),
  skillVersion: varchar("skillVersion", { length: 50 }).default("1.0").notNull(),
  category: mysqlEnum("category", [
    "governance", "deploy", "mobile", "cloud", "security",
    "algorithm", "finance", "ai", "knowledge", "cnsh",
    "recognition", "research", "application", "system"
  ]).notNull(),
  description: text("description"),
  dnaMarker: varchar("dnaMarker", { length: 255 }),
  status: mysqlEnum("status", ["active", "inactive", "deprecated"]).default("active").notNull(),
  dependencies: json("dependencies"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().notNull().$onUpdate(() => new Date()),
});

// ========== 支付回调记录表 ==========
export const paymentCallbacks = mysqlTable("payment_callbacks", {
  id: serial("id").primaryKey(),
  billNo: varchar("billNo", { length: 255 }).notNull().unique(),
  amount: varchar("amount", { length: 50 }).notNull(),
  currency: varchar("currency", { length: 10 }).default("CNY").notNull(),
  payerId: varchar("payerId", { length: 255 }),
  payerName: varchar("payerName", { length: 255 }),
  status: mysqlEnum("status", ["pending", "processing", "success", "failed", "duplicate"]).default("pending").notNull(),
  callbackData: json("callbackData"),
  processedAt: timestamp("processedAt"),
  errorMsg: text("errorMsg"),
  retryCount: int("retryCount").default(0).notNull(),
  dnaMarker: varchar("dnaMarker", { length: 255 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

// ========== 充值记录表 ==========
export const rechargeRecords = mysqlTable("recharge_records", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }).notNull(),
  billNo: varchar("billNo", { length: 255 }).notNull().unique(),
  amount: varchar("amount", { length: 50 }).notNull(),
  currency: varchar("currency", { length: 10 }).default("CNY").notNull(),
  status: mysqlEnum("status", ["initiated", "paid", "confirmed", "failed", "refunded"]).default("initiated").notNull(),
  paymentMethod: mysqlEnum("paymentMethod", ["ecny", "alipay", "wechat", "bank"]).default("ecny").notNull(),
  callbackId: bigint("callbackId", { mode: "number", unsigned: true }),
  metadata: json("metadata"),
  dnaMarker: varchar("dnaMarker", { length: 255 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().notNull().$onUpdate(() => new Date()),
});

// ========== 容器收入口 ==========
export const intakeEntries = mysqlTable("intake_entries", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }).notNull(),
  rawContent: text("rawContent").notNull(),
  contentType: mysqlEnum("contentType", ["text", "code", "link", "image", "mixed"]).default("text").notNull(),
  source: varchar("source", { length: 100 }).default("manual"), // manual/clipboard/api/webhook
  dnaV2: varchar("dnaV2", { length: 255 }), // v∞ 干支卦DNA
  dnaV1: varchar("dnaV1", { length: 255 }), // 兼容旧版
  年干支: varchar("yearGz", { length: 10 }),
  月干支: varchar("monthGz", { length: 10 }),
  日干支: varchar("dayGz", { length: 10 }),
  时辰名: varchar("hourName", { length: 20 }),
  卦名: varchar("guaName", { length: 20 }),
  五行: varchar("wuxing", { length: 10 }),
  数字根: int("dr"),
  // 六维评估
  权重层级: varchar("weightLevel", { length: 50 }),
  五行归属: varchar("wuxingAttr", { length: 10 }),
  三色审计: varchar("triColor", { length: 10 }),
  贡献值: int("contribution"),
  热度状态: varchar("heatStatus", { length: 50 }),
  去向判定: varchar("destination", { length: 100 }),
  // 五桶分拣
  bucket: mysqlEnum("bucket", ["log", "storage", "internal", "iter_pool", "archive", "fused"]).default("storage").notNull(),
  // 状态
  status: mysqlEnum("status", ["raw", "cleansing", "cleansed", "dna_stamped", "sorted", "archived"]).default("raw").notNull(),
  cleansedContent: text("cleansedContent"),
  metadata: json("metadata"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().notNull().$onUpdate(() => new Date()),
});

// ========== DNA注册表v2（新版干支卦格式） ==========
export const dnaRegistryV2 = mysqlTable("dna_registry_v2", {
  id: serial("id").primaryKey(),
  dnaV2: varchar("dnaV2", { length: 255 }).notNull().unique(),
  stamp: varchar("stamp", { length: 200 }).notNull(), // #龍芯⚡️丙午·甲午·丁丑·巳时·䷀乾
  module: varchar("module", { length: 100 }).notNull(),
  action: varchar("action", { length: 100 }).notNull(),
  hash8: varchar("hash8", { length: 16 }).notNull(),
  年干支: varchar("yearGz", { length: 10 }),
  月干支: varchar("monthGz", { length: 10 }),
  日干支: varchar("dayGz", { length: 10 }),
  时辰名: varchar("hourName", { length: 20 }),
  卦名: varchar("guaName", { length: 20 }),
  五行: varchar("wuxing", { length: 10 }),
  entityId: bigint("entityId", { mode: "number", unsigned: true }), // 关联intake_entries等
  entityType: varchar("entityType", { length: 50 }), // intake/recharge/skill等
  dnaV1: varchar("dnaV1", { length: 255 }), // 旧版关联
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

// Types
export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;
export type SmKey = typeof smKeys.$inferSelect;
export type DeviceCert = typeof deviceCerts.$inferSelect;
export type TwoFactorAuth = typeof twoFactorAuth.$inferSelect;
export type ContentItem = typeof contentItems.$inferSelect;
export type PersonaConfig = typeof personaConfigs.$inferSelect;
export type AuditLog = typeof auditLogs.$inferSelect;
export type Session = typeof sessions.$inferSelect;
export type SkillRegistry = typeof skillRegistry.$inferSelect;
export type PaymentCallback = typeof paymentCallbacks.$inferSelect;
export type RechargeRecord = typeof rechargeRecords.$inferSelect;
export type IntakeEntry = typeof intakeEntries.$inferSelect;
export type DnaRegistryV2 = typeof dnaRegistryV2.$inferSelect;

// ========== 守护扫描表（红队） ==========
export const guardianScans = mysqlTable("guardian_scans", {
  id: serial("id").primaryKey(),
  scanName: varchar("scanName", { length: 255 }).notNull(),
  scanType: mysqlEnum("scanType", [
    "dna_compliance",    // DNA合规扫描
    "code_quality",      // 代码质量扫描
    "security_vuln",     // 安全漏洞扫描
    "config_audit",      // 配置安全审计
    "supervisor_check",  // 三监督机制检查
    "system_health",     // 系统健康检查
    "integrity_verify",  // 完整性验证
  ]).notNull(),
  team: mysqlEnum("team", ["red", "blue"]).notNull(), // 红队/蓝队
  status: mysqlEnum("status", ["pending", "running", "completed", "failed", "timeout"]).default("pending"),
  severity: mysqlEnum("severity", ["info", "warning", "critical"]).default("info"),
  findings: json("findings"), // 扫描发现 [{issue, severity, location, evidence}]
  score: int("score").default(100), // 健康分 0-100
  targetModule: varchar("targetModule", { length: 255 }), // 扫描目标模块
  executionMs: int("executionMs"), // 执行耗时ms
  dnaMarker: varchar("dnaMarker", { length: 255 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

// ========== 修复记录表（蓝队） ==========
export const guardianRemediations = mysqlTable("guardian_remediations", {
  id: serial("id").primaryKey(),
  scanId: bigint("scanId", { mode: "number", unsigned: true }).notNull(),
  issue: varchar("issue", { length: 500 }).notNull(),
  remediationType: mysqlEnum("remediationType", [
    "auto_fixed",     // 自动修复
    "manual_fix",     // 人工修复
    "wont_fix",       // 不修复（已接受）
    "false_positive", // 误报
  ]).default("manual_fix").notNull(),
  actionTaken: text("actionTaken"), // 具体修复动作
  beforeState: json("beforeState"), // 修复前状态
  afterState: json("afterState"),   // 修复后状态
  verified: boolean("verified").default(false), // 是否验证通过
  verifiedAt: timestamp("verifiedAt"),
  severity: mysqlEnum("severity", ["info", "warning", "critical"]).default("info"),
  dnaMarker: varchar("dnaMarker", { length: 255 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().notNull().$onUpdate(() => new Date()),
});

// ========== 流水线运行记录 ==========
export const pipelineRuns = mysqlTable("pipeline_runs", {
  id: serial("id").primaryKey(),
  runName: varchar("runName", { length: 255 }).notNull(),
  status: mysqlEnum("status", ["running", "completed", "failed", "partial"]).default("running"),
  stages: json("stages"), // [{stage, status, startedAt, completedAt}]
  summary: json("summary"), // {totalScans, issuesFound, autoFixed, manualRequired, score}
  triggeredBy: varchar("triggeredBy", { length: 50 }).default("auto"), // auto/manual/webhook
  dnaMarker: varchar("dnaMarker", { length: 255 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  completedAt: timestamp("completedAt"),
});
