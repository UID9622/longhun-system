// 🐉 龍魂主权技术栈·API 网关 v2.0
// 新增：DNA追溯头 + 健康检查 + 按量计费接入
// DNA: #龍芯⚡️2026-08-31-API-GATEWAY-V2.0-UID9622
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 协议: MulanPSL v2（工程实现层）
package main

import (
    "bytes"
    "crypto/rand"
    "encoding/hex"
    "encoding/json"
    "fmt"
    "github.com/gin-gonic/gin"
    "log"
    "net/http"
    "net/http/httputil"
    "net/url"
    "os"
    "sync"
    "time"
)

// ──────────────────────────────────────────
// 令牌桶限流（每IP 100 req/min）
// ──────────────────────────────────────────
type TokenBucket struct {
    tokens    int
    lastReset time.Time
}
type Limiter struct {
    mu     sync.Mutex
    tokens map[string]*TokenBucket
}

func (l *Limiter) Allow(ip string) bool {
    l.mu.Lock()
    defer l.mu.Unlock()
    b, ok := l.tokens[ip]
    now := time.Now()
    if !ok || now.Sub(b.lastReset) > time.Minute {
        l.tokens[ip] = &TokenBucket{tokens: 100, lastReset: now}
        return true
    }
    if b.tokens > 0 {
        b.tokens--
        return true
    }
    return false
}

var limiter = &Limiter{tokens: make(map[string]*TokenBucket)}

// ──────────────────────────────────────────
// DNA 追溯码生成
// ──────────────────────────────────────────
func generateDNA(module string) string {
    now := time.Now().Format("2006-01-02")
    return fmt.Sprintf("#龍芯⚡️%s-%s-V1.0-UID9622", now, module)
}

// ──────────────────────────────────────────
// 计量上报（调用 pricing 服务）
// ──────────────────────────────────────────
var meterURL = os.Getenv("METER_URL") // http://localhost:8897

func recordUsage(accountID string) {
    if meterURL == "" {
        return
    }
    payload, _ := json.Marshal(map[string]interface{}{
        "account_id":    accountID,
        "resource_type": "api_call",
        "quantity":      1,
        "tier":          "personal",
    })
    http.Post(meterURL+"/meter/record", "application/json",
              bytes.NewBuffer(payload))
}

// ──────────────────────────────────────────
// 主程序
// ──────────────────────────────────────────
func main() {
    r := gin.Default()

    backend := os.Getenv("BACKEND_URL")
    if backend == "" {
        backend = "http://localhost:8080"
    }
    target, _ := url.Parse(backend)
    proxy := httputil.NewSingleHostReverseProxy(target)

    apiKey := os.Getenv("GATEWAY_API_KEY")
    if apiKey == "" {
        b := make([]byte, 16)
        rand.Read(b)
        apiKey = hex.EncodeToString(b)
        log.Printf("🔑 Generated API Key: %s", apiKey)
        os.Setenv("GATEWAY_API_KEY", apiKey)
    }

    // ── 健康检查（Kubernetes Liveness Probe 标准）
    r.GET("/health", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "status":  "healthy",
            "service": "longhun-api-gateway",
            "version": "2.0",
            "dna":     generateDNA("GATEWAY-HEALTH"),
            "tricolor": "🟢",
        })
    })

    // ── 就绪检查（Kubernetes Readiness Probe）
    r.GET("/ready", func(c *gin.Context) {
        c.JSON(200, gin.H{"ready": true})
    })

    // ── 主路由
    r.Any("/*path", func(c *gin.Context) {
        if c.Request.URL.Path == "/health" || c.Request.URL.Path == "/ready" {
            return
        }

        // 鉴权
        if c.GetHeader("X-API-Key") != apiKey {
            c.JSON(401, gin.H{
                "error":   "invalid api key",
                "dna":     generateDNA("GATEWAY-AUTH-FAIL"),
                "tricolor": "🔴",
            })
            return
        }

        // 限流
        if !limiter.Allow(c.ClientIP()) {
            c.JSON(429, gin.H{
                "error":   "rate limit exceeded (100 req/min per IP)",
                "dna":     generateDNA("GATEWAY-RATELIMIT"),
                "tricolor": "🟡",
                "retry_after": "60s",
            })
            return
        }

        // 提取账户ID（用于计量）
        accountID := c.GetHeader("X-Account-ID")
        if accountID == "" {
            accountID = "anonymous"
        }

        // 异步记录使用量（不阻塞主流程）
        go recordUsage(accountID)

        // 附加 DNA 追溯头
        c.Header("X-LH-DNA", generateDNA("GATEWAY-PROXY"))
        c.Header("X-LH-UID", "UID9622")
        c.Header("X-LH-Timestamp", time.Now().Format(time.RFC3339))

        // 反向代理
        proxy.ServeHTTP(c.Writer, c.Request)
    })

    log.Printf("🐉 龍魂 API Gateway v2.0 · 监听 :9000")
    log.Printf("🧬 DNA: %s", generateDNA("GATEWAY-START"))
    log.Fatal(r.Run(":9000"))
}
