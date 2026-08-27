# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 龍魂 e-CNY 支付回调路由
 * DNA: #龍芯⚡️丙午·乙未·丙戌·甲午·䷕贲-LONGHUN-PAYMENT-ROUTER-v1.0
 * 接收支付平台回调 → 入队 → 异步处理 → 幂等性保证
 */
import { z } from "zod";
import { eq, desc } from "drizzle-orm";
import { getDb } from "../queries/connection";
import { paymentCallbacks, rechargeRecords, auditLogs } from "@db/schema";
import { createRouter, publicQuery, authedQuery } from "../middleware";
import { paymentQueue } from "../lib/payment-queue";
import { sm3, dnaSign } from "../lib/sm-crypto";

const db = getDb();

// ========== 回调签名验证 ==========
function verifyCallbackSignature(payload: any, signature: string, secret: string): boolean {
  const sortedKeys = Object.keys(payload).sort();
  const signStr = sortedKeys.map((k) => `${k}=${payload[k]}`).join("&") + `&key=${secret}`;
  return sm3(signStr) === signature;
}

export const paymentRouter = createRouter({
  // ===== 1. 支付回调接收端（对外接口，数字人民币平台调用）=====
  webhook: publicQuery
    .input(
      z.object({
        billNo: z.string(),
        amount: z.string(),
        currency: z.string().default("CNY"),
        payerId: z.string().optional(),
        payerName: z.string().optional(),
        payTime: z.string().optional(),
        status: z.enum(["SUCCESS", "FAILED", "PENDING"]).default("SUCCESS"),
        signature: z.string().optional(),
      }).passthrough()
    )
    .mutation(async ({ input }) => {
      const startTime = Date.now();

      try {
        // 1. 快速入队（立即返回200，不阻塞支付平台）
        const enqueued = paymentQueue.enqueue({
          billNo: input.billNo,
          amount: input.amount,
          currency: input.currency,
          payerId: input.payerId,
          payerName: input.payerName,
          rawData: input,
          enqueuedAt: Date.now(),
          retries: 0,
        });

        // 2. 记录接收日志
        await db.insert(auditLogs).values({
          action: "payment.webhook.received",
          resource: `bill:${input.billNo}`,
          method: "POST",
          severity: "info",
          details: {
            amount: input.amount,
            currency: input.currency,
            enqueued,
            elapsed: Date.now() - startTime,
          },
          dnaMarker: dnaSign(input.billNo, "webhook接收"),
        });

        // 3. 立即返回成功（异步处理在后面）
        return {
          code: "SUCCESS",
          message: "已接收",
          billNo: input.billNo,
          enqueueStatus: enqueued ? "QUEUED" : "DUPLICATE",
          processedAt: new Date().toISOString(),
        };

      } catch (err: any) {
        // 记录异常但还是要返回200（防止支付平台重试风暴）
        await db.insert(auditLogs).values({
          action: "payment.webhook.error",
          resource: `bill:${input.billNo}`,
          method: "POST",
          severity: "critical",
          details: { error: err.message },
        });

        return {
          code: "SUCCESS", // 仍然返回成功，避免重试
          message: "已接收",
          billNo: input.billNo,
          enqueueStatus: "ACCEPTED",
        };
      }
    }),

  // ===== 2. 主动查询支付状态（兜底）=====
  queryStatus: authedQuery
    .input(z.object({ billNo: z.string() }))
    .query(async ({ input }) => {
      const callbacks = await db.select().from(paymentCallbacks)
        .where(eq(paymentCallbacks.billNo, input.billNo));
      const recharges = await db.select().from(rechargeRecords)
        .where(eq(rechargeRecords.billNo, input.billNo));

      return {
        billNo: input.billNo,
        callback: callbacks[0] ?? null,
        recharge: recharges[0] ?? null,
        queueStatus: paymentQueue.getStatus(),
      };
    }),

  // ===== 3. 发起充值（前端调用）=====
  initiateRecharge: authedQuery
    .input(
      z.object({
        amount: z.string(),
        currency: z.string().default("CNY"),
        paymentMethod: z.enum(["ecny", "alipay", "wechat", "bank"]).default("ecny"),
        metadata: z.any().optional(),
      })
    )
    .mutation(async ({ input, ctx }) => {
      const userId = ctx.user?.id ?? 0;
      const billNo = `LH${Date.now()}${Math.random().toString(36).substring(2, 8).toUpperCase()}`;
      const dna = dnaSign(billNo + input.amount, "充值发起");

      const result = await db.insert(rechargeRecords).values({
        userId,
        billNo,
        amount: input.amount,
        currency: input.currency,
        status: "initiated",
        paymentMethod: input.paymentMethod,
        metadata: {
          ...input.metadata,
          userAgent: ctx.req.headers.get("user-agent"),
        },
        dnaMarker: dna,
      });

      await db.insert(auditLogs).values({
        userId,
        action: "recharge.initiated",
        resource: `recharge:${billNo}`,
        method: "POST",
        severity: "info",
        details: { amount: input.amount, currency: input.currency },
        dnaMarker: dna,
      });

      return {
        billNo,
        amount: input.amount,
        currency: input.currency,
        status: "initiated",
        payUrl: `/api/trpc/payment.payPage?billNo=${billNo}`,
        dna,
      };
    }),

  // ===== 4. 获取充值记录 =====
  rechargeList: authedQuery
    .input(
      z.object({
        status: z.string().optional(),
        limit: z.number().min(1).max(200).optional(),
      }).optional()
    )
    .query(async ({ input, ctx }) => {
      const userId = ctx.user?.id;
      const limit = input?.limit ?? 50;

      let query = db.select().from(rechargeRecords)
        .where(eq(rechargeRecords.userId, userId!))
        .orderBy(desc(rechargeRecords.createdAt))
        .limit(limit);

      return query;
    }),

  // ===== 5. 模拟支付（测试用）=====
  simulatePay: authedQuery
    .input(z.object({ billNo: z.string(), amount: z.string().optional() }))
    .mutation(async ({ input }) => {
      // 构造模拟回调数据
      const mockCallback = {
        billNo: input.billNo,
        amount: input.amount ?? "1.00",
        currency: "CNY",
        payerId: "SIMULATED",
        payerName: "测试用户",
        payTime: new Date().toISOString(),
        status: "SUCCESS" as const,
      };

      // 直接入队处理
      paymentQueue.enqueue({
        billNo: mockCallback.billNo,
        amount: mockCallback.amount,
        currency: mockCallback.currency,
        payerId: mockCallback.payerId,
        payerName: mockCallback.payerName,
        rawData: mockCallback,
        enqueuedAt: Date.now(),
        retries: 0,
      });

      return { success: true, message: "模拟支付已触发", billNo: input.billNo };
    }),

  // ===== 6. 队列状态（监控用）=====
  queueStatus: authedQuery.query(() => {
    return paymentQueue.getStatus();
  }),

  // ===== 7. 回调记录查询 =====
  callbackList: authedQuery
    .input(
      z.object({
        status: z.string().optional(),
        limit: z.number().min(1).max(200).optional(),
      }).optional()
    )
    .query(async ({ input }) => {
      const limit = input?.limit ?? 50;
      return db.select().from(paymentCallbacks)
        .orderBy(desc(paymentCallbacks.createdAt))
        .limit(limit);
    }),
});
