# 龍魂海外节点 v1.0 · 合规全球连接

> DNA: #龍芯⚡️丙午·丙申·壬申·亥时·䷕贲-OVERSEAS-NODE-v1.0-9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> License: MulanPSL v2（工程层）

## 一、这是什么

龍魂在全球的**合规节点**。同一个龍魂内核，在哪个国家部署就守哪个国家的法律——
**一国一微调**的落地形态：

| 部署地 | 用谁的能力 | 服务谁 | 法律 |
|:---|:---|:---|:---|
| 中国（鲲鹏/本地） | 混元 · DeepSeek · 文心 | 中国用户 | 中国法律 |
| 海外 VPS（本节点） | OpenAI · Claude · Gemini | 海外用户 / longhun888.com 生态 | 当地法律 |

**铁律（P0）**：
- 海外节点**只服务海外业务/海外用户**，不提供境内↔境外的翻墙中转
- 不内置、不教任何绕过网络管理措施的工具（中国法律为准绳）
- API 密钥只存节点 `.env`（D2 机密），不入 git、不上传国内
- 龍魂浏览器本身零限制（原生 Chromium）；能否访问某站点取决于各节点当地网络与法律

## 二、架构

```
海外 VPS (Ubuntu/Debian)
├── lh-ai-gateway (:8788)   OpenAI-compatible AI 网关
│     └─ 海外业务把 OPENAI_BASE_URL 指向它 → OpenAI / Claude / Gemini 按模型自动路由
├── browser-headless        龍魂浏览器 headless（海外站点渲染/采集，复用鲲鹏 run.sh 模式）
└── check.sh                健康检查（curl /health + 可选 Bark 告警）
```

## 三、部署（海外 VPS 上一条命令）

```bash
# 0. 前置：一台海外 VPS（推荐 香港/新加坡/东京，2C2G 即可，月费 $5~20）
# 1. 拉部署包到海外 VPS
scp -r deploy/overseas root@<海外IP>:/opt/longhun-overseas/
# 2. 填密钥（OpenAI/Claude/Gemini 任选）
cp /opt/longhun-overseas/ai-gateway/.env.example /opt/longhun-overseas/ai-gateway/.env
vi /opt/longhun-overseas/ai-gateway/.env
# 3. 一键部署
bash /opt/longhun-overseas/setup.sh
# 4. 验证
curl http://127.0.0.1:8788/health
```

## 四、AI 网关用法（海外业务侧）

```bash
# OpenAI SDK 指向海外节点
export OPENAI_BASE_URL=https://<海外IP>:8788/v1
export OPENAI_API_KEY=<LONGHUN_GATEWAY_KEY>   # 网关自己的钥匙，不是上游 key

# 模型自动路由：模型名含 gemini → Gemini · 含 claude → Claude · 其他 → OpenAI
curl -X POST https://<海外IP>:8788/v1/chat/completions \
  -H "Authorization: Bearer $LONGHUN_GATEWAY_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"你好"}]}'
```

## 五、合规边界（必读）

1. 本节点部署在海外、服务海外，**合法合规**；部署在境内请用国内服务，勿逆向
2. 密钥管理：`.env` 权限 0600，只存海外节点；GPG 私钥永不入海外节点
3. 所有服务走 systemd 托管 + 日志留痕（append-only），符合龍魂审计观
4. 一国一微调 = 各国守各国法 = 不威胁任何国家主权

## 六、后续路线

- [ ] 老大购买/提供海外 VPS → 本部署包一键起 → 接 longhun888.com 生态
- [ ] 海外节点纳入 `lh overseas` 管理子命令（status/health/log）
- [ ] 海外节点接 Bark/飞书告警（复用 deploy/scripts/health_check.sh 模式）
