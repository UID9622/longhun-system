/**
 * 龍魂支付消息队列
 * DNA: #龍芯⚡️2026-07-11-LONGHUN-PAYMENT-QUEUE-v1.0
 * 内存队列 + 异步消费 + 幂等性
 */
import { getDb } from "../queries/connection";
import { paymentCallbacks, rechargeRecords, auditLogs } from "@db/schema";
import { eq } from "drizzle-orm";
import { sm3, dnaSign } from "./sm-crypto";

const db = getDb();

// ========== 内存消息队列 ==========
type QueueItem = {
  billNo: string;
  amount: string;
  currency: string;
  payerId?: string;
  payerName?: string;
  rawData: any;
  enqueuedAt: number;
  retries: number;
};

class PaymentQueue {
  private queue: QueueItem[] = [];
  private processing = false;
  private processedBillNos = new Set<string>();
  private maxRetries = 3;
  private concurrentLimit = 5;
  private activeConsumers = 0;

  // 入队
  enqueue(item: QueueItem): boolean {
    // 幂等性检查：内存层面快速去重
    if (this.processedBillNos.has(item.billNo)) {
      console.log(`[PaymentQueue] 重复通知已过滤: ${item.billNo}`);
      return false;
    }
    this.queue.push(item);
    console.log(`[PaymentQueue] 入队: ${item.billNo}, 队列长度: ${this.queue.length}`);
    this.startConsumer();
    return true;
  }

  // 启动消费者
  private startConsumer() {
    if (this.processing || this.queue.length === 0) return;
    this.processing = true;
    this.consumeLoop();
  }

  // 消费循环
  private async consumeLoop() {
    while (this.queue.length > 0 || this.activeConsumers > 0) {
      // 并发控制
      while (this.activeConsumers < this.concurrentLimit && this.queue.length > 0) {
        const item = this.queue.shift()!;
        this.activeConsumers++;
        this.processItem(item).finally(() => {
          this.activeConsumers--;
        });
      }
      // 小延迟防止CPU空转
      await this.sleep(50);
    }
    this.processing = false;
    console.log("[PaymentQueue] 消费者空闲");
  }

  // 处理单个消息
  private async processItem(item: QueueItem) {
    const startTime = Date.now();
    try {
      console.log(`[PaymentQueue] 处理: ${item.billNo}`);

      // 1. 数据库幂等性检查
      const existing = await db.select().from(paymentCallbacks)
        .where(eq(paymentCallbacks.billNo, item.billNo));

      if (existing.length > 0 && existing[0].status === "success") {
        console.log(`[PaymentQueue] 已处理过: ${item.billNo}`);
        this.processedBillNos.add(item.billNo);
        return;
      }

      // 2. 更新状态为处理中
      if (existing.length > 0) {
        await db.update(paymentCallbacks)
          .set({ status: "processing", retryCount: item.retries })
          .where(eq(paymentCallbacks.billNo, item.billNo));
      } else {
        await db.insert(paymentCallbacks).values({
          billNo: item.billNo,
          amount: item.amount,
          currency: item.currency,
          payerId: item.payerId,
          payerName: item.payerName,
          status: "processing",
          callbackData: item.rawData,
          dnaMarker: dnaSign(item.billNo + item.amount, "支付回调"),
        });
      }

      // 3. 业务处理：匹配充值记录并激活
      await this.processBusiness(item);

      // 4. 标记成功
      await db.update(paymentCallbacks)
        .set({ status: "success", processedAt: new Date() })
        .where(eq(paymentCallbacks.billNo, item.billNo));

      this.processedBillNos.add(item.billNo);

      // 5. 审计日志
      await db.insert(auditLogs).values({
        action: "payment.callback.success",
        resource: `payment:${item.billNo}`,
        method: "QUEUE",
        severity: "info",
        details: { amount: item.amount, duration: Date.now() - startTime },
        dnaMarker: dnaSign(item.billNo, "支付成功"),
      });

      console.log(`[PaymentQueue] 成功: ${item.billNo}, 耗时: ${Date.now() - startTime}ms`);

    } catch (err: any) {
      console.error(`[PaymentQueue] 失败: ${item.billNo}, 错误: ${err.message}`);

      // 重试逻辑
      if (item.retries < this.maxRetries) {
        item.retries++;
        item.enqueuedAt = Date.now();
        this.queue.push(item);
        console.log(`[PaymentQueue] 重新入队: ${item.billNo}, 第${item.retries}次重试`);
      } else {
        // 标记失败
        await db.update(paymentCallbacks)
          .set({ status: "failed", errorMsg: err.message })
          .where(eq(paymentCallbacks.billNo, item.billNo));

        await db.insert(auditLogs).values({
          action: "payment.callback.failed",
          resource: `payment:${item.billNo}`,
          method: "QUEUE",
          severity: "critical",
          details: { error: err.message, retries: item.retries },
        });
      }
    }
  }

  // 业务处理：匹配充值记录
  private async processBusiness(item: QueueItem) {
    // 查找匹配的充值记录
    const recharges = await db.select().from(rechargeRecords)
      .where(eq(rechargeRecords.billNo, item.billNo));

    if (recharges.length === 0) {
      // 无匹配记录，创建一条匿名充值（后续可关联用户）
      await db.insert(rechargeRecords).values({
        userId: 0, // 匿名，后续关联
        billNo: item.billNo,
        amount: item.amount,
        currency: item.currency,
        status: "paid",
        paymentMethod: "ecny",
        metadata: { autoCreated: true, payerId: item.payerId },
        dnaMarker: dnaSign(item.billNo + item.amount, "匿名充值"),
      });
    } else {
      // 更新充值状态
      const recharge = recharges[0];
      if (recharge.status === "initiated") {
        await db.update(rechargeRecords)
          .set({ status: "paid", updatedAt: new Date() })
          .where(eq(rechargeRecords.id, recharge.id));

        // TODO: 这里触发用户激活逻辑
        // 比如：更新用户余额、激活VIP、发放权限等
        console.log(`[PaymentQueue] 用户 ${recharge.userId} 充值确认: ${item.amount} ${item.currency}`);
      }
    }
  }

  private sleep(ms: number): Promise<void> {
    return new Promise((r) => setTimeout(r, ms));
  }

  // 获取队列状态（用于监控）
  getStatus() {
    return {
      pending: this.queue.length,
      activeConsumers: this.activeConsumers,
      processing: this.processing,
      processedCount: this.processedBillNos.size,
    };
  }
}

// 单例导出
export const paymentQueue = new PaymentQueue();
