# SPEC.md — 龍魂 · 流量拓扑一键部署工程包

## 目标
产出 `/mnt/agents/output/longhun-flow-deploy/` —— 拷到华为云鲲鹏服务器（Ubuntu 22.04+/Debian，arm64/x86_64 通用）后 `./deploy.sh` 一条命令完成全部部署，可回滚、可验证。

## 目录结构（焊死）
```
longhun-flow-deploy/
├── deploy.sh                  # 一键部署（幂等，含前置检查+备份+回滚触发）
├── rollback.sh                # 一键回滚
├── requirements.txt           # fastapi, uvicorn, requests
├── conf/
│   ├── nginx/nginx.conf       # 完整主配置（非占位符）
│   ├── nginx/sites-available/longhun   # 完整站点配置
│   ├── sysctl/99-longhun.conf
│   └── limits/99-longhun.conf
├── systemd/
│   ├── longhun-api.service
│   ├── longhun-collab.service
│   └── longhun-bridge.service
├── 08_BIN/
│   ├── lh_api_gateway.py      # :8970 FastAPI
│   ├── lh_collab_hub.py       # :19622 FastAPI
│   ├── lh_chat_bridge.py      # :18799 FastAPI + Ollama SSE 代理
│   ├── lh_audit.py            # 史官+耻辱墙 公共模块（哈希链）
│   └── lh_health_check.sh
├── var_www/index.html         # SPA 占位首页（含主权头展示）
└── README_DEPLOY.md           # 部署手册（流程图/验证清单/QA/故障排查）
```

## 接口契约
- `GET /health` 三个服务必须返回 `{"status":"ok","service":"<name>","dna":"<生成器DNA>"}`
- 所有 API 请求无 `X-Dragon-DNA` 头 → 403 `{"error":"P0协议要求: 缺少DNA追溯码"}`
- 审计：每个请求写 `/opt/longhun/audit/audit.jsonl`，含 prev_hash 哈希链
- DNA 一律由 `bin/lh_dna_generator.py` 算法生成，禁止手写干支
- nginx 站点配置禁用在 location 里写 `if + add_header` 组合（P0头校验改用 `map` + `error_page` 或后端强制校验）

## 关键修正点（相对稿件）
1. deploy.sh heredoc 必须写入完整配置，严禁占位符
2. 三服务全部 systemd 托管（Restart=always），禁止 nohup 裸奔
3. 创建 /var/log/longhun、/opt/longhun/{shared/{collab,handoffs,collaboration},audit}，目录权限 www-data
4. collab/handoffs 目录浏览 autoindex 改为仅内网或加注释说明风险
5. 监控告警规则：stub_status 不暴露 nginx_up 等 metric，改用 nginx-prometheus-exporter 并标注🟡未实测
6. SSL：certbot 首次签发流程写清楚；沙箱无法验证标🟡
7. nginx 配置必须过 `nginx -t`（沙箱实测）

## 验收标准
- [ ] `nginx -t` 沙箱通过（用测试路径替换证书路径后）
- [ ] 三 Python 服务沙箱逐个启动，curl /health 返回 200 + dna 字段
- [ ] 无 DNA 头请求 /api/* 返回 403
- [ ] 审计 jsonl 落盘且哈希链可校验
- [ ] deploy.sh `bash -n` 语法核验 + shellcheck（如可用）
- [ ] 所有文档头部 DNA 由生成器输出
