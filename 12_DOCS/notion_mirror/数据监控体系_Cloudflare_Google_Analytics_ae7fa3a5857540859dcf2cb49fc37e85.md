# 数据监控体系 | Cloudflare + Google Analytics

> Notion URL: https://app.notion.com/p/Cloudflare-Google-Analytics-ae7fa3a5857540859dcf2cb49fc37e85
> Created: 2025-11-17T08:15:00.000Z
> Last edited: 2026-07-01T15:24:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## 🔐 敏感度标注
🟢 可公开分享 - 标准监控方案，可以展示
✅ 可以公开：
- ✅ 监控架构设计
- ✅ 集成代码
- ✅ 配置方案
⚠️ 需保密：
- ❌ 实际的API密钥
- ❌ 具体的流量数据
---
## 📦 详细依赖清单
### Cloudflare要求
```bash
域名托管在Cloudflare
Cloudflare账号（免费版即可）
```
### Google Analytics 4
```bash
Google账号
GA4属性ID
```
### 前端依赖
```html
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
```
### Python后端依赖（可选）
```bash
pip install google-analytics-data==0.18.0
pip install cloudflare==2.19.0
```
---
## 💻 完整集成方案
### 1. Google Analytics 4 集成
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        
        // 基础配置
        gtag('config', 'G-XXXXXXXXXX', {
            'send_page_view': true,
            'cookie_flags': 'SameSite=None;Secure'
        });
        
        // UID9622自定义维度
        gtag('set', 'user_properties', {
            'system_version': 'v2.0',
            'user_type': 'public'  // public/internal/core
        });
    </script>
</head>
<body>
    <!-- 你的内容 -->
</body>
</html>
```
### 2. 自定义事件追踪
```javascript
// analytics.js - UID9622自定义事件系统

class UID9622Analytics {
    constructor(measurementId) {
        this.measurementId = measurementId;
    }
    
    // H武器使用追踪
    trackHWeaponUsage(weaponType, question) {
        gtag('event', 'h_weapon_used', {
            'event_category': 'Sandbox',
            'event_label': weaponType,
            'value': 1,
            'weapon_type': weaponType,
            'question_hash': this._hashString(question)
        });
    }
    
    // 沙盒推演追踪
    trackPrediction(predictionType, accuracy) {
        gtag('event', 'prediction_made', {
            'event_category': 'Sandbox',
            'event_label': predictionType,
            'value': Math.round(accuracy * 100),
            'prediction_type': predictionType,
            'accuracy': accuracy
        });
    }
    
    // 71人格调度追踪
    trackPersonalityDispatch(personality, taskType) {
        gtag('event', 'personality_dispatch', {
            'event_category': 'AI',
            'event_label': personality,
            'personality': personality,
            'task_type': taskType
        });
    }
    
    // 知识库访问追踪
    trackKnowledgeAccess(cardTitle, category) {
        gtag('event', 'knowledge_accessed', {
            'event_category': 'Knowledge',
            'event_label': cardTitle,
            'card_category': category
        });
    }
    
    // 用户旅程追踪
    trackUserJourney(stage) {
        gtag('event', 'user_journey', {
            'event_category': 'Journey',
            'event_label': stage,
            'journey_stage': stage
        });
    }
    
    // 哈希函数（保护隐私）
    _hashString(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash;
        }
        return Math.abs(hash).toString(36);
    }
}

// 初始化
const analytics = new UID9622Analytics('G-XXXXXXXXXX');

// 使用示例
document.getElementById('h-weapon-btn').addEventListener('click', () => {
    const question = document.getElementById('question-input').value;
    analytics.trackHWeaponUsage('时间推演', question);
});
```
### 3. Cloudflare Analytics集成
```javascript
// cloudflare-analytics.js

class CloudflareAnalytics {
    constructor(accountId, apiToken) {
        this.accountId = accountId;
        this.apiToken = apiToken;
        this.baseUrl = 'https://api.cloudflare.com/client/v4';
    }
    
