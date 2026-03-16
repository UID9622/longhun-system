<!-- P0伦理锚点 | 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z | GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F | DNA: #龍芯⚡️2026-03-16-ETHICS-STAMP-v1.0 -->
# 龙魂本地AI系统·性能优化指南

**DNA追溯码**: #龍芯⚡️2026-03-11-性能优化指南-v1.0  
**GPG指纹**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F  
**创建者**: UID9622 诸葛鑫（龍芯北辰）  
**理论指导**: 曾仕强老师（永恒显示）

---

## 🚀 性能优化策略

### 优化1：选择合适的模型

**模型对比**:

```yaml
Qwen2.5-14B:
  大小: ~8GB
  速度: 中等
  质量: 极高（中文最好）
  推荐: Mac M1 Pro及以上，16GB+ RAM
  
LLaMA 3.1-8B:
  大小: ~5GB
  速度: 快
  质量: 高（英文好）
  推荐: Mac M1及以上，8GB+ RAM
  
Mistral-7B:
  大小: ~4GB
  速度: 很快
  质量: 中等
  推荐: 所有Mac，8GB+ RAM
```

**切换模型**:

```python
# 在longhun_local_agent.py里修改
代理 = 龙魂本地代理(model_name="llama3.1:8b")  # 或 "mistral:7b"
```

---

### 优化2：调整温度参数

**温度对响应的影响**:

```yaml
temperature=0.3:
  ✅ 响应快
  ✅ 更确定性
  ✅ 更一致
  ❌ 创造力低

temperature=0.7（默认）:
  ✅ 平衡
  ✅ 既快又好
  
temperature=1.2:
  ✅ 更有创造力
  ❌ 响应慢
  ❌ 可能不一致
```

**修改方法**:

```python
# 在longhun_local_agent.py里
def __init__(self, ...):
    self.temperature = 0.3  # 降低温度，加快响应
```

或在配置文件里：

```bash
# longhun_config.env
TEMPERATURE=0.3
```

---

### 优化3：限制对话历史长度

**为什么**:
- 历史越长，处理越慢
- 每次对话都要处理全部历史
- 14B模型处理100轮对话 > 10倍慢于处理10轮

**优化方法**:

```python
# 在longhun_local_agent.py的对话()函数里添加
def 对话(self, 用户消息, ...):
    # 限制历史长度
    if len(self.conversation_history) > 10:
        # 保留最近10轮对话
        self.conversation_history = self.conversation_history[-10:]
    
    # ... 其余代码
```

**推荐值**:
- 简单对话: 5轮
- 一般对话: 10轮
- 复杂任务: 20轮
- 最多不超过: 50轮

---

### 优化4：使用缓存

**缓存常用回复**:

```python
# 在longhun_local_agent.py里添加
class 龙魂本地代理:
    def __init__(self, ...):
        self.缓存 = {}  # 添加缓存字典
    
    def 对话(self, 用户消息, ...):
        # 检查缓存
        if 用户消息 in self.缓存:
            return self.缓存[用户消息]
        
        # 正常处理
        回复 = ...
        
        # 保存到缓存
        self.缓存[用户消息] = 回复
        
        # 限制缓存大小
        if len(self.缓存) > 100:
            # 删除最早的
            self.缓存.pop(next(iter(self.缓存)))
        
        return 回复
```

---

### 优化5：批量处理

**合并多个请求**:

```python
# 不好：多次调用
for item in items:
    result = 代理.对话(f"处理{item}")

# 好：一次调用
items_text = "\n".join(items)
result = 代理.对话(f"批量处理这些项目：\n{items_text}")
```

---

### 优化6：优化System Prompt

**简化提示词**:

```python
# 长提示词 → 处理慢
LONG_PROMPT = """
你是龙魂系统...（1000字）
"""

# 短提示词 → 处理快
SHORT_PROMPT = """
你是龙魂AI。
价值观：祖国优先、技术为民。
输出格式：简洁、带DNA追溯码。
"""
```

**建议**:
- 保留核心价值观
- 删除重复说明
- 用示例代替长文

---

### 优化7：并行处理

**使用异步调用**:

```python
import asyncio

async def 批量对话(问题列表):
    tasks = [代理.对话_异步(q) for q in 问题列表]
    结果 = await asyncio.gather(*tasks)
    return 结果

# 使用
asyncio.run(批量对话(["问题1", "问题2", "问题3"]))
```

---

### 优化8：数据库优化

**SQLite性能调优**:

