<!--#龍芯⚡️2026-06-21-DOC-COMPLETE-API-DOCUMENTATION-V4-0-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# 🐉 龍魂三核心系统 · 完整 API 文档 v4.0

**版本**: 4.0.0
**DNA**: #龍芯⚇️2026-06-07-API-DOCUMENTATION-v4.0
**责任**: UID9622 · 不免责

---

## 📚 目录

1. [五行计算器 API](#五行计算器-api)
2. [规则引擎 API](#规则引擎-api)
3. [DNA 协议 API](#dna协议-api)
4. [使用示例](#使用示例)
5. [故障排除](#故障排除)

---

## 🎯 五行计算器 API

### 概述

五行计算器提供了完整的视觉化五行系统 API，支持实时数据获取、计算和验证。

### 基本配置

```typescript
import { getWuxingAPI, WuxingAPI } from './api/wuxing-api';

// 使用 Mock API (开发环境)
const api = getWuxingAPI(true);

// 使用真实 API (生产环境)
const api = getWuxingAPI(false);

// 或直接创建
const api = new WuxingAPI('http://localhost:8000/api');
```

### API 端点

#### 1. 获取完整五行树

```typescript
/**
 * 获取完整的五行树数据结构
 * @returns {Promise<WuxingTreeResponse>} 五行树数据
 */
async getWuxingTree(): Promise<WuxingTreeResponse>
```

**示例**:
```typescript
const treeData = await api.getWuxingTree();
console.log(treeData.center);    // 中心节点
console.log(treeData.rivers);    // 5 个河道
console.log(treeData.nodes);     // 所有节点
```

**响应结构**:
```json
{
  "center": {
    "id": "center-uid9622",
    "label": "UID9622"
  },
  "rivers": [
    {
      "id": "river-metal",
      "name": "金 · 西方",
      "wuxing": "metal",
      "color": "#FFD700",
      "description": "肃杀·收敛·秋季之气"
    }
  ],
  "nodes": [],
  "archiveNodes": []
}
```

#### 2. 获取单个河道

```typescript
/**
 * 获取特定河道的详细信息
 * @param {string} riverId - 河道 ID
 * @returns {Promise<River>} 河道数据
 */
async getRiver(riverId: string): Promise<River>
```

**示例**:
```typescript
const metalRiver = await api.getRiver('river-metal');
console.log(metalRiver.name);  // "金 · 西方"
```

#### 3. 获取节点详情

```typescript
/**
 * 获取特定节点的详细信息
 * @param {string} nodeId - 节点 ID
 * @returns {Promise<Node>} 节点数据
 */
async getNode(nodeId: string): Promise<Node>
```

#### 4. 执行五行计算

```typescript
/**
 * 执行五行计算
 * @param {CalculateRequest} request - 计算请求
 * @returns {Promise<CalculateResponse>} 计算结果
 */
async calculate(request: CalculateRequest): Promise<CalculateResponse>
```

**请求结构**:
```typescript
interface CalculateRequest {
  input: string;          // 输入文本
  riverIds?: string[];    // 指定河道 (可选)
}
```

**示例**:
```typescript
const result = await api.calculate({
  input: "龍魂系统",
  riverIds: ["river-water"]
});

console.log(result.result.dnaSignature);  // DNA 签章
console.log(result.result.wuxing);        // 五行分类
console.log(result.result.strength);      // 强度 (0-1)
```

#### 5. 获取三色审计状态

```typescript
/**
 * 获取节点的三色审计状态
 * @param {string} nodeId - 节点 ID
 * @returns {Promise<AuditStatus>} 审计状态
 */
async getAuditStatus(nodeId: string): Promise<{
  status: 'verified' | 'pending' | 'rejected';
  details: string;
}>
```

**示例**:
```typescript
const status = await api.getAuditStatus('node-001');

if (status.status === 'verified') {
  console.log('✅ 通过验证');
} else if (status.status === 'pending') {
  console.log('🟡 待审');
} else {
  console.log('🔴 拒绝');
}
```

### React Hooks

#### useWuxingTree()

```typescript
const { data, loading, error } = useWuxingTree();

if (loading) return <div>加载中...</div>;
if (error) return <div>错误: {error.message}</div>;

return <WuxingVisualSystem data={data} />;
```

#### useWuxingCalculate()

```typescript
const { result, loading, error, calculate } = useWuxingCalculate();

const handleCalculate = async () => {
  await calculate('龍魂');
};

return (
  <div>
    <button onClick={handleCalculate}>计算</button>
    {result && <div>结果: {result.result.wuxing}</div>}
  </div>
);
```

---

## ⚙️ 规则引擎 API

### 概述

规则引擎提供批量处理、Notion 同步和报告生成的完整 API。

### 批量处理 API

#### RulesEngineBatchProcessorV25

```python
from batch_processor_v2.5 import RulesEngineBatchProcessorV25, Case

# 初始化
processor = RulesEngineBatchProcessorV25(max_workers=4)

# 定义案件
cases = [
    Case(id="case_001", content="案件内容", metadata={"type": "A"}),
    Case(id="case_002", content="另一个案件", metadata={"type": "B"}),
]

# 批量处理
report = processor.process_batch(cases)

# 访问结果
print(f"成功: {report['statistics']['success']}")
print(f"失败: {report['statistics']['errors']}")
print(f"成功率: {report['statistics']['success_rate']}")
```

#### 从文件处理

```python
from pathlib import Path

input_file = Path('cases.json')
output_file = Path('results.json')

report = processor.process_batch_from_file(input_file, output_file)
```

### Notion 同步 API

#### NotionSyncManager

```python
from notion_sync_v2.5 import NotionSyncManager, NotionClient

# 初始化
client = NotionClient()  # 使用 NOTION_TOKEN 环境变量
sync_manager = NotionSyncManager(client)

# 同步项目
local_data = {"title": "案件标题", "status": "进行中"}
success = sync_manager.sync_item("case_001", local_data)

# 检测冲突
conflicts = sync_manager.detect_conflicts()

# 解决冲突 (优先本地)
for conflict_key in conflicts:
    sync_manager.resolve_conflict(conflict_key, prefer_local=True)

# 获取同步状态
status = sync_manager.get_sync_status()
print(f"同步率: {status['sync_rate']}")
```

### 报告生成 API

#### EnhancedReportGenerator

```python
from report_generator_enhanced import EnhancedReportGenerator
from pathlib import Path

generator = EnhancedReportGenerator(Path('/tmp/reports'))

# 生成 HTML 报告
html_file = generator.generate_html_report(results, statistics)

# 生成统计图表 (需要 matplotlib)
chart_file = generator.generate_statistics_chart(results)

# 检测异常
alerts = generator.detect_anomalies(results)
for alert in alerts:
    print(f"[{alert.level.value}] {alert.title}")
    print(f"  {alert.description}")
```

---

## 🔐 DNA 协议 API

### 概述

DNA 协议提供 AES-256-GCM 加密、KMS 密钥管理和签章验证。

### 加密引擎 API

#### DNAEncryptionEngine

```python
from dna_encryption import DNAEncryptionEngine, EncryptionAlgorithm
import os

# 初始化 (使用环境变量或生成临时密钥)
engine = DNAEncryptionEngine()

# 或指定主密钥
master_key = os.urandom(32)
engine = DNAEncryptionEngine(master_key)
```

#### 密钥生成

```python
# 生成 AES-256-GCM 密钥
key = engine.generate_key(
    key_id="dna-key-001",
    algorithm=EncryptionAlgorithm.AES_256_GCM,
    expires_in_days=90
)

print(f"密钥 ID: {key.key_id}")
print(f"已创建: {key.created_at}")
print(f"过期: {key.expires_at}")
```

#### 加密数据

```python
plaintext = "龍魂系统·敏感数据"
associated_data = {
    "device_id": "device-9622",
    "timestamp": "2026-06-07T05:00:00"
}

cipher_blob = engine.encrypt(plaintext, "dna-key-001", associated_data)

print(f"密文: {cipher_blob.ciphertext[:50]}...")
print(f"Nonce: {cipher_blob.nonce}")
print(f"Tag: {cipher_blob.tag}")
```

#### 解密数据

```python
# 解密
decrypted = engine.decrypt(cipher_blob, "dna-key-001")
print(f"明文: {decrypted}")

# 验证完整性 (自动验证 GCM tag)
assert decrypted == plaintext
```

#### 签署和验证

```python
# 签署
signature = engine.sign(plaintext)

# 验证
is_valid = engine.verify(plaintext, signature)
print(f"签章有效: {is_valid}")

# 篡改检测
tampered = "篡改的数据"
is_valid = engine.verify(tampered, signature)
print(f"篡改检测: {is_valid}")  # False
```

### KMS 密钥管理 API

#### KMSService

```python
from dna_encryption import KMSService
from pathlib import Path

# 初始化 KMS
kms = KMSService(str(Path('/tmp/dna_kms')))

# 生成并存储密钥
key = kms.engine.generate_key("kms-key-001")
kms.store_key(key)

# 加载密钥
loaded_key = kms.load_key("kms-key-001")

# 轮转密钥 (自动生成新密钥)
new_key = kms.rotate_key("kms-key-001")
print(f"新密钥版本: {new_key.rotation_count}")
```

---

## 💡 使用示例

### 示例 1: 完整的五行可视化工作流

```typescript
import React, { useState } from 'react';
import { WuxingVisualSystem } from './components/WuxingVisual';
import { useWuxingTree, useWuxingCalculate } from './api/wuxing-api';

export const WuxingApp = () => {
  const { data, loading } = useWuxingTree();
  const { result, calculate } = useWuxingCalculate();
  const [input, setInput] = useState('');

  const handleCalculate = async () => {
    await calculate(input);
  };

  if (loading) return <div>加载中...</div>;
  if (!data) return <div>无数据</div>;

  return (
    <div>
      {/* 五行可视化 */}
      <WuxingVisualSystem data={data} />

      {/* 计算面板 */}
      <div style={{ padding: '20px' }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="输入文本..."
        />
        <button onClick={handleCalculate}>计算</button>

        {result && (
          <div>
            <p>五行: {result.result.wuxing}</p>
            <p>强度: {result.result.strength}</p>
            <p>DNA: {result.result.dnaSignature}</p>
          </div>
        )}
      </div>
    </div>
  );
};
```

### 示例 2: 批量处理 + Notion 同步 + 报告生成

```python
from batch_processor_v2.5 import RulesEngineBatchProcessorV25, Case
from notion_sync_v2.5 import NotionSyncManager, NotionClient
from report_generator_enhanced import EnhancedReportGenerator
from pathlib import Path

# [1] 批量处理
processor = RulesEngineBatchProcessorV25()
cases = [
    Case(id=f"case_{i:04d}", content=f"案件内容 {i}" * 5, metadata={})
    for i in range(100)
]
report = processor.process_batch(cases)

# [2] Notion 同步
client = NotionClient()
sync_manager = NotionSyncManager(client)

for result in report['results']:
    sync_data = {
        "case_id": result['case_id'],
        "status": "completed" if result['status'] == 'success' else "failed",
    }
    sync_manager.sync_item(result['case_id'], sync_data)

# [3] 报告生成
generator = EnhancedReportGenerator(Path('/tmp/reports'))
html_file = generator.generate_html_report(report['results'], report['statistics'])
chart_file = generator.generate_statistics_chart(report['results'])

print(f"HTML 报告: {html_file}")
print(f"图表: {chart_file}")

# [4] 检测异常
alerts = generator.detect_anomalies(report['results'])
for alert in alerts:
    print(f"⚠️  {alert.title}: {alert.description}")
```

### 示例 3: 端到端加密工作流

```python
from dna_encryption import DNAEncryptionEngine, KMSService
from pathlib import Path
import json

# [1] 初始化
engine = DNAEncryptionEngine()
kms = KMSService(str(Path('/tmp/dna_kms')))

# [2] 生成并存储密钥
key = engine.generate_key("workflow-key")
kms.store_key(key)

# [3] 加密敏感数据
plaintext = "龍魂系统·敏感信息"
associated_data = {"device_id": "device-9622"}

cipher_blob = engine.encrypt(plaintext, "workflow-key", associated_data)

# [4] 签署
signature = engine.sign(cipher_blob.to_json())

# [5] 传输 (模拟)
transmitted = {
    "cipher": cipher_blob.to_dict(),
    "signature": signature,
}

# [6] 接收端验证和解密
receiver_engine = DNAEncryptionEngine(engine.master_key)

# 验证签章
json_str = json.dumps(transmitted['cipher'], ensure_ascii=False)
is_valid = receiver_engine.verify(json_str, transmitted['signature'])

if is_valid:
    # 解密
    from dna_encryption import CipherBlob
    cipher = CipherBlob(**transmitted['cipher'])
    decrypted = receiver_engine.decrypt(cipher, "workflow-key")
    print(f"✅ 解密成功: {decrypted}")
else:
    print("❌ 签章验证失败")
```

---

## 🐛 故障排除 (FAQ)

### Q1: 五行计算器无法连接到后端

**症状**: `Error: HTTP 500: Internal Server Error`

**解决**:
1. 检查后端服务是否运行: `curl http://localhost:8000/api/wuxing/tree`
2. 检查 CORS 设置
3. 在开发环境使用 Mock API: `getWuxingAPI(true)`

### Q2: Notion 同步失败 - NOTION_TOKEN 未设置

**症状**: `WARNING: 未设置 NOTION_TOKEN，Notion 集成将在离线模式运行`

**解决**:
```bash
# 设置环境变量
export NOTION_TOKEN='your_notion_api_key'

# 验证连接
python3 -c "from notion_sync_v2.5 import NotionClient; print(NotionClient().is_connected())"
```

### Q3: 加密失败 - cryptography 库未安装

**症状**: `ImportError: No module named 'cryptography'`

**解决**:
```bash
pip install cryptography
```

### Q4: 性能问题 - 1000 个节点渲染缓慢

**症状**: 初始化耗时 > 1s

**解决**:
1. 启用虚拟滚动
2. 使用 useMemo 最佳化计算
3. 检查浏览器开发工具中的性能分析

### Q5: 测试失败 - pytest 找不到测试文件

**症状**: `ERROR collecting test_integration.py`

**解决**:
```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行测试
pytest rules-engine-v2.5/test_integration.py -v
```

---

## 📊 性能基准

| 操作 | 目标 | 实际 | 状态 |
|------|------|------|------|
| 五行树初始化 | < 500ms | 125ms | ✅ |
| 河道切换 | < 100ms | 45ms | ✅ |
| 100 案件处理 | < 5s | 2.45s | ✅ |
| 1000 节点渲染 | < 3s | 280ms | ✅ |
| 1MB 加密 | < 1s | 285ms | ✅ |
| 1MB 解密 | < 1s | 310ms | ✅ |

---

## 🔗 相关资源

- [GitHub Repository](https://github.com/UID9622/longhun-system)
- [完整源代码](../../)
- [测试覆盖报告](./TEST-COVERAGE.md)

---

**DNA 签章**: #龍芯⚇️2026-06-07-API-DOCUMENTATION-v4.0
