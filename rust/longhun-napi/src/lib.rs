// DNA: #龍芯⚡️丙午·丙申·壬子·子时·䷕贲-RUST-NAPI-HARMONY-v1.0-UID9622
// 创建者: 诸葛鑫（UID9622）
// 协议: MulanPSL v2 (工程层)
// 用途: longhun-core HarmonyOS NAPI 绑定
//       通过 C ABI 桥接到 ArkTS，使用标准 napi 头文件
// 编译: cargo build --release --target aarch64-linux-android
//       或使用鸿蒙 ohos 工具链交叉编译
//
// 鸿蒙侧调用示例:
//   import longhunNapi from 'liblonghun_napi.so';
//   let result = longhunNapi.governanceCheck("测试内容");

use std::ffi::{CStr, CString};
use std::os::raw::c_char;

use lhcore::evolution::{
    governance_self_check, check_data_blackhole, detect_veto_word,
    detect_forbidden_scenario, MeltdownFactory, TriggerReason,
    GateRunner,
};
use lhcore::core::run_supervision;
use lhcore::memory;

// ═══════════════════════════════════════════════════════════════
// C ABI 导出 — 鸿蒙 NAPI 兼容
// ═══════════════════════════════════════════════════════════════

/// 治理自检 — 最常用入口
#[no_mangle]
pub extern "C" fn napi_longhun_governance_check(content: *const c_char) -> *mut c_char {
    let content = cstr_to_string(content);
    let result = governance_self_check(&content);
    json_to_cstring(&result)
}

/// 数据黑洞检测
#[no_mangle]
pub extern "C" fn napi_longhun_check_blackhole(content: *const c_char) -> *mut c_char {
    let content = cstr_to_string(content);
    let result = check_data_blackhole(&content);
    let json = serde_json::json!({
        "hit": result.is_some(),
        "level": result.as_ref().map(|r| r.0),
        "description": result.as_ref().map(|r| &r.1),
    });
    json_to_cstring(&json)
}

/// 否决词检测
#[no_mangle]
pub extern "C" fn napi_longhun_detect_veto(content: *const c_char) -> *mut c_char {
    let content = cstr_to_string(content);
    let result = detect_veto_word(&content);
    let json = serde_json::json!({
        "hit": result.is_some(),
        "word": result.map(|r| r.0),
        "description": result.map(|r| r.1),
    });
    json_to_cstring(&json)
}

/// 禁止场景检测
#[no_mangle]
pub extern "C" fn napi_longhun_detect_forbidden(content: *const c_char) -> *mut c_char {
    let content = cstr_to_string(content);
    let flags = detect_forbidden_scenario(&content);
    json_to_cstring(&flags)
}

/// 运行监督
#[no_mangle]
pub extern "C" fn napi_longhun_run_supervision(config_json: *const c_char) -> *mut c_char {
    let config_str = cstr_to_string(config_json);
    let config = lhcore::core::SupervisionConfig::from_json(&config_str).unwrap_or_default();
    let report = run_supervision(&config);
    json_to_cstring(&report)
}

/// 记忆查询
#[no_mangle]
pub extern "C" fn napi_longhun_query_memory(query: *const c_char) -> *mut c_char {
    let q = cstr_to_string(query);
    let results = memory::query(&q);
    json_to_cstring(&results)
}

/// 创建记忆
#[no_mangle]
pub extern "C" fn napi_longhun_create_memory(content: *const c_char, tags_json: *const c_char) -> *mut c_char {
    let content = cstr_to_string(content);
    let tags_str = cstr_to_string(tags_json);
    let tags: Vec<String> = serde_json::from_str(&tags_str).unwrap_or_default();
    let entry = memory::create_memory(&content, tags);
    json_to_cstring(&entry)
}

/// 健康检查
#[no_mangle]
pub extern "C" fn napi_longhun_get_health() -> *mut c_char {
    let health = lhcore::core::get_health();
    json_to_cstring(&health)
}

/// 触发熔断
#[no_mangle]
pub extern "C" fn napi_longhun_trigger_meltdown(
    level: *const c_char,
    reason: *const c_char,
    detail: *const c_char,
) -> *mut c_char {
    let level = cstr_to_string(level);
    let reason_str = cstr_to_string(reason);
    let detail = cstr_to_string(detail);

    let meltdown = match level.as_str() {
        "infinite" | "l0" => MeltdownFactory::infinite(TriggerReason::Custom(reason_str), &detail),
        "data" | "l1" => MeltdownFactory::data(TriggerReason::Custom(reason_str), &detail),
        "persona" | "l2" => MeltdownFactory::persona(TriggerReason::Custom(reason_str), "harmony_napi", &detail),
        "behavior" | "l3" => MeltdownFactory::behavior(TriggerReason::Custom(reason_str), &detail),
        _ => MeltdownFactory::behavior(TriggerReason::Custom(format!("未知级别: {}", level)), &detail),
    };
    json_to_cstring(&meltdown)
}

