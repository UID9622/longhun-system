# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 龍魂守护路由 · 红蓝对抗流水线
 * DNA: #龍芯⚡️丙午·乙未·丁亥·丙午·䷚颐-LONGHUN-GUARDIAN-ROUTER-v1.0
 */
import { z } from "zod";
import { eq, desc, sql } from "drizzle-orm";
import { getDb } from "../queries/connection";
import { guardianScans, guardianRemediations, pipelineRuns } from "@db/schema";
import { createRouter, authedQuery } from "../middleware";
import {
  runGuardianPipeline,
  scanDNACompliance,
  scanCodeQuality,
  scanSecurityVuln,
  scanConfigAudit,
  scanSupervisorCheck,
  scanSystemHealth,
  blueTeamRemediate,
} from "../lib/guardian-engine";
import { 生成DNAv2 } from "../lib/ganzhi";
import { dnaSign } from "../lib/sm-crypto";

const db = getDb();
const PROJECT_ROOT = process.cwd();

export const guardianRouter = createRouter({
  // ===== 1. 执行完整守护流水线 =====
  runPipeline: authedQuery
    .input(z.object({ trigger: z.enum(["manual", "auto", "webhook"]).default("manual").optional() }))
    .mutation(async ({ input, ctx }) => {
      const userId = ctx.user?.id ?? 0;
      const trigger = input?.trigger ?? "manual";

      // 创建流水线记录
      const dna = 生成DNAv2("GUARDIAN", "PIPELINE", trigger);
      const [runResult] = await db.insert(pipelineRuns).values({
        runName: `守护流水线-${new Date().toISOString()}`,
        status: "running",
        stages: [{ stage: "init", status: "running", startedAt: new Date().toISOString() }],
        summary: { totalScans: 0, issuesFound: 0, autoFixed: 0, manualRequired: 0, score: 100 },
        triggeredBy: trigger,
        dnaMarker: dna.full,
      });
      const runId = Number(runResult.insertId);

      // 执行流水线
      const result = await runGuardianPipeline(PROJECT_ROOT, trigger);

      // 保存所有扫描结果
      const scanIds: number[] = [];
      for (const stage of result.stages) {
        if (stage.result) {
          const sr = stage.result;
          const scanDna = 生成DNAv2("GUARDIAN", sr.scanType.toUpperCase(), sr.targetModule);
          const [scanResult] = await db.insert(guardianScans).values({
            scanName: `${sr.team === "red" ? "🔴红队" : "🔵蓝队"}·${getScanTypeLabel(sr.scanType)}`,
            scanType: sr.scanType as any,
            team: sr.team as any,
            status: sr.status as any,
            severity: sr.score < 40 ? "critical" : sr.score < 70 ? "warning" : "info",
            findings: sr.findings,
            score: sr.score,
            targetModule: sr.targetModule,
            executionMs: sr.executionMs,
            dnaMarker: scanDna.full,
          });
          scanIds.push(Number(scanResult.insertId));

          // 蓝队自动修复
          if (sr.team === "red" && sr.findings.length > 0) {
            const rems = await blueTeamRemediate(sr);
            for (const rem of rems) {
              await db.insert(guardianRemediations).values({
                scanId: Number(scanResult.insertId),
                issue: rem.issue,
                remediationType: rem.remediationType as any,
                actionTaken: rem.actionTaken,
                beforeState: rem.beforeState,
                afterState: rem.afterState,
                severity: rem.severity as any,
                dnaMarker: dnaSign(rem.issue.substring(0, 50), "guardian"),
              });
            }
          }
        }
      }

      // 更新流水线记录
      await db.update(pipelineRuns).set({
        status: result.status as any,
        stages: result.stages as any,
        summary: result.summary as any,
        completedAt: new Date(),
      }).where(eq(pipelineRuns.id, runId));

      return {
        runId,
        ...result,
        scanIds,
        dna: dna.full,
      };
    }),

  // ===== 2. 单独扫描 =====
  scan: authedQuery
    .input(z.object({
      scanType: z.enum(["dna_compliance", "code_quality", "security_vuln", "config_audit", "supervisor_check", "system_health"]),
    }))
    .mutation(async ({ input, ctx }) => {
      const userId = ctx.user?.id ?? 0;
      const dna = 生成DNAv2("GUARDIAN", input.scanType.toUpperCase());
      let result;

      switch (input.scanType) {
        case "dna_compliance": result = await scanDNACompliance(PROJECT_ROOT); break;
        case "code_quality": result = await scanCodeQuality(PROJECT_ROOT); break;
        case "security_vuln": result = await scanSecurityVuln(PROJECT_ROOT); break;
        case "config_audit": result = await scanConfigAudit(PROJECT_ROOT); break;
        case "supervisor_check": result = await scanSupervisorCheck(PROJECT_ROOT); break;
        case "system_health": result = await scanSystemHealth(); break;
      }

      // 保存扫描
      const [scanResult] = await db.insert(guardianScans).values({
        scanName: `🔴红队·${getScanTypeLabel(input.scanType)}`,
        scanType: input.scanType,
        team: "red",
        status: result.status as any,
        severity: result.score < 40 ? "critical" : result.score < 70 ? "warning" : "info",
        findings: result.findings,
        score: result.score,
        targetModule: result.targetModule,
        executionMs: result.executionMs,
        dnaMarker: dna.full,
      });
      const scanId = Number(scanResult.insertId);

      // 蓝队修复
      const rems = await blueTeamRemediate(result);
      for (const rem of rems) {
        await db.insert(guardianRemediations).values({
          scanId,
          issue: rem.issue,
          remediationType: rem.remediationType as any,
          actionTaken: rem.actionTaken,
          beforeState: rem.beforeState,
          afterState: rem.afterState,
          severity: rem.severity as any,
          dnaMarker: dnaSign(rem.issue.substring(0, 50), "guardian"),
        });
      }

      return { scanId, ...result, dna: dna.full, remediations: rems.length };
    }),

  // ===== 3. 扫描历史 =====
  scanHistory: authedQuery
    .input(z.object({ limit: z.number().min(1).max(100).optional(), team: z.enum(["red", "blue"]).optional() }).optional())
    .query(async ({ input }) => {
      const limit = input?.limit ?? 50;
      return db.select().from(guardianScans)
        .orderBy(desc(guardianScans.createdAt))
        .limit(limit);
    }),

  // ===== 4. 修复记录 =====
  remediationList: authedQuery
    .input(z.object({ scanId: z.number().optional(), limit: z.number().optional() }).optional())
    .query(async ({ input }) => {
      const limit = input?.limit ?? 50;
      return db.select().from(guardianRemediations)
        .orderBy(desc(guardianRemediations.createdAt))
        .limit(limit);
    }),

  // ===== 5. 流水线历史 =====
  pipelineHistory: authedQuery
    .input(z.object({ limit: z.number().optional() }).optional())
    .query(async ({ input }) => {
      const limit = input?.limit ?? 20;
      return db.select().from(pipelineRuns)
        .orderBy(desc(pipelineRuns.createdAt))
        .limit(limit);
    }),

  // ===== 6. 守护仪表盘 =====
  dashboard: authedQuery.query(async () => {
    const [totalScans] = await db.select({ count: sql<number>`count(*)` }).from(guardianScans);
    const [totalPipelines] = await db.select({ count: sql<number>`count(*)` }).from(pipelineRuns);
    const [totalRemediations] = await db.select({ count: sql<number>`count(*)` }).from(guardianRemediations);
    const [autoFixed] = await db.select({ count: sql<number>`count(*)` }).from(guardianRemediations).where(eq(guardianRemediations.remediationType, "auto_fixed"));

    const avgScore = await db.select({ avg: sql<number>`avg(score)` }).from(guardianScans);

    const recentScans = await db.select().from(guardianScans)
      .orderBy(desc(guardianScans.createdAt))
      .limit(10);

    const severityDist = await db
      .select({ severity: guardianScans.severity, count: sql<number>`count(*)` })
      .from(guardianScans)
      .groupBy(guardianScans.severity);

    return {
      stats: {
        totalScans: Number(totalScans?.count ?? 0),
        totalPipelines: Number(totalPipelines?.count ?? 0),
        totalRemediations: Number(totalRemediations?.count ?? 0),
        autoFixed: Number(autoFixed?.count ?? 0),
        manualRequired: Number(totalRemediations?.count ?? 0) - Number(autoFixed?.count ?? 0),
        avgScore: Math.round(Number(avgScore[0]?.avg ?? 100)),
      },
      severityDist,
      recentScans,
    };
  }),

  // ===== 7. 验证修复 =====
  verifyFix: authedQuery
    .input(z.object({ remediationId: z.number(), verified: z.boolean() }))
    .mutation(async ({ input }) => {
      await db.update(guardianRemediations).set({
        verified: input.verified,
        verifiedAt: new Date(),
      }).where(eq(guardianRemediations.id, input.remediationId));
      return { success: true };
    }),
});

function getScanTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    dna_compliance: "DNA合规扫描",
    code_quality: "代码质量扫描",
    security_vuln: "安全漏洞扫描",
    config_audit: "配置安全审计",
    supervisor_check: "三监督机制检查",
    system_health: "系统健康检查",
    integrity_verify: "完整性验证",
  };
  return labels[type] ?? type;
}