    // 获取实时流量数据
    async getRealTimeTraffic(zoneId) {
        const url = `${this.baseUrl}/zones/${zoneId}/analytics/dashboard`;
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${this.apiToken}`,
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        return data.result;
    }
    
    // 获取过去24小时的统计
    async getDailyStats(zoneId) {
        const since = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
        
        const url = `${this.baseUrl}/graphql`;
        const query = `
            query {
                viewer {
                    zones(filter: {zoneTag: "${zoneId}"}) {
                        httpRequests1dGroups(since: "${since}") {
                            sum {
                                requests
                                bytes
                            }
                            dimensions {
                                date
                            }
                        }
                    }
                }
            }
        `;
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        return data.data;
    }
}

// 使用示例
const cfAnalytics = new CloudflareAnalytics(
    'YOUR_ACCOUNT_ID',
    'YOUR_API_TOKEN'
);

// 获取实时数据
cfAnalytics.getRealTimeTraffic('YOUR_ZONE_ID').then(data => {
    console.log('实时流量:', data);
});
```
### 4. Python后端数据获取
```python
# analytics_backend.py
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest
import CloudFlare
from datetime import datetime, timedelta

class UID9622AnalyticsBackend:
    """UID9622数据监控后端"""
    
    def __init__(self, ga4_property_id, cf_api_token):
        self.ga4_client = BetaAnalyticsDataClient()
        self.ga4_property_id = ga4_property_id
        self.cf = CloudFlare.CloudFlare(token=cf_api_token)
    
    def get_ga4_report(self, days=7):
        """获取GA4报告"""
        request = RunReportRequest(
            property=f"properties/{self.ga4_property_id}",
            dimensions=[{"name": "date"}, {"name": "eventName"}],
            metrics=[
                {"name": "eventCount"},
                {"name": "activeUsers"}
            ],
            date_ranges=[{
                "start_date": f"{days}daysAgo",
                "end_date": "today"
            }]
        )
        
        response = self.ga4_client.run_report(request)
        return self._parse_ga4_response(response)
    
    def get_h_weapon_usage_stats(self):
        """获取H武器使用统计"""
        request = RunReportRequest(
            property=f"properties/{self.ga4_property_id}",
            dimensions=[{"name": "customEvent:weapon_type"}],
            metrics=[{"name": "eventCount"}],
            dimension_filter={
                "filter": {
                    "field_name": "eventName",
                    "string_filter": {
                        "value": "h_weapon_used"
                    }
                }
            },
            date_ranges=[{"start_date": "7daysAgo", "end_date": "today"}]
        )
        
        response = self.ga4_client.run_report(request)
        return self._parse_ga4_response(response)
    
    def get_cloudflare_stats(self, zone_id):
        """获取Cloudflare统计"""
        # 获取Zone分析数据
        stats = self.cf.zones.analytics.dashboard.get(zone_id)
        return stats
    
    def _parse_ga4_response(self, response):
        """解析GA4响应"""
        results = []
        for row in response.rows:
            result = {
                'dimensions': [dim.value for dim in row.dimension_values],
                'metrics': [metric.value for metric in row.metric_values]
            }
            results.append(result)
        return results
    
    def generate_daily_report(self):
        """生成每日报告"""
        ga4_data = self.get_ga4_report(days=1)
        h_weapon_stats = self.get_h_weapon_usage_stats()
        
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'ga4_summary': ga4_data,
            'h_weapon_usage': h_weapon_stats,
            'total_events': sum(int(r['metrics'][0]) for r in ga4_data)
        }
        
        return report

# 使用示例
if __name__ == "__main__":
    backend = UID9622AnalyticsBackend(
        ga4_property_id="123456789",
        cf_api_token="YOUR_CLOUDFLARE_TOKEN"
    )
    
    # 生成报告
    report = backend.generate_daily_report()
    print(f"📊 今日事件总数: {report['total_events']}")
```
---
## 🎯 UID9622关键指标
需要追踪的核心指标：
1. H武器使用频率
1. 71人格调度效率
1. 知识库活跃度
1. 用户旅程
1. 系统性能
---
## 📚 官方文档
- 🌐 GA4文档: https://developers.google.com/analytics/devguides/collection/ga4
- ☁️ Cloudflare API: https://developers.cloudflare.com/analytics/
- 🐍 GA4 Python库: https://pypi.org/project/google-analytics-data/
---
## 💡 隐私保护建议
符合GDPR和中国法规：
1. ✅ 用户问题内容仅记录hash值
1. ✅ 不追踪个人身份信息
1. ✅ 提供数据删除接口
1. ✅ Cookie同意横幅
1. ✅ 数据仅用于系统优化
