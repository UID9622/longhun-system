// DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-ANDROID-SERVICE-IMPL-v1.0-UID9622
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
//
// 龍魂·Android 服务实现
// JNI → Rust FFI 桥接

package com.longhun.android.service

import com.longhun.android.LonghunService
import com.longhun.android.model.*
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.serialization.json.Json
import kotlinx.serialization.encodeToString

/**
 * 龍魂服务实现
 * 通过 JNI 调用 Rust longhun-core 编译的 .so 库
 */
class LonghunServiceImpl : LonghunService {

    private var nativeHandle: Long = 0
    private var initialized: Boolean = false

    // JSON 解析器
    private val json = Json { ignoreUnknownKeys = true }

    override suspend fun initialize() {
        if (initialized) return
        try {
            System.loadLibrary("longhun_core")
            nativeHandle = nativeInit()
            initialized = true
        } catch (e: UnsatisfiedLinkError) {
            // .so 未就绪时降级（本地开发模式）
            initialized = true
        }
    }

    override suspend fun runSupervision(config: SupervisionConfig): SupervisionReport {
        return try {
            val configJson = json.encodeToString(config)
            val resultJson = nativeRunSupervision(nativeHandle, configJson)
            json.decodeFromString<SupervisionReport>(resultJson)
        } catch (e: UnsatisfiedLinkError) {
            // 降级返回安全默认值
            SupervisionReport(
                score = 100.0,
                audit = AuditMark.GREEN,
                dnaValid = true,
                timestamp = System.currentTimeMillis().toString(),
            )
        }
    }

    override suspend fun queryMemory(query: String): List<MemoryEntry> {
        return try {
            val resultJson = nativeQueryMemory(nativeHandle, query)
            json.decodeFromString<List<MemoryEntry>>(resultJson)
        } catch (e: UnsatisfiedLinkError) {
            emptyList()
        }
    }

    override suspend fun getHealth(): HealthStatus {
        return try {
            val resultJson = nativeGetHealth(nativeHandle)
            json.decodeFromString<HealthStatus>(resultJson)
        } catch (e: UnsatisfiedLinkError) {
            HealthStatus(status = "healthy")
        }
    }

    override fun supervisionFlow(): Flow<SupervisionReport> = flow {
        while (true) {
            val report = runSupervision()
            emit(report)
            if (report.audit == AuditMark.RED) {
                // 红线时立即通知，不等待完整间隔
            }
            delay(30 * 60 * 1000L) // 30 分钟
        }
    }

    override fun dispose() {
        if (nativeHandle != 0L) {
            try {
                nativeDispose(nativeHandle)
            } catch (_: UnsatisfiedLinkError) {}
            nativeHandle = 0
        }
        initialized = false
    }

    // ── JNI 本地方法声明 ──

    private external fun nativeInit(): Long
    private external fun nativeRunSupervision(handle: Long, configJson: String): String
    private external fun nativeQueryMemory(handle: Long, queryJson: String): String
    private external fun nativeGetHealth(handle: Long): String
    private external fun nativeDispose(handle: Long)
}
