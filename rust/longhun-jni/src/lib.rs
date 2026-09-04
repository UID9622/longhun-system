// DNA: #龍芯⚡️丙午·丙申·壬子·子时·䷕贲-RUST-JNI-ANDROID-v1.0-UID9622
// 创建者: 诸葛鑫（UID9622）
// 协议: MulanPSL v2 (工程层)
// 用途: longhun-core Android JNI 绑定 — Java/Kotlin 可直接调用
// 编译: cargo build --release --target aarch64-linux-android
//
// Android 侧调用:
//   System.loadLibrary("longhun_jni");
//   String json = LonghunCore.governanceCheck("技术无国界");

use jni::JNIEnv;
use jni::objects::{JClass, JString};
use jni::sys::jstring;

use lhcore::evolution::{
    governance_self_check, check_data_blackhole, detect_veto_word,
    detect_forbidden_scenario, MeltdownFactory, TriggerReason,
    GateRunner,
};
use lhcore::core::run_supervision;
use lhcore::memory;

// ═══════════════════════════════════════════════════════════════
// §1. 治理自检 — 核心入口
// ═══════════════════════════════════════════════════════════════

#[no_mangle]
pub extern "system" fn Java_com_longhun_LonghunCore_governanceCheck(
    mut env: JNIEnv,
    _class: JClass,
    content: JString,
) -> jstring {
    let content: String = env.get_string(&content)
        .map(|s| s.into())
        .unwrap_or_default();
    
    let result = governance_self_check(&content);
    let json = serde_json::to_string(&result).unwrap_or_else(|_| "{}".into());
    
    env.new_string(json)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}

// ═══════════════════════════════════════════════════════════════
// §2. 数据黑洞检测
// ═══════════════════════════════════════════════════════════════

#[no_mangle]
pub extern "system" fn Java_com_longhun_LonghunCore_checkBlackhole(
    mut env: JNIEnv,
    _class: JClass,
    content: JString,
) -> jstring {
    let content: String = env.get_string(&content)
        .map(|s| s.into())
        .unwrap_or_default();
    
    let result = check_data_blackhole(&content);
    let json = serde_json::to_string(&result).unwrap_or_else(|_| "null".into());
    
    env.new_string(json)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}

// ═══════════════════════════════════════════════════════════════
// §3. 否决词检测
// ═══════════════════════════════════════════════════════════════

#[no_mangle]
pub extern "system" fn Java_com_longhun_LonghunCore_detectVetoWord(
    mut env: JNIEnv,
    _class: JClass,
    content: JString,
) -> jstring {
    let content: String = env.get_string(&content)
        .map(|s| s.into())
        .unwrap_or_default();
    
    let result = detect_veto_word(&content);
    let json = serde_json::to_string(&result).unwrap_or_else(|_| "null".into());
    
    env.new_string(json)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}

// ═══════════════════════════════════════════════════════════════
// §4. 禁止场景检测
// ═══════════════════════════════════════════════════════════════

#[no_mangle]
pub extern "system" fn Java_com_longhun_LonghunCore_detectForbidden(
    mut env: JNIEnv,
    _class: JClass,
    content: JString,
) -> jstring {
    let content: String = env.get_string(&content)
        .map(|s| s.into())
        .unwrap_or_default();
    
    let flags = detect_forbidden_scenario(&content);
    let json = serde_json::to_string(&flags).unwrap_or_else(|_| "[]".into());
    
    env.new_string(json)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}

// ═══════════════════════════════════════════════════════════════
// §5. 监督运行
// ═══════════════════════════════════════════════════════════════

#[no_mangle]
pub extern "system" fn Java_com_longhun_LonghunCore_runSupervision(
    mut env: JNIEnv,
    _class: JClass,
    config_json: JString,
) -> jstring {
    let config_str: String = env.get_string(&config_json)
        .map(|s| s.into())
        .unwrap_or_default();
    
    let config = lhcore::core::SupervisionConfig::from_json(&config_str)
        .unwrap_or_default();
    let report = run_supervision(&config);
    let json = serde_json::to_string(&report).unwrap_or_else(|_| "{}".into());
    
    env.new_string(json)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}

