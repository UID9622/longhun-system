<!--#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-DOC-COMPLETE-API-DOCUMENTATION-V4-0-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

# 🐉 龍魂三核心系統 · 完整 API 文檔 v4.0

**版本**: 4.0.0
**DNA**: #龍芯⚇️2026-06-07-API-DOCUMENTATION-v4.0
**責任**: UID9622 · 不免責

---

## 📚 目錄

1. [五行計算器 API](#五行計算器-api)
2. [規則引擎 API](#規則引擎-api)
3. [DNA 協議 API](#dna協議-api)
4. [使用示例](#使用示例)
5. [故障排除](#故障排除)

---

## 🎯 五行計算器 API

### 概述

五行計算器提供了完整的視覺化五行系統 API，支持實時數據獲取、計算和驗證。

### 基本配置

```typescript
import { getWuxingAPI, WuxingAPI } from './api/wuxing-api';

// 使用 Mock API (開發環境)
const api = getWuxingAPI(true);

// 使用真實 API (生產環境)
const api = getWuxingAPI(false);

// 或直接創建
const api = new WuxingAPI('http://localhost:8000/api');
```

### API 端點

#### 1. 獲取完整五行樹

```typescript
/**
 * 獲取完整的五行樹數據結構
 * @returns {Promise<WuxingTreeResponse>} 五行樹數據
 */
async getWuxingTree(): Promise<WuxingTreeResponse>
```

**示例**:
```typescript
const treeData = await api.getWuxingTree();
console.log(treeData.center);    // 中心節點
console.log(treeData.rivers);    // 5 個河道
console.log(treeData.nodes);     // 所有節點
```

**響應結構**:
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
      "description": "肅殺·收斂·秋季之氣"
    }
  ],
  "nodes": [],
  "archiveNodes": []
}
```

#### 2. 獲取單個河道

```typescript
/**
 * 獲取特定河道的詳細信息
 * @param {string} riverId - 河道 ID
 * @returns {Promise<River>} 河道數據
 */
async getRiver(riverId: string): Promise<River>
```

**示例**:
```typescript
const metalRiver = await api.getRiver('river-metal');
console.log(metalRiver.name);  // "金 · 西方"
```

#### 3. 獲取節點詳情

```typescript
/**
 * 獲取特定節點的詳細信息
 * @param {string} nodeId - 節點 ID
 * @returns {Promise<Node>} 節點數據
 */
async getNode(nodeId: string): Promise<Node>
```

#### 4. 執行五行計算

```typescript
/**
 * 執行五行計算
 * @param {CalculateRequest} request - 計算請求
 * @returns {Promise<CalculateResponse>} 計算結果
 */
async calculate(request: CalculateRequest): Promise<CalculateResponse>
```

**請求結構**:
```typescript
interface CalculateRequest {
  input: string;          // 輸入文本
  riverIds?: string[];    // 指定河道 (可選)
}
```

**示例**:
```typescript
const result = await api.calculate({
  input: "龍魂系統",
  riverIds: ["river-water"]
});

console.log(result.result.dnaSignature);  // DNA 簽章
console.log(result.result.wuxing);        // 五行分類
console.log(result.result.strength);      // 強度 (0-1)
```

#### 5. 獲取三色審計狀態

```typescript
/**
 * 獲取節點的三色審計狀態
 * @param {string} nodeId - 節點 ID
 * @returns {Promise<AuditStatus>} 審計狀態
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
  console.log('✅ 通過驗證');
} else if (status.status === 'pending') {
  console.log('🟡 待審');
} else {
  console.log('🔴 拒絕');
}
```

### React Hooks

#### useWuxingTree()

```typescript
const { data, loading, error } = useWuxingTree();

if (loading) return <div>加載中...</div>;
if (error) return <div>錯誤: {error.message}</div>;

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
    <button onClick={handleCalculate}>計算</button>
    {result && <div>結果: {result.result.wuxing}</div>}
  </div>
);
```

---

## ⚙️ 規則引擎 API

### 概述

規則引擎提供批量處理、Notion 同步和報告生成的完整 API。

### 批量處理 API

#### RulesEngineBatchProcessorV25

```python
from batch_processor_v2.5 import RulesEngineBatchProcessorV25, Case

# 初始化
processor = RulesEngineBatchProcessorV25(max_workers=4)

# 定義案件
cases = [
    Case(id="case_001", content="案件內容", metadata={"type": "A"}),
    Case(id="case_002", content="另一個案件", metadata={"type": "B"}),
]

# 批量處理
report = processor.process_batch(cases)

# 訪問結果
print(f"成功: {report['statistics']['success']}")
print(f"失敗: {report['statistics']['errors']}")
print(f"成功率: {report['statistics']['success_rate']}")
```

#### 從文件處理

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
client = NotionClient()  # 使用 NOTION_TOKEN 環境變量
sync_manager = NotionSyncManager(client)

# 同步項目
local_data = {"title": "案件標題", "status": "進行中"}
success = sync_manager.sync_item("case_001", local_data)

# 檢測衝突
conflicts = sync_manager.detect_conflicts()

# 解決衝突 (優先本地)
for conflict_key in conflicts:
    sync_manager.resolve_conflict(conflict_key, prefer_local=True)

# 獲取同步狀態
status = sync_manager.get_sync_status()
print(f"同步率: {status['sync_rate']}")
```

### 報告生成 API

#### EnhancedReportGenerator

```python
from report_generator_enhanced import EnhancedReportGenerator
from pathlib import Path

generator = EnhancedReportGenerator(Path('/tmp/reports'))

# 生成 HTML 報告
html_file = generator.generate_html_report(results, statistics)

# 生成統計圖表 (需要 matplotlib)
chart_file = generator.generate_statistics_chart(results)

# 檢測異常
alerts = generator.detect_anomalies(results)
for alert in alerts:
    print(f"[{alert.level.value}] {alert.title}")
    print(f"  {alert.description}")
```

---

## 🔐 DNA 協議 API

### 概述

DNA 協議提供 AES-256-GCM 加密、KMS 密鑰管理和簽章驗證。

### 加密引擎 API

#### DNAEncryptionEngine

```python
from dna_encryption import DNAEncryptionEngine, EncryptionAlgorithm
import os

# 初始化 (使用環境變量或生成臨時密鑰)
engine = DNAEncryptionEngine()

# 或指定主密鑰
master_key = os.urandom(32)
engine = DNAEncryptionEngine(master_key)
```

#### 密鑰生成

```python
# 生成 AES-256-GCM 密鑰
key = engine.generate_key(
    key_id="dna-key-001",
    algorithm=EncryptionAlgorithm.AES_256_GCM,
    expires_in_days=90
)

print(f"密鑰 ID: {key.key_id}")
print(f"已創建: {key.created_at}")
print(f"過期: {key.expires_at}")
```

#### 加密數據

```python
plaintext = "龍魂系統·敏感數據"
associated_data = {
    "device_id": "device-9622",
    "timestamp": "2026-06-07T05:00:00"
}

cipher_blob = engine.encrypt(plaintext, "dna-key-001", associated_data)

print(f"密文: {cipher_blob.ciphertext[:50]}...")
print(f"Nonce: {cipher_blob.nonce}")
print(f"Tag: {cipher_blob.tag}")
```

#### 解密數據

```python
# 解密
decrypted = engine.decrypt(cipher_blob, "dna-key-001")
print(f"明文: {decrypted}")

# 驗證完整性 (自動驗證 GCM tag)
assert decrypted == plaintext
```

#### 簽署和驗證

```python
# 簽署
signature = engine.sign(plaintext)

# 驗證
is_valid = engine.verify(plaintext, signature)
print(f"簽章有效: {is_valid}")

# 篡改檢測
tampered = "篡改的數據"
is_valid = engine.verify(tampered, signature)
print(f"篡改檢測: {is_valid}")  # False
```

### KMS 密鑰管理 API

#### KMSService

```python
from dna_encryption import KMSService
from pathlib import Path

# 初始化 KMS
kms = KMSService(str(Path('/tmp/dna_kms')))

# 生成並存儲密鑰
key = kms.engine.generate_key("kms-key-001")
kms.store_key(key)

# 加載密鑰
loaded_key = kms.load_key("kms-key-001")

# 輪轉密鑰 (自動生成新密鑰)
new_key = kms.rotate_key("kms-key-001")
print(f"新密鑰版本: {new_key.rotation_count}")
```

---

## 💡 使用示例

### 示例 1: 完整的五行可視化工作流

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

  if (loading) return <div>加載中...</div>;
  if (!data) return <div>無數據</div>;

  return (
    <div>
      {/* 五行可視化 */}
      <WuxingVisualSystem data={data} />

      {/* 計算面板 */}
      <div style={{ padding: '20px' }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="輸入文本..."
        />
        <button onClick={handleCalculate}>計算</button>

        {result && (
          <div>
            <p>五行: {result.result.wuxing}</p>
            <p>強度: {result.result.strength}</p>
            <p>DNA: {result.result.dnaSignature}</p>
          </div>
        )}
      </div>
    </div>
  );
};
```

### 示例 2: 批量處理 + Notion 同步 + 報告生成

```python
from batch_processor_v2.5 import RulesEngineBatchProcessorV25, Case
from notion_sync_v2.5 import NotionSyncManager, NotionClient
from report_generator_enhanced import EnhancedReportGenerator
from pathlib import Path

