// 来源标注: #ZHUGEXIN⚡️ | UID9622 龙魂体系
// 模块定位: CNSH 字元渲染引擎 · 基础三次贝塞尔层

#ifndef TRACE_RECORD_H
#define TRACE_RECORD_H

#include <string>
#include <map>
#include <sstream>
#include "trace_config.h"

namespace LongHun::TraceCore {

    // ============================================================
    // 痕迹记录结构
    // ============================================================
    struct TraceRecord {
        std::string userId;
        std::string operation;
        std::string operationEn;
        std::string content;
        std::string timestamp;
        std::string hashValue;
        std::string dnaTrace;
        std::string version;
        std::string gpgFingerprint;
        std::map<std::string, std::string> extra;
        AuditColor  auditColor;
        std::string remark;

        // ============================================================
        // 转换为 JSON 字符串
        // ============================================================
        std::string toJson() const {
            std::ostringstream oss;
            oss << "{";

            oss << "\"用户ID\": \"" << userId << "\", ";
            oss << "\"操作类型\": \"" << operation << "\", ";
            oss << "\"操作内容\": \"" << content << "\", ";
            oss << "\"时间戳\": \"" << timestamp << "\", ";
            oss << "\"哈希验证\": \"" << hashValue << "\", ";
            oss << "\"DNA追溯\": \"" << dnaTrace << "\", ";
            oss << "\"版本\": \"" << version << "\", ";
            oss << "\"GPG指纹\": \"" << gpgFingerprint << "\", ";

            // 附加信息
            if (!extra.empty()) {
                oss << "\"附加信息\": {";
                bool first = true;
                for (const auto& [key, value] : extra) {
                    if (!first) oss << ", ";
                    oss << "\"" << key << "\": \"" << value << "\"";
                    first = false;
                }
                oss << "}, ";
            } else {
                oss << "\"附加信息\": {}, ";
            }

            // 三色状态
            std::string colorEmoji;
            switch (auditColor) {
                case AuditColor::GREEN:  colorEmoji = "🟢"; break;
                case AuditColor::YELLOW: colorEmoji = "🟡"; break;
                case AuditColor::RED:    colorEmoji = "🔴"; break;
            }
            oss << "\"三色状态\": \"" << colorEmoji << "\", ";
            oss << "\"备注\": \"" << remark << "\"";

            oss << "}";
            return oss.str();
        }

        // ============================================================
        // 转换为审计日志行
        // ============================================================
        std::string toAuditLine() const {
            std::string contentPreview = content;
            if (contentPreview.length() > 40) {
                contentPreview = contentPreview.substr(0, 40) + "...";
            }

            return timestamp + " | " + operation + " | "
                 + userId + " | " + contentPreview + " | "
                 + hashValue.substr(0, 16);
        }
    };

} // namespace LongHun::TraceCore

#endif // TRACE_RECORD_H
