// 龍魂 · Native 线程池 · 鸿蒙并发核心
// DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-THREAD-POOL-v1.0
// 联动: 生日提醒v2.0 · 情感协议 · 19人格矩阵

#ifndef LONGHUN_THREAD_POOL_H
#define LONGHUN_THREAD_POOL_H

#include <vector>
#include <queue>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <future>
#include <functional>
#include <memory>
#include <atomic>
#include <string>
#include <chrono>
#include <stdexcept>
#include <algorithm>
#include <sched.h>
#include <sys/resource.h>
#include <sys/syscall.h>
#include <unistd.h>
#include <cstring>
#include <ctime>

namespace longhun {

// === DNA 常量 ===
constexpr const char* MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
constexpr const char* MASTER_UID = "9622";
constexpr const char* CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 任务优先级 ===
enum class TaskPriority : uint8_t {
    CRITICAL  = 0,   // 紧急：声纹验证、安全告警、熔断信号
    HIGH      = 1,   // 高：实时预测、UI响应、祝福推送
    NORMAL    = 2,   // 普通：数据压缩、日志归档、批量查询
    LOW       = 3,   // 低：后台同步、模型预热、统计计算
    BACKGROUND = 4   // 后台：索引重建、数据清理、审计校验
};

// === 任务包装 ===
struct Task {
    std::function<void()> func;
    TaskPriority priority;
    uint64_t id;
    uint64_t submit_time;
    std::string dna_tag;     // DNA溯源标记
    std::string task_name;   // 任务名（调试用）

    // 优先级队列比较：数字小优先级高
    bool operator>(const Task& other) const {
        if (priority != other.priority) {
            return priority > other.priority;
        }
        return submit_time > other.submit_time;
    }
};

// === 线程池配置 ===
struct ThreadPoolConfig {
    size_t min_threads       = 4;     // 最小线程数
    size_t max_threads       = 16;    // 最大线程数
    size_t queue_capacity    = 1000;  // 队列容量
    size_t cpu_affinity_mask = 0;     // CPU亲和性掩码 (0=不绑核)
    bool use_huge_pages      = false; // 大页内存
    bool bind_numa_node      = false; // NUMA绑核
    int numa_node_id         = 0;     // NUMA节点ID
    size_t slow_task_threshold_us = 100000; // 慢任务阈值(微秒)
};

// === 线程池统计 ===
struct PoolStats {
    size_t queue_size;
    size_t active_threads;
    size_t idle_threads;
    uint64_t total_processed;
    uint64_t total_submitted;
    uint64_t total_dropped;
    uint64_t slow_tasks;
    uint64_t avg_exec_time_us;
    double cpu_utilization;
};

// ============================================================================
// 龍魂线程池
// ============================================================================
class LongHunThreadPool {
public:
    explicit LongHunThreadPool(const ThreadPoolConfig& config);
    ~LongHunThreadPool();

    // 禁止拷贝
    LongHunThreadPool(const LongHunThreadPool&) = delete;
    LongHunThreadPool& operator=(const LongHunThreadPool&) = delete;

    // === 提交任务（模板） ===
    template<typename F, typename... Args>
    auto submit(TaskPriority priority, const std::string& task_name,
                F&& f, Args&&... args)
        -> std::future<decltype(f(args...))> {

        using ReturnType = decltype(f(args...));

        auto task = std::make_shared<std::packaged_task<ReturnType()>>(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...)
        );

        std::future<ReturnType> result = task->get_future();

        Task wrapper;
        wrapper.func = [task]() { (*task)(); };
        wrapper.priority = priority;
        wrapper.id = next_task_id_.fetch_add(1);
        wrapper.submit_time = get_timestamp_us();
        wrapper.dna_tag = std::string(MASTER_DNA) + "-" + MASTER_UID;
        wrapper.task_name = task_name;

        total_submitted_.fetch_add(1);

        {
            std::unique_lock<std::mutex> lock(queue_mutex_);

            // 队列满时丢弃低优先级任务
            if (task_queue_.size() >= config_.queue_capacity) {
                if (!drop_lowest_priority()) {
                    total_dropped_.fetch_add(1);
                    lock.unlock();
                    task->set_exception(std::make_exception_ptr(
                        std::runtime_error("Task queue full, all tasks critical")
                    ));
                    return result;
                }
            }

            task_queue_.push(std::move(wrapper));
        }

        condition_.notify_one();

        // 动态扩容检查
        check_dynamic_scale();

        return result;
    }

    // 无任务名的提交
    template<typename F, typename... Args>
    auto submit(TaskPriority priority, F&& f, Args&&... args)
        -> std::future<decltype(f(args...))> {
        return submit(priority, "unnamed", std::forward<F>(f), std::forward<Args>(args)...);
    }

    // === 便捷提交 ===
    template<typename F, typename... Args>
    auto submit_critical(const std::string& name, F&& f, Args&&... args) {
        return submit(TaskPriority::CRITICAL, name, std::forward<F>(f), std::forward<Args>(args)...);
    }

    template<typename F, typename... Args>
    auto submit_high(const std::string& name, F&& f, Args&&... args) {
        return submit(TaskPriority::HIGH, name, std::forward<F>(f), std::forward<Args>(args)...);
    }

    template<typename F, typename... Args>
    auto submit_normal(const std::string& name, F&& f, Args&&... args) {
        return submit(TaskPriority::NORMAL, name, std::forward<F>(f), std::forward<Args>(args)...);
    }

    // === 状态查询 ===
    size_t get_queue_size() const;
    size_t get_active_threads() const;
    uint64_t get_total_processed() const;
    uint64_t get_total_submitted() const;
    uint64_t get_total_dropped() const;
    ThreadPoolConfig get_config() const;
    PoolStats get_stats() const;

    // === 动态调整 ===
    void resize(size_t new_min_threads, size_t new_max_threads);
    void set_cpu_affinity(size_t mask);
    void set_slow_task_threshold(size_t threshold_us);

    // === 控制 ===
    void wait_for_all();
    void shutdown();
    bool is_running() const { return !stop_.load(); }

private:
    ThreadPoolConfig config_;
    std::vector<std::thread> workers_;
    std::priority_queue<Task, std::vector<Task>, std::greater<Task>> task_queue_;
    mutable std::mutex queue_mutex_;
    std::condition_variable condition_;
    std::atomic<bool> stop_{false};
    std::atomic<uint64_t> next_task_id_{0};
    std::atomic<uint64_t> total_processed_{0};
    std::atomic<uint64_t> total_submitted_{0};
    std::atomic<uint64_t> total_dropped_{0};
    std::atomic<uint64_t> slow_tasks_{0};
    std::atomic<uint64_t> total_exec_time_us_{0};
    std::atomic<size_t> active_threads_{0};

    // 工作线程主循环
    void worker_loop(size_t thread_index);

    // 丢弃最低优先级任务
    bool drop_lowest_priority();

    // 绑定CPU核心
    void bind_cpu(size_t thread_index);

    // 动态扩缩容检查
    void check_dynamic_scale();

    // 获取微秒时间戳
    static uint64_t get_timestamp_us();

    // 设置线程名称
    static void set_thread_name(const std::string& name);
};

} // namespace longhun

#endif // LONGHUN_THREAD_POOL_H
