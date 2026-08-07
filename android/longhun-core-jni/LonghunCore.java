// DNA: #龍芯⚡️丙午·丙申·壬子·子时·䷕贲-ANDROID-JAVA-WRAPPER-v1.0-UID9622
// 创建者: 诸葛鑫（UID9622）
// 协议: MulanPSL v2 (工程层)
// 用途: Android Java 封装 — 调用 longhun_jni.so
// 用法:
//   LonghunCore lh = new LonghunCore();
//   String result = lh.governanceCheck("测试内容");
//   JSONObject r = new JSONObject(result);
//   String auditMark = r.getString("audit_mark");

package com.longhun;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * 龍魂核心引擎 Android JNI 封装
 * 
 * 使用前需 System.loadLibrary("longhun_jni")
 */
public class LonghunCore {
    
    static {
        System.loadLibrary("longhun_jni");
    }
    
    // ── Native 方法声明 ──
    
    /** 治理自检 — 最常用入口 */
    public native String governanceCheck(String content);
    
    /** 数据黑洞检测 */
    public native String checkBlackhole(String content);
    
    /** 否决词检测 */
    public native String detectVetoWord(String content);
    
    /** 禁止场景检测 */
    public native String detectForbidden(String content);
    
    /** 运行监督 */
    public native String runSupervision(String configJson);
    
    /** 记忆查询 */
    public native String queryMemory(String query);
    
    /** 触发熔断 */
    public native String triggerMeltdown(String level, String reason, String detail);
    
    /** 健康检查 */
    public native String getHealth();
    
    /** 门控审计 */
    public native String runGateCheck(String content);
    
    /** 版本信息 */
    public native String getVersion();
    
    // ── 便捷封装方法 ──
    
    /**
     * 快速治理自检，返回 audit_mark (🟢/🟡/🔴)
     */
    public String quickAudit(String content) {
        try {
            String json = governanceCheck(content);
            JSONObject obj = new JSONObject(json);
            return obj.getString("audit_mark");
        } catch (Exception e) {
            return "🔴"; // 出错即红线
        }
    }
    
    /**
     * 检查内容是否安全（无否决词、无数据黑洞）
     */
    public boolean isSafe(String content) {
        try {
            String json = governanceCheck(content);
            JSONObject obj = new JSONObject(json);
            return obj.getBoolean("veto_clean") && obj.getBoolean("gate_clean");
        } catch (Exception e) {
            return false;
        }
    }
    
    /**
     * 快速否决词检测
     */
    public String detectVetoQuick(String content) {
        try {
            String json = detectVetoWord(content);
            if (json == null || json.equals("null")) return null;
            JSONArray arr = new JSONArray(json);
            return arr.length() > 0 ? arr.getString(0) : null;
        } catch (Exception e) {
            return null;
        }
    }
}
