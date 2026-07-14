// 龍魂 · Native 线程池实现
// DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-THREAD-POOL-IMPL-v1.0

#include "thread_pool.h"

namespace longhun {

// ============================================================================
// 构造与析构
// ============================================================================

LongHunThreadPool::LongHunThreadPool(const ThreadPoolConfig& config)
    : config_(config) {

    // 修正配置
    if (config_.min_threads < 1) config_.min_threads = 1;
    if (config_.max_threads < config_.min_threads) config_.max_threads = config_.min_threads;
    if (config_.queue_capacity < 10) config_.queue_capacity = 10;

    // 创建最小线程数
    for (size_t i = 0; i < config_.min_threads; ++i) {
        workers_.emplace_back(&LongHunThreadPool::worker_loop, this, i);
    }
}

LongHunThreadPool::~LongHunThreadPool() {
    shutdown();
}

// ============================================================================
// 工作线程主循环
// ============================================================================

void LongHunThreadPool::worker_loop(size_t thread_index) {
    set_thread_name("LH-Worker-" + std::to_string(thread_index));

    // CPU绑核
    if (config_.cpu_affinity_mask != 0) {
        bind_cpu(thread_index);
    }

    // NUMA绑核
    if (config_.bind_numa_node) {
        // 简化：实际用 numa_run_on_node()
    }

    while (true) {
        Task task;

        {
            std::unique_lock<std::mutex> lock(queue_mutex_);

            condition_.wait(lock, [this] {
                return stop_.load() || !task_queue_.empty();
            });

            if (stop_.load() && task_queue_.empty()) {
                return;
            }

            if (!task_queue_.empty()) {
                // 移动任务出队
                task = std::move(const_cast<Task&>(task_queue_.top()));
                task_queue_.pop();
            }
        }

        // 执行任务
        if (task.func) {
            active_threads_.fetch_add(1);

            uint64_t start_time = get_timestamp_us();

            try {
                task.func();
            } catch (const std::exception& e) {
                // 异常捕获
                // 实际：写入 hilog
            } catch (...) {
                // 未知异常
            }

            uint64_t exec_time = get_timestamp_us() - start_time;

            total_processed_.fetch_add(1);
            total_exec_time_us_.fetch_add(exec_time);
            active_threads_.fetch_sub(1);

            // 慢任务告警
            if (exec_time > config_.slow_task_threshold_us) {
                slow_tasks_.fetch_add(1);
            }
        }
    }
}

// ============================================================================
// CPU亲和性绑定
// ============================================================================

void LongHunThreadPool::bind_cpu(size_t thread_index) {
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);

    size_t cpu_count = std::thread::hardware_concurrency();
    if (cpu_count == 0) cpu_count = 4;

    size_t target_cpu = thread_index % cpu_count;

    if (config_.cpu_affinity_mask & (1ULL << target_cpu)) {
        CPU_SET(target_cpu, &cpuset);
        int ret = pthread_setaffinity_np(pthread_self(), sizeof(cpuset), &cpuset);
        (void)ret; // 忽略失败
    }
}

// ============================================================================
// 丢弃最低优先级任务
// ============================================================================

bool LongHunThreadPool::drop_lowest_priority() {
    // 拷贝队列找最低优先级
    std::vector<Task> temp;
    temp.reserve(task_queue_.size());

    Task lowest;
    bool found = false;

    while (!task_queue_.empty()) {
        Task current = std::move(const_cast<Task&>(task_queue_.top()));
        task_queue_.pop();

        if (!found || current.priority > lowest.priority) {
            if (found) temp.push_back(std::move(lowest));
            lowest = std::move(current);
            found = true;
        } else {
            temp.push_back(std::move(current));
        }
    }

    // 恢复队列（排除最低优先级）
    for (auto& t : temp) {
        task_queue_.push(std::move(t));
    }

    // 只丢弃 BACKGROUND 任务
    if (found && lowest.priority == TaskPriority::BACKGROUND) {
        total_dropped_.fetch_add(1);
        return true;
    }

    // 被移除的是非BACKGROUND，放回去
    if (found) {
        task_queue_.push(std::move(lowest));
    }

    return false;
}

// ============================================================================
// 动态扩缩容
// ============================================================================

void LongHunThreadPool::check_dynamic_scale() {
    size_t queue_size = task_queue_.size();
    size_t current_workers = workers_.size();

    // 扩容：队列积压超过2x线程数
    if (queue_size > current_workers * 2 && current_workers < config_.max_threads) {
        size_t new_index = current_workers;
        workers_.emplace_back(&LongHunThreadPool::worker_loop, this, new_index);
    }

    // 缩容：队列空且线程超min
    if (queue_size == 0 && current_workers > config_.min_threads) {
        // 简化：不主动缩容，保持稳定
    }
}

// ============================================================================
// 状态查询
// ============================================================================

size_t LongHunThreadPool::get_queue_size() const {
    std::lock_guard<std::mutex> lock(queue_mutex_);
    return task_queue_.size();
}

size_t LongHunThreadPool::get_active_threads() const {
    return active_threads_.load();
}

uint64_t LongHunThreadPool::get_total_processed() const {
    return total_processed_.load();
}

uint64_t LongHunThreadPool::get_total_submitted() const {
    return total_submitted_.load();
}

uint64_t LongHunThreadPool::get_total_dropped() const {
    return total_dropped_.load();
}

ThreadPoolConfig LongHunThreadPool::get_config() const {
    return config_;
}

PoolStats LongHunThreadPool::get_stats() const {
    PoolStats stats;
    stats.queue_size      = get_queue_size();
    stats.active_threads  = active_threads_.load();
    stats.idle_threads    = workers_.size() - stats.active_threads;
    stats.total_processed = total_processed_.load();
    stats.total_submitted = total_submitted_.load();
    stats.total_dropped   = total_dropped_.load();
    stats.slow_tasks      = slow_tasks_.load();

    uint64_t processed = total_processed_.load();
    uint64_t total_time = total_exec_time_us_.load();
    stats.avg_exec_time_us = processed > 0 ? total_time / processed : 0;

    // CPU利用率估算
    stats.cpu_utilization = (stats.active_threads > 0)
        ? static_cast<double>(stats.active_threads) / workers_.size()
        : 0.0;

    return stats;
}

// ============================================================================
// 动态调整
// ============================================================================

void LongHunThreadPool::resize(size_t new_min, size_t new_max) {
    config_.min_threads = new_min;
    config_.max_threads = new_max;
}

void LongHunThreadPool::set_cpu_affinity(size_t mask) {
    config_.cpu_affinity_mask = mask;
}

void LongHunThreadPool::set_slow_task_threshold(size_t threshold_us) {
    config_.slow_task_threshold_us = threshold_us;
}

// ============================================================================
// 控制
// ============================================================================

void LongHunThreadPool::wait_for_all() {
    while (true) {
        {
            std::lock_guard<std::mutex> lock(queue_mutex_);
            if (task_queue_.empty() && active_threads_.load() == 0) {
                return;
            }
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

void LongHunThreadPool::shutdown() {
    stop_.store(true);
    condition_.notify_all();

    for (auto& worker : workers_) {
        if (worker.joinable()) {
            worker.join();
        }
    }

    workers_.clear();
}

// ============================================================================
// 工具函数
// ============================================================================

uint64_t LongHunThreadPool::get_timestamp_us() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return static_cast<uint64_t>(ts.tv_sec) * 1000000 + ts.tv_nsec / 1000;
}

void LongHunThreadPool::set_thread_name(const std::string& name) {
    pthread_setname_np(pthread_self(), name.c_str());
}

} // namespace longhun
