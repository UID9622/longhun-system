// DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-ANDROID-WORKER-v1.0-UID9622
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
//
// 龍魂·Android WorkManager 后台执行器
// 定期运行监督 · 自动学习闭环

package com.longhun.android

import android.content.Context
import androidx.work.*
import com.longhun.android.service.LonghunServiceImpl
import java.util.concurrent.TimeUnit

/**
 * 龍魂后台监督 Worker
 * 使用 WorkManager 实现可靠的周期后台执行
 */
class LonghunWorker(
    context: Context,
    params: WorkerParameters,
) : CoroutineWorker(context, params) {

    private val service = LonghunServiceImpl()

    override suspend fun doWork(): Result {
        return try {
            service.initialize()

            val report = service.runSupervision()
            
            // 红线告警
            if (report.audit == com.longhun.android.model.AuditMark.RED) {
                // 发送通知
                showRedlineNotification(report)
            }

            Result.success()
        } catch (e: Exception) {
            if (runAttemptCount < 3) {
                Result.retry()
            } else {
                Result.failure()
            }
        }
    }

    private fun showRedlineNotification(report: com.longhun.android.model.SupervisionReport) {
        // TODO: 通知渠道已在 Application 层配置
    }

    companion object {
        private const val WORK_NAME = "longhun_supervision"
        private const val INTERVAL_MINUTES = 30L

        /**
         * 调度后台监督任务
         */
        fun schedule(context: Context) {
            val constraints = Constraints.Builder()
                .setRequiredNetworkType(NetworkType.CONNECTED)
                .build()

            val request = PeriodicWorkRequestBuilder<LonghunWorker>(
                INTERVAL_MINUTES, TimeUnit.MINUTES
            )
                .setConstraints(constraints)
                .setBackoffCriteria(
                    BackoffPolicy.EXPONENTIAL,
                    1, TimeUnit.MINUTES
                )
                .build()

            WorkManager.getInstance(context).enqueueUniquePeriodicWork(
                WORK_NAME,
                ExistingPeriodicWorkPolicy.KEEP,
                request
            )
        }

        /**
         * 取消后台监督
         */
        fun cancel(context: Context) {
            WorkManager.getInstance(context).cancelUniqueWork(WORK_NAME)
        }

        /**
         * 立即执行一次监督
         */
        fun runNow(context: Context) {
            val request = OneTimeWorkRequestBuilder<LonghunWorker>()
                .build()
            WorkManager.getInstance(context).enqueue(request)
        }
    }
}
