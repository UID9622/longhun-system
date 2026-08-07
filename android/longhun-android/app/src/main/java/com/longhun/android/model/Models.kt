// DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-ANDROID-MODELS-v1.0-UID9622
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
//
// 龍魂·Android 数据模型

package com.longhun.android.model

import kotlinx.serialization.Serializable

/** 三色审计 */
@Serializable
enum class AuditMark {
    GREEN,   // 🟢 通过
    YELLOW,  // 🟡 待核
    RED,     // 🔴 红线
}

/** 监督配置 */
@Serializable
data class SupervisionConfig(
    val sensitivity: Double = 0.7,
    val dnaVerify: Boolean = true,
    val auditEnabled: Boolean = true,
    val maxDeviation: Double = 20.0,
)

/** 监督报告 */
@Serializable
data class SupervisionReport(
    val score: Double,
    val audit: AuditMark,
    val dnaValid: Boolean,
    val deviations: List<Deviation> = emptyList(),
    val timestamp: String = "",
    val recommendations: List<String> = emptyList(),
)

/** 偏差条目 */
@Serializable
data class Deviation(
    val field: String,
    val expected: String,
    val actual: String,
    val severity: AuditMark,
)

/** 记忆条目 */
@Serializable
data class MemoryEntry(
    val id: String,
    val priority: MemoryPriority,
    val content: String,
    val dna: String,
    val tags: List<String>,
    val createdAt: String,
    val updatedAt: String,
    val frozen: Boolean = false,
)

/** 记忆优先级 */
@Serializable
enum class MemoryPriority {
    P0,  // 永恒焊死
    P1,  // 核心协议
    P2,  // 工具定义
    P3,  // 常规记忆
}

/** 健康状态 */
@Serializable
data class HealthStatus(
    val status: String,       // healthy | degraded | critical
    val cpuPercent: Double = 0.0,
    val memoryUsedMB: Double = 0.0,
    val memoryTotalMB: Double = 0.0,
    val uptimeSeconds: Long = 0,
    val activeServices: List<String> = emptyList(),
    val auditCount: Long = 0,
    val lastCheck: String = "",
)
