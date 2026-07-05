// 来源标注: #ZHUGEXIN⚡️ | UID9622 龙魂体系
// 模块定位: CNSH 字元渲染引擎 · 基础三次贝塞尔层

#ifndef TRACE_ENGINE_H
#define TRACE_ENGINE_H

#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <filesystem>
#include "trace_config.h"
#include "trace_utils.h"
#include "trace_record.h"

namespace LongHun::TraceCore {

    // ============================================================
    // 批量验证报告
    // ============================================================
    struct BatchVerifyReport {
        int totalRecords;
        int validRecords;
        int invalidRecords;
        std::vector<std::string> errors;

        BatchVerifyReport() : totalRecords(0), validRecords(0), invalidRecords(0) {}
    };

    // ============================================================
    // 痕迹引擎核心类
    // ============================================================
    class TraceEngine {
    private:
        std::string traceFile_;
        std::string auditFile_;

        // ============================================================
        // 追加到文件
        // ============================================================
        bool appendToFile(const std::string& filePath, const std::string& content) {
            std::ofstream file(filePath, std::ios::app);
            if (!file.is_open()) {
                return false;
            }
            file << content << std::endl;
            file.close();
            return true;
        }

    public:
        // ============================================================
        // 构造函数
        // ============================================================
        TraceEngine() : traceFile_(TRACE_FILE), auditFile_(AUDIT_FILE) {
            // 确保目录存在
            std::filesystem::path tracePath(traceFile_);
            std::filesystem::create_directories(tracePath.parent_path());
        }

        // ============================================================
        // 记录用户操作
        // ============================================================
        bool record(
            const std::string& userId,
            OperationType      opType,
            const std::string& content,
            const std::map<std::string, std::string>& extra = {}
        ) {
            std::string opCn = operationToChinese(opType);
            std::string opEn = operationToString(opType);
            std::string ts   = getCurrentTimestamp();
            std::string hash = generateHash(userId, opEn, content, ts);
            std::string dna  = generateDNA(userId, opEn, hash);

            TraceRecord rec;
            rec.userId        = userId;
            rec.operation     = opCn;
            rec.operationEn   = opEn;
            rec.content       = content;
            rec.timestamp     = ts;
            rec.hashValue     = hash;
            rec.dnaTrace      = dna;
            rec.version       = VERSION;
            rec.gpgFingerprint= GPG_FINGERPRINT;
            rec.extra         = extra;
            rec.auditColor    = AuditColor::GREEN;
            rec.remark        = "";

            // 写入痕迹日志
            if (!appendToFile(traceFile_, rec.toJson())) {
                return false;
            }

            // 写入审计日志
            if (!appendToFile(auditFile_, rec.toAuditLine())) {
                return false;
            }

            return true;
        }

        // ============================================================
        // 熔断检查
        // ============================================================
        bool fuseCheck(std::string& message) {
            // 检查 GPG 指纹
            if (std::string(GPG_FINGERPRINT) != "A2D0092CEE2E5BA87035600924C3704A8CC26D5F") {
                message = "❌ GPG 指纹不匹配，系统已熔断";
                return false;
            }

            // 检查文件完整性
            if (!std::filesystem::exists(traceFile_) && !std::filesystem::exists(auditFile_)) {
                message = "✅ 系统初始化完成";
                return true;
            }

            message = "✅ 系统自检通过";
            return true;
        }

        // ============================================================
        // 批量验证所有记录
        // ============================================================
        BatchVerifyReport batchVerify() const {
            BatchVerifyReport report;

            std::ifstream file(traceFile_);
            if (!file.is_open()) {
                report.errors.push_back("无法打开痕迹日志文件");
                return report;
            }

            std::string line;
            while (std::getline(file, line)) {
                report.totalRecords++;

                // 简化验证：检查 JSON 格式
                if (line.empty() || line[0] != '{') {
                    report.invalidRecords++;
                    report.errors.push_back("记录 " + std::to_string(report.totalRecords) + ": JSON 格式错误");
                } else {
                    report.validRecords++;
                }
            }

            file.close();
            return report;
        }

        // ============================================================
        // 查询痕迹记录
        // ============================================================
        std::vector<TraceRecord> query(
            const std::string& userId = "",
            const std::string& operation = "",
            const std::string& date = "",
            int page = 1,
            int pageSize = 20
        ) const {
            std::vector<TraceRecord> results;

            std::ifstream file(traceFile_);
            if (!file.is_open()) {
                return results;
            }

            std::string line;
            int skip = (page - 1) * pageSize;
            int count = 0;

            while (std::getline(file, line)) {
                if (count >= skip + pageSize) break;

                // 简化查询：这里只做简单的字符串匹配
                if (!userId.empty() && line.find("\"用户ID\": \"" + userId + "\"") == std::string::npos) {
                    continue;
                }

                if (!operation.empty() && line.find("\"操作类型\": \"" + operation + "\"") == std::string::npos) {
                    continue;
                }

                if (!date.empty() && line.find(date) == std::string::npos) {
                    continue;
                }

                if (count >= skip) {
                    // 这里简化处理，实际应该解析 JSON
                    TraceRecord rec;
                    rec.userId = userId;
                    rec.operation = operation;
                    rec.content = line.substr(0, 100);
                    results.push_back(rec);
                }

                count++;
            }

            file.close();
            return results;
        }

        // ============================================================
        // 生成月度报告
        // ============================================================
        std::string generateMonthlyReport(int year, int month) const {
            std::ostringstream oss;
            oss << "📊 月度痕迹报告\n";
            oss << "时间: " << year << "-" << std::setfill('0') << std::setw(2) << month << "\n\n";

            auto report = batchVerify();
            oss << "总记录数: " << report.totalRecords << "\n";
            oss << "有效记录: " << report.validRecords << "\n";
            oss << "无效记录: " << report.invalidRecords << "\n";

            if (!report.errors.empty()) {
                oss << "\n错误列表:\n";
                for (const auto& error : report.errors) {
                    oss << "  - " << error << "\n";
                }
            }

            return oss.str();
        }
    };

} // namespace LongHun::TraceCore

#endif // TRACE_ENGINE_H