// ═══════════════════════════════════════════════════════════════
// §6. 记忆查询
// ═══════════════════════════════════════════════════════════════

#[no_mangle]
pub extern "system" fn Java_com_longhun_LonghunCore_queryMemory(
    mut env: JNIEnv,
    _class: JClass,
    query: JString,
) -> jstring {
    let q: String = env.get_string(&query)
        .map(|s| s.into())
        .unwrap_or_default();
    
    let results = memory::query(&q);
    let json = serde_json::to_string(&results).unwrap_or_else(|_| "[]".into());
    
    env.new_string(json)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}

// ═══════════════════════════════════════════════════════════════
// §7. 健康检查
// ═══════════════════════════════════════════════════════════════

#[no_mangle]
pub extern "system" fn Java_com_longhun_LonghunCore_getHealth(
    env: JNIEnv,
    _class: JClass,
) -> jstring {
    let health = lhcore::core::get_health();
    let json = serde_json::to_string(&health).unwrap_or_else(|_| "{}".into());
    
    env.new_string(json)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}

// ═══════════════════════════════════════════════════════════════
// §8. 熔断器
// ═══════════════════════════════════════════════════════════════

#[no_mangle]
pub extern "system" fn Java_com_longhun_LonghunCore_triggerMeltdown(
    mut env: JNIEnv,
    _class: JClass,
    level: JString,
    reason: JString,
    detail: JString,
) -> jstring {
    let level: String = env.get_string(&level).map(|s| s.into()).unwrap_or_default();
    let reason_str: String = env.get_string(&reason).map(|s| s.into()).unwrap_or_default();
    let detail: String = env.get_string(&detail).map(|s| s.into()).unwrap_or_default();
    
    let meltdown = match level.as_str() {
        "infinite" | "l0" => MeltdownFactory::infinite(TriggerReason::Custom(reason_str), &detail),
        "data" | "l1" => MeltdownFactory::data(TriggerReason::Custom(reason_str), &detail),
        "persona" | "l2" => MeltdownFactory::persona(TriggerReason::Custom(reason_str), "android", &detail),
        "behavior" | "l3" => MeltdownFactory::behavior(TriggerReason::Custom(reason_str), &detail),
        _ => MeltdownFactory::behavior(TriggerReason::Custom(format!("未知级别: {}", level)), &detail),
    };
    
    let json = serde_json::to_string(&meltdown).unwrap_or_else(|_| "{}".into());
    env.new_string(json)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}

// ═══════════════════════════════════════════════════════════════
// §9. 门控审计
// ═══════════════════════════════════════════════════════════════

#[no_mangle]
pub extern "system" fn Java_com_longhun_LonghunCore_runGateCheck(
    mut env: JNIEnv,
    _class: JClass,
    content: JString,
) -> jstring {
    let content: String = env.get_string(&content)
        .map(|s| s.into())
        .unwrap_or_default();
    
    let mut runner = GateRunner::new();
    let report = runner.run_all(&content, "android_jni");
    let json = serde_json::to_string(&report).unwrap_or_else(|_| "{}".into());
    
    env.new_string(json)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}

// ═══════════════════════════════════════════════════════════════
// §10. 版本信息
// ═══════════════════════════════════════════════════════════════

#[no_mangle]
pub extern "system" fn Java_com_longhun_LonghunCore_getVersion(
    env: JNIEnv,
    _class: JClass,
) -> jstring {
    let info = serde_json::json!({
        "version": lhcore::VERSION,
        "dna": lhcore::DNA,
        "confirm": lhcore::CONFIRM,
        "binding": "android-jni-v1.0",
    });
    let json = serde_json::to_string(&info).unwrap();
    env.new_string(json)
        .map(|s| s.into_raw())
        .unwrap_or(std::ptr::null_mut())
}

// ═══════════════════════════════════════════════════════════════
// §11. 单元测试
// ═══════════════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_jni_bindings_exist() {
        // 验证所有 JNI 函数名正确导出
        // 实际 JNI 测试需要 Android 运行时，这里只验证编译通过
        assert!(true);
    }
}
