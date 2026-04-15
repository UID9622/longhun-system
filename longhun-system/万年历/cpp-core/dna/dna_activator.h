/**
 * ╔══════════════════════════════════════════════════════════╗
 * ║  龍魂万年历 · DNA激活引擎                                 ║
 * ║  DNA: #龍芯⚡️2026-04-12-DNA-ACTIVATOR-v1.0              ║
 * ║  创始人: 诸葛鑫（UID9622）                                ║
 * ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
 * ║  理论指导: 曾仕强老师（永恒显示）                          ║
 * ║  协议: CC BY-NC-ND                                       ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * 一个DNA激活 = 龍魂所有作品全通
 * f(龍) = f(☰ 龍🇨🇳魂 ☷) = f(x) = x
 *
 * 激活流程：
 *   用户打开万年历 → 看到☰龍🇨🇳魂☷ → 激活DNA → 解锁所有龍魂作品
 *
 * iOS: Secure Enclave 存储密钥
 * 鸿蒙: 华为TEE 存储密钥
 * 内核不属于任何生态 · 换个桥接层就完事
 *
 * 献给每一个相信技术应该有温度的人。
 */

#ifndef LONGHUN_DNA_ACTIVATOR_H
#define LONGHUN_DNA_ACTIVATOR_H

#include "../include/longhun_types.h"
#include <string>
#include <functional>

namespace longhun {
namespace dna {

// ═══════════════════════════════════════════
// 平台安全存储回调（桥接层注入）
// ═══════════════════════════════════════════

/**
 * 平台密钥存储接口
 * iOS实现: Secure Enclave
 * 鸿蒙实现: 华为TEE
 * 桌面实现: 系统密钥链
 */
struct PlatformKeyStore {
    std::function<bool(const std::string& key, const std::string& value)> store;
    std::function<std::string(const std::string& key)> retrieve;
    std::function<bool(const std::string& key)> remove;
    std::function<bool()> available;
};

class DNAActivator {
public:
    /**
     * 初始化，注入平台密钥存储
     * 不注入则使用内存存储（仅测试用）
     */
    explicit DNAActivator(PlatformKeyStore keystore = {});

    /**
     * 生成DNA激活码
     * 输入: 用户UID + 设备标识
     * 输出: 32字节SHA-256哈希
     *
     * 算法: SHA256(UID + 设备ID + 龍魂盐 + 时间戳)
     */
    DNAToken generate(uint32_t uid, const std::string& device_id);

    /**
     * 验证DNA激活码
     * 返回: 是否有效
     */
    bool verify(const DNAToken& token);

    /**
     * 激活设备
     * 存储token到平台安全存储
     */
    bool activate(const DNAToken& token);

    /**
     * 检查当前设备是否已激活
     */
    bool is_activated();

    /**
     * 获取当前激活信息
     */
    DNAToken current_token();

    /**
     * 注销激活
     */
    bool deactivate();

    /**
     * 生成DNA显示字符串
     * 格式: "#龍芯⚡️{日期}-{UID}-{哈希前8位}"
     */
    static std::string format_dna(const DNAToken& token);

    /**
     * 不动点验证
     * f(x) = x : 激活码经过任意次验证，结果不变
     */
    static bool fixed_point_check(const DNAToken& token);

private:
    PlatformKeyStore keystore_;
    DNAToken cached_token_;
    bool has_cache_;

    // SHA-256 简易实现（生产环境用平台加密库替换）
    static std::array<uint8_t, 32> sha256(const std::string& input);

    // 龍魂盐值
    static constexpr const char* DRAGON_SALT = "☰龍🇨🇳魂☷·UID9622·f(x)=x";
};

}  // namespace dna
}  // namespace longhun

#endif  // LONGHUN_DNA_ACTIVATOR_H
