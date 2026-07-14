// 来源标注: #ZHUGEXIN⚡️ | UID9622 龙魂体系
// 模块定位: CNSH 字元渲染引擎 · 基础三次贝塞尔层

#ifndef TRACE_UTILS_H
#define TRACE_UTILS_H

#include <string>
#include <sstream>
#include <iomanip>
#include <chrono>
#include <openssl/sha.h>

namespace LongHun::TraceCore {

    // ============================================================
    // 当前日期 (YYYY-MM-DD)
    // ============================================================
    inline std::string getCurrentDate() {
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        std::tm* tm = std::localtime(&time);

        std::ostringstream oss;
        oss << std::setfill('0')
            << std::setw(4) << (tm->tm_year + 1900) << "-"
            << std::setw(2) << (tm->tm_mon + 1) << "-"
            << std::setw(2) << tm->tm_mday;
        return oss.str();
    }

    // ============================================================
    // 当前时间戳 (ISO 8601)
    // ============================================================
    inline std::string getCurrentTimestamp() {
        auto now = std::chrono::system_clock::now();
        auto time = std::chrono::system_clock::to_time_t(now);
        std::tm* tm = std::localtime(&time);

        std::ostringstream oss;
        oss << std::setfill('0')
            << std::setw(4) << (tm->tm_year + 1900) << "-"
            << std::setw(2) << (tm->tm_mon + 1) << "-"
            << std::setw(2) << tm->tm_mday << "T"
            << std::setw(2) << tm->tm_hour << ":"
            << std::setw(2) << tm->tm_min << ":"
            << std::setw(2) << tm->tm_sec;
        return oss.str();
    }

    // ============================================================
    // SHA-256 哈希计算
    // ============================================================
    inline std::string sha256(const std::string& input) {
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256(
            reinterpret_cast<const unsigned char*>(input.c_str()),
            input.size(),
            hash
        );

        std::ostringstream oss;
        for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
            oss << std::hex << std::setw(2) << std::setfill('0')
                << static_cast<int>(hash[i]);
        }
        return oss.str();
    }

    // ============================================================
    // 生成防篡改哈希
    // ============================================================
    inline std::string generateHash(
        const std::string& userId,
        const std::string& operation,
        const std::string& content,
        const std::string& timestamp
    ) {
        std::string combined = userId + "|" + operation + "|" + content + "|" + timestamp;
        return sha256(combined);
    }

    // ============================================================
    // 生成 DNA 追溯码
    // ============================================================
    inline std::string generateDNA(
        const std::string& userId,
        const std::string& operationEn,
        const std::string& hashValue
    ) {
        std::string hashShort = hashValue.substr(0, 8);
        for (char& c : hashShort) {
            c = static_cast<char>(std::toupper(c));
        }

        return std::string(DNA_PREFIX)
             + getCurrentDate()  + "-"
             + operationEn       + "-"
             + userId            + "-"
             + hashShort;
    }

    // ============================================================
    // 操作类型转英文
    // ============================================================
    inline std::string operationToString(OperationType op) {
        auto it = OperationTypeMap.find(op);
        if (it != OperationTypeMap.end()) {
            return it->second;
        }
        return "UNKNOWN";
    }

    // ============================================================
    // 操作类型转中文
    // ============================================================
    inline std::string operationToChinese(OperationType op) {
        auto it = OperationTypeCN.find(op);
        if (it != OperationTypeCN.end()) {
            return it->second;
        }
        return "未知";
    }

} // namespace LongHun::TraceCore

#endif // TRACE_UTILS_H
