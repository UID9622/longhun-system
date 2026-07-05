// 来源标注: #ZHUGEXIN⚡️ | UID9622 龙魂体系
// 模块定位: CNSH 字元渲染引擎 · 基础三次贝塞尔层

#ifndef TRACE_CONFIG_H
#define TRACE_CONFIG_H

#include <string>
#include <map>
#include <vector>

namespace LongHun::TraceCore {
    // ============================================================
    // 系统常量
    // ============================================================
    constexpr const char* DNA_PREFIX      = "#龍芯⚡️";
    constexpr const char* UID             = "9622";
    constexpr const char* VERSION         = "1.1";
    constexpr const char* GPG_FINGERPRINT =
        "A2D0092CEE2E5BA87035600924C3704A8CC26D5F";

    constexpr const char* TRACE_FILE      = ".star-memory/用户痕迹日志.jsonl";
    constexpr const char* AUDIT_FILE      = ".star-memory/audit.log";

    // ============================================================
    // 操作类型枚举
    // ============================================================
    enum class OperationType {
        登录     = 0,
        退出     = 1,
        注册     = 2,
        查看     = 3,
        支付     = 4,
        提交     = 5,
        修改     = 6,
        删除     = 7,
        下载     = 8,
        上传     = 9,
        其他     = 10
    };

    // ============================================================
    // 审计颜色枚举
    // ============================================================
    enum class AuditColor {
        GREEN  = 0,
        YELLOW = 1,
        RED    = 2
    };

    // ============================================================
    // 操作类型映射
    // ============================================================
    inline const std::map<OperationType, std::string> OperationTypeMap = {
        {OperationType::登录,   "LOGIN"},
        {OperationType::退出,   "LOGOUT"},
        {OperationType::注册,   "REGISTER"},
        {OperationType::查看,   "VIEW"},
        {OperationType::支付,   "PAY"},
        {OperationType::提交,   "SUBMIT"},
        {OperationType::修改,   "EDIT"},
        {OperationType::删除,   "DELETE"},
        {OperationType::下载,   "DOWNLOAD"},
        {OperationType::上传,   "UPLOAD"},
        {OperationType::其他,   "OTHER"}
    };

    inline const std::map<OperationType, const char*> OperationTypeCN = {
        {OperationType::登录,   "登录"},
        {OperationType::退出,   "退出"},
        {OperationType::注册,   "注册"},
        {OperationType::查看,   "查看"},
        {OperationType::支付,   "支付"},
        {OperationType::提交,   "提交"},
        {OperationType::修改,   "修改"},
        {OperationType::删除,   "删除"},
        {OperationType::下载,   "下载"},
        {OperationType::上传,   "上传"},
        {OperationType::其他,   "其他"}
    };

} // namespace LongHun::TraceCore

#endif // TRACE_CONFIG_H
