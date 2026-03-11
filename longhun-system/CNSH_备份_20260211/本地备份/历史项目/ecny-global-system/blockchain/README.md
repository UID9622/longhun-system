# 🔗 区块链配置

## 🏗️ Hyperledger Fabric 网络配置

### 网络架构

```
┌─────────────────────────────────────────────────────────┐
│                   数字人民币跨境清算网络                   │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   央行节点   │  │  商业银行节点 │  │  企业用户节点 │     │
│  │  (中国央行)  │  │ (中行/工行)  │  │ (阿里巴巴等) │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│           │               │               │            │
│  ┌─────────────────────────────────────────────────┐    │
│  │              Fabric区块链网络                    │    │
│  │  Orderer服务 │ Peer节点 │ 链码容器 │ 证书管理      │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### 智能合约（链码）

**文件名：`chaincode/ecny_chaincode.go`**

```go
// 数字人民币跨境清算智能合约
package main

import (
    "encoding/json"
    "fmt"
    "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// eCNYChaincode 实现跨境清算功能
type eCNYChaincode struct {
    contractapi.Contract
}

// Transaction 交易记录结构
type Transaction struct {
    ID           string  `json:"id"`
    FromCountry  string  `json:"from_country"`
    ToCountry    string  `json:"to_country"`
    Amount       float64 `json:"amount"`
    Currency     string  `json:"currency"`  // 固定为"e-CNY"
    Timestamp    string  `json:"timestamp"`
    Status       string  `json:"status"`    // PENDING, COMPLETED, FAILED
    RiskLevel    string  `json:"risk_level"` // GREEN, YELLOW, RED
}

// InitLedger 初始化账本
func (cc *eCNYChaincode) InitLedger(ctx contractapi.TransactionContextInterface) error {
    // 创建初始交易记录
    transactions := []Transaction{
        {
            ID: "tx001",
            FromCountry: "中国",
            ToCountry: "巴基斯坦",
            Amount: 1000000.00,
            Currency: "e-CNY",
            Timestamp: "2025-01-01T10:00:00Z",
            Status: "COMPLETED",
            RiskLevel: "GREEN",
        },
    }

    for _, tx := range transactions {
        txJSON, err := json.Marshal(tx)
        if err != nil {
            return err
        }
        err = ctx.GetStub().PutState(tx.ID, txJSON)
        if err != nil {
            return fmt.Errorf("failed to put to world state: %v", err)
        }
    }
    return nil
}

// CreateTransaction 创建新交易
func (cc *eCNYChaincode) CreateTransaction(
    ctx contractapi.TransactionContextInterface,
    id string,
    fromCountry string,
    toCountry string,
    amount float64,
) error {
    
    // 检查交易是否已存在
    exists, err := cc.TransactionExists(ctx, id)
    if err != nil {
        return err
    }
    if exists {
        return fmt.Errorf("transaction %s already exists", id)
    }

    // 风险评估
    riskLevel := cc.calculateRiskLevel(fromCountry, toCountry, amount)
    
    transaction := Transaction{
        ID:          id,
        FromCountry: fromCountry,
        ToCountry:   toCountry,
        Amount:      amount,
        Currency:    "e-CNY",
        Timestamp:   ctx.GetStub().GetTxTimestamp().String(),
        Status:      "PENDING",
        RiskLevel:   riskLevel,
    }

    txJSON, err := json.Marshal(transaction)
    if err != nil {
        return err
    }

    return ctx.GetStub().PutState(id, txJSON)
}

// 风险评估算法
func (cc *eCNYChaincode) calculateRiskLevel(from, to string, amount float64) string {
    // 基于一带一路国家风险评估
    friendlyCountries := []string{"巴基斯坦", "老挝", "柬埔寨", "泰国", "哈萨克斯坦"}
    
    for _, country := range friendlyCountries {
        if to == country {
            return "GREEN"
        }
    }
    
    if amount > 1000000 {
        return "YELLOW"
    }
    
    return "RED"
}

// 查询交易
func (cc *eCNYChaincode) QueryTransaction(
    ctx contractapi.TransactionContextInterface,
    id string,
) (*Transaction, error) {
    
    txJSON, err := ctx.GetStub().GetState(id)
    if err != nil {
        return nil, fmt.Errorf("failed to read from world state: %v", err)
    }
    if txJSON == nil {
        return nil, fmt.Errorf("transaction %s does not exist", id)
    }

    var transaction Transaction
    err = json.Unmarshal(txJSON, &transaction)
    if err != nil {
        return nil, err
    }

    return &transaction, nil
}

// 检查交易是否存在
func (cc *eCNYChaincode) TransactionExists(
    ctx contractapi.TransactionContextInterface,
    id string,
) (bool, error) {
    
    txJSON, err := ctx.GetStub().GetState(id)
    if err != nil {
        return false, fmt.Errorf("failed to read from world state: %v", err)
    }
    return txJSON != nil, nil
}

func main() {
    chaincode, err := contractapi.NewChaincode(&eCNYChaincode{})
    if err != nil {
        fmt.Printf("Error creating eCNY chaincode: %s", err.Error())
        return
    }

    if err := chaincode.Start(); err != nil {
        fmt.Printf("Error starting eCNY chaincode: %s", err.Error())
    }
}
```

### Docker Compose配置

**文件名：`docker-compose-fabric.yml`**

```yaml
version: '2'

services:
  # Orderer服务
  orderer.example.com:
    container_name: orderer.example.com
    image: hyperledger/fabric-orderer:2.5
    environment:
      - ORDERER_GENERAL_LISTENADDRESS=0.0.0.0
      - ORDERER_GENERAL_LISTENPORT=7050
      - ORDERER_GENERAL_LOCALMSPID=OrdererMSP
      - ORDERER_GENERAL_LOCALMSPDIR=/var/hyperledger/orderer/msp
      - ORDERER_GENERAL_TLS_ENABLED=true
      - ORDERER_GENERAL_TLS_PRIVATEKEY=/var/hyperledger/orderer/tls/server.key
      - ORDERER_GENERAL_TLS_CERTIFICATE=/var/hyperledger/orderer/tls/server.crt
      - ORDERER_GENERAL_TLS_ROOTCAS=[/var/hyperledger/orderer/tls/ca.crt]
    ports:
      - 7050:7050
    networks:
      - ecny-fabric

  # Peer节点
  peer0.pbc.gov.cn:
    container_name: peer0.pbc.gov.cn
    image: hyperledger/fabric-peer:2.5
    environment:
      - CORE_PEER_ID=peer0.pbc.gov.cn
      - CORE_PEER_ADDRESS=peer0.pbc.gov.cn:7051
      - CORE_PEER_LISTENADDRESS=0.0.0.0:7051
      - CORE_PEER_CHAINCODEADDRESS=peer0.pbc.gov.cn:7052
      - CORE_PEER_CHAINCODELISTENADDRESS=0.0.0.0:7052
      - CORE_PEER_GOSSIP_BOOTSTRAP=peer0.pbc.gov.cn:7051
      - CORE_PEER_GOSSIP_EXTERNALENDPOINT=peer0.pbc.gov.cn:7051
      - CORE_PEER_LOCALMSPID=PBCMSP
    ports:
      - 7051:7051
    depends_on:
      - orderer.example.com
    networks:
      - ecny-fabric

  # 链码容器
  chaincode-ecny:
    container_name: chaincode-ecny
    build:
      context: ./chaincode
      dockerfile: Dockerfile
    environment:
      - CORE_CHAINCODE_ID_NAME=ecnycc:1.0
      - CORE_PEER_ADDRESS=peer0.pbc.gov.cn:7052
    networks:
      - ecny-fabric

networks:
  ecny-fabric:
    driver: bridge
```

### 启动区块链网络

```bash
# 启动Fabric网络
docker-compose -f docker-compose-fabric.yml up -d

# 安装链码
docker exec -it peer0.pbc.gov.cn peer chaincode install -n ecnycc -v 1.0 -p chaincode

# 实例化链码
docker exec -it peer0.pbc.gov.cn peer chaincode instantiate -o orderer.example.com:7050 -C mychannel -n ecnycc -v 1.0 -c '{"Args":["InitLedger"]}'
```

## 🔐 安全特性

### 三色审计机制

- **🟢 绿色**：一带一路友好国家，低风险交易
- **🟡 黄色**：中等风险，需要额外审核
- **🔴 红色**：高风险，需人工干预

### 智能风控

- **交易额度监控**
- **国家风险评估**
- **实时异常检测**
- **自动告警机制**

---

**DNA确认码**：`#CNSH-BLOCKCHAIN-CONFIG-COMPLETE`

---
🔐 数字主权签名防护系统
📅 签名时间: 2025-12-18 03:24:10
🧬 DNA追溯码: #CNSH-SIGNATURE-6b283f80-20251218032410
🌐 签名人: 龙魂文化加密系统
💬 方言确认: 四川话确认：莫得问题，内容真实可靠
⚡ 卦象防护: 屯卦：云雷屯，君子以经纶
📜 内容哈希: bc87ab5890e72520
⚠️ 警告: 未经授权修改将触发DNA追溯系统
