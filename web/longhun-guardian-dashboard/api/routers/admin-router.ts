/**
 * 龍魂操作台管理路由
 * DNA: #龍芯⚡️丙午·乙未·丙戌·甲午·䷕贲-LONGHUN-ADMIN-ROUTER-v1.0
 */
import { z } from "zod";
import { eq, desc, and, like, sql } from "drizzle-orm";
import { getDb } from "../queries/connection";
const db = getDb();
import {
  smKeys,
  deviceCerts,
  twoFactorAuth,
  contentItems,
  personaConfigs,
  auditLogs,
  sessions,
  skillRegistry,
} from "@db/schema";
import { createRouter, authedQuery, adminQuery } from "../middleware";
import {
  sm3,
  sm4_encrypt,
  sm4_decrypt,
  dnaSign,
  generateSM4Key,
  generateSecretKey,
} from "../lib/sm-crypto";

export const adminRouter = createRouter({
  // ===== 国密操作 =====
  sm3Hash: authedQuery
    .input(z.object({ data: z.string() }))
    .mutation(({ input }) => ({
      hash: sm3(input.data),
      algorithm: "SM3",
      dna: dnaSign(input.data, "龍魂国密SM3"),
    })),

  sm4Encrypt: authedQuery
    .input(z.object({ plaintext: z.string(), key: z.string() }))
    .mutation(({ input }) => ({
      ciphertext: sm4_encrypt(input.plaintext, input.key),
      keyHint: input.key.substring(0, 8) + "...",
      algorithm: "SM4-CBC",
    })),

  sm4Decrypt: authedQuery
    .input(z.object({ ciphertext: z.string(), key: z.string() }))
    .mutation(({ input }) => ({
      plaintext: sm4_decrypt(input.ciphertext, input.key),
      algorithm: "SM4-CBC",
    })),

  generateSMKey: authedQuery
    .input(z.object({ name: z.string(), type: z.enum(["sm4", "secret"]) }))
    .mutation(({ input }) => ({
      key: input.type === "sm4" ? generateSM4Key() : generateSecretKey(),
      name: input.name,
      type: input.type,
      dna: dnaSign(input.name + input.type, "龍魂密钥生成"),
    })),

  dnaSign: authedQuery
    .input(z.object({ data: z.string(), secret: z.string() }))
    .mutation(({ input }) => ({
      signature: dnaSign(input.data, input.secret),
    })),

  // ===== 仪表盘统计 =====
  dashboardStats: adminQuery.query(async () => {
    const [userCount] = await db
      .select({ count: sql<number>`count(*)` })
      .from(sql`users`);
    const [deviceCount] = await db
      .select({ count: sql<number>`count(*)` })
      .from(deviceCerts);
    const [contentCount] = await db
      .select({ count: sql<number>`count(*)` })
      .from(contentItems);
    const [auditCount] = await db
      .select({ count: sql<number>`count(*)` })
      .from(auditLogs);
    const [personaCount] = await db
      .select({ count: sql<number>`count(*)` })
      .from(personaConfigs);
    const [skillCount] = await db
      .select({ count: sql<number>`count(*)` })
      .from(skillRegistry);

    const recentAudits = await db
      .select()
      .from(auditLogs)
      .orderBy(desc(auditLogs.createdAt))
      .limit(10);

    return {
      stats: {
        users: Number(userCount?.count ?? 0),
        devices: Number(deviceCount?.count ?? 0),
        contents: Number(contentCount?.count ?? 0),
        audits: Number(auditCount?.count ?? 0),
        personas: Number(personaCount?.count ?? 0),
        skills: Number(skillCount?.count ?? 0),
      },
      recentAudits,
    };
  }),

  // ===== 设备证书管理 =====
  deviceList: authedQuery.query(async () => {
    return db.select().from(deviceCerts).orderBy(desc(deviceCerts.createdAt));
  }),

  deviceCreate: authedQuery
    .input(
      z.object({
        userId: z.number(),
        deviceType: z.enum(["huawei", "apple", "other"]),
        deviceName: z.string().optional(),
        deviceModel: z.string().optional(),
        certificatePem: z.string().optional(),
        fingerprint: z.string().optional(),
      }),
    )
    .mutation(async ({ input }) => {
      const result = await db.insert(deviceCerts).values({
        ...input,
        isTrusted: false,
      });
      await db.insert(auditLogs).values({
        action: "device.create",
        resource: `device:${result[0].insertId}`,
        method: "POST",
        severity: "info",
        dnaMarker: dnaSign(JSON.stringify(input), "设备证书创建"),
      });
      return { id: Number(result[0].insertId), success: true };
    }),

  deviceUpdateTrust: authedQuery
    .input(z.object({ id: z.number(), isTrusted: z.boolean() }))
    .mutation(async ({ input }) => {
      await db
        .update(deviceCerts)
        .set({ isTrusted: input.isTrusted })
        .where(eq(deviceCerts.id, input.id));
      return { success: true };
    }),

  deviceDelete: authedQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input }) => {
      await db.delete(deviceCerts).where(eq(deviceCerts.id, input.id));
      return { success: true };
    }),

  // ===== 二次验证 =====
  twoFactorGet: authedQuery
    .input(z.object({ userId: z.number() }))
    .query(async ({ input }) => {
      const rows = await db
        .select()
        .from(twoFactorAuth)
        .where(eq(twoFactorAuth.userId, input.userId));
      return rows[0] ?? null;
    }),

  twoFactorSetup: authedQuery
    .input(
      z.object({
        userId: z.number(),
        method: z.enum(["sms", "email", "totp", "huawei"]),
        secret: z.string(),
      }),
    )
    .mutation(async ({ input }) => {
      await db.insert(twoFactorAuth).values({
        ...input,
        isEnabled: true,
        verifiedAt: new Date(),
      });
      return { success: true };
    }),

  twoFactorVerify: authedQuery
    .input(
      z.object({
        userId: z.number(),
        code: z.string(),
      }),
    )
    .mutation(async ({ input }) => {
      const rows = await db
        .select()
        .from(twoFactorAuth)
        .where(eq(twoFactorAuth.userId, input.userId));
      const tf = rows[0];
      if (!tf || !tf.isEnabled) return { verified: false };

      const valid = tf.method === "totp"
        ? sm3(input.code) === tf.secret
        : input.code === tf.secret;

      return { verified: valid };
    }),

  // ===== 内容管理 =====
  contentList: authedQuery
    .input(
      z
        .object({
          type: z.string().optional(),
          status: z.string().optional(),
          search: z.string().optional(),
        })
        .optional(),
    )
    .query(async ({ input }) => {
      let query = db.select().from(contentItems).orderBy(desc(contentItems.createdAt));
      const conditions = [];
      if (input?.type) conditions.push(eq(contentItems.type, input.type as any));
      if (input?.status) conditions.push(eq(contentItems.status, input.status as any));
      if (input?.search) conditions.push(like(contentItems.title, `%${input.search}%`));
      if (conditions.length > 0) {
        return db
          .select()
          .from(contentItems)
          .where(and(...conditions))
          .orderBy(desc(contentItems.createdAt));
      }
      return query;
    }),

  contentCreate: authedQuery
    .input(
      z.object({
        userId: z.number(),
        type: z.enum(["skill", "persona", "document", "config", "audit"]),
        title: z.string(),
        slug: z.string(),
        content: z.string().optional(),
        metadata: z.any().optional(),
        tags: z.string().optional(),
        status: z.enum(["draft", "published", "archived"]).optional(),
      }),
    )
    .mutation(async ({ input }) => {
      const dna = dnaSign(input.title + input.slug, "龍魂内容管理");
      const result = await db.insert(contentItems).values({
        ...input,
        status: input.status ?? "draft",
        dnaMarker: dna,
      });
      return { id: Number(result[0].insertId), dna, success: true };
    }),

  contentUpdate: authedQuery
    .input(
      z.object({
        id: z.number(),
        title: z.string().optional(),
        content: z.string().optional(),
        metadata: z.any().optional(),
        tags: z.string().optional(),
        status: z.enum(["draft", "published", "archived"]).optional(),
      }),
    )
    .mutation(async ({ input }) => {
      const { id, ...data } = input;
      await db.update(contentItems).set(data).where(eq(contentItems.id, id));
      return { success: true };
    }),

  contentDelete: authedQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input }) => {
      await db.delete(contentItems).where(eq(contentItems.id, input.id));
      return { success: true };
    }),

  // ===== 人格助手配置 =====
  personaList: authedQuery.query(async () => {
    return db
      .select()
      .from(personaConfigs)
      .orderBy(desc(personaConfigs.priority));
  }),

  personaCreate: authedQuery
    .input(
      z.object({
        userId: z.number(),
        personaName: z.string(),
        systemPrompt: z.string().optional(),
        triggerKeywords: z.string().optional(),
        responseStyle: z.enum(["formal", "casual", "military", "friendly"]).optional(),
        enabledSkills: z.any().optional(),
        priority: z.number().optional(),
      }),
    )
    .mutation(async ({ input }) => {
      const result = await db.insert(personaConfigs).values({
        ...input,
        isActive: true,
        responseStyle: input.responseStyle ?? "formal",
      });
      return { id: Number(result[0].insertId), success: true };
    }),

  personaUpdate: authedQuery
    .input(
      z.object({
        id: z.number(),
        personaName: z.string().optional(),
        systemPrompt: z.string().optional(),
        triggerKeywords: z.string().optional(),
        responseStyle: z.enum(["formal", "casual", "military", "friendly"]).optional(),
        enabledSkills: z.any().optional(),
        isActive: z.boolean().optional(),
        priority: z.number().optional(),
      }),
    )
    .mutation(async ({ input }) => {
      const { id, ...data } = input;
      await db.update(personaConfigs).set(data).where(eq(personaConfigs.id, id));
      return { success: true };
    }),

  personaDelete: authedQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input }) => {
      await db.delete(personaConfigs).where(eq(personaConfigs.id, input.id));
      return { success: true };
    }),

  // ===== 审计日志 =====
  auditList: authedQuery
    .input(
      z
        .object({
          severity: z.string().optional(),
          action: z.string().optional(),
          limit: z.number().min(1).max(500).optional(),
        })
        .optional(),
    )
    .query(async ({ input }) => {
      const limit = input?.limit ?? 100;
      let query = db
        .select()
        .from(auditLogs)
        .orderBy(desc(auditLogs.createdAt))
        .limit(limit);

      if (input?.severity) {
        return db
          .select()
          .from(auditLogs)
          .where(eq(auditLogs.severity, input.severity as any))
          .orderBy(desc(auditLogs.createdAt))
          .limit(limit);
      }
      return query;
    }),

  auditCreate: authedQuery
    .input(
      z.object({
        action: z.string(),
        resource: z.string().optional(),
        method: z.string().optional(),
        ipAddress: z.string().optional(),
        details: z.any().optional(),
        severity: z.enum(["info", "warning", "critical"]).optional(),
        dnaMarker: z.string().optional(),
      }),
    )
    .mutation(async ({ input, ctx }) => {
      await db.insert(auditLogs).values({
        ...input,
        userId: ctx.user?.id,
        severity: input.severity ?? "info",
        dnaMarker: input.dnaMarker ?? dnaSign(input.action, "审计日志"),
      });
      return { success: true };
    }),

  // ===== 技能注册表 =====
  skillList: authedQuery.query(async () => {
    return db
      .select()
      .from(skillRegistry)
      .orderBy(desc(skillRegistry.createdAt));
  }),

  skillCreate: adminQuery
    .input(
      z.object({
        skillName: z.string(),
        skillVersion: z.string().optional(),
        category: z.enum([
          "governance", "deploy", "mobile", "cloud", "security",
          "algorithm", "finance", "ai", "knowledge", "cnsh",
          "recognition", "research", "application", "system",
        ]),
        description: z.string().optional(),
        dnaMarker: z.string().optional(),
        dependencies: z.any().optional(),
      }),
    )
    .mutation(async ({ input }) => {
      const result = await db.insert(skillRegistry).values({
        ...input,
        skillVersion: input.skillVersion ?? "1.0",
      });
      return { id: Number(result[0].insertId), success: true };
    }),

  skillUpdate: adminQuery
    .input(
      z.object({
        id: z.number(),
        skillName: z.string().optional(),
        skillVersion: z.string().optional(),
        description: z.string().optional(),
        status: z.enum(["active", "inactive", "deprecated"]).optional(),
        dependencies: z.any().optional(),
      }),
    )
    .mutation(async ({ input }) => {
      const { id, ...data } = input;
      await db.update(skillRegistry).set(data).where(eq(skillRegistry.id, id));
      return { success: true };
    }),

  skillDelete: adminQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input }) => {
      await db.delete(skillRegistry).where(eq(skillRegistry.id, input.id));
      return { success: true };
    }),

  // ===== 国密密钥存储 =====
  smKeyList: authedQuery.query(async () => {
    return db.select().from(smKeys).orderBy(desc(smKeys.createdAt));
  }),

  smKeyCreate: authedQuery
    .input(
      z.object({
        userId: z.number(),
        keyName: z.string(),
        sm3Hash: z.string().optional(),
        sm4Key: z.string().optional(),
      }),
    )
    .mutation(async ({ input }) => {
      const dna = dnaSign(input.keyName + Date.now(), "SM密钥存储");
      const result = await db.insert(smKeys).values({
        ...input,
        dnaSignature: dna,
      });
      return { id: Number(result[0].insertId), dna, success: true };
    }),

  smKeyRevoke: authedQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input }) => {
      await db
        .update(smKeys)
        .set({ status: "revoked" })
        .where(eq(smKeys.id, input.id));
      return { success: true };
    }),
});