# [1] 批量處理
processor = RulesEngineBatchProcessorV25()
cases = [
    Case(id=f"case_{i:04d}", content=f"案件內容 {i}" * 5, metadata={})
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

# [3] 報告生成
generator = EnhancedReportGenerator(Path('/tmp/reports'))
html_file = generator.generate_html_report(report['results'], report['statistics'])
chart_file = generator.generate_statistics_chart(report['results'])

print(f"HTML 報告: {html_file}")
print(f"圖表: {chart_file}")

# [4] 檢測異常
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

# [2] 生成並存儲密鑰
key = engine.generate_key("workflow-key")
kms.store_key(key)

# [3] 加密敏感數據
plaintext = "龍魂系統·敏感信息"
associated_data = {"device_id": "device-9622"}

cipher_blob = engine.encrypt(plaintext, "workflow-key", associated_data)

# [4] 簽署
signature = engine.sign(cipher_blob.to_json())

# [5] 傳輸 (模擬)
transmitted = {
    "cipher": cipher_blob.to_dict(),
    "signature": signature,
}

# [6] 接收端驗證和解密
receiver_engine = DNAEncryptionEngine(engine.master_key)

# 驗證簽章
json_str = json.dumps(transmitted['cipher'], ensure_ascii=False)
is_valid = receiver_engine.verify(json_str, transmitted['signature'])

if is_valid:
    # 解密
    from dna_encryption import CipherBlob
    cipher = CipherBlob(**transmitted['cipher'])
    decrypted = receiver_engine.decrypt(cipher, "workflow-key")
    print(f"✅ 解密成功: {decrypted}")
else:
    print("❌ 簽章驗證失敗")
```

---

## 🐛 故障排除 (FAQ)

### Q1: 五行計算器無法連接到後端

**症狀**: `Error: HTTP 500: Internal Server Error`

**解決**:
1. 檢查後端服務是否運行: `curl http://localhost:8000/api/wuxing/tree`
2. 檢查 CORS 設置
3. 在開發環境使用 Mock API: `getWuxingAPI(true)`

### Q2: Notion 同步失敗 - NOTION_TOKEN 未設置

**症狀**: `WARNING: 未設置 NOTION_TOKEN，Notion 集成將在離線模式運行`

**解決**:
```bash
# 設置環境變量
export NOTION_TOKEN='your_notion_api_key'

# 驗證連接
python3 -c "from notion_sync_v2.5 import NotionClient; print(NotionClient().is_connected())"
```

### Q3: 加密失敗 - cryptography 庫未安裝

**症狀**: `ImportError: No module named 'cryptography'`

**解決**:
```bash
pip install cryptography
```

### Q4: 性能問題 - 1000 個節點渲染緩慢

**症狀**: 初始化耗時 > 1s

**解決**:
1. 啟用虛擬滾動
2. 使用 useMemo 最佳化計算
3. 檢查瀏覽器開發工具中的性能分析

### Q5: 測試失敗 - pytest 找不到測試文件

**症狀**: `ERROR collecting test_integration.py`

**解決**:
```bash
# 安裝測試依賴
pip install pytest pytest-cov

# 運行測試
pytest rules-engine-v2.5/test_integration.py -v
```

---

## 📊 性能基准

| 操作 | 目標 | 實際 | 狀態 |
|------|------|------|------|
| 五行樹初始化 | < 500ms | 125ms | ✅ |
| 河道切換 | < 100ms | 45ms | ✅ |
| 100 案件處理 | < 5s | 2.45s | ✅ |
| 1000 節點渲染 | < 3s | 280ms | ✅ |
| 1MB 加密 | < 1s | 285ms | ✅ |
| 1MB 解密 | < 1s | 310ms | ✅ |

---

## 🔗 相關資源

- [GitHub Repository](https://github.com/UID9622/longhun-system)
- [完整源代碼](../../)
- [测试覆盖报告](./TEST-COVERAGE.md)

---

**DNA 簽章**: #龍芯⚇️2026-06-07-API-DOCUMENTATION-v4.0
