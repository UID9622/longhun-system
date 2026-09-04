/*
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-ANDROID-JNI-v1.0-UID9622
 * CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 *
 * 龍魂·Android JNI 桥接层
 * Kotlin ↔ Rust FFI 桥接
 *
 * 编译:
 *   cd rust/longhun-core
 *   cargo build --release --target aarch64-linux-android
 *   cargo build --release --target armv7-linux-androideabi
 *   cp target/aarch64-linux-android/release/liblonghun_core.so \
 *      android/app/libs/arm64-v8a/
 *   cp target/armv7-linux-androideabi/release/liblonghun_core.so \
 *      android/app/libs/armeabi-v7a/
 */

#include <string.h>
#include <stdint.h>

// ── JNI 头文件兼容层 ──
// Android NDK 编译时：jni.h 在 NDK sysroot 内，clang 自动找到
// IDE 静态分析时：jni.h 不在 include path，提供桩定义避免红色波浪
#ifdef __has_include
  #if __has_include(<jni.h>)
    #include <jni.h>
    #define LONGHUN_JNI_REAL 1
  #endif
#else
  #include <jni.h>
  #define LONGHUN_JNI_REAL 1
#endif

#ifndef LONGHUN_JNI_REAL
  // IDE 静态分析桩：仅用于消除 clang 诊断，不影响 NDK 编译
  #include <stdarg.h>
  #define JNIEXPORT  __attribute__((visibility("default")))
  #define JNICALL
  typedef int64_t  jlong;
  typedef void*    jstring;
  typedef void*    jobject;
  typedef void*    jclass;
  typedef void*    jthrowable;
  typedef uint8_t  jboolean;
  typedef int8_t   jbyte;
  typedef uint16_t jchar;
  typedef int16_t  jshort;
  typedef int32_t  jint;
  typedef int64_t  jlong;
  typedef float    jfloat;
  typedef double   jdouble;
  typedef int32_t  jsize;
  typedef jint     jint;

  struct JNINativeInterface;
  typedef struct JNINativeInterface* JNIEnv;

  // 桩方法：仅供 IDE 索引
  static inline const char* jni_stub_GetStringUTFChars(JNIEnv* env, jstring str, void* isCopy) { return NULL; }
  static inline void        jni_stub_ReleaseStringUTFChars(JNIEnv* env, jstring str, const char* utf) {}
  static inline jstring     jni_stub_NewStringUTF(JNIEnv* env, const char* utf) { return NULL; }

  #define JNI_FALSE 0
  #define JNI_TRUE  1
#endif

// Rust FFI 头文件（由 cbindgen 生成）
// #include "longhun.h"

// ── Rust FFI 声明 ──
// 实际链接: longhun_core.so
extern char* longhun_run_supervision(const char* config_json);
extern char* longhun_query_memory(const char* query_json);
extern char* longhun_get_health(void);
extern void longhun_free_string(char* ptr);

// ── JNI 实现（NDK 编译走真实实现，IDE 静态分析走空桩）──

#ifdef LONGHUN_JNI_REAL

JNIEXPORT jlong JNICALL
Java_com_longhun_android_service_LonghunServiceImpl_nativeInit(
    JNIEnv* env, jobject thiz) {
    return 1;  // 句柄
}

JNIEXPORT jstring JNICALL
Java_com_longhun_android_service_LonghunServiceImpl_nativeRunSupervision(
    JNIEnv* env, jobject thiz, jlong handle, jstring config_json) {
    const char* config = (*env)->GetStringUTFChars(env, config_json, NULL);
    char* result = longhun_run_supervision(config);
    (*env)->ReleaseStringUTFChars(env, config_json, config);
    jstring jresult = (*env)->NewStringUTF(env, result);
    longhun_free_string(result);
    return jresult;
}

JNIEXPORT jstring JNICALL
Java_com_longhun_android_service_LonghunServiceImpl_nativeQueryMemory(
    JNIEnv* env, jobject thiz, jlong handle, jstring query_json) {
    const char* query = (*env)->GetStringUTFChars(env, query_json, NULL);
    char* result = longhun_query_memory(query);
    (*env)->ReleaseStringUTFChars(env, query_json, query);
    jstring jresult = (*env)->NewStringUTF(env, result);
    longhun_free_string(result);
    return jresult;
}

JNIEXPORT jstring JNICALL
Java_com_longhun_android_service_LonghunServiceImpl_nativeGetHealth(
    JNIEnv* env, jobject thiz, jlong handle) {
    char* result = longhun_get_health();
    jstring jresult = (*env)->NewStringUTF(env, result);
    longhun_free_string(result);
    return jresult;
}

JNIEXPORT void JNICALL
Java_com_longhun_android_service_LonghunServiceImpl_nativeDispose(
    JNIEnv* env, jobject thiz, jlong handle) {
    // 释放 Rust 运行时资源
}

#else

// ── IDE 静态分析桩（无 jni.h 时） ──
JNIEXPORT jlong JNICALL
Java_com_longhun_android_service_LonghunServiceImpl_nativeInit(
    JNIEnv* env, jobject thiz) {
    return 1;
}

JNIEXPORT jstring JNICALL
Java_com_longhun_android_service_LonghunServiceImpl_nativeRunSupervision(
    JNIEnv* env, jobject thiz, jlong handle, jstring config_json) {
    return NULL;
}

JNIEXPORT jstring JNICALL
Java_com_longhun_android_service_LonghunServiceImpl_nativeQueryMemory(
    JNIEnv* env, jobject thiz, jlong handle, jstring query_json) {
    return NULL;
}

JNIEXPORT jstring JNICALL
Java_com_longhun_android_service_LonghunServiceImpl_nativeGetHealth(
    JNIEnv* env, jobject thiz, jlong handle) {
    return NULL;
}

JNIEXPORT void JNICALL
Java_com_longhun_android_service_LonghunServiceImpl_nativeDispose(
    JNIEnv* env, jobject thiz, jlong handle) {
    // no-op stub
}

#endif
