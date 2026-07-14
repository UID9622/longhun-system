/**
 * 龍魂容器收入口路由
 * DNA: #龍芯⚡️2026-07-12-LONGHUN-INTAKE-ROUTER-v1.0
 * 统一数据入口 → 清洗 → 六维评估 → DNA盖章(v∞) → 五桶分拣
 */
import { z } from "zod";
import { eq, desc, sql } from "drizzle-orm";
import { getDb } from "../queries/connection";
import { intakeEntries, dnaRegistryV2, auditLogs } from "@db/schema";
import { createRouter, authedQuery } from "../middleware";
import {
  获取四柱,
  生成DNAv2,
  六维评估,
  四柱字符串,
  今日DNA回单,
} from "../lib/ganzhi";
import { dnaSign } from "../lib/sm-crypto";

const db = getDb();

export const intakeRouter = createRouter({
  // ===== 1. 粘贴入口 (Drop Zone) =====
  drop: authedQuery
    .input(
      z.object({
        content: z.string().min(1),
        contentType: z.enum(["text", "code", "link", "image", "mixed"]).default("text"),
        source: z.string().default("manual"),
        metadata: z.any().optional(),
      })
    )
    .mutation(async ({ input, ctx }) => {
      const userId = ctx.user?.id ?? 0;
      const now = new Date();

      // 1. 获取四柱
      const gz = 获取四柱(now);

      // 2. 六维评估
      const eval6 = 六维评估(input.content, input.metadata);

      // 3. 生成v∞ DNA
      const dna = 生成DNAv2("INTAKE", "DROP", input.content.substring(0, 50));

      // 4. 确定桶
      const bucketMap: Record<string, string> = {
        "🟢 桶1·推草日志": "log",
        "📦 桶2·入库": "storage",
        "⚡ 桶3·内部消化": "internal",
        "🔁 桶4·升级为系统能力": "iter_pool",
        "🔁 桶4·待迭代池": "iter_pool",
        "💤 桶5·归档": "archive",
        "🔴 熔断·留L4证据链": "fused",
      };
      const bucket = (bucketMap[eval6.去向判定] ?? "storage") as any;

      // 5. 写入intake_entries
      const result = await db.insert(intakeEntries).values({
        userId,
        rawContent: input.content,
        contentType: input.contentType,
        source: input.source,
        dnaV2: dna.full,
        年干支: gz.年干支,
        月干支: gz.月干支,
        日干支: gz.日干支,
        时辰名: gz.时辰名,
        卦名: gz.卦名,
        五行: gz.五行,
        数字根: gz.数字根,
        权重层级: eval6.权重层级,
        五行归属: eval6.五行归属,
        三色审计: eval6.三色审计,
        贡献值: eval6.贡献值,
        热度状态: eval6.热度状态,
        去向判定: eval6.去向判定,
        bucket,
        status: "dna_stamped",
        cleansedContent: input.content.trim(),
        metadata: input.metadata,
      });

      const entryId = Number(result[0].insertId);

      // 6. 写入DNA注册表v2
      await db.insert(dnaRegistryV2).values({
        dnaV2: dna.full,
        stamp: dna.stamp,
        module: dna.module,
        action: dna.action,
        hash8: dna.hash8,
        年干支: gz.年干支,
        月干支: gz.月干支,
        日干支: gz.日干支,
        时辰名: gz.时辰名,
        卦名: gz.卦名,
        五行: gz.五行,
        entityId: entryId,
        entityType: "intake",
      });

      // 7. 审计日志
      await db.insert(auditLogs).values({
        userId,
        action: "intake.drop",
        resource: `intake:${entryId}`,
        method: "POST",
        severity: eval6.三色审计 === "🔴" ? "critical" : eval6.三色审计 === "🟡" ? "warning" : "info",
        details: { dna: dna.full, bucket, eval6 },
        dnaMarker: dnaSign(input.content.substring(0, 100), "容器收入口"),
      });

      return {
        id: entryId,
        dna: dna.full,
        stamp: dna.stamp,
        ganzhi: 四柱字符串(gz),
        eval6,
        bucket,
        status: "dna_stamped",
      };
    }),

  // ===== 2. 批量粘贴 =====
  batchDrop: authedQuery
    .input(z.object({ items: z.array(z.object({ content: z.string(), contentType: z.string().optional() })) }))
    .mutation(async ({ input, ctx }) => {
      const results = [];
      for (const item of input.items) {
        const r = await (intakeRouter._def.procedures as any).drop?.resolve?.({
          input: { content: item.content, contentType: (item.contentType ?? "text") as any, source: "batch" },
          ctx: { ...ctx, req: { headers: new Headers() } as any },
        });
        if (r) results.push(r);
      }
      return { count: results.length, results };
    }),

  // ===== 3. 列表查询 =====
  list: authedQuery
    .input(
      z.object({
        bucket: z.string().optional(),
        status: z.string().optional(),
        triColor: z.string().optional(),
        limit: z.number().min(1).max(200).optional(),
      }).optional()
    )
    .query(async ({ input }) => {
      const limit = input?.limit ?? 50;
      return db.select().from(intakeEntries)
        .orderBy(desc(intakeEntries.createdAt))
        .limit(limit);
    }),

  // ===== 4. 更新状态 =====
  updateStatus: authedQuery
    .input(z.object({ id: z.number(), status: z.string(), bucket: z.string().optional() }))
    .mutation(async ({ input }) => {
      const data: any = { status: input.status };
      if (input.bucket) data.bucket = input.bucket;
      await db.update(intakeEntries).set(data).where(eq(intakeEntries.id, input.id));
      return { success: true };
    }),

  // ===== 5. DNA注册表v2查询 =====
  dnaList: authedQuery
    .input(z.object({ module: z.string().optional(), limit: z.number().optional() }).optional())
    .query(async ({ input }) => {
      const limit = input?.limit ?? 50;
      return db.select().from(dnaRegistryV2)
        .orderBy(desc(dnaRegistryV2.createdAt))
        .limit(limit);
    }),

  // ===== 6. 统计面板 =====
  stats: authedQuery.query(async () => {
    const [total] = await db.select({ count: sql<number>`count(*)` }).from(intakeEntries);
    const [dnatotal] = await db.select({ count: sql<number>`count(*)` }).from(dnaRegistryV2);
    const buckets = await db
      .select({ bucket: intakeEntries.bucket, count: sql<number>`count(*)` })
      .from(intakeEntries)
      .groupBy(intakeEntries.bucket);
    const colors = await db
      .select({ color: intakeEntries.三色审计, count: sql<number>`count(*)` })
      .from(intakeEntries)
      .groupBy(intakeEntries.三色审计);
    return {
      total: Number(total?.count ?? 0),
      dnaTotal: Number(dnatotal?.count ?? 0),
      buckets,
      colors,
      todayDNA: 今日DNA回单(),
    };
  }),

  // ===== 7. 删除 (实际是冻结) =====
  freeze: authedQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input }) => {
      await db.update(intakeEntries)
        .set({ status: "archived", bucket: "archive" })
        .where(eq(intakeEntries.id, input.id));
      return { success: true };
    }),
});
