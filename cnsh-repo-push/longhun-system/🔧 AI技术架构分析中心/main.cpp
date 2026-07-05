// 来源标注: #ZHUGEXIN⚡️ | UID9622 龙魂体系
// 模块定位: CNSH 字元渲染引擎 · 基础三次贝塞尔层

#include <iostream>
#include "trace_engine.h"

using namespace LongHun::TraceCore;

// ============================================================
// 主函数
// ============================================================
int main() {
    std::cout << "🔵 龙魂留痕系统 v1.1 启动中...\n\n";

    TraceEngine engine;

    // 熔断检查
    std::string fuseMsg;
    if (!engine.fuseCheck(fuseMsg)) {
        std::cout << "  " << fuseMsg << "\n";
        return 1;
    }
    std::cout << "  " << fuseMsg << "\n\n";

    // 记录用户操作
    std::cout << "📝 记录用户操作...\n";

    engine.record("UID9622", OperationType::登录,
                  "设备=iPhone15 | IP=192.168.1.1");

    engine.record("UID9622", OperationType::查看,
                  "页面=星辰记忆主页");

    engine.record("UID9622", OperationType::支付,
                  "金额=10元 | 档位=认可支持档");

    engine.record("UID9622", OperationType::提交,
                  "内容=星辰记忆v1.0文档");

    engine.record("UID0001", OperationType::登录,
                  "设备=Android | IP=10.0.0.2");

    engine.record("UID0001", OperationType::查看,
                  "页面=透明资本");

    std::cout << "  ✅ 已记录 6 条操作\n\n";

    // 批量验证
    std::cout << "🔍 批量验证...\n";
    auto report = engine.batchVerify();
    std::cout << "  总记录数: " << report.totalRecords << "\n";
    std::cout << "  有效记录: " << report.validRecords << "\n";
    std::cout << "  无效记录: " << report.invalidRecords << "\n\n";

    // 查询记录
    std::cout << "📊 查询 UID9622 的记录...\n";
    auto records = engine.query("UID9622", "", "", 1, 10);

    for (const auto& r : records) {
        std::cout << "  " << r.timestamp.substr(0, 19)
                  << " | " << r.operation << "\n";
    }

    std::cout << "\n✅ 系统运行完成\n";

    return 0;
}
