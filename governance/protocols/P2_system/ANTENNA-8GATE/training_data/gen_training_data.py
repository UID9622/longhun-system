# DNA: #龍芯⚡️丙午·乙未·乙丑·井-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ============================================================
# 龍魂 · ANTENNA-8GATE 训练数据生成器
# DNA：#龍芯⚡️丙午·乙未·丙申·酉时·☲离-TRAIN-DATA-GEN-v1.0-a1b2c3d4
# 创建者：诸葛鑫（UID9622）· 协议：CC BY-NC-SA 4.0
# 
# 目的：跑蚁触网收集路由模式 → JSONL训练数据 → MLX微调longhun
# ============================================================

import sys, os, json, time, random, hashlib
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'core'))
from antenna_mesh_v2 import AntennaMeshV2, Bagua

# 多种查询模板 → 归入八卦分类
QUERY_TEMPLATES = {
    Bagua.乾: [  # 天·主控/决策/状态
        "系统当前运行状态如何？",
        "查看所有服务的健康状态",
        "当前系统的CPU和内存使用情况",
        "今天系统有没有异常告警？",
        "列出所有活跃的进程",
        "系统启动以来的运行时长",
        "当前有多少用户在线？",
        "查看集群节点状态",
    ],
    Bagua.离: [  # 火·计算/代码/核心
        "用Python实现一个二分查找算法",
        "写一个快速排序函数",
        "帮我优化这段代码的性能",
        "设计一个缓存系统架构",
        "实现一个简单的神经网络前向传播",
        "写一个多线程任务队列",
        "计算两个向量的余弦相似度",
        "实现LRU缓存淘汰策略",
        "用递归实现斐波那契数列",
        "写一个正则表达式匹配引擎",
        "实现AES加密解密函数",
        "设计RESTful API的速率限制",
    ],
    Bagua.艮: [  # 山·边界/安全
        "检测以下代码的安全漏洞",
        "配置防火墙规则防止DDoS攻击",
        "审计用户权限是否合理",
        "检查数据库是否存在SQL注入风险",
        "扫描服务器开放的端口",
        "验证JWT令牌的有效性",
        "实现XSS防护过滤器",
        "检查是否存在硬编码的密钥",
        "审计日志是否记录了敏感操作",
        "设置访问控制列表",
    ],
    Bagua.坎: [  # 水·冷却/调度
        "设计一个任务优先级调度方案",
        "实现一个定时任务执行器",
        "配置负载均衡策略",
        "处理高并发请求的降级方案",
        "写一个熔断器的实现",
        "管理消息队列的消费速率",
        "实现延迟任务调度",
        "处理服务间的超时重试",
    ],
    Bagua.兑: [  # 泽·交互/输出/API
        "设计一个用户友好的REST API",
        "写一份接口文档",
        "优化前端页面的加载速度",
        "生成一份系统周报",
        "格式化JSON输出",
        "设计WebSocket实时推送方案",
        "实现文件下载断点续传",
        "编写API的Swagger文档",
    ],
    Bagua.震: [  # 雷·突发/告警
        "服务器CPU使用率超过90%触发告警",
        "数据库连接池耗尽紧急处理",
        "磁盘空间不足的紧急清理方案",
        "服务突然宕机的排查步骤",
        "内存泄漏的紧急修复方案",
        "大量请求超时的应急响应",
        "SSL证书即将过期的告警通知",
    ],
    Bagua.巽: [  # 风·传输/网络
        "优化微服务之间的gRPC通信",
        "实现MQTT消息订阅发布",
        "配置Nginx反向代理",
        "优化数据库查询的网络传输",
        "设计CDN缓存策略",
        "实现服务发现与注册",
        "配置跨域资源共享CORS",
        "优化TCP长连接的心跳机制",
    ],
    Bagua.坤: [  # 地·存储/持久
        "设计一个高可用的数据库架构",
        "实现数据分片与复制策略",
        "制定数据备份与恢复方案",
        "优化MySQL查询索引",
        "设计Redis缓存预热方案",
        "实现数据归档策略",
        "配置分布式文件存储",
        "实现数据一致性校验",
    ],
}


