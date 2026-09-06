// DNA: #龍芯⚡️2026-09-05-CNSH-BRIDGE-NAPI-STUB-v0.1-UID9622
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 用途: 本机（无 DevEco/HarmonyOS NDK）静态检查专用 N-API 形态占位头。
//       仅当编译环境不存在 NDK 真头 `napi/native_api.h` 时，由 cnsh_napi.cpp
//       的 __has_include 分支回退引入；真机构建恒走 NDK 真头，本文件永不参与。
// 对齐: N-API v12 主接口（类型/常量/签名与本桥实际用点对齐，非完整实现）。
#ifndef CNSH_NAPI_STUB_NATIVE_H
#define CNSH_NAPI_STUB_NATIVE_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
#define EXTERN_C_START extern "C" {
#define EXTERN_C_END }
#else
#define EXTERN_C_START
#define EXTERN_C_END
#endif

EXTERN_C_START

typedef struct napi_env__ *napi_env;
typedef struct napi_value__ *napi_value;
typedef struct napi_callback_info__ *napi_callback_info;

typedef enum {
    napi_ok,
    napi_invalid_arg,
    napi_object_expected,
    napi_string_expected,
    napi_name_expected,
    napi_function_expected,
    napi_number_expected,
    napi_boolean_expected,
    napi_array_expected,
    napi_generic_failure,
    napi_pending_exception,
    napi_cancelled,
    napi_escape_called_twice,
    napi_handle_scope_mismatch,
    napi_callback_scope_mismatch,
    napi_queue_full,
    napi_closing,
    napi_bigint_expected,
    napi_date_expected,
    napi_arraybuffer_expected,
    napi_detachable_arraybuffer_expected,
    napi_would_deadlock,
    napi_no_external_buffers_allowed,
    napi_cannot_run_js,
} napi_status;

typedef enum {
    napi_default = 0,
    napi_writable = 1 << 0,
    napi_enumerable = 1 << 1,
    napi_configurable = 1 << 2,
    napi_static = 1 << 10,
    napi_default_method = napi_writable | napi_configurable,
    napi_default_jsproperty = napi_writable | napi_enumerable | napi_configurable,
} napi_property_attributes;

typedef napi_value (*napi_callback)(napi_env env, napi_callback_info info);

typedef struct {
    const char *utf8name;
    napi_value name;
    napi_callback method;
    napi_callback getter;
    napi_callback setter;
    napi_value value;
    napi_property_attributes attributes;
    void *data;
} napi_property_descriptor;

typedef struct {
    uint32_t nm_version;
    uint32_t nm_flags;
    const char *nm_filename;
    napi_value (*nm_register_func)(napi_env env, napi_value exports);
    const char *nm_modname;
    void *nm_priv;
    void *reserved[4];
} napi_module;

#define NAPI_AUTO_LENGTH ((size_t)-1)

napi_status napi_get_cb_info(napi_env env, napi_callback_info cbinfo, size_t *argc, napi_value *argv, napi_value *this_arg, void **data);
napi_status napi_throw_error(napi_env env, const char *code, const char *msg);
napi_status napi_get_value_string_utf8(napi_env env, napi_value value, char *buf, size_t bufsize, size_t *result);
napi_status napi_create_string_utf8(napi_env env, const char *str, size_t length, napi_value *result);
napi_status napi_create_object(napi_env env, napi_value *result);
napi_status napi_set_named_property(napi_env env, napi_value object, const char *utf8name, napi_value value);
napi_status napi_define_properties(napi_env env, napi_value object, size_t property_count, const napi_property_descriptor *properties);
napi_status napi_module_register(napi_module *mod);

EXTERN_C_END

#endif /* CNSH_NAPI_STUB_NATIVE_H */