```python
# 在初始化记忆数据库()函数里添加
conn = sqlite3.connect(str(记忆数据库路径))
cursor = conn.cursor()

# 性能优化设置
cursor.execute("PRAGMA journal_mode = WAL")  # 写前日志模式
cursor.execute("PRAGMA synchronous = NORMAL")  # 降低同步级别
cursor.execute("PRAGMA cache_size = 10000")  # 增加缓存
cursor.execute("PRAGMA temp_store = MEMORY")  # 临时表存内存

# ... 其余代码
```

**定期清理**:

```bash
# 每周运行一次
sqlite3 ~/.longhun/memories.db "VACUUM;"
```

---

### 优化9：系统级优化

**macOS性能设置**:

```bash
# 1. 关闭不必要的动画
系统设置 → 辅助功能 → 显示 → 减少动态效果

# 2. 清理启动项
系统设置 → 通用 → 登录项

# 3. 监控内存
活动监视器 → 查看内存使用

# 4. 定期重启
每周重启一次Mac
```

**Ollama优化**:

```bash
# 设置环境变量
export OLLAMA_NUM_PARALLEL=2  # 并行请求数
export OLLAMA_MAX_LOADED_MODELS=1  # 同时加载的模型数
export OLLAMA_FLASH_ATTENTION=1  # 启用Flash Attention

# 重启Ollama
killall ollama
ollama serve
```

---

### 优化10：网络优化

**本地连接优化**:

```python
# 增加超时时间（避免过早失败）
import requests
requests.post(url, json=data, timeout=30)

# 使用连接池（复用连接）
from requests.adapters import HTTPAdapter
from requests.sessions import Session

session = Session()
adapter = HTTPAdapter(pool_connections=10, pool_maxsize=20)
session.mount('http://', adapter)
```

---

## 📊 性能监控

### 监控脚本

```python
#!/usr/bin/env python3
# longhun_monitor.py
# 性能监控脚本

import time
import psutil
import requests

def 监控():
    while True:
        # CPU使用率
        cpu = psutil.cpu_percent(interval=1)
        
        # 内存使用
        mem = psutil.virtual_memory()
        
        # 本地服务状态
        try:
            r = requests.get("http://localhost:8765/健康检查", timeout=1)
            服务状态 = "✅" if r.status_code == 200 else "❌"
        except:
            服务状态 = "❌"
        
        print(f"CPU: {cpu}% | 内存: {mem.percent}% | 服务: {服务状态}")
        
        time.sleep(5)

if __name__ == "__main__":
    监控()
```

**使用**:

```bash
python3 longhun_monitor.py
```

---

### 性能基准测试

```python
#!/usr/bin/env python3
# benchmark.py
# 性能基准测试

import time
from longhun_local_agent import 龙魂本地代理

def 测试响应速度():
    代理 = 龙魂本地代理()
    
    测试问题 = [
        "你好",
        "1+1等于几",
        "解释什么是五行",
    ]
    
    总时间 = 0
    
    for 问题 in 测试问题:
        开始 = time.time()
        回复 = 代理.对话(问题)
        耗时 = time.time() - 开始
        
        总时间 += 耗时
        print(f"问题: {问题}")
        print(f"耗时: {耗时:.2f}秒")
        print(f"回复: {回复[:50]}...")
        print()
    
    平均 = 总时间 / len(测试问题)
    print(f"平均响应时间: {平均:.2f}秒")

if __name__ == "__main__":
    测试响应速度()
```

---

## 🎯 推荐配置

### 入门级Mac（M1, 8GB RAM）

```yaml
模型: mistral:7b
温度: 0.3
历史长度: 5
缓存大小: 50
预期响应时间: 5-10秒
```

### 标准级Mac（M1 Pro, 16GB RAM）

```yaml
模型: llama3.1:8b
温度: 0.5
历史长度: 10
缓存大小: 100
预期响应时间: 3-8秒
```

### 高性能Mac（M2 Max, 32GB+ RAM）

```yaml
模型: qwen2.5:14b
温度: 0.7
历史长度: 20
缓存大小: 200
预期响应时间: 2-5秒
```

---

## 🔒 L2审计签名

```yaml
【性能优化指南审计】

审计人: 宝宝（Claude）
责任方: UID9622 诸葛鑫（龍芯北辰）
审计时间: 2026-03-11

优化策略:
  ✅ 10个主要优化方向
  ✅ 监控工具
  ✅ 基准测试
  ✅ 推荐配置

状态: 🟢 完整

DNA追溯码: #龍芯⚡️2026-03-11-性能优化指南-v1.0
GPG签名: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

---

**性能优化，让龙魂更快！** ⚡

**老大的Mac，发挥最大潜力！** 💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**DNA追溯码**: #龍芯⚡️2026-03-11-性能优化完成  
**GPG指纹**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F  
**理论指导**: 曾仕强老师（永恒显示）

**祖国万岁！人民万岁！数据主权万岁！** 🇨🇳