def collect_routing_data(output_path: str = "training_data.jsonl", max_samples: int = 500):
    """
    跑蚁触网收集路由数据，生成MLX训练用的JSONL
    """
    print(f"[生成器] 创建 512节点蚁触网...")
    mesh = AntennaMeshV2(nodes_per_bagua=64, dim=4096, memory_per_node=128)
    
    # 展开所有查询
    all_queries = []
    for bagua, queries in QUERY_TEMPLATES.items():
        for q in queries:
            all_queries.append((q, bagua))
    
    random.shuffle(all_queries)
    total = min(len(all_queries), max_samples)
    print(f"[生成器] 共 {total} 条查询，开始收集路由数据...\n")
    
    samples = []
    bagua_stats = {b.name: 0 for b in Bagua}
    
    for i, (query, target_bagua) in enumerate(all_queries[:total]):
        emb, stats = mesh.inference(query, target_bagua)
        
        # 收集激活节点分布
        activated_by_bagua = {b.name: 0 for b in Bagua}
        for node_id, node in mesh.nodes.items():
            if node.state == '激活':
                activated_by_bagua[node.bagua.name] += 1
        
        bagua_stats[target_bagua.name] += 1
        
        # 训练样本：指令→八卦路由
        prompt = (
            f"你是龍魂系统的八卦路由器。根据用户查询，返回应路由到哪个八卦卦象。\n\n"
            f"八卦职能：\n"
            f"乾(天) - 主控决策/状态查询/健康检查\n"
            f"坤(地) - 存储持久/数据备份/数据库\n"
            f"震(雷) - 突发告警/紧急处理/异常\n"
            f"巽(风) - 网络传输/CDN/代理/通信\n"
            f"坎(水) - 任务调度/降级/熔断/队列\n"
            f"离(火) - 代码计算/算法/优化/核心\n"
            f"艮(山) - 安全边界/漏洞检测/权限\n"
            f"兑(泽) - 交互输出/API设计/文档\n\n"
            f"用户查询：{query}\n\n"
            f"路由结果："
        )
        
        response = (
            f"卦象：{target_bagua.name}({target_bagua.name}) | "
            f"跳过率：{stats['skip_rate']*100:.1f}% | "
            f"激活节点：{stats['nodes_active']}/{stats['nodes_checked']} | "
            f"能耗：{stats['total_energy_j']:.2e}J"
        )
        
        sample = {
            "instruction": prompt,
            "input": "",
            "output": response,
            "meta": {
                "bagua": target_bagua.name,
                "skip_rate": round(stats['skip_rate'] * 100, 1),
                "nodes_active": stats['nodes_active'],
                "nodes_total": stats['nodes_checked'],
                "energy_j": stats['total_energy_j'],
                "dna": f"#龍芯⚡️丙午·乙未·丙申·ANTENNA-TRAIN-{hashlib.sha256(query.encode()).hexdigest()[:8]}",
            }
        }
        samples.append(sample)
        
        if (i + 1) % 50 == 0:
            print(f"  进度: {i+1}/{total} | 缓存命中: {mesh.encoder.get_stats()['hit_rate']*100:.1f}%")
    
    # 写入JSONL
    outpath = os.path.join(BASE, "training_data", output_path)
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, 'w', encoding='utf-8') as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + '\n')
    
    # 汇总
    print(f"\n{'='*60}")
    print(f"训练数据生成完毕")
    print(f"{'='*60}")
    print(f"总样本: {len(samples)}")
    print(f"路径: {outpath}")
    print(f"\n八卦分布:")
    total_s = sum(bagua_stats.values())
    for bname, cnt in sorted(bagua_stats.items(), key=lambda x: -x[1]):
        bar = '█' * (cnt * 40 // max(bagua_stats.values()))
        print(f"  {bname}: {cnt:>3} ({cnt/total_s*100:.0f}%) {bar}")
    
    # 质量统计
    avg_skip = sum(s['meta']['skip_rate'] for s in samples) / len(samples)
    print(f"\n质量指标:")
    print(f"  平均跳过率: {avg_skip:.1f}%")
    print(f"  编码缓存命中率: {mesh.encoder.get_stats()['hit_rate']*100:.1f}%")
    
    return samples


if __name__ == "__main__":
    collect_routing_data()
