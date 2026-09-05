// DNA: #龍芯⚡️2026-09-05-CNSH-BRIDGE-NAPI-v0.1-UID9622
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 用途: 鸿蒙 N-API(C API) 桥接层 —— 把 CNSH 逻辑（cnsh_logic.c，cnsh_cgen.py 生成）
//       导出为 ArkTS 可调用的原生方法。需 DevEco/HarmonyOS NDK 实机构建（本机无法编译）。
// 关键点: unity build —— #include "cnsh_logic.c" 使 CNSH 的 static 函数在同一编译单元可见。

#include "napi/native_api.h"
#include <string.h>

// ── CNSH 逻辑同源引入（cnsh_cgen.py --no-main 生成，含 CNSH_DNA / CNSH_GPG 常量）──
#include "cnsh_logic.c"

// ── ArkTS → 问候(名字: 字符串) -> 字符串 ──
static napi_value Bridge_问候(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    char name[256] = "";
    if (argc >= 1) {
        size_t len = 0;
        napi_get_value_string_utf8(env, args[0], name, sizeof(name), &len);
    }
    // 调用 CNSH 翻译产物（同一编译单元内 static 可见）
    const char *out = cnsh_问候(name);
    napi_value ret = nullptr;
    napi_create_string_utf8(env, out, NAPI_AUTO_LENGTH, &ret);
    return ret;
}

// ── ArkTS → 三色审计(输入: 字符串) -> 字符串（🔴空输入拒绝 / 🟢通过）──
static napi_value Bridge_三色审计(napi_env env, napi_callback_info info)
{
    size_t argc = 1;
    napi_value args[1] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    char input[512] = "";
    if (argc >= 1) {
        size_t len = 0;
        napi_get_value_string_utf8(env, args[0], input, sizeof(input), &len);
    }
    const char *out = cnsh_三色审计(input);
    napi_value ret = nullptr;
    napi_create_string_utf8(env, out, NAPI_AUTO_LENGTH, &ret);
    return ret;
}

// ── ArkTS → 自检(): DNA/GPG/编译器版本常量（可追溯应用）──
static napi_value Bridge_自检(napi_env env, napi_callback_info info)
{
    napi_value obj = nullptr;
    napi_create_object(env, &obj);
    napi_value v = nullptr;
    napi_create_string_utf8(env, CNSH_DNA, NAPI_AUTO_LENGTH, &v);
    napi_set_named_property(env, obj, "dna", v);
    napi_create_string_utf8(env, CNSH_GPG, NAPI_AUTO_LENGTH, &v);
    napi_set_named_property(env, obj, "gpg", v);
    napi_create_string_utf8(env, "cnsh_cgen.py v0.1", NAPI_AUTO_LENGTH, &v);
    napi_set_named_property(env, obj, "cgen", v);
    return obj;
}

EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports)
{
    napi_property_descriptor desc[] = {
        {"问候", nullptr, Bridge_问候, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"三色审计", nullptr, Bridge_三色审计, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"自检", nullptr, Bridge_自检, nullptr, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
EXTERN_C_END

static napi_module cnshBridgeModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "cnsh_bridge",
    .nm_priv = ((void *)0),
    .reserved = {0},
};

__attribute__((constructor)) static void RegisterCnshBridge(void)
{
    napi_module_register(&cnshBridgeModule);
}