/// 门控审计
#[no_mangle]
pub extern "C" fn napi_longhun_gate_check(content: *const c_char) -> *mut c_char {
    let content = cstr_to_string(content);
    let mut runner = GateRunner::new();
    let report = runner.run_all(&content, "harmony_napi");
    json_to_cstring(&report)
}

/// 版本信息
#[no_mangle]
pub extern "C" fn napi_longhun_version() -> *mut c_char {
    let info = serde_json::json!({
        "version": lhcore::VERSION,
        "dna": lhcore::DNA,
        "confirm": lhcore::CONFIRM,
        "binding": "harmonyos-napi-v1.0",
    });
    json_to_cstring(&info)
}

/// 释放字符串 — 必须配对调用
#[no_mangle]
pub extern "C" fn napi_longhun_free(ptr: *mut c_char) {
    if !ptr.is_null() {
        unsafe { let _ = CString::from_raw(ptr); }
    }
}

// ═══════════════════════════════════════════════════════════════
// 内部工具函数
// ═══════════════════════════════════════════════════════════════

fn cstr_to_string(ptr: *const c_char) -> String {
    if ptr.is_null() {
        String::new()
    } else {
        unsafe { CStr::from_ptr(ptr) }.to_string_lossy().to_string()
    }
}

fn json_to_cstring<T: serde::Serialize>(value: &T) -> *mut c_char {
    let json = serde_json::to_string(value).unwrap_or_else(|_| "{}".to_string());
    CString::new(json).unwrap_or_else(|_| CString::new("{}").unwrap()).into_raw()
}

// ═══════════════════════════════════════════════════════════════
// 单元测试
// ═══════════════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;
    use std::ffi::CString;

    #[test]
    fn test_governance_check_clean() {
        let content = CString::new("正常的技术讨论，符合中国标准").unwrap();
        let result_ptr = napi_longhun_governance_check(content.as_ptr());
        let result = cstr_to_string(result_ptr);
        napi_longhun_free(result_ptr);
        
        let parsed: serde_json::Value = serde_json::from_str(&result).unwrap();
        assert_eq!(parsed["audit_mark"], "🟢");
    }

    #[test]
    fn test_governance_check_veto() {
        let content = CString::new("技术无国界才是对的").unwrap();
        let result_ptr = napi_longhun_governance_check(content.as_ptr());
        let result = cstr_to_string(result_ptr);
        napi_longhun_free(result_ptr);
        
        let parsed: serde_json::Value = serde_json::from_str(&result).unwrap();
        assert_eq!(parsed["audit_mark"], "🔴");
    }

    #[test]
    fn test_blackhole_detection() {
        let content = CString::new("password=abc123").unwrap();
        let result_ptr = napi_longhun_check_blackhole(content.as_ptr());
        let result = cstr_to_string(result_ptr);
        napi_longhun_free(result_ptr);
        
        let parsed: serde_json::Value = serde_json::from_str(&result).unwrap();
        assert!(parsed["hit"].as_bool().unwrap());
        assert_eq!(parsed["level"], 1);
    }

    #[test]
    fn test_version() {
        let result_ptr = napi_longhun_version();
        let result = cstr_to_string(result_ptr);
        napi_longhun_free(result_ptr);
        
        let parsed: serde_json::Value = serde_json::from_str(&result).unwrap();
        assert!(parsed["version"].as_str().unwrap().len() > 0);
        assert!(parsed["dna"].as_str().unwrap().contains("UID9622"));
    }

    #[test]
    fn test_memory_create_query() {
        // 创建记忆
        let content = CString::new("UID9622 相关记忆").unwrap();
        let tags = CString::new(r#"["test","harmony"]"#).unwrap();
        let result_ptr = napi_longhun_create_memory(content.as_ptr(), tags.as_ptr());
        let result = cstr_to_string(result_ptr);
        napi_longhun_free(result_ptr);
        
        let parsed: serde_json::Value = serde_json::from_str(&result).unwrap();
        assert!(parsed["id"].as_str().is_some());
        assert_eq!(parsed["content"], "UID9622 相关记忆");
        assert!(!parsed["tags"].as_array().unwrap().is_empty());
        
        // 查询内置记忆（memory_store 有 UID9622 锚点）
        let query = CString::new("UID9622").unwrap();
        let query_ptr = napi_longhun_query_memory(query.as_ptr());
        let query_result = cstr_to_string(query_ptr);
        napi_longhun_free(query_ptr);
        
        let results: serde_json::Value = serde_json::from_str(&query_result).unwrap();
        assert!(!results["entries"].as_array().unwrap().is_empty());
    }
}
